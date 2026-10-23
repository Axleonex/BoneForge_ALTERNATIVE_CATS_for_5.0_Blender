# Material combiner verification — 2026-10-23

Local releases: **BoneForge 9.0.15** and **BoneCraft 9.2.15**. Neither is
published. Both retain the earlier MMD/PMX repair. Old ZIPs are preserved.

The owner's requested policy is one patch increment per distinct bug fix.
`bugfix-versions.json` records each applied increment. Versions 6–13 are
internal fix increments in these cumulative builds, not separate releases.

| Patch | Fix included in both products |
|---|---|
| .6 | MMD extension installation/detection and PMX import repair |
| .7 | Ordinary DITHERED materials incorrectly treated as transparent through the deprecated HASHED compatibility property; linked/constant alpha detection |
| .8 | Tint and alpha node calculations discarded by image-only baking; evaluate the connected Principled input graph |
| .9 | Render-hidden sources could not bake; Revert did not restore original visibility |
| .10 | Excluded materials unnecessarily copied instead of retaining their authored shared references |
| .11 | Deleted/changed analyzed sources could produce a successful empty bake and an unusable backup |
| .12 | The final rebuilt mesh did not honor the default atlas UV0 export setting |
| .13 | Multi-mesh material counts under-reported atlas slots; Revert left the post-bake count |
| .14 | Color-only meshes without authored UVs baked, then failed during final mesh assembly |
| .15 | Missing bulk source selection and dense main UI: Select All/Deselect All, folded details, clear reviewed-bake path |

## Evidence

`summary.json` contains final package/host checks. Generated settings, logs,
test images and intermediate failures remain local under this directory.

`tests/blender_material_combiner.py` generates its own meshes and materials,
then runs the registered public Analyze/Bake/Accept/Revert operators. It tests:

- Opaque, constant-alpha and linked-alpha classification in the actual host.
- Actual RGB/alpha pixels from an image plus a tint multiplier and alpha math.
- Two full mixed-material meshes: geometry, shape keys, parent relationships,
  preserved transparent-material identity, UV0, material counts, Accept and Revert.
- Cancellation before backup creation when an analyzed source was deleted.
- Color-only meshes without UVs: bake, generated UV0 and unchanged originals after Revert.

Final tests install each release ZIP into fresh isolated user directories.
BoneForge runs in standard Blender 5.2.2 LTS; BoneCraft runs in the installed
Bforartists 5.2.0 binary, whose Blender base reports 5.3.0 Alpha. No normal
installed add-on or user preference was updated by these tests.

The earlier failing reports distinguish the reproduced faults from repairs.
After the classification fix, real pixel checks still failed until graph
evaluation was corrected; after the safety fixes, UV0 and multi-mesh count
assertions still failed until final assembly/counting were corrected.

The existing focused atlas tests pass (27 tests). Two pre-existing unrelated
checks are excluded: a specific sidebar icon-layout expectation and a hardcoded
9.0.0 BoneCraft release/archive check. They failed before these changes. Current
embedded versions, export stamps, host policy, CRC and exact source parity are
checked separately by the release receipts. The 13 MMD regressions pass for
each product; those three repaired MMD files are unchanged from the previously
host-verified packages.

## Limits and next action

These are generated-fixture and headless workflow checks, not approval of a
production avatar or a visual file-browser audit. The dedicated MToon fallback
remains in place; the new graph evaluation is for a directly connected
Principled surface. Metallic and ORM channel packing remain explicitly blocked
by preflight, as before. They are not represented as working bake passes.

Install the appropriate versioned ZIP and check a copy of the production avatar.
No commit, merge or GitHub publication was performed.

BoneCraft source is the isolated `B4Artists_Tools/.claude/worktrees/bonecraft-mmd-925`
checkout based on the confirmed 9.2.5 lineage (`a1092dc`). The outer Toolkit
checkout remains an older Ghost Tool work branch with unrelated edits.

Both coding plans were classified T3 with fingerprint
`29fa965cada3128ffe57b5d85d3b9f8e5d749d780954ea14ba5f45dcca1ad8b8`.
Native continuation preserved the same recovery scope after the session's
pre-application SupervisorError admission failures. No remote proposal applied.

[UI usability review and verification](ui-review.md) covers the .15 interface update.
