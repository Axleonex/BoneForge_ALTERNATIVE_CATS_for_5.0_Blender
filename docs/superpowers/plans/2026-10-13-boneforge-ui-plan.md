# BoneForge UI Adaptation Implementation Plan

> For the executing agent: execute task-by-task through the owner-required Prime code router. Native continuation is authorized by receipt 67d2fac622324978893fe4458a0daf5a.

**Goal:** Apply the approved BoneCraft layout to shared BoneForge tools locally.
**Architecture:** Reuse existing panel draw methods and operator IDs. Add small
Blender-native menu and Scene mirror modules, with lifecycle integration.
**Tech Stack:** Python, bpy, Blender 5.1, existing BoneForge translation layer.

## Task 1: Capture baseline

Record registered operator IDs in a factory-startup Blender session before
changes. Keep this evidence under .git. Record approved design and scope.

## Task 2: Add native UI infrastructure

Create core/ui_layout.py for width-aware text and operator availability. Create
core/access.py for Add/Armature, Pose and Weight menus using only existing IDs.
Create core/scene_tab_mirror.py sharing original panel methods, preserving all
helper methods and child hierarchy. Add show_scene_tab and lifecycle calls in
core/prefs.py, __init__.py, and core/tool_toggle_operator.py.

## Task 3: Match shared panel grouping

Update taskboard/sidebar.py: wizard first, folded Quick Rig options, compact
metarig grids, Avatar Tools root and VRChat Tools parent for existing naming,
clothing and performance panels. Move io_hub/panel.py into CATS; remove only
the unavailable detection UI button in autorig/wizard.py. Keep all operator
methods intact. Translate newly introduced visible strings in all seven
existing language dictionaries.

## Task 4: Verify in standard Blender

Create tests/blender_ui_layout.py. Check registered operator parity against
baseline, resolve menu entries via RNA, draw panels with a recording layout
at narrow and normal widths for empty/mesh/armature contexts, test hidden
sidebar tabs with visible Scene mirrors, and tool-toggle lifecycle. Check
syntax, host boundary, and unchanged operator method ASTs.

## Task 5: Deliver locally

Bump patch version to 9.0.1, update README and releases/README.md, package
releases/BoneForge-9.0.1.zip from source excluding caches. Verify CRC, source
parity and checksum. Local work-branch commit only; no push or merge.
