# Ecosystem Alignment Report

**Generated:** 2026-02-24 (reconcile v6.0.0)
**Previous reconcile:** 2026-02-10 v5.0.1
**Ecosystem root:** lisa3 (this repo)
**Reconcile method:** Lisa Stage 5 skill (full scan — all 3 projects changed)
**Data source:** Local filesystem (all 3 projects)
**Projects:** Lisa (local, 4 new commits), Carlos (local, 1 new commit), Conductor (local, 1 new commit)

---

## Summary

| Status | Count | Change from v5.0.1 |
|--------|-------|---------------------|
| Aligned | 30 | +4 |
| Misaligned | 0 | unchanged |
| Gaps | 2 | +1 (G10 new) |

**Overall assessment:** Session of 2026-02-24 brought a major grounding event — Lisa, Carlos, and Conductor all had Ecosystem Position sections added to their CLAUDE.md files, giving each plugin a comprehensive mental model of the full stack. More significantly, Lisa's bead schema was aligned with the real `bd` Issue schema from `steveyegge/beads`, and upstream repos were cloned as canonical reference. Four new alignments captured. One new LOW gap: Lisa's semantic.json is stale relative to the bead schema changes.

---

## Changes Since v5.0.1

| Item | Previous | Current | Impact |
|------|----------|---------|--------|
| Lisa commits | c8971e0 | **361b0b5** | 4 new (bump-version fix, Ecosystem Position, Gastown schema alignment) |
| Carlos commits | 37c7cb7 | **df3b763** | 1 new (CLAUDE.md Ecosystem Position) |
| Conductor commits | 1fdaebf | **80ed6b2** | 1 new (CLAUDE.md Ecosystem Position) |
| Lisa bead schema | priority=string, AC=array, status="pending" | **priority=int(0-4), AC=string, status="open", issue_type** | Major alignment with real bd schema |
| Lisa CLAUDE.md | Thin Gastown section | **Full Ecosystem Position + real bd/gt architecture** | All future instances start with accurate mental model |
| Carlos CLAUDE.md | Thin 8-line ecosystem section | **Full Ecosystem Position** | Role clarity for future instances |
| Conductor CLAUDE.md | No ecosystem section | **Full Ecosystem Position + context rollover pattern** | Role clarity for future instances |
| Upstream refs | None | **~/github/steveyegge/beads + ~/github/steveyegge/gastown cloned** | Canonical schema authority now local |
| Lisa semantic.json | 2026-02-10T15:00 (fresh) | **2026-02-10T15:00 (stale — new G10)** | Bead schema changes not yet reflected |

---

## Alignments (What's Working)

### A1–A26 (unchanged from v5.0.1)
All prior alignments hold. See v5.0.1 report for full details.

### A27: Upstream Gastown/Beads repos as canonical reference
Lisa CLAUDE.md now cites `~/github/steveyegge/beads/internal/types/types.go` as the canonical Issue schema source and `~/github/steveyegge/gastown/docs/overview.md` as the architecture reference. This resolves the prior ambiguity about what "Gastown bead" means — it now points to the real Go type definition.

### A28: Lisa bead schema aligned with real `bd` Issue type
Lisa's `plugins/lisa/skills/structure/templates/bead.json` and `SKILL.md` now match the actual `bd` Issue schema:
- `priority` is integer 0–4 (was string "high"/"medium")
- `acceptance_criteria` is a newline-separated string (was array)
- `status` uses real values: `open | in_progress | blocked | deferred | closed` (was "pending")
- `issue_type` replaces `type` (matches bd field name)
- `complexity` and `evidence` moved to `metadata` (not top-level bd fields)
- `description`, `design`, `notes`, `assignee`, `labels` added as first-class fields

### A29: All three plugins document ecosystem position in CLAUDE.md
Each plugin now has a comprehensive Ecosystem Position section grounding future Claude Code instances in the full stack architecture (Gastown → Conductor → Lisa/Carlos). Stack diagram, role boundary table, interface contracts, standalone-first table, and context budget principle are consistent across all three.

### A30: `bd`/`bv`/`gt` CLI integration path documented
Lisa's `structure/SKILL.md` now documents the live integration workflow: `bd create --file=<markdown>`, `bd ready`, `bd update`, `bd close`, `bd sync`, `gt convoy create`, `gt sling`. The Propulsion Principle is documented. Staging format (`.gt/beads/*.json`) is correctly framed as intermediate, not final.

---

## Misalignments (Need Resolution)

*None.*

---

## Gaps

### G8: Conductor semantic.json MCP tool categories (LOW) — unchanged
Conductor's `semantic.json` is missing `access_control` and `cost_tracking` tool categories that were dropped during GA restructure. Tools still exist in code. No functional impact — Carlos gt-eco01 registrations work. Waiting on Conductor to add categories back in next semantic.json refresh.

### G10: Lisa semantic.json stale relative to 2026-02-24 changes (LOW) — new
Lisa's `semantic.json` was last scanned `2026-02-10T15:00Z`. Since then, four significant commits landed:
- `bump-version.sh` fixed (was pointing at deprecated plugin)
- Ecosystem Position section added to CLAUDE.md (full stack mental model)
- Bead schema aligned with real `bd` Issue type (priority int, AC string, etc.)
- `structure/SKILL.md` updated with `bd`/`gt` CLI integration and Propulsion Principle
- `~/github/steveyegge/beads` and `~/github/steveyegge/gastown` cloned as canonical refs

None of these are reflected in `.gt/memory/semantic.json`. The next `/lisa:discover` will resolve G10.

**Functional impact:** None — the semantic.json is used for reconcile cross-referencing and ecosystem context. The code changes are correct regardless.

---

## Steering Questions

| # | Question | Status |
|---|----------|--------|
| cq-02 | Is 41% agent context reduction (Carlos) sufficient for Conductor? | Carlos acted; awaiting Conductor confirmation |

---

## Next Actions

| Priority | Action | Owner | Blocks |
|----------|--------|-------|--------|
| HIGH | Run `/lisa:discover` to refresh semantic.json (resolve G10) | Lisa | Next reconcile accuracy |
| LOW | Conductor refreshes semantic.json with missing MCP categories (resolve G8) | Conductor | G8 |
| LOW | Conductor confirms cq-02 (context budget) | Conductor | cq-02 closure |
| LOW | Lisa marketplace submission | Lisa | A25 trigger |
| LOW | Carlos marketplace submission | Carlos | gt-mkt04 |
