---
description: Check for updates and upgrade CCO to the latest version
argument-hint: "[--auto] [--check]"
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

Without flags: check for update, ask before upgrading.

## Context

- CCO version: from `cco_version` in cco-rules.md frontmatter (already in context)
- Last check: from `last_update_check` in cco-rules.md frontmatter (already in context)

**DO NOT re-run these commands. Use the pre-collected values above.**

## Execution Flow

Version Check → Compare → [Upgrade] → Verify → Summary

### Phase 1: Version Check

1. Read current `cco_version` from context (cco-rules.md frontmatter)
2. WebFetch GitHub tags API: `https://api.github.com/repos/sungurerdim/ClaudeCodeOptimizer/tags`
3. Extract latest tag version (strip `v` prefix)

### Phase 2: Compare

Compare current vs latest using semver:
- Same version → "CCO is up to date (vX.Y.Z)"
- New version → proceed to upgrade flow

Display: `Current: vX.Y.Z → Latest: vA.B.C`

**--check mode:** Display version info and exit. Update `last_update_check` timestamp in cco-rules.md frontmatter.

### Phase 3: Upgrade [SKIP if --check]

**--auto mode:** Proceed without asking.

**Interactive mode:** Ask user:
- Upgrade now (Recommended) / Skip / View changelog

**Upgrade process:**

1. Determine `~/.claude/` path (`$HOME/.claude/` on Unix, `$USERPROFILE\.claude\` on Windows)
2. For each file in the release, WebFetch raw content from GitHub:
   - `rules/cco-rules.md` → `~/.claude/rules/cco-rules.md`
   - `commands/cco-optimize.md` → `~/.claude/commands/cco-optimize.md`
   - `commands/cco-align.md` → `~/.claude/commands/cco-align.md`
   - `commands/cco-commit.md` → `~/.claude/commands/cco-commit.md`
   - `commands/cco-research.md` → `~/.claude/commands/cco-research.md`
   - `commands/cco-preflight.md` → `~/.claude/commands/cco-preflight.md`
   - `commands/cco-docs.md` → `~/.claude/commands/cco-docs.md`
   - `commands/cco-update.md` → `~/.claude/commands/cco-update.md`
   - `agents/cco-agent-analyze.md` → `~/.claude/agents/cco-agent-analyze.md`
   - `agents/cco-agent-apply.md` → `~/.claude/agents/cco-agent-apply.md`
   - `agents/cco-agent-research.md` → `~/.claude/agents/cco-agent-research.md`
3. Write each file with Write tool
4. Update `cco_version` and `last_update_check` in cco-rules.md frontmatter

**Source URL pattern:** `https://raw.githubusercontent.com/sungurerdim/ClaudeCodeOptimizer/v{VERSION}/{path}`

### Phase 4: Verify

Read cco-rules.md frontmatter → confirm `cco_version` matches latest.

### Phase 5: Summary

| Mode | Output |
|------|--------|
| `--check` | `CCO: v{current} (up to date)` or `CCO: v{current} → v{latest} available. Run /cco-update to upgrade.` |
| `--auto` | `cco-update: {OK\|FAIL} \| v{current} → v{latest}` |
| Interactive | Version info, files updated count, restart reminder |

**Restart reminder:** "Restart Claude Code session to load updated rules."

## Recovery

| Situation | Recovery |
|-----------|----------|
| Update failed mid-way | Re-run `/cco-update` |
| Wrong version | Re-run `/cco-update --auto` |
| Want to rollback | Re-run installer with specific version tag |
