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

---

## Documentation Templates

Use these templates when generating documentation:

### README Template

```markdown
# {PROJECT_NAME}

{One-line description of what this project does}

[![CI](https://github.com/{owner}/{repo}/actions/workflows/ci.yml/badge.svg)](https://github.com/{owner}/{repo}/actions)
[![Coverage](https://codecov.io/gh/{owner}/{repo}/branch/main/graph/badge.svg)](https://codecov.io/gh/{owner}/{repo})

## Quick Start

\`\`\`bash
git clone https://github.com/{owner}/{repo}.git
cd {repo}
pip install -e .
pytest
\`\`\`

## Features

- **Feature 1**: {Brief description}
- **Feature 2**: {Brief description}
- **Feature 3**: {Brief description}

## Installation

\`\`\`bash
pip install {project-name}
\`\`\`

## Usage

\`\`\`python
from {project} import main

result = main.run(param1="value")
print(result)
\`\`\`

## API Reference

See [API Documentation](docs/api.md) or run the app and visit `/docs`

## Development

\`\`\`bash
# Install dev dependencies
pip install -e .[dev]

# Run tests
pytest

# Run linting
ruff check .
\`\`\`

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT License - see [LICENSE](LICENSE)
```

### ADR Template

```markdown
# ADR {NUMBER}: {TITLE}

**Status**: Proposed | Accepted | Deprecated | Superseded by ADR-{N}
**Date**: {YYYY-MM-DD}
**Deciders**: {list of people involved}

## Context

{What is the issue that we're seeing that is motivating this decision or change?}

## Decision

{What is the change that we're proposing and/or doing?}

## Consequences

### Positive
- {Benefit 1}
- {Benefit 2}

### Negative
- {Drawback 1}
- {Drawback 2}

### Neutral
- {Trade-off 1}

## Alternatives Considered

### Option A: {Name}
{Description}
- Pros: {list}
- Cons: {list}

### Option B: {Name}
{Description}
- Pros: {list}
- Cons: {list}

## References

- {Link to relevant documentation}
- {Link to related ADRs}
```

### Runbook Template

```markdown
# {SERVICE_NAME} Runbook

**Priority**: P1 (Critical) | P2 (High) | P3 (Medium)
**Owner**: {team-name}
**Last Updated**: {YYYY-MM-DD}
**Review Cycle**: Quarterly

## Overview

{Brief description of the service and its importance}

## Symptoms

- [ ] {Symptom 1 - e.g., "High error rate on /api/users"}
- [ ] {Symptom 2 - e.g., "Response time > 2s"}
- [ ] {Symptom 3 - e.g., "Health check failing"}

## Diagnosis

### Quick Health Check
\`\`\`bash
curl -s http://localhost:8000/health | jq .
kubectl get pods -l app={service} -o wide
\`\`\`

### Log Analysis
\`\`\`bash
kubectl logs -l app={service} --tail=100 | grep ERROR
\`\`\`

### Metrics Check
- Grafana Dashboard: {link}
- Key metrics to check: {list}

## Resolution

### Step 1: {Action}
\`\`\`bash
{command}
\`\`\`
Expected: {what should happen}

### Step 2: {Action}
\`\`\`bash
{command}
\`\`\`
Expected: {what should happen}

### Step 3: Verify
\`\`\`bash
curl -s http://localhost:8000/health
\`\`\`
Expected: `{"status": "healthy"}`

## Escalation Path

| Level | Team | Contact | Timeout |
|-------|------|---------|---------|
| L1 | On-call | PagerDuty | 15 min |
| L2 | {Team} | #{slack-channel} | 30 min |
| L3 | Engineering Lead | @{name} | 2 hours |

## Post-Incident

- [ ] Update this runbook with lessons learned
- [ ] Create incident report
- [ ] Schedule post-mortem if P1/P2
```

### Docstring Template (Python)

```python
def function_name(param1: str, param2: int, param3: Optional[bool] = None) -> dict:
    """
    Brief description of what this function does.

    Longer description if needed, explaining the purpose,
    algorithm, or any important details.

    Args:
        param1: Description of param1
        param2: Description of param2
        param3: Description of param3. Defaults to None.

    Returns:
        Description of return value with example:
        {"key": "value", "count": 42}

    Raises:
        ValueError: When param1 is empty
        TypeError: When param2 is not positive

    Examples:
        >>> function_name("test", 5)
        {"key": "test", "count": 5}

        >>> function_name("", 5)
        Traceback (most recent call last):
            ...
        ValueError: param1 cannot be empty
    """
    pass
```
