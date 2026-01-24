# Testing
*Test framework rules and patterns*

## Core Testing Principles

- **Edge-Cases-Mandatory**: Always test: empty/None, whitespace-only, boundary values (0, 1, max, max+1)
- **State-Matrix**: Test all valid state combinations where multiple states interact
- **Input-Variations**: Test normalized vs raw input (whitespace, case variations, unicode)
- **Error-Paths**: Test error conditions, not just happy paths
- **Deterministic**: Tests must be deterministic - no random, no time-dependent assertions
- **Type-Coercion**: Test invalid type coercion (string "1" vs int 1)

---

## Coverage Targets by Code Type

| Code Type | Line | Branch | Examples |
|-----------|------|--------|----------|
| Critical | 90-100% | 85-100% | Payment, auth, security, data integrity |
| Core | 80-90% | 75-85% | Main business logic, APIs |
| Standard | 75-85% | 70-80% | Feature code, utilities |
| Infrastructure | 60-75% | 55-70% | Config, helpers, formatters |

**Branch coverage > Line coverage** for decision logic

### Mutation Testing Targets

| Code Type | Mutation Score | Tools |
|-----------|----------------|-------|
| Critical | 80-95% | PIT (Java), Stryker (JS/TS), mutmut (Python) |
| Core | 75-85% | |
| Standard | 70-80% | |
| Infrastructure | 60-70% | |

**Purpose**: Validates test effectiveness - if mutants survive, tests are weak

---

## Unit Testing (Test:Unit)
**Trigger:** {unit_test_deps}

- **Isolation**: No shared state between tests
- **Fast-Feedback**: Tests complete in seconds (<100ms per test)
- **Mock-Boundaries**: Mock at system boundaries, not internal details
- **Assertions-Clear**: One concept per test, clear failure messages

### AAA Pattern (Mandatory)

```
# Arrange: Setup dependencies, mocks, test data
# Act: Single logical operation
# Assert: One concept per test
```

**Naming**: `[Method]_[Scenario]_[ExpectedBehavior]`
- `add_with_negative_numbers_raises_value_error`
- `login_with_valid_credentials_returns_token`
- `parse_empty_string_returns_none`

### Test Isolation Requirements

| Resource | Violation | Fix |
|----------|-----------|-----|
| Database | Direct DB calls | Mock repository interface |
| File System | File I/O | Mock file system interface |
| External APIs | Real HTTP calls | Mock HTTP client |
| System Time | `datetime.now()` | Inject clock interface |
| Random State | `random.random()` | Inject random generator |
| Test Order | Shared state | Fresh setup per test |

---

## Property-Based Testing

**Use when**:
- Testing across large input space (100s-1000s of combinations)
- Properties should hold for ANY valid input
- Complex algorithms (sorting, parsing, math, serialization)

**Generators** (Hypothesis/fast-check):
```python
# Python (Hypothesis)
@given(integers(min_value=0, max_value=1000))
@given(lists(integers()))
@given(text(alphabet=string.ascii_letters))

# JavaScript (fast-check)
fc.integer({min: 0, max: 1000})
fc.array(fc.integer())
fc.string()
```

**Common Properties**:
- Roundtrip: `decode(encode(x)) == x`
- Idempotent: `f(f(x)) == f(x)`
- Commutative: `f(a, b) == f(b, a)`
- Invariant: `len(sorted(xs)) == len(xs)`

---

## Security Testing Integration

| Phase | Technique | Timing | Tools |
|-------|-----------|--------|-------|
| Development | SAST | Pre-commit, per-PR | Semgrep, SonarQube, CodeQL |
| Development | SCA | Per-commit | Snyk, Dependabot, npm audit |
| Staging | DAST | Post-build | OWASP ZAP, Burp Suite |
| Continuous | Secret Detection | Pre-push | GitGuardian, TruffleHog, gitleaks |

**Quality Gates**:
- Block PR on CRITICAL/HIGH CVE
- Block PR on new SAST violations
- Block deploy on failed DAST scan

---

## E2E Testing (Test:E2E)
**Trigger:** {e2e_deps}

- **Critical-Paths**: Cover critical user journeys
- **Stable-Selectors**: data-testid attributes for reliable selection
- **Retry-Flaky**: Retry for network flakiness, but fix root cause
- **Parallel-Run**: Parallel execution where possible
- **Visual-Regression**: Include visual regression tests for UI

## E2E Patterns (Test:E2E)
**Trigger:** {playwright_deps}, {cypress_deps}

- **Locators-Prefer**: Use data-testid locators over CSS selectors
- **Auto-Wait**: Rely on framework auto-waiting, avoid sleep/delays
- **Intercept-API**: Use API interception for mocking external calls
- **Commands-Custom**: Create custom commands for reusable test actions

## pytest (Test:pytest)
**Trigger:** {pytest_deps}

- **Fixtures-Scope**: Use appropriate fixture scope (function/module/session)
- **Conftest-Organize**: Organize fixtures in conftest.py hierarchy
- **Parametrize-Use**: Use @pytest.mark.parametrize for test variations

---

## Coverage Tiers

### Basics (Testing:60%)
- **Unit-Isolated**: Fast, deterministic unit tests
- **Mocking**: Isolate tests from external dependencies
- **Coverage-60**: Minimum 60% line coverage

### Standard (Testing:80%)
- **Integration**: Test component interactions
- **Fixtures**: Reusable, maintainable test data
- **Coverage-80**: Minimum 80% line coverage
- **CI-on-PR**: Tests run on every PR
- **Edge-Cases-Standard**: Test empty, None, single item, typical, boundary values

### Full (Testing:90%)
- **E2E**: End-to-end tests for critical user flows
- **Contract**: Consumer-driven contract testing (if Architecture:Microservices)
- **Mutation**: Mutation testing for test effectiveness (if Priority:Quality)
- **Coverage-90**: Minimum 90% line coverage
- **Edge-Cases-Full**: Test whitespace-only, unicode, max+1, state combinations, concurrent access
