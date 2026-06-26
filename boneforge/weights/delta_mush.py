"""BoneForge Phase 2B — Delta Mush Equivalent.

Post-deformation smoothing using Blender's Corrective Smooth modifier.
Smooths mesh deformation artifacts on dense meshes after armature evaluation.
Category: Deform Management.
"""

import bpy
import json
from bpy.props import IntProperty, FloatProperty, BoolProperty, PointerProperty
from bpy.types import PropertyGroup, Operator, Panel
from boneforge.core import register_handler_chain, unregister_handler_chain
from boneforge.i18n import T


class BF_DeltaMushSettings(PropertyGroup):
    """Delta Mush parameters."""
    iterations: IntProperty(
        name="Iterations",
        description="Number of smoothing iterations",
        min=1, max=50, default=10
    )
    smooth_strength: FloatProperty(
        name="Smooth Strength",
        description="Strength of smoothing effect",
        min=0.0, max=1.0, default=0.5
    )
    pin_borders: BoolProperty(
        name="Pin Borders",
        description="Keep mesh borders fixed",
        default=True
    )
    only_smooth_deform: BoolProperty(
        name="Only Smooth Deform",
        description="Only smooth deformation, not original shape",
        default=True
    )
    before_armature: BoolProperty(
        name="Before Armature",
        description="Place Corrective Smooth modifier before Armature",
        default=False
    )


class BF_OT_AddDeltaMush(Operator):
    """Add Delta Mush (Corrective Smooth) to mesh."""
    bl_idname = "boneforge.add_delta_mush"
    bl_label = "Add Delta Mush"
    bl_options = {'REGISTER', 'UNDO'}

    iterations: IntProperty(
        name="Iterations", min=1, max=50, default=10
    )
    smooth_strength: FloatProperty(
        name="Smooth Strength", min=0.0, max=1.0, default=0.5
    )
    pin_borders: BoolProperty(
        name="Pin Borders", default=True
    )
    only_smooth_deform: BoolProperty(
        name="Only Smooth Deform", default=True
    )

    @classmethod
    def poll(cls, context):
        return (context.mode == 'OBJECT' and
                context.object and
                context.object.type == 'MESH')

    def execute(self, context):
        mesh_obj = context.object

        # Check if modifier already exists
        if "DeltaMush" in mesh_obj.modifiers:
            self.report({'WARNING'}, "Delta Mush already applied")
            return {'FINISHED'}

        # Add Corrective Smooth modifier
        mod = mesh_obj.modifiers.new(name="DeltaMush", type='CORRECTIVE_SMOOTH')

        # Configure modifier
        mod.smooth_type = 'LENGTH_WEIGHTED'
        mod.iterations = self.iterations
        mod.scale = self.smooth_strength
        mod.use_pin_boundary = self.pin_borders
        mod.rest_source = 'BIND'

        # Store settings as custom property
        settings = {
            "iterations": self.iterations,
            "smooth_strength": self.smooth_strength,
            "pin_borders": self.pin_borders,
            "only_smooth_deform": self.only_smooth_deform
        }
        mesh_obj["boneforge_p2b_deltamush"] = json.dumps(settings)

        self.report({'INFO'}, "Added Delta Mush modifier")
        return {'FINISHED'}


class BF_OT_RemoveDeltaMush(Operator):
    """Remove Delta Mush modifier."""
    bl_idname = "boneforge.remove_delta_mush"
    bl_label = "Remove Delta Mush"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (context.mode == 'OBJECT' and
                context.object and
                context.object.type == 'MESH')

    def execute(self, context):
        mesh_obj = context.object

        if "DeltaMush" in mesh_obj.modifiers:
            mesh_obj.modifiers.remove(mesh_obj.modifiers["DeltaMush"])

        if "boneforge_p2b_deltamush" in mesh_obj:
            del mesh_obj["boneforge_p2b_deltamush"]

        self.report({'INFO'}, "Removed Delta Mush modifier")
        return {'FINISHED'}


