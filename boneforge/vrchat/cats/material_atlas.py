"""BoneForge VRChat — Material Atlas Combiner.

Combines multiple materials across meshes into texture atlases, reducing
draw calls and improving VRChat avatar performance rank.

Three-zone layout:
  Zone 1 — Status Dashboard (always visible, auto-updates)
  Zone 2 — Atlas Groups (UIList, auto-classified by render type)
  Zone 3 — Advanced Options (collapsed)

Unanimous additions from design review:
  R — Post-bake authority sentence (rank before/after, outcome language)
  S — Permanent transparency separation note beneath group list
  Q — Accept / Revert binary after bake (replaces fragile undo)
  P — Cancellable per-material bake progress with status bar

Category: VRChat Cats Tools.
"""

import json
import logging
import os
import time
from array import array

import bpy
import bmesh
from bpy.props import (
    BoolProperty, CollectionProperty, EnumProperty,
    FloatProperty, IntProperty, StringProperty,
)

from boneforge.i18n import T
from bpy.types import Operator, Panel, PropertyGroup, UIList

from boneforge.core import active_armature
from boneforge.vrchat.cats import pipeline
from boneforge.vrchat.cats.uv_tools import (
    apply_atlas_uv_method,
    atlas_uv_method_items,
    get_uv_method_label,
    method_uses_seed,
    summarize_atlas_uv_result,
)
from boneforge.vrchat.cats.material_atlas_quality import (
    CHANNEL_PACK_CONVENTION,
    PACKING_PRESETS,
    ROLE_ALPHA,
    ROLE_ALBEDO,
    ROLE_AO,
    ROLE_EMISSION,
    ROLE_METALLIC,
    ROLE_NORMAL,
    ROLE_ROUGHNESS,
    ROLE_UNKNOWN,
    MaterialSource,
    TextureSource,
    build_channel_pack_plan,
    build_multipass_output_plan,
    detect_texture_role,
    diagnose_material,
    diagnose_texture,
    duplicate_texture_key,
    find_duplicate_texture_groups,
    find_shared_material_groups,
    format_quality_debug_report,
    packing_preset_settings,
    resolve_size_preset,
    role_color_space,
    role_label,
)

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────
# Constants — VRChat performance thresholds (mirrors rank.py)
# ─────────────────────────────────────────────────────────────────

_RANK_THRESHOLDS = {"Excellent": 4, "Good": 8, "Medium": 16, "Poor": 32}
_RANK_ORDER = ["Excellent", "Good", "Medium", "Poor"]
_RENDER_TYPES = ["Opaque", "Alpha Clip", "Alpha Blend", "Emissive"]
_OUTPUT_MATERIAL_TYPE_ITEMS = [
    ("AUTO", "Auto (Group)", "Use each atlas group's detected render type"),
    ("OPAQUE", "Opaque", "Force generated atlas materials to opaque"),
    ("ALPHA_CLIP", "Alpha Clip", "Force generated atlas materials to alpha clip"),
    ("ALPHA_BLEND", "Alpha Blend", "Force generated atlas materials to alpha blend"),
    ("EMISSIVE", "Emissive", "Force generated atlas materials to emissive output"),
]
_OUTPUT_MATERIAL_TYPE_MAP = {
    "OPAQUE": "Opaque",
    "ALPHA_CLIP": "Alpha Clip",
    "ALPHA_BLEND": "Alpha Blend",
    "EMISSIVE": "Emissive",
}
_OUTPUT_MATERIAL_TYPE_LABELS = {
    item_id: label
    for item_id, label, _description in _OUTPUT_MATERIAL_TYPE_ITEMS
}
_OUTPUT_SURFACE_SHADER_ITEMS = [
    ("AUTO", "Auto (Principled)", "Use the generated Principled BSDF surface"),
    ("PRINCIPLED", "Principled BSDF", "Connect a Principled BSDF to the material surface"),
    ("DIFFUSE", "Diffuse BSDF", "Connect a Diffuse BSDF to the material surface"),
    ("EMISSION", "Emission Shader", "Connect an Emission shader to the material surface"),
    ("TRANSPARENT", "Transparent BSDF", "Connect a Transparent BSDF to the material surface"),
]
_OUTPUT_SURFACE_SHADER_LABELS = {
    item_id: label
    for item_id, label, _description in _OUTPUT_SURFACE_SHADER_ITEMS
}

# VRAM cost per atlas (bytes): width * height * 4 channels * 1.33 mip factor
_VRAM_MIP_FACTOR = 1.33

_BACKUP_COLLECTION_PREFIX = "BF_Atlas_Backup_"

_TEXTURE_ROLE_ITEMS = [
    (ROLE_ALBEDO, role_label(ROLE_ALBEDO), "Base color / diffuse source"),
    (ROLE_NORMAL, role_label(ROLE_NORMAL), "Normal map source"),
    (ROLE_EMISSION, role_label(ROLE_EMISSION), "Emission source"),
    (ROLE_METALLIC, role_label(ROLE_METALLIC), "Metallic utility map"),
    (ROLE_ROUGHNESS, role_label(ROLE_ROUGHNESS), "Roughness utility map"),
    (ROLE_AO, role_label(ROLE_AO), "Ambient occlusion utility map"),
    (ROLE_UNKNOWN, role_label(ROLE_UNKNOWN), "Unclassified texture source"),
]

_SIZE_PRESET_ITEMS = [
    ("SOURCE", "Source", "Use the detected source texture dimensions"),
    ("512", "512", "Use 512 x 512"),
    ("1024", "1024", "Use 1024 x 1024"),
    ("2048", "2048", "Use 2048 x 2048"),
    ("4096", "4096", "Use 4096 x 4096"),
    ("CUSTOM", "Custom", "Use the material row width and height"),
]

_PACKING_PRESET_ITEMS = [
    (key, spec["label"], f"Margin {spec['uv_margin']}, padding {spec['padding_pixels']}px")
    for key, spec in PACKING_PRESETS.items()
]

_EXTRA_BAKE_PASSES = {
    ROLE_NORMAL: {"type": "NORMAL", "suffix": "_normal", "colorspace": "Non-Color"},
    ROLE_EMISSION: {"type": "EMIT", "suffix": "_emission", "colorspace": "sRGB"},
    ROLE_ROUGHNESS: {"type": "ROUGHNESS", "suffix": "_roughness", "colorspace": "Non-Color"},
}


# ─────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────

def _get_rank(mat_count: int) -> str:
    for rank in _RANK_ORDER:
        if mat_count <= _RANK_THRESHOLDS[rank]:
            return rank
    return "Very Poor"


def _vram_mb(resolution: str) -> float:
    res = int(resolution)
    return round((res * res * 4 * _VRAM_MIP_FACTOR) / (1024 * 1024), 1)


def _classify_material(mat) -> str:
    """Return render-type class for a material."""
    if mat is None:
        return "Opaque"

    blend = getattr(mat, "blend_method", "OPAQUE")
    if blend == "BLEND":
        return "Alpha Blend"
    if blend == "CLIP":
        return "Alpha Clip"

    # Detect emissive via Principled BSDF emission inputs
    if mat.use_nodes and mat.node_tree:
        for node in mat.node_tree.nodes:
            if node.type != 'BSDF_PRINCIPLED':
                continue
            # Blender 4.x uses 'Emission Color'; 3.x uses 'Emission'
            em_color = node.inputs.get("Emission Color") or node.inputs.get("Emission")
            em_strength = node.inputs.get("Emission Strength")
            if em_color and em_color.is_linked:
                return "Emissive"
            if em_color and em_strength:
                col = em_color.default_value
                strength = em_strength.default_value if hasattr(em_strength, "default_value") else 0.0
                if strength > 0.0 and (col[0] > 0.01 or col[1] > 0.01 or col[2] > 0.01):
                    return "Emissive"
    return "Opaque"


def _dominant_render_type(obj) -> str:
    """Return the dominant render type for a mesh object."""
    if not obj.data.materials:
        return "Opaque"
    types = [_classify_material(m) for m in obj.data.materials if m]
    # Priority: Alpha Blend > Emissive > Alpha Clip > Opaque
    for priority in ("Alpha Blend", "Emissive", "Alpha Clip", "Opaque"):
        if priority in types:
            return priority
    return "Opaque"


def _output_material_type_label(settings) -> str:
    key = getattr(settings, "output_material_type", "AUTO") or "AUTO"
    if key == "AUTO":
        return "Auto (atlas group render type)"
    return _OUTPUT_MATERIAL_TYPE_LABELS.get(key, "Auto (atlas group render type)")


def _resolve_output_render_type(group, settings) -> str:
    detected = getattr(group, "render_type", "Opaque") or "Opaque"
    key = getattr(settings, "output_material_type", "AUTO") or "AUTO"
    if key == "AUTO":
        return detected
    return _OUTPUT_MATERIAL_TYPE_MAP.get(key, detected)


def _output_surface_shader_label(settings) -> str:
    key = getattr(settings, "output_surface_shader", "AUTO") or "AUTO"
    return _OUTPUT_SURFACE_SHADER_LABELS.get(key, "Auto (Principled)")


def _resolve_output_surface_shader(settings) -> str:
    key = getattr(settings, "output_surface_shader", "AUTO") or "AUTO"
    if key == "AUTO":
        return "PRINCIPLED"
    if key in _OUTPUT_SURFACE_SHADER_LABELS:
        return key
    return "PRINCIPLED"


def _node_input(node, *names):
    for name in names:
        socket = node.inputs.get(name)
        if socket is not None:
            return socket
    return None


def _node_output(node, *names):
    for name in names:
        socket = node.outputs.get(name)
        if socket is not None:
            return socket
    return None


def _socket_name_is_alpha_like(socket) -> bool:
    name = getattr(socket, "name", "")
    key = "".join(ch.lower() for ch in name if ch.isalnum())
    return "alpha" in key or "opacity" in key or "transparent" in key


def _image_has_alpha(image) -> bool:
    return bool(image and getattr(image, "channels", 0) >= 4)


def _find_alpha_source_image_node(mat, *, allow_unlinked_alpha=False):
    if not mat or not mat.use_nodes or not mat.node_tree:
        return None

    image_nodes = [
        node for node in mat.node_tree.nodes
        if node.type == "TEX_IMAGE" and getattr(node, "image", None)
    ]
    for node in image_nodes:
        alpha_output = node.outputs.get("Alpha")
        if not alpha_output or not alpha_output.is_linked:
            continue
        if any(_socket_name_is_alpha_like(link.to_socket) for link in alpha_output.links):
            return node

    for node in image_nodes:
        node_label = getattr(node, "label", "") or node.name
        role = detect_texture_role(
            node_label,
            node_name=node.name,
            via_node_type=node.type,
        )
        if role == ROLE_ALPHA:
            return node

    if allow_unlinked_alpha:
        for node in image_nodes:
            if _image_has_alpha(node.image):
                return node

    return None


def _material_alpha_default(mat) -> float:
    if not mat or not mat.use_nodes or not mat.node_tree:
        return 1.0
    for node in mat.node_tree.nodes:
        if node.type != "BSDF_PRINCIPLED":
            continue
        alpha_input = node.inputs.get("Alpha")
        if alpha_input is not None and hasattr(alpha_input, "default_value"):
            return float(alpha_input.default_value)
    return 1.0


def _material_uses_alpha(mat) -> bool:
    if not mat:
        return False
    blend = str(getattr(mat, "blend_method", "") or "").upper()
    alpha_method = str(getattr(mat, "alpha_method", "") or "").upper()
    alpha_like = blend not in {"", "OPAQUE"} or alpha_method not in {"", "OPAQUE"}
    if _find_alpha_source_image_node(mat, allow_unlinked_alpha=alpha_like) is not None:
        return True
    return _material_alpha_default(mat) < 0.999


def _group_needs_alpha_atlas(joined, output_render_type) -> bool:
    if output_render_type in ("Alpha Blend", "Alpha Clip"):
        return True
    return any(_material_uses_alpha(mat) for mat in joined.data.materials if mat)


def _copy_source_image_node_settings(source_node, target_node):
    for attr in ("extension", "interpolation", "projection"):
        if hasattr(source_node, attr) and hasattr(target_node, attr):
            try:
                setattr(target_node, attr, getattr(source_node, attr))
            except Exception:
                pass


def _build_alpha_bake_material(source_mat):
    temp = bpy.data.materials.new(f"__BF_ALPHA_BAKE_{source_mat.name if source_mat else 'opaque'}")
    temp.use_nodes = True
    nodes = temp.node_tree.nodes
    links = temp.node_tree.links
    nodes.clear()

    output_node = nodes.new("ShaderNodeOutputMaterial")
    output_node.location = (260, 0)
    emission_node = nodes.new("ShaderNodeEmission")
    emission_node.location = (40, 0)
    strength_input = emission_node.inputs.get("Strength")
    if strength_input is not None and hasattr(strength_input, "default_value"):
        strength_input.default_value = 1.0

    alpha_like = _material_uses_alpha(source_mat)
    source_node = _find_alpha_source_image_node(source_mat, allow_unlinked_alpha=alpha_like)
    color_input = emission_node.inputs.get("Color")
    if source_node is not None and color_input is not None:
        uv_node = nodes.new("ShaderNodeUVMap")
        uv_node.uv_map = "UVMap_pre_atlas"
        uv_node.location = (-520, 0)
        tex_node = nodes.new("ShaderNodeTexImage")
        tex_node.name = "Alpha Source"
        tex_node.image = source_node.image
        tex_node.location = (-260, 0)
        _copy_source_image_node_settings(source_node, tex_node)
        links.new(uv_node.outputs["UV"], tex_node.inputs["Vector"])
        alpha_output = tex_node.outputs.get("Alpha") or tex_node.outputs.get("Color")
        if alpha_output is not None:
            links.new(alpha_output, color_input)
    elif color_input is not None:
        alpha_value = max(0.0, min(1.0, _material_alpha_default(source_mat)))
        color_input.default_value = (alpha_value, alpha_value, alpha_value, 1.0)

    links.new(emission_node.outputs["Emission"], output_node.inputs["Surface"])
    return temp


