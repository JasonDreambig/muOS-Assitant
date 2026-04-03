# MuOS AI AppBuilder Plan

## Project Name

`MuOS-Ai-AppBuilder`

## Project Goal

Create an AI assistant system that helps design, build, package, debug, and ship applications for muOS on RG35XX-class handhelds.

The assistant should help with:

- muOS app architecture
- package structure
- launcher scripts
- runtime setup
- troubleshooting on-device behavior
- SSH-driven diagnostics
- compatibility decisions
- documentation and release packaging

## Core Vision

The long-term vision is an AI assistant that acts like a dedicated muOS app engineer.

It should be able to help a developer:

1. define a muOS app idea
2. choose the right app structure
3. create the first scripts/assets
4. debug behavior live over SSH
5. package the app for sharing
6. maintain project memory between sessions

This should become a reusable workflow system, not just a pile of notes.

## Why This Project Makes Sense

We now know a number of muOS-specific facts from real device work:

- muOS uses structured launcher and archive workflows
- `mux*` modules drive large parts of the UI
- state files under `/run/muos/global/...` can influence UI behavior
- app bring-up often depends on shell scripts and practical device inspection
- SSH is extremely useful for debugging real device behavior

That means an assistant specialized for muOS can provide real value beyond a generic coding assistant.

## Product Definition

This project should produce:

1. A muOS-focused assistant specification
2. A reusable prompt/behavior asset
3. A project template for new muOS app ideas
4. Debugging playbooks for common muOS app issues
5. Packaging templates for apps and archives
6. A living knowledge base / memory system

## What The Assistant Should Be Able To Do

### Planning

- turn a muOS app idea into a build plan
- identify likely system hooks
- define package format and launcher structure
- identify technical unknowns and risk areas

### Scaffolding

- generate shell scripts
- generate menu wrappers
- generate installer scripts
- generate package layouts
- generate README and release docs

### Debugging

- suggest SSH inspection commands
- interpret `dmesg`, `ps`, `rfkill`, `bluetoothctl`, `find`, and other device-side outputs
- isolate whether a problem is:
  - missing binary
  - missing daemon
  - missing firmware
  - wrong file path
  - muOS UI integration issue
  - package layout issue

### Packaging

- prepare `.muxapp`, `.muxzip`, or `.muxupd` style plans
- define wrapper scripts for `Applications`
- help connect terminal helpers into muOS UI launch points

### Release support

- draft release notes
- prepare installation instructions
- identify which files need to be bundled
- suggest GitHub release structure

## Target Use Cases

### Use case 1: Build a simple helper app

Examples:

- Bluetooth keyboard app
- Wi-Fi helper
- file sync tool
- launcher wrapper

### Use case 2: Debug a partially working app

Examples:

- app runs from terminal but not Applications
- Bluetooth works manually but not through startup script
- package installs but does not launch

### Use case 3: Create a reusable shareable package

Examples:

- convert a working shell script into a real muOS app
- add metadata, icons, and install flow

## Recommended Outputs / Assets

This project should contain:

### 1. Assistant charter

A document that describes:

- what the assistant knows
- what it should optimize for
- how it should debug muOS projects

### 2. Prompt template

A reusable system/developer-style prompt for a muOS assistant.

### 3. Project intake template

A template for new muOS app ideas:

- project goal
- device target
- package type
- UI target
- runtime dependencies
- current status

### 4. SSH diagnostics cookbook

A list of tested command groups for:

- Bluetooth
- networking
- files
- apps
- muOS UI integration
- package inspection

### 5. Packaging templates

Starter structures for:

- simple terminal app
- Applications wrapper app
- archive package

### 6. Debugging patterns

Examples:

- "binary exists but daemon not running"
- "state file controls UI glyph"
- "working manual sequence needs packaging"

## Product Scope

### In scope for phase 1

- assistant plan
- prompt asset
- project template
- diagnostics reference
- package draft templates
- memory system

### In scope for phase 2

- reusable scripts for common muOS workflows
- starter app templates
- archive packaging helper
- release checklist

### In scope for phase 3

- richer app-generation workflows
- semi-automated packaging
- integration with GitHub release conventions
- interactive troubleshooting scripts

### Out of scope for now

- building a full autonomous coding agent product
- GUI chatbot on-device
- broad support for every Linux handheld OS

## Recommended Architecture

## Layer 1: Knowledge base

Store known muOS facts and patterns:

- file locations
- module names
- status file conventions
- package/install conventions
- device debugging workflows

## Layer 2: Prompt assets

Provide consistent AI behavior for:

- planning
- debugging
- packaging
- documentation

## Layer 3: Templates

Provide ready-to-use templates for:

- project plans
- memory files
- startup scripts
- package layouts

## Layer 4: Debugging playbooks

Provide tested flows for:

- Bluetooth bring-up
- connectivity UI hooks
- app launcher integration
- device-side diagnosis

## Key Lessons Already Learned

The assistant should encode lessons such as:

- muOS often exposes UI state through files in `/run/muos/global/...`
- `muxconnect` and similar `mux*` binaries are key integration points
- manual shell success should be treated as a packaging opportunity, not the final state
- device debugging should favor small, incremental commands
- a lot of value comes from reading the real device state, not guessing

## Recommended First Deliverables

1. Assistant charter
2. Prompt template
3. Project intake template
4. SSH diagnostics cookbook
5. Packaging template outline
6. AI memory scaffolding

## Immediate Next Actions

1. Create the assistant charter
2. Create the prompt template
3. Create the project intake template
4. Create a diagnostics cookbook
5. Add the first packaging template references

## Bottom-Line Recommendation

This project should become a reusable muOS engineering copilot system.

It should be optimized for:

- real device debugging
- practical packaging
- maintaining project memory
- turning rough experiments into shareable muOS apps
