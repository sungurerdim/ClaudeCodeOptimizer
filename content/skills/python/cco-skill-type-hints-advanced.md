---
title: Advanced Python Type Hints Skill
category: quality
description: mypy, typing, generics, protocols
metadata:
  name: "Advanced Python Type Hints"
  activation_keywords: ["type", "typing", "generic", "protocol", "typevar"]
  category: "language-python"
  language: "python"
principles: ['P_TYPE_SAFETY', 'P_LINTING_SAST', 'U_FAIL_FAST', 'U_DRY']
use_cases:
  development_philosophy: [quality_first, balanced]
  project_maturity: [active-dev, production, legacy]
---

# Advanced Python Type Hints

Master advanced Python type hints for robust static type checking with mypy and pyright.

<!-- INSTRUCTIONS: Load when activated -->
## Detailed Instructions

**Core Type System Features:**
- `Generic[T]` creates reusable generic classes
- `Protocol` defines structural subtyping (duck typing with types)
- `TypeVar` creates type variables for generic functions
- `Union[A, B]` or `A | B` (Python 3.10+) for multiple possible types
- `Literal["value"]` for exact value types

**Key Patterns:**
1. Use `Protocol` for interface-like behavior without inheritance
2. Constrain `TypeVar` with bounds for restricted generics
3. Use `Annotated` for metadata (validation, documentation)
4. Prefer `None | T` over `Optional[T]` in Python 3.10+
5. Use `@overload` for functions with multiple signatures

**Type Narrowing:**
- `isinstance()` checks narrow types automatically
- `TypeGuard` for custom type checking functions
- `assert_type()` verifies inferred types in tests

<!-- RESOURCES: Load on explicit request -->
## Examples & Resources

**Generic Classes:**
```python
from typing import Generic, TypeVar

T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

# Usage with type safety
int_stack: Stack[int] = Stack()
int_stack.push(42)  # ✓
int_stack.push("string")  # ✗ Type error
```

**Protocol for Structural Typing:**
```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> str: ...

class Circle:
    def draw(self) -> str:
        return "○"

class Square:
    def draw(self) -> str:
        return "□"

def render(shape: Drawable) -> None:
    print(shape.draw())

# Works without inheritance
render(Circle())  # ✓
render(Square())  # ✓
```

**Constrained TypeVar:**
```python
from typing import TypeVar

# Constrained to specific types
NumberType = TypeVar('NumberType', int, float)

def add(x: NumberType, y: NumberType) -> NumberType:
    return x + y

add(1, 2)      # ✓ Returns int
add(1.5, 2.3)  # ✓ Returns float
add(1, 2.3)    # ✗ Type error (mixed types)

# Bounded TypeVar
from collections.abc import Sized
T = TypeVar('T', bound=Sized)

def get_length(obj: T) -> int:
    return len(obj)  # ✓ T guaranteed to have __len__
```

**Union and Literal Types:**
```python
from typing import Literal

Status = Literal["pending", "running", "completed", "failed"]

def set_status(status: Status) -> None:
    print(f"Status: {status}")

set_status("running")  # ✓
set_status("invalid")  # ✗ Type error

# Union types (Python 3.10+)
def process(value: int | str | None) -> str:
    match value:
        case int():
            return str(value)
        case str():
            return value
        case None:
            return "empty"
```

**TypeGuard for Custom Type Checking:**
```python
from typing import TypeGuard

def is_str_list(items: list[object]) -> TypeGuard[list[str]]:
    return all(isinstance(item, str) for item in items)

def process_strings(items: list[object]) -> None:
    if is_str_list(items):
        # Type narrowed to list[str]
        for item in items:
            print(item.upper())  # ✓ Safe
```

**Function Overloads:**
```python
from typing import overload

@overload
def process(x: int) -> str: ...

@overload
def process(x: str) -> int: ...

def process(x: int | str) -> int | str:
    if isinstance(x, int):
        return str(x)
    return len(x)

result1: str = process(42)    # ✓ Correct type inferred
result2: int = process("hi")  # ✓ Correct type inferred
```

**Annotated for Metadata:**
```python
from typing import Annotated

# With validation metadata
PositiveInt = Annotated[int, "Must be positive", lambda x: x > 0]
Email = Annotated[str, "Valid email format"]

def create_user(
    age: PositiveInt,
    email: Email
) -> None:
    pass
```

**Generic Protocol:**
```python
from typing import Protocol, TypeVar

T_co = TypeVar('T_co', covariant=True)

class Getter(Protocol[T_co]):
    def get(self) -> T_co: ...

class StringGetter:
    def get(self) -> str:
        return "hello"

def use_getter(getter: Getter[str]) -> str:
    return getter.get()

use_getter(StringGetter())  # ✓ Works
```

**Type Checking Configuration (pyproject.toml):**
```toml
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pyright]
pythonVersion = "3.11"
typeCheckingMode = "strict"
```

**Anti-Patterns to Avoid:**
```python
# ✗ Avoid Any when possible
def process(data: Any) -> Any:  # Too permissive
    pass

# ✓ Use specific types or generics
T = TypeVar('T')
def process(data: T) -> T:
    pass

# ✗ Don't use mutable default arguments
def append_to(item: str, lst: list[str] = []) -> list[str]:  # Bug!
    pass

# ✓ Use None as default
def append_to(item: str, lst: list[str] | None = None) -> list[str]:
    if lst is None:
        lst = []
    return lst
```
