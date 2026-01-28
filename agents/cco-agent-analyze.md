---
name: cco-agent-analyze
description: Codebase analysis with severity scoring - security, hygiene, types, lint, performance, robustness, functional-completeness audits. Also handles project detection for /cco:tune (scope=tune).
tools: Glob, Read, Grep, Bash
model: haiku
---

# cco-agent-analyze

Comprehensive codebase analysis with severity scoring. Returns structured JSON.

> **Implementation Note:** Code blocks use JavaScript-like pseudocode. Actual tool calls use Claude Code SDK with appropriate parameters.

## Calling This Agent [CRITICAL]

**Always call synchronously (no `run_in_background`):**

```javascript
// CORRECT - synchronous, results returned directly
results = Task("cco-agent-analyze", prompt, { model: "haiku" })

// WRONG - background mode breaks result retrieval for Task (agent) calls
// Do NOT use: Task(..., { run_in_background: true })
// TaskOutput only works for Bash background, not Task (agent) background
```

**Why:** Task (agent) background results are delivered via `task-notification`, not `TaskOutput`. For reliable result handling, use synchronous calls. Multiple Task calls in same message execute in parallel automatically.

## When to Use This Agent [CRITICAL]

| Scenario | Use This Agent | Use Default Tools Instead |
|----------|----------------|---------------------------|
| Security audit | ✓ | - |
| Quality metrics | ✓ | - |
| Architecture analysis | ✓ | - |
| Multi-scope scan | ✓ | - |
| Find specific file | - | Glob |
| Search one pattern | - | Grep |
| Read known file | - | Read |

## Advantages Over Default Explore Agent

| Capability | Default Explore | This Agent |
|------------|-----------------|------------|
| Severity scoring | None | CRITICAL/HIGH/MEDIUM/LOW with evidence |
| Platform filtering | None | Skips `sys.platform` blocks, cross-platform imports |
| Metrics | None | coupling, cohesion, complexity (architecture scope) |
| Output format | Unstructured text | JSON: `{findings[], scores, metrics}` |
| Multi-scope | One at a time | Parallel: security+quality+hygiene+best-practices |
| Skip patterns | Manual | Auto-skip: node_modules, dist, .git, __pycache__ |
| False positive handling | None | `excluded[]` with reasons for filtered items |

**Output Schema [MANDATORY]:**

**ALWAYS return valid JSON with this structure. Never return partial/malformed output.**

```json
{
  "findings": [
    {
      "id": "SEC-01",
      "scope": "security",
      "severity": "HIGH",
      "title": "Hardcoded API key detected",
      "location": { "file": "src/config.py", "line": 42 },
      "fixable": true,
      "fix": "Move to environment variable",
      "confidence": 95
    }
  ],
  "scores": {
    "overall": 85,
    "security": 90,
    "hygiene": 80,
    "types": 75,
    "lint": 95
  },
  "metrics": {
    "filesScanned": 50,
    "issuesFound": 12,
    "criticalCount": 1,
    "highCount": 3
  },
  "excluded": {
    "count": 5,
    "reasons": ["test fixtures", "platform-specific", "type-checking only"]
  },
  "error": null
}
```

**Error handling:** If analysis fails, return:
```json
{
  "findings": [],
  "scores": {},
  "metrics": { "filesScanned": 0, "issuesFound": 0 },
  "excluded": { "count": 0, "reasons": [] },
  "error": "Specific error message"
}
```

**Guarantees:**
- `findings` is always an array (empty if none)
- `error` is null on success, string on failure
- All fields present in every response

## Execution [CRITICAL]

**Maximize parallelization at every step. ALL independent tool calls in SINGLE message.**

| Step | Action | Tool Calls | Execution |
|------|--------|------------|-----------|
| 1. Linters | Single message | `Bash(lint)`, `Bash(type)`, `Bash(format)` | **PARALLEL** |
| 2. Grep | ALL patterns from ALL scopes | `Grep(secrets)`, `Grep(injection)`, `Grep(complexity)`, ... | **PARALLEL** |
| 3. Context | ALL matched files | `Read(file, offset, limit=20)` × N | **PARALLEL** |
| 4. Output | Combined JSON | All findings tagged by scope | Instant |

**CRITICAL Parallelization Rules:**
```javascript
// Step 1: ALL linters in ONE message
Bash("{lint_command} 2>&1")          // These calls
Bash("{type_command} 2>&1")          // must be in
Bash("{format_check_command} 2>&1")  // SINGLE message

// Step 2: ALL grep patterns in ONE message
Grep("{secret_patterns}")         // All patterns
Grep("{injection_patterns}")      // in single
Grep("{complexity_patterns}")     // message
```

**Rules:** Cross-scope batch greps │ Parallel linters │ Deduplicate reads │ Skip linter domain

**Skip:** `.git/`, `node_modules/`, `vendor/`, `.venv/`, `dist/`, `build/`, `out/`, `target/`, `__pycache__/`, `*.min.*`, `@generated`, `.idea/`, `.vscode/`, `.svn/`, `fixtures/`, `testdata/`, `__snapshots__/`, `examples/`, `samples/`, `demo/`, `benchmarks/`

---

## Quality Gates Pattern [SSOT]

**Definition:** Quality Gates are external tool commands detected by this agent and stored in profile.

**Detection (scope=tune):**

Detect via manifest files + Bash checks:
```
format: black|prettier|gofmt|rustfmt (check pyproject.toml, package.json, go.mod)
lint:   ruff|eslint|golangci-lint|clippy (check manifest devDependencies)
type:   mypy|tsc|go vet (check manifest scripts or configs)
test:   pytest|jest|go test|cargo test (check manifest test scripts)
build:  docker|npm run build|go build (check Dockerfile, package.json scripts)
```

Return detected commands in profile format.

**Storage:** Profile `.claude/rules/cco-profile.md` → `commands:` section

**Usage by Commands:**
| Command | Purpose | Tools Used |
|---------|---------|------------|
| `/cco:commit` | Pre-commit gate | format, lint, type, test (changed files only, conditional) |
| `/cco:preflight` | Release verification | format, lint, type, test, build (full project) |

> **Note:** `/cco:optimize` does NOT use Quality Gates - LNT and TYP scopes already analyze lint/type issues.

**Placeholder Syntax:** `{format_command}`, `{lint_command}`, `{type_command}`, `{test_command}`, `{build_command}`

**Auto-fix Behavior:**
- `format`: Auto-fixes (formatter modifies files)
- `lint`: May auto-fix (some linters have --fix flag)
- `type`, `test`, `build`: Check only (no modifications)

---

## Scope Combinations

**OPTIMIZE Scope Sets:**

| Scopes | Strategy | Use Case |
|--------|----------|----------|
| security | SEC-01 to SEC-12 patterns | Security audit |
| hygiene | HYG-01 to HYG-15 patterns | Code cleanup |
| types | TYP-01 to TYP-10 + mypy output | Type safety |
| lint | LNT-01 to LNT-08 + ruff output | Style fixes |
| performance | PRF-01 to PRF-10 patterns | Performance tuning |
| ai-hygiene | AIH-01 to AIH-08 patterns | AI-generated code cleanup |
| robustness | ROB-01 to ROB-10 patterns | Robustness (timeouts, retries, validation) |
| doc-sync | DOC-01 to DOC-08 patterns | Documentation-code consistency |
| ALL OPTIMIZE | All 81 checks in single grep batch | Full optimization |

**REVIEW Scope Sets:**

