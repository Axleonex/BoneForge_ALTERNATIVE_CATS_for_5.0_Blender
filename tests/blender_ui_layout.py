"""Run with Blender --background --factory-startup --python this_file.py."""
import ast
import faulthandler
faulthandler.dump_traceback_later(30, repeat=True)
import json
import sys
sys.dont_write_bytecode = True
import zipfile
from pathlib import Path
from types import SimpleNamespace
import bpy
import addon_utils

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from boneforge.core.ui_layout import PanelDrawTarget, operator_exists

def operator_contract(source):
    tree = ast.parse(source)
    result = {}
    for cls in ast.walk(tree):
        if not isinstance(cls, ast.ClassDef):
            continue
        identifier = None
        for attr in cls.body:
            if isinstance(attr, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "bl_idname" for t in attr.targets):
                try:
                    identifier = ast.literal_eval(attr.value)
                except ValueError:
                    pass
        if identifier and identifier.startswith("boneforge."):
            result[identifier] = {method.name: ast.dump(method, include_attributes=False)
                                  for method in cls.body if isinstance(method, ast.FunctionDef)
                                  and method.name in {"execute", "invoke", "modal", "poll"}}
    return result

with zipfile.ZipFile(ROOT / "releases/BoneForge-9.0.0.zip") as baseline:
    before, after = {}, {}
    for name in baseline.namelist():
        if name.endswith(".py"):
            before.update(operator_contract(baseline.read(name)))
    for path in (ROOT / "boneforge").rglob("*.py"):
        after.update(operator_contract(path.read_bytes()))
    assert before == after, "Operator IDs or behavior changed"

ICONS = {item.identifier for item in bpy.types.UILayout.bl_rna.functions["operator"].parameters["icon"].enum_items}

class Layout:
    def __init__(self, records=None, expanded=True):
        self.records = [] if records is None else records
        self.expanded = expanded
    def _child(self, *args, **kwargs):
        return Layout(self.records, self.expanded)
    row = column = box = split = grid_flow = column_flow = _child
    def label(self, *, text="", icon="NONE", **kwargs):
        assert icon in ICONS, icon
        self.records.append(("label", text))
    def operator(self, idname, *, icon="NONE", **kwargs):
        assert operator_exists(idname), "Unregistered UI operator: " + idname
        assert icon in ICONS, "Unsupported Blender icon: " + icon
        self.records.append(("operator", idname))
        return SimpleNamespace()
    def prop(self, data, name, **kwargs):
        assert hasattr(data, name), "Missing displayed property: " + name
        self.records.append(("property", name))
    def panel(self, idname, **kwargs):
        return self._child(), self._child() if self.expanded else None
    def menu(self, name, **kwargs):
        assert hasattr(bpy.types, name), name
    def __getattr__(self, name):
        return lambda *args, **kwargs: None

class Context:
    def __init__(self, width):
        self.region = SimpleNamespace(width=width, view2d=None)
    def __getattr__(self, name):
        return getattr(bpy.context, name)

def draw(cls, context, expanded=True):
    layout = Layout(expanded=expanded)
    target = PanelDrawTarget(cls, layout)
    target.layout = layout  # Match Blender: only explicit delegated/mirror draws adapt icons.
    target.draw(context)
    assert not any(kind == "label" and "Draw error" in value for kind, value in layout.records), cls.__name__
    return layout.records

def registered_ops():
    result = set()
    for name, module in list(sys.modules.items()):
        if name.startswith("boneforge"):
            for cls in vars(module).values():
                if isinstance(cls, type) and issubclass(cls, bpy.types.Operator) and getattr(cls, "is_registered", False) and getattr(cls, "bl_idname", None):
                    result.add(cls.bl_idname)
    return result

print("CHECK: registration", flush=True)
module = addon_utils.enable("boneforge", default_set=True)
assert module is not None
original_ops = registered_ops()
assert len(original_ops) == 273, len(original_ops)
if (ROOT / ".git/ui-baseline.json").exists():
    assert sorted(original_ops) == json.loads((ROOT / ".git/ui-baseline.json").read_text())

from boneforge.core import access, scene_tab_mirror
from boneforge.core.prefs import addon_prefs
from boneforge.taskboard import sidebar
from boneforge.io_hub.panel import BF_PT_sb_io
from boneforge.vrchat.cats.cats_panel import CATS_PT_main
from boneforge.autorig.wizard import BF_PT_WizardPanel

assert BF_PT_sb_io.bl_category == "CATS"
assert sidebar.BF_PT_sb_wizard.bl_order < sidebar.BF_PT_sb_quick_rig.bl_order < sidebar.BF_PT_rb_mannequin.bl_order
for name in ("BF_PT_sb_vrc_naming", "BF_PT_sb_vrc_clothing", "BF_PT_sb_vrc_perf"):
    assert getattr(sidebar, name).bl_parent_id == "BF_PT_cats_vrc_tools"
assert len(scene_tab_mirror._classes) > 20
assert set(scene_tab_mirror.ROOTS) <= {cls.bl_idname.removesuffix("_Scene") for cls in scene_tab_mirror._classes}

