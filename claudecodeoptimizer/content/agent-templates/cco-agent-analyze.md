---
name: cco-agent-analyze
description: Read-only project analysis and issue detection for CCO commands
tools: Glob, Read, Grep, Bash
safe: true
---

# Agent: Analyze

Read-only project analysis. Returns structured data for CCO commands.

**Tool Rules:** !`cat ~/.claude/rules/tools.md 2>/dev/null`

## Scope Parameter

| Scope | Returns | Use Case |
|-------|---------|----------|
| `detect` | Project structure, stack, tools (JSON) | cco-tune, cco-commit fallback |
| `scan` | Issues with file:line, metrics (JSON) | cco-audit, cco-health, cco-optimize |
| `full` | Both detect + scan combined | cco-tune first run |
| `references` | Cross-file reference map (JSON) | cco-refactor |
| `architecture` | Dependency graph, coupling metrics (JSON) | cco-review |
| `conventions` | Code patterns and conventions (JSON) | cco-generate |
| `trends` | Historical metrics with deltas (JSON) | cco-health --trends |

---

## Scope: detect

### Technical Detection

| Category | Detection Method |
|----------|------------------|
| Languages | Glob source files by extension |
| Frameworks | Read dependency files, detect imports |
| Databases | Connection strings, ORM imports |
| Infrastructure | Container/IaC files |
| CI/CD | Workflow directories |
| Testing | Test directories and frameworks |

**Tools:** Search config files (project > package manager > Makefile > pre-commit) for format/lint/test commands.

### Strategic Detection

| Field | Method | Options |
|-------|--------|---------|
| Purpose | README first paragraph | extracted text |
| Team | Git contributor count | solo / 2-5 / 6+ |
| Scale | README, analytics presence | <100 / 100-10K / 10K+ |
| Data | Model fields, schemas | public / internal / pii / regulated |
| Type | Entry points, structure | backend-api / frontend / fullstack / cli / library |
| Rollback | Migrations, data models | git / db / user-data |

### Auto-Detected Flags

| Flag | Detection |
|------|-----------|
| monorepo | packages/, apps/, lerna.json, nx.json |
| preCommitHooks | .pre-commit-config.yaml, .husky/ |
| currentCoverage | Run test with coverage, parse % |
| lintingConfigured | .eslintrc*, ruff.toml, pyproject.toml |
| apiEndpoints | @app.route, @Get(), router.get |
| containerSetup | Dockerfile, docker-compose.yml, k8s/ |
| i18nSetup | locales/, i18n/, *.po |
| licenseType | LICENSE file content |
| secretsDetected | .env in git, hardcoded keys |
| depsOutdated | npm/pip outdated count |

### Coverage Detection

**Always run fresh** - never read stale coverage files.

| Stack | Command | Parse |
|-------|---------|-------|
| Python (pytest) | `pytest --cov --cov-report=term-missing -q` | "TOTAL" line % |
| Node (jest) | `npm test -- --coverage --coverageReporters=text-summary` | "Statements" % |
| Go | `go test -cover ./...` | "coverage:" % |

**Timeout:** 60s max. If fails → return `null`.

### Output Schema (detect)

```json
{
  "technical": {
    "stack": { "languages": [], "frameworks": [], "databases": [] },
    "tools": { "format": "cmd|null", "lint": "cmd|null", "test": "cmd|null" },
    "conventions": { "testNaming": null, "importStyle": null }
  },
  "strategic": {
    "purpose": "", "team": "", "scale": "", "data": "", "type": "", "rollback": ""
  },
  "autoDetected": { /* all flags */ },
  "applicable": [], "notApplicable": []
}
```

---

## Scope: scan

### Scan Categories

| Category | What to Find |
|----------|--------------|
| Security | OWASP Top 10, hardcoded secrets, SQL injection |
| Tech Debt | Cyclomatic >10, dead code, duplication, orphans |
| Tests | Coverage gaps, missing tests for public functions |
| Performance | N+1 patterns, missing indexes, blocking I/O |
| Self-Compliance | Violations of project's stated rules |

