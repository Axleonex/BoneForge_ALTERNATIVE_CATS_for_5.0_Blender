# BoneForge Alternative CATS for Blender 5.0

Open-Blender BoneForge package for standard Blender users.

This repository is the non-exclusive Blender build. It is centered on the CATS-style VRChat avatar workflow and packages the CATS-compatible BoneForge 8.5.0 add-on for standard Blender. Matching the B4Artists version number does not make this the B4Artists-exclusive payload.

This build is an attempted revival and continuation of no-longer-maintained free Blender avatar tools that helped VRChat artists prepare, clean, optimize, and export avatars. The focus is CATS first, because CATS is the core workflow named by this repository, with Material Combiner and UVToolkit-derived atlas controls integrated where they support that CATS workflow.

B4Artists-exclusive files must not be committed here.

## What Alternative CATS Offers

- CATS-focused avatar cleanup and preparation inside Blender.
- VRChat-oriented bone naming, humanoid mapping, viseme, eye tracking, mesh cleanup, transform, and performance helper workflows.
- CATS Material Combiner integration for building an atlas from selected materials and textures instead of blindly combining everything.
- Material and texture review before baking, including source material inspection, texture role labels, duplicate/shared source markers, and per-material controls.
- UVToolkit-derived atlas variation controls inside the CATS Material Combiner workflow, including selectable packing methods, Advanced Variation, Rotation Step, UV margin, seeded variation, oriented packing, and 0-1 bounds fitting.
- Basic Rigify and Mixamo-style rigging helpers for the standard Blender package.
- Blender 5.0-oriented packaging for the non-exclusive/open Blender release.

## Import And Export Features

Many VRChat artists look for CATS-style tools because the hard part is not just editing an avatar, but getting it back out cleanly for Unity, VRChat, or another engine. This open Blender build includes an Import / Export hub for format bridge visibility and game export access.

- VRChat / Unity export access through the VRChat phase, including the `Export to VRChat (Unity)` operator when that phase is available.
- Performance rank checking for VRChat-oriented cleanup before export.
- MMD bridge visibility for PMX import/export when the external MMD tool dependency is installed.
- VRM bridge visibility when the external VRM dependency is installed.
- Unreal Engine FBX import/export helpers for round-tripping selected armatures and meshes.
- CATS cleanup, material atlas, and UV packing tools intended to reduce material and texture friction before export.

BoneForge does not upload avatars directly to VRChat. The final Unity/VRChat upload still belongs in the VRChat Creator Companion and SDK workflow.

## Credits And Lineage

BoneForge Alternative CATS is not an official continuation of the upstream projects below. It credits them as workflow lineage and integrates compatible ideas into the BoneForge package.

- Original CATS workflow lineage: https://github.com/absolute-quantum/cats-blender-plugin
- Material Combiner lineage: https://github.com/Grim-es/material-combiner-addon
- UVToolkit method ideas and archival reference: https://github.com/oRazeD/UVToolkit

Additional detailed UV integration credits live in `boneforge/vrchat/cats/uv_tools/CREDITS.md`.

## Release Package

- `releases/BoneForge-8.5.0.zip`

## Source Package

- `boneforge/`
