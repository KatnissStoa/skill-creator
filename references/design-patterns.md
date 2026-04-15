# Skill Design Patterns

Three structural patterns cover the vast majority of skill use cases. **Select the pattern before writing any content** — the pattern determines SKILL.md's role, directory layout, and where complexity lives.

## Pattern A: Concise SKILL.md + Examples Routing

**Best for:** SOPs, internal communications, document production, bounded personal workflow assistants — tasks where the core challenge is **recognizing which sub-task the user wants and routing to the right template/example**.

### Structural Requirements

```
skill-name/
├── SKILL.md            # Task classifier + router only (short)
├── examples/           # One file per sub-task type (the real content lives here)
│   ├── weekly-report.md
│   ├── meeting-notes.md
│   └── project-update.md
├── references/         # Cross-cutting rules shared by all sub-tasks
│   └── writing-principles.md
└── templates/          # Minimal viable output templates (optional)
    └── report-template.md
```

### SKILL.md Role

SKILL.md is a **dispatcher**, not an encyclopedia. It should:

1. List the supported task types (3–7 types max)
2. Define how to identify which type the current request belongs to
3. Point to the corresponding example file for each type
4. State what to do when the request doesn't match any type (ask for clarification or reject)

SKILL.md should NOT contain the detailed format, tone, structure, or rules for each sub-task — those go in `examples/`.

### examples/ Structure

Each file in `examples/` defines one sub-task type and must include:

- **When this applies** — trigger conditions for this sub-task
- **Required inputs** — what the user must provide
- **Output structure** — sections, order, length guidance
- **Tone and style** — formality level, audience expectations
- **Common mistakes** — what to avoid for this specific type

### references/ Role

Only cross-cutting rules that apply to ALL sub-tasks:

- Writing principles (conclusion-first, evidence standards)
- Terminology glossary
- Shared formatting conventions

### Anti-Patterns

- Cramming all sub-task details into SKILL.md
- Having examples/ files that are just output templates without process guidance
- Building scripts for tasks that are better handled as text instructions

### Pattern A Query Keywords

When a user's request contains these signals, use Pattern A:

- "help me handle several types of tasks"
- "different kinds of documents/reports"
- "route to the right template"
- "task recognition", "task classification"
- SOP, chief of staff, workflow assistant, document writer
- Focus on categorization, not computation

---

## Pattern B: Scripts + References + Branch Logic + Validation

**Best for:** Industry research, file processing, data pipelines, meal planning, quantitative analysis — tasks where the core challenge is **executing repeatable multi-step processes with branching conditions and quality checks**.

### Structural Requirements

```
skill-name/
├── SKILL.md            # Process controller + module orchestrator
├── scripts/            # Repeatable automation (the core value lives here)
│   ├── analyze.py
│   ├── transform.py
│   └── validate.py
├── references/         # Domain rules, frameworks, decision criteria
│   ├── analysis-framework.md
│   ├── field-mapping.md
│   └── exception-rules.md
└── templates/          # Output structure templates
    ├── report-template.md
    └── comparison-template.md
```

### SKILL.md Role

SKILL.md is a **process controller**. It should:

1. Define the end-to-end workflow as numbered steps
2. Specify which script to run at each step
3. Define branch conditions — when to take path X vs path Y
4. Specify the final validation/QA checklist
5. Define when to stop or escalate to the user

SKILL.md should NOT contain domain-specific rules, detailed frameworks, or field-level specifications — those go in `references/`.

### scripts/ Structure

Scripts handle **repeatable, mechanical actions**:

- Data extraction, transformation, formatting
- Comparison table generation
- Field validation and completeness checks
- Batch processing and aggregation
- Output standardization

Each script should be runnable independently with clear CLI arguments.

### references/ Structure

References hold **domain knowledge the model doesn't reliably have**:

- Analysis frameworks and evaluation criteria
- Field definitions and mapping rules
- Exception handling rules and edge cases
- Priority and severity definitions
- Industry-specific standards

### Branch Logic Requirements

SKILL.md must explicitly define branches for common variations:

```
Determine the analysis type:
  Single entity analysis → Follow "Single Analysis" workflow
  Multi-entity comparison → Follow "Comparison" workflow
  Sector scan → Follow "Scan" workflow
  Insufficient data → Follow "Data Gap" protocol
```

Each branch should specify: entry conditions, steps, expected output, and exit criteria.

### Validation Requirements

Every Pattern B skill must end with a validation step that checks:

- Completeness — are all required sections/fields present?
- Consistency — do numbers/claims align across sections?
- Evidence — are conclusions supported by data (no unsupported assertions)?
- Gaps — are missing data points explicitly flagged?

### Anti-Patterns

- Putting all domain rules in SKILL.md instead of references/
- Scripts that require context-window loading (defeats the purpose)
- Missing branch logic — treating all inputs the same way
- No validation step at the end
- Writing "analysis instructions" without scripts for the repeatable parts

