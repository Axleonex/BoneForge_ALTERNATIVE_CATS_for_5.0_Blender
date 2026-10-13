"""Mirror shared Rig Builder/CATS sections into Blender's Scene Properties."""
import bpy
from .prefs import addon_prefs
from .ui_layout import PanelDrawTarget

ROOTS = ("BF_PT_rb_setup", "CATS_PT_main", "BF_PT_sb_vrchat", "BF_PT_cats_vrc_tools", "BF_PT_sb_io")
SUFFIX = "_Scene"
_classes = []

class _Preferences:
    def __init__(self, preferences):
        self.preferences = preferences
    def __getattr__(self, name):
        if name.startswith("show_tab_"):
            return True
        return getattr(self.preferences, name)

class _Context:
    """Evaluate original tab polls without changing saved sidebar preferences."""
    def __init__(self, context):
        from types import SimpleNamespace
        self.context = context
        addons = dict(context.preferences.addons.items())
        addon = addons.get("boneforge")
        if addon is not None:
            addons["boneforge"] = SimpleNamespace(preferences=_Preferences(addon.preferences))
        class PreferencesProxy:
            def __getattr__(self, name):
                return getattr(context.preferences, name)
        self.preferences = PreferencesProxy()
        self.preferences.addons = addons
    def __getattr__(self, name):
        return getattr(self.context, name)

def _poll(original):
    def poll(cls, context):
        prefs = addon_prefs(context)
        if prefs is not None and not prefs.show_scene_tab:
            return False
        return original.poll(_Context(context)) if hasattr(original, "poll") else True
    return poll

def _draw(original, method):
    def draw(self, context):
        proxy = PanelDrawTarget(original, self.layout)
        getattr(proxy, method)(_Context(context))
    return draw

def register():
    unregister()
    panels = [cls for cls in bpy.types.Panel.__subclasses__()
              if cls.is_registered and getattr(cls, "bl_space_type", "") == "VIEW_3D"]
    by_id = {getattr(cls, "bl_idname", cls.__name__): cls for cls in panels}
    from .tool_registry import get_registry
    registry = get_registry()
    owners = {"BF_PT_rb_setup": "phase3_autorig", "BF_PT_sb_vrchat": "vrchat_avatar",
              "BF_PT_cats_vrc_tools": "vrchat_avatar"}
    for order, root in enumerate(ROOTS, 1):
        if root in owners and not registry.is_enabled(owners[root]):
            continue
        queue = [root]
        while queue:
            panel_id = queue.pop(0)
            original = by_id.get(panel_id)
            if original is None:
                continue
            parent = getattr(original, "bl_parent_id", "")
            attrs = dict(bl_idname=panel_id + SUFFIX, bl_label=original.bl_label,
                         bl_space_type="PROPERTIES", bl_region_type="WINDOW",
                         bl_context="scene", bl_order=order if panel_id == root else getattr(original, "bl_order", 0),
                         bl_options=set(getattr(original, "bl_options", set())) | {"DEFAULT_CLOSED"},
                         poll=classmethod(_poll(original)), draw=_draw(original, "draw"))
            if panel_id != root:
                attrs["bl_parent_id"] = parent + SUFFIX
            if hasattr(original, "draw_header"):
                attrs["draw_header"] = _draw(original, "draw_header")
            mirror = type(panel_id + SUFFIX, (bpy.types.Panel,), attrs)
            bpy.utils.register_class(mirror)
            _classes.append(mirror)
            queue.extend(c.bl_idname for c in by_id.values() if getattr(c, "bl_parent_id", "") == panel_id)

def unregister():
    for cls in reversed(_classes):
        if cls.is_registered:
            bpy.utils.unregister_class(cls)
    _classes.clear()
