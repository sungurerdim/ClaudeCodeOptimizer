# Verification Protocol

**Load on-demand when:** Verification-related tasks, completion checks

---

## The Rule

**Related Principles:**
- **U_EVIDENCE_BASED**: Evidence-based verification is mandatory
- **U_CHANGE_VERIFICATION**: Verify all changes before claiming completion
- **U_EXPLICIT_COMPLETION**: Define and verify completion criteria

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

**Related Principles:**
- **U_COMPLETE_REPORTING**: Report actual results, not assumptions
- **U_NO_OVERENGINEERING**: Simple, direct verification

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

**Related Principles:**
- **U_TEST_FIRST**: Write tests to verify behavior
- **U_ATOMIC_COMMITS**: Commit only verified changes

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

**Related Principles:**
- **P_TEST_COVERAGE**: Verify test coverage targets
- **P_LINTING_SAST**: Enforce linting and static analysis
- **P_CI_GATES**: Same checks as CI pipeline

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

**Related Principles:**
- **U_INTEGRATION_CHECK**: Verify integration with full system
- **P_TEST_PYRAMID**: Balance unit, integration, and end-to-end tests
- **U_MINIMAL_TOUCH**: Focus verification on what changed

1. **Trust**: Verifiable claims build confidence
2. **Debugging**: If something breaks, you have proof it worked before
3. **Accountability**: Evidence shows work was actually done
4. **Reproducibility**: Others can verify your results
5. **Learning**: Shows the *how*, not just the *what*

---

## Principle References

This guide incorporates the following CCO principles:

**Universal Principles:**
- **U_EVIDENCE_BASED**: Evidence-Based Verification → `.claude/principles/U_EVIDENCE_BASED.md`
- **U_CHANGE_VERIFICATION**: Change Verification Protocol → `.claude/principles/U_CHANGE_VERIFICATION.md`
- **U_TEST_FIRST**: Test-First Development → `.claude/principles/U_TEST_FIRST.md`
- **U_ATOMIC_COMMITS**: Atomic Commits → `.claude/principles/U_ATOMIC_COMMITS.md`
- **U_INTEGRATION_CHECK**: Complete Integration Check → `.claude/principles/U_INTEGRATION_CHECK.md`
- **U_COMPLETE_REPORTING**: Complete Action Reporting → `.claude/principles/U_COMPLETE_REPORTING.md`
- **U_EXPLICIT_COMPLETION**: Explicit Completion Criteria → `.claude/principles/U_EXPLICIT_COMPLETION.md`
- **U_NO_OVERENGINEERING**: No Overengineering → `.claude/principles/U_NO_OVERENGINEERING.md`
- **U_MINIMAL_TOUCH**: Minimal Touch Policy → `.claude/principles/U_MINIMAL_TOUCH.md`

**Testing & Quality Principles:**
- **P_TEST_COVERAGE**: Test Coverage Targets → `.claude/principles/P_TEST_COVERAGE.md`
- **P_TEST_PYRAMID**: Test Pyramid → `.claude/principles/P_TEST_PYRAMID.md`
- **P_CI_GATES**: CI Gates → `.claude/principles/P_CI_GATES.md`
- **P_LINTING_SAST**: Linting & SAST Enforcement → `.claude/principles/P_LINTING_SAST.md`
