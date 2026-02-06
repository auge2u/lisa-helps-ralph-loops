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

### Q2: What is the checkpoint schema for context rollover?
**Context:** When a CLI agent's context window fills, Conductor needs to checkpoint state and hand off to a fresh session. The checkpoint format must be sufficient to resume work.
**Impact:** Blocks context rollover implementation (Phase 3, Story 9)
**Proposed Resolution:**
- Option A: Extend `.gt/` state files with agent progress markers
- Option B: Separate `.conductor/checkpoints/` directory with agent-specific state
- Option C: Use `.agent/scratchpad.md` pattern (already used by Lisa/Carlos)
**Stakeholders Needed:** Conductor architect, Lisa maintainer
**Deadline:** Before Phase 3 starts

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
