---
name: plan
description: Builds a full-scope product roadmap for an existing project by scanning PRDs in /docs, extracting legacy tasks, and creating a comprehensive plan to move from MVP/early release to the next major stage.
stage: 2
---

# Plan Skill (Stage 2)

You are acting as a **product owner** partnering with **senior engineers** and a **PMF-focused team**.

## When to Use

Use this skill when the user asks for:
- Roadmap planning from an existing repo
- Converting legacy scope or pending tasks into a clean backlog
- PRD review / reconciliation across multiple documents
- Maturity planning (MVP -> next major stage)

## Output Structure

```
project/
└── scopecraft/
    ├── VISION_AND_STAGE_DEFINITION.md
    ├── ROADMAP.md
    ├── EPICS_AND_STORIES.md
    ├── RISKS_AND_DEPENDENCIES.md
    ├── METRICS_AND_PMF.md
    └── OPEN_QUESTIONS.md
```

## Ground Rules

- Prefer evidence from the repo: `/docs`, `README`, ADRs, architecture docs, backlog/task files
- If PRDs conflict, reconcile by:
  1. Newest decision wins (when clearly dated/versioned)
  2. Note divergence explicitly
  3. Propose a decision and list stakeholders needed
- Produce outputs as files under `./scopecraft/` for easy sharing
- No `[TODO]`, `[TBD]`, or `[PLACEHOLDER]` markers in final output

## Discovery Procedure (Do This First)

### 1. Inventory Documents

- List PRDs and PRD-like docs in `/docs` (initial + historical)
- Identify architecture decisions (ADRs), constraints, and non-goals

### 2. Inventory Scope Sources

- Open issues / TODOs / backlog lists / "legacy scope" notes
- Check `.gt/memory/semantic.json` if Stage 1 completed

### 3. Infer Current Stage

Look for MVP/alpha/beta/early release signals:
- Missing monitoring
- Limited permissions model
- Minimal onboarding
- Weak reliability
- No error tracking

## Convert Legacy Scope into Backlog Model

Normalize every task into:

| Field | Description |
|-------|-------------|
| Epic | High-level feature area |
| User Story | Who/what/why format |
| Acceptance Criteria | Observable, testable |
| Dependencies | Tech + org |
| Risk Level | Low/medium/high |
| Complexity | S/M/L/XL |

## Required Outputs

### 1. VISION_AND_STAGE_DEFINITION.md

Use template: `templates/VISION_FORMAT.md`

Contents:
- Product vision summary (customer + problem + value)
- "Next major stage" definition with completion criteria
- Assumptions + constraints

### 2. ROADMAP.md

Use template: `templates/ROADMAP_FORMAT.md`

Contents (3-5 phases max):
- For each phase:
  - Objective (outcome)
  - Key deliverables
  - Definition of done
  - Metrics / KPIs
  - Major risks

### 3. EPICS_AND_STORIES.md

Use template: `templates/EPICS_FORMAT.md`

Group epics by themes:
- Core value delivery
- Adoption/onboarding
- Reliability/performance
- Security/compliance
- Developer experience / platform maturity
- Monetization/packaging (if applicable)

Each epic must include:
- User-facing intent
- Stories with acceptance criteria
- Dependencies and sequencing notes

### 4. RISKS_AND_DEPENDENCIES.md

Use template: `templates/RISK_REGISTER_FORMAT.md`

Contents:
- Technical risks, product risks, GTM risks
- Mitigations and contingency paths
- Dependency map (internal + external)

### 5. METRICS_AND_PMF.md

Use template: `templates/METRICS_FORMAT.md`

Contents:
- North Star metric + supporting metrics
- PMF signals: activation funnel, retention, usage depth
- Instrumentation plan (what must be tracked to call stage "done")

### 6. OPEN_QUESTIONS.md

Use template: `templates/OPEN_QUESTIONS_FORMAT.md`

Contents:
- Questions blocking prioritization or delivery
- Proposed experiments or stakeholder asks to resolve them

## Quality Gates

| Gate | Requirement |
|------|-------------|
| `outputs_exist` | All 6 files in scopecraft/ |
| `phases_valid` | ROADMAP.md has 3-5 `## Phase` headers |
| `stories_have_criteria` | 5+ "Acceptance Criteria" sections in EPICS |
| `risks_documented` | 3+ risk table rows with Technical/Product/GTM |
| `north_star_defined` | "North Star Metric" section exists |
| `no_placeholders` | Zero `[TODO]`/`[TBD]`/`[PLACEHOLDER]` markers |

### Self-Validation Checklist

Before completing, verify:

```
[ ] scopecraft/ has exactly 6 .md files
[ ] ROADMAP.md has 3-5 "## Phase N" sections
[ ] EPICS_AND_STORIES.md has 5+ "#### Story" sections
[ ] Each story has "Acceptance Criteria:" section
[ ] RISKS_AND_DEPENDENCIES.md has 3+ table rows with risk types
[ ] METRICS_AND_PMF.md has "North Star Metric" section
[ ] No [TODO], [TBD], or [PLACEHOLDER] markers anywhere
```

## Validation

```bash
python plugins/lisa/hooks/validate.py --stage plan
```

## Style Constraints

- Be explicit, practical, and senior-engineer-friendly
- Optimize for outcomes (PMF) and delivery feasibility
- Keep roadmap to 3-5 phases max
- Every story needs acceptance criteria

## Next Steps

After plan completes:
- Proceed to Stage 3 (Structure) → `skills/structure/SKILL.md`
- Stage 3 will extract beads from the roadmap you generated
