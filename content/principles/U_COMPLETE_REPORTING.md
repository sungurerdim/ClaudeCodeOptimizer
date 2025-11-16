---
id: U_COMPLETE_REPORTING
title: Complete Action Reporting
category: universal
severity: critical
weight: 10
enforcement: SHOULD
applicability:
  project_types: ['all']
  languages: ['all']
---

# U_COMPLETE_REPORTING: Complete Action Reporting 🔴

**Severity**: Critical

Every action must be explicitly reported to the user with precise file references. No hidden operations, no vague locations.

**Why**: Enables user to verify changes and navigate directly to affected code

**Enforcement**: SHOULD

**Project Types**: all
**Languages**: all

**Rules**:
- **Explicit File References**: Always include `file_path:line_number` when referencing code
- **Report All Actions**: Every file read, edit, search explicitly stated
- **No Hidden Operations**: No silent fixes or background changes

**❌ Bad - Vague References**:
```
"Fixed the authentication bug"
"Updated the API to handle errors"
"Improved the caching logic"
```

**✅ Good - Precise References**:
```
"Fixed authentication bug in src/auth.py:127"
"Updated API error handling in api/main.py:89-105"
"Improved caching in shared/storage.py:200-220"
```

**Examples**:

When reporting changes:
```
✅ "Added JWT refresh token support to shared/auth.py:127-145"
✅ "Fixed SQL injection in services/api/main.py:89 (parameterized query)"
✅ "Refactored Redis connection in shared/storage.py:200-220"
```

When answering questions:
```
✅ "Authentication happens in shared/auth.py:50-80"
✅ "Rate limiting is configured in shared/settings.py:120"
✅ "Database connection pool is managed in shared/core.py:30"
```

## Integration with Other Principles

- **U_EVIDENCE_BASED** (Evidence-Based Verification): Requires verifiable proof
- **U_COMPLETE_REPORTING** (Complete Action Reporting): Requires precise location references
- **U_EXPLICIT_COMPLETION** (Explicit Completion Criteria): Together ensure verifiable, locatable results
