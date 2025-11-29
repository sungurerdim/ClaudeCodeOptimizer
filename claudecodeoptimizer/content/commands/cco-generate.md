---
name: cco-generate
description: Convention-following automated generation
---

# /cco-generate

**Convention-following generation** - Read conventions from context → generate consistent components.

## Pre-Operation Safety

If uncommitted changes exist, AskUserQuestion:
→ Commit first (cco-commit) / Stash / Continue anyway

## Project Context

**First:** Run `/cco-calibrate` to ensure context is loaded.

Read `CCO_CONTEXT_START` block from CLAUDE.md:
- **Conventions** - Use testNaming, importStyle from Operational section
- **Type** - Adapt templates: CLI (argparse/click), API (endpoints), frontend (components)
- **Stack** - Use detected frameworks for idiomatic generation

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
