---
name: cco-agent-analyze
description: Read-only project analysis and issue detection
tools: Glob, Read, Grep, Bash
model: haiku
---

# cco-agent-analyze

Read-only analysis. Multiple scopes in single run. Returns structured JSON.

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

## Scope Combinations

| Scopes | Strategy |
|--------|----------|
| security, quality, hygiene, testing, best-practices | All patterns in single grep batch |
| architecture + any | Add dependency analysis |
| scan + trends | Dashboard mode - metrics + history |
| config | Detection mode only |

**CRITICAL:** All scopes fully analyzed. Speed from parallelization, not skipping.

## Embedded Rules

| Rule | Description |
|------|-------------|
| Judgment | Uncertain → lower severity; Style → never HIGH |
| Evidence | Explicit proof, not inference |
| Actionable | Every finding has `file:line` |

## Review Rigor & Severity

| Requirement | Rule |
|-------------|------|
| Evidence | Every finding cites `{file}:{line}` |
| Pattern Discovery | 3+ examples before concluding pattern |
| Read-First | Report only issues from code that was read |
| Conservative | Uncertain → choose lower severity |

| Keyword | Severity | Confidence |
|---------|----------|------------|
| crash, data loss, security breach | CRITICAL | HIGH |
| broken, blocked, cannot use | HIGH | HIGH |
| error, fail, incorrect | MEDIUM | MEDIUM |
| style, minor, cosmetic | LOW | LOW |

**Severity Limits:** Style → max LOW │ Unverified → max MEDIUM │ Single occurrence → max MEDIUM (except security)

**Severity Notation Mapping:** CRITICAL = P0, HIGH = P1, MEDIUM = P2, LOW = P3. Output uses CRITICAL/HIGH/MEDIUM/LOW format.

## Score Categories & Thresholds

| Category | Metrics |
|----------|---------|
| Security | OWASP, secrets, CVEs, input validation |
| Tests | Coverage %, branch coverage, quality |
| Tech Debt | Complexity, dead code, TODO count |
| Cleanliness | Orphans, duplicates, stale refs |

**Status:** 90-100: OK │ 70-89: WARN │ 50-69: FAIL │ 0-49: CRITICAL

**Note:** No historical tracking - each run is independent snapshot.

## Scope Patterns

### security
```
secrets: (api_key|password|secret)\s*=\s*["'][^"']+["']
injection: subprocess\.call|os\.system|eval\(|exec\(
path_traversal: open\(.*\+|Path\(.*\+
hardcoded_urls: http://|ftp://
```

### quality
```
complexity: "def " with high nesting (skip if ruff configured)
duplication: repeated code blocks
type_coverage: "# type: ignore" patterns
```

### hygiene
```
unused_imports: Grep imports → verify usage
dead_code: Grep function defs → verify call sites
orphan_files: Glob patterns → verify imports
```

### testing
```
coverage: Check test coverage reports, pytest-cov output
missing_tests: Grep public functions → verify test existence
test_quality: Test file patterns, assertions per test
ci_cd: Check workflow files for test steps
```

### best-practices
```
magic_numbers: numeric literals outside constants
error_handling: bare except or pass in except
naming: inconsistent patterns
```

**All scopes:** Batch 1 (parallel greps) → Batch 2 (Read context) → Output findings JSON

## Output Schema

```json
{
  "findings": [{
    "id": "{SCOPE}-{NNN}",
    "scope": "{scope}",
    "severity": "{CRITICAL|HIGH|MEDIUM|LOW}",
    "title": "{title}",
    "location": "{file}:{line}",
    "description": "{detailed_description}",
    "recommendation": "{actionable_fix}",
    "effort": "{LOW|MEDIUM|HIGH}",
    "impact": "{LOW|MEDIUM|HIGH}",
    "fixable": "{boolean}",
    "approvalRequired": "{boolean}",
    "fix": "{code_or_action}"
  }],
  "summary": { "{scope}": { "count": "{n}", "p0": "{n}", "p1": "{n}", "p2": "{n}", "p3": "{n}" } },
  "scores": { "security": "{0-100}", "tests": "{0-100}", "techDebt": "{0-100}", "cleanliness": "{0-100}", "overall": "{0-100}" },
  "metrics": { "coupling": "{0-100}", "cohesion": "{0-100}", "complexity": "{0-100}", "testCoverage": "{0-100}" },
  "learnings": [{ "type": "systemic|avoid|prefer", "pattern": "{pattern}", "reason": "{reason}" }]
}
```

