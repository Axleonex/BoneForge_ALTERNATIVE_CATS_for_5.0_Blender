"""BoneForge IO Hub — Game Engine Export operators.

One-click FBX export/import with presets tuned for Unreal Engine 5.
Unity/VRChat export operators live in the VRChat phase; they are only
surfaced here in the panel for discoverability.
"""

from __future__ import annotations

import bpy
from bpy.props import BoolProperty, StringProperty
from bpy_extras.io_utils import ExportHelper, ImportHelper


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

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type in {'ARMATURE', 'MESH'}

    def execute(self, context):
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
                path_mode='AUTO',
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


_classes = (
    BF_OT_ExportUnrealFBX,
    BF_OT_ImportUnrealFBX,
)


def register():
    for cls in _classes:
        try:
            bpy.utils.register_class(cls)
        except ValueError:
            pass


def unregister():
    for cls in reversed(_classes):
        try:
            bpy.utils.unregister_class(cls)
        except (RuntimeError, ValueError):
            pass
