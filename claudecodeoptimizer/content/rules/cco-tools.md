# Tools Rules
*On-demand loading for CCO commands and agents*

## Rule Usage Matrix

| Rule | Commands | Agents |
|------|----------|--------|
| Confirmation Clarity | commit, optimize, review, preflight | - |
| User Input | commit, optimize, review, preflight, checkup, research | - |
| Command Flow | ALL commands | - |
| Context Requirement | ALL except config, research | - |
| Token Efficiency | ALL commands | analyze, apply |
| Safety | commit, optimize, review, config | apply |
| Fix Workflow | optimize, commit | apply |
| Counting Principle | optimize, review, preflight | apply |
| Impact Preview | review | analyze |
| Priority | optimize, review | analyze |
| Question Patterns | ALL with AskUserQuestion | - |
| Output Formatting | ALL commands | ALL agents |
| Variable Templates | ALL | ALL |
| Dynamic Context | commit, preflight, status | - |
| Parallel Execution | ALL commands | analyze |
| Quick Mode | commit, research, review | - |
| Unattended Mode | optimize, config | apply |
| Model Strategy | optimize, review, research, commit | analyze, apply, research |
| Conservative Judgment | optimize, review | analyze |
| Skip Criteria | ALL analysis | analyze, apply |
| Progress Tracking | ALL commands | - |
| Artifact Handling | - | analyze, apply |
| Strategy Evolution | optimize, review | analyze |
| Source Tiering | research | research |

**SSOT Principle:** Rules defined here, referenced by commands/agents. Changes propagate automatically.

---

## Confirmation Clarity [CRITICAL - ALL COMMANDS]

**RULE:** User must know exactly what they're approving before confirmation. Every item clear and specific.

### Pre-Confirmation Display [MANDATORY]

Before ANY approval question, display a clear table/list of exactly what will be done:

| Command | Pre-Confirmation Display |
|---------|-------------------------|
| `/cco-commit` | Table: `No \| Type \| Title` for each commit |
| `/cco-optimize` | Table: `[Severity] Issue \| Location \| Fix Action` for each item |
| `/cco-review` | Table: `Priority \| Issue \| Location \| Recommendation` for items to apply |
| `/cco-preflight` | Table: `Check \| Status \| Issue` for blockers/warnings |

### Format Rules

```markdown
## Pending Changes

| # | Type | Description | Location |
|---|------|-------------|----------|
| 1 | {type} | {title} | {file:line} |
| 2 | {type} | {title} | {file:line} |
...

> Approve above changes?
```

**Requirements:**
- Table appears IMMEDIATELY before the approval question
- No other content between table and question
- Each row is specific and actionable
- Location is always `{file}:{line}` format
- For batch approvals, show count: "Approve {n} items above?"

### Pattern Comparison

| Incorrect | Correct |
|-----------|---------|
| "Apply fixes?" (vague) | "Apply 3 fixes above?" (after showing table) |
| "Proceed with changes?" | "Create 2 commits listed above?" |
| Description in question text | Description in table, question is short |
| Hidden changes | All changes visible before approval |

---

## User Input [REQUIRED]

### AskUserQuestion Tool Requirement [ABSOLUTE]

**RULE:** Every user interaction uses `AskUserQuestion` native tool exclusively.

| Requirement | Enforcement |
|-------------|-------------|
| **Mandatory** | ALL questions, confirmations, selections → AskUserQuestion |
| **Exclusive** | AskUserQuestion is the only method for user input |
| **Direct** | Use tool directly, questions go through tool |
| **All Stages** | Start, middle, end, follow-up → all use tool |
| **MultiSelect** | Use `multiSelect: true` when multiple selections valid |

### Applies To (ALL of these)

| Scenario | Example | MultiSelect |
|----------|---------|-------------|
| Confirmations | "Apply this configuration?" | false |
| Scope selection | "What to audit?" | true |
| Option selection | "Which files to include?" | true |
| Yes/No decisions | "Add BREAKING CHANGE footer?" | false |
| Action selection | "Accept / Modify / Cancel" | false |
| Follow-up actions | "Apply recommendations?" | true |
| Final decisions | "Proceed with release?" | false |
| Clarifications | "Which module do you mean?" | false |
| Error recovery | "How to proceed?" | false |

### Required Patterns [USE TOOL INSTEAD]