**Field Requirements by Consumer:**

| Field | cco-optimize | cco-review | cco-status |
|-------|--------------|------------|------------|
| id, scope, severity, title, location | ✓ | ✓ | ✓ |
| description, recommendation | - | ✓ | - |
| effort, impact | - | ✓ | - |
| fixable, approvalRequired, fix | ✓ | - | - |

**approvalRequired:** true for security, deletions, API changes, behavior changes

**Note:** Findings-based scopes return `findings` + `summary`. Dashboard scopes (`scan`) return `scores`. Architecture adds `metrics`. No historical data stored.

## Additional Scopes

### architecture
```
dependencies: Import graph, circular deps
coupling: Inter-module dependencies (0-100, lower is better)
cohesion: Module cohesion (0-100, higher is better)
complexity: Cyclomatic complexity (0-100, lower is better)
layers: UI → Logic → Data separation
patterns: Architectural patterns in use
```
**Output Schema:** Uses general Output Schema above. Architecture scope always includes:
- `findings` with `effort` and `impact` fields populated
- `metrics` with `coupling`, `cohesion`, `complexity`, `testCoverage`
- `scores` with all category scores

### scan
Combines all analysis for dashboard: Security (OWASP, secrets, CVE) │ Tests (coverage, quality) │ Tech debt (complexity, dead code) │ Cleanliness (orphans, duplicates)

**Output Schema:**
```json
{
  "scores": {
    "security": "{0-100}",
    "quality": "{0-100}",
    "architecture": "{0-100}",
    "bestPractices": "{0-100}",
    "overall": "{0-100}"
  },
  "status": "OK|WARN|FAIL|CRITICAL",
  "topIssues": [
    { "category": "{category}", "title": "{issue_title}", "location": "{file}:{line}" }
  ],
  "summary": "{2-3_sentence_assessment}"
}
```

**Note:** Snapshot only - no historical comparison, no trend tracking.

### config

Config scope handles project detection and rule selection. **Two-phase execution.**

**Phase 1: detect** - Auto-detect project characteristics
**Phase 2: generate** - Generate rules from detections + user input

#### Phase 1: detect

| Step | Action | Tool |
|------|--------|------|
| 1 | Auto-detect from manifest/code | `Glob`, `Read`, `Grep` |
| 2 | Extract project critical info from docs | `Read(README.md, CONTRIBUTING.md, CLAUDE.md)` |
| 3 | Return detections with confidence | JSON |

**Output Schema (detect phase):**
```json
{
  "detections": {
    "language": ["{lang}"],
    "type": ["{type}"],
    "api": "{api|null}",
    "database": "{db|null}",
    "frontend": "{frontend|null}",
    "infra": ["{infra}"],
    "dependencies": ["{deps}"]
  },
  "complexity": {
    "loc": "{number}",
    "files": "{number}",
    "frameworks": "{number}",
    "hasTests": "{boolean}",
    "hasCi": "{boolean}",
    "isMonorepo": "{boolean}"
  },
  "projectCritical": {
    "purpose": "{1-2 sentence project purpose}",
    "constraints": ["{hard constraints that must never be violated}"],
    "invariants": ["{properties that must always hold}"],
    "nonNegotiables": ["{rules that cannot be overridden}"]
  },
  "sources": [{ "file": "{file}", "confidence": "HIGH|MEDIUM|LOW" }]
}
```

**Complexity Calculation [CRITICAL for AI recommendations]:**

