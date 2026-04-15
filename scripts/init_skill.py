#!/usr/bin/env python3
"""
Skill Initializer - Creates a new skill from pattern-specific templates

Usage:
    init_skill.py <skill-name> [--pattern <a|b|c>] [--output-dir DIR]

Creates <skill-name>/ under the output directory (defaults to current working directory).
The --pattern flag selects the structural template (defaults to b).
"""

import sys
import re
from pathlib import Path


PATTERN_A_SKILL = """---
name: {skill_name}
description: "[TODO: What this skill does and WHEN to use it. Include trigger keywords users would naturally say.]"
---

# {skill_title}

[TODO: 1-2 sentences — what tasks this skill handles]

## Supported Task Types

Identify which type the current request belongs to, then follow the corresponding example.

| Type | When to Use | Example File |
| --- | --- | --- |
| [TODO: type-1] | [TODO: trigger condition] | See [examples/type-1.md](examples/type-1.md) |
| [TODO: type-2] | [TODO: trigger condition] | See [examples/type-2.md](examples/type-2.md) |

## Task Identification

Determine the task type by checking:

1. [TODO: First signal to check]
2. [TODO: Second signal to check]
3. If no type matches → ask the user to clarify before proceeding

## Out-of-Scope Handling

Do NOT attempt tasks outside the supported types above. If the request doesn't match:
- Ask the user to rephrase or clarify
- Suggest an alternative skill if applicable

## Cross-Cutting Rules

See [references/shared-principles.md](references/shared-principles.md) for rules that apply to all task types.
"""

PATTERN_B_SKILL = """---
name: {skill_name}
description: "[TODO: What this skill does and WHEN to use it. Include trigger keywords users would naturally say.]"
---

# {skill_title}

[TODO: 1-2 sentences — what process this skill executes]

## Prerequisites

```bash
[TODO: pip install / npm install commands]
```

## Workflow

1. [TODO: Step 1 — describe action, reference script if applicable]
2. [TODO: Step 2]
3. [TODO: Step 3]
4. Validate results — run the validation checklist below

## Branch Logic

Determine the processing type:

**[TODO: Condition A]** → Follow "Workflow Variant A" below
**[TODO: Condition B]** → Follow "Workflow Variant B" below
**Insufficient data** → Ask the user to provide missing information before proceeding

## Validation Checklist

Before delivering results, verify:

- [ ] [TODO: Completeness check]
- [ ] [TODO: Consistency check]
- [ ] [TODO: Evidence/data support check]
- [ ] [TODO: Gaps explicitly flagged]

## References

- **[TODO: Framework/rules]**: See [references/framework.md](references/framework.md)
- **[TODO: Field definitions]**: See [references/field-definitions.md](references/field-definitions.md)
"""

PATTERN_C_SKILL = """---
name: {skill_name}
description: "[TODO: What this skill does and WHEN to use it. Include trigger keywords users would naturally say.]"
---

# {skill_title}

[TODO: 1-2 sentences — what this skill controls]

## Trigger Conditions

Activate this skill when:
- [TODO: Specific trigger 1]
- [TODO: Specific trigger 2]

## Non-Trigger Conditions

Do NOT activate when:
- [TODO: Exclusion 1 — when to use general knowledge instead]
- [TODO: Exclusion 2 — when to suggest a different skill]

## Confirmation Gates

Always confirm with the user before:
- [TODO: Destructive/irreversible action]
- [TODO: Action involving sensitive data]

## Stop Conditions

Stop immediately and escalate when:
- [TODO: Hard failure condition]
- [TODO: Safety/risk threshold exceeded]

## Risk Levels

| Level | Definition | Action |
| --- | --- | --- |
| Low | [TODO] | Proceed normally |
| Medium | [TODO] | Warn user, proceed with confirmation |
| High | [TODO] | Stop, report findings, wait for explicit approval |
| Critical | [TODO] | Stop immediately, do NOT proceed under any circumstances |

## Workflow

[TODO: Only after all boundaries above are defined, write the execution steps]

1. [TODO: Step 1]
2. [TODO: Step 2]
3. [TODO: Step 3]

## References

- **[TODO: Branch-specific procedures]**: See [references/branch-procedures.md](references/branch-procedures.md)
- **[TODO: Risk definitions]**: See [references/risk-definitions.md](references/risk-definitions.md)
"""

PATTERN_SKILLS = {
    'a': PATTERN_A_SKILL,
    'b': PATTERN_B_SKILL,
    'c': PATTERN_C_SKILL,
}

