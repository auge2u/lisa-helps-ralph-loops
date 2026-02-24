# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**lisa-helps-ralph-loops** is a Claude Code plugin that migrates projects to [Gastown](https://github.com/steveyegge/gastown) format. It analyzes codebases, extracts work items as Beads, bundles them into Convoys, and generates `.gt/` directory structure for multi-agent execution.

**Version:** 0.3.0 | **Primary plugin:** `plugins/lisa/`

## Development Commands

```bash
# Run tests (requires PyYAML; system Python may lack it — use a venv if needed)
pip install pytest pyyaml
pytest tests/ -v

# Run specific test class or method
pytest tests/test_validate_quality_gates.py::TestPathSecurity -v

# Validate plugin outputs against quality gates
python3 plugins/lisa/hooks/validate.py --stage discover
python3 plugins/lisa/hooks/validate.py --workflow migrate --format json
python3 plugins/lisa/hooks/validate.py --stage all --format markdown

# Bump version (updates plugin.json + marketplace.json + CHANGELOG.md)
./scripts/bump-version.sh 0.4.0        # bump only
./scripts/bump-version.sh 0.4.0 --tag  # bump + git tag
```

## Two-Plugin Structure

The repo contains two plugins. Only `lisa` is active:

| Plugin | Status | Path |
|--------|--------|------|
| `lisa` | **Active (v0.3.0)** | `plugins/lisa/` |
| `lisa-loops-memory` | Deprecated (v0.2.0) | `plugins/lisa-loops-memory/` |

The marketplace registry at `.claude-plugin/marketplace.json` lists both; `lisa-loops-memory` has `"deprecated": true`.

**Note:** The existing tests in `tests/test_validate_quality_gates.py` import from the **legacy** `lisa-loops-memory` validator (`validate_quality_gates.py`), not the current `plugins/lisa/hooks/validate.py`. These are different implementations — the active one uses `gates.yaml` while the legacy one has hardcoded gates.

## Plugin Architecture

The `lisa` plugin uses a 5-stage pipeline. Each stage has corresponding files:

| Stage | Command | Skill | Agent | Output |
|-------|---------|-------|-------|--------|
| 0 | `research.md` | `research/SKILL.md` | `archaeologist.md` | `.gt/research/` |
| 1 | `discover.md` | `discover/SKILL.md` | `migrator.md` | `.gt/memory/` |
| 2 | `plan.md` | `plan/SKILL.md` | `migrator.md` | `scopecraft/` |
| 3 | `structure.md` | `structure/SKILL.md` | `migrator.md` | `.gt/beads/`, `.gt/convoys/` |
| 5 | `reconcile.md` | `reconcile/SKILL.md` | `migrator.md` | `scopecraft/` (alignment) |

Stage 4 is intentionally reserved/skipped; reconcile is numbered 5 to allow a future stage 4 insertion.

Composite commands run multiple stages sequentially:
- **`migrate.md`** — Stages 1-3 (discover + plan + structure)
- **`rescue.md`** — Stages 0-3 (research + discover + plan + structure)
- **`status.md`** — Detects completed stages and runs their quality gates

### File Relationships

```
commands/*.md     → References skill + agent in YAML frontmatter
skills/*/SKILL.md → Detailed procedures, references templates/
agents/*.md       → AI persona definitions with capabilities
gates.yaml        → Single source of truth for quality gates
hooks/validate.py → Loads gates.yaml, validates outputs
```

### Key Files

- **`gates.yaml`** — Defines all 31 quality gates across 5 stages (research, discover, plan, structure, reconcile). Edit this to change validation rules.
- **`~/.lisa/ecosystem.json`** — Ecosystem config listing project paths and git remotes for reconcile (Stage 5). Schema v2 supports `remote` field for portable identification. Created manually; schema defined in `skills/reconcile/SKILL.md`.
- **`validate.py`** — Unified validator. Supports `--stage`, `--workflow`, `--format` flags. Auto-detects `gates.yaml` location. Runs in fallback mode without PyYAML (JSON/file checks only; pattern checks skipped).
- **`.claude-plugin/marketplace.json`** — Plugin registry. Update version here when releasing (must stay in sync with `plugins/lisa/.claude-plugin/plugin.json`).

### Command Frontmatter Pattern

All commands use this YAML frontmatter structure:
```yaml
---
description: Brief description
skill: skill-name          # Must exist in skills/
agent: agent-name          # Must exist in agents/
stage: 0-3|5               # Pipeline stage number (omitted for composite commands)
---
```

Composite commands use `workflow:` instead of `stage:` and list multiple skills/agents.

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

`validate.py` enforces path security — all validated paths must resolve within the working directory. Allowed output directories: `.`, `.gt`, `scopecraft`.

## Adding New Stages/Gates

