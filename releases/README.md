# BoneForge releases

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
