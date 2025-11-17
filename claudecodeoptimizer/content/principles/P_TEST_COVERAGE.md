# P_TEST_COVERAGE: Test Coverage Targets

**Severity**: High

 Missing tests mean bugs in uncovered code discovered in production Refactoring untested code breaks functionality without warning Can't confidently change code without tests Edge cases and error path.

---

## Rules

- *No rules extracted*

---

## Examples

### ✅ Good
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
```
**Why right**: ---

### ❌ Bad
```python
# ❌ BAD: 100% coverage but tests don't verify behavior

def transfer_funds(from_account, to_account, amount):
    if amount <= 0:
        raise ValueError("Amount must be positive")

    if from_account.balance < amount:
        raise ValueError("Insufficient funds")

    from_account.balance -= amount
    to_account.balance += amount
```
**Why wrong**: ---
