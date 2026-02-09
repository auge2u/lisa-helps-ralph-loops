# Epics and Stories

## Epic: Marketplace Publication
**Theme:** Adoption
**Intent:** Lisa available on Claude Code marketplace for external users.

### Stories

#### Story 1: Submit Lisa to Claude Code marketplace
**As a** Lisa maintainer
**I want** Lisa listed on the Claude Code plugin marketplace
**So that** developers can discover and install it

**Acceptance Criteria:**
- Plugin manifest (`plugin.json`) passes marketplace validation
- Marketplace listing has description, category, and usage instructions
- Plugin installs cleanly via Claude Code plugin system
- All 5 stages documented in listing (research, discover, plan, structure, reconcile)

**Dependencies:** None
**Complexity:** M
**Risk:** Medium (marketplace requirements may need adjustments)

#### Story 2: Getting started documentation
**As a** new Lisa user
**I want** a guide that gets me from install to first pipeline run
**So that** I can use Lisa without reading source code

**Acceptance Criteria:**
- Covers: install plugin, run `/lisa:discover`, review output
- Works for standalone use (no Carlos or Conductor)
- Includes troubleshooting for common issues (PyYAML missing, etc.)
- Links to full stage documentation for deeper use

**Dependencies:** Story 1 (plugin installable)
**Complexity:** S
**Risk:** Low

---

## Epic: prductr-com Migration
**Theme:** Platform Maturity
**Intent:** All ecosystem repos under unified organization.

### Stories

#### Story 3: Transfer Lisa repository to prductr-com
**As an** ecosystem maintainer
**I want** Lisa at prductr-com/lisa3
**So that** the ecosystem has a unified public identity

**Acceptance Criteria:**
- Repository transferred with full git history and tags
- GitHub Actions CI/CD functional in new org
- README links updated to new org
- Old URL redirects automatically (GitHub feature)

**Dependencies:** prductr-com org created
**Complexity:** S
**Risk:** Medium (CI/CD secrets re-configuration)

#### Story 4: Update ecosystem config for new paths
**As a** Lisa user after migration
**I want** `~/.lisa/ecosystem.json` to work with new repo paths
**So that** reconcile finds all three projects

**Acceptance Criteria:**
- Documentation explains how to update ecosystem.json
- Reconcile gracefully handles projects at old paths (warns, doesn't fail)
- Consider git remote-based project identification (future improvement)

**Dependencies:** Story 3 (repos transferred)
**Complexity:** S
**Risk:** Low

---

## Epic: Standalone Hardening
**Theme:** Reliability
**Intent:** Lisa works reliably without ecosystem partners.

### Stories

#### Story 5: Graceful degradation without ecosystem
**As a** solo Lisa user
**I want** all pipeline stages to work without Carlos or Conductor
**So that** I get value from Lisa alone

**Acceptance Criteria:**
- Discover stage works without pre-existing `.gt/` state
- Plan stage works without Carlos analysis
- Structure stage creates beads/convoys independently
- Reconcile in standalone mode reports on single project only
- Clear messages when ecosystem partners are absent (informational, not errors)

**Dependencies:** None
**Complexity:** M
**Risk:** Low

#### Story 6: Validate pipeline on diverse projects
**As a** Lisa developer
**I want** the pipeline tested on 10+ real-world repos
**So that** I can trust it works beyond my own projects

**Acceptance Criteria:**
- Tested on Python, TypeScript, Go, Rust projects
- Tested on monorepos and single-package repos
- Tested on projects with and without docs/
- Edge cases documented (what fails and why)
- No crashes or hangs on any tested repo

**Dependencies:** Story 5 (graceful degradation)
**Complexity:** L
**Risk:** Medium

#### Story 7: PyYAML-free fallback for validate.py
**As a** Lisa user without PyYAML installed
**I want** validation to still work (with reduced functionality)
**So that** I'm not blocked by a missing dependency

**Acceptance Criteria:**
- validate.py detects missing PyYAML and falls back to JSON-only checks
- Fallback mode covers file_exists, json_valid, json_field_present checks
- Regex-based checks skip with warning (require PyYAML for gates.yaml parsing)
- Clear message about installing PyYAML for full validation

**Dependencies:** None
**Complexity:** M
**Risk:** Low

---

## Epic: Reconcile Resilience
**Theme:** Core Value
**Intent:** Reconcile handles edge cases and provides better recovery.

### Stories

#### Story 8: Git remote-based project identification
**As a** reconcile consumer
**I want** projects identified by git remote URL, not filesystem path
**So that** reconcile works regardless of where repos are cloned

**Acceptance Criteria:**
- Reconcile can identify projects by git remote origin
- Falls back to filesystem path when no git remote
- `~/.lisa/ecosystem.json` supports both path and remote fields
- Projects found even if cloned to non-standard locations

**Dependencies:** Story 4 (path migration support)
**Complexity:** M
**Risk:** Low

#### Story 9: Incremental reconcile
**As a** Lisa user
**I want** reconcile to only re-scan changed projects
**So that** reconcile is fast even with many projects

**Acceptance Criteria:**
- Reconcile checks git commit hash since last scan
- Unchanged projects skip re-scan (use cached state)
- Changed projects get full re-scan
- `--force` flag to re-scan everything
- Timestamp and hash stored in checkpoint

**Dependencies:** Story 8 (project identification stable)
**Complexity:** L
**Risk:** Medium

---

## Sequencing Notes

- Stories 1-2 (Marketplace) can start immediately
- Stories 3-4 (prductr-com) can start as soon as org is created
- Stories 5-7 (Standalone) can parallel with marketplace work
- Stories 8-9 (Reconcile) are Phase 5/6, depend on migration complete
