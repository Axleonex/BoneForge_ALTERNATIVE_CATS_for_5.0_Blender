"""Real-host MMD Tools installation and PMX import regression.

Run with isolated BLENDER_USER_* directories and --python-exit-code 1.
Arguments after --: package-parent upstream-zip evidence-json [auto].
"""
import importlib
import json
import sys
from pathlib import Path

import addon_utils
import bpy

sys.dont_write_bytecode = True
args = sys.argv[sys.argv.index('--') + 1:]
parent, archive, evidence = args[:3]
auto = args[3:] == ['auto']
if parent.lower().endswith('.zip'):
    assert bpy.ops.preferences.addon_install(filepath=parent, overwrite=True) == {'FINISHED'}
    parent = bpy.utils.user_resource('SCRIPTS', path='addons', create=True)
sys.path.insert(0, parent)
print('MMD_TEST enabling product', flush=True)
assert addon_utils.enable('boneforge', default_set=True) is not None
import boneforge
assert Path(boneforge.__file__).resolve().is_relative_to(Path(parent).resolve()), boneforge.__file__
from boneforge.mmd import bridge

# Exercise the actual file-browser operator, including activation/detection.
print('MMD_TEST installing dependency ' + ('automatically' if auto else 'from disk'), flush=True)
if auto:
    assert bpy.ops.boneforge.mmd_install_auto() == {'FINISHED'}
else:
    assert bpy.ops.boneforge.mmd_install_from_disk(filepath=archive) == {'FINISHED'}
status = bridge.mmd_addon_status()
assert status['enabled'] and status['import_pmx_available'], status
assert bridge.find_mmd_addon() is not None
module = status['module_name']
assert module.startswith('bl_ext.'), module
# This dependency is bundled as a wheel and is lost by legacy repackaging.
import opencc

# Build a valid minimal PMX with the upstream writer and a real bone.
pmx = importlib.import_module(module + '.core.pmx')
model = pmx.Model()
model.name = 'BoneForge MMD regression'
model.name_e = 'BoneForge MMD regression'
bone = pmx.Bone()
bone.name = 'Root'
bone.name_e = 'Root'
bone.location = [0.0, 0.0, 0.0]
bone.displayConnection = [0.0, 1.0, 0.0]
model.bones.append(bone)
for co in ([0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]):
    vertex = pmx.Vertex()
    vertex.co = co
    vertex.normal = [0.0, 0.0, 1.0]
    vertex.weight = pmx.BoneWeight()
    vertex.weight.bones = [0]
    model.vertices.append(vertex)
model.faces.append([0, 1, 2])
material = pmx.Material()
material.name = material.name_e = 'Test Material'
material.diffuse = [0.8, 0.8, 0.8, 1.0]
material.specular = [0.0, 0.0, 0.0]
material.ambient = [0.2, 0.2, 0.2]
material.edge_color = [0.0, 0.0, 0.0, 1.0]
material.vertex_count = 3
model.materials.append(material)
fixture = str(Path(evidence).with_suffix('.pmx'))
pmx.save(fixture, model)
before = {obj.name for obj in bpy.data.objects if obj.type == 'ARMATURE'}
assert bpy.ops.boneforge.mmd_import_pmx(filepath=fixture) == {'FINISHED'}
after = {obj.name for obj in bpy.data.objects if obj.type == 'ARMATURE'}
assert len(after - before) == 1, (before, after)
assert any(obj.type == 'MESH' and len(obj.data.vertices) == 3
           and len(obj.data.polygons) == 1 for obj in bpy.data.objects)

# A disabled stale legacy copy must not mask the enabled extension.
assert status['export_pmx_available'] and status['import_vmd_available'], status
result = {'host': bpy.app.version_string, 'binary': bpy.app.binary_path,
          'install_mode': 'auto' if auto else 'disk',
          'module': module, 'status': status, 'new_armatures': sorted(after - before),
          'wheel_dependency': opencc.__name__, 'result': 'PASS'}
Path(evidence).write_text(json.dumps(result, indent=2), encoding='utf-8')
print('MMD_HOST_PASS ' + json.dumps(result))
