"""Blender integration check: graph tools read layered (Blender 5) actions.

Blender 5 removed ``Action.fcurves``; keys live in
``layers[].strips[].channelbags[].fcurves``. A keyed armature must be found by
``_bone_fcurves`` and fixed by the Euler Filter operator (a 350 degree jump
is unwrapped). Negative control: on Blender 5 the old ``action.fcurves``
access really fails, so the test exercises the path that used to crash.

Run:  blender --background --factory-startup --python tests/blender_graph_tools_layered_actions.py
"""
import math
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)

import bpy

import boneforge
try:
    boneforge.register()
except Exception as exc:          # already registered / optional parts
    print("register note:", exc)
from boneforge.animation import graph_tools

bpy.ops.wm.read_factory_settings(use_empty=True)
try:
    boneforge.register()
except Exception as exc:
    print("register note:", exc)

arm = bpy.data.objects.new("GT_RIG", bpy.data.armatures.new("GT_RIG"))
bpy.context.scene.collection.objects.link(arm)
bpy.context.view_layer.objects.active = arm
arm.select_set(True)
bpy.ops.object.mode_set(mode='EDIT')
eb = arm.data.edit_bones.new("bone")
eb.head, eb.tail = (0, 0, 0), (0, 0, 1)
bpy.ops.object.mode_set(mode='POSE')
pb = arm.pose.bones["bone"]
pb.rotation_mode = 'XYZ'
for frame, deg in ((1, 170.0), (2, -180.0)):      # a 350 degree flip
    pb.rotation_euler = (math.radians(deg), 0, 0)
    pb.keyframe_insert("rotation_euler", frame=frame)
action = arm.animation_data.action

layered = hasattr(action, "layers") and not hasattr(action, "fcurves")
if layered:
    try:
        list(action.fcurves)
        raise AssertionError("negative control: Action.fcurves unexpectedly exists")
    except AttributeError:
        pass

fcs = list(graph_tools._bone_fcurves(action, "bone"))
assert len(fcs) == 3, ("bone curves not found on a %s action" % ("layered" if layered else "legacy"), fcs)

arm.data.bones.active = pb.bone
with bpy.context.temp_override(selected_pose_bones=[pb], active_object=arm, object=arm):
    result = bpy.ops.boneforge.euler_filter()
assert result == {'FINISHED'}, result
x = next(fc for fc in fcs if fc.array_index == 0)
jump = abs(x.keyframe_points[1].co.y - x.keyframe_points[0].co.y)
assert jump < math.radians(20), ("euler flip not unwrapped", math.degrees(jump))
print("graph tools verified on Blender %s (%s action: 3 bone curves found, "
      "euler flip 350 -> %.0f deg)" % (bpy.app.version_string,
                                       "layered" if layered else "legacy", math.degrees(jump)))
print("ALL GRAPH-TOOLS TESTS PASS")