| Instead of... | Use This Pattern |
|---------------|------------------|
| "Would you like me to...?" | AskUserQuestion with options |
| "Do you want to...?" | AskUserQuestion with Yes/No options |
| "Should I...?" | AskUserQuestion with action options |
| "Let me know if..." | AskUserQuestion with specific choices |
| "Feel free to..." | AskUserQuestion with explicit options |
| Any question mark `?` | AskUserQuestion tool call |
| Statements expecting response | AskUserQuestion with clear options |

### Option Separator [STRICT]

- **Separator**: Use semicolon (`;`) to separate options
- **Semicolon-Only**: Semicolon separates options, comma allowed within option text
- **Consistent**: Same format across all commands

**Examples:**
- ✓ `Accept; Modify; Cancel`
- ✓ `Yes, proceed anyway; No, fix first` (comma OK within single option)
- ✗ `Accept, Modify, Cancel` (ambiguous)
- ✗ `Yes, proceed anyway, No, fix first` (very ambiguous)

### Command Template Standard [REQUIRED]

All command templates MUST define interactions as tables:

```markdown
## User Input

| Question | Options | MultiSelect |
|----------|---------|-------------|
| {question}? | {opt1}; {opt2}; ... | true/false |
```

**Execution:** When command reaches this table → call `AskUserQuestion` with exact parameters.

### Few-Shot Examples

**Pattern - Single selection:**
```
User: "{action_request}"
→ AskUserQuestion:
  question: "{clarifying_question}?"
  options: ["{option_1}"; "{option_2}"; "{option_3}"]
  multiSelect: false
```

**Pattern - Multi selection:**
```
User: "{scope_request}"
→ AskUserQuestion:
  question: "{scope_question}?"
  options: ["{all_option} (Recommended)"; "{scope_1}"; "{scope_2}"]
  multiSelect: true
```

### Self-Check Before Response

Before ANY response that expects user input:
1. Does it contain `?` → Must use AskUserQuestion
2. Does it offer choices → Must use AskUserQuestion
3. Does it need confirmation → Must use AskUserQuestion
4. Is it a statement but waits for reply → Must use AskUserQuestion

## Command Flow

- **Context-Check**: Verify context.md exists, suggest /cco-config if missing
- **Read-Context**: Load `.claude/rules/cco/context.md`
- **Execute**: Command-specific logic
- **Report**: Results with accounting
- **Diff-only messages**: [CRITICAL] Generate commit messages ONLY from `git diff HEAD` content. NEVER use session memory or conversation context. Describe what the diff shows, not what you remember doing.

## Context Requirement [CRITICAL]

All commands (except `/cco-config`) require CCO context. Check at command start:

```
If context check returns "0":
  CCO context not found.
  Run /cco-config first to configure project context, then restart CLI.
  **Stop immediately.**
```

**Enforcement:** No partial execution. No fallback. Stop and instruct user.

## Token Efficiency [CRITICAL]

Minimize token usage at every step:

| Principle | Implementation |
|-----------|----------------|
| **Single-Agent** | ONE analyze agent, ONE apply agent per command |
| **Linter-First** | Run linters before grep patterns (avoid duplication) |
| **Batch-Calls** | Group multiple tool calls in single message |
| **Targeted-Reads** | Read only matched files, use offset/limit |
| **Early-Exit** | Stop when saturation reached (3× repeated themes) |

**Prefer:** Single consolidated agent │ Targeted file reads with offset/limit │ Deduplicated searches

## Safety

- **Pre-op**: Git status before modifications
- **Dirty**: Prompt Commit / Stash / Continue
- **Rollback**: Clean state enables git checkout

### Classification

**Safe (auto-apply):**

- **Remove-Imports**: Remove unused imports
- **Parameterize-SQL**: Parameterize SQL queries
- **Move-Secrets**: Move secrets to env
- **Fix-Lint**: Fix linting issues
- **Add-Types**: Add type annotations

**Risky (require approval):**

- **Auth-Changes**: Auth/CSRF changes
- **DB-Schema**: DB schema changes
- **API-Contract**: API contract changes
- **Delete-Files**: Delete files
- **Rename-Public**: Rename public APIs

## Fix Workflow

- **Flow**: Analyze > Report > Approve > Apply > Verify
- **Output-Accounting**: `Applied: N | Declined: N | Failed: N | Total: N`

