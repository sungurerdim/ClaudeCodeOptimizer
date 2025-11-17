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

Mixed commits break git bisect, vague messages waste reviewer time, and hard-to-revert commits create maintenance nightmares. Atomic commits with clear messages enable clean reverts, efficient debugging, and knowledge preservation.

---

## Core Principles

### 1. Atomic Commits

**One commit = One complete, self-contained logical change**

**"Atomic" means:**
1. **Complete** - Build and tests pass
2. **Self-contained** - Makes sense on its own
3. **Focused** - Does ONE thing
4. **Revertible** - Can revert without breaking anything

### 2. Clear Messages

**Format:**
```
<type>(<scope>): <subject>
<BLANK LINE>
<body>
```

**Subject Line Rules:**
1. ≤50 characters (hard limit: 72)
2. Start with type: feat/fix/docs/refactor/test/chore
3. Imperative mood: "add" not "added"
4. No period at end

**Body Rules:**
1. 72 characters per line
2. Explain WHY, not WHAT (code shows what)
3. Link to issues/tickets

---

## Implementation Patterns

### ✅ Good: Atomic Commits

```bash
# Commit 1: One feature
git add forms/signup.py tests/test_signup.py
git commit -m "feat(auth): add email validation to signup form

Validates format using RFC 5322 regex. Prevents typos
and invalid accounts.

Closes #123"

# Commit 2: Separate fix
git add forms/login.py
git commit -m "fix(auth): correct redirect after login

Stores return_url in session before login.
Redirects to previous page after authentication.

Fixes #456"
```

### ❌ Bad: Mixed Commit

```bash
# ❌ One commit with 3 unrelated changes
git add forms/signup.py forms/login.py utils/validators.py
git commit -m "fix: various improvements"

# Problems:
# - Can't revert just bug fix without losing feature
# - Git bisect can't identify which change broke it
# - Message doesn't explain WHAT or WHY
```

---

## Commit Types (Conventional Commits)

```bash
feat(payment): add PayPal integration          # New feature
fix(auth): prevent session timeout             # Bug fix
docs(readme): add installation instructions    # Documentation
refactor(db): extract query logic              # Code change, no behavior change
test(auth): add password reset tests           # Add/fix tests
chore(deps): upgrade axios to 1.5.0            # Maintenance
```

---

## How to Create Atomic Commits

### Technique 1: Stage Selectively

```bash
# Changed 3 files, 2 separate features
git status
# modified: auth/login.py (feature A + B)
# modified: auth/signup.py (feature A)
# modified: api/users.py (feature B)

# Commit feature A only
git add auth/signup.py
git add -p auth/login.py  # Interactively stage feature A changes
git commit -m "feat(auth): add email validation"

# Commit feature B separately
git add api/users.py auth/login.py
git commit -m "feat(api): add user profile endpoint"
```

### Technique 2: Partial Staging (git add -p)

```bash
# File has 2 unrelated changes
git add -p auth/login.py
# y = stage this hunk
# n = don't stage
# s = split hunk into smaller pieces

git commit -m "feat(auth): add email validation

Validates email format on login form.
Prevents login with invalid email addresses."

# Then stage remaining changes
git add auth/login.py
git commit -m "fix(auth): correct redirect after login"
```

---

## Anti-Patterns

### ❌ The "Mega Commit"

```bash
# ❌ End-of-day commit dump
git add .
git commit -m "fixed stuff and added features"
# 10 files, 500+ lines, 5+ unrelated changes
# Impossible to review or revert selectively
```

### ❌ WIP Commits (Squash Before Push)

```bash
# ❌ Series of meaningless commits
git commit -m "wip"
git commit -m "wip2"
git commit -m "almost working"

# ✅ Squash before pushing
git rebase -i HEAD~5  # Interactive rebase
# Squash all into one atomic commit with meaningful message
```

---

## Special Cases

### Multiple Files, One Logical Change (OK)

```bash
# ✅ OK: All files relate to same feature
git add models/user.py api/users.py tests/test_users.py
git commit -m "feat(user): add email verification

Sends verification code via email.
User enters code to activate account.

Closes #789"
# Removing any file would break the feature = atomic
```

### Cascading Renames (OK)

```bash
# ✅ OK: Rename function + all call sites
git add src/**/*.py  # 15 files
git commit -m "refactor: rename getUserById to fetchUser

Updated all 47 call sites for consistency."
# Can't partially commit (would break code) = atomic
```

---

## Implementation Checklist

### Before Committing
- [ ] One logical change per commit
- [ ] Build and tests pass
- [ ] Message follows format: `<type>(<scope>): <subject>`
- [ ] Subject ≤ 50 chars, imperative mood
- [ ] Body explains WHY with issue reference

### Before Pushing
- [ ] Clean history (squash WIP commits)
- [ ] Each commit builds and passes tests
- [ ] Can revert each commit cleanly

---

## Summary

**Core Rules:**
- **One commit = one thing** - If you can't describe it in one sentence, split it
- **Subject = WHAT (≤50 chars)** - Clear, imperative mood, no period
- **Body = WHY (72 chars/line)** - Explain problem, solution, trade-offs
- **Conventional Commits** - `<type>(<scope>): <subject>`
- **Complete and revertible** - Build passes, clean revert
- **Clean history** - Squash WIP before pushing
