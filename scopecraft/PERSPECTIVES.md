# Ecosystem Perspectives

Aggregated self-reports from each plugin's `.gt/memory/semantic.json`, compared side-by-side.

**Generated:** 2026-02-06 (reconcile v2.3.0)
**Data source:** Git remote (fresh pull from Carlos and Conductor)
**Projects scanned:** 3 attempted, 3 found (all local)
**Reconcile method:** Lisa Stage 5 skill

---

## Project Status Matrix

| Field | Lisa | Carlos | Conductor |
|-------|------|--------|-----------|
| **Status** | Found (local) | Found (pulled) | Found (pulled) |
| **Version** | 0.3.0 | 1.2.0 | 0.1.0 |
| **Stage** | alpha | beta | **alpha** (was early-development) |
| **Type** | claude-code-plugin | claude-code-plugin | framework (monorepo) |
| **Language** | Python | Python | TypeScript |
| **Schema** | semantic-memory-v1 | semantic-memory-v1 | semantic-memory-v1 |
| **Last scan** | 2026-02-06T18:00 | **2026-02-06T19:00** (rescanned) | 2026-02-06T12:00 |
| **License** | MIT | MIT | MIT |
| **gates.yaml** | Yes (v1.0, 22 gates) | **Yes (v1.0, 9 gates)** (NEW) | Yes (v1.1, ecosystem overlay) |
| **Own reconcile** | Yes (this report) | **Yes** (project-level) | **Yes** (ecosystem-level) |

---

## Lisa Self-Report

**Source:** `~/github/auge2u/lisa3/.gt/memory/semantic.json`

| Attribute | Value |
|-----------|-------|
| Name | lisa |
| Role | pipeline-and-memory |
| Description | Owns staged pipeline (research, discover, plan, structure, reconcile) and .gt/ directory schema. Ecosystem root. |
| Standalone command | `/lisa:migrate` |
| Ecosystem root | Yes (hosts reconcile and ecosystem scopecraft/) |
| Commands | 8 (research, discover, plan, structure, status, migrate, rescue, reconcile) |
| Agents | 2 (archaeologist, migrator) |
| Skills | 5 (research, discover, plan, structure, reconcile) |
| Quality gates | 22 across 4 stages |
| Gate source | gates.yaml (declarative) |

**Reads from:** target project files, Carlos semantic.json, Conductor semantic.json
**Writes to:** .gt/research/, .gt/memory/, scopecraft/, .gt/beads/, .gt/convoys/, .checkpoint.json, ALIGNMENT_REPORT.md
**Does not own:** Carlos analysis reports, Conductor state

**Constraints:** Works offline, local files only, Python 3.10+, graceful degradation when partners absent, output directories restricted to `.`, `.gt`, `scopecraft`

**Unchanged since:** v2.2.0

---

## Carlos Self-Report

**Source:** `~/github/auge2u/carlos/.gt/memory/semantic.json` (pulled from remote)

| Attribute | Value | Change from v2.2.0 |
|-----------|-------|---------------------|
| Name | carlos | — |
| Role | specialist-fixer | — |
| Version | 1.2.0 | — |
| Standalone command | `/carlos:roadmap` | — |
| Commands | 4 (roadmap, roadmap-orchestrated, verify, check-imports) | — |
| Agents | 3 (product-owner/opus, tech-auditor/sonnet, market-fit-auditor/sonnet) | — |
| Skills | 1 (roadmap-scopecraft) | — |
| Python modules | 14 | — |
| **LOC** | **11,200** | was 10,655 (+545) |
| **Tests** | **435** (8,240 LOC) + 95 security | was 401 (+34) |
| **Quality gates** | **gates.yaml v1.0 + validate_quality_gates.py** | was hardcoded only |
| **Gate loading** | **gates.yaml > ralph.yml > DEFAULT_GATES** | NEW |
| **Discovery cache** | **24h TTL from .gt/memory/semantic.json** | NEW |

