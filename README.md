# lisa-helps-ralph-loops

**lisa-helps-ralph-loops** is a migration system that analyzes existing projects and structures them for [Gastown](https://github.com/steveyegge/gastown) — Steve Yegge's multi-agent workspace manager.

## What It Does

1. **Understands your project** — Scans codebase, docs, PRDs, architecture decisions
2. **Extracts work units** — Identifies tasks, TODOs, issues, technical debt as Beads
3. **Structures for Gastown** — Generates `.gt/` directory with memory, beads, convoys
4. **Preserves context** — Creates semantic memory so agents understand project history

## Commands

### Gastown Migration

```txt
/lisa-loops-memory:analyze    # Scan project, generate semantic memory
/lisa-loops-memory:beads      # Extract work items as Beads
/lisa-loops-memory:convoy     # Bundle Beads into Convoys
/lisa-loops-memory:migrate    # Full migration (analyze + beads + convoy)
```

### Roadmap Generation (inherited from ralph-it-up)

```txt
/lisa-loops-memory:roadmap              # One-shot roadmap generation
/lisa-loops-memory:roadmap-native       # Native loop with quality gates
/lisa-loops-memory:roadmap-orchestrated # External orchestrator mode
```

## Install (Claude Code)

```txt
/plugin marketplace add auge2u/lisa-helps-ralph-loops
/plugin install lisa-loops-memory@lisa-helps-ralph-loops
```

## Quick Start

```bash
# Full migration in one command
/lisa-loops-memory:migrate

# Or run phases individually
/lisa-loops-memory:analyze  # Creates .gt/memory/semantic.json
/lisa-loops-memory:beads    # Creates .gt/beads/*.json
/lisa-loops-memory:convoy   # Creates .gt/convoys/*.json
```

## Output Structure

```
project/
├── .gt/
│   ├── memory/
│   │   ├── semantic.json   # Project facts (tech stack, constraints)
│   │   ├── episodic.json   # Decisions with TTL (~30 days)
│   │   └── procedural.json # Learned patterns
│   ├── beads/
│   │   └── gt-*.json       # Individual work items
│   └── convoys/
│       └── convoy-*.json   # Bundled work assignments
└── [existing project files]
```

## Gastown Concepts

| Term | Description |
|------|-------------|
| **Mayor** | Primary AI coordinator with full workspace context |
| **Town** | Root workspace directory (~/gt/) |
| **Rig** | Project container wrapping a git repo |
| **Polecat** | Ephemeral worker agent (spawn → work → disappear) |
| **Hook** | Git worktree for persistent state |
| **Convoy** | Work-tracking unit bundling multiple beads |
| **Bead** | Individual work item with alphanumeric ID (gt-xxxxx) |

## Bead Schema

```json
{
  "id": "gt-abc12",
  "title": "Add user authentication",
  "type": "feature",
  "complexity": "L",
  "priority": "high",
  "acceptance_criteria": [
    "User can sign up with email",
    "Session persists across refresh"
  ],
  "evidence": {
    "source": "docs/PRD.md",
    "line": 42
  }
}
```

## Convoy Schema

```json
{
  "id": "convoy-001",
  "name": "Authentication Sprint",
  "beads": ["gt-abc12", "gt-def34", "gt-ghi56"],
  "status": "pending"
}
```

## Validation

```bash
# Validate full migration
python plugins/lisa-loops-memory/hooks/validate_gastown.py

# Validate specific phase
python plugins/lisa-loops-memory/hooks/validate_gastown.py --phase analyze
python plugins/lisa-loops-memory/hooks/validate_gastown.py --phase beads
python plugins/lisa-loops-memory/hooks/validate_gastown.py --phase convoy
```

## Compatibility

| System | Role |
|--------|------|
| [Gastown](https://github.com/steveyegge/gastown) | Target platform (Mayor, Polecats) |
| [ralph-orchestrator](https://github.com/mikeyobrien/ralph-orchestrator) | Loop execution for roadmap commands |

## Roadmap

- [x] Fork from ralph-it-up v1.2.0
- [x] Define Gastown integration architecture
- [x] Create memory schema templates (.gt/memory/)
- [x] Implement project analyzer (analyze command)
- [x] Implement bead extraction (beads command)
- [x] Implement convoy generation (convoy command)
- [x] Implement full migration (migrate command)
- [x] Add Gastown validation hooks
- [ ] Integrate with Gastown Mayor API
- [ ] Add memory persistence across sessions

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT
