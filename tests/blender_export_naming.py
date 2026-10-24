"""Real-host naming, isolation, failure cleanup, and FBX roundtrip checks.

Run with --factory-startup --background --python-exit-code 1 --python FILE
-- PACKAGE_PARENT OUTPUT_DIRECTORY. Uses generated fixtures only.
"""
import json
import os
import sys
from pathlib import Path

import bpy
import addon_utils
from types import SimpleNamespace

sys.dont_write_bytecode = True
package, output = sys.argv[sys.argv.index('--') + 1:]
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
from boneforge.io_hub import bone_naming as naming
from boneforge.vrchat.humanoid import mapper
import boneforge

checks = []


def check(name):
    checks.append(name)
    print('PASS:', name, flush=True)


def fixture():
    # A host may protect or hide its startup camera/lights from Select All.
    # This generated fixture owns the factory-startup scene, including those IDs.
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    data = bpy.data.armatures.new('HumanoidData')
    arm = bpy.data.objects.new('Humanoid', data)
    bpy.context.collection.objects.link(arm)
    arm.select_set(True)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode='EDIT')
    slots = {}
    for i, slot in enumerate(naming._UNREAL):
        name = 'source_' + slot
        b = data.edit_bones.new(name)
        b.head = (0, 0, i * .1)
        b.tail = (0, 0, i * .1 + .08)
        if i:
            b.parent = data.edit_bones[0]
        slots[slot] = name
    root = data.edit_bones.new('Root')
    root.head = (0, 0, -.1)
    root.tail = (0, 0, -.02)
    data.edit_bones[0].parent = root
    bpy.ops.object.mode_set(mode='OBJECT')
    mapper.save_mapping(arm, mapper.HumanoidMapping(slots))
    mesh = bpy.data.meshes.new('BodyData')
    mesh.from_pydata([(0, 0, 0), (1, 0, 0), (0, 1, 0)], [], [(0, 1, 2)])
    obj = bpy.data.objects.new('Body', mesh)
    bpy.context.collection.objects.link(obj)
    obj.parent = arm
    mod = obj.modifiers.new('Skin', 'ARMATURE')
    mod.object = arm
    for name in slots.values():
        obj.vertex_groups.new(name=name).add([0, 1, 2], 1 / len(slots), 'REPLACE')
    obj.shape_key_add(name='Basis')
    key = obj.shape_key_add(name='Smile')
    key.data[0].co.x += .2
    arm.pose.bones[slots['LeftUpperArm']].rotation_mode = 'XYZ'
    for frame, rotation in ((1, 0), (10, .7)):
        pb = arm.pose.bones[slots['LeftUpperArm']]
        pb.rotation_euler.z = rotation
        pb.keyframe_insert('rotation_euler', frame=frame)
    constraint = arm.pose.bones[slots['RightHand']].constraints.new('COPY_ROTATION')
    constraint.target = arm
    constraint.subtarget = slots['LeftHand']
    driver = arm.pose.bones[slots['Jaw']].driver_add('rotation_euler', 0)
    driver.driver.expression = 'v'
    var = driver.driver.variables.new()
    var.name = 'v'
    var.type = 'TRANSFORMS'
    var.targets[0].id = arm
    var.targets[0].bone_target = slots['Head']
    attachment = bpy.data.objects.new('Attachment', None)
    bpy.context.collection.objects.link(attachment)
    attachment.parent = arm
    attachment.parent_type = 'BONE'
    attachment.parent_bone = slots['LeftHand']
    attachment['boneforge_vrchat_collider'] = json.dumps({
        'type': 'sphere', 'radius': .1, 'parent_bone': slots['LeftHand']})
    arm.data.bones[slots['Head']]['boneforge_vrchat_physbone'] = json.dumps({
        'collider_bones': [slots['Jaw']], 'pull': .5})
    obj.select_set(True)
    attachment.select_set(True)
    bpy.context.scene.frame_set(1)
    assert set(bpy.context.scene.objects) == {arm, obj, attachment}
    return arm, obj, attachment, slots


