"""BoneForge IO Hub — Game Engine Export operators.

One-click FBX export/import with presets tuned for Unreal Engine 5.
Unity/VRChat export operators live in the VRChat phase; they are only
surfaced here in the panel for discoverability.
"""

from __future__ import annotations

import os

import bpy
from bpy.props import BoolProperty, PointerProperty, StringProperty
from bpy.types import PropertyGroup
from bpy_extras.io_utils import ExportHelper, ImportHelper


def _sanitize_filename(name: str, fallback: str) -> str:
    cleaned = "".join("_" if ch in '<>:"/\\|?*' else ch for ch in (name or ""))
    cleaned = cleaned.strip(" .")
    return cleaned or fallback


def _resolve_export_dir(raw_path: str) -> str:
    raw_path = (raw_path or "").strip()
    if not raw_path:
        return ""
    if raw_path.startswith("//") and not bpy.data.filepath:
        return ""
    return bpy.path.abspath(raw_path)


def _with_extension(filename: str, extension: str) -> str:
    base, ext = os.path.splitext(filename)
    if ext.lower() == extension:
        return filename
    return f"{base or filename}{extension}"


def _default_unreal_export_name(context) -> str:
    obj = context.active_object
    if obj is not None:
        return _sanitize_filename(obj.name, "UnrealExport")
    return "UnrealExport"


def build_unreal_export_filepath(settings, context) -> str:
    export_dir = _resolve_export_dir(settings.unreal_export_path)
    if not export_dir:
        return ""
    name = _sanitize_filename(
        settings.unreal_export_name,
        _default_unreal_export_name(context),
    )
    return os.path.join(export_dir, _with_extension(name, ".fbx"))


class BF_GameExportSettings(PropertyGroup):
    unreal_export_path: StringProperty(
        name="Export Folder",
        description="Folder for Unreal FBX exports",
        subtype='DIR_PATH',
        default="//",
    )
    unreal_export_name: StringProperty(
        name="File Name",
        description="FBX file name for Unreal export",
        default="UnrealExport",
    )
    unreal_use_selection: BoolProperty(
        name="Selected Only",
        description="Export only selected objects",
        default=True,
    )
    unreal_apply_unit_scale: BoolProperty(
        name="Apply Unit Scale",
        description="Apply Blender unit conversion so UE imports at correct scale",
        default=True,
    )
    unreal_add_leaf_bones: BoolProperty(
        name="Add Leaf Bones",
        description="Append a terminal bone to each chain",
        default=False,
    )
    unreal_bake_anim: BoolProperty(
        name="Bake Animation",
        description="Include baked NLA/action animation data",
        default=False,
    )
    unreal_embed_textures: BoolProperty(
        name="Embed Textures",
        description="Pack image textures into the FBX for easier engine material import",
        default=True,
    )


