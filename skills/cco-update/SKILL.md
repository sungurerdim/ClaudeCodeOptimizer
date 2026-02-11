---
description: Check for updates and upgrade CCO to the latest version
argument-hint: "[--auto] [--check]"
allowed-tools: WebFetch, Read, Write, Edit, Bash, AskUserQuestion
disable-model-invocation: true
---

# /cco-update

**Update Manager** — Check for new versions, upgrade in place.

## Args

| Flag | Effect |
|------|--------|
| `--auto` | Silent update, no questions, upgrade if available |
| `--check` | Version check only, no changes |

Without flags: check for update, ask before upgrading.

## Context

- CCO version: from `cco_version` in cco-rules.md frontmatter (already in context)

## Files

All CCO files to update:

```
rules/cco-rules.md
skills/cco-optimize/SKILL.md
skills/cco-align/SKILL.md
skills/cco-commit/SKILL.md
skills/cco-research/SKILL.md
skills/cco-docs/SKILL.md
skills/cco-update/SKILL.md
skills/cco-blueprint/SKILL.md
skills/cco-pr/SKILL.md
agents/cco-agent-analyze.md
agents/cco-agent-apply.md
agents/cco-agent-research.md
```

## Execution Flow

Channel Resolve → Version Check → Compare → [Upgrade] → Verify → Summary

### Phase 0: Resolve Latest Version

Fetch latest release tag from GitHub API (`/repos/{repo}/tags?per_page=1`).

Source URL base: `https://raw.githubusercontent.com/{repo}/v{VERSION}/{path}`

### Phase 1: Version Check

1. Read current `cco_version` from context (cco-rules.md frontmatter)
2. Resolve remote version: WebFetch GitHub tags API → extract latest tag (strip `v` prefix)

### Phase 2: Compare

Compare current vs remote using semver:
- Same version → "CCO is up to date (vX.Y.Z)"
- New version → proceed to upgrade flow

Display: `Current: vX.Y.Z → Latest: vA.B.C`

**--check mode:** Display version info and exit. Update `last_update_check` timestamp in cco-rules.md frontmatter.

### Phase 3: Source Verification

Before downloading, verify the resolved ref has the expected file structure:

1. WebFetch `{BASE_URL}/rules/cco-rules.md`
2. Confirm response starts with `---` (YAML frontmatter)
3. On failure: "Release tag predates install-script model. Check repository for updates."

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
4. Create skill directories if missing (`skills/cco-*/`)
5. Write validated content to local path
6. Update `last_update_check` timestamp in cco-rules.md frontmatter

**Legacy cleanup:** Remove old CCO installations and files (all previous versions) if present:

Uninstall previous distribution models:
- v2.x plugin: `claude plugin uninstall cco@ClaudeCodeOptimizer` + `claude plugin marketplace remove ClaudeCodeOptimizer`
- v1.x pip: `pip uninstall claudecodeoptimizer -y`

Pattern-based cleanup:
- v3 commands: `commands/cco-*.md` — remove all (migrated to skills/)
- `agents/cco-*.md` — keep only: cco-agent-analyze, cco-agent-apply, cco-agent-research
- `rules/cco-*.md` — keep only: cco-rules.md
- Stale skill directories not in current v4 set

Hardcoded (v2.x commands without cco- prefix, no distinguishing pattern):
- `commands/{optimize,align,commit,research,preflight,docs,tune}.md`

Directories:
- `commands/schemas/`, `rules/{core,frameworks,languages,operations}/`, `hooks/`

Reference Go binary as preferred update method: "For future updates, consider using the Go installer: `cco install`"

### Phase 5: Verify

Read cco-rules.md frontmatter → confirm `cco_version` matches remote version.

### Phase 6: Summary

| Mode | Output |
|------|--------|
| `--check` | `CCO: v{current} (up to date)` or `CCO: v{current} → v{latest} available. Run /cco-update to upgrade.` |
| `--auto` | `cco-update: {OK\|FAIL} \| v{current} → v{latest}` |
| Interactive | Version info, files updated count, legacy cleaned count, restart reminder |

**Restart reminder:** "Restart Claude Code session to load updated rules."