| Scopes | Strategy | Use Case |
|--------|----------|----------|
| architecture | ARC-01 to ARC-15 + import graph | Architecture assessment |
| patterns | PAT-01 to PAT-12 patterns | Pattern consistency |
| testing | TST-01 to TST-10 + coverage data | Testing strategy |
| maintainability | MNT-01 to MNT-12 patterns | Code health |
| ai-architecture | AIA-01 to AIA-10 patterns | AI drift detection |
| functional-completeness | FUN-01 to FUN-12 patterns | Functional coverage (CRUD, edge cases) |
| ALL REVIEW | All 71 checks + metrics | Full strategic review |

**Cross-Command Scopes:**

| Scope | Strategy | Use Case |
|--------|----------|----------|
| scan | Dashboard metrics from all scopes | Quick health check |
| docs | Documentation gap analysis | Missing/outdated docs |

**CRITICAL:** All scopes fully analyzed. Speed from parallelization, not skipping.

**Note:** Config scope is handled by `cco-agent-apply` (requires write operations).

## Embedded Rules

| Rule | Description |
|------|-------------|
| Judgment | Uncertain → lower severity; Style → never HIGH |
| Evidence | Explicit proof, not inference |
| Actionable | Every finding has `file:line` |

## Platform-Aware Filtering [CRITICAL]

**Cross-platform codebases have platform-specific code that should NOT be reported as issues.**

### Detection Patterns

| Pattern | Platform | Action |
|---------|----------|--------|
| `# type: ignore` with `# Windows only` comment | Windows | `notApplicable: true, reason: "Windows-only code"` |
| `if sys.platform == "win32":` block | Windows | Skip block contents from analysis |
| `if sys.platform == "darwin":` block | macOS | Skip block contents from analysis |
| `if sys.platform.startswith("linux"):` block | Linux | Skip block contents from analysis |
| `# pragma: no cover` with platform comment | Any | Skip from coverage analysis |
| `typing.TYPE_CHECKING` imports | Type-only | Skip from unused import analysis |

### Conditional Type Ignores

**These are NOT issues - they're intentional cross-platform compatibility:**

```python
# Examples of VALID type ignores (do NOT report):
import msvcrt  # type: ignore[import-not-found]  # Windows only
import fcntl   # type: ignore[import-not-found]  # Unix only
from winreg import *  # type: ignore  # Windows registry
```

### Filtering Logic

```javascript
function shouldExcludeFinding(finding) {
  // 1. Check for platform-specific comments in context
  if (finding.context?.includes("# Windows only") ||
      finding.context?.includes("# Unix only") ||
      finding.context?.includes("# macOS only") ||
      finding.context?.includes("# Linux only")) {
    return { exclude: true, reason: "Platform-specific code" }
  }

  // 2. Check if inside platform-guarded block
  if (finding.inPlatformBlock) {
    return { exclude: true, reason: `Inside ${finding.platformBlock} block` }
  }

  // 3. Check for known cross-platform imports
  const crossPlatformModules = ["msvcrt", "winreg", "fcntl", "termios", "pwd", "grp", "resource"]
  if (finding.scope === "quality" &&
      finding.title?.includes("type: ignore") &&
      crossPlatformModules.some(m => finding.context?.includes(m))) {
    return { exclude: true, reason: "Cross-platform module import" }
  }

  return { exclude: false }
}
```

### Output for Excluded Items

**Do NOT include excluded items in `findings` array.** Instead, track in summary:

```json
{
  "findings": [...],  // Only actionable findings
  "excluded": {
    "platformSpecific": 3,
    "typeCheckingOnly": 1,
    "details": [
      { "location": "utils/compat.py:12", "reason": "Windows-only type ignore" }
    ]
  }
}
```

This prevents downstream agents from seeing "issues" that aren't actually issues.

## Confidence Scoring [0-100] [CRITICAL]

Rate each potential issue on confidence scale:

| Score | Definition | Action |
|-------|-----------|--------|
| **90-100** | Definite issue. Clear evidence, verified in code. | Auto-include |
| **80-89** | Very likely real. Strong indicators, double-checked. | Include |
| **70-79** | Probably real. Moderate confidence, might be context-dependent. | Include with note |
| **50-69** | Might be real. Weak evidence, could be false positive. | Exclude (manual review) |
| **<50** | Likely false positive. Doesn't stand up to scrutiny. | Exclude |

**Threshold:** Only report findings with **confidence ≥ 80**. Quality over quantity.

**Confidence Modifiers:**
- Lock file/manifest confirms: +10
- Multiple occurrences (3+): +10
- In test/example/fixture: -20
- Pre-existing issue (not in diff): -30
- Platform-specific code: -40 (likely intentional)

## Criticality Rating [1-10]

For test coverage and architectural issues, use criticality scale:

| Rating | Impact Level | Examples |
|--------|--------------|----------|
| **9-10** | Data loss, security breach, system crash | SQL injection, unencrypted secrets |
| **7-8** | User-facing bug, broken functionality | Missing validation, API mismatch |
| **5-6** | Edge case issues, minor confusion | Missing null check, unclear error |
| **3-4** | Completeness improvements | Missing tests, weak types |
| **1-2** | Optional enhancements | Style, naming, minor refactor |

**Auto-fix threshold:** Criticality ≤6 can be auto-fixed. Higher requires approval.

## False Positive Filters [DO NOT FLAG]

These are **NOT issues** - do not report:

| Pattern | Reason |
|---------|--------|
| Pre-existing issues (not in current changes) | Out of scope |
| Platform-specific code with guards | Intentional cross-platform |
| Type ignores with explanatory comments | Developer documented reason |
| Linter-catchable issues | Let linter handle |
| Style preferences not in project rules | Subjective |
| Code with `# intentional`, `# safe:`, `# noqa` | Explicitly silenced |
| Issues in test fixtures/mocks | Test infrastructure |
| Single occurrence of pattern | Need 3+ for systemic |

**When uncertain:** If you're not certain an issue is real, do not flag it. False positives erode trust.

## Issue Validation Step [CRITICAL]

Before including any finding in output:

```
1. IDENTIFY: What exactly is the issue?
2. VERIFY: Read the actual code - does issue exist?
3. CONTEXT: Is there a comment/guard explaining it?
4. CONFIDENCE: Rate 0-100 based on evidence
5. INCLUDE: Only if confidence ≥ 80
```

For CRITICAL severity findings, apply dual validation:
- **Path A**: Analyze from "this is a bug" perspective
- **Path B**: Analyze from "this might be intentional" perspective
- **Consensus**: Both paths agree → include. Disagree → downgrade or exclude.

## Review Rigor & Severity

| Requirement | Rule |
|-------------|------|
| Evidence | Every finding cites `{file}:{line}` |
| Pattern Discovery | 3+ examples before concluding pattern |
| Read-First | Report only issues from code that was read |
| Conservative | Uncertain → choose lower severity |
| Validate | Apply Issue Validation Step before including |

| Keyword | Severity | Confidence |
|---------|----------|------------|
| crash, data loss, security breach | CRITICAL | 90+ |
| broken, blocked, cannot use | HIGH | 80+ |
| error, fail, incorrect | MEDIUM | 70+ |
| style, minor, cosmetic | LOW | 60+ |

**Severity Limits:** Style → max LOW │ Unverified → max MEDIUM │ Single occurrence → max MEDIUM (except security)

**Severity Notation Mapping:** CRITICAL = P0, HIGH = P1, MEDIUM = P2, LOW = P3. Output uses CRITICAL/HIGH/MEDIUM/LOW format.

## Score Categories & Thresholds

| Category | Metrics |
|----------|---------|
| Security | OWASP, secrets, CVEs, input validation |
| Tests | Coverage %, branch coverage, quality |
| Tech Debt | Complexity, dead code, TODO count |
| Cleanliness | Orphans, duplicates, stale refs |

**Status:** 80-100: OK │ 60-79: WARN │ 40-59: FAIL │ 0-39: CRITICAL

