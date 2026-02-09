# Open Questions

## Resolved Questions

### Q1: How does reconcile discover project paths? — RESOLVED
**Decision:** Config file at `~/.lisa/ecosystem.json` listing project paths explicitly.
**Date:** 2026-02-06

### Q2: What is the checkpoint schema for context rollover? — RESOLVED
**Decision:** Hybrid SQLite + Bead File Updates. Conductor uses SQLite state store with `agent_checkpoints` table. On bead completion, status syncs back to `.gt/beads/{id}.json`. Two MCP tools: `conductor_checkpoint` and `conductor_resume_from_checkpoint`.
**Date:** 2026-02-08
**Implemented in:** Conductor convoy-003 bead gt-w5y2c

### Q3: Should gates.yaml be a shared package or duplicated? — RESOLVED
**Decision:** Each plugin owns its own `gates.yaml` following the same schema. Reconcile validates they don't conflict.
**Date:** 2026-02-06

---

## Blocking Questions

### Q4: Marketplace submission requirements (NEW)

**Question:** What are the exact requirements for Claude Code plugin marketplace submission?

**Context:** Lisa needs to be published on the marketplace for external adoption. The submission process, review criteria, and requirements are not yet documented from our side.

**Options:**
1. Submit and iterate based on feedback
2. Research requirements first, then prepare submission
3. Soft-launch via direct plugin install URL before formal marketplace listing

**Impact on Roadmap:** Blocks Phase 4 (Publish & Migrate)
**Owner:** Product
**Proposed Resolution:** Research marketplace requirements as first step of Phase 4

---

### Q5: npm scope for prductr-com packages (NEW)

**Question:** What npm scope should ecosystem packages use?

**Context:** Conductor needs npm scope for package publication. This decision affects all three projects.

**Options:**
1. **@prductr**: Matches org name, broad scope for future packages
2. **@conductor**: Clean, matches Conductor project name. May be taken.
3. **Project-specific**: @lisa, @carlos, @conductor (each plugin gets own scope)
4. **Unscoped**: No scope prefix

**Impact on Roadmap:** Blocks Conductor Phase 1 (npm publish)
**Owner:** Product/DevOps
**Proposed Resolution:** Check availability of @prductr; use as unified scope

---

## Non-Blocking Questions

### Q6: Git remote-based project identification

**Question:** Should ecosystem.json use git remote URLs instead of filesystem paths?

**Context:** After prductr-com migration, filesystem paths change. Git remotes are stable identifiers.

**Options:**
1. **Remote-based**: Identify projects by git remote origin URL
2. **Path-based with update**: Keep paths, document update procedure
3. **Both**: Support remote and path, prefer remote when available

**Impact:** Phase 5 (Standalone Hardening)
**Current Lean:** Option 3 (both, prefer remote)
**Owner:** Architecture

### Q7: Reconcile performance at scale

**Question:** How will reconcile perform with 10+ projects?

**Context:** Currently tested with 3 projects. If the ecosystem grows, reconcile needs to be efficient.

**Options:**
1. **Incremental**: Only re-scan changed projects (git hash check)
2. **Parallel**: Scan all projects concurrently
3. **Cached**: Keep last reconcile in memory, diff against current

**Impact:** Phase 6 (Ecosystem Maturity)
**Current Lean:** Option 1 (incremental with force flag)
**Owner:** Architecture

---

## Experiments Needed

### Experiment: Pipeline reliability on diverse projects
**Hypothesis:** Lisa pipeline (discover + plan + structure) works on 90%+ of GitHub repositories
**Method:** Run pipeline on 20 diverse repos; measure success rate and failure modes
**Success Criteria:** 90%+ completion without crashes; edge cases documented
**Owner:** Lisa
**When:** Phase 5

### Experiment: Standalone value proposition
**Hypothesis:** Lisa provides measurable value without Carlos or Conductor
**Method:** 5 external users try Lisa standalone; measure time to value and satisfaction
**Success Criteria:** 4/5 users report value; average time to first useful output <15 minutes
**Owner:** Product
**When:** Phase 4 (after marketplace publish)

### Experiment: Context recovery effectiveness
**Hypothesis:** Reading .checkpoint.json restores context faster than re-running reconcile
**Method:** After simulated context loss, compare time to useful context via checkpoint vs. re-scan
**Success Criteria:** Checkpoint recovery <30 seconds; re-scan >5 minutes
**Owner:** Lisa
**When:** Phase 6

---

## Parking Lot
- Multi-user support (currently single-developer focused)
- Web dashboard for ecosystem status (currently CLI-only; Conductor has dashboard)
- Plugin marketplace auto-discovery of complementary plugins
- Shared memory store beyond file-based `.gt/` (for very large ecosystems)
- Integration with non-Claude CLI agents (Gemini CLI, Copilot CLI)
- Legal/compliance plugin as fourth ecosystem member
- Finance plugin for cost optimization and budgeting