class BF_OT_BindDeltaMush(Operator):
    """Bind Delta Mush modifier to rest pose."""
    bl_idname = "boneforge.bind_delta_mush"
    bl_label = "Bind Delta Mush"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (context.mode == 'OBJECT' and
                context.object and
                context.object.type == 'MESH' and
                "DeltaMush" in context.object.modifiers)

    def execute(self, context):
        mesh_obj = context.object
        mod = mesh_obj.modifiers["DeltaMush"]

        # In Blender, Corrective Smooth uses rest_source = 'BIND' for binding
        # The binding happens when rest_source is set and the modifier is evaluated
        # We need to force evaluation
        if hasattr(mod, 'rest_source'):
            if mod.rest_source != 'BIND':
                mod.rest_source = 'BIND'

        # Force depsgraph evaluation
        depsgraph = context.evaluated_depsgraph_get()
        mesh_obj.evaluated_get(depsgraph)

        self.report({'INFO'}, "Delta Mush bound to rest pose")
        return {'FINISHED'}


class BONEFORGE_PT_p2b_delta_mush(Panel):
    """Delta Mush panel in Object mode."""
    bl_label = " "
    bl_idname = "BONEFORGE_PT_p2b_delta_mush"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "BoneForge"
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.label(text=T("Delta Mush"))

    @classmethod
    def poll(cls, context):
        return (context.mode == 'OBJECT' and
                context.object and
                context.object.type == 'MESH')

    def draw(self, context):
        layout = self.layout
        mesh_obj = context.object

        has_delta_mush = "DeltaMush" in mesh_obj.modifiers

        if has_delta_mush:
            layout.label(text=T("Delta Mush Active"), icon='MODIFIER')

            mod = mesh_obj.modifiers["DeltaMush"]

            col = layout.column(align=True)
            col.prop(mod, "iterations")
            col.prop(mod, "scale", text=T("Smooth Strength"))
            col.prop(mod, "use_pin_boundary", text=T("Pin Borders"))

            row = layout.row(align=True)
            row.operator("boneforge.bind_delta_mush", text=T("Rebind"), icon='PINNED')
            row.operator("boneforge.remove_delta_mush", text=T("Remove"), icon='X')

        else:
            layout.label(text=T("Add corrective smoothing"), icon='INFO')

            col = layout.column(align=True)
            col.prop(mesh_obj.boneforge_delta_mush, "iterations")
            col.prop(mesh_obj.boneforge_delta_mush, "smooth_strength")
            col.prop(mesh_obj.boneforge_delta_mush, "pin_borders")
            col.prop(mesh_obj.boneforge_delta_mush, "only_smooth_deform")
            col.prop(mesh_obj.boneforge_delta_mush, "before_armature")

            op = layout.operator("boneforge.add_delta_mush", icon='MODIFIER')
            op.iterations = mesh_obj.boneforge_delta_mush.iterations
            op.smooth_strength = mesh_obj.boneforge_delta_mush.smooth_strength
            op.pin_borders = mesh_obj.boneforge_delta_mush.pin_borders
            op.only_smooth_deform = mesh_obj.boneforge_delta_mush.only_smooth_deform


def _delta_mush_evaluate(scene):
    """Placeholder handler for delta mush evaluation in deform chain."""
    pass


def register():
    """Register Delta Mush classes and properties."""
    bpy.utils.register_class(BF_DeltaMushSettings)
    bpy.utils.register_class(BF_OT_AddDeltaMush)
    bpy.utils.register_class(BF_OT_RemoveDeltaMush)
    bpy.utils.register_class(BF_OT_BindDeltaMush)
    bpy.utils.register_class(BONEFORGE_PT_p2b_delta_mush)

    bpy.types.Object.boneforge_delta_mush = PointerProperty(
        type=BF_DeltaMushSettings,
        name="Delta Mush"
    )

    # Register handler chain
    register_handler_chain('deform_post', _delta_mush_evaluate, priority=60)


def unregister():
    """Unregister Delta Mush classes and properties."""
    # Unregister handler chain
    unregister_handler_chain('deform_post', _delta_mush_evaluate)

    if hasattr(bpy.types.Object, 'boneforge_delta_mush'):
        del bpy.types.Object.boneforge_delta_mush

    bpy.utils.unregister_class(BONEFORGE_PT_p2b_delta_mush)
    bpy.utils.unregister_class(BF_OT_BindDeltaMush)
    bpy.utils.unregister_class(BF_OT_RemoveDeltaMush)
    bpy.utils.unregister_class(BF_OT_AddDeltaMush)
    bpy.utils.unregister_class(BF_DeltaMushSettings)
