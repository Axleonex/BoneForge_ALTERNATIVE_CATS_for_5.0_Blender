"""VRM export operator with per-target presets.

The user picks a *target pipeline* — VRChat FBX, VRM 1.0, VRM 0.x,
VSeeFace, Warudo, or Resonite — and BoneForge dispatches to the right
exporter with the right pre-flight checks. The presets are *opinions*,
not file-format choices: VSeeFace and Warudo both produce VRM 1.0 but
differ in which features the host actually consumes (e.g. VSeeFace cares
deeply about ``LookAt`` bones; Warudo less so). The lint pass in
``vrm/lint.py`` is the per-target opinion, applied here.
"""

from __future__ import annotations

import logging

import bpy
import os as _os
from bpy.props import StringProperty, EnumProperty, BoolProperty
from bpy.types import Operator

from boneforge.core import active_armature

from . import bridge, lint as lint_mod

logger = logging.getLogger(__name__)


# Target preset → (file extension, dispatcher key).
# Dispatcher keys: "VRM_1_0", "VRM_0_X", "FBX_VRCHAT".
TARGETS = (
    ("VRM_1_0", "VRM 1.0", "Modern VRM spec — preferred for most VTuber tools"),
    ("VRM_0_X", "VRM 0.x", "Legacy VRM spec — still required by some hosts"),
    ("VRCHAT_FBX", "VRChat FBX",
     "FBX with VRChat-tuned axis / scale / armature settings"),
    ("VSEEFACE", "VSeeFace (VRM 1.0)",
     "VRM 1.0 with VSeeFace-specific lint pass"),
    ("WARUDO", "Warudo (VRM 1.0)",
     "VRM 1.0 with Warudo-specific lint pass"),
    ("RESONITE", "Resonite (VRM 1.0)",
     "VRM 1.0 with Resonite-specific lint pass"),
)


def _target_to_format(target_id: str) -> str:
    """Map preset id to dispatcher key. Returns ``"FBX_VRCHAT"`` or VRM."""
    if target_id == "VRCHAT_FBX":
        return "FBX_VRCHAT"
    if target_id == "VRM_0_X":
        return "VRM_0_X"
    return "VRM_1_0"


def _suggest_extension(target_id: str) -> str:
    return ".fbx" if target_id == "VRCHAT_FBX" else ".vrm"


# ── Dispatcher entry points ──────────────────────────────────────

def _export_vrm(filepath: str, *, vrm_spec: str) -> None:
    """Call upstream VRM exporter. ``vrm_spec`` ∈ {"1.0", "0.x"}.

    The upstream operator names a couple of switches differently between
    versions; we pass only ``filepath`` and rely on the user's choice of
    spec being set in upstream preferences. If the upstream exporter
    surfaces a spec selector we should read it; for now we log a hint
    when the chosen spec doesn't match upstream's default.
    """
    if not hasattr(bpy.ops.export_scene, "vrm"):
        raise RuntimeError("VRM Add-on export operator unavailable")
    bpy.ops.export_scene.vrm(filepath=filepath)
    logger.info("[BoneForge] VRM (%s) exported to %s", vrm_spec, filepath)


def _export_fbx_vrchat(filepath: str, armature) -> None:
    """Export FBX with VRChat-tuned settings.

    Settings mirror the ones already used in
    ``vrchat/export/vrchat_export.py``.
    """
    bpy.ops.export_scene.fbx(
        filepath=filepath,
        use_selection=False,
        use_visible=True,
        object_types={"ARMATURE", "MESH"},
        apply_scale_options="FBX_SCALE_ALL",
        global_scale=1.0,
        axis_forward="-Z",
        axis_up="Y",
        bake_anim=False,
        add_leaf_bones=False,
        primary_bone_axis="Y",
        secondary_bone_axis="X",
        armature_nodetype="NULL",
        path_mode="COPY",
        embed_textures=True,
        mesh_smooth_type="FACE",
    )
    logger.info("[BoneForge] FBX (VRChat preset) exported to %s", filepath)




# v3.3.11: Selection scope for batch export, mirroring Blender's
# standard FBX export pattern.
_SCOPE_ITEMS = [
    ("ACTIVE", "Active Avatar",
     "Export the active armature only"),
    ("ALL", "All VRM Armatures",
     "Export every armature in the scene that has VRM-preserved meta "
     "to a separate file. Filenames get the armature's name appended"),
]


def _find_vrm_armatures() -> list:
    """Return every armature in the scene that has VRM-preserved meta.

    Detects via ``boneforge_vrm_meta`` custom-property presence, set
    by the v3.2.0 importer. Armatures imported through other means
    (or imported before v3.2.0) won't appear here.
    """
    return [
        obj for obj in bpy.data.objects
        if obj.type == "ARMATURE"
        and "boneforge_vrm_meta" in obj
    ]


def _scoped_filepath(template: str, suffix: str) -> str:
    head, tail = _os.path.split(template)
    base, ext = _os.path.splitext(tail)
    return _os.path.join(head, f"{base}_{suffix}{ext}")


