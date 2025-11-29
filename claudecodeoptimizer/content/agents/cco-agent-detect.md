---
name: cco-agent-detect
description: Full project detection (technical + strategic)
tools: Glob, Read, Grep, Bash
safe: true
---

# Agent: Detect

Read-only project detection. Returns complete detection result for context.

## Purpose

Detect ALL project characteristics - both technical (stack, tools) and strategic (team, scale, data sensitivity).

## Technical Detection

| Category | Sources | Output |
|----------|---------|--------|
| Languages | Extensions, configs | `["python", "typescript"]` |
| Frameworks | Imports, deps | `["fastapi", "react"]` |
| Databases | Connection strings, ORMs | `["postgres", "redis"]` |
| Infrastructure | Docker, K8s, Terraform | `["docker", "k8s"]` |
| CI/CD | .github/, .gitlab-ci.yml | `["github-actions"]` |
| Testing | Test files, configs | `["pytest", "jest"]` |
| Tools | pyproject.toml, package.json | `{format: "ruff", lint: "eslint"}` |

## Strategic Detection

| Field | Detection Method | Output |
|-------|------------------|--------|
| Purpose | README.md first paragraph, package description | `"CLI tool for..."` |
| Team | `git shortlog -sn` contributor count | `"solo"` / `"2-5"` / `"6+"` |
| Scale | README mentions, user docs, analytics config | `"<100"` / `"100-10K"` / `"10K+"` |
| Data | Model fields (email, password, PII patterns) | `"public"` / `"internal"` / `"pii"` / `"regulated"` |
| Type | Entry points, folder structure | `"backend-api"` / `"frontend"` / `"cli"` / `"library"` |
| Rollback | migrations/ + user models analysis | `"git"` / `"db"` / `"user-data"` |

## Convention Detection

Extract existing patterns for generation consistency:
- Test naming: `test_*.py` vs `*.test.ts`
- Import style: absolute vs relative
- Directory structure: flat vs nested
- Naming: snake_case vs camelCase

## Output Format

```json
{
  "technical": {
    "stack": {
      "languages": [],
      "frameworks": [],
      "databases": [],
      "infrastructure": [],
      "cicd": [],
      "testing": []
    },
    "tools": {
      "format": null,
      "lint": null,
      "test": null
    },
    "conventions": {
      "testNaming": null,
      "importStyle": null
    },
    "applicable": ["security", "tech-debt", "tests"]
  },
  "strategic": {
    "purpose": null,
    "team": null,
    "scale": null,
    "data": null,
    "type": null,
    "rollback": null
  }
}
```

## Principles

1. **Read-only** - Never modify files
2. **Fast** - Skip deep analysis, use file presence and configs
3. **Deterministic** - Same input → same output
4. **Complete** - Return all fields, use null for undetectable
