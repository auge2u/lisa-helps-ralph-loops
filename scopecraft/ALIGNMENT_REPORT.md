# Ecosystem Alignment Report

**Generated:** 2026-02-06 (reconcile v1.1.0)
**Previous reconcile:** 2026-02-06 v1.0.0
**Ecosystem root:** lisa3 (this repo)
**Reconcile source:** Carlos repo (cross-project reconcile)
**Projects:** Lisa (found local), Carlos (found local), Conductor (found GitHub)

---

## Summary

| Status | Count | Change from v1.0.0 |
|--------|-------|---------------------|
| Aligned | 9 | +1 (Conductor exists) |
| Misaligned | 2 | -1 (M2 resolved: Conductor found) |
| New findings | 2 | Schema divergence, ecosystem awareness gap |
| Gaps | 3 | -1 (checkpoint format exists now) |

**Overall assessment:** Significant progress since v1.0.0. The biggest correction: **Conductor exists on GitHub with a comprehensive semantic.json and 8-package monorepo**. Previous reconcile incorrectly stated it was missing. However, Conductor doesn't yet describe itself as an ecosystem participant — its semantic.json uses a different schema and lacks `ecosystem_role`, `integration_points`, and `.gt/` references. The Lisa+Carlos foundation remains solid and aligned.

---

## Changes Since v1.0.0

| Item | v1.0.0 | v1.1.0 | Impact |
|------|--------|--------|--------|
| Conductor status | "Repository does not exist" | Exists on GitHub, full semantic.json, 8 packages | **M2 resolved** — Phase 3 unblocked |
| Conductor local clone | Missing | Still not cloned | Action needed |
| Carlos design doc | Not committed | Committed (`92f74a0`) | Architecture documented in Carlos repo |
| Checkpoint format | "No schema defined" | Checkpoint exists (v1.0.0 format) | **G2 partially resolved** |
| Conductor schema | N/A | Different from Lisa/Carlos | **New finding: M4** |

---

## Alignments (What's Working)

### A1: Role separation is clear and agreed
Lisa claims pipeline + memory. Carlos claims specialist-fixer. Neither claims the other's territory. Both reference the same ecosystem architecture.

### A2: .gt/ schema ownership is unambiguous
Lisa writes `.gt/` state. Carlos reads it. No write conflicts.

### A3: scopecraft/ is a shared output format
Both Lisa (plan stage) and Carlos (roadmap command) write to `scopecraft/`. Design doc designates this as shared. No conflict.

### A4: Ecosystem root agreement
Both Lisa and Carlos independently identify `lisa3` as the ecosystem root.

### A5: Standalone-first principle upheld
Lisa works without Carlos. Carlos works without Lisa. Conductor works standalone. All self-reports confirm independent operation.

### A6: Discovery handoff planned
Carlos's semantic.json explicitly states it reads `.gt/memory/semantic.json` to skip re-discovery.

### A7: Interface contracts match (Lisa ↔ Carlos)
Both plugins agree on what they read and write. No contradictions.

### A8: Gastown concepts shared
Lisa defines bead/convoy schemas. Carlos references them as read-only. Format ownership is clear.

### A9: Conductor capabilities match design doc expectations (NEW)
The design doc specified Conductor should have: MCP tools, CLI agent tracking, e2b integration, file locks, dashboard. Conductor's semantic.json confirms **all of these exist** as packages in the monorepo.

---

## Misalignments (Need Resolution)

### M1: Quality Gate Dual Source (PRIORITY: HIGH) — UNCHANGED
**Lisa's view:** `gates.yaml` is "single source of truth" with 22 gates across 4 stages
**Carlos's view:** Hardcoded 6 blocker gates, acknowledges "should align with gates.yaml"

**Impact:** Gate definitions can drift.
**Resolution:** Phase 2, Story 7 — Carlos reads Lisa's `gates.yaml` format, falls back to hardcoded if not found.
**Status:** Acknowledged by Carlos (in semantic.json), not yet implemented.

### M3: Reconcile Not Yet Wired as Lisa Pipeline Stage (PRIORITY: MEDIUM) — UNCHANGED
**Expected:** `/lisa:reconcile` implemented as Stage 5 with skill, agent, quality gates
**Actual:** Reconcile command spec exists but no skill implementation. This reconcile was run manually from Carlos.

**Impact:** Reconciliation is not repeatable via Lisa's pipeline.
**Resolution:** Implement reconcile as Stage 5 in Lisa.
**Status:** Design exists, implementation pending.

