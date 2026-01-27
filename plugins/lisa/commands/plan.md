---
description: Generate a full scope roadmap (MVP/early release to next major stage) by scanning /docs, PRDs, and legacy tasks.
skill: plan
agent: migrator
stage: 2
---

# Plan (Stage 2) - Lisa

Execute the roadmap-scopecraft skill to generate a complete product roadmap.

## When to Use

Use this command when:
- Need to create a strategic roadmap from existing docs
- Converting legacy scope into a clean backlog
- Reconciling multiple PRDs into coherent plan
- Planning maturity progression (MVP -> next stage)

## What This Does

1. **Inventory documents** - Scans `/docs`, README, ADRs
2. **Extract scope sources** - TODOs, issues, backlog files
3. **Infer current stage** - MVP/alpha/beta/early release signals
4. **Generate roadmap** - Creates 6 scopecraft output files

## Execution

1. Follow the instructions in `skills/plan/SKILL.md`
2. Use templates from `skills/plan/templates/`
3. Output all files to `./scopecraft/`

## Output

Creates `./scopecraft/` with 6 files:
1. `VISION_AND_STAGE_DEFINITION.md` - Vision and completion criteria
2. `ROADMAP.md` - 3-5 phased roadmap
3. `EPICS_AND_STORIES.md` - Epics with stories and acceptance criteria
4. `RISKS_AND_DEPENDENCIES.md` - Risk register and dependency map
5. `METRICS_AND_PMF.md` - North star metric and PMF signals
6. `OPEN_QUESTIONS.md` - Questions blocking prioritization

## Quality Gates

- [ ] All 6 output files exist
- [ ] ROADMAP.md has 3-5 phases
- [ ] Stories have acceptance criteria (5+ sections)
- [ ] Risk register has 3+ entries
- [ ] North Star Metric is defined
- [ ] No `[TODO]`/`[TBD]`/`[PLACEHOLDER]` markers remain

## Style Constraints

- Be explicit, practical, and senior-engineer-friendly
- Optimize for outcomes (PMF) and delivery feasibility
- Keep roadmap to 3-5 phases max

## Example

```bash
/lisa:plan
```

After running, review `scopecraft/ROADMAP.md` for the phased plan.

## Migration Note

This command replaces the deprecated `/lisa:roadmap` command.