## Counting Principle [CRITICAL]

**All counts MUST be at the "finding" level throughout the entire flow.**

### Definitions

| Term | Definition | Example |
|------|------------|---------|
| **Finding** | A distinct issue identified by analysis | "Type ignore comments without documentation" |
| **Location** | A specific file:line within a finding | `src/core.py:168`, `src/core.py:255` |

### Accounting Terms

| Term | Meaning | Context |
|------|---------|---------|
| `applied` | Findings successfully fixed | Both optimize and review |
| `declined` | User explicitly declined | Optimize (auto-fix context) |
| `notSelected` | User didn't select to apply | Review (selection context) |
| `failed` | Selected but couldn't fix | Both |
| `total` | All findings from analysis | Both |

### Invariants

```javascript
// Core invariant (applies to all commands):
applied + (declined OR notSelected) + failed === total

// Optimize: applied + declined + failed = total
// Review: applied + notSelected + failed = total

// Selection invariant (when user selects items):
applied + failed === selected
```

### Rules

1. **Analysis counts findings** - "4 issues found" means 4 distinct findings
2. **Summary counts findings** - "Applied: 4" means 4 findings were addressed
3. **Locations are internal detail** - Not shown in user-facing counts
4. **Invariants are mandatory** - Validate accounting at every stage

### Anti-patterns

| Wrong | Right |
|-------|-------|
| "Applied: 8" (when 4 findings with 8 locations) | "Applied: 4" |
| Counting locations in summary | Count findings only |
| Agent returns `applied: 8` for 4 findings | Agent returns `applied: 4` |
| Summary shows only applied | Summary shows all: applied, declined/notSelected, failed |

## Impact Preview

- **Direct**: Files to modify
- **Dependents**: Files that import/use
- **Tests**: Coverage of affected code
- **Risk**: LOW / MEDIUM / HIGH
- **Skip**: LOW risk, <=2 files, full coverage

## Priority

- **CRITICAL**: Security, data exposure
- **HIGH**: High-impact, low-effort
- **MEDIUM**: Balanced impact/effort
- **LOW**: Style, minor optimization

## Question Patterns

*All questions inherit User Input [MANDATORY] rules above.*

### Pagination [LIMITS]

- **Max-Questions**: 4 per AskUserQuestion call
- **Max-Options**: 4 per question
- **Overflow**: Use multiple sequential calls

### Option Batching [CRITICAL]

When options exceed 4, split into sequential questions:

| Total Options | Batches | Pattern |
|---------------|---------|---------|
| 5-8 | 2 | 4 + (1-4) |
| 9-12 | 3 | 4 + 4 + (1-4) |
| 13-16 | 4 | 4 + 4 + 4 + (1-4) |

**Batch Rules:**
- **First-Batch-Exit**: Include "None" or "Skip" in first batch to allow early exit
- **Subsequent-Skip**: Include "Skip" option in each subsequent batch
- **Numbering**: Label batches as "(1/N)", "(2/N)", etc.
- **Grouping**: Group related options together (e.g., by region, category, severity)

**Example (10 compliance options):**
```
Batch 1/3 (Common): None, SOC2, HIPAA, PCI
Batch 2/3 (Privacy): GDPR, CCPA, ISO27001, Skip  [skip if "None" in 1]
Batch 3/3 (Specialized): FedRAMP, DORA, HITRUST, Skip  [skip if "None" in 1]
```

**Skip Logic:**
- If "None" selected in first batch → skip all subsequent batches
- If "Skip" selected → proceed to next batch (no selection from current)

### Batch Approval (for fix operations)

- **MultiSelect**: true for batch approvals
- **All-Option**: First option = "All ({N})" for bulk
- **Priority-Order**: CRITICAL → HIGH → MEDIUM → LOW
- **Item-Format**: `{description} [{file:line}] [{safe|risky}]`

### Labels [MANDATORY]

- **One-Label**: Each option has exactly ONE label
- **Current**: `[current]` - matches existing config (priority 1)
- **Detected**: `[detected]` - auto-detected (priority 2)
- **Recommended**: `(Recommended)` - max 1/question (priority 3)
- **Precedence**: detected AND current → show `[current]` only

### Ordering

- **Numeric**: Ascending (60 → 70 → 80 → 90)
- **Severity**: Safest → riskiest
- **Scope**: Narrowest → widest

