# U_MINIMAL_TOUCH: Minimal Touch Policy

**Severity**: High

Edit only required files. No "drive-by improvements", no scope creep.

---

## Why

- Scope creep accumulates unpredictable changes
- More changes = more bugs, harder reviews
- Merge conflicts from unrelated files
- Can't revert targeted fix

**Core Principle**: Touch ONLY files REQUIRED for task.

---

## Decision Framework

Before editing:
1. **Is this file REQUIRED?** (not "nice to have")
2. **Does task mention this?** (not implicit)
3. **Will task fail without this?** (not "could be better")

If NO to any: **Don't touch.**

---

## Examples

### ✅ Good - Surgical
```python
# Task: "Fix login bug - session not set"
def login(username, password):
    user = authenticate(username, password)
    if user:
        session['user_id'] = user.id  # FIX
        return True
# One file, one line
```

### ❌ Bad - Scope Creep
```python
# Task: "Fix login bug"
def login(username, password):
    user = authenticate(username, password)
    if user:
        session['user_id'] = user.id  # FIX
        session['last_login'] = datetime.now()  # "While I'm here..."
        send_login_notification(user)  # "Might as well..."
# Also refactored 2 other unrelated files
```

---

## Legitimate Exceptions

### ✅ Cascading Changes (Required)
```python
# Rename requires updating all callers
-def getUserById(user_id):
+def fetchUser(user_id):
# All callers MUST update or breaks
```

### ✅ Same Root Cause
```python
# Fix broken date parser used in 3 places
# utils/date_parser.py + all usage sites
```

### ✅ Test Coverage for Fix
```python
# Fix + test verifying fix
def process_payment(amount):
    if amount is None:
        raise ValueError("Amount cannot be None")

def test_process_payment_rejects_none():
    with pytest.raises(ValueError):
        process_payment(None)
```

---

## Checklist

- [ ] Read task - what EXACTLY required?
- [ ] List required files
- [ ] Stop at required files
- [ ] Document exceptions
- [ ] Separate nice-to-haves into issues
- [ ] Review diff - verify every file required
