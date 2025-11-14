---
id: P_COMMIT_MESSAGE_CONVENTIONS
title: Commit Message Conventions
category: project-specific
severity: medium
weight: 6
applicability:
  project_types: ['all']
  languages: ['all']
---

# P_COMMIT_MESSAGE_CONVENTIONS: Commit Message Conventions 🟡

**Severity**: Medium

Use Conventional Commits: feat/fix/docs/refactor/test.

**Why**: Validates user workflows through end-to-end tests of complete system flows

**Enforcement**: Skills required - verification_protocol, root_cause_analysis

**Project Types**: all
**Languages**: all

**❌ Bad**:
```
git commit -m 'fixed stuff'
```

**✅ Good**:
```
git commit -m 'fix(api): handle null user_id in /jobs endpoint'
```
