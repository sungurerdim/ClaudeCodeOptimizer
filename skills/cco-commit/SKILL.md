---
description: Smart git commits with quality gates, atomic grouping, and conventional commit format.
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

### Phase 1: Pre-checks + Quality Gates [PARALLEL: 5 checks]

**1.0 Prerequisites:** Verify `git` is available (`git --version`). If missing → stop: "Install Git: https://git-scm.com". Then fetch remote main: `git fetch origin main 2>/dev/null` (best-effort, no-op if offline or no remote).

**1.0a Main branch guard:** If current branch is `main` or `master`:

**Step 1: Check existing feature branches**

```bash
git branch --list 'feat/*' 'fix/*' 'chore/*' 'refactor/*' 'docs/*' 'ci/*' 'test/*' 'perf/*' --sort=-committerdate
```

Existing branches = work in progress. `/cco-pr --auto-merge` deletes merged branches, so remaining ones mean unfinished work.

**Step 2: Early-analyze changes (Phase 2 logic, before branch decision)**

Read `git diff` and `git status` to classify uncommitted changes. Apply smart grouping:
- Single logical scope → one branch candidate (e.g., `feat/add-auth`)
- Multiple scopes detected → list them separately for user choice

**Step 3: Ask user**

```javascript
// When existing branches AND/OR multiple scopes detected:
AskUserQuestion([{
  question: "You're on main. Where should these changes go?",
  header: "Branch",
  options: [
    // Existing branches (if any, most recent first, max 2):
    { label: "{existing-branch}", description: "Continue on this branch ({n} commits ahead)" },
    // New branch candidates from analysis:
    { label: "New: {type}/{description}", description: "{n} files — {summary of changes}" },
    // Always last:
    { label: "Commit on main", description: "Not recommended for release-please repos" }
  ],
  multiSelect: false
}])

// When no existing branches AND single scope:
AskUserQuestion([{
  question: "You're on main. Create '{type}/{description}' for these changes?",
  header: "Branch",
  options: [
    { label: "Create branch (Recommended)", description: "{type}/{description} — {summary}" },
    { label: "Commit on main", description: "Not recommended for release-please repos" }
  ],
  multiSelect: false
}])
```

Options are dynamic: up to 2 existing branches + up to 2 new branch candidates = max 4 options.

**Step 4: Execute branch decision**

| Decision | Action |
|----------|--------|
| Existing branch | `git checkout {branch}` — uncommitted changes carry over |
| New branch | `git checkout -b {type}/{description}` — uncommitted changes carry over |
| Multiple scopes, user picks one | `git stash` the rest, `git checkout -b {branch}`, commit selected files, `git stash pop` after commit. If stash pop fails (conflict), warn: "Stash pop conflict — resolve manually with `git stash show` and `git stash drop` after resolving." |
| Commit on main | Skip guard, proceed normally |

After branch switch/creation: continue with Phase 2 (Analyze) on the branch. Subsequent `/cco-commit` calls see the feature branch → guard doesn't trigger → normal commit flow.

**Branch naming rules:**
- Format: `{type}/{short-description}` — all lowercase, hyphens for spaces
- Max 50 chars total
- Description from dominant change area, not individual files
- Examples: `feat/add-auth`, `fix/login-validation`, `chore/update-deps`, `refactor/extract-services`

**1.1 Conflict check:** If `UU`/`AA`/`DD` in git status → stop immediately.

**1.2 File type detection:** Categorize changed files as code, test, tested-content (skills/, agents/, rules/), docs, config.

**1.3 Quality Gates [PARALLEL, CONDITIONAL]:**

Run on full project (not just changed files):
- Always: secret scan + large file check on changed files
- If code changes: format, lint, type commands in parallel (background)
- If code/test/tested-content changes: test command (background)
- Pure docs/config only: skip tests

**1.4 Gate failure:** Ask "Fix first (Recommended)" or "Commit anyway". Show error details on fix.

### Phase 2: Analyze Changes

Collect all uncommitted changes. Read git diff for analysis.

