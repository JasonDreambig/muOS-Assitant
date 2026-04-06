# New Project Creation Protocol

Use this when the user says they want to create a new app or game.

The assistant should not jump straight into code generation. First gather the project intake, then convert the answers into a filled project brief the user can approve.

## Goal

Turn a rough idea into a structured project definition with the fewest questions needed to start productive work.

## Assistant behavior

1. Detect that the user is starting a new project.
2. Ask the intake questions in a short guided sequence.
3. Make reasonable suggestions when the user is unsure.
4. Fill out the project intake template on the user's behalf.
5. Reflect the result back as a concise project brief.
6. Confirm the immediate next build step and then proceed.

## Detection triggers

Use this protocol when the user says things like:

- create a new project
- start a new game
- build a new app
- make a Godot game for muOS
- turn this idea into a project

## Intake sequence

Ask only for information needed to choose the right workflow. Keep the questions practical and in plain language.

### Round 1 — project identity

Ask for:

- project name
- what the project should do
- whether it is a game, app, tool, or port

### Round 2 — build path

Ask for:

- whether this is a brand new build or an existing project
- whether they want an editable Godot project, a device-ready build, or both
- target device and known muOS version if they know it

### Round 3 — gameplay / UX requirements

Ask for:

- main user flow or core gameplay loop
- required controls
- save system needs
- target resolution or art style if relevant

### Round 4 — current assets

Ask for:

- existing files, repos, scenes, or exported builds
- proven commands or working prototypes
- known blockers

## If the user is unsure

Suggest defaults instead of stalling:

- Engine: Godot 4 for new games unless compatibility requirements suggest otherwise
- Target resolution: 640x480 for RG35XX-class devices
- Renderer: Compatibility
- First milestone: editable desktop project first, then muOS packaging
- Save path policy: plan for stable saves from day one

## Output format after intake

After the questions are answered, produce:

1. A filled version of `project_intake_template.md`
2. A short "Project Brief" summary
3. A recommended immediate next step

## Recommended next-step rules

- If the user has only an idea: scaffold the editable Godot project first
- If they already have a Godot project: run the Godot setup workflow and then the game check workflow
- If they only have an exported build: recover or recreate an editable source project before doing muOS-specific packaging
- If they already have a working device build: package and document it

## Project brief template

Use this response shape after the intake is complete:

```markdown
# Project Brief

## Project
- Name:
- Type:
- Goal:

## Build Plan
- Engine / stack:
- Editable source status:
- First output:
- Device target:
- muOS target:

## Design Constraints
- Controls:
- Resolution:
- Performance target:
- Save behavior:

## Current Assets
- Existing files:
- Proven working state:
- Main unknowns:

## Immediate Next Step
- ...
```

## Important rule

Do not treat the intake as busywork. The purpose is to reduce future rework, especially around:

- choosing Godot vs non-Godot workflows
- deciding whether the source is already editable
- avoiding export-only dead ends
- matching the game's controls and display to RG35XX hardware early
