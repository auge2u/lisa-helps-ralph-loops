# Risks and Dependencies

## Risk Register

| Risk | Type | Likelihood | Impact | Mitigation | Owner | Trigger/Signal |
|------|------|---:|---:|------|------|------|
| R1: Marketplace requirements unknown | GTM | 3 | 3 | Research requirements first (Story 4); submit and iterate | Lisa | Marketplace submission attempted |
| R2: README rewrite misses commands | Product | 2 | 2 | Cross-reference against `plugins/lisa/commands/*.md` (8 files); automated check | Lisa | External user reports wrong commands |
| R3: Repository transfer breaks CI | Technical | 3 | 2 | Test workflow in fork first; transfer during low-activity window | DevOps | CI fails after transfer |
| R4: Pipeline fails on diverse projects | Technical | 3 | 4 | Test on 10+ repos (Story 11); add fallbacks for missing docs/configs | Lisa | Crash or hang on test repo |
| R5: PyYAML dependency blocks users | Technical | 3 | 3 | Implement JSON-only fallback mode for validate.py (Story 9) | Lisa | User reports install failure |
| R6: Ecosystem path changes break reconcile | Technical | 2 | 3 | Add git remote-based identification (Story 12); document path update | Lisa | Reconcile fails after transfer |
| R7: No external user adoption | GTM | 3 | 4 | Standalone value clear; getting started guide tested on clean env | Product | Zero marketplace installs after 2 weeks |
| R8: Single developer bottleneck | Product | 4 | 4 | Document decisions in .gt/; reconcile for context recovery; open-source first | All | Break >7 days between sessions |
| R9: Claude Code plugin system changes | Technical | 2 | 4 | Track upstream changes; insulate with thin adapter; version-pin plugin format | Lisa | Plugin stops loading after CC update |
| R10: Reconcile performance at scale | Technical | 2 | 2 | Incremental reconcile (Story 13); cache unchanged projects | Lisa | Reconcile takes >30s with 5+ projects |
| R11: Stale CHANGELOG confuses users | Product | 3 | 2 | Update CHANGELOG as part of every version bump (Story 2); bump-version.sh already handles this | Lisa | User expects feature from wrong version |
| R12: Legacy test imports break on cleanup | Technical | 3 | 2 | Update test_validate_quality_gates.py imports before removing deprecated plugin | Lisa | Test suite fails after cleanup |

## Dependency Map

### External Dependencies

| Dependency | Used By | Risk Level | Notes |
|------------|---------|------------|-------|
| Claude Code Plugin System | Lisa | Medium | Plugin format stable but evolving |
| Claude Code Marketplace | Distribution | Medium | Submission requirements not yet researched |
| PyYAML | validate.py | Low | Optional with fallback mode (Story 9) |
| Gastown | .gt/ format | Medium | Lisa outputs .gt/; Gastown consumes |
| prductr-com GitHub org | Migration | Medium | Must be created before Phase 4 migration |
| pytest | Testing | Low | Standard, well-maintained |
| Python 3.10+ | Runtime | Low | Widely available |

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
  +-- Conductor Integration (GA v1.0.0)
      |
Phase 4 (Clean, Document, Ship)
  +-- README rewrite (Story 1)                 -- no deps
  +-- CHANGELOG update (Story 2)               -- no deps
  +-- Deprecated plugin archive (Story 3)      -- after Story 1
  +-- Marketplace research (Story 4)           -- no deps
  +-- Marketplace submission (Story 5)         -- after Stories 1, 4
  +-- Getting started guide (Story 6)          -- after Story 5
  +-- Repo transfer (Story 7)                  -- needs prductr-com org
  +-- Ecosystem config update (Story 8)        -- after Story 7
      |
Phase 5 (Harden & Validate)
  +-- PyYAML fallback (Story 9)                -- no deps
  +-- Graceful degradation (Story 10)          -- no deps
  +-- Diverse project testing (Story 11)       -- after Stories 9, 10
      |
Phase 6 (Ecosystem Maturity)
  +-- Git remote identification (Story 12)     -- after Story 8
  +-- Incremental reconcile (Story 13)         -- after Story 12
  +-- End-to-end ecosystem validation          -- all phases complete
```

### Critical Path

The critical path to first external user:

```
README rewrite (Story 1)
  --> Marketplace research (Story 4)
    --> Marketplace submission (Story 5)
      --> Getting started guide (Story 6)
        --> First external /lisa:discover run
```

Estimated: 2-3 weeks from start of Phase 4.

### Parallelizable Work

These can run alongside the critical path:
- CHANGELOG update (Story 2) -- immediate
- Deprecated plugin archive (Story 3) -- after Story 1
- PyYAML fallback (Story 9) -- immediate
- Graceful degradation (Story 10) -- immediate
- Repo transfer (Story 7) -- when prductr-com org ready
