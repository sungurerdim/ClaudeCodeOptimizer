---
id: C_PRODUCTION_GRADE
title: Production-Grade Code Only
category: claude-guidelines
severity: critical
weight: 10
applicability:
  project_types: ['all']
  languages: ['all']
---

# C_PRODUCTION_GRADE: Production-Grade Code Only 🔴

**Severity**: Critical

Write production-ready code from the first line. No TODO markers, debug prints, placeholder implementations, or incomplete error handling. Every line of code should be deployment-ready.

**Enforcement**: MUST

**Project Types**: all
**Languages**: all

---

## Why

### The Problem

**Non-production code creates technical debt and quality issues:**

- **TODO Accumulation** - "Temporary" TODOs become permanent, accumulating technical debt that never gets addressed
- **Debug Print Pollution** - Console.log/print statements leak sensitive data, slow performance, and clutter logs
- **Incomplete Error Handling** - Missing try/catch blocks cause production crashes from edge cases
- **Placeholder Code** - "Return null for now" implementations create silent failures in production
- **Security Holes** - Placeholder auth checks like "if true" bypass real security
- **Performance Issues** - Debug code paths (deep logging, assertions) slow production systems

### Business Value

- **Zero technical debt** - No cleanup phase needed; code is production-ready immediately
- **Always deployable** - Every commit can go to production without cleanup or "hardening"
- **Reduced bugs** - Complete error handling and edge case coverage from day one
- **Faster reviews** - No "we'll fix it later" discussions; code is complete
- **Better security** - No placeholder auth/validation that gets forgotten

### Technical Benefits

- **Complete from start** - All code paths implemented, all errors handled
- **Proper logging** - Structured logging instead of debug prints
- **Error resilience** - Comprehensive error handling prevents crashes
- **Performance ready** - No debug overhead in production builds
- **Maintainable** - Future developers don't inherit debt or cleanup tasks

### Industry Evidence

- **Google SRE** - "Code should be production-ready before merge; no TODOs in production"
- **Microsoft DevOps** - Teams with strict quality gates deploy 200x more frequently
- **Amazon** - "You build it, you run it" culture requires production-grade code from start
- **Technical Debt Studies** - Every TODO has 70% chance of never being addressed
- **Production Incident Analysis** - 40% of critical bugs traced to "temporary" code

---

## How

### Core Techniques

**1. Complete Implementations**

Never commit incomplete code with TODOs:

```python
# ❌ BAD: Incomplete with TODO
def process_payment(amount):
    # TODO: Add validation
    # TODO: Handle errors
    return payment_api.charge(amount)

# ✅ GOOD: Complete implementation
def process_payment(amount: Decimal) -> PaymentResult:
    """Process payment with full validation and error handling."""
    if amount <= 0:
        raise ValueError(f"Invalid amount: {amount}")
    if amount > MAX_TRANSACTION:
        raise ValueError(f"Amount exceeds maximum: {MAX_TRANSACTION}")

    try:
        result = payment_api.charge(amount)
        logger.info("Payment processed", extra={"amount": amount, "tx_id": result.id})
        return result
    except PaymentAPIError as e:
        logger.error("Payment failed", extra={"amount": amount, "error": str(e)})
        raise PaymentProcessingError(f"Payment failed: {e}") from e
```

**2. Proper Logging Instead of Prints**

Use structured logging, never print/console.log:

```python
# ❌ BAD: Debug prints
def authenticate_user(username, password):
    print(f"Authenticating {username}")  # Leaks username to console!
    print(f"Password: {password}")       # CRITICAL SECURITY ISSUE!
    result = auth_service.verify(username, password)
    print(f"Result: {result}")
    return result

# ✅ GOOD: Structured logging
def authenticate_user(username: str, password: str) -> AuthResult:
    """Authenticate user with proper logging."""
    logger.info("Authentication attempt", extra={"username": username})

    try:
        result = auth_service.verify(username, password)
        logger.info("Authentication successful", extra={"username": username})
        return result
    except AuthenticationError as e:
        logger.warning("Authentication failed", extra={"username": username, "reason": str(e)})
        raise
```

**3. Comprehensive Error Handling**

Handle all error cases, no bare try/catch or unhandled exceptions:

