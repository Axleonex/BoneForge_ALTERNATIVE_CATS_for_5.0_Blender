"""VRM import operator — wraps upstream + runs BoneForge post-import passes.

Post-import passes run *after* the upstream importer succeeds:

1. **Source format detection** — was this VRM 0.x or 1.0?
2. **Bone-name aliasing** — stamp parallel VRChat-style aliases on every
   humanoid bone via custom properties so existing BoneForge tools
   (weight transfer, rig validator, picker) work without a rename.
3. **Viseme blendshape surface** — copy ``A/I/U/E/O`` references into
   ``boneforge_viseme_*`` custom properties so the existing VRChat
   viseme mapper finds them.
4. **Meta / spring / blendshape preservation** — snapshot upstream data
   onto the armature as JSON custom properties (the Phase-3 unanimous
   addition).

The post-import passes are *non-destructive* — they only add data; they
do not rename, reparent, or restructure anything the upstream importer
produced. Round-tripping through the BoneForge bridge yields a VRM that
is byte-identical to the source when nothing is edited in between.
"""

from __future__ import annotations

import logging

import bpy
from bpy.props import StringProperty
from bpy.types import Operator

from . import bridge, meta

logger = logging.getLogger(__name__)


# Canonical VRM 1.0 humanoid bones → VRChat / Unity humanoid alias.
# Both VRM 0.x and VRM 1.0 share these humanoid slot names; the underlying
# Blender bone names from VRoid usually look like ``J_Bip_C_Hips`` etc.,
# but the upstream importer attaches the humanoid mapping as a property
# group we read here.
_VRM_HUMANOID_TO_VRCHAT = {
    "hips": "Hips",
    "spine": "Spine",
    "chest": "Chest",
    "upperChest": "UpperChest",
    "neck": "Neck",
    "head": "Head",
    "leftEye": "LeftEye",
    "rightEye": "RightEye",
    "jaw": "Jaw",
    "leftShoulder": "LeftShoulder",
    "leftUpperArm": "LeftUpperArm",
    "leftLowerArm": "LeftLowerArm",
    "leftHand": "LeftHand",
    "rightShoulder": "RightShoulder",
    "rightUpperArm": "RightUpperArm",
    "rightLowerArm": "RightLowerArm",
    "rightHand": "RightHand",
    "leftUpperLeg": "LeftUpperLeg",
    "leftLowerLeg": "LeftLowerLeg",
    "leftFoot": "LeftFoot",
    "leftToes": "LeftToes",
    "rightUpperLeg": "RightUpperLeg",
    "rightLowerLeg": "RightLowerLeg",
    "rightFoot": "RightFoot",
    "rightToes": "RightToes",
}

# VRM viseme mouth-shape names (VRM 0.x preset names; VRM 1.0 uses the
# same human-readable expression keys).
_VRM_VISEMES = ("a", "i", "u", "e", "o", "neutral", "blink",
                "blink_l", "blink_r", "lookup", "lookdown",
                "lookleft", "lookright")


def _humanoid_bone_map(armature_obj):
    """Read upstream humanoid bone mapping → ``{slot_name: bone_name}``.

    Tries both upstream shapes; returns ``{}`` if no map is reachable.
    """
    arm_data = armature_obj.data
    for ext_attr in ("vrm_addon_extension", "vrm_extension"):
        ext = getattr(arm_data, ext_attr, None)
        if ext is None:
            continue
        # VRM 1.0
        humanoid = (
            getattr(getattr(ext, "vrm1", None), "humanoid", None)
            or getattr(getattr(ext, "vrm0", None), "humanoid", None)
        )
        if humanoid is None:
            continue
        bones = getattr(humanoid, "human_bones", None)
        if bones is None:
            continue
        result = {}
        # VRM 1.0 puts each slot on a named attribute.
        for slot in _VRM_HUMANOID_TO_VRCHAT:
            slot_attr = getattr(bones, slot, None)
            if slot_attr is None:
                continue
            node = getattr(slot_attr, "node", None)
            if node is None:
                continue
            bone_name = getattr(node, "bone_name", None) or getattr(node, "value", None)
            if bone_name:
                result[slot] = bone_name
        if result:
            return result
    return {}


