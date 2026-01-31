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

## Policies

**See Core Rules:** `CCO Operation Standards` for No Deferrals Policy, Accounting invariant, and valid failure reasons.

## Architecture

| Step | Name | Action | Optimization |
|------|------|--------|--------------|
| 1 | Setup | Q1: Review mode selection | Single question |
| 2 | Inventory | Detect counts via Bash | Parallel Bash |
| 3 | Analyze | 4 Explore agent groups (parallel) | 4 agents in single message |
| 4 | Prioritize | 80/20 findings | Instant |
| 5 | Approval | Q2: Select fixes (conditional) | Only if needed |
| 6 | Apply | Delegate to cco-agent-apply | Agent handles batching |
| 7 | Summary | Show report | Instant |

**Key Optimization:** Step-3 launches 4 parallel Explore agent groups (Structure, Commands, Standards, Docs) in a single message = true parallel execution. Step-6 delegates to cco-agent-apply for efficient, verified fix application.

**Scope Groups:**

| Group | Categories | Checks |
|-------|-----------|--------|
| **Structure & Inventory** | 1 (Inventory) + 4 (Rules) + 9 (Release) | ~40 checks |
| **Commands & Agents** | 2 (Commands) + 3 (Agents) | ~29 checks |
| **Standards & Practices** | 5 (Token) + 6 (UX/DX) + 10 (Best Practices) | ~48 checks |
| **Documentation & Safety** | 7 (Docs) + 8 (Safety) | ~23 checks |

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

**Run analysis with 4 parallel scope groups - multiple Task calls in same message execute concurrently:**