```python
# ❌ BAD: Incomplete error handling
def fetch_user_data(user_id):
    # FIXME: Add error handling
    response = api.get(f"/users/{user_id}")
    return response.json()

# ✅ GOOD: Complete error handling
def fetch_user_data(user_id: int) -> UserData:
    """Fetch user data with comprehensive error handling."""
    if user_id <= 0:
        raise ValueError(f"Invalid user_id: {user_id}")

    try:
        response = api.get(f"/users/{user_id}", timeout=5.0)
        response.raise_for_status()
        return UserData.from_dict(response.json())

    except requests.Timeout:
        logger.error("API timeout", extra={"user_id": user_id})
        raise APITimeoutError(f"Timeout fetching user {user_id}")

    except requests.HTTPError as e:
        if e.response.status_code == 404:
            logger.info("User not found", extra={"user_id": user_id})
            raise UserNotFoundError(f"User {user_id} not found")
        logger.error("HTTP error", extra={"user_id": user_id, "status": e.response.status_code})
        raise APIError(f"HTTP {e.response.status_code}: {e}")

    except ValueError as e:
        logger.error("Invalid response data", extra={"user_id": user_id, "error": str(e)})
        raise DataValidationError(f"Invalid user data: {e}") from e
```

**4. No Placeholder Code**

Never commit placeholder returns or implementations:

```python
# ❌ BAD: Placeholder implementation
def validate_email(email):
    # TODO: Implement validation
    return True  # Placeholder - accepts anything!

def check_permissions(user, resource):
    return True  # HACK: Bypass auth for testing

# ✅ GOOD: Real implementation
import re
EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

def validate_email(email: str) -> bool:
    """Validate email format according to RFC 5322."""
    if not email or not isinstance(email, str):
        return False
    if len(email) > 254:  # RFC 5321
        return False
    return EMAIL_PATTERN.match(email) is not None

def check_permissions(user: User, resource: Resource) -> bool:
    """Check if user has access to resource."""
    if user.is_admin:
        return True
    if resource.owner_id == user.id:
        return True
    if resource.id in user.granted_resource_ids:
        return True
    logger.warning("Permission denied", extra={"user_id": user.id, "resource_id": resource.id})
    return False
```

**5. Remove All Debug Code**

No console.log, print, debugger statements:

```javascript
// ❌ BAD: Debug code left in
function processOrder(order) {
    console.log("Processing order:", order);  // Debug
    debugger;  // Left from debugging session!
    console.log("Order items:", order.items);

    const total = order.items.reduce((sum, item) => {
        console.log("Item:", item);  // More debug spam
        return sum + item.price;
    }, 0);

    console.log("Total:", total);
    return total;
}

// ✅ GOOD: Clean production code
import logger from './logger';

function processOrder(order: Order): number {
    logger.debug('Processing order', { orderId: order.id, itemCount: order.items.length });

    const total = order.items.reduce((sum, item) => sum + item.price, 0);

    logger.info('Order processed', { orderId: order.id, total });
    return total;
}
```

---

### Implementation Patterns

#### ✅ Good: Production-Ready Function

```python
def transfer_funds(
    from_account: str,
    to_account: str,
    amount: Decimal,
    idempotency_key: str
) -> TransferResult:
    """
    Transfer funds between accounts with full error handling and validation.

    Args:
        from_account: Source account ID
        to_account: Destination account ID
        amount: Transfer amount (must be positive)
        idempotency_key: Unique key to prevent duplicate transfers

    Returns:
        TransferResult with transaction details

    Raises:
        ValueError: Invalid parameters
        InsufficientFundsError: Source account has insufficient balance
        AccountNotFoundError: Account doesn't exist
        DuplicateTransferError: Idempotency key already used
    """
    # Validate inputs
    if amount <= 0:
        raise ValueError(f"Amount must be positive: {amount}")
    if not from_account or not to_account:
        raise ValueError("Account IDs required")
    if from_account == to_account:
        raise ValueError("Cannot transfer to same account")

    # Check idempotency
    if transfer_exists(idempotency_key):
        logger.info("Duplicate transfer detected", extra={"idempotency_key": idempotency_key})
        raise DuplicateTransferError(f"Transfer already processed: {idempotency_key}")

    # Perform transfer with transaction safety
    try:
        with database.transaction():
            from_balance = accounts.get_balance(from_account)
            if from_balance < amount:
                raise InsufficientFundsError(
                    f"Insufficient funds: {from_balance} < {amount}"
                )

            accounts.debit(from_account, amount)
            accounts.credit(to_account, amount)

            transfer = Transfer(
                from_account=from_account,
                to_account=to_account,
                amount=amount,
                idempotency_key=idempotency_key,
                timestamp=datetime.utcnow()
            )
            transfers.save(transfer)

            logger.info("Transfer completed", extra={
                "from": from_account,
                "to": to_account,
                "amount": str(amount),
                "transfer_id": transfer.id
            })

            return TransferResult(
                transfer_id=transfer.id,
                status="completed",
                amount=amount
            )

    except AccountNotFoundError as e:
        logger.error("Account not found", extra={"error": str(e)})
        raise
    except DatabaseError as e:
        logger.error("Database error during transfer", extra={"error": str(e)})
        raise TransferError(f"Transfer failed: {e}") from e
```