### Category Separation

Present different categories in SEPARATE batches:

| Type | Examples |
|------|----------|
| Settings | strictMode, timeout |
| Permissions | readOnly, allowDelete |
| Thresholds | coverage%, complexity |

## Output Formatting

**Follow output formats precisely. Exact formatting ensures consistency and parseability.**

### Command Summary Format [STANDARD]

All CCO commands MUST end with a consistent summary format:

```markdown
## {Command} Complete

| Metric | Value |
|--------|-------|
| {metric_1} | {value_1} |
| {metric_2} | {value_2} |
| ... | ... |

Status: {OK|WARN|FAIL} | Applied: {n} | Declined: {n} | Failed: {n}

{next_step_instruction}
```

**Command-Specific Summaries:**

| Command | Key Metrics | Status Calculation |
|---------|-------------|-------------------|
| `/cco-commit` | Commits created, Files changed, Lines +/- | OK if all commits succeed |
| `/cco-optimize` | Auto-fixed, User-approved, Declined | OK if no failures |
| `/cco-review` | Foundation status, Do Now/Plan/Consider counts | Based on foundation |
| `/cco-preflight` | Blockers, Warnings, Checks passed | FAIL if blockers, WARN if warnings |
| `/cco-config` | Files written, Detections, Questions asked | OK if all writes succeed |

### JSON Schema Standard (Structured Output)

When outputting structured data, follow this schema pattern:

```json
{
  "status": "{OK|WARN|FAIL}",
  "accounting": {
    "done": "{n}",
    "declined": "{n}",
    "failed": "{n}",
    "total": "{n}"
  },
  "items": [
    {
      "severity": "{CRITICAL|HIGH|MEDIUM|LOW}",
      "title": "{issue_description}",
      "location": "{file}:{line}",
      "action": "{Applied|Declined|Failed}"
    }
  ]
}
```

**Rules:**
- Use consistent field names across all commands
- Include `accounting` for operations with counts
- Use `location` format: `{file}:{line}` for code references

### Table Characters [STRICT]

- **Borders**: `─│┌┐└┘├┤┬┴┼`
- **Headers**: `═║╔╗╚╝`

### Alignment [REQUIRED]

- **Numbers**: Right-aligned
- **Text**: Left-aligned
- **Status**: Centered

### Status Indicators [EXACT]

- **Values**: OK | WARN | FAIL | PASS | SKIP

### Progress Bars [FORMULA]

- **Formula**: `filled = round(percentage / 100 * 8)` -> `████░░░░`

### Formatting Standards

