# BoneForge 9.0.17 export verification

Date: 2026-10-24. Exact installable ZIP SHA-256: `27ce71164df04b3815af5fcb92a3fdcb0a3b9eebd67f86958d4bf4cdcf86a727`.

- [Context checks](context.json): 19 pass. Both registered export
  operators run from Properties in Object, Pose and Edit Mode, with all three
  naming choices. They restore mode, active object, object/bone selection,
  active bone, names, mapping, frame, vertex groups and action paths.
- The nineteenth context case injects an FBX failure in Pose Mode and checks
  cleanup, restored state, the original error and absence of a written file.
- [Naming and FBX regression](naming.json): 14 groups pass, including
  real FBX reimport, animated bone movement, shape keys, groups, driver/
  constraint/NLA copies, sidecars and excluded-collection export scope.
- [Combined summary](summary.json). Archive CRC, Python syntax, metadata,
  export-version stamp, SHA-256 and exact source/ZIP parity pass.

The pre-fix shared export source reproduced `object.select_all.poll() failed,
context is incorrect` in Properties/Pose and Properties/Edit with original
names. Cleanup repeated the same invalid selection call. Scoped Object Mode
and data-API selection eliminate this failure.

These tests use generated fixtures and separate test-only installation/config
directories. Normal installed add-ons and user preferences were not changed.
Standard Blender 5.2.2 LTS and Bforartists 5.2.0 (Blender base 5.3.0 Alpha) were
used for their respective products. Real-window clicks, production avatars
and Unity/Unreal Editor acceptance remain unverified.

Run `blender_export_context.py` or `blender_export_naming.py` in the matching
host with `--background --factory-startup --python-exit-code 1 --python`, then
pass the ZIP/package-parent and an output directory after `--`. The context
script reuses fixture functions from the naming script; keep them together.
