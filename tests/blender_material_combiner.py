"""Real-host material combiner checks with generated meshes and pixel assertions.

Arguments after --: package-parent-or-ZIP output-directory.
Use isolated BLENDER_USER_CONFIG/SCRIPTS/EXTENSIONS and --python-exit-code 1.
"""
import json
import sys
from pathlib import Path

import addon_utils
import bpy

sys.dont_write_bytecode = True
package, output, *modes = sys.argv[sys.argv.index('--') + 1:]
output = Path(output)
output.mkdir(parents=True, exist_ok=True)
if package.lower().endswith('.zip'):
    assert bpy.ops.preferences.addon_install(filepath=package, overwrite=True) == {'FINISHED'}
    package = bpy.utils.user_resource('SCRIPTS', path='addons', create=True)
sys.path.insert(0, package)
assert addon_utils.enable('boneforge', default_set=True) is not None
import boneforge
assert Path(boneforge.__file__).resolve().is_relative_to(Path(package).resolve())
from boneforge.vrchat.cats import material_atlas as atlas

checks = []


def require(ok, detail):
    assert ok, detail


def reset():
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    settings = bpy.context.scene.boneforge_atlas_settings
    settings.has_backup = False
    settings.backup_collection_name = ''
    settings.atlas_groups.clear()
    settings.target_scope = 'SELECTED_MESHES'
    settings.auto_analyze_before_bake = False
    settings.preserve_originals = True
    settings.pack_method = 'SOURCE_PRESERVE'
    settings.keep_source_uv_maps = False
    settings.output_path = str(output)
    settings.bake_normal = settings.bake_emission = settings.bake_roughness = False
    settings.bake_metallic = settings.channel_pack_orm = False
    bpy.context.scene.cycles.samples = 1
    bpy.context.scene.cycles.device = 'CPU'
    bpy.context.scene.render.threads_mode = 'FIXED'
    bpy.context.scene.render.threads = 2
    return settings


def material(name, color, *, tinted=False, alpha=None):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    shader = next(n for n in nodes if n.type == 'BSDF_PRINCIPLED')
    image = bpy.data.images.new(name + '_image', width=4, height=4, alpha=True)
    image.pixels[:] = list((1, 1, 1, 0.8) if tinted else (*color, 1)) * 16
    image.pack()
    texture = nodes.new('ShaderNodeTexImage')
    texture.image = image
    if tinted:
        mix = nodes.new('ShaderNodeMixRGB')
        mix.blend_type = 'MULTIPLY'
        mix.inputs[0].default_value = 1
        mix.inputs[2].default_value = (*color, 1)
        links.new(texture.outputs['Color'], mix.inputs[1])
        links.new(mix.outputs[0], shader.inputs['Base Color'])
    else:
        links.new(texture.outputs['Color'], shader.inputs['Base Color'])
    if alpha is not None:
        multiply = nodes.new('ShaderNodeMath')
        multiply.operation = 'MULTIPLY'
        multiply.inputs[1].default_value = alpha
        links.new(texture.outputs['Alpha'], multiply.inputs[0])
        links.new(multiply.outputs[0], shader.inputs['Alpha'])
    return mat


def mesh(name, materials):
    vertices, faces = [], []
    for slot in range(len(materials)):
        offset = len(vertices)
        x = slot * 2
        vertices.extend([(x, 0, 0), (x + 1, 0, 0), (x + 1, 1, 0), (x, 1, 0)])
        faces.append(tuple(range(offset, offset + 4)))
    data = bpy.data.meshes.new(name)
    data.from_pydata(vertices, [], faces)
    obj = bpy.data.objects.new(name, data)
    bpy.context.scene.collection.objects.link(obj)
    for mat in materials:
        data.materials.append(mat)
    uv = data.uv_layers.new(name='UVMap')
    for polygon in data.polygons:
        polygon.material_index = polygon.index
        for loop, coord in zip(polygon.loop_indices, ((0, 0), (1, 0), (1, 1), (0, 1))):
            uv.data[loop].uv = coord
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    return obj


def analyze(settings, *, all_groups=False):
    require(bpy.ops.boneforge.vrc_atlas_analyze() == {'FINISHED'}, 'Analyze failed')
    for group in settings.atlas_groups:
        group.resolution = '1024'
        if all_groups:
            group.enabled = True
            for item in group.materials:
                item.enabled = True
            for item in group.textures:
                item.enabled = True


def results(settings):
    return [o for o in bpy.context.scene.objects
            if o.get('boneforge_atlas_backup') == settings.backup_collection_name]


