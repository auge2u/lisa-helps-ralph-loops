# Open Questions

## Resolved Questions

### Q1: How does reconcile discover project paths? — RESOLVED
**Decision:** Config file at `~/.lisa/ecosystem.json` listing project paths explicitly.
**Date:** 2026-02-06

### Q3: Should gates.yaml be a shared package or duplicated? — RESOLVED
**Decision:** Each plugin owns its own `gates.yaml` following the same schema. Reconcile validates they don't conflict.
**Date:** 2026-02-06

---

## Blocking Questions

(none remaining)

---

## Resolved Questions (continued)

### Q2: What is the checkpoint schema for context rollover? — RESOLVED
**Decision:** Hybrid SQLite + Bead File Updates. Conductor uses its existing SQLite state store with a new `agent_checkpoints` table for runtime checkpoint data (id, projectId, agentId, taskId, beadId, checkpointType, stage, context JSON). On bead completion, status is synced back to `.gt/beads/{id}.json` for Lisa compatibility. Two MCP tools: `conductor_checkpoint` (save) and `conductor_resume_from_checkpoint` (read).
**Date:** 2026-02-08
**Implemented in:** convoy-003 bead gt-w5y2c

---

## Experiments Needed

### Experiment: Context rollover detection accuracy
**Hypothesis:** Heartbeat degradation reliably signals context exhaustion before output quality drops
**Method:** Run a CLI agent on a large task, monitor heartbeat response time and output quality as context fills
**Success Criteria:** >90% detection before output degradation begins
**Owner:** Conductor

### Experiment: e2b sandbox cost vs. CLI agent cost for mechanical tasks
**Hypothesis:** e2b with cheap models (Haiku) costs <20% of CLI agent (Sonnet) for file scanning tasks
**Method:** Run same file scanning task via both approaches, measure cost and quality
**Success Criteria:** >60% cost reduction with equivalent output quality
**Owner:** Conductor

### Experiment: Model routing savings measurement
**Hypothesis:** Smart model routing across task types reduces costs 60-70% vs. Opus-only
**Method:** Run Carlos roadmap workflow with model routing vs. fixed-Opus, compare cost and quality
**Success Criteria:** 60-70% cost reduction, <5% quality drop (measured by gate pass rate)
**Owner:** Carlos

---

## Parking Lot
- Multi-user support (currently single-developer focused)
- Web dashboard for ecosystem status (currently CLI-only)
- Plugin marketplace discovery (auto-detect complementary plugins)
- Shared memory store beyond file-based `.gt/` (for very large ecosystems)
- Integration with non-Claude CLI agents (Gemini CLI, Copilot CLI)
- Legal/compliance plugin as fourth ecosystem member
- Finance plugin for cost optimization and budgeting
