---
id: U_MINIMAL_TOUCH
title: Minimal Touch Policy
category: universal
severity: high
weight: 8
enforcement: SHOULD
applicability:
  project_types: ['all']
  languages: ['all']
---

# U_MINIMAL_TOUCH: Minimal Touch Policy 🔴

**Severity**: High

Edit only required files. No "drive-by improvements", no scope creep.

**Enforcement**: SHOULD

**Project Types**: all
**Languages**: all

---

## Why

### The Problem
- **Scope creep** - "While I'm here" changes accumulate
- **Unpredictable changes** - Hard to review, hard to test
- **Increased risk** - More changes = more chances for bugs
- **Merge conflicts** - Touching unrelated files creates conflicts
- **Harder rollback** - Can't revert targeted fix without reverting extras

### Core Principle

**Only touch files REQUIRED for the task. Everything else is out of scope.**

### Decision Framework

Before editing a file, ask:
1. **Is this file REQUIRED for the current task?** (not "nice to have")
2. **Does the task explicitly mention this change?** (not implicit)
3. **Will the task fail without this change?** (not "could be better")

If answer is NO to any: **Don't touch the file.**

### Implementation Patterns

#### ✅ Good: Surgical Changes
```python
# Task: "Fix login bug - session not set"

# File 1: auth/login.py (REQUIRED - bug is here)
def login(username, password):
    user = authenticate(username, password)
    if user:
        session['user_id'] = user.id  # FIX: Add this line
        return True
    return False

# That's it. One file, one line added. Done.
```

#### ❌ Bad: Scope Creep
```python
# Task: "Fix login bug - session not set"

# File 1: auth/login.py (REQUIRED)
def login(username, password):
    user = authenticate(username, password)
    if user:
        session['user_id'] = user.id  # FIX
        session['last_login'] = datetime.now()  # "While I'm here..."
        send_login_notification(user)  # "Might as well add this..."
        return True
    return False

# File 2: auth/models.py (NOT REQUIRED)
class User:
    # "Let me rename this while I'm here"
    def getName(self):  # Was: get_name()
        return self.name

# File 3: auth/validators.py (NOT REQUIRED)
# "Let me refactor this function I noticed"
def validate_password(password):
    # 50 lines of refactoring nobody asked for

# File 4: tests/test_auth.py (NOT REQUIRED for the bug fix)
# "Let me improve test coverage while I'm here"
def test_edge_case_nobody_reported():
    # New test for hypothetical issue

# Result: Bug fix + 4 unrelated changes = risky PR
```

#### ✅ Good: One Thing at a Time
```python
# PR 1: Fix login bug (1 file, 1 line)
# auth/login.py
session['user_id'] = user.id  # FIX

# PR 2: Add login notification (separate PR, reviewed separately)
# auth/login.py + notification/service.py
send_login_notification(user)

# PR 3: Refactor password validator (separate PR, reviewed separately)
# auth/validators.py
def validate_password(password):
    # Refactored logic

# Result: 3 small, focused PRs - easier to review, test, and rollback
```

---

## Anti-Patterns

### ❌ Drive-By Refactoring
```python
# Task: "Fix null pointer bug in getUserProfile()"

# ❌ BAD: Also refactored unrelated code
def getUserProfile(user_id):
    user = db.get_user(user_id)
    if user is None:
        raise UserNotFoundError(user_id)  # FIX: Added null check
    return user.profile

# "While I'm here, let me refactor this unrelated function"
def getUsers():
    # Was working fine, but I changed it anyway
    return [User.from_dict(row) for row in db.query_all()]  # Changed from loop to comprehension

# ✅ GOOD: Only fix the bug
def getUserProfile(user_id):
    user = db.get_user(user_id)
    if user is None:
        raise UserNotFoundError(user_id)  # FIX: Added null check
    return user.profile

# Leave getUsers() alone - it's not broken, not part of task
```

### ❌ Formatting Spree
```diff
# Task: "Fix typo in error message"

# ❌ BAD: Also reformatted entire file
diff --git a/api/errors.py b/api/errors.py
- def handle_error(error):
-     if error.code == 404:
-         return {"message": "Not Found"}
+ def handle_error(error):
+     if error.code == 404:
+         return {"message": "Not found"}  # FIX: Lowercased "found"
+     elif error.code == 500:
+         return {"message": "Internal Server Error"}
+     elif error.code == 403:
+         return {"message": "Forbidden"}
# ... +200 lines of whitespace/formatting changes

# ✅ GOOD: Only fix the typo
diff --git a/api/errors.py b/api/errors.py
-         return {"message": "Not Found"}
+         return {"message": "Not found"}  # FIX: Lowercased "found"
```

