---
title: Verification Protocol
category: quality
tags: [verification, testing, evidence, quality]
description: Evidence-based verification workflow for all changes
use_cases:
  development_philosophy: [quality_first]
  project_maturity: [production, legacy, active-dev]
  team_dynamics: [small-2-5, medium-10-20, large-20-50]
  testing_approach: [comprehensive, balanced]
---

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

Never: "should work", "looks correct", "appears to", "seems", "probably", "might be"

Always show: Command output, exit codes, actual results, specific counts

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
2. **Debugging**: Proof it worked before simplifies troubleshooting
3. **Accountability**: Evidence shows work was done
4. **Reproducibility**: Others can verify results
5. **Learning**: Shows the *how*, not just the *what*
