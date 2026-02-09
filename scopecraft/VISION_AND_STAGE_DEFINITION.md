# Vision and Stage Definition

## Ecosystem Vision
**Customer:** Solo developers and small teams (2-10) running multiple Claude Code projects
**Problem:** Multi-project development lacks structured coordination — context gets lost between sessions, work items scatter across repos, and there's no systematic way to track quality, delegate to agents, or recover from abandoned work.
**Value:** A three-plugin ecosystem that provides structured migration, specialist analysis, and multi-agent orchestration — all communicating through stable file-based interfaces, never requiring shared runtime.

## Ecosystem Architecture

| Plugin | Role | Core Job | Status |
|--------|------|----------|--------|
| **Lisa** | Pipeline & Memory | Stages 0-5: research, discover, plan, structure, reconcile. Owns `.gt/` state format. Ecosystem root. | Alpha (v0.3.0) |
| **Carlos** | Specialist Fixer | Focused analysis: roadmap quality, market fit scoring, tech debt auditing. Small context, sharp focus. | Beta (v1.2.0) |
| **Conductor** | Orchestration & Oversight | Multi-project, multi-agent tracking. CLI-based agents (OAuth, not API). Context rollover, conflict resolution, personality curation. | **GA (v1.0.0)** |

```
CONDUCTOR (oversight, tracking, rollover) — GA v1.0.0
  - 24 MCP tools across 4 categories
  - Organization isolation, autonomy levels
  - Escalation queue, health monitoring
  - Zone-based coordination, task reassignment
       |
       | MCP tools / .gt/ files
       |
  LISA (pipeline)          CARLOS (specialist fixer)
  - Stages 0-5             - 3 agent personas registered
  - Semantic memory         - Quality gates (482 tests)
  - Beads/Convoys           - Model routing (32 combos)
  - Reconciliation          - Context optimized (~1,500 tokens)
  - .gt/ = shared state     - Reads .gt/, doesn't own it
```

## Current Stage
**Stage:** Alpha — Pipeline and reconcile functional, ecosystem integration operational, marketplace not yet published
**Evidence:**
- Lisa v0.3.0: 5-stage pipeline working (research, discover, plan, structure, reconcile)
- 31 quality gates across 5 stages defined in gates.yaml v1.1
- Reconcile v4.0.0: 24 alignments, 0 misalignments, 1 LOW gap
- All 3 ecosystem convoys complete (9/9 beads)
- Ecosystem config at `~/.lisa/ecosystem.json`
- No marketplace submission yet
- No external users

## Next Major Stage
**Target:** Beta — Ecosystem published and usable by external users
**Completion Criteria:**
- [ ] Lisa published on Claude Code marketplace
- [ ] Plugin installable via Claude Code plugin system
- [ ] Getting started documentation for new users
- [ ] Reconcile works on projects with only Lisa installed (standalone mode)
- [ ] Repository transferred to prductr-com organization
- [ ] Cross-references updated for new org paths
- [ ] First external user completes a Lisa pipeline stage

## Design Principles

1. **Standalone First** — Each plugin must remain fully functional on its own. Integration is additive, never required.
2. **Isolated but Aware** — Separate repos, separate installs, separate context windows. Communication through `.gt/` files, `scopecraft/` output, and MCP tools only.
3. **Small Context, Simple Roles** — The further downstream from orchestrator, the simpler the role.
4. **Context Rollover as First-Class Problem** — CLI agents exhaust context windows. Checkpointing, handoff, and reconciliation handle this.
5. **Insulation from Upstream Churn** — Only thin adapter layers at edges track upstream changes.
6. **Archaeology as Superpower** — The system never starts from zero. Past decisions, conversations, and failures are inputs.

## Assumptions
- CLI-based agents (OAuth subscriptions) are cheaper than API calls for sustained work
- Context windows will remain finite and exhaustion is a real operational problem
- File-based interfaces (.gt/, scopecraft/) are sufficient for inter-plugin communication
- Each plugin will have its own release cadence and can evolve independently
- Claude Code plugin marketplace will be the primary distribution channel

## Constraints
- No shared runtime or code imports between plugins
- All state persisted as local files (no external database required)
- Plugins must degrade gracefully when ecosystem partners are absent
- Lisa is the ecosystem root — reconciliation and alignment originate here
- Python-only hooks (no Node.js dependency for Lisa)
