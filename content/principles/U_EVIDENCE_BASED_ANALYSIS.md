---
id: U_EVIDENCE_BASED_ANALYSIS
title: Evidence-Based Analysis
category: universal
severity: critical
weight: 10
enforcement: SHOULD
applicability:
  project_types: ['all']
  languages: ['all']
---

# U_EVIDENCE_BASED_ANALYSIS: Evidence-Based Analysis 🔴

**Severity**: Critical

Never claim completion without command execution proof. When debugging, always trace to root cause using the 5 Whys technique. All verification requires fresh command output with exit codes. Fix at source, not symptom.

**Enforcement**: SHOULD

**Project Types**: all
**Languages**: all

---

## Why

### The Problem
- **Assumption-based development** leads to 60%+ of production bugs
- **Symptom fixing** creates whack-a-mole debugging
- "It should work" without verification causes cascading failures
- **Band-aid solutions** accumulate technical debt
- **Surface-level fixes** leave underlying bugs dormant until they explode

---

## Core Principles

### 1. Evidence-Based Verification

**Every claim MUST be supported by:**
1. **Command execution output** (not assumptions)
2. **Exit codes** (0 = success, non-zero = failure)
3. **Timestamps** (prove freshness of verification)
4. **Error messages** (when applicable)

### 2. Root Cause Analysis (5 Whys)

**Ask "Why?" five times to drill down from symptom to root cause:**

```
Problem: "API is returning 500 errors"

Why #1: Why is API returning 500?
→ Database queries are timing out

Why #2: Why are queries timing out?
→ Lock wait timeout exceeded (1213)

Why #3: Why are locks being held too long?
→ Batch update process holds locks for 30+ seconds

Why #4: Why does batch update hold locks so long?
→ It updates 100,000 rows in a single transaction

Why #5: Why does it need single transaction for 100k rows?
→ Developer thought it would be faster / ensure consistency

ROOT CAUSE: Batch process design - should chunk updates (1000 rows each)
FIX: Refactor batch process to use chunked transactions
```

---

## Implementation Workflow

### Step 1: Reproduce the Issue

```python
# ✅ ALWAYS reproduce first
def test_reproduces_bug():
    """Test that demonstrates the bug reliably"""
    result = process_data(malformed_input)
    # This should pass BEFORE fix, fail AFTER fix
    assert result.error is not None  # Bug: doesn't validate input
```

**Why reproduce:**
- Proves you understand the issue
- Enables iterative debugging
- Creates regression test for later

### Step 2: Trace Backwards from Symptom

```python
# Start at symptom and work backwards
# Symptom: "User sees blank page"

# Step 2a: Check rendering
print(f"Template data: {template_data}")  # Data is None

# Step 2b: Check data loading
print(f"DB query result: {query_result}")  # Returns empty []

# Step 2c: Check query construction
print(f"SQL query: {sql}")  # WHERE user_id = NULL

# Step 2d: Check user_id source
print(f"User ID from session: {session.get('user_id')}")  # None

# ROOT CAUSE FOUND: Session not set on login
```

### Step 3: Verify Root Cause

```python
# ✅ Verify this is THE root cause by testing hypothesis
def test_root_cause_hypothesis():
    # Hypothesis: Session not set on login causes blank page

    # Test 1: Manually set session
    session['user_id'] = 123
    result = load_user_data()
    assert result is not None  # PASSES - hypothesis supported

    # Test 2: Without session
    session.clear()
    result = load_user_data()
    assert result is None  # PASSES - confirms root cause
```

### Step 4: Fix at Root Cause

```python
# ❌ BAD: Fix symptom
def load_user_data():
    user_id = session.get('user_id')
    if user_id is None:
        return DEFAULT_DATA  # Band-aid! Doesn't fix login issue

# ✅ GOOD: Fix root cause
def login(username, password):
    user = authenticate(username, password)
    if user:
        session['user_id'] = user.id  # FIX ROOT CAUSE
        session['username'] = user.name
        return True
    return False
```

### Step 5: Verify Fix with Evidence

```bash
# Execute command and capture output
$ pytest tests/test_auth.py::test_user_login -v
================================ test session starts =================================
collected 1 item

tests/test_auth.py::test_user_login PASSED                                   [100%]

================================ 1 passed in 0.45s ==================================
$ echo $?
0

# Evidence: Test passed, exit code 0 confirms success
```

---

## Anti-Patterns

### ❌ Band-Aid Fix (Symptom Covering)

```python
# ❌ BAD: Fixing symptom
def calculate_discount(price, discount_percentage):
    try:
        result = price * (discount_percentage / 100)
        return result
    except TypeError:
        # Band-aid: Just return original price
        return price  # Hides the real issue!

# Problem: TypeError means invalid input - FIX THE INPUT VALIDATION!

# ✅ GOOD: Fix root cause
def calculate_discount(price: float, discount_percentage: float) -> float:
    # Root cause: No input validation
    if not isinstance(price, (int, float)) or price < 0:
        raise ValueError(f"Invalid price: {price}")
    if not isinstance(discount_percentage, (int, float)) or not (0 <= discount_percentage <= 100):
        raise ValueError(f"Invalid discount: {discount_percentage}")

    return price * (1 - discount_percentage / 100)
```

### ❌ Assumption-Based Claims

```plaintext
# ❌ BAD: Unverified claim
"I fixed the authentication bug."
- NO proof of execution
- NO test output
- NO verification
- UNACCEPTABLE

# ✅ GOOD: Evidence-based claim
"Fixed authentication bug. Verification:

$ pytest tests/test_auth.py -v
================================ test session starts =================================
tests/test_auth.py::test_login PASSED                                       [100%]
================================ 1 passed in 0.32s ==================================
$ echo $?
0

Root cause: Session not set on login (login.py:45)
Fix: Added session['user_id'] = user.id (login.py:47)
Evidence: Test passes, exit code 0"
```