def _copy_mask_luminance_to_image_alpha(mask_img, target_img):
    pixel_count = int(target_img.size[0]) * int(target_img.size[1]) * 4
    if pixel_count <= 0:
        return
    mask_pixels = array("f", [0.0]) * pixel_count
    target_pixels = array("f", [0.0]) * pixel_count
    mask_img.pixels.foreach_get(mask_pixels)
    target_img.pixels.foreach_get(target_pixels)
    for index in range(0, pixel_count, 4):
        alpha = max(mask_pixels[index], mask_pixels[index + 1], mask_pixels[index + 2])
        target_pixels[index + 3] = max(0.0, min(1.0, alpha))
    target_img.pixels.foreach_set(target_pixels)
    target_img.update()


def _bake_alpha_mask_to_atlas(context, joined, atlas_img, settings, atlas_name, res):
    alpha_name = f"{atlas_name}_alpha_mask"
    if alpha_name in bpy.data.images:
        bpy.data.images.remove(bpy.data.images[alpha_name])
    alpha_img = bpy.data.images.new(alpha_name, width=res, height=res, alpha=True)
    alpha_img.colorspace_settings.name = "Non-Color"

    original_materials = [mat for mat in joined.data.materials]
    temp_materials = []
    try:
        for index, source_mat in enumerate(original_materials):
            temp_mat = _build_alpha_bake_material(source_mat)
            temp_materials.append(temp_mat)
            joined.data.materials[index] = temp_mat

            target = temp_mat.node_tree.nodes.new("ShaderNodeTexImage")
            target.name = "BF_ALPHA_TARGET"
            target.image = alpha_img
            target.location = (-260, -260)
            for node in temp_mat.node_tree.nodes:
                node.select = False
            target.select = True
            temp_mat.node_tree.nodes.active = target

        context.view_layer.objects.active = joined
        _deselect_all_objects_directly(context.view_layer)
        joined.select_set(True)
        _run_with_view3d_context(
            context,
            bpy.ops.object.bake,
            "Bake atlas alpha mask",
            type="EMIT",
            use_selected_to_active=False,
            margin=settings.atlas_padding_pixels,
            use_clear=True,
        )
        _copy_mask_luminance_to_image_alpha(alpha_img, atlas_img)
    finally:
        for index, mat in enumerate(original_materials):
            joined.data.materials[index] = mat
        for temp_mat in temp_materials:
            if temp_mat.name in bpy.data.materials:
                bpy.data.materials.remove(temp_mat)
        if alpha_img.name in bpy.data.images:
            bpy.data.images.remove(alpha_img)


def _target_meshes(context, settings=None):
    """Return meshes for the current atlas scope."""
    scope = getattr(settings, "target_scope", "ACTIVE_ARMATURE") if settings else "ACTIVE_ARMATURE"

    if scope == "SELECTED_MESHES":
        return [o for o in context.selected_objects if o.type == "MESH"]

    if scope == "VISIBLE_SCENE":
        return [
            o for o in context.scene.objects
            if o.type == "MESH" and o.visible_get()
        ]

    arm = active_armature(context)
    if arm:
        return [c for c in arm.children if c.type == "MESH"]

    active = context.view_layer.objects.active
    if active is not None and active.type == "MESH":
        return [active]

    return [
        o for o in context.scene.objects
        if o.type == "MESH" and o.visible_get()
    ]


def _find_view3d_context_override(context):
    """Return a VIEW_3D override for bpy operators that need UI context."""
    wm = getattr(context, "window_manager", None)
    if wm is None:
        return None
    for window in wm.windows:
        screen = getattr(window, "screen", None)
        if screen is None:
            continue
        for area in screen.areas:
            if area.type != "VIEW_3D":
                continue
            for region in area.regions:
                if region.type == "WINDOW":
                    return {
                        "window": window,
                        "screen": screen,
                        "area": area,
                        "region": region,
                    }
    return None


def _run_with_view3d_context(context, op_call, stage: str, **kwargs):
    """Run an operator with a VIEW_3D override when one is available."""
    override = _find_view3d_context_override(context)
    try:
        if override:
            with context.temp_override(**override):
                return op_call(**kwargs)
        return op_call(**kwargs)
    except Exception as exc:
        raise RuntimeError(f"{stage} failed: {exc}") from exc


def _ensure_object_mode(context, stage: str):
    """Leave edit/pose mode before object-level atlas operations."""
    obj = getattr(context, "object", None)
    if obj is not None and getattr(obj, "mode", "OBJECT") != "OBJECT":
        _run_with_view3d_context(context, bpy.ops.object.mode_set, stage, mode="OBJECT")


def _deselect_all_objects_directly(view_layer):
    """Deselect objects without bpy.ops.object.select_all poll requirements."""
    for obj in view_layer.objects:
        try:
            obj.select_set(False)
        except RuntimeError:
            pass


def _iter_material_slots(obj):
    """Yield object material slots as (object, slot_index, material)."""
    if obj is None or getattr(obj, "type", None) != "MESH":
        return
    for slot_index, mat in enumerate(obj.data.materials):
        yield obj, slot_index, mat


def _iter_texture_nodes(mat):
    """Yield image texture nodes and image datablocks in a material."""
    if not mat or not mat.use_nodes or not mat.node_tree:
        return
    for node in mat.node_tree.nodes:
        if node.type == "TEX_IMAGE":
            yield node, node.image


def _iter_texture_images(mat):
    """Yield image datablocks used by texture nodes in a material."""
    for _node, image in _iter_texture_nodes(mat):
        yield image


def _detect_texture_node_role(node) -> str:
    """Infer semantic role for an image texture node from its outgoing links."""
    if node is None:
        return ROLE_UNKNOWN
    for output in node.outputs:
        for link in output.links:
            to_node = link.to_node
            role = detect_texture_role(
                getattr(link.to_socket, "name", ""),
                node_name=getattr(to_node, "name", ""),
                output_name=getattr(output, "name", ""),
                via_node_type=getattr(to_node, "type", ""),
            )
            if role != ROLE_UNKNOWN:
                return role
            for mid_output in getattr(to_node, "outputs", []):
                for mid_link in mid_output.links:
                    role = detect_texture_role(
                        getattr(mid_link.to_socket, "name", ""),
                        node_name=getattr(mid_link.to_node, "name", ""),
                        output_name=getattr(mid_output, "name", ""),
                        via_node_type=getattr(to_node, "type", ""),
                    )
                    if role != ROLE_UNKNOWN:
                        return role
    return ROLE_UNKNOWN


def _material_shader_type(mat) -> str:
    if not mat:
        return "EMPTY_SLOT"
    if not mat.use_nodes or not mat.node_tree:
        return "NO_NODE_TREE"
    for node in mat.node_tree.nodes:
        if node.type != "OUTPUT_MATERIAL":
            continue
        surface = node.inputs.get("Surface")
        if surface and surface.is_linked:
            source = surface.links[0].from_node
            return getattr(source, "type", "") or getattr(source, "bl_idname", "")
    for node in mat.node_tree.nodes:
        if node.type.startswith("BSDF") or node.type in {"EMISSION", "GROUP"}:
            return node.type
    return "UNKNOWN_SHADER"


def _material_emission_strength(mat) -> float:
    if not mat or not mat.use_nodes or not mat.node_tree:
        return 0.0
    for node in mat.node_tree.nodes:
        if node.type != "BSDF_PRINCIPLED":
            continue
        strength = node.inputs.get("Emission Strength")
        if strength and hasattr(strength, "default_value"):
            return float(strength.default_value or 0.0)
    return 0.0


def _texture_quality_source(mat_name, node, image) -> TextureSource:
    return TextureSource(
        material_name=mat_name or "",
        node_name=node.name if node else "",
        image_name=image.name if image else "",
        image_path=bpy.path.abspath(image.filepath) if image and image.filepath else "",
        width=int(image.size[0]) if image else 0,
        height=int(image.size[1]) if image else 0,
        colorspace=(
            image.colorspace_settings.name
            if image and image.colorspace_settings
            else ""
        ),
        packed=bool(image and image.packed_file),
        missing=image is None,
        socket_name="",
        output_name="",
        via_node_type="",
        role=_detect_texture_node_role(node),
        enabled=image is not None,
    )


def _material_quality_source(obj, slot_index, mat) -> MaterialSource:
    mat_name = mat.name if mat else "<empty>"
    textures = tuple(
        _texture_quality_source(mat_name, node, image)
        for node, image in _iter_texture_nodes(mat)
    )
    return MaterialSource(
        material_name=mat_name,
        object_name=obj.name if obj else "",
        slot_index=slot_index,
        shader_type=_material_shader_type(mat),
        use_nodes=bool(mat and mat.use_nodes),
        has_node_tree=bool(mat and mat.node_tree),
        textures=textures,
        alpha_mode=getattr(mat, "alpha_method", "") if mat else "",
        blend_method=getattr(mat, "blend_method", "") if mat else "",
        emission_strength=_material_emission_strength(mat),
    )


def _group_texture_quality_sources(group):
    return [
        TextureSource(
            material_name=item.material_name,
            node_name=item.node_name,
            image_name="" if item.missing else item.image_name,
            image_path=item.image_path,
            width=item.width,
            height=item.height,
            colorspace=item.colorspace,
            packed=item.packed,
            missing=item.missing,
            role=item.role,
            enabled=item.enabled,
        )
        for item in getattr(group, "textures", [])
    ]


def _material_source_size(group, material_item):
    for tex in getattr(group, "textures", []):
        if (
            tex.object_name == material_item.object_name
            and tex.slot_index == material_item.slot_index
            and tex.material_name == material_item.material_name
            and tex.width > 0
            and tex.height > 0
        ):
            return tex.width, tex.height
    return 0, 0


def _settings_enabled_passes(settings):
    passes = []
    if settings.bake_albedo:
        passes.append(ROLE_ALBEDO)
    if settings.bake_normal:
        passes.append(ROLE_NORMAL)
    if settings.bake_emission:
        passes.append(ROLE_EMISSION)
    if getattr(settings, "bake_metallic", False):
        passes.append(ROLE_METALLIC)
    if settings.bake_roughness:
        passes.append(ROLE_ROUGHNESS)
    return passes


def _material_key(object_name, slot_index, material_name):
    return (object_name, int(slot_index), material_name or "")


def _texture_key(object_name, slot_index, material_name, node_name, image_name):
    return (
        object_name,
        int(slot_index),
        material_name or "",
        node_name or "",
        image_name or "",
    )


def _group_detected_material_count(group) -> int:
    if hasattr(group, "materials") and len(group.materials):
        return len(group.materials)
    return int(getattr(group, "mat_count", 0))


def _group_enabled_material_count(group) -> int:
    if hasattr(group, "materials") and len(group.materials):
        return sum(1 for item in group.materials if item.enabled)
    return int(getattr(group, "mat_count", 0))


def _group_enabled_texture_count(group) -> int:
    if hasattr(group, "textures") and len(group.textures):
        return sum(1 for item in group.textures if item.enabled)
    return 0


def _enabled_material_keys(group):
    if not hasattr(group, "materials") or not len(group.materials):
        return None
    return {
        _material_key(item.object_name, item.slot_index, item.material_name)
        for item in group.materials
        if item.enabled
    }


def _enabled_texture_keys(group):
    if not hasattr(group, "textures") or not len(group.textures):
        return None
    return {
        _texture_key(
            item.object_name,
            item.slot_index,
            item.material_name,
            item.node_name,
            item.image_name,
        )
        for item in group.textures
        if item.enabled and not item.missing
    }


def _enabled_slots_by_object(group):
    result = {}
    enabled_keys = _enabled_material_keys(group)
    if enabled_keys is None:
        for mesh_item in group.meshes:
            obj = bpy.data.objects.get(mesh_item.object_name)
            if obj and obj.type == "MESH":
                result[obj.name] = set(range(len(obj.data.materials)))
        return result

    for item in group.materials:
        if not item.enabled:
            continue
        result.setdefault(item.object_name, set()).add(int(item.slot_index))
    return result


def _detected_slots_by_object(group):
    result = {}
    if hasattr(group, "materials") and len(group.materials):
        for item in group.materials:
            result.setdefault(item.object_name, set()).add(int(item.slot_index))
        return result
    for mesh_item in group.meshes:
        obj = bpy.data.objects.get(mesh_item.object_name)
        if obj and obj.type == "MESH":
            result[obj.name] = set(range(len(obj.data.materials)))
    return result


