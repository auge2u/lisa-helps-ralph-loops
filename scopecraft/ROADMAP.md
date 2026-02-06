# Ecosystem Roadmap

## Phase 1 — Foundation Alignment
**Objective (Outcome):** All three plugins have self-describing semantic memory and Lisa can read them all for reconciliation.
**Customer value:** First unified view of ecosystem state; context recovery works across projects.
**Deliverables:**
- Lisa `.gt/memory/semantic.json` populated (this repo)
- Carlos `.gt/memory/semantic.json` populated (done)
- Conductor `.gt/memory/semantic.json` populated
- Ecosystem `scopecraft/` created in Lisa root (this document set)
- First `/lisa:reconcile` produces alignment report + checkpoint
**Dependencies:** None (each plugin already works standalone)
**Risks + mitigations:**
- Conductor may not be far enough along for meaningful semantic.json -> Use placeholder with known gaps documented
- Semantic.json schema may need ecosystem-level fields -> Carlos already added `ecosystem_role`; standardize across all three
**Metrics / KRs:**
- All 3 semantic.json files pass Lisa discover quality gates
- Reconcile produces `.checkpoint.json` and `ALIGNMENT_REPORT.md`
**Definition of Done:** `/lisa:reconcile` runs successfully across all three projects, producing a checkpoint and alignment report.

## Phase 2 — Interface Contracts
**Objective (Outcome):** Carlos reads Lisa's `.gt/` state and Lisa's `gates.yaml`; shared formats are validated end-to-end.
**Customer value:** No duplicate discovery work; consistent quality standards across plugins.
**Deliverables:**
- Carlos reads `.gt/memory/semantic.json` before running discovery (skip if fresh)
- Carlos quality gates align with `gates.yaml` format (can validate Lisa outputs)
- `scopecraft/` output format validated by both Lisa and Carlos
- Interface contract tests exist for `.gt/` schema and `scopecraft/` format
**Dependencies:** Phase 1 (semantic.json populated, reconcile working)
**Risks + mitigations:**
- Carlos has hardcoded quality gates vs. Lisa's declarative gates.yaml -> Incremental migration: Carlos reads gates.yaml if present, falls back to hardcoded
- Schema drift between plugins -> Add schema version to `.gt/` files; reconcile detects version mismatches
**Metrics / KRs:**
- Carlos skips discovery when fresh semantic.json exists (latency reduction measurable)
- Zero quality gate definition duplication between Lisa and Carlos
**Definition of Done:** Running Carlos against a Lisa-discovered project uses existing `.gt/` state without re-scanning.

## Phase 3 — Conductor Integration
**Objective (Outcome):** Conductor can assign Lisa beads/convoys to agents and route analysis tasks to Carlos.
**Customer value:** Multi-agent work execution from structured work items; specialist routing for quality.
**Deliverables:**
- Conductor MCP tools: `conductor_claim_task`, `conductor_complete_task`, `conductor_heartbeat`, `conductor_lock_file`
- Conductor reads `.gt/beads/*.json` and `.gt/convoys/*.json` for task assignment
- Conductor routes quality validation to Carlos agent personas
- Context rollover works for at least one CLI agent type
- Personality curation table maps task types to agent/model tiers
**Dependencies:** Phase 2 (interface contracts stable)
**Risks + mitigations:**
- MCP protocol may change -> Conductor owns adapter layer; Lisa/Carlos are insulated
- Context rollover is hard to test -> Start with simplest case: single agent, single bead, checkpoint + resume
**Metrics / KRs:**
- At least 1 convoy successfully assigned, executed, and completed via Conductor
- Context rollover preserves state across at least 1 agent restart
**Definition of Done:** End-to-end flow: Lisa structures work -> Conductor assigns to agent -> Agent completes bead -> Carlos validates output.

## Phase 4 — Ecosystem Maturity
**Objective (Outcome):** Full ecosystem operational with reconciliation cadence, cost tracking, and e2b integration for cheap labor.
**Customer value:** Autonomous multi-agent development with quality guarantees and cost control.
**Deliverables:**
- e2b sandbox integration for mechanical tasks (file scanning, linting, test running)
- Cost tracking (subscription-based for CLI agents, token-based for API)
- Reconcile cadence established (on version ship, on architecture change, on new plugin)
- Conflict resolution pipeline (Conductor queues -> specialist review -> human escalation)
- Model routing serves entire ecosystem (not just Carlos)
**Dependencies:** Phase 3 (Conductor operational)
**Risks + mitigations:**
- e2b API instability -> e2b is optional; Conductor falls back to CLI agents
- Cost tracking complexity -> Start with simple per-run estimates, not real-time metering
**Metrics / KRs:**
- 60-70% cost reduction vs. high-tier-only model usage
- Reconcile detects drift within 1 session of a breaking change
**Definition of Done:** A multi-project development session uses all three plugins together, with measurable cost savings and quality validation.
