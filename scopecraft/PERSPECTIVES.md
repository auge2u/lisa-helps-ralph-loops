# Ecosystem Perspectives

Aggregated self-reports from each plugin's `.gt/memory/semantic.json`, compared side-by-side.

**Generated:** 2026-02-10 (reconcile v5.0.0 — Lisa Phase 4-6)
**Data source:** Local filesystem (all projects cloned)
**Projects scanned:** 3 attempted, 3 found (all local)
**Reconcile method:** Lisa Stage 5 skill (incremental — Lisa full re-scan, Carlos/Conductor checked via git hash)

---

## Project Status Matrix

| Field | Lisa | Carlos | Conductor |
|-------|------|--------|-----------|
| **Status** | Found (local) | Found (local) | Found (local) |
| **Version** | 0.3.0 | 1.2.0 | 1.0.0 |
| **Stage** | alpha | beta | ga |
| **Type** | claude-code-plugin | claude-code-plugin | framework (monorepo) |
| **Language** | Python | Python | TypeScript |
| **Schema** | semantic-memory-v1 | semantic-memory-v1 | semantic-memory-v1 |
| **Last scan** | 2026-02-08T19:00 | 2026-02-09T18:00 | 2026-02-09T14:45 |
| **Git hash** | 0ace0b4 | 37c7cb7 | 1fdaebf |
| **License** | MIT | MIT | MIT |
| **gates.yaml** | Yes (v1.1, 31 gates, 5 stages) | Yes (v1.0, 9 gates, +max support) | Yes (v1.1, ecosystem overlay) |
| **Own reconcile** | Yes (this report) | Yes (Cycle 4) | Yes (Cycle 7) |
| **semantic.json fresh?** | **Stale** (G9) | Yes | Yes |

---

## Lisa Self-Report

**Source:** `~/github/auge2u/lisa3/.gt/memory/semantic.json`

| Attribute | Value | Change from v4.0.0 |
|-----------|-------|---------------------|
| Name | lisa | — |
| Role | pipeline-and-memory | — |
| Version | 0.3.0 | — |
| Standalone command | `/lisa:migrate` | — |
| Ecosystem root | Yes | — |
| Commands | 8 | — |
| Agents | 2 (archaeologist, migrator) | — |
| Skills | 5 (research, discover, plan, structure, reconcile) | — |
| Quality gates | 31 across 5 stages | — |
| Gate source | gates.yaml v1.1 (declarative) | — |
| Checkpoint schema | Formal JSON Schema | — |
| Templates | 3 reconcile output templates | — |

**Reads from:** target project files, carlos/.gt/memory/semantic.json, conductor/.gt/memory/semantic.json
**Writes to:** .gt/research/, .gt/memory/, scopecraft/, .gt/beads/, .gt/convoys/, scopecraft/.checkpoint.json
**Does not own:** Carlos analysis reports, Conductor state

**Changes since v4.0.0 (not yet reflected in semantic.json):**
- validate.py PyYAML fallback mode (hardcoded JSON-only gates when PyYAML unavailable)
- Reconcile SKILL.md: standalone mode, incremental mode, git remote fallback
- ecosystem-config-v2 schema support (remote field per project)
- checkpoint-schema.json: +git_hash, +remote, +scan_mode fields
- docs/GETTING_STARTED.md (new)
- plugin.json: +category, +keywords, +email (marketplace-ready)
- README.md rewritten for v0.3.0
- CHANGELOG.md v0.3.0 entry
- plugins/lisa-loops-memory/DEPRECATED.md (migration guide)

---

## Carlos Self-Report

**Source:** `~/github/auge2u/carlos/.gt/memory/semantic.json`

| Attribute | Value | Change from v4.0.0 |
|-----------|-------|---------------------|
| Name | carlos | — |
| Role | specialist-fixer | — |
| Version | 1.2.0 | — |
| LOC | 11,422 | — |
| Tests | 482 + 95 security | — |
| Quality gates | gates.yaml v1.0 (9 gates) | +max support on file_count |
| Discovery cache | 24h TTL | — |
| Last scan | 2026-02-09T18:00 | Was 2026-02-09T12:00 |
| Agent context tokens | ~1,500 | — |
| Convoy-007 | COMPLETE (5/5 beads) | — |
| Own reconcile | Cycle 4 (2026-02-09) | — |

