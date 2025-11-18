---
name: code_documentation_standards
description: Document code through docstrings, comments, and architectural guides
type: project
severity: high
keywords: [documentation, code, docstrings, standards]
category: [docs]
related_skills: []
---
# P_CODE_DOCUMENTATION_STANDARDS: Code Documentation Standards

**Severity**: High

Onboarding takes weeks without docs Complex logic modified incorrectly (intent not documented) Team departures take undocumented knowledge Review delays for complex code without explanation Security a.

---

## Rules

- *No rules extracted*

---

## Examples

### ✅ Good
```python
from typing import List, Dict
from decimal import Decimal

def calculate_invoice_total(
    items: List[Dict[str, float]],
    tax_rate: float = 0.08,
    discount_percentage: float = 0,
    currency: str = "USD"
) -> Decimal:
    """
    Calculate invoice total with tax and discount.

    Workflow: Sum items → Apply discount → Calculate tax → Return total
    Why this order: Discounts reduce taxable amount in most jurisdictions.

    Args:
```
**Why right**: **Why it's good:** Clear purpose, parameter constraints, error conditions, examples, WHY explanation

### ❌ Bad
```python
# ❌ BAD: Insufficient documentation
def calc_total(items, tax=0.08, disc=0):
    """Calculate total."""  # Too vague!
    total = sum([item['p'] * item['q'] for item in items])
    total = total * (1 - disc)  # Discount calculation unexplained
    return round(total * (1 + tax), 2)  # Why round? Why 2 decimals?

# Problems: No parameter descriptions, no examples, algorithm unexplained
```
**Why wrong**: ---