def _populate_group_sources(group, objs):
    """Populate selectable material and texture rows for a group."""
    group.materials.clear()
    group.textures.clear()
    material_pairs = []
    texture_pairs = []

    for obj in objs:
        for _obj, slot_index, mat in _iter_material_slots(obj):
            mat_name = mat.name if mat else "<empty>"
            tex_nodes = list(_iter_texture_nodes(mat))
            mat_source = _material_quality_source(obj, slot_index, mat)
            mat_report = diagnose_material(mat_source)
            color_spaces = {
                image.colorspace_settings.name
                for _node, image in tex_nodes
                if image and image.colorspace_settings
            }

            mat_item = group.materials.add()
            mat_item.enabled = True
            mat_item.object_name = obj.name
            mat_item.slot_index = slot_index
            mat_item.material_name = mat_name
            mat_item.render_type = _classify_material(mat)
            mat_item.texture_count = len(tex_nodes)
            mat_item.has_no_images = len(tex_nodes) == 0
            mat_item.has_missing_image = any(image is None for _node, image in tex_nodes)
            mat_item.has_mixed_colorspace = len(color_spaces) > 1
            mat_item.diagnostic_status = mat_report["status"]
            mat_item.diagnostic_warnings = "; ".join(mat_report["warnings"])
            mat_item.duplicate_group = ""
            mat_item.fallback_size = 512
            material_pairs.append((mat_item, mat_source))

            for node, image in tex_nodes:
                tex_source = _texture_quality_source(mat_name, node, image)
                tex_report = diagnose_texture(tex_source)
                tex_item = group.textures.add()
                tex_item.enabled = image is not None
                tex_item.object_name = obj.name
                tex_item.slot_index = slot_index
                tex_item.material_name = mat_name
                tex_item.node_name = node.name
                tex_item.image_name = image.name if image else "<missing>"
                tex_item.image_path = bpy.path.abspath(image.filepath) if image and image.filepath else ""
                tex_item.width = int(image.size[0]) if image else 0
                tex_item.height = int(image.size[1]) if image else 0
                tex_item.colorspace = (
                    image.colorspace_settings.name
                    if image and image.colorspace_settings
                    else ""
                )
                tex_item.packed = bool(image and image.packed_file)
                tex_item.missing = image is None
                tex_item.role = tex_source.role
                tex_item.role_label = role_label(tex_source.role)
                tex_item.expected_colorspace = str(tex_report["colorspace_expected"])
                tex_item.diagnostic_status = str(tex_report["status"])
                tex_item.diagnostic_warnings = "; ".join(tex_report["warnings"])
                tex_item.duplicate_group = ""
                texture_pairs.append((tex_item, tex_source))

    texture_duplicates = find_duplicate_texture_groups(
        [source for _item, source in texture_pairs]
    )
    for duplicate_index, duplicate in enumerate(texture_duplicates, start=1):
        key = duplicate["key"]
        marker = f"T{duplicate_index}"
        for item, source in texture_pairs:
            if duplicate_texture_key(source) == key:
                item.duplicate_group = marker

    material_duplicates = find_shared_material_groups(
        [source for _item, source in material_pairs]
    )
    for duplicate_index, duplicate in enumerate(material_duplicates, start=1):
        marker = f"M{duplicate_index}"
        names = set(duplicate["materials"])
        for item, _source in material_pairs:
            if item.material_name in names:
                item.duplicate_group = marker

    group.duplicate_count = len(texture_duplicates) + len(material_duplicates)
    group.unknown_texture_roles = sum(
        1 for item in group.textures if item.role == ROLE_UNKNOWN
    )
    material_warnings = sum(1 for item in group.materials if item.diagnostic_warnings)
    texture_warnings = sum(1 for item in group.textures if item.diagnostic_warnings)
    group.quality_summary = (
        f"{material_warnings} material warning(s), "
        f"{texture_warnings} texture warning(s), "
        f"{group.duplicate_count} duplicate/shared group(s), "
        f"{group.unknown_texture_roles} unknown role(s)"
    )
    if material_warnings or texture_warnings or group.duplicate_count or group.unknown_texture_roles:
        group.has_warnings = True


def _copy_material_slots(mesh):
    for mat_index, mat in enumerate(mesh.materials):
        if mat is not None:
            mesh.materials[mat_index] = mat.copy()


def _remove_faces_by_material_slots(obj, slots_to_remove):
    """Remove faces assigned to material slots in *slots_to_remove*."""
    if not slots_to_remove:
        return len(obj.data.polygons) > 0
    bm = bmesh.new()
    try:
        bm.from_mesh(obj.data)
        faces = [face for face in bm.faces if face.material_index in slots_to_remove]
        if faces:
            bmesh.ops.delete(bm, geom=faces, context="FACES")
            bm.to_mesh(obj.data)
            obj.data.update()
    finally:
        bm.free()
    return len(obj.data.polygons) > 0


def _disconnect_disabled_texture_nodes(mat, object_name, slot_index, material_name, enabled_texture_keys):
    if enabled_texture_keys is None or not mat or not mat.use_nodes or not mat.node_tree:
        return
    links = mat.node_tree.links
    for node, image in _iter_texture_nodes(mat):
        key = _texture_key(
            object_name,
            slot_index,
            material_name,
            node.name,
            image.name if image else "<missing>",
        )
        if key in enabled_texture_keys:
            continue
        for output in node.outputs:
            for link in list(output.links):
                links.remove(link)


def _ensure_source_uv_node(nodes, uv_map_name, location):
    uv_node = nodes.get("BF_ATLAS_SOURCE_UV")
    if uv_node is None:
        uv_node = nodes.new("ShaderNodeUVMap")
        uv_node.name = "BF_ATLAS_SOURCE_UV"
        uv_node.label = "BoneForge Source UV"
        uv_node.location = location
    uv_node.uv_map = uv_map_name
    return uv_node


def _uses_uv_map_node(node):
    return (
        getattr(node, "type", "") == "UVMAP"
        or getattr(node, "bl_idname", "") == "ShaderNodeUVMap"
    )


def _preserve_explicit_uv_map_node(node, uv_map_name):
    if not _uses_uv_map_node(node):
        return False
    if not getattr(node, "uv_map", ""):
        node.uv_map = uv_map_name
    return True


def _route_vector_socket_to_uv(links, vector_input, uv_node):
    if vector_input is None:
        return False

    if not vector_input.is_linked:
        links.new(uv_node.outputs["UV"], vector_input)
        return True

    for link in list(vector_input.links):
        if _preserve_explicit_uv_map_node(link.from_node, uv_node.uv_map):
            return True
        upstream_input = getattr(link.from_node, "inputs", {}).get("Vector")
        if upstream_input is None:
            continue
        for old_link in list(upstream_input.links):
            if _preserve_explicit_uv_map_node(old_link.from_node, uv_node.uv_map):
                return True
        for old_link in list(upstream_input.links):
            links.remove(old_link)
        links.new(uv_node.outputs["UV"], upstream_input)
        return True

    for link in list(vector_input.links):
        links.remove(link)
    links.new(uv_node.outputs["UV"], vector_input)
    return True


def _route_source_image_nodes_to_uv(mat, uv_map_name):
    """Make copied source textures sample the original UV while baking to atlas_uv."""
    if not mat or not mat.use_nodes or not mat.node_tree:
        return 0

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    routed = 0
    for node, image in _iter_texture_nodes(mat):
        if node.name == "BF_ATLAS_TARGET" or image is None:
            continue
        vector_input = node.inputs.get("Vector")
        uv_node = _ensure_source_uv_node(
            nodes,
            uv_map_name,
            (node.location.x - 240, node.location.y),
        )
        if _route_vector_socket_to_uv(links, vector_input, uv_node):
            routed += 1
    return routed


def _assign_single_atlas_material(mesh, atlas_mat):
    mesh.materials.clear()
    mesh.materials.append(atlas_mat)
    for poly in mesh.polygons:
        poly.material_index = 0
    mesh.update()


def _validate_atlas_mesh(obj, atlas_mat):
    mesh = obj.data
    errors = []
    atlas_index = next(
        (i for i, uv in enumerate(mesh.uv_layers) if uv.name == "atlas_uv"),
        None,
    )
    if atlas_index is None:
        errors.append("missing atlas_uv map")
    elif not getattr(mesh.uv_layers[atlas_index], "active_render", False):
        errors.append("atlas_uv is not the active render UV")
    if not mesh.materials or mesh.materials[0] != atlas_mat:
        errors.append("atlas material is not slot 0")
    stale_faces = sum(1 for poly in mesh.polygons if poly.material_index != 0)
    if stale_faces:
        errors.append(f"{stale_faces} face(s) still point to old material slots")
    if errors:
        raise RuntimeError("Atlas validation failed: " + "; ".join(errors))


def _activate_atlas_uv(mesh):
    for index, uv in enumerate(mesh.uv_layers):
        is_atlas = uv.name == "atlas_uv"
        uv.active_render = is_atlas
        if is_atlas:
            try:
                mesh.uv_layers.active_index = index
            except Exception:
                uv.active = True
    return "atlas_uv" in mesh.uv_layers


def _prepare_atlas_uv_for_export(mesh, keep_source_uv_maps):
    if "atlas_uv" not in mesh.uv_layers:
        return False
    if not keep_source_uv_maps:
        for uv in list(mesh.uv_layers):
            if uv.name != "atlas_uv":
                mesh.uv_layers.remove(uv)
    return _activate_atlas_uv(mesh)


def _cleanup_transient_atlas_objects():
    """Remove internal atlas work objects left by failed bake stages."""
    for obj in list(bpy.data.objects):
        if (
            obj.name.startswith("__BF_ATLAS_")
            or obj.name.startswith("__BF_ATLAS_WORK_")
            or obj.name.startswith("ATLAS_KEEP_")
        ):
            bpy.data.objects.remove(obj, do_unlink=True)


def _build_debug_report(meshes, settings) -> str:
    """Build a copyable diagnostic report for mixed material/texture atlasing."""
    lines = [
        "BoneForge CATS Material Atlas Debug Report",
        f"Scope: {getattr(settings, 'target_scope', 'ACTIVE_ARMATURE')}",
        f"Meshes scanned: {len(meshes)}",
        f"Output: {settings.output_format} -> {bpy.path.abspath(settings.output_path)}",
        f"Output material type: {_output_material_type_label(settings)}",
        f"Output surface: {_output_surface_shader_label(settings)}",
        f"UV method: {get_uv_method_label(getattr(settings, 'pack_method', 'SOURCE_PRESERVE'))}",
        f"UV margin: {getattr(settings, 'uv_margin', 0.02)}",
        f"Packing preset: {packing_preset_settings(getattr(settings, 'packing_preset', 'SAFE_DEFAULT'))['label']}",
        f"Bake padding: {getattr(settings, 'atlas_padding_pixels', 4)} px",
        "",
    ]
    if method_uses_seed(getattr(settings, "pack_method", "")):
        lines.insert(5, f"UV seed: {getattr(settings, 'uv_random_seed', 1337)}")
        lines.insert(6, f"UV rotation step: {getattr(settings, 'uv_rotation_step', '90')}")

    if not meshes:
        lines.append("ERROR: No mesh objects were found for the current scope.")
        return "\n".join(lines)

    seen_images = {}
    total_materials = 0
    problem_count = 0
    quality_materials = []
    quality_textures = []

    for obj in meshes:
        mesh = obj.data
        uv_state = "OK" if mesh.uv_layers else "MISSING"
        if not mesh.uv_layers:
            problem_count += 1
        lines.append(f"Mesh: {obj.name} | materials={len(mesh.materials)} | uv={uv_state}")

        for slot_index, mat in enumerate(mesh.materials):
            total_materials += 1
            if mat is None:
                problem_count += 1
                lines.append(f"  [{slot_index}] ERROR: empty material slot")
                continue

            render_type = _classify_material(mat)
            mat_source = _material_quality_source(obj, slot_index, mat)
            mat_report = diagnose_material(mat_source)
            quality_materials.append(mat_source)
            if not mat.use_nodes or not mat.node_tree:
                problem_count += 1
                lines.append(
                    f"  [{slot_index}] {mat.name} | {render_type} | "
                    f"{mat_report['status']} | WARNING: material has no node tree"
                )
                continue

            tex_nodes = list(_iter_texture_nodes(mat))
            if not tex_nodes:
                problem_count += 1
                lines.append(
                    f"  [{slot_index}] {mat.name} | {render_type} | "
                    f"{mat_report['status']} | WARNING: no image texture nodes"
                )
                continue

            for node, img in tex_nodes:
                tex_source = _texture_quality_source(mat.name, node, img)
                tex_report = diagnose_texture(tex_source)
                quality_textures.append(tex_source)
                if img is None:
                    problem_count += 1
                    lines.append(f"  [{slot_index}] {mat.name} | ERROR: image node has no image")
                    continue
                key = img.name
                seen_images[key] = img
                packed = "packed" if img.packed_file else "external"
                path = bpy.path.abspath(img.filepath) if img.filepath else "<unsaved or generated>"
                lines.append(
                    f"  [{slot_index}] {mat.name} | {render_type} | "
                    f"role={tex_report['role_label']} | "
                    f"image={img.name} {img.size[0]}x{img.size[1]} {packed} | {path}"
                )

    sizes = sorted({(img.size[0], img.size[1]) for img in seen_images.values() if img})
    color_spaces = sorted({
        img.colorspace_settings.name for img in seen_images.values()
        if img and img.colorspace_settings
    })

    lines.extend([
        "",
        f"Materials scanned: {total_materials}",
        f"Images scanned: {len(seen_images)}",
        f"Image sizes: {', '.join(f'{w}x{h}' for w, h in sizes) if sizes else 'none'}",
        f"Color spaces: {', '.join(color_spaces) if color_spaces else 'none'}",
        f"Warnings/errors: {problem_count}",
    ])

    if len(sizes) > 1:
        lines.append("NOTE: Mixed source image sizes are supported, but small images may soften in a large atlas.")
    if len(color_spaces) > 1:
        lines.append("NOTE: Mixed color spaces detected. Verify the baked atlas visually before Accept.")

    if quality_materials or quality_textures:
        lines.extend([
            "",
            format_quality_debug_report(
                quality_materials,
                quality_textures,
                size_preset="SOURCE",
                packing_preset=getattr(settings, "packing_preset", "SAFE_DEFAULT"),
                enabled_passes=_settings_enabled_passes(settings),
                channel_pack=getattr(settings, "channel_pack_orm", False),
            ),
        ])

    if getattr(settings, "atlas_groups", None):
        lines.extend(["", "Selectable row state:"])
        for group in settings.atlas_groups:
            lines.append(
                f"- {group.name}: enabled={group.enabled}, "
                f"summary={getattr(group, 'quality_summary', '') or 'none'}"
            )
            for mat_item in getattr(group, "materials", []):
                state = "on" if mat_item.enabled else "off"
                duplicate = f", duplicate={mat_item.duplicate_group}" if mat_item.duplicate_group else ""
                lines.append(
                    f"  material {state}: {mat_item.object_name}[{mat_item.slot_index}] "
                    f"{mat_item.material_name} | {mat_item.diagnostic_status}{duplicate}"
                )
            for tex_item in getattr(group, "textures", []):
                state = "on" if tex_item.enabled else "off"
                duplicate = f", duplicate={tex_item.duplicate_group}" if tex_item.duplicate_group else ""
                lines.append(
                    f"  texture {state}: {tex_item.material_name}/{tex_item.node_name} "
                    f"{tex_item.image_name} | role={role_label(tex_item.role)}{duplicate}"
                )

    return "\n".join(lines)


def _store_debug_report(context, meshes, settings):
    if not getattr(settings, "debug_enabled", True):
        return
    settings.last_debug_report = _build_debug_report(meshes, settings)


def _has_high_emission(obj) -> bool:
    """True if any material has emission strength > 1.0."""
    for mat in obj.data.materials:
        if not mat or not mat.use_nodes or not mat.node_tree:
            continue
        for node in mat.node_tree.nodes:
            if node.type != 'BSDF_PRINCIPLED':
                continue
            em_strength = node.inputs.get("Emission Strength")
            if em_strength and hasattr(em_strength, "default_value"):
                if em_strength.default_value > 1.0:
                    return True
    return False


