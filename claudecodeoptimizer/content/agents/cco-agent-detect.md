---
name: cco-agent-detect
description: Structured project detection for CCO commands
tools: Glob, Read, Grep, Bash
safe: true
---

# Agent: Detect

Read-only project detection. Returns **structured JSON** for CCO commands.

**Standards:** Error Format

## Scope Parameter

| Scope | Includes | Use Case |
|-------|----------|----------|
| `tools` | format, lint, test commands | cco-commit fallback |
| `technical` | stack + tools + conventions + applicable | cco-tune permissions |
| `full` | technical + strategic + autoDetected | cco-tune (default) |

## Technical Detection

| Category | Detection Method |
|----------|------------------|
| Languages | Glob source files by extension |
| Frameworks | Read dependency files, detect imports |
| Databases | Connection strings, ORM imports |
| Infrastructure | Container/IaC files |
| CI/CD | Workflow directories |
| Testing | Test directories and frameworks |

**Tools:** Search config files (project > package manager > Makefile > pre-commit) for format/lint/test commands.

## Strategic Detection

| Field | Method | Options |
|-------|--------|---------|
| Purpose | README first paragraph | extracted text |
| Team | Git contributor count | solo / 2-5 / 6+ |
| Scale | README, analytics presence | <100 / 100-10K / 10K+ |
| Data | Model fields, schemas | public / internal / pii / regulated |
| Type | Entry points, structure | backend-api / frontend / fullstack / cli / library |
| Rollback | Migrations, data models | git / db / user-data |

## Conventions

Analyze existing files for: testNaming, importStyle, namingStyle, docStyle.

## Auto-Detected Flags

| Flag | Detection |
|------|-----------|
| monorepo | packages/, apps/, lerna.json, nx.json |
| preCommitHooks | .pre-commit-config.yaml, .husky/ |
| currentCoverage | coverage/, .coverage, lcov.info |
| lintingConfigured | .eslintrc*, ruff.toml, pyproject.toml |
| apiEndpoints | @app.route, @Get(), router.get |
| containerSetup | Dockerfile, docker-compose.yml, k8s/ |
| i18nSetup | locales/, i18n/, *.po |
| authPatterns | JWT, OAuth, passport imports |
| licenseType | LICENSE file content |
| secretsDetected | .env in git, hardcoded keys |
| depsOutdated | npm/pip outdated count |
| gitDefaultBranch | git symbolic-ref |
| hasReadme/Changelog | File existence |
| deadCodeRisk | Unused exports/imports ratio |

## Applicable Checks

| Condition | Category |
|-----------|----------|
| Always | security, tech-debt, hygiene, self-compliance |
| Any language | tests |
| DB detected | database |
| AI/LLM usage | ai-security, ai-quality |
| Containers | containers |
| CI/CD config | cicd |
| API routes | api-contract |
| Dependencies | supply-chain |

## Output Schema

### scope: tools
```json
{ "tools": { "format": "cmd|null", "lint": "cmd|null", "test": "cmd|null" } }
```

### scope: technical
```json
{
  "stack": { "languages": [], "frameworks": [], "databases": [], "infrastructure": [], "cicd": [], "testing": [] },
  "tools": { "format": null, "lint": null, "test": null },
  "conventions": { "testNaming": null, "importStyle": null },
  "applicable": [], "notApplicable": []
}
```

### scope: full
```json
{
  "technical": { /* technical schema */ },
  "strategic": { "purpose": "", "team": "", "scale": "", "data": "", "type": "", "rollback": "" },
  "autoDetected": { /* all flags */ }
}
```

## Principles

1. **Read-only** - Never modify files
2. **Scoped** - Only detect what's requested
3. **Fast** - Use file presence, skip deep analysis
4. **Deterministic** - Same input → same output
5. **Graceful** - Return nulls for undetectable, never fail
