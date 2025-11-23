---
name: git-branching-pr-review
description: Prevent merge conflicts, maintain clean history, ensure PR quality. Includes branching strategies (trunk-based, feature flags), conventional commits, PR templates, code review checklists, and rebase vs merge decision framework.
keywords: [git, branch, branching strategy, feature branch, trunk-based, pull request, PR, merge request, code review, commit, conventional commits, merge, rebase, squash, cherry-pick, conflict, CODEOWNERS]
category: quality
related_commands:
  action_types: [audit, generate, fix]
  categories: [quality]
pain_points: [3, 4]
---

# Git Workflow, Branching & PR Review

---

## Standard Structure

**This skill follows [STANDARDS_SKILLS.md](../STANDARDS_SKILLS.md):**

- **Standard sections** - Domain, Purpose, Core Techniques, Anti-Patterns, Checklist
- **Code example format** - Bad/Good pattern with specific examples
- **Detection pattern format** - Python functions with Finding objects
- **Checklist format** - Specific, verifiable items

**See STANDARDS_SKILLS.md for format details. Only skill-specific content is documented below.**

---

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

## Command Discovery Protocol

When this skill is active, find relevant commands by searching `~/.claude/commands/` metadata:

```yaml
# Search criteria for this skill's domain
action_types: [audit, generate, fix]
keywords: [git, branch, PR, commit, review, merge, rebase]
category: quality
pain_points: [3, 4]
```

**How Claude finds commands:**
1. Grep command files for `keywords:.*[pattern]` in frontmatter
2. Match `category: quality`
3. Present matching commands with their parameters

This ensures commands are always current even when renamed or updated.
