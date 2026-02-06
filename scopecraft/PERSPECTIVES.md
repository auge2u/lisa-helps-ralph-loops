# Ecosystem Perspectives

Aggregated self-reports from each plugin's `.gt/memory/semantic.json`, compared side-by-side.

**Generated:** 2026-02-06 (reconcile v2.2.0)
**Projects scanned:** 3 attempted, 3 found (all local)
**Reconcile method:** Lisa Stage 5 skill

---

## Project Status Matrix

| Field | Lisa | Carlos | Conductor |
|-------|------|--------|-----------|
| **Status** | Found (local) | Found (local) | Found (local) |
| **Version** | 0.3.0 | 1.2.0 | 0.1.0 |
| **Stage** | alpha | beta | early-development |
| **Type** | claude-code-plugin | claude-code-plugin | framework (monorepo) |
| **Language** | Python | Python | TypeScript |
| **Schema** | semantic-memory-v1 | semantic-memory-v1 | semantic-memory-v1 |
| **Last scan** | 2026-02-06 | 2026-02-06 | 2026-02-06 |
| **License** | MIT | MIT | MIT |

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

---

## Carlos Self-Report

**Source:** `~/github/auge2u/carlos/.gt/memory/semantic.json`

| Attribute | Value |
|-----------|-------|
| Name | carlos |
| Role | specialist-fixer |
| Description | Called in for focused analysis tasks. Small context, sharp focus. |
| Standalone command | `/carlos:roadmap` |
| Ecosystem root | No (lisa3 hosts) |
| Commands | 4 (roadmap, roadmap-orchestrated, verify, check-imports) |
| Agents | 3 (product-owner/opus, tech-auditor/sonnet, market-fit-auditor/sonnet) |
| Skills | 1 (roadmap-scopecraft) |
| Python modules | 14 (10,655 LOC) |
| Tests | 401 (7,686 LOC) + 95 security tests |
| Quality gates | 6 blockers (hardcoded in validate_quality_gates.py) |

