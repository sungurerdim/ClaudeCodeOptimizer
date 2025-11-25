---
name: cco-skill-git-workflow
description: Prevent merge conflicts, maintain clean history, ensure PR quality. Includes branching strategies (trunk-based, feature flags), conventional commits, PR templates, code review checklists, and rebase vs merge decision framework.
keywords: [git, branch, branching strategy, feature branch, trunk-based, pull request, PR, merge request, code review, commit, conventional commits, merge, rebase, squash, cherry-pick, conflict, CODEOWNERS]
category: quality
related_commands:
  action_types: [audit, generate, fix]
  categories: [quality]
pain_points: [9, 11]
---

# Git Workflow, Branching & PR Review

> **Standards:** Format defined in [cco-standards.md](../cco-standards.md)  
> **Discovery:** See [cco-standards.md](../cco-standards.md#18-command-discovery-protocol)


---

---

## Domain
Git branching, PR workflow, commit quality, code review

## Purpose
Prevent merge conflicts, maintain clean history, ensure PR quality

## Techniques

**Branch**: <3 days, `feature/auth`, trunk-based, feature flags

**Commit**: `type(scope): subject` - **Title: max 50 chars** (ideal), max 72 (hard limit), imperative mood, no period. Body: wrap 72 chars. Types: feat/fix/docs/style/refactor/perf/test/build/ci/chore. Atomic: <200 lines

**PR**: <400 lines, template (summary/test/checklist), 1-2 reviewers, CI passes

**Review**: security (auth/validation/secrets), tests, performance (N+1), docs

**Merge**: feature=rebase, hotfix=merge, main=squash

## Patterns

### Commit Messages

**Format:** `type(scope): subject` (max 50 chars for subject)

```bash
# ✅ GOOD: Short, imperative, no period
feat(auth): add JWT refresh tokens
fix(api): handle null user in profile endpoint
docs: update installation steps
perf(db): optimize user query with index

# ❌ BAD: Too long, wrong mood, has period
feat(auth): added a new JWT refresh token implementation with expiry.
fix(api): fixed the issue where null values were causing errors in the user profile endpoint
```

**Body (optional):**
```
type(scope): short subject line (max 50 chars)

Detailed explanation wrapped at 72 characters. Explain WHAT
and WHY, not HOW. Separate from subject with blank line.

- Bullet points are okay
- Use imperative mood: "add" not "added"
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

---

## Code Review Deep Dive (Pain Point #11)

### Why Code Review Matters

**2025 Statistics:**
- Code review comment rates dropped **-27%** since AI coding assistants
- Shallow reviews increased (scan-only, no substantive feedback)
- AI-generated code often lacks context reviewers need
- Knowledge transfer during reviews significantly reduced

### Code Review Checklist (Comprehensive)

#### Security Review
```markdown
## Security Checklist
- [ ] **Authentication**: Auth required for protected endpoints?
- [ ] **Authorization**: RBAC/ABAC checks on resources?
- [ ] **Input Validation**: All user inputs validated/sanitized?
- [ ] **SQL Injection**: Parameterized queries used?
- [ ] **XSS**: Output encoding in place?
- [ ] **CSRF**: Token validation for state-changing requests?
- [ ] **Secrets**: No hardcoded credentials, API keys, tokens?
- [ ] **Dependencies**: Known CVEs checked? (npm audit, safety)
- [ ] **Logging**: No sensitive data (PII, passwords) in logs?
- [ ] **Error Handling**: No stack traces exposed to users?
```

#### Code Quality Review
```markdown
## Quality Checklist
- [ ] **Single Responsibility**: Each function/class does one thing?
- [ ] **Naming**: Clear, descriptive variable/function names?
- [ ] **Comments**: Complex logic explained? No redundant comments?
- [ ] **Error Handling**: Errors caught, logged, handled gracefully?
- [ ] **Edge Cases**: Null, empty, boundary conditions handled?
- [ ] **Duplication**: No copy-paste code (DRY)?
- [ ] **Complexity**: Functions <20 lines, cyclomatic complexity <10?
- [ ] **Types**: Type hints/annotations present (Python, TypeScript)?
- [ ] **Magic Numbers**: Named constants used?
```

#### Testing Review
```markdown
## Testing Checklist
- [ ] **Unit Tests**: New code has tests? Coverage maintained?
- [ ] **Test Quality**: Assertions meaningful? Not just "runs without error"?
- [ ] **Edge Cases**: Tests cover null, empty, error paths?
- [ ] **Mocking**: External dependencies properly mocked?
- [ ] **Integration**: API/DB integration tested?
- [ ] **Regression**: Existing tests pass? No removed tests?
```

#### Performance Review
```markdown
## Performance Checklist
- [ ] **N+1 Queries**: No loops with individual DB queries?
- [ ] **Indexes**: Queries use appropriate indexes?
- [ ] **Pagination**: Large datasets paginated?
- [ ] **Caching**: Appropriate cache usage?
- [ ] **Async**: Long operations non-blocking?
- [ ] **Memory**: No memory leaks (large objects, event listeners)?
- [ ] **Bundle Size**: Frontend bundle impact acceptable?
```

### Review Automation

#### CODEOWNERS File
```bash
# .github/CODEOWNERS

# Global owners (fallback)
* @tech-lead @senior-dev

# Security team reviews security-sensitive code
/src/auth/**         @security-team
/src/api/payments/** @security-team @payments-team
*.secrets.*          @security-team

# Frontend team
/src/components/**   @frontend-team
/src/styles/**       @frontend-team

# Backend team
/src/services/**     @backend-team
/src/models/**       @backend-team @dba-team

# DevOps reviews infrastructure
/infrastructure/**   @devops-team
Dockerfile           @devops-team
*.yaml               @devops-team

# Docs team reviews documentation
/docs/**             @docs-team
*.md                 @docs-team
```

#### Auto-Assign Reviewers
```yaml
# .github/auto-assign.yml (GitHub Action)
addReviewers: true
addAssignees: true

# Assign reviewers based on file patterns
reviewers:
  - team-slug: backend-team
    files:
      - '**/*.py'
      - 'src/services/**'
  - team-slug: frontend-team
    files:
      - '**/*.tsx'
      - 'src/components/**'

# Round-robin to distribute load
numberOfReviewers: 2
reviewGroups:
  backend:
    - dev1
    - dev2
    - dev3
  frontend:
    - dev4
    - dev5
```

#### Required Reviews (Branch Protection)
```yaml
# Branch protection rules (GitHub)
# Settings > Branches > Branch protection rules

required_pull_request_reviews:
  required_approving_review_count: 2
  dismiss_stale_reviews: true
  require_code_owner_reviews: true
  require_last_push_approval: true

required_status_checks:
  strict: true
  contexts:
    - "ci/tests"
    - "ci/lint"
    - "security/snyk"
```

### Review Metrics (DORA-aligned)

#### Key Metrics to Track

| Metric | Good | Warning | Critical |
|--------|------|---------|----------|
| **Time to First Review** | < 4 hours | 4-24 hours | > 24 hours |
| **Time to Merge** | < 24 hours | 24-72 hours | > 72 hours |
| **Comments per PR** | 3-10 | < 3 (shallow) | > 20 (contentious) |
| **Review Iterations** | 1-2 | 3-4 | > 5 |
| **PR Size** | < 200 lines | 200-400 | > 400 |
| **Reviewer Diversity** | 3+ reviewers/week | 1-2 | 1 (bottleneck) |

#### Calculating Review Quality Score

```python
def calculate_review_quality(pr_data: dict) -> float:
    """Score PR review quality (0-100)."""
    score = 100

    # Time to first review (target: < 4 hours)
    if pr_data['time_to_first_review_hours'] > 24:
        score -= 20
    elif pr_data['time_to_first_review_hours'] > 4:
        score -= 10

    # Comment depth (not just "LGTM")
    substantive_comments = [c for c in pr_data['comments']
                           if len(c['body']) > 50]
    if len(substantive_comments) < 2:
        score -= 15  # Shallow review

    # PR size penalty
    if pr_data['lines_changed'] > 400:
        score -= 20
    elif pr_data['lines_changed'] > 200:
        score -= 10

    # Review iterations (target: 1-2)
    if pr_data['iterations'] > 4:
        score -= 15

    return max(0, score)
```

### PR Templates

#### Standard PR Template
```markdown
<!-- .github/pull_request_template.md -->

## Summary
<!-- What does this PR do? Why? -->

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to break)
- [ ] Documentation update
- [ ] Refactoring (no functional changes)

