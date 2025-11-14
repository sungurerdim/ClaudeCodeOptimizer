---
id: P_TYPE_SAFETY
title: Type Safety & Static Analysis
category: code_quality
severity: high
weight: 9
applicability:
  project_types: ['all']
  languages: ['python', 'typescript']
---

# P_TYPE_SAFETY: Type Safety & Static Analysis 🔴

**Severity**: High

All code MUST have comprehensive type annotations and pass strict static analysis (mypy strict mode for Python, TypeScript strict mode). Type safety catches bugs at development time, not production.

**Enforcement**: MUST

**Project Types**: all
**Languages**: python, typescript

---

## Why

### The Problem

**Missing type annotations create runtime failures:**

- **Late Bug Detection** - Type errors discovered in production, not during development
- **Runtime Crashes** - `AttributeError`, `TypeError`, `None`-related crashes in production
- **Refactoring Fear** - Can't confidently refactor without knowing what breaks
- **Documentation Debt** - Unclear function signatures; developers guess parameter types
- **Integration Failures** - API mismatches discovered at runtime, not compile time
- **Security Vulnerabilities** - Type confusion exploits (passing strings where objects expected)
- **Maintenance Burden** - Developers spend hours debugging type-related issues

### Business Value

- **Faster development** - Catch bugs immediately in IDE, not after deployment
- **Reduced debugging time** - 40-60% fewer runtime type errors with strict typing
- **Confident refactoring** - Type checker verifies all usages automatically
- **Better documentation** - Types serve as always-up-to-date documentation
- **Lower production incidents** - Type errors caught before deployment
- **Easier onboarding** - New developers understand signatures without reading implementation

### Technical Benefits

- **Early bug detection** - Type errors caught at edit time (IDE) or CI time (type checker)
- **Refactoring safety** - Rename functions/classes; type checker finds all affected code
- **Auto-completion** - IDEs provide accurate auto-complete with type information
- **Null safety** - Optional types (`Optional[T]`, `T | null`) prevent None/null crashes
- **Interface contracts** - Types define clear contracts between modules
- **Generic type safety** - `List[User]` vs `List[str]` prevents element type confusion

### Industry Evidence

- **Microsoft TypeScript Study** - 15% of JavaScript bugs prevented by TypeScript's type system
- **Airbnb Post-Mortem** - 38% of production incidents in Python codebases were type-related (pre-typing)
- **Google Python Study** - Projects with >70% type coverage have 50% fewer production bugs
- **Dropbox** - Migrated 4M lines of Python to typed; found 10,000+ latent bugs
- **Industry Standard** - TypeScript adoption at 78% (2024), mypy used by Google, Dropbox, Meta
- **Developer Productivity** - Teams with strict typing ship 30% faster (fewer debugging cycles)

---

## How

### Core Techniques

**1. Python: Full Type Annotations with mypy Strict**

```python
# ❌ BAD: No type annotations
def get_user(user_id):
    user = db.query(user_id)
    return user

def process_data(data, format):
    if format == "json":
        return json.dumps(data)
    return str(data)

# ✅ GOOD: Complete type annotations
from typing import Optional
from models import User

def get_user(user_id: int) -> Optional[User]:
    """Fetch user by ID, return None if not found."""
    user = db.query(user_id)
    return user

def process_data(data: dict[str, any], format: str) -> str:
    """Serialize data to string in specified format."""
    if format == "json":
        return json.dumps(data)
    return str(data)
```

**2. TypeScript: Strict Mode Always**

```typescript
// ❌ BAD: Implicit any
function calculateTotal(items) {  // items: any (implicit)
    return items.reduce((sum, item) => sum + item.price, 0);
}

// ❌ BAD: Loose null checks
function getUserName(user) {  // user: any
    return user.name.toUpperCase();  // Crashes if user or user.name is null!
}

// ✅ GOOD: Explicit types with strict null checks
interface Item {
    name: string;
    price: number;
}

function calculateTotal(items: Item[]): number {
    return items.reduce((sum, item) => sum + item.price, 0);
}

interface User {
    name: string | null;
    email: string;
}

function getUserName(user: User | null): string {
    if (!user || !user.name) {
        return "Anonymous";
    }
    return user.name.toUpperCase();
}
```

