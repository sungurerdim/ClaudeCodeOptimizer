# Code Quality
**DRY, fail-fast, type safety, immutability, precision, version management**

**Total Principles:** 14

---

## P001: Fail-Fast Error Handling

**Severity:** CRITICAL

Errors must cause immediate, visible failure. No silent fallbacks, no swallowed exceptions.

### Examples

**✅ Good:**
```
try:
    result = risky()
except SpecificError as e:
    logger.error(f'Failed: {e}')
    raise
```

**❌ Bad:**
```
try:
    result = risky()
except:
    pass
```

**Why:** Catches bugs early in development before they reach production

---

## P002: DRY Enforcement

**Severity:** HIGH

Single source of truth for all data, logic, configuration. Zero duplicate definitions.

### Examples

**✅ Good:**
```
# shared/constants.py
MAX_RETRIES = 3

# Other files
from shared.constants import MAX_RETRIES
```

**❌ Bad:**
```
MAX_RETRIES = 3  # file1
MAX_RETRIES = 3  # file2 - duplicate!
```

**Why:** Eliminates code duplication to reduce bugs and maintenance burden

---

## P003: Complete Integration Check

**Severity:** HIGH

Zero orphaned code. Every function called, every import used, every file referenced.

### Examples

**✅ Good:**
```
from utils import used_func
result = used_func()
```

**❌ Bad:**
```
import unused_module  # Never referenced
```

**Why:** Prevents runtime errors by catching type mismatches during development

---

## P004: No Backward Compatibility Debt

**Severity:** HIGH

Clean migration - delete old system entirely, no config flags for old/new.

### Examples

**✅ Good:**
```
new_func()  # Old system deleted
```

**❌ Bad:**
```
if USE_NEW_API:
    new_func()
else:
    old_func()  # Tech debt!
```

**Why:** Prevents bugs from state changes by making data unchangeable after creation

---

## P006: Precision in Calculations

**Severity:** HIGH

Use Decimal for financial, proper float types for scientific, avoid premature rounding.

### Examples

**✅ Good:**
```
from decimal import Decimal
cost = Decimal('0.1') + Decimal('0.2')  # 0.3
```

**❌ Bad:**
```
cost = 0.1 + 0.2  # 0.30000000000000004
```

**Why:** Makes code self-documenting by using clear, descriptive variable and function names

---

## P007: Immutability by Default

**Severity:** MEDIUM

Use frozen dataclasses, const by default, minimize mutable state.

### Examples

**✅ Good:**
```
@dataclass(frozen=True)
class User:  # Immutable
```

**❌ Bad:**
```
@dataclass
class User:  # Mutable
```

**Why:** Keeps functions focused on one task making them easier to test and reuse

---

## P008: Code Review Checklist Compliance

**Severity:** MEDIUM

All PRs must pass mandatory code review checklist (large teams).

### Examples

**✅ Good:**
```
# PR template with checklist:
- [ ] Tests added
- [ ] Docs updated
```

**❌ Bad:**
```
# No checklist, reviewers inconsistent
```

**Why:** Prevents tight coupling by hiding implementation details behind clean interfaces

---

## P009: Linting & SAST Enforcement

**Severity:** HIGH

Use linters (ruff/eslint) AND SAST tools (Semgrep/CodeQL/Snyk) with strict rules, enforce in CI.

### Examples

**✅ Good:**
```
# pyproject.toml - Linting with security
```
```
[tool.ruff.lint]
```
```
select = ['E', 'F', 'W', 'S', 'B']  # Include bandit security rules
```
```

```
```
# .github/workflows/ci.yml - SAST in CI
```
```
- name: Run Semgrep
```
```
  uses: semgrep/semgrep-action@v1
```
```
  with:
```
```
    config: 'p/security-audit'
```
```

```
```
- name: Run CodeQL
```
```
  uses: github/codeql-action/analyze@v2
```
```

```
```
- name: Run Snyk Code
```
```
  run: snyk code test
```

**❌ Bad:**
```
# No linter config, no SAST
```
```
# Code passes without security checks
```

**Why:** Catches security vulnerabilities and code quality issues before production

---

## P010: Performance Profiling Before Optimization

**Severity:** LOW

