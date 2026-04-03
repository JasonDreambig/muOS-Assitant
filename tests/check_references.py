#!/usr/bin/env python3
"""
Validates cross-reference integrity in assets/prompt_template.md:
  - Every file listed in the REFERENCE ASSETS table actually exists under assets/.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
ASSETS_DIR = ROOT / "assets"
PROMPT_TEMPLATE = ASSETS_DIR / "prompt_template.md"

# Match table rows like: | `workflow_guide.md` | ... |
# Also handles paths like: | `Skills/SKILL-Game-import.md` | ... |
ROW_RE = re.compile(r"\|\s*`([^`]+\.md)`\s*\|")

errors = []

text = PROMPT_TEMPLATE.read_text()

# Only look at rows in the REFERENCE ASSETS section
ref_section_match = re.search(
    r"## REFERENCE ASSETS.*?(?=\n## |\Z)", text, re.DOTALL
)

if not ref_section_match:
    print("FAIL — could not find '## REFERENCE ASSETS' section in prompt_template.md")
    sys.exit(1)

ref_section = ref_section_match.group(0)
referenced_files = ROW_RE.findall(ref_section)

if not referenced_files:
    print("WARNING: No file references found in ## REFERENCE ASSETS table")
    sys.exit(0)

for rel_path in referenced_files:
    full_path = ASSETS_DIR / rel_path
    if not full_path.exists():
        errors.append(f"  {rel_path}: referenced in prompt_template.md but file not found at {full_path}")

if errors:
    print("FAIL — reference integrity errors:")
    for e in errors:
        print(e)
    sys.exit(1)

print(f"OK — {len(referenced_files)} reference(s) validated, all files present")