- **Plain-Tables**: Use only specified table characters in tables
- **Minimal-Unicode**: Use only box-drawing characters defined above
- **Clean-Headers**: Use markdown headers (##, ###) for section titles

## Variable Templates

### Standard Format [REQUIRED]

Use consistent `{variable_name}` format for all placeholders:

| Type | Format | Example |
|------|--------|---------|
| Simple value | `{name}` | `{file}`, `{line}`, `{status}` |
| Enumerated | `{option1\|option2}` | `{OK\|WARN\|FAIL}` |
| Counted | `{n}` | Used for numbers |
| Path | `{file}:{line}` | Location references |
| Descriptive | `{noun_description}` | `{issue_description}`, `{file_path}` |

**Rules:**
- Always use snake_case for multi-word variables
- Use `{n}` for generic numeric placeholders
- Use `|` to separate enumerated options within braces

## Dynamic Context

### Injection Syntax [REQUIRED]

- **Syntax**: Use `!` backtick for real-time context
- **Git-Status**: `` `git status --short` ``
- **Branch**: `` `git branch --show-current` ``
- **CCO-Context**: `` `test -f .claude/rules/cco/context.md && head -30 .claude/rules/cco/context.md` ``

### When to Use

| Context Type | Command | Example |
|--------------|---------|---------|
| Git state | commit, refactor | `` `git status` `` |
| File content | audit, review | `` `head -50 .claude/rules/cco/context.md` `` |
| Dependencies | audit, health | `` `cat package.json \| jq .dependencies` `` |
| Recent changes | commit, review | `` `git log --oneline -5` `` |

### Benefits

- **Accuracy**: Real-time accuracy over stale assumptions
- **Anti-Hallucination**: Reduces hallucination risk
- **Efficiency**: Eliminates redundant file reads

## Parallel Execution

### When to Parallelize [REQUIRED]

| Scenario | Action |
|----------|--------|
| Independent scans | Launch parallel agents |
| Multiple file reads | Batch in single call |
| Unrelated checks | Run simultaneously |
| Dependent operations | Run sequentially |

### Agent Parallelization Pattern

- **Launch**: Launch agents simultaneously in single message
- **Scope**: Each agent handles distinct scope
- **Diverse**: Use varied search strategies per agent
- **Merge**: Merge results after all complete

### Agent Propagation [REQUIRED]

- **Context-Pass**: Pass context.md summary to all agents
- **Rules-Pass**: Include applicable rules from context
- **Format-Pass**: Specify exact output format expected
- **Todo-Pass**: Tell agents: "Make a todo list first"

**Template for agent instructions:**
```
Context: {relevant context.md fields}
Rules: {applicable rules from this file}
Output: {expected format - follow precisely}
Note: Make a todo list first, then process systematically
```

### Benefits

- **Speed**: Faster execution (N agents = ~1/N time)
- **Coverage**: Better coverage (diverse search strategies)
- **Context**: Reduced context switching

## Quick Mode

### Single-Message Enforcement [STRICT]

- **Use-Defaults**: Apply smart defaults for all options
- **Defaults**: Use smart defaults for all options
- **Direct-Output**: Output tool calls and final summary only
- **Summary**: Only tool calls, then final summary
- **MUST-Single**: Complete all steps in a single message

### Applicable Commands

| Command | Quick Behavior |
|---------|----------------|
| `/cco-commit` | Stage all, single commit, smart defaults |
| `/cco-research` | T1-T2 only, brief output, no questions |
| `/cco-review` | Smart defaults, report only |
| `/cco-preflight` | (Not applicable - requires explicit decisions) |

### Output Restriction

- **Single-Message**: Complete ALL steps in a single message
- **Allowed-Only**: Use only tools listed in command frontmatter
- **Summary-Only**: Output tool calls and final summary text only

## Conservative Judgment

### Severity Assignment [CRITICAL]

| Keyword | Severity | Confidence Required |
|---------|----------|---------------------|
| crash, data loss, security breach | CRITICAL | HIGH |
| broken, blocked, cannot use | HIGH | HIGH |
| error, fail, incorrect | MEDIUM | MEDIUM |
| style, minor, cosmetic | LOW | LOW |

### False Positive Prevention

- **Trust**: False positives erode user trust faster than missed issues
- **Lower**: When uncertain between two severities, choose lower
- **Genuine**: Only flag issues that genuinely block users
- **Evidence**: Require explicit evidence, not inference

### Severity Limits

- **Style**: Style issues → maximum severity: LOW
- **Unverified**: Unverified claims → maximum severity: MEDIUM
- **Single**: Single occurrence → maximum severity: MEDIUM (except security)

## Skip Criteria

*Base skip paths defined in Core Rules (Skip).*

### CCO Skip Markers

- **Line**: `// cco-ignore` or `# cco-ignore` - skip this line
- **File**: `// cco-ignore-file` or `# cco-ignore-file` - skip entire file
- **Markdown**: `<!-- cco-ignore -->` - skip in markdown

### Additional CCO Exclusions

- **Test Fixtures**: `fixtures/`, `testdata/`, `__snapshots__/`
- **Examples**: `examples/`, `samples/`, `demo/`, `benchmarks/`

## Progress Tracking (TodoWrite)

**All CCO commands use TodoWrite for progress visibility.** No custom step announcements.

### Requirement [CRITICAL]

1. **Start**: Create todo list with ALL steps/phases at command start
2. **Track**: Mark `in_progress` before starting each step
3. **Update**: Mark `completed` immediately after each step finishes
4. **Single**: Exactly ONE item `in_progress` at a time

### Format

```
TodoWrite([
  { content: "{step_name}", status: "in_progress", activeForm: "{step_name_ing}" },
  { content: "{step_name}", status: "pending", activeForm: "{step_name_ing}" },
  ...
])
```

### Rules

| Rule | Description |
|------|-------------|
| **Immediate** | Update status immediately, not batched |
| **Track-All** | Update every item status (completed, declined, or failed) |
| **activeForm** | Use present continuous (-ing form) |
| **content** | Use imperative form |

## Artifact Handling

- **Reference-Large**: Reference large outputs by path/ID, not inline
- **Tokenize-Efficiently**: Use `[artifact:path]` notation for files >500 lines
- **Summarize-First**: Provide digest before full artifact access
- **Chunk-Processing**: Process large data in manageable segments
- **Cache-Artifacts**: Reuse analyzed artifacts within session

## Strategy Evolution

### Learnings Section [REQUIRED]

**Location:** `.claude/rules/cco/context.md` → `## Learnings` section

**Format:**
```markdown
## Learnings

### Avoid
- {pattern}: {why it failed} → {what works instead}

### Prefer
- {pattern}: {why it works} [{impact: high|medium|low}]

### Systemic
- {issue}: {root cause} → {recommendation}
```

### Usage Flow

| Phase | Action |
|-------|--------|
| Session Start | Read context.md, note Learnings section |
| Analysis | Check Avoid patterns before recommending |
| Failure | Add to Avoid with root cause |
| Success | Add to Prefer with context |
| Systemic | Add architectural findings to Systemic |

### Rules

- **Max Items**: 5 per category (remove oldest when full)
- **Duplicates**: Update existing instead of adding new
- **Format**: Single line per learning, concise

## Unattended Mode

**Applies to:** Commands with `--auto` or `--unattended` flags.

### Behavior

| Flag | Effect |
|------|--------|
| `--auto` | Skip all questions, use safe defaults, apply auto-fixable only |
| `--unattended` | Same as --auto (alias) |

### Requirements

1. **No AskUserQuestion** - Must complete without user interaction
2. **Safe defaults only** - Conservative choices, no risky operations
3. **Auto-fixable only** - Skip items requiring approval
4. **Report at end** - Summary of what was done/skipped

### Defaults by Command

| Command | Unattended Behavior |
|---------|---------------------|
| optimize | Auto-fix safe items only, skip risky |
| config | Use detected values, skip optional questions |

**Difference from Quick Mode:** Quick Mode reduces questions but may still ask critical ones. Unattended Mode is fully non-interactive.

## Model Strategy

**Model selection based on task requirements. Opus + Haiku only (no Sonnet).**

### Selection Criteria

| Criteria | Model | Rationale |
|----------|-------|-----------|
| Code modifications | Opus | 50-75% fewer tool errors |
| Deep analysis | Opus | Complex reasoning needed |
| Synthesis/recommendations | Opus | Quality over speed |
| Read-only scanning | Haiku | Fast, low cost |
| Web search/fetch | Haiku | Speed matters |
| Large codebase (10K+) | Opus | Accuracy for scale |

### Agent Model Assignment

| Agent | Model | Reason |
|-------|-------|--------|
| cco-agent-analyze | Haiku | Read-only operations |
| cco-agent-apply | Opus | Code modifications |
| cco-agent-research | Haiku | Web fetches (synthesis uses Opus) |

### Command Model Assignment

| Command | Model | Reason |
|---------|-------|--------|
| optimize | Opus | Security/quality analysis |
| review | Opus | Architecture analysis |
| research | Opus | Complex synthesis |
| commit | Opus | Quality gates |
| Others | inherit | Orchestration only |

## Source Tiering

**Reliability scoring for research sources. Used by cco-research and cco-agent-research.**

### Tier Definitions

| Tier | Sources | Score Range | Reliability |
|------|---------|-------------|-------------|
| T1 | Official docs, specs, RFCs | 90-100 | Authoritative |
| T2 | GitHub repos, changelogs, release notes | 80-89 | Primary |
| T3 | Major tech blogs (official), tutorials | 70-79 | Trusted |
| T4 | Stack Overflow, forums, community | 60-69 | Verified |
| T5 | Personal blogs, Medium posts | 50-59 | Unverified |
| T6 | Unknown sources | 40-49 | Skip |

### Scoring Modifiers

| Modifier | Effect |
|----------|--------|
| Domain authority | +10 for official domains |
| Currency (< 6 months) | +10 |
| Stale (> 2 years) | -15 |
| Multiple sources agree | +10 per confirmation |
| Vendor/promo content | -20 |

### Usage Rules

1. **Minimum T1/T2** - At least 1 T1 or T2 source required for recommendations
2. **Contradiction Resolution** - Higher tier wins, document conflicts
3. **Saturation** - Stop when 3+ T1/T2 sources independently confirm
