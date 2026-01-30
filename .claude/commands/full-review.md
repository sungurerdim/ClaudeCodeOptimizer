---
description: CCO system health check (~130 checks across 10 categories)
argument-hint: [--auto] [--quick] [--focus=X] [--preview] [--fix]
allowed-tools: Read(*), Grep(*), Glob(*), Bash(*), Task(*), AskUserQuestion, Edit(*)
model: opus
---

# /full-review

**CCO Self-Review** - Comprehensive analysis of CCO system against its documented design principles.

> **Internal Command:** This is in `.claude/commands/` (not `commands/`), used for CCO development only.

## Args

- `--auto`: Fully unattended mode
  - **No questions asked** - analyze and fix everything
  - **No progress output** - silent execution
  - **Only final summary** - single status line at end
- `--quick`: CRITICAL and HIGH only, skip MEDIUM/LOW
- `--focus=X`: Single category (1-10 or name)
- `--preview`: Report only, no fixes applied
- `--fix`: Auto-apply safe fixes (doc count updates, terminology)

**Usage:**
- `/full-review` - Interactive mode with fix selection
- `/full-review --auto` - Silent full review and fix
- `/full-review --preview` - Report only
- `/full-review --quick --fix` - Fast check, auto-fix

## Context

- CCO repo root: !`git rev-parse --show-toplevel 2>/dev/null || echo ""`
- Is CCO repo: !`test -f .claude-plugin/plugin.json && grep -q '"name": "cco"' .claude-plugin/plugin.json && echo "1" || echo "0"`
- Args: $ARGS

## Context Check [CRITICAL]

If "Is CCO repo" returns "0":
```
Not in CCO repository root.
Run this command from the ClaudeCodeOptimizer directory.
```
**Stop immediately.**

## Mode Detection

```javascript
const args = "$ARGS"
const isUnattended = args.includes("--auto")
const isReportOnly = args.includes("--preview")

if (isUnattended) {
  // SILENT MODE: No questions, fix everything
  config = {
    action: "Fix all",
    focus: args.match(/--focus=(\w+)/)?.[1] || "all"
  }
  // → Jump directly to Step-2 analysis, skip Q1
}

if (isReportOnly) {
  config = { action: "Preview only", focus: "all" }
  // → Skip Q1, preview only
}
```

## No Deferrals Policy [CRITICAL]

When `--auto` or "Fix all" is selected:
- **Zero commentary** - No "this is complex", "needs refactor", "minor detail"
- **Zero deferrals** - No "consider later", "recommend manual", "outside scope"
- **Zero skips** - Every finding = FIXED or TECHNICAL FAILURE
- **Only technical failures** - File not found, parse error, permission denied

**See Core Rules:** `No Deferrals Policy` for forbidden responses and valid failure reasons.

## Architecture

| Step | Name | Action | Optimization |
|------|------|--------|--------------|
| 1 | Setup | Q1: Review mode selection | Single question |
| 2 | Inventory | Detect counts via Bash | Parallel Bash |
| 3 | Analyze | 10 Explore agents (parallel) | 10 agents in single message |
| 4 | Prioritize | 80/20 findings | Instant |
| 5 | Approval | Q2: Select fixes (conditional) | Only if needed |
| 6 | Apply | Delegate to cco-agent-apply | Agent handles batching |
| 7 | Summary | Show report | Instant |

**Key Optimization:** Step-3 launches ALL 10 category analyses as Explore agents in a single message = true parallel execution. Step-6 delegates to cco-agent-apply for efficient, verified fix application.

---

## Step-1: Setup [SKIP IF --auto or --preview]

```javascript
if (!isUnattended && !isReportOnly) {
  AskUserQuestion([{
    question: "How should this review proceed?",
    header: "Review mode",
    options: [
      { label: "Report only", description: "Analyze and show findings, no changes" },
      { label: "Fix safe (Recommended)", description: "Auto-fix doc counts, terminology, line endings" },
      { label: "Fix all", description: "Fix everything including manual items" }
    ],
    multiSelect: false
  }])

  // Store selection
  config.action = selectedOption  // "Report only" | "Fix safe" | "Fix all"
}
```

### Validation
- [x] User selected action mode
- → Store as: `config.action`
- → Proceed to Step-2

---

## Step-2: Inventory Detection

