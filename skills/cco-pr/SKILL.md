---
description: Create pull requests with conventional commit titles for clean release-please changelogs. Use when creating a PR or preparing changes for merge.
argument-hint: "[--auto] [--no-auto-merge] [--preview] [--draft]"
allowed-tools: Read, Grep, Glob, Bash, AskUserQuestion
---

# /cco-pr

**Smart Pull Requests** — Conventional commit title + clean body for release-please.

## Pipeline

```
PR title  →  squash merge on main  →  release-please reads title  →  changelog + version bump
```

The PR title IS the changelog entry. The PR body becomes the squash commit body. Everything must be accurate and minimal.

## Golden Rule

**The PR describes the net diff between main and HEAD — nothing else.** Not the journey of individual commits, not session decisions, not what was tried and reverted. If commit A added something and commit B removed it, the net effect is zero — do not mention it.

Run `git diff {base}...HEAD` (where `{base}` is detected in Phase 1) and describe what that diff shows.

## Context

- Status: !`git status --short --branch 2>/dev/null | cat`
- Commits on branch: !`git log --oneline $(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo main)..HEAD 2>/dev/null | cat`
- Existing PR: !`gh pr list --head "$(git branch --show-current 2>/dev/null)" --json number,title,state,url -L1 2>/dev/null | cat`

## Flags

| Flag | Effect |
|------|--------|
| `--auto` | No questions, auto-detect everything, create PR directly |
| `--no-auto-merge` | Skip auto-merge setup |
| `--preview` | Show PR plan without creating |
| `--draft` | Create as draft PR (implies --no-auto-merge) |

## Execution Flow

Validate → Quality Gates → Analyze → Build → [Review] → Create → [Merge Setup] → [Cleanup] → Summary

### Phase 1: Validate

**Steps 1-4 are independent — run in parallel. Steps 12-14 are independent of 8-11 — start in parallel with step 8.**

**Batch hints (minimize calls):**
- Steps 1, 4, 6: derive from context — if status returned output with branch name, git+repo+branch are verified
- Steps 2-3 → single runtime call: `gh auth status 2>&1` (verifies both gh available and authenticated)
- Steps 9+10 → single call: `git rev-list --left-right --count origin/{base}...HEAD` (left=behind, right=ahead)
- Step 11: derive from context — `[ahead N]` in status output = unpushed commits exist, no separate call needed
- Steps 12-14 → parallel: 3 calls in one message

1. Verify `git` available → not found: stop with "git is required"
2. Verify `gh` available → not found: stop with "gh CLI is required (https://cli.github.com)"
3. Verify `gh auth status` → not authenticated: stop with "Run `gh auth login` first"
4. Verify git repo: `git rev-parse --git-dir` → not a repo: stop with "Not a git repository"
5. Detect base branch: `git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@'` → fallback to `main`, then `master`, then stop
6. Verify not detached HEAD: `git branch --show-current` → empty: stop with "Detached HEAD — checkout a branch first"
7. On {base} → stop: "Create a branch first. Use `/cco-commit` to start."
8. `git fetch origin {base}`
9. No commits ahead of {base} → stop: "No commits to create PR for."
10. Branch behind {base} → ask rebase (--auto: rebase automatically, abort on conflict)
11. Unpushed commits → `git push -u origin {branch}`
12. PR already exists → show URL, ask: Update / Skip
13. Verify repo settings: `gh api repos/{owner}/{repo} --jq '{squash: .allow_squash_merge, title: .squash_merge_commit_title, msg: .squash_merge_commit_message, delete: .delete_branch_on_merge, auto_merge: .allow_auto_merge}'`
    - Expected: squash=true, title=PR_TITLE, msg=PR_BODY, delete=true
    - Mismatch → ask to fix (--auto: fix via `gh api -X PATCH`)
    - Detect branch protection: `gh api repos/{owner}/{repo}/branches/{base}/protection --jq '.required_status_checks.contexts' 2>/dev/null` — non-empty output = protected, empty/error = no protection. Note: `gh api` may return non-zero exit code even on success; check stdout content, not exit code.
14. Stale branch scan: `git for-each-ref --sort=committerdate refs/heads/ --format='%(refname:short) %(committerdate:relative)' --no-merged={base}` — exclude current branch, cross-reference with `gh pr list --state open --json headRefName --jq '.[].headRefName'`
    - Branches with no open PR and last commit >7 days ago → display: "Possibly forgotten: {branch} ({age}). Create PR or delete?"
    - --auto: skip (informational only)

### Phase 2: Quality Gates [ENTIRE PROJECT]

Run format, lint, and test across the **entire project**. Auto-fix all fixable issues.

**Detect toolchain:** Read CLAUDE.md blueprint (`Toolchain:` within `cco-blueprint-start/end`). No blueprint → auto-detect from project files: `package.json` scripts → npm, `go.mod` → go vet/test, `pyproject.toml` → ruff/pytest, `Cargo.toml` → cargo clippy/test, `Makefile` → make targets. Tool not found → skip silently.

**Run in order (stop on failure):**
1. **Format** — project's formatter with auto-fix (gofmt, prettier, ruff format, rustfmt, etc.)
2. **Lint** — project's linter with auto-fix (golangci-lint --fix, eslint --fix, ruff check --fix, etc.)
3. **Test** — project's test runner (go test, npm test, pytest, etc.)

Multi-module projects: run in each module directory. Tool unavailable: skip, warn once.

