---
id: P_SEMANTIC_VERSIONING
title: Semantic Versioning
category: project-specific
severity: medium
weight: 7
applicability:
  project_types: ['library', 'api']
  languages: ['all']
---

# P_SEMANTIC_VERSIONING: Semantic Versioning 🟡

**Severity**: Medium

SemVer: MAJOR.MINOR.PATCH for breaking/features/fixes.

**Why**: Communicates change impact through semantic versioning of breaking changes and features

**Enforcement**: Skills required - verification_protocol, root_cause_analysis

**Project Types**: library, api
**Languages**: all

**❌ Bad**:
```
# Random version numbers
```

**✅ Good**:
```
# v2.0.0 (breaking), v1.5.0 (feature), v1.4.1 (fix)
```