### ❌ Dependency Upgrade During Bug Fix
```python
# Task: "Fix JSON parsing bug"

# ❌ BAD: Also upgraded dependencies
# requirements.txt
-requests==2.28.0
+requests==2.31.0  # "Let me upgrade while I'm here"
-pydantic==1.10.0
+pydantic==2.5.0  # "This looks old"

# api/parser.py
import json
def parse_response(data):
    try:
        return json.loads(data)  # FIX: Added try/except
    except json.JSONDecodeError as e:
        raise ParseError(str(e))

# Result: Bug fix + dependency upgrades = risky (Pydantic 2.0 breaks everything!)

# ✅ GOOD: Separate PRs
# PR 1: Fix JSON parsing (1 file changed)
# PR 2: Upgrade dependencies (separate PR with full testing)
```

### ❌ "I Noticed This While Here"
```python
# Task: "Add email validation to signup form"

# ❌ BAD: Also fixed unrelated issues
# forms/signup.py
def validate_signup(form_data):
    if not is_valid_email(form_data['email']):  # FIX: Added
        raise ValidationError("Invalid email")

    # "I noticed password validation is weak, let me fix that too"
    if len(form_data['password']) < 12:  # NOT PART OF TASK
        raise ValidationError("Password too short")

    # "And this function name is bad, let me rename it"
    # (renamed process_user to handle_user_registration across 15 files)

# ✅ GOOD: Only email validation
def validate_signup(form_data):
    if not is_valid_email(form_data['email']):  # FIX
        raise ValidationError("Invalid email")

# Save password and naming improvements for separate PRs
```

---

## Legitimate Exceptions

**When to touch additional files:**

### ✅ Exception 1: Cascading Changes (Required)
```python
# Task: "Rename function getUserById to fetchUser"

# File 1: models/user.py (REQUIRED)
-def getUserById(user_id):
+def fetchUser(user_id):
    return db.query(User).get(user_id)

# File 2-10: All callers of getUserById (REQUIRED)
# Must update all call sites or code breaks
-user = getUserById(123)
+user = fetchUser(123)

# Legitimate: Function rename requires updating all callers
```

### ✅ Exception 2: Fixing Related Bug (Same Root Cause)
```python
# Task: "Fix date parsing bug in registration"

# File 1: utils/date_parser.py (REQUIRED - root cause)
def parse_date(date_string):
    # Fix the broken date parser
    return datetime.strptime(date_string, "%Y-%m-%d")

# File 2: forms/registration.py (REQUIRED - uses broken parser)
# File 3: forms/profile_update.py (REQUIRED - uses same broken parser)
# Both use the broken parser, both need testing

# Legitimate: Same bug, same root cause, fix together
```

### ✅ Exception 3: Test Coverage for Fix
```python
# Task: "Fix null pointer in process_payment"

# File 1: payment/processor.py (REQUIRED)
def process_payment(amount):
    if amount is None:
        raise ValueError("Amount cannot be None")  # FIX
    # ... process payment

# File 2: tests/test_payment.py (REQUIRED)
def test_process_payment_rejects_none():
    with pytest.raises(ValueError):
        process_payment(None)  # Test for the fix

# Legitimate: Test verifies the fix works
```

### ❌ NOT Exception: "Nearby Code"
```python
# Task: "Fix bug in login()"

# ❌ NOT LEGITIMATE: "It's in the same file"
def login(username, password):
    # ... fix the bug
    pass

def logout():  # Same file, but NOT REQUIRED for task
    # "Let me refactor this while I'm here"
    # NO! Logout is not part of login bug fix
    pass
```

---

## Implementation Checklist

- [ ] **Read task description carefully** - What EXACTLY is required?
- [ ] **List required files** - Which files MUST change for task to complete?
- [ ] **Stop at required files** - Resist urge to "improve while here"
- [ ] **Document exceptions** - If touching extra files, explain WHY in PR description
- [ ] **Separate nice-to-haves** - Create separate issues for improvements noticed
- [ ] **Review diff** - Before submitting, verify every changed file is required

---

## Code Review Questions

**For reviewers to ask:**
1. Is every changed file required for this task?
2. Are there drive-by improvements that should be separate PRs?
3. Does the scope match the task description?
4. Can any changes be deferred to future PRs?

**For authors to ask themselves:**
1. Did I touch any files not mentioned in task?
2. Did I refactor code unrelated to task?
3. Did I add features not requested?
4. Can I split this into smaller PRs?

---

## Metrics and Monitoring

### Key Indicators
- **Files changed per PR** - Lower is better (aim for <5)
- **Lines changed per PR** - Lower is better (aim for <400)
- **Review time** - Small PRs reviewed faster (measure)
- **Scope creep rate** - % of changes unrelated to task (aim for 0%)

### Success Criteria
- PRs have <5 files changed (80%+ of PRs)
- PRs reviewed within 24 hours (due to small size)
- Scope matches task description (100%)
- Zero rollbacks due to unrelated changes

---

## Summary

**Minimal Touch Policy** means editing ONLY files required for the current task. No drive-by improvements, no scope creep, no "while I'm here" changes.

**Core Rule**: If the file isn't required to complete the task, don't touch it.
