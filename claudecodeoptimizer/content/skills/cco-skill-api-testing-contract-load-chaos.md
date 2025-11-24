---
name: api-testing
description: Ensure API reliability and performance through contract tests (Pact), load tests (k6), chaos engineering experiments, and integration tests with testcontainers for real dependencies
keywords: [contract testing, Pact, load testing, k6, chaos engineering, integration testing, testcontainers, performance testing, API testing]
category: testing
related_commands:
  action_types: [audit, generate]
  categories: [testing]
pain_points: [4, 7, 9]
---

# Skill: API Testing - Contract, Load, Chaos

> **Standards:** Format defined in [STANDARDS_SKILLS.md](../STANDARDS_SKILLS.md)  
> **Discovery:** See [STANDARDS_COMMANDS.md](../STANDARDS_COMMANDS.md#18-command-discovery-protocol)


## Domain
Testing

## Purpose
Ensure API reliability, performance, resilience through contract tests (Pact), load tests (k6), chaos engineering, and integration tests.

## Core Techniques

- **Contract Testing**: Consumer defines expected API behavior; provider verifies against it
- **Load Testing**: Simulate realistic load to measure throughput, latency, capacity limits
- **Chaos Engineering**: Inject controlled failures to validate resilience mechanisms
- **Integration Testing**: Test with real dependencies (testcontainers), not mocks
- **Performance Benchmarking**: Continuous monitoring to detect regressions

## Patterns

### ✅ Good: Contract Test (Pact)
```python
# Consumer defines contract
pact = Consumer('UserService').has_pact_with(Provider('PaymentService'))
(pact
  .given('user has balance')
  .upon_receiving('payment request')
  .with_request(method='POST', path='/payments', body={'user_id': 123, 'amount': 50.00})
  .will_respond_with(status=200, body={'transaction_id': '...', 'status': 'success'}))

# Provider verifies
verifier = Verifier(provider='PaymentService')
verifier.verify_pacts('./pacts/userservice-paymentservice.json', provider_base_url='http://localhost:8080')
```
**Why**: Catches breaking changes before production

### ✅ Good: Load Test (k6)
```javascript
export let options = {
  stages: [
    { duration: '2m', target: 100 },
    { duration: '5m', target: 100 },
    { duration: '2m', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  let response = http.get('https://api.example.com/products');
  check(response, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  sleep(1);
}
```
**Why**: Identifies bottlenecks and capacity limits

### ✅ Good: Integration Test (Real DB)
```python
@pytest.fixture(scope="module")
def database():
    with PostgresContainer("postgres:14") as postgres:
        yield postgres.get_connection_url()

def test_user_registration_flow(database, cache):
    response = app.post('/register', json={'email': '{TEST_EMAIL}', 'password': '{TEST_PASSWORD}'})
    assert response.status_code == 201
    user = db.query(User).filter_by(email='{TEST_EMAIL}').first()
    assert user is not None
```
**Why**: Tests real dependencies, catches integration issues

### ✅ Good: Chaos Test
```yaml
steady-state-hypothesis:
  probes:
    - type: probe
      tolerance: 200
      provider: {type: http, url: https://api.example.com/health}

method:
  - type: action
    provider:
      module: chaosk8s.pod.actions
      func: terminate_pods
      arguments: {label_selector: app=backend, ns: production}
```
**Why**: Validates failover and circuit breakers

### ❌ Bad: Only Mocked Tests
```python
# ❌ Never hits real database
def test_create_user():
    mock_db = Mock()
    create_user(mock_db, user_data)
    mock_db.save.assert_called_once()
```
**Why**: Misses integration failures

### ❌ Bad: No Load Testing
```python
# ❌ Deploy without capacity testing
# Result: Production crashes under first real load
```
**Why**: Unknown performance limits

### ❌ Bad: Ignoring Contract Tests
```python
# ❌ Change API response without checking consumers
# Old: {'user_id': 123}
# New: {'id': 123}  # Breaking change!
```
**Why**: Breaks consumers in production

## Checklist

- [ ] Contract tests for provider-consumer APIs (Pact)
- [ ] Load tests with thresholds (k6: p95<500ms, error<1%)
- [ ] Integration tests with testcontainers (real DB/Redis)
- [ ] Chaos experiments for critical paths
- [ ] Progressive load: smoke → load → stress
- [ ] Track metrics: coverage, SLA%, contract failures, p95 latency
---

---