class BF_OT_ExportUnrealFBX(bpy.types.Operator, ExportHelper):
    """Export selected armature and meshes as FBX with Unreal Engine 5 presets."""

    bl_idname  = "boneforge.export_unreal_fbx"
    bl_label   = "Export to Unreal (FBX)"
    bl_options = {'REGISTER'}

    filename_ext = ".fbx"
    filter_glob: StringProperty(default="*.fbx", options={'HIDDEN'})

    use_selection: BoolProperty(
        name="Selected Only",
        description="Export only selected objects",
        default=True,
    )
    apply_unit_scale: BoolProperty(
        name="Apply Unit Scale",
        description="Apply Blender unit conversion so UE imports at correct scale",
        default=True,
    )
    add_leaf_bones: BoolProperty(
        name="Add Leaf Bones",
        description="Append a terminal bone to each chain — UE does not need these",
        default=False,
    )
    bake_anim: BoolProperty(
        name="Bake Animation",
        description="Include baked NLA/action animation data",
        default=False,
    )
    embed_textures: BoolProperty(
        name="Embed Textures",
        description="Pack image textures into the FBX for easier engine material import",
        default=True,
    )

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type in {'ARMATURE', 'MESH'}

    def execute(self, context):
        if not self.filepath:
            settings = getattr(context.scene, "boneforge_game_export_settings", None)
            if settings is not None:
                self.filepath = build_unreal_export_filepath(settings, context)
        if not self.filepath:
            self.report({'ERROR'}, "FBX export path is not set (save the .blend or choose an export folder)")
            return {'CANCELLED'}

        try:
            bpy.ops.export_scene.fbx(
                filepath=self.filepath,
                use_selection=self.use_selection,
                apply_unit_scale=self.apply_unit_scale,
                apply_scale_options='FBX_SCALE_NONE',
                axis_forward='-Z',
                axis_up='Y',
                mesh_smooth_type='OFF',
                use_mesh_modifiers=True,
                add_leaf_bones=self.add_leaf_bones,
                primary_bone_axis='Y',
                secondary_bone_axis='X',
                use_armature_deform_only=True,
                bake_anim=self.bake_anim,
                bake_anim_use_all_actions=False,
                bake_anim_force_startend_keying=True,
                path_mode='COPY' if self.embed_textures else 'AUTO',
                embed_textures=self.embed_textures,
            )
        except RuntimeError as exc:
            self.report({'ERROR'}, f"FBX export failed: {exc}")
            return {'CANCELLED'}
        self.report({'INFO'}, f"Exported: {self.filepath}")
        return {'FINISHED'}


class BF_OT_ImportUnrealFBX(bpy.types.Operator, ImportHelper):
    """Import an FBX file previously exported from Unreal Engine."""

    bl_idname  = "boneforge.import_unreal_fbx"
    bl_label   = "Import from Unreal (FBX)"
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = ".fbx"
    filter_glob: StringProperty(default="*.fbx", options={'HIDDEN'})

    automatic_bone_orientation: BoolProperty(
        name="Auto Bone Orientation",
        description="Compute best bone orientation from children (recommended for UE exports)",
        default=True,
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        try:
            bpy.ops.import_scene.fbx(
                filepath=self.filepath,
                use_manual_orientation=False,
                automatic_bone_orientation=self.automatic_bone_orientation,
                ignore_leaf_bones=True,
            )
        except RuntimeError as exc:
            self.report({'ERROR'}, f"FBX import failed: {exc}")
            return {'CANCELLED'}
        self.report({'INFO'}, f"Imported: {self.filepath}")
        return {'FINISHED'}


def draw_unreal_export_settings(layout, context):
    settings = getattr(context.scene, "boneforge_game_export_settings", None)
    if settings is None:
        layout.label(text="Unreal export settings unavailable", icon='ERROR')
        return

    layout.prop(settings, "unreal_export_path", text="Folder")
    layout.prop(settings, "unreal_export_name", text="File")

    row = layout.row(align=True)
    row.prop(settings, "unreal_use_selection", text="Selected Only")
    row.prop(settings, "unreal_apply_unit_scale", text="Unit Scale")
    row = layout.row(align=True)
    row.prop(settings, "unreal_add_leaf_bones", text="Leaf Bones")
    row.prop(settings, "unreal_bake_anim", text="Bake Anim")
    layout.prop(settings, "unreal_embed_textures", text="Embed Textures")

    if not build_unreal_export_filepath(settings, context):
        layout.label(text="Save the .blend or choose an export folder", icon='INFO')


_classes = (
    BF_GameExportSettings,
    BF_OT_ExportUnrealFBX,
    BF_OT_ImportUnrealFBX,
)


def register():
    for cls in _classes:
        try:
            bpy.utils.register_class(cls)
        except ValueError:
            pass
    if not hasattr(bpy.types.Scene, "boneforge_game_export_settings"):
        bpy.types.Scene.boneforge_game_export_settings = PointerProperty(
            type=BF_GameExportSettings
        )


def unregister():
    if hasattr(bpy.types.Scene, "boneforge_game_export_settings"):
        del bpy.types.Scene.boneforge_game_export_settings
    for cls in reversed(_classes):
        try:
            bpy.utils.unregister_class(cls)
        except (RuntimeError, ValueError):
            pass
