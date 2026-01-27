# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/auge2u/lisa-helps-ralph-loops/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/auge2u/lisa-helps-ralph-loops/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/auge2u/lisa-helps-ralph-loops/releases/tag/v0.1.0
