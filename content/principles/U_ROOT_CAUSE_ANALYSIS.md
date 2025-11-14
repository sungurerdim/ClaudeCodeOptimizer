---
id: U_ROOT_CAUSE_ANALYSIS
title: Root Cause Analysis
category: universal
severity: high
weight: 9
enforcement: SHOULD
applicability:
  project_types: ['all']
  languages: ['all']
---

# U_ROOT_CAUSE_ANALYSIS: Root Cause Analysis 🔴

**Severity**: High

When debugging, always trace to source. Fix at source, not symptom.

**Enforcement**: SHOULD

**Project Types**: all
**Languages**: all

---

## Why

### The Problem
- **Symptom fixing** creates whack-a-mole debugging - fix one symptom, another appears
- **Band-aid solutions** accumulate technical debt
- **Surface-level fixes** leave underlying bugs dormant until they explode
- **Recurring bugs** waste time fixing the same issue repeatedly
- **Cascading failures** occur when root cause spreads to other areas

### Business Value
- **90% reduction in recurring bugs** (fix once, fixed forever)
- **70% less debugging time** overall (invest upfront, save massively later)
- **Prevents escalation** - stop small bugs before they become P0 incidents
- **Improves reliability** - systems without root causes are stable
- **Reduces technical debt** - no band-aids piling up

### Technical Benefits
- **Single source of truth** - fix propagates everywhere automatically
- **Prevents related bugs** - root cause fix often prevents future similar issues
- **Cleaner codebase** - no workarounds cluttering logic
- **Confident deployment** - know issue is truly resolved
- **Knowledge building** - understanding root causes builds system expertise

### Industry Evidence
- **Toyota 5 Whys** - Legendary lean manufacturing methodology
- **Google SRE** - "Focus on root cause, not symptoms" (SRE handbook)
- **Netflix Chaos Engineering** - Find root causes before they find you
- **Amazon Root Cause Analysis (RCA)** - Required for all P0/P1 incidents
- **Microsoft postmortem culture** - "True root cause" mandatory field

---

## How

### The 5 Whys Technique

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

### Implementation Workflow

#### Step 1: Reproduce the Issue
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

#### Step 2: Trace Backwards from Symptom
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

#### Step 3: Verify Root Cause
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

#### Step 4: Fix at Root Cause
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

#### Step 5: Verify Fix Resolves Original Symptom
```python
# End-to-end test verifying symptom is gone
def test_user_sees_data_after_login():
    # Given: User logs in
    login('testuser', 'password123')

    # When: User loads page
    page_data = load_user_data()

    # Then: Data loads successfully (symptom resolved)
    assert page_data is not None
    assert page_data.user_id == 123
```

---

## Anti-Patterns

### ❌ Anti-Pattern 1: Band-Aid Fix (Symptom Covering)
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

### ❌ Anti-Pattern 2: Scatter-Shot Fixing
```python
# ❌ BAD: Fix every place symptom appears
def endpoint1():
    data = get_data()
    if data is None:
        data = []  # Fix #1

def endpoint2():
    data = get_data()
    if data is None:
        data = []  # Fix #2 (duplicate!)

def endpoint3():
    data = get_data()
    if data is None:
        data = []  # Fix #3 (duplicate!)

# Problem: get_data() is broken - fix it ONCE at root cause!

# ✅ GOOD: Fix once at root cause
def get_data():
    try:
        result = db.query("SELECT * FROM data")
        return result if result else []  # Handle empty at source
    except DatabaseError as e:
        logger.error(f"DB error: {e}")
        return []  # Graceful fallback at source

# All callers automatically fixed
def endpoint1():
    return get_data()  # Always returns list

def endpoint2():
    return get_data()  # Always returns list

def endpoint3():
    return get_data()  # Always returns list
```

### ❌ Anti-Pattern 3: Stop at First "Why"
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

### ❌ Anti-Pattern 4: Blame External Dependencies
```python
# ❌ BAD: "It's the library's fault"
def send_email(to, subject, body):
    try:
        smtp.send(to, subject, body)
    except SMTPException:
        # "SMTP library is broken, nothing we can do"
        logger.error("Email failed")
        return False

# ✅ GOOD: Investigate root cause
def send_email(to, subject, body):
    # WHY does SMTP fail?
    # Investigation reveals: No authentication credentials configured

    # ROOT CAUSE: Missing SMTP_USERNAME/SMTP_PASSWORD env vars
    if not (os.getenv('SMTP_USERNAME') and os.getenv('SMTP_PASSWORD')):
        raise ConfigurationError("SMTP credentials not configured")

    # Fix at deployment configuration, not code
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
```python
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

# Step 2: Analyze root cause commit
$ git show <bad_commit>
# Shows exact change that introduced bug
```

### Tool 3: Differential Debugging
```python
# Compare working vs broken to isolate root cause

