# BoneForge project rules

## Standard Blender release policy

- BoneForge 9.0.0 and every future BoneForge release must support standard Blender.
- BoneForge must not require Bforartists or register a Bforartists host lockout.
- Keep the add-on identity `BoneForge`, package directory `boneforge`, and release filename `BoneForge-<version>.zip`.
- BoneCraft is the separate Bforartists-exclusive product. Historical `BoneForge-BFA-*` packages belong to that lineage and must not be used as the base for an open Blender release.
- Before packaging a release, check its embedded version, source parity, and absence of Bforartists host gates, `bfa_guard.py`, and `BFA_EXCLUSIVE.md`.
- Keep the README download link, release notes, add-on metadata, and exported add-on version stamp consistent. Preserve historical release archives.
