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

```json
{
  "$schema": "bead-v1",
  "id": "gt-abc12",
  "title": "Add user authentication",
  "type": "feature",
  "complexity": "L",
  "priority": "high",
  "status": "pending",
  "dependencies": [],
  "acceptance_criteria": [
    "User can sign up with email",
    "User can sign in with Google OAuth",
    "Session persists across page refresh"
  ],
  "evidence": {
    "source": "docs/PRD-auth.md",
    "line": 42,
    "extracted": "2026-01-27T10:00:00Z"
  },
  "metadata": {
    "epic": "User Management",
    "labels": ["auth", "security"]
  }
}
```

### Bead Types

| Type | Description | Source Indicators |
|------|-------------|-------------------|
| `feature` | New functionality | PRDs, user stories, feature requests |
| `bug` | Defect fix | FIXME comments, bug issues |
| `chore` | Maintenance, refactoring | HACK comments, tech debt |
| `docs` | Documentation | README updates, API docs |
| `spike` | Research/investigation | Questions, unknowns |

### Complexity Estimates

| Size | Description | Typical Effort |
|------|-------------|----------------|
| `XS` | Trivial change | < 1 hour |
| `S` | Small task | 1-4 hours |
| `M` | Medium task | 1-2 days |
| `L` | Large task | 3-5 days |
| `XL` | Epic-sized | 1-2 weeks |

### ID Generation

Bead IDs follow Gastown convention: `gt-<5-char-alphanumeric>`

- Use lowercase letters and numbers only
- Examples: `gt-abc12`, `gt-xyz99`, `gt-m4n5p`

Generate unique IDs:
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
- [ ] At least 1 acceptance criterion
- [ ] Evidence linking to source file
- [ ] Valid complexity estimate (XS/S/M/L/XL)
- [ ] Unique ID in `gt-xxxxx` format

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
  "metadata": {
    "epic": "User Management",
    "estimated_days": 5
  }
}
```

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
| `beads_have_criteria` | All beads have acceptance_criteria array |
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

After structure completes, Gastown Mayor can:

1. **Read Memory**: Load `.gt/memory/semantic.json` for project context
2. **List Beads**: Enumerate `.gt/beads/*.json` for available work
3. **Assign Convoys**: Create/assign convoys to Polecats
4. **Track Progress**: Update bead/convoy status as work completes

### Status Transitions

```
Bead:   pending -> in_progress -> completed | blocked
Convoy: pending -> assigned -> in_progress -> completed
```

---

## Templates

See `templates/` directory for JSON templates:
- `templates/bead.json` - Bead template
- `templates/convoy.json` - Convoy template
