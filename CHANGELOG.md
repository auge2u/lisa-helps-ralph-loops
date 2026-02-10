# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] - 2026-02-10

### Added
- **New plugin: `lisa`** (replaces `lisa-loops-memory`)
  - `/lisa:research` - Stage 0: Archaeological rescue for abandoned projects
  - `/lisa:discover` - Stage 1: Extract semantic memory from project analysis
  - `/lisa:plan` - Stage 2: Generate roadmap with epics, risks, metrics
  - `/lisa:structure` - Stage 3: Create Beads and Convoys for Gastown
  - `/lisa:reconcile` - Stage 5: Cross-project ecosystem alignment
  - `/lisa:migrate` - Composite: stages 1-3
  - `/lisa:rescue` - Composite: stages 0-3
  - `/lisa:status` - Show migration progress and quality gate results
- **Agents:** `archaeologist` (Stage 0 rescue), `migrator` (Stages 1-3, 5)
- **Skills:** research, discover, plan, structure, reconcile (with templates)
- **`gates.yaml` v1.1** - Declarative quality gates (31 gates across 5 stages)
- **`validate.py`** - Unified validator loading gates from gates.yaml
  - Supports `--stage`, `--workflow`, `--format` flags
  - Path security enforcement (outputs must stay within working directory)
  - PyYAML-free fallback mode for JSON-only checks
- **Reconcile system (Stage 5)**
  - Ecosystem config at `~/.lisa/ecosystem.json`
  - Checkpoint schema (`reconcile-checkpoint-v1`)
  - 3 output templates (alignment report, perspectives, checkpoint)
  - 9 reconcile-specific quality gates
- **5-stage pipeline architecture** per `docs/ARCHITECTURE_V2.md`

### Changed
- Plugin renamed from `lisa-loops-memory` to `lisa`
- Command prefix changed from `/lisa-loops-memory:` to `/lisa:`
- Validators consolidated from 3 scripts to 1 (`validate.py`)
- Quality gates moved from hardcoded to declarative (`gates.yaml`)

### Deprecated
- `plugins/lisa-loops-memory/` - Superseded by `plugins/lisa/`
- All `/lisa-loops-memory:*` commands
- `validate_gastown.py` and `validate_quality_gates.py` (replaced by `validate.py`)
- `.agent/` scratchpad memory system (replaced by `.gt/memory/`)

### Breaking Changes
- Command prefix changed: `/lisa-loops-memory:analyze` -> `/lisa:discover`
- Command prefix changed: `/lisa-loops-memory:roadmap` -> `/lisa:plan`
- Command prefix changed: `/lisa-loops-memory:beads` + `convoy` -> `/lisa:structure`
- Custom orchestration loops removed (roadmap-native, roadmap-orchestrated)

## [0.2.0] - 2026-01-27

### Added
- **Gastown Migration Commands** (NEW)
  - `/lisa-loops-memory:analyze` - Scan project, generate semantic memory
  - `/lisa-loops-memory:beads` - Extract work items as Beads
  - `/lisa-loops-memory:convoy` - Bundle Beads into Convoys
  - `/lisa-loops-memory:migrate` - Full migration (analyze + beads + convoy)
- `gastown-migrator` agent for project analysis and migration
- `gastown-migration` skill with complete documentation
- `validate_gastown.py` - Gastown migration validator
- Bead and Convoy JSON templates
- Example outputs in `examples/gastown/`
- Test coverage for quality gate validator (25 tests)

### Fixed
- Security: Path validation for `--scratchpad` and `--output-dir` parameters
- Fixed plugin path in `bump-version.sh`
- Documentation accuracy (implemented vs planned features)

## [0.1.0] - 2026-01-27

### Added
- Initial fork from ralph-it-up v1.2.0
- Renamed plugin to `lisa-loops-memory`
- Gastown integration architecture design
- Memory schema templates in `.gt/memory/`
- Directory structure for `.gt/beads/` and `.gt/convoys/`

### Inherited (from ralph-it-up)
- `/lisa-loops-memory:roadmap` - One-shot roadmap generation
- `/lisa-loops-memory:roadmap-native` - Native Claude Code orchestration loop
- `/lisa-loops-memory:roadmap-orchestrated` - External ralph-orchestrator mode
- Quality gate validation framework (Python and Bash validators)
- Scratchpad protocol for cross-iteration context
- Outputs 6 markdown files to `./scopecraft/`

[Unreleased]: https://github.com/auge2u/lisa-helps-ralph-loops/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/auge2u/lisa-helps-ralph-loops/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/auge2u/lisa-helps-ralph-loops/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/auge2u/lisa-helps-ralph-loops/releases/tag/v0.1.0
