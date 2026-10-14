"""Host regression: unique Task Board cards and working Health Check.

Run in a factory-startup Blender/Bforartists process with --python-exit-code 1.
"""
import sys
from collections import Counter
from pathlib import Path
from types import SimpleNamespace

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def run():
    import addon_utils
    import bpy
    assert addon_utils.enable("boneforge", default_set=True) is not None
    from boneforge.taskboard import analyzer, panel
    from boneforge.taskboard.tasks import BF_Task
    from boneforge.advanced_rigging import rig_validator
    from boneforge.core.tool_toggle_operator import BF_OT_ToggleTool
    from boneforge.core.prefs import addon_prefs
    prefs = addon_prefs(bpy.context)
    prefs.language = "en"
    bpy.ops.object.armature_add()
    arm = bpy.context.object
    arm.name = "Health Check Target"
    cls = panel.BF_OT_OpenHealthCheck
    seen = []
    rig_validator.register_custom_check("test_health_target", lambda obj: seen.append(obj.name) or [])
    try:
        analyzer.get_tasks(arm)
        assert arm.name in analyzer._cache
        assert bpy.ops.boneforge.open_health_check.poll()
        assert bpy.ops.boneforge.open_health_check() == {'FINISHED'}
        assert seen[-1] == arm.name
        assert len(bpy.context.window_manager.boneforge_validation_results) > 0
        assert arm.name not in analyzer._cache, "health results invalidate stale tasks"
        bpy.ops.mesh.primitive_cube_add()
        mesh = bpy.context.object
        assert not bpy.ops.boneforge.open_health_check.poll()
        mesh.parent = arm
        assert bpy.ops.boneforge.open_health_check.poll()
        assert bpy.ops.boneforge.open_health_check() == {'FINISHED'}
        assert seen[-1] == arm.name and bpy.context.active_object == mesh
        mesh.parent = None
        modifier = mesh.modifiers.new("Avatar Rig", 'ARMATURE')
        modifier.object = arm
        assert bpy.ops.boneforge.open_health_check.poll()
        assert bpy.ops.boneforge.open_health_check() == {'FINISHED'}
        assert seen[-1] == arm.name and bpy.context.active_object == mesh
        bpy.context.view_layer.objects.active = None
        assert not bpy.ops.boneforge.open_health_check.poll()
        bpy.context.view_layer.objects.active = arm
        bpy.ops.object.mode_set(mode='POSE')
        assert bpy.ops.boneforge.open_health_check() == {'FINISHED'}
        assert bpy.context.mode == 'POSE' and seen[-1] == arm.name
        bpy.ops.object.mode_set(mode='OBJECT')
    finally:
        rig_validator._custom_checks.pop("test_health_target", None)

    reports = []
    target = SimpleNamespace(report=lambda level, message: reports.append((level, message)))
    target.execute = lambda ctx: cls.execute(target, ctx)
    class PopupWM:
        calls = []
        def invoke_popup(self, op, **kwargs):
            self.calls.append(kwargs)
            assert len(bpy.context.window_manager.boneforge_validation_results) > 0
            return {'RUNNING_MODAL'}
    class PopupContext:
        window_manager = PopupWM()
        def __getattr__(self, name):
            return getattr(bpy.context, name)
    context = PopupContext()
    assert cls.invoke(target, context, None) == {'RUNNING_MODAL'}
    assert context.window_manager.calls == [{'width': 480}]

    # Enabled package with a missing operator must report registration failure.
    validator_cls = rig_validator.BF_OT_RunValidation
    bpy.utils.unregister_class(validator_cls)
    try:
        assert cls.execute(target, bpy.context) == {'CANCELLED'}
        assert 'failed to register' in reports[-1][1]
    finally:
        bpy.utils.register_class(validator_cls)
    BF_OT_ToggleTool._deferred_work({'tool_id': 'phase2c_advanced'})
    try:
        calls = len(context.window_manager.calls)
        assert cls.invoke(target, context, None) == {'CANCELLED'}
        assert 'Enable Advanced Rigging Systems' in reports[-1][1]
        assert len(context.window_manager.calls) == calls
    finally:
        BF_OT_ToggleTool._deferred_work({'tool_id': 'phase2c_advanced'})
    assert bpy.ops.boneforge.open_health_check() == {'FINISHED'}

    class Layout:
        def __init__(self, log):
            self.log = log
        def __getattr__(self, name):
            def call(*args, **kwargs):
                self.log.append((name, args, kwargs))
                if name == 'panel':
                    return Layout(self.log), Layout(self.log)
                return Layout(self.log)
            return call
    def labels(log):
        return [kwargs.get('text', '') for name, args, kwargs in log if name == 'label']
    # The popup draws the actual result collection and a refresh action.
    log = []
    target.layout = Layout(log)
    cls.draw(target, bpy.context)
    assert any(name == 'template_list' and args[0] == 'BONEFORGE_UL_ValidationResults'
               for name, args, kwargs in log)
    assert any(name == 'operator' and args[0] == 'boneforge.open_health_check'
               for name, args, kwargs in log)
    assert target.layout.operator_context == 'EXEC_DEFAULT'

    tasks = [
        BF_Task('high_a', 'Quick A', '', 'geometry', status='suggestion', impact=10, effort=1),
        BF_Task('high_b', 'Quick B', '', 'rig_controls', status='suggestion', impact=9, effort=1),
        BF_Task('high_c', 'Quick C', '', 'rig_controls', status='suggestion', impact=8, effort=1),
        BF_Task('low_a', 'Other A', '', 'geometry', status='suggestion', impact=3, effort=3),
        BF_Task('low_b', 'Other B', '', 'skinning', status='suggestion', impact=2, effort=4),
        BF_Task('low_c', 'Other C', '', 'geometry', status='suggestion', impact=1, effort=4),
    ]
    original_get = analyzer.get_tasks
    original_panel_get = panel.get_tasks
    original_card = panel._draw_task_card
    fixture = tasks[:]
    drawn = []
    analyzer.get_tasks = lambda obj: fixture
    panel.get_tasks = lambda obj: fixture
    panel._draw_task_card = lambda layout, task, context, compact=False: drawn.append(task.task_id)
    category_key = 'boneforge_taskboard_collapsed_geometry'
    bpy.context.scene[category_key] = False
    try:
        log = []
        panel.BONEFORGE_PT_taskboard.draw(SimpleNamespace(layout=Layout(log)), bpy.context)
        assert Counter(drawn) == Counter(t.task_id for t in tasks), drawn
        assert drawn[:3] == ['high_a', 'high_b', 'high_c'], drawn
        assert 'Remaining Tasks (3)' in labels(log), labels(log)
        categories = [kwargs.get('text', '') for name, args, kwargs in log
                      if name == 'operator' and args[0] == 'boneforge.taskboard_toggle_category']
        assert any('Geometry' in text and '(2)' in text for text in categories), categories
        assert any('Skinning' in text and '(1)' in text for text in categories), categories
        assert not any('Rig Controls' in text for text in categories), categories
        bpy.context.scene[category_key] = True
        drawn.clear()
        panel.BONEFORGE_PT_taskboard.draw(SimpleNamespace(layout=Layout([])), bpy.context)
        assert Counter(drawn) == Counter(['high_a', 'high_b', 'high_c', 'low_b']), drawn
        # With fewer than three tasks, no empty Remaining Tasks section is shown.
        fixture = tasks[:2]
        log = []
        drawn.clear()
        panel.BONEFORGE_PT_taskboard.draw(SimpleNamespace(layout=Layout(log)), bpy.context)
        assert Counter(drawn) == Counter(['high_a', 'high_b']), drawn
        assert not any('Remaining Tasks' in text for text in labels(log))
        fixture = []
        log = []
        drawn.clear()
        panel.BONEFORGE_PT_taskboard.draw(SimpleNamespace(layout=Layout(log)), bpy.context)
        assert not drawn and any('No issues found' in text for text in labels(log))
    finally:
        analyzer.get_tasks = original_get
        panel.get_tasks = original_panel_get
        panel._draw_task_card = original_card
        del bpy.context.scene[category_key]
    for language in ('en', 'es', 'fr', 'pt', 'ja', 'ko', 'zh'):
        from boneforge.i18n import _load_lang
        if language != 'en':
            strings = _load_lang(language)
            for key in ('Remaining Tasks', 'Refresh Results', 'Select an armature or a mesh bound to one.',
                        'Enable Advanced Rigging Systems in add-on preferences.',
                        'Rig Validator failed to register. Check the console for details.',
                        'Failed checks: {count}', 'Warnings: {count}'):
                assert strings.get(key), (language, key)
    addon_utils.disable('boneforge', default_set=True)
    print('PASS Task Board: unique Quick Wins + Remaining Tasks; correct counts/collapse; armature, parented/modifier mesh and Pose checks; invalid selection; disabled/missing validator; popup dispatch/results/refresh; seven languages')


if __name__ == '__main__':
    run()
