# Skills — Authoring Guide

Skills are focused, task-specific guides the AI loads when a user's request matches the skill's scope. They are not run as code — they are read as context and applied as structured guidance.

---

## When to create a skill

Create a skill when a task:

- Has a repeatable workflow with clear steps (e.g., deploy a game, set up Bluetooth, package a port)
- Has gotchas or non-obvious assumptions worth capturing once and reusing
- Goes beyond what the general workflow guide covers

Do not create a skill for one-off decisions or project-specific knowledge — that belongs in the project's `Ai-memory/`.

---

## File naming

Use the format: `SKILL-<short-topic>.md`

Examples:
- `SKILL-Game-import.md`
- `SKILL-Bluetooth-setup.md`
- `SKILL-Archive-packaging.md`

---

## Required format

Every skill file must start with YAML frontmatter:

```markdown
---
name: skill-slug-here
description: One sentence explaining when to trigger this skill — this is what the AI matches against the user's task.
---
```

The `description` is the trigger. Write it as a clear statement of the task type, not a vague topic name.

Good: `Use when deploying or importing a game or native port onto muOS by hand.`  
Too vague: `Game stuff`

---

## Recommended sections

After the frontmatter, structure the skill with these sections (use only what applies):

```markdown
# Skill Title

Brief statement of when to use this skill.

## What to assume first
Key assumptions to clarify with the user before acting.

## Correct folder / file structure
The expected layout on device or on disk.

## Step-by-step workflow
Numbered steps the AI should follow or surface to the user.

## Launcher / script pattern
Boilerplate code pattern with notes.

## Verification
How to confirm the task succeeded before calling it done.

## Practical reminders
Short bullets for things commonly forgotten.

## What not to forget
Non-obvious constraints or failure modes specific to this skill.
```

Not every section is required. Only include sections that carry real guidance.

---

## Keeping the prompt_template.md in sync

After adding a new skill, update the skills table in `assets/prompt_template.md` under the `## SKILLS` section:

```markdown
| `Skills/SKILL-YourSkill.md` | One-line trigger description |
```

This ensures the AI knows the skill exists without having to scan the folder from scratch each time.

---

## Current skills

| File | Trigger |
|---|---|
| `SKILL-Game-import.md` | Deploying or importing a game, port, or runtime onto the device by hand |
| `SKILL-Input-map.md` | Mapping handheld controls on muOS — raw input capture, evtest, D-pad, face buttons, sticks, triggers, and translating results into game or engine mappings |
