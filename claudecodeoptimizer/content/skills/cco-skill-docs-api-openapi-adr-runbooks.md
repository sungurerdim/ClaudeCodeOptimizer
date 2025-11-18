---
name: cco-skill-docs-api-openapi-adr-runbooks
description: |
  Documentation, API specs (OpenAPI/Swagger), ADRs, runbooks, changelog.
  Triggers: docs, OpenAPI, ADR, runbook, changelog, docstring, API spec
  Files: docs/*, CHANGELOG.md, README.md, openapi.yaml, swagger.json
---

# Skill: Documentation - API, ADRs, Runbooks

## Purpose

**Solves**:
- **Undocumented APIs**: Auto-generate OpenAPI specs (60% of API issues from missing docs)
- **Lost Context**: ADRs preserve architecture decisions and reasoning
- **Slow Incident Response**: Runbooks reduce MTTR by 40%
- **Poor Code Docs**: Docstring standards reduce onboarding delays by 50%+

---

## Principles Included

Loads these P_ principles on-demand:

- **P_API_DOCUMENTATION_OPENAPI**: Auto-generate OpenAPI specs from code (REST APIs, GraphQL)
- **P_CODE_DOCUMENTATION_STANDARDS**: Docstrings, type hints, inline comments (functions, classes)
- **P_ADR_ARCHITECTURE_DECISIONS**: Preserve decision context, alternatives, consequences (tech choices)
- **P_CHANGELOG_MAINTENANCE**: Keep a Changelog format for release history (versioning, releases)
- **P_RUNBOOK_OPERATIONAL_DOCS**: Document symptoms, diagnosis, resolution (incident response)

Loaded only when skill activates.

---

## Auto-Activation

**Keywords**: documentation, docs, OpenAPI, ADR, runbook, changelog, docstring, API spec, Swagger
**Files**: `docs/*`, `CHANGELOG.md`, `README.md`, `openapi.yaml`, `swagger.json`

---

## Command Discovery Protocol

When this skill is active, find relevant commands by searching `~/.claude/commands/` metadata:

```yaml
# Search criteria for this skill's domain
action_types: [audit, fix, generate]
keywords: [documentation, openapi, swagger, adr, runbook, changelog, docstrings, readme, api docs]
category: docs
pain_points: [7]
```

**How Claude finds commands:**
1. Grep command files for `keywords:.*doc|openapi|adr` in frontmatter
2. Match `category: docs`
3. Present matching commands with their parameters

This ensures commands are always current even when renamed or updated.

---

## Examples

### Example 1: OpenAPI (FastAPI)
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="User API", version="1.0.0")

class User(BaseModel):
    id: int; email: str

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    """Retrieve user by ID."""
    return db.get_user(user_id)
# Docs: /docs (Swagger) or /redoc
```

### Example 2: ADR
```markdown
# ADR 003: PostgreSQL over MongoDB
**Status**: Accepted | **Date**: 2024-01-15
## Context: Need ACID transactions for payments
## Decision: Use PostgreSQL
## Consequences: +ACID, +SQL | -Vertical scaling (use replicas)
## Alternatives: MongoDB (no ACID), MySQL (worse JSON support)
```

### Example 3: Runbook
```markdown
# Database Failover | **P1** | 2024-01-15
## Symptoms: Connection timeout, health check fail
## Diagnosis: `pg_isready -h db-primary`
## Resolution:
1. Verify: `systemctl status postgresql`
2. Promote: `pg_ctl promote -D /data`
3. Update: `kubectl set env deployment/api DATABASE_URL=...`
## Escalation: L1→L2 DB team→L3 CTO (>2h)
```

### Example 4: Docstring
```python
def calculate_discount(price: Decimal, discount: float, coupon: str = None) -> Decimal:
    """Calculate final price after discount.
    Args: price (positive), discount (0-100), coupon (optional)
    Returns: Final price (2 decimals) | Raises: ValueError
    """
    if price < 0: raise ValueError(f"Invalid: {price}")
    return round(price * (1 - discount / 100), 2)
```