```javascript
// Parallel detection (relative paths - run from CCO repo root)
COMMANDS = Bash("ls ./commands/*.md 2>/dev/null | wc -l")
CORE_RULES = Bash("find ./rules/core -name 'cco-*.md' | wc -l")
LANG_RULES = Bash("find ./rules/languages -name 'cco-*.md' | wc -l")
FW_RULES = Bash("find ./rules/frameworks -name 'cco-*.md' | wc -l")
OPS_RULES = Bash("find ./rules/operations -name 'cco-*.md' | wc -l")
VERSION = Bash("grep '\"version\"' ./.claude-plugin/plugin.json | grep -oP '\\d+\\.\\d+\\.\\d+'")

// Store detected counts
inventory = {
  commands: parseInt(COMMANDS),  // Expected: 7 (optimize, align, preflight, commit, tune, research, docs)
  agents: 3,  // Fixed: cco-agent-analyze, cco-agent-apply, cco-agent-research
  coreRules: parseInt(CORE_RULES),
  langRules: parseInt(LANG_RULES),
  fwRules: parseInt(FW_RULES),
  opsRules: parseInt(OPS_RULES),
  totalRules: parseInt(CORE_RULES) + parseInt(LANG_RULES) + parseInt(FW_RULES) + parseInt(OPS_RULES),  // Expected: ~44
  version: VERSION
}
```

---

## Step-3: 10-Category Analysis [PARALLEL AGENTS]

**Use Explore agents for parallel category analysis:**

