"""BoneForge shared-tool layout, adapted from BoneCraft for standard Blender.

Rig Builder: manual-marker wizard, existing Quick Rig library, Mannequin.
BoneForge: project overview, rig setup, weights/correctives and review tools.
CATS: cleanup, Avatar Tools, VRChat Tools and Import / Export.

Panel identifiers remain stable. Menus and Scene Properties mirrors reference
only BoneForge's existing tools; no BoneCraft-exclusive features are loaded.
"""

import bpy
from bpy.types import Panel

import logging
from boneforge.i18n import T

logger = logging.getLogger(__name__)

# -- Constants -------------------------------------------------

_SPACE    = 'VIEW_3D'
_REGION   = 'UI'
_CAT      = 'BoneForge'
_CATS_CAT = 'CATS'

_RB_CAT = 'Rig Builder'


# -- Helpers ---------------------------------------------------

# =============================================================
# Confession Layer — H6 + A1 (Brainstorm Council)
#
# Classifies the active pose bone by jurisdiction and shows one
# plain-language sentence explaining what it is and how to use it.
# On first access for each armature a mapping is built and cached;
# subsequent draws are a dict lookup only.
# =============================================================

_confession_cache: dict = {}  # armature_name -> {fingerprint, bone_map}


def _build_confession_bone_map(arm_obj) -> dict:
    """Build bone classification map for a generated Rigify rig.

    Returns {bone_name: {jurisdiction, ctrl_name, orphaned, ik_fk_prop}}.

    jurisdiction values:
      CONTROL    — animator-facing controller (custom shape present)
      DEFORM     — DEF- prefix: driven by a controller
      PASSTHROUGH— MCH-/ORG-: internal mechanism, no user-facing role
      UNKNOWN    — no prefix and no custom shape (root, pivot, legacy)
    """
    all_names = {b.name for b in arm_obj.data.bones}
    pose_bones = arm_obj.pose.bones
    bone_map: dict = {}

    for bone in arm_obj.data.bones:
        name = bone.name
        pb = pose_bones.get(name)

        if name.startswith("DEF-"):
            base = name[4:]
            ctrl_name = None
            for candidate in (base, f"{base}.ctl", f"ctrl.{base}"):
                if candidate in all_names and not candidate.startswith(
                    ("DEF-", "MCH-", "ORG-")
                ):
                    ctrl_name = candidate
                    break
            if ctrl_name is None:
                base_clean = base.rstrip(".0123456789")
                for n in all_names:
                    if n.startswith(("DEF-", "MCH-", "ORG-")):
                        continue
                    if n.rstrip(".0123456789") == base_clean:
                        ctrl_name = n
                        break
            # A1 — Orphan Signal
            orphaned = (ctrl_name is not None) and (ctrl_name not in all_names)
            bone_map[name] = {
                "jurisdiction": "DEFORM",
                "ctrl_name": ctrl_name,
                "orphaned": orphaned,
                "ik_fk_prop": None,
            }

        elif name.startswith(("MCH-", "ORG-")):
            bone_map[name] = {
                "jurisdiction": "PASSTHROUGH",
                "ctrl_name": None,
                "orphaned": False,
                "ik_fk_prop": None,
            }

        else:
            has_custom_shape = pb is not None and pb.custom_shape is not None
            ik_fk_prop = None
            if pb is not None:
                for prop_key in ("ik_fk_switch", "IK_FK", "ik_fk", "IK/FK"):
                    if prop_key in pb.keys():
                        ik_fk_prop = prop_key
                        break
            bone_map[name] = {
                "jurisdiction": "CONTROL" if has_custom_shape else "UNKNOWN",
                "ctrl_name": None,
                "orphaned": False,
                "ik_fk_prop": ik_fk_prop,
            }

    return bone_map


def _get_confession_bone_map(arm_obj) -> dict:
    """Return cached bone map, rebuilding when bone count changes."""
    key = arm_obj.name
    fingerprint = len(arm_obj.data.bones)
    cached = _confession_cache.get(key)
    if cached is None or cached["fingerprint"] != fingerprint:
        bone_map = _build_confession_bone_map(arm_obj)
        _confession_cache[key] = {"fingerprint": fingerprint, "bone_map": bone_map}
        return bone_map
    return cached["bone_map"]


def _draw_confession_layer(layout, context):
    """Draw the Confession Layer for the active pose bone.

    Shows a plain-language sentence explaining bone jurisdiction.
    When no bone is selected shows an armature-level summary so the
    panel is never blank (idle frame).
    """
    obj = context.active_object
    if obj is None or obj.type != "ARMATURE":
        return

    try:
        from boneforge.autorig.quick_human import _is_generated_rigify_control_rig
    except ImportError:
        return

    if not _is_generated_rigify_control_rig(obj):
        return

    try:
        bone_map = _get_confession_bone_map(obj)
    except Exception:
        layout.label(text="Bone index unavailable.", icon="ERROR")
        return

    box = layout.box()
    col = box.column(align=True)
    col.scale_y = 0.85

    pb = context.active_pose_bone

    if pb is None:
        ctrl_count = sum(
            1 for info in bone_map.values() if info["jurisdiction"] == "CONTROL"
        )
        ik_count = sum(
            1 for info in bone_map.values()
            if info["jurisdiction"] == "CONTROL" and info["ik_fk_prop"] is not None
        )
        total = len(bone_map)
        col.label(text="Enter Pose Mode, select a bone to see its role.",
                  icon="INFO")
        col.separator(factor=0.4)
        col.label(
            text=f"{total} bones  •  {ctrl_count} controllers"
                 f"  •  {ik_count} IK/FK"
        )
        return

    name = pb.name
    info = bone_map.get(
        name,
        {"jurisdiction": "UNKNOWN", "ctrl_name": None, "orphaned": False,
         "ik_fk_prop": None},
    )
    jurisdiction = info["jurisdiction"]

    if jurisdiction == "DEFORM":
        ctrl = info["ctrl_name"]
        if info["orphaned"]:
            col.label(text="DEF bone — follows a controller.",
                      icon="CONSTRAINT_BONE")
            col.label(text=f"Expected: \"{ctrl}\"")
            col.label(text="— but that control is missing from this rig.")
        elif ctrl:
            col.label(text="DEF bone — follows its controller.",
                      icon="CONSTRAINT_BONE")
            col.label(text=f"Select \"{ctrl}\" to pose this part.")
        else:
            col.label(text="DEF bone — driven by a controller.",
                      icon="CONSTRAINT_BONE")
            col.label(text="Find and select its control bone to pose.")

    elif jurisdiction == "PASSTHROUGH":
        prefix = "MCH" if name.startswith("MCH-") else "ORG"
        col.label(text=f"{prefix} bone — internal mechanism.",
                  icon="DRIVER")
        col.label(text="Not for direct animation.")
        col.label(text="Deselect and select a controller instead.")

    elif jurisdiction == "CONTROL":
        ik_fk_prop = info["ik_fk_prop"]
        if ik_fk_prop is not None:
            try:
                val = float(pb[ik_fk_prop])
                mode = "IK" if val < 0.5 else "FK"
                col.label(text=f"Controller — {mode} mode.",
                          icon="CON_KINEMATIC")
                if mode == "IK":
                    col.label(text="Move/rotate this bone; the chain follows.")
                    col.label(text=f"Switch to FK: set \"{ik_fk_prop}\" → 1.0")
                else:
                    col.label(text="Rotate each joint independently.")
                    col.label(text=f"Switch to IK: set \"{ik_fk_prop}\" → 0.0")
            except (KeyError, TypeError, ValueError):
                col.label(text="Controller bone — grab/rotate to pose.",
                          icon="CON_KINEMATIC")
        else:
            col.label(text="Controller bone — grab/rotate to pose.",
                      icon="CON_KINEMATIC")
            col.label(text="This drives the rig's deform bones.")

    else:
        col.label(text="No declared role for this bone.", icon="QUESTION")
        col.label(text="May be a root, pivot, or legacy control.")
        col.label(text="Treat as uncharted — test before keying.")