def _has_overlapping_uvs(obj) -> bool:
    """
    Heuristic UV overlap check.
    Detects meshes where UV coordinates suggest intentional mirrored sharing
    (multiple polygons mapping to the same 0-1 UV space from different faces).
    Uses bmesh for a lightweight island count check.
    """
    if obj.type != 'MESH' or not obj.data.uv_layers:
        return False
    try:
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        uv_layer = bm.loops.layers.uv.active
        if uv_layer is None:
            bm.free()
            return False

        # Collect all UV positions (rounded to avoid float noise)
        uv_set = set()
        duplicates = 0
        for face in bm.faces:
            face_uvs = tuple(
                (round(loop[uv_layer].uv[0], 3), round(loop[uv_layer].uv[1], 3))
                for loop in face.loops
            )
            for uv in face_uvs:
                if uv in uv_set:
                    duplicates += 1
                uv_set.add(uv)
        bm.free()

        # Heuristic: if >10% of UV verts are duplicates, likely intentional overlap
        if len(uv_set) > 0 and (duplicates / len(uv_set)) > 0.1:
            return True
    except Exception as e:
        logger.warning(f"[BoneForge Atlas] UV overlap check failed on {obj.name}: {e}")
    return False


def _projected_mat_count(settings) -> int:
    """Count projected atlas material count from current group config."""
    total = 0
    for group in settings.atlas_groups:
        detected = _group_detected_material_count(group)
        enabled = _group_enabled_material_count(group)
        if not group.enabled or detected == 0:
            total += detected
            continue
        if enabled >= 2:
            total += 1
            total += max(0, detected - enabled)
        else:
            total += detected
    return total


def _build_status_sentence(settings) -> str:
    """D-Shadow Inheritance Protocol: declarative sentence for Zone 1."""
    groups = [
        g for g in settings.atlas_groups
        if g.enabled and _group_enabled_material_count(g) >= 2
    ]
    total_before = settings.total_mats_before
    total_after = _projected_mat_count(settings)
    rank_after = _get_rank(total_after)

    if not settings.atlas_groups:
        if total_before > 0:
            return (f"{total_before} materials detected — "
                    f"press Analyze to auto-group")
        return "Press Analyze to detect materials"

    if not groups:
        return (f"{total_before} materials detected — "
                f"no groups with 2+ materials enabled")

    shape_key_note = ""
    for group in settings.atlas_groups:
        for item in group.meshes:
            if item.has_shape_keys:
                shape_key_note = " and shape keys"
                break

    enabled_mats = sum(_group_enabled_material_count(g) for g in groups)
    return (
        f"{enabled_mats} materials across {len(groups)} groups — "
        f"estimated {rank_after} atlas — "
        f"bake will preserve UV maps by name{shape_key_note}"
    )


def _will_not_change_sentence(settings) -> str:
    """Second persistent line: what the bake guarantees not to touch."""
    guarantees = ["object hierarchy", "UV maps (saved as 'UVMap_pre_atlas')"]

    if True:
        guarantees.append("shape keys / blendshapes")
    if settings.preserve_originals:
        guarantees.append("originals (backup collection active)")

    return "Will not change: " + ", ".join(guarantees)


# ─────────────────────────────────────────────────────────────────
# Property Groups
# ─────────────────────────────────────────────────────────────────

class BF_AtlasMeshItem(PropertyGroup):
    """One mesh entry inside an atlas group."""
    object_name: StringProperty(name="Object")
    render_type: StringProperty(name="Render Type", default="Opaque")
    mat_count: IntProperty(name="Material Count", default=0)
    has_shape_keys: BoolProperty(name="Has Shape Keys", default=False)
    has_overlapping_uvs: BoolProperty(name="Overlapping UVs", default=False)
    has_high_emission: BoolProperty(name="Emission > 1.0", default=False)


class BF_AtlasMaterialItem(PropertyGroup):
    """Selectable material source row inside an atlas group."""
    enabled: BoolProperty(name="Include", default=True)
    object_name: StringProperty(name="Object")
    slot_index: IntProperty(name="Slot", default=0)
    material_name: StringProperty(name="Material")
    render_type: StringProperty(name="Render Type", default="Opaque")
    texture_count: IntProperty(name="Texture Count", default=0)
    has_no_images: BoolProperty(name="No Images", default=False)
    has_missing_image: BoolProperty(name="Missing Image", default=False)
    has_mixed_colorspace: BoolProperty(name="Mixed Color Space", default=False)
    diagnostic_status: StringProperty(name="Diagnostic Status", default="")
    diagnostic_warnings: StringProperty(name="Warnings", default="")
    duplicate_group: StringProperty(name="Duplicate Group", default="")
    size_override: BoolProperty(name="Override Size", default=False)
    size_preset: EnumProperty(
        name="Size",
        items=_SIZE_PRESET_ITEMS,
        default="SOURCE",
    )
    target_width: IntProperty(name="Width", default=1024, min=16, max=8192)
    target_height: IntProperty(name="Height", default=1024, min=16, max=8192)
    fallback_size: IntProperty(name="Fallback", default=512, min=16, max=8192)


class BF_AtlasTextureItem(PropertyGroup):
    """Selectable image texture source row inside an atlas group."""
    enabled: BoolProperty(name="Include", default=True)
    object_name: StringProperty(name="Object")
    slot_index: IntProperty(name="Slot", default=0)
    material_name: StringProperty(name="Material")
    node_name: StringProperty(name="Node")
    image_name: StringProperty(name="Image")
    image_path: StringProperty(name="Path")
    width: IntProperty(name="Width", default=0)
    height: IntProperty(name="Height", default=0)
    colorspace: StringProperty(name="Color Space")
    packed: BoolProperty(name="Packed", default=False)
    missing: BoolProperty(name="Missing", default=False)
    role: EnumProperty(
        name="Role",
        items=_TEXTURE_ROLE_ITEMS,
        default=ROLE_UNKNOWN,
    )
    role_label: StringProperty(name="Role Label", default="")
    expected_colorspace: StringProperty(name="Expected Color Space", default="")
    diagnostic_status: StringProperty(name="Diagnostic Status", default="")
    diagnostic_warnings: StringProperty(name="Warnings", default="")
    duplicate_group: StringProperty(name="Duplicate Group", default="")


class BF_AtlasGroup(PropertyGroup):
    """One atlas group (bakes into a single texture atlas)."""
    name: StringProperty(name="Group Name", default="Group")
    enabled: BoolProperty(name="Enabled", default=True)
    meshes: CollectionProperty(type=BF_AtlasMeshItem)
    materials: CollectionProperty(type=BF_AtlasMaterialItem)
    textures: CollectionProperty(type=BF_AtlasTextureItem)
    active_material_index: IntProperty(name="Active Material", default=0)
    active_texture_index: IntProperty(name="Active Texture", default=0)
    render_type: StringProperty(name="Render Type", default="Opaque")
    resolution: EnumProperty(
        name="Resolution",
        items=[
            ("1024", "1024", "1024 × 1024 px — 5.3 MB VRAM"),
            ("2048", "2048", "2048 × 2048 px — 21.3 MB VRAM"),
            ("4096", "4096", "4096 × 4096 px — 85.3 MB VRAM"),
        ],
        default="2048",
    )
    mat_count: IntProperty(name="Material Count", default=0)
    has_warnings: BoolProperty(name="Has Warnings", default=False)
    warn_overlap: BoolProperty(name="UV Overlap Warning", default=False)
    warn_emission: BoolProperty(name="High Emission Warning", default=False)
    quality_summary: StringProperty(name="Quality Summary", default="")
    duplicate_count: IntProperty(name="Duplicate Count", default=0)
    unknown_texture_roles: IntProperty(name="Unknown Texture Roles", default=0)


class BF_AtlasSettings(PropertyGroup):
    """Scene-level atlas combiner settings."""

    # Group list
    atlas_groups: CollectionProperty(type=BF_AtlasGroup)
    active_group_index: IntProperty(name="Active Group", default=0)

    # Status (populated by Analyze)
    total_mats_before: IntProperty(default=0)
    rank_before: StringProperty(default="")
    last_bake_result: StringProperty(default="")
    last_debug_report: StringProperty(default="")

    # Backup state
    has_backup: BoolProperty(default=False)
    backup_collection_name: StringProperty(default="")

    # Friendly defaults
    target_scope: EnumProperty(
        name="Target",
        description="Which meshes are included when Analyze or Smart Combine runs",
        items=[
            ("ACTIVE_ARMATURE", "Active Avatar", "Use mesh children of the active armature, or the active mesh if no armature is active"),
            ("SELECTED_MESHES", "Selected Meshes", "Use only selected mesh objects"),
            ("VISIBLE_SCENE", "Visible Scene", "Use every visible mesh in the scene"),
        ],
        default="ACTIVE_ARMATURE",
    )
    auto_analyze_before_bake: BoolProperty(
        name="Auto Analyze",
        description="Automatically rebuild atlas groups before one-click baking",
        default=True,
    )
    debug_enabled: BoolProperty(
        name="Debug Report",
        description="Build a copyable report of source meshes, material slots, texture images, UV state, image sizes, and color spaces",
        default=True,
    )
    color_fallback_size: IntProperty(
        name="Color Fallback Size",
        description="Atlas allocation size used for color-only materials with no image textures",
        default=512,
        min=16,
        max=8192,
    )
    packing_preset: EnumProperty(
        name="Packing Preset",
        description="Quality preset for atlas padding and bleed behavior",
        items=_PACKING_PRESET_ITEMS,
        default="SAFE_DEFAULT",
    )
    atlas_padding_pixels: IntProperty(
        name="Bake Padding",
        description="Pixel margin used by Blender's bake operation",
        default=4,
        min=0,
        max=128,
    )
    pixel_art_no_bleed: BoolProperty(
        name="Pixel Art No-Bleed",
        description="Keep padding conservative for crisp nearest-neighbor textures",
        default=False,
    )
    preserve_island_orientation: BoolProperty(
        name="Preserve Island Orientation",
        description="Prefer UV methods that avoid unnecessary island rotation where supported",
        default=True,
    )
    keep_source_uv_maps: BoolProperty(
        name="Keep Source UV Maps",
        description=(
            "Keep UVMap_pre_atlas on the output mesh. Off by default so "
            "atlas_uv becomes UV0 for FBX/Unity/VRChat export"
        ),
        default=False,
    )

    # Advanced options
    preserve_originals: BoolProperty(
        name="Preserve Backup Duplicate",
        description=(
            "Create and keep a visible pre-atlas duplicate for Revert. "
            "Turn off to remove originals after atlasing without a backup duplicate."
        ),
        default=True,
    )
    uv_margin: FloatProperty(
        name="UV Margin",
        description=(
            "Space between UV islands in the atlas. Higher values prevent texture "
            "bleeding at edges but reduce usable pixel space. 0.02 is safe for most avatars"
        ),
        default=0.02,
        min=0.001,
        max=0.1,
        precision=3,
    )
    pack_method: EnumProperty(
        name="UV Method",
        description="How the atlas work mesh is unwrapped and packed before baking",
        items=atlas_uv_method_items(include_advanced=True),
        default="SOURCE_PRESERVE",
    )
    uv_random_seed: IntProperty(
        name="UV Seed",
        description="Deterministic seed used by seeded UV variation methods",
        default=1337,
        min=0,
        max=999999,
    )
    uv_rotation_step: EnumProperty(
        name="Rotation Step",
        description="B4Artists advanced control for seeded atlas island rotation",
        items=[
            ("90", "90 deg", "Stable right-angle variation"),
            ("45", "45 deg", "More varied diagonal rotations"),
            ("180", "180 deg", "Flip-only variation"),
        ],
        default="90",
    )
    bake_albedo: BoolProperty(name="Albedo (Color)", default=True)
    bake_normal: BoolProperty(
        name="Normal Map",
        description="Bake a separate normal atlas using the host bake engine",
        default=False,
    )
    bake_emission: BoolProperty(
        name="Emission",
        description="Bake a separate emission atlas when the material graph provides emission data",
        default=False,
    )
    bake_metallic: BoolProperty(
        name="Metallic",
        description="Planned utility-map pass. Currently preflight-blocked unless channel packing can safely provide a fallback",
        default=False,
    )
    bake_roughness: BoolProperty(
        name="Roughness",
        description="Bake a separate roughness atlas when the host bake engine supports the pass",
        default=False,
    )
    channel_pack_orm: BoolProperty(
        name="Pack ORM Channels",
        description="Opt-in channel packing: R=Metallic, G=Roughness, B=AO/black, A=Alpha/opaque",
        default=False,
    )
    allow_unknown_channel_pack_roles: BoolProperty(
        name="Allow Unknown Roles",
        description="Permit channel-packing preflight even when some enabled texture rows are still Unknown",
        default=False,
    )
    output_format: EnumProperty(
        name="Output Format",
        items=[
            ("PNG", "PNG", "Standard format — emission values > 1.0 will clamp"),
            ("TGA", "TGA", "TGA format — emission values > 1.0 will clamp"),
            ("EXR", "EXR", "HDR format — preserves emission values > 1.0"),
        ],
        default="PNG",
    )
    output_material_type: EnumProperty(
        name="Output Material Type",
        description="Choose the generated atlas material render type. Auto matches each atlas group.",
        items=_OUTPUT_MATERIAL_TYPE_ITEMS,
        default="AUTO",
    )
    output_surface_shader: EnumProperty(
        name="Output Surface",
        description="Choose the shader node connected to the generated material output surface. Auto keeps Principled BSDF.",
        items=_OUTPUT_SURFACE_SHADER_ITEMS,
        default="AUTO",
    )
    output_path: StringProperty(
        name="Output Path",
        description="Folder where atlas textures are saved",
        default="//textures/atlas/",
        subtype="DIR_PATH",
    )
    show_advanced: BoolProperty(name="Advanced Options", default=False)


# ─────────────────────────────────────────────────────────────────
# UIList
# ─────────────────────────────────────────────────────────────────

