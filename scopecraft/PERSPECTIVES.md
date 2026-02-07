# Ecosystem Perspectives

Aggregated self-reports from each plugin's `.gt/memory/semantic.json`, compared side-by-side.

**Generated:** 2026-02-06 (reconcile v2.5.0)
**Data source:** Git remote (both remotes up to date)
**Projects scanned:** 3 attempted, 3 found (all local)
**Reconcile method:** Lisa Stage 5 skill

---

## Project Status Matrix

| Field | Lisa | Carlos | Conductor |
|-------|------|--------|-----------|
| **Status** | Found (local) | Found (local) | Found (pulled) |
| **Version** | 0.3.0 | 1.2.0 | 0.1.0 |
| **Stage** | alpha | beta | alpha |
| **Type** | claude-code-plugin | claude-code-plugin | framework (monorepo) |
| **Language** | Python | Python | TypeScript |
| **Schema** | semantic-memory-v1 | semantic-memory-v1 | semantic-memory-v1 |
| **Last scan** | 2026-02-06T18:00 | 2026-02-06T19:00 | 2026-02-06T12:00 |
| **License** | MIT | MIT | MIT |
| **gates.yaml** | Yes (v1.1, 31 gates, 5 stages) | Yes (v1.0, 9 gates) | Yes (v1.1, ecosystem overlay) |
| **Own reconcile** | Yes (this report, v2.5.0) | Yes (project-level) | Yes (Cycle 2) |

---

## Conductor Cycle 2 View vs Lisa Reality

Conductor now includes Lisa3 in its reconcile but reads from the marketplace-installed copy rather than the repo. This creates factual discrepancies:

| Field | Conductor Sees | Lisa3 Actual | Source Mismatch |
|-------|---------------|-------------|-----------------|
| Version | 1.1.0 | **0.3.0** | Marketplace copy vs repo |
| Gates | 29 across 5 stages | **22 across 4 stages** | Reconcile not yet in gates.yaml |
| gates.yaml version | v1.1 | **v1.0** | Different file |
| semantic.json | "Does not exist" | **Exists** (since v2.1.0) | Wrong path |
| Carlos gates.yaml | "Hardcoded, should migrate" | **Already migrated** | Stale Carlos view |
| Carlos tests | 401 | **435** | Pre-convoy-002 data |

**Resolution path:** Conductor needs to read from `~/github/auge2u/lisa3` (repo) not `~/.claude/plugins/marketplaces/lisa3/` (installed plugin).

---

## Lisa Self-Report

**Source:** `~/github/auge2u/lisa3/.gt/memory/semantic.json`

| Attribute | Value |
|-----------|-------|
| Name | lisa |
| Role | pipeline-and-memory |
| Version | 0.3.0 |
| Standalone command | `/lisa:migrate` |
| Ecosystem root | Yes |
| Commands | 8 |
| Agents | 2 (archaeologist, migrator) |
| Skills | 5 (research, discover, plan, structure, reconcile) |
| Quality gates | 31 across 5 stages (including 9 automated reconcile gates) |
| Gate source | gates.yaml v1.1 (declarative) |
| Checkpoint schema | Formal JSON Schema (`checkpoint-schema.json`) |
| Templates | 3 reconcile output templates |

**Changed in v2.5.0:** convoy-001 complete — gates.yaml v1.0→v1.1, reconcile gates automated, templates + schema added

---

## Carlos Self-Report

**Source:** `~/github/auge2u/carlos/.gt/memory/semantic.json`

| Attribute | Value |
|-----------|-------|
| Name | carlos |
| Role | specialist-fixer |
| Version | 1.2.0 |
| LOC | 11,200 |
| Tests | 435 + 95 security |
| Quality gates | gates.yaml v1.0 (9 gates) + validate_quality_gates.py |
| Discovery cache | 24h TTL from .gt/memory/semantic.json |

**Key:** Carlos has local uncommitted edits to `.gitignore` and `CLAUDE.md` but no new commits since v2.3.0.

