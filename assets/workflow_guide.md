# MuOS AppBuilder Workflow Guide

## Goal

Provide a repeatable flow for turning a muOS app idea into a working, shareable package.

## Workflow

### 1. Define the app

Use `project_intake_template.md` to capture:

- app goal
- target device
- target muOS version
- desired user experience
- current manual proof of concept

### 1a. Check for a matching skill

Before proceeding, scan `assets/Skills/` for `.md` files. Read the `description` frontmatter of each. If the user's task matches a skill, load it now and let it guide the relevant steps below. Log the skill used in `decisions.md`.

### 2. Identify the likely integration type

Decide whether the app is:

- terminal helper
- `Applications` entry
- archive package
- system tweak or status helper
- service or daemon wrapper

### 3. Prove the manual sequence

Before packaging:

- confirm the app behavior manually over SSH
- keep commands short and incremental
- capture exact working commands

### 4. Inspect muOS integration points

Use the diagnostics cookbook to find:

- relevant `mux*` modules
- state files under `/run/muos/global/...`
- launcher conventions
- existing package/app layouts

### 5. Turn the manual flow into scripts

Start with a script-first version:

- startup helper
- status helper
- launcher wrapper
- stop/cleanup helper

### 6. Add a simple wrapper

When the backend works:

- add a thin menu wrapper
- or add an `Applications` launcher

### 7. Package it

Choose a packaging path:

- terminal-only prototype
- Applications wrapper
- `.muxapp`, `.muxzip`, or `.muxupd` plan

### 8. Verify on-device

Test:

- fresh boot
- clean install
- first run
- repeat run
- stop/restart
- visible UI state if applicable

### 9. Document it

Capture:

- install steps
- launch steps
- known limitations
- fallback/reboot behavior

### 10. Update project memory

Always write down:

- what was proven
- what failed
- exact next step

## Guiding Rule

If something works manually, the next job is to package it.
