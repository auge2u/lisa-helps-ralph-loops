---
description: Full migration pipeline (discover + plan + structure). Transforms existing project into Gastown-compatible structure.
skill: discover,plan,structure
agent: migrator
workflow: migrate
---

# Migrate - Lisa

Execute the full migration pipeline to transform a project for Gastown.

## When to Use

Use this command when:
- Project context is intact (developers available, docs current)
- Want to run stages 1-3 in sequence
- Need complete Gastown migration in one command

## Pipeline Stages

| Stage | Command | Output |
|-------|---------|--------|
| 1 | discover | `.gt/memory/semantic.json` |
| 2 | plan | `scopecraft/*.md` (6 files) |
| 3 | structure | `.gt/beads/*.json`, `.gt/convoys/*.json` |

## What This Does

### Stage 1: Discover
- Scans package files for tech stack
- Reads configurations for service detection
- Analyzes documentation for constraints
- Outputs semantic memory

### Stage 2: Plan
- Inventories PRDs and scope sources
- Infers current maturity stage
- Generates phased roadmap
- Documents risks and metrics

### Stage 3: Structure
- Extracts work items from multiple sources
- Creates Gastown beads with acceptance criteria
- Bundles related beads into convoys

## Execution

Runs all three stages sequentially:

1. `skills/discover/SKILL.md` -> `.gt/memory/`
2. `skills/plan/SKILL.md` -> `scopecraft/`
3. `skills/structure/SKILL.md` -> `.gt/beads/`, `.gt/convoys/`

## Output Structure

```
project/
├── .gt/
│   ├── memory/
│   │   └── semantic.json      # Stage 1 output
│   ├── beads/
│   │   └── gt-*.json          # Stage 3 output
│   └── convoys/
│       └── convoy-*.json      # Stage 3 output
└── scopecraft/                # Stage 2 output
    ├── VISION_AND_STAGE_DEFINITION.md
    ├── ROADMAP.md
    ├── EPICS_AND_STORIES.md
    ├── RISKS_AND_DEPENDENCIES.md
    ├── METRICS_AND_PMF.md
    └── OPEN_QUESTIONS.md
```

## Quality Gates

All gates from stages 1-3 must pass:
- Semantic memory valid with project name and tech stack
- Roadmap has 3-5 phases with no placeholders
- At least 1 bead and 1 convoy created

## Example

```bash
/lisa:migrate
```

## Validation

After migration, validate all stages:

```bash
python plugins/lisa/hooks/validate.py --workflow migrate
```

## When to Use `/lisa:rescue` Instead

Use `/lisa:rescue` instead of `/lisa:migrate` when:
- Project has been abandoned 6+ months
- Original context is lost
- Need to reconstruct "why" before "what"
