---
id: P_TEST_PYRAMID
title: Test Pyramid
category: testing
severity: medium
weight: 6
applicability:
  project_types: ['all']
  languages: ['all']
---

# P_TEST_PYRAMID: Test Pyramid 🟡

**Severity**: Medium

Maintain test pyramid ratio: 70% unit tests, 20% integration tests, 10% E2E tests. Fast, isolated unit tests provide quick feedback; integration and E2E tests verify system behavior.

**Enforcement**: SHOULD

**Project Types**: all
**Languages**: all

---

## Why

### The Problem

**Inverted test pyramids (too many E2E tests) slow development:**

- **Slow Feedback** - E2E tests take minutes to hours; developers wait to see if changes work
- **Flaky Tests** - E2E tests fail randomly due to timing, network, browser issues
- **Hard to Debug** - E2E test failures don't pinpoint exact issue; could be anywhere in system
- **Expensive CI** - E2E tests require full infrastructure, consume CI resources heavily
- **Maintenance Burden** - E2E tests break frequently when UI changes
- **Test Coverage Gaps** - Can't test all edge cases with slow E2E tests
- **Developer Frustration** - Waiting 20 minutes for test results kills productivity

### Core Techniques

**1. Unit Tests: 70% of Test Suite**

```python
# ✅ GOOD: Unit test - fast, isolated, no dependencies

def calculate_discount(price: float, discount_rate: float) -> float:
    """Calculate discounted price."""
    if not 0 <= discount_rate <= 1:
        raise ValueError("Discount rate must be between 0 and 1")
    return price * (1 - discount_rate)

# Unit test (runs in <1ms)
def test_calculate_discount():
    assert calculate_discount(100, 0.2) == 80.0
    assert calculate_discount(50, 0.5) == 25.0

def test_calculate_discount_invalid_rate():
    with pytest.raises(ValueError):
        calculate_discount(100, 1.5)  # Invalid rate

# ✅ Characteristics:
# - Tests single function
# - No database, no API calls
# - Runs in milliseconds
# - Deterministic (always same result)
# - Tests edge cases easily
```

**2. Integration Tests: 20% of Test Suite**

```python
# ✅ GOOD: Integration test - tests multiple components together

class OrderService:
    def __init__(self, db, payment_gateway):
        self.db = db
        self.payment_gateway = payment_gateway

    def create_order(self, user_id, items, payment_method):
        # Save order to database
        order = self.db.create_order(user_id, items)
        # Charge payment
        payment = self.payment_gateway.charge(order.total, payment_method)
        # Update order status
        self.db.update_order_status(order.id, "paid")
        return order

# Integration test (runs in ~100ms with test database)
def test_create_order_integration(test_db, mock_payment_gateway):
    service = OrderService(test_db, mock_payment_gateway)

    user = test_db.create_user("test@example.com")
    items = [{"product_id": 1, "quantity": 2}]

    order = service.create_order(user.id, items, "credit_card")

    # Verify database state
    assert test_db.get_order(order.id).status == "paid"
    assert mock_payment_gateway.charges[-1].amount == order.total

# ✅ Characteristics:
# - Tests multiple components (service + database)
# - Uses test database (real DB interactions)
# - Mocks external services (payment gateway)
# - Runs in 100ms-1s
# - Verifies integration between components
```

**3. E2E Tests: 10% of Test Suite**

```javascript
// ✅ GOOD: E2E test - tests entire user flow

// E2E test (runs in ~5-10 seconds with browser)
test("user can complete purchase flow", async () => {
    // Start browser
    await page.goto("https://localhost:3000");

    // Login
    await page.fill("#email", "test@example.com");
    await page.fill("#password", "password123");
    await page.click("#login-button");

    // Add item to cart
    await page.click("#product-1 .add-to-cart");

    // Checkout
    await page.click("#cart-icon");
    await page.click("#checkout-button");

    // Fill payment
    await page.fill("#card-number", "4242424242424242");
    await page.click("#submit-payment");

    // Verify success
    await expect(page.locator("#order-confirmation")).toBeVisible();
});

// ✅ Characteristics:
// - Tests entire user flow through UI
// - Real browser, real database, real services
// - Runs in seconds to minutes
// - Catches integration issues across entire stack
// - Validates critical user journeys
```

**4. Test Pyramid Ratio Enforcement**

