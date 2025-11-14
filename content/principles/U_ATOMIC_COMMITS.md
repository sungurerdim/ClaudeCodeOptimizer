---
id: U_ATOMIC_COMMITS
title: Atomic Commits
category: universal
severity: medium
weight: 8
enforcement: SHOULD
applicability:
  project_types: ['all']
  languages: ['all']
---

# U_ATOMIC_COMMITS: Atomic Commits 🟡

**Severity**: Medium

Each commit contains changes related to a single logical change. Never mix unrelated changes.

**Enforcement**: SHOULD

**Project Types**: all
**Languages**: all

---

## Why

### The Problem
- **Mixed commits** make git bisect unusable
- **Hard to review** - "Which part broke it?"
- **Hard to revert** - Can't undo just the broken part
- **Unclear history** - "What did this commit actually do?"
- **Cherry-pick nightmare** - Can't pick just what you need

### Business Value
- **90% faster debugging** - Git bisect finds exact breaking commit
- **50% faster reverts** - Revert specific change without side effects
- **Better code review** - Reviewers understand each change clearly
- **Cleaner history** - Project evolution is traceable
- **Easier releases** - Cherry-pick features to release branches

### Technical Benefits
- **Git bisect works** - Binary search finds exact breaking commit
- **Clean reverts** - Revert atomic change without collateral damage
- **Selective cherry-pick** - Pick individual features
- **Clear blame** - `git blame` shows what change introduced line
- **Better diffs** - Each commit is focused, reviewable unit

### Industry Evidence
- **Linux Kernel** - Strict atomic commit policy
- **Git Pro Book** - "Make each commit a logically separate changeset"
- **Google Style Guide** - "One idea per CL"
- **Conventional Commits** - Enforces atomic semantic commits

---

## How

### Core Principle

**One commit = One complete, self-contained logical change**

### Definition: "Atomic" Means

1. **Complete**: Commit doesn't break build/tests
2. **Self-contained**: Commit makes sense on its own
3. **Focused**: Commit does ONE thing
4. **Revertible**: Can revert commit without breaking anything

### Implementation Patterns

#### ✅ Good: Atomic Commits
```bash
# Commit 1: Add email validation
git add forms/signup.py
git commit -m "feat: add email validation to signup form"

# Commit 2: Add password strength check (separate feature)
git add forms/signup.py tests/test_signup.py
git commit -m "feat: add password strength validation"

# Commit 3: Fix typo in error message (separate fix)
git add forms/signup.py
git commit -m "fix: correct typo in validation error message"

# Result: 3 atomic commits, each revertible independently
```

#### ❌ Bad: Mixed Commit
```bash
# ❌ BAD: One commit with 3 unrelated changes
git add forms/signup.py forms/login.py utils/validators.py
git commit -m "fix: various improvements"

# Changes in this commit:
# - Added email validation (feature)
# - Fixed login redirect bug (bug fix)
# - Refactored validator utils (refactor)
# - Fixed typo in error message (typo fix)

# Problems:
# - Can't revert just the bug fix without losing feature
# - Git bisect finds this commit but which change broke it?
# - Reviewer confused: What's the focus of this change?
```

#### ✅ Good: Logical Grouping
```bash
# Feature: Add user profile page

# Commit 1: Add profile model
git add models/profile.py
git commit -m "feat: add user profile model"

# Commit 2: Add profile API endpoints
git add api/profile.py tests/test_profile_api.py
git commit -m "feat: add profile CRUD API endpoints"

# Commit 3: Add profile UI
git add frontend/ProfilePage.tsx
git commit -m "feat: add user profile page UI"

# Each commit is atomic, but together they form a feature
# Can review each commit separately
# Can revert any commit if that layer has issues
```

---

## Anti-Patterns

