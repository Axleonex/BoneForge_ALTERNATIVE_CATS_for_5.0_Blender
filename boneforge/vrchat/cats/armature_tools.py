"""BoneForge VRChat CATS — Armature Tools.

Standalone (non-wizard-gated) armature utilities:
  - Merge Armatures: join a secondary armature into the active one, preserving
    mesh children and optionally re-parenting orphaned bones to the root.

Available at any time from the CATS sidebar tab.

Category: VRChat Cats Tools.
"""

import logging

import bpy
from bpy.props import BoolProperty, StringProperty
from bpy.types import Operator, Panel, PropertyGroup

from boneforge.core import active_armature
from boneforge.i18n import T
from boneforge.vrchat.cats import pipeline

logger = logging.getLogger(__name__)


# ── Settings PropertyGroup ───────────────────────────────────────────────────

class BF_ArmatureToolsSettings(PropertyGroup):
    """Per-scene settings for Armature Tools."""

    source_armature: StringProperty(
        name="Source Armature",
        description="Name of secondary armature to merge into active",
        default="",
    )
    auto_parent_bones: BoolProperty(
        name="Auto-Parent Orphan Bones",
        description="Auto-parent unparented bones from source to active armature root",
        default=True,
    )
    join_meshes_after: BoolProperty(
        name="Join Meshes After",
        description="Join all mesh children after merge using shape-key-safe join",
        default=False,
    )


# ── Helpers ──────────────────────────────────────────────────────────────────

def _apply_scale(context, obj):
    """Apply scale transform on *obj* to prevent scale mismatch after join."""
    bpy.ops.object.select_all(action='DESELECT')
    context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.transform_apply(scale=True)
    obj.select_set(False)


def _root_bone_name(arm_obj):
    """Return the name of the first top-level bone, or None when absent."""
    for bone in arm_obj.data.bones:
        if bone.parent is None:
            return bone.name
    return None


# ── Operator ─────────────────────────────────────────────────────────────────

