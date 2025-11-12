# Git Workflow Guide

**Load on-demand when:** Git operations, commit tasks, version control

---

## Overview

This guide covers the complete Git workflow for CCO projects. Workflow strategy varies by team size (configured during `/cco-init`).

---

## Branch Strategies

### Main-Only (Solo Developer)

**Simple is better**:
- ✅ Work directly on `main` branch
- ✅ Always keep it in working state
- ✅ No feature branches (solo dev = no need)
- ✅ Rollback via commit history if needed

**Rationale**: P071 (Anti-Overengineering) - Branch complexity unnecessary for solo projects

### GitHub Flow (Small Teams)

- `main` - Production-ready code
- Feature branches: `feature/<name>`
- Hotfix branches: `hotfix/<issue>`

**Process**:
1. Create feature branch from main
2. Make commits with clear messages
3. Open PR when ready
4. Code review required
5. Merge to main after approval
6. Delete feature branch

### Git Flow (Large Teams/Production)

- `main` - Production releases only
- `develop` - Integration branch
- Feature branches: `feature/<name>` (from develop)
- Release branches: `release/<version>` (from develop)
- Hotfix branches: `hotfix/<issue>` (from main)

---

## Commit Strategy

### Format (Compact)

**P072: Concise Commit Messages** - Essential info only, no verbosity

```
type(scope): concise description (max 72 chars)

- Key change 1 with brief context
- Key change 2
- Key change 3
- Impact/benefit if significant
```

**Rules**:
- ✅ Max 10 lines total
- ✅ Max 5 bullets (most important changes)
- ✅ One line per bullet
- ✅ Co-Authored-By footer (GitHub contributor attribution)
- ❌ No section headers ("Changes:", "Rationale:")
- ❌ No emojis or decorative elements

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

### Scopes (CCO-specific)

```
wizard, installer, detection, principles, commands,
skills, core, cli, tests, docs, deps, ci
```

### Examples

**✅ Good - Compact & Informative**:
```bash
refactor(ci): consolidate tools to prevent overlap (P071)

- Replace Black/Bandit/mypy with Ruff (format+lint+security)
- Remove tool configs from pyproject.toml
- Simplify workflow to 3 jobs, 5 steps total
- Format 25 files with ruff

Co-Authored-By: Claude <noreply@anthropic.com>
```

**✅ Good - Simple Fix**:
```bash
fix(ci): use cyclonedx-py environment mode

- Change from requirements to environment mode
- Fixes "requirements.txt not found" error

Co-Authored-By: Claude <noreply@anthropic.com>
```

**✅ Good - Feature**:
```bash
feat(docs): restructure documentation system

- Create content/ structure with progressive disclosure
- Split principles by category (code, security, testing, etc.)
- Reduce CLAUDE.md from 5000 to 1500 tokens

Co-Authored-By: Claude <noreply@anthropic.com>
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

- ✅ Group related changes in same category
- ✅ One logical unit per commit
- ✅ Include related tests + docs
- ❌ Don't mix different topics/categories
- ❌ No WIP commits
- ❌ No failing tests

---

## Push Strategy

### Task-Based Pushing

```bash
# After each TODO task completes
git add .
git commit -m "feat(docs): create content/ structure"
git push origin main

# After grouped changes
git commit -m "refactor(principles): split by category"
git push origin main
```

**Benefits**:
- 📊 Every change tracked
- ⏮️ Easy rollback per task
- 📝 Clear history
- 🔄 Safe incremental progress

**Never push**:
- ❌ Failing tests
- ❌ Syntax errors
- ❌ Incomplete features

---

## Versioning

### Format

`MAJOR.MINOR.PATCH-prerelease`

### Rules

- **MINOR** bump: Every milestone (P0, v0.2.0, v0.3.0, etc.)
- **MAJOR** bump: Breaking changes or significant architecture changes
- **PATCH** bump: Bug fixes between milestones

### Example Roadmap

```
v0.1.0-alpha  ✅ Initial release
v0.2.0-alpha  ⏳ P0 + Production readiness
v0.3.0-beta      UX improvements
v0.4.0-rc        Extensibility
v1.0.0           Stable release (MAJOR bump)
```

### When to Tag

```bash
# After milestone complete
git tag -a v0.2.0-alpha -m "Production Readiness Milestone