class BF_UL_VRC_AtlasGroups(UIList):
    """Displays atlas groups with render-type badge, material count, resolution."""

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        row = layout.row(align=True)

        # Enable toggle
        row.prop(item, "enabled", text="", emboss=False,
                 icon="CHECKBOX_HLT" if item.enabled else "CHECKBOX_DEHLT")

        # Group name (editable inline)
        sub = row.row(align=True)
        sub.enabled = item.enabled
        sub.prop(item, "name", text="", emboss=False)

        # Render type badge icon
        type_icons = {
            "Opaque": "MATERIAL",
            "Alpha Clip": "MOD_MASK",
            "Alpha Blend": "LIGHT_AREA",
            "Emissive": "LIGHT_SUN",
        }
        badge_icon = type_icons.get(item.render_type, "QUESTION")
        sub.label(text=item.render_type, icon=badge_icon)

        # Material count → 1
        mat_label = f"  {item.mat_count}→1" if item.mat_count >= 2 else f"  {item.mat_count} mat"
        sub.label(text=mat_label)

        # Resolution
        sub.prop(item, "resolution", text="")

        # Warning indicator
        if item.has_warnings:
            row.label(text="", icon="ERROR")


# ─────────────────────────────────────────────────────────────────
# Operators
# ─────────────────────────────────────────────────────────────────

class BF_UL_VRC_AtlasMaterials(UIList):
    """Displays selectable material slots found during Analyze."""

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        row = layout.row(align=True)
        row.prop(
            item,
            "enabled",
            text="",
            emboss=False,
            icon="CHECKBOX_HLT" if item.enabled else "CHECKBOX_DEHLT",
        )
        sub = row.row(align=True)
        sub.enabled = item.enabled
        warn_icon = "MATERIAL_DATA"
        if item.diagnostic_status == "unsupported_shader" or item.has_missing_image:
            warn_icon = "ERROR"
        elif item.diagnostic_warnings or item.duplicate_group or item.has_no_images or item.has_mixed_colorspace:
            warn_icon = "INFO"
        label = f"{item.object_name}[{item.slot_index}]  {item.material_name}"
        sub.label(text=label, icon=warn_icon)
        sub.label(text=item.render_type)
        sub.label(text=f"{item.texture_count} tex")
        if item.duplicate_group:
            sub.label(text=item.duplicate_group)


class BF_UL_VRC_AtlasTextures(UIList):
    """Displays selectable texture image nodes found during Analyze."""

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        row = layout.row(align=True)
        row.prop(
            item,
            "enabled",
            text="",
            emboss=False,
            icon="CHECKBOX_HLT" if item.enabled else "CHECKBOX_DEHLT",
        )
        sub = row.row(align=True)
        sub.enabled = item.enabled and not item.missing
        image_icon = "ERROR" if item.missing else "IMAGE_DATA"
        if not item.missing and item.diagnostic_warnings:
            image_icon = "INFO"
        size = f"{item.width}x{item.height}" if item.width and item.height else "missing"
        packed = "packed" if item.packed else "external"
        label = f"{item.material_name} / {item.node_name}: {item.image_name}"
        sub.label(text=label, icon=image_icon)
        sub.label(text=role_label(item.role))
        sub.label(text=size)
        sub.label(text=item.colorspace or packed)
        if item.duplicate_group:
            sub.label(text=item.duplicate_group)


class BF_OT_VRC_AtlasAnalyze(Operator):
    """Analyze scene materials and auto-group by render type"""
    bl_idname = "boneforge.vrc_atlas_analyze"
    bl_label = "Analyze Materials"
    bl_options = {"REGISTER"}

    def execute(self, context):
        settings = context.scene.boneforge_atlas_settings
        settings.atlas_groups.clear()
        settings.last_bake_result = ""
        settings.last_debug_report = ""

        meshes = _target_meshes(context, settings)

        if not meshes:
            self.report({"WARNING"}, "No mesh objects found")
            _store_debug_report(context, meshes, settings)
            return {"CANCELLED"}

        # Classify each mesh
        group_map = {rt: [] for rt in _RENDER_TYPES}
        total_mats = 0

        for obj in meshes:
            if not obj.data.materials:
                continue
            rt = _dominant_render_type(obj)
            group_map[rt].append(obj)
            total_mats += len(obj.data.materials)

        settings.total_mats_before = total_mats
        settings.rank_before = _get_rank(total_mats)

        # Create groups in priority order
        for rt in _RENDER_TYPES:
            objs = group_map[rt]
            if not objs:
                continue
            group = settings.atlas_groups.add()
            group.name = f"Group — {rt}"
            group.render_type = rt
            group.enabled = True
            group.resolution = "2048"

            mat_count = 0
            has_overlap = False
            has_high_em = False

            for obj in objs:
                item = group.meshes.add()
                item.object_name = obj.name
                item.render_type = rt
                item.mat_count = len(obj.data.materials)
                item.has_shape_keys = bool(obj.data.shape_keys)
                item.has_overlapping_uvs = _has_overlapping_uvs(obj)
                item.has_high_emission = _has_high_emission(obj)
                mat_count += len(obj.data.materials)
                if item.has_overlapping_uvs:
                    has_overlap = True
                if item.has_high_emission:
                    has_high_em = True

            group.mat_count = mat_count
            group.warn_overlap = has_overlap
            group.warn_emission = has_high_em
            group.has_warnings = (
                rt in ("Alpha Blend", "Emissive")
                or has_overlap
                or has_high_em
            )
            _populate_group_sources(group, objs)

        _store_debug_report(context, meshes, settings)
        projected = _projected_mat_count(settings)
        rank_after = _get_rank(projected)
        self.report(
            {"INFO"},
            f"Found {total_mats} materials in {len(settings.atlas_groups)} groups — "
            f"estimated result: {projected} mats ({rank_after})"
        )
        pipeline.append_ledger(
            context.scene,
            "atlas_analyze",
            pipeline.OUTCOME_CLEAN,
            f"Found {total_mats} materials in {len(settings.atlas_groups)} atlas groups",
        )
        return {"FINISHED"}


class BF_OT_VRC_AtlasAddGroup(Operator):
    """Add an empty atlas group"""
    bl_idname = "boneforge.vrc_atlas_add_group"
    bl_label = "Add Group"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        settings = context.scene.boneforge_atlas_settings
        group = settings.atlas_groups.add()
        group.name = f"Group {len(settings.atlas_groups)}"
        group.enabled = True
        group.resolution = "2048"
        settings.active_group_index = len(settings.atlas_groups) - 1
        return {"FINISHED"}


class BF_OT_VRC_AtlasRemoveGroup(Operator):
    """Remove the selected atlas group"""
    bl_idname = "boneforge.vrc_atlas_remove_group"
    bl_label = "Remove Group"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        settings = context.scene.boneforge_atlas_settings
        idx = settings.active_group_index
        if 0 <= idx < len(settings.atlas_groups):
            settings.atlas_groups.remove(idx)
            settings.active_group_index = max(0, idx - 1)
        return {"FINISHED"}


# ── Bake operator (with pre-flight invoke + modal progress) ──────

class BF_OT_VRC_AtlasSmartCombine(Operator):
    """Analyze and bake atlas materials with safe default settings"""
    bl_idname = "boneforge.vrc_atlas_smart_combine"
    bl_label = "Smart Combine Materials"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        settings = context.scene.boneforge_atlas_settings

        if settings.auto_analyze_before_bake or not settings.atlas_groups:
            analyze_result = bpy.ops.boneforge.vrc_atlas_analyze()
            if "FINISHED" not in analyze_result:
                self.report({"ERROR"}, "Smart Combine could not find materials to combine")
                return {"CANCELLED"}

        preflight = BF_OT_VRC_AtlasBake._build_preflight(context)
        if preflight["errors"]:
            for error in preflight["errors"]:
                self.report({"ERROR"}, error)
            _store_debug_report(context, _target_meshes(context, settings), settings)
            return {"CANCELLED"}

        try:
            bake_result = bpy.ops.boneforge.vrc_atlas_bake()
        except RuntimeError as bake_err:
            message = str(bake_err).splitlines()[-1] if str(bake_err) else "Smart Combine failed during bake"
            self.report({"ERROR"}, message)
            return {"CANCELLED"}
        if "FINISHED" not in bake_result:
            self.report({"ERROR"}, "Smart Combine failed during bake. Copy the debug report for details")
            return {"CANCELLED"}

        self.report({"INFO"}, "Smart Combine finished. Review the atlas, then Accept or Revert")
        return {"FINISHED"}


class BF_OT_VRC_AtlasCopyDebugReport(Operator):
    """Copy the latest atlas diagnostic report to the clipboard"""
    bl_idname = "boneforge.vrc_atlas_copy_debug"
    bl_label = "Copy Debug Report"
    bl_options = {"REGISTER"}

    def execute(self, context):
        settings = context.scene.boneforge_atlas_settings
        if not settings.last_debug_report:
            _store_debug_report(context, _target_meshes(context, settings), settings)

        if not settings.last_debug_report:
            self.report({"WARNING"}, "No atlas debug report available")
            return {"CANCELLED"}

        context.window_manager.clipboard = settings.last_debug_report
        self.report({"INFO"}, "Atlas debug report copied")
        return {"FINISHED"}


