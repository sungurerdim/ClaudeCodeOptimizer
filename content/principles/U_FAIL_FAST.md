---
id: U_FAIL_FAST
title: Fail-Fast Error Handling
category: universal
severity: critical
weight: 10
enforcement: SHOULD
applicability:
  project_types: ['all']
  languages: ['all']
---

# U_FAIL_FAST: Fail-Fast Error Handling 🔴

**Severity**: Critical

Errors must cause immediate, visible failure. No silent fallbacks, no swallowed exceptions.

**Enforcement**: SHOULD

**Project Types**: all
**Languages**: all

---

## Why

### The Problem
- **Silent failures** hide bugs until they cause catastrophic damage
- **Defensive programming gone wrong** - catching all errors masks root causes
- **Error accumulation** - small errors compound into system-wide corruption
- **Debugging nightmare** - failures discovered far from actual error location
- **Data corruption** - continuing execution in invalid state corrupts data

### Core Principle

**When an error occurs:**
1. ❌ **Don't** continue execution in invalid state
2. ❌ **Don't** return null/None/undefined and hope caller checks
3. ❌ **Don't** log error and continue
4. ✅ **Do** throw exception / return error / panic immediately
5. ✅ **Do** make the failure LOUD and VISIBLE
6. ✅ **Do** stop execution at error boundary

### Implementation Patterns

#### ✅ Good: Explicit Error Propagation
```python
# Python: Raise immediately, don't catch-and-continue
def process_user_data(user_id: int) -> User:
    user = db.get_user(user_id)
    if user is None:
        raise ValueError(f"User {user_id} not found")  # FAIL FAST

    if not user.is_active:
        raise PermissionError(f"User {user_id} is inactive")  # FAIL FAST

    return user  # Only reached if valid

# ❌ BAD: Silent fallback
def process_user_data_bad(user_id: int) -> User:
    user = db.get_user(user_id)
    if user is None:
        return User()  # SILENT FAILURE - returns empty user
    # ... continues with potentially invalid data
```

#### ✅ Good: Rust-style Result Types
```rust
// Rust: Explicit error handling, no exceptions
fn divide(a: f64, b: f64) -> Result<f64, String> {
    if b == 0.0 {
        Err("Division by zero".to_string())  // FAIL FAST
    } else {
        Ok(a / b)
    }
}

// Caller MUST handle both Ok and Err
match divide(10.0, 0.0) {
    Ok(result) => println!("Result: {}", result),
    Err(e) => eprintln!("Error: {}", e),  // Can't ignore error
}
```

#### ✅ Good: Go-style Error Returns
```go
// Go: Explicit error returns, check immediately
func getUserBalance(userID int) (float64, error) {
    user, err := db.GetUser(userID)
    if err != nil {
        return 0, fmt.Errorf("get user failed: %w", err)  // FAIL FAST
    }

    if user.Balance < 0 {
        return 0, errors.New("invalid balance")  // FAIL FAST
    }

    return user.Balance, nil
}

// ❌ BAD: Ignore errors
func getUserBalanceBad(userID int) float64 {
    user, _ := db.GetUser(userID)  // Ignores error!
    return user.Balance  // Might panic on nil pointer
}
```

#### ✅ Good: JavaScript Promise Rejection
```javascript
// JavaScript: Reject promises immediately
async function fetchUserData(userId) {
    const response = await fetch(`/api/users/${userId}`);

    if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);  // FAIL FAST
    }

    const data = await response.json();

    if (!data.id) {
        throw new Error("Invalid user data: missing id");  // FAIL FAST
    }

    return data;
}

// ❌ BAD: Silent fallback
async function fetchUserDataBad(userId) {
    try {
        const response = await fetch(`/api/users/${userId}`);
        return await response.json();
    } catch (e) {
        console.log("Error:", e);  // Logs but continues
        return {};  // SILENT FAILURE - returns empty object
    }
}
```

---

