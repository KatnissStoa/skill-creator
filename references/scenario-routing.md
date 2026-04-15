# Scenario Routing Guide

Use this guide to identify which design pattern fits the user's skill creation request. **Route first, build second.**

## Routing Decision Tree

Ask these questions in order:

**Q1: Is the core challenge knowing WHEN to act vs WHEN to refuse?**
→ Yes → **Pattern C** (Trigger Boundaries + Risk Control)
→ No → Continue

**Q2: Does the task involve repeatable computation, data processing, or multi-step pipelines?**
→ Yes → **Pattern B** (Scripts + References + Branch Logic + Validation)
→ No → Continue

**Q3: Is the task mainly about recognizing different sub-task types and applying different formats/templates?**
→ Yes → **Pattern A** (Concise SKILL.md + Examples Routing)
→ No → Re-examine; most skills fit one of these three. If truly novel, default to Pattern B.

## Scenario-to-Pattern Mapping

### Pattern A Scenarios

**Enterprise SOP / Chief of Staff**
- Trigger signals: weekly reports, meeting notes, project updates, management communications, action items
- Skill name example: `ops-chief-of-staff`
- Key requirement: SKILL.md as task classifier, examples/ for each document type
- Sub-tasks to route: weekly report, meeting minutes, project tracking summary, management communication draft

**Structured Document Production**
- Trigger signals: PRD, RFC, proposal, investment memo, project retrospective, formal document
- Skill name example: `structured-doc-writer`
- Key requirement: examples/ for each document type with audience, structure, evidence rules
- Sub-tasks to route: PRD, RFC, proposal, investment memo, retrospective

**Bounded Personal Workflow Assistant**
- Trigger signals: todo list, meeting prep, follow-up reminders, standard replies, archive management
- Skill name example: `bounded-workflow-assistant`
- Key requirement: hard limit of 3–5 task types, explicit rejection of out-of-scope requests
- Sub-tasks to route: weekly planning, meeting prep, follow-up tracking, standard replies, archive organization

### Pattern B Scenarios

**Industry / Sector Research**
- Trigger signals: industry analysis, competitive landscape, company research, market scan, comparison report
- Skill name example: `industry-research-analyst`
- Key requirement: research framework in references/, scripts for comparison tables and evidence gap tracking
- Branches: single company → company group comparison → sector scan → insufficient data

**File Processing / Format Conversion**
- Trigger signals: PDF, Excel, CSV, PPT, extract, clean, convert, transform, batch process
- Skill name example: `document-pipeline-processor`
- Key requirement: scripts for extraction/transformation/validation, references for field mapping rules
- Branches: parseable file → scanned/OCR file → corrupted file → missing fields

**Cooking / Nutrition Planning**
- Trigger signals: meal plan, grocery list, recipe, budget, dietary restrictions, nutrition, weekly menu
- Skill name example: `meal-planning-nutritionist`
- Key requirement: scripts for shopping list aggregation and nutrition estimation, references for dietary rules
- Branches: budget-first → nutrition-first → weight loss/muscle gain → vegetarian/gluten-free → pantry-first

**Stock / Crypto Analysis (Hybrid B+C)**
- Trigger signals: stock analysis, crypto analysis, dividend, trend, valuation, scoring model, comparison
- Skill name example: `market-analysis-engine`
- Key requirement: scripts for indicator calculation and comparison matrices, PLUS risk disclaimers from Pattern C
- Branches: stock vs crypto → single vs multi-asset → dividend vs trend → sufficient vs insufficient data

### Pattern C Scenarios

**API / Data Platform Integration**
- Trigger signals: API, endpoint, authentication, credentials, rate limit, SDK, query, data source
- Skill name example: `api-integration-operator`
- Key requirement: trigger/non-trigger/stop conditions BEFORE workflow steps, confirmation gates for writes
- Branches: read-only access → read-write access → authentication failure → rate limit hit

**Quality Review / Audit**
- Trigger signals: review, audit, quality check, compliance, approval, pass/fail, severity level
- Skill name example: `quality-reviewer`
- Key requirement: severity level system with corresponding actions (advise/block/reject)
- Branches: by material type (PRD, contract, deliverable) each with different review criteria

**Multi-Agent Orchestration**
- Trigger signals: multi-agent, delegation, role assignment, handoff, orchestration, parallel execution
- Skill name example: `multi-agent-orchestrator`
- Key requirement: role boundaries, escalation conditions, dependency enforcement, conflict resolution
- Branches: serial → parallel → review-loop → conflict resolution → fallback to single agent

**Wellness Coaching**
- Trigger signals: wellness, breathing, mood, stress, mental health, sleep, self-care, meditation
- Skill name example: `wellness-coach`
- Key requirement: strict non-trigger for medical/crisis situations, risk-level-based response routing
- Branches: immediate intervention (breathing) → ongoing tracking (mood log) → crisis → medical referral

## Keyword Detection Heuristic

When analyzing a user's skill creation request, scan for these keyword clusters to identify the pattern:

**Strong Pattern A signals** (2+ matches → Pattern A):
- "different types of", "several kinds of", "classify", "route", "template for each"
- "SOP", "workflow", "document production", "writing assistant"
- Emphasis on variety of outputs rather than complexity of process

**Strong Pattern B signals** (2+ matches → Pattern B):
- "script", "automate", "process", "pipeline", "batch"
- "analysis", "research", "framework", "scoring", "comparison"
- "validate", "check", "verify", "QA"
- Emphasis on repeatability and data processing

**Strong Pattern C signals** (2+ matches → Pattern C):
- "boundary", "limit", "refuse", "confirm", "approve"
- "risk", "safety", "audit", "compliance", "review"
- "API", "credentials", "authentication", "rate limit"
- "escalate", "stop", "crisis", "multi-agent"
- Emphasis on when NOT to do something

**Ambiguous cases:**
- If both B and C signals are strong → Hybrid B+C (Pattern B structure + Pattern C risk controls)
- If both A and B signals are strong → Check if the user needs categorization (A) or computation (B)
- If no clear signals → Ask the user: "Does this skill primarily need to (A) recognize and route different task types, (B) execute repeatable data/analysis processes, or (C) enforce boundaries and risk controls?"

## Post-Routing Checklist

After selecting a pattern, verify the routing is correct by checking:

- [ ] The pattern's "Structural Requirements" in design-patterns.md match what the user needs
- [ ] SKILL.md's intended role (dispatcher / process controller / boundary enforcer) fits the scenario
- [ ] The primary complexity source matches the pattern (variety → A, process → B, constraints → C)
- [ ] If hybrid, the primary pattern is clear and the secondary only adds specific requirements