def _delegate_draw(self, context, import_path: str, class_name: str):
    """Draw an existing panel with its own helper methods."""
    from boneforge.core.ui_layout import PanelDrawTarget
    from boneforge.core.tool_registry import get_registry
    package = import_path.split(".")[1]
    tool_id = {"autorig": "phase3_autorig", "animation": "phase2_animation",
               "weights": "phase2b_weights", "advanced_rigging": "phase2c_advanced",
               "vrchat": "vrchat_avatar"}.get(package)
    if tool_id and not get_registry().is_enabled(tool_id):
        self.layout.label(text=T("Enable the matching tool package in preferences."), icon='INFO')
        return
    try:
        module = __import__(import_path, fromlist=[class_name])
        panel = getattr(module, class_name)
        panel.draw(PanelDrawTarget(panel, self.layout), context)
    except ImportError:
        self.layout.label(text=T("Enable the matching tool package in preferences."), icon='INFO')
    except AttributeError as exc:
        logger.debug("[BoneForge] unavailable panel %s: %s", class_name, exc)
        self.layout.label(text=T("Enable the matching tool package in preferences."), icon='INFO')
    except Exception as exc:
        logger.warning("[BoneForge Sidebar] draw error in %s: %s", class_name, exc)
        self.layout.label(text=T("Draw error -- see console"), icon='ERROR')


def _draw_explainer(layout, context, line1, line2=None):
    """Width-aware help, omitted in Compact Mode."""
    if getattr(context.scene, "boneforge_vrc_compact_mode", False):
        return
    from boneforge.core.ui_layout import draw_wrapped
    col = layout.box().column(align=True)
    col.scale_y = 0.85
    draw_wrapped(col, context, T(line1), icon='INFO')
    if line2:
        draw_wrapped(col, context, T(line2))


# =============================================================
# HUB: Overview / Project Strip  (order=-1000)
# Always visible when an avatar armature is in context.
# Shows the active avatar name; Task Board + Rig Notes are children.
# =============================================================

class BF_PT_sb_overview(Panel):
    """BoneForge -> Overview hub: project strip, Task Board, Rig Notes.

    Sits at order=-1000 so it dominates the BoneForge tab. Acts as a
    persistent project strip — avatar name, quick health, and notes —
    rather than a navigation hub. Task Board and Rig Notes are children
    registered by panel.py and here respectively.
    """
    bl_label       = " "
    bl_idname      = "BF_PT_sb_overview"
    bl_space_type  = _SPACE
    bl_region_type = _REGION
    bl_category    = _CAT
    bl_order       = -1000

    def draw_header(self, context):
        self.layout.label(text=T("Overview"))

    @classmethod
    def poll(cls, context):
        try:
            prefs = context.preferences.addons["boneforge"].preferences
            if not prefs.show_tab_boneforge:
                return False
        except Exception:
            pass
        from boneforge.core import find_avatar_armature
        return find_avatar_armature(context) is not None

    def draw(self, context):
        from boneforge.core import find_avatar_armature
        arm = find_avatar_armature(context)
        if arm is None:
            return
        row = self.layout.row(align=True)
        row.label(text=arm.name, icon='ARMATURE_DATA')
        row.label(text=T("Active"), icon='CHECKMARK')


class BF_PT_sb_rig_notes(Panel):
    """Rig notes / README — advanced_rigging. Child of Overview."""
    bl_label       = " "
    bl_idname      = "BF_PT_sb_rig_notes"
    bl_space_type  = _SPACE
    bl_region_type = _REGION
    bl_category    = _CAT
    bl_parent_id   = "BF_PT_sb_overview"
    bl_options     = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.label(text=T("Rig Notes"))

    @classmethod
    def poll(cls, context):
        from boneforge.core import find_avatar_armature
        return find_avatar_armature(context) is not None

    def draw(self, context):
        _delegate_draw(self, context,
                       "boneforge.advanced_rigging.rig_notes",
                       "BONEFORGE_PT_p2c_rig_notes")


# =============================================================
# TAB: Rig Builder — unchanged, creation workflows only.
# =============================================================