def sample(obj, face):
    image = next(n.image for n in obj.data.materials[0].node_tree.nodes
                 if n.type == 'TEX_IMAGE' and n.image and n.image.name.startswith('bf_atlas'))
    uv = obj.data.uv_layers['atlas_uv']
    polygon = obj.data.polygons[face]
    u = sum(uv.data[i].uv.x for i in polygon.loop_indices) / len(polygon.loop_indices)
    v = sum(uv.data[i].uv.y for i in polygon.loop_indices) / len(polygon.loop_indices)
    x, y = min(int(u * image.size[0]), image.size[0] - 1), min(int(v * image.size[1]), image.size[1] - 1)
    index = 4 * (y * image.size[0] + x)
    return tuple(image.pixels[index:index + 4])


def graph_bake():
    settings = reset()
    red = material('Tinted red', (1, 0, 0), tinted=True, alpha=0.5)
    green = material('Green', (0, 1, 0), alpha=0.8)
    original = mesh('GraphSource', [red, green])
    original_graph = len(red.node_tree.nodes), len(red.node_tree.links)
    analyze(settings, all_groups=True)
    require(bpy.ops.boneforge.vrc_atlas_bake() == {'FINISHED'}, 'Graph bake failed')
    generated = results(settings)
    require(len(generated) == 1, 'Expected one combined graph mesh')
    pixels = [sample(generated[0], i) for i in range(2)]
    require(tuple(len(x) for x in (red.node_tree.nodes, red.node_tree.links)) == original_graph,
            'Source shader graph changed')
    require(Path(next(n.image.filepath_raw for n in generated[0].data.materials[0].node_tree.nodes
                      if n.type == 'TEX_IMAGE' and n.image)).is_file(), 'Atlas was not saved')
    require(bpy.ops.boneforge.vrc_atlas_revert() == {'FINISHED'}, 'Graph Revert failed')
    # Blender's packed RGBA source samples 0.8 RGB here; the multiply tint
    # must preserve red and remove the green/blue components of that source.
    rgb_ok = abs(pixels[0][0] - 0.8) < 0.08 and pixels[0][1] < 0.08 and pixels[0][2] < 0.08
    alpha_ok = abs(pixels[0][3] - 0.4) < 0.08 and abs(pixels[1][3] - 0.8) < 0.08
    require(rgb_ok and alpha_ok, f'Shader graph lost: RGB correct={rgb_ok}, alpha correct={alpha_ok}; pixels={pixels}')
    return {'pixels': pixels}


def roundtrip():
    settings = reset()
    red, green = material('Red', (1, 0, 0)), material('Green', (0, 1, 0))
    glass = bpy.data.materials.new('Preserved glass')
    glass.use_nodes = True
    next(n for n in glass.node_tree.nodes if n.type == 'BSDF_PRINCIPLED').inputs['Alpha'].default_value = 0.4
    a = mesh('Body', [red, green, glass])
    b = mesh('Clothing', [red, green, glass])
    a.shape_key_add(name='Basis')
    a.shape_key_add(name='Smile').data[0].co.z = 0.2
    parent = bpy.data.objects.new('Parent', None)
    bpy.context.scene.collection.objects.link(parent)
    a.parent = b.parent = parent
    a.hide_render = True
    original_uv = [tuple(point.uv) for point in a.data.uv_layers['UVMap'].data]
    analyze(settings)
    require(any(g.render_type == 'Alpha Blend' and not g.enabled for g in settings.atlas_groups),
            'Transparent group was not preserved by default')
    require(atlas._projected_mat_count(settings) == 4, 'Multi-mesh estimate under-counted material slots')
    require(bpy.ops.boneforge.vrc_atlas_bake() == {'FINISHED'}, 'Mixed bake failed')
    generated = results(settings)
    require(len(generated) == 2, 'Multi-mesh result count differs')
    uv0_correct = all(obj.data.uv_layers[0].name == 'atlas_uv' for obj in generated)
    actual_slots = sum(len({p.material_index for p in obj.data.polygons}) for obj in generated)
    counts_correct = settings.total_mats_before == actual_slots
    for obj in generated:
        require(len(obj.data.vertices) == 12 and len(obj.data.polygons) == 3, 'Geometry changed')
        require(len(obj.data.materials) == 2 and obj.parent == parent, 'Preserved slot or hierarchy lost')
        require(obj.data.materials[1] == glass, 'Transparent material was replaced')
        require(sample(obj, 0)[0] > 0.9 and sample(obj, 1)[1] > 0.9, 'Color pixels differ')
    body = next(o for o in generated if json.loads(o['boneforge_atlas_sources']) == ['Body'])
    require([key.name for key in body.data.shape_keys.key_blocks] == ['Basis', 'Smile'], 'Shape keys lost')
    require(bpy.ops.boneforge.vrc_atlas_revert() == {'FINISHED'}, 'Mixed Revert failed')
    require(settings.total_mats_before == 6, 'Revert left the reduced material count')
    require([tuple(point.uv) for point in a.data.uv_layers['UVMap'].data] == original_uv, 'Original UV changed')
    visibility_restored = a.hide_render is True and b.hide_render is False
    # Also exercise Accept on a second preview.
    for obj in bpy.context.selected_objects:
        obj.select_set(False)
    a.select_set(True)
    b.select_set(True)
    bpy.context.view_layer.objects.active = a
    analyze(settings)
    require(bpy.ops.boneforge.vrc_atlas_bake() == {'FINISHED'}, 'Second bake failed')
    names = [o.name for o in results(settings)]
    require(bpy.ops.boneforge.vrc_atlas_accept() == {'FINISHED'}, 'Accept failed')
    require(all(bpy.data.objects.get(name) for name in names), 'Accept removed the result')
    require(bpy.data.objects.get('Body') is None and bpy.data.objects.get('Clothing') is None,
            'Accept did not retire originals')
    require(not settings.has_backup, 'Accept left stale backup state')
    require(visibility_restored and uv0_correct and counts_correct,
            f'Roundtrip incorrect: render visibility restored={visibility_restored}, export UV0 correct={uv0_correct}, material count correct={counts_correct} (expected {actual_slots})')
    return {'combined_meshes': len(names), 'accept': True, 'revert': True}


