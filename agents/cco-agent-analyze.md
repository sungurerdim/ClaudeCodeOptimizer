---
name: cco-agent-analyze
description: "Sub-agent: codebase analysis with severity scoring — security, privacy, hygiene, types, performance, robustness, functional-completeness. Used by /cco-optimize, /cco-align, /cco-blueprint and autonomously for code audits."
tools: Glob, Read, Grep, Bash
model: haiku
---

# cco-agent-analyze

Comprehensive codebase analysis with severity scoring. Returns structured JSON.

## Input

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `scopes` | `string[]` | Yes | Scope IDs to analyze |
| `mode` | `string` | Yes | `"review"`, `"auto"`, or `"audit"` |
| `context` | `object` | No | Blueprint profile context: projectType, stack, qualityTarget, dataSensitivity, constraints. When provided, use for stack-specific pattern detection and severity calibration. When absent, detect from codebase. |

## Mode Behavior

| Mode | Primary caller | Also used by | Mindset | Scope |
|------|---------------|-------------|---------|-------|
| `auto` | cco-optimize | cco-blueprint (Track A, D) | Tactical. Find fixable issues in individual files. Prefer small, safe, auto-applicable fixes. Flag only what can be acted on now. | Optimize scopes only |
| `review` | cco-align | cco-blueprint (Track B, C) | Strategic. Evaluate patterns across the codebase. Flag structural issues even if not auto-fixable. Question consistency, not just correctness. | Review scopes only |
| `audit` | cco-blueprint (Track E) | — | Assessment. Score and measure. Report state without suggesting fixes. Focus on metrics (coupling, cohesion, complexity, coverage). | Audit scopes only |

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

**Zero-findings normalization:** If a scope has no findings, return score in `scores`, `issuesFound: 0` in `metrics`, and empty `findings: []`. Never return null — always use empty arrays/objects.

Finding ID format: `SCOPE-NN` (e.g., SEC-01). Severity: CRITICAL/HIGH/MEDIUM/LOW. Confidence: 0-100.

Display format: `[{severity}] {id}: {title} in {location.file}:{location.line}`

**Output delivery:** Return the JSON as the final text message to the calling command. Do NOT write output to a file. Do NOT use `run_in_background`. The calling command reads the Task tool's return value directly.

### Score Calculation

Scores are calculated per scope using this formula:

```
base_score = 100
penalty_per_CRITICAL = -25
penalty_per_HIGH = -10
penalty_per_MEDIUM = -3
penalty_per_LOW = -1

scope_score = max(0, base_score + sum(penalties))
```

Cap rules:
- Any CRITICAL finding → scope score max 40
- 3+ HIGH findings → scope score max 60
- Score never goes below 0

For review/audit mode scopes without fixable findings (architecture, patterns, etc.), score reflects structural health:
- 90-100: No significant issues, patterns are consistent
- 70-89: Minor inconsistencies, 1-2 structural concerns
- 50-69: Notable issues, multiple inconsistencies
- 30-49: Significant structural problems
- 0-29: Fundamental architectural issues

These ranges are guidelines, not formulas. Use judgment within the range based on finding severity and count.

**Overall score per agent call:** Weighted average of all scope scores in that call, using equal weights per scope within the call. The skill (not the agent) applies project-type dimension weights during consolidation.

## Execution

**Scope efficiency:** Only execute checks for scopes listed in input. Do not scan for or evaluate patterns belonging to other scopes. This reduces analysis time and prevents off-scope findings.

**Early termination:** If initial Glob returns <5 source files, flag as micro-project. Skip architecture, patterns, cross-cutting scopes entirely (insufficient codebase for meaningful analysis). Return scores based on available scopes only.

**Context-aware filtering:** When `context.projectType` is provided, auto-skip irrelevant checks and emphasize relevant ones:

Per CCO Rules: Project Types — use standardized type IDs.

UF = user-facing-defaults.