class BF_OT_CATS_MergeArmatures(Operator):
    """Merge a secondary armature into the active armature"""

    bl_idname = "boneforge.cats_merge_armatures"
    bl_label = "Merge Armatures"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        settings = context.scene.boneforge_cats_armature_tools_settings
        if not settings.source_armature.strip():
            self.report({'ERROR'}, "Set Source Armature name first")
            return {'CANCELLED'}
        return self.execute(context)

    def execute(self, context):
        scene = context.scene
        settings = scene.boneforge_cats_armature_tools_settings

        source_name = settings.source_armature.strip()
        if not source_name:
            self.report({'ERROR'}, "Set Source Armature name first")
            return {'CANCELLED'}

        # Validate source object
        source_arm = bpy.data.objects.get(source_name)
        if source_arm is None:
            self.report({'ERROR'}, f"Object '{source_name}' not found in scene")
            return {'CANCELLED'}
        if source_arm.type != 'ARMATURE':
            self.report({'ERROR'}, f"'{source_name}' is not an ARMATURE object")
            return {'CANCELLED'}

        target_arm = active_armature(context)
        if target_arm is None:
            self.report({'ERROR'}, "No active armature")
            return {'CANCELLED'}
        if source_arm is target_arm:
            self.report({'ERROR'}, "Source and target armatures must be different objects")
            return {'CANCELLED'}

        target_name = target_arm.name

        # ── Step 1: Apply scale on both armatures ──────────────────────────
        _apply_scale(context, target_arm)
        _apply_scale(context, source_arm)

        # ── Step 2: Record source bone names that have no parent ───────────
        source_root_bones = {
            bone.name for bone in source_arm.data.bones if bone.parent is None
        }

        # ── Step 3: Record source mesh children ───────────────────────────
        source_meshes = [c for c in source_arm.children if c.type == 'MESH']

        # ── Step 4: Record all source bone names before join ───────────────
        source_bone_names = {bone.name for bone in source_arm.data.bones}

        # ── Step 5: Join armatures ─────────────────────────────────────────
        bpy.ops.object.select_all(action='DESELECT')
        source_arm.select_set(True)
        target_arm.select_set(True)
        context.view_layer.objects.active = target_arm
        bpy.ops.object.join()

        # After join, source_arm is gone; target_arm is the merged result
        merged_arm = bpy.data.objects.get(target_name)
        if merged_arm is None:
            self.report({'ERROR'}, "Merged armature object not found — join may have failed")
            return {'CANCELLED'}

        # ── Step 6: Auto-parent orphaned source bones ──────────────────────
        if settings.auto_parent_bones and source_root_bones:
            context.view_layer.objects.active = merged_arm
            bpy.ops.object.mode_set(mode='EDIT')

            edit_bones = merged_arm.data.edit_bones
            root_name = _root_bone_name(merged_arm)

            # Find the target root (a bone named "Root", or the first parentless bone
            # that was NOT from the source's own root set)
            target_root_eb = None
            if root_name is not None:
                # Prefer a bone explicitly named "Root" from the target
                named_root = edit_bones.get("Root")
                if named_root is not None:
                    target_root_eb = named_root
                else:
                    # Fall back to whatever the first parentless bone is that isn't
                    # one of the source root bones
                    for eb in edit_bones:
                        if eb.parent is None and eb.name not in source_root_bones:
                            target_root_eb = eb
                            break

            if target_root_eb is not None:
                for eb in edit_bones:
                    if eb.name in source_root_bones and eb.parent is None:
                        eb.parent = target_root_eb
                        eb.use_connect = False

            bpy.ops.object.mode_set(mode='OBJECT')

        # ── Step 7: Re-parent source mesh children to merged armature ─────
        for mesh_obj in source_meshes:
            if mesh_obj.name in bpy.data.objects:
                mesh_obj.parent = merged_arm

        # ── Step 8: Optionally join meshes ─────────────────────────────────
        if settings.join_meshes_after:
            if hasattr(bpy.ops.boneforge, "vrc_join_meshes"):
                context.view_layer.objects.active = merged_arm
                merged_arm.select_set(True)
                try:
                    bpy.ops.boneforge.vrc_join_meshes()
                except Exception as exc:
                    logger.warning(f"[BoneForge] Join meshes after merge failed: {exc}")
            else:
                logger.warning("[BoneForge] boneforge.vrc_join_meshes not registered; skipping post-merge join")

        msg = f"Merged '{source_name}' into '{target_name}'"
        self.report({'INFO'}, "Armatures merged")
        pipeline.append_ledger(scene, "merge_armatures", pipeline.OUTCOME_CHANGED, msg)

        return {'FINISHED'}


# ── Panel ────────────────────────────────────────────────────────────────────

class CATS_PT_armature_tools_standalone(Panel):
    """Armature Tools panel in the CATS sidebar tab."""

    bl_label = " "
    bl_idname = "CATS_PT_armature_tools_standalone"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "CATS"

    def draw_header(self, context):
        self.layout.label(text=T("Armature Tools"))

    @classmethod
    def poll(cls, context):
        return False  # Displayed via CATS_PT_armature_tools in cats_panel.py

    def draw(self, context):
        layout = self.layout
        settings = context.scene.boneforge_cats_armature_tools_settings

        # Source armature name
        layout.label(text=T("Source Armature:"))
        layout.prop(settings, "source_armature", text="")

        layout.separator()

        layout.prop(settings, "auto_parent_bones", toggle=False)
        layout.prop(settings, "join_meshes_after", toggle=False)

        layout.separator()

        row = layout.row()
        row.scale_y = 1.4
        row.operator(
            "boneforge.cats_merge_armatures",
            text=T("Merge Armatures"),
            icon='ARMATURE_DATA',
        )

        if not settings.source_armature.strip():
            layout.label(text=T("Set source armature name to the secondary rig's object name"), icon='ERROR')

        layout.separator()
        box = layout.box()
        box.label(
            text=T("Set Source Armature name to the secondary rig's object name"),
            icon='INFO',
        )


# ── Registration ─────────────────────────────────────────────────────────────

_classes = (
    BF_ArmatureToolsSettings,
    BF_OT_CATS_MergeArmatures,
    CATS_PT_armature_tools_standalone,
)


def register():
    for cls in _classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.boneforge_cats_armature_tools_settings = bpy.props.PointerProperty(
        type=BF_ArmatureToolsSettings
    )


def unregister():
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)
    if hasattr(bpy.types.Scene, "boneforge_cats_armature_tools_settings"):
        del bpy.types.Scene.boneforge_cats_armature_tools_settings