class BF_PT_rb_setup(Panel):
    """Rig Builder -> Setup hub: Quick Rig, Auto-Rig Wizard, Mannequin."""
    bl_label       = " "
    bl_idname      = "BF_PT_rb_setup"
    bl_space_type  = _SPACE
    bl_region_type = _REGION
    bl_category    = _RB_CAT
    bl_order       = 0

    def draw_header(self, context):
        self.layout.label(text=T("Rig Builder"))

    @classmethod
    def poll(cls, context):
        try:
            prefs = context.preferences.addons["boneforge"].preferences
            if not prefs.show_tab_rig_builder:
                return False
        except Exception:
            pass
        from boneforge.core.tool_registry import get_registry
        return get_registry().is_enabled("phase3_autorig")

    def draw(self, context):
        layout = self.layout
        if context.active_object is None or context.active_object.type not in {'ARMATURE', 'MESH'}:
            layout.label(
                text=T("Pick a rig source below to start."),
                icon='INFO',
            )


# =============================================================
# HUB: Setup Rigging  (order=10)
# =============================================================

class BF_PT_sb_setup(Panel):
    """BoneForge -> Setup hub: retarget, Rigify config."""
    bl_label       = " "
    bl_idname      = "BF_PT_sb_setup"
    bl_space_type  = _SPACE
    bl_region_type = _REGION
    bl_category    = _CAT
    bl_order       = 10

    def draw_header(self, context):
        self.layout.label(text=T("Setup Rigging"))

    @classmethod
    def poll(cls, context):
        try:
            prefs = context.preferences.addons["boneforge"].preferences
            if not prefs.show_tab_boneforge:
                return False
        except Exception:
            pass
        return True

    def draw(self, context):
        obj = context.active_object
        if obj is None or obj.type != 'ARMATURE':
            self.layout.label(
                text=T("Select an armature to see Retarget and Rigify Tools."),
                icon='INFO',
            )
            return
        box = self.layout.box()
        col = box.column(align=True)
        col.scale_y = 0.75
        col.label(text=T("Tools for rigs you already have."), icon='INFO')
        col.label(text=T("Use Rig Builder tab to create a new rig."))


class BF_PT_sb_quick_rig(Panel):
    """Premade Quick Rig library — Rig Builder tab."""
    bl_label       = " "
    bl_order       = 2
    bl_idname      = "BF_PT_sb_quick_rig"
    bl_space_type  = _SPACE
    bl_region_type = _REGION
    bl_category    = _RB_CAT
    bl_parent_id   = "BF_PT_rb_setup"

    def draw_header(self, context):
        self.layout.label(text=T("Quick Rig - premade armatures"))

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout

        from boneforge.autorig.quick_human import (
            discover_rigify_metarigs,
            FALLBACK_OP_ID,
        )

        scene = context.scene

        col = layout.column(align=True)

        # Guard: scene may be None in headless/background render contexts.
        if scene is None:
            col.label(text="No active scene.", icon='ERROR')
            return

        # Safe accessors — fall back to sane defaults if scene props are not
        # yet registered (e.g. autorig module still loading on first draw).
        def _sp(name, default):
            v = getattr(scene, name, None)
            return v if v is not None else default

        rigify_rigs = discover_rigify_metarigs()

        groups = {"humans": [], "quadrupeds": [], "other": [], "unknown": []}
        for rig_descriptor in rigify_rigs:
            groups[rig_descriptor["group"]].append(rig_descriptor)

        if rigify_rigs:
            col.label(text=f"Rigify metarigs ({len(rigify_rigs)}):",
                      icon='OUTLINER_OB_ARMATURE')
            for group_key, group_label in (
                ("humans", "Humans"),
                ("quadrupeds", "Quadrupeds"),
                ("other", "Other"),
                ("unknown", "Other"),
            ):
                try:
                    self._draw_group(col, groups[group_key], group_label, scene, context)
                except Exception as exc:
                    logger.exception(
                        "[BoneForge] Quick Rig %s group draw failed",
                        group_key,
                    )
                    col.label(
                        text=f"[{group_label} group failed: {exc}]",
                        icon='ERROR',
                    )
        else:
            enable_box = col.box()
            enable_row = enable_box.row()
            enable_row.scale_y = 1.5
            enable_row.operator(
                "boneforge.enable_rigify",
                text=T("Enable Rigify"),
                icon='ADD',
            )
            enable_box.label(
                text=T("Rigify must be enabled to select Rigify default rigs."),
                icon='INFO',
            )

        col.separator(factor=0.5)
        col.label(text=T("No Rigify required:"), icon='OUTLINER_OB_ARMATURE')
        op = col.operator(
            "boneforge.add_quick_rig",
            text=T("BoneForge Basic Humanoid (19 bones)"),
            icon='ARMATURE_DATA',
        )
        op.rig_op_id = FALLBACK_OP_ID
        op.rig_label = "BoneForge Humanoid"
        op.fit_to_active_mesh    = _sp("boneforge_quick_rig_fit_to_mesh", True)
        op.parent_with_auto_weights = _sp("boneforge_quick_rig_auto_weight", False)
        op.generate_control_rig = False
        op.initial_pose          = _sp("boneforge_quick_rig_initial_pose", 'NONE')

        col.separator()
        if hasattr(col, "panel"):
            header, options = layout.panel("boneforge_quick_rig_options", default_closed=True)
            header.label(text=T("Options"))
        else:
            options = col.box()
            options.label(text=T("Options"))
        if options is not None:
            options.use_property_split = True
            options.use_property_decorate = False
        if options is not None:
            if hasattr(scene, "boneforge_quick_rig_fit_to_mesh"):
                options.prop(scene, "boneforge_quick_rig_fit_to_mesh",
                         text=T("Fit Rig to Active Mesh"),
                         icon='FULLSCREEN_ENTER')
                options.prop(scene, "boneforge_quick_rig_auto_weight",
                         icon='MOD_VERTEX_WEIGHT')
                options.prop(scene, "boneforge_quick_rig_generate_controls",
                         text=T("Add IK/FK Controllers"),
                         icon='CON_KINEMATIC')
                options.prop(scene, "boneforge_quick_rig_initial_pose",
                         text=T("Initial Pose"))
            else:
                options.label(text="Reopen Blender to load rig options.", icon='INFO')

        from boneforge.autorig.quick_human import _is_rigify_metarig
        if _is_rigify_metarig(context.active_object):
            col.separator()
            row = col.row(align=True)
            row.scale_y = 1.2
            row.operator(
                "boneforge.generate_rigify_control_rig",
                text=T("Generate Control Rig (active metarig)"),
                icon='CON_KINEMATIC',
            )
        elif (
            context.active_object is not None
            and context.active_object.type == "ARMATURE"
        ):
            col.separator()
            col.operator(
                "boneforge.inspect_rigify_controls",
                text=T("Inspect Active Rig Controls"),
                icon='VIEWZOOM',
            )

        col.label(
            text=T("Need precise marker placement? Use the Auto-Rig Wizard above."),
            icon='INFO',
        )

        col.separator()
        col.label(text=T("Switch active rig's rest pose:"), icon='POSE_HLT')
        pose_row = col.row(align=True)
        pose_row.scale_y = 1.2
        active_is_armature = (
            context.active_object is not None
            and context.active_object.type == "ARMATURE"
        )
        pose_row.enabled = active_is_armature
        t_pose_op = pose_row.operator(
            "boneforge.set_rest_pose",
            text=T("T-Pose"),
            icon='OUTLINER_OB_ARMATURE',
        )
        t_pose_op.pose_type = "T_POSE"
        a_pose_op = pose_row.operator(
            "boneforge.set_rest_pose",
            text=T("A-Pose"),
            icon='OUTLINER_OB_ARMATURE',
        )
        a_pose_op.pose_type = "A_POSE"
        if not active_is_armature:
            col.label(
                text=T("Select an armature to enable T-Pose / A-Pose."),
                icon='INFO',
            )

        col.separator()
        col.operator(
            "boneforge.diagnose_quick_rig",
            text=T("Diagnose Quick Rig (print to console)"),
            icon='CONSOLE',
        )

    def _draw_group(self, col, rigs, group_label, scene, context):
        """Render two-buttons-per-row grid for a metarig group."""
        if not rigs:
            return
        col.label(text=group_label, icon='BLANK1')
        rig_index = 0
        columns = 1 if getattr(getattr(context, "region", None), "width", 300) < 360 else 2
        while rig_index < len(rigs):
            row = col.row(align=True)
            for column_index in range(columns):
                descriptor_index = rig_index + column_index
                if descriptor_index >= len(rigs):
                    row.label(text="")
                    continue
                rig_descriptor = rigs[descriptor_index]
                try:
                    op = row.operator(
                        "boneforge.add_quick_rig",
                        text=rig_descriptor["label"],
                        icon='OUTLINER_OB_ARMATURE',
                    )
                    op.rig_op_id = rig_descriptor["op_id"]
                    op.rig_label = rig_descriptor["label"]
                    op.fit_to_active_mesh = getattr(
                        scene, "boneforge_quick_rig_fit_to_mesh", True)
                    op.parent_with_auto_weights = getattr(
                        scene, "boneforge_quick_rig_auto_weight", False)
                    op.generate_control_rig = getattr(
                        scene, "boneforge_quick_rig_generate_controls", False)
                    op.initial_pose = getattr(
                        scene, "boneforge_quick_rig_initial_pose", 'NONE')
                except Exception as exc:
                    logger.exception(
                        "[BoneForge] Quick Rig button render failed: %s",
                        rig_descriptor,
                    )
                    row.label(
                        text=f"[{rig_descriptor.get('rig_name', '?')} "
                             f"failed: {exc}]",
                        icon='ERROR',
                    )
            rig_index += columns