```javascript
// PARALLEL EXECUTION: Launch 4 scope groups in single message
// Each Task returns results directly (synchronous)
// Multiple Task calls in same message run in parallel automatically

// Group A: Structure & Inventory (Cat 1 + Cat 4 + Cat 9)
structureResults = Task("Explore", `
  CCO Structure & Inventory analysis - Categories 1, 4, 9 (~40 checks)

  CATEGORY 1 - Inventory & Sync (15 checks):
  1.1 Count files dynamically:
      - commands/*.md (expected: 7 - optimize, align, preflight, commit, tune, research, docs)
      - agents/cco-agent-*.md (expected: 3 - analyze, apply, research)
      - rules/core/cco-*.md, rules/languages/cco-*.md, rules/frameworks/cco-*.md, rules/operations/cco-*.md
  1.2 Compare detected counts against:
      - README.md: check command count, agent count, rule count claims
      - docs/commands.md: count ## /cco:* headers, compare to actual commands
      - docs/agents.md: count ## cco-agent-* headers, compare to actual agents
      - docs/rules.md: check category breakdown matches actual rule files
  1.3 SSOT Compliance:
      - Grep for orphan refs: .cco/, principles.md, projects.json, context.md (should be 0)
      - Grep for deprecated refs: cco-tune, cco-setup without /cco: prefix (should be 0)
      - Grep for legacy refs: cco-tools, cco-guide, cco-principles (should be 0)
      - Check all command refs use /cco:* format
  1.4 Dependency chain:
      - Verify Task() calls in commands/*.md reference valid agent types (cco-agent-analyze, cco-agent-apply, cco-agent-research, Explore)
      - Verify scope parameters match agent capabilities in agents/*.md
  1.5 Terminology consistency:
      - Severity: CRITICAL/HIGH/MEDIUM/LOW used consistently (not P0/P1/P2/P3)
      - Status: OK/WARN/FAIL used consistently
      - Scope names: identical between commands/*.md and agents/*.md

  CATEGORY 4 - Rules System (15 checks):
  4.1 Detection accuracy:
      - Each rule file in rules/ has clear trigger conditions
      - No orphan rules (rules without triggers)
      - Multi-language coverage: Python, JS/TS, Go, Rust rules exist
  4.2 Rule quality:
      - Each rule contains specific action verb
      - Rule names unique across all files (grep rule identifiers)
      - Examples use {placeholder} format
      - Positive framing: "Do X" preferred over "Don't do Y"
  4.3 Profile generation:
      - .claude/rules/cco-profile.md exists with required sections (Stack, Documentation, Rules Loaded)
      - /cco:tune references in commands validate profile exists

  CATEGORY 9 - Release Readiness (10 checks):
  9.1 Version consistency:
      - Compare pyproject.toml version with CHANGELOG.md latest version
      - Check SemVer format (digits.digits.digits)
  9.2 Plugin structure:
      - Verify .claude-plugin/plugin.json is valid JSON with required fields
      - Verify hooks/ directory contains SessionStart hook
      - Check core rules injection via hook additionalContext
  9.3 Cross-platform:
      - Grep for backslash paths (C:\\, D:\\) in non-.local files
      - Grep for hardcoded /home/ or /Users/ paths
      - Check for CRLF line endings in .md and .py files

  For each finding: { category: N, id: "N.N", severity: "CRITICAL|HIGH|MEDIUM|LOW",
    title: string, location: "file:line", description: string, autoFixable: bool }
  Return: { categories: [1, 4, 9], passed: n, failed: n, findings: [...] }
`, { model: "haiku" })

// Group B: Commands & Agents (Cat 2 + Cat 3)
commandsResults = Task("Explore", `
  CCO Commands & Agents analysis - Categories 2, 3 (~29 checks)

  CATEGORY 2 - Command Quality (18 checks):
  2.1 Template compliance in commands/*.md:
      - Each command has Architecture table (| Step | Name | Action |)
      - Each command has Validation blocks with pass/fail criteria
      - Fix commands report applied/failed/deferred accounting
  2.2 AskUserQuestion standards:
      - Zero plain text questions - all user interaction via AskUserQuestion tool
      - multiSelect: true used for batch selections
      - Max 4 questions × 4 options per AskUserQuestion call
      - Questions appear in early steps, not mid-execution
  2.3 Fix workflow:
      - Commands follow: Analyze → Report → Approve → Apply → Verify
      - Severity order: CRITICAL → HIGH → MEDIUM → LOW
      - Accounting invariant: applied + failed + deferred = total
      - Quality Gates only in /cco:commit and /cco:preflight (NOT in /cco:optimize)
  2.4 Mode consistency:
      - --auto mode: zero AskUserQuestion calls, smart defaults
      - --preview mode: zero Edit/Write calls, read-only
      - Check all 7 commands for --auto and --preview support

  CATEGORY 3 - Agent Quality (11 checks):
  3.1 Scope accuracy in agents/cco-agent-*.md:
      - cco-agent-analyze: verify OPTIMIZE scopes (security, hygiene, types, lint, performance,
        ai-hygiene, robustness, privacy, doc-sync, simplify) + REVIEW scopes (architecture,
        patterns, testing, maintainability, ai-architecture, functional-completeness)
      - cco-agent-apply: verify fix scope + config scope
      - cco-agent-research: verify 6 scopes (local, search, analyze, synthesize, full, dependency)
      - Compare scope lists to docs/agents.md
  3.2 Parallel execution patterns:
      - Commands use multiple Task() calls in single message for parallelism
      - Model selection: analyze/research = haiku, apply = opus
      - No run_in_background for Task (agent) calls
  3.3 Output standards:
      - JSON with findings[], metrics, status fields
      - Every finding has severity and location fields

  For each finding: { category: N, id: "N.N", severity: "CRITICAL|HIGH|MEDIUM|LOW",
    title: string, location: "file:line", description: string, autoFixable: bool }
  Return: { categories: [2, 3], passed: n, failed: n, findings: [...] }
`, { model: "haiku" })

// Group C: Standards & Practices (Cat 5 + Cat 6 + Cat 10)
standardsResults = Task("Explore", `
  CCO Standards & Best Practices analysis - Categories 5, 6, 10 (~48 checks)

  CATEGORY 5 - Token Efficiency & Specification Clarity (22 checks):
  5.1 Content density in commands/*.md and agents/*.md:
      - Tables used for tabular data (not prose paragraphs)
      - Lists for multi-item content
      - No redundant content across files (grep for identical paragraphs)
      - Files >500 lines: check if can be split or referenced
  5.2 Rule format in rules/**/*.md:
      - Rules fit < 120 chars per line
      - Grouped under ### headers
      - No duplication across core/languages/frameworks/operations
  5.3 Command efficiency:
      - Profile auto-loaded from .claude/rules/ (not manually loaded)
      - Batch reads: multiple Read() in single message where possible
      - Parallel agents: independent analyses use parallel Task() calls
  5.4 Specification clarity:
      - WHAT over HOW: check for excessive if/else pseudocode that teaches obvious logic
      - Standards over Teaching: thresholds/constraints, not rationale paragraphs
      - DRY for Policies: common patterns reference Core Rules (not duplicated)
      - No algorithm walkthroughs for obvious logic
  5.5 AskUserQuestion limits:
      - Max 4 questions per call, max 4 options per question
      - 5+ scopes split into logical groups
  5.6 Rule optimization:
      - No teaching of basics Opus 4.5 already knows
      - Each rule provides unique CCO-specific value
      - Threshold focus: numeric limits > prose descriptions

  CATEGORY 6 - UX/DX Standards (13 checks):
  6.1 Progress visibility:
      - Multi-step operations show step progress
      - Long operations (>30s) show percentage or status
  6.2 Error reporting format:
      - [{SEVERITY}] {description} in {file}:{line}
      - Actionable recommendations included
  6.3 Output formatting:
      - Status indicators: OK/WARN/FAIL/PASS/SKIP
      - No emojis in tables
  6.4 Transparency:
      - Actions pre-announced before execution
      - File lists shown before confirmation
      - Non-trivial changes explained

  CATEGORY 10 - Best Practices (13 checks):
  10.1 Claude best practices in all .md files:
      - Positive framing: "Do X" not "Don't do Y"
      - JSON schemas specified for complex outputs
      - Read-First: commands read files before editing
      - No-Hallucination: APIs/methods verified before use
      - Plan-Before-Act: Plan Review phase for complex changes
      - Agent delegation: CCO agents used over default tools
  10.2 Model selection:
      - Commands (optimize, align, commit, preflight): model: opus in frontmatter
      - Agents (analyze, research): model: haiku in frontmatter
      - Agent (apply): model: opus in frontmatter
  10.3 Anti-overengineering:
      - Grep for backward, compat, legacy (should be 0 in production code)
      - Grep for fallback, deprecated (should be 0)
      - Grep for TODO, FIXME, XXX in commands/*.md and agents/*.md
      - No duplicate analysis: optimize LNT/TYP scopes vs Quality Gates

  For each finding: { category: N, id: "N.N", severity: "CRITICAL|HIGH|MEDIUM|LOW",
    title: string, location: "file:line", description: string, autoFixable: bool }
  Return: { categories: [5, 6, 10], passed: n, failed: n, findings: [...] }
`, { model: "haiku" })

// Group D: Documentation & Safety (Cat 7 + Cat 8)
docsResults = Task("Explore", `
  CCO Documentation & Safety analysis - Categories 7, 8 (~23 checks)

  CATEGORY 7 - Documentation (12 checks):
  7.1 README.md accuracy:
      - Command count matches actual commands/*.md file count
      - Agent count matches actual agents/cco-agent-*.md file count
      - Rule count matches actual rules/**/*.md file count
      - Each feature claim has corresponding implementation
      - No references to deprecated/removed features
  7.2 docs/commands.md:
      - Has entry for each command in commands/*.md
      - Each entry has step table and usage example
      - Model info shown for each command
  7.3 docs/agents.md:
      - Has entry for each agent in agents/cco-agent-*.md
      - Every scope documented per agent
      - TRIGGERS section per agent
  7.4 docs/rules.md:
      - Core, Languages, Frameworks, Operations sections present
      - Detection → Rule mapping documented
      - All rules listed with categories

  CATEGORY 8 - Safety (11 checks):
  8.1 Security practices:
      - Zero API keys, passwords, secrets in any file (grep for api_key, password, secret, token patterns)
      - Edit/Write commands check git status first
      - Auth/DB/API changes require user confirmation
  8.2 OWASP compliance:
      - Input validation rules present in rules/
      - SQL injection, XSS prevention rules present
  8.3 Rollback capability:
      - Commands warn about uncommitted changes
      - Commit/Stash/Continue options presented
      - No --force or destructive git operations without explicit request

  For each finding: { category: N, id: "N.N", severity: "CRITICAL|HIGH|MEDIUM|LOW",
    title: string, location: "file:line", description: string, autoFixable: bool }
  Return: { categories: [7, 8], passed: n, failed: n, findings: [...] }
`, { model: "haiku" })

// Merge all parallel results
allFindings = [
  ...structureResults.findings,
  ...commandsResults.findings,
  ...standardsResults.findings,
  ...docsResults.findings
]

// Build category results from merged data
categoryResults = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(cat => ({
  category: cat,
  passed: allFindings.filter(f => f.category === cat && !f.failed).length,
  failed: allFindings.filter(f => f.category === cat).length
}))
```

**Key Optimization:** Single message with 4 Task calls = true parallel execution. Do NOT use `run_in_background` for Task (agent) calls — results are returned directly. Explore agents use Haiku model for fast, efficient codebase search.

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
| Accounting | Fix commands report applied/failed/deferred | HIGH |

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
| Accounting invariant | applied + failed + deferred = total | HIGH |
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
| Parallel agents | Multiple Task calls in single message (no run_in_background) | HIGH |
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
// BAD: Teaching HOW (40 lines of pseudocode)
for (const file of files) {
  if (shouldAnalyze(file)) { ... }
}

// BAD: Academic justification
"Studies show >50% coupling leads to 2x bug rates (Fowler 1999)"

// BAD: Policy duplication
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
    Every item = `applied`, `failed` (with "Technical: [reason]"), or `deferred` (with "Deferred: [reason]").

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
    { applied: n, failed: n, deferred: n, total: n, details: [...] }
  `, { model: "opus" })

  // Verify accounting invariant
  assert(applyResults.applied + applyResults.failed + applyResults.deferred === applyResults.total,
    "Count mismatch: applied + failed + deferred must equal total")
}
```

### Accounting Invariant
`applied + failed + deferred = total`

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