# Working environment
$ curl http://staging-api.com/endpoint
{"status": "success", "data": [...]}

# Broken environment
$ curl http://prod-api.com/endpoint
{"status": "error", "message": "Internal Server Error"}

# What's different?
$ diff <(env | grep DB) staging.env prod.env
- DB_HOST=staging-db.internal
+ DB_HOST=prod-db.internal  # Different!

# Root cause: prod-db.internal DNS not resolving
```

### Tool 4: The Rubber Duck Method
```python
# Explain the problem out loud step-by-step
# Often reveals root cause through logical explanation

"""
"So the user clicks login, which calls /api/auth/login,
which checks the database, and... wait, which database?
Oh! We're connecting to the wrong database instance!
That's why credentials aren't found!"
"""
```

### Tool 5: Add Instrumentation
```python
# ❌ BAD: Guess root cause
def process_transaction(amount):
    balance = get_balance()
    balance -= amount  # Sometimes becomes negative!
    save_balance(balance)

# ✅ GOOD: Add logging to trace root cause
def process_transaction(amount):
    logger.info(f"Transaction start: amount={amount}")
    balance = get_balance()
    logger.info(f"Current balance: {balance}")

    if balance < amount:
        logger.error(f"Insufficient funds: {balance} < {amount}")
        raise InsufficientFundsError()

    new_balance = balance - amount
    logger.info(f"New balance: {new_balance}")
    save_balance(new_balance)
    logger.info("Transaction complete")

# Logs reveal: get_balance() returns stale cached value
# ROOT CAUSE: Cache invalidation not working
```

---

## Real-World Examples

### Example 1: The Null Pointer Mystery
```java
// Symptom: NullPointerException on line 42
String username = user.getName().toLowerCase();  // Line 42

// ❌ BAD FIX: Defensive programming
String username = user != null && user.getName() != null
    ? user.getName().toLowerCase()
    : "unknown";  // Band-aid!

// ✅ GOOD: Root cause analysis
// Why #1: Why is user null? → getUserById() returns null
// Why #2: Why does getUserById() return null? → User not in cache
// Why #3: Why not in cache? → Cache expired
// Why #4: Why did cache expire? → TTL too short (60s)
// Why #5: Why TTL so short? → Copy-pasted from example code

// ROOT CAUSE: Cache TTL misconfigured
// FIX: Increase TTL to 30 minutes based on actual usage pattern
config.setCacheTTL(Duration.ofMinutes(30));
```

### Example 2: The Slow Query
```sql
-- Symptom: Query takes 30 seconds

-- ❌ BAD FIX: Increase timeout
SET query_timeout = 60;  -- Just making symptom less visible!

-- ✅ GOOD: Root cause analysis
-- Why #1: Why is query slow? → Full table scan
EXPLAIN SELECT * FROM orders WHERE user_id = 123;
-- Shows: table scan on 10M rows

-- Why #2: Why full table scan? → No index on user_id
SHOW INDEXES FROM orders;
-- Shows: Only primary key index, no user_id index

-- Why #3: Why no index? → Forgot to add in migration
-- Migration v0023 created orders table but didn't add indexes

-- Why #4: Why did migration not add indexes?
-- Developer didn't know indexes were needed (lack of review)

-- ROOT CAUSE: Missing index + inadequate code review
-- FIX: Add index + update review checklist
CREATE INDEX idx_orders_user_id ON orders(user_id);
-- Also: Add "check EXPLAIN plans" to code review checklist
```

### Example 3: The Memory Leak
```python
# Symptom: Application memory grows until OOM crash

# ❌ BAD FIX: Increase memory limit
docker run -m 16G myapp  # Was 8G, doubled it (band-aid!)

# ✅ GOOD: Root cause analysis
# Why #1: Why is memory growing? → Objects not garbage collected
import gc
print(f"Tracked objects: {len(gc.get_objects())}")  # Grows over time

# Why #2: Why not garbage collected? → Strong references held
import objgraph
objgraph.show_most_common_types(limit=10)
# Shows: 1,000,000+ EventListener objects

# Why #3: Why so many EventListener objects? → Never unregistered
# Code review reveals:
def register_user_events(user):
    listener = UserEventListener(user)
    event_bus.register(listener)
    # MISSING: event_bus.unregister(listener) when user logs out

# ROOT CAUSE: Event listeners never cleaned up
# FIX: Add cleanup on logout + context manager for auto-cleanup
class UserEventListener:
    def __enter__(self):
        event_bus.register(self)
        return self

    def __exit__(self, *args):
        event_bus.unregister(self)  # Auto-cleanup

with UserEventListener(user) as listener:
    # Listener automatically cleaned up when context exits
    handle_user_session()
