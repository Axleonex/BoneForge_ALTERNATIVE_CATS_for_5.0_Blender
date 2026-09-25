"""Blender integration check: retargeting works with layered (Blender 5) actions.

Blender 5 removed ``Action.fcurves``. A clip keyed on one armature must be
listed (bone names), found as skeletal animation, and retargeted onto another
armature's bone; played through an NLA strip (as the preview does) it must
move the target bone to the source's angle. Negative control: on Blender 5
the old ``action.fcurves`` access really fails.

Run:  blender --background --factory-startup --python tests/blender_retarget_layered_actions.py
"""
import math
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)

import bpy

bpy.ops.wm.read_factory_settings(use_empty=True)
import boneforge
try:
    boneforge.register()
except Exception as exc:
    print("register note:", exc)
from boneforge.autorig import retarget


def rig(name, bone):
    arm = bpy.data.objects.new(name, bpy.data.armatures.new(name))
    bpy.context.scene.collection.objects.link(arm)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode='EDIT')
    eb = arm.data.edit_bones.new(bone)
    eb.head, eb.tail = (0, 0, 0), (0, 0, 1)
    bpy.ops.object.mode_set(mode='OBJECT')
    return arm


src = rig("SRC", "src_bone")
dst = rig("DST", "dst_bone")
pb = src.pose.bones["src_bone"]
pb.rotation_mode = 'XYZ'
for frame, deg in ((1, 0.0), (10, 45.0)):
    pb.rotation_euler = (math.radians(deg), 0, 0)
    pb.keyframe_insert("rotation_euler", frame=frame)
clip = src.animation_data.action

layered = not hasattr(clip, "fcurves")
if layered:
    try:
        list(clip.fcurves)
        raise AssertionError("negative control: Action.fcurves unexpectedly exists")
    except AttributeError:
        pass

assert retarget._extract_bone_names_from_action(clip) == ["src_bone"], retarget._extract_bone_names_from_action(clip)
assert retarget._find_action_with_bone_animation() is clip
mappings = [{"source": "src_bone", "target": "dst_bone", "matched": True}]
out = retarget.retarget_action(clip, dst, mappings, None)
assert out is not None, "retarget produced no action"
curves = retarget._action_fcurves(out)
assert sorted(fc.data_path for fc in curves) == ['pose.bones["dst_bone"].rotation_euler'] * 3, \
    [fc.data_path for fc in curves]

dst.pose.bones["dst_bone"].rotation_mode = 'XYZ'
dst.animation_data_create()
track = dst.animation_data.nla_tracks.new()
track.strips.new(out.name, 1, out)
bpy.context.scene.frame_set(10)
angle = math.degrees(dst.pose.bones["dst_bone"].rotation_euler.x)
assert abs(angle - 45.0) < 0.5, ("preview (NLA) did not move the target bone", angle)
# Apply assigns the action directly
dst.animation_data.nla_tracks.remove(track)
dst.pose.bones["dst_bone"].rotation_euler = (0, 0, 0)
dst.animation_data.action = out
bpy.context.scene.frame_set(1)
bpy.context.scene.frame_set(10)
applied = math.degrees(dst.pose.bones["dst_bone"].rotation_euler.x)
assert abs(applied - 45.0) < 0.5, ("apply (direct action) did not move the target bone", applied)
print("retarget verified on Blender %s (%s actions: bone listed, clip found, "
      "3 curves remapped, target bone at %.1f deg on frame 10 via preview and apply)"
      % (bpy.app.version_string, "layered" if layered else "legacy", angle))
print("ALL RETARGET-COMPAT TESTS PASS")
