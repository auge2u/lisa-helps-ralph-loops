# Architecture v2: Staged Migration to Gastown

This document defines the refactored architecture for lisa-helps-ralph-loops, establishing a clear staged migration path from custom orchestration (ralph-it-up patterns) to native Gastown agent execution.

## Design Principles

1. **Gastown is the destination** — All custom orchestration is transitional
2. **Stages have clear boundaries** — Each stage completes before the next begins
3. **Outputs are portable** — Each stage produces artifacts usable independently
4. **No duplicate orchestration** — Remove custom loops that duplicate Gastown Mayor

## Stage Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        LISA-HELPS-RALPH-LOOPS                           │
│                     (Migration Tool - Transitional)                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐              │
│  │   STAGE 0    │───▶│   STAGE 1    │───▶│   STAGE 2    │              │
│  │   RESEARCH   │    │   DISCOVER   │    │     PLAN     │              │
│  │  (optional)  │    │              │    │  (optional)  │              │
│  └──────────────┘    └──────────────┘    └──────────────┘              │
│         │                   │                   │                       │
│         ▼                   ▼                   ▼                       │
│   .gt/research/       .gt/memory/         scopecraft/                  │
│   (rescue docs)       semantic.json       (6 .md files)                │
│                                                                         │
│                       ┌──────────────┐                                  │
│              ────────▶│   STAGE 3    │                                  │
│                       │  STRUCTURE   │                                  │
│                       └──────────────┘                                  │
│                              │                                          │
│                              ▼                                          │
│                        .gt/beads/                                       │
│                        .gt/convoys/                                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                            GASTOWN                                      │
│                    (Execution Platform - Target)                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐              │
│  │   STAGE 4    │───▶│   STAGE 5    │───▶│   STAGE 6    │              │
│  │    LOAD      │    │   EXECUTE    │    │    LEARN     │              │
│  └──────────────┘    └──────────────┘    └──────────────┘              │
│         │                   │                   │                       │
│         ▼                   ▼                   ▼                       │
│   Mayor reads         Polecats work       Memory updated               │
│   .gt/ structure      on Convoys          episodic/procedural          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Stage Definitions

### Stage 0: RESEARCH (Optional — Lost Project Rescue)

**Purpose**: Deep archaeological investigation for projects that have lost their way. Reconstructs original mission, documents drift, and creates a rescue plan.

**When to use**:
- Project has pivoted multiple times without clear documentation
- Original founders/architects have left, institutional knowledge lost
- Codebase has grown organically without coherent vision
- Technical debt has obscured original intent
- Team is unsure "what this project is even supposed to do anymore"

**Command**: `/lisa:research`

**Inputs**:
- Git history (commits, branches, tags)
- Abandoned/stale documentation
- Dead code, commented-out features
- Old PRDs, design docs, ADRs
- Legacy config files, environment hints
- Slack/Discord archives (if available)
- Old issues (closed, wontfix, abandoned)

**Process**:
1. **Timeline Reconstruction**
   - Analyze git history for major pivot points
   - Identify when scope changed (commit message patterns)
   - Map feature additions/removals over time
   - Find abandoned branches that hint at failed directions

2. **Mission Archaeology**
   - Extract original vision from earliest docs/commits
   - Identify stated goals vs actual implementation
   - Document what was promised vs what was built
   - Find the "why" behind architectural decisions

3. **Drift Analysis**
   - Compare original README to current state
   - Identify features that exist but aren't documented
   - Find documented features that don't exist
   - Map dependency growth (scope creep indicators)

4. **Stakeholder Reconstruction**
   - Identify who contributed what (git blame archaeology)
   - Find decision-makers from commit/PR patterns
   - Document tribal knowledge gaps

5. **Rescue Plan Synthesis**
   - Recommend: revive, retire, or reboot
   - If revive: what to keep, what to cut, what to document
   - If retire: graceful sunset plan, data migration needs
   - If reboot: lessons learned, what to preserve

**Output**: `.gt/research/` directory

```
.gt/research/
├── TIMELINE.md              # Git history analysis, pivot points
├── ORIGINAL_MISSION.md      # Reconstructed original vision
├── DRIFT_ANALYSIS.md        # What changed, when, why (if known)
├── STAKEHOLDER_MAP.md       # Who knew what, knowledge gaps
├── RESCUE_RECOMMENDATION.md # Revive/retire/reboot with rationale
└── evidence/
    ├── commits.json         # Key commits with analysis
    ├── abandoned.json       # Dead branches, closed issues
    └── dependencies.json    # Dependency timeline
```

