---
id: cco-refactor
description: Guided refactoring with safety checks
category: feature
priority: normal
principles:
  - 'U_MINIMAL_TOUCH'
  - 'U_CHANGE_VERIFICATION'
  - 'U_TEST_FIRST'
  - 'U_EVIDENCE_BASED'
  - 'C_FOLLOW_PATTERNS'
  - 'U_NO_OVERENGINEERING'
---

# Refactor Code

Guided refactoring with safety checks and test coverage for **${PROJECT_NAME}**.

**Project Type:** ${PROJECT_TYPE}
**Primary Language:** ${PRIMARY_LANGUAGE}

## Objective

Safe code refactoring:
1. Analyze refactoring target
2. Create refactoring plan
3. Run existing tests as baseline
4. Perform refactoring
5. Verify tests still pass
6. Measure improvements

**Output:** Refactored code with verification that behavior is preserved.

---

## Architecture & Model Selection

**Analysis & Planning**: Sonnet (requires deep understanding)
**Execution**: Sonnet (complex transformations)
**Verification**: Haiku (test execution)

**Execution Pattern**: Sequential with rollback on failure

---

## When to Use

**Use this command:**
- Code smells detected
- High complexity functions
- Duplicate code
- Improving maintainability
- Before adding new features

---

## Phase 1: Analyze Target

```python
import sys
sys.path.insert(0, "D:/GitHub/ClaudeCodeOptimizer")

from pathlib import Path
import ast

project_root = Path(".").resolve()

print(f"=== Refactoring Analysis ===\n")

target_file = "src/services/payment_processor.py"
target_function = "process_payment"

print(f"Target: {target_file}::{target_function}")
print()

# Analyze current state
analysis = {
    'complexity': 28,
    'lines': 187,
    'issues': [
        'High cyclomatic complexity (28)',
        'Too many responsibilities',
        'Nested conditionals (5 levels)',
        'No error handling'
    ]
}

print("Current State:")
print(f"  Complexity: {analysis['complexity']}")
print(f"  Lines: {analysis['lines']}")
print()
print("Issues:")
for issue in analysis['issues']:
    print(f"  - {issue}")
print()
```

---

## Phase 2: Create Refactoring Plan

```python
print(f"=== Refactoring Plan ===\n")

plan = '''
## Strategy: Extract Method + Simplify Conditionals

### Step 1: Extract payment validation
- Extract to validate_payment_data()
- Reduces complexity by 5

### Step 2: Extract payment processing logic
- Extract to execute_payment_transaction()
- Reduces complexity by 8

### Step 3: Extract notification logic
- Extract to send_payment_notifications()
- Reduces complexity by 4

### Step 4: Simplify error handling
- Use early returns
- Add specific exception types
- Reduces nesting by 2 levels

### Expected Outcome:
- Complexity: 28 → 11
- Lines: 187 → 120
- Functions: 1 → 4
- Testability: Improved
'''

print(plan)
print()
```

---

## Phase 3: Run Baseline Tests

```python
print(f"=== Baseline Test Run ===\n")

import subprocess

print("Running existing tests...")

try:
    result = subprocess.run(
        ['python', '-m', 'pytest', 'tests/test_payment_processor.py', '-v'],
        capture_output=True,
        text=True,
        cwd=project_root,
        timeout=60
    )

    passed = result.stdout.count(' PASSED')
    failed = result.stdout.count(' FAILED')

    print(f"Baseline Results:")
    print(f"  Passed: {passed}")
    print(f"  Failed: {failed}")
    print()

    if failed > 0:
        print("⚠ Tests failing before refactoring!")
        print("  Fix tests first before refactoring")
        print()
    else:
        print("✓ All tests passing - safe to refactor")
        print()

except (subprocess.TimeoutExpired, FileNotFoundError):
    print("ℹ Could not run tests")
    print()
```

---

## Phase 4: Perform Refactoring

```python
print(f"=== Refactoring Execution ===\n")

# Original code (simplified)
original = '''
def process_payment(self, payment_data):
    # 187 lines of complex logic
    if not payment_data:
        raise ValueError("Missing data")

    if payment_data['amount'] <= 0:
        raise ValueError("Invalid amount")

    if payment_data['currency'] not in ['USD', 'EUR']:
        raise ValueError("Invalid currency")

    # ... 180 more lines ...
'''

# Refactored code
refactored = '''
def process_payment(self, payment_data: dict) -> PaymentResult:
    """Process payment transaction"""
    # Step 1: Validate
    self._validate_payment_data(payment_data)

    # Step 2: Execute
    transaction = self._execute_payment_transaction(payment_data)

    # Step 3: Notify
    self._send_payment_notifications(transaction)

    return PaymentResult(
        success=True,
        transaction_id=transaction.id
    )

def _validate_payment_data(self, data: dict) -> None:
    """Validate payment data"""
    if not data:
        raise PaymentValidationError("Missing payment data")

    if data.get('amount', 0) <= 0:
        raise PaymentValidationError("Amount must be positive")

    if data.get('currency') not in ['USD', 'EUR', 'GBP']:
        raise PaymentValidationError(f"Unsupported currency: {data.get('currency')}")

def _execute_payment_transaction(self, data: dict) -> Transaction:
    """Execute payment transaction"""
    try:
        return self.payment_gateway.charge(
            amount=data['amount'],
            currency=data['currency'],
            source=data['payment_method']
        )
    except GatewayError as e:
        raise PaymentProcessingError(f"Transaction failed: {e}")

def _send_payment_notifications(self, transaction: Transaction) -> None:
    """Send payment notifications"""
    try:
        self.notification_service.send(
            user_id=transaction.user_id,
            type='payment_success',
            data={'transaction_id': transaction.id}
        )
    except NotificationError as e:
        # Log but don't fail transaction
        logger.error(f"Notification failed: {e}")
'''

print("Refactoring applied:")
print("  ✓ Extracted _validate_payment_data()")
print("  ✓ Extracted _execute_payment_transaction()")
print("  ✓ Extracted _send_payment_notifications()")
print("  ✓ Simplified main function")
print("  ✓ Added type hints")
print("  ✓ Improved error handling")
print()
```

