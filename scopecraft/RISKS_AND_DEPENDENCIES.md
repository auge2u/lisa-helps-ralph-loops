# Risks and Dependencies

## Risk Register

| Risk | Type | Likelihood | Impact | Mitigation | Owner |
|------|------|------------|--------|------------|-------|
| R1: Marketplace rejection | GTM | Medium | Medium | Review requirements early; test plugin install/uninstall cycle | Lisa |
| R2: Repository transfer breaks CI | Process | Medium | Low | Test workflow in fork first; transfer during low-activity window | DevOps |
| R3: Pipeline fails on diverse projects | Technical | Medium | High | Test on 10+ repos; add fallbacks for missing docs/configs | Lisa |
| R4: PyYAML dependency blocks users | Technical | Medium | Medium | Implement JSON-only fallback mode for validate.py | Lisa |
| R5: Ecosystem path changes break reconcile | Technical | Low | Medium | Add git remote-based identification; document path update | Lisa |
| R6: No external user adoption | GTM | Medium | High | Standalone value clear; Carlos/Conductor are additive | Product |
| R7: Context rollover detection unreliable | Technical | Medium | Medium | Start with explicit signals; Conductor handles this | Conductor |
| R8: Single developer bottleneck | Organizational | High | High | Document decisions in .gt/; reconcile for context recovery | All |
| R9: Claude Code plugin system changes | External | Low | High | Track upstream changes; insulate with thin adapter | Lisa |
| R10: Reconcile performance with many projects | Technical | Low | Medium | Incremental reconcile; cache unchanged projects | Lisa |

## Dependency Map

### External Dependencies

| Dependency | Used By | Risk Level | Notes |
|------------|---------|------------|-------|
| Claude Code Plugin System | Lisa | Medium | Plugin format stable but evolving |
| PyYAML | validate.py | Low | Optional with fallback mode |
| Gastown | .gt/ format | Medium | Lisa outputs .gt/; Gastown consumes |
| prductr-com GitHub org | Migration | Medium | Must be created before Phase 4 |
| Claude Code Marketplace | Distribution | Medium | Submission requirements unknown |

### Internal Dependencies (Plugin-to-Plugin)

| From | To | Interface | Required? | Status |
|------|-----|-----------|-----------|--------|
| Lisa | Carlos | `.gt/memory/semantic.json` | No | Aligned |
| Lisa | Conductor | `.gt/beads/*.json`, `.gt/convoys/*.json` | No | Aligned (Zod schema) |
| Carlos | Lisa | `scopecraft/` output format | No | Aligned |
| Conductor | Lisa | `.gt/` state for task assignment | No | Aligned (GA) |
| Conductor | Carlos | Agent personas for specialist routing | No | Aligned (gt-eco01) |

### Inter-Phase Dependencies

```
Phase 1-3 (COMPLETE)
  +-- Foundation Alignment
  +-- Interface Contracts
  +-- Conductor Integration (GA)
      |
Phase 4 (Publish & Migrate)
  +-- Marketplace submission
  +-- prductr-com transfer
  +-- Getting started docs
      |
Phase 5 (Standalone Hardening)
  +-- Graceful degradation
  +-- Diverse project validation
  +-- PyYAML fallback
      |
Phase 6 (Ecosystem Maturity)
  +-- Reconcile resilience
  +-- Cost tracking
  +-- e2b integration (via Conductor)
```

### Critical Path

The critical path to first external user is: **marketplace submission -> plugin install -> getting started guide -> first /lisa:discover run**. Standalone hardening is important but not blocking for initial publication.
