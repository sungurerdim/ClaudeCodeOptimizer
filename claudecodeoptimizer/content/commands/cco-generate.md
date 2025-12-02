---
name: cco-generate
description: Convention-following automated generation
---

# /cco-generate

**Convention-following generation** - Read conventions from context → generate consistent components.

**Standards:** Pre-Operation Safety | Context Read | Verification | Error Format

## Context Application
- **Conventions** - Use testNaming, importStyle from Operational section
- **Type** - Adapt templates: CLI (argparse/click), API (endpoints), frontend (components)
- **Stack** - Use detected frameworks for idiomatic generation
- **Priority** - If Speed → minimal scaffolding; if Quality → comprehensive with edge cases
- **Maturity** - If Legacy → match existing patterns exactly; if Greenfield → use modern idioms

## Default Behavior

When called without flags, AskUserQuestion:

```
header: "Generate"
question: "What to generate?"
multiSelect: true
options:
  - All: "Generate all applicable types"
  - Tests: "Unit/integration tests for uncovered code"
  - Docs: "Docstrings, README, OpenAPI (if API)"
  - Infra: "CI/CD pipelines, Dockerfile, pre-commit"
```

Explicit flags (`--tests`, `--docs`, `--infra`) skip this question.

## Types

**Testing:** `--tests`
- Unit/integration tests (default)
- Contract tests (if API detected)
- Load tests (if --load specified)

**Documentation:** `--docs`
- Docstrings, README (default)
- OpenAPI spec (if API detected)
- ADR (if --adr specified)

**Infrastructure:** `--infra`
- CI/CD pipelines (default)
- Dockerfile (if --docker specified)
- Pre-commit hooks (if --hooks specified)

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
/cco-generate              # Interactive: ask what to generate
/cco-generate --tests      # Unit/integration tests (+ contract if API)
/cco-generate --docs       # Docstrings, README (+ OpenAPI if API)
/cco-generate --infra      # CI/CD pipelines
/cco-generate --all        # Everything applicable
```
