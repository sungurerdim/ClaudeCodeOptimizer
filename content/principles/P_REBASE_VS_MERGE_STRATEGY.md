---
id: P_REBASE_VS_MERGE_STRATEGY
title: Rebase vs Merge Strategy
category: project-specific
severity: low
weight: 5
applicability:
  project_types: ['all']
  languages: ['all']
---

# P_REBASE_VS_MERGE_STRATEGY: Rebase vs Merge Strategy 🟢

**Severity**: Low

Rebase feature branches, merge to main (clean history).

**Why**: Documents changes clearly through structured PR descriptions and review comments

**Enforcement**: Skills required - verification_protocol, root_cause_analysis

**Project Types**: all
**Languages**: all

**❌ Bad**:
```
# Merge commits everywhere, messy history
```

**✅ Good**:
```
git rebase main  # Clean feature branch
git merge --no-ff feature  # To main
```
