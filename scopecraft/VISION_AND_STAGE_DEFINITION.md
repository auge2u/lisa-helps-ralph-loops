# Vision and Stage Definition

## Ecosystem Vision
**Customer:** Solo developers and small teams (2-10) running multiple Claude Code projects
**Problem:** Multi-project development lacks structured coordination — context gets lost between sessions, work items scatter across repos, and there's no systematic way to track quality, delegate to agents, or recover from abandoned work.
**Value:** A three-plugin ecosystem that provides structured migration, specialist analysis, and multi-agent orchestration — all communicating through stable file-based interfaces, never requiring shared runtime.

## Ecosystem Architecture

| Plugin | Role | Core Job |
|--------|------|----------|
| **Lisa** | Pipeline & Memory | Stages 0-5: research, discover, plan, structure, reconcile. Owns `.gt/` state format. Ecosystem root. |
| **Carlos** | Specialist Fixer | Focused analysis: roadmap quality, market fit scoring, tech debt auditing. Small context, sharp focus. |
| **Conductor** | Orchestration & Oversight | Multi-project, multi-agent tracking. CLI-based agents (OAuth, not API). Context rollover, conflict resolution, personality curation. |

```
CONDUCTOR (oversight, tracking, rollover)
  - Multi-project awareness
  - Agent lifecycle (heartbeat, reassignment, handoff)
  - Context exhaustion detection and rollover
  - Personality curation (which specialist for which task)
  - Conflict resolution between agents
       |
       | MCP tools / .gt/ files
       |
  LISA (pipeline)          CARLOS (specialist fixer)
  - Stages 0-5             - Called in per task
  - Semantic memory         - Quality gate enforcement
  - Beads/Convoys           - Market fit scoring
  - Reconciliation          - Tech debt auditing
  - .gt/ = shared state     - Reads .gt/, doesn't own it
```

## Current Stage
**Stage:** Alpha — Individual plugins functional, ecosystem integration not yet wired
**Evidence:**
- Lisa v0.3.0: 4-stage pipeline working (research, discover, plan, structure)
- Carlos v1.2.0: Standalone roadmap generation working, 400 tests, ecosystem role defined in semantic.json
- Conductor: Early development, `.gt/memory/semantic.json` not yet created

## Next Major Stage
**Target:** Beta — Ecosystem integration operational
**Completion Criteria:**
- [ ] All three plugins have populated `.gt/memory/semantic.json`
- [ ] Lisa reconcile can read all three semantic.json files and produce alignment report
- [ ] Carlos reads `.gt/memory/semantic.json` before running discovery (skip re-discovery)
- [ ] Carlos quality gates align with Lisa `gates.yaml` format
- [ ] Conductor can claim and complete beads via MCP tools
- [ ] Context rollover works for at least one CLI agent type
- [ ] First successful cross-project reconciliation checkpoint

## Design Principles

1. **Standalone First** — Each plugin must remain fully functional on its own. Integration is additive, never required.
2. **Isolated but Aware** — Separate repos, separate installs, separate context windows. Communication through `.gt/` files, `scopecraft/` output, and MCP tools only.
3. **Small Context, Simple Roles** — The further downstream from orchestrator, the simpler the role. Conductor=medium, Lisa=medium, Carlos=small, e2b labor=minimal.
4. **Context Rollover as First-Class Problem** — CLI agents exhaust context windows. Checkpointing, handoff, and reconciliation handle this.
5. **Insulation from Upstream Churn** — Only thin adapter layers at edges track upstream changes. Everything else insulated by stable interfaces.
6. **Personality Curation, Not Skill Generation** — Conductor composes the right capability set per task rather than generating new skills at runtime.
7. **Archaeology as Superpower** — The system never starts from zero. Past decisions, conversations, and failures are inputs.

## Assumptions
- CLI-based agents (OAuth subscriptions) are cheaper than API calls for sustained work
- Context windows will remain finite and exhaustion is a real operational problem
- File-based interfaces (.gt/, scopecraft/) are sufficient for inter-plugin communication
- Each plugin will have its own release cadence and can evolve independently

## Constraints
- No shared runtime or code imports between plugins
- All state persisted as local files (no external database required)
- Plugins must degrade gracefully when ecosystem partners are absent
- Lisa is the ecosystem root — reconciliation and alignment originate here
