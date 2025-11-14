---
id: P_TEST_COVERAGE
title: Test Coverage Targets
category: testing
severity: high
weight: 8
applicability:
  project_types: ['all']
  languages: ['all']
---

# P_TEST_COVERAGE: Test Coverage Targets 🔴

**Severity**: High

Maintain minimum 80% line coverage overall, 100% coverage for critical paths (payment, authentication, security). Coverage metrics ensure code is tested before deployment.

**Enforcement**: MUST

**Project Types**: all
**Languages**: all

---

## Why

### The Problem

**Low test coverage allows bugs to reach production:**

- **Untested Code Paths** - Missing tests mean bugs in uncovered code discovered in production
- **Regression Risk** - Refactoring untested code breaks functionality without warning
- **No Safety Net** - Can't confidently change code without tests
- **Hidden Logic Errors** - Edge cases and error paths untested, fail in production
- **Integration Gaps** - Component interactions untested until production

### Business Value

- **Reduced production bugs** - 80%+ coverage correlates with 60% fewer production incidents
- **Confident deployments** - High coverage enables continuous deployment
- **Faster development** - Tests catch issues immediately, not after deployment
- **Lower debugging costs** - Issues caught by tests cheaper to fix than production bugs

### Technical Benefits

- **Refactoring safety** - Tests verify behavior preserved during changes
- **Regression prevention** - Tests catch when changes break existing functionality
- **Documentation** - Tests document expected behavior
- **Code quality signal** - Hard-to-test code often indicates design problems

### Industry Evidence

- **Microsoft Research** - Codebases with >80% coverage have 40-50% fewer production bugs
- **Google Testing** - Critical path coverage of 100% required for production code
- **Industry Standard** - 80% coverage baseline, 100% for security/payment code
- **Developer Productivity** - Teams with high coverage ship 2x faster (confident refactoring)

---

## How

### Core Techniques

**1. Set Coverage Targets and Enforce in CI**

```yaml
# .github/workflows/test.yml
- name: Run tests with coverage
  run: pytest --cov=src --cov-report=term --cov-fail-under=80

# ✅ CI fails if coverage drops below 80%
```

**2. Measure Coverage by Component**

```bash
# pytest.ini or pyproject.toml
[tool.coverage.run]
source = ["src"]
omit = [
    "*/tests/*",
    "*/migrations/*",
    "*/__init__.py",
]

[tool.coverage.report]
# Fail if coverage < 80%
fail_under = 80

# Show missing lines
show_missing = true

# Report by file
precision = 2

[tool.coverage.html]
directory = "htmlcov"
```

**3. 100% Coverage for Critical Paths**

```python
# ✅ GOOD: Critical payment code has 100% coverage

def process_payment(amount: Decimal, card_token: str) -> PaymentResult:
    """Process payment - CRITICAL PATH, must have 100% test coverage."""

    # Validate amount
    if amount <= 0:
        raise ValueError("Amount must be positive")

    # Charge card
    try:
        charge = stripe.Charge.create(
            amount=int(amount * 100),  # Convert to cents
            currency="usd",
            source=card_token
        )
    except stripe.CardError as e:
        return PaymentResult(success=False, error=str(e))
    except stripe.StripeError as e:
        logger.error(f"Stripe error: {e}")
        raise

    return PaymentResult(success=True, charge_id=charge.id)

# Tests covering all paths (100% coverage):
class TestProcessPayment:
    def test_successful_payment(self, mock_stripe):
        result = process_payment(Decimal("100.00"), "tok_visa")
        assert result.success is True

    def test_zero_amount_raises_error(self):
        with pytest.raises(ValueError, match="must be positive"):
            process_payment(Decimal("0"), "tok_visa")

    def test_negative_amount_raises_error(self):
        with pytest.raises(ValueError, match="must be positive"):
            process_payment(Decimal("-10"), "tok_visa")

    def test_card_error_handled(self, mock_stripe_card_error):
        result = process_payment(Decimal("100.00"), "tok_declined")
        assert result.success is False
        assert "declined" in result.error

    def test_stripe_error_logged_and_raised(self, mock_stripe_error):
        with pytest.raises(stripe.StripeError):
            process_payment(Decimal("100.00"), "tok_error")

# ✅ Result: 100% coverage on critical payment code
```

