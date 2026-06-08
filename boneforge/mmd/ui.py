"""Sidebar panel for the BoneForge MMD bridge.

Layout, top to bottom:

    [Add-on status row]
        ✓ mmd_tools detected (vX.Y.Z)
                            OR
        ⚠ Not installed
        [Install paths: auto / disk / extensions / GitHub]

    [Import]
        [Import PMX / PMD…]
        [Import VMD Motion…]

    [Export]
        [Export PMX…]
        [Export VMD Motion…]
"""

from __future__ import annotations

import bpy
from bpy.types import Panel

from . import bridge
from boneforge.i18n import T


class BONEFORGE_PT_mmd(Panel):
    """BoneForge MMD bridge panel — child of the Import / Export hub.

    v3.3.12: moved from top-level to a child of BF_PT_sb_io. Hides
    via poll() when mmd_tools isn't detected — the IO hub renders
    the install row in that state.
    """

    bl_label = " "
    bl_idname = "BONEFORGE_PT_mmd"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BoneForge"
    bl_parent_id = "BF_PT_sb_io"
    bl_options = {"DEFAULT_CLOSED"}

    def draw_header(self, context):
        self.layout.label(text=T("MMD / PMX"))

    @classmethod
    def poll(cls, context):
        from . import bridge
        return bridge.find_mmd_addon() is not None

    def draw(self, context):
        layout = self.layout
        status = bridge.mmd_addon_status()

        # ── Add-on status ───────────────────────────────────────
        box = layout.box()
        if status["enabled"] and status["import_pmx_available"]:
            ver = status.get("version") or ()
            ver_text = ".".join(str(n) for n in ver) if ver else "unknown"
            box.label(
                text=f"mmd_tools: enabled (v{ver_text})",
                icon="CHECKMARK",
            )
        elif status["installed"] and not status["enabled"]:
            box.label(text=T("mmd_tools: installed but disabled"), icon="ERROR")
            box.operator(
                "boneforge.install_mmd_addon",
                text=T("Open Add-on Preferences"),
                icon="PREFERENCES",
            )
        else:
            box.label(text=T("mmd_tools: not installed"), icon="ERROR")
            box.label(
                text=T("Pick how you'd like to install it:"),
                icon="INFO",
            )
            col = box.column(align=True)
            col.operator(
                "boneforge.mmd_install_auto",
                text=T("Auto-Install Latest from GitHub"),
                icon="URL",
            )
            col.operator(
                "boneforge.mmd_install_from_disk",
                text=T("Install from .zip on Disk…"),
                icon="FILE_FOLDER",
            )
            row = col.row(align=True)
            op_ext = row.operator(
                "boneforge.mmd_open_website",
                text=T("Open Extensions Page"),
                icon="WORLD",
            )
            op_ext.target = "EXTENSIONS"
            op_gh = row.operator(
                "boneforge.mmd_open_website",
                text=T("GitHub"),
                icon="URL",
            )
            op_gh.target = "GITHUB"
            box.separator()
            box.operator(
                "boneforge.install_mmd_addon",
                text=T("Open Add-on Preferences (manual)"),
                icon="PREFERENCES",
            )
            box.label(
                text=T("Required for .pmx / .pmd / .vmd I/O"),
                icon="INFO",
            )

        layout.separator()

        # ── Import ──────────────────────────────────────────────
        col = layout.column(align=True)
        col.label(text=T("Import:"))
        row = col.row(align=True)
        row.enabled = status["import_pmx_available"]
        row.operator(
            "boneforge.mmd_import_pmx",
            text=T("Import PMX / PMD…"),
            icon="IMPORT",
        )
        row = col.row(align=True)
        row.enabled = status["import_vmd_available"]
        row.operator(
            "boneforge.mmd_import_vmd",
            text=T("Import VMD Motion…"),
            icon="ANIM",
        )
        row = col.row(align=True)
        row.enabled = status["import_vpd_available"]
        row.operator(
            "boneforge.mmd_import_vpd",
            text=T("Import VPD Pose…"),
            icon="POSE_HLT",
        )

        layout.separator()

        # ── Export ──────────────────────────────────────────────
        col = layout.column(align=True)
        col.label(text=T("Export:"))
        row = col.row(align=True)
        row.enabled = status["export_pmx_available"]
        row.operator(
            "boneforge.mmd_export_pmx",
            text=T("Export PMX…"),
            icon="EXPORT",
        )
        row = col.row(align=True)
        row.enabled = status["export_vmd_available"]
        row.operator(
            "boneforge.mmd_export_vmd",
            text=T("Export VMD Motion…"),
            icon="ANIM_DATA",
        )
        row = col.row(align=True)
        row.enabled = status["export_vpd_available"]
        row.operator(
            "boneforge.mmd_export_vpd",
            text=T("Export VPD Pose…"),
            icon="POSE_HLT",
        )

        layout.separator()

        # ── BoneForge Assist ────────────────────────────────────
        assist = layout.box()
        assist.label(text=T("BoneForge Assist"), icon="TOOL_SETTINGS")
        col = assist.column(align=True)
        col.scale_y = 0.95
        col.operator(
            "boneforge.mmd_convert_bone_names",
            text=T("Convert Bone Names → Unity"),
            icon="BONE_DATA",
        )
        col.operator(
            "boneforge.mmd_convert_physics",
            text=T("Convert Physics → PhysBones"),
            icon="RIGID_BODY",
        )
        assist.label(
            text=T("Tip: run Bone Names first, then Physics"),
            icon="INFO",
        )
