"""Blender integration check for baking a mixed render-type mesh."""

import json
import os

import bpy


body = bpy.data.objects["Body"]
for obj in bpy.context.selected_objects:
    obj.select_set(False)
body.hide_set(False)
body.select_set(True)
bpy.context.view_layer.objects.active = body

settings = bpy.context.scene.boneforge_atlas_settings
settings.target_scope = "SELECTED_MESHES"
settings.auto_analyze_before_bake = False
settings.preserve_originals = True
settings.pack_method = "SOURCE_PRESERVE"
settings.output_material_type = "AUTO"
settings.output_surface_shader = "AUTO"
settings.output_format = "PNG"
settings.output_path = os.environ["BONEFORGE_INTEGRATION_OUTPUT"]

analyze_result = bpy.ops.boneforge.vrc_atlas_analyze()
assert "FINISHED" in analyze_result, analyze_result

bake_result = bpy.ops.boneforge.vrc_atlas_bake()
assert "FINISHED" in bake_result, bake_result

session_name = settings.backup_collection_name
session_objects = [
    obj
    for obj in bpy.context.scene.objects
    if obj.get("boneforge_atlas_backup") == session_name
]
atlas_objects = [obj for obj in session_objects if obj.name.startswith("ATLAS_")]
kept_objects = [obj for obj in session_objects if obj.name.startswith("KEPT_")]

assert len(atlas_objects) == 1, [obj.name for obj in session_objects]
assert len(kept_objects) == 1, [obj.name for obj in session_objects]

atlas = atlas_objects[0]
kept = kept_objects[0]
assert atlas.name.startswith("ATLAS_Opaque_2048px"), atlas.name
assert len(atlas.data.materials) == 1
assert atlas["boneforge_atlas_output_material_type"] == "Opaque"
assert len(kept.data.materials) == 5
assert json.loads(kept["boneforge_atlas_preserved_slots"]) == [2, 3, 5, 6, 9]
assert len(kept.data.polygons) > 0
assert body.hide_get() is True
assert bpy.data.objects.get("PRE_ATLAS_Body") is not None
assert not any(obj.name.startswith("ATLAS_Alpha_Blend") for obj in session_objects)

report = {
    "atlas": atlas.name,
    "atlas_materials": len(atlas.data.materials),
    "atlas_polygons": len(atlas.data.polygons),
    "atlas_output_type": atlas["boneforge_atlas_output_material_type"],
    "kept": kept.name,
    "kept_materials": len(kept.data.materials),
    "kept_polygons": len(kept.data.polygons),
    "kept_slots": json.loads(kept["boneforge_atlas_preserved_slots"]),
    "source_hidden": body.hide_get(),
    "backup": session_name,
}
print("BONEFORGE_MIXED_BAKE_PASS=" + json.dumps(report, sort_keys=True))

validation_blend = os.path.join(
    os.environ["BONEFORGE_INTEGRATION_OUTPUT"],
    "BoneForge-8.6.5-mixed-material-validation.blend",
)
bpy.ops.wm.save_as_mainfile(filepath=validation_blend)
print("BONEFORGE_VALIDATION_BLEND=" + validation_blend)