## Anti-Patterns

### ❌ Anti-Pattern 1: Catch-All Exception Handler
```python
# ❌ BAD: Swallows ALL errors
try:
    critical_operation()
except Exception:
    pass  # SILENT FAILURE - hides all errors!

# ✅ GOOD: Only catch specific expected errors
try:
    critical_operation()
except ValueError as e:
    logger.error(f"Validation failed: {e}")
    raise  # Re-raise immediately
# Let unexpected errors propagate (fail fast)
```

### ❌ Anti-Pattern 2: Null/None as Error Signal
```python
# ❌ BAD: Returns None on error (caller might not check)
def get_config(key: str) -> Optional[str]:
    try:
        return config[key]
    except KeyError:
        return None  # SILENT FAILURE

# Caller might not check:
value = get_config("api_key")
requests.get(url, headers={"Authorization": value})  # Crashes if None

# ✅ GOOD: Raise exception immediately
def get_config(key: str) -> str:
    try:
        return config[key]
    except KeyError:
        raise ConfigError(f"Missing required config: {key}")  # FAIL FAST
```

### ❌ Anti-Pattern 3: Error Code with Continued Execution
```javascript
// ❌ BAD: Sets error flag but continues
function processPayment(amount) {
    let errorCode = 0;

    if (amount <= 0) {
        errorCode = -1;  // Sets flag but continues!
    }

    // ... continues processing invalid amount
    database.deductBalance(amount);  // Corrupts data!
    return errorCode;
}

// ✅ GOOD: Fail immediately
function processPayment(amount) {
    if (amount <= 0) {
        throw new Error(`Invalid amount: ${amount}`);  // FAIL FAST
    }

    database.deductBalance(amount);  // Only reached if valid
}
```

### ❌ Anti-Pattern 4: Log-and-Continue
```go
// ❌ BAD: Logs error but continues execution
func saveUser(user User) {
    err := db.Save(&user)
    if err != nil {
        log.Printf("Error saving user: %v", err)  // Logs but continues!
        // Continues as if save succeeded - DATA LOSS!
    }

    sendWelcomeEmail(user.Email)  // Runs even if save failed!
}

// ✅ GOOD: Return error immediately
func saveUser(user User) error {
    err := db.Save(&user)
    if err != nil {
        return fmt.Errorf("save user failed: %w", err)  // FAIL FAST
    }

    // Only send email if save succeeded
    return sendWelcomeEmail(user.Email)
}
```

---

### ✅ Legitimate Use Cases
1. **Non-critical optional features**
   ```python
   # Analytics failure shouldn't break core functionality
   try:
       analytics.track_event("user_login")
   except AnalyticsError:
       logger.warning("Analytics unavailable")
       # Continue - analytics is optional
   ```

2. **Background jobs with retry logic**
   ```python
   # Retry transient failures, fail hard on permanent ones
   @retry(max_attempts=3, backoff=exponential)
   def send_notification(user_id):
       # Transient failures retried
       # Permanent failures bubble up after retries
   ```

3. **Circuit breaker patterns**
   ```python
   # Fail fast on overloaded service
   if circuit_breaker.is_open():
       raise ServiceUnavailableError("Circuit breaker open")
   ```

4. **Graceful shutdown**
   ```python
   # Allow ongoing requests to complete during shutdown
   signal.signal(signal.SIGTERM, graceful_shutdown_handler)
   ```

### ❌ Invalid Justifications
- "We'll fix it later" - NO, fail now
- "Users don't like error messages" - Better than data corruption
- "It only fails sometimes" - Makes it worse, not better
- "The error isn't important" - Then remove the check

---

## Implementation Checklist

- [ ] **Eliminate catch-all exception handlers** (except at API boundaries)
- [ ] **Remove null/None as error signals** (use exceptions/Results)
- [ ] **Audit all `try/except` blocks** - Should only catch specific errors
- [ ] **Validate inputs immediately** - Don't defer validation
- [ ] **Add assertions for invariants** - Document assumptions
- [ ] **Use linters** - Enforce error handling (pylint, eslint, clippy)
- [ ] **Code review checklist** - "Can this fail silently?"

