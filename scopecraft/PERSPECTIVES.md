# Ecosystem Perspectives

Aggregated self-reports from each plugin's `.gt/memory/semantic.json`, compared side-by-side.

**Generated:** 2026-02-09 (reconcile v4.0.0 — Conductor GA)
**Data source:** Local filesystem (all projects cloned)
**Projects scanned:** 3 attempted, 3 found (all local)
**Reconcile method:** Lisa Stage 5 skill (full re-scan)

---

## Project Status Matrix

| Field | Lisa | Carlos | Conductor |
|-------|------|--------|-----------|
| **Status** | Found (local) | Found (local) | Found (local) |
| **Version** | 0.3.0 | 1.2.0 | **1.0.0** |
| **Stage** | alpha | beta | **ga** |
| **Type** | claude-code-plugin | claude-code-plugin | framework (monorepo) |
| **Language** | Python | Python | TypeScript |
| **Schema** | semantic-memory-v1 | semantic-memory-v1 | semantic-memory-v1 |
| **Last scan** | 2026-02-08T19:00 | 2026-02-09T12:00 | **2026-02-09T14:45** |
| **License** | MIT | MIT | MIT |
| **gates.yaml** | Yes (v1.1, 31 gates, 5 stages) | Yes (v1.0, 9 gates) | Yes (v1.1, ecosystem overlay) |
| **Own reconcile** | Yes (this report) | Yes (Cycle 4) | Yes (Cycle 7) |
| **semantic.json fresh?** | Yes | Yes | **Yes** (GA refresh) |

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

| Attribute | Value | Change from v3.6.3 |
|-----------|-------|---------------------|
| Name | carlos | — |
| Role | specialist-fixer | — |
| Version | 1.2.0 | — |
| LOC | **11,422** | — |
| Tests | **482** + 95 security | Was 448 (corrected in 09b9274) |
| Quality gates | gates.yaml v1.0 (9 gates) | — |
| Discovery cache | 24h TTL from .gt/memory/semantic.json | — |
| Last scan | **2026-02-09T12:00** | — |
| Agent context tokens | **~1,500** | — |
| Convoy-007 | **COMPLETE (5/5 beads)** | — |
| Own reconcile | **Cycle 4** (2026-02-09) | Was Cycle 3 |

