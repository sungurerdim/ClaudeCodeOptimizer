---
id: U_COMMIT_QUALITY
title: Commit Quality
category: universal
severity: medium
weight: 8
enforcement: SHOULD
applicability:
  project_types: ['all']
  languages: ['all']
---

# U_COMMIT_QUALITY: Commit Quality 🟡

**Severity**: Medium

Each commit contains ONE complete, self-contained logical change with a clear, focused message. Subject line explains WHAT changed (≤50 chars, imperative mood). Body explains WHY (72 chars/line).

**Enforcement**: SHOULD

**Project Types**: all
**Languages**: all

---

## Why

### The Problem
- **Mixed commits** make git bisect unusable - can't identify which change broke it
- **Vague messages** - "fixed stuff", "updates", "wip" provide zero information
- **Hard to review** - Unclear what changed and why
- **Hard to revert** - Can't undo just the broken part when changes are mixed
- **Lost knowledge** - Future developers can't understand decisions

---

## Core Principles

### 1. Atomic Commits

**One commit = One complete, self-contained logical change**

**"Atomic" means:**
1. **Complete** - Commit doesn't break build/tests
2. **Self-contained** - Commit makes sense on its own
3. **Focused** - Commit does ONE thing
4. **Revertible** - Can revert commit without breaking anything

### 2. Clear Messages

**Format:**
```
<type>(<scope>): <subject>
<BLANK LINE>
<body>
```

**Subject Line Rules:**
1. **≤50 characters** (hard limit: 72)
2. **Start with type**: feat/fix/docs/refactor/test/chore
3. **Imperative mood**: "add" not "added" or "adds"
4. **No period at end**
5. **Describe WHAT changed**

**Body Rules:**
1. **72 characters per line**
2. **Explain WHY, not WHAT** (code shows what)
3. **Describe problem being solved**
4. **Mention trade-offs or side effects**
5. **Link to issues/tickets**

---

## Implementation Patterns

### ✅ Good: Atomic Commits with Clear Messages

```bash
# Commit 1: Add email validation (one feature)
git add forms/signup.py tests/test_signup.py
git commit -m "feat(auth): add email validation to signup form

Users can now only signup with valid email addresses.
Validates format using RFC 5322 regex. Prevents typos
and invalid accounts.

Closes #123"

# Commit 2: Fix login redirect (separate fix)
git add forms/login.py
git commit -m "fix(auth): correct redirect after login

Login was redirecting to /home instead of previous page.
Now stores return_url in session and redirects correctly.

Fixes #456"

# Result: 2 atomic commits, each clear and revertible
```

### ❌ Bad: Mixed Commit with Vague Message

```bash
# ❌ BAD: One commit with 3 unrelated changes
git add forms/signup.py forms/login.py utils/validators.py
git commit -m "fix: various improvements"

# Changes in this commit:
# - Added email validation (feature)
# - Fixed login redirect bug (bug fix)
# - Refactored validator utils (refactor)

# Problems:
# - Can't revert just the bug fix without losing feature
# - Git bisect finds this commit but which change broke it?
# - Reviewer confused: What's the focus of this change?
# - Message doesn't explain WHAT or WHY
```

---

## Commit Types (Conventional Commits)

### feat: New feature
```bash
feat(payment): add PayPal integration
feat(ui): add dark mode toggle
feat: support CSV export
```

### fix: Bug fix
```bash
fix(auth): prevent session timeout during file upload
fix(api): return 404 for missing users instead of 500
fix: correct timezone handling in date picker
```

### docs: Documentation only
```bash
docs(readme): add installation instructions
docs(api): update authentication examples
docs: fix broken links in contributing guide
```

### refactor: Code change (no behavior change)
```bash
refactor(db): extract query logic to repository layer
refactor: rename getUserById to fetchUser
refactor(api): simplify error handling logic
```

### test: Add/fix tests
```bash
test(auth): add tests for password reset flow
test: increase coverage for payment processing
test(api): fix flaky integration test
```