**Reads from:** .gt/memory/semantic.json (with caching), .gt/beads/*.json, scopecraft/*.md
**Writes to:** scopecraft/*.md, quality gate results, analysis reports
**Does not own:** .gt/beads/, .gt/convoys/, conductor state

**Key changes since v2.2.0:**
- `plugins/carlos/gates.yaml` created — Lisa-compatible schema (gt-cg7ya)
- `DiscoveryEngine.discover()` checks `.gt/memory/semantic.json` freshness before full scan (gt-r6d2k)
- `test_gates_yaml.py` + `test_discovery_cache.py` added (34 new tests)
- Carlos ran its own project-level reconcile producing `scopecraft/ALIGNMENT_REPORT.md`

---

## Conductor Self-Report

**Source:** `~/github/habitusnet/conductor/.gt/memory/semantic.json` (pulled from remote)

| Attribute | Value | Change from v2.2.0 |
|-----------|-------|---------------------|
| Name | conductor | — |
| Role | orchestration-and-oversight | — |
| Version | 0.1.0 | — |
| **Status** | **alpha** | was early-development |
| Standalone command | conductor CLI + MCP server | — |
| Packages | 10 | — |
| Total src files | 148 | — |
| Total test files | 51 | — |
| Total tests | 1,100 | — |
| MCP tools | 19 (8 task + 5 coordination + 6 oversight) | — |
| LLM providers | 4 (Anthropic, Google, OpenAI, Z.ai) | — |
| **scopecraft/** | **NEW** — alignment report, gates.yaml draft, perspectives, checkpoint | was not present |

**Reads from:** .gt/beads/*.json, .gt/convoys/*.json, .gt/memory/semantic.json, scopecraft/
**Writes to:** Task queue state, file locks, cost events, agent lifecycle state, escalation queue
**Does not own:** .gt/ directory schema, scopecraft/ format, quality gate definitions, semantic memory generation, specialist analysis

**Key changes since v2.2.0:**
- `project.status` changed to `alpha` (was `early-development`)
- Created own `scopecraft/` with alignment report (finding Carlos 72% aligned, Conductor 91%)
- Created `scopecraft/gates.yaml` draft (v1.1) — extends Lisa's gates.yaml with reconcile stage + Carlos enrichments
- Raised 4 open queries (OQ-1 through OQ-4) — see Alignment Report for cross-references
- Phase 0 now ~90% complete per own assessment

---

## Ecosystem Role Comparison

| Responsibility | Lisa claims | Carlos claims | Conductor claims | Conflict? |
|----------------|-------------|---------------|------------------|-----------|
| Pipeline ownership | Yes | No | No | None |
| .gt/ schema ownership | Yes | No (reads only) | No (reads only, explicitly disowns) | None |
| Semantic memory | Yes (generates) | Yes (reads, **now caches**) | Yes (reads for context bundles) | None |
| Bead/convoy creation | Yes | No | No (reads for task assignment) | None |
| Quality gate definition | Yes (gates.yaml) | **Yes (gates.yaml v1.0)** | No (disowns, but drafted ecosystem overlay) | **None (was M1, RESOLVED)** |
| Quality gate enforcement | Yes (validate.py) | Yes (validate_quality_gates.py, **now reads gates.yaml**) | No | **None (was M1, RESOLVED)** |
| Roadmap generation | Yes (plan stage) | Yes (roadmap command) | No | OK: complementary |
| scopecraft/ output | Yes (writes) | Yes (writes) | Yes (reads) | OK: shared format |
| Discovery engine | Yes (skill-based) | Yes (Python-based, richer, **now with cache**) | No | OK: Carlos enriches |
| Model routing | No | Yes (model_router.py) | No | None |
| Agent tracking | No | No | Yes (full lifecycle) | None |
| Task management | No | No | Yes (MCP tools) | None |
| Context rollover | No | No | Planned (roadmap_status) | None |
| File locking | No | No | Yes (TTL-based) | None |
| Reconciliation | Yes (ecosystem root) | Yes (project-level) | Yes (ecosystem-level) | OK: complementary |
| Secrets management | No | No | Yes (multi-provider) | None |

---

## Interface Agreement Check

| Interface | Lisa says | Carlos says | Conductor says | Match? |
|-----------|-----------|-------------|----------------|--------|
| `.gt/memory/semantic.json` | "I write, others read" | "I read if exists, **cache if fresh**" | "I read for context bundles" | **FULL MATCH** |
| `scopecraft/` | "Stage 2 output" | "Roadmap output (shared)" | "I read for roadmap context" | **FULL MATCH** |
| `gates.yaml` | "Single source of truth" | **"Lisa-compatible v1.0"** | "Extends Lisa's format (v1.1 overlay)" | **FULL MATCH (was PARTIAL)** |
| `.gt/beads/*.json` | "Stage 3 output, I own" | "I read to validate" | "I read for task assignment" | **FULL MATCH** |
| `.gt/convoys/*.json` | "Stage 3 output, I own" | Not explicitly referenced | "I read for task assignment" | **FULL MATCH** |
| `ecosystem_root` | "This repo" | "lisa3 (hosts reconcile)" | "lisa3 (hosts reconcile)" | **FULL MATCH** |
| MCP tools | Not referenced | Not referenced | Yes (19 tools) | OK: Conductor's domain |
| Agent personas | Not referenced | "Can be called as specialist" | "Routes to Carlos personas" | **FULL MATCH** (Carlos <> Conductor) |

---

## Roadmap Status Comparison

| Area | Lisa | Carlos | Conductor |
|------|------|--------|-----------|
| Core functionality | Stages 0-3,5 all implemented | All commands working, gates.yaml aligned, discovery cache active | Core, DB, MCP, CLI, connectors, observer, secrets done |
| In progress | — | — | Dashboard UI, Phase 0 ~90% |
| Completed this cycle | — | **convoy-002 (gt-cg7ya, gt-r6d2k)** | Status upgrade to alpha, own reconcile |
| Planned / Next | convoy-001 (pipeline hardening) | Carlos semantic.json refresh, remaining ecosystem steps 6-8 | convoy-003 (now unblocked), Phase 1 (Dashboard MVP) |

---

## Cross-Project Reconcile Comparison

All three projects have now run reconcile. Comparing findings:

| Finding | Lisa (this report) | Carlos (own report) | Conductor (own report) |
|---------|-------------------|--------------------|-----------------------|
| M1 (gates.yaml) | **Resolved** | **Resolved** (claims done) | Flags as gap (stale view) |
| Carlos alignment | High (gates.yaml aligned) | M3: semantic.json stale | 72% (stale artifacts) |
| Conductor alignment | Alpha, reconcile present | N/A | 91% (roadmap status stale) |
| Lisa3 existence | IS this repo | References as pipeline owner | **OQ-2: thinks missing** (incorrect) |
| Convoy naming | **M5: collision flagged** | **M4: collision flagged** | N/A |

**Convergence:** Lisa and Carlos agree on key findings. Conductor has a stale view of Carlos (pre-Convoy-002) and doesn't realize Lisa3 exists. Next Conductor reconcile should clear these.

---

## Notable Changes From v2.2.0

1. **M1 resolved:** The longest-standing ecosystem misalignment (quality gate dual source) is now fixed. All three projects have gates.yaml files.
2. **First convoy completed:** convoy-002 (Carlos Interface Alignment) is the first ecosystem convoy to be fully implemented.
3. **convoy-003 unblocked:** Conductor Ecosystem Integration can now proceed.
4. **Cross-project reconcile:** All three projects have independently performed reconciliation. Findings converge, with Conductor's view being slightly stale.
5. **Conductor maturation:** Status upgraded to alpha, created own ecosystem-level reconcile with shared gates.yaml draft.
6. **Carlos growth:** 435 tests (+34), 11,200 LOC (+545), two new features (gates.yaml loading, discovery cache).
