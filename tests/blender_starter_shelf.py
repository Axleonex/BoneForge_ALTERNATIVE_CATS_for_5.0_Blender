"""Exercise starter shelf registration, catalog assets and library ownership."""
from pathlib import Path
import json
import sys
from types import SimpleNamespace

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from boneforge.autorig import rig_assets as ra


def libraries():
    return [(lib.name, lib.path) for lib in bpy.context.preferences.filepaths.asset_libraries]


def main():
    original = libraries()
    header = tuple(getattr(bpy.types.VIEW3D_HT_header.draw, '_draw_funcs', ()))
    for _ in range(2):
        ra.register()
        try:
            assert any(ra._same_path(lib.path) for lib in bpy.context.preferences.filepaths.asset_libraries)
            shelf = getattr(bpy.types, 'VIEW3D_AST_object', None) or getattr(bpy.types, ra.SHELF_IDNAME)
            assert shelf.poll(bpy.context)
            for kind in ('OBJECT', 'COLLECTION', 'MATERIAL', 'WORLD'):
                assert shelf.asset_poll(SimpleNamespace(id_type=kind))
            assert not shelf.asset_poll(SimpleNamespace(id_type='ACTION'))
            assert tuple(getattr(bpy.types.VIEW3D_HT_header.draw, '_draw_funcs', ())) == header
        finally:
            ra.unregister()
        assert libraries() == original
        assert not hasattr(bpy.types, ra.SHELF_IDNAME)

    libs = bpy.context.preferences.filepaths.asset_libraries
    preexisting = libs.new(name='My existing starter library', directory=str(ra.assets_dir()))
    ra.register()
    ra.unregister()
    assert libs.get(preexisting.name).as_pointer() == preexisting.as_pointer()
    libs.remove(preexisting)
    collision = libs.new(name=ra.LIBRARY_NAME, directory=str(Path(__file__).parent))
    ra.register()
    assert ra._owned_name() == ra.LIBRARY_NAME + ' (BoneForge)'
    ra.unregister()
    assert libs.get(collision.name).as_pointer() == collision.as_pointer()
    libs.remove(collision)
    assert libraries() == original

    manifest = json.loads((ra.assets_dir() / 'starter_rigs.json').read_text(encoding='utf-8'))
    with bpy.data.libraries.load(str(ra.assets_dir() / 'starter_rigs.blend'), assets_only=True) as (source, target):
        target.objects = source.objects
    assets = target.objects
    assert len(assets) == len(manifest) == 9
    assert {obj.name for obj in assets} == {item['label'] for item in manifest}
    for obj in assets:
        assert obj.type == 'ARMATURE' and len(obj.data.bones) > 0
        assert obj.asset_data.catalog_id == ra.CATALOG_ID
        assert ra.ASSET_TAG in obj.asset_data.tags
        assert tuple(obj.preview.image_size) == (256, 256)
    basic = next(obj for obj in assets if obj.name == 'Basic Humanoid')
    assert len(basic.data.bones) == 19
    catalog = (ra.assets_dir() / 'blender_assets.cats.txt').read_text(encoding='utf-8')
    entries = [line for line in catalog.splitlines() if line and not line.startswith(('#', 'VERSION'))]
    assert entries == [f'{ra.CATALOG_ID}:Starter Rigs:Starter Rigs']
    for obj in assets:
        bpy.data.objects.remove(obj, do_unlink=True)
    print('PASS BoneForge starter shelf: registration/reload, other assets, no header controls, library ownership, nine real assets and single catalog')


if __name__ == '__main__':
    main()
