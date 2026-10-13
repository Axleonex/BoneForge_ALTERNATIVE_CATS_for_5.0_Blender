# BoneForge shared interface adaptation

Approved by the owner on 2026-10-13; apply only to the local BoneForge project.

## Scope and layout

Use BoneCraft 9.1.3 as the layout reference for working tool overlaps. Keep the
BoneForge identity and standard Blender host support. Rig Builder contains the
manual-marker wizard, Quick Rig, and Mannequin, in that order. BoneForge keeps
its existing setup, weights, correctives, animation, and review tools. CATS
contains CATS cleanup, Avatar Tools, VRChat Tools, and Import / Export. Existing
naming, clothing, and performance panels move under VRChat Tools.

Native Add > Armature, Pose, and Weights menus expose existing operators. Scene
Properties optionally mirrors Rig Builder and the CATS sections. Sidebar tab
visibility must not hide Scene mirrors. Disabling a tool package removes its
mirrors, and re-enabling rebuilds them without duplicate registrations.

Only Blender-supported sidebar, menus, and Properties regions are used. No
Bforartists left Tool Shelf tabs, automatic detection, picker, mechanisms,
control rig builder, profile export, or other BoneCraft feature is introduced.
The disabled automatic joint-detection button is removed from the wizard UI.

## Visual treatment and experience

SUBJECT: BoneForge avatar preparation and existing rig tools.
TREATMENT: ui-tool; operated, with inherited operator behavior.
PALETTE: inherit Blender's active theme and semantic icon colors.
TYPE: inherit Blender's UI font, sizes, and native panel headers.
LAYOUT: existing tool inputs, actions, and folded options; one-column layout at
narrow widths and compact groups at wider widths. Helpers wrap to available
width. Panel headers contain text only.

First use shows what to select rather than hiding whole sections. Menu entries
only reference registered operators; package-disabled tools disappear from
menus. Compact Mode suppresses explanations without removing actions. Failures
retain the existing operator messages and undo behavior. Success means users
can reach the same working tools through familiar groups without new features.

## Acceptance

- Same registered operator IDs and implementations as local BoneForge 9.0.0.
- Shared panel/menu draws succeed on empty, mesh, and armature selections in
  standard Blender; narrow layouts and Scene mirrors retain helper methods.
- Sidebar hide preferences, package toggles, and register/unregister cycles
  preserve consistent panel access and leave no stale UI classes.
- Local 9.0.1 zip matches source, contains no Bforartists lockout, and keeps
  9.0.0 untouched. No remote publication or BoneCraft changes.

## Verification and deviations

Standard Blender 5.1.2: 604 recorded panel/menu draws pass, with the same 273
operators and unchanged execute/invoke/modal/poll bodies. Visibility, dependency
rejection, module toggle, reload, Quick Rig helpers, and seven languages pass.
Native Blender icons replace inherited unsupported icon names directly in the
shared panels. The CATS visibility preference and existing Object Data mirror
helper/registration issues were corrected as UI infrastructure.

R4 deviation: standard Blender has no Bforartists Tool Shelf tabs; native
menus/sidebar/Properties implement the approved layout. R1 deviation: existing
Quick Rig scene options remain the inputs to existing operators, preserving the
owner-requested behavior; this pass folds their presentation. R3 is checked for
the shared menu entries introduced here, not every untouched legacy operator.
R7 headers are text-only in the touched CATS/grouping panels. R10 empty-selection
root guidance and R12 narrow help/layout checks pass. Visible-window screenshot,
full legacy tooltip coverage, and Blender 4.0 runtime remain NOT VERIFIED.
