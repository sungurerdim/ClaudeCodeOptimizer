---
name: cco-generate
description: Convention-following automated generation
requires: detection
---

# /cco-generate

**Convention-following generation** - Detect conventions → generate consistent components.

## Agent Delegation

| Phase | Agent | Purpose |
|-------|-------|---------|
| Detect | `cco-agent-detect` | Identify conventions, patterns |
| Generate | `cco-agent-action` | Create files following conventions |

### MANDATORY Agent Rules

1. **NEVER use direct Edit/Write tools** - delegate to agents
2. **ALWAYS use agents as first choice**, not fallback after errors
3. Detect phase → `cco-agent-detect`
4. Generate phase → `cco-agent-action`

### Error Recovery

On "File unexpectedly modified" or tool errors:
1. Do NOT retry with direct tools
2. Immediately delegate to `cco-agent-action`
3. Agent reads fresh and creates files
4. Report agent results to user

## Pre-Operation Safety

If uncommitted changes exist, AskUserQuestion:
→ Commit first (cco-commit) / Stash / Continue anyway

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

## Convention Detection

Before generating, detect existing patterns:
- Test file naming (test_*.py vs *_test.py)
- Import style, directory structure
- Existing framework preferences

Follow detected conventions, don't impose new ones.

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
