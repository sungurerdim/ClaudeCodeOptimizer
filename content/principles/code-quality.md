# Code Quality Principles

**Generated**: 2025-11-09
**Principle Count**: 14

---

### P001: Fail-Fast Error Handling 🔴

**Severity**: Critical

Errors must cause immediate, visible failure. No silent fallbacks, no swallowed exceptions.

**Rules**:
- No bare except: clauses
- No empty catch blocks

**❌ Bad**:
```
try:\n    result = risky()\nexcept:\n    pass
```

**✅ Good**:
```
try:\n    result = risky()\nexcept SpecificError as e:\n    logger.error(f'Failed: {e}')\n    raise
```

---

### P002: DRY Enforcement 🟠

**Severity**: High

Single source of truth for all data, logic, configuration. Zero duplicate definitions.

**Rules**:
- No duplicate function definitions
- No magic numbers except 0, 1, -1

**❌ Bad**:
```
MAX_RETRIES = 3  # file1\nMAX_RETRIES = 3  # file2 - duplicate!
```

**✅ Good**:
```
# shared/constants.py\nMAX_RETRIES = 3\n\n# Other files\nfrom shared.constants import MAX_RETRIES
```

---

### P003: Complete Integration Check 🟠

**Severity**: High

Zero orphaned code. Every function called, every import used, every file referenced.

**Rules**:
- No unused imports

**❌ Bad**:
```
import unused_module  # Never referenced
```

**✅ Good**:
```
from utils import used_func\nresult = used_func()
```

---

### P004: No Backward Compatibility Debt 🟠

**Severity**: High

Clean migration - delete old system entirely, no config flags for old/new.

**Rules**:
- No USE_OLD/USE_NEW feature flags

**❌ Bad**:
```
if USE_NEW_API:\n    new_func()\nelse:\n    old_func()  # Tech debt!
```

**✅ Good**:
```
new_func()  # Old system deleted
```

---

### P006: Precision in Calculations 🟠

**Severity**: High

Use Decimal for financial, proper float types for scientific, avoid premature rounding.

**Languages**: python, javascript, java

**Rules**:
- No float for money calculations

**❌ Bad**:
```
cost = 0.1 + 0.2  # 0.30000000000000004
```

**✅ Good**:
```
from decimal import Decimal\ncost = Decimal('0.1') + Decimal('0.2')  # 0.3
```

---

### P007: Immutability by Default 🟡

**Severity**: Medium

Use frozen dataclasses, const by default, minimize mutable state.

**Languages**: python, javascript, typescript

**Rules**:
- Use frozen=True for dataclasses

**❌ Bad**:
```
@dataclass\nclass User:  # Mutable
```

**✅ Good**:
```
@dataclass(frozen=True)\nclass User:  # Immutable
```

---

### P008: Code Review Checklist Compliance 🟡

**Severity**: Medium

All PRs must pass mandatory code review checklist (large teams).

**❌ Bad**:
```
# No checklist, reviewers inconsistent
```

**✅ Good**:
```
# PR template with checklist:\n- [ ] Tests added\n- [ ] Docs updated
```

---

### P009: Linting & SAST Enforcement 🟠

**Severity**: High

Use linters (ruff/eslint) AND SAST tools (Semgrep/CodeQL/Snyk) with strict rules, enforce in CI.

**Rules**:
- Project has linter configuration
- Use SAST tools (Semgrep, CodeQL, Snyk Code)
- Linting + SAST enforced in CI pipeline
- Enable security-focused rules (bandit, eslint-plugin-security)

**❌ Bad**:
```
# No linter config, no SAST
```

**✅ Good**:
```
# pyproject.toml - Linting with security
```

---

### P010: Performance Profiling Before Optimization 🟢

**Severity**: Low

Always profile before optimizing - no premature optimization.

**❌ Bad**:
```
# Optimize without measuring first
```

**✅ Good**:
```
# Profile: python -m cProfile script.py\n# Then optimize hotspots
```

---

### P023: Type Safety & Static Analysis 🟠

**Severity**: High

All code MUST have type annotations, pass mypy/pyright strict mode.

**Languages**: python, typescript

**Rules**:
- Functions without type hints

**❌ Bad**:
```
def calculate(x, y):  # No types!
```

**✅ Good**:
```
def calculate(x: int, y: int) -> int:
```

---

### P053: Centralized Version Management 🟠

**Severity**: High

Single source of truth for version number - no fallbacks, fail-fast on import errors.

**Languages**: python, javascript, typescript, go, rust

**Rules**:
- Version defined in single location (__init__.py, package.json, Cargo.toml)
- All modules import version from central source
- No version fallbacks - fail hard on import error

**❌ Bad**:
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

**✅ Good**:
```
# __init__.py - single source
__version__ = '1.0.0'

# Other modules
from .. import __version__

# pyproject.toml
[tool.setuptools.dynamic]
version = {attr = 'package.__version__'}
```

---

### P067: Evidence-Based Verification 🔴

**Severity**: Critical

Never claim completion without command execution proof. All verification requires fresh command output with exit codes

**Rules**:
- Completion claims must include command output
- Avoid uncertainty language

**❌ Bad**:
```
"Tests should pass now"\n"Build looks correct"\n"Appears to be working"
```

**✅ Good**:
```
[Runs: pytest]\n[Output: 34/34 passed]\n[Exit code: 0]\n"All tests pass"\n\n[Runs: npm run build]\n[Output: Build successful in 2.3s]\n[Exit code: 0]\n"Build succeeds"
```

---

### P068: Grep-First Search Strategy 🟡

**Severity**: Medium

Optimize file operations using grep-first approach: files_with_matches → content → targeted Read with offset+limit

**Rules**:
- Use Grep before Read for unknown locations
- Use offset+limit for large files >500 lines

**❌ Bad**:
```
# Read entire 5000-line file\ncontent = Read("largefile.py")\n\n# No grep, blindly reading files\nRead("file1.py")\nRead("file2.py")\nRead("file3.py")
```

**✅ Good**:
```
# Grep-first approach\nfiles = Grep("pattern", output_mode="files_with_matches")\ncontext = Grep("pattern", path=files[0], output_mode="content", -C=5)\n\n# Targeted read with offset+limit\nRead("largefile.py", offset=100, limit=50)
```

---

### P071: No Overengineering - Pragmatic Solutions Only 🔴

**Severity**: Critical

Always choose the simplest solution that solves the problem. Avoid premature abstraction, unnecessary patterns, excessive architecture, or solutions built for imaginary future requirements. Every line of code is a liability - write only what is needed now.

**Rules**:
- Avoid abstraction before you have 3+ similar use cases
- Remove configuration options, generic parameters, or extensibility hooks that are not currently used
- Try simple approach before complex patterns (no need for Factory, Strategy, Observer for simple cases)

**❌ Bad**:
```
# Bad: Premature abstraction
class AbstractDataProcessorFactory:
    @abstractmethod
    def create_processor(self): pass

class SimpleDataProcessor(AbstractDataProcessorFactory):
    def create_processor(self): return Processor()

# For just ONE use case!
```

**✅ Good**:
```
# Good: Simple and direct
def send_email(to: str, subject: str, body: str):
    """Send email via SMTP."""
    smtp.send(to, subject, body)

# Add complexity only when actually needed
```

---

---

**Loading**: These principles load automatically when running relevant commands

**Reference**: Use `@PRINCIPLES.md` to load core principles, or reference this file directly