# Material combiner usability review - 2026-10-23

Local packages: BoneForge 9.0.15 and BoneCraft 9.2.15.

The previous main panel was understandable to experienced users but dense for
beginners. Always-expanded mesh diagnostics, material overrides and texture roles
interrupted selection. Copy Debug competed with everyday actions, and Smart Combine
could rebuild the analysis after manual edits when Auto Analyze was enabled.

The main panel now names three stages: choose target, choose materials and textures,
then bake and review. Smart Combine is the initial shortcut. Once an analysis exists,
the panel offers Refresh Analysis and Bake Checked Sources, so the reviewed bake
does not invoke auto-analysis. Explicit refresh still rebuilds the source lists.
Source Details is off by default; Advanced Options contains Copy Debug. Backup,
Accept and Revert controls remain visible. Baking logic is unchanged by this update.

Both lists have Select All and Deselect All. They change the Include checkboxes,
not Blender's active highlighted row. Their scope is the active atlas group. Material
and texture lists stay independent. Missing textures remain unchecked. Bulk selection
does not enable a disabled group or affect other groups. Poll rejects absent/stale
group indexes and pending atlas previews with actionable messages.

## Inventory and skill audit

Implementation: `boneforge/vrchat/cats/material_atlas.py` in both source packages.
New operator: `BF_OT_VRC_AtlasSelectSources`; menu: `BONEFORGE_MT_atlas_selection`.
New setting: `show_source_details`; new helper: `_draw_source_selection`.
Existing lists, fields and bake operators retain their underlying behavior.

These are low-tier controls inside the atlas preparation procedure, not frequently
used viewport tools. Four selection buttons are net new in the panel, and the same
actions are reachable through Object > Atlas Source Selection. The duplicate main
Copy Debug button was removed. Selected source fields and mesh information moved
under Source Details. The advanced fold has a plain Advanced Options label.

Applied skill: `G:/LapArt/skills-shared/b4artists-ui-ux/SKILL.md` for BoneCraft.
BoneForge follows the same arrangement while retaining standard Blender support.

| Rule | Result and evidence |
|---|---|
| R1 act-first, R2 no-pre-dialog | PASS: selection execute changes checkboxes immediately; REGISTER/UNDO, no dialog. `blender_atlas_selection.py` checks operator RNA and repeat execution. |
| R3 menu-reachable | PASS: `_atlas_selection_menu` registers in `VIEW3D_MT_object`; host test records four menu actions. |
| R4 standard-places | PASS for scope: low-tier procedure, no new viewport or Tool Shelf tab. |
| R5 tools-apart | PASS for touched controls: list input and bulk actions together; source overrides folded. |
| R6 setting-not-button | PASS: `show_source_details` is a checkbox. |
| R7 no-header-icons | PASS: existing `draw_header` has a text label only. |
| R8 actions-then-options | PASS for touched area: main workflow and bake precede closed Advanced Options. |
| R9 one-home | PASS: selection panel home plus permitted header menu access; duplicate debug action removed. |
| R10 show-dont-hide | PASS: source lists remain visible, disabled-group message explains how to include the group; empty setup retains Analyze and Smart Combine. |
| R11 explains-itself | PASS for added controls: operator tooltip, descriptions, hidden/skip-save button parameters, actionable poll messages. New panel/menu labels translated in all six supported non-English dictionaries. Older English-only diagnostics are outside scope. |
| R12 readable-at-width | NOT VERIFIED visually: labels shortened, but no real-window screenshot or narrow-region inspection. |
| R13 no-dead-controls | PASS: new setting controls mesh/source detail visibility; source enabled flags are consumed by preflight and bake. |
| R14 evolve | PASS: preserves panel location, lists, advanced settings and bake operators. |

Deviations: existing atlas workflow conventions retained; this is a bounded main-panel
update. No relocation of the procedure or general conversion of its options to redo.

## Evidence and limits

`tests/blender_atlas_selection.py` reproduced the missing operator before repair,
then passed from fresh ZIP installs on standard Blender 5.2.2 LTS and Bforartists
5.2.0 (Blender base 5.3.0 Alpha). It checks both lists, independence, group isolation,
missing textures, repeat execution, empty/stale/preview polls, menu registration,
collapsed/expanded draw, reviewed bake path and RNA. Reports: `ui-forge-15/result.json`
and `ui-craft-15/result.json`. Scene settings and installed add-ons are isolated.

These are host operator and recording-layout checks. Real-window visual appearance,
interactive undo/redo, localization width and first-time-user comprehension were not
verified. The UI is simpler by inspection; no usability-study score is claimed.

The focused atlas suite passes 27 tests; the same two pre-existing unrelated checks
remain excluded. Both MMD suites pass 13 checks. The five generated-fixture bake
regressions are rerun separately against each packaged ZIP.

Both small UI plans classified actual lane T1_NATIVE under policy fingerprint
`29fa965cada3128ffe57b5d85d3b9f8e5d749d780954ea14ba5f45dcca1ad8b8`.
No publishing, pushing, merging, or installed user add-on replacement was performed.
