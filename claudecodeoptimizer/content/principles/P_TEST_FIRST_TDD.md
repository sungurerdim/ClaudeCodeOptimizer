---
id: U_TEST_FIRST
title: Test-First Development
category: universal
severity: high
weight: 9
enforcement: SHOULD
applicability:
  project_types: ['all']
  languages: ['all']
---

# U_TEST_FIRST: Test-First Development

**Severity**: High

Write failing test FIRST, then implement feature, then verify test passes.

**Enforcement**: SHOULD

---

## Why

- **Tests written after** validate implementation, not behavior
- **Refactoring fear** - can't change code safely without tests
- **Over-engineering** - build more than needed without test constraints
- **TDD ensures** tests actually work (fail first), drives better design, prevents regression

### The TDD Cycle (Red-Green-Refactor)

```
1. RED: Write failing test (defines requirement)
   ↓
2. GREEN: Write minimal code to pass test (make it work)
   ↓
3. REFACTOR: Improve code quality (make it clean)
   ↓
   Repeat
```

## Implementation Example

### Step 1: RED - Write Failing Test

```python
import pytest
from auth import <function_name>

def test_authenticate_user_with_valid_credentials():
    # Arrange
    email = "user@example.com"
    password = "<test-password>"

    # Act
    result = <function_name>(email, password)

    # Assert
    assert result.success is True
    assert result.user.email == email
    assert result.user.is_authenticated is True

# Run test - SHOULD FAIL (function doesn't exist yet)
# $ pytest tests/test_auth.py
# FAILED - ImportError: cannot import name '<function_name>'
```

**Why it must fail:**
- Proves test actually works (not false positive)
- Verifies test setup
- Ensures you're testing the right thing

### Step 2: GREEN - Write Minimal Implementation

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class AuthResult:
    success: bool
    user: Optional['User'] = None

@dataclass
class User:
    email: str
    is_authenticated: bool = False

def <function_name>(email: str, password: str) -> AuthResult:
    # Minimal implementation - just pass the test
    if email and password:
        user = User(email=email, is_authenticated=True)
        return AuthResult(success=True, user=user)
    return AuthResult(success=False)

# Run test - SHOULD PASS
# $ pytest tests/test_auth.py
# PASSED
```

### Step 3: REFACTOR - Improve Quality

```python
import bcrypt
from database import get_user_by_email

def <function_name>(email: str, password: str) -> AuthResult:
    if not email or not password:
        return AuthResult(success=False)

    user = get_user_by_email(email)
    if not user:
        return AuthResult(success=False)

    if not bcrypt.checkpw(password.encode(), user.password_hash):
        return AuthResult(success=False)

    user.is_authenticated = True
    return AuthResult(success=True, user=user)

# Run test again - STILL PASSES (behavior preserved)
```

---

## Anti-Patterns

### ❌ Code-First, Test-Later

```python
# ❌ BAD: Write implementation first
def <function_name>(email, password):
    # ... 200 lines of complex logic written without tests
    return result

# Then try to write tests (too late!)
def test_<function_name>():
    # Hard to test - tightly coupled, tests implementation not behavior
```

**Problems:**
- Tests validate implementation, not requirements
- Hard to test (wasn't designed for testability)
- No guarantee tests fail when they should

### ❌ Testing Implementation Details

```python
# ❌ BAD: Test internals (brittle)
def test_authenticate_user_implementation():
    auth = AuthService()
    assert auth._hash_password("test") == auth._stored_hash  # Breaks on refactor

# ✅ GOOD: Test behavior (robust)
def test_authenticate_user_behavior():
    result = <function_name>("user@test.com", "password")
    assert result.success is True  # Tests observable behavior
```

### ❌ Skip RED Step

```python
# ❌ BAD: Write passing test immediately
def test_addition():
    assert 2 + 2 == 4  # Already passes, didn't fail first!

# ✅ GOOD: Verify test fails first
def test_addition():
    assert add(2, 2) == 4  # Fails first (add() doesn't exist)
```

---

## Best Practices

### Test One Thing at a Time

```python
# ✅ GOOD: Focused tests
def test_user_creation_with_valid_data():
    user = create_user("John", "john@example.com")
    assert user.name == "John"

def test_user_creation_rejects_invalid_email():
    with pytest.raises(ValueError):
        create_user("John", "invalid-email")

# ❌ BAD: Tests multiple things
def test_user_everything():
    user = create_user("John", "john@example.com")
    assert user.name == "John"
    assert user.id is not None
    # ... 20 more assertions (which one failed?)
```

### Follow AAA Pattern (Arrange-Act-Assert)

```python
def test_transfer_funds():
    # Arrange - Set up test data
    sender = Account(balance=100.0)
    receiver = Account(balance=50.0)

    # Act - Perform the action
    result = transfer_funds(sender, receiver, amount=30.0)

    # Assert - Verify results
    assert result.success is True
    assert sender.balance == 70.0
    assert receiver.balance == 80.0
```

### Test Behavior, Not Implementation

```python
# ❌ BAD: Tests implementation details
def test_uses_quicksort():
    sorter = Sorter()
    assert sorter.algorithm == "quicksort"  # Brittle!

# ✅ GOOD: Tests observable behavior
def test_sorts_numbers():
    result = sort_numbers([3, 1, 2])
    assert result == [1, 2, 3]  # Don't care how, just that it works
```

---

## TDD for Different Scenarios

### Bug Fix

```python
# Step 1: Write failing test that reproduces bug
def test_division_by_zero_raises_error():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)  # Currently doesn't raise, returns None

# Step 2: Fix the bug
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b

# Step 3: Test passes - bug fixed and won't regress
```

### Refactoring

```python
# Already have tests (written test-first earlier)
def test_calculate_total():
    items = [Item(price=10), Item(price=20)]
    assert calculate_total(items) == 30

# Refactor safely (tests ensure behavior preserved)
# Before:
def calculate_total(items):
    total = 0
    for item in items:
        total += item.price
    return total

# After:
def calculate_total(items):
    return sum(item.price for item in items)

# Test still passes - refactoring safe!
```

---

## Implementation Checklist

- [ ] **Before writing code:** Write failing test first
- [ ] **Verify test fails:** Run test, confirm it fails for right reason
- [ ] **Write minimal code:** Just enough to pass test
- [ ] **Verify test passes:** Run test, confirm it passes
- [ ] **Refactor:** Improve code quality while keeping tests green
- [ ] **Repeat cycle:** Next feature/behavior

---

## Common Pitfalls

1. **Writing tests after code** - Defeats the purpose of TDD
2. **Skipping RED step** - Can't verify test actually works
3. **Testing implementation details** - Makes tests brittle
4. **Large, slow tests** - Slows down feedback loop
5. **Ignoring failing tests** - "I'll fix it later" never happens

---

## Summary

**Test-First Development (TDD)** means writing failing tests BEFORE implementation. This ensures tests actually work, drives better design, and provides regression safety.

**The Cycle: RED → GREEN → REFACTOR → Repeat**

**Core Rule**: No production code without a failing test first.
