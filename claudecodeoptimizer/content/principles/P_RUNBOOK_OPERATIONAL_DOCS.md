---
name: runbook-operational-docs
description: Create clear runbooks and operational documentation for reliable on-call operations
type: project
severity: high
keywords: ["documentation", "runbook", "operations", "procedures", "on-call"]
category: ["docs", "infrastructure"]
related_skills: []
---

# P_RUNBOOK_OPERATIONAL_DOCS: Runbook and Operational Documentation

**Severity**: High

3am pages without clear procedures cause delays, mistakes, escalation issues Knowledge silos create single points of failure Manual processes introduce errors under pressure **Core Questions:** What's.

---

## Rules

- *No rules extracted*

---

## Examples

### ✅ Good
```markdown
# Runbook: Production Deployment

## Prerequisites
- [ ] All tests passing in CI/CD
- [ ] Code review completed (2+ approvals)
- [ ] CHANGELOG.md updated
- [ ] On-call coverage confirmed (next 4 hours)
- [ ] Monitoring dashboards accessible

## Phase 1: Pre-Deployment (5 min)
```
**Why right**: ```

### ❌ Bad
```markdown
# ❌ BAD: Vague documentation
1. Deploy code
2. Check that it works
3. If problems, rollback

# Problems: No step-by-step, no commands, at 3am operator doesn't know what to do

# ❌ BAD: Knowledge silos
"Talk to Alex, he handles deployments"
# Single point of failure; Alex on vacation = nobody can deploy
```
**Why wrong**: ---
