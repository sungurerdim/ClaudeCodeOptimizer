---
name: cco-generate
description: Create missing project components
categories:
  testing: [tests, contract-tests, load-tests, chaos-tests]
  docs: [openapi, docs, adr, runbook, review-checklist]
  infrastructure: [cicd, dockerfile, pre-commit, requirements]
  database: [migration, indexes]
  observability: [monitoring, logging, slo]
---

# /cco-generate

**Create missing tests, docs, configs**

---

## Flow: Confirm → Discover → Create → Done

### Confirm
Check for context from other commands. If none, discover missing components.

### Discover
1. Detect what exists (tests/, openapi.yaml, Dockerfile, etc.)
2. Identify gaps (untested functions, missing docs)
3. Report: "{X} files need tests, {Y} endpoints undocumented"

### Create
1. Generate following project conventions
2. Use existing patterns as reference
3. Track progress with TodoWrite

### Done
1. Report created files
2. Show how to use (test commands, etc.)
3. Suggest: `/cco-commit`

---

## Generation Types

| Type | Creates |
|------|---------|
| tests | Unit tests, integration tests, fixtures |
| contract-tests | Pact consumer/provider tests |
| load-tests | Locust/k6 load tests |
| chaos-tests | Failure injection tests |
| openapi | OpenAPI 3.0 spec |
| docs | Docstrings, README sections |
| adr | Architecture Decision Records |
| runbook | Operational runbooks |
| review-checklist | PR review checklist |
| cicd | GitHub Actions / GitLab CI |
| dockerfile | Multi-stage Dockerfile |
| pre-commit | Pre-commit hooks config |
| migration | Database migrations |
| indexes | Index creation scripts |
| monitoring | Prometheus metrics |
| logging | Structured logging config |
| slo | SLO definitions |

---

## Output Format

```markdown
# Generated Components

**Created:** {count} files

## Files Created
✓ tests/test_auth.py (15 tests)
✓ openapi.yaml (12 endpoints)

## Usage
Run tests: pytest tests/
View API docs: swagger-ui openapi.yaml

## Next Steps
→ Review: git diff
→ Run tests: {test_command}
→ Commit: /cco-commit
```

---

## Context Passing

Receive from `/cco-fix`:
```markdown
CONTEXT FOR /cco-generate:
Fixed {count} files. Need tests for: {file_list}
```

---

## Usage

```bash
/cco-generate                 # Interactive
/cco-generate --tests         # Generate tests
/cco-generate --openapi       # API documentation
/cco-generate --cicd          # CI/CD pipeline
/cco-generate --tests --docs  # Multiple types
/cco-generate --all           # Everything missing
/cco-generate --tests "auth"  # With focus context
```
