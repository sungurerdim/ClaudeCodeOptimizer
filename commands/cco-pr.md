---
description: Create pull requests with conventional commit titles for clean release-please changelogs
argument-hint: "[--auto] [--auto-merge] [--preview] [--draft]"
allowed-tools: Read, Grep, Glob, Bash, AskUserQuestion
model: opus
---

# /cco-pr

**Smart Pull Requests** — Conventional commit title + clean body for release-please compatibility.

**Philosophy:** The PR title becomes the squash commit message on main. Release-please reads that commit. So the PR title IS the changelog entry — get it right.

## Context

- Branch: !`git branch --show-current 2>/dev/null || echo ""`
- Base branch: !`git log --oneline main..HEAD 2>/dev/null | wc -l` commits ahead of main
- Remote: !`git remote -v 2>/dev/null | head -1`
- Recent commits on branch: !`git log --oneline main..HEAD 2>/dev/null | head -20`
- PR status: !`gh pr status --json number,title,state 2>/dev/null || echo "gh not available"`

## Flags

| Flag | Effect |
|------|--------|
| `--auto` | No questions, auto-detect everything, create PR directly |
| `--auto-merge` | Enable auto-merge after PR creation (merges when checks pass, deletes branch) |
| `--preview` | Show PR plan without creating |
| `--draft` | Create as draft PR |

## Execution Flow

Validate → Analyze → Build PR → [Review] → Create → [Merge Setup] → Summary

### Phase 1: Validate

1. Verify `git` is available (`git --version`). If missing → stop: "Install Git: https://git-scm.com"
2. Verify `gh` is available (`gh --version`). If missing → stop: "Install GitHub CLI: https://cli.github.com"
3. If on main/master → stop: "Create a branch first. Cannot PR from main."
4. If no commits ahead of base → stop: "No commits to create PR for."
5. If unpushed commits → `git push -u origin {branch}` automatically
6. If PR already exists → show existing PR URL and ask: Update / Skip
7. Check if branch is behind main:
   ```bash
   git fetch origin main
   git merge-base --is-ancestor origin/main HEAD
   ```
   If main has new commits not in branch:
   ```javascript
   AskUserQuestion([{
     question: "Branch is behind main. How to proceed?",
     header: "Sync",
     options: [
       { label: "Rebase (Recommended)", description: "git rebase origin/main — clean linear history" },
       { label: "Continue anyway", description: "Create PR without rebasing (may have merge conflicts)" },
       { label: "Cancel", description: "Abort PR creation" }
     ],
     multiSelect: false
   }])
   ```
   In `--auto` mode: rebase automatically. On conflict → `git rebase --abort`, warn, continue with PR.
8. Verify repo settings (first run per repo, cached):
   ```bash
   gh api repos/{owner}/{repo} --jq '{squash: .allow_squash_merge, title: .squash_merge_commit_title, msg: .squash_merge_commit_message, delete: .delete_branch_on_merge}'
   ```
   Expected: `squash=true, title=PR_TITLE, msg=PR_BODY, delete=true`
   If mismatch found and not `--auto`:
   ```javascript
   AskUserQuestion([{
     question: "Repo settings need adjustment for release-please compatibility. Fix now?",
     header: "Settings",
     options: [
       { label: "Fix all (Recommended)", description: "Enable squash merge with PR_TITLE format, auto-delete branches" },
       { label: "Skip", description: "Continue without fixing (changelog entries may be affected)" }
     ],
     multiSelect: false
   }])
   ```
   Fix via: `gh api repos/{owner}/{repo} -X PATCH -f allow_squash_merge=true -f squash_merge_commit_title=PR_TITLE -f squash_merge_commit_message=PR_BODY -f delete_branch_on_merge=true`
   In `--auto` mode: fix automatically, log changes.

On error: Display clear message with fix instructions.

### Phase 2: Analyze [ALL commits on branch]

Read all commits since base branch divergence:

```bash
git log main..HEAD --format="%H %s"
git diff main...HEAD --stat
```

**Commit classification:**

1. Scan ALL commit titles for conventional commit types
2. Determine dominant type:

| Pattern | PR Type |
|---------|---------|
| Any `feat` commit | `feat` (minor bump) |
| `fix` only (no feat) | `fix` (patch bump) |
| Only `chore`/`docs`/`ci`/`refactor`/`test`/`perf` | Use dominant type (no bump) |
| Any breaking change (`!` or `BREAKING CHANGE`) | Add `!` to type (major bump) |

**Breaking change detection:**

Scan all branch commits for:
- `!` suffix in commit type (e.g., `feat!:`, `fix!:`)
- `BREAKING CHANGE:` or `BREAKING-CHANGE:` in commit body (`git log main..HEAD --format="%B"`)

If any found:
- PR title: add `!` to type (e.g., `feat!(scope): summary`)
- Body: add `## Breaking Changes` section (see body template below)
- Collect all breaking change descriptions from commit footers

3. Determine scope: directory where >50% of total changes occurred. No majority → omit.
4. Generate title: `{type}({scope}): {summary}` ≤70 chars

