# Ecosystem Alignment Report

**Generated:** 2026-02-06
**Reconcile version:** 1.0.0
**Ecosystem root:** lisa3 (this repo)
**Projects:** Lisa (found), Carlos (found), Conductor (missing)

---

## Summary

| Status | Count | Details |
|--------|-------|---------|
| Aligned | 8 | Core role separation, interface contracts, ecosystem root agreement |
| Misaligned | 3 | Quality gate duplication, Conductor missing, reconcile not yet wired |
| Gaps | 4 | Reconcile skill/command not implemented, no checkpoint format, no PERSPECTIVES template |

**Overall assessment:** Foundation is solid. Lisa and Carlos agree on roles, interfaces, and ownership boundaries. The primary blocker is Conductor not existing yet, and quality gate duplication between Lisa and Carlos needs resolution in Phase 2.

---

## Alignments (What's Working)

### A1: Role separation is clear and agreed
Lisa claims pipeline + memory ownership. Carlos claims specialist-fixer role. Neither claims the other's territory. Both reference the same ecosystem architecture.

### A2: .gt/ schema ownership is unambiguous
Lisa writes `.gt/` state. Carlos reads it. No write conflicts.

### A3: scopecraft/ is a shared output format
Both Lisa (plan stage) and Carlos (roadmap command) write to `scopecraft/`. The design doc explicitly designates this as shared. No conflict.

### A4: Ecosystem root agreement
Both Lisa and Carlos independently identify `lisa3` as the ecosystem root. Reconciliation originates here.

### A5: Standalone-first principle upheld
Lisa works without Carlos. Carlos works without Lisa. Both self-reports confirm standalone capabilities with independent commands.

### A6: Discovery handoff planned
Carlos's semantic.json explicitly states it reads `.gt/memory/semantic.json` if it exists to skip re-discovery. This is the designed integration point.

### A7: Interface contracts match
Both plugins agree on what they read and write. No contradictions in `reads_from` vs `writes_to` claims.

### A8: Gastown concepts shared
Lisa defines bead/convoy schemas. Carlos references them as read-only. Format ownership is clear.

---

## Misalignments (Need Resolution)

### M1: Quality Gate Dual Source (PRIORITY: HIGH)
**Lisa's view:** `gates.yaml` is "single source of truth" with 22 gates across 4 stages, loaded by `validate.py`
**Carlos's view:** Hardcoded 6 blocker gates in `validate_quality_gates.py`, acknowledges "should align with Lisa gates.yaml"

**Impact:** Same concept (quality gates) defined in two places with different implementations. Gate definitions can drift.
**Resolution:** Phase 2, Story 7 — Carlos reads Lisa's `gates.yaml` format, falls back to hardcoded if not found.
**Status:** Acknowledged by Carlos (in semantic.json), not yet implemented.

### M2: Conductor Does Not Exist (PRIORITY: MEDIUM)
**Expected:** Multi-agent orchestration plugin at `~/github/habitusnet/conductor/`
**Actual:** Repository does not exist. No `.gt/` state, no semantic.json, no code.

**Impact:** Phase 3 (Conductor Integration) cannot start. E2b integration, context rollover, and personality curation are all blocked.
**Resolution:** Conductor needs to be created. Minimal viable scope: CLI agent tracking + bead assignment via MCP tools.
**Status:** Pre-development. The design doc describes expected capabilities but no implementation exists.

### M3: Reconcile Not Yet Wired (PRIORITY: MEDIUM)
**Expected:** `/lisa:reconcile` command with skill, agent, and quality gates
**Actual:** The reconcile command/skill/agent files do not exist in the Lisa plugin. This reconciliation was performed manually following the reconcile command spec.

**Impact:** Reconciliation is not repeatable via command. Context recovery via `--restore` flag doesn't work yet.
**Resolution:** Implement reconcile as Stage 5 in Lisa's pipeline: command, skill, and quality gates in `gates.yaml`.
**Status:** Design exists (command spec loaded), implementation pending.

---

## Gaps (Missing Pieces)

### G1: No reconcile skill implementation
The `skills/reconcile/SKILL.md` file doesn't exist. The reconcile command references it but there's no procedure definition.

### G2: No checkpoint schema defined
The `.checkpoint.json` format is described conceptually but no schema exists. This blocks context recovery.

### G3: No PERSPECTIVES template
Unlike plan stage which has 6 templates in `skills/plan/templates/`, reconcile has no templates for its outputs (ALIGNMENT_REPORT, PERSPECTIVES, .checkpoint.json).

### G4: Ecosystem project paths not configurable
Reconcile needs to know where Carlos and Conductor repos live. Currently hardcoded assumptions. Needs configuration mechanism.

---

## Steering Questions for Human Review

1. **Conductor timeline:** When should Conductor development start? Is Phase 1 (foundation alignment) completion the trigger, or should it start in parallel?

2. **Quality gate alignment approach:** Should Carlos read Lisa's `gates.yaml` directly (requires knowing Lisa's path), or should each plugin have its own `gates.yaml` following the same schema?

3. **Reconcile implementation priority:** Should reconcile be implemented as a proper Lisa stage (with command, skill, agent, gates) before Phase 2 starts, or can it remain manual for now?

4. **Project path configuration:** How should reconcile discover project paths? Options: config file (`~/.lisa/ecosystem.json`), convention (`~/github/*/`), or CLI arguments per session.

5. **Conductor repo location:** Should Conductor live under `auge2u` (personal) or `habitusnet` (org)? The design doc mentions `~/github/habitusnet/conductor/` but the repo doesn't exist there.

---

## Next Actions

| Priority | Action | Owner | Blocks |
|----------|--------|-------|--------|
| P0 | Answer steering questions 1-5 | Human | Everything below |
| P1 | Implement Lisa reconcile as Stage 5 (command + skill + templates) | Lisa | Repeatable reconciliation |
| P1 | Add reconcile quality gates to gates.yaml | Lisa | Validation of reconcile outputs |
| P2 | Create Conductor repo with minimal semantic.json | Conductor | Phase 1 completion |
| P2 | Begin gates.yaml alignment in Carlos | Carlos | Phase 2 |
| P3 | Define .checkpoint.json schema | Lisa | Context recovery |
| P3 | Add ecosystem project path configuration | Lisa | Multi-project reconcile automation |
