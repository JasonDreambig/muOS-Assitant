---
name: muos-godot-project-setup
description: Use when a developer wants to create, normalize, or recover a Godot game project so it remains editable in the Godot editor before packaging it for muOS on RG35XX devices.
---

# muOS Godot Project Setup

Use this skill when the goal is not just to export a game, but to have a clean Godot project the developer can keep editing.

This skill happens before deployment and usually before the final muOS export review.

## Goal

Produce or validate an editable Godot project with a reliable source layout, editor version, core project settings, and a clear path to later export for muOS.

## What to assume first

Clarify which of these situations you are in:

- brand new game idea with no project yet
- existing Godot project that needs muOS-targeted setup
- exported `.pck` or runtime build exists, but source project is missing
- mixed folder of assets and scripts that needs to become a proper Godot project

Important rule:

- A packaged `.pck` is not an editable source project.
- If only exported artifacts exist, say that clearly and help the user rebuild or locate the real source project.

## Editable project definition

For this assistant, a game is "editable in Godot" only if the developer has:

- a real project folder with `project.godot`
- source scenes such as `.tscn`
- source scripts such as `.gd`
- imported assets kept with their source files
- a known Godot editor version that can open the project

## Recommended source layout

Prefer a simple, readable structure:

```text
MyGame/
  project.godot
  icon.png
  README.md
  scenes/
  scripts/
  assets/
    art/
    audio/
    fonts/
  ui/
  autoload/
  exports/
  builds/
```

Guidance:

- keep editable source in the project root
- keep exported builds out of source folders
- use `builds/` or `exports/` for generated output
- do not mix device payload files into the Godot source tree unless there is a strong reason

## Step-by-step workflow

### 1. Confirm the editor version

Ask which Godot version the project should use.

Prefer:

- Godot 4.x for new projects unless the user already depends on Godot 3.x plugins or templates

Record:

- exact editor version
- whether export templates are installed

### 2. Confirm source-editability status

Determine whether the current files already include:

- `project.godot`
- scene files
- scripts
- raw art/audio assets

If not:

- explain that the project is not currently editable in Godot
- either scaffold a new source project or help reconstruct one from available assets

### 3. Normalize the folder structure

Make sure:

- scenes are grouped under `scenes/`
- scripts are grouped under `scripts/`
- source art and audio are organized under `assets/`
- exported `.pck`, device runtimes, and release zips are stored outside source folders

### 4. Set project defaults early

Before feature work grows, establish:

- project name
- version string
- main scene
- input actions
- resolution strategy
- renderer choice
- save path strategy

Recommended defaults for RG35XX-targeted games:

- base resolution: `640x480`
- renderer: Compatibility
- landscape orientation
- frame cap: `60`

### 5. Create the first source milestone

For a new project, the first editable milestone should usually include:

- opening title or boot scene
- main gameplay scene or prototype scene
- input actions wired for handheld controls
- quit handling
- placeholder save/settings path strategy

### 6. Separate source from package artifacts

Keep these distinct:

- editable Godot source project
- exported Linux ARM64 build outputs
- muOS payload layout
- release package layout

Do not treat the muOS `/ports/<game>/` payload as the main development project folder.

## Recovery workflow when only an export exists

If the user only has:

- a `.pck`
- a runtime binary
- a copied payload folder on the device

then respond with this rule:

- those files are sufficient for running the game, but not for editing it in Godot

Then help the user choose one of these paths:

1. locate the original source repository or backup
2. rebuild a new Godot source project from raw assets and gameplay requirements
3. treat the export as runtime reference only and recreate scenes/scripts manually

Do not imply that a `.pck` can be turned back into a fully editable project without loss.

## Relationship to other skills

Use this skill first when the goal is source project setup.

After the project is editable and structured:

- use `SKILL-Input-map.md` for control verification
- use `SKILL-Game-check.md` before export
- use `SKILL-Game-import.md` for on-device deployment

## Deliverable

End with a short status report containing:

- Godot version
- whether the project is truly editable
- missing source pieces, if any
- recommended next implementation step

## What not to forget

- `project.godot` is the minimum editability checkpoint
- `.pck` is a build artifact, not source
- separate source layout from muOS payload layout
- choose renderer and resolution deliberately before content expands
- record the editor version so the project reopens cleanly later