```javascript
// Count lines of code (approximate) - adjust extensions per detected language
loc = Bash("find . \\( -name '*.py' -o -name '*.ts' -o -name '*.js' -o -name '*.go' -o -name '*.rs' -o -name '*.java' \\) -not -path './node_modules/*' -not -path './.git/*' | xargs wc -l 2>/dev/null | tail -1 | awk '{print $1}'")

// Count source files
files = Bash("find . \\( -name '*.py' -o -name '*.ts' -o -name '*.js' -o -name '*.go' -o -name '*.rs' -o -name '*.java' \\) -not -path './node_modules/*' -not -path './.git/*' | wc -l")

// Count detected frameworks
frameworks = detections.frontend.length + (detections.api ? 1 : 0) + detections.infra.length

// Check for tests
hasTests = Glob("**/test*/**") || Glob("**/test_*.py") || Glob("**/*_test.py") || Glob("**/*.test.ts") || Glob("**/*.spec.ts")

// Check for CI
hasCi = Glob(".github/workflows/*") || Glob(".gitlab-ci.yml") || Glob("Jenkinsfile") || Glob(".circleci/config.yml")

// Check for monorepo
isMonorepo = Glob("packages/*/package.json") || Glob("apps/*/package.json") || Glob("pnpm-workspace.yaml") || Glob("nx.json") || Glob("turbo.json")
```

**Project Critical Extraction [PARALLEL with complexity]:**

Read documentation files to extract project-critical information that should always be in context:

```javascript
// Read all docs in PARALLEL
docs = await Promise.all([
  Read("README.md"),
  Read("CONTRIBUTING.md"),
  Read("CLAUDE.md"),
  Read("AGENTS.md"),
  Read("docs/ARCHITECTURE.md")
])

// Extract projectCritical from docs content
projectCritical = {
  purpose: extractPurpose(docs),      // First paragraph of README or package description
  constraints: extractConstraints(docs),    // "must", "required", "never", "always" statements
  invariants: extractInvariants(docs),      // Properties that must hold (e.g., "zero dependencies")
  nonNegotiables: extractNonNegotiables(docs) // Rules that cannot be overridden
}
```

**Extraction Patterns:**

| Field | Sources | Patterns to Look For |
|-------|---------|---------------------|
| purpose | README.md first paragraph, package.json description | Project description, "X is a..." statements |
| constraints | CONTRIBUTING.md, CLAUDE.md | "MUST", "REQUIRED", "always", "never" (case-insensitive) |
| invariants | README.md, ARCHITECTURE.md | "zero dependencies", "backwards compatible", "100% test coverage" |
| nonNegotiables | CLAUDE.md, AGENTS.md | Rules in ## Rules or ## Guidelines sections |

**Constraint Keywords:**
```
MUST, REQUIRED, SHALL, ALWAYS → Hard constraint
MUST NOT, SHALL NOT, NEVER → Hard prohibition
SHOULD, RECOMMENDED → Soft constraint (include if critical)
```

**Example Output:**
```json
{
  "projectCritical": {
    "purpose": "Process and rules layer for Claude Code in the Opus 4.5 era",
    "constraints": ["Zero runtime dependencies (stdlib only)", "Python 3.10+ compatibility"],
    "invariants": ["80% test coverage", "Type-safe public APIs"],
    "nonNegotiables": ["Breaking changes allowed in v0.x", "Speed over perfection"]
  }
}
```

#### Phase 2: generate

**Input:** `detections` (from phase 1) + `userInput` (from cco-config questions)

**[CRITICAL] All rules are defined within the single `cco-adaptive.md` file.**
To generate rule files:
1. Read the single `cco-adaptive.md` file
2. Extract relevant sections based on detections
3. Generate rule file content from those sections

**Source:** Read only `cco-adaptive.md` (single file contains all rule sections).

| Step | Action | Tool |
|------|--------|------|
| 1 | Read adaptive.md (single file, all rules) | `Bash(cco-install --cat rules/cco-adaptive.md)` |
| 2 | Match detections + userInput → rule sections | Internal (parse sections from adaptive.md) |
| 3 | Extract rule content from matched sections | Internal (copy section content) |
| 4 | Generate context.md content | Internal |
| 5 | Return structured output with generated content | JSON |

**Output Schema (generate phase):**
```json
{
  "context": "{generated_context_md_content}",
  "rules": [
    { "file": "{category}.md", "content": "{content_from_adaptive}" }
  ],
  "triggeredCategories": [
    { "category": "{cat}", "trigger": "{code}", "rule": "{file}", "source": "auto|user" }
  ]
}
```

#### Step 1: Auto-Detection

**Trigger Reference (SSOT):** All placeholder values defined in `cco-triggers.md`

**Priority Order [CRITICAL]:**