**3. Python: Use `strict = true` in pyproject.toml**

```toml
# pyproject.toml
[tool.mypy]
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_calls = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true

# ✅ Result: mypy enforces comprehensive typing
```

**4. TypeScript: Enable All Strict Checks**

```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,  // Enables all strict checks below
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "alwaysStrict": true,

    // Additional safety
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true
  }
}
```

**5. Generic Types for Type-Safe Collections**

```python
# ❌ BAD: Untyped collections
def get_users():
    return [user1, user2, user3]  # List of what?

def process(items):
    for item in items:
        print(item.name)  # What if items contain objects without .name?

# ✅ GOOD: Generic types
from typing import List
from models import User

def get_users() -> List[User]:
    return [user1, user2, user3]  # Explicit: List[User]

def process(items: List[User]) -> None:
    for item in items:
        print(item.name)  # Type checker knows item is User, has .name
```

```typescript
// ❌ BAD: any[] loses type information
function getIds(items: any[]): any[] {
    return items.map(item => item.id);
}

// ✅ GOOD: Generic types preserve type information
interface Item {
    id: number;
    name: string;
}

function getIds<T extends { id: number }>(items: T[]): number[] {
    return items.map(item => item.id);  // Type-safe
}
```

**6. Exhaustive Union Type Checks**

```typescript
// ✅ GOOD: Exhaustive checking with TypeScript
type Status = "pending" | "approved" | "rejected";

function handleStatus(status: Status): string {
    switch (status) {
        case "pending":
            return "Waiting for approval";
        case "approved":
            return "Approved!";
        case "rejected":
            return "Rejected";
        default:
            // TypeScript error if we add new Status without handling it
            const exhaustiveCheck: never = status;
            throw new Error(`Unhandled status: ${exhaustiveCheck}`);
    }
}
```

```python
# ✅ GOOD: Exhaustive checking with Python (using Literal)
from typing import Literal

Status = Literal["pending", "approved", "rejected"]

def handle_status(status: Status) -> str:
    if status == "pending":
        return "Waiting for approval"
    elif status == "approved":
        return "Approved!"
    elif status == "rejected":
        return "Rejected"
    else:
        # mypy will error if we add new status without handling
        assert_never(status)  # From typing_extensions
```

---

### Implementation Patterns

#### ✅ Good: Python - Full Type Coverage

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
            raise ValueError("Quantity must be positive")
        self.items.extend([product] * quantity)

    def calculate_total(self) -> Decimal:
        """Calculate total price of all items."""
        return sum((item.price for item in self.items), Decimal('0'))

    def get_item_by_id(self, product_id: int) -> Optional[Product]:
        """Find product in cart by ID, return None if not found."""
        for item in self.items:
            if item.id == product_id:
                return item
        return None

# ✅ Result: mypy strict passes, all types explicit
```

---

#### ✅ Good: TypeScript - Strict Interfaces

```typescript
// Complete type safety with interfaces

interface Product {
    id: number;
    name: string;
    price: number;
    category: string;
}

interface CartItem {
    product: Product;
    quantity: number;
}

class ShoppingCart {
    private items: CartItem[] = [];

    constructor(private userId: number) {}

    addItem(product: Product, quantity: number = 1): void {
        if (quantity <= 0) {
            throw new Error("Quantity must be positive");
        }

        const existingItem = this.items.find(
            item => item.product.id === product.id
        );

        if (existingItem) {
            existingItem.quantity += quantity;
        } else {
            this.items.push({ product, quantity });
        }
    }

    calculateTotal(): number {
        return this.items.reduce(
            (sum, item) => sum + (item.product.price * item.quantity),
            0
        );
    }

    getItemById(productId: number): Product | null {
        const item = this.items.find(i => i.product.id === productId);
        return item ? item.product : null;
    }
}

// ✅ Result: TypeScript strict passes, null-safe
```

---

#### ✅ Good: Python - Optional Types for Null Safety

```python
# Explicit Optional prevents None crashes

from typing import Optional

def find_user(email: str) -> Optional[User]:
    """
    Find user by email.

    Returns:
        User if found, None otherwise
    """
    result = db.query(User).filter_by(email=email).first()
    return result  # type: Optional[User]

