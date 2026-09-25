"""Blender integration check for baking a mixed render-type mesh."""

import json
import os

import bpy



def uv_signature(mesh, uv_name, material_index):
    uv_data = mesh.uv_layers[uv_name].data
    return sorted(
        (round(uv_data[loop_index].uv.x, 6), round(uv_data[loop_index].uv.y, 6))
        for polygon in mesh.polygons
        if polygon.material_index == material_index
        for loop_index in polygon.loop_indices
    )


body = bpy.data.objects["Body"]
source_vertex_count = len(body.data.vertices)
source_edge_count = len(body.data.edges)
source_polygon_count = len(body.data.polygons)
source_parent_name = body.parent.name if body.parent else None
source_shape_keys = (
    [key.name for key in body.data.shape_keys.key_blocks]
    if body.data.shape_keys else []
)
preserved_source_slots = [2, 3, 5, 6, 9]
source_uv_signatures = [
    uv_signature(body.data, body.data.uv_layers.active.name, slot)
    for slot in preserved_source_slots
]
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
assert len(session_objects) == 1, [obj.name for obj in session_objects]

combined = session_objects[0]
assert combined.name.startswith("ATLAS_Body"), combined.name
assert len(combined.data.vertices) == source_vertex_count
assert len(combined.data.edges) == source_edge_count
assert len(combined.data.polygons) == source_polygon_count
assert len(combined.data.materials) == 6
assert (combined.parent.name if combined.parent else None) == source_parent_name
assert (
    [key.name for key in combined.data.shape_keys.key_blocks]
    if combined.data.shape_keys else []
) == source_shape_keys
assert [
    uv_signature(combined.data, "atlas_uv", material_index)
    for material_index in range(1, 6)
] == source_uv_signatures
assert combined["boneforge_atlas_output_material_type"] == "Opaque"
assert json.loads(combined["boneforge_atlas_preserved_slots"]) == [2, 3, 5, 6, 9]
assert body.hide_get() is True
assert bpy.data.objects.get("PRE_ATLAS_Body") is not None
assert not any(obj.name.startswith("ATLAS_Alpha_Blend") for obj in session_objects)
assert not any(obj.name.startswith("KEPT_") for obj in session_objects)

report = {
    "combined": combined.name,
    "combined_materials": len(combined.data.materials),
    "combined_vertices": len(combined.data.vertices),
    "combined_edges": len(combined.data.edges),
    "combined_polygons": len(combined.data.polygons),
    "atlas_output_type": combined["boneforge_atlas_output_material_type"],
    "preserved_slots": json.loads(combined["boneforge_atlas_preserved_slots"]),
    "source_hidden": body.hide_get(),
    "backup": session_name,
}
print("BONEFORGE_MIXED_BAKE_PASS=" + json.dumps(report, sort_keys=True))

validation_blend = os.path.join(
    os.environ["BONEFORGE_INTEGRATION_OUTPUT"],
    "BoneForge-8.6.6-mixed-material-validation.blend",
)
bpy.ops.wm.save_as_mainfile(filepath=validation_blend)
print("BONEFORGE_VALIDATION_BLEND=" + validation_blend)
