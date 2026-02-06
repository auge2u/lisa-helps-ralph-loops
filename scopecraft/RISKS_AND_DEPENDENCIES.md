# Risks and Dependencies

## Risk Register

| Risk | Type | Likelihood | Impact | Mitigation | Owner | Trigger/Signal |
|---|---|---:|---:|---|---|---|
| Conductor too early for meaningful integration | Technical | 4 | 3 | Use placeholder semantic.json; reconcile handles missing plugins gracefully | Lisa | Conductor has no `.gt/` directory |
| Schema drift between plugins | Technical | 3 | 4 | Version schemas (`semantic-memory-v1`); reconcile detects version mismatches | Lisa | Reconcile finds incompatible schema versions |
| Context rollover detection unreliable | Technical | 4 | 4 | Start with explicit signals, not implicit detection; checkpoint aggressively | Conductor | Agent produces degraded output near context limit |
| MCP protocol changes break Conductor | External | 3 | 3 | Conductor owns thin adapter layer; Lisa/Carlos are insulated | Conductor | MCP spec update announcement |
| e2b sandbox API instability | External | 3 | 2 | e2b is optional; fall back to CLI agents for all tasks | Conductor | e2b API errors in production |
| Quality gate duplication between Lisa and Carlos | Process | 5 | 3 | Phase 2 aligns Carlos gates with `gates.yaml`; single source of truth | Carlos | Same gate defined differently in two places |
| Plugin release cadence divergence | Process | 3 | 2 | Reconcile cadence: re-run on every version ship | Lisa | Reconcile shows drifted alignment status |
| CLI agent cost unpredictability | Financial | 3 | 3 | Model routing (Carlos) targets 60-70% savings; cost tracking in Phase 4 | Carlos | Per-run cost exceeds $2 budget |
| Single developer bottleneck | Organizational | 4 | 4 | Document decisions in `.gt/`; reconcile provides context recovery for cold starts | All | Break >7 days between sessions |

## Dependency Map

### External Dependencies

| Dependency | Used By | Risk Level | Notes |
|------------|---------|------------|-------|
| Claude Code Plugin System | All three | Medium | Plugin format is stable but evolving |
| MCP Protocol | Conductor | Medium | Core protocol stable; tool definitions may change |
| e2b Sandbox API | Conductor | Low | Optional; graceful degradation if unavailable |
| PyYAML | Lisa, Carlos | Low | Stable, well-maintained |
| Gastown | Lisa | Medium | Lisa outputs .gt/ format; Gastown consumes it |

### Internal Dependencies (Plugin-to-Plugin)

| From | To | Interface | Required? |
|------|-----|-----------|-----------|
| Lisa | Carlos | `.gt/memory/semantic.json` | No (Carlos can self-discover) |
| Lisa | Conductor | `.gt/beads/*.json`, `.gt/convoys/*.json` | No (Conductor can create own tasks) |
| Carlos | Lisa | `scopecraft/` output format | No (Carlos writes own scopecraft/) |
| Conductor | Lisa | `.gt/` state for task assignment | No (Conductor can use own task queue) |
| Conductor | Carlos | Agent personas for specialist routing | No (Conductor can use generic agents) |

### Inter-Phase Dependencies

```
Phase 1 (Foundation)
  ├── Lisa semantic.json
  ├── Carlos semantic.json ✓
  ├── Conductor semantic.json
  └── Ecosystem scopecraft/ ← THIS DOCUMENT SET
        │
Phase 2 (Interface Contracts)
  ├── Carlos reads .gt/ state
  ├── Gates.yaml alignment
  └── Interface contract tests
        │
Phase 3 (Conductor Integration)
  ├── MCP task assignment
  ├── Bead/convoy consumption
  └── Context rollover
        │
Phase 4 (Ecosystem Maturity)
  ├── e2b integration
  ├── Cost tracking
  ├── Model routing (ecosystem-wide)
  └── Conflict resolution pipeline
```