---

## Metrics and Monitoring

### Key Indicators
- **Silent failure rate** - Errors caught in logs but not surfaced
- **Error distance** - Lines between error occurrence and detection
- **Recovery time** - Time from failure to root cause identification
- **Data corruption incidents** - Failures that corrupted data

### Monitoring
```python
# Track failures explicitly
from prometheus_client import Counter

failures = Counter('app_failures_total', 'Total failures', ['type'])

def critical_operation():
    try:
        result = dangerous_call()
        if not validate(result):
            failures.labels(type='validation').inc()
            raise ValidationError("Invalid result")  # FAIL FAST
        return result
    except ExternalAPIError as e:
        failures.labels(type='api').inc()
        raise  # Re-raise immediately
```

---

## Language-Specific Patterns

### Python: Raise, Don't Return None
```python
# ✅ Pythonic fail-fast
def get_user(user_id: int) -> User:
    user = db.query(User).get(user_id)
    if user is None:
        raise UserNotFoundError(f"User {user_id} not found")
    return user
```

### Rust: Result<T, E> Types
```rust
// ✅ Rust-style explicit errors
fn parse_age(input: &str) -> Result<u8, ParseError> {
    input.parse::<u8>()
        .map_err(|_| ParseError::InvalidAge(input.to_string()))
}
```

### Go: Error Returns + Check Immediately
```go
// ✅ Go-style error handling
if err := validateInput(data); err != nil {
    return fmt.Errorf("validation failed: %w", err)
}
```

### TypeScript: Throw on Invalid State
```typescript
// ✅ TypeScript fail-fast
function processOrder(order: Order): Receipt {
    if (order.items.length === 0) {
        throw new Error("Cannot process empty order");
    }
    // ... process
}
```

---

## Testing Fail-Fast Behavior

### Test That Failures Fail
```python
# Test that invalid input causes immediate failure
def test_fail_fast_on_invalid_user():
    with pytest.raises(UserNotFoundError):
        get_user(user_id=99999)  # Should raise, not return None

def test_fail_fast_on_invalid_amount():
    with pytest.raises(ValueError, match="Amount must be positive"):
        process_payment(amount=-10)

# ❌ BAD: Test passes when it should fail
def test_bad():
    result = get_user(99999)  # Returns None silently
    assert result is None  # Test passes but behavior is wrong!
```

---

## Migration Strategy

### Phase 1: Identify Silent Failures (Week 1)
```bash
# Find catch-all exception handlers
grep -r "except:" . --include="*.py"
grep -r "catch (e)" . --include="*.js"

# Find functions returning null on error
grep -r "return None" . --include="*.py"
grep -r "return null" . --include="*.js"
```

### Phase 2: Add Fail-Fast Assertions (Week 2-3)
```python
# Add assertions to document invariants
def calculate_discount(price: float, discount: float) -> float:
    assert price >= 0, "Price cannot be negative"
    assert 0 <= discount <= 1, "Discount must be between 0 and 1"
    return price * (1 - discount)
```

### Phase 3: Refactor Exception Handlers (Week 4+)
```python
# Before: Catch-all
try:
    process()
except:
    pass

# After: Specific + re-raise
try:
    process()
except ValueError as e:
    logger.error(f"Validation error: {e}")
    raise
except NetworkError as e:
    logger.error(f"Network error: {e}")
    raise
# Unexpected errors propagate automatically
```

---

## Summary

**Fail-Fast Error Handling** means errors cause immediate, visible failure instead of silent continuation. This prevents error accumulation, data corruption, and debugging nightmares.

**Core Rule**: If an operation fails, STOP IMMEDIATELY. Don't log-and-continue, don't return null, don't catch-all exceptions.
