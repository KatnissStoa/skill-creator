# Execution mode (`metadata.execution_mode`)

Skills declare **where** they should run by setting `metadata.execution_mode` in `SKILL.md` frontmatter. Allowed values: **`inherit`**, **`fork`**, **`sandbox`**.

This is **orthogonal** to design patterns (A/B/C): pattern describes **structure**; execution mode describes **runtime isolation and routing**.

## Product rule: skill authoring (`skill-creator`)

Skills whose **primary purpose** is to **create, scaffold, merge, vet, or validate** skill packages for end users MUST set **`metadata.execution_mode: sandbox`**. That includes the **skill-creator** skill (this repository’s authoring package).

**Rationale:** Skill authoring entails writing **generated trees and files** under a workspace, running **local tooling** (`init_skill.py`, `quick_validate.py`, `security_scan.py`), handling **imported** zips or remote repos/URLs, and often delivering a **.zip** artifact. These are **execution and data-plane** operations (Step 1). They MUST run in a **sandbox** runtime—**`fork` is not sufficient** for this product requirement, even though a forked session also isolates tokens.

Individual skills that are **not** meta-authoring tools still follow Step 1–3 below; this rule **does not** force every Pattern B skill to `sandbox`, only skills whose job is **authoring or adopting** skill packages.

## What each mode means (ADK semantics)

| Mode | Meaning |
|------|---------|
| **`inherit`** | **Default.** After the skill loads, work continues in the **parent** agent’s normal skill flow. The parent’s **context, history, model, and mounted tools** are shared. No separate sub-agent session. |
| **`fork`** | A **short-lived sub-agent** runs in a **new session** (e.g. via a fork handler / `SubAgentRunner`). Only the **final result** is returned to the parent. The sub-session **does not** carry the parent’s full history; it typically receives the skill content plus the **latest user task**. **Independent** tool allow/deny lists, model override, timeouts, and `max_turns` are possible. Skill text is **not** treated like trusted system policy: it is delivered as **task-side** content (e.g. `task_prompt` / first user message) while **system** comes from **trusted** agent configuration—this reduces **prompt injection** surface relative to in-place execution. Main benefit: **token isolation** (avoid polluting the parent context) and **policy isolation** for tools/model. **`fork` is not an OS/container sandbox.** |
| **`sandbox`** | **Heavy isolation** (e.g. SandboxAgent / sandbox runtime): appropriate for **shell execution**, **dependency installs**, **broad filesystem access**, **untrusted inputs**, and **artifacts** (files produced on disk). Use when the checklist below says sandbox—**do not** substitute `fork` for execution safety. |

**Precedence:** If **any** sandbox criterion applies → use **`sandbox`** (it overrides inherit/fork). Among the remainder, choose **`fork`** only when a **fork motivation** applies; otherwise prefer **`inherit`**.

---

## Step 1 — Route to `sandbox` (execution and data plane)

If **any** of the following is true, set **`metadata.execution_mode: sandbox`**:

| # | Criterion |
|---|-----------|
| 1 | The skill’s `SKILL.md` or bundled instructions imply **running** user-facing automation: **run**, **execute**, **bash**, **script**, shells, compilers, or similar. |
| 2 | The skill **reads or writes** the local filesystem beyond trivial, tightly scoped paths (or scope is unclear). |
| 3 | The skill **installs** extra dependencies (package managers, downloads of toolchains). |
| 4 | The skill processes **untrusted** content: arbitrary web pages, pasted URLs, or **user uploads** without a strict, safe subset. |
| 5 | The skill’s outputs are **artifacts** meant as files: CSV, PNG/PDF, generated code trees, zips, etc. |

These address **execution and data-plane** risk. **`fork` does not satisfy these** by itself.

---

## Step 2 — Otherwise, `fork` vs `inherit` (session and prompt plane)

If **no** sandbox criterion applies, use **`fork`** when **any** fork motivation applies:

| # | Fork motivation |
|---|------------------|
| F1 | **Token / context pollution:** multi-step workflow, large references, or repeated tool use would **bloat** the parent session—keep work in a **child session** and return a **compact** result. |
| F2 | **Prompt-injection posture:** skill body is **long**, **complex**, or from a **partially untrusted** source (e.g. user-editable or imported package)—prefer **task-side** delivery of skill text and **trusted** system configuration (**fork** semantics). |
| F3 | **Different tool or model policy:** this skill needs a **different** tool allow/deny list, **model**, **timeout**, or **`max_turns`** than the parent (**fork** supports independent configuration). |
| F4 | **Session boundary:** intermediate reasoning and tool traces should **not** persist in the parent’s long-term history—only the **aggregated outcome** should. |

If **none** of F1–F4 apply and the skill is **lightweight**, **trusted**, and fits **in-place** execution, use **`inherit`**.

### Typical `inherit` fits (all must hold: no sandbox, no fork need)

- Single-turn or short **Q&A**, summarization, translation.  
- **Simple API calls** with small, structured responses (e.g. weather lookup) **without** writing artifacts, **without** ingesting arbitrary untrusted files/URLs as primary input.  
- Classification / intent routing **without** heavy sub-session tool churn or independent tool policy.

**Important:** If a scenario *looks* like “simple Q&A” but involves **untrusted uploads/URLs** or **file artifacts**, **sandbox** (Step 1) wins—do not downgrade to `inherit`.

---

## Step 3 — Quick decision table

| Situation | Mode |
|-----------|------|
| **Skill authoring / `skill-creator`-class tools** (see [Product rule](#product-rule-skill-authoring-skill-creator)) | **`sandbox`** |
| Any Step 1 sandbox criterion | **`sandbox`** |
| No sandbox criterion + any F1–F4 | **`fork`** |
| No sandbox criterion + no F1–F4 | **`inherit`** |

---

## Authoring notes

- **Source of truth for routers:** `metadata.execution_mode`. Keep `description` focused on **WHAT / WHEN** to trigger; optionally add **one short line** about execution if it helps operators (stay within length limits; see `quick_validate.py`).  
- **Pattern hints (non-binding):** Meta-authoring skills (**skill-creator**): **`sandbox`** (product rule). Other skills: Pattern A often `inherit` or `fork`; Pattern B often `sandbox` or `fork` when scripts run; Pattern C often `fork` when boundaries and tools differ from the parent—**always** reconcile with the checklists above.  
- **YAML:** Nested `metadata` requires valid YAML; use PyYAML for `quick_validate.py` when frontmatter uses nested mappings.

---

## Example frontmatter (`sandbox`)

```yaml
---
name: example-data-pipeline
description: >-
  USE WHEN the user wants to transform CSV files, run local validation scripts,
  or produce downloadable reports. …
metadata:
  execution_mode: sandbox
---
```

Sandbox-specific download or mount instructions belong in the **SKILL.md body** (skill-specific URLs and steps), not in this reference file.
