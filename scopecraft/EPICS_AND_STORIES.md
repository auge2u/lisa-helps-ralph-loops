# Epics and Stories

## Epic: Documentation and Cleanup
**Theme:** Adoption
**Intent:** Lisa's public-facing documentation accurately describes the current v0.3.0 system so new users aren't confused by stale references.

### Stories

#### Story 1: Rewrite README for v0.3.0
**As a** prospective Lisa user
**I want** the README to describe current commands, install process, and output structure
**So that** I can evaluate and use Lisa without reading source code

**Acceptance Criteria:**
- [ ] All command references use `/lisa:` prefix (not `/lisa-loops-memory:`)
- [ ] Install instructions work with Claude Code plugin system
- [ ] Output structure shows all 5 stages and their directories
- [ ] Gastown concepts table updated
- [ ] Validation section references `validate.py` (not legacy validators)
- [ ] Compatibility section reflects current ecosystem (Lisa, Carlos, Conductor)

**Dependencies:** None
**Complexity:** M
**Risk:** Low

#### Story 2: Update CHANGELOG for v0.3.0
**As a** Lisa user tracking changes
**I want** CHANGELOG.md to document all v0.3.0 changes
**So that** I know what's new, changed, and deprecated

**Acceptance Criteria:**
- [ ] v0.3.0 entry documents: new plugin name, new commands, new agents, gates.yaml, validate.py
- [ ] Deprecated items listed (old commands, old validators, `.agent/` memory)
- [ ] Breaking changes called out (renamed plugin, changed command prefix)
- [ ] Links section updated with correct comparison URLs

**Dependencies:** None
**Complexity:** S
**Risk:** Low

#### Story 3: Archive deprecated lisa-loops-memory plugin
**As a** codebase maintainer
**I want** the deprecated plugin clearly marked and optionally removed
**So that** new contributors aren't confused by two plugins

**Acceptance Criteria:**
- [ ] `plugins/lisa-loops-memory/` either removed or has a deprecation notice
- [ ] marketplace.json keeps `"deprecated": true` entry for backward compatibility
- [ ] No active code references the old plugin path
- [ ] CLAUDE.md test note about legacy imports updated

**Dependencies:** Story 1 (README updated first)
**Complexity:** S
**Risk:** Low

---

## Epic: Marketplace Publication
**Theme:** Adoption
**Intent:** Lisa available on Claude Code marketplace for external users to discover and install.

### Stories

#### Story 4: Research marketplace submission requirements
**As a** Lisa maintainer
**I want** to understand what Claude Code marketplace requires for plugin submission
**So that** we can prepare our submission without rejection cycles

**Acceptance Criteria:**
- [ ] Submission requirements documented (manifest fields, description, category)
- [ ] Plugin install/uninstall cycle tested locally
- [ ] Any gaps between current plugin.json and marketplace requirements identified
- [ ] Submission checklist created

**Dependencies:** None
**Complexity:** S
**Risk:** Medium (requirements may be undocumented)

#### Story 5: Submit Lisa to Claude Code marketplace
**As a** Lisa maintainer
**I want** Lisa listed on the Claude Code plugin marketplace
**So that** developers can discover and install it

**Acceptance Criteria:**
- [ ] Plugin manifest passes marketplace validation
- [ ] Marketplace listing has description, category, and usage instructions
- [ ] Plugin installs cleanly via Claude Code plugin system
- [ ] All 5 stages documented in listing
- [ ] Uninstall leaves no artifacts

**Dependencies:** Story 1 (README), Story 4 (requirements research)
**Complexity:** M
**Risk:** Medium (marketplace requirements may need adjustments)

#### Story 6: Getting started documentation
**As a** new Lisa user
**I want** a guide that gets me from install to first pipeline run
**So that** I can use Lisa without reading source code

**Acceptance Criteria:**
- [ ] Covers: install plugin, run `/lisa:discover`, review output
- [ ] Works for standalone use (no Carlos or Conductor required)
- [ ] Includes troubleshooting for common issues (PyYAML missing, no docs/ dir)
- [ ] Links to full stage documentation for deeper use
- [ ] Tested on a clean environment with no pre-existing .gt/ state

**Dependencies:** Story 5 (plugin installable)
**Complexity:** S
**Risk:** Low

---

## Epic: Repository Migration
**Theme:** Platform Maturity
**Intent:** All ecosystem repos under unified prductr-com organization.

### Stories

#### Story 7: Transfer Lisa repository to prductr-com
**As an** ecosystem maintainer
**I want** Lisa at prductr-com/lisa3
**So that** the ecosystem has a unified public identity

**Acceptance Criteria:**
- [ ] Repository transferred with full git history and tags
- [ ] GitHub Actions CI/CD functional in new org
- [ ] README links updated to new org
- [ ] plugin.json and marketplace.json URLs updated
- [ ] Old URL redirects automatically (GitHub feature)

