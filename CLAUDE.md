# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**lisa-helps-ralph-loops** is a migration system that analyzes existing projects and structures them for [Gastown](https://github.com/steveyegge/gastown) — Steve Yegge's multi-agent workspace manager.

**Current version:** 0.3.0 (see `.claude-plugin/marketplace.json`)

## Commands (v0.3.0 - Lisa Plugin)

### Primary Commands

| Command | Stage | Purpose |
|---------|-------|---------|
| `/lisa:research` | 0 | Archaeological rescue for lost/abandoned projects |
| `/lisa:discover` | 1 | Extract semantic memory from project analysis |
| `/lisa:plan` | 2 | Generate roadmap with epics, risks, metrics |
| `/lisa:structure` | 3 | Create Beads and Convoys for Gastown |
| `/lisa:migrate` | 1-3 | Full pipeline (discover + plan + structure) |
| `/lisa:rescue` | 0-3 | Full rescue pipeline for abandoned projects |
| `/lisa:status` | — | Show progress and quality gate results |

### Deprecated Commands (will be removed in v0.4.0)

| Old Command | Replacement |
|-------------|-------------|
| `/lisa:analyze` | `/lisa:discover` |
| `/lisa:beads` | `/lisa:structure` |
| `/lisa:convoy` | `/lisa:structure` |
| `/lisa:roadmap` | `/lisa:plan` |
| `/lisa:roadmap-native` | `/lisa:plan` |
| `/lisa:roadmap-orchestrated` | `/lisa:plan` |

## Repository Structure

```
.claude-plugin/marketplace.json    # Marketplace registry
plugins/
  lisa/                            # v0.3.0 plugin (primary)
    .claude-plugin/plugin.json     # Plugin manifest
    gates.yaml                     # Quality gates configuration
    commands/
      research.md                  # Stage 0: Archaeological rescue
      discover.md                  # Stage 1: Semantic memory
      plan.md                      # Stage 2: Roadmap generation
      structure.md                 # Stage 3: Beads + Convoys
      migrate.md                   # Stages 1-3 pipeline
      rescue.md                    # Stages 0-3 pipeline
      status.md                    # Progress display
      _deprecated/                 # Deprecated commands
    agents/
      archaeologist.md             # Stage 0 specialist
      migrator.md                  # Stages 1-3 specialist
    skills/
      research/                    # Stage 0 skill
      discover/                    # Stage 1 skill
      plan/                        # Stage 2 skill
      structure/                   # Stage 3 skill
    hooks/
      validate.py                  # Unified validator
  lisa-loops-memory/               # v0.2.0 plugin (legacy)
    ...
tests/
  test_validate_quality_gates.py   # Quality gate tests
```

## Staged Architecture (v0.3.0)

| Stage | Command | Purpose | Output |
|-------|---------|---------|--------|
| 0 | `research` | Rescue lost context | `.gt/research/` |
| 1 | `discover` | Extract project facts | `.gt/memory/` |
| 2 | `plan` | Generate roadmap | `scopecraft/` |
| 3 | `structure` | Create work items | `.gt/beads/`, `.gt/convoys/` |

### Workflows

- **migrate** (Stages 1-3): For active projects with intact context
- **rescue** (Stages 0-3): For abandoned projects needing context reconstruction

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

## Output Structure

After migration, projects have a `.gt/` directory:

```
project/
├── .gt/
│   ├── research/              # Stage 0 output (rescue only)
│   │   ├── timeline.json
│   │   └── rescue.json
│   ├── memory/
│   │   ├── semantic.json      # Permanent facts (tech stack, constraints)
│   │   ├── episodic.json      # Decisions with TTL (~30 days)
│   │   └── procedural.json    # Learned patterns
│   ├── beads/
│   │   ├── gt-abc12.json      # Individual work items
│   │   └── ...
│   └── convoys/
│       └── convoy-001.json    # Bundled work assignments
├── scopecraft/                # Stage 2 output
│   ├── VISION_AND_STAGE_DEFINITION.md
│   ├── ROADMAP.md
│   ├── EPICS_AND_STORIES.md
│   ├── RISKS_AND_DEPENDENCIES.md
│   ├── METRICS_AND_PMF.md
│   └── OPEN_QUESTIONS.md
└── [existing project files]
```

