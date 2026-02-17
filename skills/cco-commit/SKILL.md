---
description: Smart git commits with quality gates, atomic grouping, and conventional commit format. Use when committing changes or the user asks to commit.
argument-hint: "[--preview] [--single] [--staged-only]"
allowed-tools: Read, Grep, Edit, Bash, AskUserQuestion
---

# /cco-commit

**Smart Commits** — Fast quality gates + atomic grouping, no unnecessary questions.

## Context

- Git status: !`git status --short 2>/dev/null || echo ""`
- Branch: !`git branch --show-current 2>/dev/null || echo ""`
- Recent commits: !`git log --oneline -5 2>/dev/null || echo ""`
- All changes (staged+unstaged): !`git diff HEAD --shortstat 2>/dev/null || echo ""`
- Staged only: !`git diff --cached --shortstat 2>/dev/null || echo ""`
- Unpushed commits: !`git log @{upstream}..HEAD --oneline 2>/dev/null || echo ""`

**Scope:** All uncommitted changes included by default (staged + unstaged + untracked). Use `--staged-only` for staged changes only.

## Flags

| Flag | Effect |
|------|--------|
| `--preview` | Show commit plan only, don't execute |
| `--single` | Force single commit |
| `--staged-only` | Commit only staged changes |

## Execution Flow

Pre-checks → Analyze → Execute → Verify → Summary

### Phase 1: Pre-checks + Quality Gates

**1.1 Prerequisites:** Verify `git` available. Fetch remote: `git fetch origin main 2>/dev/null` (best-effort).

**1.2 Main branch guard [ON MAIN ONLY]:** If on `main` or `master`:

1. Check existing feature branches: `git branch --list 'feat/*' 'fix/*' 'chore/*' 'refactor/*' 'docs/*' 'ci/*' 'test/*' 'perf/*' --sort=-committerdate`
2. Early-analyze changes (Phase 2 logic) to classify scope and generate branch candidates
3. Ask user where changes should go:

```javascript
AskUserQuestion([{
  question: "You're on main. Where should these changes go?",
  header: "Branch",
  options: [
    // Up to 2 existing branches (most recent first):
    { label: "{existing-branch}", description: "Continue on this branch ({n} commits ahead)" },
    // Up to 2 new branch candidates from analysis:
    { label: "New: {type}/{description}", description: "{n} files — {summary}" },
    // Always last:
    { label: "Commit on main", description: "Not recommended for release-please repos" }
  ],
  multiSelect: false
}])
// Single scope + no existing branches → simpler "Create branch?" / "Commit on main" prompt
```

| Decision | Action |
|----------|--------|
| Existing branch | `git checkout {branch}` — uncommitted changes carry over |
| New branch | `git checkout -b {type}/{description}` |
| Multiple scopes, user picks one | `git stash` the rest, checkout branch, commit selected, `git stash pop` |
| Commit on main | Skip guard, proceed normally |

Branch naming: `{type}/{short-description}`, all lowercase, hyphens, max 50 chars.

**1.3 Conflict check:** `UU`/`AA`/`DD` in status → stop.

**1.4 File type detection:** Categorize as code, test, tested-content (skills/, agents/, rules/), docs, config.

**1.5 Quality Gates [CHANGED FILES ONLY]:**
- Always: secret scan + large file check on changed files
- Code changes: format + lint on changed files only (no tests)
  - Detect toolchain from CLAUDE.md blueprint (`Toolchain:` line within `cco-blueprint-start/end` markers), or auto-detect from project files (go.mod, package.json, pyproject.toml, Cargo.toml, etc.). If no blueprint found, suggest: "Tip: Run `/cco-blueprint --init` to save toolchain config."
  - Run the project's formatter with auto-fix on changed files only
  - Run the project's linter with auto-fix on changed files/packages only
  - If a tool is not installed or not configured: skip, warn once
- Pure docs/config: skip all code checks
- If format/lint changed files: include those changes in the commit

**1.6 Gate failure [CONDITIONAL]:** Ask "Fix first (Recommended)" or "Commit anyway".

### Phase 2: Analyze Changes

Read git diff. Collect all uncommitted changes.

**Amend detection (unpushed commits only):**

| Condition | Action |
|-----------|--------|
| Trivial change (≤3 lines) | Amend most recent unpushed commit |
| File overlap with unpushed commit | Amend that commit |
| Same logical scope as unpushed commit | Amend that commit |
| No overlap and non-trivial | New commit |

Amend: `git add {files} && git commit --amend --no-edit`. Update message if it no longer describes changes. Safety: never amend pushed commits.

**Smart grouping:** ≤5 files or single logical change → single commit. Multiple distinct changes → split. Default: single.

Display commit plan table: type, title, file count. If amending: `(amend → {short-hash})`.

### Phase 3: Execute Commits [DIRECT]

No approval question — table was shown, commit directly. Skip in `--preview`.

Stage files → build conventional commit message → create commit.

**Title:** `type(scope): title` ≤50 chars. If >50 → ask user. Scope: directory where >50% of files changed, omit if no majority.

**Type detection (release-please compatible):**

| Type | Bump | When |
|------|------|------|
| `feat` | minor | New user-facing capability |
| `fix` | patch | Corrects broken behavior |
| `feat!`/`fix!` | major | Breaks existing consumers |
| `refactor` | none | Code restructuring, no behavior change |
| `chore` | none | Maintenance, deps, build config |
| `docs` | none | Documentation only |
| `perf` | none | Performance improvement |
| `test` | none | Test additions or fixes |
| `ci` | none | CI/CD pipeline changes |

**Anti-bump rules (CRITICAL for release-please):**
- `feat` = user can now DO something new. Internal → `refactor`/`chore`
- Improving existing behavior is NOT `feat` → `refactor`/`perf`/`chore`
- Docs, tests, CI, config, dev tooling are NEVER `feat`/`fix`
- `fix` = something was BROKEN. Preventive → `refactor`/`chore`
- Uncertain → prefer non-bumping type
- `BREAKING CHANGE` footer only for changes breaking existing consumers

**Message rules:**
1. Analyze git diff content only — not session memory
2. Describe what changed, not why
3. Breaking: `type!`, add BREAKING CHANGE footer
4. Trailer: `Co-Authored-By: {model} <noreply@anthropic.com>` — no non-trailer lines after body
5. Lowercase after colon: `feat(api): add endpoint` not `feat(api): Add endpoint`

### Phase 4: Verify

`git log` to confirm commits. Verify working tree clean (unless `--staged-only`).

### Phase 5: Summary

Commit count, file count, branch, commit list, next steps (`git push`). Stash reminder if applicable.
