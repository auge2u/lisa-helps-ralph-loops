---
name: structure
description: Extracts work items as Beads and bundles them into Convoys for Gastown multi-agent execution.
stage: 3
---

# Structure Skill (Stage 3)

This skill extracts work items from the project and structures them as Gastown Beads and Convoys.

## When to Use

Use this skill when:
- Have completed Stage 1 (Discover) and optionally Stage 2 (Plan)
- Ready to create actionable work items
- Want to structure work for Gastown multi-agent execution
- Need to bundle related tasks for efficient assignment

## Output Structure

```
project/
├── .gt/
│   ├── beads/
│   │   ├── gt-abc12.json    # Individual work items
│   │   ├── gt-def34.json
│   │   └── ...
│   └── convoys/
│       ├── convoy-001.json  # Bundled work assignments
│       └── ...
└── [existing project files]
```

---

## Part 1: Bead Extraction

### Extraction Sources (Priority Order)

Scan for work items in:

1. **GitHub Issues** (most authoritative)
   ```bash
   gh issue list --state open --json number,title,body,labels
   ```

2. **PRD Documents**
   - `docs/*.md` with user stories
   - `docs/PRD*.md` files

3. **TODO Comments in Source Code**
   - `// TODO:`, `# TODO:`, `/* TODO */`
   - `// FIXME:`, `// HACK:`, `// XXX:`

4. **Existing Roadmap Outputs**
   - `scopecraft/EPICS_AND_STORIES.md` (from Stage 2)
   - `scopecraft/OPEN_QUESTIONS.md`

5. **Backlog Files**
   - `BACKLOG.md`, `TODO.md`
   - `docs/backlog/`, `docs/roadmap/`

### Bead Schema

Aligned with the real `bd` Issue schema (from `github.com/steveyegge/beads`):

```json
{
  "$schema": "bead-v1",
  "id": "gt-abc12",
  "title": "Add user authentication",
  "description": "Implement OAuth2 login flow and session management",
  "design": "Use Passport.js with Google and GitHub strategies",
  "acceptance_criteria": "User can sign up with email\nUser can sign in with Google OAuth\nSession persists across page refresh",
  "notes": "See docs/PRD-auth.md for background",
  "issue_type": "feature",
  "priority": 1,
  "status": "open",
  "assignee": "",
  "labels": ["auth", "security"],
  "dependencies": [],
  "metadata": {
    "complexity": "L",
    "epic": "User Management",
    "evidence": {
      "source": "docs/PRD-auth.md",
      "line": 42,
      "extracted": "2026-01-27T10:00:00Z"
    }
  }
}
```

**Schema notes (from real `bd` types):**
- `acceptance_criteria` is a **string** (newline-separated), not an array
- `priority` is an **integer**: 0=critical, 1=high, 2=medium, 3=low, 4=backlog
- `status` is `open` (not `pending`) — real values: open | in_progress | blocked | deferred | closed
- `issue_type` maps directly to `bd` types (not `type`)
- `complexity` and `evidence` live in `metadata` (not top-level `bd` fields)

### Issue Types

| Type | Description | Source Indicators |
|------|-------------|-------------------|
| `feature` | New functionality | PRDs, user stories, feature requests |
| `bug` | Defect fix | FIXME comments, bug issues |
| `task` | Generic work item | TODO comments, operational tasks |
| `chore` | Maintenance, refactoring | HACK comments, tech debt |
| `epic` | Large feature container | Feature areas, milestones |
| `decision` | Architecture decision | ADRs, design docs |

### Priority Values

| Value | Label | Description |
|-------|-------|-------------|
| 0 | P0 / critical | Blockers, production issues |
| 1 | P1 / high | Sprint priorities |
| 2 | P2 / medium | Normal work (default) |
| 3 | P3 / low | Nice-to-have |
| 4 | P4 / backlog | Future consideration |

### Complexity Estimates (metadata only)

| Size | Description | Typical Effort |
|------|-------------|----------------|
| `XS` | Trivial change | < 1 hour |
| `S` | Small task | 1-4 hours |
| `M` | Medium task | 1-2 days |
| `L` | Large task | 3-5 days |
| `XL` | Epic-sized | 1-2 weeks |

### ID Generation

Bead IDs use the rig prefix + 5-char alphanumeric. For the gastown rig the prefix is `gt-`:

```python
import random
import string
def generate_bead_id():
    chars = string.ascii_lowercase + string.digits
    return f"gt-{''.join(random.choices(chars, k=5))}"
```

### Bead Quality Requirements

Every bead must have:
- [ ] Clear, actionable title
- [ ] Substantive description (why + what)
- [ ] Acceptance criteria (as newline-separated string)
- [ ] Evidence in metadata linking to source file
- [ ] Valid complexity in metadata (XS/S/M/L/XL)
- [ ] Unique ID in `gt-xxxxx` format

### bd CLI Integration

Lisa's `.gt/beads/*.json` files are a staging format. To create real `bd` issues:

```bash
# Option 1: Import from a markdown file Lisa generates
bd create --file=.gt/beads/bd-import.md

# Option 2: Create one at a time (for scripting)
bd create "Add user authentication" \
  --type=feature --priority=1 \
  --acceptance="User can sign up with email\nSession persists" \
  --description="Implement OAuth2 login"

# Check unblocked work
bd ready

# Claim and complete
bd update gt-abc12 --status=in_progress
bd close gt-abc12
bd sync  # commit beads changes to git
```