## Quality Gates

### Stage 0: Research

| Gate | Requirement |
|------|-------------|
| `timeline_constructed` | timeline.json exists |
| `mission_clarified` | mission.statement populated |
| `drift_analyzed` | drift.factors has entries |
| `recommendation_made` | recommendation.action set |
| `evidence_gathered` | 3+ files analyzed |

### Stage 1: Discover

| Gate | Requirement |
|------|-------------|
| `semantic_valid` | semantic.json is valid JSON |
| `project_identified` | project.name is populated |
| `tech_stack_detected` | At least 2 tech_stack fields |
| `evidence_recorded` | At least 1 file analyzed |

### Stage 2: Plan

| Gate | Requirement |
|------|-------------|
| `outputs_exist` | 6 files in scopecraft/ |
| `phases_valid` | 3-5 phases in ROADMAP.md |
| `stories_have_criteria` | 5+ acceptance criteria sections |
| `risks_documented` | 3+ risk table rows |
| `north_star_defined` | North Star Metric section exists |
| `no_placeholders` | Zero `[TODO]`/`[TBD]`/`[PLACEHOLDER]` |

### Stage 3: Structure

| Gate | Requirement |
|------|-------------|
| `beads_extracted` | At least 1 bead created |
| `beads_have_criteria` | All beads have acceptance criteria |
| `beads_have_sources` | All beads have evidence |
| `beads_valid_ids` | IDs match `gt-[a-z0-9]{5}` |
| `convoy_created` | At least 1 convoy created |
| `convoy_size_valid` | Convoys have 3-7 beads |
| `convoy_beads_exist` | All referenced beads exist |

## Validation

Unified validator supporting all stages:

```bash
# Validate specific stage
python plugins/lisa/hooks/validate.py --stage discover
python plugins/lisa/hooks/validate.py --stage plan
python plugins/lisa/hooks/validate.py --stage structure

# Validate all stages
python plugins/lisa/hooks/validate.py --stage all

# Validate workflow
python plugins/lisa/hooks/validate.py --workflow migrate
python plugins/lisa/hooks/validate.py --workflow rescue

# Output formats
python plugins/lisa/hooks/validate.py --format json
python plugins/lisa/hooks/validate.py --format markdown
```

Exit codes: `0`=pass, `1`=blocker failed, `2`=warning, `3`=security error

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run single test file
pytest tests/test_validate_quality_gates.py -v

# Run specific test class or method
pytest tests/test_validate_quality_gates.py::TestPathSecurity -v
```

## Quality Standards

### Beads Must Have

- Clear, actionable title
- At least 1 acceptance criterion
- Evidence linking to source file
- Valid complexity estimate (XS/S/M/L/XL)
- Unique ID in `gt-xxxxx` format

### Convoys Must Have

- 3-7 beads (optimal batch size)
- Coherent theme (epic, skill, or dependency chain)
- All referenced beads exist

### Memory Must Have

- Valid JSON structure
- Non-null project.name
- At least 2 tech_stack fields populated
- Evidence with files_analyzed list

## Architecture Notes

### Staged Pipeline

The v0.3.0 architecture introduces a 4-stage pipeline:

1. **Research (Stage 0)**: Archaeological rescue for lost projects
   - Git archaeology, timeline reconstruction
   - Mission extraction, drift analysis
   - Rescue recommendation (revive/pivot/archive)

2. **Discover (Stage 1)**: Extract semantic memory
   - Tech stack detection from package files
   - Service detection from configs
   - Constraints and non-goals from docs

3. **Plan (Stage 2)**: Generate strategic roadmap
   - Vision and stage definition
   - Phased roadmap (3-5 phases)
   - Epics, risks, metrics

4. **Structure (Stage 3)**: Create Gastown work items
   - Extract beads from multiple sources
   - Bundle beads into convoys

### Plugin Architecture

- **Commands** (`commands/*.md`) — User-facing slash commands
- **Skills** (`skills/*/SKILL.md`) — Detailed procedures
- **Agents** (`agents/*.md`) — Specialized AI personas
- **Hooks** (`hooks/*.py`) — Python validators
- **Gates** (`gates.yaml`) — Quality gate definitions
