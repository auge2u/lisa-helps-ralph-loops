# Ecosystem Perspectives

Aggregated self-reports from each plugin's `.gt/memory/semantic.json`, compared side-by-side.

**Generated:** 2026-02-06
**Projects scanned:** 3 attempted, 2 found, 1 missing

---

## Project Status Matrix

| Field | Lisa | Carlos | Conductor |
|-------|------|--------|-----------|
| **Status** | Found | Found | MISSING (repo does not exist) |
| **Version** | 0.3.0 | 1.2.0 | N/A |
| **Stage** | alpha | beta | pre-development |
| **Type** | claude-code-plugin | claude-code-plugin | N/A |
| **Language** | Python | Python | N/A |
| **Last scan** | 2026-02-06 | 2026-02-06 | N/A |

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
| Skills | 4 (research, discover, plan, structure) |
| Quality gates | 22 across 4 stages |
| Gate source | gates.yaml (declarative) |

**Reads from:** target project files, carlos semantic.json, conductor semantic.json
**Writes to:** .gt/research/, .gt/memory/, scopecraft/, .gt/beads/, .gt/convoys/, .checkpoint.json, ALIGNMENT_REPORT.md
**Does not own:** Carlos analysis reports, Conductor state

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
| Python modules | 13 (10,655 LOC) |
| Tests | 400 (6,621 LOC) + 94 security tests |
| Quality gates | 6 blockers (hardcoded in validate_quality_gates.py) |

**Reads from:** .gt/memory/semantic.json, .gt/beads/*.json, scopecraft/*.md
**Writes to:** scopecraft/*.md, quality gate results, analysis reports
**Does not own:** .gt/beads/, .gt/convoys/, conductor state

**Additional capabilities:**
- Multi-agent workflow: ingest_scope -> [tech_audit, market_fit_audit] -> synthesis
- Model routing: haiku/sonnet/opus tiers targeting 60-70% savings
- Discovery engine: detects 10 package managers, 8 frameworks, 6 databases, 4 CI systems

---

## Conductor Self-Report

**Source:** `~/github/habitusnet/conductor/.gt/memory/semantic.json`

**STATUS: MISSING** — The conductor repo does not exist at `~/github/habitusnet/conductor/`.

**Expected role (from ecosystem architecture doc):**
- Orchestration & Oversight
- Multi-project awareness
- Agent lifecycle management (heartbeat, reassignment, handoff)
- Context exhaustion detection and rollover
- Personality curation
- Conflict resolution
- MCP tools: conductor_claim_task, conductor_complete_task, conductor_heartbeat, conductor_lock_file

---

## Ecosystem Role Comparison

| Responsibility | Lisa claims | Carlos claims | Conductor expected | Conflict? |
|----------------|-------------|---------------|-------------------|-----------|
| Pipeline ownership | Yes | No | No | None |
| .gt/ schema ownership | Yes | No (reads only) | No (reads only) | None |
| Semantic memory | Yes (generates) | Yes (reads) | Expected (reads) | None |
| Bead/convoy creation | Yes | No | No | None |
| Quality gate definition | Yes (gates.yaml) | Yes (hardcoded) | No | MISALIGNMENT: dual source |
| Quality gate enforcement | Yes (validate.py) | Yes (validate_quality_gates.py) | Expected (routes to Carlos) | MISALIGNMENT: dual enforcement |
| Roadmap generation | Yes (plan stage) | Yes (roadmap command) | No | OK: complementary |
| scopecraft/ output | Yes (writes) | Yes (writes) | No | OK: shared format |
| Discovery engine | Yes (skill-based) | Yes (Python-based, richer) | No | OK: Carlos enriches |
| Model routing | No | Yes (model_router.py) | Expected | None |
| Agent tracking | No | No | Expected | None |
| Context rollover | No | No | Expected | None |
| Reconciliation | Yes (ecosystem root) | No | No | None |

---

## Interface Agreement Check

| Interface | Lisa says | Carlos says | Match? |
|-----------|-----------|-------------|--------|
| `.gt/memory/semantic.json` | "I write, others read" | "I read if exists, skip re-discovery" | Yes |
| `scopecraft/` | "Stage 2 output" | "Roadmap output (shared format)" | Yes |
| `gates.yaml` | "Single source of truth (22 gates)" | "Should align with Lisa gates.yaml" | PARTIAL: Carlos acknowledges but hasn't aligned yet |
| `.gt/beads/*.json` | "Stage 3 output, I own" | "I read to validate/analyze" | Yes |
| `ecosystem_root` | "This repo" | "lisa3 (hosts reconcile)" | Yes |
