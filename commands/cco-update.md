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
commands/cco-preflight.md
commands/cco-docs.md
commands/cco-update.md
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

**Interactive mode:** Ask user:
- Upgrade now (Recommended) / Skip / View changelog

**Upgrade process:**

1. Determine `~/.claude/` path (`$HOME/.claude/` on Unix, `$USERPROFILE\.claude\` on Windows)
2. For each CCO file, WebFetch raw content from resolved source URL
3. Validate each file starts with `---` (YAML frontmatter) before writing
4. Write validated content to local path
5. Update `last_update_check` timestamp in cco-rules.md frontmatter

**Legacy cleanup:** Remove old files from previous CCO versions if present:
- `commands/{optimize,align,commit,research,preflight,docs}.md` (without `cco-` prefix)
- `commands/schemas/` directory

### Phase 5: Verify

Read cco-rules.md frontmatter → confirm `cco_version` matches remote version.

### Phase 6: Summary

| Mode | Output |
|------|--------|
| `--check` | `CCO: v{current} (up to date)` or `CCO: v{current} → v{latest} available. Run /cco-update to upgrade.` |
| `--auto` | `cco-update: {OK\|FAIL} \| v{current} → v{latest} ({channel})` |
| Interactive | Version info, channel, files updated count, legacy cleaned count, restart reminder |

**Restart reminder:** "Restart Claude Code session to load updated rules."
