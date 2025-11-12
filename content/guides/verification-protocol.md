# Verification Protocol

**Load on-demand when:** Verification-related tasks, completion checks

---

## The Rule

**BEFORE claiming any work is complete:**

1. **IDENTIFY**: What command proves this claim?
2. **RUN**: Execute the command (fresh, complete output)
3. **VERIFY**: Check exit code, count failures
4. **REPORT**: State claim WITH evidence

---

## Examples

### ✅ Good - Evidence-Based

```
[Runs pytest]
[Shows: 34/34 passed]
[Exit code: 0]
"All tests pass"

[Runs npm run build]
[Shows: Build successful in 2.3s]
[Exit code: 0]
"Build succeeds"

[Runs ruff check .]
[Shows: All checks passed]
[Exit code: 0]
"Code passes linting"
```

### ❌ Bad - No Evidence

```
"Tests should pass now"
"Build looks correct"
"Appears to be working"
"Seems like it's fixed"
```

---

## Language to Avoid

**Never use**:
- "should work"
- "looks correct"
- "appears to"
- "seems like"
- "probably"
- "might be"

**Always show**:
- Command output
- Exit codes
- Actual results
- Specific counts (e.g., "34/34 passed", not "tests pass")

---

## Application Examples

### Code Changes

```bash
# After implementing a feature
pytest tests/test_feature.py -v
# Output: 5/5 passed
# Exit code: 0
✅ Claim: "All feature tests pass (5/5)"

# After fixing a bug
pytest tests/test_bug_fix.py -v
# Output: 1/1 passed
# Exit code: 0
✅ Claim: "Bug fix verified (test passes)"
```

### Build Operations

```bash
# After updating dependencies
npm run build
# Output: Build completed successfully in 12.4s
# Exit code: 0
✅ Claim: "Build succeeds with new dependencies"

# After refactoring
python -m py_compile module.py
# Output: (no output)
# Exit code: 0
✅ Claim: "Syntax valid (compiles without errors)"
```

### Quality Checks

```bash
# After code cleanup
ruff check .
# Output: All checks passed
# Exit code: 0
✅ Claim: "Code passes all linting checks"

# After type hint additions
mypy src/
# Output: Success: no issues found
# Exit code: 0
✅ Claim: "Type checking passes"
```

---

## Why This Matters

1. **Trust**: Verifiable claims build confidence
2. **Debugging**: If something breaks, you have proof it worked before
3. **Accountability**: Evidence shows work was actually done
4. **Reproducibility**: Others can verify your results
5. **Learning**: Shows the *how*, not just the *what*

---

## Principle Reference

This guide implements **P067: Evidence-Based Verification**

See: [@PRINCIPLES.md](../PRINCIPLES.md) or [@~/.cco/principles/core.md](../principles/core.md)

---

*Part of CCO Documentation System*
*Load when needed: @~/.cco/guides/verification-protocol.md*
