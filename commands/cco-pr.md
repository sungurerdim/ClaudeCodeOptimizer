---
description: Create pull requests with conventional commit titles for clean release-please changelogs
argument-hint: "[--auto] [--preview] [--draft]"
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
| `--preview` | Show PR plan without creating |
| `--draft` | Create as draft PR |

## Execution Flow

Validate → Analyze → Build PR → [Review] → Create → Summary

### Phase 1: Validate

1. If on main/master → stop: "Create a branch first. Cannot PR from main."
2. If no commits ahead of base → stop: "No commits to create PR for."
3. If `gh` not available → stop: "Install GitHub CLI: https://cli.github.com"
4. If unpushed commits → `git push -u origin {branch}` automatically
5. If PR already exists → show existing PR URL and ask: Update / Skip

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

## Test plan
- [ ] {verification steps}

Co-Authored-By: {model} <noreply@anthropic.com>
```

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
    { label: "Create PR (Recommended)", description: "Create PR with the title and body shown above" },
    { label: "Edit title", description: "Let me change the title before creating" },
    { label: "Create as draft", description: "Create as draft PR for further work" },
    { label: "Cancel", description: "Don't create PR" }
  ],
  multiSelect: false
}])
```

If "Edit title" → ask user for new title, validate conventional commit format.

### Phase 4: Create

```bash
gh pr create --title "{title}" --body "{body}" [--draft]
```

If `--draft` flag or user selected draft → add `--draft`.

On error: If `gh pr create` fails, display the title and body for manual creation.

### Phase 5: Summary

```
PR CREATED
==========
URL:    {pr_url}
Title:  {title}
Branch: {branch} → main
Type:   {type} → {bump effect on next release}
Draft:  {yes/no}

Next: Review and merge via GitHub
      Squash merge will use this title as the commit message
```

--auto mode: `cco-pr: {OK|FAIL} | {pr_url} | {type} → {bump}`

## Release-Please Integration

This command is designed for repos using release-please with squash merge:

```
Branch commits → /cco-pr → PR with conventional title → Squash merge →
  → main has 1 clean conventional commit → release-please reads it →
  → Clean changelog entry (1 line, no duplicates)
```

**Required GitHub repo setting** (one-time):
- Settings → General → Pull Requests → Allow squash merging
- Default commit message: "Pull request title and description"

This ensures the squash commit uses the PR title (conventional commit) as the commit message, not the concatenated individual commit messages.
