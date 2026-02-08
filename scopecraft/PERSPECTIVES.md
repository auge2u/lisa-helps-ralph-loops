# Ecosystem Perspectives

Aggregated self-reports from each plugin's `.gt/memory/semantic.json`, compared side-by-side.

**Generated:** 2026-02-08 (reconcile v3.0.0)
**Data source:** Local filesystem (all projects cloned)
**Projects scanned:** 3 attempted, 3 found (all local)
**Reconcile method:** Lisa Stage 5 skill

---

## Project Status Matrix

| Field | Lisa | Carlos | Conductor |
|-------|------|--------|-----------|
| **Status** | Found (local) | Found (local) | Found (local) |
| **Version** | 0.3.0 | 1.2.0 | 0.1.0 |
| **Stage** | alpha | beta | alpha |
| **Type** | claude-code-plugin | claude-code-plugin | framework (monorepo) |
| **Language** | Python | Python | TypeScript |
| **Schema** | semantic-memory-v1 | semantic-memory-v1 | semantic-memory-v1 |
| **Last scan** | 2026-02-06T18:00 | 2026-02-06T19:00 | 2026-02-06T12:00 |
| **License** | MIT | MIT | MIT |
| **gates.yaml** | Yes (v1.1, 31 gates, 5 stages) | Yes (v1.0, 9 gates) | Yes (v1.1, ecosystem overlay) |
| **Own reconcile** | Yes (this report, v3.0.0) | Yes (project-level) | Yes (Cycle 2) |
| **semantic.json fresh?** | Yes | Yes | **No** (stale since convoy-003) |

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

**Reads from:** target project files, carlos/.gt/memory/semantic.json, conductor/.gt/memory/semantic.json
**Writes to:** .gt/research/, .gt/memory/, scopecraft/, .gt/beads/, .gt/convoys/, scopecraft/.checkpoint.json
**Does not own:** Carlos analysis reports, Conductor state

**No changes since v2.5.0.**

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

**Reads from:** .gt/memory/semantic.json, .gt/beads/*.json, scopecraft/*.md
**Writes to:** scopecraft/*.md, quality gate results, analysis reports
**Does not own:** .gt/beads/, .gt/convoys/, conductor state

**No changes since v2.5.0.**

---

## Conductor Self-Report

**Source:** `~/github/habitusnet/conductor/.gt/memory/semantic.json`

| Attribute | Value | Actual (post convoy-003) |
|-----------|-------|--------------------------|
| Name | conductor | conductor |
| Status | alpha | alpha |
| Version | 0.1.0 | 0.1.0 |
| MCP tools | 22 (listed) | **26** (+4 new) |
| Detection types | 9 | **10** (+context_exhaustion) |
| Autonomous actions | 7 | **8** (+save_checkpoint_and_pause) |
| Bead consumption | "planned" | **implemented** (gt-k3m8n) |
| Context rollover | "planned" | **implemented** (gt-x9p4w) |
| Checkpoint schema | not mentioned | **implemented** (gt-w5y2c) |

**Reads from:** .gt/beads/*.json, .gt/convoys/*.json, .gt/memory/semantic.json, scopecraft/
**Writes to:** Task queue state, file locks, cost events, agent lifecycle, escalation queue
**Does not own:** .gt/ schema, scopecraft/ format, quality gate definitions, semantic memory generation

**Key change:** convoy-003 commit `d6b9426` adds 1804 lines across 18 files. Semantic.json needs refresh to reflect new capabilities.

---

## Ecosystem Role Comparison

All roles aligned. No conflicts.

| Responsibility | Lisa | Carlos | Conductor | Conflict? |
|----------------|------|--------|-----------|-----------|
| Pipeline ownership | Yes | No | No | None |
| Quality gate definition | Yes (gates.yaml v1.1) | Yes (gates.yaml v1.0) | No (overlay proposal) | None (M1 RESOLVED) |
| Reconciliation | Yes (ecosystem root) | Yes (project-level) | Yes (ecosystem-level) | OK: complementary |
| Bead/convoy creation | Yes | No | No | None |
| Bead consumption | No | No | **Yes** (NEW) | None (A17) |
| Context rollover | No | No | **Yes** (NEW) | None |
| Specialist analysis | No | Yes | No | None |

---

## Interface Agreement Check

| Interface | Lisa | Carlos | Conductor | Match? |
|-----------|------|--------|-----------|--------|
| gates.yaml | v1.1, canonical source | v1.0, Lisa-compatible | v1.1 overlay proposal | **FULL MATCH** |
| Bead schema | `gt-xxxxx` format | reads beads | **BeadSchema Zod** (imports) | **FULL MATCH** (A17) |
| Convoy schema | `convoy-NNN` format | N/A | **ConvoySchema Zod** (imports) | **FULL MATCH** (A17) |
| Checkpoint schema | `reconcile-checkpoint-v1` | N/A | `AgentCheckpointSchema` (different purpose) | OK: complementary |
| Heartbeat | N/A | N/A | Enhanced (+token tracking) | OK: backward compatible |

---

## Schema Divergence Note

All three projects now use `semantic-memory-v1` schema. No divergence.

Conductor's `AgentCheckpointSchema` (for runtime context rollover) is distinct from Lisa's `reconcile-checkpoint-v1` (for ecosystem state recovery). These serve different purposes and do not need to converge.

---

## Notable Changes From v2.5.0

1. **convoy-003 COMPLETE:** Conductor Ecosystem Integration — 3 beads done (gt-w5y2c, gt-k3m8n, gt-x9p4w).
2. **All 9 beads done:** 3/3 convoys complete. No pending work items.
3. **Q2 resolved:** Checkpoint schema — Hybrid SQLite + Bead File Updates.
4. **4 new MCP tools:** conductor_checkpoint, conductor_resume_from_checkpoint, conductor_import_beads, conductor_complete_bead.
5. **Enhanced heartbeat:** Now accepts tokenCount, tokenLimit, currentStage for context exhaustion warning.
6. **Context exhaustion detection:** New observer pattern + decision rule + checkpoint-and-pause action.
7. **Bead import pipeline:** Conductor reads .gt/beads/ and .gt/convoys/, maps to internal tasks, syncs status back.
8. **48 new tests:** checkpoint-handler (5), context-exhaustion-detector (11), rules (2), sqlite-checkpoints (18), plus existing tests verified.
9. **G7 identified:** Conductor semantic.json stale — needs /lisa:discover refresh.