### Pattern B Query Keywords

When a user's request contains these signals, use Pattern B:

- "structured analysis", "research framework", "evaluation"
- "file processing", "data pipeline", "batch", "transform"
- "meal plan", "nutrition", "recipe", "shopping list"
- "scoring model", "comparison matrix", "standard report"
- Focus on process, computation, repeatable steps

---

## Pattern C: Trigger Boundaries + Risk Control + Multi-Branch Documentation

**Best for:** API integrations, quality reviews, wellness coaching, multi-agent orchestration — tasks where the core challenge is **knowing when to act, when to refuse, when to confirm, and how to handle high-risk situations**.

### Structural Requirements

```
skill-name/
├── SKILL.md            # Boundary definitions + risk rules (the core value is in the constraints)
├── references/         # Branch-specific detailed procedures
│   ├── auth-patterns.md
│   ├── error-handling.md
│   ├── risk-levels.md
│   └── escalation-rules.md
├── scripts/            # Operational scripts (optional, for automation)
│   └── validate.py
└── templates/          # Output templates for different outcomes
    ├── confirmation-request.md
    ├── error-report.md
    └── result-summary.md
```

### SKILL.md Role

SKILL.md is a **boundary enforcer**. Its sections should appear in this order:

1. **Trigger conditions** — WHEN this skill activates (be exhaustive)
2. **Non-trigger conditions** — WHEN this skill must NOT activate (equally important)
3. **Confirmation gates** — WHAT requires user confirmation before proceeding
4. **Stop conditions** — WHEN to halt and escalate
5. **Risk levels** — severity definitions and corresponding actions
6. **Workflow** — the actual execution steps (comes AFTER all boundaries are defined)

SKILL.md should NOT contain variant-specific procedures — those go in `references/` organized by branch.

### Boundary Definition Requirements

**Trigger conditions** must be specific:

```
Activate when:
- User asks to call [specific API]
- User provides API credentials and a query
- User references a configured data source

Do NOT activate when:
- User asks about APIs in general (use general knowledge)
- Request involves an unconfigured/unknown API
- Request would modify production data without explicit confirmation
```

**Confirmation gates** must list every action requiring user approval:

```
Always confirm before:
- Any write/delete/update operation
- First-time use of new credentials
- Queries touching PII or financial data
- Operations exceeding rate limits
```

**Stop conditions** must define hard limits:

```
Stop immediately and escalate when:
- Authentication fails twice consecutively
- Response contains unexpected PII
- User describes symptoms of a medical emergency (wellness context)
- Conflict between agents cannot be resolved by rules (multi-agent context)
```

### references/ Structure (Multi-Branch)

Organize by **branch/variant**, not by topic:

```
references/
├── branch-read-only.md      # Procedures for read-only API access
├── branch-read-write.md     # Procedures for read-write access (stricter)
├── branch-error-recovery.md # What to do when things fail
└── risk-definitions.md      # Severity levels and escalation thresholds
```

Each branch file includes: entry conditions, step-by-step procedure, risk checkpoints, and exit criteria.

### Risk Control Requirements

Every Pattern C skill must define:

1. **Risk levels** (e.g., low/medium/high/critical) with clear definitions
2. **Actions per level** — what the skill does at each risk level
3. **Escalation path** — how to hand off to the user at each level
4. **Prohibitions** — what the skill must NEVER do regardless of user request

### Anti-Patterns

- Defining trigger conditions but not non-trigger conditions
- Missing confirmation gates for destructive operations
- Writing a "helpful assistant" instead of a constrained operator
- Putting all procedures in SKILL.md instead of branching to references/
- Risk levels defined but with no corresponding actions
- "Soft" stop conditions that can be overridden too easily

### Pattern C Query Keywords

When a user's request contains these signals, use Pattern C:

- "API", "integration", "authentication", "credentials"
- "review", "audit", "quality check", "compliance"
- "wellness", "health", "coaching", "mental health"
- "multi-agent", "orchestration", "delegation", "escalation"
- "when to refuse", "risk", "boundary", "confirmation"
- Focus on constraints, safety, boundaries

---

## Hybrid Patterns

Some scenarios combine patterns. The dominant pattern determines SKILL.md structure; the secondary adds specific requirements:

**B + C (e.g., Stock/Crypto Analysis)**
- Primary: Pattern B (scripts, frameworks, branch logic, validation)
- Add from C: Risk disclaimers, prohibition on investment advice, uncertainty flagging

**A + B (e.g., Research with document templates)**
- Primary: Pattern A (task routing to different document types)
- Add from B: Scripts for data processing, validation checklist

When combining, keep SKILL.md structured according to the primary pattern and add the secondary pattern's requirements as a clearly labeled section.