def snapshot(arm, mesh, attachment):
    action = arm.animation_data.action
    return {
        'ids': [len(bpy.data.objects), len(bpy.data.meshes), len(bpy.data.armatures),
                len(bpy.data.actions), len(bpy.data.shape_keys)],
        'bones': [b.name for b in arm.data.bones],
        'groups': [g.name for g in mesh.vertex_groups],
        'paths': [f.data_path for f in naming._curves(action)],
        'names': [arm.name, mesh.name, attachment.name],
        'selected': sorted(o.name for o in bpy.context.selected_objects),
        'active': bpy.context.active_object.name,
        'mapping': arm['boneforge_vrchat_humanoid'],
        'parent': attachment.parent_bone,
        'constraint': arm.pose.bones['source_RightHand'].constraints[0].subtarget,
        'driver': arm.animation_data.drivers[0].driver.variables[0].targets[0].bone_target,
        'frame': bpy.context.scene.frame_current,
    }


arm, mesh, attachment, slots = fixture()
before = snapshot(arm, mesh, attachment)
for preset in ('UNITY', 'UNREAL'):
    mapping, recognized = naming.make_plan(arm, preset)
    assert len(recognized) == len(slots)
    with naming.export_copies(bpy.context, [arm, mesh, attachment], preset) as copies:
        a, m, at = copies[arm], copies[mesh], copies[attachment]
        assert a is not arm and a.data is not arm.data
        assert m.data is not mesh.data and m.data.shape_keys is not mesh.data.shape_keys
        assert m.modifiers[0].object == a
        assert a.animation_data.action is not arm.animation_data.action
        for slot, old in slots.items():
            target = mapping.get(old, old)
            assert target in a.data.bones, target
            assert target in m.vertex_groups, target
        assert at.parent is a and at.parent_bone == mapping[slots['LeftHand']]
        con = a.pose.bones[mapping[slots['RightHand']]].constraints[0]
        assert con.target == a and con.subtarget == mapping[slots['LeftHand']]
        drv = a.animation_data.drivers[0]
        assert drv.driver.variables[0].targets[0].id == a
        assert drv.driver.variables[0].targets[0].bone_target == mapping[slots['Head']]
        assert all('source_' not in fc.data_path for fc in naming._curves(a.animation_data.action))
        assert all('source_' not in fc.data_path for fc in a.animation_data.drivers)
        bpy.context.scene.frame_set(10)
        assert abs(a.pose.bones[mapping[slots['LeftUpperArm']]].rotation_euler.z - .7) < 1e-5
        bpy.context.scene.frame_set(1)
        from boneforge.vrchat.export import sidecar
        side = sidecar.generate_sidecar(a, bpy.context.scene.boneforge_vrc_export_settings)
        smap = {s['slot_name']: s['bone_name'] for s in side['humanoid_mapping']['slots']}
        assert smap['Hips'] == mapping[slots['Hips']]
        del a['boneforge_vrchat_humanoid']
        assert naming.make_plan(a, preset)[0] == {}
        opposite = 'UNREAL' if preset == 'UNITY' else 'UNITY'
        reverse, recognized_again = naming.make_plan(a, opposite)
        assert len(recognized_again) == len(slots) and reverse
    assert snapshot(arm, mesh, attachment) == before
    check(preset + ' copies: weights, shape keys, action evaluation, drivers, constraints, attachment, sidecar, source preservation')

try:
    with naming.export_copies(bpy.context, [arm, mesh, attachment], 'UNREAL'):
        raise RuntimeError('injected exporter failure')
except RuntimeError:
    pass
assert snapshot(arm, mesh, attachment) == before
check('failure restores selection, active object, names and all datablock counts')

# Every export section exposes the same registered choices, with safe default.
settings = bpy.context.scene.boneforge_game_export_settings
unity = bpy.context.scene.boneforge_vrc_export_settings
for owner in (settings, unity):
    assert owner.bone_naming == 'NONE'
    assert {i[0] for i in naming.naming_items(owner, bpy.context)} == {'NONE', 'UNITY', 'UNREAL'}
check('registered settings/defaults in both export sections')

# Collision and ambiguity must fail before any scene mutation.
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='EDIT')
b = arm.data.edit_bones.new('pelvis')
b.head = (0, 0, -1)
b.tail = (0, 0, -.9)
bpy.ops.object.mode_set(mode='OBJECT')
collision_before = snapshot(arm, mesh, attachment)
try:
    with naming.export_copies(bpy.context, [arm, mesh], 'UNREAL'):
        raise AssertionError('collision accepted')
