---
name: skill-creator
description: Guide for creating or updating skills that extend an agent's capabilities via specialized knowledge, workflows, or tool integrations. For any modification or improvement request, MUST first read this skill and follow its update workflow instead of editing files directly.
license: Complete terms in LICENSE.txt
---

# Skill authoring

This document guides you through creating effective skills.

## User-facing communication (required)

When talking to the user—especially when they ask to **create**, **design**, or **improve** a skill (e.g. “help me create a skill”):

- **Never** say you are loading, invoking, switching to, or using a named skill or workflow package. Do not name this guidance, its folder, or any skill identifier (e.g. phrases like “load skill creator”, “using Skill Creator”, “the skill-creator skill”, “I’ve activated …”).
- **Never** explain *which* internal resource you are following—only *what* you will do for them next.
- **Do** use plain language: walk through design choices, ask brief clarifying questions **only when the request is underspecified**, scaffold files, and describe steps as normal assistant work (“I’ll help you structure this”, “Here’s the next step”).

These rules apply to every step below; they do not change the technical workflow, only how you frame it to the user.

## About Skills

Skills are modular, self-contained packages that extend an agent's capabilities by providing specialized knowledge, workflows, and tools — procedural knowledge that no model fully possesses on its own.

### What Skills Provide

1. Specialized workflows - Multi-step procedures for specific domains
2. Tool integrations - Instructions for working with specific file formats or APIs
3. Domain expertise - Company-specific knowledge, schemas, business logic
4. Bundled resources - Scripts, references, and assets for complex and repetitive tasks

## Core Principles

### Concise is Key

The context window is a shared resource. Only add context the agent doesn't already have. Prefer concise examples over verbose explanations.

### Set Appropriate Degrees of Freedom

- **High freedom** (text instructions): Multiple valid approaches, context-dependent decisions
- **Medium freedom** (pseudocode/parameterized scripts): Preferred pattern exists, some variation acceptable
- **Low freedom** (specific scripts): Fragile operations, consistency critical, exact sequence required

### Anatomy of a Skill

```
skill-name/
├── SKILL.md (required)       - YAML frontmatter (name + description) + markdown instructions
└── Bundled Resources (optional)
    ├── scripts/              - Executable code (Python/Bash/etc.)
    ├── references/           - Documentation loaded into context as needed
    ├── examples/             - Sub-task templates (Pattern A) or input/output pairs
    └── templates/            - Output assets (logos, fonts, boilerplate)
```

- **Frontmatter** fields `name` and `description` determine when the skill triggers. Be clear and comprehensive.
- **Body** loads only after triggering. Keep under 500 lines.
- **`scripts/`** — token efficient, runs without loading into context
- **`references/`** — loaded as needed. For large files (>10k words), include grep patterns in SKILL.md
- **`examples/`** — sub-task specific write-ups (Pattern A) or input/output demonstrations
- **`templates/`** — output assets, not loaded into context

Avoid duplication: information lives in SKILL.md OR references, not both. Do NOT include README.md or CHANGELOG.md.

## Security (required)

Before you **initialize**, **merge**, or **deliver** any skill, apply `references/security-vetting.md`. There are two entry paths:

1. **Imported skill** — User uploads a package (folder/zip) or gives a downloadable link/repo to adopt.
   - Obtain and read all files; run `scripts/security_scan.py` on the extracted skill directory when it exists on disk.
   - Produce the vetting report format from that reference. If risk is not clearly **LOW**, or red flags remain, **tell the user what is wrong** and **ask whether they still want to create/adopt** the skill. Do not run `init_skill.py` or copy their tree into a new skill until they explicitly confirm (or they withdraw).
2. **Authored in chat** — No import; you draft the skill from the conversation.
   - After the draft exists as files, run the same review and `security_scan.py` when applicable.
   - If you find issues, **fix the artifact yourself** (remove exfiltration, narrow scope, replace dangerous instructions with safe, explicit steps), re-scan or re-read, then deliver the **final** content. Only ask the user if fixing would **change the stated purpose** in a way they must choose (e.g. removing a feature).