class BF_OT_VRC_AtlasBake(Operator):
    """Bake atlas textures for all enabled groups with pre-flight check"""
    bl_idname = "boneforge.vrc_atlas_bake"
    bl_label = "Bake Atlas"
    bl_options = {"REGISTER", "UNDO"}

    # Pre-flight dialog fields (shown in invoke dialog)
    _preflight_lines: list = []
    _groups_to_bake: list = []

    # ── Pre-flight helpers ────────────────────────────────────────

    @staticmethod
    def _build_preflight(context):
        """Collect pre-flight info lines and validate groups."""
        settings = context.scene.boneforge_atlas_settings
        lines_proceed = []
        lines_skip = []
        lines_change = []
        lines_stable = []
        errors = []

        bake_groups = []

        if settings.has_backup:
            errors.append("Accept or Revert the current atlas result before baking another atlas.")

        if not settings.bake_albedo:
            errors.append("Albedo (Color) must stay enabled so the atlas material has a base texture.")

        enabled_passes = _settings_enabled_passes(settings)
        all_texture_sources = []
        for group in settings.atlas_groups:
            all_texture_sources.extend(_group_texture_quality_sources(group))
        pass_plan = build_multipass_output_plan(
            enabled_passes,
            all_texture_sources,
            base_name="atlas",
            allow_unknown_roles=True,
        )
        for output in pass_plan["outputs"]:
            if output["role"] != ROLE_ALBEDO:
                lines_change.append(
                    f"  Extra output planned: {output['image_name']} ({output['label']})"
                )
        for skipped in pass_plan["skipped"]:
            lines_skip.append(
                f"  {skipped['reason']}; the pass will produce fallback bake data if selected"
            )
        if getattr(settings, "bake_metallic", False):
            errors.append(
                "Metallic atlas pass is not enabled yet: Blender has no direct metallic bake pass in this pipeline. "
                "Leave Metallic off until source-map channel packing is verified."
            )
        if getattr(settings, "channel_pack_orm", False):
            channel_plan = build_channel_pack_plan(
                all_texture_sources,
                allow_unknown_roles=getattr(settings, "allow_unknown_channel_pack_roles", False),
            )
            for channel, spec in CHANNEL_PACK_CONVENTION.items():
                lines_skip.append(
                    f"  ORM {channel}: {spec['label']} "
                    f"(fallback {channel_plan['channels'][channel]['fallback']})"
                )
            if channel_plan["errors"]:
                errors.extend(channel_plan["errors"])
            errors.append(
                "ORM channel packing is preflight-only in this build until the metallic source path is host-verified."
            )

        for group in settings.atlas_groups:
            if not group.enabled:
                lines_skip.append(f"  {group.name} — disabled by user")
                continue
            enabled_mats = _group_enabled_material_count(group)
            detected_mats = _group_detected_material_count(group)
            disabled_mats = max(0, detected_mats - enabled_mats)
            if enabled_mats < 2:
                lines_skip.append(
                    f"  {group.name} — only {enabled_mats} material "
                    f"(single-material groups have no effect)"
                )
                continue
            bake_groups.append(group)

            res = group.resolution
            vram = _vram_mb(res)
            lines_proceed.append(
                f"  {group.name}: {enabled_mats} of {detected_mats} materials → "
                f"atlas_{group.render_type.lower().replace(' ', '_')}_{res}px "
                f"({vram} MB VRAM)"
            )
            if disabled_mats:
                lines_skip.append(
                    f"    [i] {group.name}: {disabled_mats} material(s) excluded and kept separate"
                )
            disabled_textures = (
                len(group.textures) - _group_enabled_texture_count(group)
                if hasattr(group, "textures") else 0
            )
            if disabled_textures > 0:
                lines_skip.append(
                    f"    [i] {group.name}: {disabled_textures} texture image(s) excluded from the bake"
                )
            if getattr(group, "quality_summary", ""):
                lines_skip.append(f"    [i] {group.name}: {group.quality_summary}")
            for material_item in getattr(group, "materials", []):
                if not material_item.enabled:
                    continue
                if material_item.size_override or material_item.has_no_images:
                    source_width, source_height = _material_source_size(group, material_item)
                    size_plan = resolve_size_preset(
                        material_item.size_preset if material_item.size_override else "SOURCE",
                        source_width=source_width,
                        source_height=source_height,
                        custom_width=material_item.target_width,
                        custom_height=material_item.target_height,
                        fallback_size=material_item.fallback_size or settings.color_fallback_size,
                    )
                    if not size_plan["valid"]:
                        errors.append(
                            f"{material_item.material_name}: invalid texture size "
                            f"{size_plan['width']}x{size_plan['height']}"
                        )
                    lines_skip.append(
                        f"    [i] {material_item.material_name}: size plan "
                        f"{size_plan['width']}x{size_plan['height']} ({size_plan['preset']})"
                    )
            if group.warn_overlap:
                lines_skip.append(
                    f"    [!] {group.name} — overlapping UVs detected. "
                    f"Atlas UV will use {get_uv_method_label(settings.pack_method)}"
                )
            if group.warn_emission and settings.output_format != "EXR":
                lines_skip.append(
                    f"    [!] {group.name} — emission > 1.0 detected. "
                    f"Values will clamp to 1.0 in {settings.output_format}. "
                    f"Switch to EXR to preserve HDR emission"
                )

        if not bake_groups:
            errors.append("No groups with 2+ materials are enabled. Nothing to bake.")

        if settings.keep_source_uv_maps:
            lines_change.append(
                "  Atlas UV generated with selected UV method; source UV maps kept by advanced setting"
            )
            lines_skip.append(
                "    [!] Kept source UV maps can export atlas_uv as UV1 in FBX/Unity"
            )
        else:
            lines_change.append(
                "  Export UV set: atlas_uv becomes UV0; source UV maps removed from atlas mesh"
            )
        lines_change.append(
            "  Source textures forced to sample original UVs during bake"
        )
        lines_change.append(
            "  Atlas mesh validated before originals are hidden"
        )
        packing = packing_preset_settings(settings.packing_preset)
        lines_change.append(
            f"  Packing preset: {packing['label']} "
            f"(padding {settings.atlas_padding_pixels}px, margin {settings.uv_margin})"
        )
        lines_change.append(
            f"  Output material type: {_output_material_type_label(settings)}"
        )
        lines_change.append(
            f"  Output surface: {_output_surface_shader_label(settings)}"
        )
        after = sum(1 for g in bake_groups) + sum(
            _group_detected_material_count(g) for g in settings.atlas_groups
            if not g.enabled or _group_enabled_material_count(g) < 2
        ) + sum(
            max(0, _group_detected_material_count(g) - _group_enabled_material_count(g))
            for g in bake_groups
        )
        lines_change.append(
            f"  Material slots: {settings.total_mats_before} → ~{after}"
        )
        if settings.preserve_originals:
            lines_change.append(
                f"  Backup collection: {_BACKUP_COLLECTION_PREFIX}[timestamp] (visible)"
            )

        lines_stable.append("  Mesh geometry (no vertices moved)")
        lines_stable.append("  Object hierarchy and parent relationships")
        lines_stable.append("  Shape keys / blendshapes")

        return {
            "proceed": lines_proceed,
            "skip": lines_skip,
            "change": lines_change,
            "stable": lines_stable,
            "errors": errors,
            "bake_groups": bake_groups,
        }

    # ── Invoke: pre-flight dialog ─────────────────────────────────

    def invoke(self, context, event):
        settings = context.scene.boneforge_atlas_settings
        if not settings.atlas_groups:
            self.report({"ERROR"}, "Run Analyze first to detect material groups")
            return {"CANCELLED"}

        pf = self._build_preflight(context)
        self._preflight_lines = pf
        self._groups_to_bake = pf["bake_groups"]

        if pf["errors"]:
            for e in pf["errors"]:
                self.report({"ERROR"}, e)
            return {"CANCELLED"}

        return context.window_manager.invoke_props_dialog(self, width=520)

    def draw(self, context):
        """Draw the pre-flight dialog."""
        layout = self.layout
        pf = self._preflight_lines

        layout.label(text=T("ATLAS PRE-FLIGHT CHECK"), icon="VIEWZOOM")
        layout.separator()

        if pf.get("proceed"):
            layout.label(text=T("WILL BAKE:"))
            for line in pf["proceed"]:
                layout.label(text=line)
            layout.separator()

        if pf.get("skip"):
            layout.label(text=T("NOTES / WARNINGS:"))
            for line in pf["skip"]:
                layout.label(text=line, icon="INFO")
            layout.separator()

        if pf.get("change"):
            layout.label(text=T("WHAT WILL CHANGE:"))
            for line in pf["change"]:
                layout.label(text=line)
            layout.separator()

        if pf.get("stable"):
            layout.label(text=T("WHAT WILL NOT CHANGE:"), icon="CHECKMARK")
            for line in pf["stable"]:
                layout.label(text=line)

    # ── Execute: backup + bake ────────────────────────────────────

    def execute(self, context):
        settings = context.scene.boneforge_atlas_settings
        pf = self._build_preflight(context)
        bake_groups = pf["bake_groups"]
        if pf["errors"]:
            for e in pf["errors"]:
                self.report({"ERROR"}, e)
            pipeline.append_ledger(
                context.scene,
                "atlas_bake",
                pipeline.OUTCOME_FAILED,
                "; ".join(pf["errors"]),
            )
            self._groups_to_bake = []
            return {"CANCELLED"}
        self._preflight_lines = pf
        self._groups_to_bake = bake_groups

        _store_debug_report(context, _target_meshes(context, settings), settings)
        wm = context.window_manager
        total_steps = len(bake_groups)
        wm.progress_begin(0, total_steps)

        try:
            # Step 1 — backup originals
            if settings.preserve_originals:
                backup_name = _BACKUP_COLLECTION_PREFIX + str(int(time.time()))
                self._create_backup(context, bake_groups, backup_name)
                settings.backup_collection_name = backup_name
                settings.has_backup = True

            # Step 2 — bake each group
            mats_before = settings.total_mats_before
            mats_after_count = mats_before
            results = []

            for step, group in enumerate(bake_groups):
                wm.progress_update(step)
                result = self._bake_group(context, group, settings)
                if result:
                    results.append(result)
                    mats_after_count -= (_group_enabled_material_count(group) - 1)

            wm.progress_end()

            # Post-bake authority sentence (unanimous addition R)
            rank_before = _get_rank(mats_before)
            rank_after = _get_rank(mats_after_count)
            authority = (
                f"Baked {len(results)} atlas group(s). "
                f"Reduced from {mats_before} to {mats_after_count} materials — "
                f"rank: {rank_after}"
            )
            settings.last_bake_result = authority
            settings.total_mats_before = mats_after_count

            self.report({"INFO"}, authority)
            pipeline.append_ledger(
                context.scene,
                "atlas_bake",
                pipeline.OUTCOME_CHANGED,
                authority,
                {
                    "groups": len(results),
                    "scope": settings.target_scope,
                    "format": settings.output_format,
                    "output_path": settings.output_path,
                    "uv_method": settings.pack_method,
                },
            )
            pipeline.set_phase_complete(context.scene, "material_atlas", pipeline.OUTCOME_CHANGED)
            self._groups_to_bake = []

        except Exception as e:
            wm.progress_end()
            _cleanup_transient_atlas_objects()
            logger.exception("[BoneForge Atlas] Bake failed")
            self.report({"ERROR"}, f"Atlas bake failed: {e}")
            pipeline.append_ledger(
                context.scene,
                "atlas_bake",
                pipeline.OUTCOME_FAILED,
                f"Atlas bake failed: {e}",
            )
            pipeline.set_phase_complete(context.scene, "material_atlas", pipeline.OUTCOME_FAILED)
            return {"CANCELLED"}

        return {"FINISHED"}

    # ── Bake internals ────────────────────────────────────────────

    def _create_backup(self, context, bake_groups, backup_name):
        """Duplicate all target meshes into a visible backup collection."""
        scene = context.scene
        backup_coll = bpy.data.collections.new(backup_name)
        scene.collection.children.link(backup_coll)

        seen = set()
        for group in bake_groups:
            for item in group.meshes:
                if item.object_name in seen:
                    continue
                seen.add(item.object_name)
                obj = bpy.data.objects.get(item.object_name)
                if obj is None:
                    continue
                dup = obj.copy()
                dup.data = obj.data.copy()
                dup.name = f"PRE_ATLAS_{obj.name}"
                backup_coll.objects.link(dup)
                dup.hide_set(False)
                dup.hide_viewport = False
                dup.hide_render = False

        # Keep the backup collection visible so users can inspect the preserved duplicate.
        layer_coll = self._find_layer_collection(
            context.view_layer.layer_collection, backup_name
        )
        if layer_coll:
            layer_coll.hide_viewport = False
            layer_coll.exclude = False

    def _find_layer_collection(self, layer_coll, name):
        if layer_coll.name == name:
            return layer_coll
        for child in layer_coll.children:
            result = self._find_layer_collection(child, name)
            if result:
                return result
        return None

    def _bake_group(self, context, group, settings):
        """
        Bake one atlas group.

        Workflow:
        1. Collect mesh objects for this group
        2. Duplicate them into a working set
        3. Join into one mesh
        4. Preserve original UV as 'UVMap_pre_atlas'
        5. Create 'atlas_uv' UV map
        6. Smart UV Project → Pack Islands on joined mesh
        7. Create atlas Image
        8. Add Image Texture node (selected, unlinked) to each material
        9. Bake DIFFUSE with Cycles → atlas image
        10. Create new atlas material with Image Texture → BSDF
        11. Assign atlas material to the working mesh
        12. Reparent working mesh to armature (if present)
        13. Hide/remove original group meshes from view
        """
        res = int(group.resolution)
        arm = active_armature(context)
        scene = context.scene
        enabled_slots_by_obj = _enabled_slots_by_object(group)
        detected_slots_by_obj = _detected_slots_by_object(group)
        enabled_texture_keys = _enabled_texture_keys(group)

        # Collect source objects
        source_objs = []
        for item in group.meshes:
            obj = bpy.data.objects.get(item.object_name)
            if obj and obj.type == "MESH" and enabled_slots_by_obj.get(obj.name):
                source_objs.append(obj)

        if not source_objs:
            return None
        source_names = [obj.name for obj in source_objs]

        # ── Create working duplicates ──────────────────────────
        _ensure_object_mode(context, "Prepare atlas bake")
        _deselect_all_objects_directly(context.view_layer)
        work_objs = []
        keep_objs = []
        for obj in source_objs:
            detected_slots = detected_slots_by_obj.get(obj.name, set(range(len(obj.data.materials))))
            enabled_slots = enabled_slots_by_obj.get(obj.name, set())
            disabled_slots = set(detected_slots) - set(enabled_slots)

            if disabled_slots:
                keep = obj.copy()
                keep.data = obj.data.copy()
                _copy_material_slots(keep.data)
                keep.name = f"ATLAS_KEEP_{obj.name}"
                scene.collection.objects.link(keep)
                if not _remove_faces_by_material_slots(keep, set(enabled_slots)):
                    bpy.data.objects.remove(keep, do_unlink=True)
                else:
                    if arm:
                        keep.parent = arm
                    keep["boneforge_atlas_excluded_materials"] = json.dumps(sorted(disabled_slots))
                    keep_objs.append(keep)

            dup = obj.copy()
            dup.data = obj.data.copy()
            _copy_material_slots(dup.data)
            if not _remove_faces_by_material_slots(dup, disabled_slots):
                bpy.data.objects.remove(dup, do_unlink=True)
                continue
            for mat_index, mat in enumerate(dup.data.materials):
                if mat is not None:
                    original_mat = obj.data.materials[mat_index] if mat_index < len(obj.data.materials) else mat
                    original_name = original_mat.name if original_mat else mat.name
                    _disconnect_disabled_texture_nodes(
                        mat,
                        obj.name,
                        mat_index,
                        original_name,
                        enabled_texture_keys,
                    )
            dup.name = f"__BF_ATLAS_WORK_{obj.name}"
            scene.collection.objects.link(dup)
            dup.select_set(True)
            work_objs.append(dup)

        if not work_objs:
            for keep in keep_objs:
                bpy.data.objects.remove(keep, do_unlink=True)
            return None

        # ── Preserve original UV map ──────────────────────────
        for obj in work_objs:
            mesh = obj.data
            if mesh.uv_layers.active:
                original_uv = mesh.uv_layers.active
                if original_uv.name != "UVMap_pre_atlas":
                    original_uv.name = "UVMap_pre_atlas"

        # ── Join into one working mesh ────────────────────────
        _ensure_object_mode(context, "Prepare atlas join")
        _deselect_all_objects_directly(context.view_layer)
        for obj in work_objs:
            obj.select_set(True)
        context.view_layer.objects.active = work_objs[0]
        try:
            if len(work_objs) > 1:
                _run_with_view3d_context(context, bpy.ops.object.join, "Join atlas work meshes")
        except Exception as join_err:
            for w in work_objs:
                if w.name in bpy.data.objects:
                    bpy.data.objects.remove(w, do_unlink=True)
            for keep in keep_objs:
                if keep.name in bpy.data.objects:
                    bpy.data.objects.remove(keep, do_unlink=True)
            raise RuntimeError(f"Join failed — work objects cleaned up: {join_err}")
        joined = context.view_layer.objects.active
        joined.name = f"__BF_ATLAS_{group.render_type.replace(' ', '_')}"

        # ── Create atlas UV map ───────────────────────────────
        mesh = joined.data
        if "atlas_uv" in mesh.uv_layers:
            mesh.uv_layers.remove(mesh.uv_layers["atlas_uv"])
        atlas_uv = mesh.uv_layers.new(name="atlas_uv")

        # Bake into atlas_uv; copied source image nodes read UVMap_pre_atlas explicitly.
        for uv in mesh.uv_layers:
            uv.active_render = (uv.name == "atlas_uv")
        _activate_atlas_uv(mesh)

        # ── Smart UV Project → Pack Islands ───────────────────
        uv_result = apply_atlas_uv_method(context, joined, settings, _run_with_view3d_context)
        joined["boneforge_atlas_uv_method"] = uv_result["method"]
        joined["boneforge_atlas_uv_result"] = summarize_atlas_uv_result(uv_result)
        logger.info("[BoneForge Atlas] %s", joined["boneforge_atlas_uv_result"])

        # ── Create atlas image ────────────────────────────────
        atlas_name = (
            f"bf_atlas_{group.render_type.lower().replace(' ', '_')}_{res}px"
        )
        if atlas_name in bpy.data.images:
            bpy.data.images.remove(bpy.data.images[atlas_name])
        atlas_img = bpy.data.images.new(atlas_name, width=res, height=res, alpha=True)
        atlas_img.colorspace_settings.name = "sRGB"
        extra_images = {}
        output_render_type = _resolve_output_render_type(group, settings)

        # ── Add Image Texture node to each material ───────────
        source_uv_routes = 0
        for mat in joined.data.materials:
            if not mat or not mat.use_nodes:
                continue
            nodes = mat.node_tree.nodes
            source_uv_routes += _route_source_image_nodes_to_uv(mat, "UVMap_pre_atlas")
            # Remove any existing BF target node
            old = nodes.get("BF_ATLAS_TARGET")
            if old:
                nodes.remove(old)
            img_node = nodes.new("ShaderNodeTexImage")
            img_node.name = "BF_ATLAS_TARGET"
            img_node.image = atlas_img
            img_node.location = (-300, -400)
            # Must be selected and active — this is the bake target
            for n in nodes:
                n.select = False
            img_node.select = True
            nodes.active = img_node
        needs_alpha_atlas = _group_needs_alpha_atlas(joined, output_render_type)

        # ── Bake DIFFUSE ──────────────────────────────────────
        saved_engine = scene.render.engine
        scene.render.engine = "CYCLES"
        enabled_passes = set(_settings_enabled_passes(settings))

        try:
            context.view_layer.objects.active = joined
            _deselect_all_objects_directly(context.view_layer)
            joined.select_set(True)
            _run_with_view3d_context(
                context,
                bpy.ops.object.bake,
                "Bake atlas texture",
                type="DIFFUSE",
                pass_filter={"COLOR"},
                use_selected_to_active=False,
                margin=settings.atlas_padding_pixels,
                use_clear=True,
            )
            if needs_alpha_atlas:
                _bake_alpha_mask_to_atlas(context, joined, atlas_img, settings, atlas_name, res)
            for role, spec in _EXTRA_BAKE_PASSES.items():
                if role not in enabled_passes:
                    continue
                pass_name = f"{atlas_name}{spec['suffix']}"
                if pass_name in bpy.data.images:
                    bpy.data.images.remove(bpy.data.images[pass_name])
                pass_img = bpy.data.images.new(pass_name, width=res, height=res, alpha=True)
                pass_img.colorspace_settings.name = spec["colorspace"]
                for mat in joined.data.materials:
                    if not mat or not mat.use_nodes:
                        continue
                    nodes = mat.node_tree.nodes
                    target = nodes.get("BF_ATLAS_TARGET")
                    if target is None:
                        continue
                    target.image = pass_img
                    for node in nodes:
                        node.select = False
                    target.select = True
                    nodes.active = target
                _run_with_view3d_context(
                    context,
                    bpy.ops.object.bake,
                    f"Bake {role_label(role)} atlas",
                    type=spec["type"],
                    use_selected_to_active=False,
                    margin=settings.atlas_padding_pixels,
                    use_clear=True,
                )
                extra_images[role] = pass_img
            for mat in joined.data.materials:
                if mat and mat.use_nodes and mat.node_tree:
                    target = mat.node_tree.nodes.get("BF_ATLAS_TARGET")
                    if target is not None:
                        target.image = atlas_img
        except Exception as bake_err:
            scene.render.engine = saved_engine
            logger.warning("[BoneForge Atlas] Cycles bake failed for %s: %s", group.name, bake_err)
            raise
        scene.render.engine = saved_engine

        keep_source_uv_maps = getattr(settings, "keep_source_uv_maps", False)
        _prepare_atlas_uv_for_export(joined.data, keep_source_uv_maps)

        # ── Save atlas image ──────────────────────────────────
        out_dir = bpy.path.abspath(settings.output_path)
        if out_dir and not os.path.isdir(out_dir):
            try:
                os.makedirs(out_dir, exist_ok=True)
            except OSError:
                out_dir = ""

        fmt_ext = {"PNG": ".png", "TGA": ".tga", "EXR": ".exr"}
        ext = fmt_ext.get(settings.output_format, ".png")
        if out_dir:
            img_path = os.path.join(out_dir, atlas_name + ext)
            atlas_img.filepath_raw = img_path
            atlas_img.file_format = settings.output_format
            try:
                atlas_img.save()
            except Exception as save_err:
                logger.warning(f"[BoneForge Atlas] Could not save image: {save_err}")
            for role, image in extra_images.items():
                image.filepath_raw = os.path.join(out_dir, image.name + ext)
                image.file_format = settings.output_format
                try:
                    image.save()
                except Exception as save_err:
                    logger.warning(
                        "[BoneForge Atlas] Could not save %s atlas: %s",
                        role_label(role),
                        save_err,
                    )

        # ── Build atlas material ──────────────────────────────
        mat_name = f"M_{atlas_name}"
        if mat_name in bpy.data.materials:
            bpy.data.materials.remove(bpy.data.materials[mat_name])
        atlas_mat = bpy.data.materials.new(mat_name)
        atlas_mat.use_nodes = True
        # Set blend mode to match the selected output render type.
        if output_render_type == "Alpha Blend":
            atlas_mat.blend_method = "BLEND"
        elif output_render_type == "Alpha Clip":
            atlas_mat.blend_method = "CLIP"
        else:
            atlas_mat.blend_method = "OPAQUE"

        nodes = atlas_mat.node_tree.nodes
        links = atlas_mat.node_tree.links
        nodes.clear()
        output_node = nodes.new("ShaderNodeOutputMaterial")
        output_node.location = (520, 0)
        tex_node = nodes.new("ShaderNodeTexImage")
        tex_node.name = "Atlas"
        tex_node.image = atlas_img
        tex_node.location = (-300, 0)
        uv_node = nodes.new("ShaderNodeUVMap")
        uv_node.uv_map = "atlas_uv"
        uv_node.location = (-550, 0)
        links.new(uv_node.outputs["UV"], tex_node.inputs["Vector"])

        output_surface_shader = _resolve_output_surface_shader(settings)
        if output_surface_shader == "DIFFUSE":
            surface_node = nodes.new("ShaderNodeBsdfDiffuse")
            surface_node.name = "Atlas Diffuse Surface"
            surface_shader_output = _node_output(surface_node, "BSDF")
        elif output_surface_shader == "EMISSION":
            surface_node = nodes.new("ShaderNodeEmission")
            surface_node.name = "Atlas Emission Surface"
            surface_shader_output = _node_output(surface_node, "Emission")
            strength_input = _node_input(surface_node, "Strength")
            if strength_input is not None and hasattr(strength_input, "default_value"):
                strength_input.default_value = 1.0
        elif output_surface_shader == "TRANSPARENT":
            surface_node = nodes.new("ShaderNodeBsdfTransparent")
            surface_node.name = "Atlas Transparent Surface"
            surface_shader_output = _node_output(surface_node, "BSDF")
        else:
            surface_node = nodes.new("ShaderNodeBsdfPrincipled")
            surface_node.name = "Atlas Principled Surface"
            surface_shader_output = _node_output(surface_node, "BSDF")
        surface_node.location = (0, 0)

        surface_color_input = _node_input(surface_node, "Base Color", "Color")
        if surface_color_input is not None and not (
            output_surface_shader == "EMISSION" and ROLE_EMISSION in extra_images
        ):
            links.new(tex_node.outputs["Color"], surface_color_input)

        if ROLE_NORMAL in extra_images:
            normal_input = _node_input(surface_node, "Normal")
            normal_tex = nodes.new("ShaderNodeTexImage")
            normal_tex.name = "Atlas Normal"
            normal_tex.image = extra_images[ROLE_NORMAL]
            normal_tex.location = (-300, -250)
            normal_map = nodes.new("ShaderNodeNormalMap")
            normal_map.location = (0, -250)
            links.new(uv_node.outputs["UV"], normal_tex.inputs["Vector"])
            links.new(normal_tex.outputs["Color"], normal_map.inputs["Color"])
            if normal_input is not None:
                links.new(normal_map.outputs["Normal"], normal_input)
        if ROLE_EMISSION in extra_images:
            emission_tex = nodes.new("ShaderNodeTexImage")
            emission_tex.name = "Atlas Emission"
            emission_tex.image = extra_images[ROLE_EMISSION]
            emission_tex.location = (-300, -500)
            links.new(uv_node.outputs["UV"], emission_tex.inputs["Vector"])
            if output_surface_shader == "EMISSION":
                emission_input = _node_input(surface_node, "Color")
                emission_strength = _node_input(surface_node, "Strength")
            elif output_surface_shader == "PRINCIPLED":
                emission_input = _node_input(surface_node, "Emission Color", "Emission")
                emission_strength = _node_input(surface_node, "Emission Strength")
            else:
                emission_input = None
                emission_strength = None
            if emission_input is not None:
                links.new(emission_tex.outputs["Color"], emission_input)
            if emission_strength is not None and hasattr(emission_strength, "default_value"):
                emission_strength.default_value = 1.0
        elif output_render_type == "Emissive" and output_surface_shader == "PRINCIPLED":
            emission_input = _node_input(surface_node, "Emission Color", "Emission")
            emission_strength = _node_input(surface_node, "Emission Strength")
            if emission_input is not None:
                links.new(tex_node.outputs["Color"], emission_input)
            if emission_strength is not None and hasattr(emission_strength, "default_value"):
                emission_strength.default_value = 1.0
        if ROLE_ROUGHNESS in extra_images:
            roughness_tex = nodes.new("ShaderNodeTexImage")
            roughness_tex.name = "Atlas Roughness"
            roughness_tex.image = extra_images[ROLE_ROUGHNESS]
            roughness_tex.location = (-300, -750)
            links.new(uv_node.outputs["UV"], roughness_tex.inputs["Vector"])
            roughness_input = _node_input(surface_node, "Roughness")
            if roughness_input is not None:
                links.new(roughness_tex.outputs["Color"], roughness_input)

        surface_output = surface_shader_output
        if output_render_type in ("Alpha Blend", "Alpha Clip"):
            alpha_input = _node_input(surface_node, "Alpha")
            if alpha_input is not None:
                links.new(tex_node.outputs["Alpha"], alpha_input)
            elif output_surface_shader != "TRANSPARENT" and surface_shader_output is not None:
                transparent_node = nodes.new("ShaderNodeBsdfTransparent")
                transparent_node.name = "Atlas Alpha Transparent"
                transparent_node.location = (0, -220)
                mix_node = nodes.new("ShaderNodeMixShader")
                mix_node.name = "Atlas Alpha Surface Mix"
                mix_node.location = (260, -80)
                links.new(tex_node.outputs["Alpha"], mix_node.inputs[0])
                links.new(transparent_node.outputs["BSDF"], mix_node.inputs[1])
                links.new(surface_shader_output, mix_node.inputs[2])
                surface_output = _node_output(mix_node, "Shader")
        if surface_output is not None:
            links.new(surface_output, output_node.inputs["Surface"])

        # ── Assign atlas material to joined mesh ──────────────
        _assign_single_atlas_material(joined.data, atlas_mat)
        _validate_atlas_mesh(joined, atlas_mat)

        # ── Reparent to armature if present ──────────────────
        if arm:
            joined.parent = arm
            armature_mod = joined.modifiers.get("Armature")
            if not armature_mod:
                armature_mod = joined.modifiers.new("Armature", "ARMATURE")
            armature_mod.object = arm

        # ── Hide original source objects ──────────────────────
        for obj in source_objs:
            if settings.preserve_originals:
                obj.hide_set(True)
                obj.hide_render = True
            else:
                bpy.data.objects.remove(obj, do_unlink=True)

        # Clean up working name
        joined.name = (
            f"ATLAS_{group.render_type.replace(' ', '_')}_{res}px"
        )
        joined["boneforge_atlas_backup"] = settings.backup_collection_name
        joined["boneforge_atlas_sources"] = json.dumps(source_names)
        joined["boneforge_atlas_source_uv_routes"] = source_uv_routes
        joined["boneforge_atlas_uv0"] = "atlas_uv"
        joined["boneforge_atlas_source_uv_maps_kept"] = bool(keep_source_uv_maps)
        joined["boneforge_atlas_output_material_type"] = output_render_type
        joined["boneforge_atlas_output_material_mode"] = getattr(
            settings,
            "output_material_type",
            "AUTO",
        )
        joined["boneforge_atlas_output_surface_shader"] = output_surface_shader
        joined["boneforge_atlas_output_surface_mode"] = getattr(
            settings,
            "output_surface_shader",
            "AUTO",
        )
        joined["boneforge_atlas_outputs"] = json.dumps(
            {role: image.name for role, image in extra_images.items()}
        )
        for keep in keep_objs:
            keep.name = keep.name.replace("ATLAS_KEEP_", "KEPT_", 1)
            keep["boneforge_atlas_backup"] = settings.backup_collection_name
            keep["boneforge_atlas_source_group"] = group.name

        return joined.name


