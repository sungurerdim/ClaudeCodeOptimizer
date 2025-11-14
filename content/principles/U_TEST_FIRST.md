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

# U_TEST_FIRST: Test-First Development 🔴

**Severity**: High

Write failing test FIRST, then implement feature, then verify test passes.

**Enforcement**: SHOULD

**Project Types**: all
**Languages**: all

---

## Why

### The Problem
- **Code without tests** is legacy code (Michael Feathers)
- **Tests written after** often test implementation, not behavior
- **Unclear requirements** lead to wrong implementations
- **Refactoring fear** - can't change code without breaking it
- **Regression bugs** - changes break existing functionality
- **Over-engineering** - build more than needed

### Business Value
- **80% fewer production bugs** (IBM research on TDD)
- **40-50% less debugging time** (Microsoft TDD study)
- **Better design** - testable code is modular code
- **Faster onboarding** - tests document expected behavior
- **Confident refactoring** - tests verify behavior preservation
- **Lower maintenance costs** - regression prevention

### Technical Benefits
- **Clarity of requirements** - test forces you to define "done"
- **Better API design** - writing tests first improves interfaces
- **Immediate feedback** - know instantly if implementation works
- **Regression safety** - prevent old bugs from returning
- **Living documentation** - tests show how code should work
- **Forces modularity** - untestable code gets refactored

### Industry Evidence
- **Kent Beck (TDD creator)** - "I'm not a great programmer; I'm just a good programmer with great habits"
- **Google Testing Blog** - Teams using TDD have 40-90% fewer defects
- **IBM Research** - TDD reduces defect density by 40-90%
- **Microsoft Study** - TDD increases initial dev time by 15% but reduces debugging by 50%
- **ThoughtWorks Tech Radar** - TDD is "Adopt" status

---

## How

### The TDD Cycle (Red-Green-Refactor)

```
1. 🔴 RED: Write failing test (defines requirement)
   ↓
2. 🟢 GREEN: Write minimal code to pass test (make it work)
   ↓
3. 🔵 REFACTOR: Improve code quality (make it clean)
   ↓
   Repeat
```

### Implementation Workflow

#### Step 1: 🔴 RED - Write Failing Test
```python
# ALWAYS write the test FIRST
import pytest
from auth import authenticate_user

def test_authenticate_user_with_valid_credentials():
    # Arrange
    email = "user@example.com"
    password = "secure_password"

    # Act
    result = authenticate_user(email, password)

    # Assert
    assert result.success is True
    assert result.user.email == email
    assert result.user.is_authenticated is True

# Run test - SHOULD FAIL (function doesn't exist yet)
# $ pytest tests/test_auth.py::test_authenticate_user_with_valid_credentials
# FAILED - ImportError: cannot import name 'authenticate_user'
```

**Why it must fail:**
- Proves test actually works (not false positive)
- Verifies test runner configuration
- Ensures you're testing the right thing

#### Step 2: 🟢 GREEN - Write Minimal Implementation
```python
# auth.py - Write SIMPLEST code to pass test
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

def authenticate_user(email: str, password: str) -> AuthResult:
    # Minimal implementation - just pass the test
    if email and password:
        user = User(email=email, is_authenticated=True)
        return AuthResult(success=True, user=user)
    return AuthResult(success=False)

# Run test - SHOULD PASS
# $ pytest tests/test_auth.py::test_authenticate_user_with_valid_credentials
# PASSED
```

**Why minimal:**
- Avoid over-engineering
- Focus on requirements (test defines them)
- Easier to refactor simple code

#### Step 3: 🔵 REFACTOR - Improve Quality
```python
# Now add proper implementation with database, hashing, etc.
import bcrypt
from database import get_user_by_email

def authenticate_user(email: str, password: str) -> AuthResult:
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
# $ pytest tests/test_auth.py::test_authenticate_user_with_valid_credentials
# PASSED
```

**Why refactor:**
- Tests guarantee behavior preservation
- Safe to improve code quality
- Incrementally evolve design

