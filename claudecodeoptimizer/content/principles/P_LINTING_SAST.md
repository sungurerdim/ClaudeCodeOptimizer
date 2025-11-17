# P_LINTING_SAST: Linting & SAST Enforcement

**Severity**: High

 SQL injection, XSS, hardcoded secrets slip through without SAST Unused imports, undefined variables, type errors undetected Code style varies across team without linting Logic errors (unreachable cod.

---

## Rules

- *No rules extracted*

---

## Examples

### ✅ Good
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
```
**Why right**: ---

### ❌ Bad
```python
# ❌ BAD: Code with no linting/SAST catches none of these:

import requests  # Unused import (would be caught by Ruff)

def get_data(user_id):
    # SQL injection vulnerability (would be caught by Semgrep)
    query = f"SELECT * FROM users WHERE id = {user_id}"
    db.execute(query)

    # Hardcoded secret (would be caught by truffleHog)
    api_key = "sk_live_1234567890"
```
**Why wrong**: ---
