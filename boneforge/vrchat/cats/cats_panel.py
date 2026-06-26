"""BoneForge VRChat CATS — Main N-Panel Tab (VIEW_3D sidebar).

The hub panel for all CATS-equivalent avatar tools. Uses bl_category="CATS"
so BoneForge occupies the established CATS tab that VRChat avatar creators
already know. Each sub-panel draws a focused set of operators inline.

All panels follow the project pattern:
    bl_label = " "  (single space)
    draw_header(self, context) sets the visible header text.
"""

import bpy
from bpy.types import Panel

from boneforge.core import active_armature
from boneforge.i18n import T
from boneforge.vrchat.cats import pipeline


# ── Shared tab / space config ───────────────────────────────────────────────

_SPACE = 'VIEW_3D'
_REGION = 'UI'
_CATEGORY = "CATS"  # Proper noun — never wrapped in T()


# ── Status icon helpers ─────────────────────────────────────────────────────

def _phase_icon(status) -> str:
    if status == pipeline.OUTCOME_CHANGED:
        return 'CHECKMARK'
    if status == pipeline.OUTCOME_CLEAN:
        return 'RADIOBUT_OFF'
    if status == pipeline.OUTCOME_FAILED:
        return 'CANCEL'
    return 'DOT'


# ── Main panel ──────────────────────────────────────────────────────────────

class CATS_PT_main(Panel):
    """CATS hub panel — shows active armature name and hosts sub-panels."""

    bl_label = " "
    bl_idname = "CATS_PT_main"
    bl_space_type = _SPACE
    bl_region_type = _REGION
    bl_category = _CATEGORY
    bl_order = 0

    def draw_header(self, context):
        self.layout.label(text="CATS", icon='ARMATURE_DATA')

    @classmethod
    def poll(cls, context):
        return True  # Tab always visible; sub-panels gate per armature

    def draw(self, context):
        layout = self.layout
        arm = active_armature(context)
        if arm is not None:
            layout.row().label(text=arm.name, icon='OUTLINER_OB_ARMATURE')
        else:
            layout.label(text=T("Select an armature to begin"), icon='ARMATURE_DATA')


# ── Sub-panel: Pipeline Status ──────────────────────────────────────────────

class CATS_PT_pipeline_status(Panel):
    """Overview of per-phase pipeline completion status."""

    bl_label = " "
    bl_idname = "CATS_PT_pipeline_status"
    bl_space_type = _SPACE
    bl_region_type = _REGION
    bl_category = _CATEGORY
    bl_parent_id = "CATS_PT_main"
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.label(text=T("Pipeline Status"), icon='STRIP_COLOR_04')

    @classmethod
    def poll(cls, context):
        return active_armature(context) is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        grid = layout.grid_flow(
            row_major=True, columns=1, even_columns=True, even_rows=False, align=True,
        )
        for phase_id in pipeline.PIPELINE_PHASES:
            status = pipeline.get_phase_status(scene, phase_id)
            grid.row(align=True).label(
                text=phase_id.replace("_", " ").title(),
                icon=_phase_icon(status),
            )


# ── Sub-panel: Fix Model ────────────────────────────────────────────────────

class CATS_PT_fix_model(Panel):
    """Fix Model settings and operator."""

    bl_label = " "
    bl_idname = "CATS_PT_fix_model"
    bl_space_type = _SPACE
    bl_region_type = _REGION
    bl_category = _CATEGORY
    bl_parent_id = "CATS_PT_main"

    def draw_header(self, context):
        self.layout.label(text=T("Fix Model"), icon='MODIFIER')

    @classmethod
    def poll(cls, context):
        return active_armature(context) is not None

    def draw(self, context):
        layout = self.layout
        settings = getattr(context.scene, "boneforge_vrc_fix_model_settings", None)
        if settings is not None:
            col = layout.column(align=True)
            col.prop(settings, "apply_modifiers", toggle=True)
            col.prop(settings, "remove_doubles", toggle=True)
            col.prop(settings, "recalculate_normals", toggle=True)
            col.prop(settings, "remove_loose", toggle=True)
            col.prop(settings, "remove_empty_groups", toggle=True)
            if hasattr(settings, "remove_constraints"):
                col.prop(settings, "remove_constraints", toggle=True)
            if hasattr(settings, "remove_rigidbodies"):
                col.prop(settings, "remove_rigidbodies", toggle=True)
            layout.separator(factor=0.5)
        layout.operator("boneforge.vrc_fix_model", text=T("Fix Model"), icon='MODIFIER')


