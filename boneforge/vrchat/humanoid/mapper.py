"""BoneForge VRChat — Humanoid Bone Mapper.

Map armature bones to Unity Humanoid bone slots (21 required, many optional).
Store and retrieve mappings from armature custom properties.
Category: VRChat Setup.
"""

import json

import bpy
from bpy.props import StringProperty
from bpy.types import Operator, Panel

from boneforge.core import active_armature

import logging
from boneforge.i18n import T

logger = logging.getLogger(__name__)

# ── Constants ────────────────────────────────────────────────────────

# 21 required humanoid bone slots (first 20 are actual requirement)
REQUIRED_SLOTS = [
    "Hips",
    "Spine",
    "Chest",
    "UpperChest",
    "Neck",
    "Head",
    "LeftShoulder",
    "RightShoulder",
    "LeftUpperArm",
    "RightUpperArm",
    "LeftLowerArm",
    "RightLowerArm",
    "LeftHand",
    "RightHand",
    "LeftUpperLeg",
    "RightUpperLeg",
    "LeftLowerLeg",
    "RightLowerLeg",
    "LeftFoot",
    "RightFoot",
]

# Optional slots beyond the 20 required
OPTIONAL_SLOTS = [
    "Jaw",
    "LeftEye",
    "RightEye",
    "LeftThumbProximal",
    "LeftThumbIntermediate",
    "LeftThumbDistal",
    "LeftIndexProximal",
    "LeftIndexIntermediate",
    "LeftIndexDistal",
    "LeftMiddleProximal",
    "LeftMiddleIntermediate",
    "LeftMiddleDistal",
    "LeftRingProximal",
    "LeftRingIntermediate",
    "LeftRingDistal",
    "LeftLittleProximal",
    "LeftLittleIntermediate",
    "LeftLittleDistal",
    "RightThumbProximal",
    "RightThumbIntermediate",
    "RightThumbDistal",
    "RightIndexProximal",
    "RightIndexIntermediate",
    "RightIndexDistal",
    "RightMiddleProximal",
    "RightMiddleIntermediate",
    "RightMiddleDistal",
    "RightRingProximal",
    "RightRingIntermediate",
    "RightRingDistal",
    "RightLittleProximal",
    "RightLittleIntermediate",
    "RightLittleDistal",
    "LeftToes",
    "RightToes",
]

ALL_SLOTS = REQUIRED_SLOTS + OPTIONAL_SLOTS


# ── HumanoidMapping class ────────────────────────────────────────────

class HumanoidMapping:
    """Stores slot → bone_name mappings for a humanoid avatar."""

    def __init__(self, mapping_dict=None):
        """Initialize from dict or empty."""
        self.mapping = mapping_dict or {}

    def set_slot(self, slot_name, bone_name):
        """Map a slot to a bone name."""
        if bone_name:
            self.mapping[slot_name] = bone_name
        else:
            self.mapping.pop(slot_name, None)

    def get_slot(self, slot_name):
        """Get bone name for a slot, or None."""
        return self.mapping.get(slot_name)

    def to_dict(self):
        """Export as dict."""
        return dict(self.mapping)

    def validate_required(self):
        """Check which required slots are missing. Returns list of missing slot names."""
        missing = []
        for slot in REQUIRED_SLOTS:
            if slot not in self.mapping or not self.mapping[slot]:
                missing.append(slot)
        return missing

    def completion_percent(self):
        """Return percentage of required slots mapped (0-100)."""
        mapped = sum(1 for s in REQUIRED_SLOTS if self.mapping.get(s))
        return int((mapped / len(REQUIRED_SLOTS)) * 100)


# ── Utility functions ────────────────────────────────────────────────

def _get_armature_bones(armature):
    """Get all bone names in an armature."""
    if not armature or armature.type != "ARMATURE":
        return []
    return [b.name for b in armature.data.bones]


