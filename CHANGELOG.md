# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- Security: Added path validation to prevent arbitrary file write in `--scratchpad` parameter
- Security: Added allowed directory validation for `--output-dir` parameter
- Fixed wrong plugin path in `bump-version.sh` script
- Fixed documentation to accurately distinguish implemented vs planned features

## [0.1.0] - 2026-01-27

### Added
- Initial fork from ralph-it-up v1.2.0
- Renamed plugin to `lisa-loops-memory`
- Gastown integration architecture design (documented, not yet implemented)
- Memory schema templates in `.gt/memory/` (semantic, episodic, procedural JSON templates)
- Directory structure for `.gt/beads/` and `.gt/convoys/` (placeholders for future implementation)

### Inherited (Working Features from ralph-it-up)
- `/lisa-loops-memory:roadmap` - One-shot roadmap generation
- `/lisa-loops-memory:roadmap-native` - Native Claude Code orchestration loop
- `/lisa-loops-memory:roadmap-orchestrated` - External ralph-orchestrator mode
- Quality gate validation framework (Python and Bash validators)
- Scratchpad protocol for cross-iteration context
- Outputs 6 markdown files to `./scopecraft/`

### Changed
- Project renamed from ralph-it-up to lisa-helps-ralph-loops
- Plugin renamed from ralph-it-up-roadmap to lisa-loops-memory
- Target platform: [Gastown](https://github.com/steveyegge/gastown) multi-agent workspace

### Planned (Not Yet Implemented)
The following Gastown migration features are on the roadmap:
- `/lisa-loops-memory:analyze` - Project analysis and memory generation
- `/lisa-loops-memory:migrate` - Gastown Rig structure generation
- `/lisa-loops-memory:beads` - Work item extraction as Beads
- `/lisa-loops-memory:convoy` - Convoy creation from Beads

[Unreleased]: https://github.com/auge2u/lisa-helps-ralph-loops/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/auge2u/lisa-helps-ralph-loops/releases/tag/v0.1.0
