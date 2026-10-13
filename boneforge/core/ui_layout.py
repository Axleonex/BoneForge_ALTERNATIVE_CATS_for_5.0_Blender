"""Small Blender-native presentation helpers; no operator behavior."""
import inspect
import textwrap

def operator_exists(idname):
    import bpy
    category, name = idname.split(".", 1)
    try:
        getattr(getattr(bpy.ops, category), name).get_rna_type()
        return True
    except (AttributeError, KeyError, RuntimeError):
        return False

def draw_wrapped(layout, context, text, *, icon="NONE"):
    region = getattr(context, "region", None)
    width = getattr(region, "width", 300) or 300
    scale = getattr(getattr(context.preferences, "system", None), "ui_scale", 1.0)
    columns = max(16, int((width / max(scale, 0.5) - 48) / 7))
    for index, line in enumerate(textwrap.wrap(str(text), width=columns) or [""]):
        layout.label(text=line, icon=icon if index == 0 else "NONE")

_ICON_ALIASES = {"REFRESH": "FILE_REFRESH", "EYE": "HIDE_OFF", "PAINT_SUBTRACT": "REMOVE",
                 "PAINT_ADD": "ADD", "FLOODFILL": "BRUSH_DATA", "WEIGHT_MIRROR": "MOD_MIRROR",
                 "WEIGHT_NORMALIZE": "MOD_VERTEX_WEIGHT", "BREAKDOWNER_POSE": "IPO_BEZIER"}
_icons = None

class NativeLayout:
    """Translate inherited non-Blender icons at the presentation boundary."""
    def __init__(self, layout):
        object.__setattr__(self, "_layout", layout)

    def __setattr__(self, name, value):
        setattr(self._layout, name, value)

    def __getattr__(self, name):
        value = getattr(self._layout, name)
        if not callable(value):
            return value
        def call(*args, **kwargs):
            global _icons
            if "icon" in kwargs:
                if _icons is None:
                    import bpy
                    _icons = {item.identifier for item in bpy.types.UILayout.bl_rna.functions["operator"].parameters["icon"].enum_items}
                icon = kwargs["icon"]
                if icon not in _icons:
                    candidate = _ICON_ALIASES.get(icon, "NONE")
                    kwargs["icon"] = candidate if candidate in _icons else "NONE"
            result = value(*args, **kwargs)
            def wrap(item):
                return NativeLayout(item) if isinstance(item, type(self._layout)) else item
            if isinstance(result, tuple):
                return tuple(wrap(item) for item in result)
            return wrap(result)
        return call

class PanelDrawTarget:
    """Reuse a panel's draw helpers without instantiating a bpy Panel."""
    def __init__(self, panel_class, layout):
        self.panel_class = panel_class
        self.layout = layout if isinstance(layout, NativeLayout) else NativeLayout(layout)

    def __getattr__(self, name):
        value = inspect.getattr_static(self.panel_class, name)
        return value.__get__(self, self.panel_class) if hasattr(value, "__get__") else value
