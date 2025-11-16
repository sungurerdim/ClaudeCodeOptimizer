---
id: C_NO_UNSOLICITED_TESTS
title: No Unsolicited Tests or Linters
category: claude-guidelines
severity: high
weight: 8
applicability:
  project_types: ['all']
  languages: ['all']
---

# C_NO_UNSOLICITED_TESTS: No Unsolicited Tests or Linters 🔴

**Severity**: High

Never run tests, linters, formatters, or repository scans unless explicitly requested by the user. Respect user's workflow, time, and development process. Only run these tools when user explicitly asks or when part of documented workflow.

**Enforcement**: MUST

**Project Types**: all
**Languages**: all

---

## Why

### The Problem

**Unsolicited tests and linters disrupt user workflow:**

- **Workflow Disruption** - Running tests interrupts user's train of thought and immediate next action
- **Time Waste** - Tests may take minutes; user didn't budget time for test runs
- **Resource Consumption** - Linters/tests consume CPU, memory, and potentially API quotas
- **Unwanted Noise** - Test failures or lint warnings clutter output when user didn't ask
- **False Urgency** - Failing tests create pressure to fix immediately when user may have planned differently
- **Configuration Conflicts** - User may have specific test/lint configurations not yet run

### Core Techniques

**1. Never Run Tests Unless Explicitly Requested**

```python
# After making code changes:

# ❌ BAD: Running tests without asking
Write("src/auth.py", new_code)
Bash("pytest tests/", description="Run tests")  # Unsolicited!
# Output: ❌ 3 tests failed

# ✅ GOOD: Complete work, offer to run tests
Write("src/auth.py", new_code)
"""
Changes complete. The authentication module has been updated.

Would you like me to run the tests?
"""
```

**2. Never Run Linters Proactively**

```python
# After implementing feature:

# ❌ BAD: Running linter without request
Write("src/service.py", implementation)
Bash("ruff check src/", description="Run Ruff linter")  # Unsolicited!
# Output: 15 lint warnings

# ✅ GOOD: Implement, then offer to lint
Write("src/service.py", implementation)
"""
Implementation complete.

Would you like me to run Ruff to check for linting issues?
"""
```

**3. Never Run Formatters Without Permission**

```bash
# ❌ BAD: Auto-formatting without asking
Bash("black src/", description="Format code with Black")  # Modifies files!

# ✅ GOOD: Ask first
"""
Code changes complete.

Would you like me to format the code with Black?
"""
```

**4. Offer Testing as Option, Don't Execute**

```python
# After bug fix:

# ❌ BAD: Immediately verify with tests
Edit("src/calculator.py", ...)
Bash("pytest tests/test_calculator.py", description="Verify fix")  # Unsolicited

# ✅ GOOD: Offer verification
Edit("src/calculator.py", ...)
"""
Bug fix applied to calculator.py:67.

Would you like me to:
1. Run the calculator tests to verify the fix?
2. Run all tests?
3. Nothing - you'll test manually
"""
```

**5. When Tests ARE Requested**

```python
# User: "Fix the login bug and verify with tests"

# ✅ GOOD: Explicit request includes testing
Edit("src/auth.py", ...)
Bash("pytest tests/test_auth.py -v", description="Run auth tests to verify fix")

# Explicit "verify" or "test" means run tests
```

---

### Implementation Patterns

#### ✅ Good: Offer Testing, Don't Execute

```python
# Task: Fix authentication timeout bug

# Fix the bug
Edit("src/auth.py",
     old_string="timeout=30",
     new_string="timeout=60")

# ✅ GOOD: Offer to test
"""
Timeout bug fixed: Increased auth timeout from 30s to 60s (auth.py:145).

Would you like me to run the authentication tests to verify?
"""

# Wait for user approval before running tests
```

---

#### ✅ Good: User Explicitly Requests Testing

```python
# User: "Add email validation and run the tests"

# Implement feature
Edit("src/validators.py", ...)

# Run tests (explicitly requested!)
Bash("pytest tests/test_validators.py -v",
     description="Run validator tests")

# ✅ RESULT: Tests run because user explicitly requested
```

---

#### ✅ Good: Documented Workflow Includes Testing

```python
# User has documented workflow:
# "After implementing features, always run: pytest && ruff check"

# Implement feature
Write("src/feature.py", implementation)

# Follow documented workflow
Bash("pytest && ruff check",
     description="Run tests and linting per project workflow")

# ✅ RESULT: Part of established workflow, not unsolicited
```

---

#### ❌ Bad: Proactive Test Execution

```python
# ❌ BAD: Running tests without request
Edit("src/payment.py", payment_fix)
Bash("pytest tests/test_payment.py",
     description="Verify payment fix")  # Unsolicited!

# Output:
# ===== test session starts =====
# tests/test_payment.py ....F                            [100%]
# ===== 1 failed, 4 passed =====

# Problems:
# - User didn't ask for tests
# - Test failure creates pressure
# - May have wanted to test later
```

