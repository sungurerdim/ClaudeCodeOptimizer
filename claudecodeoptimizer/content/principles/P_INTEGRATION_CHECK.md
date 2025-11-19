---
id: U_INTEGRATION_CHECK
title: Complete Integration Check
category: universal
severity: high
weight: 8
applicability:
  project_types: ['all']
  languages: ['all']
---

# U_INTEGRATION_CHECK: Complete Integration Check 🔴

**Severity**: High

Zero orphaned code. Every function called, every import used, every file referenced.

**Enforcement**: SHOULD

**Project Types**: all
**Languages**: all

---

## Why

### The Problem
- **Orphaned code** - Functions/modules nobody calls
- **Dead imports** - Unused dependencies cluttering code
- **Broken references** - Code references nonexistent functions
- **Runtime surprises** - Integration issues discovered in production
- **Import hell** - Circular dependencies, missing imports

### Core Checks

**Every change MUST verify:**
1. ✅ **All imports used** - No unused imports
2. ✅ **All functions called** - No orphaned functions
3. ✅ **All references valid** - No broken function calls
4. ✅ **All files integrated** - No disconnected modules
5. ✅ **Types align** - Function signatures match call sites

### Implementation Patterns

#### ✅ Good: Integrated Code
```python
# utils/validator.py
def <function_name>(email: str) -> bool:
    return "@" in email and "." in email

# <user_api_file>.py
from utils.validator import <function_name>  # ✅ Imported

def register_user(email: str):
    if not <function_name>(email):  # ✅ Called
        raise ValueError("Invalid email")
    # ... save user

# ✅ GOOD: <function_name> is imported AND called
```

#### ❌ Bad: Orphaned Code
```python
# utils/validator.py
def <function_name>(email: str) -> bool:
    return "@" in email and "." in email

def validate_phone(phone: str) -> bool:  # ❌ Nobody calls this
    return len(phone) == 10

# <user_api_file>.py
from utils.validator import <function_name>, validate_phone  # ❌ validate_phone unused

def register_user(email: str):
    if not <function_name>(email):
        raise ValueError("Invalid email")
    # ❌ validate_phone imported but never used
```

---

## Auto-Detection Tools

### Python: Ruff/Flake8/Pylint
```bash
# Find unused imports
ruff check . --select F401  # Unused imports
ruff check . --select F841  # Unused variables

# Find dead code
vulture .  # Detects unused code

# Fix automatically
ruff check . --fix  # Auto-remove unused imports
```

### JavaScript/TypeScript: ESLint
```bash
# .eslintrc.json
{
  "rules": {
    "no-unused-vars": "error",
    "no-unused-imports": "error"
  }
}

# Find and fix
eslint . --fix
```

### Go: Go Compiler
```bash
# Go compiler catches unused imports automatically
go build  # Fails if unused imports

# Find unused code
go vet ./...
golangci-lint run
```

### Rust: Rustc
```bash
# Rust warns on unused code by default
cargo build
# warning: unused import: `std::collections::HashMap`

# Make warnings errors
cargo build --deny warnings
```

---

## Integration Testing

### Test 1: Build Succeeds
```bash
# ✅ If build succeeds, basic integration works
npm run build  # JavaScript/TypeScript
cargo build    # Rust
go build       # Go
python -m py_compile src/**/*.py  # Python

# Build success = imports resolve, types align
```

### Test 2: Import Resolution
```python
# Python: Try importing everything
import importlib
import os

for root, dirs, files in os.walk('src'):
    for file in files:
        if file.endswith('.py'):
            module = file[:-3]
            try:
                importlib.import_module(module)
                print(f"✓ {module}")
            except ImportError as e:
                print(f"✗ {module}: {e}")
```

### Test 3: Dead Code Detection
```bash
# Find code never executed in tests
coverage run -m pytest tests/
coverage report --show-missing

# Any file with 0% coverage = potentially orphaned
```

### Test 4: Dependency Graph
```bash
# Python: Generate import graph
pydeps src/ --max-bacon=2

# JavaScript: Analyze bundle
webpack-bundle-analyzer

# Check for:
# - Circular dependencies
# - Unused modules
# - Disconnected subgraphs
```

---

## Anti-Patterns

### ❌ Unused Imports
```python
# ❌ BAD: Imports never used
import json  # Never called
import datetime  # Never called
from utils import helper1, helper2, helper3  # Only helper1 used

def process():
    result = helper1()  # Only this one used
    return result

# ✅ GOOD: Import only what you use
from utils import helper1

def process():
    result = helper1()
    return result
```

### ❌ Dead Functions
```python
# ❌ BAD: Function defined but never called
def calculate_discount(price, discount):  # ❌ Nobody calls this
    return price * (1 - discount)

def process_order(order):
    total = sum(item.price for item in order.items)
    # ❌ Should call calculate_discount but doesn't
    return total

# ✅ GOOD: Either use it or delete it
def calculate_discount(price, discount):
    return price * (1 - discount)

def process_order(order):
    subtotal = sum(item.price for item in order.items)
    total = calculate_discount(subtotal, order.discount)  # ✅ Used
    return total
```

### ❌ Broken References
```typescript
// ❌ BAD: Calling nonexistent function
import { validateUser } from './validators';

function registerUser(userData) {
    <function_name>(userData.email);  // ❌ <function_name> doesn't exist!
    // Should be: validateUser(userData)
}

// ✅ GOOD: Call what exists
import { validateUser } from './validators';

function registerUser(userData) {
    validateUser(userData);  // ✅ Exists and imported
}
```

---

## Implementation Checklist

- [ ] **Enable unused code detection** - Linters/compilers configured
- [ ] **CI enforcement** - Build fails on unused imports
- [ ] **Pre-commit hooks** - Auto-remove unused imports before commit
- [ ] **Regular audits** - Monthly dead code cleanup
- [ ] **Test coverage** - High coverage ensures code is called
- [ ] **Dependency graph** - Visualize and verify connections
- [ ] **Import analysis** - Check all imports resolve correctly

---

## CI Integration

### GitHub Actions
```yaml
name: Integration Check

on: [push, pull_request]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Check unused imports
        run: |
          ruff check . --select F401  # Unused imports
          ruff check . --select F841  # Unused variables
      - name: Check dead code
        run: vulture . --min-confidence 80
      - name: Build verification
        run: python -m py_compile src/**/*.py
```

---

## Metrics and Monitoring

### Key Indicators
- **Dead code percentage** - % of code never executed (aim for 0%)
- **Unused import count** - Number of unused imports (aim for 0)
- **Build success rate** - % of builds that pass integration checks
- **Coverage** - % of code covered by tests (aim for high coverage)

### Success Criteria
- Zero unused imports (enforced by CI)
- Zero dead functions (detected by coverage + audits)
- 100% build success rate (all references valid)
- High test coverage (ensures code is integrated)

---

## Summary

**Complete Integration Check** means verifying every function is called, every import is used, and every reference is valid. Zero orphaned code, zero broken integrations.

**Core Rule**: If it's not integrated (called, imported, referenced), remove it or fix the integration.
