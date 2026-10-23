"""Host checks for atlas bulk selection and progressive disclosure.

After --: package parent or release ZIP, output JSON.
"""
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import addon_utils
import bpy

sys.dont_write_bytecode = True
package, report = sys.argv[sys.argv.index('--') + 1:]
if package.lower().endswith('.zip'):
    assert bpy.ops.preferences.addon_install(filepath=package, overwrite=True) == {'FINISHED'}
    package = bpy.utils.user_resource('SCRIPTS', path='addons', create=True)
sys.path.insert(0, package)
assert addon_utils.enable('boneforge', default_set=True)
from boneforge.vrchat.cats import material_atlas as atlas

settings = bpy.context.scene.boneforge_atlas_settings
settings.atlas_groups.clear()
op = bpy.ops.boneforge.vrc_atlas_select_sources
assert not op.poll(), 'Empty analysis must explain why selection is unavailable'
groups = [settings.atlas_groups.add() for _ in range(2)]
for i, group in enumerate(groups):
    group.name = f'Group {i}'
    for j in range(3):
        mat = group.materials.add()
        mat.material_name = f'Material {j}'
        mat.enabled = False
        tex = group.textures.add()
        tex.image_name = f'Image {j}'
        tex.enabled = False
        tex.missing = j == 2
settings.active_group_index = 0
groups[0].enabled = False  # Preserved transparent groups must stay disabled.
assert op.poll()
for _ in range(2):
    assert op(target='MATERIALS', select=True) == {'FINISHED'}
    assert all(m.enabled for m in groups[0].materials)
assert not any(m.enabled for m in groups[1].materials)
assert not any(t.enabled for t in groups[0].textures)
assert not groups[0].enabled
assert op(target='TEXTURES', select=True) == {'FINISHED'}
assert [t.enabled for t in groups[0].textures] == [True, True, False]
assert not any(t.enabled for t in groups[1].textures)
assert op(target='MATERIALS', select=False) == {'FINISHED'}
assert not any(m.enabled for m in groups[0].materials)
assert groups[0].textures[0].enabled
assert op(target='TEXTURES', select=False) == {'FINISHED'}
assert not any(t.enabled for t in groups[0].textures)
settings.active_group_index = 99
assert not op.poll()
settings.active_group_index = 0
settings.has_backup = True
assert not op.poll(), 'Preview must be accepted or reverted first'
settings.has_backup = False

icons = {x.identifier for x in bpy.types.UILayout.bl_rna.functions['operator'].parameters['icon'].enum_items}


class Layout:
    def __init__(self, records=None):
        self.records = [] if records is None else records
    def child(self, *args, **kwargs):
        return Layout(self.records)
    row = column = box = split = grid_flow = child
    def label(self, *, text='', icon='NONE', **kwargs):
        assert icon in icons, icon
        self.records.append(('label', text))
    def operator(self, idname, *, text='', icon='NONE', **kwargs):
        assert icon in icons, icon
        category, name = idname.split('.')
        getattr(getattr(bpy.ops, category), name).get_rna_type()
        props = SimpleNamespace()
        self.records.append(('operator', idname, text, props))
        return props
    def prop(self, data, name, **kwargs):
        assert hasattr(data, name), name
        self.records.append(('prop', name))
    def template_list(self, idname, *args, **kwargs):
        self.records.append(('list', idname))
    def separator(self):
        pass


def draw():
    layout = Layout()
    atlas.BONEFORGE_PT_vrc_w2_atlas.draw(SimpleNamespace(layout=layout), bpy.context)
    return layout.records


settings.show_advanced = False
settings.show_source_details = False
records = draw()
bulk = [r for r in records if r[0:2] == ('operator', 'boneforge.vrc_atlas_select_sources')]
assert {(r[3].target, r[3].select) for r in bulk} == {
    ('MATERIALS', True), ('MATERIALS', False), ('TEXTURES', True), ('TEXTURES', False)}
assert len(bulk) == 4
assert not any(r[0:2] == ('prop', 'size_override') for r in records)
assert not any(r[0:2] == ('prop', 'role') for r in records)
assert not any(r[0:2] == ('operator', 'boneforge.vrc_atlas_smart_combine') for r in records)
assert not any(r[0:2] == ('operator', 'boneforge.vrc_atlas_copy_debug') for r in records)
settings.show_source_details = True
records = draw()
assert ('prop', 'size_override') in records and ('prop', 'role') in records
settings.show_advanced = True
assert any(r[0:2] == ('operator', 'boneforge.vrc_atlas_copy_debug') for r in draw())
layout = Layout()
atlas.BONEFORGE_MT_atlas_selection.draw(SimpleNamespace(layout=layout), bpy.context)
assert len([r for r in layout.records if r[0] == 'operator']) == 4
assert atlas._atlas_selection_menu in bpy.types.VIEW3D_MT_object.draw._draw_funcs
settings.atlas_groups.clear()
assert any(r[0:2] == ('operator', 'boneforge.vrc_atlas_smart_combine') for r in draw())
assert 'UNDO' in atlas.BF_OT_VRC_AtlasSelectSources.bl_options
rna = op.get_rna_type()
assert all(rna.properties[p].is_hidden and rna.properties[p].is_skip_save for p in ('target', 'select'))

result = {'result': 'PASS', 'host': bpy.app.version_string,
          'version': list(__import__('boneforge').bl_info['version']),
          'checks': ['materials all/none', 'textures all/none', 'missing textures excluded',
                     'group isolation', 'preserved group remains disabled', 'independent lists',
                     'repeat action', 'empty/stale/backup polls', 'registered menu',
                     'collapsed/expanded draw', 'reviewed bake path', 'operator RNA']}
Path(report).parent.mkdir(parents=True, exist_ok=True)
Path(report).write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result), flush=True)