# ── Sub-panel: Visemes ──────────────────────────────────────────────────────

class CATS_PT_visemes(Panel):
    """Viseme generator and shape-key mapper operators."""

    bl_label = " "
    bl_idname = "CATS_PT_visemes"
    bl_space_type = _SPACE
    bl_region_type = _REGION
    bl_category = _CATEGORY
    bl_parent_id = "CATS_PT_main"
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.label(text=T("Visemes"), icon='SHAPEKEY_DATA')

    @classmethod
    def poll(cls, context):
        return active_armature(context) is not None

    def draw(self, context):
        layout = self.layout
        settings = getattr(context.scene, "boneforge_cats_viseme_settings", None)
        if settings is not None:
            col = layout.column(align=True)
            col.prop(settings, "a_shape", text=T("A Shape"))
            col.prop(settings, "o_shape", text=T("O Shape"))
            col.prop(settings, "ch_shape", text=T("CH Shape"))
            layout.prop(settings, "overwrite_existing")
            layout.separator(factor=0.5)
            layout.operator(
                "boneforge.cats_auto_detect_shapes",
                text=T("Auto-Detect"),
                icon='VIEWZOOM',
            )
        layout.operator(
            "boneforge.cats_generate_visemes",
            text=T("Generate Visemes"),
            icon='SHAPEKEY_DATA',
        )


# ── Sub-panel: Eye Tracking ─────────────────────────────────────────────────

class CATS_PT_eye_tracking(Panel):
    """Eye tracking bone and constraint setup."""

    bl_label = " "
    bl_idname = "CATS_PT_eye_tracking"
    bl_space_type = _SPACE
    bl_region_type = _REGION
    bl_category = _CATEGORY
    bl_parent_id = "CATS_PT_main"
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.label(text=T("Eye Tracking"), icon='HIDE_OFF')

    @classmethod
    def poll(cls, context):
        return active_armature(context) is not None

    def draw(self, context):
        layout = self.layout
        settings = getattr(context.scene, "boneforge_cats_eye_settings", None)
        if settings is not None:
            col = layout.column(align=True)
            col.prop(settings, "left_eye_bone", text=T("Left Eye"))
            col.prop(settings, "right_eye_bone", text=T("Right Eye"))
            layout.separator(factor=0.5)
            col = layout.column(align=True)
            col.prop(settings, "up_limit", text=T("Up Limit"))
            col.prop(settings, "down_limit", text=T("Down Limit"))
            col.prop(settings, "side_limit", text=T("Side Limit"))
            layout.separator(factor=0.5)
        layout.operator(
            "boneforge.cats_autodetect_eyes",
            text=T("Auto-Detect"),
            icon='VIEWZOOM',
        )
        layout.operator(
            "boneforge.cats_create_eye_tracking",
            text=T("Create Eye Tracking"),
            icon='HIDE_OFF',
        )


# ── Sub-panel: Pose & Shape Keys ────────────────────────────────────────────

class CATS_PT_pose_shape(Panel):
    """Pose-to-shape-key bake and shape-key-to-basis flatten."""

    bl_label = " "
    bl_idname = "CATS_PT_pose_shape"
    bl_space_type = _SPACE
    bl_region_type = _REGION
    bl_category = _CATEGORY
    bl_parent_id = "CATS_PT_main"
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.label(text=T("Pose & Shape Keys"), icon='POSE_HLT')

    @classmethod
    def poll(cls, context):
        return active_armature(context) is not None

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.operator(
            "boneforge.cats_pose_to_shape",
            text=T("Pose to Shape Key"),
            icon='POSE_HLT',
        )
        col.operator(
            "boneforge.cats_shape_key_to_basis",
            text=T("Shape Key to Basis"),
            icon='SHAPEKEY_DATA',
        )