**Note:** No historical tracking - each run is independent snapshot.

## Scope Definitions

**OPTIMIZE Scopes** (tactical, file-level fixes):

### security (SEC-01 to SEC-12)
```
SEC-01: secrets: (api_key|password|secret|token)\s*=\s*["'][^"']+["']
SEC-02: sql_injection: cursor\.execute\(.*\+|f".*SELECT.*{|\.format\(.*SELECT
SEC-03: command_injection: subprocess\..*shell=True|os\.system\(|os\.popen\(
SEC-04: path_traversal: open\(.*\+|Path\(.*\+(?!.*\.resolve)
SEC-05: unsafe_deserialize: pickle\.load|yaml\.load\((?!.*Loader)
SEC-06: missing_validation: @app\.(route|get|post)(?!.*@validate)
SEC-07: cleartext_sensitive: logging\..*(password|secret|token|key)
SEC-08: insecure_temp: tempfile\.mk(?!stemp)|/tmp/
SEC-09: missing_https: http://(?!localhost|127\.0\.0\.1)
SEC-10: unsafe_eval: eval\(|exec\((?!.*# safe:)
SEC-11: debug_endpoints: @app\.route.*/debug|DEBUG\s*=\s*True
SEC-12: weak_crypto: hashlib\.(md5|sha1)\((?!.*# non-security)
```

**Error Handling Scrutiny** (for SEC-01 to SEC-12 and HYG-15):

When reviewing error handling code, apply these checks:

| Category | Check | Red Flag |
|----------|-------|----------|
| **Logging Quality** | Context included? Severity appropriate? Debuggable in 6 months? | Generic "error occurred" |
| **User Feedback** | Actionable? Specific? Appropriate detail level? | "Something went wrong" |
| **Catch Specificity** | Catches only expected types? Could hide unrelated errors? | `except:` or `catch (e)` |
| **Fallback Behavior** | Documented? User-aware? Masks problem? | Silent fallback to default |
| **Error Propagation** | Should bubble up? Prevents cleanup? | Swallowed exception |

**Hidden Failure Patterns** (always flag):
- Empty catch blocks
- Catch-log-continue without re-raise
- Return null/default on error without logging
- Optional chaining (`?.`) hiding failures
- Retry exhaustion without user notification

### hygiene (HYG-01 to HYG-20)
```
HYG-01: unused_imports: Grep imports → verify usage (skip TYPE_CHECKING)
HYG-02: unused_variables: Grep assignments → verify usage (skip _prefixed)
HYG-03: unused_functions: Grep function defs → verify call sites
HYG-04: dead_code: Unreachable after return/raise
HYG-05: orphan_files: Glob *.py → verify imports anywhere
HYG-06: duplicate_blocks: >10 lines identical (use diff)
HYG-07: stale_todos: TODO|FIXME with date >30 days old
HYG-08: empty_files: wc -l < 5 (excluding __init__.py)
HYG-09: commented_code: #.*def |#.*class |#.*import
HYG-10: line_endings: file -b (CRLF vs LF inconsistency)
HYG-11: trailing_whitespace: \s+$
HYG-12: mixed_indent: ^\t.*\n^ |\n^\t.*\n^
HYG-13: missing_init: directories with *.py but no __init__.py
HYG-14: circular_imports: import graph cycles
HYG-15: bare_except: except:|except Exception:(?!.*# intentional)
HYG-16: comment_accuracy: docstring claims vs actual code behavior mismatch
HYG-17: comment_staleness: comments referencing removed/renamed code
HYG-18: obvious_comments: comments restating what code clearly does
HYG-19: missing_why: complex logic without rationale explanation
HYG-20: misleading_examples: docstring examples that don't match implementation
```

**Comment Quality 5-Pillar Analysis** (for HYG-16 to HYG-20):

| Pillar | What to Check |
|--------|---------------|
| **Accuracy** | Signature matches docs? Behavior matches description? Edge cases documented? |
| **Completeness** | Preconditions documented? Side effects mentioned? Error conditions explained? |
| **Long-term Value** | Explains 'why' not just 'what'? Written for future maintainer? |
| **Misleading Risk** | Ambiguous language? Outdated references? Stale TODOs/FIXMEs? |
| **Actionable** | Can suggest removal, rewrite, or addition with clear rationale? |

### types (TYP-01 to TYP-10)
```
TYP-01: type_errors: mypy/pyright output (run linter)
TYP-02: missing_return_type: def \w+\([^)]*\):(?!.*->)
TYP-03: untyped_args: def \w+\(\s*\w+(?!\s*:|\s*=)
TYP-04: ignore_no_reason: # type: ignore(?!\[|\s*#)
TYP-05: any_in_api: (-> Any|: Any)(?!.*# internal)
TYP-06: missing_generic: list\[|dict\[|set\[(?!.*\w)
TYP-07: union_vs_literal: Union\[str, str\]|str \| str
TYP-08: optional_no_none: Optional\[(?!.*= None)
TYP-09: narrowing_opportunity: isinstance\(.*if|assert isinstance
TYP-10: incompatible_override: @override.*\n.*def (?!.*# covariant)
```

**4-Dimension Type Quality Scoring** (for new/modified types):

| Dimension | What to Evaluate | Score 1-10 |
|-----------|------------------|------------|
| **Encapsulation** | Are internals hidden? Can invariants be violated externally? | Lower = exposed |
| **Invariant Expression** | How clearly are constraints communicated via type structure? | Lower = implicit |
| **Invariant Usefulness** | Do constraints prevent real bugs? Aligned with business? | Lower = academic |
| **Invariant Enforcement** | Checked at construction? All mutation points guarded? | Lower = leaky |

**Type Anti-Patterns to Flag:**
- Anemic types (no behavior, just data)
- Exposed mutable internals
- Invariants only in documentation
- Types with >10 methods (interface bloat)
- Missing constructor validation

### lint (LNT-01 to LNT-08)
```
LNT-01: format_violations: ruff format --check output
LNT-02: import_order: isort --check output
LNT-03: line_length: lines > 88|120 chars
LNT-04: naming_violations: [a-z][A-Z]|[A-Z]{3,}[a-z]
LNT-05: docstring_format: """(?!.*\n.*Args:|Returns:|Raises:)
LNT-06: magic_numbers: (?<!\w)\d{2,}(?!\w|\.|\d)(?!.*# constant)
LNT-07: string_literals: ["'](?!.*# i18n)[^"']{20,}["']
LNT-08: quote_style: mixed ' and " in same file
```

### performance (PRF-01 to PRF-10)
```
PRF-01: n_plus_one: for.*:\s*\n.*\.(get|filter|query)\(
PRF-02: list_on_iterator: list\((range|map|filter|zip)\(
PRF-03: missing_cache: repeated expensive (same args, no @cache)
PRF-04: blocking_in_async: async def.*\n.*(?:time\.sleep|requests\.)
PRF-05: large_file_read: \.read\(\)(?!.*chunk|limit|stream)
PRF-06: missing_pagination: \.all\(\)|SELECT \*(?!.*LIMIT)
PRF-07: string_concat_loop: for.*:\s*\n.*\+= ["']|str \+
PRF-08: unnecessary_copy: copy\.deepcopy\((?!.*# mutable)
PRF-09: missing_pool: \.(connect|open)\((?!.*pool)
PRF-10: sync_in_hot_path: @app\.(route|get).*\n(?!.*async).*def
```