**Amend detection (unpushed commits):**

If there are unpushed commits on the current branch, check whether new changes should amend an existing commit instead of creating a new one:

| Condition | Action |
|-----------|--------|
| Change is trivial (≤3 lines or single-line fix) | Amend to most recent unpushed commit |
| Changed file(s) overlap with files in an unpushed commit | Amend to that commit (most relevant match) |
| Change is in the same logical scope as an unpushed commit | Amend to that commit |
| Multiple unpushed commits match | Prefer the most recent one |
| No overlap and non-trivial | Create new commit (normal flow) |

**Amend execution:** `git add {files} && git commit --amend --no-edit` (preserves original message). If the amended commit's message no longer accurately describes the changes, update it.

**Safety:** Only amend commits that have NOT been pushed. Never amend if `git log @{upstream}..HEAD` is empty or upstream tracking fails with no `origin/{branch}` match (means branch was already pushed or is tracking).

**Smart grouping:** ≤5 files or single logical change → single commit. Multiple distinct logical changes → split into separate commits. Default: single commit.

Display commit plan table: type, title, file count. If amending, show `(amend → {short-hash})` next to the entry.

### Phase 3: Execute Commits [DIRECT]

No approval question — table was shown, commit directly. Skip in `--preview` mode.

For each commit: stage files → build conventional commit message → create commit.

**Title Rules:**
- Format: `type(scope): title` or `type!: title` for breaking
- Must be ≤50 characters total
- If >50 chars → stop and ask user

**Scope detection:** Directory where >50% of files changed. No majority → omit scope.

**Type detection (release-please compatible):**

| Type | Release Bump | When | Examples |
|------|-------------|------|----------|
| `feat` | **minor** | New user-facing capability that didn't exist before | New endpoint, new CLI flag, new UI component |
| `fix` | **patch** | Corrects broken behavior users can observe | Bug fix, crash fix, incorrect output |
| `feat!`/`fix!` | **major** | Change that breaks existing consumers | Removed endpoint, renamed export, changed return type |
| `refactor` | none | Code restructuring with no behavior change | Extract function, rename internal var, reorganize files |
| `chore` | none | Maintenance, dependencies, build config | Update deps, CI config, linter rules, internal tooling |
| `docs` | none | Documentation only | README, comments, API docs, changelog |
| `perf` | none | Performance improvement, no new behavior | Cache optimization, query tuning, lazy loading |
| `test` | none | Test additions or fixes | New test cases, fix flaky test |
| `ci` | none | CI/CD pipeline changes | Workflow files, deployment scripts |

**Anti-bump rules (CRITICAL for release-please):**
- `feat` = something a user/consumer can now DO that they couldn't before. If it's internal → `refactor` or `chore`
- Improving existing behavior (faster, cleaner, more robust) is NOT `feat` → use `refactor`, `perf`, or `chore`
- Adding/updating docs, tests, CI, config, or dev tooling is NEVER `feat` or `fix`
- `fix` = something was BROKEN and now works. Preventive improvements are `refactor` or `chore`
- When uncertain between `feat`/`fix` and a non-bumping type → prefer the non-bumping type
- `BREAKING CHANGE` footer only for changes that break existing consumers (API, CLI, library users)

**Message rules:**
1. Analyze git diff content only — not session memory
2. Describe what changed, not why
3. Breaking changes: append exclamation mark to type (e.g., feat!), add BREAKING CHANGE footer with description of what breaks
4. Append trailer only: `Co-Authored-By: {model} <noreply@anthropic.com>` — no other non-trailer lines after the body (GitHub ignores trailers if non-trailer content is mixed in)
5. Title must be lowercase after the colon (e.g., `feat(api): add user endpoint` not `feat(api): Add user endpoint`)

### Phase 4: Verify

Check commits created successfully via `git log`. Verify working tree clean (unless `--staged-only`).

### Phase 5: Summary

Show: commit count, file count, branch, status, commit list, next steps (`git push`). Stash reminder if applicable.
