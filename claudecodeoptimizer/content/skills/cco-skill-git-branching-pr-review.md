---
title: Git Workflow, Branching & PR Review
category: git
description: Branching strategy, PR guidelines, commit conventions, code review checklists, merge vs rebase
metadata:
  name: "Git Workflow, Branching & PR Review"
  activation_keywords: ["git", "branch", "branching strategy", "feature branch", "trunk-based", "pull request", "PR", "merge request", "code review", "commit", "commit message", "conventional commits", "merge", "rebase", "squash", "cherry-pick", "conflict", "CODEOWNERS", "PR template"]
  category: "git"
principles: ['P_BRANCHING_STRATEGY', 'P_PR_GUIDELINES', 'P_COMMIT_MESSAGE_CONVENTIONS', 'P_GIT_COMMIT_QUALITY', 'P_CODE_REVIEW_CHECKLIST_COMPLIANCE', 'P_REBASE_VS_MERGE_STRATEGY']
use_cases:
  development_philosophy: [quality_first, balanced, move_fast]
  project_maturity: [greenfield, active-dev, production]
---

# Git Workflow, Branching & PR Review

## Domain
Git branching, PR workflow, commit quality, code review

## Purpose
Prevent merge conflicts, maintain clean history, ensure PR quality

## Techniques

**Branch**: <3 days, `feature/auth`, trunk-based, feature flags

**Commit**: `type(scope): msg` (feat/fix/docs), atomic, <200 lines

**PR**: <400 lines, template (summary/test/checklist), 1-2 reviewers, CI passes

**Review**: security (auth/validation/secrets), tests, performance (N+1), docs

**Merge**: feature=rebase, hotfix=merge, main=squash

## Patterns

### Commit
```bash
feat(auth): add JWT refresh token
fix(api): handle null in /profile
docs: update install steps
```

### PR
```markdown
## Summary
Added user profile API for mobile

## Testing
- [x] Unit tests pass
- [x] Manual: create/update/delete
- [x] Edge: invalid ID, missing fields
```

### Rebase
```bash
git checkout feature/api
git rebase origin/main
git push --force-with-lease
```

### Review
```
Security: input validation, auth, secrets
Quality: tests, errors, docs
Performance: N+1, indexes, loops
```

## Checklist
- [ ] Branch <3 days, conventional commits
- [ ] PR <400 lines, tests pass
- [ ] Review: security/quality/perf
- [ ] Merge: rebase/squash, docs updated
