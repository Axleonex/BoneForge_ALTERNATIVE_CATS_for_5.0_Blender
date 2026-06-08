"""BoneForge Phase 2B — Flood Fill Weight Tools.

Quick weight assignment operators: flood to zero, flood to one
(with proportional reduction), and flood to custom value.
Category: Weight Tools.
"""

import bpy
from bpy.props import FloatProperty, BoolProperty
import logging
from boneforge.i18n import T

logger = logging.getLogger(__name__)


class BONEFORGE_PT_p2b_flood_fill(bpy.types.Panel):
    """Flood fill weight tools panel."""
    bl_label = " "
    bl_idname = "BONEFORGE_PT_p2b_flood_fill"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BoneForge"

    def draw_header(self, context):
        self.layout.label(text=T("Flood Fill"))

    @classmethod
    def poll(cls, context):
        return context.mode == "PAINT_WEIGHT"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        col = layout.column(align=True)
        col.label(text=T("Flood Fill:"))

        # Flood to zero
        col.operator("boneforge.flood_to_zero", text=T("Flood to 0.0"))

        # Flood to one
        col.operator("boneforge.flood_to_one", text=T("Flood to 1.0"))

        # Flood to custom
        row = col.row(align=True)
        row.prop(scene, "boneforge_flood_custom_value", text=T("Custom Value"))
        row.operator("boneforge.flood_to_custom", text=T("Flood"))

        # Custom flood normalize toggle
        col.prop(scene, "boneforge_flood_normalize", text=T("Normalize Custom"))


class BF_OT_FloodToZero(bpy.types.Operator):
    """Set active vertex group to 0.0 on all/selected vertices."""
    bl_idname = "boneforge.flood_to_zero"
    bl_label = "Flood to Zero"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return (context.mode == "PAINT_WEIGHT" and
                context.active_object and
                context.active_object.type == "MESH" and
                context.active_object.vertex_groups.active)

    def execute(self, context):
        obj = context.active_object
        mesh = obj.data
        vgroup = obj.vertex_groups.active

        affected_count = 0

        # v3.1.6 (M-1): assigned-only walk; vg.remove is also list-tolerant.
        affected_verts = [
            vert.index for vert in mesh.vertices
            if any(vge.group == vgroup.index and vge.weight > 0.0
                   for vge in vert.groups)
        ]
        for vert_idx in affected_verts:
            vgroup.remove([vert_idx])
            affected_count += 1

        self.report({"INFO"}, f"Zeroed {vgroup.name} on {affected_count} vertices")
        return {"FINISHED"}


class BF_OT_FloodToOne(bpy.types.Operator):
    """Set active vertex group to 1.0 and reduce other weights proportionally."""
    bl_idname = "boneforge.flood_to_one"
    bl_label = "Flood to One"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return (context.mode == "PAINT_WEIGHT" and
                context.active_object and
                context.active_object.type == "MESH" and
                context.active_object.vertex_groups.active)

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        obj = context.active_object
        mesh = obj.data
        vgroup = obj.vertex_groups.active

        affected_count = 0

        # Apply flood to one with proportional reduction
        for vert in mesh.vertices:
            # Get other group weights
            other_weights = {}
            total_other = 0.0

            # v3.1.6 (M-1): assigned-only weight read.
            for vge in vert.groups:
                if vge.group == vgroup.index or vge.weight <= 0.0:
                    continue
                other_weights[vge.group] = vge.weight
                total_other += vge.weight

            # Set active group to 1.0
            vgroup.add([vert.index], 1.0, "REPLACE")

            # Reduce other weights proportionally
            if total_other > 0.0 and total_other > 1e-6:
                scale_factor = 0.0  # Active bone gets 1.0, so remaining budget is 0

                for vg_idx, weight in other_weights.items():
                    new_weight = weight * scale_factor
                    if new_weight > 0.0:
                        obj.vertex_groups[vg_idx].add([vert.index], new_weight, "REPLACE")
                    else:
                        obj.vertex_groups[vg_idx].remove([vert.index])

            affected_count += 1

        self.report({"INFO"}, f"Flooded {vgroup.name} to 1.0 on {affected_count} vertices")
        return {"FINISHED"}


class BF_OT_FloodToCustom(bpy.types.Operator):
    """Set active vertex group to custom float value."""
    bl_idname = "boneforge.flood_to_custom"
    bl_label = "Flood to Custom"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return (context.mode == "PAINT_WEIGHT" and
                context.active_object and
                context.active_object.type == "MESH" and
                context.active_object.vertex_groups.active)

    def execute(self, context):
        obj = context.active_object
        mesh = obj.data
        scene = context.scene
        vgroup = obj.vertex_groups.active

        custom_value = scene.boneforge_flood_custom_value
        normalize = scene.boneforge_flood_normalize

        affected_count = 0

        # Flood to custom value
        for vert in mesh.vertices:
            if custom_value > 0.0:
                vgroup.add([vert.index], custom_value, "REPLACE")
                affected_count += 1

        # Normalize if requested
        if normalize and custom_value > 0.0:
            for vert in mesh.vertices:
                total_weight = 0.0
                weights = {}

                # v3.1.6 (M-1): assigned-only weight read.
                weights = {vge.group: vge.weight
                           for vge in vert.groups if vge.weight > 0.0}
                total_weight = sum(weights.values())

                if total_weight > 0.0 and abs(total_weight - 1.0) > 0.001:
                    inv = 1.0 / total_weight
                    for vg_idx, weight in weights.items():
                        obj.vertex_groups[vg_idx].add(
                            [vert.index], weight * inv, "REPLACE",
                        )

        self.report({"INFO"}, f"Flooded {vgroup.name} to {custom_value} on {affected_count} vertices")
        return {"FINISHED"}


def register():
    """Register flood fill tool classes and properties."""
    bpy.utils.register_class(BONEFORGE_PT_p2b_flood_fill)
    bpy.utils.register_class(BF_OT_FloodToZero)
    bpy.utils.register_class(BF_OT_FloodToOne)
    bpy.utils.register_class(BF_OT_FloodToCustom)

    # Scene properties
    bpy.types.Scene.boneforge_flood_custom_value = FloatProperty(
        name="Custom Value",
        description="Custom weight value for flood",
        min=0.0,
        max=1.0,
        default=0.5
    )

    bpy.types.Scene.boneforge_flood_normalize = BoolProperty(
        name="Normalize",
        description="Normalize weights after flooding",
        default=False
    )


def unregister():
    """Unregister flood fill tool classes and properties."""
    bpy.utils.unregister_class(BONEFORGE_PT_p2b_flood_fill)
    bpy.utils.unregister_class(BF_OT_FloodToZero)
    bpy.utils.unregister_class(BF_OT_FloodToOne)
    bpy.utils.unregister_class(BF_OT_FloodToCustom)

    # Clean up properties
    if hasattr(bpy.types.Scene, "boneforge_flood_custom_value"):
        del bpy.types.Scene.boneforge_flood_custom_value
    if hasattr(bpy.types.Scene, "boneforge_flood_normalize"):
        del bpy.types.Scene.boneforge_flood_normalize
