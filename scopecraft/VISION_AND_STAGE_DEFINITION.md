# Vision and Stage Definition

## Product Vision
**Customer:** Solo developers and small teams with existing projects that need structured work extraction for multi-agent execution.
**Problem:** Projects accumulate scattered scope (TODOs, issues, docs, dead code) that no single agent can comprehend. Context windows exhaust. Work items have no structure. Multi-agent handoff is manual.
**Value:** Lisa scans any project, extracts semantic memory, generates a roadmap, and structures work items (Beads/Convoys) that Gastown agents can execute — preserving context across sessions and agents.

## Ecosystem Architecture

| Plugin | Role | Core Job | Status |
|--------|------|----------|--------|
| **Lisa** | Pipeline & Memory | Stages 0-5: research, discover, plan, structure, reconcile. Owns `.gt/` state format. Ecosystem root. | Alpha (v0.3.0) |
| **Carlos** | Specialist Fixer | Focused analysis: roadmap quality, market fit scoring, tech debt auditing. Small context, sharp focus. | Beta (v1.2.0) |
| **Conductor** | Orchestration & Oversight | Multi-project, multi-agent tracking. Organization isolation, autonomy levels, context rollover. | GA (v1.0.0) |

```
CONDUCTOR (oversight, tracking, rollover) -- GA v1.0.0
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
**Stage:** Alpha -- 5-stage pipeline functional, ecosystem wiring complete, no external distribution
**Evidence:**
- Lisa v0.3.0: 5-stage pipeline working (research, discover, plan, structure, reconcile)
- 31 quality gates across 5 stages defined in gates.yaml v1.1
- Reconcile v4.0.0: 24 alignments, 0 misalignments, 1 LOW gap
- All 3 ecosystem convoys complete (9/9 beads)
- Ecosystem config at `~/.lisa/ecosystem.json` with 3 projects
- README outdated (still references v0.2.0 commands and deprecated plugin name)
- CHANGELOG not updated for v0.3.0
- No marketplace publication
- No getting started guide for external users
- No CI/CD pipeline
- PyYAML required with no fallback
- Single developer, no external validation

## Next Major Stage
**Target:** Beta (v1.0.0) -- Published, documented, standalone-reliable
**Completion Criteria:**
- [ ] README and CHANGELOG updated to reflect v0.3.0+ commands
- [ ] Lisa published on Claude Code marketplace and installable
- [ ] Getting started guide enables first pipeline run in <15 minutes
- [ ] Pipeline tested on 10+ diverse real-world repos without crashes
- [ ] validate.py works without PyYAML (fallback mode)
- [ ] All stages work standalone (no Carlos/Conductor required)
- [ ] Repository transferred to prductr-com organization
- [ ] First external user completes a Lisa pipeline stage

## Design Principles

1. **Standalone First** -- Each plugin must remain fully functional on its own. Integration is additive, never required.
2. **Isolated but Aware** -- Separate repos, separate installs, separate context windows. Communication through `.gt/` files, `scopecraft/` output, and MCP tools only.
3. **Small Context, Simple Roles** -- The further downstream from orchestrator, the simpler the role.
4. **Context Rollover as First-Class Problem** -- CLI agents exhaust context windows. Checkpointing, handoff, and reconciliation handle this.
5. **Insulation from Upstream Churn** -- Only thin adapter layers at edges track upstream changes.
6. **Archaeology as Superpower** -- The system never starts from zero. Past decisions, conversations, and failures are inputs.

## Assumptions
- CLI-based agents (OAuth subscriptions) are cheaper than API calls for sustained work
- Context windows will remain finite and exhaustion is a real operational problem
- File-based interfaces (.gt/, scopecraft/) are sufficient for inter-plugin communication
- Each plugin will have its own release cadence and can evolve independently
- Claude Code plugin marketplace will be the primary distribution channel
- External users will try Lisa standalone before adopting the full ecosystem

## Constraints
- No shared runtime or code imports between plugins
- All state persisted as local files (no external database required)
- Plugins must degrade gracefully when ecosystem partners are absent
- Lisa is the ecosystem root -- reconciliation and alignment originate here
- Python-only hooks (no Node.js dependency for Lisa)
- Allowed output directories: `.`, `.gt`, `scopecraft` (enforced by validate.py)
