# BoneForge Alternative CATS for Blender 5.0

This repository is centered on the CATS-style VRChat avatar workflow and packages the CATS-compatible BoneForge add-on for Blender 5.0 and 4.0 versions.

This build is an attempted revival and continuation of no-longer-maintained free Blender avatar tools that helped VRChat artists prepare, clean, optimize, and export avatars. The focus is CATS first, with Material Combiner and UVToolkit-derived atlas controls integrated where they support that CATS workflow.

> This tool was built with heavy AI assistance and is under active bug-fixing.
> If you hit a problem, a screenshot or a short note about what you were doing
> helps a lot — please open an [issue](../../issues).

## Version and Blender support

**Current release: BoneForge 9.0.2.**

BoneForge 9.0.0 and all future BoneForge releases support standard Blender.
BoneForge does not require Bforartists and must not contain a Bforartists host
lockout. Release packages use the name `BoneForge-<version>.zip`.

BoneCraft is the separate Bforartists-exclusive add-on. Older packages named
`BoneForge-BFA-*` belong to that product lineage; they are not open Blender
BoneForge releases.

Version 9.0.0 continues the open Blender 8.6.9 codebase, including the weight
recalculation tools and atlas selection guidance already committed in this
repository. The older 8.6.9 zip does not contain those committed updates.
See [release notes](releases/README.md). The [manual](docs/BoneForge_Documentation.md) and [translated editions](docs/localized/) describe the 9.0.2 interface, including tabs, nested sections and moved tool locations.

## Install

1. Download the add-on zip: **[BoneForge-9.0.2.zip](https://github.com/Axleonex/BoneForge_ALTERNATIVE_CATS_for_5.0_Blender/raw/refs/heads/main/releases/BoneForge-9.0.2.zip)** (or grab it from the [Releases](../../releases) page).
2. In Blender, open **Edit → Preferences → Add-ons**.
3. Click the **dropdown arrow (˅) at the top-right of the Add-ons panel → Install from Disk…**
4. Select the `BoneForge-9.0.2.zip` you downloaded.
5. Tick the checkbox next to **BoneForge** to enable it.
6. In the 3D Viewport, press **N** to open the sidebar — BoneForge adds its tabs there.

Do not unzip the file by hand. Blender installs directly from the `.zip`.

**Updating from an older version:** disable and remove the previous BoneForge add-on in Preferences first, then restart Blender before installing the new zip. Installing over a live copy can leave stale registered classes behind.

## Other Features BoneForge Offers

- CATS-focused avatar cleanup and preparation inside Blender.
- VRChat-oriented bone naming, humanoid mapping, viseme, eye tracking, mesh cleanup, transform, and performance helper workflows.
- CATS Material Combiner integration for building an atlas from selected materials and textures instead of blindly combining everything.
- Material and texture review before baking, including source material inspection, texture role labels, duplicate/shared source markers, and per-material controls.
- UVToolkit-derived atlas variation controls inside the CATS Material Combiner workflow, including selectable packing methods, Advanced Variation, Rotation Step, UV margin, seeded variation, oriented packing, and 0-1 bounds fitting.
- Basic BoneForge and Mixamo-style rigging helpers for the standard Blender package.
- Auto-rigging and Rigify Mesh Creation Rigbuilder. 

## Import And Export Features

- VRChat / Unity export access through the VRChat phase, including the `Export to VRChat (Unity)` operator when that phase is available.
- Performance rank checking for VRChat-oriented cleanup before export.
- MMD bridge visibility for PMX import/export when the external MMD tool dependency is installed.
- VRM bridge visibility when the external VRM dependency is installed.
- Unreal Engine FBX import/export helpers for round-tripping selected armatures and meshes.
- CATS cleanup, material atlas, and UV packing tools intended to reduce material and texture friction before export.

BoneForge does not upload avatars directly to VRChat. The final Unity/VRChat upload still belongs in the VRChat Creator Companion and SDK workflow.

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