## Testing
<!-- How was this tested? -->
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Screenshots (if applicable)
<!-- Add screenshots for UI changes -->

## Checklist
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review
- [ ] I have commented complex code
- [ ] I have updated documentation
- [ ] My changes generate no new warnings
- [ ] Tests pass locally
- [ ] Any dependent changes have been merged

## Related Issues
<!-- Link related issues: Fixes #123, Relates to #456 -->
```

#### Security-Focused PR Template
```markdown
<!-- For security-sensitive PRs -->

## Security Impact Assessment

### Authentication/Authorization
- [ ] This PR modifies authentication logic
- [ ] This PR modifies authorization/permissions
- [ ] This PR adds new API endpoints

### Data Handling
- [ ] This PR handles sensitive data (PII, credentials)
- [ ] This PR modifies encryption/hashing
- [ ] This PR changes data storage

### External Dependencies
- [ ] This PR adds new dependencies
- [ ] Dependencies have been checked for CVEs

### Security Review Required
- [ ] Security team review requested
- [ ] Threat model updated (if applicable)
```

### Effective Review Comments

#### Good Comment Examples
```markdown
# ✅ GOOD: Specific, actionable, explains why

"This query will cause N+1 issues with 100+ users.
Consider using `prefetch_related('orders')` here.
See: https://docs.djangoproject.com/en/4.0/ref/models/querysets/#prefetch-related"