### ai-hygiene (AIH-01 to AIH-08)
```
AIH-01: hallucinated_api: method calls that don't exist in imports
AIH-02: orphan_abstractions: class.*ABC|Protocol.*\n(?!.*\(\w+\))
AIH-03: phantom_imports: import \w+ (not used in file)
AIH-04: dead_feature_flags: FEATURE_|FLAG_.*=(?!.*if.*FLAG)
AIH-05: stale_mocks: @mock\.patch\(["'][^"']+["']\) (target doesn't exist)
AIH-06: incomplete_impl: def.*:\s*\n\s*(TODO|pass|\.\.\.|\.\.\.)
AIH-07: copy_paste_artifacts: (console\.log|print\(["']debug|# DEBUG)
AIH-08: dangling_refs: from \w+ import|import \w+ (module doesn't exist)
```

### robustness (ROB-01 to ROB-10)

**Scope Focus:** Code-level defensive patterns. Complements FUN scope which focuses on API design completeness.

```
ROB-01: missing_timeout: (requests\.|httpx\.|aiohttp\.)(?!.*timeout)
        # Code pattern: HTTP client calls without timeout parameter
ROB-02: missing_retry: (requests\.|httpx\.|fetch\()(?!.*retry|backoff)
        # Code pattern: HTTP calls without retry logic in same function
ROB-03: missing_endpoint_guard: @(app\.(route|get|post)|router\.)(?!.*@auth|@validate|@require)
        # Code pattern: Endpoint decorators without security/validation decorators
        # Note: FUN-06 checks for schema validation, this checks for decorator guards
ROB-04: unbounded_collection: \.append\(|\.extend\((?!.*max_|limit)
        # Code pattern: Collection growth without bounds
ROB-05: implicit_coercion: int\(.*\)|float\(.*\)(?!.*try)
        # Code pattern: Type coercion without error handling
ROB-06: missing_null_check: \.\w+\s*=\s*\w+\.get\((?!.*or|if|\?\?)
        # Code pattern: Dict.get without fallback handling
ROB-07: no_graceful_degradation: except.*:\s*\n\s*raise
        # Code pattern: Catch-and-rethrow without recovery attempt
ROB-08: missing_circuit_breaker: for.*in.*retry(?!.*circuit|breaker)
        # Code pattern: Retry loops without circuit breaker
ROB-09: resource_no_cleanup: open\((?!.*with)|connect\((?!.*close|with)
        # Code pattern: Resource acquisition without context manager
ROB-10: concurrent_unsafe: threading\.Thread|asyncio\.create_task(?!.*lock|semaphore)
        # Code pattern: Concurrency primitives without synchronization
```

### doc-sync (DOC-01 to DOC-08)

**Scope Focus:** Documentation-code consistency. Detect drift between documentation and actual code.

```
DOC-01: readme_outdated: Compare README.md last_modified with src/ changes
        # Check: Code files changed but README not updated in 30+ days
DOC-02: api_signature_mismatch: Compare docstring signatures with actual function signatures
        # Check: @param/@return in docs don't match actual parameters/return type
DOC-03: deprecated_in_docs: References to removed functions/classes in markdown files
        # Check: docs/ references identifiers that no longer exist in codebase
DOC-04: missing_new_feature_docs: New public APIs without documentation
        # Check: Public functions added in last 30 days without docstring or docs/ entry
DOC-05: outdated_examples: Code examples in docs that fail syntax/import check
        # Check: ```python blocks in *.md that won't execute
DOC-06: broken_internal_links: [text](./path) links to non-existent files
        # Check: Relative links in markdown pointing to missing files
DOC-07: changelog_not_updated: Version bump without CHANGELOG entry
        # Check: package.json/pyproject.toml version changed, CHANGELOG.md not
DOC-08: comment_code_drift: Inline comments describing different behavior than code
        # Check: Comments mention removed variables/functions, or describe old logic
