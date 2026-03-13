---
description: Repository structure, settings, CI/CD, and team configuration — audit and setup. Use for repo health, branch policies, CI validation, or team onboarding.
argument-hint: "[--auto] [--preview] [--scope=<name>]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Edit
  - Write
  - Task
  - AskUserQuestion
---

# /cco-repo

**Repository Health** — Audit and configure repo settings, branch policies, CI/CD, and team structure.

## Flags

| Flag | Effect |
|------|--------|
| `--auto` | All scopes, no questions, fix everything |
| `--preview` | Audit only, no changes |
| `--scope=X` | Specific scope(s), comma-separated |

## Context

- Git status: !`git status --short --branch`
- Args: $ARGUMENTS

## Scopes

| Scope | Focus |
|-------|-------|
| settings | Squash merge, delete-on-merge, auto-merge, default branch, visibility |
| protection | Branch protection rules, required reviews, status checks |
| hygiene | Stale branches, merged branch cleanup, orphan remotes |
| metadata | Title, description, topics/tags, homepage URL, license |
| ci | Workflow validation, required checks, CI/local parity |
| deps | Dependency policy (Dependabot/Renovate config, pinning, audit) |
| team | CODEOWNERS, review assignments, contributor guidelines |
| structure | Directory conventions, .gitignore completeness, config sprawl |

## State Management

Per CCO Rules: State Management. This skill uses task prefix `[RPO]`.

| Task | Created | Completed |
|------|---------|-----------|
| `[RPO] Repo audit: {scopes}` | Phase 1 complete | Phase 6 end |
| `[RPO] Audit: {N} findings` | Phase 2 complete | — (updated in-place) |
| `[RPO] Applied: {N}` | Phase 5 complete | — (updated in-place) |

**Recovery:** At Phase 1 start, run `TaskList`. If a `[RPO]` task exists with status `in_progress` → resume from last completed phase using task description as context anchor.

## Execution Flow

Setup → Audit → Gap Analysis → Plan Review → Apply → Summary

### Phase 1: Setup

**1.1 Prerequisites (parallel):**
1. Verify `git` available → not found: stop
2. Verify `gh` available → not found: stop with "gh CLI is required (https://cli.github.com)"
3. Verify `gh auth status` → not authenticated: stop with "Run `gh auth login` first"
4. Detect repo: `gh api repos/{owner}/{repo} --jq '{name, default_branch, visibility, description, topics, license: .license.spdx_id}'`

**1.2 Scope selection [SKIP if --auto or --scope]:**

```javascript
AskUserQuestion([{
  question: "Which areas should be audited?",
  header: "Scopes",
  options: [
    { label: "Settings & Protection (Recommended)", description: "Merge config, branch rules" },
    { label: "Hygiene", description: "Stale branches, merged branch cleanup" },
    { label: "CI & Dependencies", description: "Workflow validation, dependency policy" },
    { label: "Metadata & Team", description: "Description, topics, CODEOWNERS" },
    { label: "All", description: "Full repo audit" }
  ],
  multiSelect: true
}])
```

--auto default: all scopes.

### Phase 2: Audit

Run scope-specific checks via `gh api` and local inspection:

**settings:**
- `gh api repos/{owner}/{repo} --jq '{squash: .allow_squash_merge, title: .squash_merge_commit_title, msg: .squash_merge_commit_message, delete: .delete_branch_on_merge, auto_merge: .allow_auto_merge}'`
- Expected: squash=true, title=PR_TITLE, msg=PR_BODY, delete=true
- Mismatch → finding

**protection:**
- `gh api repos/{owner}/{repo}/branches/{base}/protection 2>/dev/null`
- Check: required reviews, status checks, up-to-date requirement
- No protection on default branch → HIGH finding

**hygiene:**
- Stale branches: `git for-each-ref --sort=committerdate refs/heads/ --format='%(refname:short) %(committerdate:relative)' --no-merged={base}` — cross-reference with `gh pr list --state open --json headRefName --jq '.[].headRefName'`
- Branches with no open PR and last commit >7 days ago → MEDIUM finding
- Merged branches: `git branch --merged {base}` — filter out {base}

**metadata:**
- Missing description → MEDIUM
- No topics → LOW
- No license → MEDIUM (public repo), skip (private)
- No homepage URL → LOW

**ci:**
- Glob `.github/workflows/*.yml` → no workflows = HIGH
- Check for lint/test/build jobs in workflows
- CI/local parity: compare CI commands vs local toolchain (Per CCO Rules: Toolchain Detection)

**deps:**
- Check for `.github/dependabot.yml` or `renovate.json`
- No dependency management → MEDIUM (public repo)
- Audit: `gh api repos/{owner}/{repo}/vulnerability-alerts 2>/dev/null`

**team:**
- Team size > 1: check for CODEOWNERS → missing = MEDIUM
- Public repo: check for CONTRIBUTING.md → missing = LOW

**structure:**
- .gitignore completeness: check for common patterns (node_modules, .env, build/, dist/, *.exe)
- Config sprawl: count root-level config files

### Phase 3: Gap Analysis

Display findings table: scope, severity, issue, current state, recommended state.

### Phase 4: Plan Review [SKIP if --auto]

Per CCO Rules: Plan Review Protocol.

### Phase 5: Apply [SKIP if --preview]

Apply fixes via `gh api -X PATCH` (settings), `gh api -X PUT` (protection), `git branch -d` (hygiene), Write tool (config files).

Per CCO Rules: Accounting.

### Phase 6: Summary

Per CCO Rules: Accounting, Auto Mode.

```
repo complete
=============
| Scope      | Findings | Fixed | Status |
|------------|----------|-------|--------|
| settings   |     2    |   2   |   OK   |
| protection |     1    |   0   |  WARN  |
| hygiene    |     3    |   3   |   OK   |
| Total      |     6    |   5   |  WARN  |

Applied: 5 | Failed: 0 | Needs Approval: 1 | Total: 6
```

--auto: `repo: {OK|WARN|FAIL} | Applied: N | Failed: N | Needs Approval: N | Total: N`
