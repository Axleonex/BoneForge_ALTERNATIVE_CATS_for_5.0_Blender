# BoneForge releases

## 9.0.5 — Starter Rigs catalog (local build)

Local package: [BoneForge-9.0.5.zip](BoneForge-9.0.5.zip). Unpublished.

- Adds an Object Mode asset shelf for standard Blender, reusing a host Object shelf when one exists.
- Includes nine real starter skeleton/metarig assets in one **Starter Rigs** catalog.
- Displays other compatible asset libraries and catalogs alongside the starters.
- Adds no controls to the top-left viewport header.
- Updates add-on metadata and export-sidecar stamp to 9.0.5.

Open the bottom shelf's catalog menu, choose **All** libraries and check
**Starter Rigs** once to enable its tab. The host does not expose automatic tab
configuration to Python. Drag a thumbnail into the viewport to import a rig;
use Quick Rig for fitted generation and Rigify control generation.

Focused standard Blender checks cover registration, reload, other assets,
library ownership and all nine bundled assets. The existing 628 panel/menu
draw checks and Task Board suite pass on Blender 5.2.2. The package receipt
records integrity, source parity, version stamps and absence of Bforartists gates.

## 9.0.4 — Health Check and Task Board (repository build)

Repository package: [BoneForge-9.0.4.zip](BoneForge-9.0.4.zip). No 9.0.4 GitHub Release has been published.

- Open Health Check runs the registered validator and displays refreshable results.
- Accepts an armature or a mesh bound to one; explains a disabled or unavailable validator.
- Quick Wins keeps the top three recommendations. Remaining Tasks lists only other cards, with correct counts and no empty categories.
- Add-on metadata, export-sidecar stamp and current manual labels are 9.0.4.

Verified in standard Blender 5.1.2: 628 panel/menu draws, existing tool placements,
273 registered operators (only Health Check behavior changes), sidebar/Scene
visibility, toggles, reload and seven languages. Focused Task Board tests cover
selection, validator execution/availability, popup dispatch/results/refresh and
unique cards/counts/collapse. Native popup appearance is not visually verified.

Package entries: 156. SHA-256: `0ee80234c9f86c76d532e51ab75159634f0e8972929c02faa74ad515820c9139`.
The [package receipt](BoneForge-9.0.4-receipt.json) records CRC, source parity,
version stamps and absence of Bforartists host gates. Earlier archives remain available.

## 9.0.3 — VRChat export interface cleanup

Download: [BoneForge-9.0.3.zip](BoneForge-9.0.3.zip).

Adapts BoneCraft 9.2.3's export-panel cleanup to standard Blender:

- Removes Export to VRChat from CATS → Avatar Tools, including its Scene-tab copy.
- Keeps VRChat export under CATS → Import / Export → Unity / VRChat.
- Updates Avatar Tools overview text in all seven languages.
- Updates add-on metadata, the exported sidecar version stamp, README download links and current manual labels to 9.0.3.

Standard Blender 5.1.2 passes 628 panel/menu draw checks, export placement,
sidebar/Scene visibility, package toggles, reload, all seven languages and
parity of all 273 operator implementations. No BoneCraft-exclusive feature
or Bforartists host gate is added. Live-window appearance is not verified.

Package entries: 156. SHA-256: `2153a62d6fb84d8ca48b106fa7e0d0eecbd362e0da1ee964c017aeeeccef022d`.
The [package receipt](BoneForge-9.0.3-receipt.json) records CRC, source parity,
version stamps and absence of Bforartists host gates. Historical archives are retained.

## 9.0.2 — BoneCraft 9.2.2 workflow grouping (local)

Download: [BoneForge-9.0.2.zip](BoneForge-9.0.2.zip).

Adapts BoneCraft 9.2.2's organization to existing standard Blender tools:

- Bone Merge: BoneForge → Setup Rigging.
- Delta Mush and Proximity Wrap: BoneForge → Skin.
- Viseme Library, with its Lip Sync child: CATS → Avatar Tools, between Hair
  Physics and Export.
- VRChat Viseme Mapping and Face Tracking: CATS → VRChat Tools → Facial,
  between Clothing and Naming. Performance is the first section in VRChat Tools.