```javascript
// Create tasks for progress tracking
TaskCreate({ subject: "CCO Full Review", description: "10-category system health check" })

// Launch ALL category analyses in SINGLE message for true parallelism
// Explore agent: fast codebase search, pattern matching, keyword search

// BATCH 1: Structure & Quality (5 categories)
const cat1 = Task("Explore", `
  CCO Inventory & Sync check:
  1. Count files: commands/*.md, rules/core/cco-*.md, rules/languages/cco-*.md, rules/frameworks/cco-*.md, rules/operations/cco-*.md
  2. Compare counts to README.md, docs/commands.md, docs/agents.md, docs/rules.md
  3. Check for orphan refs: .cco/, principles.md, projects.json, context.md
  4. Verify terminology consistency: CRITICAL/HIGH/MEDIUM/LOW, OK/WARN/FAIL
  Return: { category: 1, passed: n, failed: n, findings: [...] }
`, { model: "haiku", run_in_background: true })

const cat2 = Task("Explore", `
  CCO Command Quality check:
  1. Verify Architecture tables in commands/*.md
  2. Check AskUserQuestion usage (no plain text questions)
  3. Verify fix workflow: Analyze → Report → Approve → Apply
  4. Check --auto and --preview mode consistency
  Return: { category: 2, passed: n, failed: n, findings: [...] }
`, { model: "haiku", run_in_background: true })

const cat3 = Task("Explore", `
  CCO Agent Quality check:
  1. Verify agent scopes in agents/cco-agent-*.md match docs/agents.md
  2. Check parallel execution patterns (single message for multiple Task calls)
  3. Verify output schemas (JSON with findings, metrics, status)
  Return: { category: 3, passed: n, failed: n, findings: [...] }
`, { model: "haiku", run_in_background: true })

const cat4 = Task("Explore", `
  CCO Rules System check:
  1. Verify detection triggers map to rules
  2. Check rule quality: actionable, unique names, placeholder format
  3. Verify /cco:tune produces cco-profile.md with required fields
  Return: { category: 4, passed: n, failed: n, findings: [...] }
`, { model: "haiku", run_in_background: true })

const cat5 = Task("Explore", `
  CCO Token Efficiency check:
  1. Tables > prose, lists > paragraphs
  2. No redundancy across files
  3. Profile auto-loaded from .claude/rules/
  4. Specification clarity: WHAT over HOW, Standards over Teaching
  Return: { category: 5, passed: n, failed: n, findings: [...] }
`, { model: "haiku", run_in_background: true })

// BATCH 2: Standards & Readiness (5 categories)
const cat6 = Task("Explore", `
  CCO UX/DX Standards check:
  1. Progress visibility for multi-step operations
  2. Error format: [SEVERITY] description in file:line
  3. Output formatting standards
  4. Pre-announce actions before execution
  Return: { category: 6, passed: n, failed: n, findings: [...] }
`, { model: "haiku", run_in_background: true })

const cat7 = Task("Explore", `
  CCO Documentation check:
  1. README accuracy vs detected counts
  2. docs/commands.md completeness
  3. docs/agents.md completeness
  4. docs/rules.md category coverage
  Return: { category: 7, passed: n, failed: n, findings: [...] }
`, { model: "haiku", run_in_background: true })

const cat8 = Task("Explore", `
  CCO Safety check:
  1. No secrets in code (API keys, passwords)
  2. OWASP compliance rules present
  3. Rollback capability (dirty warning, stash options)
  Return: { category: 8, passed: n, failed: n, findings: [...] }
`, { model: "haiku", run_in_background: true })

const cat9 = Task("Explore", `
  CCO Release Readiness check:
  1. Version consistency (plugin.json, CHANGELOG)
  2. Plugin structure (.claude-plugin/, hooks/)
  3. Cross-platform (forward slashes, no hardcoded paths, LF line endings)
  Return: { category: 9, passed: n, failed: n, findings: [...] }
`, { model: "haiku", run_in_background: true })

const cat10 = Task("Explore", `
  CCO Best Practices check:
  1. Positive rules ("Do X" not "Don't do Y")
  2. Model selection (opus for coding, haiku for analysis)
  3. Anti-overengineering (no BC hacks, no TODOs)
  4. Agent delegation patterns
  Return: { category: 10, passed: n, failed: n, findings: [...] }
`, { model: "haiku", run_in_background: true })

// ALL 10 agents launched in parallel - wait for results
const results = await Promise.all([
  TaskOutput(cat1.id), TaskOutput(cat2.id), TaskOutput(cat3.id),
  TaskOutput(cat4.id), TaskOutput(cat5.id), TaskOutput(cat6.id),
  TaskOutput(cat7.id), TaskOutput(cat8.id), TaskOutput(cat9.id),
  TaskOutput(cat10.id)
])

allFindings = results.flatMap(r => r.findings)
categoryResults = results.map(r => ({ category: r.category, passed: r.passed, failed: r.failed }))
```

**Key Optimization:** Single message with 10 Task calls = true parallel execution. Explore agents use Haiku model for fast, efficient searches.

---

## Category 1: Inventory & Sync (15 checks)

### 1.1 Dynamic Count Detection
```bash
COMMANDS=$(ls ./commands/*.md 2>/dev/null | wc -l)
CORE_RULES=$(find ./rules/core -name 'cco-*.md' | wc -l)
LANG_RULES=$(find ./rules/languages -name 'cco-*.md' | wc -l)
FW_RULES=$(find ./rules/frameworks -name 'cco-*.md' | wc -l)
OPS_RULES=$(find ./rules/operations -name 'cco-*.md' | wc -l)
# Store as session variables for later phases
```

### 1.2 Documentation Sync
Compare detected counts against:
- README.md (command count, agent count, rule counts)
- docs/commands.md (## /cco-* headers)
- docs/agents.md (## cco-agent-* headers)
- docs/rules.md (category breakdowns)

**Mismatch = HIGH** with auto-fix suggestion.

### 1.3 SSOT Compliance
- Rule uniqueness: grep rule names across files, count > 1 = HIGH
- Orphan detection: grep for `.cco/`, `principles.md`, `projects.json`, `context.md` = 0
- Deprecated refs: grep for `cco-tune`, `cco-setup`, `cco-help` (without /cco: prefix) = 0
- Legacy cleanup: grep for `cco-tools`, `cco-guide`, `cco-principles` = 0
- Command format: All command refs use `/cco:*` format (not `/optimize`) = HIGH

### 1.4 Dependency Chain
- Agent invocations use valid agent types = CRITICAL
- Scope parameters match agent capabilities = HIGH
- Commands delegate to /cco:tune --preview for profile validation = HIGH
- Input/output compatibility: agent outputs match consumer expectations = HIGH

### 1.5 Terminology Consistency
Cross-file terminology must match exactly:
- Severity terms: CRITICAL/HIGH/MEDIUM/LOW (not P0/P1/P2/P3 in user-facing)
- Status terms: OK/WARN/FAIL (consistent everywhere)
- Scope names: identical in agent definitions and docs
- Category names: identical in rules and docs
- Variable names: {placeholder} format consistent

**Mismatch = HIGH**

---

## Category 2: Command Quality (18 checks)

### 2.1 Template Compliance (IF PRESENT)
| Element | Check | Severity |
|---------|-------|----------|
| Architecture table | Correct `\| Step \| Name \| Action \|` format | HIGH |
| Validation blocks | Clear pass/fail criteria | MEDIUM |
| Context check | Commands needing context verify it exists | HIGH |
| Accounting | Fix commands report done/fail | HIGH |

**NOT findings:** Simple commands, short commands without architecture tables.

### 2.2 AskUserQuestion Standards
| Check | Requirement | Severity |
|-------|-------------|----------|
| Tool usage | Zero plain text questions (all via AskUserQuestion) | CRITICAL |
| MultiSelect | `multiSelect: true` for batch selections | HIGH |
| Option limits | Max 4 questions × max 4 options per call | MEDIUM |
| Overflow | Sequential calls for 5+ options | MEDIUM |
| All option | First option is "All ({n})" for batches | MEDIUM |
| Label order | `[current]` > `[detected]` > `(Recommended)` | LOW |
| Timing | Questions in early steps, not mid-execution | HIGH |
| Pre-action | Explanation precedes confirmation request | HIGH |
| Selection | Only user-selected items processed | CRITICAL |

### 2.3 Fix Workflow
Required flow: `Analyze → Report → Approve → Apply → Verify`

| Check | Requirement | Severity |
|-------|-------------|----------|
| Analysis first | Analyze precedes Apply | CRITICAL |
| Severity order | CRITICAL → HIGH → MEDIUM → LOW | MEDIUM |
| Granular selection | User can select individual fixes | HIGH |
| Before/after | Changes shown post-apply | MEDIUM |
| Accounting invariant | applied + failed = total | HIGH |
| Quality Gates | Only in /cco:commit and /cco:preflight (not /cco:optimize) | HIGH |

### 2.4 Mode Consistency
| Mode | Behavior | Severity |
|------|----------|----------|
| `--auto` | Zero AskUserQuestion calls, smart defaults | HIGH |
| `--preview` | Zero Edit/Write calls, preview only | HIGH |
| Mode parity | `--auto` quality equals interactive | MEDIUM |

---

## Category 3: Agent Quality (11 checks)

### 3.1 Scope Accuracy
Dynamically detect scopes from agent definitions, compare to docs/agents.md.

**Current Agent Scopes:**
- **cco-agent-analyze**: OPTIMIZE (security, hygiene, types, lint, performance, ai-hygiene, robustness, doc-sync) + REVIEW (architecture, patterns, testing, maintainability, ai-architecture, functional-completeness) + config + docs
- **cco-agent-apply**: fixes, config
- **cco-agent-research**: local, search, analyze, synthesize, full, dependency

| Check | Requirement | Severity |
|-------|-------------|----------|
| Analyze scopes | Documented = implemented (8 OPTIMIZE + 6 REVIEW) | HIGH |
| Apply scopes | Documented = implemented | HIGH |
| Research scopes | Documented = implemented (6 scopes) | HIGH |
| No overlap | ROB vs FUN clearly differentiated (code-level vs API-level) | MEDIUM |
| Description | Agent descriptions match behavior | HIGH |

### 3.2 Parallel Execution
| Check | Requirement | Severity |
|-------|-------------|----------|
| Single message | Multiple Task() in one assistant message | HIGH |
| Model selection | analyze/research = haiku, apply = opus | HIGH |
| Result merge | Parent combines agent outputs correctly | HIGH |
| Context prop | Agents receive profile from .claude/rules/ | MEDIUM |

### 3.3 Output Standards
Required schema:
```json
{
  "findings": [{ "severity": "{level}", "location": "{file}:{line}" }],
  "metrics": { "score": "{n}" },
  "status": "{OK|WARN|FAIL}"
}
```

| Check | Requirement | Severity |
|-------|-------------|----------|
| JSON format | Parseable output | CRITICAL |
| Severity field | Every finding has severity | HIGH |
| Location field | file:line where applicable | HIGH |
| Metrics | Analysis scopes return numeric metrics | MEDIUM |

---

## Category 4: Rules System (15 checks)

### 4.1 Detection Accuracy
| Detection | Trigger | Severity |
|-----------|---------|----------|
| Language | Manifest files (pyproject.toml, package.json) | CRITICAL |
| Framework | Dependency analysis | HIGH |
| Infrastructure | Config presence (Dockerfile, k8s/) | HIGH |
| Team/Scale | User input via AskUserQuestion | HIGH |

Checks:
- Every detection maps to 1+ rules = HIGH
- No orphan rules (every rule has trigger) = HIGH
- Cumulative tiers work (Large includes Medium + Small) = HIGH
- Detection coverage: all major languages/frameworks have rules = HIGH
- Multi-language support: Python, JS/TS, Go, Rust, Java covered = MEDIUM

### 4.2 Rule Quality
| Check | Requirement | Severity |
|-------|-------------|----------|
| Actionable | Contains specific action verb | HIGH |
| No overlap | Rule names unique across files | HIGH |
| Placeholders | Examples use `{placeholder}` format | MEDIUM |
| Positive | "Do X" not "Don't do Y" | MEDIUM |
| Concrete value | Each rule produces measurable benefit | HIGH |
| Verifiable | Rule compliance can be checked | MEDIUM |

### 4.3 Profile Generation
Auto-setup (via /cco:tune) must produce:

| Check | Requirement | Severity |
|-------|-------------|----------|
| Profile created | `.claude/rules/cco-profile.md` exists after setup | CRITICAL |
| Detections | project, stack, maturity, commands, patterns detected | HIGH |
| User choices | team, data, priority recorded (if interactive) | HIGH |
| Commands section | format, lint, type, test, build commands detected | HIGH |

---

## Category 5: Token Efficiency & Specification Clarity (22 checks)

### 5.1 Content Density
| Check | Requirement | Severity |
|-------|-------------|----------|
| Tables > prose | Tabular data uses `\|` format | MEDIUM |
| Lists > paragraphs | Multi-item uses bullets | LOW |
| Front-loading | Critical info in first 20% | MEDIUM |
| No redundancy | Zero identical content across files | HIGH |
| Large files | >500 lines referenced by path | MEDIUM |

### 5.2 Rule Format
| Check | Requirement | Severity |
|-------|-------------|----------|
| Single-line | Rules fit < 120 chars | LOW |
| Grouping | Rules under `###` headers | MEDIUM |
| No duplication | Unique across Core/AI/Adaptive | HIGH |

### 5.3 Command Efficiency
| Check | Requirement | Severity |
|-------|-------------|----------|
| Profile auto-loaded | Profile from .claude/rules/ via Claude auto-context | HIGH |
| Batch reads | Multiple Read() in single message | MEDIUM |
| Parallel agents | Independent analyses parallel | HIGH |
| Background tasks | Long operations use run_in_background: true | HIGH |
| Quick mode | Minimal output, haiku model | MEDIUM |

### 5.4 Specification Clarity [CRITICAL]

**Philosophy:** Claude knows software engineering. Don't teach HOW - specify WHAT you want and your STANDARDS. Let the model apply its expertise systematically.

**Three Pillars:**
1. **WHAT over HOW**: Define desired output, not implementation steps
2. **Standards over Teaching**: State thresholds/constraints, not rationale
3. **DRY for Policies**: Common patterns in Core Rules, commands reference them

#### 5.4.1 Output Specification
| Check | Requirement | Severity |
|-------|-------------|----------|
| I/O contract | Steps define Input → Output → Constraints | HIGH |
| Schema provided | JSON/object structure for complex outputs | HIGH |
| Success criteria | Clear definition of "done" | HIGH |
| No algorithm walkthrough | Zero if/else pseudocode for obvious logic | HIGH |

#### 5.4.2 Standards Declaration
| Check | Requirement | Severity |
|-------|-------------|----------|
| Thresholds only | Numeric limits without prose justification | MEDIUM |
| No academic rationale | Zero citations for industry standards | MEDIUM |
| Quality table | Metrics in table format, not paragraphs | MEDIUM |
| Severity defined | Clear CRITICAL/HIGH/MEDIUM/LOW criteria | HIGH |

#### 5.4.3 Policy Consolidation
| Check | Requirement | Severity |
|-------|-------------|----------|
| Core Rules reference | Repeated policies point to `CCO Operation Standards` | HIGH |
| No policy duplication | No Deferrals, Intensity, Accounting appear once | HIGH |
| Single definition | Each concept has exactly one authoritative source | HIGH |

**Good pattern:**
```markdown
## Step-2: Analysis
**Input:** File list from Step-1
**Output:** `{ findings: Finding[], metrics: Metrics }`
**Constraints:** Confidence >= 70, max 20 findings/scope, platform-specific excluded
**Policies:** See Core Rules > CCO Operation Standards
```

**Bad patterns:**
```markdown
// ❌ Teaching HOW (40 lines of pseudocode)
for (const file of files) {
  if (shouldAnalyze(file)) { ... }
}

// ❌ Academic justification
"Studies show >50% coupling leads to 2x bug rates (Fowler 1999)"

// ❌ Policy duplication
"AI never decides to skip..." (repeated in 4 files)
```

### 5.5 AskUserQuestion Limits
| Check | Requirement | Severity |
|-------|-------------|----------|
| Max 4 questions | Single AskUserQuestion call ≤4 questions | HIGH |
| Max 4 options | Each question ≤4 options (Other added auto) | HIGH |
| Scope grouping | 5+ scopes split into logical groups (Code Quality / Advanced) | HIGH |
| No overflow | Never truncate options - split across questions | CRITICAL |

### 5.6 Rule Optimization [CRITICAL]

**Philosophy:** Opus 4.5 knows software engineering. Rules should constrain/configure, not teach.

#### Rule Value Assessment
| Keep | Remove | Severity |
|------|--------|----------|
| Specific thresholds (complexity <15, timeout 30s) | Generic principles (DRY, SOLID, KISS) | HIGH |
| CCO-specific formats (`[SEVERITY] desc in file:line`) | Basic patterns (use async/await) | HIGH |
| Framework gotchas (Express error handler = 4 params) | How-to guides (how to use React hooks) | MEDIUM |
| Non-obvious constraints (SSRF IP blocklist) | OWASP explanations (what is XSS) | MEDIUM |
| Concrete values (bcrypt, argon2 for passwords) | General advice (use strong hashing) | HIGH |

#### Rule Optimization Checks
| Check | Requirement | Severity |
|-------|-------------|----------|
| No teaching | Rules don't explain basics Opus knows | HIGH |
| Threshold focus | Numeric limits > prose descriptions | MEDIUM |
| CCO-specific value | Each rule provides unique CCO value | HIGH |
| No duplication | Same concept not repeated across files | HIGH |
| Actionable | Every rule maps to detectable violation | MEDIUM |
| Table format | Structured data uses tables, not paragraphs | LOW |

#### Optimization Heuristics
```
IF rule explains something in Opus training data → REMOVE
IF rule is generic best practice → REMOVE or COMPRESS to threshold
IF rule has CCO-specific threshold/format → KEEP
IF rule documents non-obvious gotcha → KEEP
IF rule appears in multiple files → CONSOLIDATE to single source
```

**Good rule:** `Cyclomatic Complexity: 1-10 good, 11-15 review, 16+ refactor`
**Bad rule:** `Use meaningful variable names for better code readability`

---

## Category 6: UX/DX Standards (13 checks)

### 6.1 Progress Visibility
| Check | When Required | Severity |
|-------|---------------|----------|
| Step format | IF multi-step | LOW |
| Long ops % | IF >30s operation | MEDIUM |
| Phase separation | IF complex command | LOW |

**NOT findings:** Simple 1-3 step commands without progress tracking.

### 6.2 Error Reporting
Format: `[{SEVERITY}] {description} in {file}:{line}`

| Check | Requirement | Severity |
|-------|-------------|----------|
| Severity prefix | All errors prefixed | HIGH |
| Location | file:line for code issues | HIGH |
| Fix suggestion | Actionable recommendation | MEDIUM |

### 6.3 Output Formatting
| Element | Standard | Severity |
|---------|----------|----------|
| Borders | `─│┌┐└┘├┤┬┴┼` | LOW |
| Numbers | Right-aligned | LOW |
| Status | `OK` `WARN` `FAIL` `PASS` `SKIP` | MEDIUM |
| No emojis | Zero in tables | MEDIUM |

### 6.4 Transparency
| Check | Requirement | Severity |
|-------|-------------|----------|
| Pre-announce | State action before execution | HIGH |
| Change preview | List files before confirmation | HIGH |
| Impact note | Explain non-trivial changes | MEDIUM |

---

## Category 7: Documentation (12 checks)

### 7.1 README Accuracy
Use detected counts from Category 1.

| Check | Requirement | Severity |
|-------|-------------|----------|
| Command count | Matches {actual_commands} | HIGH |
| Agent count | Matches {actual_agents} | HIGH |
| Rule count | Matches {actual_total_rules} | HIGH |
| Features | Each claim has implementation | HIGH |
| No ghosts | Zero deprecated feature refs | MEDIUM |

### 7.2 docs/commands.md
| Check | Requirement | Severity |
|-------|-------------|----------|
| All commands | {actual_commands} `/cco:*` command entries | HIGH |
| Step tables | Each has `\| Step \|` table | MEDIUM |
| Examples | Each has usage code block | MEDIUM |
| Model info | Each shows model in table | MEDIUM |

### 7.3 docs/agents.md
| Check | Requirement | Severity |
|-------|-------------|----------|
| All agents | {actual_agents} `## cco-agent-*` headers | HIGH |
| Scopes | Every scope documented | HIGH |
| Triggers | TRIGGERS section per agent | MEDIUM |

### 7.4 docs/rules.md
| Check | Requirement | Severity |
|-------|-------------|----------|
| Categories | Core, Languages, Frameworks, Operations sections | HIGH |
| Triggers | Detection → Rule mapping (stack detection) | HIGH |
| Rule list | All {totalRules} rules listed | MEDIUM |
| Hook injection | Core rules via SessionStart hook explained | MEDIUM |

---

## Category 8: Safety (11 checks)

### 8.1 Security Practices
| Check | Requirement | Severity |
|-------|-------------|----------|
| No secrets | Zero API keys, passwords in code | CRITICAL |
| Git check | Edit/Write commands check git first | HIGH |
| Risky approval | Auth/DB/API changes need user confirm | HIGH |
| Safe auto | Lint fixes can auto-apply | MEDIUM |

### 8.2 OWASP Compliance
| Check | Requirement | Severity |
|-------|-------------|----------|
| Input validation | `Input-Boundary` rule in Core | HIGH |
| SQL injection | Prevention rule in Adaptive | HIGH |
| XSS | Prevention rule in Adaptive | HIGH |
| Auth | Verification rule in Adaptive | HIGH |

### 8.3 Rollback Capability
| Check | Requirement | Severity |
|-------|-------------|----------|
| Dirty warning | Commands warn about uncommitted changes | HIGH |
| Options | Commit / Stash / Continue presented | HIGH |
| No force | Zero `--update` without explicit request | CRITICAL |

---

## Category 9: Release Readiness (10 checks)

### 9.1 Version Consistency
| Check | Requirement | Severity |
|-------|-------------|----------|
| pyproject.toml | Version matches CHANGELOG | CRITICAL |
| CHANGELOG | Latest version matches pyproject | HIGH |
| SemVer | `\d+\.\d+\.\d+` format | HIGH |
| Breaking | MAJOR bumps list breaking changes | MEDIUM |

### 9.2 Plugin Structure
| Check | Requirement | Severity |
|-------|-------------|----------|
| Plugin manifest | `.claude-plugin/plugin.json` valid JSON | CRITICAL |
| Hooks | `hooks/` contains SessionStart hook | HIGH |
| Core rules | Core rules injected via hook additionalContext | HIGH |
| Profile preservation | /cco:tune preserves existing profile unless --update | HIGH |

### 9.3 Cross-Platform
| Check | Requirement | Severity |
|-------|-------------|----------|
| Paths | Forward slashes only | HIGH |
| No hardcode | Zero C:\, /home/specific refs | HIGH |
| Line endings | LF only, no CRLF | MEDIUM |

---

## Category 10: Best Practices (13 checks)

### 10.1 Claude Best Practices
| Check | Requirement | Severity |
|-------|-------------|----------|
| Positive | "Do X" not "Don't do Y" | HIGH |
| Schemas | JSON output format specified | HIGH |
| CoT | CRITICAL-HIGH use 4-step reasoning | MEDIUM |
| Self-consistency | CRITICAL uses multi-path validation | MEDIUM |
| Placeholders | All examples use `{placeholder}` | HIGH |
| Read-First | Commands read files before editing | CRITICAL |
| No-Hallucination | Verify APIs/methods exist before use | CRITICAL |
| Plan-Before-Act | Plan Review phase for complex changes (>10 findings) | HIGH |
| Agent delegation | Use CCO agents over default tools where applicable | HIGH |

### 10.2 Model Selection
| Check | Requirement | Severity |
|-------|-------------|----------|
| Opus for coding | /cco:optimize, /cco:align, /cco:commit, /cco:preflight use opus | HIGH |
| Haiku for analysis | cco-agent-analyze, cco-agent-research use haiku | MEDIUM |
| Opus for apply | cco-agent-apply uses opus (fewer errors in code changes) | HIGH |
| Documented | Each command shows model in frontmatter | MEDIUM |

### 10.3 Anti-Overengineering
| Check | Requirement | Severity |
|-------|-------------|----------|
| No BC hacks | Zero `backward`, `compat`, `legacy` | HIGH |
| No fallbacks | Zero `fallback`, `deprecated` | HIGH |
| No TODOs | Zero `TODO`, `FIXME`, `XXX` in production code | MEDIUM |
| Purpose | Each component has documented purpose | MEDIUM |
| Simplicity | Simple commands remain simple | HIGH |
| No duplicate analysis | optimize LNT/TYP scopes don't duplicate Quality Gates | HIGH |
| SSOT | Single source of truth for patterns (Quality Gates in agents) | HIGH |

---

## Output Format

```
═══════════════════════════════════════════════════════════
                     CCO FULL REVIEW
═══════════════════════════════════════════════════════════

Detected:
  Commands: {n}  Agents: {n}  Rules: {n} (core:{n} + lang:{n} + fw:{n} + ops:{n})

┌─────────────────────────┬────────┬────────┬────────┐
│ Category                │ Passed │ Failed │ Status │
├─────────────────────────┼────────┼────────┼────────┤
│ 1. Inventory & Sync     │   {n}  │   {n}  │  {st}  │
│ 2. Command Quality      │   {n}  │   {n}  │  {st}  │
│ 3. Agent Quality        │   {n}  │   {n}  │  {st}  │
│ 4. Rules System         │   {n}  │   {n}  │  {st}  │
│ 5. Token Efficiency     │   {n}  │   {n}  │  {st}  │
│ 6. UX/DX Standards      │   {n}  │   {n}  │  {st}  │
│ 7. Documentation        │   {n}  │   {n}  │  {st}  │
│ 8. Safety               │   {n}  │   {n}  │  {st}  │
│ 9. Release Readiness    │   {n}  │   {n}  │  {st}  │
│ 10. Best Practices      │   {n}  │   {n}  │  {st}  │
├─────────────────────────┼────────┼────────┼────────┤
│ TOTAL (~141 checks)     │   {n}  │   {n}  │  {st}  │
└─────────────────────────┴────────┴────────┴────────┘

{if findings}
## 80/20 Prioritized Findings

### Quick Win (CRITICAL + HIGH, auto-fixable)
  [{SEVERITY}] {category}.{check}: {issue}
    Location: {file}:{line}
    Fix: {action}

### Moderate (HIGH, manual intervention needed)
  ...

### Complex (MEDIUM)
  ...

### Major (LOW)
  ...

Summary: C:{n} H:{n} M:{n} L:{n}
Accounting: quickWin:{n} + moderate:{n} + complex:{n} + major:{n} = total:{n}
{/if}
═══════════════════════════════════════════════════════════
```

---

## Step-5: Fix Approval [SKIP IF --auto or --preview or zero findings]

```javascript
if (config.action !== "Report only" && findings.length > 0) {
  // Group by effort category (for reporting only, not filtering in Fix all mode)
  const quickWin = findings.filter(f => f.autoFixable && (f.severity === "CRITICAL" || f.severity === "HIGH"))
  const moderate = findings.filter(f => !f.autoFixable && f.severity === "HIGH")
  const complex = findings.filter(f => f.severity === "MEDIUM")
  const major = findings.filter(f => f.severity === "LOW")

  if (config.action === "Fix safe") {
    // Auto-apply safe fixes, skip risky ones
    toApply = quickWin
  } else if (config.action === "Fix all") {
    // Apply ALL findings - effort categories are for reporting only
    toApply = [...quickWin, ...moderate, ...complex, ...major]
  } else {
    // Interactive: ask user
    AskUserQuestion([{
      question: "Which findings should be fixed?",
      header: "Fix scope",
      options: [
        { label: `All (${findings.length})`, description: "Fix everything now" },
        { label: `Quick Win (${quickWin.length})`, description: "CRITICAL + HIGH, auto-fixable" },
        { label: `Safe only (${quickWin.length})`, description: "Auto-fixable items only" },
        { label: "None", description: "Report only, no fixes" }
      ],
      multiSelect: false
    }])

    // Process selection
    toApply = selectedOption === "All" ? [...quickWin, ...moderate, ...complex, ...major]
            : selectedOption.startsWith("Quick Win") ? quickWin
            : selectedOption.startsWith("Safe") ? quickWin.filter(f => f.autoFixable)
            : []
  }
}
```

### Validation
- [x] User selected fix scope OR auto-mode active
- → Store as: `toApply`
- → Proceed to Step-6

---

## Step-6: Apply Fixes [DELEGATE TO AGENT]

```javascript
if (toApply.length > 0) {
  const isFixAll = config.action === "Fix all"

  // Delegate fix application to cco-agent-apply
  applyResults = Task("cco-agent-apply", `
    fixes: ${JSON.stringify(toApply)}
    fixAll: ${isFixAll}

    Apply CCO system fixes. Types include:
    - doc-sync: Update counts in README, docs files
    - terminology: Fix inconsistent terms (CRITICAL/HIGH vs P0/P1)
    - line-ending: Convert CRLF to LF
    - orphan-ref: Remove deprecated references

    ${isFixAll ? `
    FIX-ALL MODE [MANDATORY]:
    Fix ALL items. Zero skips allowed.
    Every item = FIXED or TECHNICAL FAILURE (with reason).

    FORBIDDEN RESPONSES (never use these as skip reasons):
    - "This is too complex" → Fix it
    - "This is a minor detail" → Fix it anyway
    - "Consider doing this later" → Do it NOW
    - "Recommend manual review" → Apply the fix

    ONLY VALID FAILURES: File not found, parse error, permission denied
    ` : ""}

    CRITICAL - Counting:
    - Count FINDINGS, not locations
    - Each fix = 1 item

    Return:
    { applied: n, failed: n, total: n, details: [...] }
  `, { model: "opus" })

  // Verify accounting invariant
  assert(applyResults.applied + applyResults.failed === applyResults.total,
    "Count mismatch: applied + failed must equal total")
}
```

### Accounting Invariant
`applied + failed = total`

---

## Step-7: Summary

Show final report with:
1. Category summary table
2. Prioritized findings (if any remain)
3. Applied/Failed counts (skipped items noted separately if applicable)
4. Verification status

---

## Anti-Overengineering Guard

Before flagging, ask: (1) Does absence break something? (2) Confuse users? (3) Worth complexity?

**All NO → not a finding.**

NON-findings (concrete examples):
- Simple command without explicit progress tracking
- Fast command without progress bar
- 2-step command without architecture table

---

## Severity Definitions

| Severity | Criteria |
|----------|----------|
| CRITICAL | Security risk, broken functionality, data loss |
| HIGH | Principle violation, doc mismatch, incorrect behavior |
| MEDIUM | Suboptimal but functional |
| LOW | Style, minor improvement |

**When uncertain → choose lower severity.**

---

## Recovery

| Situation | Recovery |
|-----------|----------|
| Fix broke a command | `git checkout -- {file}` |
| Multiple files affected | `git checkout .` |
| Want to review changes | `git diff` |
| Wrong category focus | Re-run with `--focus=X` |

---

## Rules

1. **Context first** - Verify CCO repo before analysis
2. **Dynamic counts** - Never hardcode counts
3. **80/20 prioritization** - Quick Win → Moderate → Complex
4. **Evidence required** - Every finding needs file:line
5. **Self-consistency** - CRITICAL needs dual-path validation:
   - Path A: Analyze as if CCO is broken
   - Path B: Analyze as if CCO works correctly
   - Consensus: Both agree → CRITICAL. Disagree → downgrade to HIGH

**See Core Rules:** Reasoning Strategies for Step-Back and Chain of Thought patterns.

---

## Accounting

**Invariant:** `passed + failed = total` (per category and overall)

```javascript
// Verify at end of each category
assert(category.passed + category.failed === category.totalChecks,
  `Category ${name}: ${passed} + ${failed} != ${totalChecks}`)

// Verify overall (dynamic count based on active checks)
const totalChecks = allCategories.reduce((sum, c) => sum + c.totalChecks, 0)
assert(allCategories.reduce((sum, c) => sum + c.passed, 0) +
       allCategories.reduce((sum, c) => sum + c.failed, 0) === totalChecks,
  `Total checks must equal ${totalChecks}`)
```
