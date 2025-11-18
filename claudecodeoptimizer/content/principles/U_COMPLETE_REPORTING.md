---
name: complete-reporting
description: Every action must be explicitly reported with precise file references for verification and navigation
type: universal
severity: critical
keywords: [reporting, documentation, precision, traceability]
category: [quality, workflow]
---

# U_COMPLETE_REPORTING: Complete Action Reporting

**Severity**: Critical

Every action must be explicitly reported with precise file references. No hidden operations, no vague locations.

---

## Why

Enables user verification and direct navigation to affected code via `file_path:line_number` format.

---

## Rules

- **Precise References**: Always `file_path:line_number` when referencing code
- **Report All Actions**: Every file read, edit, search explicitly stated
- **No Hidden Ops**: No silent fixes or background changes

---

## Examples

### ❌ Bad - Vague
```
"Fixed the authentication bug"
"Updated the API to handle errors"
"Improved the caching logic"
```

### ✅ Good - Precise
```
"Fixed authentication bug in <auth_file>.py:<line>"
"Updated API error handling in <api_file>.py:<line_range>"
"Improved caching in <cache_file>.py:<line_range>"
```

---

## Reporting Pattern

**When reporting changes:**
```
✅ "Added JWT refresh token support to <auth_file>.py:<line>-145"
✅ "Fixed SQL injection in services/<api_file>.py:89 (parameterized query)"
✅ "Refactored Redis connection in <cache_file>.py:<line_range>"
```

**When answering questions:**
```
✅ "Authentication happens in <auth_file>.py:<line_range>"
✅ "Rate limiting configured in <config_file>.py:<line>"
✅ "DB connection pool managed in <core_file>.py:<line>"
```

---

## Integration

Works with:
- **U_EVIDENCE_BASED**: Requires verifiable proof
- **U_EXPLICIT_COMPLETION**: Together ensure verifiable, locatable results
