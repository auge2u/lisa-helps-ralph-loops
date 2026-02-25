# Efficiency Optimization Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Fix 6 correctness bugs and 2 token-efficiency issues across the lisa plugin's agents, skills, hooks, and CONTRIBUTING.md.

**Architecture:** Targeted in-place edits — no file moves, no restructuring. Correctness fixes first (Fixes 1–6), efficiency trims second (Fixes 7–8). Each fix is a standalone commit.

**Tech Stack:** Python 3 (validate.py), Markdown (skill/agent/command files), YAML (gates.yaml), pytest for smoke-testing.

**Design doc:** `docs/plans/2026-02-25-efficiency-optimization-design.md`

---

## Task 1: Fix bead schema in migrator.md (Stage 3 section)

**Files:**
- Modify: `plugins/lisa/agents/migrator.md` (Stage 3 bead schema JSON block, ~lines 125–142)

**Context:** The JSON example in the Stage 3 section uses the old schema. Five fields are wrong. The canonical schema is in `plugins/lisa/skills/structure/SKILL.md` lines 68–91.

**Step 1: Open and read the current wrong block**

In `plugins/lisa/agents/migrator.md`, find the Stage 3 bead schema block. It currently reads:

```json
{
  "$schema": "bead-v1",
  "id": "gt-abc12",
  "title": "Add user authentication",
  "type": "feature",
  "complexity": "L",
  "priority": "high",
  "acceptance_criteria": [
    "User can sign up with email",
    "User can sign in with Google OAuth"
  ],
  "evidence": {
    "source": "docs/PRD-auth.md",
    "line": 42
  }
}
```

**Step 2: Replace with canonical schema**

Replace the entire JSON block with:

```json
{
  "$schema": "bead-v1",
  "id": "gt-abc12",
  "title": "Add user authentication",
  "description": "Implement OAuth2 login flow and session management",
  "acceptance_criteria": "User can sign up with email\nUser can sign in with Google OAuth\nSession persists across page refresh",
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

Key changes:
- `"type"` → `"issue_type"`
- `"priority": "high"` → `"priority": 1`
- `"acceptance_criteria": [...]` → `"acceptance_criteria": "...\n..."` (string)
- `"complexity"` moved into `metadata`
- `"evidence"` moved into `metadata`
- Added missing fields: `description`, `status`, `assignee`, `labels`, `dependencies`

**Step 3: Verify the fix visually**

Read back the modified section and confirm all 5 field corrections are present.

**Step 4: Commit**

```bash
git add plugins/lisa/agents/migrator.md
git commit -m "fix: correct bead schema in migrator.md Stage 3

5 field errors vs canonical schema in structure/SKILL.md:
- type → issue_type
- priority string → integer
- acceptance_criteria array → newline string
- complexity/evidence promoted to metadata"
```

---

## Task 2: Fix convoy schema in migrator.md (Stage 3 section)

**Files:**
- Modify: `plugins/lisa/agents/migrator.md` (convoy schema block, ~lines 164–175)

**Context:** The convoy schema example is missing `gt_convoy_cmd`, `assigned_to`, `created`, and `metadata` fields present in the authoritative schema in `skills/structure/SKILL.md` lines 210–227.

**Step 1: Find the current convoy schema block**

In `plugins/lisa/agents/migrator.md`, find:

```json
{
  "$schema": "convoy-v1",
  "id": "convoy-001",
  "name": "Authentication Sprint",
  "description": "Implement core user authentication",
  "beads": ["gt-abc12", "gt-def34", "gt-ghi56"],
  "status": "pending"
}
```

**Step 2: Replace with complete schema**

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

**Step 3: Commit**

```bash
git add plugins/lisa/agents/migrator.md
git commit -m "fix: add missing fields to convoy schema in migrator.md

Add gt_convoy_cmd, assigned_to, created, metadata to match
authoritative schema in skills/structure/SKILL.md"
```

---

## Task 3: Fix acceptance_criteria comment in structure/SKILL.md

**Files:**
- Modify: `plugins/lisa/skills/structure/SKILL.md` (~line 289, Quality Gates table)

**Context:** The gate description says "array" but `acceptance_criteria` is a string (newline-separated), not an array. This is a documentation bug that can mislead implementers.

**Step 1: Find the line**

In `plugins/lisa/skills/structure/SKILL.md`, find the Quality Gates table entry:

```
| `beads_have_criteria` | All beads have acceptance_criteria array |
```

**Step 2: Fix the comment**

Change to:

```
| `beads_have_criteria` | All beads have acceptance_criteria string |
```

**Step 3: Commit**

```bash
git add plugins/lisa/skills/structure/SKILL.md
git commit -m "fix: correct acceptance_criteria type in structure/SKILL.md gates comment