1. Add stage to `gates.yaml` under `stages:`
2. Create `commands/<name>.md` with proper frontmatter
3. Create `skills/<name>/SKILL.md` with procedures
4. Create templates in `skills/<name>/templates/`
5. Update workflows in `gates.yaml` if needed
6. Run `python3 plugins/lisa/hooks/validate.py --stage <name>` to test

## Ecosystem Position

Lisa is a **standalone plugin** and the **ecosystem root** of a three-plugin system. Understanding where it sits in the broader landscape is essential for making good decisions about what Lisa owns vs. what it defers.

### The Broader Stack

```
gastown.dev (Mayor)
  ↑ git worktrees, bead assignments
Conductor (orchestration layer)
  - 21 MCP tools: conductor_import_beads, conductor_claim_task, conductor_complete_bead, etc.
  - "lisa in conductor" and "carlos in conductor" = same plugins, invoked by Conductor's personality curation
  - File locks, heartbeat, cost tracking, context rollover, e2b sandboxes
  ↑ .gt/beads/*.json, .gt/convoys/*.json
Lisa (pipeline & memory) ←→ Carlos (specialist fixer)
  - Stages 0-5                   - Reads .gt/, doesn't own it
  - Owns .gt/ schema              - Writes scopecraft/
  - Owns gates.yaml               - Called by Lisa's plan stage
  - Writes beads/convoys          - Called by Conductor for quality routing
```

**Gastown** (gastown.dev) is the orchestration system that consumes Lisa's output. The Mayor assigns beads to agents via git-worktree-backed convoys. Lisa's job is to produce well-formed beads and convoys for the Mayor to work with.

**Conductor** is the MCP server between Lisa's file output and agent execution. It ingests Lisa's beads (`conductor_import_beads`), tracks them through the task lifecycle, manages file locks, detects context exhaustion, and routes tasks to the right personality. "Lisa in Conductor" and "Carlos in Conductor" mean Conductor's personality curation can invoke either plugin for the appropriate task — they are the same plugins, not separate implementations.

**Carlos** is the specialist fixer. During Lisa's plan stage, Carlos's agent personas (tech-auditor, market-fit-auditor, product-owner) provide the richer analysis that Lisa's skill-based scanning cannot. Carlos reads `.gt/memory/semantic.json` to avoid re-discovery. Carlos never owns or writes to `.gt/beads/` or `.gt/convoys/`.

### Interface Contracts (what Lisa owns)

| Interface | Owner | Consumers |
|-----------|-------|-----------|
| `.gt/` directory schema | **Lisa** | Carlos (reads), Conductor (imports beads) |
| `gates.yaml` format | **Lisa** | Carlos (enforces same schema v1.0) |
| `scopecraft/` docs | Lisa + Carlos (both write) | Reconcile, humans, Conductor context bundles |
| Bead/convoy format (`gt-xxxxx`) | **Lisa** | Gastown Mayor, Conductor `conductor_import_beads` |
| `.checkpoint.json` | **Lisa** (reconcile stage) | All three plugins for context recovery |

### scopecraft as Shared Language

`scopecraft/` is the human-readable layer that all three plugins speak. Lisa's plan stage (Stage 2) produces the six core files. Carlos refines them. Reconcile writes `ALIGNMENT_REPORT.md` and `.checkpoint.json`. Conductor reads them as context bundles when agents claim tasks. The files are the API — no plugin imports code from another.

### Lisa as Spin-off

Lisa is designed to be **standalone first** — `/lisa:migrate` runs end-to-end with no ecosystem partners required. Integration is additive:

| Alone | + Carlos | + Conductor | + Gastown |
|-------|----------|-------------|-----------|
| Full pipeline, own analysis | Richer plan stage, deeper quality gates | Multi-agent execution of beads, context rollover | Mayor assigns beads, git-worktree persistence |

When evolving Lisa, learn from the ecosystem without coupling to it. Carlos's `pipeline_orchestrator.py` and `model_router.py` show how to compose Lisa stages programmatically. Conductor's checkpoint/resume pattern mirrors Lisa's stage boundary checkpointing. Gastown's Mayor model shows the intended consumer of convoy bundles.

### Context Budget Principle

Each role is scoped to the context it needs:

| Layer | Context | Knows |
|-------|---------|-------|
| Gastown Mayor | Medium | All projects, all agents, convoy assignments |
| Conductor | Medium | All projects, agents, budgets, task queue |
| Lisa | Medium | One project's full lifecycle |
| Carlos | Small | One task, called in for sharp focus |
| e2b agents | Minimal | One bead, relevant files only |

Lisa's pipeline stages are checkpointed precisely because context is finite. Each stage boundary writes to `.gt/` so work survives context exhaustion and can be resumed by a fresh session.

## Releasing

Versions must stay in sync across two files:
- `plugins/lisa/.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`

Use `./scripts/bump-version.sh <version>` to update both automatically.