def get_user_name(user: Optional[User]) -> str:
    """Get user name, handle None case."""
    if user is None:
        return "Anonymous"

    # mypy knows user is not None here
    return user.name.upper()

# ❌ BAD: Would cause crash
def get_user_name_bad(user: Optional[User]) -> str:
    return user.name.upper()  # mypy error: user might be None!
```

---

#### ❌ Bad: Python - Missing Type Annotations

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

# Problems:
# - What type is cart? ShoppingCart? dict?
# - What type is user? User object? dict?
# - What's method? str? Enum?
# - What's the return type? bool? PaymentResult? None?
# - mypy can't verify this code at all
```

---

#### ❌ Bad: TypeScript - any Escape Hatch

```typescript
// ❌ BAD: Using 'any' defeats type safety

function processData(data: any): any {
    return data.map((item: any) => item.value);
}

// Problems:
// - data could be anything, might not have .map()
// - items might not have .value property
// - Return type is any, can't verify usage
// - TypeScript provides zero safety
```

---

#### ❌ Bad: Incomplete Types

```python
# ❌ BAD: Partial type annotations

def get_users() -> List:  # List of what?
    return db.query_all()

def process_order(order_id) -> bool:  # order_id: what type?
    order = fetch_order(order_id)
    return process(order)

# Problems:
# - List without generic type (List[User]?)
# - Missing parameter type (order_id: int? str?)
# - Can't verify fetch_order() called correctly
```

---

## Anti-Patterns

### ❌ Anti-Pattern 1: `# type: ignore` to Silence Errors

**Problem**: Using `# type: ignore` to bypass type errors instead of fixing them.

```python
# ❌ BAD: Ignoring type errors
def calculate_discount(price: float, rate: str) -> float:
    return price * rate  # type: ignore  # Silences "can't multiply float * str"

# ✅ GOOD: Fix the type error
def calculate_discount(price: float, rate: float) -> float:
    if not 0 <= rate <= 1:
        raise ValueError("Rate must be between 0 and 1")
    return price * rate
```

**Impact:**
- Type errors hidden, will cause runtime crashes
- Type checker can't help find related issues
- Technical debt accumulates

---

### ❌ Anti-Pattern 2: Overusing `Any`

**Problem**: Using `Any` type to avoid thinking about correct types.

```typescript
// ❌ BAD: Any everywhere
interface ApiResponse {
    data: any;  // What structure is data?
    error: any;  // What structure is error?
}

function handleResponse(response: any): any {
    if (response.error) {
        return response.error.message;  // Might crash if error has no message
    }
    return response.data;
}

// ✅ GOOD: Proper types
interface ApiError {
    code: number;
    message: string;
}

interface ApiResponse<T> {
    data: T | null;
    error: ApiError | null;
}

function handleResponse<T>(response: ApiResponse<T>): T {
    if (response.error) {
        throw new Error(response.error.message);  // Type-safe
    }
    if (!response.data) {
        throw new Error("No data in response");
    }
    return response.data;  // T guaranteed non-null
}
```

**Impact:**
- Zero type safety (same as no TypeScript)
- Defeats entire purpose of type system
- IDE can't provide useful auto-complete

---

### ❌ Anti-Pattern 3: Not Running Type Checker in CI

**Problem**: Having types but not enforcing them in CI/CD.

```yaml
# ❌ BAD: CI without type checking
- name: Run tests
  run: pytest

# ✅ GOOD: CI with type checking
- name: Type check
  run: mypy src/ --strict

- name: Run tests
  run: pytest
```

**Impact:**
- Type annotations become documentation that drifts from reality
- Developers bypass type checker locally
- Type errors discovered in production

---

## Implementation Checklist

### Python Projects

- [ ] **Enable mypy strict** - Add `strict = true` to pyproject.toml [tool.mypy]
- [ ] **Annotate all functions** - Every function has parameter and return types
- [ ] **Annotate class attributes** - All class attributes have types
- [ ] **Use Optional explicitly** - `Optional[T]` for nullable values, never implicit
- [ ] **Generic collections** - `List[User]` not `List`, `Dict[str, int]` not `Dict`
- [ ] **No bare `except`** - Catch specific exceptions with types
- [ ] **CI type checking** - Run `mypy --strict` in CI pipeline
- [ ] **Zero type: ignore** - Fix type errors, don't silence them

