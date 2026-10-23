# MMD / PMX installation repair — 2026-10-23

Current cumulative releases are BoneForge 9.0.15 and BoneCraft 9.2.15; see ../combiner-evidence/README.md. This file preserves the earlier MMD-only evidence.

**BoneCraft version correction:** the initial 9.1.3 checkout was stale.
The user's installed BoneCraft is 9.2.5. The corrected 9.2.5 repair candidate
and receipt replace the 9.1.3 recommendation. The original evidence below
remains an accurate record of the older checkout tests; corrected 9.2.5
evidence is recorded separately in `bonecraft-9.2.5-summary.json`.

Scope: BoneForge 9.0.5 and the current local BoneCraft 9.1.3 source. Local
repair candidates retain their base embedded versions and have `-mmd-fix`
filenames. Historical releases are preserved. Nothing was published.

## Reproduced cause

The upstream MMD Tools 4.5.14 release ZIP has both `__init__.py` and
`blender_manifest.toml` at its root and bundles an OpenCC wheel. The previous
installer treated that ZIP as a legacy add-on, wrapped it, and reported success.
A real Blender 5.2.2 run then found no available MMD importer. The extension
installer branch also used the nonexistent singular `package_install_file`
operator, omitted the required repository, and ignored cancellation results.

Modern MMD extensions use names such as `bl_ext.user_default.mmd_tools` and
need no legacy `bl_info`. Detection previously missed these extensions and
could let a disabled legacy installation mask an enabled extension.

Upstream references:

- https://github.com/MMD-Blender/blender_mmd_tools/releases/tag/v4.5.14
- https://github.com/blender/blender/blob/main/scripts/addons_core/bl_pkg/bl_extension_ops.py

## Repair

- Route root-manifest ZIPs through `extensions.package_install_files`, with
  an explicit enabled local user repository and `enable_on_install=True`.
- Never fall back to legacy installation after an extension installation fails.
- Preserve direct and wrapped legacy installations and check their results.
- Discover both namespaced extensions and legacy MMD packages; prefer an
  enabled copy and verify the PMX operator after activation.
- Report failed activation and cancelled PMX imports without claiming success.
- Use the current MMD-Blender upstream URL for automatic downloads.

## Verification

`summary.json` records the final evidence. Tests run with isolated
`BLENDER_USER_CONFIG`, `BLENDER_USER_SCRIPTS` and `BLENDER_USER_EXTENSIONS`
under this directory. The normal installed add-ons and user preferences were
not edited. Generated dependency files, logs and settings are local only.

Before the repair: 13 Python regression tests produced 10 failures and 1 error.
After the repair: all 13 pass against each product (26 checks total).

Real-host tests use the official MMD Tools release, verify its bundled OpenCC
wheel, and import a valid PMX containing a bone, weighted triangle and material.
Assertions require a new armature and a three-vertex mesh with one face. The
tests cover disk installation and the actual GitHub automatic download path.
The packaged add-ons are installed from their candidate ZIPs in fresh isolated
settings and tested again. ZIP receipts check CRC, embedded identity and exact
source parity; BoneForge also excludes the Bforartists gate files.

These are headless workflow checks. File-browser appearance and a user's
production avatar are not visually tested. VMD/VPD/export operators are probed
for availability; their data round trips are outside this repair.

Commands from `G:\LapArt\Projects\Blender_Addons`:

```powershell
# [PowerShell]
python BoneForge_Free/tests/test_mmd_install.py
python B4Artists_Tools/bonecraft/tests/test_mmd_install.py
```

For the real-host script, set the three `BLENDER_USER_*` variables to fresh
project-local directories. Pass `--background --factory-startup
--python-exit-code 1 --python <tests/blender_mmd_install.py> --
<package-parent-or-zip> <official-mmd-zip> <evidence-json> [auto]` to the host.

## Routing record

The canonical evaluator selected `recommended_lane=T3_PRIME_OMP` and
`actual_lane=T3_PRIME_OMP`, fingerprint
`29fa965cada3128ffe57b5d85d3b9f8e5d749d780954ea14ba5f45dcca1ad8b8`.
The bounded packet attempt encountered repeated `SupervisorError` admission
failures before any source application. Its stalled local transport was stopped;
native continuation completed the repair under the shared recoverable-failure
policy (`DEGRADED_NATIVE_CONTINUE`, no escalation). No remote proposal was applied.
Adaptive review classification was inconclusive; it is not counted as a passed
review. The executable tests and package receipts are the validation evidence.
