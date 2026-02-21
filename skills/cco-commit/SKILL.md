---
description: Smart git commits with quality gates, atomic grouping, and conventional commit format. Use when committing changes or the user asks to commit.
argument-hint: "[--preview] [--single] [--staged-only]"
allowed-tools: Read, Grep, Edit, Bash, AskUserQuestion
---

# /cco-commit

**Smart Commits** — Quality gates + atomic grouping + conventional commit format.

## Golden Rule

**The commit message describes what `git diff` shows — nothing else.** Not what you discussed in the session, not what you tried and reverted, not what you planned. Read the diff, describe the diff.

## Context

- Status + branch: !`git status --short --branch`
- Recent commits: !`git log --oneline -5`
- All changes (staged+unstaged): !`git diff HEAD --shortstat`
- Staged only: !`git diff --cached --shortstat`

**Scope:** All uncommitted changes included by default (staged + unstaged + untracked). Use `--staged-only` for staged changes only.

## Flags

| Flag | Effect |
|------|--------|
| `--preview` | Show commit plan only, don't execute |
| `--single` | Force single commit |
| `--staged-only` | Commit only staged changes |

## Execution Flow

Pre-checks → Analyze → Execute → Verify → Summary

### Phase 1: Pre-checks

**1.1 Prerequisites:**
1. Verify `git` available → not found: stop with "git is required"

**Steps 2-4 are independent — run in parallel:**

2. Verify git repo: `git rev-parse --git-dir` → not a repo: stop with "Not a git repository. Run `git init` first."
3. Verify not detached HEAD: `git branch --show-current` → empty: stop with "Detached HEAD — checkout a branch first"
4. `git fetch origin 2>/dev/null` (best-effort, no stop on failure)

**1.2 Branch management:**

**On main/master:**

1. Scan feature branches: `git branch --list 'feat/*' 'fix/*' 'chore/*' 'refactor/*' 'docs/*' 'ci/*' 'test/*' 'perf/*' --sort=-committerdate`
2. Early-analyze uncommitted changes to classify type and scope
3. Ask user:

```javascript
AskUserQuestion([{
  question: "You're on main. Where should these changes go?",
  header: "Branch",
  options: [
    // Up to 2 existing branches (best scope match first, most recent second):
    { label: "{branch}", description: "{n} commits ahead · last: {relative time}" },
    // 1 new branch suggestion from change analysis:
    { label: "New: {type}/{desc} (Recommended)", description: "{n} files — {scope summary}" },
    // Always last — if release-please config found, description: "Not recommended — bypasses changelog pipeline"
    { label: "Commit on main", description: "Direct commit, skip branch workflow" }
  ],
  multiSelect: false
}])
```

| Decision | Action |
|----------|--------|
| Existing branch | `git checkout {branch}` — uncommitted changes carry over |
| New branch | `git checkout -b {type}/{desc}` |
| Commit on main | Proceed normally |

Branch naming: `{type}/{short-description}`, lowercase, hyphens, max 50 chars.

**On feature branch:** If changes don't match branch scope (e.g., on `feat/add-login` but changes are all CI files), ask:

```javascript
AskUserQuestion([{
  question: "Changes don't seem related to this branch ({branch}). Continue?",
  header: "Scope",
  options: [
    { label: "Continue here (Recommended)", description: "Include in current branch" },
    { label: "New branch", description: "Create {type}/{desc} from {base}" }
  ],
  multiSelect: false
}])
```

If "New branch": stash, checkout {base}, create branch, pop stash.

**1.3 Conflict check:** `UU`/`AA`/`DD` in status → stop.