arm_data = bpy.data.armatures.new("UI test rig")
arm = bpy.data.objects.new("UI test rig", arm_data)
bpy.context.collection.objects.link(arm)
mesh = bpy.data.objects.get("Cube")
draws = 0
for active in (None, mesh, arm):
    bpy.context.view_layer.objects.active = active
    for width in (220, 480):
        context = Context(width)
        for expanded in (False, True):
            for cls in (*sidebar._CLASSES, BF_PT_sb_io, CATS_PT_main, *scene_tab_mirror._classes, *access._CLASSES):
                if not hasattr(cls, "poll") or cls.poll(context):
                    records = draw(cls, context, expanded)
                    assert not any(kind == "operator" and value == "boneforge.autorig_run_detection" for kind, value in records)
                    draws += 1
        # All wizard steps reuse their original helpers through the wrapper.
        session = bpy.context.scene.boneforge_autorig_session
        session.is_active = True
        session.mesh_object_name = mesh.name
        for step in range(9):
            session.wizard_step = step
            draw(sidebar.BF_PT_sb_wizard, context)
            draws += 1
        session.is_active = False

print("CHECK: draws completed", draws, flush=True)
from boneforge.autorig import quick_human
original_discovery = quick_human.discover_rigify_metarigs
try:
    quick_human.discover_rigify_metarigs = lambda: [{"group": "humans", "op_id": quick_human.FALLBACK_OP_ID,
                                                   "label": "Sample metarig", "rig_name": "sample"}]
    for width in (220, 480):
        draw(sidebar.BF_PT_sb_quick_rig, Context(width))
        draw(getattr(bpy.types, "BF_PT_sb_quick_rig_Scene"), Context(width))
        draw(access.BF_MT_quick_rig, Context(width))
        draws += 3
finally:
    quick_human.discover_rigify_metarigs = original_discovery

prefs = addon_prefs(bpy.context)
assert prefs is not None
prefs.show_tab_rig_builder = prefs.show_tab_cats = False
assert not sidebar.BF_PT_rb_setup.poll(bpy.context)
assert not CATS_PT_main.poll(bpy.context)
for root in scene_tab_mirror.ROOTS:
    assert getattr(bpy.types, root + "_Scene").poll(bpy.context), root
prefs.show_scene_tab = False
assert not any(cls.poll(bpy.context) for cls in scene_tab_mirror._classes)
prefs.show_scene_tab = prefs.show_tab_rig_builder = prefs.show_tab_cats = True

# Exercise the actual UI toggle callback, without waiting on a timer.
from boneforge.core.tool_toggle_operator import BF_OT_ToggleTool
# Rejecting a dependency-blocked toggle must restore the complete mirror tree.
print("CHECK: blocked toggle", flush=True)
before_mirrors = {cls.bl_idname for cls in scene_tab_mirror._classes}
BF_OT_ToggleTool._deferred_work({"tool_id": "io_hub"})
assert before_mirrors == {cls.bl_idname for cls in scene_tab_mirror._classes}
for leaf in ("mmd_bridge", "vrm_bridge"):
    BF_OT_ToggleTool._deferred_work({"tool_id": leaf})
for tool_id, panel_id in (("io_hub", "BF_PT_sb_io"), ("phase3_autorig", "BF_PT_rb_setup"), ("taskboard_overview", "BF_PT_rb_setup")):
    print("CHECK: toggle", tool_id, flush=True)
    BF_OT_ToggleTool._deferred_work({"tool_id": tool_id})
    assert not hasattr(bpy.types, panel_id + "_Scene"), (tool_id, panel_id)
    BF_OT_ToggleTool._deferred_work({"tool_id": tool_id})
    assert hasattr(bpy.types, panel_id + "_Scene"), (tool_id, panel_id)
for leaf in ("vrm_bridge", "mmd_bridge"):
    BF_OT_ToggleTool._deferred_work({"tool_id": leaf})
assert registered_ops() == original_ops

for language in ("en", "ja", "ko", "zh", "pt", "es", "fr"):
    prefs.language = language
    draw(sidebar.BF_PT_sb_vrchat, Context(220))
    draw(sidebar.BF_PT_cats_vrc_tools, Context(220))
prefs.language = "en"

print("CHECK: unregister", flush=True)
addon_utils.disable("boneforge", default_set=True)
assert not scene_tab_mirror._classes
assert not any(hasattr(bpy.types, cls.bl_idname) for cls in access._CLASSES)
assert not registered_ops(), "Operators left registered"
module = addon_utils.enable("boneforge", default_set=True)
assert module is not None and registered_ops() == original_ops
print("CHECK: unregister", flush=True)
addon_utils.disable("boneforge", default_set=True)
faulthandler.cancel_dump_traceback_later()
print("PASS:", draws, "panel/menu draws; 273 unchanged operators; sidebar/Scene visibility; toggles; reload; seven languages; Blender", bpy.app.version_string)
