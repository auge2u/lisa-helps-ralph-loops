# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**lisa-helps-ralph-loops** is a migration system that analyzes existing projects and structures them for [Gastown](https://github.com/steveyegge/gastown) — Steve Yegge's multi-agent workspace manager.

**Current version:** 0.2.0 (see `.claude-plugin/marketplace.json`)

## Commands

### Gastown Migration Commands

| Command | Purpose |
|---------|---------|
| `/lisa-loops-memory:analyze` | Scan project, generate semantic memory |
| `/lisa-loops-memory:beads` | Extract work items as Beads |
| `/lisa-loops-memory:convoy` | Bundle Beads into Convoys |
| `/lisa-loops-memory:migrate` | Full migration (analyze + beads + convoy) |

### Roadmap Commands (inherited from ralph-it-up)

| Command | Purpose |
|---------|---------|
| `/lisa-loops-memory:roadmap` | One-shot roadmap generation |
| `/lisa-loops-memory:roadmap-native` | Native Claude Code loop with quality gates |
| `/lisa-loops-memory:roadmap-orchestrated` | External orchestrator mode (ralph-orchestrator) |

## Repository Structure

```
.claude-plugin/marketplace.json    # Marketplace registry
plugins/
  lisa-loops-memory/
    .claude-plugin/plugin.json     # Plugin manifest
    commands/
      analyze.md                   # Gastown: generate memory
      beads.md                     # Gastown: extract work items
      convoy.md                    # Gastown: bundle beads
      migrate.md                   # Gastown: full migration
      roadmap.md                   # Roadmap: one-shot
      roadmap-native.md            # Roadmap: native loop
      roadmap-orchestrated.md      # Roadmap: orchestrator mode
    agents/
      gastown-migrator.md          # Migration specialist agent
      product-owner.md             # Roadmap agent
      roadmap-orchestrator.md      # Loop orchestrator agent
    skills/
      gastown-migration/           # Gastown migration skill
        SKILL.md                   # Core logic, quality gates
        templates/                 # Bead, convoy JSON templates
      roadmap-scopecraft/          # Roadmap skill
        SKILL.md
        templates/
    hooks/
      validate_gastown.py          # Gastown migration validator
      validate_quality_gates.py    # Roadmap quality gates
      validate-gates-handler.sh    # Bash validator
    examples/
      gastown/                     # Sample Gastown outputs
      scopecraft/                  # Sample roadmap outputs
.gt/
  memory/                          # Memory schema templates
  beads/                           # Bead output directory
  convoys/                         # Convoy output directory
tests/
  test_validate_quality_gates.py   # Quality gate tests
```

## Gastown Concepts

| Term | Description |
|------|-------------|
| **Mayor** | Primary AI coordinator with full workspace context |
| **Town** | Root workspace directory (~/gt/) containing all projects |
| **Rig** | Project container wrapping a git repository |
| **Polecat** | Ephemeral worker agent (spawn → work → disappear) |
| **Hook** | Git worktree for persistent state surviving restarts |
| **Convoy** | Work-tracking unit bundling multiple beads |
| **Bead** | Individual work item with alphanumeric ID (e.g., gt-abc12) |

## Output Structure

After migration, projects have a `.gt/` directory:

```
project/
├── .gt/
│   ├── memory/
│   │   ├── semantic.json      # Permanent facts (tech stack, constraints)
│   │   ├── episodic.json      # Decisions with TTL (~30 days)
│   │   └── procedural.json    # Learned patterns
│   ├── beads/
│   │   ├── gt-abc12.json      # Individual work items
│   │   └── ...
│   └── convoys/
│       └── convoy-001.json    # Bundled work assignments
└── [existing project files]
```

## Quality Gates

### Gastown Migration Gates

| Gate | Requirement |
|------|-------------|
| `semantic_valid_json` | semantic.json is valid JSON |
| `project_identified` | project.name is populated |
| `tech_stack_detected` | At least 2 tech_stack fields |
| `beads_extracted` | At least 1 bead created |
| `beads_have_criteria` | All beads have acceptance criteria |
| `convoy_created` | At least 1 convoy created |
| `convoy_size_valid` | Convoys have 3-7 beads |

### Roadmap Quality Gates

| Gate | Requirement |
|------|-------------|
| `all_outputs_exist` | 6 `.md` files in scopecraft/ |
| `phases_in_range` | 3-5 phases in ROADMAP.md |
| `stories_have_acceptance_criteria` | 5+ acceptance criteria sections |
| `risks_documented` | 3+ risk table rows |
| `metrics_defined` | North Star Metric section exists |
| `no_todo_placeholders` | Zero `[TODO]`/`[TBD]`/`[PLACEHOLDER]` markers |

## Validation

```bash
# Gastown migration validation
python plugins/lisa-loops-memory/hooks/validate_gastown.py
python plugins/lisa-loops-memory/hooks/validate_gastown.py --phase analyze

# Roadmap validation
./plugins/lisa-loops-memory/hooks/validate-gates-handler.sh
python plugins/lisa-loops-memory/hooks/validate_quality_gates.py
```

Exit codes: `0`=pass, `1`=blocker failed, `2`=warning, `3`=security error

## Running Tests

```bash
pytest tests/ -v
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

## Development Roadmap

- [x] Fork from ralph-it-up v1.2.0
- [x] Rename plugin to lisa-loops-memory
- [x] Define Gastown integration architecture
- [x] Create memory schema templates (.gt/memory/)
- [x] Add path security validation to hooks
- [x] Add test coverage for quality gates
- [x] Implement analyze command (project scanning)
- [x] Implement beads command (work item extraction)
- [x] Implement convoy command (bead bundling)
- [x] Implement migrate command (full migration)
- [x] Add Gastown migration validator
- [ ] Integrate with Gastown Mayor API
- [ ] Add memory persistence across sessions