---

#### ❌ Bad: Automatic Linting

```python
# ❌ BAD: Proactive linting
Write("src/api.py", new_endpoints)
Bash("ruff check src/api.py",
     description="Check code quality")  # Unsolicited!

# Output:
# src/api.py:15:1: E501 Line too long (127 > 120 characters)
# src/api.py:23:1: F401 'typing.List' imported but unused
# Found 2 errors.

# Problems:
# - User didn't request linting
# - Creates unnecessary noise
# - May have different lint config in mind
```

---

#### ❌ Bad: Automatic Formatting

```bash
# ❌ BAD: Formatting without permission
Bash("black src/ && isort src/",
     description="Format and sort imports")  # Modifies files!

# Problems:
# - Changes files without permission
# - May conflict with user's format preferences
# - User loses control over when formatting happens
```

---

## Anti-Patterns

### ❌ Anti-Pattern 1: "Helpful" Test Execution

**Problem**: Running tests to be "helpful" without user request.

```python
# ❌ BAD: Proactive testing
Edit("src/models.py", database_fix)
Bash("pytest tests/", description="Verify changes")  # Unsolicited
# → 45 tests run, 3 failed
# → Noise and distraction

# ✅ GOOD: Offer testing
Edit("src/models.py", database_fix)
"Database fix applied. Would you like me to run the tests?"
```

**Impact:**
- Interrupts user workflow
- Creates false urgency (failing tests)
- Wastes time if user planned to test later

---

### ❌ Anti-Pattern 2: Automatic Code Quality Checks

**Problem**: Running linters/formatters after every change.

```python
# ❌ BAD: Auto-lint after changes
Edit("src/utils.py", new_function)
Bash("ruff check src/utils.py", description="Check quality")
Bash("mypy src/utils.py", description="Type check")
Bash("black src/utils.py --check", description="Format check")
# Three unsolicited checks!

# ✅ GOOD: Complete work, offer checks
Edit("src/utils.py", new_function)
"New function added. Would you like me to run quality checks (ruff, mypy, black)?"
```

**Impact:**
- Output cluttered with lint warnings
- Multiple tool runs slow response
- User may have planned to batch lint later

---

### ❌ Anti-Pattern 3: Assuming Test-Driven Workflow

**Problem**: Assuming user follows TDD without confirmation.

```python
# ❌ BAD: Assuming TDD workflow
# User: "Add login feature"

# Write test first (assuming TDD)
Write("tests/test_login.py", test_code)
Bash("pytest tests/test_login.py", description="Run failing test")
# Then implement feature
Write("src/login.py", implementation)
Bash("pytest tests/test_login.py", description="Verify passing test")

# Problems:
# - User may not follow TDD
# - Two unsolicited test runs
# - User didn't request test-first approach

# ✅ GOOD: Implement as requested, offer testing
Write("src/login.py", implementation)
"Login feature complete. Would you like me to add tests?"
```

**Impact:**
- Imposes workflow user didn't request
- Extra test runs waste time
- May not align with team practices

---

## Implementation Checklist

### Before Running ANY Tests

- [ ] **Explicit user request?** - Did user say "run tests" or "verify"?
- [ ] **Part of documented workflow?** - Is testing part of established process?
- [ ] **User asked for verification?** - Did user request confirmation changes work?
- [ ] **If not requested** - Offer to run tests, don't execute

### Before Running Linters/Formatters

- [ ] **User explicitly requested?** - Did user ask for lint/format?
- [ ] **Pre-commit hook?** - Is this part of automated pre-commit process?
- [ ] **CI/CD simulation?** - User asked to simulate CI checks?
- [ ] **If not requested** - Don't run, or ask first

### What to Offer (Not Execute)

- [ ] **Test execution** - "Would you like me to run tests?"
- [ ] **Linting** - "Would you like me to check for lint issues?"
- [ ] **Formatting** - "Would you like me to format the code?"
- [ ] **Type checking** - "Would you like me to run type checks?"
- [ ] **Security scans** - "Would you like me to scan for security issues?"

### When Execution IS Justified

- [ ] **Explicit command** - User says "run pytest" or "lint the code"
- [ ] **Documented workflow** - Project docs specify automatic testing
- [ ] **Verification requested** - User asks to "verify" or "validate" changes
- [ ] **CI/CD simulation** - User requests "run what CI would run"

---

## Summary

**No Unsolicited Tests or Linters** means never running tests, linters, formatters, or scans unless user explicitly requests them. Always offer, never assume. Respect user's workflow control and timing preferences.

**Core Rules:**

- **Never run tests unsolicited** - Wait for explicit "run tests" request
- **Never run linters proactively** - Offer to lint, don't execute
- **Never auto-format** - Formatting modifies files; requires permission
- **Offer, don't execute** - "Would you like me to run tests?" not running tests
- **Respect documented workflows** - Follow established project testing processes