**Why it's production-grade:**
- Complete docstring with args, returns, raises
- Input validation for all parameters
- Idempotency check prevents duplicates
- Transaction safety for atomicity
- Comprehensive error handling
- Structured logging (no prints)
- Type hints for clarity
- Business logic complete (no TODOs)

---

#### ❌ Bad: Non-Production Code

```python
def transfer_funds(from_account, to_account, amount):
    # TODO: Add validation
    # TODO: Check balance
    # FIXME: Use transactions
    print(f"Transferring {amount} from {from_account} to {to_account}")  # Debug

    # HACK: Bypassing balance check for testing
    # if get_balance(from_account) < amount:
    #     return None

    debit(from_account, amount)
    credit(to_account, amount)

    print("Transfer complete")  # Debug
    return True  # TODO: Return proper result object
```

**Why it's non-production:**
- TODOs indicate incomplete implementation
- No input validation
- Debug prints leak transaction data
- Commented-out critical logic (HACK)
- No error handling
- No logging
- Returns boolean instead of rich result
- No type hints
- No documentation

---

## Anti-Patterns

### ❌ Anti-Pattern 1: TODO Comments

**Problem**: TODOs rarely get addressed and accumulate technical debt.

```python
# ❌ BAD: TODOs everywhere
def create_user(email, password):
    # TODO: Validate email format
    # TODO: Check password strength
    # TODO: Hash password
    # TODO: Check for duplicate emails
    # FIXME: Add proper error handling
    user = User(email=email, password=password)
    db.save(user)
    return user

# ✅ GOOD: Complete implementation
import bcrypt
from email_validator import validate_email

def create_user(email: str, password: str) -> User:
    """Create user with validation, password hashing, and duplicate checking."""
    # Validate email
    try:
        valid = validate_email(email)
        email = valid.email
    except EmailNotValidError as e:
        raise ValueError(f"Invalid email: {e}")

    # Check password strength
    if len(password) < 12:
        raise ValueError("Password must be at least 12 characters")
    if not any(c.isupper() for c in password):
        raise ValueError("Password must contain uppercase letter")
    if not any(c.isdigit() for c in password):
        raise ValueError("Password must contain digit")

    # Check for duplicates
    if db.user_exists(email):
        raise DuplicateUserError(f"User already exists: {email}")

    # Hash password
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Create user
    user = User(email=email, password_hash=password_hash)
    db.save(user)

    logger.info("User created", extra={"email": email, "user_id": user.id})
    return user
```

**Impact:**
- TODOs rarely get fixed (70% never addressed)
- Creates false sense of completeness
- Security holes in production

---

### ❌ Anti-Pattern 2: Debug Prints in Production

**Problem**: Print statements leak data, clutter logs, slow performance.

```javascript
// ❌ BAD: Console.log everywhere
function loginUser(username, password) {
    console.log("Login attempt:", username, password);  // SECURITY ISSUE!

    const user = db.getUser(username);
    console.log("User object:", user);  // Leaks user data

    if (user && checkPassword(password, user.passwordHash)) {
        console.log("Login successful");
        console.log("Session token:", createSession(user));  // Leaks token!
        return user;
    }

    console.log("Login failed");
    return null;
}

// ✅ GOOD: Structured logging
import logger from './logger';

function loginUser(username: string, password: string): User | null {
    logger.info('Login attempt', { username });

    const user = db.getUser(username);
    if (!user) {
        logger.warning('Login failed - user not found', { username });
        return null;
    }

    if (!checkPassword(password, user.passwordHash)) {
        logger.warning('Login failed - invalid password', { username });
        return null;
    }

    const session = createSession(user);
    logger.info('Login successful', { username, userId: user.id });
    return user;
}
```

**Impact:**
- Passwords, tokens leaked to console
- Production logs cluttered
- Performance degradation

---

### ❌ Anti-Pattern 3: Placeholder Implementations

**Problem**: Placeholder code bypasses critical logic.