---

## Conductor Self-Report

**Source:** `~/github/habitusnet/conductor/.gt/memory/semantic.json`

| Attribute | Value | Change from v2.3.0 |
|-----------|-------|---------------------|
| Name | conductor | — |
| Status | alpha | — |
| Version | 0.1.0 | — |
| **Reconcile cycle** | **Cycle 2** | was Cycle 1 |
| **Projects scanned** | **3** (Conductor, Carlos, Lisa3) | was 2 |
| **New steering questions** | **3** (checkpoint, gates, Carlos migration) | was 0 |

**Key changes since v2.3.0:**
- Cycle 2 reconcile includes Lisa3 for the first time
- OQ-2 refined from "Who builds Lisa3?" to "Should Lisa3 be standalone?"
- OQ-4 updated with Lisa3 gates.yaml analysis
- 3 new steering questions raised (sq-c2-01 through sq-c2-03)
- Carlos alignment scored at 95% (up from 72%)

---

## Ecosystem Role Comparison

Unchanged from v2.3.0. All roles aligned. No conflicts.

| Responsibility | Lisa | Carlos | Conductor | Conflict? |
|----------------|------|--------|-----------|-----------|
| Pipeline ownership | Yes | No | No | None |
| Quality gate definition | Yes (gates.yaml v1.0) | Yes (gates.yaml v1.0) | No (overlay proposal) | **None (was M1, RESOLVED)** |
| Reconciliation | Yes (ecosystem root) | Yes (project-level) | Yes (ecosystem-level) | OK: complementary |

---

## Interface Agreement Check

| Interface | Lisa | Carlos | Conductor | Match? |
|-----------|------|--------|-----------|--------|
| gates.yaml | v1.0, canonical source | v1.0, Lisa-compatible | v1.1 overlay proposal | **FULL MATCH** |
| Checkpoint schema | `reconcile-checkpoint-v1` | N/A | Different format | **GAP** (cosmetic — no cross-read needed) |
| Reconcile gates | Manual checklist (gt-e4q8b pending) | N/A | 6-gate proposal in overlay | **GAP** (premature — Lisa3 gates not implemented yet) |

---

## Cross-Project Reconcile Comparison

| Finding | Lisa (v2.4.0) | Carlos (own) | Conductor (Cycle 2) |
|---------|--------------|-------------|---------------------|
| M1 resolved | Yes | Yes | **Doesn't know** (stale Carlos view) |
| Lisa3 alignment | Self: has semantic.json, 22 gates | N/A | 85% (factual errors) |
| Carlos alignment | High (gates.yaml done) | M3: semantic.json stale | 95% (doesn't know about gates.yaml) |
| Checkpoint schema | Our format is canonical | N/A | Flags as mismatch (valid finding) |

**Convergence improving.** Conductor's Cycle 2 is a big step forward (includes Lisa3), but needs to correct data sources. Next Conductor pull of this v2.4.0 should resolve most discrepancies.

---

## Notable Changes From v2.4.0

1. **convoy-001 COMPLETE:** Lisa Pipeline Hardening — 4 beads done (gate fix, templates, schema, reconcile gates).
2. **gates.yaml v1.1:** 22→31 gates, 4→5 stages, ecosystem workflow added.
3. **Reconcile gates automated:** 9 gates replace manual checklist. `validate.py --stage reconcile` now works.
4. **Formal checkpoint schema:** JSON Schema at `checkpoint-schema.json`, validated against existing checkpoint.
5. **All steering questions decided:** SQ8 (eco-convoy-NNN), SQ9 (batch later), SQ10 (Phase 1).
6. **sq-c2-01 + sq-c2-02 implemented:** Schema tolerance in SKILL.md, reconcile gates canonical in gates.yaml.
7. **G3 resolved:** Reconcile output templates created (3 files).
8. **C2 partially self-corrected:** Lisa3 now has 31 gates/5 stages (Conductor claimed 29/5, was actually 22/4).
