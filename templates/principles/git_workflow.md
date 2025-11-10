# Git Workflow
**Commit conventions, branching, PR guidelines, versioning**

**Total Principles:** 8

---

## P043: Commit Message Conventions

**Severity:** MEDIUM

Use Conventional Commits: feat/fix/docs/refactor/test.

### Examples

**✅ Good:**
```
git commit -m 'fix(api): handle null user_id in /jobs endpoint'
```

**❌ Bad:**
```
git commit -m 'fixed stuff'
```

**Why:** Validates user workflows through end-to-end tests of complete system flows

---

## P044: Branching Strategy

**Severity:** MEDIUM

Git Flow for releases, Trunk-Based for CI/CD.

### Examples

**✅ Good:**
```
# Feature branches -> main (with CI/CD)
```

**❌ Bad:**
```
# Everyone commits to main
```

**Why:** Improves test quality by verifying tests actually catch bugs through mutation testing

---

## P045: PR Guidelines

**Severity:** MEDIUM

PR template with description, tests, breaking changes checklist.

### Examples

**✅ Good:**
```
# .github/pull_request_template.md with checklist
```

**❌ Bad:**
```
# No PR template, inconsistent reviews
```

**Why:** Maintains consistency through conventional commit messages and automated changelog

---

## P046: Rebase vs Merge Strategy

**Severity:** LOW

Rebase feature branches, merge to main (clean history).

### Examples

**✅ Good:**
```
git rebase main  # Clean feature branch
git merge --no-ff feature  # To main
```

**❌ Bad:**
```
# Merge commits everywhere, messy history
```

**Why:** Documents changes clearly through structured PR descriptions and review comments

---

## P047: Semantic Versioning

**Severity:** MEDIUM

SemVer: MAJOR.MINOR.PATCH for breaking/features/fixes.

### Examples

**✅ Good:**
```
# v2.0.0 (breaking), v1.5.0 (feature), v1.4.1 (fix)
```

**❌ Bad:**
```
# Random version numbers
```

**Why:** Communicates change impact through semantic versioning of breaking changes and features

---

## P072: Concise Commit Messages

**Severity:** MEDIUM

Commit messages must be compact: max 10 lines total, max 5 bullets in body, no verbosity. Focus on essential changes only.

### Examples

**✅ Good:**
```
refactor(ci): consolidate tools (P071)

- Replace Black/Bandit/mypy with Ruff (format+lint+security)
- Remove tool configs from pyproject.toml
- Simplify workflow to 3 jobs, 5 steps total

Co-Authored-By: Claude <noreply@anthropic.com>
```

**❌ Bad:**
```
refactor: eliminate tool redundancy

Tool Consolidation (3 tools instead of 5):
- Replace Black + mypy + Bandit with Ruff
- Keep pip-audit (CVE scanning)
...

Dependency Changes (pyproject.toml):
- Remove: black, mypy from dev dependencies
...
[15 more lines]
```

**Why:** Concise commits are faster to read, easier to scan in history, and reduce noise

---

## P073: Atomic Commits

**Severity:** MEDIUM

Each commit must contain changes related to a single logical change or category. Never mix unrelated changes in one commit.

### Examples

**✅ Good:**
```
# Commit 1: Bug fix only
git commit -m "fix(auth): handle expired tokens in login"
# Modified: auth.py
```
```
# Commit 2: Tests only
git commit -m "test(auth): add tests for token expiration"
# Modified: tests/test_auth.py
```
```
# Single commit for tightly coupled changes
git commit -m "fix(auth): handle null user in session middleware"
# Modified: auth.py, middleware.py, tests/test_auth.py
# (All changes address the same logical issue)
```

**❌ Bad:**
```
git commit -m "fix login bug, add tests, update README, refactor database"
# Modified: auth.py, tests/, README.md, db.py (4 unrelated changes)
```
```
# Mix refactor with new feature
git commit -m "refactor db and add caching"
```

**Why:** Atomic commits make git bisect, revert, and code review easier and more effective

---

## P074: Automated Semantic Versioning

**Severity:** MEDIUM

Automatically bump version based on conventional commit type following Semantic Versioning (SemVer). Version bumps are determined by commit message prefix: feat: → MINOR, fix: → PATCH, feat!/BREAKING CHANGE: → MAJOR.

### Examples

**✅ Good:**
```
# Solo dev - automatic
git commit -m "feat(api): add user registration"
→ Version auto-bumps: 1.2.0 → 1.3.0
→ pyproject.toml updated
→ Git tag v1.3.0 created
```
```
# Small team - PR-based
PR: feat(auth): add JWT refresh tokens
→ Reviewer confirms MINOR bump
→ On merge: version bumps 1.2.0 → 1.3.0
→ CHANGELOG.md updated from PR description
```
```
# Large org - manual
Release manager reviews sprint commits
→ Manually bumps version for release
→ Creates release branch
→ Merges to main with tag
```

**❌ Bad:**
```
# Inconsistent versioning
1.2.0 → 1.2.5 (random jump)
1.2.5 → 1.4.0 (skipped 1.3.x)
1.4.0 → 2.0.0 (no BREAKING CHANGE marker)
```
```
# Wrong bump type
feat(api): add field → 1.2.0 → 1.2.1 (should be MINOR)
fix(bug): patch → 1.2.0 → 1.3.0 (should be PATCH)
```

**Why:** Eliminates manual versioning errors and ensures consistent version history aligned with actual changes

---