**Reads from:** .gt/memory/semantic.json, .gt/beads/*.json, scopecraft/*.md
**Writes to:** scopecraft/*.md, quality gate results, analysis reports
**Does not own:** .gt/beads/, .gt/convoys/, conductor state

### Carlos New Commits (since v3.6.3)

| Commit | Description |
|--------|-------------|
| 09b9274 | Test count corrected 448 → 482 in semantic.json and scopecraft docs |
| 2193f6e | Cycle 4 reconcile — full ecosystem, 98% alignment, all misalignments resolved |

---

## Conductor Self-Report

**Source:** `~/github/habitusnet/conductor/.gt/memory/semantic.json`

| Attribute | Value | Change from v3.6.3 |
|-----------|-------|---------------------|
| Name | conductor | — |
| Status | **ga** | Was alpha |
| Version | **1.0.0** | Was 0.1.0 |
| TypeScript | **5.9.3** | Was 5.7.2 |
| Turborepo | **2.8.3** | Was 2.3.3 |
| Next.js | **16.1.6** | Was 15.1.0 |
| Vitest | **4.0.18** | Was 4.0.16 |
| MCP tools | **24 listed** (4 categories) | Was 19 (5 categories) |
| Tests | **1,374** | Was ~1,100 (estimated) |
| Packages | **10** | — |
| Src files | **148** | Was 144 |
| Test files | **52** | Was 49 |
| Observer src | **26** | Was 28 |
| Dashboard src | **80** | Was 48 |
| Convoys | **5 complete** | Was 3 (eco-convoys only) |
| Beads | **22 total** (19 complete, 3 deferred) | Was 9 eco-beads only |
| Last scan | **2026-02-09T14:45** | Was 2026-02-09T13:00 |
| Own reconcile | **Cycle 7** | Was Cycle 3.1 |
| Deploy targets | **+Vercel** | Was Local/Neon/Firebase/Cloudflare |
| Security auth | **+Neon Auth for dashboard** | Was OAuth only |

**Reads from:** .gt/beads/*.json, .gt/convoys/*.json, .gt/memory/semantic.json, scopecraft/
**Writes to:** Task queue state, file locks, cost events, agent lifecycle, escalation queue
**Does not own:** .gt/ schema, scopecraft/ format, quality gate definitions, semantic memory generation

### Conductor MCP Tool Restructuring

Old categories (v3.6.3): task_management (4), coordination (5), access_control (4), cost_tracking (2), ecosystem (4) = 19

New categories (v4.0.0): task_management (8), coordination (7), oversight (5), ecosystem (4) = 24

| Category | New Tools | Notes |
|----------|-----------|-------|
| task_management | +conductor_start_task, +conductor_complete_task, +conductor_fail_task, +conductor_block_task | Full task lifecycle |
| coordination | +conductor_check_conflicts, +conductor_get_zones, +conductor_health_status | Zone-based isolation |
| oversight | NEW category: reassign_task, pause/resume_agent, escalate, broadcast | Autonomous oversight |
| ecosystem | unchanged | checkpoint, bead import |

**Note:** access_control tools (conductor_request_access, conductor_check_access, etc.) and cost_tracking tools (conductor_report_usage, conductor_get_budget) are not listed in the new semantic.json categories. Verified: conductor_request_access still exists in server.ts code — functional but uncategorized in self-report.

### Conductor Convoy Completion

| Convoy | Name | Status | Beads |
|--------|------|--------|-------|
| convoy-001 | Dashboard Core MVP | Complete | 6 |
| convoy-002 | E2B Sandbox Hardening | Complete | 3 |
| convoy-003 | Multi-Agent Hardening | Complete | 4 |
| convoy-004 | Multi-Tenancy & Oversight | Complete | 3 |
| convoy-005 | GA Launch Prep | Complete | 3 |

### Conductor New Capabilities (GA)

| Capability | Implementation |
|------------|----------------|
| Organization isolation | Multi-tenant data isolation, RBAC (gt-m4001) |
| Autonomy levels | full_auto, supervised, assisted, manual (gt-o5001) |
| Escalation queue | Priority-based system with dashboard (gt-o5002) |
| Zone-based isolation | File ownership boundaries, zone matching |
| Health monitoring | Heartbeat tracking, status thresholds |
| Task reassignment | Auto-reassignment on agent failure |
| Capability matching | Agent-task matching via capabilities |

---

## Ecosystem Role Comparison

All roles aligned. No conflicts.

| Responsibility | Lisa | Carlos | Conductor | Conflict? |
|----------------|------|--------|-----------|-----------|
| Pipeline ownership | Yes | No | No | None |
| Quality gate definition | Yes (gates.yaml v1.1) | Yes (gates.yaml v1.0) | No (overlay) | None |
| Reconciliation | Yes (ecosystem root) | Yes (project-level) | Yes (ecosystem-level) | OK: complementary |
| Bead/convoy creation | Yes | No | No | None |
| Bead consumption | No | No | **Yes** (GA) | None |
| Context rollover | No | No | **Yes** (GA) | None |
| Specialist analysis | No | Yes | No | None |
| Agent context budget | No | **Yes** (41% reduced) | TBD (cq-02) | Pending |
| **Organization isolation** | No | No | **Yes** (GA) | None |
| **Autonomous oversight** | No | No | **Yes** (GA) | None |
| **Zone-based coordination** | No | No | **Yes** (GA) | None |

---

## Interface Agreement Check

| Interface | Lisa | Carlos | Conductor | Match? |
|-----------|------|--------|-----------|--------|
| gates.yaml | v1.1, canonical source | v1.0, Lisa-compatible | v1.1 overlay | **FULL MATCH** |
| Bead schema | `gt-xxxxx` format | reads beads | **BeadSchema Zod** (imports) | **FULL MATCH** |
| Convoy schema | `eco-convoy-NNN` / `convoy-NNN` | N/A | **ConvoySchema Zod** (imports) | **FULL MATCH** |
| Checkpoint schema | `reconcile-checkpoint-v1` | N/A | `AgentCheckpointSchema` | OK: complementary |
| Heartbeat | N/A | N/A | Enhanced (+token tracking) | OK: backward compatible |
| Agent context | N/A | **~1,500 tokens** | TBD (cq-02) | **Pending** (non-blocking) |
| Agent registration | N/A | **conductor_request_access()** | Tool exists in code | **FULL MATCH** |
| Model routing | N/A | **Carlos owns model_router.py** | Consumes via metadata.modelTier | **FULL MATCH** |
| Ecosystem metadata | N/A | **get_ecosystem_metadata()** | Reads metadata.modelTier | **FULL MATCH** |
| **MCP task lifecycle** | N/A | N/A | **8 tools** (claim→complete/fail) | New in GA |
| **Oversight tools** | N/A | N/A | **5 tools** (reassign, escalate) | New in GA |

---

## Schema Divergence Note

All three projects use `semantic-memory-v1` schema. No divergence.

Conductor's `AgentCheckpointSchema` (for runtime context rollover) is distinct from Lisa's `reconcile-checkpoint-v1` (for ecosystem state recovery). These serve different purposes and do not need to converge.

---

## Notable Changes From v3.6.3

1. **Conductor GA (v1.0.0):** alpha → ga. 5 convoys complete, 1,374 tests, 24 MCP tools, v1.0.0 tag published.
2. **Conductor MCP restructured:** task_management expanded (4→8), coordination expanded (5→7), new oversight category (5 tools). Access control and cost tracking not separately categorized.
3. **Conductor new capabilities:** organization isolation, autonomy levels, escalation queue, zone-based coordination, health monitoring, task reassignment, capability matching.
4. **Conductor tech stack upgrades:** TypeScript 5.9.3, Turborepo 2.8.3, Next.js 16.1.6, Vitest 4.0.18, +Vercel deployment.
5. **Carlos test count corrected:** 448 → 482 (commit 09b9274). Cycle 4 project reconcile completed (2193f6e).
6. **21 new Conductor commits** since last reconcile (a9bca30..1fdaebf).