**4. Track Coverage Trends Over Time**

```yaml
# .github/workflows/coverage-report.yml
- name: Generate coverage badge
  run: |
    coverage run -m pytest
    coverage report
    coverage-badge -o coverage.svg

- name: Comment coverage on PR
  run: |
    coverage report --format=markdown >> $GITHUB_STEP_SUMMARY
```

**5. Identify Untested Code**

```bash
# Generate HTML coverage report
pytest --cov=src --cov-report=html

# Open htmlcov/index.html
# Red lines = not covered
# Green lines = covered

# Find files with <80% coverage
coverage report --skip-covered --sort=cover
```

**6. Exclude Non-Testable Code**

```python
# ✅ GOOD: Exclude type checking blocks from coverage

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    # Import only for type checking, not runtime
    from models import User

# ✅ Exclude unreachable defensive code
def process(data):
    if data is None:
        raise ValueError("Data required")

    # Process data
    ...

    # Defensive programming: should never happen
    if some_impossible_condition:  # pragma: no cover
        raise RuntimeError("Impossible state reached")
```

---

### Implementation Patterns

#### ✅ Good: High Coverage with Quality Tests

```python
# Function with comprehensive test coverage

def calculate_tax(amount: Decimal, state: str) -> Decimal:
    """Calculate sales tax based on state."""
    tax_rates = {
        "CA": Decimal("0.0725"),
        "NY": Decimal("0.08"),
        "TX": Decimal("0.0625"),
    }

    if state not in tax_rates:
        raise ValueError(f"Unknown state: {state}")

    return amount * tax_rates[state]

# Tests achieving 100% coverage
def test_calculate_tax_california():
    assert calculate_tax(Decimal("100"), "CA") == Decimal("7.25")

def test_calculate_tax_new_york():
    assert calculate_tax(Decimal("100"), "NY") == Decimal("8.00")

def test_calculate_tax_texas():
    assert calculate_tax(Decimal("100"), "TX") == Decimal("6.25")

def test_calculate_tax_unknown_state():
    with pytest.raises(ValueError, match="Unknown state: ZZ"):
        calculate_tax(Decimal("100"), "ZZ")

# ✅ Result: 100% line coverage, all branches tested
```

---

#### ❌ Bad: High Coverage, Low Quality Tests

```python
# ❌ BAD: 100% coverage but tests don't verify behavior

def transfer_funds(from_account, to_account, amount):
    if amount <= 0:
        raise ValueError("Amount must be positive")

    if from_account.balance < amount:
        raise ValueError("Insufficient funds")

    from_account.balance -= amount
    to_account.balance += amount
    return True

# Bad test: Achieves coverage but doesn't verify correctness
def test_transfer_funds_bad():
    from_acc = Account(balance=100)
    to_acc = Account(balance=50)
    result = transfer_funds(from_acc, to_acc, 30)
    # ❌ Doesn't verify balances changed correctly!
    assert result is True  # Weak assertion

# ✅ GOOD: Coverage + correctness verification
def test_transfer_funds_good():
    from_acc = Account(balance=100)
    to_acc = Account(balance=50)
    result = transfer_funds(from_acc, to_acc, 30)
    # ✅ Verifies balances changed correctly
    assert from_acc.balance == Decimal("70")
    assert to_acc.balance == Decimal("80")
    assert result is True
```

---

## Anti-Patterns

### ❌ Anti-Pattern 1: Coverage Without Quality

**Problem**: Achieving high coverage with weak tests that don't verify behavior.