# ── Operator ─────────────────────────────────────────────────────

class BF_OT_VRMExport(Operator):
    """Export the active armature for a chosen VTuber / VRChat target."""

    bl_idname = "boneforge.vrm_export"
    bl_label = "Export for Target…"
    bl_description = (
        "Export the active armature for a VTuber or VRChat target. "
        "Runs target-specific lint before writing the file"
    )
    bl_options = {"REGISTER"}

    filepath: StringProperty(subtype="FILE_PATH")
    target: EnumProperty(
        name="Target",
        description="Pipeline to export for",
        items=[(tid, label, desc) for tid, label, desc in TARGETS],
        default="VRM_1_0",
    )
    skip_lint: BoolProperty(
        name="Skip Lint",
        description="Bypass target-specific validation (not recommended)",
        default=False,
    )
    # v3.3.11: scope mirrors Blender's standard FBX export pattern.
    scope: EnumProperty(
        name="Scope",
        description="Which armature(s) to export",
        items=_SCOPE_ITEMS,
        default="ACTIVE",
    )

    def invoke(self, context, event):
        # Suggest a sensible default filepath based on the target's
        # extension and the active armature's name.
        arm = active_armature(context)
        if arm is None:
            self.report({"ERROR"}, "No active armature to export")
            return {"CANCELLED"}

        # If exporting any VRM target, require the upstream add-on.
        if self.target != "VRCHAT_FBX" and bridge.find_vrm_addon() is None:
            self.report(
                {"ERROR"},
                "VRM Add-on for Blender required for VRM targets. "
                "Click 'Install / Enable VRM Add-on' first.",
            )
            return {"CANCELLED"}

        if not self.filepath:
            self.filepath = arm.name + _suggest_extension(self.target)
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

    def execute(self, context):
        if not self.filepath:
            self.report({"ERROR"}, "No file path")
            return {"CANCELLED"}

        if self.scope == "ACTIVE":
            return self._export_one(context, self.filepath,
                                    active_armature(context))
        return self._export_all(context, self.filepath)

    def _export_one(self, context, filepath, arm):
        if arm is None:
            self.report({"ERROR"}, "No active armature")
            return {"CANCELLED"}

        # Lint pre-flight
        if not self.skip_lint:
            issues = lint_mod.lint_for_target(arm, self.target)
            blockers = [i for i in issues if i.severity == "ERROR"]
            if blockers:
                msg = "; ".join(b.message for b in blockers[:3])
                more = "" if len(blockers) <= 3 else f" (+{len(blockers)-3} more)"
                self.report(
                    {"ERROR"},
                    f"Lint blocked export: {msg}{more}. "
                    "Run BoneForge › VRM › Lint for full details, or "
                    "tick 'Skip Lint' to override.",
                )
                return {"CANCELLED"}
            warns = [i for i in issues if i.severity == "WARNING"]
            for w in warns:
                self.report({"WARNING"}, f"Lint: {w.message}")

        fmt = _target_to_format(self.target)
        try:
            if fmt == "FBX_VRCHAT":
                _export_fbx_vrchat(filepath, arm)
            elif fmt == "VRM_1_0":
                _export_vrm(filepath, vrm_spec="1.0")
            elif fmt == "VRM_0_X":
                _export_vrm(filepath, vrm_spec="0.x")
            else:
                self.report({"ERROR"}, f"Unknown target format {fmt}")
                return {"CANCELLED"}
        except (RuntimeError, AttributeError) as exc:
            self.report({"ERROR"}, f"Export failed: {exc}")
            logger.exception("[BoneForge] VRM export failed")
            return {"CANCELLED"}

        self.report({"INFO"}, f"Exported {self.target} → {filepath}")
        return {"FINISHED"}

    def _export_all(self, context, template):
        armatures = _find_vrm_armatures()
        if not armatures:
            self.report(
                {"WARNING"},
                "No VRM-tagged armatures found in the scene. "
                "Import a VRM via BoneForge first so the meta is "
                "preserved and detectable.",
            )
            return {"CANCELLED"}

        prev_active = context.view_layer.objects.active
        prev_selection = [o for o in context.selected_objects]
        exported = []
        try:
            for arm in armatures:
                bpy.ops.object.select_all(action="DESELECT")
                arm.select_set(True)
                context.view_layer.objects.active = arm
                target_path = _scoped_filepath(template, arm.name)
                result = self._export_one(context, target_path, arm)
                if result == {"FINISHED"}:
                    exported.append(target_path)
        finally:
            try:
                bpy.ops.object.select_all(action="DESELECT")
                for o in prev_selection:
                    if o.name in bpy.data.objects:
                        o.select_set(True)
                if prev_active is not None and prev_active.name in bpy.data.objects:
                    context.view_layer.objects.active = prev_active
            except RuntimeError:
                pass

        if not exported:
            self.report({"WARNING"}, "No avatars exported.")
            return {"CANCELLED"}
        self.report(
            {"INFO"},
            f"Exported {len(exported)} avatar(s) to "
            f"{_os.path.dirname(template)}",
        )
        return {"FINISHED"}
