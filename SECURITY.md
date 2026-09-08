# Security Policy

## Supported Versions

Only the latest published version of the `lisa` plugin is supported. There is no
long-term-support branch; security fixes land as a new version via
`./scripts/bump-version.sh` and a corresponding GitHub Release.

The `lisa-loops-memory` plugin is deprecated and does not receive security fixes —
migrate to `lisa`.

## Scope

Lisa is a Claude Code plugin that runs entirely as local file analysis and
generation inside the user's own Claude Code session:

- No hosted service, no server, no database.
- No API keys or credentials of its own.
- All outputs are local files under `.gt/`, `scopecraft/`, and `.checkpoint.json`
  in the user's project directory.
- The research/archaeologist stage (`/lisa:research`, `/lisa:rescue`) optionally
  shells out to the user's own authenticated `gh` CLI for a read-only issue/PR
  snapshot; it never writes to GitHub and degrades gracefully when `gh` isn't
  authenticated.

`plugins/lisa/hooks/validate.py` resolves file paths relative to the working
directory and trusts `gates.yaml` as developer-controlled config (see
`CLAUDE.md`'s "Validation" section). Its write/check surface is restricted to
`.`, `.gt`, and `scopecraft` — a path escaping those directories is a bug worth
reporting under this policy.

## Reporting a Vulnerability

Please **do not** open a public GitHub issue for a suspected vulnerability.

Instead, email **auge2u@gmail.com** with:

- A description of the issue and its impact.
- Steps to reproduce, or a minimal example.
- The affected version (`plugins/lisa/.claude-plugin/plugin.json`'s `version` field).

You should expect an initial response within a few days. Once a fix is confirmed,
it will be released as a new version and credited in `CHANGELOG.md` unless you
prefer to remain anonymous.