```python
# ✅ GOOD: Verify test pyramid ratio with pytest

# conftest.py
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Report test pyramid metrics after test run."""
    reports = terminalreporter.stats

    # Count test types based on markers or directory
    unit_tests = len([t for t in reports.get('passed', []) if 'tests/unit/' in t.nodeid])
    integration_tests = len([t for t in reports.get('passed', []) if 'tests/integration/' in t.nodeid])
    e2e_tests = len([t for t in reports.get('passed', []) if 'tests/e2e/' in t.nodeid])

    total = unit_tests + integration_tests + e2e_tests

    if total > 0:
        unit_pct = (unit_tests / total) * 100
        integration_pct = (integration_tests / total) * 100
        e2e_pct = (e2e_tests / total) * 100

        print(f"\n=== Test Pyramid ===")
        print(f"Unit:        {unit_tests:3d} ({unit_pct:.1f}%) - Target: 70%")
        print(f"Integration: {integration_tests:3d} ({integration_pct:.1f}%) - Target: 20%")
        print(f"E2E:         {e2e_tests:3d} ({e2e_pct:.1f}%) - Target: 10%")

        # Warn if pyramid is inverted
        if e2e_pct > 30:
            print(f"⚠️  WARNING: Too many E2E tests ({e2e_pct:.1f}% > 30%)")
        if unit_pct < 50:
            print(f"⚠️  WARNING: Too few unit tests ({unit_pct:.1f}% < 50%)")
```

**5. Organize Tests by Type**

```bash
# ✅ GOOD: Directory structure enforces pyramid

tests/
├── unit/              # 70% - Fast, isolated tests
│   ├── test_models.py
│   ├── test_services.py
│   ├── test_utils.py
│   └── test_validators.py
├── integration/       # 20% - Component integration tests
│   ├── test_api.py
│   ├── test_database.py
│   └── test_payment.py
└── e2e/              # 10% - Full user flow tests
    ├── test_purchase_flow.py
    └── test_registration_flow.py

# Run different test levels separately:
pytest tests/unit/              # Fast: ~1-5 seconds
pytest tests/integration/       # Medium: ~10-30 seconds
pytest tests/e2e/              # Slow: ~1-5 minutes
```

**6. Test Different Layers Differently**

```python
# ✅ GOOD: Test business logic with unit tests

# Business logic (pure function) → Unit test
def calculate_shipping_cost(weight_kg: float, distance_km: float) -> float:
    """Calculate shipping cost based on weight and distance."""
    base_cost = 5.0
    weight_cost = weight_kg * 0.5
    distance_cost = distance_km * 0.1
    return base_cost + weight_cost + distance_cost

def test_calculate_shipping_cost():  # Unit test - fast!
    assert calculate_shipping_cost(10, 100) == 20.0
    assert calculate_shipping_cost(0, 0) == 5.0

# Database layer → Integration test
class OrderRepository:
    def save_order(self, order):
        """Save order to database."""
        return self.db.insert(order)

def test_save_order(test_db):  # Integration test - medium speed
    repo = OrderRepository(test_db)
    order = Order(user_id=1, total=100)
    saved = repo.save_order(order)
    assert test_db.get_order(saved.id) is not None

# Full user flow → E2E test
def test_complete_purchase_flow(browser):  # E2E test - slow
    # Full browser test of entire checkout flow
    ...
```

---

### Implementation Patterns

#### ✅ Good: Comprehensive Unit Test Coverage

```python
# Business logic function with comprehensive unit tests

def process_refund(order: Order, amount: Decimal) -> Refund:
    """
    Process refund for order.

    Raises:
        ValueError: If amount exceeds order total
        ValueError: If order already fully refunded
    """
    if amount > order.total:
        raise ValueError(f"Refund amount {amount} exceeds order total {order.total}")

    if order.refunded_amount + amount > order.total:
        raise ValueError(f"Total refunds would exceed order total")

    refund = Refund(order_id=order.id, amount=amount)
    order.refunded_amount += amount
    return refund

# Comprehensive unit tests (all run in <100ms total)
class TestProcessRefund:
    def test_successful_partial_refund(self):
        order = Order(id=1, total=Decimal("100"), refunded_amount=Decimal("0"))
        refund = process_refund(order, Decimal("30"))
        assert refund.amount == Decimal("30")
        assert order.refunded_amount == Decimal("30")

    def test_successful_full_refund(self):
        order = Order(id=1, total=Decimal("100"), refunded_amount=Decimal("0"))
        refund = process_refund(order, Decimal("100"))
        assert refund.amount == Decimal("100")
        assert order.refunded_amount == Decimal("100")

    def test_refund_exceeds_total(self):
        order = Order(id=1, total=Decimal("100"), refunded_amount=Decimal("0"))
        with pytest.raises(ValueError, match="exceeds order total"):
            process_refund(order, Decimal("150"))

    def test_multiple_refunds_exceed_total(self):
        order = Order(id=1, total=Decimal("100"), refunded_amount=Decimal("80"))
        with pytest.raises(ValueError, match="would exceed order total"):
            process_refund(order, Decimal("30"))

    def test_zero_amount_refund(self):
        order = Order(id=1, total=Decimal("100"), refunded_amount=Decimal("0"))
        refund = process_refund(order, Decimal("0"))
        assert refund.amount == Decimal("0")

# ✅ Result: 5 unit tests cover all paths in <100ms
```

