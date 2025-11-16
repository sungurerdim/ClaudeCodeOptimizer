---
id: P_LINTING_SAST
title: Linting & SAST Enforcement
category: code_quality
severity: high
weight: 8
applicability:
  project_types: ['all']
  languages: ['all']
---

# P_LINTING_SAST: Linting & SAST Enforcement 🔴

**Severity**: High

Use linters (Ruff/ESLint) AND SAST tools (Semgrep/CodeQL/Snyk) with strict rules enforced in CI. Catch security vulnerabilities and code quality issues before production.

**Enforcement**: MUST

**Project Types**: all
**Languages**: all

---

## Why

### The Problem

**No linting/SAST allows bugs and vulnerabilities to reach production:**

- **Security Vulnerabilities** - SQL injection, XSS, hardcoded secrets slip through without SAST
- **Code Quality Issues** - Unused imports, undefined variables, type errors undetected
- **Inconsistent Style** - Code style varies across team without linting
- **Subtle Bugs** - Logic errors (unreachable code, always-true conditions) missed
- **No Safety Net** - Developers can commit dangerous code without warnings

### Core Techniques

**1. Python: Ruff + Bandit + Semgrep**

```toml
# pyproject.toml
[tool.ruff]
line-length = 120
target-version = "py311"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "F",   # pyflakes
    "W",   # pycodestyle warnings
    "S",   # bandit (security)
    "B",   # flake8-bugbear
    "I",   # isort
    "N",   # pep8-naming
    "UP",  # pyupgrade
]

[tool.ruff.lint.per-file-ignores]
"tests/*" = ["S101"]  # Allow assert in tests

# CI: .github/workflows/lint.yml
- name: Run Ruff
  run: ruff check src/

- name: Run Semgrep (SAST)
  uses: semgrep/semgrep-action@v1
  with:
    config: >-
      p/security-audit
      p/owasp-top-ten
      p/python
```

**2. JavaScript/TypeScript: ESLint + Security Plugins**

```javascript
// .eslintrc.js
module.exports = {
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:security/recommended',  // Security rules
  ],
  plugins: ['security', '@typescript-eslint'],
  rules: {
    'security/detect-object-injection': 'error',
    'security/detect-non-literal-regexp': 'warn',
    'security/detect-unsafe-regex': 'error',
    '@typescript-eslint/no-explicit-any': 'error',
  }
};

// package.json
"scripts": {
  "lint": "eslint src --ext .ts,.tsx --max-warnings 0"
}

// CI
- run: npm run lint
- uses: github/codeql-action/analyze@v2
```

**3. SAST Tools Configuration**

```yaml
# .semgrep.yml
rules:
  - id: hardcoded-secret
    pattern: |
      $X = "sk_live_..."
    message: Hardcoded Stripe secret key detected
    severity: ERROR

  - id: sql-injection
    pattern: |
      execute($QUERY)
    message: Potential SQL injection
    severity: ERROR

# .github/workflows/sast.yml
- name: Semgrep Scan
  uses: semgrep/semgrep-action@v1
  with:
    config: >-
      p/security-audit
      p/secrets
      p/owasp-top-ten

- name: CodeQL Analysis
  uses: github/codeql-action/init@v2
  with:
    languages: python, javascript

- name: Snyk Code Test
  run: snyk code test --severity-threshold=high
```

**4. Pre-commit Hooks (Fast Feedback)**

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: [-c, pyproject.toml]

# Install: pre-commit install
# Result: Linting on every commit (instant feedback)
```

**5. Fix Common Security Issues Found by SAST**

```python
# ❌ BAD: SQL Injection (flagged by Semgrep/Bandit)
def get_user(email):
    query = f"SELECT * FROM users WHERE email = '{email}'"
    cursor.execute(query)  # S608: SQL injection!

# ✅ GOOD: Parameterized query
def get_user(email):
    query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (email,))  # Safe!

# ❌ BAD: Hardcoded secret (flagged by Semgrep/trufflehog)
API_KEY = "sk_live_abc123def456"  # S105: Hardcoded password!

# ✅ GOOD: Environment variable
import os
API_KEY = os.environ["STRIPE_API_KEY"]  # Safe!

# ❌ BAD: Command injection (flagged by Bandit)
import subprocess
user_input = request.args.get('file')
subprocess.call(f"cat {user_input}", shell=True)  # S602: Shell injection!