**RESCUE_RECOMMENDATION.md Structure**:
```markdown
# Rescue Recommendation: [PROJECT_NAME]

## Verdict: [REVIVE | RETIRE | REBOOT]

## Executive Summary
[2-3 sentences on project state and recommendation]

## Evidence Summary
- Original mission: [extracted from earliest docs]
- Current state: [what it actually does today]
- Drift magnitude: [LOW | MEDIUM | HIGH | CRITICAL]
- Technical debt level: [estimate]
- Documentation coverage: [X% of features documented]

## If REVIVE
### Keep
- [Feature/component that aligns with mission]
- [Core value that still matters]

### Cut
- [Feature that doesn't serve mission]
- [Dead code / abandoned experiment]

### Document
- [Undocumented behavior that should stay]
- [Tribal knowledge to capture]

### Immediate Actions
1. [First thing to do]
2. [Second thing to do]

## If RETIRE
### Sunset Timeline
- [ ] Notify stakeholders
- [ ] Data export/migration plan
- [ ] Redirect/deprecation notices
- [ ] Archive date

### Preserve
- [Lessons learned]
- [Reusable components]

## If REBOOT
### Preserve from Original
- [Core concept worth keeping]
- [Architecture decision that was right]

### Abandon
- [Approach that failed]
- [Assumption that was wrong]

### New Foundation
- [What the reboot should focus on]
- [Constraints for v2]
```

**Quality Gates**:
| Gate | Requirement | Severity |
|------|-------------|----------|
| `timeline_created` | TIMELINE.md exists with 3+ pivot points | blocker |
| `mission_extracted` | ORIGINAL_MISSION.md has stated goals | blocker |
| `drift_analyzed` | DRIFT_ANALYSIS.md documents changes | blocker |
| `recommendation_made` | RESCUE_RECOMMENDATION.md has verdict | blocker |
| `evidence_collected` | 1+ evidence files in evidence/ | warning |

**Exit Criteria**: All blocker gates pass, user reviews and accepts rescue recommendation.

