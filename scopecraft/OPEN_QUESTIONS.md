# Open Questions

## Blocking Questions

### Q1: How does Conductor discover project paths for multi-project awareness?
**Context:** Conductor needs to know where Lisa, Carlos, and other project repos live on disk. Currently reconcile requires explicit paths.
**Impact:** Blocks Phase 3 (Conductor can't find projects to orchestrate without this)
**Proposed Resolution:**
- Option A: Configuration file listing project paths (e.g., `~/.conductor/projects.json`)
- Option B: Convention-based discovery (scan `~/github/` for `.gt/` directories)
- Option C: User provides paths per session via CLI flags
**Stakeholders Needed:** Conductor architect
**Deadline:** Before Phase 3 starts

### Q2: What is the checkpoint schema for context rollover?
**Context:** When a CLI agent's context window fills, Conductor needs to checkpoint state and hand off to a fresh session. The checkpoint format must be sufficient to resume work.
**Impact:** Blocks context rollover implementation (Phase 3, Story 9)
**Proposed Resolution:**
- Option A: Extend `.gt/` state files with agent progress markers
- Option B: Separate `.conductor/checkpoints/` directory with agent-specific state
- Option C: Use `.agent/scratchpad.md` pattern (already used by Lisa/Carlos)
**Stakeholders Needed:** Conductor architect, Lisa maintainer
**Deadline:** Before Phase 3 starts

### Q3: Should gates.yaml be a shared package or duplicated?
**Context:** Carlos needs to read Lisa's `gates.yaml` format. Currently Carlos has hardcoded gates. The question is whether `gates.yaml` becomes a shared schema or Carlos reads Lisa's file directly.
**Impact:** Blocks Phase 2 quality gate alignment (Story 7)
**Proposed Resolution:**
- Option A: Carlos reads Lisa's `gates.yaml` from ecosystem root (requires knowing Lisa's path)
- Option B: Each plugin has own `gates.yaml` following same schema; reconcile validates they don't conflict
- Option C: Shared gates.yaml published as artifact; both plugins consume it
**Stakeholders Needed:** Lisa maintainer, Carlos maintainer
**Deadline:** Phase 2

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
