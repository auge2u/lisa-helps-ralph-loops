# Getting Started with Lisa

Lisa analyzes your project and creates structured work items for multi-agent execution. This guide takes you from install to first output in under 15 minutes.

## Prerequisites

- [Claude Code](https://claude.ai/code) installed and configured
- A project you want to analyze (any language, any size)

## Install

```
/install-plugin auge2u/lisa-helps-ralph-loops
```

Verify the install worked:

```
/lisa:status
```

## Your First Pipeline Run

### Step 1: Discover (recommended starting point)

Navigate to your project directory, then run:

```
/lisa:discover
```

This scans your project and creates `.gt/memory/semantic.json` with:
- Project name, type, and primary language
- Tech stack (runtime, framework, database, etc.)
- Constraints and personas
- Evidence of files analyzed

**What to look for:** Open `.gt/memory/semantic.json` and verify it accurately describes your project. If something's wrong, you can edit it manually -- Lisa treats it as the source of truth for later stages.

### Step 2: Plan (optional but recommended)

```
/lisa:plan
```

This generates 6 planning files in `scopecraft/`:
- `VISION_AND_STAGE_DEFINITION.md` -- Where your project is and where it's going
- `ROADMAP.md` -- 3-5 phased plan with deliverables
- `EPICS_AND_STORIES.md` -- User stories with acceptance criteria
- `RISKS_AND_DEPENDENCIES.md` -- Risk register and dependency map
- `METRICS_AND_PMF.md` -- Success metrics and PMF signals
- `OPEN_QUESTIONS.md` -- Blocking decisions and experiments

**What to look for:** Review `ROADMAP.md` first. Does the phasing make sense? Are the risks real? Edit any file directly -- these are your planning docs.

### Step 3: Structure

```
/lisa:structure
```

This creates Gastown-compatible work items:
- `.gt/beads/gt-xxxxx.json` -- Individual work items with acceptance criteria
- `.gt/convoys/convoy-NNN.json` -- Bundles of 3-7 related beads

**What to look for:** Each bead should have clear acceptance criteria and link back to a source (story, issue, or TODO). Convoys should group related work.

### One-Command Alternative

Run all three stages at once:

```
/lisa:migrate
```

## Validating Output

Check that Lisa's output meets quality standards:

```bash
python3 plugins/lisa/hooks/validate.py --stage discover
python3 plugins/lisa/hooks/validate.py --stage plan
python3 plugins/lisa/hooks/validate.py --stage structure
```

Or validate everything:

```bash
python3 plugins/lisa/hooks/validate.py --stage all
```

**Note:** Full validation requires PyYAML (`pip install pyyaml`). Without it, the validator runs in fallback mode with reduced checks.

## Troubleshooting

### "PyYAML is required" or "Running in fallback mode"

The validator needs PyYAML for full gate checking. Install it:

```bash
pip install pyyaml
```

Validation still works without it -- you'll get file existence and JSON structure checks, but pattern-based checks (like counting phases in ROADMAP.md) are skipped.

### Discover produces sparse semantic.json

If your project has minimal documentation, discover will have less to work with. You can:
1. Add a README.md describing your project
2. Run discover again -- it will pick up new docs
3. Edit `.gt/memory/semantic.json` manually to fill gaps

### Plan produces generic output

Plan works best when it has good inputs:
- A populated `.gt/memory/semantic.json` (run discover first)
- Documentation in `docs/` directory
- Existing issues, TODOs, or backlog files

### Structure creates too few beads

Structure extracts from `scopecraft/` files (run plan first) and any existing issues. If you skipped plan, structure still works but will have fewer sources to extract from.

## What's Next

- **Rescue a lost project?** Use `/lisa:research` for deep git archaeology before discover
- **Check ecosystem alignment?** Use `/lisa:reconcile` if you have multiple Lisa-managed projects
- **Full rescue pipeline?** Use `/lisa:rescue` to run all stages including research

## Ecosystem (Optional)

Lisa works standalone. For more power, add ecosystem partners:

| Plugin | What it adds |
|--------|-------------|
| **Carlos** | Specialist analysis (roadmap quality, market fit, tech debt) |
| **Conductor** | Multi-agent orchestration (task assignment, context rollover) |

Each plugin is independent. Install one or all three -- Lisa detects available partners automatically.
