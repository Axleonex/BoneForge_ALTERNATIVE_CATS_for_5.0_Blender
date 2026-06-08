"""BoneForge Task Board — Main panel, Quick Win section, and Health Bar.

Registers one top-level panel in the dedicated 'BoneForge' N-panel tab:

    BONEFORGE_PT_taskboard
        ├─ Health bar row   (score badge + label + armature name)
        ├─ Quick Win section (top-3 highest impact/effort ratio tasks)
        └─ Full task list   (grouped by category, each group collapsible)

Each task card shows:
    [status icon]  Title  [Fix button if operator is set]
    Description text (muted, wrapped)

An operator BF_OT_OpenHealthCheck opens the existing rig_validator panel.
An operator BF_OT_InvalidateTaskCache forces re-analysis.
"""

import bpy
from bpy.types import Panel, Operator

from boneforge.i18n import T
from .analyzer import (
    get_tasks,
    get_quick_wins,
    get_health_score,
    get_tasks_by_category,
    invalidate,
    invalidate_all,
)
from .tasks import (
    CATEGORY_LABELS,
    CATEGORY_ICONS,
    STATUS_ERROR,
    STATUS_WARNING,
    STATUS_SUGGESTION,
)

import logging

logger = logging.getLogger(__name__)

# ── Health bar score colour thresholds ───────────────────────
# Blender theme icon names used as colour proxies in the label.
_SCORE_ICONS = {
    90: "FUND",        # green circle  — Excellent
    70: "LAYER_ACTIVE", # yellow       — Good
    40: "ERROR",        # orange/red   — Needs work
     0: "CANCEL",       # red          — Critical
}


def _score_icon(score: int) -> str:
    for threshold in sorted(_SCORE_ICONS, reverse=True):
        if score >= threshold:
            return _SCORE_ICONS[threshold]
    return "CANCEL"


# ── Text wrap helper ──────────────────────────────────────────

def _wrap_text(context, text: str, indent_units: int = 1) -> list:
    """Split *text* into lines that fit the current panel width.

    Uses region.width and ui_scale to estimate available characters.
    indent_units: number of box/indent levels (each costs ~20px).
    Returns a list of strings, one per display line.
    """
    try:
        ui_scale   = context.preferences.system.ui_scale
        region_px  = context.region.width
        # Subtract panel padding (~40px) + per-indent cost (~22px each).
        usable_px  = region_px - 40 - (indent_units * 22)
        # At ui_scale 1.0, default Blender font is ~6.5px per character.
        chars_wide = max(20, int(usable_px / (6.5 * ui_scale)))
    except Exception:
        chars_wide = 44  # safe fallback when context is unusual

    words  = text.split()
    lines  = []
    line   = ""
    for word in words:
        candidate = (line + " " + word).strip()
        if len(candidate) <= chars_wide:
            line = candidate
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines or [""]


# ── Shared draw helper ────────────────────────────────────────

def _draw_task_card(layout, task, context, compact: bool = False):
    """Draw a single task as a card row inside *layout*.

    compact=True omits the description lines (used in Quick Win section).
    context is required for text-wrap width calculation.
    """
    box = layout.box()
    row = box.row(align=True)
    row.label(text="", icon=task.icon)

    title_col = row.column()
    title_col.scale_x = 1.0
    title_col.label(text=task.title)

    if task.operator:
        op_col = row.column()
        op_col.scale_x = 0.9
        try:
            op_col.operator(task.operator, text=T(task.operator_text), icon='PLAY')
        except Exception:
            # Operator not registered in this Blender session — show label only.
            op_col.label(text=T(task.operator_text), icon='PLAY')

    if not compact and task.description:
        for line in _wrap_text(context, task.description, indent_units=1):
            desc_row = box.row()
            desc_row.scale_y = 0.8
            desc_row.label(text=line)


# ── Operators ─────────────────────────────────────────────────

class BF_OT_InvalidateTaskCache(Operator):
    """Force the Task Board to re-analyse the active armature."""
    bl_idname  = "boneforge.taskboard_refresh"
    bl_label   = "Refresh Task Board"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return (
            context.active_object is not None
            and context.active_object.type == 'ARMATURE'
        )

    def execute(self, context):
        obj = context.active_object
        if obj:
            invalidate(obj.name)
        self.report({'INFO'}, "Task Board refreshed.")
        return {'FINISHED'}


class BF_OT_InvalidateAllTaskCache(Operator):
    """Clear the Task Board cache for all armatures."""
    bl_idname  = "boneforge.taskboard_refresh_all"
    bl_label   = "Refresh All"
    bl_options = {'REGISTER'}

    def execute(self, context):
        invalidate_all()
        self.report({'INFO'}, "Task Board cache cleared.")
        return {'FINISHED'}


class BF_OT_OpenHealthCheck(Operator):
    """Open the BoneForge Health Check (Rig Validator) popup."""
    bl_idname  = "boneforge.open_health_check"
    bl_label   = "Open Health Check"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return (
            context.active_object is not None
            and context.active_object.type == 'ARMATURE'
        )

    def execute(self, context):
        # Delegate to the rig_validator operator if registered.
        try:
            bpy.ops.boneforge.run_rig_validation()
        except AttributeError:
            self.report({'WARNING'}, "Rig Validator not available.")
        return {'FINISHED'}


# ── Main panel ────────────────────────────────────────────────

