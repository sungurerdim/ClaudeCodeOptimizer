---
id: U_CONCISE_COMMITS
title: Concise Commit Messages
category: universal
severity: medium
weight: 7
enforcement: SHOULD
applicability:
  project_types: ['all']
  languages: ['all']
---

# U_CONCISE_COMMITS: Concise Commit Messages 🟡

**Severity**: Medium

Write clear, focused commit messages. Subject line explains WHAT changed. Body explains WHY.

**Enforcement**: SHOULD

**Project Types**: all
**Languages**: all

---

## Why

### The Problem
- **Vague messages** - "fixed stuff", "updates", "wip"
- **Can't understand history** - What did this commit actually do?
- **Hard code archaeology** - Why was this change made?
- **Wasted review time** - Reviewers spend time figuring out intent
- **Lost knowledge** - Future developers can't understand decisions

### Business Value
- **80% faster code review** - Clear intent = faster approval
- **50% faster onboarding** - New developers understand history
- **Better debugging** - `git blame` reveals WHY code exists
- **Preserved context** - Decisions documented in commit messages
- **Easier audits** - Compliance requirements met through clear history

### Technical Benefits
- **Self-documenting code** - Commit messages explain changes
- **Better `git log`** - Scanning history actually useful
- **Effective `git blame`** - Understand why line was added
- **Changelog generation** - Auto-generate from commit messages
- **Release notes** - Commits describe features/fixes

### Industry Evidence
- **Conventional Commits** - Standard format for semantic versioning
- **Linux Kernel** - Strict 50/72 format enforced
- **Angular Commit Guidelines** - Used by thousands of projects
- **Semantic Release** - Automates versioning from commit messages

---

## How

### Format: Subject + Body

```
<type>(<scope>): <subject>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```

### Subject Line Rules

1. **50 characters max** (hard limit: 72)
2. **Start with type**: feat/fix/docs/refactor/test/chore
3. **Use imperative mood**: "add" not "added" or "adds"
4. **No period at end**
5. **Describe WHAT changed**

### Body Rules (Optional but Recommended)

1. **72 characters per line**
2. **Explain WHY, not WHAT** (code shows what)
3. **Describe problem being solved**
4. **Mention side effects or trade-offs**
5. **Link to issues/tickets**

---

## Implementation Patterns

#### ✅ Good: Clear and Concise
```bash
feat(auth): add email verification on signup

Users can now verify their email address during signup.
Sends verification code via email, user enters code to activate
account. Prevents fake accounts.

Closes #123
```

#### ❌ Bad: Vague
```bash
updates
```

#### ✅ Good: Fix with Context
```bash
fix(api): prevent null pointer in getUserProfile

getUserProfile() crashed when user had no profile data.
Added null check before accessing profile.photo_url.

Fixes production issue reported by users, affecting ~5% of users.

Fixes #456
```

#### ❌ Bad: No Context
```bash
fixed bug
```

---

## Conventional Commits Types

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
refactor: rename getUserById to fetchUser for consistency
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

### perf: Performance improvement
```bash
perf(db): add index on user_id for faster queries
perf(api): cache user profile data (reduces latency 70%)
perf: optimize image compression algorithm
```

### style: Code style/formatting
```bash
style: apply Prettier formatting to codebase
style(lint): fix ESLint warnings in auth module
style: consistent spacing in function declarations
```

---

## Anti-Patterns

### ❌ Too Vague
```bash
# ❌ BAD
fix
update
changes
wip
stuff
asdf
```

### ❌ Too Technical (Missing WHY)
```bash
# ❌ BAD
fix: change if (x == null) to if (x === null)

# ✅ GOOD
fix(auth): use strict equality to prevent type coercion

Loose equality (==) allowed undefined to equal null, causing
authentication to pass for undefined users. Strict equality (===)
fixes this security issue.
```

### ❌ Essay
```bash
# ❌ BAD (too long)
feat: add user authentication with JWT tokens and also refactored the
entire user service to use dependency injection and cleaned up some
old code and fixed a bug in the login function and updated tests and
also improved error handling

# ✅ GOOD (focused, one thing)
feat(auth): add JWT token authentication

Implements stateless authentication using JWT tokens.
Tokens expire after 24 hours. Refresh token support added.

Replaces session-based auth (session management was scaling issue).
```

### ❌ Past Tense
```bash
# ❌ BAD (past tense)
feat: added email validation
fix: fixed null pointer bug

# ✅ GOOD (imperative mood)
feat: add email validation
fix: prevent null pointer in getUserProfile
```

---

## Templates

### Feature Addition
```bash
feat(<scope>): <what you added>

<why it's needed>
<how it works (brief)>
<any trade-offs or limitations>

Closes #<issue-number>
```

### Bug Fix
```bash
fix(<scope>): <what you fixed>

<what the bug was>
<how you fixed it>
<why this approach>

Fixes #<issue-number>
```

### Breaking Change
```bash
feat!(<scope>): <what changed>

BREAKING CHANGE: <what breaks>
<how to migrate>
<why this change was necessary>

Closes #<issue-number>
```

---

## Tools

### Git Commit Template
```bash
# ~/.gitmessage
<type>(<scope>): <subject>

# Why is this change needed?
#

# How does it address the issue?
#

# What side effects does it have?
#

# Closes #

# Type: feat|fix|docs|refactor|test|chore|perf|style
# Scope: auth|api|ui|db|etc
# Subject: imperative mood, 50 chars
# Body: 72 chars per line
```

Set as default:
```bash
git config --global commit.template ~/.gitmessage
```

### Commitizen (Interactive CLI)
```bash
npm install -g commitizen cz-conventional-changelog

# Use with: git cz instead of git commit
# Prompts for type, scope, subject, body
```

### Commitlint (Enforce Format)
```bash
npm install --save-dev @commitlint/{cli,config-conventional}

# .commitlintrc.json
{
  "extends": ["@commitlint/config-conventional"],
  "rules": {
    "subject-case": [2, "never", ["upper-case"]],
    "subject-max-length": [2, "always", 50]
  }
}
```

---

## Implementation Checklist

- [ ] **Type prefix** (feat/fix/docs/etc)
- [ ] **Subject ≤ 50 chars** (hard limit: 72)
- [ ] **Imperative mood** ("add" not "added")
- [ ] **No period at end**
- [ ] **Body wraps at 72 chars** (if present)
- [ ] **Body explains WHY** (not what - code shows what)
- [ ] **References issue/ticket** (Closes #123)
- [ ] **Atomic** (one logical change, see U_ATOMIC_COMMITS)

---

## Cross-References

**Related Principles:**
- **U_ATOMIC_COMMITS** - Concise messages require atomic commits
- **U_MINIMAL_TOUCH** - Smaller changes = easier to describe
- **U_EVIDENCE_BASED** - Commit message claims should match reality

---

## Industry Standards Alignment

- **Conventional Commits** - Standardized semantic format
- **Semantic Versioning** - Commit types drive version bumps
- **Angular Commit Guidelines** - Industry-standard format
- **Linux Kernel** - 50/72 rule enforced
- **Git Best Practices** - Imperative mood, clear subjects

---

## Summary

**Concise Commit Messages** means clear, focused messages that explain WHAT changed (subject) and WHY (body). Follow Conventional Commits format for consistency.

**Core Rule**: Subject = WHAT (50 chars). Body = WHY (72 chars/line). Imperative mood.

**Remember**: "Future you will thank present you for clear commit messages."

**Impact**: 80% faster code review, 50% faster onboarding, preserved project knowledge.