**Reads from:** .gt/memory/semantic.json, .gt/beads/*.json, scopecraft/*.md
**Writes to:** scopecraft/*.md, quality gate results, analysis reports
**Does not own:** .gt/beads/, .gt/convoys/, conductor state

**Additional capabilities:**
- Multi-agent workflow: ingest_scope -> [tech_audit, market_fit_audit] -> synthesis
- Model routing: haiku/sonnet/opus tiers targeting 60-70% savings
- Discovery engine: detects 10 package managers, 8 frameworks, 6 databases, 4 CI systems
- Security: CWE-22 path traversal, CWE-1333 ReDoS, CWE-78 shell injection protections

---

## Conductor Self-Report

**Source:** `~/github/habitusnet/conductor/.gt/memory/semantic.json`

| Attribute | Value |
|-----------|-------|
| Name | conductor |
| Role | orchestration-and-oversight |
| Description | Multi-project, multi-agent tracking for CLI-based agents. Handles task assignment, context rollover, conflict resolution, personality curation, and autonomous oversight. |
| Standalone command | conductor CLI + MCP server |
| Ecosystem root | No (lisa3 hosts) |
| Packages | 10 (core, state, db, secrets, mcp-server, connectors, cli, e2b-runner, observer, dashboard) |
| Total src files | 148 |
| Total test files | 51 |
| Total tests | 1,100 |
| MCP tools | 19 (8 task management + 5 coordination + 6 oversight) |
| Observer patterns | 9 detection types, 4 autonomy levels, 7 autonomous actions |
| LLM providers | 4 (Anthropic, Google, OpenAI, Z.ai) |
| Supported agents | 6 (Claude Opus/Sonnet/Haiku, Gemini Flash, Codex, GPT-4o) |

**Reads from:** .gt/beads/*.json, .gt/convoys/*.json, .gt/memory/semantic.json, scopecraft/
**Writes to:** Task queue state, file locks, cost events, agent lifecycle state, escalation queue
**Does not own:** .gt/ directory schema, scopecraft/ format, quality gate definitions, semantic memory generation, specialist analysis

**Key patterns:**
- CLI-First: Subscription-based CLI tools are primary workers, not API orchestration
- MCP Coordination: All agents connect via MCP for task/lock/heartbeat management
- Oversight Agent: Dedicated CLI-based observer monitors others with pattern detection
- API Fallback: API orchestration only for emergencies
- Two DB layers: SQLite (simple) + Drizzle ORM (production PostgreSQL)

**Constraints:** CLI-first (not API orchestrator), subscription-based billing, self-coordinating agents, Node.js >= 20.0.0, ESM only

---

## Ecosystem Role Comparison

| Responsibility | Lisa claims | Carlos claims | Conductor claims | Conflict? |
|----------------|-------------|---------------|------------------|-----------|
| Pipeline ownership | Yes | No | No | None |
| .gt/ schema ownership | Yes | No (reads only) | No (reads only, explicitly disowns) | None |
| Semantic memory | Yes (generates) | Yes (reads) | Yes (reads for context bundles) | None |
| Bead/convoy creation | Yes | No | No (reads for task assignment) | None |
| Quality gate definition | Yes (gates.yaml) | Yes (hardcoded) | No (disowns) | **M1: Dual source** |
| Quality gate enforcement | Yes (validate.py) | Yes (validate_quality_gates.py) | No | **M1: Dual enforcement** |
| Roadmap generation | Yes (plan stage) | Yes (roadmap command) | No | OK: complementary |
| scopecraft/ output | Yes (writes) | Yes (writes) | Yes (reads) | OK: shared format |
| Discovery engine | Yes (skill-based) | Yes (Python-based, richer) | No | OK: Carlos enriches |
| Model routing | No | Yes (model_router.py) | No | None |
| Agent tracking | No | No | Yes (full lifecycle) | None |
| Task management | No | No | Yes (MCP tools) | None |
| Context rollover | No | No | Planned (roadmap_status) | None |
| File locking | No | No | Yes (TTL-based) | None |
| E2B sandbox | No | No | Yes | None |
| Conflict resolution | No | No | Yes (zone, lock, merge, review strategies) | None |
| Autonomous oversight | No | No | Yes (observer agent) | None |
| Reconciliation | Yes (ecosystem root) | No | No | None |
| Secrets management | No | No | Yes (multi-provider) | None |
| Personality curation | No | No | Yes (maps tasks to agent tiers) | None |

---

## Interface Agreement Check

| Interface | Lisa says | Carlos says | Conductor says | Match? |
|-----------|-----------|-------------|----------------|--------|
| `.gt/memory/semantic.json` | "I write, others read" | "I read if exists" | "I read for context bundles" | **FULL MATCH** |
| `scopecraft/` | "Stage 2 output" | "Roadmap output (shared)" | "I read for roadmap context" | **FULL MATCH** |
| `gates.yaml` | "Single source of truth" | "Should align" | "Does not own" | **PARTIAL**: Carlos acknowledges but hasn't aligned |
| `.gt/beads/*.json` | "Stage 3 output, I own" | "I read to validate" | "I read for task assignment" | **FULL MATCH** |
| `.gt/convoys/*.json` | "Stage 3 output, I own" | Not explicitly referenced | "I read for task assignment" | **FULL MATCH** |
| `ecosystem_root` | "This repo" | "lisa3 (hosts reconcile)" | "lisa3 (hosts reconcile)" | **FULL MATCH** |
| MCP tools | Not referenced | Not referenced | Yes (19 tools) | OK: Conductor's domain |
| Task queue | Not referenced | Not referenced | Yes (full workflow) | OK: Conductor's domain |
| File locks | Not referenced | Not referenced | Yes (TTL-based) | OK: Conductor's domain |
| Agent personas | Not referenced | "Can be called as specialist" | "Routes to Carlos personas" | **FULL MATCH** (Carlos <> Conductor) |

---

## Roadmap Status Comparison

| Area | Lisa | Carlos | Conductor |
|------|------|--------|-----------|
| Core functionality | Stages 0-3 implemented, Stage 5 implemented | All commands working | Core, DB, MCP, CLI, connectors, observer, secrets done |
| In progress | — | — | Dashboard UI |
| Planned / Next | Templates for reconcile outputs, formal gates.yaml for Stage 5 | gates.yaml alignment | WebSocket notifications, auction system, Lisa bead consumption, Carlos specialist routing, context rollover |

---

## Work Structure (NEW in v2.2.0)

Lisa Stage 3 (structure) extracted 9 beads across 3 convoys covering all remaining ecosystem work:

| Convoy | Owner | Beads | Phase | Est. Days |
|--------|-------|-------|-------|-----------|
| convoy-001: Lisa Pipeline Hardening | Lisa | 4 (gate fix, reconcile templates, checkpoint schema, reconcile gates) | 1-2 | 3 |
| convoy-002: Carlos Interface Alignment | Carlos | 2 (.gt/ state reading, gates.yaml M1 resolution) | 2 | 5 |
| convoy-003: Conductor Ecosystem Integration | Conductor | 3 (checkpoint spike, bead/convoy reading, context rollover) | 3 | 14 |

**Pipeline status:** discover (Stage 1) + plan (Stage 2) + structure (Stage 3) + reconcile (Stage 5) — all operational.

---

## Notable Changes From v1.1.0

1. **Conductor growth**: 8 packages -> 10 packages (added observer, secrets). 148 src files, 1,100 tests. Significant maturation.
2. **Schema unification**: All three projects now use `semantic-memory-v1`. Direct comparison is fully possible.
3. **Ecosystem awareness**: All three projects now declare ecosystem_role, integration_points, non_goals. The "who reads what" chain is complete.
4. **Lisa Stage 5**: Reconcile pipeline fully operational. Lisa `semantic.json` now reflects Stage 5 in skills, pipeline, and agent stages.
5. **Lisa Stage 3**: 9 beads + 3 convoys extracted. All remaining work items structured with acceptance criteria and dependencies.
