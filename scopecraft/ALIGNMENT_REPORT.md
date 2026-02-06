# Ecosystem Alignment Report

**Generated:** 2026-02-06 (reconcile v2.1.0)
**Previous reconcile:** 2026-02-06 v2.0.0
**Ecosystem root:** lisa3 (this repo)
**Reconcile method:** Lisa Stage 5 skill
**Projects:** Lisa (local), Carlos (local), Conductor (local)

---

## Summary

| Status | Count | Change from v2.0.0 |
|--------|-------|---------------------|
| Aligned | 12 | — |
| Misaligned | 1 | — |
| Gaps | 1 | -1 (G6 resolved: Lisa semantic.json updated) |

**Overall assessment:** Incremental improvement from v2.0.0. The only change is G6 resolved — Lisa's `semantic.json` now includes Stage 5 reconcile in pipeline, skills, and agent stages. One misalignment remains (M1: Carlos quality gate dual source) with a clear resolution path. One gap remains (G3: no reconcile output templates). All steering questions resolved.

---

## Changes Since v2.0.0

| Item | v2.0.0 | v2.1.0 | Impact |
|------|--------|--------|--------|
| Lisa semantic.json | Missing reconcile in skills/pipeline | Reconcile skill, Stage 5 pipeline, migrator stages [1,2,3,5], evidence updated | **G6 resolved** |

---

## Alignments (What's Working)

### A1: Role separation is clear and agreed
Lisa claims pipeline + memory. Carlos claims specialist-fixer. Conductor claims orchestration-and-oversight. All three now use `semantic-memory-v1` and explicitly declare their `ecosystem_role`. No role overlap.

### A2: .gt/ schema ownership is unambiguous
Lisa writes `.gt/` state. Carlos reads it. Conductor now explicitly declares it reads `.gt/beads/*.json` and `.gt/convoys/*.json` and does not own the `.gt/` directory schema.

### A3: scopecraft/ is a shared output format
Lisa (plan stage) and Carlos (roadmap command) write to `scopecraft/`. Conductor reads it for project roadmap context. All three agree this is shared.

### A4: Ecosystem root agreement
All three projects independently identify `lisa3` as the ecosystem root hosting reconcile and ecosystem `scopecraft/`.

### A5: Standalone-first principle upheld
All three self-reports confirm independent operation with `standalone: true`. Lisa: `/lisa:migrate`. Carlos: `/carlos:roadmap`. Conductor: CLI + MCP server.

### A6: Discovery handoff planned
Carlos reads `.gt/memory/semantic.json` to skip re-discovery. Conductor reads it for project context in context bundles. Lisa generates it. Chain is clear.

### A7: Interface contracts match (Lisa <> Carlos)
Lisa provides `.gt/memory/semantic.json`, `gates.yaml` schema, `scopecraft/` format. Carlos reads all three. No contradictions.

### A8: Interface contracts match (Lisa <> Conductor)
Lisa provides `.gt/beads/*.json` and `.gt/convoys/*.json`. Conductor declares it reads both for task assignment. Lisa provides `.gt/memory/semantic.json`. Conductor reads it for personality curation. No contradictions.

### A9: Interface contracts match (Carlos <> Conductor)
Conductor routes to Carlos agent personas (tech-auditor, market-fit-auditor, product-owner). Carlos confirms it can be called as specialist. Conductor receives quality gate validation from Carlos. No contradictions.

### A10: Non-goals are complementary (NEW)
Each project explicitly lists what it does NOT do, and those responsibilities map to another project:
- Lisa non-goals -> Carlos (specialist analysis) + Conductor (orchestration)
- Carlos non-goals -> Lisa (pipeline) + Conductor (orchestration)
- Conductor non-goals -> Lisa (pipeline, semantic memory, roadmap) + Carlos (quality gates, specialist analysis)

### A11: Conductor schema aligned (NEW — was M4)
Conductor now uses `semantic-memory-v1` schema with full `ecosystem_role`, `integration_points`, `non_goals`, and `evidence` sections. Direct comparison is possible across all three projects.

### A12: All projects locally accessible (NEW — was G5)
All three repos are cloned locally. No GitHub API fallback needed for reconcile.

---

## Misalignments (Need Resolution)

### M1: Quality Gate Dual Source (PRIORITY: HIGH) — UNCHANGED
**Lisa's view:** `gates.yaml` is "single source of truth" with 22 gates across 4 stages
**Carlos's view:** Hardcoded 6 blocker gates in `validate_quality_gates.py`, acknowledges "should align with gates.yaml"
**Conductor's view:** No quality gates (lists Lisa/Carlos gates as "does not own")