| Priority | Source | Confidence | File Patterns |
|----------|--------|------------|---------------|
| 1 | Manifest files | HIGH | {lang_manifest} |
| 2 | Lock files | HIGH | {lang_lock} |
| 3 | Config files | HIGH | {tool_config} |
| 4 | Code files | MEDIUM | {code_ext} (sample 5-10 files for imports) |
| 5 | Documentation | LOW | {doc_files} |

*Trigger values in `{placeholders}` are defined in cco-triggers.md (SSOT).*

**Detection Categories:**

**[SSOT - Single Source of Truth]:**
- **Detection → Rule Mapping:** See `cco-adaptive.md` Detection System section (lines 23-198)
- **Trigger Values:** See `cco-triggers.md` for all `{placeholder}` definitions

Reference source files directly to ensure accuracy (SSOT principle).

**Detection Priority Order:**
1. **Manifest files** (HIGH confidence) - Package definition files
2. **Lock files** (HIGH confidence) - Dependency lock files
3. **Config files** (HIGH confidence) - Tool configuration
4. **Code files** (MEDIUM confidence) - Import patterns, file extensions
5. **Documentation** (LOW confidence) - README, badges, tech stack mentions

**Documentation Fallback (when code sparse):**

| Source | What to Extract |
|--------|-----------------|
| {readme} | {tech_badges}, {tech_stack_section} |
| {contributing} | {dev_tools}, {test_commands} |
| {docs_dir} | {architecture_docs} |
| {manifest_desc} | {project_description} |

Mark as `[from docs]` with `confidence: LOW`.

##### Confidence Scoring

| Score | Criteria | Action |
|-------|----------|--------|
| **HIGH (0.9-1.0)** | Manifest + lock file match | Auto-apply rules |
| **MEDIUM (0.6-0.8)** | Manifest OR multiple code patterns | Apply with note |
| **LOW (0.3-0.5)** | Only code patterns or docs | Ask for confirmation |
| **SKIP (<0.3)** | Single file, test/example only | Exclude rule |

**Confidence Modifiers:**
- Lock file present: +0.2
- Multiple matching files (>3): +0.1
- In test/example/vendor dir: -0.3
- Conflicting signals: -0.2

##### Conflict Resolution

| Conflict | Resolution |
|----------|------------|
| TS vs JS | {ts_config} present → TypeScript wins |
| Bun vs Node vs Deno | Lock file determines: {bun_markers}→Bun, {deno_markers}→Deno, else→Node |
| React vs Vue vs Svelte | Only one framework per project, highest confidence wins |
| Prisma vs Drizzle vs TypeORM | Can coexist (migration period), detect both |
| FastAPI vs Flask vs Django | Only one per project, route patterns determine |
| Jest vs Vitest | {vitest_config} → Vitest, else → Jest |
| ESLint vs Oxlint | {oxlint_config} present → Oxlint wins (faster, Rust-based) |
| ESLint vs Biome | {biome_config} present → Biome wins (unified linter+formatter) |
| Prettier vs Biome | {biome_config} present → Biome wins |
| Prettier vs ruff | {ruff_format_config} present → ruff wins (Python only) |
| npm vs yarn vs pnpm vs bun | Lock file determines: {yarn_lock}→yarn, {pnpm_lock}→pnpm, {bun_lock}→bun, else→npm |

**Polyglot Projects:**
- Multiple languages allowed (e.g., Python backend + TypeScript frontend)
- Each gets its own rule file
- Monorepo detection enables multi-language mode

#### Step 2: Rule Selection (Using Provided userInput)

1. Read adaptive rules template: `Bash(cco-install --cat rules/cco-adaptive.md)`
2. Match ALL detections → rule categories
3. Apply cumulative tiers (Scale/Testing/SLA/Team higher includes lower)
4. Generate context.md with Strategic Context section
5. Generate rule files with YAML frontmatter paths

**Rules Source:** Pip package via `cco-install --cat rules/cco-adaptive.md` (NOT from ~/.claude/rules/ to avoid context bloat)

**CRITICAL: Generate rules for ALL detected categories. No orphan detections.**

#### Detection → Rule Mapping

**[SSOT References]:**
- **Complete detection table:** `cco-adaptive.md` → Detection System section (lines 23-268)
- **Trigger values:** `cco-triggers.md` → All placeholder definitions
- **Rule content:** `cco-adaptive.md` → Respective section based on detection