### M4: Conductor Schema Divergence (PRIORITY: HIGH) — NEW
**Expected:** Conductor uses `semantic-memory-v1` schema with `ecosystem_role`, `integration_points`, `non_goals`
**Actual:** Conductor uses `https://gastown.dev/schemas/semantic-memory.json` — a different schema without ecosystem fields

**Impact:** Lisa's reconcile cannot directly compare Conductor's self-report against Lisa/Carlos. Conductor doesn't declare what it reads from `.gt/`, what it writes, or its ecosystem boundaries.
**Resolution:** Add `ecosystem_role`, `integration_points`, and `non_goals` fields to Conductor's semantic.json (can keep existing fields too — additive change).
**Status:** Not yet acknowledged by Conductor.

**Details (see PERSPECTIVES.md for full comparison):**
- Missing: `ecosystem_role.reads_from` (should reference `.gt/beads/*.json`, `.gt/convoys/*.json`)
- Missing: `ecosystem_role.writes_to` (task status, file locks, cost events)
- Missing: `ecosystem_role.does_not_own` (`.gt/` schema, `scopecraft/`, quality gates)
- Missing: `integration_points.lisa` and `integration_points.carlos`

---

## Gaps (Remaining)

### G1: No reconcile skill implementation — UNCHANGED
The `skills/reconcile/SKILL.md` file doesn't exist in Lisa. Reconcile was run from Carlos following the command spec.

### G3: No PERSPECTIVES template — UNCHANGED
Reconcile has no templates for its outputs unlike plan stage which has 6.

### G4: Ecosystem project paths not configurable — UNCHANGED
Reconcile needs `~/.lisa/ecosystem.json` to know where Carlos and Conductor repos live.

### G5: Conductor not cloned locally — NEW
Conductor exists on GitHub (`habitusnet/conductor`) but isn't cloned to `~/github/habitusnet/conductor/`. Reconcile had to use GitHub API to read its semantic.json.

---

## Resolved Items

### ~~M2: Conductor Does Not Exist~~ — RESOLVED
**v1.0.0 said:** "Repository does not exist. No `.gt/` state, no semantic.json, no code."
**v1.1.0 finding:** Repository exists at `habitusnet/conductor` on GitHub. Has comprehensive semantic.json (8 packages, full domain model, multiple LLM integrations). Pushed 2026-02-06.
**Resolution:** Clone locally and add `ecosystem_role` fields.

### ~~G2: No checkpoint schema defined~~ — PARTIALLY RESOLVED
**v1.0.0 said:** "No schema exists."
**v1.1.0 finding:** `.checkpoint.json` exists with `reconcile-checkpoint-v1` schema. Contains project state, alignment summary, misalignments, decisions, and next triggers.
**Remaining:** Schema not formally documented (but the checkpoint itself serves as the de facto spec).

---

## Steering Questions — RESOLVED (carried from v1.0.0)

| # | Question | Decision |
|---|----------|----------|
| 1 | Conductor timeline | **After Phase 1** — Focus on Lisa + Carlos foundation first |
| 2 | Quality gate alignment | **Each plugin gets own `gates.yaml`** following same schema |
| 3 | Reconcile implementation | **Lightweight** — command + skill now; defer agent and quality gates |
| 4 | Project path configuration | **Config file** at `~/.lisa/ecosystem.json` |
| 5 | Conductor repo location | **habitusnet org** — `~/github/habitusnet/conductor/` |

### New Steering Questions (v1.1.0)

| # | Question | Options |
|---|----------|---------|
| 6 | Schema alignment approach | Should Conductor adopt `semantic-memory-v1` schema, or should reconcile handle multiple schemas? |
| 7 | Conductor ecosystem fields | Should `ecosystem_role` be added to Conductor's existing semantic.json or as a separate file? |

---

## Next Actions

| Priority | Action | Owner | Blocks | Status |
|----------|--------|-------|--------|--------|
| **P0** | Clone Conductor locally | User | Local reconcile, all Conductor work | NEW |
| **P0** | Add `ecosystem_role` + `integration_points` to Conductor semantic.json | Conductor | Schema alignment, reconcile comparison | NEW |
| P1 | Implement Lisa reconcile command + skill (lightweight) | Lisa | Repeatable reconciliation | Unchanged |
| P1 | Create `~/.lisa/ecosystem.json` config for project paths | Lisa | Multi-project reconcile | Unchanged |
| P2 | Create Carlos `gates.yaml` following Lisa's schema | Carlos | Phase 2 gate alignment | Unchanged |
| P3 | Define .checkpoint.json schema formally | Lisa | Context recovery | Unchanged |
| P3 | Add reconcile quality gates to Lisa's gates.yaml | Lisa | Validation of reconcile outputs | Unchanged |
