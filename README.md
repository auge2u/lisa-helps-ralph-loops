# Lisa - Staged Migration System for Gastown

Lisa is a Claude Code plugin that analyzes projects and structures them for [Gastown](https://github.com/steveyegge/gastown) multi-agent execution. It scans codebases, extracts semantic memory, generates roadmaps, creates structured work items (Beads/Convoys), and reconciles ecosystem state across projects.

## What It Does

1. **Rescues lost projects** - Reconstructs context from git history and abandoned docs
2. **Understands your project** - Extracts tech stack, constraints, and personas into semantic memory
3. **Plans your roadmap** - Generates phased roadmap with epics, risks, and metrics
4. **Structures work** - Creates Beads (work items) and Convoys (bundles) for Gastown agents
5. **Reconciles ecosystems** - Cross-validates multiple projects for alignment and drift

## Install

```
/install-plugin auge2u/lisa-helps-ralph-loops
```

## Commands

| Command | Stage | Purpose |
|---------|-------|---------|
| `/lisa:research` | 0 | Archaeological rescue for abandoned projects |
| `/lisa:discover` | 1 | Extract semantic memory from project analysis |
| `/lisa:plan` | 2 | Generate roadmap with epics, risks, metrics |
| `/lisa:structure` | 3 | Create Beads and Convoys for Gastown |
| `/lisa:reconcile` | 5 | Cross-project alignment report and checkpoint |
| `/lisa:migrate` | 1+2+3 | Full pipeline (discover + plan + structure) |
| `/lisa:rescue` | 0+1+2+3 | Full rescue (research + discover + plan + structure) |
| `/lisa:status` | - | Show migration progress and quality gate results |

## Quick Start

```bash
# Full migration in one command
/lisa:migrate

# Or run stages individually
/lisa:discover     # Creates .gt/memory/semantic.json
/lisa:plan         # Creates scopecraft/ (6 planning files)
/lisa:structure    # Creates .gt/beads/*.json and .gt/convoys/*.json

# Check progress
/lisa:status
```

## Output Structure

```
project/
├── .gt/
│   ├── research/          # Stage 0: rescue docs (optional)
│   ├── memory/
│   │   └── semantic.json  # Stage 1: project facts
│   ├── beads/
│   │   └── gt-*.json      # Stage 3: individual work items
│   └── convoys/
│       └── convoy-*.json  # Stage 3: bundled work assignments
└── scopecraft/
    ├── VISION_AND_STAGE_DEFINITION.md  # Stage 2
    ├── ROADMAP.md
    ├── EPICS_AND_STORIES.md
    ├── RISKS_AND_DEPENDENCIES.md
    ├── METRICS_AND_PMF.md
    └── OPEN_QUESTIONS.md
```

## Gastown Concepts

| Term | Description |
|------|-------------|
| **Bead** | Work item with ID `gt-xxxxx`, acceptance criteria, evidence |
| **Convoy** | Bundle of 3-7 related beads for agent assignment |
| **Memory** | Semantic (facts), episodic (decisions), procedural (patterns) |
| **Mayor** | Gastown's primary AI coordinator |
| **Polecat** | Ephemeral worker agent in Gastown |

## Validation

Lisa uses declarative quality gates defined in `gates.yaml` (31 gates across 5 stages).

```bash
# Validate specific stage
python3 plugins/lisa/hooks/validate.py --stage discover
python3 plugins/lisa/hooks/validate.py --stage plan

# Validate all stages
python3 plugins/lisa/hooks/validate.py --stage all

# Output formats
python3 plugins/lisa/hooks/validate.py --stage plan --format json
python3 plugins/lisa/hooks/validate.py --stage plan --format markdown

# Validate workflow
python3 plugins/lisa/hooks/validate.py --workflow migrate
```

Requires Python 3.10+ and PyYAML (`pip install pyyaml`). Runs in fallback mode without PyYAML (JSON-only checks).

Exit codes: `0` = pass, `1` = blocker failed, `2` = warning only, `3` = security error.

## Ecosystem

Lisa is the root of a three-plugin ecosystem:

| Plugin | Role | Status |
|--------|------|--------|
| **Lisa** | Pipeline & Memory | Alpha (v0.3.0) |
| **[Carlos](https://github.com/auge2u/carlos)** | Specialist Fixer | Beta (v1.2.0) |
| **[Conductor](https://github.com/habitusnet/conductor)** | Orchestration | GA (v1.0.0) |

Each plugin works standalone. The ecosystem is additive -- install one or all three.

Reconcile (`/lisa:reconcile`) reads `~/.lisa/ecosystem.json` to find project paths and cross-validate alignment.

## Version

Current: **v0.3.0** (active plugin: `plugins/lisa/`)

See [CHANGELOG.md](CHANGELOG.md) for release history.

## License

MIT
