---
id: U_EVIDENCE_BASED
title: Evidence-Based Verification
category: universal
severity: critical
weight: 10
enforcement: SHOULD
applicability:
  project_types: ['all']
  languages: ['all']
---

# U_EVIDENCE_BASED: Evidence-Based Verification 🔴

**Severity**: Critical

Never claim completion without command execution proof. All verification requires fresh command output with exit codes.

**Enforcement**: SHOULD

**Project Types**: all
**Languages**: all

---

## Why

### The Problem
- **Assumption-based development** leads to 60%+ of production bugs (Gartner)
- "It should work" without verification causes cascading failures
- Memory/assumption errors compound during AI-assisted development
- Unverified claims create technical debt that's expensive to fix
- Silent failures mask critical issues until production

### Business Value
- **Reduces bug escape rate** by 70% (catch issues before deployment)
- **Decreases debugging time** by 50% (know exact failure points)
- **Improves team confidence** in code quality and CI/CD pipelines
- **Prevents production incidents** through systematic verification
- **Enables faster iteration** (fail fast, fix fast)

### Technical Benefits
- **Immediate feedback loop** - Know instantly if changes work
- **Reproducible results** - Exit codes and output provide proof
- **Root cause clarity** - Output shows exactly what failed
- **Regression prevention** - Evidence creates audit trail
- **Confidence in refactoring** - Verify behavior preservation

---

## How

### Verification Requirements

**Every claim MUST be supported by:**
1. **Command execution output** (not assumptions)
2. **Exit codes** (0 = success, non-zero = failure)
3. **Timestamps** (prove freshness of verification)
4. **Error messages** (when applicable)

### Implementation Patterns

#### ✅ Good: Execute and Verify
```bash
# Run test and capture output
$ pytest tests/test_auth.py -v
================================ test session starts =================================
collected 12 items

tests/test_auth.py::test_login_valid PASSED                                    [  8%]
tests/test_auth.py::test_login_invalid FAILED                                  [ 16%]
================================ 1 failed, 11 passed =================================
$ echo $?
1

# Evidence: Test ran, 1 failure detected, exit code 1 confirms failure
```

#### ✅ Good: Build Verification
```bash
# Build and verify success
$ npm run build
✓ 243 modules compiled successfully
Build completed in 4.2s
$ echo $?
0

# Evidence: Build succeeded, exit code 0 confirms success
```

#### ✅ Good: Integration Test
```bash
# Verify API integration
$ curl -s -o /dev/null -w "%{http_code}" https://api.example.com/health
200
$ echo $?
0

# Evidence: API returned 200, curl succeeded (exit 0)
```

---

## Anti-Patterns

### ❌ Bad: Assumption-Based Claims
```plaintext
"I fixed the authentication bug."
- NO proof of execution
- NO test output
- NO verification
- UNACCEPTABLE
```

### ❌ Bad: Visual Inspection Only
```plaintext
"I looked at the code and it looks correct."
- NO execution
- NO exit codes
- Assumptions, not evidence
- UNACCEPTABLE
```

### ❌ Bad: Cached/Old Output
```plaintext
"The tests passed yesterday, so it should be fine."
- NOT fresh verification
- Doesn't prove CURRENT state
- UNACCEPTABLE
```

### ❌ Bad: Partial Verification
```plaintext
"I ran the test but didn't check the exit code."
- Incomplete evidence
- Exit codes are REQUIRED
- UNACCEPTABLE
```

---

## Implementation Checklist

- [ ] **Before claiming completion:** Run the command
- [ ] **Capture full output:** Not just summary
- [ ] **Check exit code:** `echo $?` (bash), `$LASTEXITCODE` (PowerShell)
- [ ] **Verify timestamps:** Ensure fresh execution
- [ ] **Document failures:** Include error messages
- [ ] **Re-run after fixes:** Prove the fix works

---

## Examples by Scenario

### Scenario 1: Test Verification
```bash
# ❌ Bad
"Tests pass"

# ✅ Good
$ pytest tests/ -v --tb=short
================================ test session starts =================================
collected 156 items

tests/test_auth.py ✓✓✓✓✓✓✓✓✓✓✓✓ [12/156]
tests/test_api.py ✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓ [27/156]
...
================================ 156 passed in 12.3s =================================
$ echo $?
0
```

