---
title: Git Workflow Guide
category: version-control
tags: [git, team, collaboration, branching]
description: Git commit, branching, and PR guidelines for teams
use_cases:
  team_dynamics: [small-2-5, medium-10-20, large-20-50]
  git_workflow: [git_flow, github_flow, gitlab_flow]
---

# Git Workflow Guide

**Load on-demand when:** Git operations, commit tasks, version control

---

## Branch Strategies

### Main-Only (Solo Developer)

**Solo**: Work directly on `main`, keep working state, rollback via history

### GitHub Flow (Small Teams)

- `main` (production) → Feature branch → PR → Merge
- Hotfix branches: `hotfix/<issue>`

### Git Flow (Large Teams)

- `main` (releases) → `develop` (integration) → Feature branches
- Release: `release/<version>`
- Hotfix: `hotfix/<issue>`

---

## Commit Strategy

### Format (Compact)


```
type(scope): concise description (max 72 chars)

- Key change 1 with brief context
- Key change 2
- Key change 3
- Impact/benefit if significant
```

Rules: Max 10 lines, max 5 bullets, no headers or emojis

### Types

```
feat:     New feature
fix:      Bug fix
docs:     Documentation only
refactor: Code improvement (no behavior change)
test:     Add/update tests
chore:    Build, deps, config
style:    Formatting, linting (no logic change)
perf:     Performance improvement
```

### Scopes (Example)

```
api, auth, db, ui, core, cli, tests, docs, deps, ci
```

### Examples

**✅ Good - Compact & Informative**:
```bash
refactor(ci): consolidate tools to prevent overlap (U_NO_OVERENGINEERING)

- Replace Black/Bandit/mypy with Ruff (format+lint+security)
- Remove tool configs from pyproject.toml
- Simplify workflow to 3 jobs, 5 steps total
- Format 25 files with ruff
```

**✅ Good - Simple Fix**:
```bash
fix(ci): use cyclonedx-py environment mode

- Change from requirements to environment mode
- Fixes "requirements.txt not found" error
```

**✅ Good - Feature**:
```bash
feat(docs): restructure documentation system

- Create content/ structure with progressive disclosure
- Split principles by category (code, security, testing, etc.)
- Reduce CLAUDE.md from 5000 to 1500 tokens
```

**❌ Bad - Too Verbose**:
```bash
refactor: eliminate tool redundancy

Tool Consolidation (3 tools instead of 5):
- Replace Black + mypy + Bandit with Ruff (all-in-one)
- Keep pip-audit (CVE scanning)
...

Dependency Changes (pyproject.toml):
- Remove: black, mypy from dev dependencies
...
[15 more lines]
```

**❌ Bad - Too Vague**:
```bash
feat: updates and fixes
```

### Commit Rules

- Group related changes, one logical unit per commit
- Include related tests + docs
- No WIP, no failing tests, no mixed topics

---

## Push Strategy

Push after each task completion with clear commit messages.

**Rules**: No failing tests, syntax errors, or incomplete features

---

## Versioning

Format: `MAJOR.MINOR.PATCH-prerelease`

- **MINOR**: Milestones
- **MAJOR**: Breaking changes/architecture changes
- **PATCH**: Bug fixes between milestones

Tag at milestones with release notes. Major version bump requires API stability guarantee and migration guide.

---

## Daily Workflow Example

```bash
# Morning: Start on TODO task
# ... work on P0.1 Task 1 (Export/import removal) ...

# Midday: Task 1 complete
git add claudecodeoptimizer/commands/config.md \
        claudecodeoptimizer/ai/command_selection.py
git commit -m "feat(commands): remove export/import functionality

- Remove export/import from config.md
- Remove export/import rules from command_selection.py
- Update command descriptions
- Tests pass

Closes #P0.1-Task1"

git push origin main

# Afternoon: Task 2 complete
git add claudecodeoptimizer/wizard/orchestrator.py \
        claudecodeoptimizer/core/installer.py \
        tests/unit/test_installer.py
git commit -m "fix(wizard): install only recommended commands

- Filter commands to core + recommended only
- Update installer to accept command list
- Add tests for command filtering
- Verify ~/.claude/commands/ contains only 8-12 commands

Closes #P0.1-Task2"

git push origin main
```

---

## Commit Quality Checklist

**Before committing**:
- Tests pass
- Code formatted and linted
- No security vulnerabilities or exposed secrets
- Commit message follows format
- Related docs updated

Run checks:
```bash
git status && git diff --cached
ruff format --check . && ruff check .
pip-audit --desc
pytest tests/ -v
```

---

## Rollback Strategies

- Undo unpushed: `git reset --soft HEAD~1` (keep changes) or `--hard` (discard)
- Undo pushed: `git revert <commit-hash>` then push
- Rollback to task: Each task = 1 commit for easy identification

## Best Practices

- Commit per task, group related changes, push after each task
- Tag at milestones, keep main working, write clear messages
- No WIP code, failing tests, or batch commits
