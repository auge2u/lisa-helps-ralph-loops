# lisa-helps-ralph-loops

**lisa-helps-ralph-loops** is a migration system that analyzes existing projects and structures them for [Gastown](https://github.com/steveyegge/gastown) — Steve Yegge's multi-agent workspace manager.

## What It Does

1. **Understands your project** — Scans codebase, docs, PRDs, architecture decisions
2. **Extracts work units** — Identifies tasks, TODOs, issues, technical debt
3. **Structures for Gastown** — Generates Rigs, Beads, and Convoys for multi-agent execution
4. **Preserves context** — Creates semantic memory so agents understand project history

## Why?

Gastown coordinates 20-30 Claude Code agents working simultaneously. But agents need:
- **Project context** — What is this? What tech stack? What constraints?
- **Work breakdown** — Clear beads (issues) organized into convoys
- **Persistent memory** — Facts that survive agent restarts

**lisa-helps-ralph-loops** bridges the gap between messy existing projects and Gastown's structured multi-agent workflow.

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

## Install (Claude Code)

```txt
/plugin marketplace add auge2u/lisa-helps-ralph-loops
/plugin install lisa-loops-memory@lisa-helps-ralph-loops
```

## Commands

```txt
/lisa-loops-memory:analyze              # Analyze project, generate memory
/lisa-loops-memory:migrate              # Generate Gastown Rig structure
/lisa-loops-memory:beads                # Extract work items as Beads
/lisa-loops-memory:convoy               # Create Convoy from Beads
```

## Migration Workflow

```
┌─────────────────────┐
│   Existing Project  │
│   (messy repo)      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  lisa-helps-ralph   │
│  ┌───────────────┐  │
│  │ 1. Analyze    │  │  ← Scan code, docs, PRDs
│  │ 2. Extract    │  │  ← Find tasks, debt, issues
│  │ 3. Structure  │  │  ← Create memory + beads
│  └───────────────┘  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Gastown Rig       │
│   ├── .gt/          │
│   │   ├── memory/   │  ← Semantic facts
│   │   ├── beads/    │  ← Work items
│   │   └── convoys/  │  ← Work bundles
│   └── [project]     │
└─────────────────────┘
           │
           ▼
┌─────────────────────┐
│   Mayor assigns     │
│   Polecats execute  │
│   Hooks persist     │
└─────────────────────┘
```

## Memory Architecture

lisa-helps-ralph creates memory that Gastown agents can consume:

```
.gt/memory/
├── semantic.json      # Permanent facts (tech stack, constraints, personas)
├── episodic.json      # Decisions and rationale (TTL ~30 days)
└── procedural.json    # Learned patterns (complexity estimates, risk factors)
```

### Semantic Memory (Facts)

```json
{
  "project": {
    "name": "my-app",
    "type": "web-application",
    "primary_language": "TypeScript"
  },
  "tech_stack": {
    "database": "Neon PostgreSQL",
    "auth": "Firebase Auth",
    "deployment": "Cloudflare Workers"
  },
  "constraints": [
    "Must support offline mode",
    "HIPAA compliance required"
  ]
}
```

### Beads (Work Items)

```json
{
  "id": "gt-abc12",
  "title": "Add user authentication",
  "type": "feature",
  "complexity": "L",
  "dependencies": ["gt-xyz99"],
  "acceptance_criteria": [
    "User can sign up with email",
    "User can sign in with Google OAuth",
    "Session persists across browser restart"
  ]
}
```

### Convoys (Work Bundles)

```json
{
  "id": "convoy-001",
  "name": "Authentication Sprint",
  "beads": ["gt-abc12", "gt-def34", "gt-ghi56"],
  "assigned_to": null,
  "status": "pending"
}
```

## Outputs

After migration, your project has:

```
project/
├── .gt/
│   ├── memory/
│   │   ├── semantic.json
│   │   ├── episodic.json
│   │   └── procedural.json
│   ├── beads/
│   │   ├── gt-abc12.json
│   │   ├── gt-def34.json
│   │   └── ...
│   └── convoys/
│       └── convoy-001.json
└── [existing project files]
```

## Compatibility

| System | Role |
|--------|------|
| [Gastown](https://github.com/steveyegge/gastown) | Target platform (Mayor, Polecats) |
| [ralph-orchestrator](https://github.com/mikeyobrien/ralph-orchestrator) | Loop execution |
| [multi-agent-ralph-loop](https://github.com/alfredolopez80/multi-agent-ralph-loop) | Memory patterns |

## Roadmap

- [x] Fork from ralph-it-up v1.2.0
- [ ] Implement project analyzer (code, docs, PRDs)
- [ ] Implement bead extraction (tasks → beads)
- [ ] Implement convoy generation
- [ ] Implement Gastown .gt/ structure output
- [ ] Integrate with Gastown Mayor API

## License

MIT