### ❌ The "Mega Commit"
```bash
# ❌ BAD: End-of-day commit
git add .
git commit -m "fixed stuff and added features"

# Contains:
# M src/auth/login.py
# M src/auth/signup.py
# M src/api/users.py
# M src/api/orders.py
# A src/api/products.py
# M tests/test_auth.py
# M tests/test_api.py
# M utils/validators.py
# M config/settings.py
# D old_code/legacy.py

# 10 files, 500+ lines, 5+ unrelated changes
# Impossible to review, impossible to revert selectively
```

### ❌ The "Cleanup" Commit
```bash
# ❌ BAD: Mixing feature with cleanup
git commit -m "Add payment processing + cleanup old code"

# Changes:
# - Add payment processing logic (feature)
# - Delete unused imports (cleanup)
# - Rename variables (refactor)
# - Fix formatting (style)
# - Update dependencies (maintenance)

# Should be 5 separate commits
```

### ❌ The "WIP" Commits
```bash
# ❌ BAD: Series of meaningless commits
git commit -m "wip"
git commit -m "wip2"
git commit -m "almost working"
git commit -m "fixed it"
git commit -m "really fixed it this time"

# ✅ GOOD: Squash before pushing
git rebase -i HEAD~5  # Interactive rebase
# Squash all into one atomic commit with meaningful message
```

---

## How to Create Atomic Commits

### Technique 1: Stage Selectively
```bash
# You changed 3 files, but they're 2 separate features

# Check what changed
git status
# modified: auth/login.py (feature A + B)
# modified: auth/signup.py (feature A)
# modified: api/users.py (feature B)

# Commit feature A only
git add auth/signup.py
git add -p auth/login.py  # Interactively stage feature A changes only
git commit -m "feat: add email validation"

# Commit feature B separately
git add api/users.py
git add auth/login.py  # Rest of changes
git commit -m "feat: add user profile API"
```

### Technique 2: Partial Staging (git add -p)
```bash
# File has 2 unrelated changes

# auth/login.py:
# - Lines 10-20: Feature A (email validation)
# - Lines 50-60: Feature B (redirect fix)

# Stage only Feature A
git add -p auth/login.py
# At each hunk:
# y = stage this hunk (Feature A)
# n = don't stage (Feature B)
# s = split hunk into smaller pieces

git commit -m "feat: add email validation"

# Then stage Feature B
git add auth/login.py
git commit -m "fix: correct redirect after login"
```

### Technique 3: Amend Small Mistakes
```bash
# Made commit but forgot to add test file
git commit -m "feat: add email validation"

# Oh no, forgot the test!
git add tests/test_email_validation.py
git commit --amend  # Adds to previous commit

# Result: One atomic commit with feature + test
```

### Technique 4: Rebase to Clean History
```bash
# Before pushing, clean up commit history
git rebase -i HEAD~5

# Interactive rebase opens editor:
pick abc1234 feat: add email validation
pick def5678 wip
pick ghi9012 fix typo
pick jkl3456 wip2
pick mno7890 tests working

# Reorder and squash:
pick abc1234 feat: add email validation
squash def5678 wip
squash ghi9012 fix typo
squash jkl3456 wip2
pick mno7890 tests: add email validation tests

# Result: 2 clean atomic commits instead of 5 messy ones
```

---

## Testing Atomicity

### Test 1: Can You Revert It?
```bash
# If commit is atomic, reverting should work cleanly
git revert <commit-hash>

# ✅ GOOD: Clean revert, no conflicts
# ❌ BAD: Revert causes conflicts (commit wasn't self-contained)
```

### Test 2: Does Build Pass?
```bash
# Checkout the commit
git checkout <commit-hash>

# Run build and tests
npm run build && npm test

# ✅ GOOD: Build passes, tests pass (commit is complete)
# ❌ BAD: Build fails or tests fail (commit is incomplete)
```

### Test 3: Does Message Match Content?
```bash
# Look at commit
git show <commit-hash>

# ✅ GOOD: Message describes exactly what changed
# ❌ BAD: Message says "fix auth" but also changes API and DB
```

