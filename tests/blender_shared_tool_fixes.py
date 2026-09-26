"""Blender integration check: three shared-tool fixes (8.6.9).

- Rig validator "select bone": on Blender 5 selection lives on the pose bone;
  the old path cancelled and selected nothing.
- Delta Mush "Bind": setting rest_source = 'BIND' alone never bound the
  modifier; Blender's own bind operator must run.
- Deform control: the module had no ``unregister``, so disabling the add-on
  raised an error.

Run:  blender --background --factory-startup --python tests/blender_shared_tool_fixes.py
"""
import contextlib
import io
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

# 1. select a bone from the validator list
arm = bpy.data.objects.new("A", bpy.data.armatures.new("A"))
bpy.context.scene.collection.objects.link(arm)
bpy.context.view_layer.objects.active = arm
arm.select_set(True)
bpy.ops.object.mode_set(mode='EDIT')
for name, z in (("B1", 0.0), ("B2", 1.0)):
    eb = arm.data.edit_bones.new(name)
    eb.head, eb.tail = (0, 0, z), (0, 0, z + 1.0)
bpy.ops.object.mode_set(mode='POSE')
result = bpy.ops.boneforge.select_validation_bone(bone_name="B2")
pb = arm.pose.bones["B2"]
selected = pb.select if hasattr(pb, "select") else arm.data.bones["B2"].select
assert result == {'FINISHED'} and selected, ("select bone", result, selected)
bpy.ops.object.mode_set(mode='OBJECT')

# 2. Delta Mush bind really binds
bpy.ops.mesh.primitive_cube_add()
cube = bpy.context.active_object
mod = cube.modifiers.new("DeltaMush", 'CORRECTIVE_SMOOTH')
result = bpy.ops.boneforge.bind_delta_mush()
assert result == {'FINISHED'} and mod.is_bind, ("delta mush bind", result, mod.is_bind)

# 3. the add-on unregisters without errors
out = io.StringIO()
with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
    boneforge.unregister()
errors = [line for line in out.getvalue().splitlines() if "failed to unregister" in line]
assert not errors, errors

print("SHARED TOOL FIXES PASS (bone select, delta mush bind, clean unregister)")