class BONEFORGE_PT_taskboard(Panel):
    """BoneForge Task Board — persistent navigation surface."""
    bl_label       = " "
    bl_idname      = "BONEFORGE_PT_taskboard"
    bl_space_type  = "VIEW_3D"
    bl_region_type = "UI"
    bl_category    = "BoneForge"
    bl_parent_id   = "BF_PT_sb_overview"

    def draw_header(self, context):
        self.layout.label(text=T("Task Board"))

    @classmethod
    def poll(cls, context):
        # v3.3.5: avatar context — armature OR a mesh parented / armature-
        # modifier-bound to one. Lets Task Board stay visible during
        # weight painting / shape key editing on a child mesh.
        from boneforge.core import find_avatar_armature
        return find_avatar_armature(context) is not None

    def draw(self, context):
        from boneforge.core import find_avatar_armature
        layout = self.layout
        arm_obj = find_avatar_armature(context)
        if arm_obj is None:
            layout.label(
                text=T("No avatar armature found."),
                icon="INFO",
            )
            return

        # ── Health bar ────────────────────────────────────────
        score, label = get_health_score(arm_obj)
        health_box = layout.box()
        health_row = health_box.row(align=True)
        health_row.label(text=f"{score}", icon=_score_icon(score))
        health_row.label(text=f"{label}  ·  {arm_obj.name}")
        health_row.operator(
            "boneforge.open_health_check",
            text="", icon="VIEWZOOM",
        )
        health_row.operator(
            "boneforge.taskboard_refresh",
            text="", icon="FILE_REFRESH",
        )

        tasks = get_tasks(arm_obj)

        if not tasks:
            layout.separator()
            col = layout.column()
            col.scale_y = 1.2
            col.label(text=T("No issues found — rig looks good!"), icon="CHECKMARK")
            return

        # ── Quick Win section ─────────────────────────────────
        quick_wins = get_quick_wins(arm_obj, n=3)
        if quick_wins:
            layout.separator(factor=0.5)
            qw_header = layout.row()
            qw_header.label(text=T("Quick Wins"), icon="SOLO_ON")

            for task in quick_wins:
                _draw_task_card(layout, task, context, compact=False)

        # ── Full task list ────────────────────────────────────
        layout.separator(factor=0.5)
        all_row = layout.row()
        all_row.label(text=f"All Tasks ({len(tasks)})", icon="LINENUMBERS_ON")

        for category, cat_tasks in get_tasks_by_category(arm_obj):
            cat_label = CATEGORY_LABELS.get(category, category.title())
            cat_icon  = CATEGORY_ICONS.get(category, "DOT")

            # Collapsible sub-section per category.
            prop_key = f"boneforge_taskboard_collapsed_{category}"
            scene    = context.scene
            collapsed = scene.get(prop_key, False)

            cat_row = layout.row()
            cat_row.alignment = 'LEFT'
            expand_icon = 'TRIA_RIGHT' if collapsed else 'TRIA_DOWN'
            op = cat_row.operator(
                "boneforge.taskboard_toggle_category",
                text=f"{cat_label}  ({len(cat_tasks)})",
                icon=expand_icon,
                emboss=False,
            )
            op.category = category

            if not collapsed:
                for task in cat_tasks:
                    _draw_task_card(layout, task, context, compact=False)


class BONEFORGE_PT_taskboard_no_arm(Panel):
    """Shown in the Overview hub when no armature is active."""
    bl_label       = " "
    bl_idname      = "BONEFORGE_PT_taskboard_no_arm"
    bl_space_type  = "VIEW_3D"
    bl_region_type = "UI"
    bl_category    = "BoneForge"
    bl_parent_id   = "BF_PT_sb_overview"

    def draw_header(self, context):
        self.layout.label(text=T("Task Board"))

    @classmethod
    def poll(cls, context):
        return (
            context.active_object is None
            or context.active_object.type != 'ARMATURE'
        )

    def draw(self, context):
        # v3.2.2: the duplicate Start Auto-Rig button was removed here per
        # user feedback. The Auto-Rig Wizard panel (bl_order = -100) is
        # always visible at the top of the BoneForge tab and carries the
        # only Start button. Keep a hint so this Task Board sub-panel
        # doesn't render blank when no armature is selected.
        layout = self.layout
        layout.label(text=T("No armature selected."), icon="ARMATURE_DATA")
        layout.separator(factor=0.5)
        layout.label(
            text=T("Use the 'Auto-Rig Wizard' panel above to start a new rig."),
            icon='INFO',
        )


# ── Category collapse toggle operator ────────────────────────

class BF_OT_ToggleTaskCategory(Operator):
    """Toggle collapse state for a task category in the Task Board."""
    bl_idname  = "boneforge.taskboard_toggle_category"
    bl_label   = "Toggle Category"
    bl_options = {'REGISTER', 'INTERNAL'}

    category: bpy.props.StringProperty(default="")

    def execute(self, context):
        if not self.category:
            return {'CANCELLED'}
        prop_key = f"boneforge_taskboard_collapsed_{self.category}"
        current  = context.scene.get(prop_key, False)
        context.scene[prop_key] = not current
        return {'FINISHED'}


# ── Registration ────────────────────────────────────────────

_CLASSES = (
    BF_OT_InvalidateTaskCache,
    BF_OT_InvalidateAllTaskCache,
    BF_OT_OpenHealthCheck,
    BF_OT_ToggleTaskCategory,
    BONEFORGE_PT_taskboard,
)


def register():
    for cls in _CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(_CLASSES):
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass
