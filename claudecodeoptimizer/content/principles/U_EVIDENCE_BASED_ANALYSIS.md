# U_EVIDENCE_BASED_ANALYSIS: Evidence-Based Analysis

**Severity**: Critical

Never claim completion without command execution proof. Trace to root cause using 5 Whys. Fix at source, not symptom.

---

## Why

Assumption-based development causes 60%+ production bugs. Symptom fixing creates whack-a-mole debugging. Band-aids accumulate technical debt.

---

## Core Principles

### 1. Evidence-Based Verification

Every claim needs:
1. Command execution output
2. Exit codes (0 = success)
3. Timestamps (prove freshness)
4. Error messages (when applicable)

### 2. Root Cause Analysis (5 Whys)

Ask "Why?" five times:

```
Problem: API returning 500 errors
Why #1: Database queries timing out
Why #2: Lock wait timeout exceeded
Why #3: Batch update holds locks 30+ seconds
Why #4: Updates 100,000 rows in single transaction
Why #5: Developer thought single transaction faster
ROOT CAUSE: Batch process design flaw
FIX: Chunk updates (1000 rows each)
```

---

## Workflow

### 1. Reproduce and Trace Backwards
```python
def test_reproduces_bug():
    result = process_data(malformed_input)
    assert result.error is not None
```

### 2. Verify Root Cause
```python
def test_root_cause_hypothesis():
    session['user_id'] = 123
    result = load_user_data()
    assert result is not None  # PASSES
```

### 3. Fix at Root
```python
# ❌ BAD: Fix symptom
def load_user_data():
    user_id = session.get('user_id')
    if user_id is None:
        return DEFAULT_DATA  # Band-aid!

# ✅ GOOD: Fix root cause
def login(username, password):
    user = authenticate(username, password)
    if user:
        session['user_id'] = user.id  # FIX
        return True
```

### 4. Verify with Evidence
```bash
$ pytest tests/test_auth.py::test_user_login -v
tests/test_auth.py::test_user_login PASSED [100%]
$ echo $?
0
```

---

## Anti-Patterns

### ❌ Band-Aid Fix
```python
# ❌ Hiding issue
try:
    return price * (discount_percentage / 100)
except TypeError:
    return price  # Band-aid!

# ✅ Fix input validation
def calculate_discount(price: float, discount_percentage: float) -> float:
    if not isinstance(price, (int, float)) or price < 0:
        raise ValueError(f"Invalid price: {price}")
    return price * (1 - discount_percentage / 100)
```

### ❌ Assumption-Based Claims
```plaintext
# ❌ "Fixed authentication bug." [NO proof]

# ✅ "Fixed authentication bug.
$ pytest tests/test_auth.py -v
tests/test_auth.py::test_login PASSED
$ echo $?
0
Root cause: Session not set (login.py:<line>)
Fix: Added session['user_id'] = user.id"
```

---

## Checklist

- [ ] Run command before claiming completion
- [ ] Capture output with timestamps
- [ ] Check exit code
- [ ] Ask "Why?" 5 times minimum
- [ ] Verify root cause hypothesis
- [ ] Fix at source, never band-aids
- [ ] Add regression test
