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

# C_PRODUCTION_GRADE: Production-Grade Code Only

**Severity**: Critical

Write production-ready code from the first line. No TODO markers, debug prints, placeholder implementations, or incomplete error handling. Every line should be deployment-ready.

**Enforcement**: MUST

---

## Why

**Non-production code creates technical debt:**

- **TODO Accumulation** - "Temporary" TODOs become permanent technical debt
- **Debug Print Pollution** - console.log/print leak sensitive data and clutter logs
- **Incomplete Error Handling** - Missing try/catch causes production crashes
- **Placeholder Code** - "Return null for now" creates silent failures
- **Security Holes** - Placeholder auth like "if true" bypasses real security

---

## Core Patterns

### 1. Complete Implementations (No TODOs)

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

### 2. Proper Logging (Never Print)

```python
# ❌ BAD: Debug prints
def authenticate_user(username, password):
    print(f"Authenticating {username}")  # Leaks username!
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

### 3. Comprehensive Error Handling

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
            raise UserNotFoundError(f"User {user_id} not found")
        logger.error("HTTP error", extra={"user_id": user_id, "status": e.response.status_code})
        raise APIError(f"HTTP {e.response.status_code}: {e}")

    except ValueError as e:
        logger.error("Invalid response data", extra={"user_id": user_id})
        raise DataValidationError(f"Invalid user data: {e}") from e
```

---

## Production-Ready Example

### ✅ Complete Production Function

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

    Raises:
        ValueError: Invalid parameters
        InsufficientFundsError: Source account has insufficient balance
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
                raise InsufficientFundsError(f"Insufficient funds: {from_balance} < {amount}")

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

            return TransferResult(transfer_id=transfer.id, status="completed", amount=amount)

    except AccountNotFoundError as e:
        logger.error("Account not found", extra={"error": str(e)})
        raise
    except DatabaseError as e:
        logger.error("Database error during transfer", extra={"error": str(e)})
        raise TransferError(f"Transfer failed: {e}") from e
```

### ❌ Non-Production Equivalent

```python
def transfer_funds(from_account, to_account, amount):
    # TODO: Add validation
    # TODO: Check balance
    # FIXME: Use transactions
    print(f"Transferring {amount} from {from_account} to {to_account}")

    # HACK: Bypassing balance check for testing
    # if get_balance(from_account) < amount:
    #     return None

    debit(from_account, amount)
    credit(to_account, amount)

    print("Transfer complete")
    return True  # TODO: Return proper result object
```

**Problems with non-production code:**
- TODOs indicate incomplete implementation
- No input validation
- Debug prints leak transaction data
- Commented-out critical logic (HACK)
- No error handling or logging
- Returns boolean instead of rich result

---

## Anti-Patterns

### ❌ Placeholder Implementations

```python
# ❌ BAD: Placeholders that bypass security
def check_admin(user):
    return True  # HACK: Bypass for testing

def validate_input(data):
    return data  # TODO: Sanitize inputs

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

    sanitized = html.escape(data)

    if len(sanitized) > MAX_INPUT_LENGTH:
        raise ValueError(f"Input exceeds maximum length: {MAX_INPUT_LENGTH}")

    return sanitized
```

**Impact:**
- Security bypasses go to production
- Critical validation missing
- Silent failures

---

## Implementation Checklist

### Code Quality

- [ ] **No TODO/FIXME/HACK** - Complete all implementations
- [ ] **No debug prints** - Remove console.log, print, debugger
- [ ] **Complete error handling** - Handle all error cases
- [ ] **Proper logging** - Use structured logging, never print
- [ ] **Type hints** - Add types for parameters and returns

### Validation & Security

- [ ] **Input validation** - Validate all inputs with error messages
- [ ] **Edge case handling** - Test boundary conditions
- [ ] **Security checks** - Implement real auth/authz, no placeholders
- [ ] **Sanitization** - Sanitize all user inputs

### Documentation

- [ ] **Docstrings complete** - Document args, returns, raises
- [ ] **Inline comments** - Explain complex logic (not what code does)

### Testing

- [ ] **Unit tests pass** - All tests green before commit
- [ ] **Manual verification** - Test in local environment

---

## Summary

**Production-Grade Code Only** means writing deployment-ready code from the first line: complete implementations, proper error handling, structured logging, no TODOs, and no debug code.

**Core Rules:**

- **No TODOs** - Complete all implementations; no "we'll fix it later"
- **No debug prints** - Use structured logging, never console.log/print
- **Complete error handling** - Handle all error cases with specific exceptions
- **No placeholders** - No `return True` bypasses or stub implementations
- **Proper logging** - Structured, searchable logs; no sensitive data
