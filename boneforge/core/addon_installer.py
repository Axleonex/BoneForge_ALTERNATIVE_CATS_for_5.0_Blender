"""Shared helpers for installing third-party addons from .zip files.

Solves the common failure mode where a downloaded zip is "flat" —
``__init__.py`` (or ``blender_manifest.toml``) at the root of the
zip instead of inside a folder. Blender's
``bpy.ops.preferences.addon_install`` rejects flat zips with the
error::

    ZIP packaged incorrectly; __init__.py should be in a directory,
    not at top-level

This is what mmd_tools' recent releases hit when installed via the
legacy add-on installer (the new release zip is structured for the
Blender 4.2 Extensions platform). It's also what some VRM addon
fork releases trigger.

The :func:`smart_install_zip` flow:

1. Inspect the zip's structure.
2. If ``__init__.py`` or ``blender_manifest.toml`` sits at the root,
   extract → re-zip with everything wrapped in a single directory →
   try ``addon_install`` against the wrapped zip.
3. If the zip is already structured correctly, install directly.
4. Surface a structured ``InstallResult`` to the caller — success
   flag, human-readable message, and the eventual filepath used.
"""

from __future__ import annotations

import logging
import os
import shutil
import tempfile
import zipfile
from dataclasses import dataclass
from typing import Optional

import bpy

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class InstallResult:
    """Outcome of an attempted addon install."""

    success: bool
    message: str
    repackaged: bool = False
    auto_enabled: bool = False  # True when the Extensions system handles enable
    error: Optional[Exception] = None


def inspect_zip_structure(filepath: str) -> dict:
    """Return a dict describing the zip's top-level layout.

    Keys:
        members          — full list of names
        top_level_files  — set of files (no slash) at root
        top_level_dirs   — set of directory names at root
        has_init_at_root — bool
        has_manifest_at_root — bool
        single_top_dir   — name of the single top-level dir, if any
    """
    with zipfile.ZipFile(filepath) as zf:
        members = zf.namelist()

    top_files = {m for m in members if "/" not in m and m}
    top_dirs = {m.split("/", 1)[0] for m in members if "/" in m}

    return {
        "members":              members,
        "top_level_files":      top_files,
        "top_level_dirs":       top_dirs,
        "has_init_at_root":     "__init__.py" in top_files,
        "has_manifest_at_root": "blender_manifest.toml" in top_files,
        "single_top_dir":       (next(iter(top_dirs)) if len(top_dirs) == 1
                                 and not top_files else None),
    }


def _try_extension_install(filepath: str) -> InstallResult:
    """Try installing via the Blender 4.2+ Extensions system.

    Returns a successful InstallResult if the Extensions API is
    available and accepted the zip, otherwise a failed result so the
    caller can fall back to the legacy path.
    """
    try:
        bpy.ops.extensions.package_install_file(filepath=filepath)
        return InstallResult(
            success=True,
            message="Installed as Blender 4.2+ Extension",
            auto_enabled=True,
        )
    except AttributeError:
        return InstallResult(
            success=False,
            message="bpy.ops.extensions not available (pre-4.2 Blender)",
        )
    except RuntimeError as exc:
        return InstallResult(
            success=False,
            message=f"extensions.package_install_file failed: {exc}",
            error=exc,
        )


def smart_install_zip(
    filepath: str,
    *,
    fallback_folder_name: str = "addon",
) -> InstallResult:
    """Install *filepath* via Blender's add-on installer, repackaging
    if the zip's structure would otherwise be rejected.

    *fallback_folder_name* is used as the wrapper directory's name
    when the zip is flat and we have no other hint. Pass the addon's
    canonical Python module name here (e.g. ``"mmd_tools"``,
    ``"VRM_Addon_for_Blender"``) so the resulting installed module
    has a sensible identifier.
    """
    if not os.path.isfile(filepath):
        return InstallResult(
            success=False,
            message=f"File not found: {filepath}",
        )

    try:
        info = inspect_zip_structure(filepath)
    except (zipfile.BadZipFile, OSError) as exc:
        return InstallResult(
            success=False,
            message=f"Could not read zip: {exc}",
            error=exc,
        )

    # Path 0: Blender 4.2+ Extension zip (blender_manifest.toml at root,
    # no __init__.py) — try the Extensions installer first before falling
    # back to the legacy repackage path, which Blender 4.2+ rejects.
    if info["has_manifest_at_root"] and not info["has_init_at_root"]:
        ext_result = _try_extension_install(filepath)
        if ext_result.success:
            return ext_result
        logger.info(
            "[BoneForge] Extension installer did not succeed (%s); "
            "falling back to legacy repackage path",
            ext_result.message,
        )

    needs_wrap = (
        info["has_init_at_root"] or info["has_manifest_at_root"]
    )

    # Path 1: zip is structured normally — try direct install.
    if not needs_wrap:
        try:
            bpy.ops.preferences.addon_install(
                filepath=filepath, overwrite=True,
            )
            return InstallResult(
                success=True,
                message="Installed directly",
            )
        except RuntimeError as exc:
            err_str = str(exc)
            if "ZIP packaged incorrectly" not in err_str:
                # Some other failure — give up
                return InstallResult(
                    success=False,
                    message=f"addon_install failed: {exc}",
                    error=exc,
                )
            # Fall through and try repackaging
            logger.info(
                "[BoneForge] addon_install reported zip-structure issue; "
                "attempting auto-repackage"
            )

    # Path 2: zip is flat — repackage with a folder wrap.
    return _install_with_wrap(filepath, fallback_folder_name)


def _install_with_wrap(filepath: str, folder_name: str) -> InstallResult:
    """Extract → wrap in folder → re-zip → install."""
    with tempfile.TemporaryDirectory() as td:
        extracted = os.path.join(td, "extracted")
        try:
            with zipfile.ZipFile(filepath) as zf:
                zf.extractall(extracted)
        except (zipfile.BadZipFile, OSError) as exc:
            return InstallResult(
                success=False,
                message=f"Failed to extract zip: {exc}",
                error=exc,
            )

        wrapped_zip = os.path.join(td, "wrapped.zip")
        try:
            with zipfile.ZipFile(
                wrapped_zip, "w", zipfile.ZIP_DEFLATED,
            ) as out_zf:
                for root, _, files in os.walk(extracted):
                    for f in files:
                        full = os.path.join(root, f)
                        rel = os.path.relpath(full, extracted)
                        out_zf.write(
                            full, os.path.join(folder_name, rel),
                        )
        except OSError as exc:
            return InstallResult(
                success=False,
                message=f"Failed to repackage zip: {exc}",
                error=exc,
            )

        try:
            bpy.ops.preferences.addon_install(
                filepath=wrapped_zip, overwrite=True,
            )
            return InstallResult(
                success=True,
                message=f"Installed (repackaged into {folder_name}/)",
                repackaged=True,
            )
        except RuntimeError as exc:
            return InstallResult(
                success=False,
                message=(
                    f"addon_install failed even after repackaging: "
                    f"{exc}. The zip may be a Blender 4.2+ Extension "
                    "(see manual install instructions)."
                ),
                error=exc,
                repackaged=True,
            )