| Type ID | Skip | Emphasize |
|---------|------|-----------|
| `cli` | PRD: container/health/scaling. FUN: pagination/CRUD/cache/UI. ARC: layers. PAT: DI. UF: all | SEC: arg injection, path traversal. ROB: signals, exit. DXQ: help/errors |
| `library` | PRD: container/health/shutdown/scaling. FUN: CRUD/pagination/UI. UF: all | SEC: public API input. TYP: public API types. PAT: SOLID. DOC: API docs |
| `api` | FUN: UI. UF: all | SEC+PRD+PRF+ROB: all relevant. PRF: N+1, pooling, pagination |
| `web` | PRD: container (unless SSR), secrets, scaling. PRF: N+1, pooling | UF: i18n/a11y/responsive. SEC: XSS/CORS. PRF: bundle, lazy load |
| `mobile` | PRD: container/deploy/scaling. PRF: N+1, pooling | UF: i18n/a11y/responsive. SEC: storage, cert pinning. PRF: memory, battery. ROB: offline |
| `desktop` | PRD: container, scaling. PRF: pooling | SEC: file access, IPC. ROB: crash recovery, auto-update. UF: i18n/a11y |
| `monorepo` | Per-package filtering by sub-type | ARC: cross-package coupling. PAT: consistency. PST: conventions |
| `iac` | PRD: API. FUN: UI/CRUD. TST: unit thresholds. UF: all | SEC: secrets, least privilege. ROB: idempotency, rollback. DXQ: env docs |
| `devtool` | PRD: container. FUN: UI. UF: all | DXQ+DOC: all. PAT: plugin patterns. SEC: supply chain |
| `data` | FUN: UI/CRUD. UF: all. PAT: DI/component | SEC: data access, PII. PRF: batch, memory. ROB: retry, validation |
| `ml` | FUN: UI/CRUD. UF: all. ARC: layers. PRD: web checks | SEC: input, poisoning. PRF: latency, GPU. ROB: versioning, fallback |
| `embedded` | PRD: container/scaling. FUN: UI/CRUD. UF: all. ARC: microservices | SEC: signing, overflow. PRF: footprint, realtime. ROB: watchdog, failsafe |
| `game` | PRD: all. FUN: CRUD/pagination. ARC: layers. UF: partial | PRF: framerate, memory, assets. SEC: anti-cheat. ROB: save, crash |
| `extension` | PRD: container/scaling. FUN: CRUD. UF: context-dependent | SEC: permissions, CSP. PAT: lifecycle, messaging. DXQ: manifest |

When context is absent, apply all checks (no filtering).
When `context.qualityTarget` is "Prototype", apply only security + hygiene scopes regardless of type.

**Steps 1-2 are independent — run in parallel.**

1. **Linters** — If project has configured linters (detected from config files like .eslintrc, biome.json, pyproject.toml, Makefile), run them via Bash. Skip if no tooling detected.
2. **Grep** — All patterns from all scopes in single parallel batch
3. **Context** — Read matched files in parallel (offset+limit=50 around match). MANDATORY: never report a finding without completing this step. If context reveals false positive → discard. For findings about repository hygiene (committed binaries, coverage files, secrets in repo): batch verify via `git ls-files {file1} {file2} ...` in a single Bash call — files not in output are untracked. If untracked or .gitignored → discard finding.
4. **Output** — Combined JSON with findings tagged by scope. **Cross-scope dedup:** Before output, check for findings at same file:line across scopes. Merge duplicates: keep highest severity, combine scope tags, use first ID.