def stale_analysis():
    settings = reset()
    obj = mesh('DeletedAfterAnalyze', [material('A', (1, 0, 0)), material('B', (0, 1, 0))])
    analyze(settings)
    bpy.data.objects.remove(obj, do_unlink=True)
    try:
        outcome = bpy.ops.boneforge.vrc_atlas_bake()
    except RuntimeError:
        outcome = {'CANCELLED'}
    require(outcome == {'CANCELLED'}, 'Stale source analysis reported a successful empty bake')
    require(not settings.has_backup, 'Invalid bake created an unusable backup')
    return {'stale_bake': 'CANCELLED'}


def classification():
    reset()
    solid = material('Ordinary solid', (1, 0, 0))
    transparent = material('Linked transparency', (1, 1, 1), alpha=0.5)
    constant = bpy.data.materials.new('Constant transparency')
    constant.use_nodes = True
    next(n for n in constant.node_tree.nodes if n.type == 'BSDF_PRINCIPLED').inputs['Alpha'].default_value = 0.4
    actual = [atlas._classify_material(mat) for mat in (solid, transparent, constant)]
    detail = {'classes': actual, 'solid_legacy_method': str(getattr(solid, 'blend_method', 'absent')),
              'solid_surface_method': str(getattr(solid, 'surface_render_method', 'absent'))}
    require(actual == ['Opaque', 'Alpha Blend', 'Alpha Blend'], detail)
    return detail


def no_uv_color_only():
    settings = reset()
    materials = []
    for name, color in [('Constant red', (1, 0, 0, 1)), ('Constant green', (0, 1, 0, 1))]:
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        next(n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED').inputs['Base Color'].default_value = color
        materials.append(mat)
    original = mesh('NoUVSource', materials)
    for uv in list(original.data.uv_layers):
        original.data.uv_layers.remove(uv)
    analyze(settings)
    require(bpy.ops.boneforge.vrc_atlas_bake() == {'FINISHED'}, 'No-UV color bake failed')
    generated = results(settings)
    require(len(generated) == 1 and generated[0].data.uv_layers[0].name == 'atlas_uv',
            'No-UV source did not receive export UV0')
    require(sample(generated[0], 0)[0] > 0.9 and sample(generated[0], 1)[1] > 0.9,
            'Color-only atlas lost the constant source colors')
    require(bpy.ops.boneforge.vrc_atlas_revert() == {'FINISHED'}, 'No-UV Revert failed')
    require(settings.total_mats_before == 2, 'No-UV Revert left the reduced material count')
    require(len(original.data.uv_layers) == 0, 'Revert added UVs to the original mesh')
    return {'color_bake': True, 'generated_uv0': True, 'original_untouched': True}


cases = [('material_classification', classification), ('shader_graph_pixels', graph_bake),
         ('mixed_mesh_accept_revert', roundtrip), ('deleted_source_preflight', stale_analysis),
         ('no_uv_color_only', no_uv_color_only)]
if modes == ['no_uv_only']:
    cases = [cases[-1]]
for name, check in cases:
    print('COMBINER_CHECK ' + name, flush=True)
    try:
        detail = check()
        checks.append({'name': name, 'result': 'PASS', 'detail': detail})
    except Exception as exc:
        import traceback
        traceback.print_exc()
        checks.append({'name': name, 'result': 'FAIL', 'detail': str(exc)})

report = {'product': boneforge.bl_info['name'], 'version': boneforge.bl_info['version'],
          'host': bpy.app.version_string, 'checks': checks,
          'result': 'PASS' if all(c['result'] == 'PASS' for c in checks) else 'FAIL'}
(output / 'result.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print('COMBINER_RESULT ' + json.dumps(report), flush=True)
assert report['result'] == 'PASS', report