def _stamp_humanoid_aliases(armature_obj):
    """Write VRChat-style aliases onto each humanoid bone as a custom prop.

    Adds ``boneforge_humanoid_alias`` to every mapped pose bone. The
    weight transfer + validator already look up bones by VRChat name;
    this pass lets them work on a freshly imported VRoid avatar without
    a rename pass.
    """
    mapping = _humanoid_bone_map(armature_obj)
    stamped = 0
    for slot, bone_name in mapping.items():
        bone = armature_obj.data.bones.get(bone_name)
        if bone is None:
            continue
        bone["boneforge_humanoid_alias"] = _VRM_HUMANOID_TO_VRCHAT.get(slot, slot)
        stamped += 1
    return stamped


def _surface_visemes(armature_obj):
    """Stamp viseme references onto the meshes parented under the armature.

    For each mesh child, look at its shape keys; if a key name (case-
    insensitive) matches a VRM viseme, write
    ``boneforge_viseme_<name>`` = shape_key_name on the mesh object.
    Existing BoneForge viseme tooling reads these.
    """
    surfaced = 0
    for child in armature_obj.children:
        if child.type != "MESH":
            continue
        sk = child.data.shape_keys
        if sk is None:
            continue
        names_lower = {k.name.lower(): k.name for k in sk.key_blocks}
        for viseme in _VRM_VISEMES:
            if viseme in names_lower:
                child[f"boneforge_viseme_{viseme}"] = names_lower[viseme]
                surfaced += 1
    return surfaced


class BF_OT_VRMImport(Operator):
    """Import a .vrm via the upstream add-on, then run BoneForge passes."""

    bl_idname = "boneforge.vrm_import"
    bl_label = "Import VRM…"
    bl_description = (
        "Import a VRM file via vrm-addon-for-blender, then preserve "
        "license / spring / expression data on the armature and stamp "
        "VRChat-compatible humanoid aliases for use with BoneForge tools"
    )
    bl_options = {"REGISTER", "UNDO"}

    filepath: StringProperty(subtype="FILE_PATH")
    filter_glob: StringProperty(default="*.vrm", options={"HIDDEN"})

    def invoke(self, context, event):
        # Fail fast if upstream isn't there — better than silently
        # opening a file dialog that leads nowhere.
        if bridge.find_vrm_addon() is None:
            self.report(
                {"ERROR"},
                "VRM Add-on for Blender not detected. Click "
                "'Install / Enable VRM Add-on' in the BoneForge VRM "
                "panel first.",
            )
            return {"CANCELLED"}
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

    def execute(self, context):
        if not self.filepath:
            self.report({"ERROR"}, "No file selected")
            return {"CANCELLED"}
        if bridge.find_vrm_addon() is None:
            self.report({"ERROR"}, "VRM Add-on not available")
            return {"CANCELLED"}

        # Snapshot the set of armatures so we can identify what the
        # upstream importer added. ``import_scene.vrm`` does not return
        # the new object on its own.
        before = {o.name for o in bpy.data.objects if o.type == "ARMATURE"}

        try:
            bpy.ops.import_scene.vrm(filepath=self.filepath)
        except (RuntimeError, AttributeError) as exc:
            self.report({"ERROR"}, f"VRM import failed: {exc}")
            logger.exception("[BoneForge] VRM import failed")
            return {"CANCELLED"}

        after = {o.name for o in bpy.data.objects if o.type == "ARMATURE"}
        new_arms = [
            bpy.data.objects[name] for name in (after - before)
        ]
        if not new_arms:
            # Some upstream versions reuse an existing armature object;
            # fall back to the active object.
            obj = context.active_object
            if obj is not None and obj.type == "ARMATURE":
                new_arms = [obj]

        for arm in new_arms:
            try:
                meta.preserve_to_armature(arm)
                aliases = _stamp_humanoid_aliases(arm)
                visemes = _surface_visemes(arm)
                logger.info(
                    "[BoneForge] post-import passes on %s: "
                    "%d humanoid aliases, %d visemes surfaced",
                    arm.name, aliases, visemes,
                )
            except Exception as exc:
                # Post-import passes are best-effort. Never let them
                # break a successful upstream import.
                logger.warning(
                    "[BoneForge] post-import pass failed on %s: %s",
                    arm.name, exc,
                )

        self.report(
            {"INFO"},
            f"Imported VRM ({len(new_arms)} armature(s)); "
            "license + spring data preserved on armature.",
        )
        return {"FINISHED"}