Always profile before optimizing - no premature optimization.

### Examples

**✅ Good:**
```
# Profile: python -m cProfile script.py
# Then optimize hotspots
```

**❌ Bad:**
```
# Optimize without measuring first
```

**Why:** Improves code clarity by writing functions that return values instead of modifying state

---

## P023: Type Safety & Static Analysis

**Severity:** HIGH

All code MUST have type annotations, pass mypy/pyright strict mode.

### Examples

**✅ Good:**
```
def calculate(x: int, y: int) -> int:
```

**❌ Bad:**
```
def calculate(x, y):  # No types!
```

**Why:** Adds security layer by validating all external input before processing

---

## P053: Centralized Version Management

**Severity:** HIGH

Single source of truth for version number - no fallbacks, fail-fast on import errors.

### Examples

**✅ Good:**
```
# __init__.py - single source
__version__ = '1.0.0'

# Other modules
from .. import __version__

# pyproject.toml
[tool.setuptools.dynamic]
version = {attr = 'package.__version__'}
```

**❌ Bad:**
```
# Multiple version definitions
__version__ = '1.0.0'
# In another file:
VERSION = '1.0.0'

# Fallback pattern (anti-pattern)
try:
    from . import __version__
except:
    __version__ = '0.0.0'
```

**Why:** Prevents version conflicts by centralizing version definition in single source file

---

## P067: Evidence-Based Verification

**Severity:** CRITICAL

Never claim completion without command execution proof. All verification requires fresh command output with exit codes

### Examples

**✅ Good:**
```
[Runs: pytest]
[Output: 34/34 passed]
[Exit code: 0]
"All tests pass"

[Runs: npm run build]
[Output: Build successful in 2.3s]
[Exit code: 0]
"Build succeeds"
```

**❌ Bad:**
```
"Tests should pass now"
"Build looks correct"
"Appears to be working"
```

**Why:** Ensures all claims are backed by objective evidence, preventing false confidence

---

## P068: Grep-First Search Strategy

**Severity:** MEDIUM

Optimize file operations using grep-first approach: files_with_matches → content → targeted Read with offset+limit

### Examples

**✅ Good:**
```
# Grep-first approach
files = Grep("pattern", output_mode="files_with_matches")
context = Grep("pattern", path=files[0], output_mode="content", -C=5)

# Targeted read with offset+limit
Read("largefile.py", offset=100, limit=50)
```

**❌ Bad:**
```
# Read entire 5000-line file
content = Read("largefile.py")

# No grep, blindly reading files
Read("file1.py")
Read("file2.py")
Read("file3.py")
```

**Why:** Minimizes token usage and improves performance through strategic file access

---

## P071: No Overengineering - Pragmatic Solutions Only

**Severity:** CRITICAL

Always choose the simplest solution that solves the problem. Avoid premature abstraction, unnecessary patterns, excessive architecture, or solutions built for imaginary future requirements. Every line of code is a liability - write only what is needed now.

### Examples

**✅ Good:**
```
# Good: Simple and direct
def send_email(to: str, subject: str, body: str):
    """Send email via SMTP."""
    smtp.send(to, subject, body)

# Add complexity only when actually needed
```
```
# Good: Extract abstraction when you have multiple cases
def process_csv(file): ...
def process_json(file): ...
# After 3rd format, THEN create: DataProcessor interface
```
```
// Good: Start simple
function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price, 0);
}
// Clean, direct, no unnecessary classes
```

**❌ Bad:**
```
# Bad: Premature abstraction
class AbstractDataProcessorFactory:
    @abstractmethod
    def create_processor(self): pass

class SimpleDataProcessor(AbstractDataProcessorFactory):
    def create_processor(self): return Processor()

# For just ONE use case!
```
```
# Bad: Over-configured
class EmailSender:
    def __init__(self, smtp_host, port, use_tls, use_ssl, timeout, 
                 retry_count, retry_delay, max_retries, fallback_host):
        # 9 parameters for a simple email sender
```
```
// Bad: Unnecessary pattern
class UserRepositoryFactory {
  createRepository() {
    return new UserRepository();
  }
}
// Just use: new UserRepository()
```

**Why:** Simpler code is easier to understand, maintain, debug, and change

---