Do not name internal policy files to the user; just do the review and describe findings in plain language.

### Progressive Disclosure

Three-level loading: Metadata (~100 words) → SKILL.md body (<500 lines) → Bundled resources (as needed).

Keep core workflow in SKILL.md; move variant-specific details to reference files. See `references/progressive-disclosure-patterns.md` for splitting strategies.

## Design Patterns

Every skill fits one of three structural patterns. **Select the pattern before writing any content** — the pattern determines SKILL.md's role, directory layout, and where complexity lives.

### Quick Pattern Selection

Read the user's request and identify the primary challenge:

**Pattern A — Concise SKILL.md + Examples Routing**
- Primary challenge: recognizing sub-task types and applying the right format/template
- SKILL.md role: task classifier and dispatcher
- Best for: SOPs, document production, bounded workflow assistants
- Signals: "different types of tasks", "several document formats", "route to the right template"

**Pattern B — Scripts + References + Branch Logic + Validation**
- Primary challenge: executing repeatable multi-step processes with quality checks
- SKILL.md role: process controller and orchestrator
- Best for: research analysis, file processing, data pipelines, meal/nutrition planning, quantitative scoring
- Signals: "structured analysis", "batch processing", "validation", "scoring model"

**Pattern C — Trigger Boundaries + Risk Control + Multi-Branch Docs**
- Primary challenge: knowing when to act, when to refuse, when to confirm
- SKILL.md role: boundary enforcer
- Best for: API integrations, quality reviews, wellness coaching, multi-agent orchestration
- Signals: "API credentials", "quality audit", "risk control", "when to refuse"

**Hybrid B+C** — Use Pattern B structure + add Pattern C risk controls. For scenarios like stock/crypto analysis that need both process rigor and risk disclaimers.

If uncertain, see `references/scenario-routing.md` for the full decision tree, keyword detection heuristic, and scenario-to-pattern mapping. See `references/design-patterns.md` for detailed structural requirements of each pattern.

## Skill Creation Process

All paths in the steps below (e.g. `scripts/init_skill.py`, `references/workflows.md`) are **relative to this skill's root directory** — the directory where this SKILL.md is located. Resolve them from that base before executing.

0. **Security gate** — If the user brought an external skill (upload or URL), vet **before** scaffolding or merging (see **Security (required)** and `references/security-vetting.md`). If they confirm despite warnings, proceed. If the skill is only authored in chat, vet and remediate **before** final delivery (same reference).

1. **Route** — identify the design pattern
2. **Understand** — gather concrete examples from the user’s description and/or from supplied files or fetched content (see Step 2); skip extra requirement questions when already specified
3. **Plan** — decide reusable contents based on the pattern
4. **Initialize** — scaffold the skill
5. **Edit** — implement resources and write SKILL.md
6. **Validate** — run checks and deliver
7. **Iterate** — improve from real usage

### Step 0: Security gate

Follow **Security (required)** and `references/security-vetting.md` at the appropriate time:

- **Imported skill** — Complete source review and user confirmation (if needed) **before** Step 4.
- **Authored in chat** — Run full vetting and remediation **before** final delivery in Step 6.

### Step 1: Route to Design Pattern

Analyze the user's request and select the design pattern autonomously:

1. Scan for keyword signals (see Quick Pattern Selection above)
2. If ambiguous, consult `references/scenario-routing.md` for the full decision tree
3. If still unclear after routing analysis, ask: "Does this skill primarily need to (A) route different task types, (B) run repeatable analysis processes, or (C) enforce risk boundaries?"
4. Read `references/design-patterns.md` for the selected pattern's structural requirements

Do NOT ask the user to confirm the pattern choice — decide based on signals and proceed. Only ask when signals are genuinely ambiguous after consulting the routing guide.

### Step 2: Understand the Skill

**Skip requirement clarification when the user already gave enough to proceed.** Go straight to Step 3 (Plan)—and run Step 0 (Security) on schedule when importing—if **any** of these holds:

1. **Explicit description** — They stated a usable spec: purpose, scope, triggers, outputs, constraints, or other concrete detail (more than a bare “create a skill” with no substance).
2. **Uploaded skill package** — They attached or provided paths to an existing skill folder/zip in the workspace you can read.
3. **Downloadable skill link** — They gave a URL or repo link to fetch or clone; use retrieved files as the source of truth for requirements.

In those cases, infer gaps from context and sensible defaults; **do not** send a blocking “one question first” message for requirements.

**When the request is still underspecified** (e.g. only “help me create a skill” with no detail and no files/link), ask **one** brief clarification before proceeding. Keep it short; combine at most 2 key unknowns in a single message. End with: *"Or just say 'go' and I'll generate with sensible defaults."*

Pick the most important unknown based on the pattern:

- **Pattern A**: "What are the main task types this skill should handle?"
- **Pattern B**: "Any specific frameworks, data sources, or output format preferences?"
- **Pattern C**: "Any hard boundaries — things the skill must never do?"

Do NOT ask multiple rounds of questions. One message, then proceed — either with the user's answer or with defaults.

**Note:** Skipping requirement questions does **not** skip **Security (required)** or user confirmation when vetting finds non‑LOW risk on an import—those are separate from requirement gathering.

### Step 3: Plan Reusable Contents

| Resource Type | When to Use                     | Example                             |
| ------------- | ------------------------------- | ----------------------------------- |
| `scripts/`    | Code rewritten repeatedly       | `rotate_pdf.py` for PDF rotation    |
| `templates/`  | Same boilerplate each time      | HTML/React starter for webapp       |
| `references/` | Documentation needed repeatedly | Database schemas for BigQuery skill |
| `examples/`   | Sub-task write-ups (Pattern A)  | `weekly-report.md` with format/tone |

**Pattern-specific planning:**

**Pattern A** — Plan one example file per sub-task type. Each defines: trigger conditions, required inputs, output structure, tone/style, common mistakes. References hold only cross-cutting rules.

**Pattern B** — Plan scripts for every repeatable mechanical action. Plan references for every domain framework/rule set the model doesn't reliably know. Plan branch logic for every meaningful variation. Plan a validation checklist.

**Pattern C** — Plan SKILL.md sections in this order: trigger conditions → non-trigger conditions → confirmation gates → stop conditions → risk levels → workflow. Plan references organized by branch (not by topic).

### Step 4: Initialize the Skill

Skip if the skill already exists and only needs iteration.

Run `init_skill.py` to scaffold a new skill with the appropriate pattern:

```bash
python scripts/init_skill.py <skill-name> --pattern <a|b|c>
python scripts/init_skill.py <skill-name> --pattern b --output-dir /path/to/skills
```

The `--pattern` flag creates pattern-specific directory structure and SKILL.md template. Defaults to pattern B if not specified.

### Step 5: Edit the Skill

The skill is for another agent instance to use. Include non-obvious procedural knowledge and domain-specific details.

#### Pattern-Specific SKILL.md Structure

**Pattern A SKILL.md sections:**
1. Overview — what tasks this skill handles
2. Supported task types — list with brief descriptions
3. Task identification — how to determine which type matches the request
4. Routing table — task type → example file mapping
5. Out-of-scope handling — what to do for unrecognized requests
6. Cross-cutting rules — reference to shared principles

**Pattern B SKILL.md sections:**
1. Overview — what process this skill executes
2. Prerequisites — dependencies, setup
3. Workflow — numbered steps with script invocations
4. Branch logic — decision points with clear conditions
5. Validation checklist — quality gates at the end
6. Error handling — what to do when steps fail

**Pattern C SKILL.md sections:**
1. Trigger conditions — when to activate (exhaustive list)
2. Non-trigger conditions — when NOT to activate (equally important)
3. Confirmation gates — what requires user approval
4. Stop conditions — when to halt immediately
5. Risk levels — severity definitions and actions
6. Workflow — execution steps (comes AFTER all boundaries)

#### Design References