---

## Part 2: Convoy Bundling

### Convoy Creation Rules

| Rule | Requirement |
|------|-------------|
| Size | 3-7 beads per convoy (optimal batch) |
| Coherence | Related beads grouped together |
| Dependencies | Respect bead dependency order |
| Parallelization | Independent convoys can run concurrently |

### Bundling Strategies

1. **By Epic**
   - Group all beads from same epic/feature area
   - Best for feature-focused sprints

2. **By Dependency Chain**
   - Chain dependent beads sequentially
   - Best for complex features with prerequisites

3. **By Skill**
   - Group beads requiring similar expertise
   - Best for specialist assignment

4. **By Size**
   - Combine small beads (XS/S) together
   - Isolate large beads (L/XL)
   - Best for balanced workloads

### Convoy Schema

```json
{
  "$schema": "convoy-v1",
  "id": "convoy-001",
  "name": "Authentication Sprint",
  "description": "Implement core user authentication features",
  "beads": ["gt-abc12", "gt-def34", "gt-ghi56"],
  "assigned_to": null,
  "status": "pending",
  "created": "2026-01-27T10:00:00Z",
  "gt_convoy_cmd": "gt convoy create \"Authentication Sprint\" gt-abc12 gt-def34 gt-ghi56",
  "metadata": {
    "epic": "User Management",
    "estimated_days": 5
  }
}
```

The `gt_convoy_cmd` field is the actual `gt` CLI command to create this convoy in a live Gastown environment. Polecats are assigned via `gt sling <bead-id> <rig>`.

### ID Generation

Convoy IDs: `convoy-` + 3-digit number

- Sequential numbering: `convoy-001`, `convoy-002`, etc.
- Pad with zeros for sorting

### Convoy Quality Requirements

Every convoy must have:
- [ ] 3-7 beads (optimal batch size)
- [ ] Coherent theme (epic, skill, or dependency chain)
- [ ] All referenced beads exist in `.gt/beads/`
- [ ] Clear description of bundle purpose

---

## Execution Procedure

### Step 1: Create Directories

```bash
mkdir -p .gt/beads .gt/convoys
```

### Step 2: Extract Beads

For each source:
1. Scan for work items
2. Extract title, description, criteria
3. Classify type and complexity
4. Generate unique ID
5. Link evidence to source
6. Write to `.gt/beads/gt-xxxxx.json`

### Step 3: Bundle into Convoys

1. Group beads by chosen strategy
2. Ensure 3-7 beads per convoy
3. Verify all bead references exist
4. Generate convoy ID
5. Write to `.gt/convoys/convoy-xxx.json`

### Step 4: Validate

```bash
python plugins/lisa/hooks/validate.py --stage structure
```

---

## Quality Gates

### Bead Gates

| Gate | Requirement |
|------|-------------|
| `beads_extracted` | At least 1 bead created |
| `beads_have_criteria` | All beads have acceptance_criteria string |
| `beads_have_sources` | All beads have evidence.source |
| `beads_valid_ids` | All IDs match `gt-[a-z0-9]{5}` pattern |

### Convoy Gates

| Gate | Requirement |
|------|-------------|
| `convoy_created` | At least 1 convoy created |
| `convoy_size_valid` | All convoys have 3-7 beads |
| `convoy_beads_exist` | All referenced bead IDs exist in `.gt/beads/` |

---

## Integration with Gastown

Lisa's `.gt/beads/` and `.gt/convoys/` are **staging directories**. The real Gastown toolchain uses:

- **`bd`** — the beads CLI (issue tracking, Dolt-backed SQL database in `.beads/`)
- **`bv`** — the graph analysis CLI (read-only, use `bv --robot-triage` not bare `bv`)
- **`gt`** — the Gastown workspace manager (convoys, polecats, rigs, worktrees)

### Live Integration Workflow

```bash
# 1. Create real bd issues from Lisa's staging beads
#    Either run individual bd create commands, or produce a markdown file:
bd create --file=.gt/beads/bd-import.md

# 2. Create a convoy in Gastown from the bead IDs
gt convoy create "Authentication Sprint" gt-abc12 gt-def34 gt-ghi56

# 3. Sling work to polecats (ephemeral workers) or crew
gt sling gt-abc12 <rig>           # assign to a polecat on the rig
gt convoy status hq-cv-abc        # track convoy progress

# 4. Workers pick up and complete
bd ready                          # see unblocked work
bd update gt-abc12 --status=in_progress
bd close gt-abc12
bd sync                           # commit beads changes to git
```

### Real Bead Status Values

```
open → in_progress → closed
         ↓
       blocked
       deferred
```

### The Propulsion Principle

Gastown agents follow: **"If you find something on your hook, YOU RUN IT."**
When a bead is slotted to a polecat, it executes immediately — no confirmation needed.
Lisa's quality gates and acceptance criteria are what make that safe to do.

---

## Templates

See `templates/` directory for JSON templates:
- `templates/bead.json` - Bead template
- `templates/convoy.json` - Convoy template
