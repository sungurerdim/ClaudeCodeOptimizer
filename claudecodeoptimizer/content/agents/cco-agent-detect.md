---
name: cco-agent-detect
description: Full project detection (technical + strategic)
tools: Glob, Read, Grep, Bash
safe: true
---

# Agent: Detect

Read-only project detection. Returns scoped detection result.

## Scope Parameter

Commands specify detection scope in prompt. Only run detection for requested scope.

| Scope | Includes | Use Case |
|-------|----------|----------|
| `tools` | format, lint, test commands only | cco-commit (fallback when no context) |
| `technical` | stack + tools + conventions + applicable | cco-config (permission allow lists) |
| `full` | technical + strategic (purpose, team, scale, data, type, rollback) | cco-context |

**Note:** Most commands read from CLAUDE.md (stored by cco-context), not from detect agent directly.

**Default:** If no scope specified, assume `full`.

**Example prompts:**
- `"Detect project tools (scope: tools)"` → only tools detection
- `"Full project detection (scope: full)"` → everything

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

## Output Format (by scope)

### scope: tools
```json
{
  "tools": {
    "format": "ruff format .",
    "lint": "ruff check .",
    "test": "pytest tests/"
  }
}
```

### scope: technical
```json
{
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
}
```

### scope: full
```json
{
  "technical": {
    "stack": { "languages": [], "frameworks": [], "databases": [], "infrastructure": [], "cicd": [], "testing": [] },
    "tools": { "format": null, "lint": null, "test": null },
    "conventions": { "testNaming": null, "importStyle": null },
    "applicable": []
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
2. **Scoped** - Only detect what's requested, skip the rest
3. **Fast** - Skip deep analysis, use file presence and configs
4. **Deterministic** - Same input → same output
