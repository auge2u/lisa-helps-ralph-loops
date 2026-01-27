---
description: Full rescue pipeline (research + discover + plan + structure). For abandoned projects needing context reconstruction.
skill: research,discover,plan,structure
agent: archaeologist,migrator
workflow: rescue
---

# Rescue - Lisa

Execute the full rescue pipeline for abandoned or lost projects.

## When to Use

Use this command when:
- Project has been abandoned for 6+ months
- Original developers are unavailable
- Documentation is severely outdated
- "Why was this built?" is unclear
- Need complete context reconstruction before migration

## Pipeline Stages

| Stage | Command | Purpose | Output |
|-------|---------|---------|--------|
| 0 | research | Reconstruct lost context | `.gt/research/` |
| 1 | discover | Extract current facts | `.gt/memory/` |
| 2 | plan | Generate roadmap | `scopecraft/` |
| 3 | structure | Create work items | `.gt/beads/`, `.gt/convoys/` |

## What This Does

### Stage 0: Research (Unique to Rescue)
- Performs git archaeology on commit history
- Reconstructs project timeline
- Infers original mission from early commits
- Analyzes scope drift from original vision
- Provides rescue recommendation (revive/archive/pivot)

### Stages 1-3: Same as `/lisa:migrate`
Only proceeds if Stage 0 recommends "revive" or "pivot"

## Execution

Runs all four stages sequentially:

1. `skills/research/SKILL.md` -> `.gt/research/`
2. `skills/discover/SKILL.md` -> `.gt/memory/`
3. `skills/plan/SKILL.md` -> `scopecraft/`
4. `skills/structure/SKILL.md` -> `.gt/beads/`, `.gt/convoys/`

## Decision Point After Research

After Stage 0 completes, the rescue recommendation determines next steps:

| Recommendation | Action |
|----------------|--------|
| **revive** | Continue with stages 1-3 |
| **pivot** | Continue with stages 1-3 (adjusted scope) |
| **archive** | Stop - project should be archived |

## Output Structure

```
project/
├── .gt/
│   ├── research/              # Stage 0 output (rescue only)
│   │   ├── timeline.json
│   │   └── rescue.json
│   ├── memory/
│   │   └── semantic.json
│   ├── beads/
│   │   └── gt-*.json
│   └── convoys/
│       └── convoy-*.json
└── scopecraft/
    └── *.md (6 files)
```

## Quality Gates

All gates from stages 0-3 must pass:
- Research has timeline and recommendation
- Semantic memory valid with project name
- Roadmap has 3-5 phases
- At least 1 bead and convoy created

## Example

```bash
/lisa:rescue
```

## Validation

After rescue, validate all stages:

```bash
python plugins/lisa/hooks/validate.py --workflow rescue
```

## When to Use `/lisa:migrate` Instead

Use `/lisa:migrate` (without research) when:
- Project is actively maintained
- Original team is available
- Documentation is reasonably current
- Context is not lost
