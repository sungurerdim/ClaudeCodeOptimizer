---
description: Create pull requests with conventional commit titles for clean release-please changelogs. Use when creating a PR or preparing changes for merge.
argument-hint: "[--auto] [--no-auto-merge] [--preview] [--draft]"
allowed-tools: Read, Grep, Glob, Bash, AskUserQuestion
---

# /cco-pr

**Smart Pull Requests** — Conventional commit title + clean body for release-please compatibility.

The PR title becomes the squash commit message on main → release-please reads it → changelog entry. PR title IS the changelog entry.

## Context

- Branch: !`git branch --show-current 2>/dev/null || echo ""`
- Commits on branch: !`git log --oneline main..HEAD 2>/dev/null || echo ""`
- Existing PR: !`gh pr view --json number,title,state,url 2>/dev/null || echo "none"`

## Flags

| Flag | Effect |
|------|--------|
| `--auto` | No questions, auto-detect everything, create PR directly |
| `--no-auto-merge` | Skip auto-merge setup |
| `--preview` | Show PR plan without creating |
| `--draft` | Create as draft PR (implies --no-auto-merge) |

## Execution Flow

Validate → Analyze → Build PR → [Review] → Create → [Merge Setup] → Summary

### Phase 1: Validate

1. Verify `git` and `gh` are available. Missing → stop with install link.
2. `git fetch origin main`
3. If on main/master → stop: "Create a branch first."
4. If no commits ahead of base → stop: "No commits to create PR for."
5. If unpushed commits → `git push -u origin {branch}`
6. If PR already exists → show URL, ask: Update / Skip
7. If branch behind main → ask rebase (--auto: rebase automatically, abort on conflict)
8. Verify repo settings (single API call): `gh api repos/{owner}/{repo} --jq '{squash: .allow_squash_merge, title: .squash_merge_commit_title, msg: .squash_merge_commit_message, delete: .delete_branch_on_merge, auto_merge: .allow_auto_merge}'`
   - Expected: squash=true, title=PR_TITLE, msg=PR_BODY, delete=true, auto_merge=true
   - Mismatch → ask to fix (--auto: fix automatically via `gh api -X PATCH`)

### Phase 2: Analyze [ALL commits on branch]

```bash
git log main..HEAD --format="%H %s"
git diff main...HEAD --stat
```

**Diff-over-messages:** Build PR body from `git diff main...HEAD`, NOT from commit messages. Commit messages inform type classification only.

**Commit classification:**
1. Scan ALL commit titles for conventional commit types
2. Dominant type: any `feat` → feat (minor), fix only → fix (patch), only chore/docs/ci/etc → dominant (no bump)
3. Breaking change: exclamation in type OR `BREAKING CHANGE:` in commit body → append `!` to PR type

**Scope:** directory where >50% of changes occurred. No majority → omit.

**Title:** `{type}({scope}): {summary}` ≤70 chars

**Anti-bump rules (CRITICAL for release-please):**
- `feat` = user can now DO something new. Internal → `refactor`/`chore`
- Improving existing behavior is NOT `feat` → `refactor`/`perf`/`chore`
- Docs, tests, CI, config, dev tooling are NEVER `feat`/`fix`
- `fix` = something was BROKEN. Preventive → `refactor`/`chore`
- Uncertain → prefer non-bumping type

**Body constraints:** Summary: 1-3 bullets, max 15 words per bullet. Changes: max 5 grouped items. Test plan: 2-4 items. Total body: max 30 lines.

**Body:**

```markdown
## Summary
- {1-3 bullet points — what changed and why}

## Changes
- {key changes grouped by area}

## Breaking Changes
- {only if breaking — what breaks + migration path}

## Test plan
- [ ] {verification steps}

Co-Authored-By: {model} <noreply@anthropic.com>
```

If breaking changes present, append `BREAKING CHANGE: {description}` footer after Co-Authored-By for release-please.

Body rules: summarize logical change (not per-commit list), single Co-Authored-By trailer.

### Phase 3: Review [SKIP if --auto]

Display PR plan (branch, title, type, bump effect, body preview).

```javascript
AskUserQuestion([{
  question: "Create this pull request?",
  header: "PR Action",
  options: [
    { label: "Create + Auto-merge (Recommended)", description: "Squash + delete branch when checks pass" },
    { label: "Create PR only", description: "Merge manually later" },
    { label: "Create as draft", description: "Draft PR for further work" },
    { label: "Cancel", description: "Don't create PR" }
  ],
  multiSelect: false
}])
```

### Phase 4: Create

```bash
gh pr create --title "{title}" --body "{body}" [--draft]
```

On error: display title and body for manual creation.

### Phase 5: Merge Setup [DEFAULT]

Skip when: `--no-auto-merge`, `--draft`, or user selected "Create PR only" / "Create as draft".

```bash
gh pr merge {number} --auto --squash
```

If auto-merge unsupported (no branch protection): `gh pr merge {number} --squash`

After merge setup: `git checkout main && git pull origin main`, delete local feature branch with `git branch -d {branch}`.

### Phase 6: Summary

PR URL, title, type → bump effect, auto-merge status, draft status. If auto-merge enabled: "You are now on main." If disabled: "Review and merge via GitHub."

--auto: `cco-pr: {OK|FAIL} | {pr_url} | {type} → {bump} | auto-merge: {on|off}`
