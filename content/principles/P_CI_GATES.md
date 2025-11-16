---
id: P_CI_GATES
title: CI Gates
category: testing
severity: high
weight: 8
applicability:
  project_types: ['all']
  languages: ['all']
---

# P_CI_GATES: CI Gates 🔴

**Severity**: High

All PRs must pass mandatory CI gates (linting, testing, coverage, security scans, build verification) before merge. No bypassing gates, no manual overrides without documented approval.

**Enforcement**: MUST

**Project Types**: all
**Languages**: all

---

## Why

### The Problem

**No CI gates allows broken code to reach production:**

- **Broken Code Merged** - Code with lint errors, test failures, or security vulnerabilities merged to main
- **Inconsistent Quality** - Developers can skip quality checks, leading to variable code quality
- **Manual Review Bottleneck** - Reviewers waste time catching issues that automation should catch
- **Production Bugs** - Untested code paths and broken functionality discovered by users
- **Regression Risk** - Changes break existing functionality without detection
- **No Accountability** - Can't track when/why quality standards were bypassed

### Core Techniques

**1. Linting Gate (Code Quality)**

```yaml
# .github/workflows/ci.yml

name: CI Pipeline

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install linter
        run: pip install ruff

      - name: Run Ruff (linting)
        run: ruff check src/ --output-format=github

      # ✅ CI fails if linting fails (gate enforced)
```

**2. Testing Gate (Functionality Verification)**

```yaml
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -e .
          pip install pytest pytest-cov

      - name: Run tests
        run: pytest tests/ -v --tb=short

      # ✅ CI fails if any test fails (gate enforced)
```

**3. Coverage Gate (Test Completeness)**

```yaml
  coverage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -e .
          pip install pytest pytest-cov

      - name: Run tests with coverage
        run: pytest --cov=src --cov-report=term --cov-fail-under=80

      # ✅ CI fails if coverage < 80% (gate enforced)

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          fail_ci_if_error: true
```

**4. Security Scanning Gate (SAST)**

```yaml
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run Semgrep (SAST)
        uses: semgrep/semgrep-action@v1
        with:
          config: >-
            p/security-audit
            p/owasp-top-ten
            p/secrets

      - name: Run CodeQL Analysis
        uses: github/codeql-action/init@v2
        with:
          languages: python

      - uses: github/codeql-action/analyze@v2

      # ✅ CI fails if high-severity security issues found (gate enforced)
```

**5. Build Gate (Deployment Readiness)**

```yaml
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Build application
        run: |
          python -m build
          pip install dist/*.whl

      - name: Verify build
        run: python -c "import claudecodeoptimizer; print(claudecodeoptimizer.__version__)"

      # ✅ CI fails if build fails (gate enforced)
```

**6. Branch Protection Rules (Enforce Gates)**

```yaml
# GitHub Settings -> Branches -> Branch protection rules for 'main'

✅ Require status checks to pass before merging
  ✅ lint
  ✅ test
  ✅ coverage
  ✅ security
  ✅ build

✅ Require branches to be up to date before merging
✅ Do not allow bypassing the above settings
✅ Require approvals: 1
```

**7. Composite CI Pipeline (All Gates)**

```yaml
# .github/workflows/ci.yml (complete)

name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  # Gate 1: Code Quality
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install ruff
      - run: ruff check src/ --output-format=github

  # Gate 2: Type Safety
  typecheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install mypy
      - run: mypy src/ --strict

  # Gate 3: Testing
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -e .[test]
      - run: pytest tests/ -v --tb=short

  # Gate 4: Coverage
  coverage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -e .[test]
      - run: pytest --cov=src --cov-fail-under=80 --cov-report=xml
      - uses: codecov/codecov-action@v3

  # Gate 5: Security
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: semgrep/semgrep-action@v1
        with:
          config: p/security-audit

  # Gate 6: Build
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: python -m build
      - run: pip install dist/*.whl
      - run: python -c "import claudecodeoptimizer"

  # All gates must pass for PR to be mergeable
```

---

### Implementation Patterns

#### ✅ Good: Comprehensive CI Gates

```yaml
# Complete CI pipeline with all essential gates

name: Quality Gates

on: [pull_request]

jobs:
  # Gate 1: Code style and quality
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm install
      - run: npm run lint  # ESLint with strict rules
      # ✅ Fails CI if any lint errors

  # Gate 2: Type checking
  typecheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm install
      - run: npm run typecheck  # TypeScript strict mode
      # ✅ Fails CI if any type errors

  # Gate 3: Unit + Integration tests
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm install
      - run: npm test  # Jest/Vitest
      # ✅ Fails CI if any test fails

  # Gate 4: Coverage threshold
  coverage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm install
      - run: npm test -- --coverage --coverageThreshold='{"global":{"lines":80}}'
      # ✅ Fails CI if coverage < 80%

  # Gate 5: Security scanning
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: semgrep/semgrep-action@v1
      - run: npm audit --audit-level=high
      # ✅ Fails CI if high-severity vulnerabilities found

  # Gate 6: Build verification
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm install
      - run: npm run build
      # ✅ Fails CI if build fails

# Branch protection requires ALL gates to pass
```

---

#### ✅ Good: Gate Failure Transparency

```yaml
# CI with clear failure reporting

- name: Run tests
  run: pytest tests/ -v --tb=short
  # If fails, shows clear error message with test names

- name: Coverage check
  run: |
    coverage run -m pytest
    coverage report --fail-under=80 --show-missing
  # If fails, shows which files are under-covered

- name: Linting
  run: ruff check src/ --output-format=github
  # If fails, shows file:line annotations in GitHub UI

# ✅ Developers get actionable feedback on gate failures
```

---

#### ❌ Bad: Skipping Gates