**What happens next**:
- If **REVIVE**: Proceed to Stage 1 (DISCOVER) with research context
- If **RETIRE**: Stop here, execute sunset plan (outside this tool's scope)
- If **REBOOT**: Create new project, optionally run RESEARCH on old one for lessons

---

### Stage 1: DISCOVER

**Purpose**: Understand the project and extract permanent facts into semantic memory.

**Command**: `/lisa:discover`

**Inputs**:
- Project source files (package.json, configs, etc.)
- Documentation (README, docs/, ADRs)
- Existing codebase structure

**Process**:
1. Scan package manifests → detect tech stack
2. Scan configs → detect services, deployment targets
3. Scan docs → extract constraints, personas, non-goals
4. Record evidence of all analyzed files

**Output**: `.gt/memory/semantic.json`

```json
{
  "$schema": "https://gastown.dev/schemas/semantic-memory-v1.json",
  "project": {
    "name": "my-app",
    "type": "web-application",
    "primary_language": "TypeScript"
  },
  "tech_stack": {
    "runtime": "Node.js 20",
    "framework": "Next.js 14",
    "database": "Neon PostgreSQL"
  },
  "constraints": ["GDPR compliant", "Offline-capable"],
  "personas": [{"name": "Developer", "needs": ["..."]}],
  "evidence": {
    "files_analyzed": ["package.json", "README.md"],
    "last_scan": "2026-01-27T10:00:00Z"
  }
}
```

**Quality Gates**:
| Gate | Requirement | Severity |
|------|-------------|----------|
| `semantic_valid` | Valid JSON | blocker |
| `project_identified` | project.name populated | blocker |
| `tech_stack_detected` | 2+ tech_stack fields | blocker |
| `evidence_recorded` | 1+ files in evidence | warning |

**Exit Criteria**: All blocker gates pass.

---

### Stage 2: PLAN

**Purpose**: Generate structured planning artifacts from scattered documentation.

**Command**: `/lisa:plan`

**Inputs**:
- `.gt/memory/semantic.json` (from Stage 1)
- PRDs, backlog files, existing roadmaps
- GitHub issues (if available)

**Process**:
1. Load semantic memory for project context
2. Scan planning documents (docs/, PRDs, backlogs)
3. Synthesize into 6 structured planning files
4. Single pass — no iteration (Gastown will handle refinement)

**Output**: `scopecraft/` directory

```
scopecraft/
├── VISION_AND_STAGE.md       # Problem, customer, next milestone
├── ROADMAP.md                # 3-5 phases with outcomes
├── EPICS_AND_STORIES.md      # Features with acceptance criteria
├── RISKS.md                  # Risk register with mitigations
├── METRICS.md                # North Star + supporting metrics
└── OPEN_QUESTIONS.md         # Blocking decisions needed
```

**Quality Gates**:
| Gate | Requirement | Severity |
|------|-------------|----------|
| `outputs_exist` | 6 .md files created | blocker |
| `phases_valid` | 3-5 phases in ROADMAP.md | blocker |
| `stories_have_criteria` | 5+ acceptance criteria sections | blocker |
| `risks_documented` | 3+ risks with type/mitigation | blocker |
| `north_star_defined` | North Star Metric present | blocker |
| `no_placeholders` | Zero [TODO]/[TBD] markers | blocker |

**Exit Criteria**: All gates pass OR user accepts incomplete output.

**Important**: This is a ONE-SHOT operation. No custom loops. If output is incomplete, user can:
1. Re-run with better source docs
2. Manually edit scopecraft/ files
3. Proceed to Stage 3 with partial planning (Gastown agents can refine)

---

### Stage 3: STRUCTURE

**Purpose**: Transform planning artifacts into Gastown-native work items.

**Command**: `/lisa:structure`

**Inputs**:
- `.gt/memory/semantic.json` (from Stage 1)
- `scopecraft/*.md` (from Stage 2, optional)
- GitHub issues, TODO comments, backlog files

**Process**:
1. Extract work items from all sources
2. Deduplicate (same item from multiple sources → single bead)
3. Generate bead for each unique work item
4. Bundle related beads into convoys (3-7 per convoy)

**Output**: `.gt/beads/` and `.gt/convoys/`

**Bead Schema** (`.gt/beads/gt-xxxxx.json`):
```json
{
  "$schema": "https://gastown.dev/schemas/bead-v1.json",
  "id": "gt-abc12",
  "title": "Add user authentication",
  "type": "feature",
  "complexity": "L",
  "status": "pending",
  "acceptance_criteria": [
    "User can sign up with email",
    "Session persists across refresh"
  ],
  "sources": [
    {"type": "prd", "file": "docs/PRD.md", "line": 42},
    {"type": "issue", "ref": "GH-123"}
  ],
  "metadata": {
    "epic": "User Management",
    "labels": ["auth", "security"],
    "scopecraft_ref": "EPICS_AND_STORIES.md#story-1-1"
  }
}
```

**Convoy Schema** (`.gt/convoys/convoy-NNN.json`):
```json
{
  "$schema": "https://gastown.dev/schemas/convoy-v1.json",
  "id": "convoy-001",
  "name": "Authentication Sprint",
  "description": "Core user auth features",
  "beads": ["gt-abc12", "gt-def34", "gt-ghi56"],
  "strategy": "by_epic",
  "status": "pending",
  "metadata": {
    "epic": "User Management",
    "phase": "Phase 1"
  }
}
```

**Quality Gates**:
| Gate | Requirement | Severity |
|------|-------------|----------|
| `beads_extracted` | 1+ beads created | blocker |
| `beads_have_criteria` | All beads have 2+ acceptance criteria | blocker |
| `beads_have_sources` | All beads link to source | blocker |
| `beads_unique` | No duplicate bead IDs | blocker |
| `convoy_created` | 1+ convoy created | blocker |
| `convoy_size_valid` | All convoys have 3-7 beads | warning |
| `convoy_beads_exist` | All referenced beads exist | blocker |
| `convoy_strategy_coherent` | Beads in convoy share metadata trait | warning |

**Exit Criteria**: All blocker gates pass.

---

### Stages 4-6: GASTOWN EXECUTION

These stages are **outside this plugin's scope**. Gastown handles:

**Stage 4: LOAD**
- Mayor reads `.gt/` directory
- Loads semantic memory for context
- Indexes available beads and convoys

**Stage 5: EXECUTE**
- Mayor assigns convoys to Polecats
- Polecats work on beads, update status
- Mayor coordinates, handles blockers

**Stage 6: LEARN**
- Completed work updates episodic memory (decisions made)
- Patterns discovered update procedural memory
- Memory persists for future runs

---

## Command Mapping

### New Commands (v2)

| Command | Stage | Purpose |
|---------|-------|---------|
| `/lisa:research` | 0 | Deep dive into lost project, create rescue plan |
| `/lisa:discover` | 1 | Extract semantic memory |
| `/lisa:plan` | 2 | Generate planning artifacts (one-shot) |
| `/lisa:structure` | 3 | Create beads and convoys |
| `/lisa:migrate` | 1+2+3 | Full migration pipeline (skips research) |
| `/lisa:rescue` | 0+1+2+3 | Full pipeline starting with research |
| `/lisa:status` | — | Show current stage, gate results |

### Deprecated Commands

| Old Command | Replacement | Reason |
|-------------|-------------|--------|
| `/lisa-loops-memory:analyze` | `/lisa:discover` | Renamed for clarity |
| `/lisa-loops-memory:beads` | `/lisa:structure` | Merged with convoy |
| `/lisa-loops-memory:convoy` | `/lisa:structure` | Merged with beads |
| `/lisa-loops-memory:roadmap` | `/lisa:plan` | Renamed, simplified |
| `/lisa-loops-memory:roadmap-native` | **REMOVED** | Custom loops → Gastown |
| `/lisa-loops-memory:roadmap-orchestrated` | **REMOVED** | Custom loops → Gastown |

### Deprecation Timeline

```
v0.2.x (current)  — All commands available, deprecation warnings added
v0.3.0            — New commands available, old commands warn + redirect
v0.4.0            — Old commands removed, clean v2 API only
v1.0.0            — Stable release with Gastown Mayor API integration
```

---

## Data Flow

```
                                        ┌─────────────────┐
                                        │  Project Files  │
                                        │  (source code,  │
                                        │   docs, config) │
                                        └────────┬────────┘
                                                 │
        ┌────────────────────────────────────────┼────────────────┐
        │                                        │                │
        ▼                                        │                │
  ┌───────────┐                                  │                │
  │  Stage 0  │ (optional: lost projects only)   │                │
  │ RESEARCH  │                                  │                │
  └─────┬─────┘                                  │                │
        │                                        │                │
        ▼                                        ▼                │
  ┌───────────┐                           ┌───────────┐          │
  │.gt/research│                          │  Stage 1  │          │
  │(rescue docs)│─────────────────────────│ DISCOVER  │          │
  └───────────┘   (context for discovery) └─────┬─────┘          │
                                                │                │
                                                ▼                │
                                         ┌────────────┐          │
                                         │ .gt/memory │          │
                                         │ semantic   │          │
                                         └─────┬──────┘          │
                                               │                 │
                         ┌─────────────────────┼─────────────────┘
                         │                     │
                         ▼                     ▼
                   ┌───────────┐         ┌──────────┐
                   │  Stage 2  │         │ Stage 3  │
                   │   PLAN    │────────▶│STRUCTURE │
                   │(optional) │         │          │
                   └─────┬─────┘         └────┬─────┘
                         │                    │
                         ▼                    ▼
                  ┌────────────┐        ┌────────────┐
                  │ scopecraft │        │ .gt/beads  │
                  │ (6 files)  │        │ .gt/convoys│
                  └────────────┘        └──────┬─────┘
                                               │
                                               ▼
                                     ┌─────────────────┐
                                     │    GASTOWN      │
                                     │     MAYOR       │
                                     │  (reads .gt/)   │
                                     └─────────────────┘
```

### Stage Dependencies

| Stage | Requires | Optional Input |
|-------|----------|----------------|
| 0. RESEARCH | Git history, old docs | Slack archives, old issues |
| 1. DISCOVER | Project files | Stage 0 output (research context) |
| 2. PLAN | Stage 1 output | PRDs, backlogs |
| 3. STRUCTURE | Stage 1 output | Stage 2 output, GitHub issues |

**Key insights**:
- **Stage 0 (RESEARCH)** is optional — only for lost/confused projects needing rescue
- **Stage 2 (PLAN)** is optional — skip if work items already exist elsewhere
- Direct paths: DISCOVER → STRUCTURE (if planning done externally)
- Full rescue: RESEARCH → DISCOVER → PLAN → STRUCTURE

---

## Removed Concepts

### Custom Orchestration Loop

**What it was**:
```
roadmap-native / roadmap-orchestrated:
  while iteration < 15:
    generate outputs
    run quality gates
    if all pass: LOOP_COMPLETE
    else: update scratchpad, retry
```

**Why removed**:
- Duplicates Gastown Mayor's orchestration
- Custom memory (.agent/scratchpad.md) conflicts with Gastown memory
- LOOP_COMPLETE signal is Gastown-incompatible
- Iteration limits are arbitrary (Gastown handles resource management)

**Replacement**: One-shot generation + Gastown refinement

If Stage 2 output is incomplete:
1. User reviews scopecraft/ files
2. User re-runs `/lisa:plan` with better inputs, OR
3. User proceeds to Stage 3 (partial planning is acceptable)
4. Gastown agents can refine during execution

### ralph-orchestrator Integration

**What it was**: External process controlling iteration loop

**Why removed**:
- Gastown Mayor IS the orchestrator
- External orchestration adds complexity without value
- ralph-orchestrator protocol (scratchpad, LOOP_COMPLETE) not Gastown-native

**Replacement**: Direct Gastown Mayor API integration (v1.0.0 target)

---

## Memory Architecture

### This Plugin Creates (Stages 0-3)

| File | Type | Created By | Purpose |
|------|------|------------|---------|
| `.gt/research/*.md` | Rescue docs | Stage 0 | Project archaeology |
| `.gt/research/evidence/*.json` | Evidence | Stage 0 | Historical data |
| `.gt/memory/semantic.json` | Permanent | Stage 1 | Project facts |
| `scopecraft/*.md` | Planning | Stage 2 | Human-readable roadmap |
| `.gt/beads/*.json` | Work items | Stage 3 | Individual tasks |
| `.gt/convoys/*.json` | Work bundles | Stage 3 | Grouped assignments |

### Gastown Creates (Stages 4-6)

| File | Type | Created By | Purpose |
|------|------|------------|---------|
| `.gt/memory/episodic.json` | Temporal | Gastown | Decisions with TTL |
| `.gt/memory/procedural.json` | Learned | Gastown | Patterns discovered |
| `.gt/beads/*.json` | Updated | Gastown | Status changes |
| `.gt/convoys/*.json` | Updated | Gastown | Assignment, completion |

**Separation of concerns**:
- This plugin: Creates initial structure (write)
- Gastown: Updates during execution (read/write)

---

## Validation Architecture

### Single Validator

Consolidate `validate_gastown.py` and `validate_quality_gates.py` into one:

```
plugins/lisa/
  hooks/
    validate.py           # Unified validator
```

**CLI Interface**:
```bash
# Validate specific stage
python -m lisa.validate --stage research
python -m lisa.validate --stage discover
python -m lisa.validate --stage plan
python -m lisa.validate --stage structure

# Validate all completed stages
python -m lisa.validate --all

# Output formats
python -m lisa.validate --stage research --format json
python -m lisa.validate --stage discover --format markdown
```

**Programmatic Interface**:
```python
from lisa.validate import StageValidator

validator = StageValidator(base_dir=".")
results = validator.validate_stage("discover")
# results: List[GateResult]

report = validator.generate_report(results, format="markdown")
```

### Gate Registry

All gates defined in single configuration:

```yaml
# lisa/gates.yaml
stages:
  research:
    gates:
      - id: timeline_created
        check: pattern_count
        path: .gt/research/TIMELINE.md
        pattern: "## Pivot"
        min: 3
        severity: blocker
      - id: mission_extracted
        check: file_exists
        path: .gt/research/ORIGINAL_MISSION.md
        severity: blocker
      - id: drift_analyzed
        check: file_exists
        path: .gt/research/DRIFT_ANALYSIS.md
        severity: blocker
      - id: recommendation_made
        check: pattern_exists
        path: .gt/research/RESCUE_RECOMMENDATION.md
        pattern: "## Verdict: (REVIVE|RETIRE|REBOOT)"
        severity: blocker
      - id: evidence_collected
        check: file_count
        path: .gt/research/evidence/*.json
        min: 1
        severity: warning

  discover:
    gates:
      - id: semantic_valid
        check: json_valid
        path: .gt/memory/semantic.json
        severity: blocker
      - id: project_identified
        check: json_field_present
        path: .gt/memory/semantic.json
        field: project.name
        severity: blocker
      # ...

  plan:
    gates:
      - id: outputs_exist
        check: file_count
        path: scopecraft/*.md
        expect: 6
        severity: blocker
      # ...

  structure:
    gates:
      - id: beads_extracted
        check: file_count
        path: .gt/beads/gt-*.json
        min: 1
        severity: blocker
      # ...
```

---

## Migration Path for Existing Users

### From v0.2.x to v0.3.0

1. **Rename commands in scripts**:
   ```bash
   # Old
   /lisa-loops-memory:analyze
   /lisa-loops-memory:roadmap

   # New
   /lisa:discover
   /lisa:plan
   ```

2. **Remove orchestration dependencies**:
   - Delete `.agent/` directory (custom memory)
   - Delete `ralph.yml` if present
   - Remove ralph-orchestrator from workflow

3. **Update validation calls**:
   ```bash
   # Old
   python plugins/lisa-loops-memory/hooks/validate_gastown.py
   python plugins/lisa-loops-memory/hooks/validate_quality_gates.py

   # New
   python -m lisa.validate --all
   ```

### From v0.3.0 to v1.0.0

1. **Gastown integration**:
   - Ensure Gastown is installed and configured
   - Run `/lisa:migrate` to prepare project
   - Hand off to Gastown Mayor for execution

---

## File Structure (v2)

```
lisa-helps-ralph-loops/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   └── lisa/                          # Renamed from lisa-loops-memory
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── commands/
│       │   ├── research.md            # Stage 0 (lost project rescue)
│       │   ├── discover.md            # Stage 1
│       │   ├── plan.md                # Stage 2
│       │   ├── structure.md           # Stage 3
│       │   ├── migrate.md             # Full pipeline (1+2+3)
│       │   ├── rescue.md              # Full rescue (0+1+2+3)
│       │   └── status.md              # Show progress
│       ├── agents/
│       │   ├── archaeologist.md       # Stage 0: research specialist
│       │   └── migrator.md            # Stages 1-3: migration specialist
│       ├── skills/
│       │   ├── research/
│       │   │   ├── SKILL.md           # Archaeological investigation
│       │   │   └── templates/         # Rescue doc templates
│       │   ├── discover/
│       │   │   └── SKILL.md
│       │   ├── plan/
│       │   │   ├── SKILL.md
│       │   │   └── templates/         # Output templates
│       │   └── structure/
│       │       ├── SKILL.md
│       │       └── templates/         # Bead/convoy templates
│       ├── hooks/
│       │   └── validate.py            # Unified validator
│       ├── gates.yaml                 # Gate definitions
│       └── examples/
│           ├── research/              # Sample rescue docs
│           ├── discover/              # Sample semantic.json
│           ├── plan/                  # Sample scopecraft/
│           └── structure/             # Sample beads/convoys
├── docs/
│   ├── ARCHITECTURE_V2.md             # This document
│   ├── MIGRATION_GUIDE.md             # User migration instructions
│   └── GASTOWN_INTEGRATION.md         # Mayor API details
├── tests/
│   ├── test_research.py
│   ├── test_discover.py
│   ├── test_plan.py
│   ├── test_structure.py
│   └── test_validate.py
└── CLAUDE.md
```

---

## Implementation Phases

### Phase 1: Foundation (v0.3.0)

- [ ] Rename plugin: `lisa-loops-memory` → `lisa`
- [ ] Create new command files (research, discover, plan, structure, migrate, rescue, status)
- [ ] Create archaeologist agent for research stage
- [ ] Add deprecation warnings to old commands
- [ ] Consolidate validators into single `validate.py`
- [ ] Create `gates.yaml` configuration
- [ ] Update CLAUDE.md

### Phase 2: Cleanup (v0.4.0)

- [ ] Remove old commands (analyze, beads, convoy, roadmap-*)
- [ ] Remove `.agent/` memory system
- [ ] Remove ralph-orchestrator integration
- [ ] Remove dual validator (bash)
- [ ] Add comprehensive tests

### Phase 3: Integration (v1.0.0)

- [ ] Gastown Mayor API integration
- [ ] Automatic handoff after Stage 3
- [ ] Bidirectional memory sync
- [ ] Status command shows Gastown execution state

---

## Success Criteria

### v0.3.0

- [ ] New commands work end-to-end
- [ ] Old commands show deprecation warning but still function
- [ ] Single validator covers all stages
- [ ] 80% test coverage on validator

### v0.4.0

- [ ] Clean API (no legacy commands)
- [ ] No custom orchestration code
- [ ] Documentation updated
- [ ] Migration guide published

### v1.0.0

- [ ] Gastown Mayor reads .gt/ structure successfully
- [ ] Polecats can execute convoys created by this plugin
- [ ] Memory persists across Gastown sessions
- [ ] Zero manual handoff required
