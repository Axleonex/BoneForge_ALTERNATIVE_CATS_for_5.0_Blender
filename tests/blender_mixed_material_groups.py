"""Blender integration check for mixed render-type material analysis."""

import json

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

result = bpy.ops.boneforge.vrc_atlas_analyze()
assert "FINISHED" in result, result

actual = []
for group in settings.atlas_groups:
    actual.append(
        {
            "render_type": group.render_type,
            "enabled": bool(group.enabled),
            "slots": [
                {
                    "slot_index": int(item.slot_index),
                    "enabled": bool(item.enabled),
                    "render_type": item.render_type,
                }
                for item in group.materials
            ],
        }
    )

expected = [
    {
        "render_type": "Opaque",
        "enabled": True,
        "slots": [
            {"slot_index": 0, "enabled": True, "render_type": "Opaque"},
            {"slot_index": 1, "enabled": True, "render_type": "Opaque"},
            {"slot_index": 3, "enabled": True, "render_type": "Opaque"},
            {"slot_index": 5, "enabled": True, "render_type": "Opaque"},
            {"slot_index": 6, "enabled": True, "render_type": "Opaque"},
            {"slot_index": 9, "enabled": True, "render_type": "Opaque"},
        ],
    },
    {
        "render_type": "Alpha Blend",
        "enabled": False,
        "slots": [
            {"slot_index": 2, "enabled": False, "render_type": "Alpha Blend"},
        ],
    },
]

print("BONEFORGE_MIXED_GROUPS_ACTUAL=" + json.dumps(actual, sort_keys=True))
assert actual == expected, json.dumps(actual, indent=2)
print("BONEFORGE_MIXED_GROUPS_PASS")