---

#### ✅ Good: Integration Test for Database Operations

```python
# Integration test: Test service + database integration

class OrderService:
    def __init__(self, db, email_service):
        self.db = db
        self.email_service = email_service

    def cancel_order(self, order_id: int, reason: str) -> Order:
        order = self.db.get_order(order_id)
        if order.status == "shipped":
            raise ValueError("Cannot cancel shipped order")

        order.status = "cancelled"
        order.cancellation_reason = reason
        self.db.update_order(order)
        self.email_service.send_cancellation_email(order)
        return order

# Integration test with test database
def test_cancel_order_integration(test_db, mock_email_service):
    service = OrderService(test_db, mock_email_service)

    # Setup: Create order in test database
    order = test_db.create_order(user_id=1, total=Decimal("100"), status="pending")

    # Execute: Cancel order
    cancelled = service.cancel_order(order.id, "Customer request")

    # Verify: Database state changed
    db_order = test_db.get_order(order.id)
    assert db_order.status == "cancelled"
    assert db_order.cancellation_reason == "Customer request"

    # Verify: Email sent
    assert mock_email_service.sent_emails[-1].order_id == order.id

# ✅ Result: Integration test runs in ~100ms with test DB
```

---

#### ❌ Bad: Inverted Pyramid (Too Many E2E Tests)

```javascript
// ❌ BAD: Testing every edge case with E2E tests

// E2E test for simple validation (should be unit test!)
test("user cannot submit form with invalid email", async () => {
    await page.goto("https://localhost:3000/register");
    await page.fill("#email", "invalid-email");  // Invalid
    await page.click("#submit");
    await expect(page.locator(".error")).toHaveText("Invalid email");
});

// E2E test for calculation (should be unit test!)
test("discount calculation shows correct price", async () => {
    await page.goto("https://localhost:3000/product/1");
    const price = await page.locator("#price").textContent();
    expect(price).toBe("$80.00");  // 20% discount on $100
});

// Problems:
// - Each E2E test takes 5-10 seconds
// - Testing simple logic that should be unit tested
// - Flaky (browser timing issues)
// - Can't test all edge cases (too slow)
// - Expensive CI runs

// ✅ GOOD: Unit test these instead
test("validateEmail rejects invalid email", () => {
    expect(validateEmail("invalid-email")).toBe(false);
});  // <1ms

test("calculateDiscount applies 20% correctly", () => {
    expect(calculateDiscount(100, 0.2)).toBe(80);
});  // <1ms
```

---

#### ❌ Bad: No Test Organization

```bash
# ❌ BAD: All tests mixed together

tests/
├── test_everything.py  # 1000 lines, unit + integration + E2E mixed
├── test_more.py
└── test_stuff.py

# Problems:
# - Can't run just fast tests
# - Can't measure pyramid ratio
# - CI runs all tests always (slow)
# - No clear test strategy
```

---

## Anti-Patterns

### ❌ Anti-Pattern 1: Testing Business Logic with E2E Tests

**Problem**: Using slow E2E tests for simple logic that should be unit tested.

```python
# ❌ BAD: E2E test for simple validation
@pytest.mark.e2e
def test_password_strength_weak(browser):
    browser.goto("/register")
    browser.fill("#password", "123")
    browser.click("#submit")
    assert browser.find(".error").text == "Password too weak"
    # Takes 5 seconds to run

# ✅ GOOD: Unit test for validation logic
def test_password_strength_weak():
    assert validate_password_strength("123") == "weak"
    # Takes <1ms to run
```