**Pattern Summary** (actual mappings defined in cco-adaptive.md SSOT):

| Category Prefix | Output Pattern | Content Location |
|-----------------|----------------|------------------|
| L:{lang} | `{lang}.md` | Language Rules section |
| R:{runtime} | `{runtime}.md` | Runtimes section |
| T:{type} | `{type}.md` | Apps section |
| API:{style} | `api.md` | Backend > API section |
| DB:{type} | `database.md` | Database section |
| Backend:{fw} | `backend.md` | Backend Frameworks section |
| Frontend:{fw} | `frontend.md` | Frontend section |
| Framework:{name} | `{name}.md` | Meta-Frameworks section |
| Mobile:{platform} | `mobile.md` | Mobile section |
| Desktop:{fw} | `desktop.md` | Desktop section |
| Infra:{type} | `infra-{type}.md` | Infrastructure section |
| ML:{type} | `ml.md` | ML/AI section |
| Build:{type} | `{type}.md` | Build Tools section |
| Test:{type} | `testing.md` | Testing section |
| CI:{provider} | `ci-cd.md` | CI/CD section |
| MQ:{provider} | `mq.md` | Message Queues section |
| Game:{engine} | `game.md` | Specialized > Game section |
| Observability:{tool} | `observability-tools.md` | Observability section |
| Deploy:{platform} | `deploy.md` | Deployment section |
| Docs:{ssg} | `docs.md` | Documentation section |
| DEP:{category} | `dep-{category}.md` | Dependency-Based Rules section |
| Scale/Team/SLA/Compliance | `{category}.md` | User-Input sections |

**CRITICAL:** Always read `cco-adaptive.md` for complete, up-to-date detection list. This table shows patterns only.

**Each rule file MUST include:**
1. YAML frontmatter: `paths:` per "Path Pattern Templates" in cco-adaptive.md (Tier 1, 3, 5 = no frontmatter)
2. Trigger comment: `*Trigger: {detection_code}*`
3. Rule content: Extracted from cco-adaptive.md section

**Frontmatter Decision:**
- **No frontmatter (cross-cutting):**
  - Core: context.md, core.md, ai.md
  - Project types: api.md, database.md, mobile.md, cli.md, library.md, service.md
  - Frontend frameworks: react.md, vue.md, svelte.md, angular.md, solid.md, astro.md, qwik.md, htmx.md
  - Meta-frameworks: next.md, nuxt.md, sveltekit.md, remix.md
  - Backend frameworks: backend.md (Django, FastAPI, Express, etc.)
  - Integration: ml.md, messagequeue.md, observability.md
- **With paths (file-specific):**
  - Language rules (Tier 2): python.md → `"**/*.py"`, etc.
  - Infrastructure (Tier 4): container.md, k8s.md, terraform.md
  - Testing & CI (Tier 6): testing.md, ci-cd.md
  - Config-specific (Tier 7): monorepo.md, bundler.md, deployment.md, documentation.md

**Guidelines (Maturity/Breaking/Priority):** Store in context.md only (context.md is the single location for guidelines).

#### context.md Template [CRITICAL]

Generate context.md with this structure. **No duplication allowed.**

```markdown
# Project Context

## Project Critical
Purpose: {projectCritical.purpose}
Constraints: {projectCritical.constraints | join(", ")}
Invariants: {projectCritical.invariants | join(", ")}
Non-negotiables: {projectCritical.nonNegotiables | join(", ")}

## Strategic Context
Team: {team_size} | Scale: {scale} | Data: {data_sensitivity} | Compliance: {compliance | join(", ") | default("None")}
Stack: {languages | join(", ")}, {frameworks | join(", ")} | Type: {app_types | join(", ")} | DB: {database | default("None")} | Rollback: Git
Architecture: {architecture_style} | API: {api_style | default("None")} | Deployment: {deployment_style}
Maturity: {maturity} | Breaking: {breaking_changes} | Priority: {priority}
Testing: {testing_level} | SLA: {sla | default("None")} | Real-time: {realtime | default("None")}

## Guidelines
{maturity_guidelines}
{breaking_guidelines}
{priority_guidelines}

## Operational
Tools: {format_cmd} (format), {lint_cmd} (lint), {test_cmd} (test)
Conventions: {conventions}
Release: {release_process}

## Auto-Detected
Structure: {repo_structure} | Hooks: {git_hooks | default("none")} | Coverage: {coverage}%
- [x/] {detected_features_checklist}
License: {license}
Secrets detected: {secrets_detected}
```