Run independent tool calls in parallel. Per CCO Rules: Skip Patterns.

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
| patterns | PAT-01 to PAT-15 | Inconsistent error handling/logging/async, SOLID/DRY violations, primitive obsession, data clumps, framework-specific anti-patterns (DI bypass, manual validation vs framework validators, sync-in-async, non-idiomatic middleware/decorator usage — detected from stack in blueprint profile or codebase) |
| testing | TST-01 to TST-10 | Coverage by module vs threshold (from blueprint or 80% default), critical path test existence (auth, payment, data flow, error paths), test-to-code ratio, missing negative/boundary tests, test isolation issues (shared state, execution order dependency), mock vs real dependency balance, flaky test indicators (sleep, time-dependent, network calls) |
| maintainability | MNT-01 to MNT-12 | Cyclomatic complexity >15, cognitive complexity >20, methods >50 lines, >4 parameters, nesting >3 levels, magic numbers/strings in business logic, hardcoded config that should be env/settings, boolean parameter flags (control coupling), temporal coupling (must-call-in-order without enforcement) |
| ai-architecture | AIA-01 to AIA-10 | Over-engineering (interface with 1 impl, abstract class with 1 subclass, factory for 1 type, generic wrapper around single use case), local-only solutions presented as reusable (single-caller utility modules, config for 1 value), architectural drift (module violating its own established pattern), pattern inconsistency (same problem solved 3+ different ways across codebase) |
| functional-completeness | FUN-01 to FUN-18 | Missing CRUD/pagination/filter, incomplete error handling, state transition gaps, caching/indexing strategy |
| production-readiness | PRD-01 to PRD-07 | Health/readiness probe completeness, graceful shutdown handling, config validation at startup, secret injection method (env vs hardcoded), container/deployment hygiene (Dockerfile best practices, compose config), observability hooks (structured logging, metrics endpoints, trace propagation), scaling bottlenecks (stateful components, connection pool limits, single points of failure) |
| cross-cutting | XCT-01 to XCT-05 | Decision impact tracing: how one architectural choice affects other areas (performance, testability, security, maintainability). Only report concrete cross-area impacts with evidence at file:line |

### Audit Scopes (project-level assessment)

| Scope | ID Range | Focus |
|-------|----------|-------|
| stack-assessment | STK-01 to STK-10 | Framework fitness, runtime currency, build tool match, redundant deps, dep weight, SDK alignment |
| dependency-health | DEP-01 to DEP-10 | Abandoned packages, license conflicts, pinning strategy, dev/prod boundary, duplicate versions, known CVEs, supply chain risk, outdated major versions |
| dx-quality | DXQ-01 to DXQ-10 | Setup friction, env docs, script discoverability, CI/local parity, error message quality, IDE support |
| project-structure | PST-01 to PST-10 | Directory conventions, naming consistency, feature isolation, config sprawl, gitignore completeness |

## Fix Suggestion Principles

Per CCO Rules: Fix Quality. Every `fix` field must comply.

**Fix quality gate:** Before including a `fix` field: (1) Grep for existing implementations — if found, reference instead of creating new, (2) Read 2-3 existing patterns — match the style, (3) verify minimal change. If verification fails → set `fix` to: "Use existing {pattern} from {file}:{line}".

## Judgment Rules

Per CCO Rules: Severity Levels, Confidence Scoring, Skip Patterns.

| Rule | Detail |
|------|--------|
| Evidence | Every finding cites `file:line`. Read actual code before reporting. |
| Conservative | Uncertain → lower severity. Style → max LOW. Single occurrence → max MEDIUM (except security). |
| Pattern threshold | 3+ examples before concluding systemic pattern |
| CRITICAL validation | Analyze as "this is a bug" AND "this might be intentional". Both agree → include. Disagree → downgrade. |
| CRITICAL/HIGH gate | Before finalizing: (1) re-read the file section, (2) check skip patterns, (3) verify not test/mock/fixture context, (4) for "committed to repo" findings — verify file is actually git-tracked via `git ls-files`, (5) check surrounding 5 lines for intent signals (comments explaining why, variable names suggesting intentionality like `_deliberately`, `_unsafe_but_ok`). Any check fails → downgrade one severity level. |
