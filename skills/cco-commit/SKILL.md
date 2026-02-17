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

- Git status: !`git status --short 2>/dev/null | cat`
- Branch: !`git branch --show-current 2>/dev/null | cat`
- Recent commits: !`git log --oneline -5 2>/dev/null | cat`
- All changes (staged+unstaged): !`git diff HEAD --shortstat 2>/dev/null | cat`
- Staged only: !`git diff --cached --shortstat 2>/dev/null | cat`
- Unpushed commits: !`git log @{upstream}..HEAD --oneline 2>/dev/null | cat`

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

**1.1 Prerequisites:** Verify `git` available. `git fetch origin main 2>/dev/null` (best-effort).

**1.2 Main branch guard [ON MAIN ONLY]:** If on `main` or `master`:

1. Check existing feature branches: `git branch --list 'feat/*' 'fix/*' 'chore/*' 'refactor/*' 'docs/*' 'ci/*' 'test/*' 'perf/*' --sort=-committerdate`
2. Analyze changes to classify scope and generate branch candidates
3. Ask user:

```javascript
AskUserQuestion([{
  question: "You're on main. Where should these changes go?",
  header: "Branch",
  options: [
    // Up to 2 existing branches (most recent first):
    { label: "{existing-branch}", description: "Continue on this branch ({n} commits ahead)" },
    // Up to 2 new branch candidates:
    { label: "New: {type}/{description}", description: "{n} files — {summary}" },
    // Always last:
    { label: "Commit on main", description: "Not recommended for release-please repos" }
  ],
  multiSelect: false
}])
```

Branch naming: `{type}/{short-description}`, all lowercase, hyphens, max 50 chars.

**1.3 Conflict check:** `UU`/`AA`/`DD` in status → stop.

**1.4 Quality Gates [CHANGED FILES ONLY]:**
- Always: secret scan + large file check
- Code files: format + lint (no tests) on changed files only
  - Detect toolchain from CLAUDE.md blueprint (`Toolchain:` within `cco-blueprint-start/end`) or auto-detect from project files. No blueprint → suggest `/cco-blueprint --init`.
  - Run formatter then linter with auto-fix. Skip if tool unavailable.
- Docs/config only: skip code checks
- If format/lint modified files: include those changes in the commit
- On failure: ask "Fix first (Recommended)" or "Commit anyway"

### Phase 2: Analyze

Run `git diff` (or `git diff --cached` for `--staged-only`). This is the **only input** for building the commit message.

**Amend detection (unpushed commits only):**

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
- `feat` = user can now DO something new they couldn't before. Internal improvement → `refactor`/`chore`
- `fix` = something was BROKEN for end users. Preventive improvement → `refactor`/`chore`
- When uncertain → prefer non-bumping type
- **Type ≠ scope.** `ci: fix config` = no bump. `fix(ci): fix config` = patch bump. Use the correct TYPE for the change category, not `fix`/`feat` with a scope qualifier.
- CI, docs, tests, config, tooling → always use their own type (`ci:`, `docs:`, `test:`, `chore:`), never `feat`/`fix`

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
