# lisa-helps-ralph-loops

**lisa-helps-ralph-loops** extends the Ralph Loop pattern with **memory persistence** for multi-agent autonomous coding workflows.

Inspired by [multi-agent-ralph-loop](https://github.com/alfredolopez80/multi-agent-ralph-loop), this plugin adds:

- **Semantic memory** — Permanent facts about the project (persists forever)
- **Episodic memory** — Decisions and rationale (expires ~30 days)
- **Procedural memory** — Learned patterns and heuristics (evolves over time)

## Why Memory?

Standard Ralph Loops are stateless — each iteration starts fresh. This works for simple tasks but fails for complex, multi-session projects where:

- Context is lost between sessions
- Decisions are re-made without remembering prior rationale
- Patterns aren't learned from repeated observations

**lisa-helps-ralph-loops** makes iterations cumulative rather than stateless.

## Install (Claude Code)

```txt
/plugin marketplace add auge2u/lisa-helps-ralph-loops
/plugin install lisa-loops-memory@lisa-helps-ralph-loops
```

## Commands

```txt
/lisa-loops-memory:roadmap              # One-shot roadmap generation
/lisa-loops-memory:roadmap-native       # Native loop with memory
/lisa-loops-memory:roadmap-orchestrated # External orchestrator mode
```

## Memory Architecture

```
.agent/
├── memory/
│   ├── semantic.json      # Permanent facts (project, tech stack, personas)
│   ├── episodic.json      # Decisions with timestamps and expiry
│   └── procedural.json    # Learned patterns and heuristics
├── scratchpad.md          # Cross-iteration working memory
└── validation-results.json
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
  "personas": [
    { "name": "indie-developer", "priority": "primary" }
  ]
}
```

### Episodic Memory (Decisions)

```json
{
  "decisions": [
    {
      "id": "dec-001",
      "timestamp": "2026-01-27T10:00:00Z",
      "expires": "2026-02-26T10:00:00Z",
      "decision": "Prioritize reliability over new features",
      "rationale": "User churn feedback indicated stability concerns",
      "context": "Phase 2 planning session"
    }
  ]
}
```

### Procedural Memory (Patterns)

```json
{
  "patterns": [
    {
      "id": "pat-001",
      "observation": "Stories touching auth module are usually L/XL complexity",
      "confidence": 0.85,
      "observations_count": 12
    }
  ]
}
```

## Outputs

Files written to `./scopecraft/`:

- `VISION_AND_STAGE_DEFINITION.md`
- `ROADMAP.md`
- `EPICS_AND_STORIES.md`
- `RISKS_AND_DEPENDENCIES.md`
- `METRICS_AND_PMF.md`
- `OPEN_QUESTIONS.md`

## Compatibility

| System | Support |
|--------|---------|
| Claude Code | Native |
| ralph-orchestrator v2.2.0 | Full |
| multi-agent-ralph-loop | Inspired by |

## Roadmap

- [x] Fork from ralph-it-up v1.2.0
- [ ] Implement semantic memory store
- [ ] Implement episodic memory with TTL
- [ ] Implement procedural memory learning
- [ ] Add memory-aware agents
- [ ] Multi-model consensus (future)

## License

MIT