"SQL injection risk: user input directly in query.
Use parameterized query: `cursor.execute('SELECT * FROM users WHERE id = %s', [user_id])`"

"Missing null check. If `user.profile` is None, line 45 will raise AttributeError.
Consider: `if user.profile and user.profile.avatar:`"
```

#### Bad Comment Examples
```markdown
# ❌ BAD: Vague, no context, not actionable

"This looks wrong"
"Fix this"
"LGTM" (without actually reviewing)
"Nit: spacing" (trivial, should be automated)
```

### Review Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| **Rubber Stamping** | Approve without reading | Require substantive comments |
| **Bikeshedding** | Debate trivial issues | Focus on substance, automate style |
| **Hero Reviewer** | One person reviews all | Round-robin assignment |
| **Review Fatigue** | Large PRs get shallow reviews | Enforce PR size limits |
| **Delayed Reviews** | PRs sit for days | Track time-to-review metric |
| **Personal Attacks** | "This is stupid" | Focus on code, not author |

### Reviewer Guidelines

```markdown
## Reviewer Responsibilities

1. **Respond within 4 hours** (business hours)
   - If busy, comment "Will review by [time]"

2. **Review thoroughly**
   - Security, logic, tests, performance
   - Not just syntax/style (automate that)

3. **Be constructive**
   - Explain WHY, not just WHAT
   - Suggest solutions, not just problems
   - Praise good code too

4. **Use conventional comments**
   - `nit:` - Minor, optional suggestion
   - `suggestion:` - Recommended improvement
   - `question:` - Need clarification
   - `issue:` - Must fix before merge
   - `praise:` - Great work!

5. **Don't block unnecessarily**
   - Approve with minor nits
   - Trust author to address feedback
```

## Checklist
- [ ] Branch <3 days, conventional commits
- [ ] PR <400 lines, tests pass
- [ ] Review: security/quality/perf
- [ ] Merge: rebase/squash, docs updated
- [ ] CODEOWNERS configured for auto-assignment
- [ ] Review metrics tracked (time-to-review, comments/PR)
- [ ] PR template enforced
- [ ] Reviewer guidelines documented

