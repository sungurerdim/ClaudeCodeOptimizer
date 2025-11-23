---
name: ci_gates
description: Enforce quality gates in CI/CD pipelines for code and security standards
type: project
severity: high
keywords: [ci, cd, gates, quality, automation]
category: [quality]
related_skills: []
---
# P_CI_GATES: CI Gates

**Severity**: High

 Code with lint errors, test failures, or security vulnerabilities merged to main Developers can skip quality checks, leading to variable code quality Reviewers waste time catching issues that automat.

---

## Rules

- *No rules extracted*

---

## Examples

### ✅ Good
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

```
**Why right**: ---

### ❌ Bad
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
```
**Why wrong**: ---
---

## Checklist

- [ ] *No rules extracted*

