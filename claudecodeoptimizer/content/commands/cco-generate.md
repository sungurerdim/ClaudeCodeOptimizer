---
name: cco-generate
description: Convention-following automated generation
---

# /cco-generate

**Convention-following generation** - Read conventions from context → generate consistent components.

## Pre-Operation

**Follow Pre-Operation Safety from cco-standards Workflow section.**

## Project Context

**Follow Context Read from cco-standards Workflow section.**

From context apply:
- **Conventions** - Use testNaming, importStyle from Operational section
- **Type** - Adapt templates: CLI (argparse/click), API (endpoints), frontend (components)
- **Stack** - Use detected frameworks for idiomatic generation
- **Priority** - If Speed → minimal scaffolding; if Quality → comprehensive with edge cases
- **Maturity** - If Legacy → match existing patterns exactly; if Greenfield → use modern idioms

## Types

**Testing:**
- `--tests` - Unit/integration tests
- `--contract-tests` - API contract tests
- `--load-tests` - Performance tests

**Documentation:**
- `--openapi` - API specification
- `--docs` - Docstrings, README
- `--adr` - Architecture Decision Records
- `--runbook` - Operational runbooks

**Infrastructure:**
- `--cicd` - GitHub Actions / GitLab CI
- `--dockerfile` - Multi-stage Dockerfile
- `--pre-commit` - Pre-commit hooks

## Convention Enforcement

Use conventions from context (stored in Operational section):
- Test file naming (testNaming)
- Import style (importStyle)
- Existing tools and frameworks

Follow stored conventions, don't impose new ones.

## Generation Guidelines

### Tests (`--tests`)

Analyze existing test patterns first:
1. Discover test directory structure (`tests/`, `test/`, `__tests__/`, `*.test.*`)
2. Match naming convention (`test_*.py`, `*.test.ts`, `*_test.go`)
3. Use same assertion library (pytest, jest, testing, etc.)
4. Follow AAA pattern: Arrange → Act → Assert

Generate for:
- Public functions without tests
- Edge cases for existing tested functions
- Integration tests for API endpoints

### Documentation (`--openapi`, `--docs`)

**OpenAPI:** Extract from code:
- Route decorators/handlers → paths
- Request/response types → schemas
- Validation rules → constraints
- Auth middleware → security schemes

**Docstrings:** Match existing style:
- Google style, NumPy style, or JSDoc
- Include types if not using type annotations
- Document exceptions/errors

### Infrastructure (`--cicd`, `--dockerfile`)

**CI/CD:** Detect platform and create:
- `.github/workflows/ci.yml` for GitHub
- `.gitlab-ci.yml` for GitLab
- Include: lint → test → build stages

**Dockerfile:** Multi-stage build:
- Base image from stack detection
- Dev dependencies in build stage only
- Non-root user in final stage
- Health check if applicable

## Verification

After generation:
- created = planned
- generated tests pass
- no import errors

## Usage

```bash
/cco-generate --tests
/cco-generate --openapi
/cco-generate --cicd
```
