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


class PanelDrawTarget:
    """Reuse a panel's draw helpers without instantiating a bpy Panel."""
    def __init__(self, panel_class, layout):
        self.panel_class = panel_class
        self.layout = layout

    def __getattr__(self, name):
        value = inspect.getattr_static(self.panel_class, name)
        return value.__get__(self, self.panel_class) if hasattr(value, "__get__") else value