acceptance_criteria is a newline-separated string, not an array"
```

---

## Task 4: Remove dead code from validate.py

**Files:**
- Modify: `plugins/lisa/hooks/validate.py` (lines 44–55 and line 86)

**Context:** Three things defined but never used:
1. `ALLOWED_BASE_DIRS` (line 44) — set of allowed dirs, never referenced
2. `validate_path_security()` (lines 47–55) — function defined, never called
3. `self.cwd` in `UnifiedValidator.__init__` (line 86) — assigned, never read in any method

These suggest path-traversal protection was started but never completed. Remove the dead code and add a TODO comment near `_check_file_exists` as a breadcrumb.

**Step 1: Remove `ALLOWED_BASE_DIRS` constant**

Delete line 44:
```python
ALLOWED_BASE_DIRS = {".", ".gt", "scopecraft", "./", "./.gt", "./scopecraft"}
```

**Step 2: Remove `validate_path_security()` function**

Delete lines 47–55:
```python
def validate_path_security(path: str, cwd: Path) -> Path:
    """Validate path is within working directory."""
    resolved = Path(path).resolve()
    try:
        resolved.relative_to(cwd)
        return resolved
    except ValueError:
        print(f"Security error: Path '{path}' resolves outside working directory", file=sys.stderr)
        sys.exit(3)
```

**Step 3: Remove `self.cwd` assignment**

In `UnifiedValidator.__init__`, delete line 86:
```python
self.cwd = Path.cwd().resolve()
```

**Step 4: Add a TODO breadcrumb**

In `_check_file_exists`, add a comment before the path resolution:

```python
def _check_file_exists(self, gate: dict, stage: str) -> GateResult:
    """Check if file exists."""
    # TODO: add path traversal check if validate is ever exposed as a service
    file_path = self.base_dir / gate["path"]
```

**Step 5: Run the test suite to confirm nothing broke**

```bash
cd /Users/auge2u/github/auge2u/lisa3
pip install pytest pyyaml -q
pytest tests/ -v
```

Expected: 25/25 tests pass (same as before — tests cover legacy validator, not this code, but confirms no import errors).

**Step 6: Quick smoke test**

```bash
python3 plugins/lisa/hooks/validate.py --stage discover --format text
```

Expected: runs without error (may show gate failures if no `.gt/` dir, but no Python exceptions).

**Step 7: Commit**

```bash
git add plugins/lisa/hooks/validate.py
git commit -m "fix: remove dead code from validate.py

ALLOWED_BASE_DIRS, validate_path_security(), and self.cwd were
defined but never called/used. Add TODO breadcrumb near
_check_file_exists for future path traversal protection."
```

---

## Task 5: Fix redundant exit code computation in validate.py

**Files:**
- Modify: `plugins/lisa/hooks/validate.py` (`main()` function, ~lines 818–826)

**Context:** `print_results()` returns `(blockers, warnings)` but those values are immediately overwritten at lines 821–822. The return value is always discarded. Fix: call `print_results` for its side effect only; remove the tuple unpacking.

**Step 1: Find the relevant block in `main()`**

```python
    else:
        blockers, warnings = print_results(results, args.verbose)

    # Determine exit code
    blockers = sum(1 for r in results if not r.passed and r.severity == "blocker")
    warnings = sum(1 for r in results if not r.passed and r.severity == "warning")
```

**Step 2: Remove the tuple unpacking**

Change:
```python
        blockers, warnings = print_results(results, args.verbose)
```
To:
```python
        print_results(results, args.verbose)
```

Leave lines 821–822 (`blockers = sum(...)` and `warnings = sum(...)`) as-is — these are the authoritative source for the exit code calculation regardless of output format.

**Step 3: Run smoke test**

```bash
python3 plugins/lisa/hooks/validate.py --stage discover --format text
python3 plugins/lisa/hooks/validate.py --stage discover --format json
python3 plugins/lisa/hooks/validate.py --stage discover --format markdown
```

Expected: all three complete without Python errors.

**Step 4: Commit**

```bash
git add plugins/lisa/hooks/validate.py
git commit -m "fix: remove unused return value from print_results() in main()

print_results() returns (blockers, warnings) but those values were
immediately overwritten by the sum() calls below. Call for side
effect only; exit code computation at lines 821-822 is authoritative."
```

---

## Task 6: Fix stale plugin path in CONTRIBUTING.md

**Files:**
- Modify: `CONTRIBUTING.md` (line 31, "Version locations" section)

**Context:** CONTRIBUTING.md references `plugins/ralph-it-up-roadmap/.claude-plugin/plugin.json` — the old plugin name. Plugin was renamed to `lisa`.

**Step 1: Find the stale line**

In `CONTRIBUTING.md`, under "Version locations":

```
- `plugins/ralph-it-up-roadmap/.claude-plugin/plugin.json`
```

**Step 2: Replace with correct path**

```
- `plugins/lisa/.claude-plugin/plugin.json`
```

**Step 3: Commit**

```bash
git add CONTRIBUTING.md
git commit -m "fix: update stale plugin path in CONTRIBUTING.md