class BF_PT_sb_wizard(Panel):
    """Auto-Rig Wizard — Rig Builder tab."""
    bl_label       = " "
    bl_order       = 1
    bl_idname      = "BF_PT_sb_wizard"
    bl_space_type  = _SPACE
    bl_region_type = _REGION
    bl_category    = _RB_CAT
    bl_parent_id   = "BF_PT_rb_setup"

    def draw_header(self, context):
        self.layout.label(text=T("Auto-Rig Wizard"))

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        _delegate_draw(self, context,
                       "boneforge.autorig.wizard",
                       "BF_PT_WizardPanel")


class BF_PT_rb_mannequin(Panel):
    """Mannequin generation — Rig Builder tab."""
    bl_label       = " "
    bl_order       = 3
    bl_idname      = "BF_PT_rb_mannequin"
    bl_space_type  = _SPACE
    bl_region_type = _REGION
    bl_category    = _RB_CAT
    bl_parent_id   = "BF_PT_rb_setup"

    def draw_header(self, context):
        self.layout.label(text=T("Mannequin"))

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        _delegate_draw(self, context,
                       "boneforge.autorig.mannequin",
                       "BF_PT_MannequinPanel")


class BF_PT_sb_retarget(Panel):
    """Retarget panel — autorig. Child of Setup Rigging."""
    bl_label       = " "
    bl_idname      = "BF_PT_sb_retarget"
    bl_space_type  = _SPACE
    bl_region_type = _REGION
    bl_category    = _CAT
    bl_parent_id   = "BF_PT_sb_setup"
    bl_options     = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.label(text=T("Retarget"))

    @classmethod
    def poll(cls, context):
        return (
            context.active_object is not None
            and context.active_object.type == 'ARMATURE'
        )

    def draw(self, context):
        _draw_explainer(
            self.layout, context,
            "Remaps animation data from one armature to another.",
            "Use when applying animations built for a different skeleton.",
        )
        _delegate_draw(self, context,
                       "boneforge.autorig.retarget",
                       "BF_PT_RetargetPanel")


class BF_PT_sb_rigify(Panel):
    """Rigify enhancement — animation. Child of Setup Rigging."""
    bl_label       = " "
    bl_idname      = "BF_PT_sb_rigify"
    bl_space_type  = _SPACE
    bl_region_type = _REGION
    bl_category    = _CAT
    bl_parent_id   = "BF_PT_sb_setup"
    bl_options     = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.label(text=T("Rigify Tools"))

    @classmethod
    def poll(cls, context):
        return (
            context.active_object is not None
            and context.active_object.type == 'ARMATURE'
        )

    def draw(self, context):
        _draw_explainer(
            self.layout, context,
            "Enhance and manage Rigify-generated control rigs.",
            "Use after generating a Rigify rig to access BoneForge enhancements.",
        )
        _delegate_draw(self, context,
                       "boneforge.animation.rigify_enhance",
                       "BF_PT_RigifyEnhancePanel")


# =============================================================
# HUB: Skin  (order=20)
# =============================================================

