---
metadata:
  name: "Test-First Verification"
  activation_keywords: ["characterization", "behavior capture", "before refactoring", "before fixing"]
  category: "enforcement"
principles: ['U_TEST_FIRST', 'U_EVIDENCE_BASED', 'U_CHANGE_VERIFICATION', 'P_TEST_COVERAGE', 'U_INTEGRATION_CHECK']
---

# Test-First Verification

Capture current behavior BEFORE modifying code to prevent silent breakage during refactoring.

<!-- INSTRUCTIONS: Load when activated -->
## Detailed Instructions

### When This Skill Activates

This skill activates BEFORE any code modification command:
- `/cco-fix-code` applies auto-fixes
- `/cco-refactor-duplicates` extracts duplicate code
- `/cco-cleanup-dead-code` removes unused code

**Trigger:** Command identifies code to modify

### The Core Principle

**Characterization Tests = Tests that assert CURRENT behavior (not ideal, just current)**

Why?
- Refactoring should NOT change behavior
- Tests verify behavior stays identical
- If test fails after refactor → behavior changed (may be bug)

### The Protocol

For each function to modify:

1. **ANALYZE Current Behavior**
   - Run function with sample inputs
   - Capture actual outputs
   - Note edge cases (None, empty, exceptions)

2. **GENERATE Characterization Test**
   ```python
   def test_characterization_<function_name>():
       """Captures current behavior before refactoring.

       This test asserts CURRENT behavior, not necessarily CORRECT behavior.
       If this test fails after refactoring, behavior changed.
       """
       # Test case 1: Normal inputs
       assert function(normal_input) == current_output

       # Test case 2: Edge case
       assert function(edge_case) == current_edge_output

       # Test case 3: Error case (if applicable)
       with pytest.raises(CurrentException):
           function(bad_input)
   ```

3. **RUN Characterization Test**
   ```bash
   pytest test_characterization_*.py
   # MUST pass (tests current behavior)
   ```

4. **APPLY Code Change**
   - Perform refactoring/fix/cleanup

5. **RUN Characterization Test Again**
   ```bash
   pytest test_characterization_*.py
   # If PASS → behavior unchanged ✓
   # If FAIL → behavior changed ⚠ (review needed)
   ```

6. **RUN Full Test Suite**
   ```bash
   pytest
   # Ensure no regressions
   ```

7. **COMMIT** (with characterization tests)
   ```bash
   git add <modified_code> test_characterization_*.py
   git commit -m "refactor: extract duplicate function (behavior verified)"
   ```

<!-- RESOURCES: Load on explicit request -->
## Examples & Resources

### Example 1: Refactoring Duplicate Code

**Before:**
```python
# services/api/handlers.py
def process_request(data):
    if not data:
        return {"error": "No data"}
    result = validate(data)
    if result:
        return {"status": "success", "data": result}
    return {"error": "Invalid"}

# services/worker/tasks.py (duplicate!)
def process_request(data):
    if not data:
        return {"error": "No data"}
    result = validate(data)
    if result:
        return {"status": "success", "data": result}
    return {"error": "Invalid"}
```

**Command:** `/cco-refactor-duplicates`

**Skill activates:**

```
"Found duplicate: process_request() in 2 locations
Generating characterization tests..."
```

**Generated test:**
```python
# test_characterization_process_request.py
import pytest
from services.api.handlers import process_request as api_process
from services.worker.tasks import process_request as worker_process

def test_characterization_api_process_request():
    """Captures current behavior of API handler before refactoring."""

    # Test case 1: Valid data
    result = api_process({"key": "value"})
    assert result == {"status": "success", "data": {"key": "value"}}

    # Test case 2: None
    result = api_process(None)
    assert result == {"error": "No data"}

    # Test case 3: Empty dict
    result = api_process({})
    assert result == {"error": "No data"}

    # Test case 4: Invalid data
    result = api_process({"bad": "data"})
    assert result == {"error": "Invalid"}

def test_characterization_worker_process_request():
    """Captures current behavior of worker task before refactoring."""

    # Same tests for worker version
    result = worker_process({"key": "value"})
    assert result == {"status": "success", "data": {"key": "value"}}

    # ... (same test cases)
```

**Skill:**
```
"Running characterization tests..."
pytest test_characterization_process_request.py
"✓ 8/8 tests pass (current behavior captured)"

"Safe to refactor. Proceed? (y/n)"
```

**User:** y

**After refactoring:**
```python
# shared/handlers.py (NEW - extracted)
def process_request(data):
    if not data:
        return {"error": "No data"}
    result = validate(data)
    if result:
        return {"status": "success", "data": result}
    return {"error": "Invalid"}

# services/api/handlers.py (UPDATED)
from shared.handlers import process_request

# services/worker/tasks.py (UPDATED)
from shared.handlers import process_request
```

**Skill:**
```
"Refactoring complete. Verifying behavior..."
pytest test_characterization_process_request.py
"✓ 8/8 tests pass (behavior unchanged!)"

"Running full test suite..."
pytest
"✓ All tests pass"

"Committing refactoring + characterization tests..."
```

### Example 2: Fixing Code with Auto-Fix