plugins/ralph-it-up-roadmap was renamed to plugins/lisa"
```

---

## Task 7: Condense lookup tables in discover/SKILL.md

**Files:**
- Modify: `plugins/lisa/skills/discover/SKILL.md` (Tech Stack Extraction section, ~lines 82–123)

**Context:** Three separate detection tables (Framework, Database, Auth) have 30+ rows. These are common knowledge for Claude. Collapse to a single "Label Conventions" block that preserves output normalization without the verbose tables.

**Step 1: Find the section to replace**

In `plugins/lisa/skills/discover/SKILL.md`, find the entire "## Tech Stack Extraction" section (~lines 82–123). It contains:
- "### Framework Detection" table (10 rows)
- "### Database Detection" table (7 rows)
- "### Auth Detection" table (6 rows)

**Step 2: Replace with compact label conventions block**

Replace the three subsections with:

```markdown
## Tech Stack Extraction

Scan package and config files for dependencies, then map to canonical label names:

- **Frameworks:** "Next.js", "React", "Vue.js", "Angular", "Express.js", "Fastify", "Django", "Flask", "FastAPI", "Ruby on Rails", "Gin"
- **Databases:** "PostgreSQL", "MySQL", "MongoDB", "Redis" — include ORM if present ("Prisma", "Drizzle", "TypeORM")
- **Auth:** "Firebase Auth", "Auth0", "NextAuth.js", "Clerk", "Supabase Auth", "Passport.js"

Use exact names above. If a dependency doesn't match a known canonical name, use the package name as-is.
```

Keep everything before (the "### 1. Package Files" table) and after (the "## Output: semantic.json" section) unchanged.

**Step 3: Verify the output schema example is still intact**

Confirm the `semantic.json` example block below the trimmed section is unchanged.

**Step 4: Commit**

```bash
git add plugins/lisa/skills/discover/SKILL.md
git commit -m "perf: condense tech stack lookup tables in discover/SKILL.md

Replace 3 separate detection tables (~30 rows) with a single compact
Label Conventions block. Preserves output normalization; removes
content Claude knows natively."
```

---

## Task 8: Replace duplicate bead schema in migrator.md with reference

**Files:**
- Modify: `plugins/lisa/agents/migrator.md` (Stage 3 section — after Task 1/2 have already fixed the schemas)

**Context:** After Tasks 1 and 2, the migrator.md schemas are now correct. But the full bead JSON block is still duplicated from `structure/SKILL.md`. Replace it with a compact reference block to eliminate the maintenance surface.

**Step 1: Find the Stage 3 bead schema block**

In `plugins/lisa/agents/migrator.md`, find the "### Bead Schema" subsection under Stage 3. It now contains the corrected full JSON example (from Task 1).

**Step 2: Replace full JSON with compact reference**

Replace the entire `### Bead Schema` block (heading + JSON) with:

```markdown
### Bead Schema

Full schema: `skills/structure/SKILL.md`. Critical types to get right:
- `acceptance_criteria`: **string** (newline-separated), not array
- `priority`: **integer** (0=critical, 1=high, 2=medium, 3=low, 4=backlog), not string
- `issue_type`: field name (not `type`)
- `complexity` + `evidence` live in `metadata` (not top-level)
```

**Step 3: Verify the Convoy Schema block and ID Generation are still present**

The convoy schema (from Task 2) and "### ID Generation" section should remain unchanged below.

**Step 4: Commit**

```bash
git add plugins/lisa/agents/migrator.md
git commit -m "perf: replace duplicate bead schema in migrator.md with reference

Full schema lives in skills/structure/SKILL.md. Keep only the
critical type notes that are easy to get wrong. Eliminates the
duplication surface that caused the schema drift fixed in prior commits."
```

---

## Final Verification

**Step 1: Run full test suite**

```bash
pytest tests/ -v
```

Expected: 25/25 pass.

**Step 2: Run full validation smoke test**

```bash
python3 plugins/lisa/hooks/validate.py --stage all --format text
```

Expected: runs to completion, prints gate results (some may fail if project outputs don't exist — that's fine; no Python exceptions).

**Step 3: Verify validate.py has no import errors**

```bash
python3 -c "import plugins.lisa.hooks.validate" 2>/dev/null || python3 plugins/lisa/hooks/validate.py --help
```

Expected: help text prints cleanly.

**Step 4: Check git log**

```bash
git log --oneline -10
```

Expected: 8 new commits on top of the design doc commit.
