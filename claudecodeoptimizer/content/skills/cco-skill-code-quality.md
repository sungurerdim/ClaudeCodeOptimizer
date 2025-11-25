---
name: cco-skill-code-quality
description: Manage code quality through complexity reduction and technical debt tracking. Includes cyclomatic/cognitive complexity limits, code smell detection, refactoring patterns (Extract Method, Split Class), and debt prioritization with impact/effort analysis.
keywords: [refactor, complexity, code smell, technical debt, maintainability, cyclomatic, cognitive, duplication, SOLID, clean code]
category: quality
related_commands:
  action_types: [audit, fix, optimize]
  categories: [quality]
pain_points: [1, 2, 3]
---

# Skill: Code Quality & Refactoring

> **Standards:** Format defined in [cco-standards.md](../cco-standards.md)  
> **Discovery:** See [cco-standards.md](../cco-standards.md#18-command-discovery-protocol)


## Domain
Code quality, refactoring, complexity management

## Purpose
Manage code quality through complexity reduction and technical debt tracking.

**Solves**: Unmaintainable code (complexity >10), technical debt accumulation, code smells, slow feature velocity

**Impact**: High
---

---

## Guidance Areas

### Code Smell Detection
Automated detection of duplication, long methods, god objects, feature envy

### Refactoring Patterns
Safe refactoring techniques (Extract Method, Replace Conditional) with automated tests

### Technical Debt Tracking
Quantify, prioritize, schedule debt paydown (interest rate, principal, impact)

### Cyclomatic Complexity Limits
Functions >10 cyclomatic complexity exponentially harder to test/debug

### Cognitive Complexity
Cognitive complexity >15 exceeds working memory capacity

### Fail-Fast Strategy
Fail immediately on invalid conditions vs propagating errors

### Integration Check
Prevent dead code, ensure all paths reachable and tested

### Production Grade
No TODOs, placeholders, or incomplete implementations in production

---

## Activation

Auto-loads on: refactor, complexity, code smell, technical debt, maintainability keywords

---

## Examples

**Complexity Detection**
```
User: "Review this function" (cyclomatic complexity 18)
Result: Flags violation, suggests Extract Method to reduce <10
```

**Code Smell**
```
User: "Class hard to maintain" (1200 lines, 30 methods)
Result: Identifies God Object, suggests Split Class by responsibility
```

**Refactoring**
```
User: "Refactor duplicated code across 5 files"
Result: Applies Extract Function, creates shared module, updates 5 files
```

**Technical Debt**
```
User: "Prioritize TODO comments"
Result: Scans codebase, categorizes by impact/effort, generates paydown roadmap
```

---

## Analysis Patterns (Claude Executes)

When auditing tech debt or code quality, use these analysis patterns:

### Code Smell Detection

```bash
# 1. Large files (>300 lines)
find . -name "*.py" -type f ! -path "*/venv/*" ! -path "*/__pycache__/*" -exec wc -l {} \; | awk '$1 > 300 {print}'

# 2. TODO/FIXME/HACK markers
grep -rn "TODO\|FIXME\|HACK\|XXX\|BUG\|OPTIMIZE" --include="*.py" --include="*.js" --include="*.ts" .

# 3. Console/print statements (debug leftovers)
grep -rn "console\.log\|print(" --include="*.py" --include="*.js" --include="*.ts" .

# 4. Deep nesting (>4 levels)
grep -n "^        " --include="*.py" -r . | grep "if \|for \|while \|try:\|with "

# 5. Parameter bloat (>5 parameters)
grep -rn "def .*(.*, .*, .*, .*, .*)" --include="*.py" .
```

### Complexity Analysis

```bash
# Using radon (if installed)
radon cc -s -a --min C .

# Using flake8 with mccabe
flake8 --max-complexity 10 --select=C901 .

# Manual complexity indicators
grep -rn "if \|elif \|for \|while \|and \|or \|except " --include="*.py" . | \
  awk -F: '{files[$1]++} END {for (f in files) if (files[f] > 15) print f, files[f]}'
```

### Dependency Analysis

```bash
# 1. Outdated packages
pip list --outdated --format=columns

# 2. Unused imports (use ruff)
ruff check --select=F401 .

# 3. Security vulnerabilities
pip-audit  # or: safety check
```

### Dead Code Detection

```bash
# 1. Comprehensive dead code (use vulture)
vulture . --min-confidence 80

# 2. Commented-out code blocks
grep -rn "^#.*def \|^#.*class \|^#.*if \|^#.*for " --include="*.py" .
```

---

## Technical Debt Register Template

```markdown
## Technical Debt Register

| ID | Category | Description | File:Line | Severity | Effort | Interest | Status |
|----|----------|-------------|-----------|----------|--------|----------|--------|
| TD-001 | Quality | Function complexity=18 | {file}:{line} | High | 2h | High | Open |
| TD-002 | Architecture | Tight coupling | {module_a}↔{module_b} | Medium | 4h | Medium | Open |
| TD-003 | Test | Missing payment tests | src/payments/ | Critical | 8h | Critical | Open |

### Severity
- **Critical**: Blocking production quality
- **High**: Fix this sprint
- **Medium**: Fix within month
- **Low**: Fix when convenient

### Interest Rate (cost over time)
- **Critical**: Daily (bugs, incidents)
- **High**: Weekly (slowdowns)
- **Medium**: Monthly (maintenance)
- **Low**: Stable

### Sprint Allocation
- 20% of sprint for debt paydown
- Prioritize: Interest > Severity > Effort
```

---

## Debt Categories

1. **Code Quality** - Complexity, long methods, smells
2. **Architecture** - Coupling, patterns, boundaries
3. **Test** - Missing tests, low coverage, flaky
4. **Documentation** - Missing/outdated docs
5. **Dependency** - Outdated packages, CVEs
6. **Performance** - N+1, no caching, slow algos
7. **Security** - Vulnerabilities, weak auth
8. **Infrastructure** - Manual deploys, no CI/CD
9. **Design** - God objects, feature envy

---

## Core Refactoring Patterns

### Extract Method

**When**: Function doing multiple things, repeated code blocks

```python
# ❌ BAD: Mixed responsibilities
def process_order(order):
    # Validate
    if not order.items:
        raise ValueError("Empty order")
    if order.total < 0:
        raise ValueError("Invalid total")

    # Calculate tax
    tax = order.total * 0.08
    total_with_tax = order.total + tax

    # Send notification
    message = f"Order {order.id}: ${total_with_tax}"
    send_email(order.user.email, message)
    send_sms(order.user.phone, message)

    return total_with_tax

# ✅ GOOD: Single responsibility per function
def process_order(order):
    validate_order(order)
    total = calculate_total_with_tax(order)
    notify_user(order, total)
    return total

def validate_order(order):
    if not order.items:
        raise ValueError("Empty order")
    if order.total < 0:
        raise ValueError("Invalid total")

def calculate_total_with_tax(order, tax_rate=0.08):
    return order.total * (1 + tax_rate)

def notify_user(order, total):
    message = f"Order {order.id}: ${total}"
    send_email(order.user.email, message)
    send_sms(order.user.phone, message)
```

### Replace Conditional with Polymorphism

**When**: Switch/if-elif chains based on type

```python
# ❌ BAD: Type-based conditionals
def calculate_shipping(item):
    if item.type == "book":
        return 2.99
    elif item.type == "electronics":
        return 9.99 if item.weight > 2 else 5.99
    elif item.type == "clothing":
        return 4.99
    else:
        return 7.99

# ✅ GOOD: Polymorphism
class ShippingStrategy:
    def calculate(self, item): raise NotImplementedError

class BookShipping(ShippingStrategy):
    def calculate(self, item): return 2.99

class ElectronicsShipping(ShippingStrategy):
    def calculate(self, item):
        return 9.99 if item.weight > 2 else 5.99

class ClothingShipping(ShippingStrategy):
    def calculate(self, item): return 4.99

SHIPPING_STRATEGIES = {
    "book": BookShipping(),
    "electronics": ElectronicsShipping(),
    "clothing": ClothingShipping(),
}

def calculate_shipping(item):
    strategy = SHIPPING_STRATEGIES.get(item.type)
    return strategy.calculate(item) if strategy else 7.99
```

### Introduce Parameter Object

**When**: Functions with 5+ parameters

```python
# ❌ BAD: Parameter bloat
def create_user(name, email, phone, address, city, state, zip_code, country):
    ...

# ✅ GOOD: Parameter object
@dataclass
class Address:
    street: str
    city: str
    state: str
    zip_code: str
    country: str

@dataclass
class UserData:
    name: str
    email: str
    phone: str
    address: Address

def create_user(user_data: UserData):
    ...
```

### Replace Magic Numbers

```python
# ❌ BAD: Magic numbers
if user.age >= 21:
    if order.total >= 50:
        discount = order.total * 0.1

# ✅ GOOD: Named constants
LEGAL_DRINKING_AGE = 21
FREE_SHIPPING_THRESHOLD = 50
LOYALTY_DISCOUNT_RATE = 0.1

if user.age >= LEGAL_DRINKING_AGE:
    if order.total >= FREE_SHIPPING_THRESHOLD:
        discount = order.total * LOYALTY_DISCOUNT_RATE
```

---

## Code Smells Catalog

### Long Method (>20 lines)

**Symptom**: Function does too much
**Fix**: Extract Method, decompose into smaller functions

### Large Class (>300 lines)

**Symptom**: God object with too many responsibilities
**Fix**: Split Class by responsibility (Single Responsibility Principle)

### Feature Envy

**Symptom**: Method uses another class's data more than its own
```python
# ❌ Feature envy
def calculate_bonus(employee):
    return employee.salary * employee.years * employee.performance_rating / 100

# ✅ Move to Employee class
class Employee:
    def calculate_bonus(self):
        return self.salary * self.years * self.performance_rating / 100
```

### Data Clumps

**Symptom**: Same group of variables always together
```python
# ❌ Data clump
def process(start_x, start_y, end_x, end_y):
    ...

# ✅ Introduce object
@dataclass
class Point:
    x: int
    y: int

def process(start: Point, end: Point):
    ...
```

### Primitive Obsession

**Symptom**: Using primitives for domain concepts
```python
# ❌ Primitive
def send_email(to: str):  # What format? Valid?
    ...

# ✅ Domain type
class Email:
    def __init__(self, address: str):
        if "@" not in address:
            raise ValueError("Invalid email")
        self.address = address

def send_email(to: Email):
    ...
```

### Dead Code

**Symptom**: Unreachable or unused code
```python
# ❌ Dead code
def calculate(x):
    return x * 2
    print("Done")  # Never executed

# ✅ Remove dead code
def calculate(x):
    return x * 2
```

---

## Complexity Metrics

### Cyclomatic Complexity

**Formula**: `Edges - Nodes + 2` (simplified: count decision points + 1)

| Complexity | Risk Level | Action |
|------------|------------|--------|
| 1-5 | Low | OK |
| 6-10 | Moderate | Monitor |
| 11-20 | High | Refactor |
| >20 | Very High | Split immediately |

```python
# Complexity = 1 (no decisions)
def simple():
    return 42

# Complexity = 4 (3 decisions + 1)
def moderate(x, y):
    if x > 0:      # +1
        if y > 0:  # +1
            return x + y
        else:
            return x - y
    elif x < 0:    # +1
        return -x
    return 0
```

### Cognitive Complexity

Measures how hard code is to understand (not just control flow).

```python
# Low cognitive (linear)
def process(items):
    total = 0
    for item in items:
        total += item.price
    return total

# High cognitive (nested + breaks)
def process_complex(items):
    total = 0
    for item in items:           # +1 (nesting=0)
        if item.active:          # +2 (nesting=1)
            if item.discount:    # +3 (nesting=2)
                total += item.price * 0.9
                continue         # +1 (break)
            total += item.price
    return total
```

---

## SOLID Quick Reference

| Principle | Meaning | Violation Smell |
|-----------|---------|-----------------|
| **S**ingle Responsibility | One reason to change | God class, mixed concerns |
| **O**pen/Closed | Open for extension, closed for modification | Type switches, hardcoded cases |
| **L**iskov Substitution | Subtypes replaceable | NotImplementedError in subclass |
| **I**nterface Segregation | Small, focused interfaces | Unused interface methods |
| **D**ependency Inversion | Depend on abstractions | Hardcoded dependencies |

---

## Anti-Patterns

### ❌ Shotgun Surgery

Changing one feature requires editing many files.

```python
# Problem: Add new payment method = edit 10 files
# - PaymentController
# - PaymentService
# - PaymentValidator
# - PaymentRepository
# - etc.

# Fix: Consolidate into single module with clear interface
```

### ❌ Copy-Paste Programming

```python
# ❌ BAD: Duplicated with slight variations
def process_credit_card(amount):
    validate_amount(amount)
    log_transaction("credit", amount)
    charge_credit_card(amount)
    send_receipt("credit", amount)

def process_paypal(amount):
    validate_amount(amount)
    log_transaction("paypal", amount)
    charge_paypal(amount)
    send_receipt("paypal", amount)

# ✅ GOOD: Extract common flow
def process_payment(amount, payment_type, charge_fn):
    validate_amount(amount)
    log_transaction(payment_type, amount)
    charge_fn(amount)
    send_receipt(payment_type, amount)
```

### ❌ Boolean Blindness

```python
# ❌ BAD: What does True mean?
process_order(order, True, False, True)

# ✅ GOOD: Named parameters or enums
process_order(
    order,
    send_confirmation=True,
    expedited=False,
    gift_wrap=True,
)
```

### ❌ Comment Smell

```python
# ❌ BAD: Comment explains bad code
# Loop through users and check if active and has orders
for u in data:
    if u[3] == 1 and len(u[7]) > 0:
        process(u)

# ✅ GOOD: Self-documenting code
for user in users:
    if user.is_active and user.has_orders:
        process(user)
```

---

## Checklist

### Before Refactoring
- [ ] Tests exist and pass
- [ ] Understand current behavior
- [ ] Identify specific smell/problem
- [ ] Plan incremental changes

### Complexity
- [ ] Functions: cyclomatic complexity ≤ 10
- [ ] Functions: cognitive complexity ≤ 15
- [ ] Functions: ≤ 20 lines (excluding docstrings)
- [ ] Classes: ≤ 300 lines
- [ ] Parameters: ≤ 5 per function

### Code Smells
- [ ] No duplicated code blocks
- [ ] No magic numbers/strings
- [ ] No dead/unreachable code
- [ ] No commented-out code
- [ ] No TODO/FIXME in production

### After Refactoring
- [ ] Tests still pass
- [ ] Behavior unchanged
- [ ] Code more readable
- [ ] Complexity reduced (measured)
