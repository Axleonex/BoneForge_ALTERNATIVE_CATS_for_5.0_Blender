"""Capture an isolated native window with an existing catalog and starter rigs.

Run the intended host with --factory-startup --python this_file -- ADDON_ROOT OUT.
No user preferences or startup file are saved.
"""
from pathlib import Path
import json
import sys

import bpy

args = sys.argv[sys.argv.index('--') + 1:]
root, out = (Path(arg).resolve() for arg in args[:2])
out.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(root))
from boneforge.autorig import quick_human as qh, rig_assets as ra

bpy.context.preferences.view.show_splash = False
bpy.context.preferences.use_preferences_save = False
# A separate ordinary asset library proves that the catalogs can coexist.
fixture = out / 'fixture-library'
fixture.mkdir(exist_ok=True)
cube = bpy.data.objects.get('Cube')
if cube is None:
    bpy.ops.mesh.primitive_cube_add()
    cube = bpy.context.active_object
cube.asset_mark()
cube.asset_data.catalog_id = 'b770d107-8f02-4a02-a1d0-dbbce9e3e731'
bpy.data.libraries.write(str(fixture / 'existing.blend'), {cube}, fake_user=True, compress=True)
cube.asset_clear()
(fixture / 'blender_assets.cats.txt').write_text(
    'VERSION 1\n\nb770d107-8f02-4a02-a1d0-dbbce9e3e731:Primitives:Primitives\n', encoding='utf-8')
bpy.context.preferences.filepaths.asset_libraries.new(name='Existing Assets', directory=str(fixture))
qh.register()
ra.register()
area = next(a for a in bpy.context.screen.areas if a.type == 'VIEW_3D')


def configure():
    area.spaces.active.show_region_asset_shelf = True
    states = []
    for region in area.regions:
        if region.type in {'ASSET_SHELF', 'ASSET_SHELF_HEADER'}:
            with bpy.context.temp_override(area=area, region=region):
                shelf = bpy.context.asset_shelf
                if shelf:
                    shelf.asset_library_reference = 'ALL'
                    shelf.show_names = True
                    shelf.preview_size = 80
                states.append({'region': region.type, 'shelf': shelf.bl_idname if shelf else None,
                               'size': [region.width, region.height]})
    (out / 'window-state.json').write_text(json.dumps(states, indent=2), encoding='utf-8')
    area.tag_redraw()
    bpy.app.timers.register(capture, first_interval=8)


def capture():
    bpy.ops.screen.screenshot(filepath=str(out / 'catalog-tab.png'))
    if '--selector' in args:
        region = next(r for r in area.regions if r.type == 'ASSET_SHELF_HEADER')
        bpy.context.window.event_simulate(type='MOUSEMOVE', value='NOTHING',
                                         x=region.x + 30, y=region.y + region.height // 2)
        bpy.app.timers.register(open_selector, first_interval=1)
    else:
        bpy.app.timers.register(lambda: bpy.ops.wm.quit_blender() and None, first_interval=1)


def open_selector():
    region = next(r for r in area.regions if r.type == 'ASSET_SHELF_HEADER')
    with bpy.context.temp_override(area=area, region=region):
        bpy.ops.wm.call_panel('INVOKE_DEFAULT', name='ASSETSHELF_PT_catalog_selector', keep_open=True)
    bpy.app.timers.register(capture_selector, first_interval=2)


def capture_selector():
    bpy.ops.screen.screenshot(filepath=str(out / 'catalog-selector.png'))
    if '--check' in args:
        at = args.index('--check')
        x, y = map(int, args[at + 1:at + 3])
        def checked_first():
            if '--second-check' in args:
                second = args.index('--second-check')
                second_x, second_y = map(int, args[second + 1:second + 3])
                click(second_x, second_y, close_selector)
            else:
                close_selector()
        click(x, y, checked_first)
    else:
        bpy.app.timers.register(lambda: bpy.ops.wm.quit_blender() and None, first_interval=1)


def close_selector():
    bpy.ops.screen.screenshot(filepath=str(out / 'catalog-selector-after-click.png'))
    (out / 'event-state.json').write_text(json.dumps({
        'window': [bpy.context.window.width, bpy.context.window.height],
        'preferences_dirty': bpy.context.preferences.is_dirty,
        'regions': [(r.type, r.x, r.y, r.width, r.height) for r in area.regions],
    }, indent=2), encoding='utf-8')
    for event_type, value in [('MOUSEMOVE', 'NOTHING'), ('LEFTMOUSE', 'PRESS'), ('LEFTMOUSE', 'RELEASE')]:
        bpy.context.window.event_simulate(type=event_type, value=value, x=500, y=500)
    bpy.app.timers.register(capture_enabled_tab, first_interval=2)


def capture_enabled_tab():
    bpy.ops.screen.screenshot(filepath=str(out / 'catalog-tab-enabled.png'))
    if '--activate' in args:
        at = args.index('--activate')
        x, y = map(int, args[at + 1:at + 3])
        click(x, y, capture_selected_tab)
    else:
        bpy.app.timers.register(lambda: bpy.ops.wm.quit_blender() and None, first_interval=1)


def click(x, y, done):
    # Separate event ticks so native checkbox/tab release handling completes.
    bpy.context.window.event_simulate(type='MOUSEMOVE', value='NOTHING', x=x, y=y)
    def press():
        bpy.context.window.event_simulate(type='LEFTMOUSE', value='PRESS', x=x, y=y)
        bpy.app.timers.register(release, first_interval=.25)
    def release():
        bpy.context.window.event_simulate(type='LEFTMOUSE', value='RELEASE', x=x, y=y)
        bpy.app.timers.register(done, first_interval=1)
    bpy.app.timers.register(press, first_interval=.5)


def capture_selected_tab():
    bpy.ops.screen.screenshot(filepath=str(out / 'starter-rigs-selected.png'))
    bpy.app.timers.register(lambda: bpy.ops.wm.quit_blender() and None, first_interval=1)


bpy.app.timers.register(configure, first_interval=3)
