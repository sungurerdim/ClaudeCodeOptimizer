---
id: P_IMMUTABILITY_BY_DEFAULT
title: Immutability by Default
category: code_quality
severity: medium
weight: 6
applicability:
  project_types: ['all']
  languages: ['python', 'javascript', 'typescript']
---

# P_IMMUTABILITY_BY_DEFAULT: Immutability by Default 🟡

**Severity**: Medium

Use frozen dataclasses, const by default, minimize mutable state.

**Why**: Keeps functions focused on one task making them easier to test and reuse

**Enforcement**: Skills required - verification_protocol, test_first, root_cause_analysis

**Project Types**: all
**Languages**: python, javascript, typescript

**Rules**:
- **Prefer Frozen Dataclass**: Use frozen=True for dataclasses

**❌ Bad**:
```
@dataclass
class User:  # Mutable
```

**✅ Good**:
```
@dataclass(frozen=True)
class User:  # Immutable
```

## Autofix Available
