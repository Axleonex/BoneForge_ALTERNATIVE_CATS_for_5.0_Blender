# BoneForge releases

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