---

## Anti-Patterns

### ❌ Anti-Pattern 1: Code-First, Test-Later
```python
# ❌ BAD: Write implementation first
def authenticate_user(email, password):
    # ... 200 lines of complex logic
    # ... written without tests
    return result

# Then try to write tests (too late!)
def test_authenticate_user():
    # Hard to test - tightly coupled, many dependencies
    # Tests become brittle, testing implementation not behavior
```

**Problems:**
- Tests validate implementation, not requirements
- Hard to test (wasn't designed for testability)
- Misses edge cases discovered during test writing
- No guarantee tests actually fail when they should

### ❌ Anti-Pattern 2: Testing Implementation Details
```python
# ❌ BAD: Test internals (brittle)
def test_authenticate_user_implementation():
    auth = AuthService()
    # Testing internal method names, private state
    assert auth._hash_password("test") == auth._stored_hash
    assert auth._check_cache() == True

# ✅ GOOD: Test behavior (robust)
def test_authenticate_user_behavior():
    result = authenticate_user("user@test.com", "password")
    assert result.success is True  # Test observable behavior
```

### ❌ Anti-Pattern 3: One Test After Everything
```python
# ❌ BAD: Write all code, then one big test
def process_order(order):
    # ... 500 lines of complex business logic
    pass

def test_everything():
    # One massive test trying to cover everything
    # Hard to debug, slow, brittle
    assert process_order(order).total == expected_total
```

**Problems:**
- Can't identify which part fails
- Encourages complex, untestable code
- Misses edge cases
- Violates TDD cycle

### ❌ Anti-Pattern 4: Skip RED Step
```python
# ❌ BAD: Write passing test immediately
def test_addition():
    assert 2 + 2 == 4  # Already passes, didn't fail first!

# ✅ GOOD: Verify test fails first
def test_addition():
    assert add(2, 2) == 4  # Fails first (add() doesn't exist)
```

**Why RED matters:**
- Proves test actually works
- Prevents false positives
- Validates test setup

---

## Examples by Language

### Python (pytest)
```python
# Step 1: RED - Write failing test
def test_calculate_discount():
    product = Product(price=100.0)
    discount = Discount(percentage=10)

    result = calculate_discount(product, discount)

    assert result == 90.0

# Run: pytest -v
# FAILED: NameError: name 'calculate_discount' is not defined ✓

# Step 2: GREEN - Minimal implementation
def calculate_discount(product: Product, discount: Discount) -> float:
    return product.price * (1 - discount.percentage / 100)

# Run: pytest -v
# PASSED ✓

# Step 3: REFACTOR - Add validation, edge cases
def calculate_discount(product: Product, discount: Discount) -> float:
    if product.price < 0:
        raise ValueError("Price cannot be negative")
    if not (0 <= discount.percentage <= 100):
        raise ValueError("Discount must be between 0 and 100")

    return product.price * (1 - discount.percentage / 100)

# Run: pytest -v
# PASSED ✓ (behavior preserved, quality improved)
```

### JavaScript (Jest)
```javascript
// Step 1: RED - Write failing test
describe('User Registration', () => {
  test('creates new user with hashed password', async () => {
    const userData = { email: 'test@example.com', password: 'secret123' };

    const user = await registerUser(userData);

    expect(user.email).toBe(userData.email);
    expect(user.password).not.toBe(userData.password); // Should be hashed
    expect(user.id).toBeDefined();
  });
});

// Run: npm test
// FAILED: ReferenceError: registerUser is not defined ✓

// Step 2: GREEN - Minimal implementation
async function registerUser(userData) {
  const hashedPassword = await bcrypt.hash(userData.password, 10);
  const user = {
    id: uuid(),
    email: userData.email,
    password: hashedPassword,
  };
  return user;
}

// Run: npm test
// PASSED ✓
```

### Go (testing package)
```go
// Step 1: RED - Write failing test
func TestValidateEmail(t *testing.T) {
    tests := []struct {
        email string
        want  bool
    }{
        {"valid@example.com", true},
        {"invalid", false},
        {"@example.com", false},
    }

    for _, tt := range tests {
        got := ValidateEmail(tt.email)
        if got != tt.want {
            t.Errorf("ValidateEmail(%q) = %v, want %v", tt.email, got, tt.want)
        }
    }
}

// Run: go test
// FAILED: undefined: ValidateEmail ✓

// Step 2: GREEN - Minimal implementation
func ValidateEmail(email string) bool {
    return strings.Contains(email, "@") && strings.Contains(email, ".")
}

// Run: go test
// PASSED ✓

// Step 3: REFACTOR - Use proper regex
func ValidateEmail(email string) bool {
    regex := regexp.MustCompile(`^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`)
    return regex.MatchString(email)
}

// Run: go test
// PASSED ✓
```

---

## TDD Best Practices

### 1. Test One Thing at a Time
```python
# ✅ GOOD: Focused tests
def test_user_creation_with_valid_data():
    user = create_user("John", "john@example.com")
    assert user.name == "John"

def test_user_creation_rejects_invalid_email():
    with pytest.raises(ValueError):
        create_user("John", "invalid-email")

def test_user_creation_generates_unique_id():
    user1 = create_user("John", "john@example.com")
    user2 = create_user("Jane", "jane@example.com")
    assert user1.id != user2.id

# ❌ BAD: Tests multiple things
def test_user_everything():
    user = create_user("John", "john@example.com")
    assert user.name == "John"
    assert user.id is not None
    assert user.email == "john@example.com"
    # ... 20 more assertions (which one failed?)
```

### 2. Follow AAA Pattern (Arrange-Act-Assert)
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

### 3. Test Behavior, Not Implementation
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

### 4. Write Simplest Test First
```python
# ✅ Start with simplest case
def test_sum_two_numbers():
    assert add(2, 3) == 5

# Then add complexity
def test_sum_with_negative_numbers():
    assert add(-2, 3) == 1

def test_sum_with_floats():
    assert add(2.5, 3.5) == 6.0

def test_sum_with_large_numbers():
    assert add(10**100, 10**100) == 2 * 10**100
```

### 5. Keep Tests Fast
```python
# ✅ GOOD: Fast unit tests (< 10ms)
def test_calculate_tax():
    assert calculate_tax(100.0, rate=0.2) == 20.0

# ❌ BAD: Slow tests (database, network, sleep)
def test_save_user():
    user = User(name="John")
    db.connect()  # Slow!
    db.save(user)  # Slow!
    time.sleep(1)  # Very slow!
    assert db.get_user(user.id) is not None
```

**Solution: Use mocks/fakes for unit tests**
```python
# ✅ GOOD: Mock external dependencies
def test_save_user_fast(mock_db):
    user = User(name="John")
    save_user(user, db=mock_db)
    mock_db.save.assert_called_once_with(user)
```

---

## TDD for Different Scenarios

### Scenario 1: New Feature
```python
# Step 1: Write test for new feature
def test_user_can_update_profile():
    user = User(name="John", email="john@example.com")

    updated_user = update_profile(user, name="Jane")

    assert updated_user.name == "Jane"
    assert updated_user.email == "john@example.com"  # Unchanged

# Step 2: Implement feature
# Step 3: Verify test passes
```

### Scenario 2: Bug Fix
```python
# Step 1: Write failing test that reproduces bug
def test_division_by_zero_raises_error():
    # This test reveals the bug
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)  # Currently doesn't raise, returns None

# Step 2: Fix the bug
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b

# Step 3: Test passes - bug fixed and won't regress
```

### Scenario 3: Refactoring
```python
# Already have tests (written test-first earlier)
def test_calculate_total():
    items = [Item(price=10), Item(price=20)]
    assert calculate_total(items) == 30

# Refactor implementation (tests ensure behavior preserved)
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

## Metrics and Monitoring

### Key Indicators
- **Test coverage:** % of code covered by tests (aim for 80%+)
- **Test failure rate:** % of tests that fail (should be low in main branch)
- **TDD adoption:** % of features developed test-first
- **Time to feedback:** How quickly tests run (< 10s for unit tests)

### Success Criteria
- All new features have tests written first
- Tests fail before implementation (verify RED step)
- Tests pass after implementation (GREEN step)
- Code coverage maintained or improved
- Zero production bugs that existing tests should have caught

---

## Cross-References

**Related Principles:**
- **U_EVIDENCE_BASED** - Tests provide evidence of correctness
- **U_FAIL_FAST** - Tests fail immediately on incorrect behavior
- **U_ROOT_CAUSE_ANALYSIS** - Failing tests pinpoint exact issue
- **U_INTEGRATION_CHECK** - Integration tests verify system behavior
- **P_TEST_COVERAGE** - Measure test completeness (aim 80%+)
- **P_TEST_PYRAMID** - Balance unit/integration/e2e tests
- **P_TEST_ISOLATION** - Tests should be independent
- **P_CI_GATES** - Automated test runs on every commit

**Enables:**
- **U_NO_OVERENGINEERING** - Tests prevent building unnecessary features
- **U_CHANGE_VERIFICATION** - Tests verify changes don't break existing functionality

---

## Industry Standards Alignment

- **Kent Beck (TDD Creator)** - Original TDD methodology (Red-Green-Refactor)
- **Uncle Bob (Clean Code)** - "The only way to go fast is to go well"
- **Martin Fowler** - Refactoring with test safety net
- **Google Testing Blog** - Advocates for test-first development
- **XP (Extreme Programming)** - TDD is a core practice
- **BDD (Behavior-Driven Development)** - Evolution of TDD with Given-When-Then
- **ISO/IEC 29119 (Software Testing)** - Test design before implementation

---

## Tools and Frameworks

### Python
- **pytest** - Industry standard testing framework
- **unittest** - Built-in testing framework
- **hypothesis** - Property-based testing
- **coverage.py** - Test coverage measurement

### JavaScript/TypeScript
- **Jest** - Zero-config testing framework
- **Vitest** - Fast unit testing (Vite ecosystem)
- **Mocha** - Flexible testing framework
- **Chai** - BDD/TDD assertion library

### Go
- **testing** - Built-in testing package
- **testify** - Additional assertions and mocking
- **gomock** - Mocking framework

### Rust
- **cargo test** - Built-in test runner
- **proptest** - Property-based testing
- **mockall** - Mocking library

---

## Common Pitfalls

1. **Writing tests after code** - Defeats the purpose of TDD
2. **Skipping RED step** - Can't verify test actually works
3. **Testing implementation details** - Makes tests brittle
4. **Large, slow tests** - Slows down feedback loop
5. **Too much mocking** - Tests become disconnected from reality
6. **Ignoring failing tests** - "I'll fix it later" never happens
7. **100% coverage obsession** - Focus on valuable tests, not just coverage number

---

## Migration Strategy

### Phase 1: Start with New Features (Week 1-2)
- All NEW features use TDD from now on
- Don't retrofit existing code yet
- Build TDD habit on greenfield work

### Phase 2: Bug Fixes Test-First (Week 3-4)
- Every bug fix starts with failing test
- Test reproduces bug, then fix makes it pass
- Prevents regression

### Phase 3: Refactoring with Tests (Week 5+)
- Add tests to existing code before refactoring
- Use tests as safety net for improvements
- Gradually increase coverage

---

## Summary

**Test-First Development (TDD)** means writing failing tests BEFORE implementation. This ensures tests actually work, drives better design, and provides regression safety.

**The Cycle: 🔴 RED → 🟢 GREEN → 🔵 REFACTOR → Repeat**

**Core Rule**: No production code without a failing test first.

**Remember**: "If it's not tested first, it's not TDD."

**Impact**: 80% fewer production bugs, 50% less debugging time, confident refactoring, better design.
