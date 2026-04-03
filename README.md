# MuOS AI AppBuilder

MuOS AI AppBuilder is a project workspace for creating a reusable AI-assisted workflow for building and debugging muOS applications on RG35XX-class handhelds.

## Purpose

This project turns hard-won muOS experience into reusable assets:

- project planning templates
- prompt assets
- debugging playbooks
- packaging templates
- release checklists
- memory scaffolding

## Folder Guide

- [`muos_ai_appbuilder_plan.md`](muos_ai_appbuilder_plan.md)
  Main project plan.

- [`assets`](assets/)
  Reusable assistant assets, prompts, templates, and references.

- `Ai-memory/` (gitignored, created per-project)
  Project memory system for resuming work cleanly.

## Current Status

The first version includes:

- assistant charter
- prompt template
- project intake template
- diagnostics cookbook
- troubleshooting patterns
- package layout templates
- release checklist
- workflow guide

## How to Use

### Starting a new project

**1. Load the assistant**

Open a new AI session (Claude, ChatGPT, or similar). Paste the full contents of [`assets/prompt_template.md`](assets/prompt_template.md) as the system prompt or first message. This gives the AI its muOS context — device facts, file paths, packaging conventions, debugging taxonomy, and the skills index.

**2. Fill out the intake template**

Copy [`assets/project_intake_template.md`](assets/project_intake_template.md) and fill in the fields for your project: app name, goal, target device, desired UX, and any manual steps you've already proven. Hand the filled-out template to the AI.

**3. Let the AI lead**

The AI will follow the 10-step workflow in [`assets/workflow_guide.md`](assets/workflow_guide.md) — from defining the app through proving it manually, scripting it, packaging it, and verifying it on-device. You don't need to read the workflow yourself; the AI knows it.

**4. Debug with the cookbook**

When something breaks on the device, ask the AI to diagnose it. It will pull commands from [`assets/ssh_diagnostics_cookbook.md`](assets/ssh_diagnostics_cookbook.md) and [`assets/troubleshooting_patterns.md`](assets/troubleshooting_patterns.md). You run the commands over SSH and paste the output back — the AI interprets and responds.

**5. Package using the templates**

When the app works manually, the AI will help you turn it into a proper muOS package. It references [`assets/package_templates.md`](assets/package_templates.md) for the right folder layout depending on your app type (terminal helper, Applications entry, or archive package).

**6. Use skills for specific tasks**

Some tasks have dedicated skill guides in [`assets/Skills/`](assets/Skills/). The AI checks for a matching skill at the start of any focused task (e.g. deploying a game port) and loads the relevant one automatically. You can also ask for a skill by name.

**7. Ship it**

Before releasing, work through [`assets/release_checklist.md`](assets/release_checklist.md) with the AI. It covers packaging, permissions, UX verification, and GitHub release structure.

---

### Resuming a session

If you created an `Ai-memory/` folder in a previous session, point the AI to it at the start of the new session:

> "Continue the project. Memory files are in `Ai-memory/`."

The AI will read `project_memory_report.md`, `decisions.md`, and `next_steps.md` to pick up exactly where you left off — no re-explaining required.

---

### Adding new skills

If you find yourself doing the same kind of task repeatedly, it's a candidate for a skill. Follow the authoring guide in [`assets/Skills/README.md`](assets/Skills/README.md) to write a new `SKILL-*.md` file, then add it to the skills table in `assets/prompt_template.md`.
