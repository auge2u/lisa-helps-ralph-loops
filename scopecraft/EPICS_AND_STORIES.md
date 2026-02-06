# Epics and Stories

## Epic: Ecosystem Self-Description
**Theme:** Core Value
**Intent:** Every plugin can describe itself in a machine-readable format that reconcile can consume.

### Stories

#### Story 1: Populate Lisa semantic.json
**As a** Lisa user
**I want** Lisa's `.gt/memory/semantic.json` to contain actual project data
**So that** reconcile has Lisa's self-report to compare against the ecosystem

**Acceptance Criteria:**
- [ ] `project.name` is "lisa" with correct version
- [ ] `tech_stack` includes Python, PyYAML, pytest
- [ ] `ecosystem_role` field describes pipeline & memory ownership
- [ ] `evidence.files_analyzed` lists actual scanned files

**Dependencies:** None
**Complexity:** S
**Risk:** Low

#### Story 2: Populate Conductor semantic.json
**As a** ecosystem participant
**I want** Conductor's `.gt/memory/semantic.json` to exist
**So that** reconcile sees all three projects

**Acceptance Criteria:**
- [ ] File exists at `conductor/.gt/memory/semantic.json`
- [ ] `project.name` is "conductor"
- [ ] `ecosystem_role` describes orchestration responsibilities
- [ ] At minimum, `project` and `ecosystem_role` fields populated (even if tech_stack is sparse)

**Dependencies:** Conductor repo must exist with some content
**Complexity:** S
**Risk:** Medium (Conductor may be too early for meaningful discovery)

#### Story 3: Standardize ecosystem_role schema
**As a** reconcile consumer
**I want** all three plugins to use the same `ecosystem_role` schema
**So that** reconcile can compare roles, interfaces, and ownership boundaries

**Acceptance Criteria:**
- [ ] `ecosystem_role` has: `role`, `description`, `reads_from`, `writes_to`, `does_not_own`, `standalone`, `ecosystem_root`
- [ ] Schema documented in Lisa's reconcile skill
- [ ] Carlos already conforms (verified)
- [ ] Lisa and Conductor updated to conform

**Dependencies:** Story 1, Story 2
**Complexity:** M
**Risk:** Low

---

## Epic: Reconciliation Pipeline
**Theme:** Core Value
**Intent:** Lisa can produce alignment reports and checkpoints across the ecosystem.

### Stories

#### Story 4: Implement reconcile command
**As a** Lisa user
**I want** `/lisa:reconcile` to read semantic.json from multiple projects
**So that** I get an alignment report showing drift, gaps, and contradictions

**Acceptance Criteria:**
- [ ] Reads semantic.json from configurable project paths
- [ ] Produces `scopecraft/ALIGNMENT_REPORT.md` with per-plugin status
- [ ] Produces `scopecraft/.checkpoint.json` with reconcile timestamp and state
- [ ] Detects missing plugins gracefully (warns but doesn't fail)
- [ ] Compares `ecosystem_role` fields for contradictions

**Dependencies:** Story 1, Story 2 (at least 2 of 3 plugins must have semantic.json)
**Complexity:** L
**Risk:** Medium

#### Story 5: Reconcile checkpoint format
**As a** ecosystem plugin
**I want** `.checkpoint.json` to capture the ecosystem state at reconciliation time
**So that** any plugin can read it to understand current alignment without re-running reconcile

**Acceptance Criteria:**
- [ ] Contains timestamp, reconcile version, project list
- [ ] Per-project: semantic.json hash, version, last_scan date
- [ ] Alignment status: aligned/drifted/missing per project
- [ ] Human-readable companion: `ALIGNMENT_REPORT.md`

**Dependencies:** Story 4
**Complexity:** M
**Risk:** Low

---

## Epic: Carlos Integration
**Theme:** Adoption
**Intent:** Carlos reads Lisa's state instead of re-discovering, and quality gates align.

### Stories

#### Story 6: Carlos reads .gt/memory/semantic.json
**As a** Carlos user working on a Lisa-discovered project
**I want** Carlos to detect existing semantic.json and skip redundant discovery
**So that** analysis is faster and consistent with Lisa's findings

**Acceptance Criteria:**
- [ ] Carlos checks for `.gt/memory/semantic.json` before running discovery
- [ ] If fresh (< 24h), skips discovery and uses existing data
- [ ] If stale or missing, runs discovery as normal
- [ ] Logs whether it used cached or fresh discovery

**Dependencies:** Phase 1 complete (semantic.json populated)
**Complexity:** M
**Risk:** Low

#### Story 7: Create Carlos gates.yaml following Lisa's schema
**As a** ecosystem maintainer
**I want** Carlos to have its own `gates.yaml` following Lisa's schema
**So that** quality standards use the same format and reconcile can validate consistency

**Acceptance Criteria:**
- [ ] Carlos has `gates.yaml` in the same schema as Lisa's
- [ ] Carlos `validate_quality_gates.py` reads from `gates.yaml` instead of hardcoded gates
- [ ] Gate check types are compatible (file_exists, json_valid, pattern_exists, etc.)
- [ ] Reconcile can compare both `gates.yaml` files for conflicts

**Dependencies:** Story 6
**Complexity:** L
**Risk:** Medium (different validation engines)
**Decision:** Each plugin owns gates.yaml, same schema, reconcile validates (resolved 2026-02-06)

---

## Epic: Conductor Task Assignment
**Theme:** Core Value
**Intent:** Conductor can assign structured work items to agents.

### Stories

#### Story 8: Conductor reads beads/convoys
**As a** Conductor orchestrator
**I want** to read `.gt/beads/*.json` and `.gt/convoys/*.json`
**So that** I can assign structured work to agents

**Acceptance Criteria:**
- [ ] Conductor enumerates bead files and parses bead-v1 schema
- [ ] Conductor enumerates convoy files and parses convoy-v1 schema
- [ ] Task assignment respects convoy grouping (assign convoy, not individual beads)
- [ ] Bead status updates written back to `.gt/beads/`

**Dependencies:** Lisa structure stage must have run on target project
**Complexity:** L
**Risk:** Medium

#### Story 9: Context rollover for CLI agents
**As a** Conductor operator
**I want** CLI agents to checkpoint and resume when context windows fill
**So that** long-running work doesn't fail from context exhaustion

**Acceptance Criteria:**
- [ ] Agent writes checkpoint to `.gt/` at stage boundaries
- [ ] Conductor detects context exhaustion (heartbeat degradation or explicit signal)
- [ ] Fresh session reads checkpoint and continues from last completed step
- [ ] At least one successful checkpoint + resume demonstrated

**Dependencies:** Story 8 (task assignment working)
**Complexity:** XL
**Risk:** High (context detection is imprecise)

---

### Sequencing Notes
- Stories 1-3 are Phase 1 and can start immediately
- Story 4 requires at least 2 populated semantic.json files
- Stories 6-7 are Carlos-side work, can parallel with Story 4-5
- Stories 8-9 are Phase 3, depend on stable interface contracts from Phase 2
