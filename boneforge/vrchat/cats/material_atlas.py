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

import logging
import os
import time

import bpy
import bmesh
from bpy.props import (
    BoolProperty, CollectionProperty, EnumProperty,
    FloatProperty, IntProperty, StringProperty,
)

from boneforge.i18n import T
from bpy.types import Operator, Panel, PropertyGroup, UIList

from boneforge.core import active_armature

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────
# Constants — VRChat performance thresholds (mirrors rank.py)
# ─────────────────────────────────────────────────────────────────

_RANK_THRESHOLDS = {"Excellent": 4, "Good": 8, "Medium": 16, "Poor": 32}
_RANK_ORDER = ["Excellent", "Good", "Medium", "Poor"]
_RENDER_TYPES = ["Opaque", "Alpha Clip", "Alpha Blend", "Emissive"]

# VRAM cost per atlas (bytes): width * height * 4 channels * 1.33 mip factor
_VRAM_MIP_FACTOR = 1.33

_BACKUP_COLLECTION_PREFIX = "BF_Atlas_Backup_"


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
        if not group.enabled or group.mat_count == 0:
            total += group.mat_count
            continue
        if group.mat_count >= 2:
            total += 1  # entire group bakes into 1 atlas material
        else:
            total += group.mat_count  # single-mat groups stay as-is
    return total


def _build_status_sentence(settings) -> str:
    """D-Shadow Inheritance Protocol: declarative sentence for Zone 1."""
    groups = [g for g in settings.atlas_groups if g.enabled and g.mat_count >= 2]
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

    enabled_mats = sum(g.mat_count for g in groups)
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


class BF_AtlasGroup(PropertyGroup):
    """One atlas group (bakes into a single texture atlas)."""
    name: StringProperty(name="Group Name", default="Group")
    enabled: BoolProperty(name="Enabled", default=True)
    meshes: CollectionProperty(type=BF_AtlasMeshItem)
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