**Anti-bump rules (same as /cco-commit):**
- `feat` = user-facing NEW capability. Internal improvements → `refactor`/`chore`
- `fix` = something was BROKEN. Preventive work → `refactor`/`chore`
- When uncertain → prefer non-bumping type

**Body generation:**

```markdown
## Summary
- {1-3 bullet points describing what changed and why}

## Changes
- {key changes grouped by area, not per-commit}

## Breaking Changes
- {only if breaking changes detected, otherwise omit this section}
- {each breaking change with what breaks and migration path}

## Test plan
- [ ] {verification steps}

Co-Authored-By: {model} <noreply@anthropic.com>
```

**BREAKING CHANGE footer (release-please):**

When `## Breaking Changes` section is present, append a `BREAKING CHANGE` footer to the body (after Co-Authored-By). Release-please reads this footer from the squash commit body:

```
BREAKING CHANGE: {description of what breaks}
```

This ensures release-please triggers a major version bump even if the PR title uses `feat!` notation (belt and suspenders).

Body rules:
- Summarize the logical change, NOT list individual commits
- Group related changes (e.g., "Updated all command files for format consistency")
- Single Co-Authored-By trailer at the end (not per-commit)
- No commit hashes or individual commit references in body

### Phase 3: Review [SKIP if --auto]

Display PR plan:

```
PULL REQUEST PLAN
=================
Branch: {branch} → main ({n} commits)
Title:  {conventional commit title}
Type:   {type} → {bump effect}
Draft:  {yes/no}

## Summary
{body preview}
```

```javascript
AskUserQuestion([{
  question: "Create this pull request?",
  header: "PR Action",
  options: [
    { label: "Create + Auto-merge (Recommended)", description: "Create PR and enable auto-merge (squash + delete branch when checks pass)" },
    { label: "Create PR only", description: "Create PR, merge manually later on GitHub" },
    { label: "Create as draft", description: "Create as draft PR for further work" },
    { label: "Cancel", description: "Don't create PR" }
  ],
  multiSelect: false
}])
```

If "Create PR only" → skip Phase 5 (merge setup).

### Phase 4: Create

```bash
gh pr create --title "{title}" --body "{body}" [--draft]
```

If `--draft` flag or user selected draft → add `--draft`.

On error: If `gh pr create` fails, display the title and body for manual creation.

### Phase 5: Merge Setup [CONDITIONAL]

Triggers when: user selected "Create + Auto-merge", or `--auto-merge` flag, or `--auto` flag.

```bash
gh pr merge {number} --auto --squash --delete-branch
```

This tells GitHub to:
1. Squash merge the PR when all required checks pass (or immediately if no checks)
2. Delete the remote branch after merge

If auto-merge is not supported (no branch protection rules), fall back to immediate merge:
```bash
gh pr merge {number} --squash --delete-branch
```

On error: If merge setup fails, warn but don't fail. PR is already created. Display manual merge instructions.

**Local cleanup (after merge completes):**

After enabling auto-merge, switch to main and prepare for next work:

```bash
git checkout main && git pull origin main
```

If the branch was a feature branch (not `dev` or long-lived), delete local copy:
```bash
git branch -d {branch}
```

### Phase 6: Summary

```
PR CREATED
==========
URL:        {pr_url}
Title:      {title}
Branch:     {branch} → main
Type:       {type} → {bump effect on next release}
Auto-merge: {enabled|disabled}
Draft:      {yes/no}

{if auto-merge enabled}
Auto-merge is enabled. PR will squash-merge and branch will be deleted when checks pass.
You are now on main. Ready for next feature branch.

{if auto-merge disabled}
Next: Review and merge via GitHub (squash merge recommended)
```

--auto mode: `cco-pr: {OK|FAIL} | {pr_url} | {type} → {bump} | auto-merge: {on|off}`

## Release-Please Integration

This command is designed for repos using release-please with squash merge:

```
Branch commits → /cco-pr → PR with conventional title → Squash merge →
  → main has 1 clean conventional commit → release-please reads it →
  → Clean changelog entry (1 line, no duplicates)
```

**Required GitHub repo settings** (one-time):
- Settings → General → Pull Requests → Allow squash merging
- Default commit message: "Pull request title and description"
- **Automatically delete head branches**: ✅ (auto-cleanup remote branches after merge)

Optional (enables `--auto-merge`):
- Settings → Branches → Branch protection rule for `main` → Require status checks

This ensures the squash commit uses the PR title (conventional commit) as the commit message, not the concatenated individual commit messages.

## Feature Branch Workflow

Recommended workflow with `/cco-commit` + `/cco-pr`:

```
1. /cco-commit detects you're on main → creates feature branch automatically
2. Work + commit on feature branch
3. /cco-pr → creates PR + enables auto-merge
4. PR squash-merges → branch deleted → you're back on main
5. Repeat from step 1
```

This ensures:
- Clean main history (1 squash commit per PR)
- Release-please reads clean conventional commits
- No branch sync issues (feature branches are disposable)
- No manual branch management needed
