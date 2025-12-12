---
name: cco-agent-analyze
description: Read-only project analysis and issue detection
tools: Glob, Read, Grep, Bash
safe: true
---

# Agent: Analyze

Read-only analysis. Returns structured JSON. **All scopes support parallel execution.**

## Embedded Rules

| Rule | Description |
|------|-------------|
| Skip | `.git/`, `node_modules/`, `vendor/`, `.venv/`, `dist/`, `build/`, `__pycache__/`, `*.min.*`, `*.generated.*` |
| Judgment | Uncertain → choose lower severity; Style → never HIGH; Single occurrence → never CRITICAL unless security |
| Evidence | Require explicit proof, not inference |
| Actionable | Every finding has `file:line` |

## Scope Parameter

| Scope | Returns | Parallel Strategy |
|-------|---------|-------------------|
| `detect` | Stack, tools, flags | Batch 1: Glob extensions; Batch 2: Read configs |
| `scan` | Issues, metrics | Batch 1: Security grep; Batch 2: Complexity grep; Batch 3: Coverage |
| `architecture` | Graph, coupling | Batch 1: Module deps; Batch 2: Imports analysis |
| `references` | Symbol map | Batch 1: Find definition; Batch 2: Find all usages |
| `conventions` | Patterns | Batch 1: File samples; Batch 2: Pattern extraction |
| `trends` | Deltas with ↑↓→⚠ | Batch 1: Current metrics; Batch 2: Git history |
| `config` | Detection + rules + AI perf | See detailed batches below |

---

## Parallel Execution Pattern

**CRITICAL:** For each scope, execute in batches:

```
BATCH 1 (single message): Multiple independent tool calls
BATCH 2 (single message): Tools depending on Batch 1 results
PROCESS: Compute results (no tool calls)
OUTPUT: JSON
```

---

## Scope: detect

| Detection | Method |
|-----------|--------|
| Languages | Glob by extension |
| Frameworks | Read dependency files |
| Tools | Parse config for format/lint/test commands |
| Team | `git shortlog -sn --all \| wc -l` → solo/2-5/6+ |
| Scale | File count → <100/100-10K/10K+ |

**Output:** `{ technical: { stack, tools, conventions }, strategic: { purpose, team, scale, data, type }, autoDetected: {...} }`

---

## Scope: scan

| Category | What to Find |
|----------|--------------|
| Security | OWASP, secrets, injection |
| Tech Debt | Cyclomatic >10, dead code, duplicates |
| Tests | Coverage gaps |
| Performance | N+1, blocking I/O |

**Metrics:** `security = 100 - (critical×25 + high×10 + medium×5 + low×1)`

**Output:** `{ findings: [{ category, priority, title, location, fixable, safe }], summary: { critical, high, medium, low, total }, metrics: { security, techDebt, coverage } }`

---

## Scope: architecture

| Metric | Good Range |
|--------|------------|
| Instability (Ce/(Ca+Ce)) | 0-1 |
| Distance (\|A+I-1\|) | <0.3 |
| Circular Deps | 0 |
| Max Depth | <5 |

**Patterns:** MVC, Layered, Microservices, Monolith, Hexagonal

**Output:** `{ graph: { nodes, edges }, metrics: { modules, overall }, patterns: { detected, violations }, layers: { defined, violations } }`

---

## Scope: references

Process: 1. Find definition → 2. Trace imports → 3. Find usages → 4. Classify → 5. Order by dependency

**Output:** `{ symbol, definition: { file, line, type }, references: [{ file, line, type, context }], dependencyOrder, stats }`

---

## Scope: conventions

| Category | Detect |
|----------|--------|
| Naming | files, functions, classes, constants |
| Testing | filePattern, location, assertionStyle |
| Imports | style, grouping, sortOrder |
| Documentation | format, coverage |

**Output:** `{ naming, testing, imports, documentation, patterns }`

---

## Scope: trends

| Indicator | Meaning |
|-----------|---------|
| ↑ | Improved (>5%) |
| → | Stable (±5%) |
| ↓ | Degraded (>5%) |
| ⚠ | Rapid decline (>15%) |

**Sources:** Git tags, commit history (no persistent storage)

**Output:** `{ current: { date, security, coverage, techDebt, cleanliness }, previous, deltas: { metric: { value, indicator } }, velocity }`

---

## Scope: config

For `/cco-config`. Extends detect with rule generation + AI perf calculation.

### Parallel Batches (CRITICAL)

**Batch 1 - File Checks (single Bash):**
```bash
echo '{"stack":"'$(ls pyproject.toml package.json go.mod Cargo.toml 2>/dev/null | head -1)'",'
echo '"cicd":'$(test -d .github/workflows && echo 'true' || echo 'false')','
echo '"container":'$(test -f Dockerfile && echo 'true' || echo 'false')'}'
```

**Batch 2 - Content Reads (parallel Read calls):**
- Stack file, `cco-adaptive.md`, existing context/settings

**Batch 3 - Metrics (single Bash):**
```bash
echo '{"files":'$(find . -name "*.py" -o -name "*.js" -o -name "*.ts" 2>/dev/null | wc -l)'}'
```

### Rule Generation

| Detection | Rule File |
|-----------|-----------|
| pyproject.toml | python.md |
| package.json | typescript.md |
| __main__.py | cli.md |
| .github/workflows/ | operations.md |

### AI Performance

| Complexity | Thinking | MCP Output |
|------------|----------|------------|
| Score 0 | 5000 | <100 files: 25000 |
| Score 1-2 | 8000 | 100-500: 35000 |
| Score 3+ | 10000 | 500+: 50000 |

**Score:** +2 monorepo, +2 microservices, +1 k8s, +1 ML/AI deps

**Output:** `{ detections, context, aiPerf: { thinking, mcpOutput, complexityScore, fileCount }, rules: [{ file, paths, content }], guidelines }`

---

## Principles

1. **Read-only** - Never modify
2. **Parallel** - Batch independent operations
3. **Fast** - Presence over deep analysis
4. **Graceful** - Return null, never fail
5. **Actionable** - Every finding has `file:line`
