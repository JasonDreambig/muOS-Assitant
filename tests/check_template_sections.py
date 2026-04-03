#!/usr/bin/env python3
"""
Validates that required Markdown headings are present in template files.

Rules:
  - assets/project_intake_template.md must contain all required intake headings.
  - Each SKILL-*.md must contain at least one of the recommended skill sections.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
ASSETS_DIR = ROOT / "assets"
SKILLS_DIR = ASSETS_DIR / "Skills"

errors = []

# ---------------------------------------------------------------------------
# project_intake_template.md — these headings are the contract with the AI
# ---------------------------------------------------------------------------
INTAKE_REQUIRED = [
    "## Project Name",
    "## Goal",
    "## Target Device",
    "## Target muOS Version",
    "## App Type",
    "## Desired User Experience",
    "## Current Working State",
    "## Proven Manual Commands",
    "## Risks / Unknowns",
    "## Immediate Next Step",
]

intake_path = ASSETS_DIR / "project_intake_template.md"
intake_text = intake_path.read_text()

for heading in INTAKE_REQUIRED:
    if heading not in intake_text:
        errors.append(f"project_intake_template.md: missing required section '{heading}'")

# ---------------------------------------------------------------------------
# SKILL-*.md — every skill must have at least a title heading and one section
# ---------------------------------------------------------------------------
SKILL_MINIMUM_SECTIONS = [
    "## What to assume first",
    "## Correct folder",
    "## Step-by-step",
    "## Verification",
    "## Practical reminders",
    "## What not to forget",
    "## Launcher",
]

for skill_path in sorted(SKILLS_DIR.glob("SKILL-*.md")):
    text = skill_path.read_text()

    # Must have at least one H1 title after frontmatter
    lines = text.splitlines()
    h1_lines = [l for l in lines if l.startswith("# ") and not l.startswith("# ---")]
    if not h1_lines:
        errors.append(f"{skill_path.name}: missing H1 title heading")

    # Must have at least one recognised section heading
    has_section = any(s in text for s in SKILL_MINIMUM_SECTIONS)
    if not has_section:
        errors.append(
            f"{skill_path.name}: contains no recognised skill sections "
            f"(expected at least one of: {', '.join(SKILL_MINIMUM_SECTIONS)})"
        )

if errors:
    print("FAIL — template section errors:")
    for e in errors:
        print(f"  {e}")
    sys.exit(1)

print("OK — all template sections validated successfully")