```

---

## Implementation Checklist

- [ ] **When bug appears:** Don't jump to fix, start investigation
- [ ] **Reproduce reliably:** Create test that demonstrates bug
- [ ] **Ask "Why?" 5 times:** Drill down from symptom to root cause
- [ ] **Verify root cause:** Test hypothesis before implementing fix
- [ ] **Fix at source:** Change root cause, not symptoms
- [ ] **Verify fix propagates:** Original symptom should disappear automatically
- [ ] **Add regression test:** Ensure bug never returns
- [ ] **Document root cause:** Share learning with team

---

## Metrics and Monitoring

### Key Indicators
- **Bug recurrence rate:** % of bugs that return after "fix"
- **Time to root cause:** Hours from symptom report to root cause identification
- **Fix effectiveness:** % of fixes that resolve issue permanently
- **Related bug prevention:** Bugs prevented by root cause fix (not just reported bug)

### Success Criteria
- Zero recurring bugs (fixed once = fixed forever)
- Root cause identified in < 2 hours for P1 issues
- 90%+ fix effectiveness (permanent resolution)
- Documented root cause for all P0/P1 incidents

---

## Cross-References

**Related Principles:**
- **U_EVIDENCE_BASED** - Root cause requires evidence, not assumptions
- **U_FAIL_FAST** - Fast failure helps isolate root cause quickly
- **U_TEST_FIRST** - TDD helps identify root cause during development
- **U_INTEGRATION_CHECK** - Integration issues often reveal root causes
- **P_AUDIT_LOGGING** - Logs enable root cause analysis
- **P_OBSERVABILITY_WITH_OTEL** - Tracing helps identify root causes
- **P_CONTINUOUS_PROFILING** - Performance root causes found through profiling

**Enables:**
- **U_CHANGE_VERIFICATION** - Verifying root cause fix resolves all symptoms
- **U_DRY** - Fixing root cause once eliminates duplicate symptom fixes

---

## Industry Standards Alignment

- **Toyota 5 Whys** - Lean manufacturing root cause methodology
- **Six Sigma DMAIC** - Define, Measure, Analyze, Improve, Control
- **ITIL Incident Management** - Root cause analysis required for major incidents
- **Google SRE Practices** - Postmortem culture with root cause requirement
- **Amazon COE (Correction of Error)** - 5 Whys mandatory for all incidents
- **ISO/IEC 27001** - Root cause analysis for security incidents
- **Kepner-Tregoe Problem Solving** - Systematic root cause identification

---

## Tools and Techniques

### Python
```python
import pdb  # Python debugger
pdb.set_trace()  # Break at suspected root cause

import logging
logging.basicConfig(level=logging.DEBUG)  # Trace execution

import traceback
traceback.print_exc()  # Full stack trace to root cause
```

### JavaScript
```javascript
console.trace();  // Print stack trace

debugger;  // Break in browser DevTools

Error.captureStackTrace(this);  // Capture stack for analysis
```

### Go
```go
import "runtime/debug"
debug.PrintStack()  // Print stack trace

import "log"
log.Printf("Checkpoint: value=%v", value)  // Trace execution
```

### General Tools
- **Git bisect** - Find root cause commit
- **strace / ltrace** - System call tracing (Linux)
- **dtrace** - Dynamic tracing (macOS/BSD)
- **Wireshark** - Network packet analysis
- **gdb / lldb** - Native debuggers

---

## Common Pitfalls

1. **Stopping too early** - Fix first symptom found, not actual root
2. **Blaming external factors** - "It's the database/network/library" without proof
3. **Time pressure shortcuts** - "No time for root cause, just fix it quick"
4. **Assumption-based debugging** - Guessing root cause instead of proving it
5. **Ignoring related symptoms** - Fix one symptom, ignore others from same root
6. **No verification** - Assume fix works without testing
7. **No documentation** - Fix bug but don't document root cause for future

---

## Migration Strategy

### Phase 1: Awareness (Week 1)
- Train team on 5 Whys technique
- Require "root cause" field in bug reports
- Review recent bug fixes - were they root causes or symptoms?

### Phase 2: Practice (Week 2-4)
- Apply 5 Whys to all new bugs
- Document root cause analysis in PR descriptions
- Track bug recurrence rate

### Phase 3: Culture (Week 5+)
- Root cause analysis mandatory for all P0/P1 incidents
- Share root cause findings in team meetings
- Celebrate deep root cause discoveries
- Build knowledge base of common root causes

---

## Summary

**Root Cause Analysis** means always tracing from symptom to underlying cause and fixing at the source. Use the 5 Whys technique to drill down systematically.

**Core Rule**: Fix the disease, not the symptoms.

**Remember**: "Band-aids accumulate. Root cause fixes compound."

**Impact**: 90% reduction in recurring bugs, 70% less overall debugging time, permanent solutions instead of temporary patches.