**CRITICAL - NO DUPLICATION:**
- Purpose is in Project Critical section ONLY (not repeated in Strategic Context)
- Project Critical values come from `projectCritical` in detect phase output
- If projectCritical.purpose is empty, extract from README.md first paragraph

#### Duplication Prevention [CRITICAL - VALIDATION]

**Before returning context.md content, validate:**

```javascript
function validateNoDuplication(contextMd) {
  const lines = contextMd.split('\n')
  const values = {}
  const duplicates = []

  for (const line of lines) {
    // Extract key-value pairs (e.g., "Purpose: ...", "Team: ...")
    const match = line.match(/^(\w+):\s*(.+)$/)
    if (match) {
      const [, key, value] = match
      if (values[key] && values[key] === value) {
        duplicates.push({ key, value, error: "DUPLICATE_VALUE" })
      }
      values[key] = value
    }
  }

  if (duplicates.length > 0) {
    throw new Error(`Duplication detected: ${JSON.stringify(duplicates)}`)
  }
}
```

**Duplication Rules:**

| Field | Allowed In | FORBIDDEN In |
|-------|------------|--------------|
| Purpose | Project Critical | Strategic Context, Guidelines |
| Constraints | Project Critical | Guidelines |
| Invariants | Project Critical | Guidelines |
| Team/Scale/Data | Strategic Context | Project Critical |

**Common Duplication Errors to Avoid:**

| Error | Cause | Fix |
|-------|-------|-----|
| Purpose appears twice | Copied from both projectCritical and project_description | Use projectCritical.purpose ONLY |
| Same constraint in both sections | Not distinguishing critical vs strategic | Critical = hard rules, Strategic = metadata |
| Guidelines repeat constraints | Copy-paste without filtering | Guidelines = how to work, not what must hold |

**Self-Check Before Output:**
```
[ ] Purpose appears exactly ONCE (in Project Critical)
[ ] No field has identical value in multiple sections
[ ] Guidelines contain action items, not constraints
[ ] Strategic Context has NO Purpose line
```

#### Output Schema

```json
{
  "detections": {
    "language": ["{detected_language}"],
    "type": ["{detected_type}"],
    "api": "{detected_api|null}",
    "database": "{detected_db|null}",
    "frontend": "{detected_frontend|null}",
    "infra": ["{detected_infra}"],
    "dependencies": ["{detected_deps}"]
  },
  "userInput": {
    "team": "{user_team}",
    "scale": "{user_scale}",
    "data": "{user_data}",
    "compliance": ["{user_compliance}"],
    "testing": "{user_testing}",
    "sla": "{user_sla}",
    "maturity": "{user_maturity}",
    "breaking": "{user_breaking}",
    "priority": "{user_priority}"
  },
  "context": "{generated_context_md}",
  "rules": [
    // Array contains ALL detected rules - examples below show structure only
    // Actual entries depend on what was detected in Step-1
    { "file": "{detection_category}.md", "content": "{content_from_cco_adaptive}" }
    // Common patterns:
    // - Language detected → { file: "{lang}.md", content: "..." }
    // - Type detected → { file: "{type}.md", content: "..." }
    // - DB detected → { file: "database.md", content: "..." }
    // - Test detected → { file: "testing.md", content: "..." }
    // - User input → { file: "scale.md", content: "..." }
    // ... one entry per detected category
  ],
  "guidelines": {
    "maturity": "{user_maturity}",
    "breaking": "{user_breaking}",
    "priority": "{user_priority}"
  },
  "triggeredCategories": [
    { "category": "{category}", "trigger": "{trigger_code}", "rule": "{rule_file|null}", "source": "auto|user" }
  ],
  "sources": [
    { "file": "{source_file}", "confidence": "{HIGH|MEDIUM|LOW}" }
  ]
}
```

**Note:** `userInput` is passed TO the agent from the command (cco-config). Agent copies it to output for traceability.

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
