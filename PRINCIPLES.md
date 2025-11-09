# Development Principles

**Generated**: 2025-11-09
**Total Principles**: 72 (across all categories)
**Core Principles**: 3 (always loaded)

---

## Quick Reference (Core Principles - Always Apply)

These principles are **MANDATORY** and apply to **ALL work, ALWAYS**.

### P001: Fail-Fast Error Handling ⚠️

Errors must cause immediate, visible failure. No silent fallbacks, no swallowed exceptions.

**Key Rules**:
- No bare except: clauses
- No empty catch blocks

**Example**:
```python
# ✅ Good
try:
    result = risky()
except SpecificError as e:
    logger.error(f'Failed: {e}')
    raise

# ❌ Bad
try:
    result = risky()
except:
    pass
```

---

### P067: Evidence-Based Verification ⚠️

Never claim completion without command execution proof. All verification requires fresh command output with exit codes

**Key Rules**:
- Completion claims must include command output
- Avoid uncertainty language

**Example**:
```python
# ✅ Good
[Runs: pytest]
[Output: 34/34 passed]
[Exit code: 0]
"All tests pass"

[Runs: npm run build]
[Output: Build successful in 2.3s]
[Exit code: 0]
"Build succeeds"

# ❌ Bad
"Tests should pass now"
"Build looks correct"
"Appears to be working"
```

---

### P071: No Overengineering - Pragmatic Solutions Only ⚠️

Always choose the simplest solution that solves the problem. Avoid premature abstraction, unnecessary patterns, excessive architecture, or solutions built for imaginary future requirements. Every line of code is a liability - write only what is needed now.

**Key Rules**:
- Avoid abstraction before you have 3+ similar use cases
- Remove configuration options, generic parameters, or extensibility hooks that are not currently used
- Try simple approach before complex patterns (no need for Factory, Strategy, Observer for simple cases)

**Example**:
```python
# ✅ Good
# Good: Simple and direct
def send_email(to: str, subject: str, body: str):
    """Send email via SMTP."""
    smtp.send(to, subject, body)

# Add complexity only when actually needed

# ❌ Bad
# Bad: Premature abstraction
class AbstractDataProcessorFactory:
    @abstractmethod
    def create_processor(self): pass

class SimpleDataProcessor(AbstractDataProcessorFactory):
    def create_processor(self): return Processor()

# For just ONE use case!
```

---

## Full Principles by Category

For detailed principles, see category-specific documents:

- **[Core Principles](docs/cco/principles/core.md)** - 3 principles
  - Always loaded
- **[Code Quality](docs/cco/principles/code-quality.md)** - 14 principles
  - DRY, type safety, immutability, precision, version management
- **[Security & Privacy](docs/cco/principles/security-privacy.md)** - 19 principles
  - Encryption, zero-trust, privacy-first, auth, secrets, input validation
- **[Testing](docs/cco/principles/testing.md)** - 6 principles
  - Test pyramid, coverage, isolation, integration, CI gates
- **[Architecture](docs/cco/principles/architecture.md)** - 10 principles
  - Event-driven, microservices, separation of concerns, patterns
- **[Performance](docs/cco/principles/performance.md)** - 5 principles
  - Caching, async I/O, database optimization, lazy loading
- **[Operational Excellence](docs/cco/principles/operations.md)** - 10 principles
  - IaC, observability, health checks, config as code
- **[Git Workflow](docs/cco/principles/git-workflow.md)** - 5 principles
  - Commit conventions, branching, PR guidelines, versioning
- **[API Design](docs/cco/principles/api-design.md)** - 2 principles
  - RESTful conventions, versioning, error handling

---

## Token Optimization

**Progressive Disclosure Strategy**:
- **Core principles** loaded by default: ~500 tokens
- **Category-specific** principles loaded on-demand: ~500-2000 tokens each
- **Total available**: ~8000 tokens (all categories)

**Reduction**: 16x (8000 → 500 tokens for typical usage)

Category-specific principles load automatically when running relevant commands:
- `/cco-audit code` → loads Code Quality principles
- `/cco-audit security` → loads Security principles
- `/cco-test` → loads Testing principles
- `/cco-analyze` → loads Architecture principles
- `/cco-optimize` → loads Performance principles

---

## Using These Principles

### In Claude Code

Reference this file in any conversation:
```
@PRINCIPLES.md  # Load core principles
@PRINCIPLES.md Check if this code follows our principles
@PRINCIPLES.md What principle applies to error handling?
```

For category-specific principles:
```
@docs/cco/principles/security.md  # Load security principles
@docs/cco/principles/testing.md   # Load testing principles
```

### In Commands

All CCO commands use these principles:
- `/cco-audit code` - Check code quality principles
- `/cco-audit security` - Check security principles
- `/cco-audit all` - Check all applicable principles
- `/cco-fix` - Auto-fix violations

### Updating Principles

Your principles are customized based on your project configuration. To update:

1. **Change preferences**: Edit `.cco/project.json`
2. **Regenerate**: Run `/cco-init` or modify preferences via wizard
3. **Review changes**: Check `git diff PRINCIPLES.md`

---

*Auto-generated by ClaudeCodeOptimizer*
*Principle Database: 72 total principles*
*Reference with: @PRINCIPLES.md*