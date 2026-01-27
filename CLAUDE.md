# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**lisa-helps-ralph-loops** is a migration system that analyzes existing projects and structures them for [Gastown](https://github.com/steveyegge/gastown) — Steve Yegge's multi-agent workspace manager.

> **Status:** Early development. Core Gastown migration features are planned but not yet implemented. Currently includes inherited roadmap generation functionality from [ralph-it-up](https://github.com/auge2u/ralph-it-up).

**Current version:** 0.1.0 (see `.claude-plugin/marketplace.json`)

## What's Implemented vs Planned

### Available Now (Inherited from ralph-it-up)

These commands work today:

| Command | Purpose |
|---------|---------|
| `/lisa-loops-memory:roadmap` | One-shot roadmap generation |
| `/lisa-loops-memory:roadmap-native` | Native Claude Code loop with quality gates |
| `/lisa-loops-memory:roadmap-orchestrated` | External orchestrator mode (ralph-orchestrator) |

**Outputs:** Generates 6 markdown files in `./scopecraft/`:
- `VISION_AND_STAGE_DEFINITION.md`
- `ROADMAP.md`
- `EPICS_AND_STORIES.md`
- `RISKS_AND_DEPENDENCIES.md`
- `METRICS_AND_PMF.md`
- `OPEN_QUESTIONS.md`

### Planned (Not Yet Implemented)

These Gastown migration features are on the roadmap:

| Command | Purpose | Status |
|---------|---------|--------|
| `/lisa-loops-memory:analyze` | Analyze project, generate memory | PLANNED |
| `/lisa-loops-memory:migrate` | Generate Gastown Rig structure | PLANNED |
| `/lisa-loops-memory:beads` | Extract work items as Beads | PLANNED |
| `/lisa-loops-memory:convoy` | Create Convoy from Beads | PLANNED |

## Repository Structure

```
.claude-plugin/marketplace.json    # Marketplace registry
plugins/
  lisa-loops-memory/
    .claude-plugin/plugin.json     # Plugin manifest
    commands/
      roadmap.md                   # One-shot roadmap (IMPLEMENTED)
      roadmap-native.md            # Native loop (IMPLEMENTED)
      roadmap-orchestrated.md      # Orchestrator mode (IMPLEMENTED)
    agents/
      product-owner.md             # Agent for roadmap (IMPLEMENTED)
      roadmap-orchestrator.md      # Loop orchestrator (IMPLEMENTED)
    skills/
      roadmap-scopecraft/          # Core roadmap skill (IMPLEMENTED)
        SKILL.md
        templates/
    hooks/
      validate_quality_gates.py    # Python validator (IMPLEMENTED)
      validate-gates-handler.sh    # Bash validator (IMPLEMENTED)
    templates/
      ralph.yml                    # ralph-orchestrator config
      scratchpad.md
    examples/
      scopecraft/                  # Sample outputs
.gt/
  memory/                          # Memory schema templates (DEFINED)
    semantic.json
    episodic.json
    procedural.json
  beads/                           # Placeholder (PLANNED)
  convoys/                         # Placeholder (PLANNED)
scripts/
  bump-version.sh                  # Version management
```

## Gastown Concepts

| Term | Description |
|------|-------------|
| **Mayor** | Primary AI coordinator with full workspace context |
| **Town** | Root workspace directory (~/gt/) containing all projects |
| **Rig** | Project container wrapping a git repository |
| **Polecat** | Ephemeral worker agent (spawn -> work -> disappear) |
| **Hook** | Git worktree for persistent state surviving restarts |
| **Convoy** | Work-tracking unit bundling multiple beads |
| **Bead** | Individual work item with alphanumeric ID (e.g., gt-abc12) |

## Target Architecture (Planned)

When Gastown migration features are implemented, projects will have:

```
project/
├── .gt/
│   ├── memory/
│   │   ├── semantic.json      # Permanent facts (tech stack, constraints)
│   │   ├── episodic.json      # Decisions with TTL (~30 days)
│   │   └── procedural.json    # Learned patterns
│   ├── beads/
│   │   └── gt-*.json          # Individual work items
│   └── convoys/
│       └── convoy-*.json      # Bundled work assignments
└── [existing project files]
```

## Quality Gates (Implemented)

For the roadmap commands, these gates must pass before `LOOP_COMPLETE`:

| Gate | Requirement |
|------|-------------|
| `all_outputs_exist` | 6 `.md` files in scopecraft/ |
| `phases_in_range` | 3-5 `## Phase \d` headers in ROADMAP.md |
| `stories_have_acceptance_criteria` | 5+ "Acceptance Criteria" sections |
| `risks_documented` | 3+ risk table rows |
| `metrics_defined` | "North Star Metric" section exists |
| `no_todo_placeholders` | Zero `[TODO]`/`[TBD]`/`[PLACEHOLDER]` markers |

### Validation

```bash
# Native bash validator (zero dependencies, recommended)
./plugins/lisa-loops-memory/hooks/validate-gates-handler.sh

# Python validator (more features)
python plugins/lisa-loops-memory/hooks/validate_quality_gates.py
```

Exit codes: `0`=pass, `1`=blocker failed, `2`=warning, `3`=security error

## Development Roadmap

- [x] Fork from ralph-it-up v1.2.0
- [x] Rename plugin to lisa-loops-memory
- [x] Define Gastown integration architecture
- [x] Create memory schema templates (.gt/memory/)
- [x] Add path security validation to hooks
- [ ] **Implement project analyzer** (scan code, docs, PRDs)
- [ ] **Implement bead extraction** (tasks -> beads)
- [ ] **Implement convoy generation** (bundle beads)
- [ ] **Implement .gt/ structure output**
- [ ] Integrate with Gastown Mayor API
- [ ] Add memory persistence across sessions
- [ ] Add test coverage

## Quality Standards

For future Gastown features:
- Beads must have acceptance criteria
- Beads must reference evidence (file paths)
- Memory must be valid JSON
- Convoys should have 3-7 beads (optimal batch size)
- Complexity estimates: S/M/L/XL

For current roadmap features:
- Commands must be deterministic and file-output driven
- Quality gates must pass before LOOP_COMPLETE
- Prefer outcomes/KRs over feature lists
- Roadmap phases limited to 3-5 max
- All outputs reference repo evidence where possible