BoneForge has no Other Tools module; none is introduced. All 273 registered
operators and their execute/invoke/modal/poll bodies remain unchanged. No
BoneCraft-exclusive tool or Bforartists requirement is added. The add-on and
export metadata are 9.0.2; prior release archives are retained.

Verified in standard Blender 5.1.2: 636 panel/menu draw checks, all five placement
checks, Lip Sync drawing in Pose mode, Scene and Object Data mirror placement,
relocated tool-package toggles, sidebar visibility, reload, operator parity,
and seven languages. Live-window appearance is not verified.

Reference: BoneCraft 9.2.2 (`bonecraft-v9.2.2`, source `bc91de5`). Its 232-file
archive SHA-256 matches the published release digest.

Package entries: 156. SHA-256: `4e7513fd81ed4e49cc8c58d01f2455a5a2b20555be418c9a4d24f9a4f9b2d48b`.

## 9.0.1 — shared interface layout (local)

Download: [BoneForge-9.0.1.zip](BoneForge-9.0.1.zip).

Adopts BoneCraft's layout for existing BoneForge tools in standard Blender:
CATS groups Avatar Tools, VRChat Tools and Import / Export; the wizard precedes
Quick Rig; rig options fold; narrow layouts wrap help. Native Add/Armature,
Pose and Weights menus expose existing operators. Optional Scene Properties
mirrors preserve panel helpers and stay accessible when sidebar tabs are hidden.
Package toggles rebuild both Scene and Object Data mirrors without stale copies.
Inherited non-Blender icons use native Blender equivalents; no icon-conversion
wrapper is required. New translation entries use readable multiline dictionaries.

The release keeps all 273 existing operators and their execute/invoke/modal/poll
implementations. Tool-toggle infrastructure refreshes UI mirrors. It adds no
BoneCraft-exclusive functionality or Bforartists requirement. Basic mesh-based
marker guessing remains unchanged; inference-based detection stays disabled.

Verified on standard Blender 5.1.2 using `tests/blender_ui_layout.py`: 604 panel
and menu draws across empty/mesh/armature selection and narrow/normal widths,
Quick Rig helper reuse, sidebar/Scene visibility, dependency-blocked and normal
package toggles, unregister/re-register, and all seven supported languages.
Archive CRC, source parity, version metadata, and absence of host gates pass.
A visible-window screenshot and the operator execution workflows were not
retested; the change preserves existing action implementations. The declared
minimum remains Blender 4.0; that older host was not run during this update.

Package entries: 156. SHA-256: `b8e5b6d2170b91b22a692938ff2bf5ef34a6594e3ae1dec3174d22885926fbbb`.

## 9.0.0 — standard Blender release

BoneForge 9.0.0 establishes the permanent naming and host-support boundary:
all BoneForge releases from 9.0.0 onward support standard Blender and contain
no Bforartists host lockout. BoneCraft remains the separate Bforartists-exclusive
product. Historical `BoneForge-BFA-*` packages are part of the BoneCraft lineage.

Download: [BoneForge-9.0.0.zip](BoneForge-9.0.0.zip).

This release continues the open Blender 8.6.9 source at commit `a8a97f3`.
It includes the automatic body/clothing weight recalculation tools and clearer
atlas group/material selection controls already committed after the 8.6.9 zip
was packaged. This release changes the add-on version and exported version
stamp to 9.0.0; it adds no new rigging or avatar behavior.

The declared Blender minimum remains 4.0.0. The package keeps the `boneforge`
directory and `BoneForge` identity so existing preferences continue to match.
Existing manuals describe 8.6.9 and remain useful for the inherited workflows.
Earlier release archives are retained for historical reference.

### Package checks

- Embedded add-on version: `9.0.0`.
- Exported add-on version stamp: `9.0.0`.
- Package entries: 153, all under `boneforge/`, matching the source files.
- No Bforartists host gate or lockout marker files.
- SHA-256: `59202c5f3216c2008bd20e878cffacb0a6ee619ca5ba305f79cc0fee780254fc`.

Package integrity, source parity, and Python syntax were checked. This version
change was not run inside Blender; package checks do not establish runtime
compatibility for every individual feature.