def auto_map_humanoid(armature):
    """Auto-map humanoid slots using naming convention detection.

    Looks for common bone naming patterns (e.g. "Armature|Spine|chest" patterns).
    Returns HumanoidMapping object.
    """
    bones = _get_armature_bones(armature)
    bones_lower = {b.lower(): b for b in bones}

    mapping_dict = {}

    # Common naming patterns for each slot
    patterns = {
        "Hips": ["hips", "hip", "pelvis", "root"],
        "Spine": ["spine", "spine1"],
        "Chest": ["chest", "spine2"],
        "UpperChest": ["upperchest", "upper_chest", "spine3"],
        "Neck": ["neck"],
        "Head": ["head"],
        "LeftShoulder": ["left_shoulder", "l_shoulder", "shoulder_l"],
        "RightShoulder": ["right_shoulder", "r_shoulder", "shoulder_r"],
        "LeftUpperArm": ["left_upperarm", "l_upperarm", "upper_arm_l"],
        "RightUpperArm": ["right_upperarm", "r_upperarm", "upper_arm_r"],
        "LeftLowerArm": ["left_lowerarm", "l_lowerarm", "lower_arm_l", "left_forearm", "l_forearm"],
        "RightLowerArm": ["right_lowerarm", "r_lowerarm", "lower_arm_r", "right_forearm", "r_forearm"],
        "LeftHand": ["left_hand", "l_hand", "hand_l"],
        "RightHand": ["right_hand", "r_hand", "hand_r"],
        "LeftUpperLeg": ["left_upperleg", "l_upperleg", "upper_leg_l", "left_thigh", "l_thigh"],
        "RightUpperLeg": ["right_upperleg", "r_upperleg", "upper_leg_r", "right_thigh", "r_thigh"],
        "LeftLowerLeg": ["left_lowerleg", "l_lowerleg", "lower_leg_l", "left_calf", "l_calf"],
        "RightLowerLeg": ["right_lowerleg", "r_lowerleg", "lower_leg_r", "right_calf", "r_calf"],
        "LeftFoot": ["left_foot", "l_foot", "foot_l"],
        "RightFoot": ["right_foot", "r_foot", "foot_r"],
        "Jaw": ["jaw"],
        "LeftEye": ["left_eye", "l_eye", "eye_l"],
        "RightEye": ["right_eye", "r_eye", "eye_r"],
    }

    for slot, pattern_list in patterns.items():
        for pattern in pattern_list:
            if pattern in bones_lower:
                mapping_dict[slot] = bones_lower[pattern]
                break

    return HumanoidMapping(mapping_dict)


def get_mapping(armature):
    """Retrieve stored mapping from armature custom property."""
    key = "boneforge_vrchat_humanoid"
    if hasattr(armature, key):
        try:
            data = json.loads(getattr(armature, key))
            return HumanoidMapping(data)
        except (json.JSONDecodeError, TypeError, ValueError) as e:
            # M-07: Log JSON parse errors for debugging
            logger.error(f"[BoneForge] JSON parse error loading humanoid mapping: {e}")
    return HumanoidMapping()


def save_mapping(armature, mapping):
    """Save mapping to armature custom property."""
    key = "boneforge_vrchat_humanoid"
    armature[key] = json.dumps(mapping.to_dict())


# ── Operators ────────────────────────────────────────────────────────

class BF_OT_VRC_AutoMapHumanoid(Operator):
    """Auto-map humanoid slots based on naming conventions."""

    bl_idname = "boneforge.vrc_auto_map_humanoid"
    bl_label = "Auto-Map Humanoid"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        arm = active_armature(context)
        if not arm:
            self.report({"ERROR"}, "No active armature selected")
            return {"CANCELLED"}

        mapping = auto_map_humanoid(arm)
        save_mapping(arm, mapping)

        missing = mapping.validate_required()
        if missing:
            self.report(
                {"WARNING"},
                f"Mapped {len(REQUIRED_SLOTS) - len(missing)}/{len(REQUIRED_SLOTS)} "
                f"required slots. Missing: {', '.join(missing[:5])}"
            )
        else:
            self.report({"INFO"}, "Successfully mapped all required humanoid slots")

        return {"FINISHED"}


class BF_OT_VRC_SetHumanoidSlot(Operator):
    """Set a single humanoid bone slot."""

    bl_idname = "boneforge.vrc_set_humanoid_slot"
    bl_label = "Set Humanoid Slot"
    bl_options = {"REGISTER", "UNDO"}

    slot_name: StringProperty(
        name="Slot",
        description="Humanoid slot name"
    )
    bone_name: StringProperty(
        name="Bone",
        description="Target bone name"
    )

    def execute(self, context):
        arm = active_armature(context)
        if not arm:
            return {"CANCELLED"}

        # Validate bone exists
        bones = _get_armature_bones(arm)
        if self.bone_name and self.bone_name not in bones:
            self.report({"ERROR"}, f"Bone '{self.bone_name}' not found")
            return {"CANCELLED"}

        mapping = get_mapping(arm)
        mapping.set_slot(self.slot_name, self.bone_name)
        save_mapping(arm, mapping)

        return {"FINISHED"}