class BF_PT_sb_skin(Panel):
    """BoneForge -> Skin hub: weights and corrective shapes."""
    bl_label       = " "
    bl_idname      = "BF_PT_sb_skin"
    bl_space_type  = _SPACE
    bl_region_type = _REGION
    bl_category    = _CAT
    bl_order       = 20

    def draw_header(self, context):
        self.layout.label(text=T("Skin"))

    @classmethod
    def poll(cls, context):
        try:
            prefs = context.preferences.addons["boneforge"].preferences
            if not prefs.show_tab_boneforge:
                return False
        except Exception:
            pass
        obj = context.active_object
        return obj is not None and obj.type in {'ARMATURE', 'MESH'}

    def draw(self, context):
        obj = context.active_object
        layout = self.layout
        layout.label(
            text=obj.name if obj else "No object selected",
            icon='MOD_VERTEX_WEIGHT',
        )
        box = layout.box()
        col = box.column(align=True)
        col.scale_y = 0.75
        col.label(text=T("Paint weights and fix mesh deformation."), icon='INFO')
        col.label(text=T("Expand a section below to get started."))


class BF_PT_sb_weights(Panel):
    """Weight tools — weights. Child of Skin."""
    bl_label       = " "
    bl_idname      = "BF_PT_sb_weights"
    bl_space_type  = _SPACE
    bl_region_type = _REGION
    bl_category    = _CAT
    bl_parent_id   = "BF_PT_sb_skin"
    bl_options     = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.label(text=T("Weight Tools"))

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type in {'ARMATURE', 'MESH'}

    def draw(self, context):
        layout = self.layout
        _draw_explainer(
            layout, context,
            "Paint and adjust vertex weights that control mesh deformation.",
            "Use when the mesh pinches, collapses, or moves wrong during posing.",
        )
        from boneforge.weights.weight_tools import draw_automatic_weight_recalculation
        draw_automatic_weight_recalculation(layout, context)
        for module_path, class_name in (
            ("boneforge.weights.weight_tools",    "BONEFORGE_PT_p2b_flood_fill"),
            ("boneforge.weights.weight_transfer", "BONEFORGE_PT_p2b_weight_transfer"),
            ("boneforge.weights.weight_mirror",   "BONEFORGE_PT_p2b_weight_mirror"),
            ("boneforge.weights.weight_table",    "BONEFORGE_PT_p2b_weight_table"),
            ("boneforge.weights.deform_control",  "BONEFORGE_PT_p2b_deform_control"),
        ):
            layout.separator(factor=0.3)
            _delegate_draw(self, context, module_path, class_name)


class BF_PT_sb_correctives(Panel):
    """Corrective shape keys — animation. Child of Skin."""
    bl_label       = " "
    bl_idname      = "BF_PT_sb_correctives"
    bl_space_type  = _SPACE
    bl_region_type = _REGION
    bl_category    = _CAT
    bl_parent_id   = "BF_PT_sb_skin"
    bl_options     = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.label(text=T("Correctives"))

    @classmethod
    def poll(cls, context):
        return (
            context.active_object is not None
            and context.active_object.type == 'ARMATURE'
        )

    def draw(self, context):
        _draw_explainer(
            self.layout, context,
            "Add corrective shape keys that fix deformation at specific poses.",
            "Use after weight painting to clean up stubborn problem areas at joints.",
        )
        _delegate_draw(self, context,
                       "boneforge.animation.correctives",
                       "BF_PT_CorrectivesPanel")


# =============================================================
# HUB: VRChat  (order=35)
# 3 clusters communicated through panel naming and explainer text:
#   A — VRChat Setup (panels ordered 1-2)
#   B — Body & Physics (panels ordered 4-6)
#   C — Finalize     (panels ordered 7-8)
# =============================================================

class BF_PT_sb_vrchat(Panel):
    """Shared avatar setup and physics tools."""
    bl_label = " "
    bl_idname = "BF_PT_sb_vrchat"
    bl_space_type = _SPACE
    bl_region_type = _REGION
    bl_category = _CATS_CAT
    bl_order = 35

    def draw_header(self, context):
        self.layout.label(text=T("Avatar Tools"))

    @classmethod
    def poll(cls, context):
        from boneforge.core.prefs import addon_prefs
        prefs = addon_prefs(context)
        from boneforge.core.tool_registry import get_registry
        return (prefs is None or prefs.show_tab_cats) and get_registry().is_enabled("vrchat_avatar")

    def draw(self, context):
        from boneforge.core.ui_layout import draw_wrapped
        layout = self.layout
        obj = context.active_object
        if obj is None or obj.type not in {'ARMATURE', 'MESH'}:
            draw_wrapped(layout, context, T("Select an armature or mesh to use avatar tools."), icon='INFO')
            return
        draw_wrapped(layout, context, obj.name, icon='COMMUNITY')
        layout.prop(context.scene, "boneforge_vrc_compact_mode", text=T("Compact Mode"))
        _draw_explainer(layout, context, "Humanoid bones, hair physics, visemes and avatar export.",
                        "Naming, clothing and performance are in VRChat Tools.")


class BF_PT_cats_vrc_tools(Panel):
    """Shared naming, clothing and performance sections."""
    bl_label = " "
    bl_idname = "BF_PT_cats_vrc_tools"
    bl_space_type = _SPACE
    bl_region_type = _REGION
    bl_category = _CATS_CAT
    bl_order = 36
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.label(text=T("VRChat Tools"))

    @classmethod
    def poll(cls, context):
        from boneforge.core.prefs import addon_prefs
        prefs = addon_prefs(context)
        from boneforge.core.tool_registry import get_registry
        return (prefs is None or prefs.show_tab_cats) and get_registry().is_enabled("vrchat_avatar")

    def draw(self, context):
        from boneforge.core.ui_layout import draw_wrapped
        obj = context.active_object
        if obj is None or obj.type not in {'ARMATURE', 'MESH'}:
            draw_wrapped(self.layout, context, T("Select an armature or mesh to use avatar tools."), icon='INFO')
        else:
            _draw_explainer(self.layout, context, "Naming, clothing and performance tools for your avatar.")


# ── Cluster A — VRChat Setup ───────────────────────────────────

