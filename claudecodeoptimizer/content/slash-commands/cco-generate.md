---
name: cco-generate
description: Convention-following automated generation
---

# /cco-generate

**Convention-following generation** - Read conventions → generate consistent components.

**Standards:** Command Flow | Approval Flow | Output Formatting

## Context Application

| Field | Effect |
|-------|--------|
| Conventions | Use testNaming, importStyle from Operational section |
| Type | CLI: argparse/click; API: endpoints + OpenAPI; Frontend: components + stories |
| Stack | Use detected frameworks for idiomatic generation |
| Priority | Speed → minimal scaffolding; Quality → comprehensive with edge cases |
| Maturity | Legacy → match existing patterns exactly; Greenfield → modern idioms |
| Scale | 10K+ → add monitoring, health checks, metrics; <100 → minimal infra |
| Data | PII → encryption helpers, audit logging; Regulated → compliance boilerplate |

## Flow

Per Command Flow standard.

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

**Sub-category selection (only when single flag used):**
- `--tests` → ask (multiSelect): All | Unit/Integration | Contract | Load
- `--docs` → ask (multiSelect): All | Docstrings | OpenAPI | ADR
- `--infra` → ask (multiSelect): All | CI/CD | Docker | Hooks

Note: `--all` or interactive "All" selection includes all sub-categories automatically.

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

## Output

**Standards:** Output Formatting

Tables:
1. **Generation Plan** - Type | Target | Convention | Status
2. **Files Created** - File | Lines | Description
3. **Verification** - Inline: created = planned, tests pass, no import errors

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