# ✅ GOOD: Sanitized input
import shlex
user_input = shlex.quote(request.args.get('file'))
subprocess.call(["cat", user_input])  # Safe!
```

---

### Implementation Patterns

#### ✅ Good: Complete Linting + SAST Setup

```yaml
# CI Pipeline with full security scanning

name: Quality & Security

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

      - name: Install dependencies
        run: |
          pip install ruff bandit

      - name: Run Ruff (linting)
        run: ruff check src/ --output-format=github

      - name: Run Bandit (security)
        run: bandit -r src/ -f json -o bandit-report.json

  sast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Semgrep Scan
        uses: semgrep/semgrep-action@v1
        with:
          config: >-
            p/security-audit
            p/owasp-top-ten
            p/secrets

      - name: CodeQL Analysis
        uses: github/codeql-action/init@v2
        with:
          languages: python
      - uses: github/codeql-action/analyze@v2

      - name: Snyk Security Scan
        uses: snyk/actions/python@master
        with:
          command: code test

# Result: 4 layers of security scanning on every PR
```

---

#### ❌ Bad: No Linting or SAST

```python
# ❌ BAD: Code with no linting/SAST catches none of these:

import requests  # Unused import (would be caught by Ruff)

def get_data(user_id):
    # SQL injection vulnerability (would be caught by Semgrep)
    query = f"SELECT * FROM users WHERE id = {user_id}"
    db.execute(query)

    # Hardcoded secret (would be caught by truffleHog)
    api_key = "sk_live_1234567890"

    # Type error (would be caught by mypy)
    result = "string" + 5  # TypeError!

    # Unreachable code (would be caught by Ruff)
    return result
    print("This never executes")

# All these issues deploy to production without linting/SAST!
```

---

## Anti-Patterns

### ❌ Anti-Pattern 1: Ignoring Linter Warnings

**Problem**: Using `# noqa` or `// eslint-disable` to silence warnings instead of fixing.

```python
# ❌ BAD: Silence security warnings
def unsafe_query(user_input):
    query = f"SELECT * FROM data WHERE id = {user_input}"  # noqa: S608
    # Silenced SQL injection warning!

# ✅ GOOD: Fix the issue
def safe_query(user_input):
    query = "SELECT * FROM data WHERE id = %s"
    cursor.execute(query, (user_input,))
```

**Impact:** Security vulnerabilities slip through

---

### ❌ Anti-Pattern 2: SAST Without Action

**Problem**: Running SAST but not fixing findings.

```bash
# ❌ BAD: SAST finds issues but CI still passes
- run: semgrep --config=p/security-audit || true  # Ignores failures!

# ✅ GOOD: Fail CI on security issues
- run: semgrep --config=p/security-audit --error
```

**Impact:** False sense of security

---

## Implementation Checklist

### Linting Setup

- [ ] **Configure linter** - Ruff (Python), ESLint (JS), Clippy (Rust)
- [ ] **Enable security rules** - Bandit (Python), eslint-plugin-security (JS)
- [ ] **Strict mode** - Zero warnings allowed in CI
- [ ] **Pre-commit hooks** - Lint on every commit

### SAST Setup

- [ ] **Semgrep** - Configure rulesets (p/security-audit, p/owasp-top-ten)
- [ ] **CodeQL** - Enable for GitHub repos
- [ ] **Snyk Code** - Scan for vulnerabilities
- [ ] **Secret scanning** - truffleHog, GitGuardian, or GitHub secret scanning

### CI Enforcement

- [ ] **Linting in CI** - Fail build on lint errors
- [ ] **SAST in CI** - Fail build on high-severity findings
- [ ] **PR comments** - Bot comments on lint/SAST findings
- [ ] **Block merge** - Don't allow merge with failures

---

## Summary

**Linting & SAST Enforcement** means using linters (Ruff/ESLint) AND SAST tools (Semgrep/CodeQL/Snyk) with strict rules enforced in CI to catch security vulnerabilities and code quality issues before production.

**Core Rules:**
- **Linting required** - Ruff/ESLint with strict rules
- **SAST required** - Semgrep + CodeQL + Snyk
- **CI enforcement** - Build fails on lint/SAST errors
- **Pre-commit hooks** - Fast local feedback
- **Fix, don't ignore** - Don't silence warnings