class BF_PT_sb_vrc_naming(Panel):
    """Bone naming: convention presets, batch rename, detection."""
    bl_label       = " "
    bl_idname      = "BF_PT_sb_vrc_naming"
    bl_space_type  = _SPACE
    bl_region_type = _REGION
    bl_category    = _CATS_CAT
    bl_parent_id   = "BF_PT_cats_vrc_tools"
    bl_order       = 4
    bl_options     = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.label(text=T("VRChat Naming Extras"))

    @classmethod
    def poll(cls, context):
        return (
            context.active_object is not None
            and context.active_object.type == 'ARMATURE'
        )

    def draw(self, context):
        layout = self.layout
        _draw_explainer(
            layout, context,
            "Renames your armature bones to the format VRChat requires.",
            "Run after rig structure is finalized — before Set Up Humanoid Bones.",
        )
        for module_path, class_name in (
            ("boneforge.vrchat.naming.presets",      "BONEFORGE_PT_vrc_naming_presets"),
            ("boneforge.vrchat.naming.batch_rename", "BONEFORGE_PT_vrc_batch_rename"),
            ("boneforge.vrchat.naming.detector",     "BONEFORGE_PT_vrc_naming_detect"),
        ):
            layout.separator(factor=0.3)
            _delegate_draw(self, context, module_path, class_name)


class BF_PT_sb_vrc_humanoid(Panel):
    """Humanoid bone mapping, validator, and eye bone setup."""
    bl_label       = " "
    bl_idname      = "BF_PT_sb_vrc_humanoid"
    bl_space_type  = _SPACE
    bl_region_type = _REGION
    bl_category    = _CATS_CAT
    bl_parent_id   = "BF_PT_sb_vrchat"
    bl_order       = 2
    bl_options     = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.label(text=T("Set Up Humanoid Bones"))

    @classmethod
    def poll(cls, context):
        return (
            context.active_object is not None
            and context.active_object.type == 'ARMATURE'
        )

    def draw(self, context):
        layout = self.layout
        _draw_explainer(
            layout, context,
            "Maps your bones to VRChat's humanoid avatar definition.",
            "Required for IK, locomotion, and full-body tracking to work.",
        )
        for module_path, class_name in (
            ("boneforge.vrchat.humanoid.mapper",    "BONEFORGE_PT_vrc_humanoid"),
            ("boneforge.vrchat.humanoid.validator", "BONEFORGE_PT_vrc_humanoid_validator"),
            ("boneforge.vrchat.humanoid.eye_setup", "BONEFORGE_PT_vrc_eye_setup"),
        ):
            layout.separator(factor=0.3)
            _delegate_draw(self, context, module_path, class_name)


# ── Cluster B — Body & Physics ─────────────────────────────────

class BF_PT_sb_vrc_hair(Panel):
    """Hair physics: chain detection, generation, PhysBone, colliders."""
    bl_label       = " "
    bl_idname      = "BF_PT_sb_vrc_hair"
    bl_space_type  = _SPACE
    bl_region_type = _REGION
    bl_category    = _CATS_CAT
    bl_parent_id   = "BF_PT_sb_vrchat"
    bl_order       = 4
    bl_options     = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.label(text=T("Add Hair Physics"))

    @classmethod
    def poll(cls, context):
        return (
            context.active_object is not None
            and context.active_object.type == 'ARMATURE'
        )

    def draw(self, context):
        layout = self.layout
        _draw_explainer(
            layout, context,
            "Sets up PhysBone chains on hair, ears, tails, or accessories.",
            "Run after Set Up Humanoid Bones. Skip if avatar has no dynamic parts.",
        )
        for module_path, class_name in (
            ("boneforge.vrchat.hair.detector",  "BONEFORGE_PT_vrc_hair_detect"),
            ("boneforge.vrchat.hair.generator", "BONEFORGE_PT_vrc_hair_generator"),
            ("boneforge.vrchat.hair.physbone",  "BONEFORGE_PT_vrc_physbone"),
            ("boneforge.vrchat.hair.collision", "BONEFORGE_PT_vrc_colliders"),
        ):
            layout.separator(factor=0.3)
            _delegate_draw(self, context, module_path, class_name)


class BF_PT_sb_vrc_clothing(Panel):
    """Clothing: bone match, collision detection, merge workflow."""
    bl_label       = " "
    bl_idname      = "BF_PT_sb_vrc_clothing"
    bl_space_type  = _SPACE
    bl_region_type = _REGION
    bl_category    = _CATS_CAT
    bl_parent_id   = "BF_PT_cats_vrc_tools"
    bl_order       = 2
    bl_options     = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.label(text=T("Attach Clothing"))

    @classmethod
    def poll(cls, context):
        return (
            context.active_object is not None
            and context.active_object.type == 'ARMATURE'
        )

    def draw(self, context):
        layout = self.layout
        _draw_explainer(
            layout, context,
            "Merges clothing meshes to the skeleton and transfers bone weights.",
            "Run after weight painting the base body in the Skin tab.",
        )
        for module_path, class_name in (
            ("boneforge.vrchat.clothing.collision",  "BONEFORGE_PT_vrc_collision"),
            ("boneforge.vrchat.clothing.merge",      "BONEFORGE_PT_vrc_clothing_merge"),
        ):
            layout.separator(factor=0.3)
            _delegate_draw(self, context, module_path, class_name)


class BF_PT_sb_vrc_visemes(Panel):
    """VRChat viseme mapping and SteamVR face tracking setup."""
    bl_label       = " "
    bl_idname      = "BF_PT_sb_vrc_visemes"
    bl_space_type  = _SPACE
    bl_region_type = _REGION
    bl_category    = _CATS_CAT
    bl_parent_id   = "BF_PT_cats_vrc_tools"
    bl_order       = 3
    bl_options     = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.label(text=T("Facial"))

    @classmethod
    def poll(cls, context):
        return (
            context.active_object is not None
            and context.active_object.type == 'ARMATURE'
        )

    def draw(self, context):
        layout = self.layout
        _draw_explainer(
            layout, context,
            "Generates blend shapes VRChat drives from your mic for lip sync.",
            "Requires existing blend shapes on your mesh. Skip if no lip sync needed.",
        )
        for module_path, class_name in (
            ("boneforge.vrchat.visemes.vrchat_mapper", "BONEFORGE_PT_vrc_viseme_mapper"),
            ("boneforge.vrchat.visemes.face_tracking", "BONEFORGE_PT_vrc_face_tracking"),
        ):
            layout.separator(factor=0.3)
            _delegate_draw(self, context, module_path, class_name)


# ── Cluster C — Finalize ───────────────────────────────────────

