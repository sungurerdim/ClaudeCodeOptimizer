# Core Development Principles

**⚠️ CRITICAL: Always Apply These Principles ⚠️**

**Generated**: 2025-11-09
**Principle Count**: 3

These are the most critical principles that apply to ALL work, ALWAYS.

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

**Note**: These core principles are always loaded (~500 tokens)

For category-specific principles, see:
- [Code Quality](code-quality.md)
- [Security](security.md)
- [Testing](testing.md)
- [Architecture](architecture.md)
- [Performance](performance.md)
- [Operations](operations.md)
- [Git Workflow](git-workflow.md)
- [API Design](api-design.md)