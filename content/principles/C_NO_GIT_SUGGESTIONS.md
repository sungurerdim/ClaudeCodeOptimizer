---
id: C_NO_GIT_SUGGESTIONS
title: No Git Commit Suggestions
category: claude-guidelines
severity: medium
weight: 5
applicability:
  project_types: ['all']
  languages: ['all']
---

# C_NO_GIT_SUGGESTIONS: No Git Commit Suggestions 🟡

**Severity**: Medium

Never suggest git commands (add, commit, push) or commit messages unless explicitly requested by the user. User manages their own git workflow and timing. Only provide git-related assistance when user explicitly asks or when part of documented workflow (e.g., `/commit` command).

**Enforcement**: SHOULD

**Project Types**: all
**Languages**: all

---

## Why

### The Problem

**Unsolicited git suggestions disrupt user's workflow control:**

- **Workflow Disruption** - User may have specific git workflow (feature branches, squash commits, etc.)
- **Timing Control Loss** - User decides when to commit, not AI
- **Team Process Conflicts** - Team may have commit message conventions or PR processes
- **Premature Commits** - User may want to batch multiple changes before committing
- **Branch Strategy Ignorance** - AI doesn't know if user is on feature branch, main, or experimental branch

### Business Value

- **Respects user autonomy** - User maintains full control over git workflow
- **Team alignment** - Doesn't conflict with team's git practices
- **Flexibility** - User can commit when ready, not when AI suggests
- **Prevents errors** - Avoids premature commits or wrong branch commits

### Technical Benefits

- **User-controlled timing** - Commits happen when user has verified changes
- **Proper commit atomicity** - User groups changes logically, not arbitrarily
- **Branch management** - User commits to correct branch at correct time
- **Workflow alignment** - Respects project's specific git workflow

### Industry Evidence

- **Developer Surveys** - 90% of developers have specific git workflow preferences
- **Team Practices** - Git workflows vary: GitFlow, GitHub Flow, trunk-based, etc.
- **Commit Convention Tools** - Teams use Conventional Commits, signed commits, etc.
- **Code Review** - Commit timing often tied to PR creation and review readiness

---

## How

### Core Techniques

**1. Never Suggest Git Commands**

```python
# After making code changes:

# ❌ BAD: Suggest git commands
"""
Changes complete!

Next steps:
git add .
git commit -m "fix: authentication bug"
git push origin feature/auth-fix
"""

# ✅ GOOD: Report changes, let user handle git
"""
Changes complete!

Modified files:
- src/auth.py (fixed authentication timeout bug)
- tests/test_auth.py (added test for timeout scenario)
"""
```

**2. Never Create Commit Messages Unless Requested**

```python
# User: "Fix the login bug"

# ❌ BAD: Proactively create commit message
Edit("auth.py", ...)
"""
Bug fixed!

Suggested commit message:
git commit -m "fix: resolve login timeout issue"
"""

# ✅ GOOD: Fix bug, report completion
Edit("auth.py", ...)
"""
Login timeout bug fixed (auth.py:127).

The timeout has been increased from 30s to 60s.
"""
```

**3. When Git Commands ARE Requested**

```python
# User: "Fix the bug and commit the changes"
# OR
# User: "/commit" (documented slash command)

# ✅ GOOD: Explicit request, provide git assistance
Edit("auth.py", ...)
Bash("git add src/auth.py tests/test_auth.py")
Bash("git commit -m 'fix: increase login timeout to 60s'")
```

**4. Never Suggest `git push`**

```bash
# ❌ BAD: Suggest pushing
"""
Changes committed!

Run: git push origin main
"""

# ✅ GOOD: Report commit, don't suggest push
"""
Changes committed locally.

Commit: a4f3c2b - fix: increase login timeout
"""
```

**5. When PR Creation is Requested**

```python
# User: "Create a pull request for this feature"

# ✅ GOOD: Explicit PR request includes git operations
Bash("git push origin feature/new-auth")
Bash("gh pr create --title 'Add OAuth support' --body 'Implements OAuth...'")
```

---

### Implementation Patterns

#### ✅ Good: Report Changes, No Git Suggestions

```python
# After implementing feature:

"""
Feature implementation complete!

Files modified:
- src/payment_processor.py (added Stripe integration)
- src/config.py (added STRIPE_API_KEY setting)
- tests/test_payment.py (added Stripe integration tests)

All tests passing locally.
"""

# Let user decide when/how to commit
```

---

#### ✅ Good: User Explicitly Requests Commit

```python
# User: "Fix the bug and create a commit"

# Fix the bug
Edit("calculator.py",
     old_string="return a / b",
     new_string="return a / b if b != 0 else 0")

# Create commit (explicitly requested)
Bash("git add calculator.py")
Bash("git commit -m 'fix: prevent division by zero in calculator'")

"""
Bug fixed and committed.

Commit: b7e9d2a - fix: prevent division by zero in calculator
"""
```

---

#### ✅ Good: Documented Workflow (Slash Command)

```python
# User has /commit slash command documented

# User: "/commit"

# Read git status and diff
Bash("git status")
Bash("git diff")

# Draft commit message based on changes
commit_msg = analyze_changes_and_create_message()

# Execute commit
Bash(f"git add .")
Bash(f"git commit -m '{commit_msg}'")
```

---

#### ❌ Bad: Unsolicited Git Workflow Suggestions

```python
# ❌ BAD: Suggesting entire git workflow
"""
Changes complete!

Suggested workflow:
1. git checkout -b feature/user-profiles
2. git add .
3. git commit -m "feat: add user profile pages"
4. git push origin feature/user-profiles
5. Create PR on GitHub
"""

# ✅ GOOD: Just report what was done
"""
Changes complete!

Added user profile pages:
- src/profile.py (profile model and routes)
- templates/profile.html (profile view)
- tests/test_profile.py (profile tests)
"""
```