class BF_PT_sb_vrc_perf(Panel):
    """VRChat performance: rank check, optimizer, poly decimation."""
    bl_label       = " "
    bl_idname      = "BF_PT_sb_vrc_perf"
    bl_space_type  = _SPACE
    bl_region_type = _REGION
    bl_category    = _CATS_CAT
    bl_parent_id   = "BF_PT_cats_vrc_tools"
    bl_order       = 1
    bl_options     = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.label(text=T("Check Performance"))

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type in {'ARMATURE', 'MESH'}

    def draw(self, context):
        layout = self.layout
        _draw_explainer(
            layout, context,
            "Measures your avatar against VRChat's performance tiers (Excellent-Very Poor).",
            "Shows what's costing you rank. Run before Export.",
        )
        for module_path, class_name in (
            ("boneforge.vrchat.performance.rank",       "BONEFORGE_PT_vrc_performance"),
            ("boneforge.vrchat.performance.optimizer",  "BONEFORGE_PT_vrc_optimizer"),
            ("boneforge.vrchat.performance.decimation", "BONEFORGE_PT_vrc_decimation"),
        ):
            layout.separator(factor=0.3)
            _delegate_draw(self, context, module_path, class_name)


class BF_PT_sb_vrc_export(Panel):
    """VRChat export: FBX to Unity + sidecar generation."""
    bl_label       = " "
    bl_idname      = "BF_PT_sb_vrc_export"
    bl_space_type  = _SPACE
    bl_region_type = _REGION
    bl_category    = _CATS_CAT
    bl_parent_id   = "BF_PT_sb_vrchat"
    bl_order       = 8
    bl_options     = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.label(text=T("Export to VRChat"))

    @classmethod
    def poll(cls, context):
        return (
            context.active_object is not None
            and context.active_object.type == 'ARMATURE'
        )

    def draw(self, context):
        layout = self.layout
        _draw_explainer(
            layout, context,
            "Packages your avatar for VRChat SDK upload. Final step.",
            "Complete needed VRChat setup and body/physics steps first.",
        )

        layout.separator(factor=0.3)

        try:
            from boneforge.vrchat.export.vrchat_export import draw_export_settings
            draw_export_settings(layout, context)
        except Exception:
            layout.label(text=T("Export settings unavailable"), icon='INFO')

        layout.separator(factor=0.3)

        col = layout.column(align=True)
        col.scale_y = 1.2
        try:
            col.operator(
                "boneforge.vrc_export_to_unity",
                text=T("Export to VRChat (Unity)"),
                icon='EXPORT',
            )
        except Exception:
            col.label(text=T("Export operator unavailable"), icon='ERROR')

        layout.separator(factor=0.5)

        col2 = layout.column(align=True)
        try:
            col2.operator(
                "boneforge.vrc_generate_sidecar",
                text=T("Generate Sidecar"),
                icon='FILE_SCRIPT',
            )
            col2.operator(
                "boneforge.vrc_copy_unity_script_path",
                text=T("Copy Importer Path"),
                icon='COPYDOWN',
            )
        except Exception:
            col2.label(text=T("Sidecar operators unavailable"), icon='INFO')

        layout.separator(factor=0.4)

        mtoon_col = layout.column(align=True)
        mtoon_col.label(text=T("Material Check:"), icon='MATERIAL')
        mtoon_col.operator(
            "boneforge.vrc_check_mtoon",
            text=T("Check / Preserve MToon"),
            icon='SHADING_RENDERED',
        )


# =============================================================
# HUB: Review  (order=40)
# Formerly "Animate". Renamed to "Review" — contains animation
# organisation tools AND inspect/diagnostic tools. bl_idname
# kept as BF_PT_sb_animate so all child panels keep their links.
# =============================================================

class BF_PT_sb_animate(Panel):
    """BoneForge -> Review hub: animate, inspect, validate.

    Merges the former Animate and Inspect tabs. bl_idname preserved
    as BF_PT_sb_animate so Collections, Pose Library, Graph Tools,
    and Bone Inspector (registered by bone_inspector.py) keep their
    bl_parent_id links without modification.
    """
    bl_label       = " "
    bl_idname      = "BF_PT_sb_animate"
    bl_space_type  = _SPACE
    bl_region_type = _REGION
    bl_category    = _CAT
    bl_order       = 40

    def draw_header(self, context):
        self.layout.label(text=T("Review"))

    @classmethod
    def poll(cls, context):
        try:
            prefs = context.preferences.addons["boneforge"].preferences
            if not prefs.show_tab_boneforge:
                return False
        except Exception:
            pass
        return (
            context.active_object is not None
            and context.active_object.type == 'ARMATURE'
        )

    def draw(self, context):
        self.layout.label(
            text=context.active_object.name,
            icon='ACTION',
        )


class BF_PT_sb_collections(Panel):
    """Bone collection manager — ui_panels. Child of Review."""
    bl_label       = " "
    bl_idname      = "BF_PT_sb_collections"
    bl_space_type  = _SPACE
    bl_region_type = _REGION
    bl_category    = _CAT
    bl_parent_id   = "BF_PT_sb_animate"
    bl_options     = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.label(text=T("Collections"))

    @classmethod
    def poll(cls, context):
        return (
            context.active_object is not None
            and context.active_object.type == 'ARMATURE'
        )

    def draw(self, context):
        _draw_explainer(
            self.layout, context,
            "Manage and toggle bone collection visibility on your armature.",
            "Organize control, deform, and helper bone groups.",
        )
        _delegate_draw(self, context,
                       "boneforge.ui_panels.collection_ui",
                       "BF_PT_CollectionPanel")


class BF_PT_sb_pose_lib(Panel):
    """Pose library — animation. Child of Review."""
    bl_label       = " "
    bl_idname      = "BF_PT_sb_pose_lib"
    bl_space_type  = _SPACE
    bl_region_type = _REGION
    bl_category    = _CAT
    bl_parent_id   = "BF_PT_sb_animate"
    bl_options     = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.label(text=T("Pose Library"))

    @classmethod
    def poll(cls, context):
        return (
            context.active_object is not None
            and context.active_object.type == 'ARMATURE'
        )

    def draw(self, context):
        _draw_explainer(
            self.layout, context,
            "Save and apply named poses to your rig.",
            "Use for storing expressions, rest poses, or animation reference frames.",
        )
        _delegate_draw(self, context,
                       "boneforge.animation.pose_library",
                       "BF_PT_PoseLibraryPanel")