**Impact:** Gate definitions can drift between Lisa and Carlos.
**Resolution:** Phase 2, Story 7 — Carlos creates own `gates.yaml` following same schema. Reconcile validates consistency.
**Status:** Unchanged. Carlos still uses hardcoded gates.

---

## Gaps (Remaining)

### G3: No reconcile output templates — UNCHANGED
Reconcile has no templates for its outputs (ALIGNMENT_REPORT.md, PERSPECTIVES.md) unlike the plan stage which has 6 templates. Output format is defined in the skill procedure but not as reusable templates.

### ~~G6: Lisa semantic.json stale on Stage 5~~ — RESOLVED
Lisa's `.gt/memory/semantic.json` now includes reconcile in `capabilities.skills`, `pipeline.stages` includes Stage 5, and `migrator` agent lists stages `[1, 2, 3, 5]`.

---

## Resolved Items

### ~~M3: Reconcile Not a Lisa Pipeline Stage~~ — RESOLVED
**v1.1.0 said:** "Reconcile was run manually from Carlos."
**v2.0.0 finding:** Stage 5 reconcile implemented with command (`commands/reconcile.md`), skill (`skills/reconcile/SKILL.md`), and ecosystem config (`~/.lisa/ecosystem.json`).
**Resolution:** This reconcile is the first run through the implemented pipeline.

### ~~M4: Conductor Schema Divergence~~ — RESOLVED
**v1.1.0 said:** "Uses `gastown semantic-memory.json` schema, missing ecosystem_role, integration_points, non_goals"
**v2.0.0 finding:** Conductor now uses `semantic-memory-v1` with full ecosystem fields. Previous scan noted as `2026-02-05T15:35:00Z (v1.0.0, gastown schema, no ecosystem fields)`.
**Resolution:** SQ6 answered (Conductor adopted `semantic-memory-v1`). SQ7 answered (added to existing `semantic.json`).

### ~~G1: No reconcile skill implementation~~ — RESOLVED
**v1.1.0 said:** "skills/reconcile/SKILL.md doesn't exist"
**v2.0.0 finding:** Skill file created with 6-step procedure, output schemas, and error handling.

### ~~G4: Ecosystem project paths not configurable~~ — RESOLVED
**v1.1.0 said:** "Reconcile needs ~/.lisa/ecosystem.json"
**v2.0.0 finding:** `~/.lisa/ecosystem.json` created with `ecosystem-config-v1` schema.

### ~~G5: Conductor not cloned locally~~ — RESOLVED
**v1.1.0 said:** "Reconcile had to use GitHub API."
**v2.0.0 finding:** Conductor cloned at `~/github/habitusnet/conductor/`.

### ~~G6: Lisa semantic.json stale on Stage 5~~ — RESOLVED
**v2.0.0 said:** "Missing reconcile in skills/pipeline."
**v2.1.0 finding:** `semantic.json` updated with reconcile skill, Stage 5 pipeline entry, migrator stages `[1, 2, 3, 5]`, and evidence for new files.

---

## Steering Questions — All Previously Open Questions RESOLVED

| # | Question | Decision |
|---|----------|----------|
| 1 | Conductor timeline | **After Phase 1** — Focus on Lisa + Carlos foundation first |
| 2 | Quality gate alignment | **Each plugin gets own `gates.yaml`** following same schema |
| 3 | Reconcile implementation | **Lightweight** — command + skill (implemented) |
| 4 | Project path configuration | **Config file** at `~/.lisa/ecosystem.json` (implemented) |
| 5 | Conductor repo location | **habitusnet org** — `~/github/habitusnet/conductor/` (cloned) |
| 6 | Schema alignment approach | **RESOLVED:** Conductor adopted `semantic-memory-v1` |
| 7 | Conductor ecosystem fields | **RESOLVED:** Added to existing `semantic.json` |

No new steering questions.

---

## Next Actions

| Priority | Action | Owner | Blocks | Status |
|----------|--------|-------|--------|--------|
| P1 | Create Carlos `gates.yaml` following Lisa's schema | Carlos | M1 resolution, Phase 2 gate alignment | Unchanged |
| ~~P2~~ | ~~Update Lisa `semantic.json` to include Stage 5 in pipeline/skills~~ | ~~Lisa~~ | ~~G6~~ | Resolved v2.1.0 |
| P3 | Create reconcile output templates (like plan stage has) | Lisa | G3, output consistency | Unchanged |
| P3 | Define `.checkpoint.json` schema formally | Lisa | Context recovery documentation | Unchanged |
