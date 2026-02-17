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

Run `git diff main...HEAD` and describe what that diff shows.

## Context

- Branch: !`git branch --show-current 2>/dev/null || echo ""`
- Commits on branch: !`git log --oneline main..HEAD 2>/dev/null || echo ""`
- Existing PR: !`gh pr list --head $(git branch --show-current) --json number,title,state,url -L1 2>/dev/null`

## Flags

| Flag | Effect |
|------|--------|
| `--auto` | No questions, auto-detect everything, create PR directly |
| `--no-auto-merge` | Skip auto-merge setup |
| `--preview` | Show PR plan without creating |
| `--draft` | Create as draft PR (implies --no-auto-merge) |

## Execution Flow

Validate → Quality Gates → Analyze → Build → [Review] → Create → [Merge Setup] → Summary

### Phase 1: Validate

1. Verify `git` and `gh` available
2. `git fetch origin main`
3. On main/master → stop: "Create a branch first."
4. No commits ahead → stop: "No commits to create PR for."
5. Branch behind main → ask rebase (--auto: rebase automatically, abort on conflict)
6. Unpushed commits → `git push -u origin {branch}`
7. PR already exists → show URL, ask: Update / Skip
8. Verify repo settings: `gh api repos/{owner}/{repo} --jq '{squash: .allow_squash_merge, title: .squash_merge_commit_title, msg: .squash_merge_commit_message, delete: .delete_branch_on_merge, auto_merge: .allow_auto_merge}'`
   - Expected: squash=true, title=PR_TITLE, msg=PR_BODY, delete=true, auto_merge=true
   - Mismatch → ask to fix (--auto: fix via `gh api -X PATCH`)

### Phase 2: Quality Gates [ENTIRE PROJECT]

Run format, lint, and test across the **entire project**. Auto-fix all fixable issues.

**Detect toolchain:** Read CLAUDE.md blueprint (`Toolchain:` within `cco-blueprint-start/end`). No blueprint → auto-detect from project files + suggest `/cco-blueprint --init`.

**Run in order (stop on failure):**
1. **Format** — project's formatter with auto-fix (gofmt, prettier, ruff format, rustfmt, etc.)
2. **Lint** — project's linter with auto-fix (golangci-lint --fix, eslint --fix, ruff check --fix, etc.)
3. **Test** — project's test runner (go test, npm test, pytest, etc.)

Multi-module projects: run in each module directory. Tool unavailable: skip, warn once.

If format/lint changed files → stage and commit as `chore: format and lint fixes`.
If tests fail → stop. Do NOT create PR with failing tests.

### Phase 3: Analyze

```bash
git diff main...HEAD          # THE source of truth for PR content
git diff main...HEAD --stat   # file-level summary
git log main..HEAD --oneline  # commit titles — only for type classification
```

**Net diff principle:** The PR describes `git diff main...HEAD`. Period. Commit history is only used to determine the conventional commit type. The body describes the final state difference, not the development journey.

**Type classification:**
1. Scan commit titles for conventional types
2. Any `feat` commit → PR type is `feat` (minor bump)
3. Only `fix` commits → PR type is `fix` (patch bump)
4. Only non-bumping types → PR type is the dominant one (no bump)
5. `!` in any commit type or `BREAKING CHANGE:` in any commit body → append `!`

**Anti-bump rules (release-please reads PR title for changelog):**
- `feat` = user can now DO something new they couldn't before. Internal improvement → `refactor`/`chore`
- `fix` = something was BROKEN for end users. Preventive improvement → `refactor`/`chore`
- When uncertain → prefer non-bumping type
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

Display: branch, title, type → bump effect, body preview.

Populate each option's `markdown` field with the PR body preview (title + summary + changes). This lets the user see exactly what will be created before confirming.

```javascript
AskUserQuestion([{
  question: "Create this pull request?",
  header: "PR Action",
  options: [
    { label: "Create + Auto-merge (Recommended)", description: "Squash + delete branch when checks pass",
      markdown: "{title}\n\n{body}\n\n── auto-merge: squash + delete branch" },
    { label: "Create PR only", description: "Merge manually later",
      markdown: "{title}\n\n{body}\n\n── merge: manual" },
    { label: "Create as draft", description: "Draft PR for further work",
      markdown: "{title}\n\n{body}\n\n── status: draft" },
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

```bash
gh pr merge {number} --auto --squash
```

If auto-merge unsupported: `gh pr merge {number} --squash`

After merge: `git checkout main && git pull origin main`, delete local branch.

### Phase 7: Summary

PR URL, title, type → bump effect, auto-merge status. Auto-merge enabled: "You are now on main." Disabled: "Merge via GitHub."

--auto output: `cco-pr: {OK|FAIL} | {url} | {type} → {bump} | auto-merge: {on|off}`