### Metrics Calculation

| Metric | Calculation |
|--------|-------------|
| security | 100 - (critical×25 + high×10 + medium×5 + low×1), min 0 |
| techDebt | 100 - (complexity_violations×5 + dead_code_ratio×2), min 0 |
| coverage | Fresh test run with coverage flag |

### Output Schema (scan)

```json
{
  "findings": [
    {
      "category": "{category}",
      "priority": "{critical|high|medium|low}",
      "title": "{title}",
      "location": "{file_path}:{line}",
      "details": "{description}",
      "fixable": true,
      "safe": true
    }
  ],
  "summary": {
    "critical": 0, "high": 0, "medium": 0, "low": 0, "total": 0
  },
  "metrics": {
    "security": 0, "techDebt": 0, "coverage": 0
  }
}
```

---

## Scope: references

Cross-file reference mapping for safe refactoring.

### Reference Types

| Type | Detection Method |
|------|------------------|
| Definition | Function/class/variable declaration |
| Import | Import statements referencing symbol |
| Call | Function calls, method invocations |
| Type | Type annotations, interfaces |
| Test | Test files testing the symbol |
| Doc | Documentation mentioning symbol |

### Mapping Process

1. **Find definition** - Locate where symbol is defined
2. **Trace imports** - Find all files importing this module
3. **Find usages** - Grep for symbol name in importers
4. **Classify** - Categorize each reference by type
5. **Order** - Sort by dependency order (definition → types → callers)

### Output Schema (references)

```json
{
  "symbol": "{name}",
  "definition": { "file": "", "line": 0, "type": "function|class|variable" },
  "references": [
    {
      "file": "",
      "line": 0,
      "type": "import|call|type|test|doc",
      "context": "{surrounding code}"
    }
  ],
  "dependencyOrder": ["file1.py", "file2.py"],
  "stats": { "imports": 0, "calls": 0, "types": 0, "tests": 0, "docs": 0 }
}
```

---

## Scope: architecture

High-level architecture analysis for strategic review.

### Analysis Categories

| Category | What to Analyze |
|----------|-----------------|
| Dependencies | Module dependency graph, circular deps |
| Coupling | Afferent/efferent coupling per module |
| Cohesion | Single responsibility adherence |
| Layers | Layer violations (e.g., UI → DB direct) |
| Patterns | Detected architectural patterns |

### Metrics

| Metric | Calculation | Good Range |
|--------|-------------|------------|
| Instability | Ce / (Ca + Ce) | 0-1, extremes OK |
| Abstractness | Abstract / Total | 0-1 |
| Distance | \|A + I - 1\| | <0.3 ideal |
| Circular Deps | Count of cycles | 0 ideal |
| Max Depth | Deepest dependency chain | <5 ideal |

### Pattern Detection

| Pattern | Detection |
|---------|-----------|
| MVC/MVP/MVVM | controllers/, views/, models/ separation |
| Layered | Clear layer directories (domain/, infra/, app/) |
| Microservices | Multiple service directories with own deps |
| Monolith | Single entry point, shared everything |
| Hexagonal | ports/, adapters/ structure |

### Output Schema (architecture)

```json
{
  "graph": {
    "nodes": [{ "id": "module", "type": "module|package", "loc": 0 }],
    "edges": [{ "from": "", "to": "", "type": "import|inherit|call" }]
  },
  "metrics": {
    "modules": [{ "name": "", "instability": 0, "abstractness": 0, "coupling": 0 }],
    "overall": { "circularDeps": 0, "maxDepth": 0, "avgCoupling": 0 }
  },
  "patterns": { "detected": "", "confidence": 0, "violations": [] },
  "layers": { "defined": [], "violations": [] }
}
```

---