---

#### ❌ Bad: Suggesting Commit Messages

```python
# ❌ BAD: Unsolicited commit message
"""
Feature implementation complete!

Suggested commit:
git commit -m "feat(auth): add OAuth2 support with Google provider

- Implemented OAuth2 flow
- Added Google provider integration
- Updated configuration
"
"""

# ✅ GOOD: Report implementation details
"""
OAuth2 implementation complete!

Implementation details:
- OAuth2 flow in src/auth/oauth.py
- Google provider in src/auth/providers/google.py
- Configuration updates in src/config.py
- Tests in tests/test_oauth.py
"""
```

---

## Anti-Patterns

### ❌ Anti-Pattern 1: "Helpful" Git Suggestions

**Problem**: Suggesting git commands to be "helpful."

```python
# ❌ BAD: Helpful but unsolicited
"""
All done!

Don't forget to:
git add .
git commit -m "your message"
"""

# ✅ GOOD: Report completion only
"""
Implementation complete!

Modified: 3 files
Added: 2 new files
Tests: All passing
"""
```

**Impact:**
- User may have different commit strategy
- Might commit to wrong branch
- Interrupts user's planned workflow

---

### ❌ Anti-Pattern 2: Assuming Branch Strategy

**Problem**: Suggesting branch operations without knowing strategy.

```bash
# ❌ BAD: Assuming feature branch workflow
"""
Ready to merge!

git checkout main
git merge feature/new-auth
git push origin main
"""

# ✅ GOOD: Report status, let user handle merging
"""
Feature complete and all tests passing.

Branch: feature/new-auth
Files changed: 8
Tests added: 12
"""
```

**Impact:**
- Team may use different branching strategy
- May be trunk-based development (no feature branches)
- Could push to protected branch

---

### ❌ Anti-Pattern 3: Premature Commit Suggestions

**Problem**: Suggesting commits before user is ready.

```python
# User: "Add email validation"

Edit("validators.py", ...)

# ❌ BAD: Immediately suggest commit
"""
Email validation added!

git commit -m "add email validation"
"""

# ✅ GOOD: Report completion, user decides when to commit
"""
Email validation added to validators.py:45.

Function: validate_email(email: str) -> bool
Raises ValueError on invalid format.
"""
```

**Impact:**
- User may want to add tests first
- May want to batch with other changes
- May want different commit message format

---

## Implementation Checklist

### Never Do (Unless Explicitly Requested)

- [ ] ❌ **Suggest `git add`** - User controls staging
- [ ] ❌ **Suggest `git commit`** - User controls commit timing
- [ ] ❌ **Suggest `git push`** - User controls push timing
- [ ] ❌ **Create commit messages** - User writes messages (unless requested)
- [ ] ❌ **Suggest branch operations** - User manages branches

### Always Do

- [ ] ✅ **Report changes** - List modified/added files clearly
- [ ] ✅ **Describe changes** - Explain what was changed and why
- [ ] ✅ **Mention tests** - Report test status if relevant
- [ ] ✅ **Wait for requests** - Let user ask for git assistance

### When Git IS Requested

- [ ] ✅ **User says "commit"** - Provide commit assistance
- [ ] ✅ **Slash commands** - Follow documented `/commit`, `/pr` commands
- [ ] ✅ **PR creation** - Push and create PR when explicitly requested
- [ ] ✅ **Commit message help** - Draft message when user asks

---

## Cross-References

**Related Principles:**

- **C_NO_UNSOLICITED_TESTS** - Similar "ask first" philosophy
- **C_NO_PROACTIVE_DOCS** - Don't create artifacts without request
- **U_ATOMIC_COMMITS** - When user DOES commit, make commits atomic
- **U_CONCISE_COMMITS** - When user requests commit messages, make them concise

**Workflow Integration:**
- After changes: Report what was done, don't suggest commits
- If user has `/commit` slash command: Follow that workflow
- For PR creation: Only when explicitly requested
- Never assume user's git workflow or branch strategy

---

## Summary

**No Git Commit Suggestions** means never suggesting git commands (add, commit, push) or commit messages unless user explicitly requests them. Report changes clearly, let user control git workflow timing and execution.

**Core Rules:**

- **Never suggest `git add/commit/push`** - User controls git workflow
- **Never create commit messages** - Unless explicitly requested
- **Report changes clearly** - List files and describe modifications
- **Respect user autonomy** - User decides when to commit, not AI
- **When requested** - Provide full git assistance when user explicitly asks

**Remember**: "Report changes. Let user git. Only assist with git when explicitly requested."

**Impact**: Respects user workflow control, prevents premature commits, aligns with team practices, maintains user autonomy.

---

**Valid Git Requests:**
- ✅ "Commit these changes"
- ✅ "Create a commit with message X"
- ✅ "/commit" (documented slash command)
- ✅ "Push and create PR"
- ✅ "Help me write a commit message"

**NOT Valid (Report, Don't Suggest):**
- ❌ User doesn't mention git
- ❌ "I'll probably commit later" (thinking, not requesting)
- ❌ Silence after implementation (report changes, no git)

---

**Completion Report Template:**
```
[Feature/Fix] complete!

Modified files:
- path/to/file1.py ([description])
- path/to/file2.py ([description])

Added files:
- path/to/new_file.py ([description])

Test status: [All passing / Added X tests / etc.]

[Any additional relevant information]
```

**Don't add:**
- ❌ "git add ..."
- ❌ "git commit ..."
- ❌ "Suggested commit message: ..."
- ❌ "Next steps: push to remote..."
