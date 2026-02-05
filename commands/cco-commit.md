---
description: Smart git commits with quality gates and atomic grouping
argument-hint: "[--preview] [--single] [--staged-only]"
allowed-tools: Read, Grep, Edit, Bash, AskUserQuestion
model: opus
---

# /cco-commit

**Smart Commits** — Fast quality gates + atomic grouping, no unnecessary questions.

## Context

- Git status: !`git status --short 2>/dev/null || echo ""`
- Branch: !`git branch --show-current 2>/dev/null || echo ""`
- Recent commits: !`git log --oneline -5 2>/dev/null || echo ""`
- Stash list: !`git stash list --oneline 2>/dev/null | head -3`
- All changes (staged+unstaged): !`git diff HEAD --shortstat 2>/dev/null || echo ""`
- Staged only: !`git diff --cached --shortstat 2>/dev/null || echo ""`
- Untracked files: !`git ls-files --others --exclude-standard 2>/dev/null | wc -l`

**DO NOT re-run these commands. Use the pre-collected values above.**

**[CRITICAL] Scope:** ALL uncommitted changes included by default (staged + unstaged + untracked). Use `--staged-only` for staged changes only.

## Update Check

1. Read `cco_version` and `last_update_check` from context (cco-rules.md frontmatter, already loaded)
2. If last check >24 hours ago → `/cco-update --check`
3. New version available → display: `CCO vX.Y.Z available. Run /cco-update to upgrade.`

## Flags

| Flag | Effect |
|------|--------|
| `--preview` | Show commit plan only, don't execute |
| `--single` | Force single commit |
| `--staged-only` | Commit only staged changes |

## Execution Flow

Pre-checks → Analyze → Execute → Verify → Summary

### Phase 1: Pre-checks + Quality Gates [PARALLEL]

**1.1 Conflict check [BLOCKER]:** If `UU`/`AA`/`DD` in git status → stop immediately.

**1.2 File type detection:** Categorize changed files as code, test, tested-content (commands/, agents/, rules/), docs, config.

**1.3 Quality Gates [PARALLEL + CONDITIONAL]:**

Run on full project (not just changed files):
- Always: secret scan + large file check on changed files
- If code changes: format, lint, type commands in parallel (background)
- If code/test/tested-content changes: test command (background)
- Pure docs/config only: skip tests

**1.4 Gate failure:** Ask "Fix first (Recommended)" or "Commit anyway". Show error details on fix.

### Phase 2: Analyze Changes

Collect all uncommitted changes. Read git diff for analysis.

**Smart grouping:** ≤5 files or single logical change → single commit. Different features/scopes → split (only with `--split`). Default: single commit.

Display commit plan table: type, title, file count.

### Phase 3: Execute Commits [DIRECT]

No approval question — table was shown, commit directly. Skip in `--preview` mode.

For each commit: stage files → build conventional commit message → create commit.

**Title Rules [CRITICAL]:**
- Format: `type(scope): title` or `type!: title` for breaking
- MUST be ≤50 characters total
- If >50 chars → STOP and ask user

**Scope detection:** Directory where >50% of files changed. No majority → omit scope.

**Type detection (release-please compatible):**

| Type | Release Bump | When |
|------|-------------|------|
| `feat` | minor | New functionality |
| `fix` | patch | Bug fixes |
| `feat!`/`fix!` | major | Breaking changes |
| `refactor` | none | Code restructuring |
| `perf`/`test`/`docs`/`ci`/`chore` | none | Internal changes |

**Message rules:**
1. ONLY analyze git diff content — NEVER use session memory
2. Describe WHAT changed, not WHY
3. Breaking changes: append `!` to type, add `BREAKING CHANGE:` footer
4. Append signature: `Generated with [Claude Code]` + `Co-Authored-By: {model} <noreply@anthropic.com>`

### Phase 4: Verify

Check commits created successfully via `git log`. Verify working tree clean (unless `--staged-only`).

### Phase 5: Summary

Show: commit count, file count, branch, status, commit list, next steps (`git push`). Stash reminder if applicable.

## Recovery

| Situation | Recovery |
|-----------|----------|
| Wrong files | `git reset --soft HEAD~1` |
| Bad message | `git commit --amend` (if not pushed) |
| Gate broke something | `git checkout -- {file}` |
