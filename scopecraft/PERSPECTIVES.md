# Ecosystem Perspectives

Aggregated self-reports from each plugin's `.gt/memory/semantic.json`, compared side-by-side.

**Generated:** 2026-02-06 (reconcile v1.1.0)
**Projects scanned:** 3 attempted, 3 found
**Reconcile source:** Carlos repo (cross-project)

---

## Project Status Matrix

| Field | Lisa | Carlos | Conductor |
|-------|------|--------|-----------|
| **Status** | Found (local) | Found (local) | Found (GitHub only, not cloned) |
| **Version** | 0.3.0 | 1.2.0 | 1.0.0 |
| **Stage** | alpha | beta | early development |
| **Type** | claude-code-plugin | claude-code-plugin | framework (monorepo) |
| **Language** | Python | Python | TypeScript |
| **Last scan** | 2026-02-06 | 2026-02-06 | 2026-02-05 |
| **Schema** | semantic-memory-v1 | semantic-memory-v1 | gastown semantic-memory (different) |

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

**Source:** `habitusnet/conductor` on GitHub (`.gt/memory/semantic.json`)

| Attribute | Value |
|-----------|-------|
| Name | Conductor |
| Role | Multi-LLM orchestration framework |
| Description | Enables autonomous agents (Claude Code, Codex CLI, Gemini CLI) to coordinate on shared codebases via MCP |
| Type | TypeScript monorepo (Turborepo) |
| Runtime | Node.js >= 20.0.0 |
| Database | SQLite (local) / PostgreSQL via Neon (production) |
| ORM | Drizzle ORM 0.38.3 |
| Frontend | Next.js 15.1.0 + React 19 + Tailwind |
| Testing | Vitest 4.0.16 |
| MCP | @modelcontextprotocol/sdk 1.0.0 |
| Sandbox | E2B (e2b, @e2b/code-interpreter) |
| CLI | Commander.js 12.1.0 + Ink 5.1.0 |

**Packages (8):**
- `@conductor/core` — Zod schemas, types, agent profiles, conflict detection
- `@conductor/state` — SQLite state store (legacy)
- `@conductor/db` — Drizzle ORM for SQLite/PostgreSQL
- `@conductor/mcp-server` — MCP server exposing tools to agents
- `@conductor/cli` — Commander.js CLI
- `@conductor/e2b-runner` — E2B sandbox integration
- `@conductor/connectors` — GitHub, LLM provider integrations
- `@conductor/dashboard` — Next.js oversight dashboard

**Key patterns:**
- CLI-First: Subscription-based CLI agents, not API orchestration
- MCP Coordination: All agents connect via MCP for task management
- Oversight Agent: Dedicated CLI agent monitors others
- API Fallback: API orchestration only for emergencies

**Supported agents:** Claude (Opus 4), Claude Sonnet 4, Claude Haiku, Gemini 2.0 Flash, Codex, GPT-4o

**Does NOT have:** `ecosystem_role` field in semantic.json (uses different schema)

---

## Ecosystem Role Comparison

| Responsibility | Lisa claims | Carlos claims | Conductor has | Conflict? |
|----------------|-------------|---------------|---------------|-----------|
| Pipeline ownership | Yes | No | No | None |
| .gt/ schema ownership | Yes | No (reads only) | No (not referenced) | **GAP**: Conductor doesn't reference .gt/ |
| Semantic memory | Yes (generates) | Yes (reads) | No (own schema) | **GAP**: Different schemas |
| Bead/convoy creation | Yes | No | No | None |
| Quality gate definition | Yes (gates.yaml) | Yes (hardcoded) | No | MISALIGNMENT: dual source |
| Quality gate enforcement | Yes (validate.py) | Yes (validate_quality_gates.py) | No | MISALIGNMENT: dual enforcement |
| Roadmap generation | Yes (plan stage) | Yes (roadmap command) | No | OK: complementary |
| scopecraft/ output | Yes (writes) | Yes (writes) | No | OK: shared format |
| Discovery engine | Yes (skill-based) | Yes (Python-based, richer) | No | OK: Carlos enriches |
| Model routing | No | Yes (model_router.py) | No | None |
| Agent tracking | No | No | Yes (full lifecycle) | None |
| Task management | No | No | Yes (MCP tools) | None |
| Context rollover | No | No | Expected (design doc) | **GAP**: Not yet visible in Conductor code |
| File locking | No | No | Yes | None |
| E2B sandbox | No | No | Yes | None |
| Conflict resolution | No | No | Expected | **GAP**: Not yet visible |
| Reconciliation | Yes (ecosystem root) | No | No | None |

---

## Interface Agreement Check

| Interface | Lisa says | Carlos says | Conductor says | Match? |
|-----------|-----------|-------------|----------------|--------|
| `.gt/memory/semantic.json` | "I write, others read" | "I read if exists" | Not referenced | **PARTIAL**: Conductor doesn't know about .gt/ |
| `scopecraft/` | "Stage 2 output" | "Roadmap output (shared)" | Not referenced | **PARTIAL**: Conductor doesn't produce scopecraft/ |
| `gates.yaml` | "Single source of truth" | "Should align" | Not referenced | **PARTIAL**: Carlos acknowledges but hasn't aligned |
| `.gt/beads/*.json` | "Stage 3 output, I own" | "I read to validate" | Not referenced | **PARTIAL**: Conductor should consume beads |
| `ecosystem_root` | "This repo" | "lisa3 (hosts reconcile)" | Not referenced | **PARTIAL**: Conductor doesn't declare |
| MCP tools | Not referenced | Not referenced | Yes (MCP server) | **GAP**: Lisa/Carlos don't reference MCP |
| Task queue | Not referenced | Not referenced | Yes (full workflow) | OK: Conductor's domain |
| File locks | Not referenced | Not referenced | Yes (TTL-based) | OK: Conductor's domain |

---

## Schema Divergence Note

Conductor uses a different semantic.json schema (`https://gastown.dev/schemas/semantic-memory.json`) than Lisa/Carlos (`semantic-memory-v1`). Key differences:

| Field | Lisa/Carlos | Conductor |
|-------|-------------|-----------|
| `$schema` | `"semantic-memory-v1"` | `"https://gastown.dev/schemas/semantic-memory.json"` |
| `ecosystem_role` | Present (role, reads_from, writes_to, does_not_own) | **Missing** |
| `non_goals` | Present | **Missing** |
| `integration_points` | Present (lisa/conductor/ralph references) | **Missing** |
| `architecture` | Not detailed | Full monorepo package map |
| `domain_concepts` | Not present | Full domain model (orgs, projects, agents, tasks, file locks) |
| `llm_integrations` | Not present | Full provider + model list |
| `deployment` | Not present | Local + production configs |

This is the **most important reconciliation finding**: Conductor's semantic.json doesn't yet describe its ecosystem role, what it reads/writes from the shared `.gt/` state, or how it relates to Lisa and Carlos. It describes itself as a standalone framework, not as an ecosystem participant.
