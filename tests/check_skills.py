#!/usr/bin/env python3
"""
Validates all skill files in assets/Skills/:
  1. Every SKILL-*.md has required YAML frontmatter (name, description).
  2. Every skill is listed in the skills table in assets/prompt_template.md.
  3. Every skill is listed in the skills table in assets/Skills/README.md.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
SKILLS_DIR = ROOT / "assets" / "Skills"
PROMPT_TEMPLATE = ROOT / "assets" / "prompt_template.md"
SKILLS_README = SKILLS_DIR / "README.md"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
FIELD_RE = re.compile(r"^(\w+):\s*(.+)$", re.MULTILINE)

errors = []


def parse_frontmatter(path: Path) -> dict:
    text = path.read_text()
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    return dict(FIELD_RE.findall(m.group(1)))


def check_file_mentioned(skill_filename: str, label: str, file_path: Path) -> bool:
    content = file_path.read_text()
    return skill_filename in content


skill_files = sorted(SKILLS_DIR.glob("SKILL-*.md"))

if not skill_files:
    print("WARNING: No SKILL-*.md files found in assets/Skills/")
    sys.exit(0)

for skill_path in skill_files:
    fm = parse_frontmatter(skill_path)

    if not fm:
        errors.append(f"{skill_path.name}: missing YAML frontmatter (must start with ---)")
        continue

    for field in ("name", "description"):
        if field not in fm:
            errors.append(f"{skill_path.name}: frontmatter missing required field '{field}'")
        elif not fm[field].strip():
            errors.append(f"{skill_path.name}: frontmatter field '{field}' is empty")

    if not check_file_mentioned(skill_path.name, "prompt_template.md", PROMPT_TEMPLATE):
        errors.append(
            f"{skill_path.name}: not listed in assets/prompt_template.md ## SKILLS table"
        )

    if not check_file_mentioned(skill_path.name, "Skills/README.md", SKILLS_README):
        errors.append(
            f"{skill_path.name}: not listed in assets/Skills/README.md skills table"
        )

if errors:
    print("FAIL — skill validation errors:")
    for e in errors:
        print(f"  {e}")
    sys.exit(1)

print(f"OK — {len(skill_files)} skill file(s) validated successfully")