**Impact:**
- 5000x slower (5s vs 1ms)
- Can't test all edge cases (too slow)
- Flaky test failures
- Expensive CI resources

---

### ❌ Anti-Pattern 2: No Integration Tests

**Problem**: Jumping directly from unit tests to E2E tests, skipping integration layer.

```python
# ❌ BAD: Only unit tests and E2E tests, no integration

# Unit test: Tests function in isolation
def test_create_user_unit():
    user = User("test@example.com", "password")
    assert user.email == "test@example.com"

# E2E test: Tests entire system (skips integration layer)
def test_create_user_e2e(browser):
    browser.goto("/register")
    browser.fill("#email", "test@example.com")
    browser.click("#submit")
    assert browser.find(".success").is_visible()

# ❌ Missing: Integration test for database interaction
# Result: Don't know if UserService + Database integration works
# until running slow E2E test

# ✅ GOOD: Add integration test
def test_create_user_integration(test_db):
    service = UserService(test_db)
    user = service.create_user("test@example.com", "password")
    assert test_db.get_user(user.id).email == "test@example.com"
    # Runs in ~100ms, catches DB integration bugs
```

**Impact:**
- Miss integration bugs until E2E tests
- Slow feedback loop
- Hard to debug (E2E test doesn't pinpoint issue)

---

### ❌ Anti-Pattern 3: Flaky E2E Tests Not Addressed

**Problem**: E2E tests fail randomly, team ignores or re-runs them.

```javascript
// ❌ BAD: Flaky E2E test that fails 20% of the time

test("load user dashboard", async () => {
    await page.goto("/dashboard");
    await page.click("#load-data");  // Triggers API call
    await expect(page.locator("#user-stats")).toBeVisible();
    // ❌ Fails randomly: timing issue, API call not complete
});

// ✅ GOOD: Fix flakiness with proper waits
test("load user dashboard", async () => {
    await page.goto("/dashboard");
    await page.click("#load-data");
    // Wait for API call to complete
    await page.waitForResponse(response =>
        response.url().includes("/api/stats") && response.status() === 200
    );
    await expect(page.locator("#user-stats")).toBeVisible();
});
```

**Impact:**
- Developers lose trust in tests
- "Flaky test" → "Re-run CI" becomes norm
- Real bugs hidden among flaky failures
- Wasted CI resources

---

## Implementation Checklist

### Test Pyramid Ratio

- [ ] **70% unit tests** - Fast, isolated, no external dependencies
- [ ] **20% integration tests** - Test component interactions (DB, services)
- [ ] **10% E2E tests** - Test critical user flows only
- [ ] **Measure ratio** - Track test count by type in CI
- [ ] **Warn on violations** - CI warns if pyramid inverted

### Unit Tests

- [ ] **Test business logic** - All pure functions have unit tests
- [ ] **Fast execution** - Unit test suite runs in <10 seconds
- [ ] **No external dependencies** - No database, API, file system
- [ ] **Comprehensive coverage** - Test all edge cases, error paths
- [ ] **Run on every commit** - Unit tests in pre-commit hook

### Integration Tests

- [ ] **Test component integration** - Service + database, service + API
- [ ] **Use test fixtures** - Test database, mocked external services
- [ ] **Medium speed** - Integration suite runs in <1 minute
- [ ] **Critical paths only** - Don't integration test everything

### E2E Tests

- [ ] **Critical flows only** - Purchase, registration, login
- [ ] **Happy paths primarily** - E2E for main success scenarios
- [ ] **Stable, not flaky** - Fix flaky tests immediately
- [ ] **Run before deployment** - E2E tests in staging/pre-prod

---

## Summary

**Test Pyramid** means maintaining 70% unit tests, 20% integration tests, 10% E2E tests. Unit tests provide fast feedback; integration tests verify component interactions; E2E tests validate critical user flows.

**Core Rules:**

- **70% unit tests** - Fast (<1ms each), isolated, no dependencies
- **20% integration tests** - Medium speed (~100ms), test component interactions
- **10% E2E tests** - Slow (seconds), test critical user journeys
- **Organize by type** - Separate directories for unit/integration/e2e
- **Measure ratio** - Track test pyramid metrics in CI
- **Fix inverted pyramid** - If >30% E2E tests, convert to unit/integration tests