### Test 4: Git Bisect Works?
```bash
# Find which commit introduced bug
git bisect start
git bisect bad HEAD
git bisect good v1.0.0

# Git will check out middle commits
# At each step: Test if bug exists

# ✅ GOOD: Bisect finds exact atomic commit that broke it
# ❌ BAD: Bisect finds mega-commit, still don't know which change broke it
```

---

## Examples by Scenario

### Scenario 1: Bug Fix
```bash
# ✅ GOOD: Atomic bug fix
# 1 commit = 1 bug fix
git commit -m "fix: prevent null pointer in getUserProfile"

# File changes:
# M src/api/users.py (add null check)
# A tests/test_users_null.py (test for fix)

# Complete, self-contained, revertible
```

### Scenario 2: New Feature
```bash
# ✅ GOOD: Feature split into atomic commits

# Commit 1: Data layer
git commit -m "feat(db): add user preferences table"
# M migrations/001_add_preferences.sql
# M models/preferences.py

# Commit 2: API layer
git commit -m "feat(api): add preferences CRUD endpoints"
# M api/preferences.py
# A tests/test_preferences_api.py

# Commit 3: UI layer
git commit -m "feat(ui): add preferences settings page"
# A frontend/PreferencesPage.tsx
# A frontend/PreferencesForm.tsx

# Each commit is atomic, together they're a feature
```

### Scenario 3: Refactoring
```bash
# ✅ GOOD: Refactor split into logical steps

# Commit 1: Extract function (no behavior change)
git commit -m "refactor: extract email validation to helper"

# Commit 2: Rename for clarity (no behavior change)
git commit -m "refactor: rename validateUser to validateUserInput"

# Commit 3: Add tests for refactored code
git commit -m "test: add tests for validation helpers"

# Each step atomic, verifiable, revertible
```

---

## Special Cases

### Multiple Files, One Logical Change
```bash
# ✅ OK: Multiple files for one logical change
git add models/user.py api/users.py tests/test_users.py
git commit -m "feat: add user email verification"

# All files relate to same feature (email verification)
# Removing any file would break the feature
# This is atomic because it's ONE logical change
```

### Cascading Renames
```bash
# ✅ OK: Rename function + update all call sites
git add src/**/*.py  # 15 files changed
git commit -m "refactor: rename getUserById to fetchUser"

# All changes are part of one logical operation (rename)
# Can't partially commit (would break code)
# This is atomic
```

---

## Implementation Checklist

- [ ] **One logical change per commit**
- [ ] **Build passes at each commit**
- [ ] **Tests pass at each commit**
- [ ] **Commit message describes change accurately**
- [ ] **Can revert commit cleanly**
- [ ] **No "WIP" or "fix" commits in history before pushing**
- [ ] **Used git rebase -i to clean history before pushing**

---

## Cross-References

**Related Principles:**
- **U_CONCISE_COMMITS** - Clear commit messages for atomic commits
- **U_MINIMAL_TOUCH** - Fewer files = easier atomic commits
- **U_TEST_FIRST** - Tests make commits atomic (feature + test together)
- **U_EVIDENCE_BASED** - Each commit should be verifiable

---

## Industry Standards Alignment

- **Linux Kernel** - Strict one change per patch policy
- **Git Pro Book** - "Make each commit a logically separate changeset"
- **Conventional Commits** - Semantic versioning with atomic commits
- **Google Style Guide** - One idea per change list
- **Trunk-Based Development** - Small, atomic commits to trunk

---

## Summary

**Atomic Commits** means each commit contains ONE complete, self-contained logical change. Never mix unrelated changes in a single commit.

**Core Rule**: One commit = one thing. If you can't describe the commit in one sentence, split it.

**Remember**: "A commit should tell a story. One story. Not an anthology."

**Impact**: 90% faster debugging (git bisect), 50% faster reverts, clearer history.