# ── Sub-panel: Mesh Tools ───────────────────────────────────────────────────

class CATS_PT_material_atlas(Panel):
    """Material atlas combiner, delegated to the shared atlas panel."""

    bl_label = " "
    bl_idname = "CATS_PT_material_atlas"
    bl_space_type = _SPACE
    bl_region_type = _REGION
    bl_category = _CATEGORY
    bl_parent_id = "CATS_PT_main"
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.label(text=T("Material Atlas"), icon='MATERIAL')

    @classmethod
    def poll(cls, context):
        return active_armature(context) is not None or (
            context.active_object is not None and context.active_object.type == 'MESH'
        )

    def draw(self, context):
        from boneforge.vrchat.cats import material_atlas
        material_atlas.BONEFORGE_PT_vrc_w2_atlas.draw(self, context)


class CATS_PT_mesh_tools(Panel):
    """Mesh separation utilities."""

    bl_label = " "
    bl_idname = "CATS_PT_mesh_tools"
    bl_space_type = _SPACE
    bl_region_type = _REGION
    bl_category = _CATEGORY
    bl_parent_id = "CATS_PT_main"
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.label(text=T("Mesh Tools"), icon='MESH_DATA')

    @classmethod
    def poll(cls, context):
        return active_armature(context) is not None

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.operator(
            "boneforge.cats_separate_by_materials",
            text=T("Separate by Materials"),
            icon='MATERIAL',
        )
        col.operator(
            "boneforge.cats_separate_by_loose",
            text=T("Separate by Loose Parts"),
            icon='MESH_DATA',
        )
        col.operator(
            "boneforge.cats_separate_by_shape_keys",
            text=T("Separate by Shape Keys"),
            icon='SHAPEKEY_DATA',
        )


# ── Sub-panel: Transforms & FBT ─────────────────────────────────────────────

class CATS_PT_transforms(Panel):
    """Apply transforms and Full Body Tracking bone adjustments."""

    bl_label = " "
    bl_idname = "CATS_PT_transforms"
    bl_space_type = _SPACE
    bl_region_type = _REGION
    bl_category = _CATEGORY
    bl_parent_id = "CATS_PT_main"
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.label(text=T("Transforms & FBT"), icon='OBJECT_ORIGIN')

    @classmethod
    def poll(cls, context):
        return active_armature(context) is not None

    def draw(self, context):
        layout = self.layout
        layout.operator(
            "boneforge.cats_apply_all_transforms",
            text=T("Apply All Transforms"),
            icon='OBJECT_ORIGIN',
        )
        layout.separator(factor=0.5)
        col = layout.column(align=True)
        col.operator(
            "boneforge.cats_fix_fbt",
            text=T("Fix FBT"),
            icon='CON_ROTLIKE',
        )
        col.operator(
            "boneforge.cats_remove_fbt",
            text=T("Remove FBT"),
            icon='CANCEL',
        )


# ── Sub-panel: Bone Tools ───────────────────────────────────────────────────