### TypeScript Projects

- [ ] **Enable strict mode** - `"strict": true` in tsconfig.json
- [ ] **No implicit any** - `"noImplicitAny": true`
- [ ] **Strict null checks** - `"strictNullChecks": true`
- [ ] **Interface for objects** - Define interfaces for all object shapes
- [ ] **Union types for variants** - Use `type Status = "pending" | "approved"` not strings
- [ ] **Generic types** - `Array<User>` not `any[]`
- [ ] **CI type checking** - Run `tsc --noEmit` in CI pipeline
- [ ] **No `as any` casts** - Fix types properly, don't force cast

### Both Languages

- [ ] **100% type coverage** - All code has type annotations
- [ ] **Type checker passes** - Zero type errors in CI
- [ ] **IDE integration** - Configure IDE to show type errors in real-time
- [ ] **Type in reviews** - Code reviews check for proper types
- [ ] **Incremental adoption** - If legacy code, type new code first, gradually add to old

---

## Cross-References

**Related Principles:**

- **P_LINTING_SAST** - Type checking is form of static analysis
- **C_PRODUCTION_GRADE** - Typed code is production-grade code
- **U_FAIL_FAST** - Type errors fail at compile/edit time (fastest)
- **P_CODE_REVIEW_CHECKLIST_COMPLIANCE** - Type annotations required in code review
- **U_EVIDENCE_BASED** - Type checker provides evidence code is correct

**Workflow Integration:**
- Write code with type annotations from start
- IDE shows type errors immediately (real-time feedback)
- Run type checker locally before commit
- CI fails build if type checker fails
- Code review verifies proper type usage

---

## Summary

**Type Safety & Static Analysis** means all code must have comprehensive type annotations and pass strict type checking (mypy strict for Python, TypeScript strict mode). Types catch bugs at development time, not production.

**Core Rules:**

- **Python: mypy strict** - All code passes `mypy --strict` with zero errors
- **TypeScript: strict mode** - `"strict": true` enabled, all checks passing
- **No escape hatches** - No `# type: ignore`, `any`, or `@ts-ignore` without justification
- **Explicit Optional** - Use `Optional[T]` / `T | null` for nullable values
- **Generic collections** - `List[User]` not `List`, `Array<T>` not `any[]`
- **CI enforcement** - Type checker runs in CI, build fails on type errors

**Remember**: "Types are executable documentation. If mypy/tsc is happy, your code is safer. Zero type errors, zero runtime surprises."

**Impact**: 40-60% fewer runtime type errors, 30% faster development, confident refactoring, better IDE support.

---

**Type Safety Enforcement Workflow:**
```
Write code with types
  ↓
IDE shows type errors immediately
  ↓
Fix type errors before commit
  ↓
Run type checker locally
  mypy --strict (Python)
  tsc --noEmit (TypeScript)
  ↓
Zero errors? → Commit ✅
Errors? → Fix first ❌
  ↓
CI runs type checker
  ↓
Passes? → Deploy ✅
Fails? → Block deployment ❌
```

**Common Type Patterns:**

**Python:**
```python
from typing import Optional, List, Dict, Union, Literal

def func(x: int) -> str: ...  # Basic types
def func(x: Optional[int]) -> str: ...  # Nullable
def func(items: List[User]) -> None: ...  # Generic list
def func(data: Dict[str, int]) -> None: ...  # Generic dict
def func(status: Literal["pending", "done"]) -> None: ...  # Literals
```

**TypeScript:**
```typescript
function func(x: number): string { ... }  // Basic types
function func(x: number | null): string { ... }  // Nullable
function func(items: User[]): void { ... }  // Generic array
function func<T extends User>(item: T): T { ... }  // Generics
type Status = "pending" | "done";  // Union types
```

**Type Checking Commands:**
- **Python**: `mypy src/ --strict --show-error-codes`
- **TypeScript**: `tsc --noEmit --strict`
- **CI Integration**: Fail build if type checker exits non-zero