except ValueError as exc:
    assert 'conflict' in str(exc) or 'duplicate' in str(exc)
assert snapshot(arm, mesh, attachment) == collision_before
bpy.ops.object.mode_set(mode='EDIT')
arm.data.edit_bones.remove(arm.data.edit_bones['pelvis'])
bpy.ops.object.mode_set(mode='OBJECT')
check('occupied target rejected without scene mutation')

track = arm.animation_data.nla_tracks.new()
strip = track.strips.new('NLA test', 20, arm.animation_data.action)
with naming.export_copies(bpy.context, [arm, mesh], 'UNREAL') as copies:
    copied_strip = copies[arm].animation_data.nla_tracks[-1].strips[0]
    assert copied_strip.action is not strip.action
    assert all('source_' not in fc.data_path for fc in naming._curves(copied_strip.action))
arm.animation_data.nla_tracks.remove(track)
assert snapshot(arm, mesh, attachment) == before
check('NLA action copies and renamed channels preserve original NLA')

class Layout:
    def __init__(self):
        self.props = []
        self.labels = []
    def prop(self, owner, prop, **kwargs):
        assert hasattr(owner, prop), prop
        self.props.append(prop)
    def label(self, **kwargs):
        self.labels.append(kwargs.get('text', ''))
    def operator(self, *args, **kwargs):
        return SimpleNamespace()
    def __getattr__(self, name):
        return lambda *a, **k: self

from boneforge.io_hub.game_export import draw_unreal_export_settings
from boneforge.vrchat.export.vrchat_export import draw_export_settings
for owner, draw in ((settings, draw_unreal_export_settings), (unity, draw_export_settings)):
    for preset in ('NONE', 'UNITY', 'UNREAL'):
        owner.bone_naming = preset
        layout = Layout()
        draw(layout, bpy.context)
        assert 'bone_naming' in layout.props
        if preset != 'NONE':
            assert any('source_Hips' in label for label in layout.labels)
    owner.bone_naming = 'NONE'
check('both export settings draw all naming choices and before/after previews')

def roundtrip(path, preset, animated, forbidden=None):
    existing = set(bpy.data.objects)
    existing_data = {coll: set(getattr(bpy.data, coll)) for coll in
                     ('meshes', 'armatures', 'actions')}
    assert bpy.ops.import_scene.fbx(filepath=str(path)) == {'FINISHED'}
    imported = set(bpy.data.objects) - existing
    if forbidden:
        assert not any(o.name.startswith(forbidden) for o in imported)
    rig = next(o for o in imported if o.type == 'ARMATURE')
    body = next(o for o in imported if o.type == 'MESH')
    target = slots['Hips'] if preset == 'NONE' else ('Hips' if preset == 'UNITY' else 'pelvis')
    assert target in rig.data.bones and target in body.vertex_groups
    assert body.data.shape_keys and 'Smile' in body.data.shape_keys.key_blocks
    if animated:
        assert rig.animation_data and rig.animation_data.action
        curves = list(naming._curves(rig.animation_data.action))
        assert curves and any(len(fc.keyframe_points) > 1 for fc in curves)
        arm_bone = slots['LeftUpperArm'] if preset == 'NONE' else (
            'LeftUpperArm' if preset == 'UNITY' else 'upperarm_l')
        bpy.context.scene.frame_set(1)
        first = rig.pose.bones[arm_bone].matrix.to_quaternion()
        bpy.context.scene.frame_set(10)
        last = rig.pose.bones[arm_bone].matrix.to_quaternion()
        assert first.rotation_difference(last).angle > .1, 'Imported bone did not move'
        bpy.context.scene.frame_set(1)
    for obj in imported:
        bpy.data.objects.remove(obj, do_unlink=True)
    for coll, original_ids in existing_data.items():
        collection = getattr(bpy.data, coll)
        for data in set(collection) - original_ids:
            collection.remove(data)
    for obj in bpy.context.selected_objects:
        obj.select_set(False)
    for obj in (arm, mesh, attachment):
        obj.select_set(True)
    bpy.context.view_layer.objects.active = arm

