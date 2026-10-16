"""Starter rigs in the viewport's native asset shelf and catalog tabs."""
from pathlib import Path

import bpy

LIBRARY_NAME = "BoneForge Rigs"
CATALOG_ID = "869ee94b-534c-44d1-9285-3a746947cbde"
CATALOG_NAME = "Starter Rigs"
ASSET_TAG = "boneforge_starter_rig"
SHELF_IDNAME = "BF_AST_boneforge_starters"
_OWNED_KEY = "boneforge_starter_library_owned"


def assets_dir():
    return Path(__file__).resolve().parents[1] / "assets"


def _preferences():
    addon = bpy.context.preferences.addons.get(__package__.split('.')[0])
    return addon.preferences if addon else None


def _owned_name():
    prefs = _preferences()
    return (prefs.starter_library_owned if prefs else
            bpy.app.driver_namespace.get(_OWNED_KEY, ""))


def _set_owned(name):
    prefs = _preferences()
    if prefs:
        prefs.starter_library_owned = name
    if name:
        bpy.app.driver_namespace[_OWNED_KEY] = name
    else:
        bpy.app.driver_namespace.pop(_OWNED_KEY, None)


def _same_path(path):
    return Path(path).resolve() == assets_dir()


def register_library():
    if not (assets_dir() / "starter_rigs.blend").is_file():
        raise FileNotFoundError("The bundled BoneForge starter rig library is missing")
    libraries = bpy.context.preferences.filepaths.asset_libraries
    if any(_same_path(lib.path) for lib in libraries):
        return
    name = LIBRARY_NAME
    if libraries.get(name):
        name = LIBRARY_NAME + " (BoneForge)"
    if libraries.get(name):
        raise RuntimeError("Both BoneForge asset library names are already in use")
    libraries.new(name=name, directory=str(assets_dir()))
    _set_owned(name)


def unregister_library():
    libraries = bpy.context.preferences.filepaths.asset_libraries
    owned = _owned_name()
    library = libraries.get(owned) if owned else None
    if library and _same_path(library.path):
        libraries.remove(library)
    _set_owned("")


class BF_AST_boneforge_starters(bpy.types.AssetShelf):
    """Supply Object Mode's asset shelf on standard Blender."""
    bl_idname = SHELF_IDNAME
    bl_space_type = 'VIEW_3D'
    bl_options = {'DEFAULT_VISIBLE', 'STORE_ENABLED_CATALOGS_IN_PREFERENCES'}
    bl_default_preview_size = 96

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    @classmethod
    def asset_poll(cls, asset):
        # Let the host import objects and retain the user's other catalogs.
        return asset.id_type in {'OBJECT', 'COLLECTION', 'MATERIAL', 'WORLD'}


def register():
    register_library()
    # Reuse a host's Object shelf when present; standard Blender needs one.
    if not hasattr(bpy.types, 'VIEW3D_AST_object'):
        bpy.utils.register_class(BF_AST_boneforge_starters)


def unregister():
    live = getattr(bpy.types, SHELF_IDNAME, None)
    if live is not None:
        bpy.utils.unregister_class(live)
    unregister_library()