class BF_OT_VRC_AtlasAccept(Operator):
    """Accept atlas result and permanently delete the original backup"""
    bl_idname = "boneforge.vrc_atlas_accept"
    bl_label = "Accept — Delete Backup"
    bl_options = {"REGISTER", "UNDO"}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(
            self,
            event,
        )

    def execute(self, context):
        settings = context.scene.boneforge_atlas_settings
        if not settings.has_backup:
            self.report({"WARNING"}, "No backup to delete")
            return {"CANCELLED"}

        coll = bpy.data.collections.get(settings.backup_collection_name)
        source_names = set()
        for obj in context.scene.objects:
            if obj.get("boneforge_atlas_backup") != settings.backup_collection_name:
                continue
            raw_sources = obj.get("boneforge_atlas_sources", "[]")
            try:
                source_names.update(json.loads(raw_sources))
            except (TypeError, ValueError):
                pass

        for name in source_names:
            obj = bpy.data.objects.get(name)
            if obj is not None:
                bpy.data.objects.remove(obj, do_unlink=True)

        if coll:
            # Remove all objects in collection
            for obj in list(coll.objects):
                bpy.data.objects.remove(obj, do_unlink=True)
            bpy.data.collections.remove(coll)

        settings.has_backup = False
        settings.backup_collection_name = ""
        self.report({"INFO"}, "Backup deleted — atlas accepted")
        return {"FINISHED"}