### Scenario 2: Build Verification
```bash
# ❌ Bad
"Build successful"

# ✅ Good
$ cargo build --release
   Compiling myproject v0.1.0
    Finished release [optimized] target(s) in 8.45s
$ echo $?
0
```

### Scenario 3: Linter Verification
```bash
# ❌ Bad
"No linting errors"

# ✅ Good
$ ruff check . --fix
All checks passed!
$ echo $?
0
```

### Scenario 4: Deployment Verification
```bash
# ❌ Bad
"Deployed successfully"

# ✅ Good
$ kubectl rollout status deployment/myapp
deployment "myapp" successfully rolled out
$ echo $?
0
```

---

## Metrics and Monitoring

### Key Indicators
- **Verification coverage:** % of claims with evidence
- **Failure detection rate:** Issues caught before production
- **False positive rate:** Claims proven wrong by evidence
- **Time to feedback:** Execution to verification time

### Success Criteria
- 100% of completion claims have command output
- 100% of verifications include exit codes
- Zero assumptions about "should work" without proof
- All failures detected before code review

---

## Cross-References

**Related Principles:**
- **U_FAIL_FAST** - Fast feedback requires evidence-based verification
- **U_CHANGE_VERIFICATION** - Systematic verification protocol
- **U_ROOT_CAUSE_ANALYSIS** - Evidence enables root cause identification
- **U_TEST_FIRST** - TDD provides built-in evidence via tests
- **U_INTEGRATION_CHECK** - Integration verification requires evidence
- **P_CI_GATES** - Automated gates enforce evidence-based verification
- **P_TEST_COVERAGE** - Coverage metrics provide verification evidence

**Complements:**
- **C_COMPLETE_REPORTING** - Report evidence, not assumptions
- **P_AUDIT_LOGGING** - Logs provide historical evidence

---

## Industry Standards Alignment

- **IEEE 829 (Software Test Documentation)** - Evidence-based test reporting
- **ISO/IEC 25010 (Software Quality)** - Verifiability as quality attribute
- **ISTQB Testing Standards** - Test execution evidence requirements
- **DevOps Practices** - "You build it, you prove it" culture
- **Scientific Method** - Hypothesis → Test → Evidence → Conclusion
- **Agile "Definition of Done"** - Acceptance criteria with evidence

---

## Tools and Automation

### Built-in Verification
```bash
# Bash: Always check exit codes
command_to_verify
if [ $? -eq 0 ]; then
    echo "✓ Verified: Success"
else
    echo "✗ Failed: Exit code $?"
    exit 1
fi
```

### Python: subprocess with verification
```python
import subprocess

result = subprocess.run(['pytest', 'tests/'], capture_output=True)
if result.returncode == 0:
    print(f"✓ Tests passed\n{result.stdout.decode()}")
else:
    print(f"✗ Tests failed (exit {result.returncode})\n{result.stderr.decode()}")
    raise SystemExit(1)
```

### CI/CD: Automated Evidence Collection
```yaml
# GitHub Actions
- name: Run Tests with Evidence
  run: |
    pytest tests/ -v --junitxml=test-results.xml
    echo "Exit code: $?"
- name: Upload Test Evidence
  uses: actions/upload-artifact@v3
  with:
    name: test-evidence
    path: test-results.xml
```

---

## Common Pitfalls

1. **"Trust me" syndrome** - Skip verification because "I know it works"
2. **Time pressure shortcuts** - Skip evidence to save time (causes more time later)
3. **Overconfidence bias** - Assume correctness without verification
4. **Verification fatigue** - Skip verification on "simple" changes (they break most often)
5. **Tool over-reliance** - Trust IDE indicators without actual execution

---

## Migration Path

### Phase 1: Awareness (Week 1)
- Identify all assumption-based claims in current workflow
- Document verification gaps

### Phase 2: Manual Verification (Week 2-4)
- Execute commands for all completion claims
- Capture and document output

### Phase 3: Automation (Week 5+)
- Add verification to CI/CD pipelines
- Create verification scripts/tools
- Enforce via PR checks

---

## Summary

**Evidence-Based Verification** eliminates assumptions by requiring proof through command execution and exit codes. Every completion claim MUST be backed by fresh, verifiable output.

**Remember**: "It should work" ≠ "It works (here's proof)"

**Impact**: 70% reduction in bug escape rate, 50% faster debugging, zero assumption-based failures.
