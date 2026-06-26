# BoneForge Documentation
### Version 7.1.3 | For VRChat Users

---

## Table of Contents

- [Getting Started](#getting-started)
  - [What is BoneForge?](#what-is-boneforge)
  - [Open Blender vs B4Artists Build Split](#open-blender-vs-b4artists-build-split)
  - [Installing BoneForge](#installing-boneforge)
  - [Finding BoneForge in Blender](#finding-boneforge-in-blender)
  - [Where Should I Start?](#where-should-i-start)
- [Quick Guides](#quick-guides)
  1. [Get Your First Avatar Into VRChat](#guide-1-get-your-first-avatar-into-vrchat)
  2. [Bring a VRoid Avatar into VRChat](#guide-2-bring-a-vroid-avatar-into-vrchat)
  3. [Bring an MMD Avatar into VRChat](#guide-3-bring-an-mmd-avatar-into-vrchat)
  4. [Fix Your Avatar's Bone Names](#guide-4-fix-your-avatars-bone-names)
  5. [Map Your Avatar to VRChat's Body System](#guide-5-map-your-avatar-to-vrchats-body-system)
  6. [Add Hair Physics](#guide-6-add-hair-physics)
  7. [Attach Clothing That Moves With Your Body](#guide-7-attach-clothing-that-moves-with-your-body)
  8. [Set Up Lip Sync](#guide-8-set-up-lip-sync)
  9. [Improve Your Avatar's Performance](#guide-9-improve-your-avatars-performance)
  10. [Save and Reuse Poses](#guide-10-save-and-reuse-poses)
  11. [Merge Two Rigs Together](#guide-11-merge-two-rigs-together)
  12. [Fix Upload Problems](#guide-12-fix-upload-problems)
  13. [Get Your Avatar VRChat-Ready with CATS](#guide-13-get-your-avatar-vrchat-ready-with-cats)
- [CATS Plugin — Before You Begin: The Pipeline Order](#cats-plugin--before-you-begin-the-pipeline-order)
- [Feature Reference](#feature-reference)
- [CATS Tool Reference](#cats-tool-reference)
- [Quick-Fix Index](#quick-fix-index)
- [Glossary](#glossary)

---

# Getting Started

## What is BoneForge?

BoneForge is a Blender add-on that helps you prepare 3D avatars for VRChat, VRoid/VRM, and MMD. Think of it as a helper toolkit that sits inside Blender and handles the complicated parts of getting your avatar's skeleton set up correctly.

**What Blender does:** Blender is the 3D software where you edit your avatar's shape, textures, and movement system before uploading to VRChat. It is free and powerful, but can feel confusing at first.

**What BoneForge adds:** BoneForge adds panels and buttons to Blender that automate the most tedious steps — things like organizing bones, fixing names, setting up physics, and exporting in the right format.

**New in 8.4.6:** The open Blender build is version-aligned with the B4Artists release while remaining the standard Blender package. It exposes the complete CATS Material Atlas UV variation set for the CATS/Material Combiner/UVToolkit workflow, including **Advanced Variation** and **Rotation Step**, but it does not include B4Artists-exclusive rigging, control picker, lockout, or host-specific content.

**New in 8.3.6:** Smart Combine now makes `atlas_uv` the export UV0 by default after baking. The pre-atlas source UV map is removed from the generated atlas mesh unless **Keep Source UV Maps** is enabled in Advanced settings.

**New in 8.3.5:** Smart Combine now forces source textures to sample the preserved pre-atlas UV during baking, validates the generated atlas mesh before hiding originals, and resets all atlas faces to the final atlas material slot to prevent gray or scrambled robe/clothing chunks.

**New in 8.3.4:** The CATS Material Atlas Combiner now adds quality-parity inspection controls before baking: shader/material diagnostics, texture role labels, duplicate/shared source markers, per-material size overrides, packing presets, optional Normal/Emission/Roughness output bakes, and preflight blockers for Metallic/ORM channel packing until that path is verified.

**New in 8.3.3:** The CATS Material Atlas Combiner now includes selectable UV packing methods in the existing Material Atlas workflow. Smart Pack, Grid Pack, Seeded Variation, Oriented Pack, and Fit 0-1 Bounds are available from Advanced settings, with UV method details recorded in the debug report and bake ledger.

**New in 8.3.2:** The CATS Material Atlas Combiner now analyzes selectable material and texture rows before baking. You can inspect the materials and image textures found in the active avatar, selected meshes, or visible scene, then disable individual materials or texture images before running Bake Atlas. This update also fixes a taskboard icon compatibility traceback and a Material Atlas bake context error that could appear when baking from the sidebar while a mesh was in Edit Mode.

**New in 7.1.3 (preference label cleanup):** Two add-on preference toggles were renamed so they now match the sidebar tab they control. "VRChat Avatar Tools" is now labelled **CATS** (matches the CATS sidebar tab). "Task Board & Sidebar" is now labelled **Rig Builder** (matches the Rig Builder sidebar tab). No tools were removed — only the on/off labels in Edit > Preferences > Add-ons > BoneForge changed.

**New in 7.1.1:** BoneForge now includes the **CATS Plugin** — a complete suite of model preparation tools specifically designed for getting VRChat avatars clean, optimized, and fully configured. CATS lives in its own sidebar tab and uses a pipeline system that guides you through the right order of operations every time.

**What BoneForge cannot do:**
- It cannot model or sculpt your avatar's body shape
- It cannot create textures or materials from scratch
- It cannot upload to VRChat directly (you still need the VRChat Creator Companion / SDK)

---

## Open Blender vs B4Artists Build Split

BoneForge has two 8.4.6 builds with different package boundaries. Matching
version numbers do not mean the same payload.

| Area | Open Blender BoneForge 8.4.6 | BoneForge BFA 8.4.6 |
| --- | --- | --- |
| Host | Standard Blender | Bforartists only |
| Add-on identity | `BoneForge` | `BoneForge BFA` |
| Repository | `Axleonex/BoneForge_ALTERNATIVE_CATS_for_5.0_Blender` | `Axleonex/BoneForge_B4Artists` |
| Release zip | `BoneForge-8.4.6.zip` | `BoneForge-BFA-8.4.6.zip` |
| CATS avatar cleanup | Included | Included |
| Material Combiner | Included | Included |
| UVToolkit-derived Material Combiner controls | Included, including Advanced Variation and Rotation Step | Included, same CATS / Material Combiner / UVToolkit behavior |
| Basic BoneForge and Mixamo-style avatar helpers | Included | Included |
| BFA host lockout | Not included | Included |
| Production control-rig construction | Not included | B4Artists-exclusive |
| Smart landmark / joint detection suite | Not included as a BFA production suite | B4Artists-exclusive |
| Animator control layer | Not included | B4Artists-exclusive |
| Control Picker / rig UI | Not included | B4Artists-exclusive |
| Advanced retargeting core and source maps | Not included as a BFA production suite | B4Artists-exclusive |
| Profile-driven game export | Not included as a BFA production suite | B4Artists-exclusive |
| BFA marker files | Must not contain `bfa_guard.py` or `BFA_EXCLUSIVE.md` | Must contain `bfa_guard.py` and `BFA_EXCLUSIVE.md` |

The open Blender build is the non-exclusive standard-Blender package. It now
receives the complete CATS, Material Combiner, and UVToolkit-derived workflow.
The B4Artists build remains the exclusive package for the production rigging
suite, host lockout, control rig builder, animator controls, control picker,
advanced retarget/export systems, and Bforartists-specific packaging.

---

## Installing BoneForge

**What you need before starting:**
- Blender 4.0 or newer (download free at blender.org)
- The BoneForge `.zip` file

**Steps:**

1. Open Blender
2. Go to **Edit > Preferences** (top menu bar)
3. Click **Add-ons** on the left side
4. Click **Install from Disk** (top right of the Add-ons panel)
5. Navigate to your BoneForge `.zip` file and select it
6. Click **Install Add-on**
7. Find "BoneForge" in the add-on list and check the checkbox to enable it
8. Click the arrow next to BoneForge to expand its settings — you can choose which tools to enable

**You should see:** A new panel called "BoneForge" appear in the right sidebar of the 3D viewport (press **N** to open/close the sidebar). You will also see a separate **CATS** tab in the same sidebar.

---

## Finding BoneForge in Blender

When BoneForge is installed, here is where everything lives:

**The Sidebar (most common):** Press **N** in the 3D viewport to open a panel on the right side. You will see tabs including BoneForge's tools organized by task.

**Tabs you will use most:**
- **Rig Builder** — Build a new rig from scratch
- **Setup Rigging** — Retargeting and Rigify tools
- **Skin** — Weight and deformation tools
- **VRChat** — Everything for VRChat export
- **Review / Animate** — Bone visibility, pose library, validation
- **CATS** — Model cleanup, visemes, eye tracking, and full VRChat prep pipeline *(new in 7.1.1)*

**The CATS tab is a separate tab** from the main BoneForge tabs. Scroll down the sidebar tab list if you do not see it immediately — it appears after the BoneForge tabs.

**Fix Model First, Every Time:** When using the CATS tab, always start with **Fix Model** before running any other CATS tool. The CATS pipeline uses a Ledger to track which steps you have completed. Each tool checks the Ledger and will warn you if you try to run it out of order. See [CATS Plugin — Before You Begin: The Pipeline Order](#cats-plugin--before-you-begin-the-pipeline-order) for the full explanation.

**The N-Panel Hotkey:** You can press **Ctrl+Shift+R** in the 3D viewport to pop up BoneForge's quick panel wherever your cursor is, without navigating to the sidebar.

---

## Where Should I Start?

Choose the description that best fits you:

> **"You are a person who has a brand new 3D model file (FBX, OBJ, or Blender file) and wants to rig it for VRChat from scratch."**
> → Go to [Guide 1: Get Your First Avatar Into VRChat](#guide-1-get-your-first-avatar-into-vrchat)

> **"You are a person who made your avatar in VRoid Studio and exported a VRM file."**
> → Go to [Guide 2: Bring a VRoid Avatar into VRChat](#guide-2-bring-a-vroid-avatar-into-vrchat)

> **"You are a person who has an MMD model (PMX file) and wants to use it in VRChat."**
> → Go to [Guide 3: Bring an MMD Avatar into VRChat](#guide-3-bring-an-mmd-avatar-into-vrchat)

> **"You are a person who already has a rigged avatar but it won't upload because the bones have wrong names."**
> → Go to [Guide 4: Fix Your Avatar's Bone Names](#guide-4-fix-your-avatars-bone-names)

> **"You are a person who has a rigged avatar and wants to get it fully VRChat-ready — lip sync, eye tracking, clean mesh, all at once."**
> → Go to [Guide 13: Get Your Avatar VRChat-Ready with CATS](#guide-13-get-your-avatar-vrchat-ready-with-cats)

> **"You are a person who wants to fix a specific problem."**
> → Go to the [Quick-Fix Index](#quick-fix-index)

---

# Quick Guides

---

## Guide 1: Get Your First Avatar Into VRChat

> **Time:** About 45–60 minutes for a complete first run
> **Result:** A fully rigged, VRChat-ready avatar exported as an FBX file

**Before you begin — check these:**
- [ ] Your 3D model is imported into Blender (File > Import, choose your format)
- [ ] The model is in a T-pose (arms out to the sides, body upright) — or close to it
- [ ] The model has no obvious broken geometry (no random floating triangles)
- [ ] You can see your model in the 3D viewport as a solid grey shape

---

### Step 1 — Open the Rig Builder

In the right sidebar (press **N** if it is not visible), click the **Rig Builder** tab. You will see three options: Quick Rig, Wizard, and Mannequin.

Click **Wizard** to start the guided rigging process.

**What you should be seeing:** A panel that says "Start" with a button to begin the wizard.

---

### Step 2 — Start the Wizard and Select Your Mesh

Click **Start Wizard**. The wizard will ask you to select your mesh (your avatar's 3D body shape).

Click on your avatar in the 3D viewport to select it, then click **Confirm Selection** in the wizard panel.

**What you should be seeing:** The wizard advances to a screen showing "Rig Type."

> **Rig type** = the style of skeleton BoneForge will create. For VRChat avatars that look like humans, choose **Human**.

---

### Step 3 — Set Finger Count

The wizard asks how many fingers your avatar has on each hand. For a standard human avatar, this is **5 per hand**. If your avatar has fewer or stylized hands, adjust accordingly.

---

### Step 4 — Place Body Markers

This is the most important step. You are placing dot markers on your avatar to show BoneForge where each major body part is located. Think of it like pinning a map — you are telling BoneForge "the pelvis is here, the head is here," and BoneForge figures out all the bone positions from those pins.

**How to place a marker:**
1. Select the marker name from the list (e.g., "Pelvis")
2. Click **Place Marker**
3. Click on the correct spot on your avatar in the 3D viewport
4. The marker dot turns **green** when confirmed

**Tip — Use Auto-Detect:** Click **Guess Body Markers** and BoneForge will attempt to place all markers automatically based on your mesh shape. Check that each marker is green and in a reasonable position. You can click any marker and use **Move Marker** to adjust.

**Tip — Use Symmetry:** Enable **Mirror** to automatically place the right-side marker whenever you place a left-side marker. This saves time for arms, legs, shoulders, and feet.

**Required markers (15 total):** Pelvis, three spine points, neck, head, both shoulders, both upper arms, both forearms, both hands, both thighs, both shins, both feet.

**What you should be seeing:** All 15 markers showing green dots on your avatar.

---

### Step 5 — Place Face Markers (Optional)

If your avatar has a face that you want to animate (blinking, expressions, lip sync), place the face markers too. These are optional but strongly recommended for VRChat.

Click **Guess Face Markers** for automatic placement, then adjust as needed.

---

### Step 6 — Place Finger Markers

Click **Guess Finger Markers** for automatic finger placement. BoneForge will trace each finger chain from knuckle to fingertip.

---

### Step 7 — Review and Generate

Click **Next** to reach the Review screen. BoneForge shows a summary of what it is about to create. Click **Generate Rig**.

**What you should be seeing:** BoneForge creates a skeleton (shown as orange bones) inside your avatar. Your avatar's skin should be automatically attached to the skeleton so it deforms when you move the bones.

> **Skin/weight painting** = the process of deciding which parts of your avatar's mesh follow which bones. BoneForge handles this automatically in the initial pass, but you can refine it later using the Weight Tools (see Feature Reference).

---

### Step 8 — Fix Bone Names for VRChat

After generating, your bones need to follow VRChat's naming rules. Go to the **VRChat** tab in the sidebar and click **Fix Bone Names > Auto-Detect and Rename**.

**What you should be seeing:** All bones in the list show green checkmarks.

---

### Step 9 — Map to VRChat Humanoid

Still in the VRChat tab, find the **Humanoid Mapper** section. Click **Auto-Map Humanoid**. This connects each of your avatar's bones to VRChat's humanoid system (the system VRChat uses to make avatars move in sync with your real-world movements).

Run **Validate Humanoid** to check for any remaining issues.

**What you should be seeing:** A list of humanoid slots (Hips, Spine, Head, etc.) each showing a bone name next to it.

---

### Step 10 — Export for VRChat

Go to the **VRChat** tab → **Export** section. Click **Export to VRChat (FBX)**.

Choose a save location and click **Export**.

**What you should be seeing:** A `.fbx` file saved to your chosen location. This file is what you import into the VRChat Creator Companion.

---

**What This Unlocks:** You now have a fully rigged VRChat avatar file. From here you can add hair physics (Guide 6), attach clothing (Guide 7), set up lip sync (Guide 8), and optimize performance (Guide 9). For a one-stop cleanup and VRChat configuration workflow using the new CATS tools, see Guide 13.

---

## Guide 2: Bring a VRoid Avatar into VRChat

> **Time:** About 15–25 minutes
> **Result:** Your VRoid `.vrm` file ready for VRChat export

**Before you begin — check these:**
- [ ] You have exported your avatar from VRoid Studio as a `.vrm` file
- [ ] BoneForge is installed and enabled
- [ ] The VRM bridge add-on is installed (see below)

---

### Step 1 — Install the VRM Bridge

BoneForge needs a helper add-on to open VRM files. In the BoneForge sidebar, go to the **VRM** section and click **Install VRM Add-on Automatically**. If that fails, click **Open VRM Website** to download the official VRM add-on manually and install it the same way you installed BoneForge.

---

### Step 2 — Import Your VRM File

Go to **File > Import > VRM (.vrm)** and select your VRoid file.

**What you should be seeing:** Your VRoid character appears in Blender with its skeleton already in place.

---

### Step 3 — Auto-Map to VRChat Humanoid

Go to the **VRChat** tab in the BoneForge sidebar. Click **Auto-Map Humanoid**. VRoid avatars follow a standard skeleton format, so this usually completes automatically without any manual adjustments.

---

### Step 4 — Fix Bone Names

Click **Fix Bone Names > Auto-Detect and Rename**. VRoid uses its own naming system; this converts the names to what VRChat expects.

---

### Step 5 — Set Up Visemes (Lip Sync)

VRoid avatars already have blend shapes (the face movements for expressions and lip sync) built in. Go to the **VRChat** tab → **Visemes** and click **Auto-Map Visemes**. BoneForge will match VRoid's shape keys to VRChat's 15 lip-sync phonemes automatically.

---

### Step 6 — Export

Click **Export to VRChat (FBX)** in the VRChat Export section.

**What This Unlocks:** Your VRoid avatar is now ready to import into the VRChat Creator Companion. You can also add hair physics (Guide 6) and optimize performance (Guide 9) before uploading.

---

## Guide 3: Bring an MMD Avatar into VRChat

> **Time:** About 20–30 minutes
> **Result:** Your MMD `.pmx` model ready for VRChat

**Before you begin — check these:**
- [ ] You have a `.pmx` or `.pmd` MMD model file
- [ ] BoneForge is installed
- [ ] The MMD Tools add-on is installed (see Step 1)

---

### Step 1 — Install MMD Tools

In the BoneForge sidebar, scroll to the **MMD** section and click **Install MMD Tools Automatically**. If that fails, click **Open MMD Website** to download MMD Tools manually.

---

### Step 2 — Import Your PMX File

Go to **File > Import > MikuMikuDance Model (.pmx/.pmd)** and select your model.

**What you should be seeing:** Your MMD character appears in Blender with Japanese-style bone names.

---

### Step 3 — Fix Bone Names

MMD uses Japanese bone names that VRChat cannot understand. In the **VRChat > Naming** section, click **Detect Convention**. BoneForge will recognize the MMD naming style. Then click **Translate Bone Names** to convert them to VRChat-compatible names.

Alternatively, use the **CATS tab → Bone Name Translation** tool, which supports automatic language detection for Japanese, Chinese, Korean, Portuguese, Spanish, and French bone names in a single click.

---

### Step 4 — Clean Up the Model

MMD models often have extra geometry and duplicate vertices. Go to **VRChat > Cleanup** and click:
- **Fix Model** — removes problem geometry
- **Join Meshes** — combines body parts into one mesh (recommended for VRChat)
- **Remove Unused Vertex Groups** — removes empty bone assignments

For a guided, pipeline-ordered version of this cleanup, use the **CATS tab** and follow the pipeline order described in [Guide 13](#guide-13-get-your-avatar-vrchat-ready-with-cats).

---

### Step 5 — Map to VRChat Humanoid

Click **Auto-Map Humanoid** in the VRChat Humanoid section. MMD's skeleton is similar to VRChat's, so most slots fill automatically. Fix any unmatched slots manually by clicking the slot and choosing the correct bone from the dropdown.

---

### Step 6 — Export

Click **Export to VRChat (FBX)**.

**What This Unlocks:** Your MMD avatar is now ready for VRChat. You can add hair physics (Guide 6) and set up lip sync (Guide 8) before uploading.

---

## Guide 4: Fix Your Avatar's Bone Names

> **Time:** About 5–15 minutes
> **Result:** All bones renamed to VRChat-compatible names

**Before you begin — check these:**
- [ ] Your avatar is open in Blender with its skeleton (armature) visible
- [ ] You know roughly what naming format your avatar uses (e.g., Mixamo, VRoid, Unity, custom)

---

### Step 1 — Detect Current Naming Style

Go to the **VRChat** tab → **Naming** section. Click **Detect Convention**. BoneForge will analyze your bone names and show you what style it detected (Mixamo, Ready Player Me, Unity, or Custom).

For models with bone names in Japanese, Chinese, Korean, Portuguese, Spanish, or French, use the **CATS tab → Bone Name Translation** tool instead. It auto-detects the source language and converts everything to English VRChat names in one step.

---

### Step 2 — Auto-Translate (Recommended)

If BoneForge detected a known naming style, click **Translate Bone Names**. This renames everything automatically.

**What you should be seeing:** The bone list shows VRChat-compatible names like `Hips`, `Spine`, `Chest`, `LeftUpperArm`, etc.

---

### Step 3 — Manual Fixes (If Needed)

If some bones were not automatically renamed, use the tools in the **Batch Rename** section:

- **Find and Replace** — Type the old text in the left box, the new text in the right box, click Apply
- **Add Prefix** — Adds text to the start of all bone names (e.g., turning `Arm` into `Left_Arm`)
- **Add Suffix** — Adds text to the end of all bone names
- **Remove Prefix / Remove Suffix** — Strips added text

---

### Step 4 — Save as a Preset (Optional)

If you have a custom avatar with unique naming, click **Save Custom Preset** after getting everything named correctly. This saves your naming rules so you can apply them instantly to future avatars.

**What This Unlocks:** Correct bone names allow the Humanoid Mapper (Guide 5) to work automatically. Without correct names, VRChat's avatar system cannot recognize how your character should move.

---

## Guide 5: Map Your Avatar to VRChat's Body System

> **Time:** About 10–15 minutes
> **Result:** Your avatar's skeleton connected to VRChat's humanoid movement system

**Before you begin — check these:**
- [ ] Your avatar's bones are named correctly (see Guide 4 if not)
- [ ] Your avatar is in Blender with its skeleton selected
- [ ] You are in **Object Mode** (check the dropdown in the top-left of the viewport)

---

### Step 1 — Open the Humanoid Mapper

Go to the **VRChat** tab → **Humanoid** section.

---

### Step 2 — Auto-Map

Click **Auto-Map Humanoid**. BoneForge scans your skeleton and fills in the required body slots automatically.

> A **humanoid slot** is like a labeled hook that VRChat uses: "Hips goes here, Head goes here, Left Hand goes here." BoneForge matches your bones to these hooks.

**What you should be seeing:** A list of slots (Hips, Spine, Chest, Neck, Head, LeftUpperArm, etc.) each with a bone name filled in next to it.

---

### Step 3 — Check for Errors

Click **Validate Humanoid**. BoneForge checks all required slots are filled and the hierarchy makes sense.

- **Green** = correct
- **Yellow** = warning (not required but recommended)
- **Red** = error (must fix before export)

---

### Step 4 — Fix Errors Manually

If any red errors appear, click the error message. BoneForge will highlight the problem bone. Use the dropdown next to the slot to select the correct bone manually.

---

### Step 5 — Set Up Eye Tracking (Optional)

If your avatar has eye bones, go to the **Eye Setup** section. Click **Fix Eye Bones** to ensure both eye bones are named and positioned correctly. Click **Auto-Map Blink Shapes** to connect your blink animations.

For a more complete eye tracking setup including constraint creation and VRChat LeftEye/RightEye bone naming, use the **CATS tab → Eye Tracking Setup** tool described in [Guide 13, Phase 3](#phase-3--eye-tracking).

**What This Unlocks:** Once humanoid mapping is complete, your avatar will move properly in VRChat — IK (inverse kinematics, the system that makes your in-game hands follow your real controllers) will work, and your avatar will track your real-world movements correctly.

---

## Guide 6: Add Hair Physics

> **Time:** About 15–25 minutes
> **Result:** Your avatar's hair (and any soft accessories) bouncing and swaying naturally in VRChat

**Before you begin — check these:**
- [ ] Your avatar has hair bones already in the skeleton (bones that form chains from the scalp outward)
- [ ] Your avatar is open in Blender with the skeleton selected

> **PhysBone** = VRChat's name for a component that makes bones bounce and swing as if they have weight. BoneForge creates these automatically from your hair bone chains.

---

### Step 1 — Detect Hair Chains

Go to the **VRChat** tab → **Hair Physics** section. Click **Detect Hair Chains**.

BoneForge scans your skeleton for chains of bones that look like hair (multiple bones chained end-to-end, branching from a root). It lists all the chains it found.

**What you should be seeing:** A list of chain names, each with a start bone and a number of chain links.

---

### Step 2 — Review Detected Chains

Look through the list. If BoneForge detected something that is not hair (like a tail bone you want to handle separately, or a belt chain), you can remove it from the list by clicking the minus button next to it.

---

### Step 3 — Choose a Physics Preset

Select a preset that matches how you want your hair to feel:
- **Stiff** — Hair that barely moves, like a helmet or rigid braid
- **Normal** — Natural flowing hair with moderate bounce
- **Bouncy** — Very loose, floaty hair with lots of movement

---

### Step 4 — Generate PhysBone Components

Click **Generate Hair PhysBones**. BoneForge creates the physics components on all detected chains using your chosen preset.

**What you should be seeing:** Each hair chain in the list now shows a physics icon.

---

### Step 5 — Fine-Tune Physics (Optional)

Click on any chain in the list and use the sliders to adjust:
- **Stiffness** — How much the bone resists bending (higher = stiffer)
- **Damping** — How quickly the swinging slows down (higher = less bouncy, more floaty)
- **Gravity** — How much the hair pulls downward (negative values pull upward)
- **Drag** — Air resistance (higher = slower, smoother movement)
- **Collision Radius** — How thick the physics collision zone around each bone is

---

### Step 6 — Add Colliders (Recommended)

Colliders are invisible shapes that prevent hair from clipping through your avatar's head and body. Click **Place Default Colliders** to automatically add standard collision shapes to your head, shoulders, and chest.

**What you should be seeing:** Small sphere or capsule shapes appearing around your avatar's head and upper body.

---

### Step 7 — Preview (Optional)

Click **Play Physics Preview** to simulate the hair movement in Blender's viewport. Click **Stop** when done.

**What This Unlocks:** Your avatar's hair will now move naturally in VRChat when you turn your head, jump, or dance. You can apply the same process to tails, dangling accessories, or any other chain of bones you want to swing freely.

---

## Guide 7: Attach Clothing That Moves With Your Body

> **Time:** About 20–30 minutes
> **Result:** Clothing mesh fully attached to your avatar's skeleton, moving correctly with your body

**Before you begin — check these:**
- [ ] Your base avatar is open in Blender and has a completed skeleton
- [ ] Your clothing item is imported into the same Blender file as a separate mesh object
- [ ] The clothing roughly fits around your avatar's body (it does not need to be perfect)

---

### Step 1 — Open Clothing Tools

Go to the **VRChat** tab → **Clothing** section.

---

### Step 2 — Add Your Clothing to the List

Click **Add Clothing Item** and select your clothing mesh from the dropdown. Repeat for each clothing piece you want to attach.

---

### Step 3 — Match Bones

Click **Match Bones** with your clothing item selected. BoneForge compares your clothing's skeleton (if it has one) to your base avatar's skeleton and creates a mapping between them.

If your clothing came with its own skeleton, BoneForge tries to find the equivalent bone in your base skeleton. For example, a "left arm" bone in the clothing skeleton gets matched to your avatar's left arm bone.

**What you should be seeing:** A list of bone pairs showing clothing bone → avatar bone.

---

### Step 4 — Review and Fix Mismatches

Any unmatched bones appear in yellow. For each unmatched bone, click the dropdown next to it and manually select the closest bone from your base skeleton.

For clothing without its own skeleton, skip this step.

---

### Step 5 — Merge Clothing

Click **Merge Clothing**. BoneForge transfers the clothing mesh's weights (the assignments that decide which bones move which part of the mesh) to your base skeleton.

> **Weights** (also called weight painting) = numbers that tell each vertex (point) of your mesh how much it should be moved by each bone. If your left sleeve has weight on the left arm bone, moving the left arm bone will pull the sleeve with it.

**What you should be seeing:** Your clothing is now listed under your main avatar skeleton in the scene. Moving a skeleton bone should move both the body and the clothing together.

---

### Step 6 — Check for Clipping

Use the **Detect Collisions** button to scan for areas where the clothing mesh is poking through the body mesh. Adjust colliders or refine weights in problem areas.

**What This Unlocks:** Your avatar now has clothing that moves naturally with your body. You can repeat this process for each outfit piece. For advanced weight adjustments, see the Weight Tools section in the Feature Reference.

---

## Guide 8: Set Up Lip Sync

> **Time:** About 10–20 minutes
> **Result:** Your avatar's mouth moving correctly when you speak in VRChat

**Before you begin — check these:**
- [ ] Your avatar's head mesh has mouth shape keys (also called blend shapes or morph targets — these are the different mouth positions for speaking)
- [ ] You know roughly what the shape keys are named (check the Shape Keys panel in Blender's Properties panel on the right side)

> **Viseme** = a specific mouth shape that corresponds to a sound. "AA" is for the "ahh" sound, "OH" is for the "ohhh" sound, etc. VRChat needs 15 specific visemes to drive your avatar's lip sync.
>
> **Shape key / blend shape** = a saved version of your mesh in a different position. Your mouth-open shape key is a saved version of your mesh with the mouth open.

---

### Step 1 — Open the Viseme Mapper

Go to the **VRChat** tab → **Visemes** section.

---

### Step 2 — Auto-Map Visemes

Click **Auto-Map Visemes**. BoneForge scans your mesh's shape keys and tries to match them to VRChat's 15 phoneme slots by name.

**What you should be seeing:** Most of the 15 phoneme slots filled with shape key names.

---

### Step 3 — Fill in Missing Slots

For any empty phoneme slots, click the dropdown next to the slot and select the closest matching shape key from your mesh. Common matches:

| VRChat Phoneme | What it sounds like | Shape key to look for |
|---|---|---|
| `aa` | "ahh" | mouth_open, A, aa |
| `oh` | "ohh" | mouth_o, OH, oh |
| `ch` | "ch" / "sh" | mouth_ch, CH |
| `mm` | lips together (M, B, P) | mouth_m, MM, lips_together |
| `ss` | "sss" / "zzz" | mouth_s, SS |

**Alternative — CATS Viseme Generator:** If your avatar does not have existing viseme shape keys, use the **CATS tab → Viseme Generator** to create all 15 VRChat visemes from scratch using just three base shapes (A, O, CH). See [Guide 13, Phase 2](#phase-2--viseme-generation) for a step-by-step walkthrough.

---

### Step 4 — Preview a Viseme

Click any phoneme name to preview what that mouth shape looks like on your avatar. Click it again to return to neutral.

---

### Step 5 — Set Up Face Tracking (Optional)

If you want VRChat's face tracking to work with your avatar, enable **Face Tracking** in the Face Tracking section and adjust the expression smoothing slider.

**What This Unlocks:** Your avatar's mouth will now move when you talk in VRChat, making you look far more natural in conversations. Expression and emotion systems build on top of the shape keys you just mapped.

---

## Guide 9: Improve Your Avatar's Performance

> **Time:** About 15–25 minutes
> **Result:** Avatar with a better VRChat performance rating and faster loading time for other players

**Before you begin — check these:**
- [ ] Your avatar is complete (rigged, clothed, lip sync set up)
- [ ] You know your target performance tier (Good or Excellent for most users)

> **Performance rank** = VRChat's rating system for how demanding your avatar is. Very Poor avatars may be hidden by other players. Good or Excellent avatars load fast and are always visible.

---

### Step 1 — Check Current Performance Rank

Go to the **VRChat** tab → **Performance** section. Click **Calculate Rank**. BoneForge shows your current estimated rank and the specific numbers causing it (polygon count, material count, bone count, etc.).

---

### Step 2 — Clean Up the Mesh

In the **Cleanup** section, run these in order:

1. **Fix Model** — Removes duplicate geometry and fixes common mesh errors
2. **Remove Unused Shape Keys** — Deletes blend shapes that are not mapped to anything (frees memory)
3. **Remove Unused Vertex Groups** — Removes empty bone weight assignments
4. **Remove Zero-Weight Bones** — Deletes bones that do not move any part of the mesh

---

### Step 3 — Reduce Polygon Count (If Needed)

If your polygon count is too high, use the **Decimation** tool:

1. Move the **Decimation Ratio** slider (0.5 = halve the polygon count, 0.8 = remove 20%)
2. Click **Preview Decimation** to see the result without committing
3. Click **Apply Decimation** when you are happy with the result

> Start at 0.8 and work downward — small reductions rarely affect visible quality but can significantly improve performance.

---

### Step 4 — Merge Materials (Optional)

If your avatar uses many different materials (color zones, texture sheets), use the **Material Atlas** section to combine them:

1. Click **Analyze** to see your current material layout
2. Click **Add Group** to create groups of materials to merge
3. Choose your atlas resolution (2048 recommended for most avatars)
4. Click **Bake Atlas** — BoneForge combines the materials into one texture sheet
5. Click **Accept** to apply, or **Revert** if you are not happy with the result

The CATS tab's **Material Atlas Combiner** offers the same Accept/Revert workflow in a streamlined interface — see [CATS Tool Reference: Material Atlas Combiner](#material-atlas-combiner).

---

### Step 5 — Recalculate Rank

Click **Calculate Rank** again to see your improved performance score.

**What This Unlocks:** A better performance rank means more players will see your avatar without it being blocked. An Excellent or Good avatar loads quickly, consumes less GPU, and is always visible to other players by default.

---

## Guide 10: Save and Reuse Poses

> **Time:** About 5–10 minutes
> **Result:** A saved library of poses you can apply to your avatar with one click

**Before you begin — check these:**
- [ ] Your avatar has a completed skeleton in Blender
- [ ] You are in **Pose Mode** (click your armature, then press **Ctrl+Tab** and choose Pose Mode from the menu, or use the dropdown in the top-left of the viewport)

---

### Step 1 — Open the Pose Library

Go to the **Review** tab in the BoneForge sidebar and find the **Pose Library** section.

---

### Step 2 — Pose Your Avatar

Move your avatar's bones into the position you want to save. Rotate arms, tilt the head — any combination of bone positions becomes a pose.

---

### Step 3 — Save the Pose

Click **Save Pose**. A dialog appears asking for a name and category. Type something descriptive (e.g., "Peace Sign" or "Thinking") and an optional category (e.g., "Greetings", "Action").

Click **OK**. A thumbnail of the current viewport is captured automatically.

---

### Step 4 — Apply a Saved Pose

Click the thumbnail image of any saved pose in the Pose Library panel. Click **Apply Pose** to snap your avatar to that position.

- **Apply Blended** — Applies the pose at partial strength (a slider from 0% to 100%), great for mixing two poses together
- **Apply Mirrored** — Applies the pose flipped left-to-right, giving you a matching pose for the other side

---

### Step 5 — Export and Import Poses

Click **Export Poses** to save your pose library to a `.bfpose` file — a small file you can keep with your project or share with others. Click **Import Poses** to load poses from a `.bfpose` file.

**What This Unlocks:** A personal pose library you can use across projects. You can build a full set of reference poses, blend between them for animation keyframing, or share poses with other BoneForge users.

---

## Guide 11: Merge Two Rigs Together

> **Time:** About 25–40 minutes depending on complexity
> **Result:** Two separate skeletons combined into one, with all weights preserved

**Before you begin — check these:**
- [ ] Both the base avatar and the secondary character (clothing rig, accessory rig, etc.) are in the same Blender file
- [ ] Both have been rigged and weighted

> **Rig merge** = the process of absorbing one skeleton into another so you end up with a single combined skeleton. Useful when you have a body rig and a hair/outfit rig that need to become one.

---

### Step 1 — Open Bone Merge

Go to the **Review** tab → **Bone Merge** section. Or find it in the sidebar's Bone Merge tab.

---

### Step 2 — Stage 1: Analyze

Select your **Target Armature** (the main skeleton that will survive) and your **Source Armature** (the secondary skeleton being absorbed).

Click **Analyze**. BoneForge compares the two skeletons and creates a diff table showing:
- ✓ **Matched** — bones that exist in both and align correctly
- **+** **Source Only** — bones from the secondary skeleton with no match in the main skeleton
- **−** **Target Only** — bones in the main skeleton not found in the secondary

Click **Acknowledge** after reviewing. This unlocks Stage 2.

---

### Step 3 — Stage 2: Resolve Names

For each **Source Only** bone (marked with +), you need to decide what to do with it:

- **Rename it** to match an existing bone in the main skeleton if they serve the same purpose
- **Mark as Unique** if it is a new bone that has no equivalent (it will be added to the main skeleton as-is)

Click **Normalize** to automatically rename all the standard bones (spine, arms, legs, etc.) that BoneForge recognizes.

For bones BoneForge cannot recognize, click **Propose** to get a suggested name based on the bone's position, then adjust manually.

Click **Verify** when all Source Only bones are resolved. This unlocks Stage 3.

---

### Step 4 — Stage 3: Merge

Click **Dry Run** first. This shows you a preview of what the merge will do without making any changes. Review the report.

When satisfied, click **Execute Merge**. BoneForge automatically creates a backup of both armatures before merging, then combines them.

**What you should be seeing:** One armature in your scene containing all bones from both skeletons, with all meshes properly weighted.

**What This Unlocks:** A single unified rig that is easier to export, edit, and work with. Required for any avatar that has separate clothing or accessory rigs.

---

## Guide 12: Fix Upload Problems

> **Time:** About 5–15 minutes depending on the issue

**Before you begin:** Identify your specific problem from the list below and jump to that section.

---

### "Upload failed — bones not recognized"

Your bones have names VRChat does not understand. → Go to [Guide 4: Fix Your Avatar's Bone Names](#guide-4-fix-your-avatars-bone-names)

---

### "Avatar is in T-pose / not moving with me in VRChat"

The humanoid mapping is missing or incorrect. → Go to [Guide 5: Map Your Avatar to VRChat's Body System](#guide-5-map-your-avatar-to-vrchats-body-system)

---

### "Mesh is deforming weirdly / skin stretching wrong"

The bone weights need adjustment. → See **Weight Transfer** and **Weight Mirror** in the [Feature Reference](#feature-reference).

---

### "Hair is clipping through the head"

Hair colliders are missing or too small. → Go to [Guide 6: Add Hair Physics](#guide-6-add-hair-physics), Step 6.

---

### "Avatar is Very Poor performance and being blocked by other players"

→ Go to [Guide 9: Improve Your Avatar's Performance](#guide-9-improve-your-avatars-performance)

---

### "Lip sync not working"

Visemes are not mapped correctly. → Go to [Guide 8: Set Up Lip Sync](#guide-8-set-up-lip-sync)

---

### "Rig validator shows red errors"

Go to the **Review** tab → **Rig Validator** section. Click **Run Validation**. For each red error, click the error message — BoneForge selects the problem bone for you. Read the error description and follow its suggestion, or check the [Quick-Fix Index](#quick-fix-index).

---

### "VRM import not working"

The VRM bridge add-on may not be installed. → Go to [Guide 2](#guide-2-bring-a-vroid-avatar-into-vrchat), Step 1.

---

### "MMD import not working"

The MMD Tools add-on may not be installed. → Go to [Guide 3](#guide-3-bring-an-mmd-avatar-into-vrchat), Step 1.

---

## Guide 13: Get Your Avatar VRChat-Ready with CATS

> **Time:** About 20–35 minutes for a full pipeline run
> **Result:** A clean, optimized avatar with lip sync, eye tracking, and correct transforms — ready for VRChat upload

**Before you begin — read this first:**

The CATS tools use a **Pipeline** system. Each phase must be completed in the correct order. The CATS sidebar shows a **Ledger** — a row of checkmarks that tracks which phases you have completed. A grayed-out tool means its required earlier step has not been checked off yet.

**Always start with Fix Model. Every time. Without exception.**

Read [CATS Plugin — Before You Begin: The Pipeline Order](#cats-plugin--before-you-begin-the-pipeline-order) before continuing if you have not already.

**Before you begin — check these:**
- [ ] Your avatar is imported into Blender and visible in the 3D viewport
- [ ] The CATS tab is visible in the N-panel sidebar (press N if the sidebar is hidden)
- [ ] Your avatar is selected (click it in the viewport or the outliner)

---

### Phase 1 — Fix Model

The Fix Model step is the mandatory foundation for everything else in CATS. Run it first, even if your model looks fine. It removes hidden problems that would otherwise silently break the tools that come after.

**What Fix Model does:**
- Removes duplicate vertices
- Removes loose geometry (disconnected triangles floating away from the body)
- Recalculates surface normals (the directions that determine which side of the mesh faces outward)
- Cleans up degenerate faces (triangles collapsed to a line or a point)
- Applies any un-applied scale or rotation that would confuse later tools

**Steps:**
1. In the **CATS** tab, find the **Fix Model** button at the top of the panel
2. Make sure your avatar's mesh is selected in the viewport
3. Click **Fix Model**
4. Wait for the operation to complete — for large meshes this may take a few seconds
5. Check that the **Ledger** now shows a checkmark (✓) next to Fix Model

**What you should be seeing:** Your avatar looks identical or very slightly cleaner. The Ledger's first slot now shows ✓. Previously grayed-out tools in the CATS panel are now available.

> **If your model disappears or looks inside-out after Fix Model:** Your mesh's normals were inverted. In Blender, select the mesh, enter Edit Mode (Tab), select all faces (A), then go to Mesh > Normals > Flip to correct it. Then re-run Fix Model.

---

### Phase 2 — Viseme Generation

Requires: Fix Model ✓

The Viseme Generator creates all 15 VRChat lip-sync mouth shapes from three base shapes you already have. If your avatar already has complete viseme shape keys, you can skip this phase — but you should still check the Viseme Mapper in the VRChat tab to confirm the keys are correctly named.

**What the Viseme Generator does:**

VRChat needs 15 specific mouth shapes (called visemes) to drive your avatar's lips when you speak. Most avatars only have a few basic mouth shapes. The CATS Viseme Generator mathematically combines your existing base shapes to produce the remaining 12.

The three base shapes it works from:
- **A** — Wide open mouth (the "ahh" shape)
- **O** — Rounded mouth (the "ohh" shape)
- **CH** — Narrow open mouth with teeth showing (the "ch" / "sh" shape)

**Steps:**
1. In the **CATS** tab, find the **Viseme Generator** section
2. Use the dropdowns to select which of your avatar's existing shape keys corresponds to A, O, and CH. If your keys are named differently (like `mouth_open`, `vrc.v_oh`, `mouth_wide`), select the closest match
3. Click **Generate Visemes**
4. CATS creates 15 new shape keys named to VRChat's standard (`vrc.v_aa`, `vrc.v_oh`, `vrc.v_ch`, etc.)
5. Check that the **Ledger** now shows a checkmark (✓) next to Visemes

**What you should be seeing:** Your mesh now has 15 new shape keys in the Shape Keys panel (Properties → Object Data Properties → Shape Keys). The Ledger's second slot shows ✓.

> **If your avatar has no mouth shape keys at all:** You will need to create at least A, O, and CH manually in Blender (using Edit Mode sculpting or shape key editing) before CATS can generate the rest. See the Glossary entry for **Shape Key** for a basic introduction.

---

### Phase 3 — Eye Tracking

Requires: Fix Model ✓

The Eye Tracking Setup tool configures your avatar's eye bones to work with VRChat's built-in eye tracking system. This makes your avatar's eyes move naturally and look at other players.

**What Eye Tracking Setup does:**
- Locates your avatar's left and right eye bones
- Renames them to VRChat's required names (`LeftEye` and `RightEye`)
- Creates the rotation constraints VRChat needs to drive eye movement
- Limits eye rotation to a natural range (prevents eyes from spinning 360°)
- Verifies both bones are positioned correctly relative to the head bone

Without the Fix Model step completed first, the eye bone detection may lock onto orphaned duplicate vertices from the original mesh rather than the live eye geometry, placing constraints at wrong positions. Users who skipped Fix Model before running Eye Tracking Setup report their avatar arriving in VRChat with both eyes locked in a downward stare that cannot be corrected without re-running the full pipeline.

**Steps:**
1. In the **CATS** tab, find the **Eye Tracking Setup** section
2. Click **Auto-Detect Eye Bones** — CATS searches your skeleton for bones whose names or positions match typical eye bone patterns
3. Verify that the Left Eye Bone and Right Eye Bone fields show the correct bones. If not, use the dropdown to select them manually
4. Click **Setup Eye Tracking**
5. Check that the **Ledger** now shows a checkmark (✓) next to Eye Tracking

**What you should be seeing:** Both eye bones are renamed and now have rotation constraints visible in the Bone Constraints panel. The Ledger's third slot shows ✓.

> **If CATS cannot find eye bones:** Your skeleton may not have dedicated eye bones. Some avatar formats (particularly older MMD models) use shape keys for blinking instead of bones. If that is your case, skip this phase — VRChat will fall back to shape-key-based eye animation automatically if no eye bones are found.

---

### Phase 4 — Pose to Shape Key

Requires: Fix Model ✓

The Pose to Shape Key tool converts your avatar's current posed position into a shape key (blend shape). This is useful for capturing custom expressions or rest poses that you want to use in VRChat's expressions menu.

Without the Fix Model step, the vertex order can contain gaps from removed duplicate vertices that have not yet been reconciled, causing the shape key to capture distorted geometry rather than the actual posed shape. Users who reached this step without Fix Model report shape keys that make the mesh explode outward when triggered in VRChat.

**Steps:**
1. Pose your avatar using Blender's Pose Mode (select the armature, press Ctrl+Tab, choose Pose Mode)
2. Move the bones into the expression or position you want to capture
3. Return to Object Mode (press Ctrl+Tab again)
4. In the **CATS** tab, find the **Shape Key Tools** section
5. Click **Pose to Shape Key**
6. Name the new shape key when prompted
7. Check that the **Ledger** now shows a checkmark (✓) next to Pose to Shape

**What you should be seeing:** A new shape key appears in your mesh's shape key list. Set its value to 1.0 in the Shape Keys panel to verify it shows the correct pose.

> **Shape Key to Basis:** The companion tool, **Shape Key to Basis**, does the opposite — it bakes a shape key back into your mesh's neutral rest shape. Use this when you want to lock in a corrected rest pose permanently. This also requires Fix Model ✓ first; applying a shape key to a mesh with lingering duplicate vertices can merge geometry incorrectly.

---

### Phase 5 — Apply Transforms

Requires: Fix Model ✓, Visemes ✓, Eye Tracking ✓, Pose to Shape ✓

This is the final phase. Apply Transforms freezes all pending position, rotation, and scale data into your mesh and skeleton so that everything reads as clean zero values (position 0,0,0 / rotation 0°,0°,0° / scale 1.0,1.0,1.0). VRChat's SDK requires clean transforms — un-applied scale in particular causes avatars to appear at the wrong size or to have physics that behaves incorrectly.

Applying transforms on a mesh that still has unfixed geometry (missing Fix Model), unresolved viseme shape keys, or unconfigured eye constraints will permanently bake those broken states into the mesh. Users who applied transforms before completing the pipeline report avatars that appear correctly sized in Blender but spawn at a fraction of normal height in VRChat, with no way to fix it without re-importing from source.

**Transform tools in this phase:**
- **Apply All Transforms** — Applies position, rotation, and scale to both the mesh and the armature simultaneously
- **Fix FBT** — Applies a specific transform correction for Full Body Tracking setups (moves the root bone to floor level)
- **Remove FBT** — Removes the FBT correction if you applied it by mistake or no longer need it

**Steps:**
1. Confirm all four earlier Ledger checkmarks are showing (✓✓✓✓)
2. In the **CATS** tab, find the **Transform Tools** section
3. Click **Apply All Transforms**
4. Check that the **Ledger** now shows a checkmark (✓) next to Apply Transforms — all five slots should now be checked (✓✓✓✓✓)
5. Go to the **VRChat** tab → **Export** section and export your avatar as FBX

**What you should be seeing:** All five Ledger slots show ✓. Your avatar is ready to import into the VRChat Creator Companion.

---

**What This Unlocks:** A fully pipeline-processed avatar with clean geometry, all 15 visemes, configured eye tracking, any custom expressions you created, and clean transforms — the complete set of requirements for a VRChat upload that works correctly from the first attempt.

---

# CATS Plugin — Before You Begin: The Pipeline Order

**Read this before using any CATS tool for the first time.**

The CATS tools are not a menu of independent options — they are a pipeline. Each step builds on the previous one. Running them out of order produces broken results that are invisible until you are already in VRChat, at which point they cannot be fixed without starting over.

---

## The Five Phases, In Order

The CATS Ledger — visible at the top of the CATS panel — tracks your progress through these phases with checkmarks:

1. **Fix Model** — Clean the mesh. Remove duplicates, broken geometry, and bad normals. This is the foundation every other step depends on.

2. **Visemes** — Generate all 15 VRChat lip-sync mouth shapes from your three base shapes (A, O, CH).

3. **Eye Tracking** — Set up VRChat's eye movement system using your avatar's eye bones.

4. **Pose to Shape** — Capture any custom poses or expressions as shape keys.

5. **Apply Transforms** — Freeze all position/rotation/scale data so your avatar has clean transforms for upload.

---

## The Ledger

The Ledger is the row of checkmarks at the top of the CATS panel. Each phase has one slot. When a phase completes successfully, its slot fills with a ✓.

Tools that depend on an earlier phase being complete will appear grayed out (unavailable) until that phase's checkmark is shown. This prevents you from accidentally running steps out of order.

The Ledger resets when you start working on a new avatar. It is stored per-session in Blender's scene data.

---

## Why This Order

Each phase modifies the mesh or skeleton in ways the next phase depends on:

- **Fix Model must be first** because it changes vertex count, removes duplicates, and corrects normals. Any tool that reads vertex positions (viseme generation, eye bone detection, pose capture) will produce wrong results if it runs against a mesh that still has duplicate or broken vertices.

- **Visemes before Eye Tracking** because both tools modify shape key and bone data. Running them in this order ensures shape key slots are allocated before constraint data is written.

- **Eye Tracking before Pose to Shape** because Pose to Shape captures the full mesh state including bone-driven deformations. Having eye constraints in place before capturing ensures the neutral eye position is correct in the saved shape.

- **Apply Transforms last** because it permanently freezes all data. Any unfixed geometry, unmapped shape keys, or misconfigured constraints get locked in permanently. Once transforms are applied, you cannot go back to fix earlier phases without re-importing from source.

---

## What Breaks If You Skip a Step

**Skip Fix Model:**
Every subsequent tool is running against a mesh that may contain duplicate vertices at the same position. The Viseme Generator will produce shape keys that control both the real vertex and its hidden duplicate — in VRChat, the duplicate vertex stays behind while the real one moves, causing a torn or glitched mouth at every lip-sync shape. Eye Tracking Setup may attach constraints to the duplicate eye mesh rather than the visible one, locking the eyes into a fixed stare. Apply Transforms will permanently bake all of these errors into the mesh with no way to recover.

**Skip Visemes:**
The five pipeline phases are ordered, but the Ledger treats a missing Viseme checkmark as an incomplete pipeline. Apply Transforms will not run until all earlier phases are checked — this protects you from uploading an avatar with no lip sync. If you intentionally do not want CATS visemes (because you have existing ones), mark the phase complete manually using the **Mark Complete** button next to the Viseme Generator.

**Skip Eye Tracking:**
Your avatar will have no eye movement in VRChat and will stare straight forward at all times. This is acceptable if your avatar has no eye bones — use **Mark Complete** to bypass this phase.

**Skip Pose to Shape:**
If you have no custom expressions to save, this phase is optional. Use **Mark Complete** to advance to Apply Transforms without it.

---

# Feature Reference

This section covers every tool in BoneForge in detail. Use this when you want to understand a specific feature more deeply, or when the Quick Guides do not cover your exact situation.

Each feature entry includes:
- What it does in plain language
- When you would use it
- What all the settings do

---

## Rig UI Tools (Phase 1)

**Stability: Stable | Introduced: 5.0**

These tools help you manage the visual side of working with armatures — which bones are visible, how they are organized, and quick access shortcuts.

---

### Bone Collection Panel

**What it does:** Shows all of your skeleton's bone groups as labeled buttons. Click a button to show or hide that group.

> A **bone collection** is a named group of bones. For example, you might have collections called "IK Controls," "Face Bones," and "Deform Bones." Hiding a collection makes those bones invisible in the viewport — useful for focusing on one part of the rig.

**Key controls:**
- **Toggle button** — Shows/hides the collection
- **Solo button (eye icon)** — Hides all other collections, showing only this one
- **Show All / Hide All** — Quick buttons to show or hide everything at once
- **Select Bones** — Selects all bones in the collection
- **Reorder arrows** — Move collections up and down in the list
- **Rename** — Give a collection a custom display name
- **Icon / Color** — Assign a custom icon and color to the button for visual organization
- **Sections** — Group multiple collections under a collapsible header

**Where to find it:** Review tab → Collections section

---

### Visibility Bookmarks

**What it does:** Saves a snapshot of which bone collections are currently visible, so you can switch between saved views instantly.

**Example use:** You have set up a view showing only the face bones for expression work. Save it as "Face Only." Then show everything for weight painting. Save it as "Full Rig." Now you can switch between these views with one click instead of toggling each collection manually.

**Key controls:**
- **Save Bookmark** — Saves the current visibility state with a name
- **Restore Bookmark** — Applies a saved state
- **Color indicators** — Color-coded markers next to each bookmark for quick visual identification
- **Expand** — Shows additional bookmark slots beyond the default four

**Default bookmark buttons:** FK Arms, IK Body, Face Only, Full Rig

**Where to find it:** Review tab → Bookmarks section

---

### Hotkey Quick Panel

**What it does:** Opens a floating version of the bone collection and bookmarks panel wherever your cursor is, without navigating to the sidebar.

**How to use:** Press **Ctrl+Shift+R** in the 3D viewport. The panel appears at your cursor. Click outside it to dismiss.

**Where to change the hotkey:** BoneForge Preferences (Edit > Preferences > Add-ons > BoneForge)

---

## Animation Tools (Phase 2)

**Stability: Stable | Introduced: 5.0**

---

### Pose Library

**What it does:** Stores named poses with thumbnail previews that you can apply to your avatar with one click.

**Key controls:**
- **Save Pose** — Stores the current bone positions as a named pose entry with an auto-captured thumbnail
- **Apply Pose** — Snaps bones to the saved pose
- **Apply Blended (0–100%)** — Applies the pose at partial strength, mixing with the current position
- **Apply Mirrored** — Applies the pose flipped left-to-right
- **Delete** — Removes a pose entry
- **Rename** — Changes a pose's display name
- **Set Category** — Tags the pose for filtering
- **Filter** — Shows only poses matching a category tag
- **Refresh Thumbnail** — Re-renders the preview image from the current viewport
- **Export** — Saves poses to a `.bfpose` file
- **Import** — Loads poses from a `.bfpose` file

**Where to find it:** Review tab → Pose Library section

---

### Rigify Enhancement

**What it does:** Automatically detects Rigify-generated control rigs and sets up BoneForge's collection panels, bookmarks, and property sliders to match Rigify's standard controls.

> **Rigify** is a Blender built-in system for generating animation-ready rigs. If you used Rigify to build your rig, this tool wires BoneForge's UI to Rigify's IK/FK controls automatically.

**Key controls:**
- **Enable Rigify** — Manually triggers enhancement on the active armature
- **Auto-Enhance** — Runs automatically when a Rigify rig is selected (optional toggle)
- **Re-Enhance** — Rebuilds the BoneForge panels from scratch for the current Rigify rig
- **IK/FK slider** — Blends between IK (position-based) and FK (rotation-based) control on arms and legs
- **Stretch toggles** — Enables or disables stretchy IK on limbs
- **Parent space switches** — Changes which space a limb's IK target is parented to (World, Root, etc.)
- **Head/Neck follow** — Controls how much the head/neck follows the body rotation

**Where to find it:** Setup Rigging tab → Rigify section

---

### Corrective Shape Keys

**What it does:** Creates shape keys (blend shapes) that automatically activate when a bone reaches a specific angle. Used to fix mesh pinching or collapsing at extreme poses.

**Example use:** Your character's elbow mesh collapses when fully bent. You sculpt a corrected version of that elbow and link it to the arm bone so it automatically applies at 150° of bend.

**Key controls:**
- **Create Corrective** — Dialog to set which bone drives the shape key, at what rotation angle it activates, and how smoothly it fades in (falloff range)
- **Edit** — Adjust the activation angle and falloff for an existing corrective
- **Delete** — Removes the corrective and its driver
- **Rotation axis** — Which axis (X, Y, or Z) triggers the shape key
- **Activation angle** — The rotation angle (in degrees) at which the shape key reaches full strength (1.0)
- **Falloff** — How many degrees before the activation angle the shape key starts fading in (larger = smoother transition)

**Where to find it:** Skin tab → Correctives section

---

### Graph Tools and Breakdowner

**What it does:** A set of animation refinement tools for working with keyframes and pose transitions.

**Key tools:**

- **Breakdowner** — Hold down the operator key and drag your mouse left-right to blend the current frame's pose between the nearest keyframes. Like an interactive "in-between" creator.
- **Delta Move** — Nudge selected bones by a precise amount in screen space or world space. Useful for fine-positioning during animation.
- **Buffer Curves** — Save the current animation curves to memory (Capture), then swap back and forth between the saved version and the edited version (Swap). Like undo/redo for animation curves only.
- **Smart Bake** — Bakes simulation or constraint-driven animation to keyframes with reduced keyframe density (removes redundant keys automatically)
- **Euler Filter** — Fixes rotation flipping artifacts in animation curves caused by gimbal lock
- **Tangent Tools** — Set keyframe handle types (Auto, Vector, Aligned, Free) on selected keyframes

**Where to find it:** Review tab → Graph Tools section

---

## Weight Tools (Phase 2B)

**Stability: Stable | Introduced: 5.0**

These tools control how your mesh deforms when bones move. Think of weights as the instructions telling each part of your mesh which bones to follow — and by how much.

---

### Weight Mirror

**What it does:** Copies weights from one side of your avatar to the mirror-opposite side. Essential for symmetrical characters.

**Key controls:**
- **Mirror All Weights** — Mirrors every bone group to its opposite side
- **Mirror Active Weight** — Only mirrors the currently selected bone group
- **Axis** — Which axis is the mirror plane (X is standard for humanoids facing +Y)
- **Direction** — Bidirectional (copy both ways), Left to Right (left side is the source), Right to Left
- **Search Distance** — Maximum distance (in Blender units) to consider two vertices a "pair." Increase if your mesh is not perfectly symmetrical
- **Normalize After** — Ensures all weights sum to 1.0 after mirroring

**Where to find it:** Skin tab → Weight Mirror section

---

### Weight Transfer

**What it does:** Copies weights from one source mesh or bone group to a target. Used when attaching clothing to a body rig, or copying weights from a high-resolution mesh to a lower-resolution one.

**Key controls:**
- **Source Group** — The bone group to copy FROM
- **Target Group** — The bone group to copy TO
- **Threshold** — Minimum weight value to transfer (lower values = transfer more, including faint influence)
- **Normalize After Transfer** — Keeps all weights summing to 1.0

**Transfer method:**
- **Nearest Vertex** — Each target vertex gets the weight from the closest source vertex
- **Nearest Face** — Uses face projection for smoother results on curved surfaces

**Where to find it:** Skin tab → Weight Transfer section

---

### Weight Table

**What it does:** A spreadsheet-style view showing exact weight values for each selected vertex against each bone. Lets you type in precise numbers.

**How to use:** Select vertices in Edit Mode, then open the Weight Table. Each row is a vertex, each column is a bone. Click any cell and type a new value (0.0 to 1.0).

**Key controls:**
- **Set Weight** — Apply a typed value to a specific vertex/bone cell
- **Zero Weight** — Clear a specific cell to 0.0
- **Tag Deform Bones** — Marks selected bones as deform bones (needed for them to appear in weight paint mode)

**Where to find it:** Skin tab → Weight Table section

---

### Delta Mush

**What it does:** Applies a smoothing deformation to your mesh that reduces pinching and collapsing at joints. The mesh stays close to its original shape at rest, but deforms more cleanly during movement.

**Key controls:**
- **Add Delta Mush** — Adds the Delta Mush modifier to your mesh
- **Bind** — Bakes the current rest shape, anchoring the smoothing to that baseline
- **Remove** — Removes the modifier
- **Iterations** — How many smoothing passes to apply (higher = smoother, but may lose detail)
- **Influence** — How strong the smoothing effect is (0 = off, 1 = full strength)

**Where to find it:** Skin tab → Delta Mush section

---

### Proximity Wrap

**What it does:** Makes one mesh follow the surface of another mesh closely, like a second skin. Useful for clothing that needs to hug a body tightly.

**Key controls:**
- **Bind** — Attaches the clothing mesh to the body mesh using proximity detection
- **Rebind** — Re-calculates the attachment with different settings
- **Unbind** — Removes the proximity wrap link
- **Target Mesh** — The mesh the clothing should follow
- **Max Distance** — How far from the target surface the wrapping effect reaches
- **Falloff** — How the wrapping effect fades off at the edges (Smooth or Linear)

**Where to find it:** Skin tab → Proximity Wrap section

---

### Shape Library

**What it does:** Stores and retrieves shape key states (blend shape configurations). Save a set of active shape keys as a named preset and reapply it later.

**Key controls:**
- **Save Shape** — Records the current shape key values as a named entry
- **Apply Shape** — Sets your mesh's shape keys to match a saved entry
- **Copy Shape From** — Copies a shape key from another object into your current mesh

**Where to find it:** Skin tab → Shape Library section

---

## Rig Controls (Phase 2C)

**Stability: Mixed — see individual entries | Introduced: 5.5+**

---

### Space Switching

**What it does:** Lets you change which "space" a bone is anchored to during animation. For example, a hand holding a prop can be switched from following the body (body space) to staying in place in the world (world space) with one click.

**Stability: Stable**

**Key controls:**
- **Add Space** — Creates a new space option for the active bone (name it, set type to World/Origin/Bone, set which bone to follow)
- **Remove Space** — Deletes a space option
- **Switch Space** — Moves the bone to the selected space and adds a keyframe
- **Switch Without Key** — Switches space without keyframing
- **Set Default Space** — Sets which space the bone starts in

**Where to find it:** Review tab → Space Switching section

---

### Spline IK

**What it does:** Creates a Spline IK setup — a system where a chain of bones follows the shape of a curve. Used for tails, tentacles, ropes, long hair strands, or spines that need smooth, sweeping movement.

**Stability: Stable (bug-fixed in 6.1.1)**

**Key controls:**
- **Generate Spline IK** — Creates the curve and IK constraint on your selected bone chain
- **Remove Spline IK** — Removes the setup
- **Start/End Bone** — First and last bones of the chain
- **Curve Resolution** — How many segments the control curve has (more segments = smoother but heavier)

**Where to find it:** Review tab → Spline IK section

---

### Chain Dynamics

**What it does:** Applies physics-like secondary motion to a bone chain. The bones simulate inertia — they lag behind when the parent moves and bounce back when it stops. Used for hair strands, tails, and accessories.

**Stability: Stable**

**Key controls:**
- **Add Chain Dynamics** — Attaches dynamics to a bone chain
- **Remove Chain Dynamics** — Removes them
- **Bake Chain Dynamics** — Converts the simulated motion into keyframes (required for export)
- **Stiffness** — How resistant the chain is to bending
- **Damping** — How quickly the motion settles
- **Gravity** — Downward pull on the chain

**Where to find it:** Review tab → Chain Dynamics section

---

### Ribbon / Bendy Bones

**What it does:** Creates a ribbon-style deformation system using Bendy Bones — a Blender feature that lets a single bone segment curve and twist smoothly. Good for lips, eyebrows, belts, and other soft curved areas.

**Stability: Stable**

**Key controls:**
- **Generate Ribbon** — Creates the ribbon bone structure
- **Remove Ribbon** — Removes it
- **Segment Count** — Number of sub-divisions along the ribbon
- **Twist Amount** — How much the ribbon can twist end-to-end

**Where to find it:** Review tab → Ribbon section

---

### Viseme / Lip Sync System

**What it does:** Creates and manages viseme (mouth shape) sets linked to shape keys. For VRChat viseme mapping, use the VRChat Viseme Mapper instead. For generating visemes from scratch, use the CATS Viseme Generator.

**Stability: Stable**

**Key controls:**
- **New Viseme Set** — Creates a named collection of viseme entries
- **Record Viseme** — Saves the current shape key state as a viseme
- **Preview Viseme** — Plays back a viseme's shape key values
- **Delete Set** — Removes a viseme set

**Where to find it:** Review tab → Viseme section

---

### SDK / Custom Drivers

**What it does:** Creates links between bone positions and shape keys without using Python expressions. Move a bone to a specific position, record that as a keyframe, and assign a shape key value — BoneForge creates the driver curve automatically.

**Stability: Experimental**

**Example use:** Move the eyebrow bone up by 10 units → shape key "Brow Raised" = 1.0. Move it back to rest → shape key = 0.0. Now the shape key follows the bone automatically.

**Key controls:**
- **Create Driver** — Opens a dialog to set source bone, target shape key, and the axis/distance to measure
- **Edit Driver** — Modify an existing driver
- **Delete Driver** — Removes it
- **Record Point** — At the current bone position, records the current shape key value as a point on the driver curve
- **Set Driver Value** — Manually types a shape key value for a recorded point

**Where to find it:** Review tab → SDK Author section

---

### Rig Validator

**What it does:** Checks your rig against a set of rules and reports any problems — naming errors, missing bones, bad hierarchy, weight issues, and VRChat-specific requirements.

**Stability: Stable**

**Key controls:**
- **Run Validation** — Executes all checks and shows results
- **Select Bone** — Jumps to the bone that failed a specific check
- **Export Report** — Saves the validation results as a text or Markdown file
- **Rule Set** — Choose Standard (general rigging rules) or VRChat (VRChat-specific requirements)

**Where to find it:** Review tab → Rig Validator section

---

### Rig Notes

**What it does:** Lets you attach written notes to your rig file — useful for documenting what you have set up, leaving reminders, or collaborating with others.

**Stability: Stable**

**Key controls:**
- **Add Note** — Creates a new note with a title and text body
- **Edit Note** — Modifies existing text
- **Remove Note** — Deletes a note
- **Rig Readme** — Displays notes in a formatted, read-only view

**Where to find it:** Review tab → Rig Notes section

---

## Auto-Rigging (Phase 3)

**Stability: Stable | Introduced: 6.0**

---

### Auto-Rig Wizard

**What it does:** A step-by-step guided process that places marker points on your mesh and automatically generates a complete skeleton with weights. The main way to create a new rig from scratch in BoneForge.

See [Guide 1: Get Your First Avatar Into VRChat](#guide-1-get-your-first-avatar-into-vrchat) for a complete walkthrough.

**Steps:** Select Mesh → Set Rig Type → Set Finger Count → Place Body Markers → Place Face Markers → Place Finger Markers → Review → Generate

**Key wizard controls:**
- **Guess Markers** — Auto-detects marker positions from mesh geometry
- **Place Marker** — Interactive point placement in the 3D viewport
- **Move Marker** — Reposition a placed marker
- **Reset Marker** — Clears a marker back to unplaced
- **Mirror** — Auto-mirrors markers across the centerline when placing
- **Confirm All Green** — Locks in all green (valid) markers at once
- **Back / Next** — Navigate wizard steps
- **Generate** — Creates the armature from confirmed markers
- **Cancel** — Abandons the wizard and undoes any changes

**Where to find it:** Rig Builder tab → Wizard section

---

### Quick Human

**What it does:** Generates a complete human rig with one click using preset defaults. Faster than the Wizard but less customizable.

**Key controls:**
- **Generate Quick Rig** — Creates a default human skeleton, weights, and BoneForge panels immediately

**Where to find it:** Rig Builder tab → Quick Rig section

---

### Mannequin Generator

**What it does:** Creates a stylized human figure mesh with adjustable body proportions. Useful as a starting reference when you do not have a 3D model yet.

**Stability: Stable**

**Key controls:**
- **Add Mannequin** — Opens proportion settings and generates the figure
- **Quick Mannequin** — Generates with default proportions immediately
- **Regenerate** — Rebuilds with different settings
- **Remove** — Deletes the mannequin and its rig
- **Gender** — Male or Female body proportions
- **Height** — Total height in centimeters (120–220 cm range)
- **Head proportion** — Relative head size
- **Torso/Arm/Leg proportions** — Relative length adjustments
- **Muscularity** — Body type from lean to heavily built

**Where to find it:** Rig Builder tab → Mannequin section

---

### Animation Retargeting

**What it does:** Takes an animation (a series of keyframed poses) from one skeleton and applies it to a different skeleton. Lets you use Mixamo animations, motion capture data, or any other animation source on your custom rig.

**Stability: Stable**

**Key controls:**
- **Select Clip** — Choose an animation to retarget
- **Import Clip** — Load animation from a file
- **Auto-Match Bones** — Detects matching bones between the source and target skeletons by name
- **Preview** — Plays the retargeted animation in the viewport
- **Apply** — Writes the retargeted motion as keyframes on your rig
- **Bone Mapping editor** — For each source bone, specify which target bone receives its motion
- **Retarget Method** — Simple (direct rotation transfer) or IK-Aware (accounts for limb length differences)
- **Frame Range** — Start and end frame of the animation to import

**Where to find it:** Setup Rigging tab → Retargeting section

---

## Bone Merge

**Stability: Stable | Introduced: 6.0**

See [Guide 11: Merge Two Rigs Together](#guide-11-merge-two-rigs-together) for a complete walkthrough.

**The three stages:**
1. **Scope (Stage 1)** — Analyze and review the differences between two armatures
2. **Rename (Stage 2)** — Resolve naming conflicts and mark unique bones
3. **Execute (Stage 3)** — Dry-run preview, then merge

**Key controls:**
- **Source Armature** — The secondary skeleton being absorbed
- **Target Armature** — The main skeleton that survives
- **Analyze** — Compares the two skeletons and creates the diff table
- **Normalize** — Auto-renames all standard bones to a consistent naming convention
- **Propose** — Suggests names for unrecognized source-only bones
- **Apply Rename** — Renames one bone entry (one undo step)
- **Batch** — Applies a naming pattern to multiple entries at once (supports `{bone}`, `{side}`, `{index}` tokens)
- **Mark Unique** — Flags a bone as intentionally new (will be added, not merged)
- **Dry Run** — Shows what the merge would do without changing anything
- **Execute Merge** — Creates a backup and performs the merge

**Naming standards:** Mixamo Prefixed, Mixamo Stripped, or Custom

**Where to find it:** Review tab → Bone Merge section

---

## VRChat Tools

**Stability: Stable | Introduced: 5.0, expanded 6.0**

---

### Humanoid Mapper and Validator

Maps your skeleton's bones to VRChat's required humanoid slots and checks for errors.

See [Guide 5: Map Your Avatar to VRChat's Body System](#guide-5-map-your-avatar-to-vrchats-body-system).

---

### Hair Physics

Generates PhysBone components for dynamic hair and accessories.

See [Guide 6: Add Hair Physics](#guide-6-add-hair-physics).

---

### Clothing Merge

Attaches clothing meshes to your base avatar's skeleton.

See [Guide 7: Attach Clothing That Moves With Your Body](#guide-7-attach-clothing-that-moves-with-your-body).

---

### Naming Conventions

**What it does:** Detects your skeleton's naming format and renames bones to VRChat's standard.

See [Guide 4: Fix Your Avatar's Bone Names](#guide-4-fix-your-avatars-bone-names).

**Available presets:** Mixamo, Ready Player Me, Unity Standard, Custom (save your own)

**Batch tools:** Add Prefix, Remove Prefix, Add Suffix, Remove Suffix, Find & Replace (plain text and regular expression)

**Where to find it:** VRChat tab → Naming section

---

### Viseme Mapper

**What it does:** Maps your mesh's shape keys to VRChat's 15 lip-sync phonemes.

See [Guide 8: Set Up Lip Sync](#guide-8-set-up-lip-sync).

For generating visemes from scratch when your avatar does not have them yet, see [CATS Tool Reference: Viseme Generator](#viseme-generator-cats).

**VRChat's 15 phonemes:** `aa`, `ch`, `dd`, `e`, `ff`, `ih`, `kk`, `mm`, `nn`, `oh`, `r`, `ss`, `th`, `uh`, `pp`

---

### Performance and Optimization

**What it does:** Measures your avatar's VRChat performance rank and provides tools to improve it.

See [Guide 9: Improve Your Avatar's Performance](#guide-9-improve-your-avatars-performance).

**Performance tiers (best to worst):** Excellent → Good → Medium → Poor → Very Poor

**Tools:**
- **Calculate Rank** — Estimates your current performance tier
- **Decimate** — Reduces polygon count by a percentage
- **Remove Unused Shape Keys** — Clears unmapped blend shapes
- **Remove Unused Vertex Groups** — Clears empty bone assignments
- **Remove Zero-Weight Bones** — Removes bones with no mesh influence
- **Merge Same-Material Meshes** — Combines meshes that share the same material
- **Material Atlas** — Bakes multiple materials into a single texture sheet

---

### Mesh Cleanup

**What it does:** Fixes common mesh problems before export.

**Tools:**
- **Fix Model** — Removes duplicate vertices, loose geometry, and calculates correct normals automatically
- **Join Meshes** — Combines all meshes into one while keeping material slots
- **Apply Transforms** — Freezes scale/rotation so they read as 1.0/0° (required by some exporters)

**Where to find it:** VRChat tab → Cleanup section

---

### VRChat Export

**What it does:** Exports your finished avatar as an FBX file formatted specifically for VRChat's SDK.

**Key settings:**
- **Merge All Meshes** — Combines into one mesh on export (recommended)
- **Apply Shape Keys to Basis** — Merges all active shape keys into the base mesh shape before exporting
- **Include Armature / Mesh / Materials / Animations** — Toggle which data is included in the export

**Where to find it:** VRChat tab → Export section

---

## VRM Bridge

**Stability: Stable | Requires VRM add-on | Introduced: 5.5**

---

### VRM Import

**What it does:** Imports `.vrm` files (VRoid Studio, Virtual Cast, and other VRM-format avatars) into Blender with their materials, skeleton, and shape keys preserved.

**File > Import > VRM (.vrm)**

**Note:** Requires the VRMC-io VRM add-on to be installed. Use BoneForge's VRM installer (VRM tab → Install VRM Add-on) for easy setup.

---

### VRM Export

**What it does:** Exports your rigged character back to VRM format for use in VRoid-compatible apps, Virtual Cast, or Resonite.

**Key settings:**
- **Model Name** — Your avatar's display name
- **Author / License** — Creator information stored in the VRM metadata
- **VRM Version** — Typically 1.0 for current apps

**Where to find it:** VRM tab → Export section

---

### VRM Linter

**What it does:** Validates your scene against VRM export requirements — checks for required humanoid bones, metadata completeness, and material setup.

Click **Run VRM Lint** to see results.

**Where to find it:** VRM tab → Lint section

---

## MMD Bridge

**Stability: Stable | Requires MMD Tools add-on | Introduced: 5.5**

---

### MMD Import

**What it does:** Imports MMD model files (`.pmx`, `.pmd`) into Blender with bone structure and materials.

**Supported formats:**
- `.pmx` / `.pmd` — MMD model files
- `.vmd` — MMD animation files
- `.vpd` — MMD pose files

**Note:** Requires MMD Tools to be installed. Use BoneForge's MMD installer (MMD tab → Install MMD Tools) for easy setup.

---

### MMD Export

**What it does:** Exports your work back to PMX/VMD/VPD format for use in MMD Studio or other MMD-compatible software.

**Where to find it:** MMD tab → Export section

---

## I/O Hub (Export Hub)

**Stability: Stable | Introduced: 6.0**

---

### Export Hub

**What it does:** A central panel for all export formats — VRChat (FBX), VRM, MMD (PMX), Unreal Engine (FBX), and Unity.

**Target options:**
- **VRChat (Unity FBX)** — Standard VRChat export
- **VRM** — Delegates to VRM exporter
- **MMD (PMX)** — Delegates to MMD exporter
- **Unreal Engine FBX** — FBX with Unreal-specific settings and LOD support
- **Unity General** — FBX + metadata sidecar for Unity projects

**Common FBX settings:**
- **Include Armature / Mesh / Materials / Animations** — Toggle export components
- **Bake Animation** — Converts constraint-driven animation to raw keyframes for compatibility
- **FBX Version** — ASCII or Binary format

**Where to find it:** In the sidebar under the I/O Hub tab (registered at the bottom of the sidebar)

---

### Bridge Manager

**What it does:** Checks which format-bridge add-ons (VRM, MMD) are currently installed and their versions. Shows installation buttons for any that are missing.

**Where to find it:** VRM tab or MMD tab → top section

---

## Taskboard

**Stability: Stable | Introduced: 6.0**

---

### Project Overview Panel

**What it does:** Shows a summary of the current avatar project — the avatar's name, a health indicator, and a list of pending tasks detected by BoneForge's analyzer.

The task analyzer automatically identifies common issues (missing humanoid bones, unresolved naming, missing visemes, etc.) and lists them as actionable items.

**Where to find it:** Review tab → Overview section

---

### Bone Inspector

**What it does:** Shows detailed information about the currently selected bone — its name, parent, constraints, custom properties, and drivers. Also lets you edit basic properties directly without entering Edit Mode.

**Key information shown:**
- Bone name and parent
- Constraint list (click to expand details)
- Driver list (click to open the driver editor)
- Custom property values (editable inline)

**Where to find it:** Review tab → Bone Inspector section

---

### Bone Context Menu

**What it does:** Adds BoneForge-specific options to the right-click context menu when you right-click a bone in the viewport or outliner. Quick access to common per-bone operations without opening a panel.

**Automatically available** when BoneForge is installed.

---

# CATS Tool Reference

**Stability: Stable | Introduced: 7.1.1**

The CATS tools live in their own **CATS** tab in the N-panel sidebar. They are separate from the main BoneForge tabs. All CATS tools operate within the pipeline system described in [CATS Plugin — Before You Begin: The Pipeline Order](#cats-plugin--before-you-begin-the-pipeline-order).

---

## Fix Model

**Pipeline phase:** Phase 1 (mandatory first step)
**Ledger slot:** 1 of 5

**What it does:** Performs a comprehensive one-click mesh cleanup before any other CATS operation. Removes hidden problems that would silently corrupt every subsequent step.

**Operations performed:**
- Merges duplicate vertices at the same position
- Removes loose geometry (disconnected faces not attached to the main body)
- Recalculates face normals (fixes inside-out surfaces)
- Removes degenerate faces (zero-area triangles and lines)
- Removes doubles on the UV map
- Applies all pending scale and rotation transforms

**Key controls:**
- **Fix Model** — Runs all operations above on the selected mesh in one pass
- **Threshold** — Merge distance for duplicate vertex detection (default: 0.0001 Blender units). Increase if vertices are slightly misaligned; decrease if you want to avoid merging vertices that are close but intentionally separate

**Where to find it:** CATS tab → Fix Model section (top of panel)

---

## Bone Name Translation

**What it does:** Detects the source language of your skeleton's bone names and translates them to English VRChat-compatible names.

**Supported source languages:**
- Japanese (日本語) — Most common, used by MMD and many VRChat community models
- Chinese (中文) — Simplified and Traditional
- Korean (한국어)
- Portuguese (Português)
- Spanish (Español)
- French (Français)

The translation uses a built-in dictionary of known bone name patterns for each language. It does not require internet access and runs entirely offline.

**Key controls:**
- **Auto-Detect Language** — Analyzes the current bone names and identifies the source language automatically
- **Translate Bone Names** — Applies the translation after detection
- **Manual Language Select** — Override the auto-detected language if it chose incorrectly
- **Preview** — Shows a before/after comparison without committing changes

**Note on scope:** Bone Name Translation handles the language of the *source model's bone names*, not the language of your Blender interface. If you have a Japanese MMD model you want to use in the English version of VRChat, use this tool regardless of which language Blender is set to.

**Where to find it:** CATS tab → Bone Name Translation section

---

## Zero Weight Bone Cleanup

**What it does:** Finds and removes bones that have zero influence over the mesh — bones that exist in the skeleton but do not move any vertices. These bones waste performance budget without contributing anything visible.

**Key controls:**
- **Find Zero Weight Bones** — Scans the skeleton and lists all bones with zero mesh influence
- **Remove Selected** — Deletes the bones you have checked in the list
- **Remove All Found** — Removes all zero-weight bones at once
- **Threshold** — Minimum weight sum to consider a bone "non-zero." Default is 0.001; lower values keep more bones

**When to use:** After attaching clothing or merging armatures, extra bones often get carried over without being assigned to any mesh. Run this after Join Meshes and before exporting.

**Where to find it:** CATS tab → Bone Tools section → Zero Weight Bones

---

## Join Meshes

**What it does:** Combines all separate mesh objects in your scene into a single unified mesh. VRChat performs best with one mesh per avatar.

**Shape key conflict handling:** When joining meshes that have different sets of shape keys, CATS automatically resolves conflicts by padding missing shape keys on each mesh with a neutral (zero-value) shape, ensuring the final merged mesh has a consistent shape key set across all vertices.

**Key controls:**
- **Join All Meshes** — Merges every mesh object in the scene into one
- **Join Selected** — Merges only the currently selected mesh objects
- **Merge by Material** — Joins only meshes that share a material (useful for partial merges)

**When to use:** After all clothing and accessories are attached and weighted. Do not run Join Meshes before CATS Fix Model — joining meshes before cleanup can spread duplicate vertex problems from one mesh object to another, making them harder to remove. Users who joined meshes before Fix Model report the resulting single mesh retaining phantom vertices from all original objects, causing the Viseme Generator to produce shape keys that visibly tear the mesh apart at the seams.

**Where to find it:** CATS tab → Mesh Tools section → Join Meshes

---

## Material Atlas Combiner

**What it does:** Bakes multiple materials into a single texture atlas sheet. Fewer materials = better VRChat performance rating.

This is the same atlas process available in the main VRChat tab, presented with an Accept/Revert workflow that lets you preview the result before committing.

**Key controls:**
- **Analyze** — Shows your current material count and estimated savings
- **Atlas Resolution** — Size of the combined texture output (1024 / 2048 / 4096 pixels)
- **Material rows** - Let you disable individual material slots and inspect diagnostics, duplicate groups, and size overrides
- **Texture rows** - Let you disable individual image nodes and inspect or override their role labels
- **UV Method** - Chooses how the atlas work mesh is unwrapped and packed before baking, including Advanced Variation
- **UV Seed / Rotation Step** - Controls deterministic variation for seeded UV packing
- **Packing Preset / Bake Padding** - Records atlas quality settings and controls bake edge padding
- **Bake Passes** - Albedo is the default; Normal, Emission, and Roughness can be explicitly baked as separate outputs; Metallic and ORM channel packing are blocked until their source path is verified
- **Bake Atlas** — Combines all materials and shows a preview
- **Accept** — Commits the atlas and replaces your original materials
- **Revert** — Undoes the atlas and restores your original materials

**Lineage credits:** This workflow continues the BoneForge CATS integration lineage, credits the original Cats Blender Plugin, credits Grim-es/material-combiner-addon for the Material Combiner lineage, and credits UV Toolkit by Alexander Belyakov plus the oRazeD/UVToolkit archival repository for UV workflow inspiration. BoneForge implements its own integrated atlas UV helpers instead of vendoring UVToolkit source.

**Where to find it:** CATS tab → Material Atlas section

---

## Eye Tracking Setup

**Pipeline phase:** Phase 3
**Ledger slot:** 3 of 5
**Requires:** Fix Model ✓

This tool requires Fix Model to be completed first. Without it, the eye bone detection may latch onto remnant duplicate geometry from the head mesh instead of the actual eye bone, placing rotation constraints at a point in empty space. Users who ran Eye Tracking Setup before Fix Model describe their avatar looking permanently downward at the floor with no way to correct it in VRChat without redoing the full pipeline.

**What it does:** Locates your avatar's eye bones, renames them to VRChat's required names (`LeftEye` and `RightEye`), and creates the rotation constraints that drive natural eye movement in VRChat.

**Key controls:**
- **Auto-Detect Eye Bones** — Searches for bones matching common eye bone name patterns and positions
- **Left Eye Bone / Right Eye Bone** — Manual dropdowns to assign the correct bones if auto-detect fails
- **Setup Eye Tracking** — Renames bones and creates all required constraints
- **Eye Rotation Limits** — Maximum rotation angle for up/down and left/right movement (default: 30°)
- **Test Eye Movement** — Animates the eye bones through their range to verify constraints work

**Where to find it:** CATS tab → Eye Tracking Setup section

---

## Shape Key Tools

**Pipeline phase (Pose to Shape):** Phase 4
**Ledger slot:** 4 of 5
**Requires:** Fix Model ✓

Both tools in this section require Fix Model to be completed first. Capturing a shape key from a mesh that still contains duplicate vertices records both the real vertex and its hidden duplicate — when the shape key is later triggered in VRChat, users report the mesh tearing at the face as duplicate vertices pull in opposite directions.

---

### Pose to Shape Key

**What it does:** Captures the current posed position of your avatar's mesh (including all bone deformations) and saves it as a new shape key. Use this to create custom expressions, clothing morphs, or alternate rest positions.

**Steps:**
1. Pose your avatar in Pose Mode
2. Return to Object Mode
3. Click **Pose to Shape Key**
4. Name the shape key when prompted
5. Verify the result by setting the new key's value to 1.0

**Key controls:**
- **Pose to Shape Key** — Captures current deformed state as a new shape key
- **Name** — Name field for the new shape key

**Where to find it:** CATS tab → Shape Key Tools section

---

### Shape Key to Basis

**What it does:** Bakes an existing shape key back into the mesh's neutral rest position. Effectively applies the shape key permanently as the new default pose.

**Use carefully:** This is a one-way operation. The shape key is removed and its deformation becomes the new base mesh shape. Make sure to run Fix Model first — applying a shape key to a mesh with lingering duplicate vertices can cause those vertices to merge at incorrect positions permanently.

**Key controls:**
- **Shape Key to Basis** — Bakes the selected shape key into the rest mesh and removes the key

**Where to find it:** CATS tab → Shape Key Tools section

---

## Transform Tools

**Pipeline phase (Apply Transforms):** Phase 5
**Ledger slot:** 5 of 5
**Requires:** Fix Model ✓, Visemes ✓, Eye Tracking ✓, Pose to Shape ✓

Apply Transforms is the final pipeline step. Running it before all earlier phases are complete bakes the incomplete state into the mesh permanently — there is no undo that can recover earlier pipeline data once transforms are applied and the file is saved. Users who applied transforms mid-pipeline describe having to re-import their avatar from source and restart the entire process from Fix Model.

---

### Apply All Transforms

**What it does:** Applies position, rotation, and scale to both the mesh and the armature simultaneously, setting all transform values to clean zero/identity (location 0,0,0 / rotation 0°,0°,0° / scale 1,1,1). Required for correct behavior in VRChat's SDK.

**Key controls:**
- **Apply All Transforms** — Applies to both mesh and armature at once

**Where to find it:** CATS tab → Transform Tools section

---

### Fix FBT

**What it does:** Applies a transform correction specifically for Full Body Tracking setups. Moves the root bone so it sits at floor level, which is required for VRChat's FBT calibration system to work correctly.

**When to use:** Only if you intend to use Full Body Tracking with your avatar. Run after Apply All Transforms.

**Key controls:**
- **Fix FBT** — Applies the FBT root bone correction

**Where to find it:** CATS tab → Transform Tools section

---

### Remove FBT

**What it does:** Removes the FBT correction added by Fix FBT. Use this if you applied Fix FBT by mistake or no longer want FBT support on the avatar.

**Key controls:**
- **Remove FBT** — Reverts the FBT root bone adjustment

**Where to find it:** CATS tab → Transform Tools section

---

## Viseme Generator (CATS)

**Pipeline phase:** Phase 2
**Ledger slot:** 2 of 5
**Requires:** Fix Model ✓

This tool requires Fix Model to be completed first. Generating visemes on a mesh with duplicate vertices produces shape keys that control both the actual mouth vertices and any hidden duplicates beneath them — in VRChat, the duplicates hold their original position while the real vertices move, creating a torn or split-mouth artifact at every phoneme. Users who skipped Fix Model before running the Viseme Generator consistently report a mouth that appears to rip apart at the corners when speaking.

**What it does:** Mathematically generates all 15 VRChat lip-sync viseme shape keys from three base shapes you define. The generator uses weighted coefficient blending so each output viseme looks like a natural combination of the base shapes rather than a mechanical interpolation.

**The 15 visemes generated:** `vrc.v_aa`, `vrc.v_ch`, `vrc.v_dd`, `vrc.v_e`, `vrc.v_ff`, `vrc.v_ih`, `vrc.v_kk`, `vrc.v_mm`, `vrc.v_nn`, `vrc.v_oh`, `vrc.v_r`, `vrc.v_ss`, `vrc.v_th`, `vrc.v_uh`, `vrc.v_pp`

**Base shapes needed:**
- **A** — Wide open mouth ("ahh")
- **O** — Rounded mouth ("ohh")
- **CH** — Narrow teeth-showing mouth ("ch" / "sh")

**Key controls:**
- **A Shape** — Dropdown to select your "A" base shape key
- **O Shape** — Dropdown to select your "O" base shape key
- **CH Shape** — Dropdown to select your "CH" base shape key
- **Generate Visemes** — Creates all 15 output shape keys
- **Preview** — Cycles through the generated visemes so you can check the results before committing
- **Blend Strength** — Scales the coefficient multipliers up or down globally (1.0 = default; reduce if visemes look too extreme)

**Where to find it:** CATS tab → Viseme Generator section

---

## Bone Tools

**What it does:** A set of utility operations for managing bones in your skeleton.

---

### Create Root Bone

**What it does:** Adds a root bone at the base of your skeleton (at the world origin, floor level) and parents all existing top-level bones to it. VRChat requires a root bone as the top of the hierarchy.

**Key controls:**
- **Create Root Bone** — Adds a bone named `Root` at position 0,0,0 and re-parents the armature hierarchy

**When to use:** When your skeleton has no root bone, or when the Rig Validator reports "missing root bone" errors.

**Where to find it:** CATS tab → Bone Tools section

---

### Merge Short Bones

**What it does:** Finds bones below a specified minimum length and merges them into their parent bone. Very short bones are often artifacts from import or from bone chain generation — they consume performance budget without contributing visible deformation.

**Key controls:**
- **Min Length** — Bones shorter than this value (in Blender units) are candidates for merging
- **Preview** — Shows which bones would be merged without committing
- **Merge** — Applies the merge

**Where to find it:** CATS tab → Bone Tools section

---

### Duplicate Bones

**What it does:** Creates copies of selected bones — useful for setting up twist bones, deform bone layers, or adding a copy of a control chain for a different purpose.

**Key controls:**
- **Duplicate Selected** — Creates a copy of each selected bone with a `.copy` suffix
- **Mirror Duplicate** — Duplicates and mirrors across the centerline, creating left/right pairs

**Where to find it:** CATS tab → Bone Tools section

---

## Armature Tools

---

### Merge Armatures

**What it does:** Combines two separate armatures (skeletons) into one. Similar to BoneForge's Bone Merge tool but optimized for the simpler use case of merging a clothing armature into a body armature.

**Key controls:**
- **Base Armature** — The main skeleton (survives the merge)
- **Merge Armature** — The secondary skeleton (absorbed)
- **Merge** — Executes the merge
- **Connect Bones** — Optionally re-parents the merged bones to the base armature's nearest bone instead of keeping them as top-level bones

**For complex multi-stage merges with naming conflict resolution**, use BoneForge's full Bone Merge tool in the Review tab instead.

**Where to find it:** CATS tab → Armature Tools section

---

## Mesh Tools

**What it does:** Additional mesh separation utilities beyond the basic Join Meshes tool.

---

### Separate by Materials

**What it does:** Splits a joined mesh into separate objects — one per material. Useful if you need to work on a specific material zone independently.

**Key controls:**
- **Separate by Materials** — Splits the active mesh by material assignment

**Where to find it:** CATS tab → Mesh Tools section

---

### Separate by Loose Parts

**What it does:** Splits a mesh at disconnected geometry boundaries — each group of connected faces becomes its own object. Useful for isolating accessories or props that were accidentally joined.

**Key controls:**
- **Separate by Loose Parts** — Splits the active mesh at geometry boundaries

**Where to find it:** CATS tab → Mesh Tools section

---

### Separate by Shape Keys

**What it does:** Splits a mesh by shape key data — separates vertices that have shape key animation from those that do not. Useful for isolating the animated face mesh from a static body when you need to work on only one.

**Key controls:**
- **Separate by Shape Keys** — Creates two objects: one with shape key data, one without

**Where to find it:** CATS tab → Mesh Tools section

---

## CATS Validator

**What it does:** Checks your avatar against the CATS pipeline requirements and reports any phases that are incomplete, out of order, or have configuration problems.

The Validator is separate from BoneForge's main Rig Validator — it focuses specifically on CATS pipeline state rather than general rigging correctness.

**Key controls:**
- **Run CATS Validation** — Checks all five pipeline phases and reports status
- **Jump to Phase** — Opens the relevant CATS panel section for any phase that failed
- **Force Reset Ledger** — Clears all Ledger checkmarks and resets the pipeline to the beginning (use if you re-imported the mesh and need to run the full pipeline again)

**Validation checks performed:**
- Fix Model: Was it run on the current mesh? (Detects if the mesh was modified after Fix Model ran)
- Visemes: Are all 15 VRChat phoneme shape keys present and named correctly?
- Eye Tracking: Are `LeftEye` and `RightEye` bones present with correct constraints?
- Pose to Shape: Is at least one custom shape key present (or was the phase marked complete)?
- Apply Transforms: Are all transforms at clean values (scale 1,1,1 / rotation 0,0,0)?

**Where to find it:** CATS tab → Validator section (bottom of panel)

---

# Quick-Fix Index

Use this section when something has gone wrong and you need to find the answer fast.

| Problem | Where to look |
|---|---|
| Upload fails — bones not recognized | [Guide 4](#guide-4-fix-your-avatars-bone-names) + [VRChat Naming](#naming-conventions) |
| Avatar in T-pose / doesn't track movement | [Guide 5](#guide-5-map-your-avatar-to-vrchats-body-system) + [Humanoid Mapper](#humanoid-mapper-and-validator) |
| Mesh deforming weirdly / skin stretching | [Weight Transfer](#weight-transfer) + [Weight Mirror](#weight-mirror) |
| One side of body has different weights | [Weight Mirror](#weight-mirror) |
| Hair clips through head | [Guide 6, Step 6](#step-6--add-colliders-recommended) — add colliders |
| Hair physics not moving | [Guide 6](#guide-6-add-hair-physics) — check chain detection + physics preset |
| Clothing clips through body | [Guide 7](#guide-7-attach-clothing-that-moves-with-your-body) + check BVH collision detection |
| Lip sync not working | [Guide 8](#guide-8-set-up-lip-sync) + [Viseme Mapper](#viseme-mapper) |
| Avatar is Very Poor performance | [Guide 9](#guide-9-improve-your-avatars-performance) + [Performance Optimization](#performance-and-optimization) |
| VRM import fails | [Guide 2, Step 1](#step-1--install-the-vrm-bridge) — install VRM add-on |
| MMD import fails | [Guide 3, Step 1](#step-1--install-mmd-tools) — install MMD Tools |
| Rig validator shows red errors | [Rig Validator](#rig-validator) — run validation and follow error messages |
| Bones vanished / can't see any bones | [Bone Collection Panel](#bone-collection-panel) → click Show All |
| Can't find BoneForge panels | Press **N** in 3D viewport, look for BoneForge tabs |
| Export FBX is missing bones | Check armature is selected before exporting; enable "Include Armature" |
| Shape keys disappeared after export | Enable "Include Shape Keys" in export settings |
| Weights are all on the wrong bones | Re-run Auto-Weight in the Wizard, or use Weight Transfer |
| Two rigs need to be one | [Guide 11: Merge Two Rigs Together](#guide-11-merge-two-rigs-together) |
| Corrective shape not activating | Check bone axis and activation angle in [Corrective Shape Keys](#corrective-shape-keys) |
| Animation looks wrong on different rig | [Animation Retargeting](#animation-retargeting) — check bone mappings |
| CATS tools are grayed out / unavailable | Run Fix Model first — [CATS Pipeline Order](#cats-plugin--before-you-begin-the-pipeline-order) |
| Mouth tears apart or splits when speaking | Fix Model was skipped — re-run from Phase 1 — [Guide 13, Phase 1](#phase-1--fix-model) |
| Avatar eyes are stuck looking down in VRChat | Eye Tracking Setup ran before Fix Model — re-run from Fix Model — [CATS: Eye Tracking Setup](#eye-tracking-setup) |
| Shape key makes mesh explode when triggered | Pose to Shape Key ran before Fix Model — re-run from Fix Model — [CATS: Shape Key Tools](#shape-key-tools) |
| Avatar spawns at wrong size in VRChat | Apply Transforms ran before completing pipeline — re-import from source, restart from Fix Model |
| Bone names are Japanese / Chinese / Korean | [CATS: Bone Name Translation](#bone-name-translation) |
| Avatar has no lip sync and no existing shape keys | [CATS: Viseme Generator](#viseme-generator-cats) — generate 15 visemes from 3 base shapes |
| CATS Ledger checkmarks disappeared | Mesh was modified after pipeline — run CATS Validator, then re-run affected phases |
| Apply Transforms button still grayed out | Not all 4 earlier Ledger phases are checked — check Validator for which phase is incomplete |

---

# Glossary

**Armature** — Blender's word for a skeleton. A collection of bones that can be posed and animated.

**Blend Shape** — See Shape Key.

**Bone** — A single segment of a skeleton. Bones are arranged in a hierarchy (parent → child) where child bones follow parent bones.

**Bone Collection** — A named group of bones for organizational purposes. You can show or hide entire collections at once.

**CATS** — The CATS Plugin, a suite of model preparation tools added to BoneForge in version 7.1.1. CATS provides a guided pipeline for cleaning, configuring, and VRChat-readying avatars. CATS lives in its own sidebar tab separate from the main BoneForge tabs.

**CATS Pipeline** — The five-phase ordered workflow used by the CATS Plugin: Fix Model → Visemes → Eye Tracking → Pose to Shape → Apply Transforms. Each phase must be completed before the next is available.

**Corrective Shape Key** — A shape key (blend shape) that automatically activates when a bone reaches a specific angle, used to fix mesh deformation at extreme poses.

**Deform Bone** — A bone that is marked as a deformation bone, meaning it directly influences the mesh's shape. Not all bones need to deform the mesh; some exist only as controls.

**Eye Tracking Setup** — The CATS tool that configures your avatar's eye bones (`LeftEye`, `RightEye`) and creates the rotation constraints VRChat uses to drive natural eye movement. Phase 3 of the CATS Pipeline.

**FBT (Full Body Tracking)** — A VRChat feature that uses external hardware (such as Vive Trackers) to track your full body position including hips and feet. BoneForge's Fix FBT tool adjusts the avatar's root bone for correct FBT calibration.

**FBX** — A file format used to transfer 3D models, skeletons, and animations between software. The standard format for VRChat.

**Fix Model** — The CATS tool that performs comprehensive one-click mesh cleanup: removes duplicate vertices, loose geometry, and bad normals. Always the first step in the CATS Pipeline (Phase 1). Every other CATS tool depends on Fix Model having been run first.

**FK (Forward Kinematics)** — A control method where you manually rotate each bone in the chain. Rotating the shoulder bone moves the arm; you then rotate the elbow, then the wrist. Natural for broad body poses.

**IK (Inverse Kinematics)** — A control method where you position the endpoint (like the hand) and the software automatically calculates all the intermediate bone rotations. Natural for precise hand/foot placement.

**Humanoid** — VRChat's built-in avatar system that maps bones to standard body positions so all avatars use the same movement controls.

**Ledger** — The row of checkmarks visible at the top of the CATS panel. Tracks which of the five CATS Pipeline phases have been completed for the current avatar. A filled checkmark (✓) means the phase is done. Tools that depend on earlier phases are grayed out until the required Ledger slots are checked.

**Mark Complete** — A button available next to optional CATS Pipeline phases (Eye Tracking, Pose to Shape). Clicking it marks the phase as complete in the Ledger without running the tool — used when you want to skip an optional phase intentionally.

**Mesh** — The 3D surface geometry that makes up your avatar's visible body.

**MMD (MikuMikuDance)** — A free 3D animation software popular in Japan and the anime community. Uses `.pmx` model files and `.vmd` animation files.

**Morph Target** — See Shape Key.

**PhysBone** — VRChat's component for making bones simulate physics (bounce, swing, collide). Applied to hair, tails, dangling accessories, etc.

**Pipeline** — An ordered sequence of operations where each step depends on the previous one being correct. The CATS Plugin uses a five-phase pipeline to ensure model preparation happens in the correct order.

**PMX** — The main 3D model file format used by MikuMikuDance.

**Pose Mode** — A Blender mode for posing and animating bones. Select the armature, then press **Ctrl+Tab** and choose Pose Mode, or use the dropdown in the top-left of the viewport.

**Rig / Rigging** — The process of building a skeleton inside a 3D model and connecting the mesh to the skeleton so it can be posed and animated.

**Shape Key** — A saved version of a mesh in a specific deformed position. Blend shapes can be blended together or activated at different strengths. Used for facial expressions, lip sync, and body morphs.

**SDK (Software Development Kit)** — In VRChat context, the VRChat Creator Companion and its Unity tools for uploading and managing avatars.

**Spline IK** — An IK system where a chain of bones follows the path of a curve. Used for tails, tentacles, long hair strands, and spines.

**T-Pose** — A reference pose where the character stands upright with arms extended horizontally to the sides. Required for rigging.

**Vertex** — A single point in 3D space. Meshes are made of thousands of vertices connected by edges and faces.

**Vertex Group** — A named selection of vertices in Blender, used to define which vertices are influenced by which bone.

**Viseme** — A specific mouth shape associated with a phoneme (speech sound). VRChat uses 15 visemes for lip sync.

**Viseme Generator** — The CATS tool that mathematically creates all 15 VRChat viseme shape keys from three base shapes (A, O, CH). Phase 2 of the CATS Pipeline. Requires Fix Model ✓ first.

**VMD** — MikuMikuDance animation file format.

**VPD** — MikuMikuDance pose file format.

**VRM** — An open file format for 3D humanoid avatars, used by VRoid Studio and many virtual avatar platforms.

**Weight / Weight Painting** — The process of assigning values (0.0 to 1.0) to each vertex specifying how strongly it is influenced by each bone. Higher weight = more influence. Weight painting is the visual tool for adjusting these values.

**Wizard** — BoneForge's step-by-step guided rigging tool that walks you through placing markers and automatically generating a skeleton.

**Zero Weight Bone** — A bone in a skeleton that has no influence over any mesh vertices. These bones take up performance budget without contributing to the avatar's appearance. The CATS Zero Weight Bone Cleanup tool removes them automatically.

---

*BoneForge Documentation | Version 7.1.3*
*For support, check the BoneForge GitHub page or community Discord.*
