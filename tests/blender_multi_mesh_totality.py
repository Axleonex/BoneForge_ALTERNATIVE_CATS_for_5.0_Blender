"""Blender integration check that atlasing preserves each source mesh object."""

import json
import os

import bpy


body = bpy.data.objects["Body"]
body_copy = body.copy()
body_copy.data = body.data.copy()
body_copy.name = "BodyCopy"
bpy.context.scene.collection.objects.link(body_copy)

preserved_source_slots = [2, 3, 5, 6, 9]
source_face_counts = [
    sum(1 for polygon in body.data.polygons if polygon.material_index == slot)
    for slot in preserved_source_slots
]

source_counts = {
    body.name: (len(body.data.vertices), len(body.data.edges), len(body.data.polygons)),
    body_copy.name: (
        len(body_copy.data.vertices),
        len(body_copy.data.edges),
        len(body_copy.data.polygons),
    ),
}
for obj in bpy.context.selected_objects:
    obj.select_set(False)
for obj in (body, body_copy):
    obj.hide_set(False)
    obj.select_set(True)
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

assert "FINISHED" in bpy.ops.boneforge.vrc_atlas_analyze()
assert "FINISHED" in bpy.ops.boneforge.vrc_atlas_bake()

session_name = settings.backup_collection_name
results = [
    obj
    for obj in bpy.context.scene.objects
    if obj.get("boneforge_atlas_backup") == session_name
]
assert len(results) == 2, [obj.name for obj in results]
assert not any(obj.name.startswith("KEPT_") for obj in results)

results_by_source = {
    json.loads(obj["boneforge_atlas_sources"])[0]: obj
    for obj in results
}
assert set(results_by_source) == {"Body", "BodyCopy"}
for source_name, expected_counts in source_counts.items():
    result = results_by_source[source_name]
    actual_counts = (
        len(result.data.vertices),
        len(result.data.edges),
        len(result.data.polygons),
    )
    assert actual_counts == expected_counts, (source_name, actual_counts, expected_counts)
    assert len(result.data.materials) == 6
    assert [
        sum(
            1
            for polygon in result.data.polygons
            if polygon.material_index == material_index
        )
        for material_index in range(1, 6)
    ] == source_face_counts
    assert json.loads(result["boneforge_atlas_preserved_slots"]) == [2, 3, 5, 6, 9]

assert results_by_source["Body"].data.materials[0] is results_by_source["BodyCopy"].data.materials[0]
assert body.hide_get() is True
assert body_copy.hide_get() is True
print(
    "BONEFORGE_MULTI_MESH_TOTALITY_PASS="
    + json.dumps(
        {
            source_name: {
                "result": result.name,
                "counts": source_counts[source_name],
                "materials": len(result.data.materials),
            }
            for source_name, result in sorted(results_by_source.items())
        },
        sort_keys=True,
    )
)