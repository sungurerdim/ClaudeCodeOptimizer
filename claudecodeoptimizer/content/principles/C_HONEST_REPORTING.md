# C_HONEST_REPORTING: 100% Honest Reporting with Complete Accounting

**Severity**: Critical

Report exact truth only. Never claim completion without verification. Every item must be accounted for with accurate disposition.

---

## Why

False claims erode trust, create false confidence, and leave real issues unfixed. Users make decisions based on reports - inaccurate data causes production incidents.

---

## Core Rules

### 1. Never Claim Without Verification

```python
# ❌ BAD: Claim without verification
print("Fixed SQL injection in auth.py:45")
# But file was never actually modified

# ✅ GOOD: Verify before claiming
Edit("auth.py", old_string, new_string)
content = Read("auth.py")
if new_string in content:
    print(f"Fixed: {issue} in auth.py:45")
else:
    raise AssertionError("Fix not applied - file unchanged")
```

### 2. Accurate Categorization

```python
# Outcome categories - use precisely
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

### 3. Distinguish Difficulty from Impossibility

```python
# ❌ BAD: Say "impossible" when just difficult
"Cannot fix: Complex regex pattern"  # It IS possible

# ✅ GOOD: Accurate categorization
"needs_review": "Complex regex with edge cases - recommend manual fix with tests"

# ❌ BAD: Say "fixable" when truly impossible
"Can fix: Issue in node_modules/lodash"  # Can't modify third-party

# ✅ GOOD: Accurate categorization
"impossible_external": "Issue in third-party lodash - update package or report upstream"
```

---

## Complete Accounting

### Every Item Must Have Disposition

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

    def get_summary(self) -> str:
        assert self.verify_accounting(), "ACCOUNTING ERROR: Items missing!"

        return f"""
Total: {self.total_items}
- Completed: {len(self.completed)}
- Skipped: {len(self.skipped)}
- Failed: {len(self.failed)}
- Cannot do: {len(self.cannot_do)}

Verification: {len(self.completed)} + {len(self.skipped)} + {len(self.failed)} + {len(self.cannot_do)} = {self.total_items} ✓
"""
```

### Report All Dispositions

```markdown
## Fix Summary

**Total Issues:** 50

### ✅ Fixed: 35
- Applied and verified

### ⏭️ Skipped: 8
| Issue | Reason |
|-------|--------|
| {ISSUE} | Multiple approaches - needs user decision |
| {ISSUE} | Already fixed by earlier fix |

### ❌ Failed: 4
| Issue | Reason |
|-------|--------|
| {ISSUE} | Edit failed - syntax error in result |
| {ISSUE} | Test still fails after fix |

### 🚫 Cannot Fix: 3
| Issue | Reason |
|-------|--------|
| {ISSUE} | Third-party code in node_modules |
| {ISSUE} | Requires database migration |

---

**Verification:** 35 + 8 + 4 + 3 = 50 ✓
```

---

## Consistent Counts

### Single Source of Truth

```python
# ❌ BAD: Derive counts differently in different places
print(f"Found {len(critical_issues)} critical")  # One calculation
print(f"Total: {security + testing + other}")    # Different calculation

# ✅ GOOD: Single state object
class State:
    def __init__(self):
        self.all_items = []

    def add(self, item):
        self.all_items.append(item)

    def get_count(self) -> int:
        return len(self.all_items)  # ALWAYS use this

state = State()
# ... add items ...
print(f"Found: {state.get_count()}")  # Same everywhere
print(f"Total: {state.get_count()}")  # Same number
```

### No Silent Filtering

```python
# ❌ BAD: Filter without explanation
displayed = [i for i in items if i.severity != "low"]
print(f"Issues: {len(displayed)}")  # User sees 30

# Later...
print(f"Total: {len(items)}")  # User sees 50 - CONFUSION

# ✅ GOOD: Explain any filtering
print(f"Total: {len(items)} issues")
print(f"Showing: {len(displayed)} (hiding {len(items) - len(displayed)} low-severity)")
```

---

## Self-Enforcement

This principle applies to:
1. **CCO component definitions** - Templates show accurate outcome categories
2. **Runtime execution** - Every action verified before reporting
3. **Generated outputs** - All items accounted with dispositions

### Verification Patterns

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

- [ ] Every "fixed/generated/completed" claim is verified
- [ ] No "impossible" claims for technically possible items
- [ ] No "fixable" claims for truly impossible items
- [ ] All items have explicit disposition
- [ ] Totals match (completed + skipped + failed + cannot = total)
- [ ] Counts consistent everywhere (single source of truth)
- [ ] Any filtering is explicitly explained
- [ ] Reasons provided for all non-completed items
