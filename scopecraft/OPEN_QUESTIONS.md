# Open Questions

## Resolved Questions

### Q1: How does Lisa discover other plugins? -- RESOLVED
**Decision:** Config file at `~/.lisa/ecosystem.json` listing project paths explicitly.
**Date:** 2026-02-06

### Q2: What is the checkpoint schema for context rollover? -- RESOLVED
**Decision:** Hybrid SQLite + Bead File Updates. Conductor uses SQLite state store with `agent_checkpoints` table. On bead completion, status syncs back to `.gt/beads/{id}.json`. Two MCP tools: `conductor_checkpoint` and `conductor_resume_from_checkpoint`.
**Date:** 2026-02-08
**Implemented in:** Conductor convoy-003 bead gt-w5y2c

### Q3: Should gates.yaml be a shared package or duplicated? -- RESOLVED
**Decision:** Each plugin owns its own `gates.yaml` following the same schema. Reconcile validates they don't conflict.
**Date:** 2026-02-06
**Validated:** Carlos gates.yaml v1.0 follows Lisa schema; Conductor uses v1.1 overlay.

---

## Blocking Questions

### Q4: Marketplace submission requirements

**Question:** What are the exact requirements for Claude Code plugin marketplace submission?

**Context:** Lisa needs to be published on the marketplace for external adoption. The submission process, review criteria, and required manifest fields are not documented from our side. This is the first step of Phase 4.

**Options:**
1. Submit current plugin.json and iterate on rejection feedback
2. Research requirements thoroughly before first submission
3. Soft-launch via direct plugin install URL, formal submission later

**Impact on Roadmap:** Blocks Story 5 (marketplace submission) and downstream Stories 6, 7
**Owner:** Product
**Proposed Resolution:** Research as first action in Phase 4 (Story 4). Check Claude Code docs, existing plugin examples, and any submission guidelines.
**Deadline:** Before Phase 4 implementation begins

---

### Q5: npm scope for prductr-com packages

**Question:** What npm scope should ecosystem packages use when published?

**Context:** Conductor needs npm scope for package publication. This decision affects all three projects' external identities.

**Options:**
1. **@prductr** -- Matches org name, broad scope for future packages
2. **@conductor** -- Clean, matches Conductor project name (may be taken)
3. **Per-project scopes** -- @lisa, @carlos, @conductor (fragmented)
4. **Unscoped** -- No prefix, simplest but may conflict

**Impact on Roadmap:** Blocks Conductor npm publish; does not block Lisa Phase 4
**Owner:** Product/DevOps
**Proposed Resolution:** Check availability of @prductr on npm; use as unified scope
**Deadline:** Before Conductor publish

---

## Non-Blocking Questions

### Q6: Git remote-based project identification

**Question:** Should ecosystem.json use git remote URLs instead of filesystem paths for project identification?

**Context:** After prductr-com migration, filesystem paths change for all three projects. Git remote origin URLs are stable identifiers that work regardless of where repos are cloned.

**Options:**
1. **Remote-based only** -- Identify by `git remote get-url origin`
2. **Path-based with migration docs** -- Keep paths, document update procedure
3. **Both with preference** -- Support `remote` and `path` fields, prefer remote when available

**Impact:** Phase 6 (Reconcile Resilience), Story 12
**Current Lean:** Option 3 (both, prefer remote) -- backward compatible, gradually migrate
**Owner:** Architecture

### Q7: Reconcile performance at scale

**Question:** How will reconcile perform with 10+ projects in the ecosystem?

**Context:** Currently tested with 3 projects. If the ecosystem grows (more plugins, user projects), reconcile needs to remain fast.

**Options:**
1. **Incremental** -- Only re-scan changed projects (git hash check)
2. **Parallel** -- Scan all projects concurrently
3. **Cached** -- Keep last reconcile state, diff against current

**Impact:** Phase 6 (Ecosystem Maturity), Story 13
**Current Lean:** Option 1 (incremental with `--force` flag)
**Owner:** Architecture

### Q8: Deprecated plugin removal timing

**Question:** When should `plugins/lisa-loops-memory/` be removed vs. just marked deprecated?

**Context:** The deprecated plugin is confusing for new contributors but the existing tests import from it. Removal requires test migration.

**Options:**
1. **Remove immediately** in Phase 4 (clean break)
2. **Archive with notice** -- add DEPRECATED.md, remove in v1.0.0
3. **Remove after test migration** -- update tests first, then delete

**Impact:** Phase 4, Story 3
**Current Lean:** Option 3 (update tests first for safety)
**Owner:** Engineering

---

## Experiments Needed

### Experiment: Pipeline reliability on diverse projects
**Hypothesis:** Lisa pipeline (discover + plan + structure) completes without crashes on 90%+ of GitHub repositories with standard project structure
**Method:** Run pipeline on 20 diverse repos (5 Python, 5 TypeScript, 5 Go, 5 other); record success/failure per stage
**Success Criteria:** 90%+ completion without crashes; all failure modes documented with workarounds
**Owner:** Lisa
**When:** Phase 5, Story 11

### Experiment: Standalone value proposition
**Hypothesis:** Lisa provides measurable value to users who have never heard of Carlos or Conductor
**Method:** 5 external developers try Lisa standalone on their own projects; measure time to value and satisfaction
**Success Criteria:** 4/5 users report value; average time to first useful output <15 minutes
**Owner:** Product
**When:** Phase 4, after marketplace publish

### Experiment: Context recovery effectiveness
**Hypothesis:** Reading .checkpoint.json restores useful working context faster than re-running reconcile from scratch
**Method:** After simulated context loss (new conversation, no prior context), compare time to useful context: checkpoint read vs. full re-scan
**Success Criteria:** Checkpoint recovery <30 seconds; re-scan >5 minutes
**Owner:** Lisa
**When:** Phase 6

---

## Parking Lot
- Multi-user support (currently single-developer focused)
- Web dashboard for ecosystem status (Conductor has dashboard, Lisa is CLI-only)
- Plugin marketplace auto-discovery of complementary plugins
- Shared memory store beyond file-based `.gt/` (for very large ecosystems)
- Integration with non-Claude CLI agents (Gemini CLI, Copilot CLI)
- Legal/compliance plugin as fourth ecosystem member
- Gastown Mayor API direct integration (depends on Gastown roadmap)