### chore: Maintenance tasks
```bash
chore(deps): upgrade axios to 1.5.0
chore: update .gitignore for IDE files
chore(ci): add Node 20 to test matrix
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
git commit -m "feat(auth): add email validation"

# Commit feature B separately
git add api/users.py auth/login.py
git commit -m "feat(api): add user profile endpoint"
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

git commit -m "feat(auth): add email validation

Validates email format on login form.
Prevents login with invalid email addresses."

# Then stage Feature B
git add auth/login.py
git commit -m "fix(auth): correct redirect after login

Stores return URL in session before login.
Redirects to previous page after successful authentication."
```

### Technique 3: Amend Small Mistakes

```bash
# Made commit but forgot to add test file
git commit -m "feat(auth): add email validation"

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
pick abc1234 feat(auth): add email validation
pick def5678 wip
pick ghi9012 fix typo
pick jkl3456 wip2
pick mno7890 tests working

# Reorder and squash:
pick abc1234 feat(auth): add email validation
squash def5678 wip
squash ghi9012 fix typo
squash jkl3456 wip2
pick mno7890 test(auth): add email validation tests

# Result: 2 clean atomic commits instead of 5 messy ones
```

---

## Anti-Patterns

### ❌ The "Mega Commit"

```bash
# ❌ BAD: End-of-day commit
git add .
git commit -m "fixed stuff and added features"

# Contains:
# 10 files, 500+ lines, 5+ unrelated changes
# Impossible to review, impossible to revert selectively
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

### ❌ Vague/Essay Messages

```bash
# ❌ BAD: Too vague
git commit -m "updates"

# ❌ BAD: Too long
git commit -m "feat: add user authentication with JWT tokens and also \
refactored the entire user service to use dependency injection and \
cleaned up some old code and fixed a bug in the login function"

# ✅ GOOD: Clear and focused
git commit -m "feat(auth): add JWT token authentication

Implements stateless authentication using JWT tokens.
Tokens expire after 24 hours. Refresh token support added.

Replaces session-based auth (session management was scaling issue)."
```

---

## Testing Commit Quality

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

# ✅ GOOD: Bisect finds exact atomic commit that broke it
# ❌ BAD: Bisect finds mega-commit, still don't know which change broke it
```

---

## Special Cases

### Multiple Files, One Logical Change (OK)

```bash
# ✅ OK: Multiple files for one logical change
git add models/user.py api/users.py tests/test_users.py
git commit -m "feat(user): add email verification

Adds email verification to user signup flow.
Sends verification code via email. User enters code to activate account.

Closes #789"

# All files relate to same feature (email verification)
# Removing any file would break the feature
# This is atomic because it's ONE logical change
```

### Cascading Renames (OK)

```bash
# ✅ OK: Rename function + update all call sites
git add src/**/*.py  # 15 files changed
git commit -m "refactor: rename getUserById to fetchUser

Renames for consistency with other fetch* methods.
Updated all 47 call sites across codebase."

# All changes are part of one logical operation (rename)
# Can't partially commit (would break code)
# This is atomic
```

---

## Implementation Checklist

### Before Committing
- [ ] **One logical change per commit** - Not mixing features/fixes/refactors
- [ ] **Build passes** - Run build/tests before committing
- [ ] **Tests pass** - All tests green
- [ ] **Message follows format** - <type>(<scope>): <subject>
- [ ] **Subject ≤ 50 chars** - Concise and clear
- [ ] **Imperative mood** - "add" not "added"
- [ ] **Body explains WHY** - Not just what (code shows what)
- [ ] **References issue** - Closes #123 or Fixes #456

### Before Pushing
- [ ] **Clean history** - Use git rebase -i to squash WIP commits
- [ ] **No "fix typo" commits** - Amend or squash
- [ ] **Each commit builds** - Verify with git rebase -i --exec "npm test"
- [ ] **Can revert cleanly** - Test git revert on each commit

---

## Summary

**Commit Quality** means atomic commits (one complete, focused change) with clear messages (subject explains WHAT in ≤50 chars, body explains WHY).

**Core Rules:**
- **One commit = one thing** - If you can't describe it in one sentence, split it
- **Subject = WHAT (≤50 chars)** - Clear, imperative mood, no period
- **Body = WHY (72 chars/line)** - Explain problem, solution, trade-offs
- **Conventional Commits format** - <type>(<scope>): <subject>
- **Complete and revertible** - Build passes, can revert cleanly
- **Clean history** - Squash WIP commits before pushing
