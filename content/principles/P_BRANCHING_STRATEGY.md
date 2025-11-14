---
id: P_BRANCHING_STRATEGY
title: Branching Strategy
category: project-specific
severity: medium
weight: 6
applicability:
  project_types: ['all']
  languages: ['all']
---

# P_BRANCHING_STRATEGY: Branching Strategy 🟡

**Severity**: Medium

Git Flow for releases, Trunk-Based for CI/CD.

**Why**: Improves test quality by verifying tests actually catch bugs through mutation testing

**Enforcement**: Skills required - verification_protocol, root_cause_analysis

**Project Types**: all
**Languages**: all

**❌ Bad**:
```
# Everyone commits to main
```

**✅ Good**:
```
# Feature branches -> main (with CI/CD)
```
