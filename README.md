# lisa-helps-ralph-loops

**lisa-helps-ralph-loops** is a migration system that analyzes existing projects and structures them for [Gastown](https://github.com/steveyegge/gastown) — Steve Yegge's multi-agent workspace manager.

> **Status:** Early development. Core Gastown migration features are planned but not yet implemented. Currently includes inherited roadmap generation functionality from [ralph-it-up](https://github.com/auge2u/ralph-it-up).

## Vision

1. **Understands your project** — Scans codebase, docs, PRDs, architecture decisions
2. **Extracts work units** — Identifies tasks, TODOs, issues, technical debt
3. **Structures for Gastown** — Generates Rigs, Beads, and Convoys for multi-agent execution
4. **Preserves context** — Creates semantic memory so agents understand project history

## Current Status

### Available Now (Inherited from ralph-it-up)

These commands work today for roadmap generation:

```txt
/lisa-loops-memory:roadmap              # One-shot roadmap generation
/lisa-loops-memory:roadmap-native       # Native loop with quality gates
/lisa-loops-memory:roadmap-orchestrated # External orchestrator mode
```

**Output:** Generates 6 markdown files in `./scopecraft/`:
- `VISION_AND_STAGE_DEFINITION.md`
- `ROADMAP.md`
- `EPICS_AND_STORIES.md`
- `RISKS_AND_DEPENDENCIES.md`
- `METRICS_AND_PMF.md`
- `OPEN_QUESTIONS.md`

### Planned (Not Yet Implemented)

These Gastown migration commands are on the roadmap:

```txt
/lisa-loops-memory:analyze    # [PLANNED] Analyze project, generate memory
/lisa-loops-memory:migrate    # [PLANNED] Generate Gastown Rig structure
/lisa-loops-memory:beads      # [PLANNED] Extract work items as Beads
/lisa-loops-memory:convoy     # [PLANNED] Create Convoy from Beads
```

## Install (Claude Code)

```txt
/plugin marketplace add auge2u/lisa-helps-ralph-loops
/plugin install lisa-loops-memory@lisa-helps-ralph-loops
```

## Gastown Concepts

| Gastown Term | What It Is |
|--------------|------------|
| **Mayor** | Primary AI coordinator with full workspace context |
| **Town** | Root workspace directory (~/gt/) |
| **Rig** | Project container wrapping a git repo |
| **Polecat** | Ephemeral worker agent (spawn → work → disappear) |
| **Hook** | Git worktree for persistent state |
| **Convoy** | Work-tracking unit bundling multiple beads |
| **Bead** | Individual work item (issue) with alphanumeric ID |

## Target Architecture

When complete, lisa-helps-ralph will produce this structure:

```
project/
├── .gt/
│   ├── memory/
│   │   ├── semantic.json   # Permanent facts (tech stack, constraints)
│   │   ├── episodic.json   # Decisions with TTL (~30 days)
│   │   └── procedural.json # Learned patterns
│   ├── beads/
│   │   └── gt-*.json       # Individual work items
│   └── convoys/
│       └── convoy-*.json   # Bundled work assignments
└── [existing project files]
```

## Memory Architecture (Planned)

### Semantic Memory (Facts)
```json
{
  "project": { "name": "my-app", "type": "web-application" },
  "tech_stack": { "database": "Neon PostgreSQL", "auth": "Firebase Auth" },
  "constraints": ["Must support offline mode", "HIPAA compliance required"]
}
```

### Beads (Work Items)
```json
{
  "id": "gt-abc12",
  "title": "Add user authentication",
  "type": "feature",
  "complexity": "L",
  "acceptance_criteria": ["User can sign up with email", "Session persists"]
}
```

### Convoys (Work Bundles)
```json
{
  "id": "convoy-001",
  "name": "Authentication Sprint",
  "beads": ["gt-abc12", "gt-def34"],
  "status": "pending"
}
```

## Compatibility

| System | Role |
|--------|------|
| [Gastown](https://github.com/steveyegge/gastown) | Target platform (Mayor, Polecats) |
| [ralph-orchestrator](https://github.com/mikeyobrien/ralph-orchestrator) | Loop execution |
| [multi-agent-ralph-loop](https://github.com/alfredolopez80/multi-agent-ralph-loop) | Memory patterns inspiration |

## Roadmap

- [x] Fork from ralph-it-up v1.2.0
- [x] Define Gastown integration architecture
- [x] Create memory schema templates (.gt/memory/)
- [ ] **Implement project analyzer** (scan code, docs, PRDs)
- [ ] **Implement bead extraction** (tasks → beads)
- [ ] **Implement convoy generation** (bundle beads)
- [ ] **Implement .gt/ structure output**
- [ ] Integrate with Gastown Mayor API
- [ ] Add memory persistence across sessions

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Note that the core Gastown migration features are not yet implemented — contributions welcome!

## License

MIT
