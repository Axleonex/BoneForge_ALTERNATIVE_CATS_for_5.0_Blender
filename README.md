# BoneForge Alternative CATS for Blender 5.0

Open-Blender BoneForge package for standard Blender users.

This repository is the non-exclusive Blender build. It is centered on the CATS-style VRChat avatar workflow and packages the CATS-compatible BoneForge 8.5.1 add-on for standard Blender. Matching the B4Artists version number does not make this the B4Artists-exclusive payload.

This build is an attempted revival and continuation of no-longer-maintained free Blender avatar tools that helped VRChat artists prepare, clean, optimize, and export avatars. The focus is CATS first, because CATS is the core workflow named by this repository, with Material Combiner and UVToolkit-derived atlas controls integrated where they support that CATS workflow.

B4Artists-exclusive files must not be committed here.

> This tool was built with heavy AI assistance and is under active bug-fixing.
> If you hit a problem, a screenshot or a short note about what you were doing
> helps a lot — please open an [issue](../../issues).

## Requirements

- **Blender 4.0 or newer.** The add-on manifest declares a minimum of Blender 4.0, and packaging is oriented toward the Blender 5.0 release.
- This is a **legacy add-on** (`bl_info`), not a Blender 4.2+ Extension. Install it with **Install from Disk**, as described below — it will not appear in the Extensions online repository.
- Optional bridges only light up when their external dependency is already installed: MMD tools for PMX/VMD, and the VRM add-on for VRM.

## Install

1. Download the add-on zip: **[BoneForge-8.5.1.zip](https://github.com/Axleonex/BoneForge_ALTERNATIVE_CATS_for_5.0_Blender/raw/main/releases/BoneForge-8.5.1.zip)** (or grab it from the [Releases](../../releases) page).
2. In Blender, open **Edit → Preferences → Add-ons**.
3. Click the **dropdown arrow (˅) at the top-right of the Add-ons panel → Install from Disk…**
4. Select the `BoneForge-8.5.1.zip` you downloaded.
5. Tick the checkbox next to **BoneForge** to enable it.
6. In the 3D Viewport, press **N** to open the sidebar — BoneForge adds its tabs there.

Do not unzip the file by hand. Blender installs directly from the `.zip`.

**Updating from an older version:** disable and remove the previous BoneForge add-on in Preferences first, then restart Blender before installing the new zip. Installing over a live copy can leave stale registered classes behind.

## What Alternative CATS Offers

- CATS-focused avatar cleanup and preparation inside Blender.
- VRChat-oriented bone naming, humanoid mapping, viseme, eye tracking, mesh cleanup, transform, and performance helper workflows.
- CATS Material Combiner integration for building an atlas from selected materials and textures instead of blindly combining everything.
- Material and texture review before baking, including source material inspection, texture role labels, duplicate/shared source markers, and per-material controls.
- UVToolkit-derived atlas variation controls inside the CATS Material Combiner workflow, including selectable packing methods, Advanced Variation, Rotation Step, UV margin, seeded variation, oriented packing, and 0-1 bounds fitting.
- Basic BoneForge and Mixamo-style rigging helpers for the standard Blender package.
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

## What Is Not Included Here

This repository is not the B4Artists-exclusive BoneForge package. The open Blender build should not include:

- B4Artists host lockout or BFA marker files.
- Production control-rig construction.
- Smart landmark/joint detection suite.
- Animator control layer.
- Control Picker / rig UI.
- Advanced B4Artists-only retargeting source maps.
- Profile-driven B4Artists production export suite.

Those features belong only in the separate B4Artists-exclusive repository.

## Documentation

Manuals are in [`docs/`](docs/):

- [`docs/BoneForge_Documentation.pdf`](docs/BoneForge_Documentation.pdf) — user manual (PDF)
- [`docs/BoneForge_Documentation.md`](docs/BoneForge_Documentation.md) — same manual in Markdown

Translated manuals live in [`docs/localized/`](docs/localized/) — English, Japanese, Chinese, Korean, French, Spanish, and Portuguese, each as both Markdown and PDF.

## Source Package

The unpacked, readable source is in [`boneforge/`](boneforge/) so you can read it on GitHub without downloading anything. The source folder and the `releases/` zip contain the same code; the zip is just packaged for one-click install.

## Credits And Lineage

BoneForge Alternative CATS is not an official continuation of the upstream projects below. It credits them as workflow lineage and integrates compatible ideas into the BoneForge package.

- Original CATS workflow lineage: https://github.com/absolute-quantum/cats-blender-plugin
- Material Combiner lineage: https://github.com/Grim-es/material-combiner-addon
- UVToolkit method ideas and archival reference: https://github.com/oRazeD/UVToolkit

Additional detailed UV integration credits live in [`boneforge/vrchat/cats/uv_tools/CREDITS.md`](boneforge/vrchat/cats/uv_tools/CREDITS.md).

## License

Released under the **GNU General Public License v2.0 or later** — see [`LICENSE`](LICENSE).