**Reads from:** .gt/memory/semantic.json, .gt/beads/*.json, scopecraft/*.md
**Writes to:** scopecraft/*.md, quality gate results, analysis reports
**Does not own:** .gt/beads/, .gt/convoys/, conductor state

### Carlos New Commits (since v4.0.0)

| Commit | Description |
|--------|-------------|
| 1df05cd | Refresh scopecraft roadmap to v1.2.0 |
| 09b9274 | Test count corrected 448 → 482 |
| 2193f6e | Cycle 4 reconcile — full ecosystem, 98% alignment |
| ded0a2c | Semantic.json discovery scan refresh (68 commits) |
| 37c7cb7 | **Add min/max support to file_count gate** |

---

## Conductor Self-Report

**Source:** `~/github/habitusnet/conductor/.gt/memory/semantic.json`

| Attribute | Value | Change from v4.0.0 |
|-----------|-------|---------------------|
| Name | conductor | — |
| Status | ga | — |
| Version | 1.0.0 | — |
| TypeScript | 5.9.3 | — |
| MCP tools | 24 listed (4 categories) | — |
| Tests | 1,374 | — |
| Packages | 10 | — |
| Convoys | 5 complete | — |
| Beads | 22 total (19 complete, 3 deferred) | — |
| Last scan | 2026-02-09T14:45 | — |
| Own reconcile | Cycle 7 | — |

**No changes since v4.0.0.**

**Reads from:** .gt/beads/*.json, .gt/convoys/*.json, .gt/memory/semantic.json, scopecraft/
**Writes to:** Task queue state, file locks, cost events, agent lifecycle, escalation queue
**Does not own:** .gt/ schema, scopecraft/ format, quality gate definitions, semantic memory generation

---

## Ecosystem Role Comparison

All roles aligned. No conflicts.

| Responsibility | Lisa | Carlos | Conductor | Conflict? |
|----------------|------|--------|-----------|-----------|
| Pipeline ownership | Yes | No | No | None |
| Quality gate definition | Yes (gates.yaml v1.1) | Yes (gates.yaml v1.0) | No (overlay) | None |
| Reconciliation | Yes (ecosystem root) | Yes (project-level) | Yes (ecosystem-level) | OK: complementary |
| Bead/convoy creation | Yes | No | No | None |
| Bead consumption | No | No | Yes (GA) | None |
| Context rollover | No | No | Yes (GA) | None |
| Specialist analysis | No | Yes | No | None |
| Agent context budget | No | Yes (41% reduced) | TBD (cq-02) | Pending |
| Organization isolation | No | No | Yes (GA) | None |
| Autonomous oversight | No | No | Yes (GA) | None |
| Zone-based coordination | No | No | Yes (GA) | None |
| **Marketplace readiness** | **Yes** (plugin.json ready) | Pending (gt-mkt04) | N/A | None |
| **Standalone validation** | **Yes** (PyYAML fallback) | Yes | Yes | None |

---

## Interface Agreement Check

| Interface | Lisa | Carlos | Conductor | Match? |
|-----------|------|--------|-----------|--------|
| gates.yaml | v1.1, canonical source | v1.0, Lisa-compatible (+max) | v1.1 overlay | **FULL MATCH** |
| Bead schema | `gt-xxxxx` format | reads beads | BeadSchema Zod (imports) | **FULL MATCH** |
| Convoy schema | `eco-convoy-NNN` / `convoy-NNN` | N/A | ConvoySchema Zod (imports) | **FULL MATCH** |
| Checkpoint schema | `reconcile-checkpoint-v1` | N/A | `AgentCheckpointSchema` | OK: complementary |
| Ecosystem config | **v2** (remote field) | reads | reads | **FULL MATCH** |
| Heartbeat | N/A | N/A | Enhanced (+token tracking) | OK: backward compatible |
| Agent context | N/A | ~1,500 tokens | TBD (cq-02) | Pending (non-blocking) |
| Agent registration | N/A | conductor_request_access() | Tool exists in code | **FULL MATCH** |
| Model routing | N/A | Carlos owns model_router.py | Consumes via metadata.modelTier | **FULL MATCH** |
| Ecosystem metadata | N/A | get_ecosystem_metadata() | Reads metadata.modelTier | **FULL MATCH** |
| MCP task lifecycle | N/A | N/A | 8 tools (claim→complete/fail) | New in GA |
| Oversight tools | N/A | N/A | 5 tools (reassign, escalate) | New in GA |

---

## Schema Divergence Note

All three projects use `semantic-memory-v1` schema. No divergence.

Carlos gates.yaml v1.0 now supports `max` parameter on `file_count` and `pattern_count` gates (commit 37c7cb7). Lisa gates.yaml v1.1 already supported this — Carlos is now aligned with Lisa's gate feature set.

---

## Notable Changes From v4.0.0

1. **Lisa Phase 4-6 implementation:** README rewritten, CHANGELOG added, validate.py fallback mode, reconcile standalone/incremental modes, ecosystem-config-v2, getting started guide, marketplace-ready plugin.json.
2. **Carlos gates.yaml enhanced:** min/max support on file_count gate (37c7cb7). Semantic.json rescanned (ded0a2c, last_scan now 2026-02-09T18:00).
3. **Conductor unchanged:** Still at 1fdaebf, no new commits since GA.
4. **Ecosystem config v2:** All 3 projects now have git remote URLs in `~/.lisa/ecosystem.json`.
5. **Lisa semantic.json stale (G9):** Last scan 2026-02-08, missing Phase 4-6 changes.
