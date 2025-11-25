---
name: cco-skill-testing-fundamentals
description: Use this skill when testing strategy, test quality, or test architecture is mentioned
keywords: [test, testing, coverage, unit tests, integration tests, e2e, test pyramid, test isolation, property testing, flaky tests, pytest, jest, mock, fixture]
category: testing
related_commands:
  action_types: [audit, fix, generate]
  categories: [testing]
pain_points: [4]
---

# Skill: Testing Strategy - Test Pyramid, Coverage & Isolation

> **Standards:** Format defined in [cco-standards.md](../cco-standards.md)  
> **Discovery:** See [cco-standards.md](../cco-standards.md#18-command-discovery-protocol)


## Purpose

Prevent production defects, flaky tests, and inadequate test coverage through comprehensive testing strategies.

**Solves**:
- **Inadequate Test Coverage**: Most production bugs occur in untested code paths
- **Inverted Test Pyramid**: Slow e2e tests dominate, causing slow CI runs
- **Flaky Tests**: Non-isolated tests fail randomly, reducing developer trust
- **Missing Edge Cases**: Property testing catches significantly more bugs than example-based tests alone

**Impact**: Critical
---

---

## Guidance Areas

### Test Pyramid
**Category**: Testing Architecture
**Why**: Fast unit tests (majority), moderate integration tests, minimal e2e tests
**Triggers when**: Test strategy, CI performance, test suite design

### Test Coverage
**Category**: Test Quality
**Why**: Measure and enforce minimum coverage thresholds (high coverage target)
**Triggers when**: Analyzing test gaps, reviewing PRs, quality gates

### Test Isolation
**Category**: Test Reliability
**Why**: Each test runs independently; shared state causes most flaky tests
**Triggers when**: Debugging flaky tests, test fixtures, parallelization

### Property Testing
**Category**: Advanced Testing
**Why**: Generative testing finds edge cases manual tests miss (significant additional coverage)
**Triggers when**: Testing complex algorithms, data validation, invariant checking

### Integration Tests
**Category**: Testing Strategy
**Why**: Verify component interactions without full system overhead
**Triggers when**: API integrations, database interactions, multi-module workflows

**Note**: This guidance is loaded into context only when this skill activates.

---

## Automatic Activation

This skill auto-loads when Claude detects:
- **Keywords**: test, testing, coverage, unit test, integration test, e2e, flaky, isolation, property, mock, fixture
- **User intent**: "improve test coverage", "fix flaky tests", "test strategy review"
- **File context**: `*test*.py`, `*_test.go`, `*.spec.ts`, `test_*.py`, `*Test.java`

**No manual invocation needed** - Claude autonomously decides based on context.

---

## Related Skills

Skills that work well together:
- **Code quality skills**: Testing drives refactoring
- **CI/CD skills**: Test pyramid determines CI gate thresholds

---

## Examples

### Example 1: Slow Test Suite
```
User: "Our test suite takes 20 minutes to run. How can we speed it up?"
       ↓
Skill: cco-skill-testing-fundamentals auto-loads (detects "test suite")
       ↓
Guidance: Test Pyramid, Test Isolation active
       ↓
Result: Analyzes test distribution, identifies inverted pyramid, recommends e2e → unit refactor
```

### Example 2: Flaky Tests
```
User: "Why do our tests fail randomly?"
       ↓
Skill: cco-skill-testing-fundamentals (detects "flaky test" intent)
       ↓
Guidance: Test Isolation active
       ↓
Result: Identifies shared state, non-deterministic dependencies, parallelization issues
```

### Example 3: File Context
```
User opens: test_auth.py
       ↓
Skill: cco-skill-testing-fundamentals (detects "test_*.py" pattern)
       ↓
Guidance: Test Isolation, Test Coverage active
       ↓
Result: Checks isolation violations, coverage gaps, property-based opportunities
```

---

## Test Analysis Patterns (Claude Executes)

When auditing test coverage or quality, use these analysis patterns:

### Find Untested Code

```bash
# Find Python files without corresponding tests
find . -name "*.py" -path "*/src/*" -o -name "*.py" -path "*/${PROJECT}/*" | \
  while read f; do
    base=$(basename "${f%.py}")
    if ! find tests/ -name "*${base}*test*.py" -o -name "test_*${base}*.py" 2>/dev/null | grep -q .; then
      echo "Untested: $f"
    fi
  done

# Coverage analysis with threshold
pytest --cov=src --cov-report=term-missing --cov-fail-under=80

# List functions and check for tests
# Create safe temp directory (sandboxed)
mkdir -p .tmp
grep -rhn "^def \|^async def " --include="*.py" src/ | \
  sed 's/.*def \([a-zA-Z_][a-zA-Z0-9_]*\).*/\1/' | sort -u > .tmp/funcs.txt
grep -rh "def test_" --include="*.py" tests/ | \
  sed 's/.*def test_\([a-zA-Z_][a-zA-Z0-9_]*\).*/\1/' | sort -u > .tmp/tested.txt
echo "Potentially untested functions:"
comm -23 .tmp/funcs.txt .tmp/tested.txt
```

### Flaky Test Detection

```bash
# Time-dependent tests (potential flakiness)
grep -rn "random\|time.sleep\|datetime.now\|time.time\|uuid" --include="*test*.py" .

# Shared state indicators
grep -rn "global \|cls\.\|self\.__class__\|setUpModule\|tearDownModule" --include="*test*.py" .

# Network calls in tests (should be mocked)
grep -rn "requests\.\|urllib\|http\.client\|aiohttp" --include="*test*.py" . | grep -v "mock\|patch\|@responses"

# Database without fixtures
grep -rn "\.save()\|\.create()\|\.delete()" --include="*test*.py" . | grep -v "factory\|fixture"
```

### Test Pyramid Analysis

```bash
# Count test types
echo "Unit tests (test_*.py in tests/unit/):"
find tests/unit -name "test_*.py" 2>/dev/null | wc -l

echo "Integration tests (tests/integration/):"
find tests/integration -name "test_*.py" 2>/dev/null | wc -l

echo "E2E tests (tests/e2e/):"
find tests/e2e -name "test_*.py" 2>/dev/null | wc -l

# Ideal ratio: 70% unit, 20% integration, 10% e2e
```

### Test Quality Indicators

```bash
# Tests with no assertions (likely incomplete)
grep -L "assert\|pytest.raises\|self.assert" tests/**/test_*.py 2>/dev/null

# Tests with too many assertions (should be split)
grep -c "assert" tests/**/test_*.py 2>/dev/null | awk -F: '$2 > 10 {print "Too many assertions:", $1, $2}'

# Mock overuse (>5 mocks in one test)
grep -c "@patch\|@mock\|MagicMock\|Mock(" tests/**/test_*.py 2>/dev/null | awk -F: '$2 > 5 {print "Mock overuse:", $1, $2}'
```

---

## Core Techniques

### Test Pyramid

```
        /\
       /  \     E2E (10%)     - Slow, expensive, real browser/network
      /----\
     /      \   Integration   - Medium speed, real DB/cache
    /--------\  (20%)
   /          \ Unit (70%)    - Fast, isolated, mocked deps
  /____________\

Target: 70% unit / 20% integration / 10% e2e
```

**Unit Test (Isolated)**
```python
# ✅ GOOD: Fast, isolated, tests ONE function
def test_calculate_discount():
    # Arrange
    price = 100
    discount_rate = 0.2

    # Act
    result = calculate_discount(price, discount_rate)

    # Assert
    assert result == 80

# Test pure logic, no I/O, no external dependencies
# Runs in milliseconds
```

**Integration Test (Component Interactions)**
```python
# ✅ GOOD: Tests real database interaction
@pytest.mark.integration
def test_user_repository_creates_user(db_session):
    # Arrange
    repo = UserRepository(db_session)
    user_data = {"email": "test@example.com", "name": "Test"}

    # Act
    user = repo.create(user_data)

    # Assert
    assert user.id is not None
    assert db_session.query(User).get(user.id) is not None

# Uses real database (often via testcontainers)
# Runs in seconds
```

**E2E Test (Full System)**
```python
# ✅ GOOD: Tests full user journey
@pytest.mark.e2e
def test_user_registration_flow(browser):
    # Navigate and interact
    browser.get("/register")
    browser.find_element(By.ID, "email").send_keys("user@test.com")
    browser.find_element(By.ID, "password").send_keys("secure123")
    browser.find_element(By.ID, "submit").click()

    # Verify
    assert "Welcome" in browser.page_source
    assert browser.current_url == "/dashboard"

# Real browser, real backend, real database
# Runs in tens of seconds
```

### Test Isolation

**CRITICAL**: Each test must be independent. No shared state.

```python
# ❌ BAD: Shared state causes flakiness
class TestUserService:
    user = None  # Class-level shared state!

    def test_create_user(self):
        self.user = create_user("alice")  # Sets shared state
        assert self.user.name == "alice"

    def test_delete_user(self):
        delete_user(self.user)  # Depends on previous test!
        assert self.user is None

# ✅ GOOD: Each test independent
class TestUserService:
    def test_create_user(self, user_factory):
        user = user_factory.create(name="alice")
        assert user.name == "alice"

    def test_delete_user(self, user_factory):
        user = user_factory.create(name="bob")
        delete_user(user)
        assert User.query.get(user.id) is None
```

**Fixture Scope Best Practices:**
```python
# ✅ Function scope (default) - isolated per test
@pytest.fixture
def user():
    return create_user("test")

# ✅ Module scope - shared within file (read-only data)
@pytest.fixture(scope="module")
def config():
    return load_test_config()

# ⚠️ Session scope - use sparingly (expensive setup)
@pytest.fixture(scope="session")
def database():
    db = create_test_db()
    yield db
    db.drop_all()
```

### Test Coverage

**Target Thresholds:**
| Coverage Level | Meaning | Recommendation |
|----------------|---------|----------------|
| < 50% | Critical gaps | Urgent: Add tests |
| 50-70% | Moderate | Improve gradually |
| 70-80% | Good | Standard target |
| 80-90% | Strong | Most projects goal |
| > 90% | Excellent | Diminishing returns |

**Coverage Configuration (pytest-cov):**
```ini
# pyproject.toml
[tool.coverage.run]
source = ["src"]
branch = true
omit = ["*/tests/*", "*/__init__.py"]

[tool.coverage.report]
fail_under = 80
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
]
```

**Coverage Enforcement:**
```bash
# CI pipeline
pytest --cov=src --cov-report=xml --cov-fail-under=80
```

---

## Test Doubles

| Type | Purpose | Example |
|------|---------|---------|
| **Stub** | Returns canned data | `stub.get_user.return_value = fake_user` |
| **Mock** | Verifies interactions | `mock.save.assert_called_once_with(user)` |
| **Spy** | Records calls | `spy.log.call_count == 3` |
| **Fake** | Working implementation | `FakeEmailService` (no real emails) |

### Mock vs Stub

```python
# STUB: Control input, don't verify
def test_user_greeting_with_stub():
    user_repo = Mock()
    user_repo.get_by_id.return_value = User(name="Alice")  # Stub

    service = GreetingService(user_repo)
    greeting = service.greet(user_id=1)

    assert greeting == "Hello, Alice!"
    # No verification of how get_by_id was called

# MOCK: Verify interaction
def test_user_save_with_mock():
    user_repo = Mock()
    service = UserService(user_repo)

    service.update_name(user_id=1, name="Bob")

    # Verify correct method called with correct args
    user_repo.update.assert_called_once_with(1, name="Bob")
```

### Patching External Dependencies

```python
from unittest.mock import patch, MagicMock

# ✅ GOOD: Patch at usage point
@patch("myapp.services.user_service.requests.get")
def test_fetch_external_api(mock_get):
    mock_get.return_value.json.return_value = {"data": "test"}

    result = fetch_external_data()

    assert result == {"data": "test"}
    mock_get.assert_called_once()

# ✅ GOOD: Context manager for targeted patch
def test_send_notification():
    with patch("myapp.notifications.send_email") as mock_send:
        mock_send.return_value = True

        result = notify_user(user_id=1, message="Hello")

        assert result is True
        mock_send.assert_called_once()
```

---

## Property Testing (Hypothesis)

### What is Property Testing?

Instead of specific examples, define **properties** that must always hold.

```python
from hypothesis import given, strategies as st

# Example-based: Test specific values
def test_sort_example():
    assert sort([3, 1, 2]) == [1, 2, 3]
    assert sort([]) == []
    assert sort([1]) == [1]

# Property-based: Test invariants
@given(st.lists(st.integers()))
def test_sort_properties(lst):
    sorted_lst = sort(lst)

    # Property 1: Same length
    assert len(sorted_lst) == len(lst)

    # Property 2: Same elements
    assert sorted(lst) == sorted(sorted_lst)

    # Property 3: Ordered
    assert all(a <= b for a, b in zip(sorted_lst, sorted_lst[1:]))
```

### Common Properties

```python
# Idempotence: f(f(x)) == f(x)
@given(st.text())
def test_normalize_idempotent(text):
    once = normalize(text)
    twice = normalize(once)
    assert once == twice

# Symmetry: encode(decode(x)) == x
@given(st.binary())
def test_encode_decode_symmetry(data):
    encoded = encode(data)
    decoded = decode(encoded)
    assert decoded == data

# Invariant: property always holds
@given(st.integers(min_value=0))
def test_factorial_positive(n):
    result = factorial(n)
    assert result >= 1

# Commutativity: f(a, b) == f(b, a)
@given(st.integers(), st.integers())
def test_add_commutative(a, b):
    assert add(a, b) == add(b, a)
```

### Strategies for Complex Data

```python
from hypothesis import strategies as st

# User object strategy
user_strategy = st.builds(
    User,
    name=st.text(min_size=1, max_size=100),
    email=st.emails(),
    age=st.integers(min_value=0, max_value=150),
)

@given(user_strategy)
def test_user_validation(user):
    # Should never raise for valid user
    assert validate_user(user)

# Nested structures
order_strategy = st.builds(
    Order,
    id=st.uuids(),
    items=st.lists(
        st.builds(Item, name=st.text(), price=st.decimals(min_value=0)),
        min_size=1,
    ),
    created_at=st.datetimes(),
)
```

---

## Flaky Test Mitigation

### Common Causes and Fixes

| Cause | Detection | Fix |
|-------|-----------|-----|
| **Time dependency** | `datetime.now()` in tests | Freeze time with `freezegun` |
| **Random data** | `random.choice()` | Set seed or use factories |
| **Race conditions** | Async/parallel tests | Add proper waits/locks |
| **External services** | Network calls | Mock all externals |
| **Shared state** | Class variables | Use fixtures with proper scope |
| **Order dependency** | Pass alone, fail together | Ensure isolation |

### Time Freezing

```python
from freezegun import freeze_time

# ❌ BAD: Depends on current time
def test_expired_token_flaky():
    token = create_token(expires_in=3600)
    # Sometimes fails near midnight
    assert not token.is_expired()

# ✅ GOOD: Frozen time
@freeze_time("2024-01-15 12:00:00")
def test_expired_token():
    token = create_token(expires_in=3600)
    assert not token.is_expired()

    with freeze_time("2024-01-15 14:00:00"):
        assert token.is_expired()
```

### Async Test Patterns

```python
import pytest
import asyncio

# ✅ GOOD: Proper async testing
@pytest.mark.asyncio
async def test_async_fetch():
    result = await fetch_data()
    assert result is not None

# ✅ GOOD: Timeout for hanging tests
@pytest.mark.asyncio
@pytest.mark.timeout(5)
async def test_with_timeout():
    result = await slow_operation()
    assert result == expected
```

---

## Fixtures Best Practices

### Factory Pattern

```python
import pytest
from faker import Faker

fake = Faker()

@pytest.fixture
def user_factory(db_session):
    """Factory for creating test users with defaults."""
    created_users = []

    def _create_user(
        email=None,
        name=None,
        is_active=True,
    ):
        user = User(
            email=email or fake.email(),
            name=name or fake.name(),
            is_active=is_active,
        )
        db_session.add(user)
        db_session.commit()
        created_users.append(user)
        return user

    yield _create_user

    # Cleanup
    for user in created_users:
        db_session.delete(user)
    db_session.commit()

# Usage
def test_active_users(user_factory):
    active = user_factory(is_active=True)
    inactive = user_factory(is_active=False)

    users = get_active_users()

    assert active in users
    assert inactive not in users
```

### Testcontainers

```python
import pytest
from testcontainers.postgres import PostgresContainer

@pytest.fixture(scope="session")
def postgres():
    """Real PostgreSQL in Docker for integration tests."""
    with PostgresContainer("postgres:15") as pg:
        yield pg.get_connection_url()

@pytest.fixture
def db_session(postgres):
    """Database session with transaction rollback."""
    engine = create_engine(postgres)
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.rollback()
    session.close()
```

---

## Anti-Patterns

### ❌ Testing Implementation Details

```python
# ❌ BAD: Tests internal structure
def test_user_creation_bad():
    service = UserService()
    service.create_user("alice@test.com")

    # Testing private attribute
    assert service._cache["alice@test.com"] is not None
    assert service._db_calls == 1

# ✅ GOOD: Tests behavior
def test_user_creation_good():
    service = UserService()
    user = service.create_user("alice@test.com")

    # Test observable behavior
    assert user.email == "alice@test.com"
    assert service.get_user("alice@test.com") == user
```

### ❌ Too Much Mocking

```python
# ❌ BAD: Everything mocked, tests nothing
def test_over_mocked():
    repo = Mock()
    service = Mock()
    validator = Mock()
    logger = Mock()

    # What are we even testing?
    handler = Handler(repo, service, validator, logger)
    handler.process(Mock())

    validator.validate.assert_called_once()

# ✅ GOOD: Mock only externals
def test_properly_mocked(user_factory):
    repo = UserRepository()  # Real repo
    validator = EmailValidator()  # Real validator

    with patch("myapp.mailer.send") as mock_send:  # Mock external
        handler = Handler(repo, validator)
        handler.process(user_factory())

        mock_send.assert_called_once()
```

### ❌ Assertion-Free Tests

```python
# ❌ BAD: No assertions
def test_user_flow():
    user = create_user("test")
    update_user(user, name="new")
    delete_user(user)
    # Test passes if no exception, but proves nothing

# ✅ GOOD: Meaningful assertions
def test_user_flow():
    user = create_user("test")
    assert user.id is not None

    update_user(user, name="new")
    assert user.name == "new"

    delete_user(user)
    assert get_user(user.id) is None
```

### ❌ Ignoring Edge Cases

```python
# ❌ BAD: Only happy path
def test_divide():
    assert divide(10, 2) == 5

# ✅ GOOD: Include edge cases
class TestDivide:
    def test_normal(self):
        assert divide(10, 2) == 5

    def test_zero_dividend(self):
        assert divide(0, 5) == 0

    def test_zero_divisor(self):
        with pytest.raises(ZeroDivisionError):
            divide(10, 0)

    def test_negative(self):
        assert divide(-10, 2) == -5

    def test_float_result(self):
        assert divide(5, 2) == 2.5
```

---

## Checklist

### Test Suite Health
- [ ] Coverage >= 80% (or team-defined threshold)
- [ ] Test pyramid ratio: ~70% unit / 20% integration / 10% e2e
- [ ] No flaky tests (run 10x passes 10x)
- [ ] Tests run in < 5 min for unit, < 15 min total

### Test Quality
- [ ] Each test has clear Arrange/Act/Assert structure
- [ ] Each test has meaningful assertion(s)
- [ ] Tests are independent (run in any order)
- [ ] Test names describe what they verify

### Isolation
- [ ] No global/shared state between tests
- [ ] External services mocked (HTTP, DB, files)
- [ ] Time-dependent code uses frozen time
- [ ] Random data uses seeded generators or factories

### CI Integration
- [ ] Tests run on every PR
- [ ] Coverage reported and enforced
- [ ] Flaky test detection enabled
- [ ] Parallel execution for speed
