---
name: type-safety
description: Use type annotations and static analysis to catch errors before runtime
type: project
severity: high
keywords: ["types", "type-safety", "static-analysis", "mypy", "quality"]
category: ["quality"]
related_skills: []
---

# P_TYPE_SAFETY: Type Safety & Static Analysis

**Severity**: High

 Type errors discovered in production, not during development `AttributeError`, `TypeError`, `None`-related crashes in production Can't confidently refactor without knowing what breaks Unclear functio.

---

## Rules

- *No rules extracted*

---

## Examples

### ✅ Good
```python
# Complete type annotations for module

from typing import Optional, List, Dict, Union
from decimal import Decimal
from models import User, Product

class ShoppingCart:
    """Shopping cart with type-safe operations."""

    def __init__(self, user: User) -> None:
        self.user: User = user
        self.items: List[Product] = []

    def add_item(self, product: Product, quantity: int = 1) -> None:
        """Add product to cart with quantity."""
        if quantity <= 0:
```
**Why right**: ---

### ❌ Bad
```python
# ❌ BAD: No types, mypy can't help

def process_payment(cart, user, method):
    total = cart.calculate_total()

    if method == "credit":
        return charge_credit_card(user.card, total)
    elif method == "paypal":
        return charge_paypal(user.paypal_email, total)
    else:
        return None
```
**Why wrong**: ---
