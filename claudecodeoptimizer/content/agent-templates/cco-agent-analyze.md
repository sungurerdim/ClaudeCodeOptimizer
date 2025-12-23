---
name: cco-agent-analyze
description: Read-only project analysis and issue detection
tools: Glob, Read, Grep, Bash
safe: true
model: haiku
---

# Agent: Analyze

Read-only analysis. Multiple scopes in single run. Returns structured JSON.

**Model:** Haiku (fast, read-only operations)

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

**Skip:** `.git/`, `node_modules/`, `vendor/`, `.venv/`, `dist/`, `build/`, `__pycache__/`, `*.min.*`

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
| No Speculation | Never report issues in unread code |
| Conservative | Uncertain → choose lower severity |

| Keyword | Severity | Confidence |
|---------|----------|------------|
| crash, data loss, security breach | CRITICAL | HIGH |
| broken, blocked, cannot use | HIGH | HIGH |
| error, fail, incorrect | MEDIUM | MEDIUM |
| style, minor, cosmetic | LOW | LOW |

**Prohibited:** Style → never CRITICAL/HIGH │ Unverified → never above MEDIUM │ Single occurrence → never CRITICAL unless security

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
  "findings": [{ "id": "{SCOPE}-{NNN}", "scope": "...", "severity": "{P0-P3}", "title": "...", "location": "{file}:{line}", "fixable": true, "approvalRequired": true, "fix": "..." }],
  "summary": { "{scope}": { "count": "{n}", "p0": "{n}", "p1": "{n}", "p2": "{n}", "p3": "{n}" } },
  "scores": { "security": "{0-100}", "tests": "{0-100}", "techDebt": "{0-100}", "cleanliness": "{0-100}", "overall": "{0-100}" },
  "metrics": { "coupling": "{0-100}", "cohesion": "{0-100}", "complexity": "{0-100}" },
  "learnings": [{ "type": "systemic|avoid|prefer", "pattern": "...", "reason": "..." }]
}
```

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
**Output Schema:**
```json
{
  "findings": [{ "id": "{SCOPE}-{NNN}", "scope": "architecture", "severity": "{P0-P3}", "title": "...", "location": "{file}:{line}", "description": "...", "recommendation": "...", "effort": "{LOW|MEDIUM|HIGH}", "impact": "{LOW|MEDIUM|HIGH}" }],
  "metrics": {
    "coupling": "{0-100}",
    "cohesion": "{0-100}",
    "complexity": "{0-100}"
  },
  "scores": {
    "security": "{0-100}",
    "tests": "{0-100}",
    "techDebt": "{0-100}",
    "cleanliness": "{0-100}",
    "overall": "{0-100}"
  }
}
```

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
| 2 | Return detections with confidence | JSON |

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
  "sources": [{ "file": "{file}", "confidence": "HIGH|MEDIUM|LOW" }]
}
```

#### Phase 2: generate

**Input:** `detections` (from phase 1) + `userInput` (from cco-config questions)

**[CRITICAL] Rule files do NOT exist as separate files in the CCO package.**
All rules are defined as sections within `cco-adaptive.md`. You must:
1. Read the single `cco-adaptive.md` file
2. Extract relevant sections based on detections
3. Generate rule file content from those sections

**NEVER try to read separate `{category}.md` files from CCO package - they don't exist.**

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

Do NOT duplicate these tables here. Read from source files to ensure accuracy.

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
| **SKIP (<0.3)** | Single file, test/example only | Don't apply |

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

| Category | Detection Pattern | Rule File | Content Source in cco-adaptive.md |
|----------|-------------------|-----------|-----------------------------------|
| Language | L:{lang} | `{lang}.md` | Language Rules → {Lang} section |
| Runtime | R:{runtime} | `{runtime}.md` | Runtimes section |
| App Type | T:{type} | `{type}.md` | Apps > {Type} section |
| API | API:{style} | `api.md` | Backend > API section |
| Database | DB:{type} | `database.md` | Backend > Data section |
| Backend | Backend:{fw} | `backend.md` | Backend Frameworks section |
| Frontend | Frontend:{fw} | `frontend.md` | Frontend section |
| Framework | Framework:{name} | `{name}.md` | Meta-Frameworks section |
| Mobile | Mobile:{platform} | `mobile.md` | Apps > Mobile section |
| Desktop | Desktop:{fw} | `desktop.md` | Apps > Desktop section |
| Infra | Infra:{type} | `{type}.md` | Infrastructure section |
| ML/AI | ML:{type} | `ml.md` | ML/AI section |
| Build | Build:{type} | `{type}.md` | Build Tools section |
| Testing | Test:{type} | `testing.md` | Testing Rules section |
| CI/CD | CI:{provider} | `ci-cd.md` | CI/CD section |
| MQ | MQ:{provider} | `mq.md` | Message Queues section |
| ORM | ORM:{orm} | `orm.md` | ORM-specific rules (Exposed, etc.) |
| Game | Game:{engine} | `game.md` | Specialized > Game section |
| RT | RT:{level} | `realtime.md` | Real-time section |
| i18n | i18n | `i18n.md` | i18n section |
| Observability | Observability:{tool} | `observability-tools.md` | Observability Tools section |
| Deploy | Deploy:{platform} | `deploy.md` | Deployment Platforms section |
| Docs | Docs:{ssg} | `docs.md` | Documentation Generators section |
| User:Scale | Scale:{tier} | `scale.md` | Scale Rules section |
| User:Team | Team:{size} | `team.md` | Team Rules section |
| User:Security | Data:PII/Regulated | `security.md` | Security Rules section |
| User:Compliance | Compliance:{std} | `compliance.md` | Compliance Rules section |
| User:SLA | SLA:{level} | `observability.md` | Observability Rules section |
| Dependency | DEP:{category} | `dep-{category}.md` | Dependency-Based Rules section |

**Each rule file MUST include:**
1. YAML frontmatter: `paths:` matching relevant files
2. Trigger comment: `*Trigger: {detection_code}*`
3. Rule content: Extracted from cco-adaptive.md section

**Guidelines (Maturity/Breaking/Priority):** Store in context.md only, don't generate rule files.

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
    { "category": "{category}", "trigger": "{trigger_code}", "rule": "{rule_file|null}", "source": "{auto|user|detected}" }
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
