---
id: P_CODE_REVIEW_CHECKLIST_COMPLIANCE
title: Code Review Checklist Compliance
category: code_quality
severity: medium
weight: 7
applicability:
  project_types: ['all']
  languages: ['all']
---

# P_CODE_REVIEW_CHECKLIST_COMPLIANCE: Code Review Checklist Compliance 🟡

**Severity**: Medium

All PRs must pass mandatory code review checklist (large teams).

**Why**: Prevents tight coupling by hiding implementation details behind clean interfaces

**Enforcement**: Skills required - verification_protocol

**Project Types**: all
**Languages**: all

**❌ Bad**:
```
# No checklist, reviewers inconsistent
```

**✅ Good**:
```
# PR template with checklist:
- [ ] Tests added
- [ ] Docs updated
```