**1.4 Quality Gates [CHANGED FILES ONLY]:**
- Always: secret scan + large file check
- Code files: format + lint (no tests) on changed files only
  - Detect toolchain (same pattern as cco-pr Phase 2): first check CLAUDE.md blueprint (`Toolchain:` within `cco-blueprint-start/end`). No blueprint → auto-detect from project files: `package.json` scripts → npm, `go.mod` → go vet, `pyproject.toml` → ruff, `Cargo.toml` → cargo clippy, `Makefile` → make lint. Per CCO Rules: Tool Prerequisites.
  - Run formatter then linter with auto-fix. Skip if tool unavailable.
- Docs/config only: skip code checks
- If format/lint modified files: include those changes in the commit
- On failure: ask "Fix first (Recommended)" or "Commit anyway"

### Phase 2: Analyze

Run `git diff` (or `git diff --cached` for `--staged-only`). This is the **only input** for building the commit message.

**Amend detection (unpushed commits only):**

First: check if upstream tracking exists: `git rev-parse @{upstream} 2>/dev/null`. If no upstream, treat ALL local commits as unpushed (compare against base branch instead: `git log {base}..HEAD`).

| Condition | Action |
|-----------|--------|
| ≤3 lines changed | Amend most recent unpushed commit |
| File overlap with unpushed commit | Amend that commit |
| Same logical scope as unpushed commit | Amend that commit |
| Otherwise | New commit |

Safety: never amend pushed commits. If amending, update message only if it no longer matches the diff.

**Smart grouping:** ≤5 files or single logical change → single commit. Multiple distinct changes → split. Default: single.

Display commit plan table: type, title, file count. If amending: `(amend → {short-hash})`.

### Phase 3: Execute [DIRECT]

No approval question — plan table was shown. Skip in `--preview`.

Stage files → build message → commit.

**Title:** `type(scope): description` — max 50 chars. Scope: directory with >50% of changes, omit if no majority.

**Conventional commit types:**

| Type | Version bump | Use when |
|------|-------------|----------|
| `feat` | minor | New user-facing capability |
| `fix` | patch | Corrects broken behavior for end users |
| `feat!`/`fix!` | major | Breaks existing consumers |
| `refactor` | none | Code restructuring, no behavior change |
| `chore` | none | Maintenance, deps, build config |
| `docs` | none | Documentation only |
| `perf` | none | Performance improvement |
| `test` | none | Test additions or fixes |
| `ci` | none | CI/CD pipeline changes |

**Anti-bump rules (release-please reads these types):**

Litmus test — both must be YES for a bump:

| Question | YES | NO |
|----------|-----|----|
| Can end users do something they **couldn't** before? | `feat` | `refactor`/`chore` |
| Was something **broken** for end users and now works? | `fix` | `refactor`/`chore` |

Common misclassifications:

| Change | Looks like | Actually |
|--------|-----------|----------|
| Add internal helper/utility | feat | refactor |
| Improve existing feature's code | feat | refactor/perf |
| Harden edge cases / add guards | fix | chore |
| Add missing types/validation | fix | chore |
| Update skill/agent/rule prompts | feat | chore |
| Update dependencies | fix | chore |
| CI, docs, tests, config | feat/fix | ci/docs/test/chore |

- When uncertain → **always** prefer non-bumping type
- **Type ≠ scope.** `ci: fix config` = no bump. `fix(ci): fix config` = patch bump. Use the correct TYPE.
- CI, docs, tests, config, tooling → always their own type, never `feat`/`fix`

**Message construction:**
1. Read `git diff` — this is the sole input
2. Title: lowercase after colon, imperative mood — `feat(api): add endpoint` not `feat(api): Add endpoint`
3. Body (optional): only if the change is non-obvious. Keep it to 1-3 lines.
4. Trailer: exactly one `Co-Authored-By: {model} <noreply@anthropic.com>` — no duplicates, no non-trailer lines after it
5. Breaking changes: use `type!` in title + `BREAKING CHANGE: description` footer

### Phase 4: Verify

`git log` to confirm. Verify working tree clean (unless `--staged-only`).

### Phase 5: Summary

Commit count, file count, branch, commit hashes. Next step: `git push` or `/cco-pr`.
