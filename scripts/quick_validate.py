#!/usr/bin/env python3
"""
Quick validation script for skills

Usage:
    quick_validate.py <path-to-skill>

Accepts a relative or absolute path to a skill directory.
"""

import sys
import re
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None


def parse_frontmatter(text):
    """Extract YAML frontmatter without requiring PyYAML for simple cases."""
    if not text.startswith('---'):
        return None, "No YAML frontmatter found"

    match = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
    if not match:
        return None, "Invalid frontmatter format"

    raw = match.group(1)

    if yaml:
        try:
            data = yaml.safe_load(raw)
            if not isinstance(data, dict):
                return None, "Frontmatter must be a YAML dictionary"
            return data, None
        except yaml.YAMLError as e:
            return None, f"Invalid YAML: {e}"

    # Fallback: simple key: value parsing when PyYAML is unavailable
    MULTILINE_MARKERS = ('>', '|', '>-', '|-')
    data = {}
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if ':' in line:
            key, _, val = line.partition(':')
            val = val.strip()
            if val in MULTILINE_MARKERS:
                return None, (
                    f"Frontmatter key '{key.strip()}' uses YAML multiline syntax ('{val}'). "
                    "Install PyYAML (`pip install pyyaml`) for full YAML support."
                )
            data[key.strip()] = val.strip('"').strip("'")
    return data, None


def validate_skill(skill_path):
    skill_path = Path(skill_path).resolve()

    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "SKILL.md not found"

    content = skill_md.read_text()
    frontmatter, err = parse_frontmatter(content)
    if err:
        return False, err

    ALLOWED_KEYS = {'name', 'description', 'license', 'allowed-tools', 'metadata'}
    unexpected = set(frontmatter.keys()) - ALLOWED_KEYS
    if unexpected:
        return False, f"Unexpected frontmatter key(s): {', '.join(sorted(unexpected))}. Allowed: {', '.join(sorted(ALLOWED_KEYS))}"

    if 'name' not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if 'description' not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    name = str(frontmatter['name']).strip()
    if name:
        if not re.match(r'^[a-z0-9-]+$', name):
            return False, f"Name '{name}' must be hyphen-case (lowercase, digits, hyphens only)"
        if name.startswith('-') or name.endswith('-') or '--' in name:
            return False, f"Name '{name}' has invalid hyphen placement"
        if len(name) > 64:
            return False, f"Name too long ({len(name)} chars, max 64)"

    desc = str(frontmatter.get('description', '')).strip()
    if desc:
        if '<' in desc or '>' in desc:
            return False, "Description cannot contain angle brackets"
        if len(desc) > 1024:
            return False, f"Description too long ({len(desc)} chars, max 1024)"

    warnings = []
    if '[TODO:' in desc or '[TODO:' in name:
        warnings.append("Frontmatter still contains [TODO: placeholders")
    body = content[content.index('---', 3) + 3:].strip() if content.count('---') >= 2 else ''
    if not body:
        warnings.append("SKILL.md body is empty (no content after frontmatter)")

    if warnings:
        return True, "Valid (with warnings):\n  - " + "\n  - ".join(warnings)
    return True, "Valid"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: quick_validate.py <path-to-skill>")
        print("\nExamples:")
        print("  quick_validate.py ./my-skill")
        print("  quick_validate.py /absolute/path/to/skill")
        sys.exit(1)

    path = Path(sys.argv[1]).resolve()
    print(f"Validating: {path}")

    valid, msg = validate_skill(sys.argv[1])
    print(msg)
    sys.exit(0 if valid else 1)
