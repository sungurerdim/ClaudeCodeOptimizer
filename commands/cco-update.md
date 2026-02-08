---
description: Check for updates and upgrade CCO to the latest version
argument-hint: "[--auto] [--check] [--dev] [--stable]"
allowed-tools: WebFetch, Read, Write, Edit, Bash, AskUserQuestion
model: opus
---

# /cco-update

**Update Manager** — Check for new versions, upgrade in place.

## Args

| Flag | Effect |
|------|--------|
| `--auto` | Silent update, no questions, upgrade if available |
| `--check` | Version check only, no changes |
| `--dev` | Use dev channel (latest dev branch commit) |
| `--stable` | Use stable channel (latest release tag, default) |

Without flags: check for update, ask before upgrading.

## Context

- CCO version: from `cco_version` in cco-rules.md frontmatter (already in context)
- Last check: from `last_update_check` in cco-rules.md frontmatter (already in context)

## Files

All CCO files to update:

```
rules/cco-rules.md
commands/cco-optimize.md
commands/cco-align.md
commands/cco-commit.md
commands/cco-research.md
commands/cco-docs.md
commands/cco-update.md
commands/cco-blueprint.md
commands/cco-pr.md
agents/cco-agent-analyze.md
agents/cco-agent-apply.md
agents/cco-agent-research.md
```

## Execution Flow

Channel Resolve → Version Check → Compare → [Upgrade] → Verify → Summary

### Phase 0: Channel Resolve

Determine channel from args:
- `--dev` → channel = dev
- `--stable` or no flag → channel = stable

| Channel | Git ref | Source URL base |
|---------|---------|-----------------|
| stable | Latest tag from GitHub API (`/repos/{repo}/tags?per_page=1`) | `https://raw.githubusercontent.com/{repo}/v{VERSION}/{path}` |
| dev | `dev` branch | `https://raw.githubusercontent.com/{repo}/dev/{path}` |

### Phase 1: Version Check

1. Read current `cco_version` from context (cco-rules.md frontmatter)
2. Resolve remote version:
   - **stable:** WebFetch GitHub tags API → extract latest tag (strip `v` prefix)
   - **dev:** WebFetch `rules/cco-rules.md` from dev branch → extract `cco_version` from frontmatter

### Phase 2: Compare

Compare current vs remote using semver:
- Same version → "CCO is up to date (vX.Y.Z)"
- New version → proceed to upgrade flow
- **dev channel:** Also compare even if versions match (dev may have newer commits at same version)

Display: `Current: vX.Y.Z → Latest: vA.B.C (channel)`

**--check mode:** Display version info and exit. Update `last_update_check` timestamp in cco-rules.md frontmatter.

### Phase 3: Preflight

Before downloading, verify the resolved ref has the expected file structure:

1. WebFetch `{BASE_URL}/rules/cco-rules.md`
2. Confirm response starts with `---` (YAML frontmatter)
3. On failure:
   - **stable:** "Release tag predates install-script model. Use --dev."
   - **dev:** "Could not fetch files from dev branch."

### Phase 4: Upgrade [SKIP if --check]

**--auto mode:** Proceed without asking.

**Interactive mode:**
```javascript
AskUserQuestion([{
  question: "New version available. What should be done?",
  header: "Upgrade",
  options: [
    { label: "Upgrade now (Recommended)", description: "Download and install the new version" },
    { label: "Skip", description: "Stay on current version" },
    { label: "View changelog", description: "See what changed before deciding" }
  ],
  multiSelect: false
}])
```

**Upgrade process:**

1. Determine `~/.claude/` path (`$HOME/.claude/` on Unix, `$USERPROFILE\.claude\` on Windows)
2. For each CCO file, WebFetch raw content from resolved source URL
3. Validate each file starts with `---` (YAML frontmatter) before writing
4. Write validated content to local path
5. Update `last_update_check` timestamp in cco-rules.md frontmatter

**Legacy cleanup:** Remove old CCO installations and files (v1.x + v2.x) if present:

Uninstall previous distribution models:
- v2.x plugin: `claude plugin uninstall cco@ClaudeCodeOptimizer` + `claude plugin marketplace remove ClaudeCodeOptimizer`
- v1.x pip: `pip uninstall claude-code-optimizer -y`

Pattern-based (scan directory, keep only current v3 files, remove rest):
- `commands/cco-*.md` — keep only: cco-optimize, cco-align, cco-commit, cco-research, cco-docs, cco-update, cco-blueprint, cco-pr
- `agents/cco-*.md` — keep only: cco-agent-analyze, cco-agent-apply, cco-agent-research
- `rules/cco-*.md` — keep only: cco-rules.md

Hardcoded (v2.x commands without cco- prefix, no distinguishing pattern):
- `commands/{optimize,align,commit,research,preflight,docs,tune}.md`

Directories:
- `commands/schemas/`, `rules/{core,frameworks,languages,operations}/`, `hooks/`

### Phase 5: Verify

Read cco-rules.md frontmatter → confirm `cco_version` matches remote version.

### Phase 6: Summary

| Mode | Output |
|------|--------|
| `--check` | `CCO: v{current} (up to date)` or `CCO: v{current} → v{latest} available. Run /cco-update to upgrade.` |
| `--auto` | `cco-update: {OK\|FAIL} \| v{current} → v{latest} ({channel})` |
| Interactive | Version info, channel, files updated count, legacy cleaned count, restart reminder |

**Restart reminder:** "Restart Claude Code session to load updated rules."