Completed:
- P0: wshobson/agents integration
- 60% test coverage
- CI/CD pipeline operational
- Zero critical bugs

See CHANGELOG.md for details"

git push origin v0.2.0-alpha
```

### Major Version Triggers

**0.x → 1.x**:
- ✅ API stability guarantee
- ✅ Production-ready quality
- ✅ Breaking changes minimized
- ✅ Migration guide provided

**1.x → 2.x**:
- ✅ Fundamental architecture change
- ✅ Breaking API changes
- ✅ Plugin system overhaul
- ✅ Must provide upgrade path

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

# End of day: Update TODO
git add TODO.md
git commit -m "docs(todo): mark P0.1 tasks 1-2 as complete"
git push origin main
```

---

## Commit Quality Checklist

**Before committing**:
- [ ] All files in commit are related (same category/topic)
- [ ] Tests pass (`pytest tests/ -v`)
- [ ] Code formatted (`ruff format --check .`)
- [ ] Linter clean (`ruff check .`)
- [ ] No security vulnerabilities (`pip-audit --desc`)
- [ ] No exposed secrets (`/cco-scan-secrets` or `python -m claudecodeoptimizer scan-secrets`)
- [ ] No debug code or commented blocks
- [ ] Commit message follows format
- [ ] Related docs updated

**Verification** (Run all checks):
```bash
# 1. Check what's staged
git status
git diff --cached

# 2. Format check
ruff format --check .

# 3. Linting
ruff check .

# 4. Security: Dependencies
pip-audit --desc

# 5. Security: Secrets
python -m claudecodeoptimizer scan-secrets

# 6. Tests
pytest tests/ -v

# 7. Commit only if ALL pass
git commit -m "type(scope): message"
```

**Quick pre-commit script** (optional):
```bash
# Save as scripts/pre-commit-check.sh
#!/bin/bash
set -e

echo "🔍 Running pre-commit checks..."

echo "✓ Format check..."
ruff format --check .

echo "✓ Linting..."
ruff check .

echo "✓ Security: Dependencies..."
pip-audit --desc

echo "✓ Security: Secrets..."
python -m claudecodeoptimizer scan-secrets

echo "✓ Tests..."
pytest tests/ -v

echo "✅ All checks passed! Ready to commit."
```

**Usage**:
```bash
# Run all checks
bash scripts/pre-commit-check.sh

# If all pass, commit
git commit -m "type(scope): message"
```

---

## Rollback Strategies

### Undo Last Commit (Not Pushed)

```bash
git reset --soft HEAD~1  # Keep changes
git reset --hard HEAD~1  # Discard changes
```

### Undo Pushed Commit

```bash
# Find commit to revert
git log --oneline

# Revert specific commit
git revert <commit-hash>
git push origin main
```

### Rollback to Specific Task

```bash
# Each task = 1 commit, easy to identify
git log --grep="P0.1-Task1"
git checkout <commit-hash>
```

---

## Best Practices Summary

**DO**:
- ✅ Commit per TODO task
- ✅ Group related changes
- ✅ Push after each task
- ✅ Tag at milestones
- ✅ Keep main working
- ✅ Write clear messages

**DON'T**:
- ❌ Mix unrelated changes
- ❌ Commit WIP code
- ❌ Push failing tests
- ❌ Create unnecessary branches (solo)
- ❌ Batch multiple tasks
- ❌ Skip commit messages

---

## Principle References

- **P071**: Anti-Overengineering (Branch strategy)
- **P067**: Evidence-Based Verification (Commit verification)

See: [@~/.cco/principles/git-workflow.md](../principles/git-workflow.md)

---

*Part of CCO Documentation System*
*Load when needed: @~/.cco/guides/git-workflow.md*
