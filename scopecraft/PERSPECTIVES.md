# Ecosystem Perspectives

**Generated:** 2026-02-24 (reconcile v6.0.1)
**Projects scanned:** 3 attempted, 3 found (Lisa: full rescan; Carlos + Conductor: cached)

---

## Project Status Matrix

| Field | Lisa | Carlos | Conductor |
|-------|------|--------|-----------|
| Status | found | found | found |
| Version | 0.3.0 | 1.2.0 | 1.0.0 |
| Release status | alpha | beta | ga |
| Schema | semantic-memory-v1 | semantic-memory-v1 | semantic-memory-v1 |
| Last scan | 2026-02-24 (**fresh**) | 2026-02-09 | 2026-02-09 |
| Primary language | Python | Python | TypeScript |
| Git hash | b77b730 | df3b763 | 80ed6b2 |
| Semantic freshness | FRESH (G10 resolved) | ok | ok |

---

## Lisa Self-Report

**Source:** `.gt/memory/semantic.json` (scanned 2026-02-24T12:00:00Z — fresh)

| Attribute | Value |
|-----------|-------|
| Role | pipeline-and-memory |
| Ecosystem root | Yes |
| Standalone command | `/lisa:migrate` |
| Pipeline stages | research(0), discover(1), plan(2), structure(3), reconcile(5) |
| Quality gates | 31 (gates.yaml v1.1, 298 lines) |
| Tests | 25 (pytest, legacy validator) |
| Validator | validate.py (833 lines, PyYAML fallback) |
| Semantic sections | 19 |
| Files analyzed | 44 |

**Reads from:** target project files, carlos/.gt/memory/semantic.json, conductor/.gt/memory/semantic.json, ~/.lisa/ecosystem.json

**Writes to:** .gt/research/, .gt/memory/, scopecraft/, .gt/beads/, .gt/convoys/, scopecraft/.checkpoint.json, scopecraft/ALIGNMENT_REPORT.md

**Does not own:** Carlos analysis reports, Conductor state

**Gastown toolchain documented in semantic.json:**
- `bd` CLI: Beads issue tracking (Dolt SQL), `bd create --file=<markdown>`, `bd ready`, `bd update`, `bd close`, `bd sync`
- `bv` CLI: Graph analysis (read-only, always `--robot-*` flags)
- `gt` CLI: Workspace manager, `gt convoy create`, `gt sling <bead-id> <rig>`, `gt convoy status`
- Propulsion Principle: "If you find something on your hook, YOU RUN IT"
- Upstream refs: `~/github/steveyegge/beads` (canonical Issue schema), `~/github/steveyegge/gastown` (architecture)

---

## Carlos Self-Report

**Source:** `~/github/auge2u/carlos/.gt/memory/semantic.json` (scanned 2026-02-09 — cached, unchanged)

| Attribute | Value |
|-----------|-------|
| Role | specialist-fixer |
| Ecosystem root | No (lisa3 is root) |
| Standalone command | `/carlos:roadmap` |
| Python modules | 15 |
| Python LOC | ~11,422 |
| Tests | 482 (pytest, 80% coverage enforced) |
| Agent personas | product-owner (Opus), tech-auditor (Sonnet), market-fit-auditor (Sonnet) |

**Reads from:** .gt/memory/semantic.json, .gt/beads/*.json, scopecraft/*.md

**Writes to:** scopecraft/*.md, quality gate results, analysis reports

**Does not own:** .gt/beads/, .gt/convoys/, conductor state

**Notable since last scan:** CLAUDE.md Ecosystem Position section added (df3b763) — no code changes

---

## Conductor Self-Report

**Source:** `~/github/habitusnet/conductor/.gt/memory/semantic.json` (scanned 2026-02-09 — cached, unchanged)

| Attribute | Value |
|-----------|-------|
| Role | orchestration-and-oversight |
| Ecosystem root | No (lisa3 is root) |
| Status | GA (v1.0.0) |
| MCP tools | 21 (conductor_import_beads, conductor_claim_task, etc.) |
| Language | TypeScript (Turborepo monorepo) |
| Database | SQLite (local) / PostgreSQL Neon (production) |
| Tests | ~1,374 (Vitest) |

**Reads from:** .gt/beads/*.json, .gt/convoys/*.json, .gt/memory/semantic.json, scopecraft/

**Writes to:** Task queue state (SQLite/PostgreSQL), file locks, cost events, agent lifecycle state, escalation queue

**Does not own:** .gt/ directory schema, scopecraft/ output format, quality gate definitions

**Notable since last scan:** CLAUDE.md Ecosystem Position section added (80ed6b2) — no code changes, G8 (MCP categories) still open

---

## Ecosystem Role Comparison

| Responsibility | Lisa | Carlos | Conductor | Conflict? |
|----------------|------|--------|-----------|-----------|
| .gt/ schema ownership | ✅ owns | reads only | reads only | No |
| gates.yaml ownership | ✅ owns | enforces (compatible schema) | reads | No |
| Bead/convoy creation | ✅ structure stage | ❌ | imports via conductor_import_beads | No |
| scopecraft/ writing | ✅ plan stage | ✅ refines | ❌ reads only | No |
| Roadmap generation | ✅ plan stage | ✅ (richer) | ❌ | No (complementary) |
| Agent lifecycle | ❌ | ❌ | ✅ owns | No |
| Context rollover | ✅ stage checkpoints | ❌ | ✅ owns | No (complementary) |
| Model routing | ❌ | ✅ model_router.py | consumes | No |
| Reconcile (ecosystem) | ✅ stage 5 | ❌ | ❌ | No |

---

## Interface Agreement Check

| Interface | Lisa says | Carlos says | Conductor says | Match? |
|-----------|-----------|-------------|----------------|--------|
| .gt/beads/*.json | writes (stage 3) | reads | reads + imports | ✅ |
| scopecraft/ | writes (stage 2) | reads + refines | reads as context bundles | ✅ |
| .gt/memory/semantic.json | writes (stage 1) | reads (discovery cache) | reads (personality curation) | ✅ |
| gates.yaml | owns (Lisa schema v1.1) | enforces (compatible v1.0) | reads (overlay) | ✅ |
| Conductor MCP tools | not used | callable via task routing | owns/serves | ✅ |

---

## Upstream Ecosystem Reference

| Repo | Purpose | Local path |
|------|---------|------------|
| steveyegge/beads | Canonical `bd` Issue schema (`internal/types/types.go`) | ~/github/steveyegge/beads |
| steveyegge/gastown | Architecture reference (`docs/overview.md`) | ~/github/steveyegge/gastown |

Lisa's `.gt/beads/*.json` format is a staging area. Real execution uses `bd create`, `gt convoy create`, `gt sling`.
