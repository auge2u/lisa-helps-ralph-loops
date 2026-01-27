# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**lisa-helps-ralph-loops** is a migration system that analyzes existing projects and structures them for [Gastown](https://github.com/steveyegge/gastown) — Steve Yegge's multi-agent workspace manager.

**Current version:** 0.1.0 (see `.claude-plugin/marketplace.json`)

**Target platform:** [Gastown](https://github.com/steveyegge/gastown) multi-agent workspace

## What This Does

1. **Analyzes existing projects** — Scans codebase, docs, PRDs, architecture decisions
2. **Extracts work units** — Identifies tasks, TODOs, issues, technical debt as Beads
3. **Structures for Gastown** — Generates `.gt/` directory with memory, beads, convoys
4. **Preserves context** — Creates semantic memory so Gastown agents understand project history

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

## Repository Structure

```
.claude-plugin/marketplace.json    # Marketplace registry
plugins/
  lisa-loops-memory/
    .claude-plugin/plugin.json     # Plugin manifest
    commands/
      analyze.md                   # Analyze project, generate memory
      migrate.md                   # Generate Gastown Rig structure
      beads.md                     # Extract work items as Beads
      convoy.md                    # Create Convoy from Beads
    agents/
      project-analyzer.md          # Understands existing projects
      bead-extractor.md            # Extracts work items
      gastown-migrator.md          # Structures for Gastown
    skills/
      project-analysis/            # Core analysis logic
      bead-extraction/             # Work item extraction
      gastown-migration/           # Gastown structure generation
    templates/
      bead.json                    # Bead template
      convoy.json                  # Convoy template
      memory/                      # Memory templates
```

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
│   │   ├── gt-def34.json
│   │   └── ...
│   └── convoys/
│       └── convoy-001.json    # Bundled work assignments
└── [existing project files]
```

## Memory Architecture

### Semantic Memory (Facts)

Permanent knowledge about the project:
- Project identity (name, type, language)
- Tech stack (database, auth, deployment)
- Constraints and non-goals
- User personas

### Episodic Memory (Decisions)

Decisions with timestamps and expiry:
- What was decided
- Why (rationale)
- Context (who, when)
- Expiry (~30 days default)

### Procedural Memory (Patterns)

Learned heuristics:
- Complexity patterns
- Risk factors
- Success/failure patterns

## Bead Structure

```json
{
  "id": "gt-abc12",
  "title": "Add user authentication",
  "type": "feature",
  "complexity": "L",
  "priority": "high",
  "dependencies": ["gt-xyz99"],
  "acceptance_criteria": [
    "User can sign up with email",
    "User can sign in with Google OAuth"
  ],
  "evidence": {
    "source": "docs/PRD-auth.md",
    "line": 42
  }
}
```

## Convoy Structure

```json
{
  "id": "convoy-001",
  "name": "Authentication Sprint",
  "description": "Implement core auth features",
  "beads": ["gt-abc12", "gt-def34", "gt-ghi56"],
  "assigned_to": null,
  "status": "pending",
  "created": "2026-01-27T10:00:00Z"
}
```

## Commands

| Command | Purpose |
|---------|---------|
| `/lisa-loops-memory:analyze` | Analyze project, generate memory |
| `/lisa-loops-memory:migrate` | Generate Gastown `.gt/` structure |
| `/lisa-loops-memory:beads` | Extract work items as Beads |
| `/lisa-loops-memory:convoy` | Create Convoy from Beads |

## Migration Workflow

1. **Analyze** — Scan `/docs`, README, code for project understanding
2. **Extract Memory** — Create semantic facts, capture decisions
3. **Extract Beads** — Convert TODOs, issues, PRD items to Beads
4. **Create Convoys** — Bundle related Beads into work assignments
5. **Output `.gt/`** — Write Gastown-compatible structure

## Integration with Gastown

After migration, the Mayor can:
1. Read `.gt/memory/` for project context
2. Read `.gt/beads/` for available work items
3. Create/assign convoys to Polecats
4. Polecats read beads and execute in Hooks

## Quality Standards

- Beads must have acceptance criteria
- Beads must reference evidence (file paths)
- Memory must be valid JSON
- Convoys should have 3-7 beads (optimal batch size)
- Complexity estimates: S/M/L/XL

## Roadmap

- [x] Fork from ralph-it-up v1.2.0
- [x] Define Gastown integration architecture
- [ ] Implement project analyzer
- [ ] Implement bead extraction
- [ ] Implement convoy generation
- [ ] Implement `.gt/` structure output
- [ ] Test with Gastown Mayor
