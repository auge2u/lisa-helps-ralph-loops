# Ecosystem Perspectives

Aggregated self-reports from each plugin's `.gt/memory/semantic.json`, compared side-by-side.

**Generated:** 2026-02-08 (reconcile v3.3.0)
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
| **Last scan** | **2026-02-08T19:00** | **2026-02-08T12:00** | **2026-02-08T14:00** |
| **License** | MIT | MIT | MIT |
| **gates.yaml** | Yes (v1.1, 31 gates, 5 stages) | Yes (v1.0, 9 gates) | Yes (v1.1, ecosystem overlay) |
| **Own reconcile** | Yes (this report, v3.3.0) | Yes (project-level, Cycle 3) | Yes (Cycle 3.1) |
| **semantic.json fresh?** | Yes | **Yes** (refreshed 2026-02-08) | **Yes** (refreshed 2026-02-08) |

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

**No changes since v3.1.0.**

---

## Carlos Self-Report

**Source:** `~/github/auge2u/carlos/.gt/memory/semantic.json`

| Attribute | Value | Change from v3.1.0 |
|-----------|-------|---------------------|
| Name | carlos | — |
| Role | specialist-fixer | — |
| Version | 1.2.0 | — |
| LOC | **11,022** | Was 11,200 (-178) |
| Tests | 435 + 95 security | — |
| Quality gates | gates.yaml v1.0 (9 gates) | — |
| Discovery cache | 24h TTL from .gt/memory/semantic.json | — |
| Last scan | **2026-02-08T12:00** | Was 2026-02-06T19:00 |
| Agent context tokens | **~1,500** | Was ~2,521 (41% reduction) |
| Convoy-007 | **60% (3/5 beads)** | Was 40% (2/5) |
| Commits | **61** | Was ~54 |

**Reads from:** .gt/memory/semantic.json, .gt/beads/*.json, scopecraft/*.md
**Writes to:** scopecraft/*.md, quality gate results, analysis reports
**Does not own:** .gt/beads/, .gt/convoys/, conductor state

### Carlos Convoy-007 (Project-Level)

| Bead | Title | Status | Step |
|------|-------|--------|------|
| gt-cg7ya | gates.yaml in Lisa-compatible schema | Complete | 4 |
| gt-r6d2k | Discovery cache via .gt/ freshness | Complete | 5 |
| gt-eco02 | **Agent context footprint -41%** | **Complete** | **7** |
| gt-eco01 | MCP agent registration | Planned (blocked: cq-01) | 6 |
| gt-eco03 | Ecosystem model router | Planned (blocked: cq-03) | 8 |

---

## Conductor Self-Report

**Source:** `~/github/habitusnet/conductor/.gt/memory/semantic.json`

| Attribute | Value | Change from v3.2.0 |
|-----------|-------|---------------------|
| Name | conductor | — |
| Status | alpha | — |
| Version | 0.1.0 | — |
| MCP tools | **19** (verified) | Was 22 (inaccurate) — corrected to match codebase |
| Detection types | **10** | Was 9 (+context_exhaustion) |
| Autonomous actions | **8** | Was 7 (+save_checkpoint_and_pause) |
| Bead consumption | **implemented** (gt-k3m8n) | Was "planned" in semantic.json |
| Context rollover | **implemented** (gt-x9p4w) | Was "planned" in semantic.json |
| Checkpoint schema | **implemented** (gt-w5y2c) | Was missing from semantic.json |
| Last scan | **2026-02-08T14:00** | Was 2026-02-06T12:00 (stale) |
| Observer src_files | **28** | Was 26 (+2 convoy-003) |
| Dashboard src_files | **48** | Was 80 (corrected) |

**Reads from:** .gt/beads/*.json, .gt/convoys/*.json, .gt/memory/semantic.json, scopecraft/
**Writes to:** Task queue state, file locks, cost events, agent lifecycle, escalation queue
**Does not own:** .gt/ schema, scopecraft/ format, quality gate definitions, semantic memory generation

**Conductor semantic.json refreshed** (2026-02-08T14:00): MCP tools corrected to 19 (was 22), convoy-003 capabilities reflected in completed roadmap items, package file counts corrected. G7 RESOLVED. Checkpoint updated to v3.3.0/Cycle 3.1.

---

## Ecosystem Role Comparison

All roles aligned. No conflicts.

| Responsibility | Lisa | Carlos | Conductor | Conflict? |
|----------------|------|--------|-----------|-----------|
| Pipeline ownership | Yes | No | No | None |
| Quality gate definition | Yes (gates.yaml v1.1) | Yes (gates.yaml v1.0) | No (overlay proposal) | None (M1 RESOLVED) |
| Reconciliation | Yes (ecosystem root) | Yes (project-level) | Yes (ecosystem-level) | OK: complementary |
| Bead/convoy creation | Yes | No | No | None |
| Bead consumption | No | No | **Yes** | None (A17) |
| Context rollover | No | No | **Yes** | None |
| Specialist analysis | No | Yes | No | None |
| Agent context budget | No | **Yes** (41% reduced) | TBD (cq-02) | Pending confirmation |

---

## Interface Agreement Check

| Interface | Lisa | Carlos | Conductor | Match? |
|-----------|------|--------|-----------|--------|
| gates.yaml | v1.1, canonical source | v1.0, Lisa-compatible | v1.1 overlay proposal | **FULL MATCH** |
| Bead schema | `gt-xxxxx` format | reads beads | **BeadSchema Zod** (imports) | **FULL MATCH** (A17) |
| Convoy schema | `eco-convoy-NNN` (ecosystem) / `convoy-NNN` (project) | N/A | **ConvoySchema Zod** (imports) | **FULL MATCH** (A17) |
| Checkpoint schema | `reconcile-checkpoint-v1` | N/A | `AgentCheckpointSchema` (different purpose) | OK: complementary |
| Heartbeat | N/A | N/A | Enhanced (+token tracking) | OK: backward compatible |
| Agent context | N/A | **~1,500 tokens (3 agents)** | TBD (cq-02) | **Pending** |

---

## Schema Divergence Note

All three projects use `semantic-memory-v1` schema. No divergence.

Conductor's `AgentCheckpointSchema` (for runtime context rollover) is distinct from Lisa's `reconcile-checkpoint-v1` (for ecosystem state recovery). These serve different purposes and do not need to converge.

---

## Notable Changes From v3.2.0

1. **Conductor semantic.json refreshed:** 2026-02-08T14:00, G7 RESOLVED. MCP tools corrected 22→19, convoy-003 capabilities moved from planned to completed.
2. **Conductor alignment:** 94%→96% (+2, semantic.json fresh + tools corrected).
3. **All semantic.json files now fresh:** Lisa (2026-02-06T18:00), Carlos (2026-02-08T12:00), Conductor (2026-02-08T14:00).
4. **0 gaps remaining:** All misalignments and gaps resolved ecosystem-wide.
5. **Conductor checkpoint:** v3.3.0/Cycle 3.1, reflects discovery refresh.

### Previous Notable Changes (v3.2.0)

1. Carlos gt-eco02 complete: agent context footprint reduced 41% (287→119 lines, ~2,521→~1,500 tokens).
2. Carlos scan refreshed: 2026-02-08T12:00, LOC corrected to 11,022.
3. A18 added: Agent context budget alignment confirmed.
4. Carlos→Conductor questions surfaced: cq-01 (MCP format), cq-02 (context budget), cq-03 (model routing).
