---
name: evidence-based-analysis
description: Never claim completion without command execution proof, trace to root cause using 5 Whys
type: universal
severity: critical
keywords: [testing, verification, root cause analysis, evidence]
category: [quality, workflow]
---

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

### 2. Complete Accounting

Every item must have a disposition. Never lose track of work:

```python
@dataclass
class AccountingState:
    total_items: int = 0
    completed: List = field(default_factory=list)
    skipped: List[Tuple[Item, str]] = field(default_factory=list)  # (item, reason)
    failed: List[Tuple[Item, str]] = field(default_factory=list)   # (item, reason)
    cannot_do: List[Tuple[Item, str]] = field(default_factory=list) # (item, reason)

    def verify_accounting(self) -> bool:
        """Totals MUST match."""
        accounted = (len(self.completed) + len(self.skipped) +
                    len(self.failed) + len(self.cannot_do))
        return accounted == self.total_items
```

**Formula:** `total = completed + skipped + failed + cannot-do`

### 3. Accurate Outcome Categorization

Use precise categories, never claim "fixed" without verification:

```python
OUTCOMES = {
    # Truly completed
    "fixed": "Change applied AND verified in file",
    "generated": "File created AND exists on disk",
    "completed": "Action performed AND result confirmed",

    # Requires human action
    "needs_decision": "Multiple valid approaches - user must choose",
    "needs_review": "Complex change - requires human verification",
    "requires_approval": "Risky change - needs explicit permission",

    # Outside tool scope
    "requires_migration": "Database schema change - needs migration script",
    "requires_config": "External system configuration needed",
    "requires_infra": "Infrastructure change needed",

    # Truly impossible
    "impossible_external": "Issue in third-party code",
    "impossible_design": "Requires architectural redesign",
    "impossible_runtime": "Runtime-only issue, not fixable in code",
}
```

**Distinguish difficulty from impossibility:**
- ❌ "Cannot fix: Complex regex" (it IS possible)
- ✅ "needs_review: Complex regex with edge cases"
- ❌ "Can fix: Issue in node_modules" (CAN'T modify third-party)
- ✅ "impossible_external: Update package or report upstream"

### 4. Root Cause Analysis (5 Whys)

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

**CRITICAL: Never trust agent output blindly. Always verify.**

```python
# ❌ BAD: Blind trust
agent_result = Task("Fix auth bug")
# No verification

# ✅ GOOD: Verify
agent_result = Task("Fix auth bug")

# Verify file changed
content = Read("auth.py", offset=145, limit=20)
assert "session['user_id']" in content

# Verify accounting
assert result.fixed + result.skipped == result.total

# Run tests
Bash("pytest tests/test_auth.py -v")
```

**Agent Verification Checklist:**

- [ ] Agent claimed "fixed" → Verify file actually changed (Read or git diff)
- [ ] Agent claimed "generated" → Verify file exists (Read or ls)
- [ ] Agent claimed "optimized" → Verify token reduction (word count before/after)
- [ ] Agent provided accounting → Verify formula: `total = completed + skipped + failed`
- [ ] Agent skipped items → Verify reasons are legitimate (not excuses)
- [ ] Agent reported numbers → Verify counts match reality (grep, find, wc)

**Common Output Errors to Detect:**

```python
# Agent: "Fixed 10 issues"
# Verify:
Bash("git diff --stat")  # How many files changed?
# If 0 changes → Claim incorrect!

# Agent: "Applied 20 optimizations"
# Verify accounting:
assert 20 == len(applied) + len(skipped) + len(failed)
# If formula doesn't balance → Items unaccounted for!
```

**Reason Verification:**

```python
# ❌ UNVERIFIABLE (reject):
"File was being modified externally"  # Check git status first!
"Section already optimal"  # Measure tokens to verify!
# ✅ VERIFIABLE:
"File doesn't exist: <path>"  # Verifiable
"Git conflict detected"  # Verifiable
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

### ❌ Inconsistent Counts
```python
# ❌ BAD: Different calculations produce different numbers
print(f"Found {len(critical_issues)} critical")  # One place
print(f"Total: {security + testing + other}")    # Different place

# ✅ GOOD: Single source of truth
class State:
    def __init__(self):
        self.all_items = []

    def get_count(self) -> int:
        return len(self.all_items)  # ALWAYS use this

state = State()
# ... add items ...
print(f"Found: {state.get_count()}")  # Same everywhere
print(f"Total: {state.get_count()}")  # Same number
```

### ❌ Silent Filtering
```python
# ❌ BAD: Filter without explanation
displayed = [i for i in items if i.severity != "low"]
print(f"Issues: {len(displayed)}")  # User sees 30
# Later...
print(f"Total: {len(items)}")  # User sees 50 - CONFUSION

# ✅ GOOD: Explain filtering explicitly
print(f"Total: {len(items)} issues")
print(f"Showing: {len(displayed)} (hiding {len(items) - len(displayed)} low-severity)")
```

---

## Verification Patterns

```python
# After any file modification
def verify_edit(file_path: str, expected_content: str) -> bool:
    content = Read(file_path)
    return expected_content in content

# After any generation
def verify_created(file_path: str) -> bool:
    return os.path.exists(file_path)

# Before claiming completion
def claim_completion(action: str, verification: bool):
    if not verification:
        raise AssertionError(f"Cannot claim '{action}' - verification failed")
    return f"Completed: {action}"
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
- [ ] Every item has disposition (completed/skipped/failed/cannot-do)
- [ ] Totals match (accounting formula verified)
- [ ] Counts consistent everywhere (single source)
- [ ] Any filtering explicitly explained
- [ ] Accurate outcome categories (not "fixed" without verification)