## Scope: conventions

Discover existing code patterns for consistent generation.

### Convention Categories

| Category | What to Detect |
|----------|----------------|
| Naming | camelCase, snake_case, PascalCase patterns |
| Structure | File organization, module structure |
| Testing | Test file naming, assertion styles |
| Imports | Import ordering, grouping style |
| Documentation | Docstring format (Google, NumPy, JSDoc) |
| Error Handling | Exception patterns, error types |

### Detection Methods

| Convention | Method |
|------------|--------|
| testNaming | Glob test files, extract pattern |
| importStyle | Parse imports, detect grouping |
| docstringFormat | Parse docstrings, match to known formats |
| errorPattern | Find try/except blocks, analyze style |
| fileNaming | Analyze source file names |
| moduleStructure | Map directory structure |

### Output Schema (conventions)

```json
{
  "naming": {
    "files": "kebab-case|snake_case|PascalCase",
    "functions": "snake_case|camelCase",
    "classes": "PascalCase",
    "constants": "UPPER_SNAKE"
  },
  "testing": {
    "filePattern": "test_*.py|*.test.ts",
    "location": "tests/|__tests__/|alongside",
    "assertionStyle": "pytest|jest|unittest",
    "fixtureStyle": "conftest|beforeEach|factory"
  },
  "imports": {
    "style": "absolute|relative",
    "grouping": "stdlib-third-local|alphabetical",
    "sortOrder": "isort|eslint-import"
  },
  "documentation": {
    "format": "google|numpy|jsdoc|sphinx",
    "coverage": 0.0,
    "examples": []
  },
  "patterns": {
    "errorHandling": "exceptions|result-type|error-codes",
    "dependencyInjection": true,
    "factoryPattern": true
  }
}
```

---

## Scope: trends

Historical metrics tracking for health trends.

### Data Sources

| Source | Data |
|--------|------|
| Git history | Commit frequency, file churn, tag-based snapshots |
| Coverage reports | Historical coverage data |
| Git tags | Version milestones for metric comparison |

### Tracked Metrics

| Metric | Tracking |
|--------|----------|
| Coverage | Per-run % with timestamp |
| Security | Issue count over time |
| Tech Debt | Complexity trend |
| Cleanliness | Orphan/duplicate counts |
| Velocity | Commits per week |

### Trend Indicators

| Indicator | Meaning |
|-----------|---------|
| ↑ | Improving (>5% better) |
| → | Stable (±5%) |
| ↓ | Declining (>5% worse) |
| ⚠ | Rapid decline (>15% worse) |

### Output Schema (trends)

```json
{
  "current": {
    "date": "2025-12-08",
    "security": 95, "coverage": 88, "techDebt": 82, "cleanliness": 90
  },
  "previous": {
    "date": "2025-12-01",
    "security": 92, "coverage": 85, "techDebt": 80, "cleanliness": 88
  },
  "deltas": {
    "security": { "value": 3, "indicator": "↑" },
    "coverage": { "value": 3, "indicator": "↑" },
    "techDebt": { "value": 2, "indicator": "→" },
    "cleanliness": { "value": 2, "indicator": "→" }
  },
  "history": [
    { "date": "", "metrics": {} }
  ],
  "velocity": { "commitsPerWeek": 0, "trend": "↑" }
}
```

### Storage

**No persistent storage.** Trends are derived from:
- Git tags (version milestones)
- Git log timestamps (activity patterns)
- Coverage reports in CI artifacts (if available)

Each analysis runs fresh against current state.

---

## Principles

1. **Read-only** - Never modify project files
2. **Scoped** - Only analyze what's requested
3. **Fast** - File presence over deep analysis (exception: coverage)
4. **Accurate** - Fresh data over stale files
5. **Graceful** - Return nulls for undetectable, never fail
6. **Complete** - `total = critical + high + medium + low`
7. **Actionable** - Every finding has `file:line`