class BF_OT_VRC_ValidateMapping(Operator):
    """Validate humanoid mapping completeness."""

    bl_idname = "boneforge.vrc_validate_humanoid_mapping"
    bl_label = "Validate Mapping"
    bl_options = {"REGISTER"}

    def execute(self, context):
        arm = active_armature(context)
        if not arm:
            return {"CANCELLED"}

        mapping = get_mapping(arm)
        missing = mapping.validate_required()

        if missing:
            self.report(
                {"WARNING"},
                f"Missing {len(missing)} required slots: "
                f"{', '.join(missing[:8])}"
            )
        else:
            self.report({"INFO"}, "All required humanoid slots are mapped!")

        return {"FINISHED"}


class BF_OT_VRC_TPosePreview(Operator):
    """Apply T-pose to the armature for preview."""

    bl_idname = "boneforge.vrc_t_pose_preview"
    bl_label = "T-Pose Preview"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from mathutils import Quaternion

        arm = active_armature(context)
        if arm is None:
            self.report({'ERROR'}, "No active armature")
            return {'CANCELLED'}

        if not arm.pose:
            self.report({'ERROR'}, "No pose data available")
            return {'CANCELLED'}

        # Reset all pose bone rotations to identity (rest pose = T-pose assumption)
        reset_count = 0
        for pose_bone in arm.pose.bones:
            # Reset rotation
            pose_bone.rotation_quaternion = Quaternion((1, 0, 0, 0))
            pose_bone.rotation_euler = (0, 0, 0)
            pose_bone.rotation_axis_angle = (0, 0, 1, 0)
            # Reset location offset
            pose_bone.location = (0, 0, 0)
            # Reset scale
            pose_bone.scale = (1, 1, 1)
            reset_count += 1

        # Force viewport update
        context.view_layer.update()

        self.report({'INFO'}, f"Reset {reset_count} bones to rest pose (T-pose)")
        return {'FINISHED'}


# ── Panel ────────────────────────────────────────────────────────────

class BONEFORGE_PT_vrc_humanoid(Panel):
    """Humanoid mapper panel."""

    bl_label = " "
    bl_idname = "BONEFORGE_PT_vrc_humanoid"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
    bl_parent_id = "BONEFORGE_PT_vrc_main"

    def draw_header(self, context):
        self.layout.label(text=T("Humanoid Mapper"))

    @classmethod
    def poll(cls, context):
        return active_armature(context) is not None

    def draw(self, context):
        arm = active_armature(context)
        layout = self.layout

        if not arm:
            return

        mapping = get_mapping(arm)
        bones = _get_armature_bones(arm)

        # Progress indicator
        completion = mapping.completion_percent()
        row = layout.row()
        row.label(text=f"Required Slots: {completion}%")

        # Auto-map button
        layout.operator(
            "boneforge.vrc_auto_map_humanoid",
            text=T("Auto-Map All")
        )

        # Validate button
        layout.operator(
            "boneforge.vrc_validate_humanoid_mapping",
            text=T("Validate")
        )

        layout.separator()

        # Required slots section
        box = layout.box()
        row = box.row()
        row.label(text=T("Required Slots (20)"), icon="ARMATURE_DATA")

        for slot in REQUIRED_SLOTS:
            row = box.row()
            row.label(text=slot, icon="BONE_DATA")

            current_bone = mapping.get_slot(slot)
            row.label(text=current_bone or "(unmapped)")

        layout.separator()

        # Optional slots section (collapsed)
        box = layout.box()
        row = box.row(align=True)
        row.label(text=T("Optional Slots"), icon="COLLAPSEMENU")

        for slot in OPTIONAL_SLOTS[:5]:
            row = box.row()
            row.label(text=slot, icon="BONE_DATA")
            current_bone = mapping.get_slot(slot)
            row.label(text=current_bone or "(unmapped)")

        layout.separator()
        layout.label(text=T("Also configure visemes in Face Tracking panel"), icon="INFO")


# ── Registration ─────────────────────────────────────────────────────

classes = (
    BF_OT_VRC_AutoMapHumanoid,
    BF_OT_VRC_SetHumanoidSlot,
    BF_OT_VRC_ValidateMapping,
    BF_OT_VRC_TPosePreview,
    BONEFORGE_PT_vrc_humanoid,
)


def register():
    """Register humanoid mapper classes."""
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    """Unregister humanoid mapper classes."""
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