class BF_OT_VRC_AtlasRevert(Operator):
    """Revert to original meshes from backup, removing atlas result"""
    bl_idname = "boneforge.vrc_atlas_revert"
    bl_label = "Revert — Restore Originals"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        settings = context.scene.boneforge_atlas_settings
        if not settings.has_backup:
            self.report({"WARNING"}, "No backup to restore from")
            return {"CANCELLED"}

        coll = bpy.data.collections.get(settings.backup_collection_name)
        if not coll:
            self.report({"ERROR"}, f"Backup collection not found: {settings.backup_collection_name}")
            settings.has_backup = False
            return {"CANCELLED"}

        # Remove atlas meshes created by this backup/session.
        scene = context.scene
        to_remove = [
            obj for obj in scene.objects
            if obj.get("boneforge_atlas_backup") == settings.backup_collection_name
        ]
        for obj in to_remove:
            bpy.data.objects.remove(obj, do_unlink=True)

        # Restore originals first; backup duplicates are a fallback if a source was removed.
        for obj in list(coll.objects):
            orig_name = obj.name.replace("PRE_ATLAS_", "", 1)
            original = bpy.data.objects.get(orig_name)
            if original is not None:
                original.hide_set(False)
                original.hide_render = False
                bpy.data.objects.remove(obj, do_unlink=True)
                continue

            obj.name = orig_name
            try:
                scene.collection.objects.link(obj)
            except RuntimeError:
                pass
            obj.hide_set(False)
            obj.hide_render = False

        bpy.data.collections.remove(coll)

        settings.has_backup = False
        settings.backup_collection_name = ""
        settings.last_bake_result = ""
        self.report({"INFO"}, "Reverted to original meshes")
        return {"FINISHED"}


# ─────────────────────────────────────────────────────────────────
# Panel — Zone 1 / 2 / 3 layout
# ─────────────────────────────────────────────────────────────────

class BONEFORGE_PT_vrc_w2_atlas(Panel):
    """Material Atlas Combiner — beneath VRC Cats Tools in Rig Mapping."""

    bl_label = " "
    bl_idname = "BONEFORGE_PT_vrc_w2_atlas"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'scene'
    bl_options = {"DEFAULT_CLOSED"}

    def draw_header(self, context):
        self.layout.label(text=T("Material Atlas"))

    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def draw(self, context):
        layout = self.layout
        settings = context.scene.boneforge_atlas_settings

        # ── ZONE 1 — Status Dashboard ─────────────────────────
        status_box = layout.box()
        col = status_box.column(align=True)

        # D-Shadow declarative sentence
        sentence = _build_status_sentence(settings)
        col.label(text=sentence, icon="INFO")

        # Second line — guarantee sentence (unanimous addition S / D-Shadow)
        if settings.atlas_groups:
            guarantee = _will_not_change_sentence(settings)
            col.label(text=guarantee, icon="CHECKMARK")

        # Post-bake authority sentence (unanimous addition R)
        if settings.last_bake_result:
            result_row = col.row()
            result_row.alert = False
            col.separator()
            col.label(text=settings.last_bake_result, icon="CHECKMARK")

        # Material count + rank display
        if settings.total_mats_before > 0:
            col.separator()
            after = _projected_mat_count(settings)
            rank_before = settings.rank_before or _get_rank(settings.total_mats_before)
            rank_after = _get_rank(after)

            row = col.row(align=True)
            row.label(text=f"Now:  {settings.total_mats_before} mats  [{rank_before}]")
            row.label(text=f"→  {after} mats  [{rank_after}]")

        col.separator()
        col.prop(settings, "target_scope")
        smart_row = col.row()
        smart_row.scale_y = 1.35
        smart_row.operator(
            "boneforge.vrc_atlas_smart_combine",
            text=T("Smart Combine Materials"),
            icon="MATERIAL",
        )

        tool_row = col.row(align=True)
        tool_row.operator("boneforge.vrc_atlas_analyze", text=T("Analyze"), icon="VIEWZOOM")
        tool_row.operator("boneforge.vrc_atlas_copy_debug", text=T("Copy Debug"), icon="COPYDOWN")
        backup_row = col.row(align=True)
        backup_row.prop(settings, "preserve_originals", text=T("Preserve Backup Duplicate"))
        if not settings.preserve_originals:
            col.label(
                text=T("Off: no Revert backup; originals are removed after atlasing"),
                icon="ERROR",
            )
        if settings.has_backup:
            accept_row = col.row(align=True)
            accept_row.alert = True
            accept_row.operator(
                "boneforge.vrc_atlas_accept",
                text=T("Accept — Delete Backup"),
                icon="TRASH",
            )
            accept_row.alert = False
            revert_row = col.row(align=True)
            revert_row.operator(
                "boneforge.vrc_atlas_revert",
                text=T("Revert — Restore Originals"),
                icon="LOOP_BACK",
            )

        layout.separator()

        # ── ZONE 2 — Grouping Control ─────────────────────────
        if settings.atlas_groups:
            layout.label(text=T("Atlas Groups:"))

            # UIList
            row = layout.row()
            row.template_list(
                "BF_UL_VRC_AtlasGroups", "",
                settings, "atlas_groups",
                settings, "active_group_index",
                rows=4,
            )

            # Group list buttons
            btn_col = row.column(align=True)
            btn_col.operator("boneforge.vrc_atlas_add_group", text="", icon="ADD")
            btn_col.operator("boneforge.vrc_atlas_remove_group", text="", icon="REMOVE")

            # Expanded group detail
            idx = settings.active_group_index
            if 0 <= idx < len(settings.atlas_groups):
                active_group = settings.atlas_groups[idx]
                detail_box = layout.box()
                dcol = detail_box.column(align=True)

                if active_group.warn_overlap:
                    dcol.label(
                        text=T("[!] Overlapping UVs detected - atlas_uv will use the selected UV method"),
                        icon="ERROR",
                    )
                    dcol.label(
                        text=T("     (original UVs preserved as 'UVMap_pre_atlas')"),
                        icon="BLANK1",
                    )

                if active_group.warn_emission and settings.output_format != "EXR":
                    dcol.label(
                        text=T("[!] Emission > 1.0 detected — values will clamp in PNG/TGA"),
                        icon="LIGHT_SUN",
                    )
                    dcol.label(
                        text=T("     Switch output to EXR in Advanced to preserve HDR"),
                        icon="BLANK1",
                    )

                if active_group.render_type in ("Alpha Blend", "Emissive"):
                    dcol.label(
                        text=f"[i] {active_group.render_type} — kept in separate group",
                        icon="INFO",
                    )
                    dcol.label(
                        text=T("     Mixing with Opaque breaks VRChat render order"),
                        icon="BLANK1",
                    )

                if not active_group.warn_overlap and not active_group.warn_emission and \
                        active_group.render_type not in ("Alpha Blend", "Emissive"):
                    dcol.label(
                        text=f"{_group_enabled_material_count(active_group)} materials → 1 atlas at {active_group.resolution}px",
                        icon="CHECKMARK",
                    )

                # Meshes in this group
                if active_group.meshes:
                    dcol.separator()
                    dcol.label(text=T("Meshes in group:"))
                    for item in active_group.meshes:
                        mesh_row = dcol.row(align=True)
                        icon = "MESH_DATA"
                        if item.has_shape_keys:
                            icon = "SHAPEKEY_DATA"
                        mesh_row.label(text=f"  {item.object_name}", icon=icon)
                        mesh_row.label(text=f"{item.mat_count} mats")
                        if item.has_shape_keys:
                            mesh_row.label(text=T("[SK]"))
                        if item.has_overlapping_uvs:
                            mesh_row.label(text=T("[UV!]"))

                if active_group.materials:
                    dcol.separator()
                    enabled_mats = _group_enabled_material_count(active_group)
                    dcol.label(
                        text=T(
                            f"Materials to combine: {enabled_mats}/{len(active_group.materials)}"
                        ),
                        icon="MATERIAL_DATA",
                    )
                    dcol.template_list(
                        "BF_UL_VRC_AtlasMaterials", "",
                        active_group, "materials",
                        active_group, "active_material_index",
                        rows=5,
                    )
                    mat_idx = active_group.active_material_index
                    if 0 <= mat_idx < len(active_group.materials):
                        mat_item = active_group.materials[mat_idx]
                        mat_detail = dcol.box()
                        mat_detail.label(text=T("Selected Material:"), icon="MATERIAL_DATA")
                        mat_detail.label(text=mat_item.diagnostic_status or "supported")
                        if mat_item.diagnostic_warnings:
                            mat_detail.label(text=mat_item.diagnostic_warnings, icon="INFO")
                        if mat_item.duplicate_group:
                            mat_detail.label(text=f"Duplicate/shared group: {mat_item.duplicate_group}", icon="COPYDOWN")
                        size_row = mat_detail.row(align=True)
                        size_row.prop(mat_item, "size_override")
                        size_row.prop(mat_item, "size_preset", text="")
                        if mat_item.size_override and mat_item.size_preset == "CUSTOM":
                            custom_row = mat_detail.row(align=True)
                            custom_row.prop(mat_item, "target_width")
                            custom_row.prop(mat_item, "target_height")
                        if mat_item.has_no_images:
                            mat_detail.prop(mat_item, "fallback_size")

                if active_group.textures:
                    dcol.separator()
                    enabled_tex = _group_enabled_texture_count(active_group)
                    dcol.label(
                        text=T(
                            f"Texture images: {enabled_tex}/{len(active_group.textures)}"
                        ),
                        icon="IMAGE_DATA",
                    )
                    dcol.template_list(
                        "BF_UL_VRC_AtlasTextures", "",
                        active_group, "textures",
                        active_group, "active_texture_index",
                        rows=5,
                    )
                    tex_idx = active_group.active_texture_index
                    if 0 <= tex_idx < len(active_group.textures):
                        tex_item = active_group.textures[tex_idx]
                        tex_detail = dcol.box()
                        tex_detail.label(text=T("Selected Texture:"), icon="IMAGE_DATA")
                        tex_detail.prop(tex_item, "role")
                        tex_detail.label(text=f"Expected: {role_color_space(tex_item.role)}")
                        if tex_item.diagnostic_warnings:
                            tex_detail.label(text=tex_item.diagnostic_warnings, icon="INFO")
                        if tex_item.duplicate_group:
                            tex_detail.label(text=f"Duplicate source group: {tex_item.duplicate_group}", icon="COPYDOWN")

            # Permanent transparency note (unanimous addition S)
            layout.separator()
            note_row = layout.row()
            note_row.label(
                text=T("Transparent / emissive materials kept in separate groups by default."),
                icon="INFO",
            )

            layout.separator()

            # Primary action
            bake_row = layout.row()
            bake_row.scale_y = 1.4
            bake_row.operator("boneforge.vrc_atlas_bake", text=T("Bake Atlas"), icon="RENDER_STILL")

        # ── ZONE 3 — Advanced Options ─────────────────────────
        adv_box = layout.box()
        adv_header = adv_box.row()
        adv_header.prop(
            settings, "show_advanced",
            text=T("Override Inherited Settings"),
            icon="TRIA_DOWN" if settings.show_advanced else "TRIA_RIGHT",
            emboss=False,
        )

        if settings.show_advanced:
            adv_col = adv_box.column(align=True)

            adv_col.label(text=T("Workflow:"))
            adv_col.prop(settings, "auto_analyze_before_bake")
            adv_col.prop(settings, "debug_enabled")
            adv_col.operator("boneforge.vrc_atlas_copy_debug", text=T("Copy Debug Report"), icon="COPYDOWN")
            adv_col.separator()

            adv_col.label(text=T("Bake Passes:"))
            adv_col.prop(settings, "bake_albedo")
            adv_col.prop(settings, "bake_normal")
            emission_row = adv_col.row()
            emission_row.prop(settings, "bake_emission")
            adv_col.prop(settings, "bake_metallic")
            adv_col.prop(settings, "bake_roughness")
            adv_col.prop(settings, "channel_pack_orm")
            if settings.channel_pack_orm:
                adv_col.prop(settings, "allow_unknown_channel_pack_roles")
                adv_col.label(text=T("ORM is blocked until metallic packing is verified."), icon="INFO")
            if settings.bake_metallic:
                adv_col.label(text=T("Metallic pass is preflight-blocked in this build."), icon="ERROR")

            adv_col.separator()
            adv_col.label(text=T("UV Packing:"))
            adv_col.prop(settings, "packing_preset")
            adv_col.prop(settings, "uv_margin")
            adv_col.prop(settings, "atlas_padding_pixels")
            adv_col.prop(settings, "pixel_art_no_bleed")
            adv_col.prop(settings, "preserve_island_orientation")
            adv_col.prop(settings, "keep_source_uv_maps")
            adv_col.prop(settings, "pack_method")
            if method_uses_seed(settings.pack_method):
                adv_col.prop(settings, "uv_random_seed")
                adv_col.prop(settings, "uv_rotation_step")

            adv_col.separator()
            adv_col.label(text=T("Output:"))
            adv_col.prop(settings, "color_fallback_size", text=T("Fallback Size"))
            adv_col.prop(settings, "output_format", text=T("Format Output"))
            adv_col.prop(settings, "output_material_type", text=T("Material Output Type"))
            adv_col.prop(settings, "output_surface_shader", text=T("Surface Output"))
            if settings.output_format == "EXR":
                adv_col.label(
                    text=T("EXR preserves HDR emission — use for glow accessories"),
                    icon="INFO",
                )
            adv_col.prop(settings, "output_path", text=T("Path Output"))



# ─────────────────────────────────────────────────────────────────
# Registration
# ─────────────────────────────────────────────────────────────────

_classes = (
    BF_AtlasMeshItem,
    BF_AtlasMaterialItem,
    BF_AtlasTextureItem,
    BF_AtlasGroup,
    BF_AtlasSettings,
    BF_UL_VRC_AtlasGroups,
    BF_UL_VRC_AtlasMaterials,
    BF_UL_VRC_AtlasTextures,
    BF_OT_VRC_AtlasAnalyze,
    BF_OT_VRC_AtlasAddGroup,
    BF_OT_VRC_AtlasRemoveGroup,
    BF_OT_VRC_AtlasSmartCombine,
    BF_OT_VRC_AtlasCopyDebugReport,
    BF_OT_VRC_AtlasBake,
    BF_OT_VRC_AtlasAccept,
    BF_OT_VRC_AtlasRevert,
)


def register():
    for cls in _classes:
        try:
            bpy.utils.register_class(cls)
        except RuntimeError as e:
            logger.error(f"[BoneForge Atlas] Failed to register {cls.__name__}: {e}")

    bpy.types.Scene.boneforge_atlas_settings = bpy.props.PointerProperty(
        type=BF_AtlasSettings
    )


def unregister():
    if hasattr(bpy.types.Scene, "boneforge_atlas_settings"):
        del bpy.types.Scene.boneforge_atlas_settings

    for cls in reversed(_classes):
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError as e:
            logger.error(f"[BoneForge Atlas] Failed to unregister {cls.__name__}: {e}")
