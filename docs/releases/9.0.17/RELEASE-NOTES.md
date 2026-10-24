# BoneForge 9.0.17 — Export presets and mode fix

[Download BoneForge-9.0.17.zip](https://github.com/Axleonex/BoneForge_ALTERNATIVE_CATS_for_5.0_Blender/releases/download/v9.0.17/BoneForge-9.0.17.zip) · [Tagged release](https://github.com/Axleonex/BoneForge_ALTERNATIVE_CATS_for_5.0_Blender/releases/tag/v9.0.17).

Both Unity/VRChat and Unreal export sections now offer **Bone Names**:
**Keep Original Names**, **Unity-Preset**, or **Unreal-Preset**. The preview
shows recognized bones and proposed names. Renaming applies to temporary
export copies, with vertex groups, animation references and sidecar bone
references following the export names. The working rig retains its names.

The main export buttons now work from Object, Pose and Edit Mode. They
temporarily use Object Mode, then restore the original mode and selection.
Preparation and cleanup use data-API selection, fixing the repeated
`object.select_all.poll() failed, context is incorrect` export traceback.

Active-action FBX baking also works when no separate NLA strips exist.
Recognized optional humanoid bones, fingers and toes participate in naming.
Conflicting names block renaming instead of producing `.001` suffixes.
Existing MMD/PMX and material-combiner repairs are retained.

Naming preserves the existing hierarchy, rest pose and orientations. Unity
Avatar mapping or Unreal retargeting may still be needed; these presets do
not construct a complete Manny/Quinn skeleton.

## Install or update in standard Blender

1. Download **BoneForge-9.0.17.zip** above. Install the ZIP directly.
2. For an update, save your work, disable/remove the older add-on in
   Preferences, and restart the host before installing the new ZIP.
3. Open **Edit → Preferences → Add-ons**, open the menu at the upper right,
   choose **Install from Disk…**, and select **BoneForge-9.0.17.zip**.
4. Enable **BoneForge** and check that Preferences reports **9.0.17**.
5. Select the armature and open **Import / Export → Game Engine Export**.
   Choose **Bone Names** in the Unity/VRChat or Unreal section, then export.

## Validation

The exact ZIP passes 19 context cases and 14 naming/
FBX regression groups in its matching host. Metadata, export stamp, ZIP CRC,
SHA-256 and exact source parity were checked. User installations are outside
this GitHub update. Product manuals retain their historical capture/version
labels; the export naming guide supplements them for this release.
