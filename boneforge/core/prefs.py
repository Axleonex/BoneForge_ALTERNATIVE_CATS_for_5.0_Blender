"""BoneForge addon-wide user preferences.

Central preferences panel with per-module enable/disable toggles
and shared settings. Each phase module reads its enabled state from
here but never writes to it.
"""

import bpy
from bpy.props import (
    BoolProperty,
    EnumProperty,
    FloatProperty,
    IntProperty,
    StringProperty,
)


def _on_language_change(self, context):
    """Force all 3D viewport sidebar panels to redraw on language switch."""
    from boneforge.i18n import T  # noqa: trigger cache reset
    import bpy as _bpy
    try:
        for window in _bpy.context.window_manager.windows:
            for area in window.screen.areas:
                if area.type == 'VIEW_3D':
                    for region in area.regions:
                        if region.type == 'UI':
                            region.tag_redraw()
    except Exception:
        pass


class BoneForgePreferences(bpy.types.AddonPreferences):
    """Global addon preferences for BoneForge.

    Exposes user-configurable toggles (module enablement, UI options,
    defaults) that persist across Blender sessions. Accessed via
    Edit → Preferences → Add-ons → BoneForge, and programmatically
    through ``boneforge.core.addon_prefs(context)``.
    """

    bl_idname = "boneforge"

    # ── i18n language selector ───────────────────────────────────
    language: EnumProperty(
        name="Language",
        description="BoneForge interface language",
        items=[
            ("en", "English",    "English",    0),
            ("ja", "日本語",      "Japanese",   1),
            ("ko", "한국어",      "Korean",     2),
            ("zh", "中文",        "Mandarin",   3),
            ("pt", "Português",  "Portuguese", 4),
            ("es", "Español",    "Spanish",    5),
            ("fr", "Français",   "French",     6),
        ],
        default="en",
        update=_on_language_change,
    )

    # ── v3.3.0 tool registry persistence ────────────────────────
    # CSV of enabled tool ids, written by BF_OT_ToggleTool. Empty/unset
    # means "first run — enable all defaults". Read at register time by
    # boneforge.__init__._load_enabled_set.
    enabled_tools_csv: StringProperty(
        name="Enabled Tools",
        description="Internal: comma-separated list of enabled tool ids",
        default="",
        options={'HIDDEN'},
    )

    # ── Legacy module toggles (kept for backward-compat read on first
    # 3.3.0 register; new toggle UI lives below in draw()) ──────

    enable_collection_ui: BoolProperty(
        name="Bone Collection Panel",
        description="Show the bone-collection grouping panel in the 3D viewport sidebar",
        default=True,
    )
    enable_bookmarks: BoolProperty(
        name="Visibility Bookmarks",
        description="Enable saving and restoring bone-collection visibility states",
        default=True,
    )
    enable_hotkey_popup: BoolProperty(
        name="Hotkey Pop-up",
        description="Enable the floating pop-up panel triggered by a viewport hotkey",
        default=True,
    )

    # ── Hotkey popup settings ───────────────────────────────────

    popup_width: IntProperty(
        name="Pop-up Width",
        description="Remembered width of the hotkey pop-up panel in pixels",
        default=300,
        min=200,
        max=600,
    )



    # ── Phase 2 module toggles ─────────────────────────────────

    # v3.0.26: enable_tween removed (Tween Machine was animation-centric).
    enable_pose_library: BoolProperty(
        name="Pose Library",
        description="Enable the visual pose browser with thumbnail previews",
        default=True,
    )
    enable_graph_tools: BoolProperty(
        name="Graph & Viewport Tools",
        description="Enable breakdowner, delta mover, and inline graph editor",
        default=True,
    )
    enable_correctives: BoolProperty(
        name="Corrective Shape Keys",
        description="Enable angle-based corrective shape key authoring",
        default=True,
    )
    enable_rigify_enhance: BoolProperty(
        name="Rigify Auto-Enhancement",
        description="Enable automatic Rigify rig detection and enhancement",
        default=True,
    )

    # ── Phase 2B module toggles ──────────────────────────────────

    enable_shapes: BoolProperty(
        name="Custom Bone Shapes",
        description="Enable the bone shape library and shape generators",
        default=True,
    )
    enable_weight_mirror: BoolProperty(
        name="Weight Mirror",
        description="Enable mesh-relative weight mirroring with KDTree matching",
        default=True,
    )
    enable_weight_transfer: BoolProperty(
        name="Weight Transfer",
        description="Enable cross-mesh weight transfer tools",
        default=True,
    )
    enable_weight_table: BoolProperty(
        name="Weight Table",
        description="Enable tabular vertex weight editing",
        default=True,
    )
    enable_weight_tools: BoolProperty(
        name="Weight Paint Tools",
        description="Enable flood-to-zero, flood-to-one, and custom weight tools",
        default=True,
    )
    enable_deform_control: BoolProperty(
        name="Deform/Control Tagging",
        description="Enable bone deform/control tagging and FBX export helpers",
        default=True,
    )
    enable_delta_mush: BoolProperty(
        name="Delta Mush",
        description="Enable Corrective Smooth modifier wrapper for smooth deformations",
        default=True,
    )
    enable_proximity_wrap: BoolProperty(
        name="Proximity Wrap",
        description="Enable Surface Deform modifier wrapper for mesh binding",
        default=True,
    )

    # ── Phase 2C module toggles ──────────────────────────────────

    enable_space_switch: BoolProperty(
        name="Space Switching",
        description="Enable keyframed parent space switching with Child Of constraints",
        default=True,
    )
    enable_rig_validator: BoolProperty(
        name="Rig Validator",
        description="Enable armature validation checks and custom check registry",
        default=True,
    )
    enable_spline_ik: BoolProperty(
        name="Spline IK Builder",
        description="Enable NURBS-based Spline IK chain creation",
        default=True,
    )
    enable_ribbon: BoolProperty(
        name="Ribbon Builder",
        description="Enable NURBS ribbon surface strip deformation",
        default=True,
    )
    enable_sdk_system: BoolProperty(
        name="Set-Driven Keys",
        description="Enable generalized driver creation and SDK workflow",
        default=True,
    )
    enable_chain_dynamics: BoolProperty(
        name="Chain Dynamics",
        description="Enable Verlet-integration secondary motion on bone chains",
        default=True,
    )
    enable_viseme: BoolProperty(
        name="Viseme System",
        description="Enable viseme shape key management and lip sync generation",
        default=True,
    )
    enable_rig_notes: BoolProperty(
        name="Rig Notes",
        description="Enable rig documentation, viewport overlays, and rig readme",
        default=True,
    )
    enable_game_export: BoolProperty(
        name="Game Export",
        description="Enable game engine export helpers and deform-only baking",
        default=True,
    )

    # ── VRChat phase toggles ──────────────────────────────────

    enable_vrchat: BoolProperty(
        name="CATS",
        description="Enable VRChat avatar assembly, PhysBones, visemes, and export",
        default=True,
    )

    # ── Phase 3 module toggles ─────────────────────────────────

    enable_autorig: BoolProperty(
        name="Auto-Rig Wizard",
        description="Enable the in-viewport auto-rigging wizard",
        default=True,
    )
    enable_retarget: BoolProperty(
        name="Animation Retargeting",
        description="Enable the clip browser and retargeting engine",
        default=True,
    )

    # ── Phase 3 proportion overrides ──────────────────────────

    proportion_shoulder: FloatProperty(
        name="Shoulder Ratio",
        description="Neck base to shoulder as fraction of total arm length",
        default=0.18,
        min=0.05,
        max=0.40,
        precision=3,
    )
    proportion_elbow: FloatProperty(
        name="Elbow Ratio",
        description="Shoulder to elbow as fraction of total arm length",
        default=0.48,
        min=0.30,
        max=0.65,
        precision=3,
    )
    proportion_hip: FloatProperty(
        name="Hip Ratio",
        description="Pelvis center to hip joint as fraction of leg length",
        default=0.10,
        min=0.02,
        max=0.25,
        precision=3,
    )
    proportion_knee: FloatProperty(
        name="Knee Ratio",
        description="Hip to knee as fraction of leg length",
        default=0.52,
        min=0.35,
        max=0.65,
        precision=3,
    )

    # ── Phase 3 clip library ──────────────────────────────────

    clip_library_path: StringProperty(
        name="Clip Library",
        description="Folder containing animation clip files (FBX, BVH, .blend)",
        subtype='DIR_PATH',
        default="",
    )

    # ── Phase 2 settings ───────────────────────────────────────

    smart_bake_tolerance: FloatProperty(
        name="Smart Bake Tolerance",
        description="Maximum deviation from linear interpolation before a keyframe is kept",
        default=0.01,
        min=0.001,
        max=1.0,
        precision=4,
    )

    # ── v7.1.1 Sidebar tab visibility ──────────────────────────
    show_tab_boneforge: BoolProperty(
        name="BoneForge",
        description="Show the BoneForge tab in the 3D viewport N-panel",
        default=True,
    )
    show_tab_cats: BoolProperty(
        name="CATS",
        description="Show the CATS tab in the 3D viewport N-panel",
        default=True,
    )
    show_tab_rig_builder: BoolProperty(
        name="Rig Builder",
        description="Show the Rig Builder tab in the 3D viewport N-panel",
        default=True,
    )

    def draw(self, context):
        from boneforge.i18n import T
        layout = self.layout

        # Language selector
        lang_box = layout.box()
        lang_box.label(text=T("Language / 言語 / 언어 / 语言"), icon='WORLD_DATA')
        lang_box.prop(self, "language")
        layout.separator(factor=0.5)

        # ── Sidebar Tabs ────────────────────────────────────────
        tabs_box = layout.box()
        tabs_box.label(text=T("Sidebar Tabs"), icon='WINDOW')
        col = tabs_box.column(align=True)
        col.prop(self, "show_tab_boneforge")
        col.prop(self, "show_tab_cats")
        col.prop(self, "show_tab_rig_builder")
        layout.separator(factor=0.5)

        # v3.3.1: Tools list driven by the registry. Two-column split
        # (40% toggle button, 60% description) with checkbox-style
        # icons so the click target and current state are visually
        # obvious. Each click goes through BF_OT_ToggleTool which
        # defers the register/unregister via bpy.app.timers (no crash).
        box = layout.box()
        box.label(text=T("Tools"), icon='PREFERENCES')
        col = box.column(align=True)
        col.label(
            text=T("Click a tool to toggle it. Disabling removes the tool's classes and panels from this session."),
            icon='INFO',
        )
        col.separator(factor=0.5)

        try:
            from boneforge.core.tool_registry import get_registry
            registry = get_registry()
        except ImportError:
            col.label(
                text=T("Tool registry unavailable."),
                icon='ERROR',
            )
        else:
            tools = sorted(registry.all_tools(), key=lambda m: m.name)
            if not tools:
                col.label(
                    text=T("No tools registered yet — Blender may still be loading."),
                    icon='INFO',
                )
            for manifest in tools:
                enabled = registry.is_enabled(manifest.id)

                # 40 / 60 split — button on the left, description on
                # the right. Keeps buttons visually distinct from
                # full-width labels.
                split = col.split(factor=0.4, align=True)

                op = split.operator(
                    "boneforge.toggle_tool",
                    text=T(manifest.name),
                    icon=("CHECKBOX_HLT" if enabled else "CHECKBOX_DEHLT"),
                    depress=enabled,
                )
                op.tool_id = manifest.id

                desc_row = split.row(align=True)
                desc_row.label(
                    text=T(manifest.description),
                    icon=manifest.icon,
                )

                if manifest.depends_on:
                    dep_split = col.split(factor=0.4, align=True)
                    dep_split.label(text="")
                    dep_split.label(
                        text=f"requires: {', '.join(manifest.depends_on)}",
                        icon='LINK_BLEND',
                    )

                col.separator(factor=0.3)

        # v3.3.1: legacy toggle box removed from UI. The BoolProperty
        # fields (enable_collection_ui etc.) are still defined on this
        # AddonPreferences class so v3.2.x user preferences round-trip
        # without erroring; they just don't render any more. Removal
        # in 3.4.0.

        # v3.3.1: settings boxes below are gated on the registry's
        # enabled state for the corresponding phase. If the phase is
        # disabled, its settings are hidden — there's nothing to
        # configure.
        try:
            from boneforge.core.tool_registry import get_registry
            _registry = get_registry()
            _is_enabled = _registry.is_enabled
        except ImportError:
            _is_enabled = lambda _id: True  # fail open

        # Hotkey popup (ui_panels)
        if _is_enabled("phase1_panels"):
            box = layout.box()
            box.label(text=T("Hotkey Pop-up"), icon='EVENT_OS')
            box.prop(self, "popup_width")
            box.label(
                text=T("Configure the hotkey in Keymap → 3D View → BoneForge Rig Panel"),
                icon='INFO',
            )

            box.separator(factor=0.5)

        # v3.2.3: Maintenance — hot-reload, state purge.
        box = layout.box()
        box.label(text=T("Maintenance"), icon='RECOVER_LAST')
        col = box.column(align=True)
        col.label(
            text=T("If you re-installed BoneForge and Blender still shows the old UI, click Reload below."),
            icon='INFO',
        )
        col.label(
            text=T("Reloading purges sys.modules, scrubs Scene props, and deletes __pycache__/ files. No restart needed."),
        )
        row = col.row(align=True)
        row.operator(
            "boneforge.reload_addon",
            text=T("Reload BoneForge"),
            icon='FILE_REFRESH',
        )
        row.operator(
            "boneforge.purge_state",
            text=T("Purge State"),
            icon='TRASH',
        )


# ── Helper ──────────────────────────────────────────────────────

def addon_prefs(context: bpy.types.Context) -> BoneForgePreferences:
    """Convenience accessor for BoneForge addon preferences."""
    return context.preferences.addons["boneforge"].preferences


# ── Registration ────────────────────────────────────────────────

classes = (BoneForgePreferences,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