class BF_PT_sb_graph(Panel):
    """Graph & Animation tools — animation. Child of Review."""
    bl_label       = " "
    bl_idname      = "BF_PT_sb_graph"
    bl_space_type  = _SPACE
    bl_region_type = _REGION
    bl_category    = _CAT
    bl_parent_id   = "BF_PT_sb_animate"
    bl_options     = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.label(text=T("Graph Tools"))

    @classmethod
    def poll(cls, context):
        return (
            context.active_object is not None
            and context.active_object.type == 'ARMATURE'
        )

    def draw(self, context):
        _draw_explainer(
            self.layout, context,
            "Clean F-curves, smooth keyframes, and manage animation curve data.",
            "Companion tools for working in the Graph Editor.",
        )
        _delegate_draw(self, context,
                       "boneforge.animation.graph_tools",
                       "BF_PT_GraphToolsPanel")


class BF_PT_sb_rig_validator(Panel):
    """Rig validation checks — advanced_rigging. Child of Review."""
    bl_label       = " "
    bl_idname      = "BF_PT_sb_rig_validator"
    bl_space_type  = _SPACE
    bl_region_type = _REGION
    bl_category    = _CAT
    bl_parent_id   = "BF_PT_sb_animate"
    bl_options     = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.label(text=T("Rig Validator"))

    @classmethod
    def poll(cls, context):
        return (
            context.active_object is not None
            and context.active_object.type == 'ARMATURE'
        )

    def draw(self, context):
        _draw_explainer(
            self.layout, context,
            "Checks for common rig errors — missing bones, broken constraints, naming issues.",
            "Run when something behaves unexpectedly or before handing off the rig.",
        )
        _delegate_draw(self, context,
                       "boneforge.advanced_rigging.rig_validator",
                       "BONEFORGE_PT_p2c_rig_validator")


class BF_PT_sb_rig_readme(Panel):
    """Rig Readme — per-armature documentation — advanced_rigging. Child of Review."""
    bl_label       = " "
    bl_idname      = "BF_PT_sb_rig_readme"
    bl_space_type  = _SPACE
    bl_region_type = _REGION
    bl_category    = _CAT
    bl_parent_id   = "BF_PT_sb_animate"
    bl_options     = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.label(text=T("Rig Readme"))

    @classmethod
    def poll(cls, context):
        return (
            context.active_object is not None
            and context.active_object.type == 'ARMATURE'
        )

    def draw(self, context):
        _draw_explainer(
            self.layout, context,
            "View or edit the embedded README for this rig.",
            "Documents bone conventions, known quirks, and usage notes.",
        )
        _delegate_draw(self, context,
                       "boneforge.advanced_rigging.rig_notes",
                       "BONEFORGE_PT_p2c_rig_readme")


class BF_PT_sb_bone_counsel(Panel):
    """Bone Role Counsel — Confession Layer (H6 + A1).

    Shows one plain-language sentence about the selected bone's
    jurisdiction (controller, DEF, MCH/ORG, unknown) so animators
    always know whether they are touching the right bone.

    When no bone is selected shows an armature summary (idle frame)
    so the panel is never blank.
    """
    bl_label       = "Bone Role"
    bl_idname      = "BF_PT_sb_bone_counsel"
    bl_space_type  = _SPACE
    bl_region_type = _REGION
    bl_category    = _CAT
    bl_parent_id   = "BF_PT_sb_animate"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        if obj is None or obj.type != "ARMATURE":
            return False
        try:
            from boneforge.autorig.quick_human import _is_generated_rigify_control_rig
            return _is_generated_rigify_control_rig(obj)
        except ImportError:
            return False

    def draw(self, context):
        _draw_confession_layer(self.layout, context)


# =============================================================
# Registration
# NOTE: every parent panel MUST precede its children.
# BONEFORGE_PT_taskboard* registered by panel.py
# BONEFORGE_PT_bone_inspector registered by bone_inspector.py
# =============================================================

_CLASSES = (
    # Project strip + children
    BF_PT_sb_overview,
    BF_PT_sb_rig_notes,
    # Rig Builder tab — parent before children (unchanged)
    BF_PT_rb_setup,
    BF_PT_sb_quick_rig,
    BF_PT_sb_wizard,
    BF_PT_rb_mannequin,
    # Setup Rigging hub — parent before children
    BF_PT_sb_setup,
    BF_PT_sb_retarget,
    BF_PT_sb_rigify,
    # Skin hub — parent before children
    BF_PT_sb_skin,
    BF_PT_sb_weights,
    BF_PT_sb_correctives,
    # VRChat hub — parent before children (A then B then C)
    BF_PT_sb_vrchat,
    BF_PT_cats_vrc_tools,
    BF_PT_sb_vrc_naming,     # A-1
    BF_PT_sb_vrc_humanoid,   # A-2
    BF_PT_sb_vrc_hair,       # B-4
    BF_PT_sb_vrc_clothing,   # B-5
    BF_PT_sb_vrc_visemes,    # B-6
    BF_PT_sb_vrc_perf,       # C-7
    BF_PT_sb_vrc_export,     # C-8
    # Review hub — parent before children (animate + inspect merged)
    BF_PT_sb_animate,
    BF_PT_sb_collections,
    BF_PT_sb_pose_lib,
    BF_PT_sb_graph,
    BF_PT_sb_rig_validator,
    BF_PT_sb_rig_readme,
    BF_PT_sb_bone_counsel,  # Confession Layer — bone role guidance (v8.2.1)
)


def register():
    for cls in _CLASSES:
        bpy.utils.register_class(cls)
    # Compact Mode: user toggle to hide VRChat explainer text.
    # Default False so new users see explainers by default.
    bpy.types.Scene.boneforge_vrc_compact_mode = bpy.props.BoolProperty(
        name="Compact Mode",
        description=(
            "Hide explainer text in VRChat panels. "
            "Turn on once you know the pipeline."
        ),
        default=False,
    )


def unregister():
    for cls in reversed(_CLASSES):
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass
    if hasattr(bpy.types.Scene, "boneforge_vrc_compact_mode"):
        del bpy.types.Scene.boneforge_vrc_compact_mode