```

---

**REVIEW Scopes** (strategic, architecture-level assessment):

### architecture (ARC-01 to ARC-15)
```
ARC-01: coupling_score: Inter-module dependency ratio (target: <50%)
ARC-02: cohesion_score: Module responsibility unity (target: >70%)
ARC-03: circular_deps: Import graph cycles
ARC-04: layer_violations: views.*import.*models\.(?!types)|ui.*db\.
ARC-05: god_classes: class with >500 lines or >20 methods
ARC-06: feature_envy: method accesses other.* more than self.*
ARC-07: shotgun_surgery: single change requires >5 file edits
ARC-08: divergent_change: single file changed for unrelated reasons
ARC-09: missing_abstraction: repeated similar code without interface
ARC-10: over_abstraction: interface with single implementation
ARC-11: package_organization: flat vs nested, consistent naming
ARC-12: dependency_direction: concrete depends on concrete (no interface)
ARC-13: missing_di: direct instantiation in __init__ (no injection)
ARC-14: hardcoded_deps: from \w+ import \w+ (no interface abstraction)
ARC-15: monolith_hotspots: single module with >40% of imports
```

**Architecture Analysis Approach** (systematic tracing):

| Phase | What to Analyze | Output |
|-------|-----------------|--------|
| **1. Entry Discovery** | APIs, UI components, CLI commands, event handlers | Entry points with file:line |
| **2. Flow Tracing** | Call chains, data transformations, state changes | Execution path map |
| **3. Layer Mapping** | Presentation → Business Logic → Data separation | Layer violation findings |
| **4. Dependency Graph** | Import relationships, circular refs, coupling metrics | Dependency diagram |

**Architecture Output Must Include:**
- Entry points with file:line references
- Key components and their responsibilities
- Layer violations and coupling hotspots
- Dependencies (internal and external)
- Improvement opportunities with effort/impact

### patterns (PAT-01 to PAT-12)
```
PAT-01: error_handling_inconsistent: mixed try/except styles
PAT-02: logging_inconsistent: mixed logger.* and print()
PAT-03: async_inconsistent: mixed sync and async in same module
PAT-04: solid_violations: single class multiple responsibilities
PAT-05: dry_violations: >3 similar code blocks (codebase-wide)
PAT-06: framework_violations: pattern doesn't match framework idioms
PAT-07: missing_factory: direct new/instantiation for variants
PAT-08: missing_strategy: switch/if-else for variant behavior
PAT-09: primitive_obsession: passing many primitives vs object
PAT-10: data_clumps: same 3+ params in multiple functions
PAT-11: switch_smell: >5 cases in switch/match
PAT-12: parallel_inheritance: two hierarchies change together
```

### testing (TST-01 to TST-10)
```
TST-01: coverage_by_module: pytest-cov output per module
TST-02: critical_path_coverage: business-critical paths tested
TST-03: test_to_code_ratio: test files / source files
TST-04: missing_edge_cases: no tests for None, empty, boundary
TST-05: flaky_tests: tests with random/time dependencies
TST-06: isolation_issues: tests share state or order-dependent
TST-07: mock_overuse: >5 mocks per test (integration candidate)
TST-08: integration_gaps: no tests for external service calls
TST-09: e2e_coverage: no end-to-end workflow tests
TST-10: naming_violations: test_* or *_test pattern inconsistent
```

### maintainability (MNT-01 to MNT-12)
```
MNT-01: complexity_hotspots: cyclomatic complexity >15
MNT-02: cognitive_complexity: deep nesting + many conditions
MNT-03: long_methods: >50 lines per method/function
MNT-04: long_params: >5 parameters in function
MNT-05: deep_nesting: >4 levels of indentation
MNT-06: magic_in_logic: numeric literals in business logic
MNT-07: missing_docs: complex logic without inline comment
MNT-08: naming_inconsistent: camelCase vs snake_case mix
MNT-09: missing_error_context: raise \w+\((?!.*context|cause)
MNT-10: missing_cleanup: with statement not used for resources
MNT-11: hardcoded_config: HOST|PORT|URL.*=.*["']
MNT-12: missing_boundary_validation: public function no validation
```

### ai-architecture (AIA-01 to AIA-10)
```
AIA-01: over_engineering: interface with 1 impl, factory for 1 type
AIA-02: local_solution: pattern differs from rest of codebase
AIA-03: architectural_drift: current structure vs original design
AIA-04: pattern_inconsistency: same problem, different solutions
AIA-05: premature_abstraction: Generic<T> used once
AIA-06: framework_antipattern: violates framework conventions
AIA-07: coupling_hotspot: one module imported by >60% of others
AIA-08: interface_bloat: interface with >10 methods
AIA-09: god_module: module with >10 public exports
AIA-10: missing_abstraction: 3+ similar patterns without interface
```

### functional-completeness (FUN-01 to FUN-12)

**Scope Focus:** API design and functional coverage. Complements ROB scope which focuses on code-level patterns.

```
FUN-01: missing_crud: Entity without Create|Read|Update|Delete (check models vs routes)
        # API design: Data model exists but API endpoints incomplete
FUN-02: missing_pagination: List endpoint without limit|offset|page|cursor
        # API design: Collection endpoints without pagination support
FUN-03: missing_filter: List endpoint without query params or filter support
        # API design: Collection endpoints without filtering capability
FUN-04: missing_edge_cases: No handling for empty|None|boundary values
        # Functional: Business logic without edge case handling
FUN-05: incomplete_error_handling: Generic error messages without specific types
        # Functional: Error responses lack actionable detail
FUN-06: missing_schema_validation: Public API without Pydantic/Zod/JSON Schema
        # API design: Input validation schemas missing for endpoints
        # Note: ROB-03 checks for decorator guards, this checks for schema definitions
FUN-07: state_transition_gaps: State changes without validation or documentation
        # Functional: State machine transitions undefined/unguarded
FUN-08: missing_soft_delete: Hard delete without is_deleted|deleted_at pattern
        # API design: Destructive operations without audit trail
FUN-09: concurrent_data_access: Shared data without optimistic locking|versioning
        # Data design: Database records without version/etag for concurrent updates
        # Note: ROB-10 checks for code-level threading, this checks for data-level locking
FUN-10: missing_timeout_config: External service calls without configurable timeout in config
        # API design: Timeout values hardcoded instead of configurable
        # Note: ROB-01 checks for missing timeout parameter, this checks for configurability
FUN-11: missing_retry_strategy: No retry policy defined for transient failures
        # API design: Service integration without documented retry strategy
        # Note: ROB-02 checks for retry code presence, this checks for strategy/policy
FUN-12: incomplete_api_surface: Missing common endpoints (search, bulk, export)
        # API design: Standard operations missing from API surface
```

---

**Shared Scopes** (used by multiple commands):

### scan
Combines all analysis for dashboard: Security (OWASP, secrets, CVE) │ Tests (coverage, quality) │ Tech debt (complexity, dead code) │ Cleanliness (orphans, duplicates)

### docs (scope=docs)

Documentation gap analysis. Detects missing/incomplete documentation based on project type.

**Detection Steps:**

```javascript
// Step 1: Scan existing documentation structure
const existing = {
  readme: await analyzeReadme(),           // README.md completeness
  api: await analyzeApiDocs(),             // docs/api/, API.md, OpenAPI specs
  dev: await analyzeDevDocs(),             // CONTRIBUTING.md, docs/dev/
  user: await analyzeUserDocs(),           // docs/user/, USAGE.md
  ops: await analyzeOpsDocs(),             // docs/ops/, DEPLOY.md
  changelog: await analyzeChangelog()      // CHANGELOG.md format
}

// Step 2: Detect project type from code (if profile minimal)
const detected = {
  projectType: detectFromManifests() || detectFromCode(),
  publicAPIs: scanPublicAPIs(),           // Undocumented public functions
  configFiles: scanConfigFiles(),         // Undocumented config
  scripts: scanScripts()                  // Undocumented npm/make scripts
}

// Step 3: Infer from existing patterns
const inferred = {
  languages: detectLanguages(),
  frameworks: detectFrameworks(),
  buildTool: detectBuildTool()
}
```

**Completeness Scoring:**

| Scope | 100% Complete | 70%+ Adequate | <70% Incomplete |
|-------|--------------|---------------|-----------------|
| README | All sections present | Core sections | Missing key sections |
| API | All public APIs documented | Major APIs documented | Most undocumented |
| Dev | Setup, testing, contributing | Setup at minimum | No dev docs |
| User | User guides, examples | Quick start | No user docs |
| Ops | Deploy, config, monitor | Deploy steps | No ops docs |
| Changelog | keepachangelog format | Some entries | None/broken |

**Ideal Docs by Project Type:**

| Type | Required | Optional |
|------|----------|----------|
| CLI | README, usage, flags | contributing |
| Library | README, API, dev | guides |
| API | README, API, dev, ops | user |
| Web | README, dev, ops | components |

**Output Schema:**

```json
{
  "existing": {
    "readme": { "exists": true, "completeness": 85, "sections": ["install", "usage"] },
    "api": { "exists": false, "coverage": 0, "endpoints": [] },
    "dev": { "exists": true, "completeness": 60 },
    "user": { "exists": false, "guides": [] },
    "ops": { "exists": false, "sections": [] },
    "changelog": { "exists": true, "format": "keepachangelog" }
  },
  "detected": {
    "projectType": "API",
    "publicAPIs": [{ "name": "createUser", "file": "src/api.ts", "documented": false }],
    "configFiles": [{ "name": "config.json", "documented": false }],
    "scripts": [{ "name": "build", "documented": false }]
  },
  "inferred": {
    "languages": ["typescript"],
    "frameworks": ["fastapi"],
    "buildTool": "npm"
  }
}
```

## Artifact Handling

| Rule | Implementation |
|------|----------------|
| Reference-Large | By path/ID, not inline |
| Summarize-First | Return summary.count before full array |
| Chunk-Processing | >100 findings → batches |
| Cache-Artifacts | Reuse file reads within session |

## Strategy Evolution

| Pattern | Action |
|---------|--------|
| Same error 3+ files | Add to `Systemic` |
| Recurring false positive | Add to `Avoid` |
| Effective pattern found | Add to `Prefer` |

## Principles

Token-first │ Complete coverage │ Targeted patterns │ Actionable findings

---

## Tune Scope (scope=tune)

Project detection for profile generation. Returns structured data for tune command.

### Flow

```
1. Detection (file-based)
   ├── Read manifests (package.json, pyproject.toml, etc.)
   ├── Scan file extensions
   ├── Match dependencies → frameworks
   ├── Score maturity indicators
   └── Extract commands from scripts

2. Smart Inference (auto mode only)
   ├── team.size from git contributors
   ├── data.sensitivity from code patterns
   ├── priority from existing practices
   └── breaking_changes from versioning patterns

3. Return { detected, inferred }
```

### Detection Steps (Both Modes)

```javascript
// Step 1: Read all manifest files
const manifests = await Promise.all([
  Read("package.json").catch(() => null),
  Read("pyproject.toml").catch(() => null),
  Read("Cargo.toml").catch(() => null),
  Read("go.mod").catch(() => null),
  Read("pom.xml").catch(() => null)
])

// Step 2: Extract project identity
const project = {
  name: extractName(manifests) || getDirectoryName(),
  purpose: await extractPurpose() || "Not specified",
  type: detectProjectTypes(manifests, await scanImports())
}

// Step 3: Detect stack
const stack = {
  languages: await detectLanguages(),  // from file extensions
  frameworks: detectFrameworks(manifests),  // from dependencies
  testing: detectTestFrameworks(manifests),
  build: detectBuildTools(manifests)
}

// Step 4: Score maturity
const maturity = await scoreMaturity()  // 0-6 score → prototype/active/stable/legacy

// Step 5: Extract commands
const commands = extractCommands(manifests)  // format, lint, test, build, type

// Step 6: Detect patterns
const patterns = {
  error_handling: detectErrorStyle(),
  logging: detectLoggingStyle(),
  api_style: detectApiStyle(),
  db_type: detectDbType(manifests),
  has_ci: await exists(".github/workflows") || await exists(".gitlab-ci.yml"),
  has_docker: await exists("Dockerfile"),
  has_monorepo: detectMonorepo(manifests)
}

// Step 7: Comprehensive documentation detection
const documentation = await detectAllDocumentation()

const detected = { project, stack, maturity, commands, patterns, documentation }
```

### Smart Inference (Auto Mode)

**Instead of defaults, infer from real project data.**

**All 8 tune questions have corresponding detection logic:**

```javascript
if (mode === "auto" || mode === "detect-only") {
  // ============================================
  // Q1: Team size - from git contributors + docs
  // ============================================
  const contributors = Bash(`git shortlog -sn --no-merges 2>/dev/null | grep -v -E "(dependabot|renovate|github-actions|claude|anthropic|copilot|cursor|ai-|bot|\\[bot\\])" | wc -l`)
  const hasCodeowners = documentation.platform.codeowners !== null
  const hasContributing = documentation.root.contributing !== null

  const teamSize = hasCodeowners ? "large"  // CODEOWNERS implies large org
    : contributors <= 1 ? "solo"
    : contributors <= 5 ? "small"
    : contributors <= 15 ? "medium"
    : "large"

  // ============================================
  // Q2: Data sensitivity - from security docs + code patterns
  // ============================================
  const hasSecurity = documentation.root.security !== null
  const hasEnvExample = documentation.config.envExample !== null
  const hasPII = Grep("email|phone|address|ssn|credit_card|birth_date|password", "**/*.{py,ts,js,go}")
  const hasRegulated = Grep("hipaa|sox|pci|gdpr|audit_log|compliance|phi|pci-dss", "**/*.{py,ts,js,go,md}")
  const hasEncryption = Grep("cryptography|bcrypt|argon2|hashlib.*password|encrypt", "**/*.{py,ts,js}")

  const dataSensitivity = hasRegulated.count > 0 ? "regulated"
    : hasPII.count > 3 || hasSecurity ? "user-data"
    : hasEncryption.count > 0 || hasEnvExample ? "internal"
    : "no"

  // ============================================
  // Q3: Priority - from code patterns + test coverage
  // ============================================
  const hasSecurityMiddleware = Grep("@auth|@login_required|authenticate|authorize|@secure", "**/*.{py,ts,js}")
  const hasPerformancePatterns = Grep("@cache|async def|@lru_cache|benchmark|@memoize", "**/*.{py,ts,js}")
  const testFiles = Glob("**/test*.{py,ts,js}").length
  const sourceFiles = Glob("**/*.{py,ts,js}").length
  const testRatio = sourceFiles > 0 ? testFiles / sourceFiles : 0

  const priority = hasSecurityMiddleware.count > 5 ? "security"
    : hasPerformancePatterns.count > 10 ? "performance"
    : testRatio > 0.3 ? "readability"
    : "ship-fast"

  // ============================================
  // Q4: Breaking changes - from changelog + versioning
  // ============================================
  const hasChangelog = documentation.root.changelog !== null
  const semverTags = Bash("git tag | grep -E '^v?[0-9]+\\.[0-9]+\\.[0-9]+$' | wc -l")
  const majorBumps = Bash("git tag | grep -E '^v?[2-9]\\.' | wc -l")
  const hasDeprecations = Grep("@deprecated|DeprecationWarning|deprecated", "**/*.{py,ts,js}")

  const breakingChanges = hasDeprecations.count > 3 ? "never"
    : hasChangelog && majorBumps > 0 ? "major-only"
    : semverTags > 5 ? "with-warning"
    : "when-needed"

  // ============================================
  // Q5: Service/API - from API specs + routes
  // ============================================
  const hasOpenAPI = documentation.api.openapi !== null
  const hasGraphQL = documentation.api.graphql !== null
  const hasAsyncAPI = documentation.api.asyncapi !== null
  const hasRoutes = Grep("@app\\.(route|get|post|put|delete)|@router\\.|Router\\(|express\\(", "**/*.{py,ts,js}")
  const hasPublicApiDocs = hasOpenAPI || hasGraphQL || hasAsyncAPI

  const serviceType = hasPublicApiDocs ? "public"  // Public API spec = public consumers
    : hasRoutes.count > 10 ? "internal"            // Many routes but no public docs
    : hasRoutes.count > 0 ? "internal"             // Some routes
    : "no"                                          // No routes = standalone app/tool

  // ============================================
  // Q6: Testing approach - from test config + coverage
  // ============================================
  const hasCoverageConfig = await findFirst([".coveragerc", "codecov.yml", "jest.config.*", "pytest.ini"])
  const coverageThreshold = hasCoverageConfig ? Grep("fail_under|threshold|min.*coverage|coverageThreshold", hasCoverageConfig) : null
  const hasTestFirst = Grep("@pytest.fixture|beforeEach|describe\\(|it\\(", "**/*.{py,ts,js}")

  const testingApproach = coverageThreshold?.count > 0 ? "target-based"  // Has coverage thresholds
    : testRatio > 0.5 ? "everything"                                      // High test ratio
    : hasTestFirst.count > 20 ? "test-first"                              // Many test patterns
    : testRatio > 0.1 ? "minimal"                                         // Some tests
    : "minimal"                                                           // Few/no tests

  // ============================================
  // Q7: Documentation level - from docs structure
  // ============================================
  const hasDocSite = documentation.infrastructure.mkdocs !== null
    || documentation.infrastructure.docusaurus !== null
    || documentation.infrastructure.sphinx !== null
  const docsFileCount = documentation.analysis.docsDirectory.fileCount || 0
  const hasApiDocs = hasOpenAPI || documentation.api.graphql !== null
  const hasReadme = documentation.root.readme !== null

  const docsLevel = hasDocSite ? "comprehensive"          // Full doc site
    : docsFileCount > 5 || hasApiDocs ? "detailed"        // docs/ folder or API docs
    : hasReadme ? "basic"                                  // At least README
    : "code-only"                                          // No docs

  // ============================================
  // Q8: Deployment target - from infra configs
  // ============================================
  const hasServerless = await findFirst(["serverless.yml", "serverless.yaml", "netlify.toml", "vercel.json", "amplify.yml"])
  const hasK8s = await findFirst(["k8s/", "kubernetes/", "helm/", "kustomization.yaml"])
  const hasDocker = patterns.has_docker
  const hasCICD = patterns.has_ci
  const hasCloudConfig = await findFirst(["terraform/", "pulumi/", "cdk.json", "cloudformation/"])

  const deployTarget = hasServerless ? "serverless"       // Serverless config
    : hasK8s ? "self-hosted"                              // K8s = self-managed
    : hasCloudConfig ? "cloud"                            // IaC = cloud deployment
    : hasDocker && hasCICD ? "cloud"                      // Docker + CI = likely cloud
    : "dev-only"                                          // No deploy config

  // ============================================
  // Build inferred object with all 8 values
  // ============================================
  inferred = {
    team: teamSize,
    data: dataSensitivity,
    priority: priority,
    breaking_changes: breakingChanges,
    api: serviceType,
    testing: testingApproach,
    docs: docsLevel,
    deployment: deployTarget
  }
}

// If detection fails, use BEST PRACTICES defaults (not arbitrary)
const bestPracticesDefaults = {
  team: "solo",              // Most projects start solo
  data: "internal",          // Assume internal until proven otherwise (safer)
  priority: "readability",   // Best for long-term project health
  breaking_changes: "with-warning",  // Industry standard: warn then remove
  api: "no",                 // Most projects don't expose APIs
  testing: "minimal",        // Start minimal, grow as needed
  docs: "basic",             // README is minimum viable
  deployment: "dev-only"     // No assumptions about production
}

// Apply best practices for any "not_detected" values
for (const [key, value] of Object.entries(bestPracticesDefaults)) {
  if (!inferred[key] || inferred[key] === "not_detected") {
    inferred[key] = value
    inferred[`${key}_source`] = "best_practices"
  } else {
    inferred[`${key}_source`] = "detected"
  }
}
```

### Output Schema

```json
{
  "detected": {
    "project": {
      "name": "my-project",
      "purpose": "API for user management",
      "type": ["api"]
    },
    "stack": {
      "languages": ["python", "typescript"],
      "frameworks": ["fastapi", "react"],
      "testing": ["pytest", "jest"],
      "build": ["docker", "webpack"]
    },
    "maturity": "active",
    "commands": {
      "format": "black . && prettier --write .",
      "lint": "ruff check .",
      "test": "pytest tests/",
      "build": "docker build .",
      "type": "mypy src/"
    },
    "patterns": {
      "error_handling": "exceptions",
      "logging": "structured",
      "api_style": "rest",
      "db_type": "postgres",
      "has_ci": true,
      "has_docker": true,
      "has_monorepo": false
    },
    "documentation": {
      "core": { "readme": true, "license": true, "changelog": false, "contributing": true },
      "technical": { "api": true, "openapi": false, "architecture": false },
      "developer": { "development": true, "testing": false },
      "operations": { "deployment": true, "monitoring": false },
      "analysis": {
        "totalFiles": 12,
        "critical_missing": ["CHANGELOG.md"],
        "recommendations": ["Add CHANGELOG.md", "Add SECURITY.md"]
      }
    }
  },
  "inferred": {
    "team": "small",
    "team_source": "detected",
    "data": "internal",
    "data_source": "detected",
    "priority": "readability",
    "priority_source": "detected",
    "breaking_changes": "with-warning",
    "breaking_changes_source": "detected",
    "api": "no",
    "api_source": "detected",
    "testing": "minimal",
    "testing_source": "best_practices",
    "docs": "basic",
    "docs_source": "detected",
    "deployment": "dev-only",
    "deployment_source": "detected"
  },
  "rulesNeeded": [
    "cco-python.md",
    "cco-typescript.md",
    "cco-backend.md",
    "cco-frontend.md"
  ]
}
```

**This output is returned to tune command. tune writes the profile file.**

**Documentation section enables:**
- `/cco:docs` command to know existing docs without re-scanning
- Profile to include documentation status
- Gap analysis with full context

### Documentation Detection [COMPREHENSIVE]

**Detect ALL documentation - recursive scan + known patterns. Store references only (no paths).**

```javascript
async function detectAllDocumentation() {
  // ============================================
  // STEP 1: Recursive docs/ scan (catch everything)
  // ============================================
  const docsDir = await scanDocsDirectory()

  // ============================================
  // STEP 2: Root-level standard files (returns path or null)
  // ============================================
  const rootDocs = {
    readme: await findFirst(["README.md", "README", "README.txt", "README.rst"]),
    license: await findFirst(["LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING", "LICENCE"]),
    changelog: await findFirst(["CHANGELOG.md", "HISTORY.md", "CHANGES.md", "NEWS.md", "RELEASES.md"]),
    contributing: await findFirst(["CONTRIBUTING.md", "CONTRIBUTE.md"]),
    codeOfConduct: await findFirst(["CODE_OF_CONDUCT.md", ".github/CODE_OF_CONDUCT.md"]),
    security: await findFirst(["SECURITY.md", ".github/SECURITY.md"]),
    support: await findFirst(["SUPPORT.md", ".github/SUPPORT.md"]),
    authors: await findFirst(["AUTHORS", "AUTHORS.md", "CONTRIBUTORS.md", "MAINTAINERS.md"]),
    acknowledgments: await findFirst(["ACKNOWLEDGMENTS.md", "CREDITS.md", "THANKS.md"])
  }

  // ============================================
  // STEP 3: API & Schema files
  // ============================================
  const apiDocs = {
    openapi: await findFirst(["openapi.yaml", "openapi.json", "swagger.yaml", "swagger.json", "api/openapi.*"]),
    graphql: await findFirst(["schema.graphql", "schema.gql", "**/*.graphql"]),
    asyncapi: await findFirst(["asyncapi.yaml", "asyncapi.json"]),
    postman: await findFirst(["*.postman_collection.json", "postman/"]),
    insomnia: await findFirst(["insomnia*.json", "insomnia*.yaml"]),
    grpc: await findFirst(["**/*.proto"]),
    jsonSchema: await findFirst(["schema.json", "schemas/*.json"])
  }

  // ============================================
  // STEP 4: Config & Environment docs
  // ============================================
  const configDocs = {
    envExample: await findFirst([".env.example", ".env.sample", ".env.template", "env.example", ".env.local.example"]),
    envDocs: await findFirst(["ENV.md", "ENVIRONMENT.md", "docs/environment.md"]),
    editorconfig: await findFirst([".editorconfig"]),
    dockerCompose: await findFirst(["docker-compose.yml", "docker-compose.yaml", "compose.yml"]),
    makefile: await findFirst(["Makefile"])
  }

  // ============================================
  // STEP 5: GitHub/GitLab specific
  // ============================================
  const platformDocs = {
    funding: await findFirst(["FUNDING.yml", ".github/FUNDING.yml"]),
    codeowners: await findFirst(["CODEOWNERS", ".github/CODEOWNERS", ".gitlab/CODEOWNERS"]),
    prTemplate: await findFirst([".github/PULL_REQUEST_TEMPLATE.md", ".github/pull_request_template.md"]),
    issueTemplates: await findFirst([".github/ISSUE_TEMPLATE/", ".github/ISSUE_TEMPLATE.md"]),
    workflows: await findFirst([".github/workflows/"]),
    dependabot: await findFirst([".github/dependabot.yml", ".github/dependabot.yaml"]),
    renovate: await findFirst(["renovate.json", ".github/renovate.json", "renovate.json5"])
  }

  // ============================================
  // STEP 6: Build & CI docs
  // ============================================
  const ciDocs = {
    github: await findFirst([".github/workflows/"]),
    gitlab: await findFirst([".gitlab-ci.yml"]),
    circleci: await findFirst([".circleci/"]),
    jenkins: await findFirst(["Jenkinsfile", "jenkins/"]),
    travis: await findFirst([".travis.yml"]),
    azure: await findFirst(["azure-pipelines.yml"]),
    bitbucket: await findFirst(["bitbucket-pipelines.yml"]),
    drone: await findFirst([".drone.yml"]),
    taskfile: await findFirst(["Taskfile.yml", "Taskfile.yaml"])
  }

  // ============================================
  // STEP 7: Documentation infrastructure
  // ============================================
  const docInfra = {
    mkdocs: await findFirst(["mkdocs.yml"]),
    docusaurus: await findFirst(["docusaurus.config.js", "docusaurus.config.ts"]),
    sphinx: await findFirst(["docs/conf.py", "sphinx/"]),
    gitbook: await findFirst([".gitbook.yaml", "book.json"]),
    vuepress: await findFirst(["docs/.vuepress/"]),
    mdbook: await findFirst(["book.toml"]),
    hugo: await findFirst(["config.toml"]),  // Simplified
    jekyll: await findFirst(["_config.yml"]),
    typedoc: await findFirst(["typedoc.json"]),
    jsdoc: await findFirst(["jsdoc.json", "jsdoc.config.js"]),
    storybook: await findFirst([".storybook/"])
  }

  // ============================================
  // STEP 8: Database & migration docs
  // ============================================
  const dbDocs = {
    migrations: await findFirst(["migrations/", "alembic/", "db/migrate/", "prisma/migrations/"]),
    prisma: await findFirst(["prisma/schema.prisma"]),
    typeorm: await findFirst(["ormconfig.json", "ormconfig.js"]),
    sequelize: await findFirst([".sequelizerc"]),
    seeds: await findFirst(["seeds/", "seeders/", "db/seeds/"])
  }

  // ============================================
  // STEP 9: Diagrams & visual docs
  // ============================================
  const diagrams = {
    mermaid: (await Glob("**/*.{mmd,mermaid}")).length,
    plantuml: (await Glob("**/*.{puml,plantuml}")).length,
    drawio: (await Glob("**/*.drawio")).length,
    excalidraw: (await Glob("**/*.excalidraw")).length,
    docImages: (await Glob("docs/**/*.{png,svg,jpg,gif,webp}")).length
  }

  // ============================================
  // ANALYSIS: Summarize findings (counts only)
  // ============================================
  const analysis = {
    // docs/ directory summary
    docsDirectory: {
      exists: docsDir.exists,
      fileCount: docsDir.fileCount,
      subdirs: docsDir.subdirs  // ["api", "guides", "tutorials"] etc.
    },

    // Category scores as "found/total" strings
    categories: {
      core: `${countFound(rootDocs)}/${Object.keys(rootDocs).length}`,
      api: `${countFound(apiDocs)}/${Object.keys(apiDocs).length}`,
      config: `${countFound(configDocs)}/${Object.keys(configDocs).length}`,
      platform: `${countFound(platformDocs)}/${Object.keys(platformDocs).length}`,
      ci: `${countFound(ciDocs)}/${Object.keys(ciDocs).length}`,
      infrastructure: `${countFound(docInfra)}/${Object.keys(docInfra).length}`,
      database: `${countFound(dbDocs)}/${Object.keys(dbDocs).length}`,
      diagrams: sumValues(diagrams)
    },

    // Critical missing (based on project type)
    criticalMissing: detectCriticalMissing(rootDocs, apiDocs, project.type),

    // Total docs found
    totalFiles: docsDir.fileCount + countFound(rootDocs) + countFound(apiDocs) + countFound(configDocs)
  }

  // Return REFERENCES ONLY - no paths stored
  return {
    root: rootDocs,         // { readme: true, license: true, ... }
    api: apiDocs,           // { openapi: true, graphql: false, ... }
    config: configDocs,     // { envExample: true, ... }
    platform: platformDocs, // { codeowners: true, ... }
    ci: ciDocs,             // { github: true, gitlab: false, ... }
    infrastructure: docInfra,
    database: dbDocs,
    diagrams: diagrams,     // { mermaid: 3, plantuml: 0, ... }
    analysis: analysis
  }
}

// Recursive docs/ directory scan
async function scanDocsDirectory() {
  if (!await exists("docs/")) {
    return { exists: false, fileCount: 0, subdirs: [] }
  }

  const allFiles = await Glob("docs/**/*.{md,mdx,rst,txt,adoc,html}")
  const subdirs = [...new Set(
    allFiles
      .map(f => f.replace("docs/", "").split("/")[0])
      .filter(d => d && !d.includes("."))
  )]

  return {
    exists: true,
    fileCount: allFiles.length,
    subdirs: subdirs  // e.g., ["api", "guides", "architecture"]
  }
}

// Helper: Find first matching pattern, return path or null
async function findFirst(patterns) {
  for (const pattern of patterns) {
    if (pattern.includes("*")) {
      const matches = await Glob(pattern)
      if (matches.length > 0) return matches[0]  // Return first match path
    } else if (await exists(pattern)) {
      return pattern  // Return the path
    }
  }
  return null  // Not found
}

// Helper: Count non-null values in object
function countFound(obj) {
  return Object.values(obj).filter(v => v !== null && v !== false).length
}

// Helper: Sum numeric values
function sumValues(obj) {
  return Object.values(obj).reduce((a, b) => a + (typeof b === 'number' ? b : 0), 0)
}

// Helper: Detect critical missing docs based on project type
function detectCriticalMissing(rootDocs, apiDocs, projectType) {
  const critical = []

  // Universal requirements
  if (!rootDocs.readme) critical.push("README")
  if (!rootDocs.license) critical.push("LICENSE")

  // Type-specific requirements
  if (projectType.includes("api") || projectType.includes("library")) {
    if (!apiDocs.openapi && !apiDocs.graphql) {
      critical.push("API schema")
    }
  }
  if (projectType.includes("library") || projectType.includes("package")) {
    if (!rootDocs.changelog) critical.push("CHANGELOG")
  }
  if (projectType.includes("open-source")) {
    if (!rootDocs.contributing) critical.push("CONTRIBUTING")
  }

  return critical
}
```

### Documentation Output Schema (in detected.documentation)

**Format: Simple references (path as string if exists, null if not). No dynamic injection.**

```json
{
  "documentation": {
    "root": {
      "readme": "README.md",
      "license": "LICENSE",
      "changelog": null,
      "contributing": "CONTRIBUTING.md",
      "codeOfConduct": null,
      "security": null,
      "support": null,
      "authors": "AUTHORS.md",
      "acknowledgments": null
    },
    "api": {
      "openapi": "openapi.yaml",
      "graphql": null,
      "asyncapi": null,
      "postman": null,
      "grpc": "api/service.proto",
      "jsonSchema": null
    },
    "config": {
      "envExample": ".env.example",
      "editorconfig": ".editorconfig",
      "dockerCompose": "docker-compose.yml",
      "makefile": "Makefile"
    },
    "platform": {
      "codeowners": "CODEOWNERS",
      "prTemplate": ".github/PULL_REQUEST_TEMPLATE.md",
      "issueTemplates": ".github/ISSUE_TEMPLATE/",
      "workflows": ".github/workflows/",
      "dependabot": ".github/dependabot.yml"
    },
    "ci": {
      "github": ".github/workflows/",
      "gitlab": null,
      "jenkins": null
    },
    "infrastructure": {
      "mkdocs": null,
      "docusaurus": "docusaurus.config.js",
      "typedoc": "typedoc.json",
      "storybook": ".storybook/"
    },
    "database": {
      "migrations": "prisma/migrations/",
      "prisma": "prisma/schema.prisma",
      "seeds": null
    },
    "diagrams": {
      "mermaid": 3,
      "plantuml": 0,
      "drawio": 1,
      "docImages": 12
    },
    "analysis": {
      "docsDirectory": {
        "exists": true,
        "fileCount": 24,
        "subdirs": ["api", "guides", "architecture"]
      },
      "categories": {
        "core": "6/9",
        "api": "2/7",
        "config": "4/5",
        "platform": "5/7",
        "ci": "1/9",
        "infrastructure": "2/11",
        "database": "2/5",
        "diagrams": 16
      },
      "criticalMissing": ["CHANGELOG", "SECURITY"],
      "totalFiles": 30
    }
  }
}
```

**Key principle:** Path stored as-is when found, `null` when not found. No template variables, no injection format.

---

### What This Agent Does NOT Do

- ❌ Write files
- ❌ Create directories
- ❌ Modify any project files
- ❌ Ask questions (questions are asked by tune command in parallel)

### What This Agent Does

- ✅ Read manifests, configs, source files
- ✅ Detect languages, frameworks, patterns
- ✅ **Detect ALL documentation types (50+ file patterns)**
- ✅ Infer team/data/priority from code analysis
- ✅ Return structured JSON data