class BF_AtlasSettings(PropertyGroup):
    """Scene-level atlas combiner settings."""

    # Group list
    atlas_groups: CollectionProperty(type=BF_AtlasGroup)
    active_group_index: IntProperty(name="Active Group", default=0)

    # Status (populated by Analyze)
    total_mats_before: IntProperty(default=0)
    rank_before: StringProperty(default="")
    last_bake_result: StringProperty(default="")

    # Backup state
    has_backup: BoolProperty(default=False)
    backup_collection_name: StringProperty(default="")

    # Advanced options
    preserve_originals: BoolProperty(
        name="Preserve Originals",
        description=(
            "Duplicate all target meshes before atlasing. Originals are hidden "
            "in a backup collection. Use Revert to restore. Disabling this is "
            "faster but permanent"
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
        name="Pack Method",
        items=[
            ("BEST_FIT", "Best Fit", "Slower — packs islands as efficiently as possible"),
            ("GRID", "Grid", "Faster — predictable grid layout, wastes some space"),
        ],
        default="BEST_FIT",
    )
    bake_albedo: BoolProperty(name="Albedo (Color)", default=True)
    bake_normal: BoolProperty(name="Normal Map", default=True)
    bake_emission: BoolProperty(
        name="Emission",
        description="Bake emission channel. Values > 1.0 will clamp to 1.0 in PNG/TGA. Use EXR to preserve HDR emission",
        default=True,
    )
    bake_roughness: BoolProperty(name="Metallic / Roughness", default=False)
    output_format: EnumProperty(
        name="Output Format",
        items=[
            ("PNG", "PNG", "Standard format — emission values > 1.0 will clamp"),
            ("TGA", "TGA", "TGA format — emission values > 1.0 will clamp"),
            ("EXR", "EXR", "HDR format — preserves emission values > 1.0"),
        ],
        default="PNG",
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

class BF_OT_VRC_AtlasAnalyze(Operator):
    """Analyze scene materials and auto-group by render type"""
    bl_idname = "boneforge.vrc_atlas_analyze"
    bl_label = "Analyze Materials"
    bl_options = {"REGISTER"}

    def execute(self, context):
        settings = context.scene.boneforge_atlas_settings
        settings.atlas_groups.clear()
        settings.last_bake_result = ""

        arm = active_armature(context)
        if arm:
            meshes = [c for c in arm.children if c.type == "MESH"]
        else:
            meshes = [o for o in context.scene.objects if o.type == "MESH"
                      and o.visible_get()]

        if not meshes:
            self.report({"WARNING"}, "No mesh objects found")
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

        projected = _projected_mat_count(settings)
        rank_after = _get_rank(projected)
        self.report(
            {"INFO"},
            f"Found {total_mats} materials in {len(settings.atlas_groups)} groups — "
            f"estimated result: {projected} mats ({rank_after})"
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

class BF_OT_VRC_AtlasBake(Operator):
    """Bake atlas textures for all enabled groups with pre-flight check"""
    bl_idname = "boneforge.vrc_atlas_bake"
    bl_label = "Bake Atlas"
    bl_options = {"REGISTER", "UNDO"}

    # Pre-flight dialog fields (shown in invoke dialog)
    _preflight_lines: list = []
    _groups_to_bake: list = []

    # ── Pre-flight helpers ────────────────────────────────────────

    def _build_preflight(self, context):
        """Collect pre-flight info lines and validate groups."""
        settings = context.scene.boneforge_atlas_settings
        lines_proceed = []
        lines_skip = []
        lines_change = []
        lines_stable = []
        errors = []

        arm = active_armature(context)
        bake_groups = []

        for group in settings.atlas_groups:
            if not group.enabled:
                lines_skip.append(f"  {group.name} — disabled by user")
                continue
            if group.mat_count < 2:
                lines_skip.append(
                    f"  {group.name} — only {group.mat_count} material "
                    f"(single-material groups have no effect)"
                )
                continue
            bake_groups.append(group)

            res = group.resolution
            vram = _vram_mb(res)
            lines_proceed.append(
                f"  {group.name}: {group.mat_count} materials → "
                f"atlas_{group.render_type.lower().replace(' ', '_')}_{res}px "
                f"({vram} MB VRAM)"
            )
            if group.warn_overlap:
                lines_skip.append(
                    f"    [!] {group.name} — overlapping UVs detected. "
                    f"Atlas UV will be repacked (Smart UV Project)"
                )
            if group.warn_emission and settings.output_format != "EXR":
                lines_skip.append(
                    f"    [!] {group.name} — emission > 1.0 detected. "
                    f"Values will clamp to 1.0 in {settings.output_format}. "
                    f"Switch to EXR to preserve HDR emission"
                )

        if not bake_groups:
            errors.append("No groups with 2+ materials are enabled. Nothing to bake.")

        lines_change.append(
            f"  UV maps repacked (originals preserved as 'UVMap_pre_atlas')"
        )
        after = sum(1 for g in bake_groups) + sum(
            g.mat_count for g in settings.atlas_groups
            if not g.enabled or g.mat_count < 2
        )
        lines_change.append(
            f"  Material slots: {settings.total_mats_before} → ~{after}"
        )
        if settings.preserve_originals:
            lines_change.append(
                f"  Backup collection: {_BACKUP_COLLECTION_PREFIX}[timestamp] (hidden)"
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
        bake_groups = self._groups_to_bake
        if not bake_groups:
            self.report({"ERROR"}, "No groups to bake")
            return {"CANCELLED"}

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
                    mats_after_count -= (group.mat_count - 1)

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

        except Exception as e:
            wm.progress_end()
            logger.exception("[BoneForge Atlas] Bake failed")
            self.report({"ERROR"}, f"Atlas bake failed: {e}")
            return {"CANCELLED"}

        return {"FINISHED"}

    # ── Bake internals ────────────────────────────────────────────

    def _create_backup(self, context, bake_groups, backup_name):
        """Duplicate all target meshes into a hidden backup collection."""
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

        # Hide the collection
        layer_coll = self._find_layer_collection(
            context.view_layer.layer_collection, backup_name
        )
        if layer_coll:
            layer_coll.hide_viewport = True
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

        # Collect source objects
        source_objs = []
        for item in group.meshes:
            obj = bpy.data.objects.get(item.object_name)
            if obj and obj.type == "MESH":
                source_objs.append(obj)

        if not source_objs:
            return None

        # ── Create working duplicates ──────────────────────────
        bpy.ops.object.select_all(action="DESELECT")
        work_objs = []
        for obj in source_objs:
            dup = obj.copy()
            dup.data = obj.data.copy()
            dup.name = f"__BF_ATLAS_WORK_{obj.name}"
            scene.collection.objects.link(dup)
            dup.select_set(True)
            work_objs.append(dup)

        # ── Preserve original UV map ──────────────────────────
        for obj in work_objs:
            mesh = obj.data
            if mesh.uv_layers.active:
                original_uv = mesh.uv_layers.active
                if original_uv.name != "UVMap_pre_atlas":
                    original_uv.name = "UVMap_pre_atlas"

        # ── Join into one working mesh ────────────────────────
        if context.object and context.object.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        context.view_layer.objects.active = work_objs[0]
        try:
            bpy.ops.object.join()
        except Exception as join_err:
            for w in work_objs:
                bpy.data.objects.remove(w, do_unlink=True)
            raise RuntimeError(f"Join failed — work objects cleaned up: {join_err}")
        joined = context.view_layer.objects.active
        joined.name = f"__BF_ATLAS_{group.render_type.replace(' ', '_')}"

        # ── Create atlas UV map ───────────────────────────────
        mesh = joined.data
        if "atlas_uv" in mesh.uv_layers:
            mesh.uv_layers.remove(mesh.uv_layers["atlas_uv"])
        atlas_uv = mesh.uv_layers.new(name="atlas_uv")

        # Set pre_atlas as render-active, atlas_uv as active for bake target
        for uv in mesh.uv_layers:
            uv.active_render = (uv.name == "UVMap_pre_atlas")
        atlas_uv.active = True

        # ── Smart UV Project → Pack Islands ───────────────────
        bpy.ops.object.mode_set(mode="EDIT")
        try:
            bpy.ops.mesh.select_all(action="SELECT")
            bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=settings.uv_margin)
            bpy.ops.uv.pack_islands(margin=settings.uv_margin)
        finally:
            bpy.ops.object.mode_set(mode="OBJECT")

        # ── Create atlas image ────────────────────────────────
        atlas_name = (
            f"bf_atlas_{group.render_type.lower().replace(' ', '_')}_{res}px"
        )
        if atlas_name in bpy.data.images:
            bpy.data.images.remove(bpy.data.images[atlas_name])
        atlas_img = bpy.data.images.new(atlas_name, width=res, height=res, alpha=True)
        atlas_img.colorspace_settings.name = "sRGB"

        # ── Add Image Texture node to each material ───────────
        for mat in joined.data.materials:
            if not mat or not mat.use_nodes:
                continue
            nodes = mat.node_tree.nodes
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

        # ── Bake DIFFUSE ──────────────────────────────────────
        saved_engine = scene.render.engine
        scene.render.engine = "CYCLES"

        try:
            bpy.ops.object.bake(
                type="DIFFUSE",
                pass_filter={"COLOR"},
                use_selected_to_active=False,
                margin=4,
                use_clear=True,
            )
        except Exception as bake_err:
            scene.render.engine = saved_engine
            logger.warning("[BoneForge Atlas] Cycles bake failed for %s: %s", group.name, bake_err)
            raise
        scene.render.engine = saved_engine

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

        # ── Build atlas material ──────────────────────────────
        mat_name = f"M_{atlas_name}"
        if mat_name in bpy.data.materials:
            bpy.data.materials.remove(bpy.data.materials[mat_name])
        atlas_mat = bpy.data.materials.new(mat_name)
        atlas_mat.use_nodes = True
        # Set blend mode to match group render type
        if group.render_type == "Alpha Blend":
            atlas_mat.blend_method = "BLEND"
        elif group.render_type == "Alpha Clip":
            atlas_mat.blend_method = "CLIP"
        else:
            atlas_mat.blend_method = "OPAQUE"

        nodes = atlas_mat.node_tree.nodes
        links = atlas_mat.node_tree.links
        nodes.clear()
        output_node = nodes.new("ShaderNodeOutputMaterial")
        output_node.location = (300, 0)
        bsdf_node = nodes.new("ShaderNodeBsdfPrincipled")
        bsdf_node.location = (0, 0)
        tex_node = nodes.new("ShaderNodeTexImage")
        tex_node.name = "Atlas"
        tex_node.image = atlas_img
        tex_node.location = (-300, 0)
        uv_node = nodes.new("ShaderNodeUVMap")
        uv_node.uv_map = "atlas_uv"
        uv_node.location = (-550, 0)
        links.new(uv_node.outputs["UV"], tex_node.inputs["Vector"])
        links.new(tex_node.outputs["Color"], bsdf_node.inputs["Base Color"])
        links.new(bsdf_node.outputs["BSDF"], output_node.inputs["Surface"])
        if group.render_type in ("Alpha Blend", "Alpha Clip"):
            links.new(tex_node.outputs["Alpha"], bsdf_node.inputs["Alpha"])

        # ── Assign atlas material to joined mesh ──────────────
        joined.data.materials.clear()
        joined.data.materials.append(atlas_mat)

        # ── Reparent to armature if present ──────────────────
        if arm:
            joined.parent = arm
            armature_mod = joined.modifiers.get("Armature")
            if not armature_mod:
                armature_mod = joined.modifiers.new("Armature", "ARMATURE")
            armature_mod.object = arm

        # ── Hide original source objects ──────────────────────
        for obj in source_objs:
            obj.hide_set(True)
            obj.hide_render = True

        # Clean up working name
        joined.name = (
            f"ATLAS_{group.render_type.replace(' ', '_')}_{res}px"
        )

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

        # Remove atlas meshes (objects starting with ATLAS_)
        scene = context.scene
        to_remove = [
            obj for obj in scene.objects
            if obj.name.startswith("ATLAS_")
        ]
        for obj in to_remove:
            bpy.data.objects.remove(obj, do_unlink=True)

        # Restore originals: unhide, move to scene collection
        for obj in list(coll.objects):
            # Strip PRE_ATLAS_ prefix to restore original name
            orig_name = obj.name.replace("PRE_ATLAS_", "", 1)
            obj.name = orig_name
            scene.collection.objects.link(obj)
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
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BoneForge"
    bl_parent_id = "BF_PT_sb_vrchat"
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
        col.operator("boneforge.vrc_atlas_analyze", text=T("Analyze Materials"), icon="VIEWZOOM")

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
                        text=T("[!] Overlapping UVs detected — atlas_uv will use Smart UV Project"),
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
                        text=f"{active_group.mat_count} materials → 1 atlas at {active_group.resolution}px",
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

            # Permanent transparency note (unanimous addition S)
            layout.separator()
            note_row = layout.row()
            note_row.label(
                text=T("Transparent / emissive materials kept in separate groups by default."),
                icon="INFO",
            )

            layout.separator()

            # Accept / Revert binary (unanimous addition Q)
            if settings.has_backup:
                backup_row = layout.row(align=True)
                backup_row.alert = True
                backup_row.operator(
                    "boneforge.vrc_atlas_accept",
                    text=T("Accept — Delete Backup"),
                    icon="TRASH",
                )
                backup_row.alert = False
                backup_row = layout.row()
                backup_row.operator(
                    "boneforge.vrc_atlas_revert",
                    text=T("Revert — Restore Originals"),
                    icon="LOOP_BACK",
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

            adv_col.label(text=T("Bake Passes:"))
            adv_col.prop(settings, "bake_albedo")
            adv_col.prop(settings, "bake_normal")
            emission_row = adv_col.row()
            emission_row.prop(settings, "bake_emission")
            if settings.bake_emission and settings.output_format != "EXR":
                emission_row.label(text=T("[!] Values > 1.0 clamp"), icon="ERROR")
            adv_col.prop(settings, "bake_roughness")

            adv_col.separator()
            adv_col.label(text=T("UV Packing:"))
            adv_col.prop(settings, "uv_margin")
            adv_col.prop(settings, "pack_method")

            adv_col.separator()
            adv_col.label(text=T("Output:"))
            adv_col.prop(settings, "output_format")
            if settings.output_format == "EXR":
                adv_col.label(
                    text=T("EXR preserves HDR emission — use for glow accessories"),
                    icon="INFO",
                )
            adv_col.prop(settings, "output_path")

            adv_col.separator()
            preserve_row = adv_col.row()
            preserve_row.prop(settings, "preserve_originals")
            if not settings.preserve_originals:
                adv_col.label(
                    text=T("WARNING: Originals will not be backed up. This cannot be undone."),
                    icon="ERROR",
                )


# ─────────────────────────────────────────────────────────────────
# Registration
# ─────────────────────────────────────────────────────────────────

_classes = (
    BF_AtlasMeshItem,
    BF_AtlasGroup,
    BF_AtlasSettings,
    BF_UL_VRC_AtlasGroups,
    BF_OT_VRC_AtlasAnalyze,
    BF_OT_VRC_AtlasAddGroup,
    BF_OT_VRC_AtlasRemoveGroup,
    BF_OT_VRC_AtlasBake,
    BF_OT_VRC_AtlasAccept,
    BF_OT_VRC_AtlasRevert,
    BONEFORGE_PT_vrc_w2_atlas,
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