```yaml
# ❌ BAD: Bypass gates with || true

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: pytest tests/ || true  # ❌ Always succeeds, even if tests fail!

  lint:
    runs-on: ubuntu-latest
    steps:
      - run: ruff check src/ || echo "Linting failed but continuing"  # ❌ Gate bypassed!

  coverage:
    runs-on: ubuntu-latest
    steps:
      - run: pytest --cov=src --cov-fail-under=80 || true  # ❌ No coverage enforcement!

# Problem: All gates pass even when quality checks fail!
# Impact: Broken code merged to main, production bugs
```

---

#### ❌ Bad: No Branch Protection

```yaml
# ❌ BAD: CI runs but results ignored

# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: pytest tests/  # ✅ Tests run

# But no branch protection rules configured!
# → Developers can merge PRs even if CI fails
# → No enforcement of quality gates

# ✅ GOOD: Configure branch protection
# GitHub Settings -> Branches -> main
# ✅ Require status checks to pass before merging
# ✅ Require "test", "lint", "coverage" checks
```

---

## Anti-Patterns

### ❌ Anti-Pattern 1: Manual Override of Gates

**Problem**: Allowing developers to bypass CI gates "just this once."

```yaml
# ❌ BAD: Allow manual bypass

# Branch protection:
❌ Allow administrators to bypass required status checks
❌ Allow force pushes to main

# Result: Developers bypass gates when under pressure
# "We'll fix the tests later" (never happens)

# ✅ GOOD: No bypasses
✅ Require status checks to pass before merging
✅ Do not allow bypassing the above settings
✅ Include administrators in restrictions
```

**Impact**: Quality gates become optional, code quality degrades

---

### ❌ Anti-Pattern 2: Too Many Gates (Slow Feedback)

**Problem**: CI takes 30+ minutes, developers work around it.

```yaml
# ❌ BAD: Slow CI pipeline

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - run: slow_linter  # 5 minutes

  test:
    runs-on: ubuntu-latest
    steps:
      - run: pytest tests/  # 15 minutes (no parallelization)

  e2e:
    runs-on: ubuntu-latest
    steps:
      - run: cypress run  # 20 minutes (all E2E tests on every PR)

# Total: 40 minutes
# Result: Developers push commits without waiting for CI

# ✅ GOOD: Fast gates
jobs:
  quick-checks:  # <2 minutes
    - run: ruff check src/  # 10 seconds
    - run: mypy src/  # 30 seconds
    - run: pytest tests/unit/ -n auto  # 1 minute (parallel)

  full-tests:  # <10 minutes
    - run: pytest tests/ -n auto  # 8 minutes (parallel)

  nightly-e2e:  # Run on schedule, not every PR
    - run: cypress run
```

**Impact**: Slow CI leads to workarounds, defeats purpose of gates

---

### ❌ Anti-Pattern 3: Gates Without Actionable Feedback

**Problem**: CI fails but developers don't know why or how to fix.

```yaml
# ❌ BAD: Unclear failure messages

- name: Run tests
  run: pytest tests/ --tb=no  # No traceback!
  # Fails with: "AssertionError" (no context)

- name: Coverage
  run: coverage run -m pytest && coverage report --fail-under=80
  # Fails with: "Total coverage: 78%" (doesn't show which files)

# ✅ GOOD: Clear, actionable feedback

- name: Run tests
  run: pytest tests/ -v --tb=short
  # Fails with: "test_login FAILED: AssertionError: Expected 200, got 401"

- name: Coverage
  run: |
    coverage run -m pytest
    coverage report --fail-under=80 --show-missing
  # Fails with:
  # src/auth.py: 65% coverage (lines 45-50, 78-82 missing)
  # src/payment.py: 72% coverage (lines 120-135 missing)
```

**Impact**: Developers waste time debugging unclear failures

---

## Implementation Checklist

### CI Pipeline Setup

- [ ] **Linting gate** - Ruff (Python), ESLint (JS), Clippy (Rust)
- [ ] **Type checking gate** - mypy (Python), TypeScript strict mode
- [ ] **Testing gate** - pytest, Jest, Vitest with failure reporting
- [ ] **Coverage gate** - 80% minimum, fail under threshold
- [ ] **Security gate** - Semgrep, CodeQL, dependency scanning
- [ ] **Build gate** - Verify successful build/compilation

### Branch Protection

- [ ] **Require status checks** - All gates must pass before merge
- [ ] **Require branch up-to-date** - Rebase before merge
- [ ] **No force pushes** - Prevent history rewriting on main
- [ ] **No bypassing gates** - Applies to everyone, including admins
- [ ] **Require code review** - At least 1 approval required

### Performance Optimization

- [ ] **Parallel jobs** - Run gates concurrently (not sequentially)
- [ ] **Caching** - Cache dependencies (pip cache, npm cache)
- [ ] **Matrix testing** - Test multiple versions in parallel
- [ ] **Fast feedback** - Quick checks first (lint before slow tests)

### Developer Experience

- [ ] **Clear failure messages** - Actionable error output
- [ ] **Fast CI** - Total time <10 minutes for standard checks
- [ ] **PR comments** - Bot comments with coverage, lint results
- [ ] **Pre-commit hooks** - Catch issues locally before CI

---

## Summary

**CI Gates** means all PRs must pass mandatory automated gates (linting, testing, coverage, security scans, build verification) before merge. No bypassing gates, no manual overrides without documented approval.

**Core Rules:**
- **All gates required** - Lint, test, coverage, security, build must all pass
- **Branch protection enforced** - GitHub/GitLab blocks merge if gates fail
- **No bypassing** - No `|| true`, no admin overrides
- **Fast feedback** - CI completes in <10 minutes
- **Actionable errors** - Clear messages on gate failures
