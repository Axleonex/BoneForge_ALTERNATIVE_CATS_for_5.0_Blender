"""Build the starter library using BoneForge's existing generators.

[PowerShell] blender --background --factory-startup --python scripts/build_starter_assets.py
"""
import json
from pathlib import Path
import sys

import bpy

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from boneforge.autorig import quick_human as qh, rig_assets as ra


def preview(armature, group):
    """Rasterize the real rest skeleton for a readable asset thumbnail."""
    size = 256
    axes = (0, 2) if group == 'humans' else (1, 2)
    lines = [(tuple(b.head_local[a] for a in axes),
              tuple(b.tail_local[a] for a in axes)) for b in armature.data.bones]
    points = [p for line in lines for p in line]
    low = [min(p[a] for p in points) for a in range(2)]
    high = [max(p[a] for p in points) for a in range(2)]
    scale = min(220 / max(high[a] - low[a], .01) for a in range(2))
    center = [(low[a] + high[a]) / 2 for a in range(2)]
    pixels = [.035, .045, .065, 1.] * (size * size)
    for head, tail in lines:
        start = [128 + (head[a] - center[a]) * scale for a in range(2)]
        end = [128 + (tail[a] - center[a]) * scale for a in range(2)]
        steps = max(1, int(max(abs(end[a] - start[a]) for a in range(2)) * 2))
        for n in range(steps + 1):
            x, y = [round(start[a] + (end[a] - start[a]) * n / steps) for a in range(2)]
            for dx, dy in ((0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)):
                if 0 <= x + dx < size and 0 <= y + dy < size:
                    offset = ((y + dy) * size + x + dx) * 4
                    pixels[offset:offset + 4] = [.95, .47, .08, 1.]
    image = armature.preview_ensure()
    image.image_size = (size, size)
    image.image_pixels_float = pixels


def main():
    if not qh.enable_rigify_if_available():
        raise RuntimeError("Rigify must be installed to rebuild all starter assets")
    starters = [dict(rig_name="fallback", op_id=qh.FALLBACK_OP_ID,
                     label="Basic Humanoid", group="humans", requires_rigify=False)]
    starters += [dict(r, requires_rigify=True) for r in qh.discover_rigify_metarigs()]
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    for starter in starters:
        if starter['requires_rigify']:
            module, operator = starter['op_id'].split('.', 1)
            getattr(getattr(bpy.ops, module), operator)()
            armature = bpy.context.active_object
        else:
            armature = qh._build_fallback_skeleton(bpy.context)
        if bpy.context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        armature.name = armature.data.name = starter['label']
        armature.asset_mark()
        armature.asset_data.catalog_id = ra.CATALOG_ID
        armature.asset_data.tags.new(ra.ASSET_TAG)
        armature.asset_data.description = (
            "Starter skeleton. Drag into the viewport. " +
            ("Enable Rigify to generate controls from this metarig."
             if starter['requires_rigify'] else "No Rigify required."))
        preview(armature, starter['group'])
    ra.assets_dir().mkdir(exist_ok=True)
    (ra.assets_dir() / 'blender_assets.cats.txt').write_text(
        f"# BoneForge starter rig catalog\nVERSION 1\n\n{ra.CATALOG_ID}:{ra.CATALOG_NAME}:{ra.CATALOG_NAME}\n",
        encoding='utf-8')
    (ra.assets_dir() / 'starter_rigs.json').write_text(
        json.dumps(starters, indent=2) + '\n', encoding='utf-8')
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(ra.assets_dir() / 'starter_rigs.blend'), compress=True)
    print("WROTE", len(starters), "BoneForge starter assets")


if __name__ == '__main__':
    main()
