# Ecosystem Roadmap

**Last Updated:** 2026-02-10 (Plan Stage 2 execution)

## Overview

This roadmap takes Lisa from **Alpha (v0.3.0)** to **Beta (v1.0.0)** -- the transition from "working pipeline" to "published, standalone-reliable ecosystem root."

### Current Status

| Phase | Status | Key Achievement |
|-------|--------|-----------------|
| Phase 1: Foundation Alignment | **Complete** | All 3 semantic.json populated, reconcile operational |
| Phase 2: Interface Contracts | **Complete** | Carlos gates.yaml aligned, discovery cache, shared schemas |
| Phase 3: Conductor Integration | **Complete** | Conductor GA (v1.0.0), 24 MCP tools, ecosystem convoys done |

### What Remains

```
Phase 4 ---------> Phase 5 ----------> Phase 6
Clean, Document,   Harden &            Ecosystem
Ship (v0.4.0)      Validate (v0.5.0)   Maturity (v1.0.0)
~3 weeks           ~4 weeks            ongoing
```

---

## Completed Phases (1-3)

### Phase 1 -- Foundation Alignment (COMPLETE)
All 3 semantic.json populated. Reconcile v4.0.0 produced. 24 alignments, 0 misalignments, 1 LOW gap (G8: Conductor MCP tool listing incomplete).

### Phase 2 -- Interface Contracts (COMPLETE)
Carlos gates.yaml v1.0 follows Lisa schema. Discovery cache working (24h TTL). All interface contracts aligned. Bead/convoy schemas validated via Zod in Conductor.

### Phase 3 -- Conductor Integration (COMPLETE)
Conductor GA (v1.0.0). 24 MCP tools across 4 categories. Context rollover via SQLite + bead sync. Bead import pipeline. Carlos personas registered. Model routing. 5 convoys complete (19/22 beads). 1,374 tests.

---

## Phase 4 -- Clean, Document, Ship

**Objective (Outcome):** Lisa is published on Claude Code marketplace with accurate documentation, clean codebase, and a working getting started path for new users.

**Customer Value:** External developers can discover, install, and use Lisa on their own projects without reading source code.

**Deliverables:**
- README rewritten for v0.3.0+ commands (remove all v0.2.0 references)
- CHANGELOG updated with v0.3.0 release notes
- Deprecated `lisa-loops-memory` plugin removed or clearly archived
- Getting started guide: install -> discover -> review output
- Plugin manifest validated for marketplace submission
- Lisa submitted to Claude Code marketplace
- Repository transferred to prductr-com organization
- CI/CD configured in new org (quality gate validation on PR)
- Ecosystem config documentation updated for new paths

**Dependencies:**
- prductr-com GitHub organization created
- Marketplace submission process understood (research as first step)
- Carlos marketplace submission in parallel (gt-mkt04)

**Risks + Mitigations:**
- Marketplace rejection -> Research requirements before submission; iterate on feedback
- README rewrite misses commands -> Cross-reference against `plugins/lisa/commands/*.md`
- Path changes break reconcile -> Test reconcile before and after transfer; document path update procedure

**Metrics / KRs:**
- README accurately describes all 8 commands and 5 stages
- Plugin installable from marketplace (verified by fresh install)
- Getting started guide tested on clean machine (no pre-existing .gt/)
- Reconcile runs successfully after repo transfer

**Definition of Done:** A new user installs Lisa from marketplace, follows the getting started guide, runs `/lisa:discover` on their project, and gets a populated `.gt/memory/semantic.json`.

---

## Phase 5 -- Harden and Validate

**Objective (Outcome):** Lisa works reliably as a standalone plugin across diverse projects without crashes, unclear errors, or hard dependencies on ecosystem partners.

**Customer Value:** Users trust Lisa to work on their Python, TypeScript, Go, or Rust projects without surprises.

**Deliverables:**
- validate.py runs without PyYAML (JSON-only fallback mode with clear warning)
- Graceful degradation when Carlos or Conductor absent (informational messages, not errors)
- All pipeline stages work without pre-existing `.gt/` state
- Reconcile in standalone mode reports on single project only
- External validation: pipeline tested on 10+ diverse open-source repos
- Edge case documentation (what fails, why, workarounds)
- Error messages guide users toward fixes (missing deps, unsupported project types)

**Dependencies:**
- Phase 4 complete (plugin published, users providing feedback)
- Access to diverse test repos (Python, TypeScript, Go, Rust, monorepo, minimal)

**Risks + Mitigations:**
- Pipeline assumptions break on unfamiliar project structures -> Test broadly; add fallbacks for missing docs/configs
- PyYAML fallback reduces validation coverage -> Clearly document which checks require PyYAML
- External users report issues faster than we can fix -> Prioritize crashes over feature requests

**Metrics / KRs:**
- Pipeline completes on 10+ repos across 4+ language ecosystems without crashes
- Zero hard dependencies on Carlos or Conductor (all stages pass in isolation)
- validate.py runs in fallback mode without PyYAML (file_exists and json_valid checks work)
- 90%+ pipeline stage completion rate on tested repos

**Definition of Done:** A user with only Lisa installed can run the full pipeline (discover -> plan -> structure) on any Python/TypeScript/Go project and get valid beads + convoys.

---

## Phase 6 -- Ecosystem Maturity

**Objective (Outcome):** Full ecosystem operational with reconcile cadence, incremental scanning, cost tracking, and proven multi-agent execution.

**Customer Value:** Autonomous multi-agent development with quality guarantees, cost control, and context recovery that survives developer breaks.

**Deliverables:**
- Git remote-based project identification in ecosystem.json (path + remote, prefer remote)
- Incremental reconcile (skip unchanged projects via git hash check, `--force` flag)
- Reconcile cadence established (on version ship, on architecture change, on new plugin)
- End-to-end validated: Lisa structure -> Conductor assign -> Agent complete -> Carlos validate
- e2b sandbox integration for mechanical tasks (via Conductor)
- Cost tracking across ecosystem (model routing serves all plugins)
- Conflict resolution pipeline (Conductor queues -> specialist review -> human escalation)

**Dependencies:**
- Phase 5 complete (standalone stable, external validation)
- Conductor deployed and operational (Phase 1 of Conductor roadmap)
- External users providing ecosystem feedback

**Risks + Mitigations:**
- e2b API instability -> e2b is optional; Conductor falls back to CLI agents
- Cost tracking complexity -> Start with simple per-run estimates, not real-time metering
- Reconcile performance with many projects -> Incremental scanning solves this
- Multi-agent coordination failure modes -> Conductor autonomy levels allow human escalation

**Metrics / KRs:**
- 60-70% cost reduction vs. high-tier-only model usage
- Reconcile detects drift within 1 session of a breaking change
- End-to-end flow demonstrated with all 3 plugins
- Context recovery via checkpoint restores useful context in <30 seconds

**Definition of Done:** A multi-project development session uses all three plugins together, with measurable cost savings and quality validation.