**Before:**
```python
# shared/utils.py
def calculate_total(items):
    total = 0
    for item in items:
        total += item
    return total
```

**Command:** `/cco-fix-code` (wants to use sum() instead of loop)

**Skill activates:**

```
"Generating characterization test for calculate_total()..."
```

**Generated test:**
```python
# test_characterization_calculate_total.py
import pytest
from shared.utils import calculate_total

def test_characterization_calculate_total():
    """Captures current behavior before auto-fix."""

    # Test case 1: Normal list
    assert calculate_total([1, 2, 3, 4]) == 10

    # Test case 2: Empty list
    assert calculate_total([]) == 0

    # Test case 3: Negative numbers
    assert calculate_total([-1, 1, -2, 2]) == 0

    # Test case 4: Single item
    assert calculate_total([42]) == 42

    # Test case 5: What about None? (edge case discovered)
    # Current code: UnboundLocalError (bug!)
    with pytest.raises(UnboundLocalError):
        calculate_total(None)

    # Test case 6: What about strings? (edge case discovered)
    # Current code: TypeError (expected)
    with pytest.raises(TypeError):
        calculate_total(["a", "b"])
```

**Skill:**
```
"⚠ Discovered edge case: calculate_total(None) raises UnboundLocalError
This is a BUG in current code. Should we fix it? (y/n)"
```

**User:** y

**Skill:**
```
"Updating characterization test to assert CORRECT behavior..."
```

**Updated test:**
```python
def test_characterization_calculate_total():
    # ... (previous tests)

    # Test case 5: None should raise ValueError (correct behavior)
    with pytest.raises(ValueError, match="items cannot be None"):
        calculate_total(None)
```

**After auto-fix:**
```python
def calculate_total(items):
    if items is None:
        raise ValueError("items cannot be None")
    return sum(items)
```

**Skill:**
```
"Running characterization tests..."
"✓ All tests pass (behavior corrected + optimized)"
```

### Edge Case Discovery

Characterization tests often discover bugs!

**Common Discoveries:**

1. **None handling missing**
   ```python
   # Current code crashes on None
   # Characterization test exposes this
   with pytest.raises(AttributeError):
       function(None)

   # After fix: proper validation
   with pytest.raises(ValueError, match="input cannot be None"):
       function(None)
   ```

2. **Empty collection handling**
   ```python
   # Current code returns wrong value for empty list
   assert function([]) == 0  # Should be None?

   # Prompt discussion: "Is 0 correct for empty list?"
   ```

3. **Type inconsistencies**
   ```python
   # Function returns dict sometimes, None other times
   result = function(valid_input)
   assert isinstance(result, dict)

   result = function(invalid_input)
   assert result is None  # Should raise exception instead?
   ```

### Integration with Commands

#### fix-code.md
Add after Phase 2 (Filter Safe Fixes):

```markdown
## Phase 2.5: Generate Characterization Tests

Before applying fixes, activate test-first-verification:

Use Skill tool:
Skill("test-first-verification")

For each function to fix:
1. Generate characterization test (current behavior)
2. Run test (must pass)
3. Apply fix
4. Run test again (must still pass)
5. If test fails → behavior changed → manual review
```

#### refactor-duplicates.md
Add at the beginning:

```markdown
## Phase 0: Characterization Test Generation

Before refactoring, activate test-first-verification:

Use Skill tool:
Skill("test-first-verification")

This ensures:
- Current behavior captured
- Refactoring safe
- No silent breakage
```

### Test File Naming Convention

```
test_characterization_<function_name>.py
```

Examples:
- `test_characterization_process_request.py`
- `test_characterization_calculate_total.py`
- `test_characterization_validate_user_input.py`

**Location:** Same directory as regular tests (`tests/`)

**Lifecycle:**
- Keep characterization tests for 1 sprint
- After 1 sprint: Merge into regular test suite or delete
- Rationale: Once refactoring is stable, integrate into main tests

### Anti-Patterns to Prevent

#### WRONG: Refactor First, Test Later

```
User: "I'll extract this duplicate function"
<Extracts to shared module>
<Changes imports>
<Runs tests>
Tests: "AssertionError: expected 200, got 404"
User: "Did my refactoring break this? Or was test already broken?"
<No way to know - no baseline>
```

#### RIGHT: Characterization Test First

```
Skill: "Generating characterization test..."
<Creates test that asserts current behavior>
Skill: "Current behavior: returns 404 for invalid input"
Skill: "Is this correct? (y/n)"
User: "No, should return 400"
Skill: "Updating test to assert correct behavior..."
<Now refactoring AND bug fix in one step>
```

### Success Metrics

**Before (without skill):**
- Behavior changes: 30% of refactorings
- Debugging time: 1-2 hours per broken refactoring
- Confidence: Low (fear of refactoring)

**After (with skill):**
- Behavior changes: 5% (and caught immediately)
- Debugging time: 10 minutes (test shows exact difference)
- Confidence: High (tests prove behavior unchanged)

### When to Skip This Skill

Skip characterization tests if:
- Function is brand new (no "current behavior" to capture)
- Function is already covered by comprehensive tests
- Refactoring is trivial (rename variable)
- User explicitly requests: `/cco-fix-code --no-characterization`