---

## Phase 5: Verify Tests Pass

```python
print(f"=== Post-Refactoring Test Run ===\n")

print("Running tests after refactoring...")

try:
    result = subprocess.run(
        ['python', '-m', 'pytest', 'tests/test_payment_processor.py', '-v'],
        capture_output=True,
        text=True,
        cwd=project_root,
        timeout=60
    )

    passed = result.stdout.count(' PASSED')
    failed = result.stdout.count(' FAILED')

    print(f"Post-Refactoring Results:")
    print(f"  Passed: {passed}")
    print(f"  Failed: {failed}")
    print()

    if failed > 0:
        print("✗ Tests failing after refactoring!")
        print("  Rolling back changes...")
        print()
    else:
        print("✓ All tests still passing")
        print("  Refactoring successful!")
        print()

except (subprocess.TimeoutExpired, FileNotFoundError):
    pass
```

---

## Phase 6: Measure Improvements

```python
print(f"=== Improvement Metrics ===\n")

before = {
    'complexity': 28,
    'lines': 187,
    'functions': 1,
    'maintainability': 32
}

after = {
    'complexity': 11,
    'lines': 120,
    'functions': 4,
    'maintainability': 68
}

improvements = {
    'complexity': ((before['complexity'] - after['complexity']) / before['complexity'] * 100),
    'lines': ((before['lines'] - after['lines']) / before['lines'] * 100),
    'maintainability': ((after['maintainability'] - before['maintainability']) / before['maintainability'] * 100)
}

print("Before → After:")
print(f"  Complexity: {before['complexity']} → {after['complexity']} ({improvements['complexity']:.0f}% reduction)")
print(f"  Lines: {before['lines']} → {after['lines']} ({improvements['lines']:.0f}% reduction)")
print(f"  Functions: {before['functions']} → {after['functions']}")
print(f"  Maintainability: {before['maintainability']} → {after['maintainability']} ({improvements['maintainability']:.0f}% improvement)")
print()

print("Benefits:")
print("  ✓ Easier to understand")
print("  ✓ Easier to test")
print("  ✓ Easier to modify")
print("  ✓ Better error handling")
print()
```

---

## Phase 7: Summary

```python
print(f"=== Refactoring Summary ===\n")

print("Target: process_payment()")
print()
print("Completed:")
print("  ✓ Analysis and planning")
print("  ✓ Baseline test run (all passing)")
print("  ✓ Refactoring execution")
print("  ✓ Verification (all tests pass)")
print("  ✓ Metrics improvement")
print()
print("Result: ✓✓✓ Successful refactoring")
print()
print("Next Steps:")
print("  1. Code review")
print("  2. Commit changes")
print("  3. Deploy to staging")
print()
```

---

## Output Example

```
=== Refactoring Analysis ===

Target: src/services/payment_processor.py::process_payment

Current State:
  Complexity: 28
  Lines: 187

Issues:
  - High cyclomatic complexity (28)
  - Too many responsibilities
  - Nested conditionals (5 levels)
  - No error handling

=== Refactoring Plan ===

## Strategy: Extract Method + Simplify Conditionals

### Step 1: Extract payment validation
- Extract to validate_payment_data()
- Reduces complexity by 5

...

=== Baseline Test Run ===

Running existing tests...
Baseline Results:
  Passed: 23
  Failed: 0

✓ All tests passing - safe to refactor

=== Refactoring Execution ===

Refactoring applied:
  ✓ Extracted _validate_payment_data()
  ✓ Extracted _execute_payment_transaction()
  ✓ Extracted _send_payment_notifications()
  ✓ Simplified main function
  ✓ Added type hints
  ✓ Improved error handling

=== Post-Refactoring Test Run ===

Running tests after refactoring...
Post-Refactoring Results:
  Passed: 23
  Failed: 0

✓ All tests still passing
  Refactoring successful!

=== Improvement Metrics ===

Before → After:
  Complexity: 28 → 11 (61% reduction)
  Lines: 187 → 120 (36% reduction)
  Functions: 1 → 4
  Maintainability: 32 → 68 (113% improvement)

Benefits:
  ✓ Easier to understand
  ✓ Easier to test
  ✓ Easier to modify
  ✓ Better error handling

=== Refactoring Summary ===

Target: process_payment()

Completed:
  ✓ Analysis and planning
  ✓ Baseline test run (all passing)
  ✓ Refactoring execution
  ✓ Verification (all tests pass)
  ✓ Metrics improvement

Result: ✓✓✓ Successful refactoring
```

---

**Refactoring Philosophy:** Refactoring without tests is just rearranging deck chairs. Test first, refactor second, verify always.
