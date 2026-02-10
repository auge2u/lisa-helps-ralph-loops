# DEPRECATED

This plugin (`lisa-loops-memory`) has been superseded by the `lisa` plugin at `plugins/lisa/`.

## Migration

| Old Command | New Command |
|-------------|-------------|
| `/lisa-loops-memory:analyze` | `/lisa:discover` |
| `/lisa-loops-memory:roadmap` | `/lisa:plan` |
| `/lisa-loops-memory:roadmap-native` | Removed (use `/lisa:plan`) |
| `/lisa-loops-memory:roadmap-orchestrated` | Removed (use `/lisa:plan`) |
| `/lisa-loops-memory:beads` | `/lisa:structure` |
| `/lisa-loops-memory:convoy` | `/lisa:structure` |
| `/lisa-loops-memory:migrate` | `/lisa:migrate` |

## What Changed

- Plugin renamed: `lisa-loops-memory` -> `lisa`
- Commands use `/lisa:` prefix
- Custom orchestration loops removed (Gastown handles this)
- Validators consolidated into `validate.py` with `gates.yaml`
- `.agent/` scratchpad memory replaced by `.gt/memory/`

## Timeline

- **v0.3.0**: New `lisa` plugin active; this plugin retained for reference
- **v1.0.0**: This plugin directory will be removed