**Dependencies:** prductr-com org created
**Complexity:** S
**Risk:** Medium (CI/CD secrets need re-configuration)

#### Story 8: Update ecosystem config for new paths
**As a** Lisa user after migration
**I want** `~/.lisa/ecosystem.json` to work with new repo paths
**So that** reconcile finds all three projects

**Acceptance Criteria:**
- [ ] Documentation explains how to update ecosystem.json after migration
- [ ] Reconcile gracefully handles projects at old paths (warns, doesn't fail)
- [ ] Reconcile handles missing projects without crashing (skip with warning)

**Dependencies:** Story 7 (repos transferred)
**Complexity:** S
**Risk:** Low

---

## Epic: Standalone Hardening
**Theme:** Reliability
**Intent:** Lisa works reliably without ecosystem partners on diverse projects.

### Stories

#### Story 9: PyYAML-free fallback for validate.py
**As a** Lisa user without PyYAML installed
**I want** validation to still work with reduced functionality
**So that** I'm not blocked by a missing dependency

**Acceptance Criteria:**
- [ ] validate.py detects missing PyYAML at import time
- [ ] Fallback mode covers file_exists, json_valid, json_field_present, json_field_count checks
- [ ] Pattern-based checks (pattern_exists, pattern_count) skip with clear warning
- [ ] Exit message recommends `pip install pyyaml` for full validation
- [ ] Fallback mode tested (rename pyyaml temporarily, run validator)

**Dependencies:** None
**Complexity:** M
**Risk:** Low

#### Story 10: Graceful degradation without ecosystem
**As a** solo Lisa user
**I want** all pipeline stages to work without Carlos or Conductor
**So that** I get value from Lisa alone

**Acceptance Criteria:**
- [ ] Discover stage works without pre-existing `.gt/` state
- [ ] Plan stage works without Carlos analysis
- [ ] Structure stage creates beads/convoys independently
- [ ] Reconcile in standalone mode reports on single project only
- [ ] Clear messages when ecosystem partners are absent (informational, not errors)
- [ ] No tracebacks or crashes when ecosystem.json references missing projects

**Dependencies:** None
**Complexity:** M
**Risk:** Low

#### Story 11: Validate pipeline on diverse projects
**As a** Lisa developer
**I want** the pipeline tested on 10+ real-world repos
**So that** I can trust it works beyond my own projects

**Acceptance Criteria:**
- [ ] Tested on Python, TypeScript, Go, Rust projects
- [ ] Tested on monorepos and single-package repos
- [ ] Tested on projects with and without docs/ directory
- [ ] Tested on minimal projects (just a README and source)
- [ ] Edge cases documented (what fails and why)
- [ ] No crashes or hangs on any tested repo
- [ ] 90%+ success rate across test repos

**Dependencies:** Story 9 (PyYAML fallback), Story 10 (graceful degradation)
**Complexity:** L
**Risk:** Medium (unknown failure modes in unfamiliar projects)

---

## Epic: Reconcile Resilience
**Theme:** Core Value
**Intent:** Reconcile handles edge cases, scales beyond 3 projects, and provides context recovery.

### Stories

#### Story 12: Git remote-based project identification
**As a** reconcile consumer
**I want** projects identified by git remote URL, not just filesystem path
**So that** reconcile works regardless of where repos are cloned

**Acceptance Criteria:**
- [ ] Reconcile can identify projects by git remote origin
- [ ] Falls back to filesystem path when no git remote
- [ ] `~/.lisa/ecosystem.json` supports both `path` and `remote` fields
- [ ] Projects found even if cloned to non-standard locations
- [ ] Migration guide for existing ecosystem.json users

**Dependencies:** Story 8 (path migration support)
**Complexity:** M
**Risk:** Low

#### Story 13: Incremental reconcile
**As a** Lisa user with many projects
**I want** reconcile to only re-scan changed projects
**So that** reconcile is fast even as the ecosystem grows

**Acceptance Criteria:**
- [ ] Reconcile checks git commit hash since last checkpoint
- [ ] Unchanged projects skip re-scan (use cached state from checkpoint)
- [ ] Changed projects get full re-scan
- [ ] `--force` flag to re-scan everything regardless
- [ ] Timestamp and hash stored per-project in checkpoint
- [ ] Performance measurably better with 5+ projects

**Dependencies:** Story 12 (project identification stable)
**Complexity:** L
**Risk:** Medium (cache invalidation edge cases)

---

## Sequencing Notes

- Stories 1-3 (Documentation/Cleanup) can start immediately -- no external dependencies
- Story 4 (marketplace research) can start immediately, informs Story 5
- Stories 7-8 (Migration) can start as soon as prductr-com org is created
- Stories 9-10 (Standalone) can parallel with marketplace work
- Story 11 (Diverse testing) depends on Stories 9-10
- Stories 12-13 (Reconcile) are Phase 6, depend on migration complete and external feedback
- Critical path to first external user: Story 1 -> Story 4 -> Story 5 -> Story 6
