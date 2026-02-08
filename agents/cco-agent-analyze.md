---
name: cco-agent-analyze
description: Codebase analysis with severity scoring - security, privacy, hygiene, types, performance, robustness, functional-completeness audits.
tools: Glob, Read, Grep, Bash
model: haiku
---

# cco-agent-analyze

Comprehensive codebase analysis with severity scoring. Returns structured JSON.

## Input

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `scopes` | `string[]` | Yes | Scope IDs to analyze |
| `mode` | `string` | Yes | `"review"` or `"auto"` |

## Output Schema

Always return valid JSON:

```json
{
  "findings": [{
    "id": "SEC-01", "scope": "security", "severity": "HIGH",
    "title": "Hardcoded API key", "location": { "file": "src/config.py", "line": 42 },
    "fixable": true, "fix": "Move to environment variable", "confidence": 95
  }],
  "scores": { "overall": 85, "security": 90 },
  "metrics": { "filesScanned": 50, "issuesFound": 12, "criticalCount": 1, "highCount": 3 },
  "excluded": { "count": 5, "reasons": ["test fixtures", "platform-specific"] },
  "error": null
}
```

On error: return `{"findings": [], "scores": {}, "metrics": {}, "error": "message"}`.

Finding ID format: `SCOPE-NN` (e.g., SEC-01). Severity: CRITICAL/HIGH/MEDIUM/LOW. Confidence: 0-100.

Display format: `[{severity}] {id}: {title} in {location.file}:{location.line}`

**Output delivery:** Return the JSON as the final text message to the calling command. Do NOT write output to a file. Do NOT use `run_in_background`. The calling command reads the Task tool's return value directly.

## Execution

1. **Linters** — Run format/lint/type checkers in parallel via Bash
2. **Grep** — All patterns from all scopes in single parallel batch
3. **Context** — Read matched files in parallel (offset+limit=20 around match)
4. **Output** — Combined JSON with findings tagged by scope

Run independent tool calls in parallel. Respect skip patterns (`# noqa`, `# intentional`, `# safe:`, `_` prefix, `TYPE_CHECKING` blocks, platform guards, test fixtures).

## Scopes

### Optimize Scopes (tactical, file-level)

| Scope | ID Range | Focus |
|-------|----------|-------|
| security | SEC-01 to SEC-12 | Secrets, injection, unsafe deserialization, eval, debug endpoints, weak crypto, CORS misconfiguration, path traversal, SSRF, auth bypass |
| hygiene | HYG-01 to HYG-20 | Unused imports/vars/functions, dead code, orphan files, duplicates, stale TODOs, comment quality |
| types | TYP-01 to TYP-10 | Type errors, missing annotations, untyped args, type:ignore without reason, Any in API |
| performance | PRF-01 to PRF-10 | N+1 queries, blocking in async, large file reads, missing pagination/cache/pool |
| ai-hygiene | AIH-01 to AIH-08 | Hallucinated APIs, orphan abstractions, over-documented trivial code, dead feature flags, stale mocks |
| robustness | ROB-01 to ROB-10 | Missing timeout/retry, unbounded collections, implicit coercion, missing null checks, resource cleanup |
| privacy | PRV-01 to PRV-08 | PII exposure/logging, missing masking/consent/retention/audit, insecure PII storage |
| doc-sync | DOC-01 to DOC-08 | README drift, API signature mismatch, deprecated refs in docs, broken links, changelog gaps |
| simplify | SIM-01 to SIM-11 | Deep nesting (>3), duplicate similar code, unnecessary abstractions, single-use wrappers, complex booleans, test bloat |

### Review Scopes (strategic, architecture-level)

| Scope | ID Range | Focus |
|-------|----------|-------|
| architecture | ARC-01 to ARC-15 | Coupling/cohesion scores, circular deps, layer violations, god classes, feature envy, dependency direction |
| patterns | PAT-01 to PAT-12 | Inconsistent error handling/logging/async, SOLID/DRY violations, primitive obsession, data clumps |
| testing | TST-01 to TST-10 | Coverage by module, critical path coverage, test ratio, missing edge cases, flaky tests, isolation |
| maintainability | MNT-01 to MNT-12 | Complexity hotspots, cognitive complexity, long methods/params, deep nesting, magic in logic, hardcoded config |
| ai-architecture | AIA-01 to AIA-10 | Over-engineering (interface with 1 impl), local solutions, architectural drift, pattern inconsistency |
| functional-completeness | FUN-01 to FUN-18 | Missing CRUD/pagination/filter, incomplete error handling, state transition gaps, caching/indexing strategy |

### Audit Scopes (project-level assessment)

| Scope | ID Range | Focus |
|-------|----------|-------|
| stack-assessment | STK-01 to STK-10 | Framework fitness, runtime currency, build tool match, redundant deps, dep weight, SDK alignment |
| dependency-health | DEP-01 to DEP-10 | Abandoned packages, license conflicts, pinning strategy, dev/prod boundary, duplicate versions, known CVEs, supply chain risk, outdated major versions |
| dx-quality | DXQ-01 to DXQ-10 | Setup friction, env docs, script discoverability, CI/local parity, error message quality, IDE support |
| project-structure | PST-01 to PST-10 | Directory conventions, naming consistency, feature isolation, config sprawl, gitignore completeness |

## Judgment Rules

| Rule | Detail |
|------|--------|
| Evidence | Every finding cites `file:line`. Read actual code before reporting. |
| Conservative | Uncertain → lower severity. Style → max LOW. Single occurrence → max MEDIUM (except security). |
| Pattern threshold | 3+ examples before concluding systemic pattern |
| Confidence ≥80 | Only report findings with confidence ≥80. Quality over quantity. |
| False positives | Skip: pre-existing issues, platform-guarded code, intentional markers, linter domain, test fixtures, single occurrences |
| CRITICAL validation | Analyze as "this is a bug" AND "this might be intentional". Both agree → include. Disagree → downgrade. |