```python
# ❌ BAD: Placeholder that bypasses security
def check_admin(user):
    return True  # HACK: Bypass for testing

def validate_input(data):
    return data  # TODO: Sanitize inputs

def rate_limit_check(user):
    return True  # FIXME: Implement rate limiting

# ✅ GOOD: Real implementations
def check_admin(user: User) -> bool:
    """Check if user has admin privileges."""
    if not user:
        return False
    return 'admin' in user.roles or user.is_superuser

def validate_input(data: str) -> str:
    """Sanitize and validate user input."""
    if not data:
        raise ValueError("Input required")

    # Remove dangerous characters
    sanitized = html.escape(data)

    # Enforce length limits
    if len(sanitized) > MAX_INPUT_LENGTH:
        raise ValueError(f"Input exceeds maximum length: {MAX_INPUT_LENGTH}")

    return sanitized

def rate_limit_check(user: User) -> bool:
    """Check if user is within rate limits."""
    key = f"rate_limit:{user.id}"
    count = redis.get(key) or 0

    if int(count) >= RATE_LIMIT_PER_MINUTE:
        logger.warning("Rate limit exceeded", extra={"user_id": user.id})
        return False

    redis.incr(key)
    redis.expire(key, 60)  # Reset after 1 minute
    return True
```

**Impact:**
- Security bypasses go to production
- Critical validation missing
- Silent failures

---

## Implementation Checklist

### Code Quality

- [ ] **No TODO/FIXME/HACK** - Remove all marker comments; complete implementations
- [ ] **No debug prints** - Remove console.log, print, debugger statements
- [ ] **Complete error handling** - Handle all error cases with specific exceptions
- [ ] **Proper logging** - Use structured logging, never print
- [ ] **Type hints/annotations** - Add types for all function parameters and returns

### Validation & Security

- [ ] **Input validation** - Validate all inputs with specific error messages
- [ ] **Edge case handling** - Test and handle boundary conditions
- [ ] **Security checks** - Implement real auth/authz, no placeholders
- [ ] **Rate limiting** - Implement where applicable
- [ ] **Sanitization** - Sanitize all user inputs

### Documentation

- [ ] **Docstrings complete** - Document args, returns, raises
- [ ] **Inline comments** - Explain complex logic, not what code does
- [ ] **README updated** - Document any new features or changes
- [ ] **API docs current** - Update OpenAPI/Swagger if API changed

### Testing & Verification

- [ ] **Unit tests pass** - All tests green before commit
- [ ] **Integration tests** - Test critical paths end-to-end
- [ ] **Manual verification** - Test in local environment
- [ ] **No skipped tests** - Fix or remove skipped/ignored tests

---

## Cross-References

**Related Principles:**

- **U_TEST_FIRST** - Write tests first to ensure complete implementations
- **U_FAIL_FAST** - Proper error handling fails fast with clear errors
- **U_NO_OVERENGINEERING** - Production-grade doesn't mean over-engineered
- **C_CROSS_PLATFORM_BASH** - Production code must work on all platforms
- **P_LINTING_SAST** - Linters catch TODOs, prints, and incomplete code

**Workflow Integration:**
- Configure linters to fail on TODO/FIXME/HACK comments
- Pre-commit hooks check for console.log/print statements
- CI gates require 100% test coverage
- Code review checklist includes production-grade criteria

---

## Summary

**Production-Grade Code Only** means writing deployment-ready code from the first line: complete implementations, proper error handling, structured logging, no TODOs, and no debug code.

**Core Rules:**

- **No TODOs** - Complete all implementations; no "we'll fix it later"
- **No debug prints** - Use structured logging, never console.log/print
- **Complete error handling** - Handle all error cases with specific exceptions
- **No placeholders** - No `return True` bypasses or stub implementations
- **Proper logging** - Structured, searchable logs; no sensitive data

**Remember**: "Every line deployment-ready. No TODOs. No prints. No placeholders. Production-grade from day one."

**Impact**: Zero technical debt, always deployable, reduced bugs, faster reviews, better security, no cleanup phase needed.

---

**Quality Gates:**
```
Pre-Commit:
  ✓ No TODO/FIXME/HACK comments
  ✓ No console.log/print statements
  ✓ No debugger statements
  ✓ All tests pass
  ✓ Linting passes

Code Review:
  ✓ Complete error handling
  ✓ Input validation present
  ✓ Proper logging (no prints)
  ✓ Type hints/annotations
  ✓ Documentation complete

CI/CD:
  ✓ Unit tests pass
  ✓ Integration tests pass
  ✓ Security scans pass
  ✓ Performance acceptable
  ✓ Cross-platform verified
```
