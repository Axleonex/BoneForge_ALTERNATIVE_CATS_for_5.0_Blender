"""Pure-Python regressions for dependency installation and MMD discovery.

[PowerShell] python tests/test_mmd_install.py [path-to-boneforge]
"""
import importlib.util
import sys
import tempfile
import types
import unittest
import zipfile
from pathlib import Path
from unittest.mock import Mock, patch

PACKAGE = Path(sys.argv.pop(1)).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / 'boneforge'
sys.dont_write_bytecode = True


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, PACKAGE / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class MMDTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.addons = []
        self.modules = []
        self.ops = types.SimpleNamespace(
            preferences=types.SimpleNamespace(addon_install=Mock(return_value={'FINISHED'}), addon_enable=Mock(return_value={'CANCELLED'})),
            extensions=types.SimpleNamespace(package_install_files=Mock(return_value={'FINISHED'})),
            mmd_tools=types.SimpleNamespace(),
        )
        self.bpy = types.ModuleType('bpy')
        self.bpy.ops = self.ops
        self.bpy.context = types.SimpleNamespace(preferences=types.SimpleNamespace(
            addons=self.addons,
            extensions=types.SimpleNamespace(repos=[types.SimpleNamespace(
                module='user_default', enabled=True, use_remote_url=False, source='USER')]),
        ))
        self.bpy.types = types.SimpleNamespace(Operator=type('Operator', (), {}))
        props = types.ModuleType('bpy.props')
        props.StringProperty = props.EnumProperty = lambda **kw: None
        self.bpy.props = props
        btypes = types.ModuleType('bpy.types')
        btypes.Operator = self.bpy.types.Operator
        au = types.ModuleType('addon_utils')
        au.modules = Mock(side_effect=lambda **kw: self.modules)
        au.module_bl_info = lambda mod: getattr(mod, 'bl_info', {})
        i18n = types.ModuleType('boneforge.i18n')
        i18n.T = lambda text: text
        self.addCleanup(patch.stopall)
        patch.dict(sys.modules, {'bpy': self.bpy, 'bpy.props': props, 'bpy.types': btypes, 'addon_utils': au, 'boneforge.i18n': i18n}).start()
        self.installer = load('_test_installer', 'core/addon_installer.py')
        self.bridge = load('_test_bridge', 'mmd/bridge.py')

    def archive(self, files):
        path = Path(self.temp.name) / 'addon.zip'
        with zipfile.ZipFile(path, 'w') as archive:
            for name in files:
                archive.writestr(name, '')
        return str(path)

    def test_extension_with_init_uses_extensions(self):
        path = self.archive(['blender_manifest.toml', '__init__.py'])
        result = self.installer.smart_install_zip(path)
        self.assertTrue(result.success)
        self.ops.extensions.package_install_files.assert_called_once_with(
            filepath=path, repo='user_default', enable_on_install=True)
        self.ops.preferences.addon_install.assert_not_called()

    def test_cancelled_extension_is_failure_without_legacy_fallback(self):
        self.ops.extensions.package_install_files.return_value = {'CANCELLED'}
        result = self.installer.smart_install_zip(self.archive(['blender_manifest.toml', '__init__.py']))
        self.assertFalse(result.success)
        self.ops.preferences.addon_install.assert_not_called()

    def test_extension_error_does_not_install_as_legacy(self):
        self.ops.extensions.package_install_files.side_effect = RuntimeError('incompatible version')
        result = self.installer.smart_install_zip(self.archive(['blender_manifest.toml']))
        self.assertFalse(result.success)
        self.ops.preferences.addon_install.assert_not_called()

    def test_no_local_repository_reports_failure(self):
        self.bpy.context.preferences.extensions.repos = []
        self.assertFalse(self.installer.smart_install_zip(self.archive(['blender_manifest.toml'])).success)

    def test_cancelled_legacy_is_failure(self):
        self.ops.preferences.addon_install.return_value = {'CANCELLED'}
        self.assertFalse(self.installer.smart_install_zip(self.archive(['mmd_tools/__init__.py'])).success)

    def test_cancelled_flat_legacy_is_failure(self):
        self.ops.preferences.addon_install.return_value = {'CANCELLED'}
        self.assertFalse(self.installer.smart_install_zip(self.archive(['__init__.py'])).success)

    def test_legacy_still_installs(self):
        self.assertTrue(self.installer.smart_install_zip(self.archive(['mmd_tools/__init__.py'])).success)

    def test_flat_legacy_still_wraps(self):
        result = self.installer.smart_install_zip(self.archive(['__init__.py']), fallback_folder_name='mmd_tools')
        self.assertTrue(result.success)
        self.assertTrue(result.repackaged)

    def test_namespaced_extension_without_bl_info_is_detected(self):
        mod = types.SimpleNamespace(__name__='bl_ext.user_default.mmd_tools')
        self.modules.append(mod)
        self.addons.append(types.SimpleNamespace(module=mod.__name__))
        self.assertIs(self.bridge.find_mmd_addon(), mod)
        self.assertTrue(self.bridge.mmd_addon_status()['enabled'])

    def test_enabled_extension_wins_over_disabled_legacy(self):
        old = types.SimpleNamespace(__name__='mmd_tools', bl_info={'name': 'MMD Tools'})
        active = types.SimpleNamespace(__name__='bl_ext.user_default.mmd_tools', bl_info={'name': 'MMD Tools'})
        self.modules.extend([old, active])
        self.addons.append(types.SimpleNamespace(module=active.__name__))
        status = self.bridge.mmd_addon_status()
        self.assertTrue(status['enabled'])
        self.assertEqual(status['module_name'], active.__name__)

    def test_cancelled_enable_is_not_success(self):
        self.modules.append(types.SimpleNamespace(__name__='mmd_tools', bl_info={'name': 'MMD Tools'}))
        self.assertIsNone(self.bridge._enable_first_mmd_addon())

    def test_missing_rna_operator_is_unavailable(self):
        op = Mock()
        op.get_rna_type.side_effect = RuntimeError('not registered')
        self.ops.mmd_tools.import_model = op
        self.assertFalse(self.bridge.is_mmd_op_available('import_model'))

    def test_cancelled_pmx_import_is_not_success(self):
        package = types.ModuleType('_test_mmd')
        package.__path__ = []
        package.bridge = self.bridge
        patch.dict(sys.modules, {'_test_mmd': package}).start()
        importer = load('_test_mmd.importer', 'mmd/importer.py')
        self.bridge.find_mmd_addon = lambda: object()
        self.ops.mmd_tools.import_model = Mock(return_value={'CANCELLED'})
        self.bpy.data = types.SimpleNamespace(objects=[])
        op = importer.BF_OT_MMDImportPMX()
        op.filepath = 'test.pmx'
        op.report = Mock()
        self.assertEqual(op.execute(self.bpy.context), {'CANCELLED'})


if __name__ == '__main__':
    unittest.main()
