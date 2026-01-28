# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**lisa-helps-ralph-loops** is a Claude Code plugin that migrates projects to [Gastown](https://github.com/steveyegge/gastown) format. It analyzes codebases, extracts work items as Beads, bundles them into Convoys, and generates `.gt/` directory structure for multi-agent execution.

**Version:** 0.3.0 | **Primary plugin:** `plugins/lisa/`

## Development Commands

```bash
# Run tests
pytest tests/ -v

# Run specific test
pytest tests/test_validate_quality_gates.py::TestPathSecurity -v

# Validate plugin outputs
python3 plugins/lisa/hooks/validate.py --stage discover
python3 plugins/lisa/hooks/validate.py --workflow migrate --format json
```

## Plugin Architecture

The `lisa` plugin uses a 4-stage pipeline. Each stage has corresponding files:

| Stage | Command | Skill | Agent | Output |
|-------|---------|-------|-------|--------|
| 0 | `research.md` | `research/SKILL.md` | `archaeologist.md` | `.gt/research/` |
| 1 | `discover.md` | `discover/SKILL.md` | `migrator.md` | `.gt/memory/` |
| 2 | `plan.md` | `plan/SKILL.md` | `migrator.md` | `scopecraft/` |
| 3 | `structure.md` | `structure/SKILL.md` | `migrator.md` | `.gt/beads/`, `.gt/convoys/` |

### File Relationships

```
commands/*.md     → References skill + agent in YAML frontmatter
skills/*/SKILL.md → Detailed procedures, references templates/
agents/*.md       → AI persona definitions with capabilities
gates.yaml        → Single source of truth for quality gates
hooks/validate.py → Loads gates.yaml, validates outputs
```

### Key Files

- **`gates.yaml`** — Defines all 22 quality gates across 4 stages. Edit this to change validation rules.
- **`validate.py`** — Unified validator. Supports `--stage`, `--workflow`, `--format` flags.
- **`.claude-plugin/marketplace.json`** — Plugin registry. Update version here when releasing.

### Command Frontmatter Pattern

All commands use this YAML frontmatter structure:
```yaml
---
description: Brief description
skill: skill-name          # Must exist in skills/
agent: agent-name          # Must exist in agents/
stage: 0-3                 # Pipeline stage number
---
```

## Gastown Concepts

| Term | Description |
|------|-------------|
| **Bead** | Work item with ID `gt-xxxxx`, acceptance criteria, evidence |
| **Convoy** | Bundle of 3-7 related beads for assignment |
| **Memory** | Semantic (facts), episodic (decisions), procedural (patterns) |

## Validation

Quality gates are defined in `gates.yaml` with these check types:
- `file_exists`, `file_count` — Check files exist
- `json_valid`, `json_field_present`, `json_field_count` — Validate JSON structure
- `pattern_exists`, `pattern_count` — Regex matching in files
- `cross_reference` — Verify references between files

Exit codes: `0`=pass, `1`=blocker, `2`=warning, `3`=security error

## Adding New Stages/Gates

1. Add stage to `gates.yaml` under `stages:`
2. Create `commands/<name>.md` with proper frontmatter
3. Create `skills/<name>/SKILL.md` with procedures
4. Create templates in `skills/<name>/templates/`
5. Update workflows in `gates.yaml` if needed
6. Run `python3 plugins/lisa/hooks/validate.py --stage <name>` to test