```python
# ❌ BAD: High coverage, low quality
def test_everything():
    calculate_discount(100, 0.2)  # Covers line but doesn't assert!
    process_order(order_data)     # Covers line but no verification!
    # Coverage: 100%, Value: 0%

# ✅ GOOD: Coverage + verification
def test_calculate_discount():
    result = calculate_discount(100, 0.2)
    assert result == 80.0  # Verifies correct result

def test_process_order():
    order = process_order(order_data)
    assert order.status == "processed"
    assert order.total == expected_total
```

**Impact**: False confidence - code "tested" but bugs slip through

---

### ❌ Anti-Pattern 2: Ignoring Coverage Gaps

**Problem**: Not investigating why certain code isn't covered.

```python
# ❌ BAD: Code not covered, no investigation

def process_refund(order):
    if order.status != "paid":
        return RefundResult(success=False, error="Order not paid")

    # This branch never covered by tests - but why?
    if order.payment_method == "crypto":  # 0% coverage
        return process_crypto_refund(order)  # Untested!

    return process_standard_refund(order)

# ✅ GOOD: Investigate coverage gap, add test or remove dead code
def test_crypto_refund():
    order = Order(status="paid", payment_method="crypto")
    result = process_refund(order)
    # Now covered!
```

**Impact**: Untested code paths harbor bugs

---

## Implementation Checklist

### Coverage Setup

- [ ] **Enable coverage tracking** - Use pytest-cov (Python), nyc (Node.js)
- [ ] **Set minimum threshold** - 80% overall, 100% for critical paths
- [ ] **CI enforcement** - Fail builds if coverage drops
- [ ] **Exclude test code** - Don't measure coverage of tests themselves
- [ ] **HTML reports** - Generate readable coverage reports

### Coverage Targets

- [ ] **Overall: 80%** - Minimum across entire codebase
- [ ] **Critical paths: 100%** - Payment, authentication, security
- [ ] **New code: 90%+** - All new code well-tested
- [ ] **Core business logic: 95%+** - High coverage on main functionality

### Coverage Monitoring

- [ ] **Track trends** - Monitor coverage over time
- [ ] **PR comments** - Show coverage diff in pull requests
- [ ] **Coverage badge** - Display current coverage in README
- [ ] **Alert on drops** - Notify when coverage decreases

---

## Cross-References

**Related Principles:**
- **P_TEST_PYRAMID** - Coverage should follow pyramid ratio
- **P_TEST_ISOLATION** - Isolated tests improve coverage accuracy
- **P_CI_GATES** - Coverage checked in CI gates
- **U_TEST_FIRST** - TDD naturally achieves high coverage

**Workflow Integration:**
- Write tests for all new code (90%+ coverage)
- CI fails if coverage drops below 80%
- Review coverage reports for gaps
- 100% coverage required for critical paths before merge

---

## Summary

**Test Coverage Targets** means maintaining minimum 80% line coverage overall, 100% for critical paths. Coverage metrics ensure code tested before deployment.

**Core Rules:**
- **80% minimum** - Overall codebase coverage threshold
- **100% critical paths** - Payment, auth, security fully tested
- **CI enforcement** - Build fails if coverage drops
- **Quality over quantity** - Coverage with strong assertions
- **Investigate gaps** - Understand why code isn't covered

**Remember**: "Coverage measures what's tested, not quality of tests. Aim for 80%+ with strong assertions."

**Impact**: 60% fewer production bugs, confident refactoring, faster development, lower debugging costs.

---

**Coverage Tools:**
- **Python**: `pytest --cov=src --cov-report=term`
- **JavaScript**: `nyc npm test` or `jest --coverage`
- **Go**: `go test -cover ./...`
- **Java**: JaCoCo, Cobertura

**Coverage Configuration (Python):**
```toml
[tool.coverage.run]
source = ["src"]
omit = ["*/tests/*", "*/migrations/*"]

[tool.coverage.report]
fail_under = 80
show_missing = true
skip_covered = false

[tool.coverage.html]
directory = "htmlcov"
```

**CI Integration:**
```yaml
- run: pytest --cov=src --cov-fail-under=80
- run: coverage xml
- uses: codecov/codecov-action@v3
```
