# Export bone naming

Available in BoneForge 9.0.17 and BoneCraft 9.2.17.

Open **Import / Export → Game Engine Export**. Both **Unity / VRChat** and
**Unreal Engine 5** have a **Bone Names** choice:

| Choice | Result |
|---|---|
| Keep Original Names | Existing names; the default. |
| Unity-Preset | Recognized bones use Unity Humanoid slot names, such as `Hips`, `LeftUpperArm` and `LeftIndexProximal`. |
| Unreal-Preset | Recognized bones use Unreal humanoid names, such as `pelvis`, `spine_01`, `upperarm_l`, `index_01_l` and `ball_l`. An existing separate `Root` becomes `root`. |

The preview shows recognized/renamed counts and the first three changes.
Unrecognized bones keep their names. Saved **Humanoid Mapper** slots take
precedence over name detection. Optional chest, neck, shoulders, eyes, jaw,
fingers and toes participate when recognized or explicitly mapped.

For Unity export, run **Auto-Map Humanoid**, review the required slots and
correct them before exporting. BoneCraft's **Export (Profile)** file browser
also offers **Bone Names** and inherits the Unreal section's selection when
launched from its panel. Its existing export-format profile remains separate.
For named profile exports choose **Active Action** or **No Animation**.
**All Actions** requires **Keep Original Names**, because it can include
unbound actions from other rigs.

Presets apply to temporary export copies. The working rig retains its bone
names, groups, actions, drivers and constraints. Export copies carry renamed
vertex groups and animation channels; Unity sidecars carry the corresponding
Humanoid, PhysBone and collider names. Cleanup restores selection and removes
temporary data on success or failure.

Conflicting target names, ambiguous detection and reused humanoid slots block
renaming instead of producing Blender `.001` suffixes. Include the armature with its meshes. Since 9.0.17 / 9.2.17 the main export
buttons temporarily use Object Mode and restore your previous mode and selection. Make linked objects local first.

These are naming profiles. They do not rebuild a skeleton, add missing joints,
change bone orientation or rest pose, or guarantee direct Manny/Quinn skeleton
compatibility. Unity Avatar mapping or Unreal retargeting may still be needed.
The Unity/VRChat exporter retains its existing rest-pose/no-animation behavior;
the Unreal exporter includes animation when **Bake Animation** is enabled.

[Host verification](../tests/export-context-evidence/README.md).