class CATS_PT_bone_tools(Panel):
    """Bone root creation, merge, and duplicate utilities."""

    bl_label = " "
    bl_idname = "CATS_PT_bone_tools"
    bl_space_type = _SPACE
    bl_region_type = _REGION
    bl_category = _CATEGORY
    bl_parent_id = "CATS_PT_main"
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.label(text=T("Bone Tools"), icon='BONE_DATA')

    @classmethod
    def poll(cls, context):
        return active_armature(context) is not None

    def draw(self, context):
        layout = self.layout
        settings = getattr(context.scene, "boneforge_cats_bone_tools_settings", None)
        if settings is not None:
            col = layout.column(align=True)
            col.prop(settings, "root_bone_name", text=T("Root Name"))
        layout.operator(
            "boneforge.cats_create_bone_root",
            text=T("Create Root Bone"),
            icon='BONE_DATA',
        )
        layout.separator(factor=0.5)
        if settings is not None:
            layout.prop(settings, "merge_threshold", text=T("Merge Threshold"))
        layout.operator(
            "boneforge.cats_merge_bones",
            text=T("Merge Bones"),
            icon='AUTOMERGE_ON',
        )
        layout.separator(factor=0.5)
        layout.operator(
            "boneforge.cats_duplicate_bones",
            text=T("Duplicate Bones"),
            icon='DUPLICATE',
        )


# ── Sub-panel: Armature Tools ───────────────────────────────────────────────

class CATS_PT_armature_tools(Panel):
    """Merge armatures (standalone modal)."""

    bl_label = " "
    bl_idname = "CATS_PT_armature_tools"
    bl_space_type = _SPACE
    bl_region_type = _REGION
    bl_category = _CATEGORY
    bl_parent_id = "CATS_PT_main"
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.label(text=T("Armature Tools"), icon='ARMATURE_DATA')

    @classmethod
    def poll(cls, context):
        return active_armature(context) is not None

    def draw(self, context):
        layout = self.layout
        settings = getattr(context.scene, "boneforge_cats_armature_tools_settings", None)
        if settings is not None:
            col = layout.column(align=True)
            col.prop(settings, "source_armature", text=T("Source"))
            col.prop(settings, "auto_parent_bones")
            col.prop(settings, "join_meshes_after")
            layout.separator(factor=0.5)
        layout.operator(
            "boneforge.cats_merge_armatures",
            text=T("Merge Armatures"),
            icon='ARMATURE_DATA',
        )


# ── Sub-panel: Operation Ledger ─────────────────────────────────────────────

class CATS_PT_ledger(Panel):
    """Scrollable log of all CATS pipeline operations."""

    bl_label = " "
    bl_idname = "CATS_PT_ledger"
    bl_space_type = _SPACE
    bl_region_type = _REGION
    bl_category = _CATEGORY
    bl_parent_id = "CATS_PT_main"
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.label(text=T("Operation Ledger"), icon='TEXT')

    @classmethod
    def poll(cls, context):
        return active_armature(context) is not None

    def draw(self, context):
        layout = self.layout
        ledger = pipeline.get_ledger(context.scene)

        if not ledger:
            layout.label(text=T("No ledger entries"), icon='INFO')
        else:
            col = layout.column(align=True)
            for entry in ledger:
                status = entry.get("status", "")
                op_id = entry.get("op_id", "?")
                message = entry.get("message", "")
                t = entry.get("time", "")
                icon = (
                    'CHECKMARK' if status == pipeline.OUTCOME_CHANGED else
                    'RADIOBUT_OFF' if status == pipeline.OUTCOME_CLEAN else
                    'CANCEL' if status == pipeline.OUTCOME_FAILED else 'DOT'
                )
                col.row(align=True).label(
                    text=f"[{t}] {op_id} — {message}" if t else f"{op_id} — {message}",
                    icon=icon,
                )

        layout.separator(factor=0.5)
        row = layout.row(align=True)
        row.operator("boneforge.cats_clear_ledger", text=T("Clear"), icon='TRASH')
        row.operator("boneforge.cats_copy_ledger", text=T("Copy"), icon='COPYDOWN')


# ── Registration ────────────────────────────────────────────────────────────

classes = (
    CATS_PT_main,
    CATS_PT_pipeline_status,
    CATS_PT_fix_model,
    CATS_PT_visemes,
    CATS_PT_eye_tracking,
    CATS_PT_pose_shape,
    CATS_PT_material_atlas,
    CATS_PT_mesh_tools,
    CATS_PT_transforms,
    CATS_PT_bone_tools,
    CATS_PT_armature_tools,
    CATS_PT_ledger,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
