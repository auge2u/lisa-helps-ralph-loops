# Design: Codebase Efficiency Optimization

**Date:** 2026-02-25
**Approach:** C — Fix correctness bugs + targeted token efficiency trimming
**Scope:** `plugins/lisa/` agents, skills, hooks, and CONTRIBUTING.md

---

## Problem

Two categories of issues found through full codebase review:

1. **Correctness bugs** — `migrator.md` has a stale bead schema (5 wrong fields) that will cause agents to produce beads failing `validate.py` gates. Dead code in `validate.py` that was never wired up. Stale reference in `CONTRIBUTING.md`.

2. **Token inefficiency** — `discover/SKILL.md` has ~30 lookup-table rows Claude knows natively. `migrator.md` duplicates the bead schema from `structure/SKILL.md` — the same duplication that caused the schema drift.

---

## Correctness Fixes (8 changes)

### Fix 1 — `agents/migrator.md` bead schema (Stage 3)

5 wrong fields in the example JSON vs canonical schema in `structure/SKILL.md`:

| Current (wrong) | Correct |
|---|---|
| `"type": "feature"` | `"issue_type": "feature"` |
| `"priority": "high"` | `"priority": 1` (integer) |
| `"acceptance_criteria": [...]` | `"acceptance_criteria": "...\n..."` (string) |
| `"complexity": "L"` at top level | moved to `metadata.complexity` |
| `"evidence": {...}` at top level | moved to `metadata.evidence` |

### Fix 2 — `agents/migrator.md` convoy schema

Missing fields vs authoritative schema: `gt_convoy_cmd`, `assigned_to`, `created`, `metadata`.

### Fix 3 — `skills/structure/SKILL.md` quality gates comment

Line ~289: `"All beads have acceptance_criteria array"` → `"All beads have acceptance_criteria string"`.

### Fix 4 — `validate.py` dead code removal

- `validate_path_security()` (lines 47–55): defined, never called
- `ALLOWED_BASE_DIRS` (line 44): defined, never used
- `self.cwd` in `UnifiedValidator.__init__`: assigned, never read

Remove all three. Add a `# TODO: add path traversal protection if validate is exposed as a service` comment near `_check_file_exists`.

### Fix 5 — `validate.py` redundant exit code computation

`print_results()` returns `(blockers, warnings)` but those values are immediately overwritten at lines 821–822. Remove the tuple unpacking from the `print_results` call (call for side effect only). Lines 821–822 remain the authoritative source.

### Fix 6 — `CONTRIBUTING.md` stale plugin path

Line 31: `plugins/ralph-it-up-roadmap/.claude-plugin/plugin.json` → `plugins/lisa/.claude-plugin/plugin.json`.

---

## Token Efficiency Fixes (2 changes)

### Fix 7 — `skills/discover/SKILL.md` — Condense lookup tables

Replace the three separate Framework/Database/Auth Detection tables (~30 rows) with a single compact "Label Conventions" block:

```
### Tech Stack Label Conventions
Use canonical names:
- Frameworks: "Next.js", "React", "Vue.js", "Angular", "Express.js", "FastAPI", "Django", "Flask", "Ruby on Rails", "Gin"
- Databases: "PostgreSQL", "MySQL", "MongoDB", "Redis" + ORM if present ("Prisma", "Drizzle", "TypeORM")
- Auth: "Firebase Auth", "Auth0", "NextAuth.js", "Clerk", "Supabase Auth", "Passport.js"
```

Removes ~50 lines. Preserves output label normalization intent.

### Fix 8 — `agents/migrator.md` — Replace duplicate Stage 3 bead schema with reference

Remove the full JSON bead example from Stage 3 in migrator.md. Replace with:

```
### Bead Schema
Full schema in `skills/structure/SKILL.md`. Key types:
- `acceptance_criteria`: string (newline-separated), not array
- `priority`: integer (0=critical … 4=backlog), not string
- `issue_type`: field name (not `type`)
- `complexity` + `evidence` live in `metadata`
```

Removes ~40 lines. Eliminates the duplication surface that caused Fix 1.

---

## Files Changed

| File | Changes |
|------|---------|
| `plugins/lisa/agents/migrator.md` | Fix 1, Fix 2, Fix 8 |
| `plugins/lisa/skills/structure/SKILL.md` | Fix 3 |
| `plugins/lisa/skills/discover/SKILL.md` | Fix 7 |
| `plugins/lisa/hooks/validate.py` | Fix 4, Fix 5 |
| `CONTRIBUTING.md` | Fix 6 |

---

## Non-Goals

- No restructuring of gates.yaml or command files
- No changes to reconcile/SKILL.md, research/SKILL.md, or plan/SKILL.md
- No test changes (tests cover legacy validator, not current plugin)
- No version bump (these are internal fixes, not API changes)
