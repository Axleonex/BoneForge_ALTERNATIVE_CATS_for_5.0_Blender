"""Native Blender menu access for BoneForge's existing operators."""
import bpy
from boneforge.i18n import T
from .ui_layout import operator_exists

POSE_ENTRIES = (
    ("boneforge.breakdowner", "Breakdowner", "IPO_BEZIER", None),
    ("boneforge.delta_move", "Delta Move", "TRANSFORM_ORIGINS", None),
    ("boneforge.euler_filter", "Euler Filter", "GRAPH", None),
    ("boneforge.tangent_set_type", "Auto Clamped Tangents", "HANDLE_AUTOCLAMPED", {"type": "AUTO_CLAMPED"}),
    ("boneforge.tangent_set_type", "Vector Tangents", "HANDLE_VECTOR", {"type": "VECTOR"}),
    ("boneforge.rig_panel_popup", "Bone Collections", "GROUP_BONE", None),
    ("boneforge.show_all_collections", "Show All Collections", "HIDE_OFF", None),
    ("boneforge.hide_all_collections", "Hide All Collections", "HIDE_ON", None),
    ("boneforge.run_validation", "Validate Rig", "CHECKMARK", None),
    ("boneforge.open_health_check", "Health Check", "VIEWZOOM", None),
)
WEIGHT_ENTRIES = (
    ("boneforge.flood_to_zero", "Flood to Zero", "REMOVE", None),
    ("boneforge.flood_to_one", "Flood to One", "ADD", None),
    ("boneforge.flood_to_custom", "Flood to Custom", "BRUSH_DATA", None),
    ("boneforge.mirror_active_weight", "Mirror Active Weight", "MOD_MIRROR", None),
    ("boneforge.normalize_vertex_weights", "Normalize Selected", "MOD_VERTEX_WEIGHT", None),
    ("boneforge.automatic_bone_weight_recalculation", "Automatic Bone Weight Recalculation", "MOD_VERTEX_WEIGHT", None),
)

def draw_entries(layout, entries):
    for idname, label, icon, properties in entries:
        if operator_exists(idname):
            op = layout.operator(idname, text=T(label), icon=icon)
            for name, value in (properties or {}).items():
                setattr(op, name, value)

def _quick_rig(layout, context, rig_id, label):
    op = layout.operator("boneforge.add_quick_rig", text=T(label), icon="ARMATURE_DATA")
    op.rig_op_id = rig_id
    op.rig_label = label
    scene = context.scene
    op.fit_to_active_mesh = getattr(scene, "boneforge_quick_rig_fit_to_mesh", True)
    op.parent_with_auto_weights = getattr(scene, "boneforge_quick_rig_auto_weight", False)
    op.generate_control_rig = getattr(scene, "boneforge_quick_rig_generate_controls", False)
    op.initial_pose = getattr(scene, "boneforge_quick_rig_initial_pose", "NONE")

class BF_MT_quick_rig(bpy.types.Menu):
    bl_idname = "BF_MT_quick_rig"
    bl_label = "BoneForge"
    def draw(self, context):
        if not operator_exists("boneforge.add_quick_rig"):
            return
        from boneforge.autorig.quick_human import FALLBACK_OP_ID, discover_rigify_metarigs
        self.layout.operator_context = "EXEC_REGION_WIN"
        _quick_rig(self.layout, context, FALLBACK_OP_ID, "BoneForge Humanoid")
        for rig in discover_rigify_metarigs():
            _quick_rig(self.layout, context, rig["op_id"], rig["label"])

class BF_MT_pose(bpy.types.Menu):
    bl_idname = "BF_MT_pose"
    bl_label = "BoneForge"
    def draw(self, context):
        draw_entries(self.layout, POSE_ENTRIES)

class BF_MT_weights(bpy.types.Menu):
    bl_idname = "BF_MT_weights"
    bl_label = "BoneForge"
    def draw(self, context):
        draw_entries(self.layout, WEIGHT_ENTRIES)

def _add(self, context):
    if operator_exists("boneforge.add_quick_rig"):
        self.layout.menu(BF_MT_quick_rig.bl_idname, text=T("BoneForge"))

def _pose(self, context):
    if any(operator_exists(entry[0]) for entry in POSE_ENTRIES):
        self.layout.menu(BF_MT_pose.bl_idname, text=T("BoneForge"))

def _weights(self, context):
    if any(operator_exists(entry[0]) for entry in WEIGHT_ENTRIES):
        self.layout.menu(BF_MT_weights.bl_idname, text=T("BoneForge"))

_CLASSES = (BF_MT_quick_rig, BF_MT_pose, BF_MT_weights)
_HOOKS = (("VIEW3D_MT_armature_add", _add), ("VIEW3D_MT_pose", _pose), ("VIEW3D_MT_paint_weight", _weights))

def register():
    for cls in _CLASSES:
        bpy.utils.register_class(cls)
    for name, callback in _HOOKS:
        menu = getattr(bpy.types, name, None)
        if menu is not None:
            menu.append(callback)

def unregister():
    for name, callback in reversed(_HOOKS):
        menu = getattr(bpy.types, name, None)
        if menu is not None:
            menu.remove(callback)
    for cls in reversed(_CLASSES):
        if cls.is_registered:
            bpy.utils.unregister_class(cls)