If format/lint changed files → stage and commit as `chore: format and lint fixes`.
If tests fail → stop. Do NOT create PR with failing tests.

### Phase 3: Analyze

```bash
git diff {base}...HEAD          # THE source of truth for PR content and file summary
```

Commit titles for type classification: use from Context section (already resolved at skill load). Do NOT re-run `git log` — it is redundant.

**Net diff principle:** The PR describes `git diff {base}...HEAD`. Period. Commit history is only used to determine the conventional commit type. The body describes the final state difference, not the development journey.

**Type classification (net diff is source of truth, not commit history):**
1. Scan commit titles for conventional types as **initial signal**
2. Validate against `git diff {base}...HEAD` — the net diff overrides commit types:
   - New user-facing capability in the final diff? → `feat`
   - Broken behavior fixed in the final diff? → `fix`
   - Neither? → dominant non-bumping type from commits
3. If commits say `feat` but net diff shows only internal restructuring → PR type is `refactor`/`chore`
4. `!` in any commit type or `BREAKING CHANGE:` in any commit body → append `!`

**Anti-bump rules (PR title = changelog entry = version bump):**

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
| Update skill/agent/rule prompts | feat | chore |
| Update dependencies | fix | chore |
| CI, docs, tests, config | feat/fix | ci/docs/test/chore |

- When uncertain → **always** prefer non-bumping type
- **Type ≠ scope.** `ci: fix config` = no bump. `fix(ci): fix config` = patch bump. Use the correct TYPE.
- CI, docs, tests, config, tooling → always `ci:`, `docs:`, `test:`, `chore:` — never `feat`/`fix`

**Title:** `{type}({scope}): {summary}` — max 70 chars. Scope: directory with >50% of changes, omit if no majority.

**Body:**

```markdown
## Summary
- {1-3 bullets — net changes vs main, max 15 words each}

## Changes
- {grouped by area, max 5 items — only what's in the final diff}

## Breaking Changes
- {only if breaking — what breaks + migration path}
```

**Body rules:**
- Describe the net diff, not the commit history
- No `## Test plan` — CI is the test plan
- No `Co-Authored-By` in body — commits already have it, GitHub auto-includes on squash merge
- Breaking changes: add `BREAKING CHANGE: {description}` as the last line
- Max 20 lines total

### Phase 4: Review [SKIP if --auto]

Display: branch, title, body preview, version annotation.

**Version annotation** — append to each option's markdown as the first `──` line:
- All signals agree: `── version: {type} → {effect}`
- Net diff overrode commits or borderline: `── version: ~{type} → {effect} (estimated)`

Effects: `feat` → minor bump, `fix` → patch bump, `feat!`/`fix!` → major bump, anything else → no bump.

```javascript
AskUserQuestion([{
  question: "Create this pull request?",
  header: "PR Action",
  options: [
    { label: "Create + Auto-merge (Recommended)", description: "Squash + delete branch when checks pass",
      markdown: "{title}\n\n{body}\n\n── version: {type} → {effect}\n── auto-merge: squash + delete branch" },
    { label: "Create PR only", description: "Merge manually later",
      markdown: "{title}\n\n{body}\n\n── version: {type} → {effect}\n── merge: manual" },
    { label: "Create as draft", description: "Draft PR for further work",
      markdown: "{title}\n\n{body}\n\n── version: {type} → {effect}\n── status: draft" },
    { label: "Cancel", description: "Don't create PR" }
  ],
  multiSelect: false
}])
```

### Phase 5: Create

```bash
gh pr create --title "{title}" --body "{body}" [--draft]
```

On error: display title and body for manual creation.

### Phase 6: Merge Setup [DEFAULT]

Skip when: `--no-auto-merge`, `--draft`, user selected "Create PR only" or "Create as draft".

**With branch protection (from step 13):**

```bash
gh pr merge {number} --auto --squash
```

**Without branch protection (direct merge):**

1. Check CI status: `gh pr checks {number} --json name,state --jq '.[].state' 2>/dev/null`
   - Any `FAILURE` → interactive: warn "CI checks failing. Merge anyway?"; --auto: merge anyway (CI is advisory without branch protection)
   - Otherwise → proceed
2. `gh pr merge {number} --squash`

After merge: `git checkout {base} && git pull origin {base}`, delete local branch.

### Phase 6.1: Branch Cleanup [AFTER MERGE ONLY]

Skip when: merge not completed, `--draft`, or user selected "Create PR only".

**Steps 1-2 are independent — run in parallel:**

1. Detect merged branches: `git branch --merged {base} | grep -vE '^\*|{base}$' || true`
2. Detect remote merged branches: `git branch -r --merged origin/{base} | grep -vE '{base}|HEAD' | sed 's/origin\///' || true`
3. Combine unique results, exclude current branch

If merged branches found:

```javascript
AskUserQuestion([{
  question: "{n} merged branch(es) found. Clean up?",
  header: "Cleanup",
  options: [
    { label: "Delete all (Recommended)", description: "{branch-list}" },
    { label: "Skip", description: "Keep merged branches" }
  ],
  multiSelect: false
}])
```

On "Delete all": `git branch -d {branch}` for each local, `git push origin --delete {branch}` for remote-only. On error: warn and continue.

--auto: delete all silently.

### Phase 7: Summary

PR URL, title, type → bump effect, auto-merge status. Auto-merge enabled: "You are now on main." Disabled: "Merge via GitHub."

--auto output: `cco-pr: {OK|FAIL} | {url} | {type} → {bump} | auto-merge: {on|off}`
