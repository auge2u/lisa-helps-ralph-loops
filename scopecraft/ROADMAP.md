# Ecosystem Roadmap

**Last Updated:** 2026-02-10 (post-Conductor GA refresh)

## Overview

This roadmap takes Lisa from **Alpha (v0.3.0)** to **Beta (v1.0.0)** — the transition from "working pipeline" to "publishable ecosystem root."

### Current Status Summary

| Phase | Status | Key Achievement |
|-------|--------|-----------------|
| Phase 1: Foundation | **Complete** | All 3 semantic.json populated, reconcile operational |
| Phase 2: Interface Contracts | **Complete** | Carlos gates.yaml aligned, discovery cache, shared schemas |
| Phase 3: Conductor Integration | **Complete** | Conductor GA, 24 MCP tools, ecosystem convoys done |
| Phase 4: Publish & Migrate | Next | Marketplace submission, prductr-com org transfer |

```
          Phase 1-3
          COMPLETE ──► Phase 4 ────► Phase 5 ────► Phase 6
                       Publish &      Standalone     Ecosystem
                       Migrate        Hardening      Maturity
                       (3 weeks)      (4 weeks)      (ongoing)
```

---

## Completed Phases (1-3)

### Phase 1 — Foundation Alignment (COMPLETE)
All 3 semantic.json populated. Reconcile v4.0.0 produced. 24 alignments, 0 misalignments, 1 LOW gap.

### Phase 2 — Interface Contracts (COMPLETE)
Carlos gates.yaml v1.0 follows Lisa schema. Discovery cache working. All interface contracts aligned.

### Phase 3 — Conductor Integration (COMPLETE)
Conductor GA (v1.0.0). 24 MCP tools. Context rollover. Bead import pipeline. Carlos personas registered. Model routing. 5 convoys complete. 1,374 tests.

---

## Phase 4 — Publish and Migrate (3 weeks)

**Objective (Outcome):** Lisa published on Claude Code marketplace, all 3 repos transferred to prductr-com organization.

**Customer Value:** External users can install Lisa, run pipeline stages, and benefit from ecosystem coordination.

**Deliverables:**
- Lisa plugin submitted to Claude Code marketplace
- Repository transferred from auge2u/lisa3 to prductr-com/lisa3
- CI/CD configured in new org
- Ecosystem config (`~/.lisa/ecosystem.json`) documentation updated
- Getting started guide for new users
- Reconcile handles new org paths gracefully

**Dependencies:**
- prductr-com GitHub org created
- Marketplace submission process understood
- Carlos marketplace submission in parallel (gt-mkt04)

**Risks + Mitigations:**
- Marketplace rejection -> Review submission requirements early; fix any issues
- Path changes break reconcile -> Add path resolution that follows git remotes, not filesystem paths
- Users confused by 3-plugin ecosystem -> Standalone getting-started that works with Lisa only

**Metrics / KRs:**
- Lisa installable via Claude Code marketplace
- Repository accessible at prductr-com/lisa3
- Getting started guide enables first pipeline run
- Reconcile works after path change

**Definition of Done:** A new user installs Lisa from marketplace, runs `/lisa:discover` on their project, and gets a populated `.gt/memory/semantic.json`.

---

## Phase 5 — Standalone Hardening (4 weeks)

**Objective (Outcome):** Lisa works reliably as a standalone plugin without Carlos or Conductor.

**Customer Value:** Users get value from Lisa without installing the full ecosystem.

**Deliverables:**
- Graceful degradation when ecosystem partners absent
- Error messages guide users toward ecosystem benefits without requiring them
- Validate.py runs without PyYAML (fallback mode)
- Pipeline stages work on projects without `.gt/` pre-existing state
- External validation: test on 10+ diverse open-source repos
- Edge case documentation

**Dependencies:**
- Phase 4 complete (plugin published)
- External user feedback

**Risks + Mitigations:**
- Pipeline assumptions don't hold for diverse projects -> Test broadly; add fallbacks for missing docs/configs
- Gates too strict for small projects -> Consider project size profiles (from Carlos Phase 4)
- PyYAML dependency blocks users -> Fallback to JSON-only validation

**Metrics / KRs:**
- Pipeline completes on 10+ diverse repos without errors
- Zero hard dependencies on Carlos or Conductor
- validate.py runs in fallback mode without PyYAML

**Definition of Done:** A user with only Lisa installed can run the full pipeline (discover → plan → structure) on any Python/TypeScript/Go project.

---

## Phase 6 — Ecosystem Maturity (ongoing)

**Objective (Outcome):** Full ecosystem operational with reconciliation cadence, cost tracking, and e2b integration.

**Customer Value:** Autonomous multi-agent development with quality guarantees and cost control.

**Deliverables:**
- Reconcile cadence established (on version ship, on architecture change, on new plugin)
- e2b sandbox integration for mechanical tasks (via Conductor)
- Cost tracking (model routing serves entire ecosystem)
- Model routing serves entire ecosystem (not just Carlos)
- Conflict resolution pipeline (Conductor queues -> specialist review -> human escalation)

**Dependencies:** Phase 5 (standalone stable), Conductor deployed (Phase 1 of Conductor roadmap)

**Risks + Mitigations:**
- e2b API instability -> e2b is optional; Conductor falls back to CLI agents
- Cost tracking complexity -> Start with simple per-run estimates

**Metrics / KRs:**
- 60-70% cost reduction vs. high-tier-only model usage
- Reconcile detects drift within 1 session of a breaking change
- End-to-end: Lisa structure -> Conductor assign -> Agent complete -> Carlos validate

**Definition of Done:** A multi-project development session uses all three plugins together, with measurable cost savings and quality validation.