PATTERN_DIRS = {
    'a': {
        'examples': {
            'type-1.md': "# [TODO: Task Type 1]\n\n## When This Applies\n\n[TODO: Trigger conditions]\n\n## Required Inputs\n\n[TODO: What the user must provide]\n\n## Output Structure\n\n[TODO: Sections, order, length]\n\n## Tone and Style\n\n[TODO: Formality, audience]\n\n## Common Mistakes\n\n[TODO: What to avoid]\n",
            'type-2.md': "# [TODO: Task Type 2]\n\n## When This Applies\n\n[TODO: Trigger conditions]\n\n## Required Inputs\n\n[TODO: What the user must provide]\n\n## Output Structure\n\n[TODO: Sections, order, length]\n\n## Tone and Style\n\n[TODO: Formality, audience]\n\n## Common Mistakes\n\n[TODO: What to avoid]\n",
        },
        'references': {
            'shared-principles.md': "# Shared Principles\n\n[TODO: Cross-cutting rules for all task types — writing style, evidence standards, formatting conventions]\n",
        },
        'templates': {},
    },
    'b': {
        'scripts': {
            'example.py': '#!/usr/bin/env python3\n"""[TODO: Repeatable automation script for {skill_name}]"""\n\ndef main():\n    print("[TODO: Implement]")\n\nif __name__ == "__main__":\n    main()\n',
        },
        'references': {
            'framework.md': "# [TODO: Domain Framework]\n\n[TODO: Analysis framework, evaluation criteria, or domain rules]\n",
            'field-definitions.md': "# [TODO: Field Definitions]\n\n[TODO: Field mapping, data schemas, or classification criteria]\n",
        },
        'templates': {
            'report-template.md': "# [TODO: Report Template]\n\n[TODO: Standard output structure]\n",
        },
    },
    'c': {
        'references': {
            'branch-procedures.md': "# Branch Procedures\n\n## [TODO: Branch 1 — e.g., Read-Only Access]\n\n### Entry Conditions\n\n[TODO]\n\n### Steps\n\n[TODO]\n\n### Risk Checkpoints\n\n[TODO]\n\n## [TODO: Branch 2 — e.g., Read-Write Access]\n\n### Entry Conditions\n\n[TODO]\n\n### Steps\n\n[TODO]\n\n### Risk Checkpoints\n\n[TODO]\n",
            'risk-definitions.md': "# Risk Definitions\n\n## Severity Levels\n\n[TODO: Detailed definitions for Low/Medium/High/Critical]\n\n## Escalation Thresholds\n\n[TODO: When to escalate from one level to the next]\n\n## Prohibitions\n\n[TODO: What the skill must NEVER do regardless of user request]\n",
        },
        'templates': {
            'confirmation-request.md': "# Confirmation Request Template\n\n**Action**: [what will be done]\n**Risk Level**: [low/medium/high]\n**Reason for confirmation**: [why this needs approval]\n\nProceed? (yes/no)\n",
        },
    },
}

PATTERN_LABELS = {
    'a': 'Pattern A (Concise SKILL.md + Examples Routing)',
    'b': 'Pattern B (Scripts + References + Branch Logic + Validation)',
    'c': 'Pattern C (Trigger Boundaries + Risk Control + Multi-Branch Docs)',
}


def title_case(name):
    return ' '.join(w.capitalize() for w in name.split('-'))


def validate_name(name):
    if not name or len(name) < 2:
        return False, "Name must be at least 2 characters"
    if len(name) > 64:
        return False, f"Name too long ({len(name)} chars, max 64)"
    if not re.match(r'^[a-z0-9][a-z0-9-]*[a-z0-9]$', name):
        return False, f"Name '{name}' must be hyphen-case (lowercase, digits, hyphens; no leading/trailing hyphens)"
    if '--' in name:
        return False, f"Name '{name}' cannot contain consecutive hyphens"
    return True, ""


def init_skill(skill_name, pattern, output_dir):
    valid, err = validate_name(skill_name)
    if not valid:
        print(f"Error: {err}")
        return None

    if pattern not in PATTERN_SKILLS:
        print(f"Error: Unknown pattern '{pattern}'. Use a, b, or c.")
        return None

    skill_dir = Path(output_dir) / skill_name

    if skill_dir.exists():
        print(f"Error: directory already exists: {skill_dir}")
        return None

    try:
        skill_dir.mkdir(parents=True)
    except Exception as e:
        print(f"Error creating directory: {e}")
        return None

    skill_title = title_case(skill_name)

    (skill_dir / 'SKILL.md').write_text(
        PATTERN_SKILLS[pattern].format(skill_name=skill_name, skill_title=skill_title)
    )

    for dir_name, files in PATTERN_DIRS[pattern].items():
        sub_dir = skill_dir / dir_name
        sub_dir.mkdir(exist_ok=True)
        for filename, content in files.items():
            file_path = sub_dir / filename
            file_path.write_text(content.format(skill_name=skill_name, skill_title=skill_title))
            if filename.endswith('.py'):
                file_path.chmod(0o750)

    label = PATTERN_LABELS[pattern]
    print(f"Skill '{skill_name}' created at {skill_dir}")
    print(f"Design pattern: {label}")
    print("Next: edit SKILL.md, customize or delete placeholder files, then run quick_validate.py")
    return skill_dir


def main():
    args = sys.argv[1:]
    output_dir = "."
    pattern = "b"

    if '--output-dir' in args:
        idx = args.index('--output-dir')
        if idx + 1 >= len(args):
            print("Error: --output-dir requires a value")
            sys.exit(1)
        output_dir = args[idx + 1]
        args = args[:idx] + args[idx + 2:]

    if '--pattern' in args:
        idx = args.index('--pattern')
        if idx + 1 >= len(args):
            print("Error: --pattern requires a value (a, b, or c)")
            sys.exit(1)
        pattern = args[idx + 1].lower()
        args = args[:idx] + args[idx + 2:]

    if len(args) != 1:
        print("Usage: init_skill.py <skill-name> [--pattern <a|b|c>] [--output-dir DIR]")
        print("\n  skill-name: hyphen-case, lowercase, max 64 chars")
        print("  --pattern:  design pattern (default: b)")
        print("    a = Concise SKILL.md + Examples Routing")
        print("    b = Scripts + References + Branch Logic + Validation")
        print("    c = Trigger Boundaries + Risk Control + Multi-Branch Docs")
        print("  --output-dir: where to create the skill (default: current directory)")
        print("\nExamples:")
        print("  init_skill.py ops-chief-of-staff --pattern a")
        print("  init_skill.py industry-research-analyst --pattern b")
        print("  init_skill.py api-integration-operator --pattern c")
        print("  init_skill.py meal-planner --pattern b --output-dir /path/to/skills")
        sys.exit(1)

    result = init_skill(args[0], pattern, output_dir)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