Consult these based on your needs:
- **Multi-step processes**: See `references/workflows.md`
- **Output formats or quality standards**: See `references/output-patterns.md`
- **Splitting content across files**: See `references/progressive-disclosure-patterns.md`

#### Implementation Order

1. Build `scripts/`, `references/`, `templates/`, `examples/` identified in Step 3
2. Test scripts to ensure correctness
3. Delete unused example files from initialization
4. Write SKILL.md frontmatter (`name` + `description` — the trigger mechanism)
   - `description` must cover both **WHAT** (capability) and **WHEN** (trigger scenarios):
     - Good: `"PDF form filling and field extraction. Use for: filling fillable PDFs, reading form field values, batch processing PDF forms."`
     - Bad: `"Helps with PDF stuff."`
5. Write SKILL.md body following the pattern-specific section order above

Use imperative/infinitive form in instructions.

### Step 6: Validate and Deliver

Run the validation script:

```bash
python scripts/quick_validate.py <path-to-skill>
```

Run the security scan (heuristic; confirm hits in context):

```bash
python scripts/security_scan.py <path-to-skill>
```

Fix any errors and re-validate. For skills **authored in chat**, if the scan or manual review finds issues, **edit the skill** to remove or neutralize risk, then re-run both commands until acceptable. For **imported** skills, the user should already have confirmed in Step 0; if new issues appear only after edits, apply the same confirmation rule.

Then check these quality criteria that the script cannot verify:

- [ ] SKILL.md body < 500 lines
- [ ] `description` contains keywords a user would naturally say (trigger accuracy)
- [ ] Terminology is consistent across SKILL.md and reference files
- [ ] All file references from SKILL.md are one level deep (no nested refs)
- [ ] No tool/library choices left ambiguous — give a default, add escape hatch only for exceptions

**Pattern-specific checks:**

- [ ] **Pattern A**: Each sub-task type has a dedicated example file; SKILL.md does NOT contain sub-task details
- [ ] **Pattern A**: Out-of-scope handling is defined (ask for clarification or reject)
- [ ] **Pattern B**: Every branch condition is explicit (no implicit "else do the same thing")
- [ ] **Pattern B**: Validation/QA step exists at the end of the workflow
- [ ] **Pattern B**: Domain rules live in references/, not inlined in SKILL.md
- [ ] **Pattern C**: Non-trigger conditions are defined (not just trigger conditions)
- [ ] **Pattern C**: Confirmation gates exist for destructive/irreversible operations
- [ ] **Pattern C**: Stop conditions define hard limits that cannot be overridden
- [ ] **Pattern C**: Risk levels have corresponding actions (not just definitions)

**Delivery package and chat prompt (required):**

- Deliver the finished skill as **one `.zip` archive** (the skill package), not only as a loose folder or file listing, whenever the environment supports offering a downloadable or attachable zip.
- **One identifier everywhere** — the string must match SKILL.md frontmatter `name`, the workspace folder from `init_skill.py`, the zip file name, the download filename users get, and the **single top-level directory inside the zip** (all the same hyphen-case value, e.g. `meal-planner`):
  - Zip file on disk / in the attachment: `{name}.zip`
  - Download / save-as filename: `{name}.zip` (do not use generic names like `skill.zip`, `archive.zip`, or timestamps unless the user asked)
  - Zip contents layout: `{name}/SKILL.md` plus bundled subfolders under `{name}/` — extracting `{name}.zip` must yield a folder named exactly `{name}`, not a different root folder name, not duplicate nesting like `{name}/{name}/`, and not a flat zip with files at the archive root.
- In the **same assistant message** that presents the completed skill (zip / card / attachment), include this sentence for the user **verbatim** (English): `Click the card below to try your skill in chat.`

Then deliver the final skill files to the user (as the zip above when applicable). For **authored-in-chat** work, the delivered artifact must be the **post-remediation** version (no known HIGH/EXTREME issues left unaddressed).

### Step 7: Iterate

1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Update SKILL.md or bundled resources
4. Test again
