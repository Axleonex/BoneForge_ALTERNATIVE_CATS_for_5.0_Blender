"""Public export operators from Properties in Object, Pose and Edit Mode.

Arguments: PACKAGE_PARENT_OR_ZIP OUTPUT_DIRECTORY [--probe].
Runs in a factory-startup host; reuses only generated-fixture functions from
blender_export_naming.py, not that script's executing test body.
"""
import ast
import json
import os
import sys
from pathlib import Path
from unittest.mock import patch
from types import SimpleNamespace

import bpy
import addon_utils

sys.dont_write_bytecode = True
package, output, *options = sys.argv[sys.argv.index('--') + 1:]
output = Path(os.environ['LAPART_RUN_DIR'] if output == '@run' else output)
output.mkdir(parents=True, exist_ok=True)
if package.lower().endswith('.zip'):
    for kind in ('CONFIG', 'SCRIPTS', 'EXTENSIONS', 'DATAFILES'):
        folder = output / ('user-' + kind.lower())
        folder.mkdir(exist_ok=True)
        os.environ['BLENDER_USER_' + kind] = str(folder)
    assert Path(bpy.utils.user_resource('SCRIPTS', create=True)).resolve() == (output / 'user-scripts').resolve()
    bpy.ops.preferences.addon_install(filepath=package, overwrite=True)
    package = bpy.utils.user_resource('SCRIPTS', path='addons', create=True)
sys.path.insert(0, package)
assert addon_utils.enable('boneforge', default_set=True) is not None
import boneforge
from boneforge.io_hub import bone_naming as naming
from boneforge.vrchat.humanoid import mapper
from boneforge.vrchat.export import vrchat_export

fixture_source = Path(__file__).with_name('blender_export_naming.py')
module = ast.parse(fixture_source.read_text(encoding='utf-8'))
helpers = [n for n in module.body if isinstance(n, ast.FunctionDef) and n.name in {'fixture', 'snapshot'}]
exec(compile(ast.Module(body=helpers, type_ignores=[]), str(fixture_source), 'exec'))

area = next(a for a in bpy.context.screen.areas if a.type == 'PROPERTIES')
region = next(r for r in area.regions if r.type == 'WINDOW')
reports = []


def state(arm, mesh, attachment):
    data = snapshot(arm, mesh, attachment)
    data['mode'] = arm.mode
    data['object_selection'] = sorted(o.name for o in bpy.context.view_layer.objects if o.select_get())
    bones = arm.data.edit_bones if arm.mode == 'EDIT' else arm.pose.bones
    data['bone_selection'] = sorted(b.name for b in bones
        if getattr(b, 'select', getattr(getattr(b, 'bone', None), 'select', False)))
    bone_data = arm.data.edit_bones if arm.mode == 'EDIT' else arm.data.bones
    data['active_bone'] = bone_data.active.name if bone_data.active else None
    return data


def prepare(mode):
    if bpy.context.object and bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    arm, mesh, attachment, slots = fixture()
    for b in arm.pose.bones:
        setattr(b if hasattr(b, 'select') else b.bone, 'select', False)
    b = arm.pose.bones[slots['LeftHand']]
    setattr(b if hasattr(b, 'select') else b.bone, 'select', True)
    arm.data.bones.active = arm.data.bones[slots['LeftHand']]
    if mode != 'OBJECT':
        bpy.ops.object.mode_set(mode=mode)
    return arm, mesh, attachment


cases = [('UNITY_EXPORT', 'POSE', 'NONE'), ('UNITY_EXPORT', 'EDIT', 'NONE')]
if '--probe' not in options:
    cases = [(target, mode, preset) for target in ('UNITY_EXPORT', 'UNREAL_EXPORT')
             for mode in ('OBJECT', 'POSE', 'EDIT') for preset in ('NONE', 'UNITY', 'UNREAL')]

for target, mode, preset in cases:
    arm, mesh, attachment = prepare(mode)
    settings = bpy.context.scene.boneforge_vrc_export_settings
    settings.export_path = str(output)
    settings.avatar_name = f'{target}-{mode}-{preset}'
    settings.bone_naming = preset
    settings.export_sidecar = False
    settings.embed_textures = False
    path = output / (settings.avatar_name + '.fbx')
    before = state(arm, mesh, attachment)
    result, error = None, None
    with bpy.context.temp_override(area=area, region=region):
        try:
            if target == 'UNITY_EXPORT':
                result = bpy.ops.boneforge.vrc_export_to_unity()
            else:
                result = bpy.ops.boneforge.export_unreal_fbx(filepath=str(path),
                    bone_naming=preset, use_selection=True, embed_textures=False)
        except Exception as exc:
            error = str(exc)
    restored = state(arm, mesh, attachment) == before
    row = {'target': target, 'mode': mode, 'preset': preset, 'result': sorted(result or []),
           'error': error, 'restored': restored, 'file_exists': path.is_file()}
    reports.append(row)
    print(json.dumps(row), flush=True)
    if '--probe' not in options:
        assert result == {'FINISHED'} and path.is_file(), row
        assert restored, row

if '--probe' not in options:
    # Fail at the actual exporter boundary while the caller starts in Pose Mode.
    arm, mesh, attachment = prepare('POSE')
    settings = bpy.context.scene.boneforge_vrc_export_settings
    settings.export_path = str(output)
    settings.avatar_name = 'injected-error'
    settings.bone_naming = 'UNITY'
    before = state(arm, mesh, attachment)
    messages = []
    injected = []
    def fail_export(**kwargs):
        injected.append(kwargs)
        raise RuntimeError('injected FBX error')
    class BpyProxy:
        ops = SimpleNamespace(export_scene=SimpleNamespace(fbx=fail_export))
        def __getattr__(self, name):
            return getattr(bpy, name)
    with bpy.context.temp_override(area=area, region=region):
        with patch.object(vrchat_export, 'bpy', BpyProxy()):
            try:
                bpy.ops.boneforge.vrc_export_to_unity()
            except RuntimeError as exc:
                messages.append(str(exc))
    assert state(arm, mesh, attachment) == before
    assert len(injected) == 1
    assert any('injected FBX error' in m for m in messages), messages
    assert not (output / 'injected-error.fbx').exists()
    reports.append({'target': 'failure cleanup in Pose', 'restored': True})

summary = {'result': 'PROBE' if '--probe' in options else 'PASS',
           'host': bpy.app.version_string, 'version': boneforge.bl_info['version'], 'cases': reports}
(output / 'summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
print(json.dumps(summary), flush=True)