### ❌ Stop at First "Why"

```python
# Problem: "API is slow"

# ❌ BAD: Stop at first why
Why: "API is slow"
Because: "Database query takes 5 seconds"
Fix: Add caching  # WRONG - didn't find root cause!

# ✅ GOOD: Keep asking why
Why #1: Why is API slow? → DB query takes 5s
Why #2: Why does query take 5s? → Scanning 1M rows
Why #3: Why scanning 1M rows? → No index on user_id column
Why #4: Why no index? → Database schema missing indexes
Why #5: Why missing indexes? → Migration script incomplete

ROOT CAUSE: Migration script didn't create indexes
FIX: Add index creation to migration, apply to all environments
```

---

## Verification Examples

### Example 1: Test Verification

```bash
# ❌ Bad: Unverified claim
"Tests pass"

# ✅ Good: Evidence-based verification
$ pytest tests/ -v --tb=short
================================ test session starts =================================
collected 156 items

tests/test_auth.py ✓✓✓✓✓✓✓✓✓✓✓✓ [12/156]
tests/test_api.py ✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓ [27/156]
...
================================ 156 passed in 12.3s ==================================
$ echo $?
0

# Evidence: 156 tests passed, exit code 0
```

### Example 2: Build Verification

```bash
# ❌ Bad: Assumption
"Build successful"

# ✅ Good: Command output
$ npm run build
✓ 243 modules compiled successfully
Build completed in 4.2s
$ echo $?
0

# Evidence: Build succeeded, exit code 0
```

### Example 3: Root Cause Analysis

```bash
# Symptom: NullPointerException on line 42
String username = user.getName().toLowerCase();  # Line 42

# ❌ BAD FIX: Defensive programming
String username = user != null && user.getName() != null
    ? user.getName().toLowerCase()
    : "unknown";  # Band-aid!

# ✅ GOOD: Root cause analysis
# Why #1: Why is user null? → getUserById() returns null
# Why #2: Why does getUserById() return null? → User not in cache
# Why #3: Why not in cache? → Cache expired
# Why #4: Why did cache expire? → TTL too short (60s)
# Why #5: Why TTL so short? → Copy-pasted from example code

# ROOT CAUSE: Cache TTL misconfigured
# FIX: Increase TTL to 30 minutes based on actual usage pattern
config.setCacheTTL(Duration.ofMinutes(30));
```

---

## Root Cause Analysis Tools

### Tool 1: Stack Trace Analysis

```python
# Use stack traces to trace backwards
try:
    process_order(order)
except Exception as e:
    import traceback
    print("=== FULL STACK TRACE ===")
    traceback.print_exc()
    # Stack trace shows exact path from symptom to root cause
```

### Tool 2: Binary Search Debugging

```bash
# When root cause is unclear, use binary search
# Problem: "Tests passed yesterday, failing today"

# Step 1: git bisect to find bad commit
$ git bisect start
$ git bisect bad HEAD  # Current commit is bad
$ git bisect good v1.2.0  # Last known good version
# Git will checkout middle commit - test it
$ pytest tests/
$ git bisect good  # If tests pass
$ git bisect bad   # If tests fail
# Repeat until root cause commit found
```

### Tool 3: The 5 Whys Template

```
Problem: [Symptom]

Why #1: [First cause]
Why #2: [Deeper cause]
Why #3: [Even deeper]
Why #4: [Almost there]
Why #5: [Root cause]

ROOT CAUSE: [The real issue]
FIX: [Solution at root]
VERIFICATION: [Evidence that fix works]
```

---

## Implementation Checklist

### Evidence-Based Verification
- [ ] **Before claiming completion:** Run the command
- [ ] **Capture full output:** Not just summary
- [ ] **Check exit code:** `echo $?` (bash), `$LASTEXITCODE` (PowerShell)
- [ ] **Verify timestamps:** Ensure fresh execution
- [ ] **Document failures:** Include error messages
- [ ] **Re-run after fixes:** Prove the fix works

### Root Cause Analysis
- [ ] **Reproduce reliably:** Create test that demonstrates bug
- [ ] **Ask "Why?" 5 times:** Drill down from symptom to root cause
- [ ] **Verify root cause:** Test hypothesis before implementing fix
- [ ] **Fix at source:** Change root cause, not symptoms
- [ ] **Verify fix propagates:** Original symptom should disappear
- [ ] **Add regression test:** Ensure bug never returns
- [ ] **Document root cause:** Share learning with team

---

## Metrics and Monitoring

### Key Indicators
- **Verification coverage:** % of claims with evidence
- **Bug recurrence rate:** % of bugs that return after "fix"
- **Root cause accuracy:** % of fixes that resolve issue permanently
- **Time to root cause:** Hours from symptom to root cause identification

### Success Criteria
- 100% of completion claims have command output
- 100% of verifications include exit codes
- Zero recurring bugs (fixed once = fixed forever)
- Root cause identified in < 2 hours for P1 issues

---

## Summary

**Evidence-Based Analysis** eliminates assumptions by requiring proof through command execution and exit codes, while using the 5 Whys technique to trace from symptom to root cause. Every completion claim MUST be backed by fresh, verifiable output, and every fix MUST address the root cause, not symptoms.

**Core Rules:**
- **No assumptions** - Execute commands, capture output, verify exit codes
- **Fresh evidence** - Recent execution, not cached results
- **5 Whys** - Always drill down to root cause
- **Fix at source** - Never apply band-aids to symptoms
- **Verify fix** - Prove the fix resolves the original symptom