for preset in ('NONE', 'UNITY', 'UNREAL'):
    path = output / (preset + '.fbx')
    result = bpy.ops.boneforge.export_unreal_fbx(
        filepath=str(path), bone_naming=preset, bake_anim=True,
        embed_textures=False, use_selection=True)
    assert result == {'FINISHED'} and path.is_file()
    assert snapshot(arm, mesh, attachment) == before
    roundtrip(path, preset, animated=True)
    check(preset + ' public Unreal exporter FBX roundtrip: names, weights, shape keys, baked animation')

for preset in ('NONE', 'UNITY', 'UNREAL'):
    unity.export_path = str(output)
    unity.avatar_name = 'Unity-' + preset
    unity.bone_naming = preset
    unity.embed_textures = False
    unity.export_sidecar = True
    expected = snapshot(arm, mesh, attachment)
    assert bpy.ops.boneforge.vrc_export_to_unity() == {'FINISHED'}
    path = output / (unity.avatar_name + '.fbx')
    assert path.is_file()
    assert snapshot(arm, mesh, attachment) == expected
    side = json.loads(path.with_suffix('.bfvrc').read_text(encoding='utf-8'))
    smap = {s['slot_name']: s['bone_name'] for s in side['humanoid_mapping']['slots']}
    if preset != 'NONE':
        assert smap['Hips'] == ('Hips' if preset == 'UNITY' else 'pelvis')
        mapping = naming.make_plan(arm, preset)[0]
        assert side['physbone_chains'][0]['root_bone'] == mapping[slots['Head']]
        assert side['physbone_chains'][0]['collider_bones'] == [mapping[slots['Jaw']]]
        assert any(c['parent_bone'] == mapping[slots['LeftHand']] for c in side['colliders'])
    roundtrip(path, preset, animated=False)
    check(preset + ' public Unity exporter FBX/sidecar roundtrip and source preservation')

if (Path(boneforge.__file__).parent / 'io_hub/profile_export.py').is_file():
    from boneforge.io_hub.profile_export import export_with_profile
    from boneforge.io_hub import profiles
    # Pick the real FBX profile registry ID; do not assume its spelling.
    profile = next(key for key, p in profiles.EXPORT_PROFILES.items() if p['container'] == 'FBX')
    ok, message = export_with_profile(bpy.context, profile, str(output / 'Unsafe-All.fbx'),
                                      action_mode='ALL', t_pose=False, bone_naming='UNREAL')
    assert not ok and 'Active Action' in message
    assert not (output / 'Unsafe-All.fbx').exists()
    assert snapshot(arm, mesh, attachment) == before
    ok, message = export_with_profile(bpy.context, profile, str(output / 'Profile.fbx'),
                                      t_pose=False, bone_naming='UNREAL')
    assert ok, message
    assert snapshot(arm, mesh, attachment) == before
    roundtrip(output / 'Profile.fbx', 'UNREAL', animated=True)
    check('BoneCraft profile exporter uses Unreal naming with source preservation')

# Whole-view-layer export must preserve excluded collections' export scope.
print('Whole-view-layer fixture:', [(o.name, o.type) for o in bpy.context.view_layer.objects], flush=True)
collection = bpy.data.collections.new('Excluded collection')
bpy.context.scene.collection.children.link(collection)
excluded = bpy.data.objects.new('NeverExportExcluded', None)
collection.objects.link(excluded)
bpy.context.view_layer.layer_collection.children[collection.name].exclude = True
expected = snapshot(arm, mesh, attachment)
path = output / 'ViewLayer.fbx'
assert bpy.ops.boneforge.export_unreal_fbx(filepath=str(path), bone_naming='UNREAL',
    bake_anim=True, embed_textures=False, use_selection=False) == {'FINISHED'}
assert snapshot(arm, mesh, attachment) == expected
roundtrip(path, 'UNREAL', animated=True, forbidden='NeverExportExcluded')
check('whole-view-layer named export keeps excluded objects out of FBX')

report = {'result': 'PASS', 'host': bpy.app.version_string,
          'version': boneforge.bl_info['version'], 'checks': checks}
(output / 'summary.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report), flush=True)
