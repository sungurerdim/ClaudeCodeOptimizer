---
name: cco-full-review
description: CCO system health check (129 checks across 10 categories)
allowed-tools: Read(*), Grep(*), Glob(*), Bash(*), Task(*), TodoWrite
model: opus
---

# CCO Full Review

Comprehensive analysis of CCO system against its documented design principles.

---

## Context Check [CRITICAL]

```bash
# Verify CCO repo is accessible
CCO_REPO=$(test -d /home/node/ClaudeCodeOptimizer && echo "1" || echo "0")
```

If CCO_REPO = "0":
```
CCO repository not found at expected location.
Cannot perform self-review without access to CCO source.
```
**Stop immediately.**

---

## Progress Tracking

```javascript
TodoWrite([
  { content: "Phase-1: Inventory detection", status: "in_progress", activeForm: "Detecting inventory" },
  { content: "Phase-2: Run 10-category analysis", status: "pending", activeForm: "Analyzing categories" },
  { content: "Phase-3: Prioritize findings", status: "pending", activeForm: "Prioritizing findings" },
  { content: "Phase-4: Apply fixes (if --fix)", status: "pending", activeForm: "Applying fixes" },
  { content: "Phase-5: Generate report", status: "pending", activeForm: "Generating report" }
])
```

---

## Execution Strategy

```javascript
// Model selection based on flags
const model = args.includes("--quick") ? "haiku" : "opus"

// Parallel category analysis (Categories 1-10 in parallel batches)
const batch1 = Promise.all([
  analyzeCategory(1, "Inventory & Sync"),
  analyzeCategory(2, "Command Quality"),
  analyzeCategory(3, "Agent Quality"),
  analyzeCategory(4, "Rules System"),
  analyzeCategory(5, "Token Efficiency")
])

const batch2 = Promise.all([
  analyzeCategory(6, "UX/DX Standards"),
  analyzeCategory(7, "Documentation"),
  analyzeCategory(8, "Safety"),
  analyzeCategory(9, "Release Readiness"),
  analyzeCategory(10, "Best Practices")
])

// Merge results
allFindings = [...await batch1, ...await batch2].flat()
```

---

## Category 1: Inventory & Sync (15 checks)

### 1.1 Dynamic Count Detection
```bash
COMMANDS=$(ls ~/.claude/commands/cco-*.md 2>/dev/null | wc -l)
CORE_RULES=$(grep -c "^- \*\*" ~/.claude/rules/cco/core.md)
AI_RULES=$(grep -c "^- \*\*" ~/.claude/rules/cco/ai.md)
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
- Orphan detection: grep for `.cco/`, `principles.md`, `projects.json` = 0
- Deprecated refs: grep for `cco-tune`, `cco-setup`, `cco-help` = 0
- Legacy cleanup: grep for `cco-tools`, `cco-guide`, `cco-principles` = 0

### 1.4 Dependency Chain
- Agent invocations use valid agent types = CRITICAL
- Scope parameters match agent capabilities = HIGH
- Commands read context.md where required = HIGH
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
| TodoWrite | IF used: in_progress → completed flow | MEDIUM |
| Validation blocks | Clear pass/fail criteria | MEDIUM |
| Context check | Commands needing context verify it exists | HIGH |
| Accounting | Fix commands report done/declined/fail | HIGH |

**NOT findings:** Simple commands without TodoWrite, short commands without architecture tables.

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
| Accounting invariant | done + declined + fail = total | HIGH |

### 2.4 Mode Consistency
| Mode | Behavior | Severity |
|------|----------|----------|
| `--auto` | Zero AskUserQuestion calls, smart defaults | HIGH |
| `--dry-run` | Zero Edit/Write calls, preview only | HIGH |
| Mode parity | `--auto` quality equals interactive | MEDIUM |

---

## Category 3: Agent Quality (11 checks)

### 3.1 Scope Accuracy
Dynamically detect scopes from agent definitions, compare to docs/agents.md.

| Check | Requirement | Severity |
|-------|-------------|----------|
| Analyze scopes | Documented = implemented | HIGH |
| Apply scopes | Documented = implemented | HIGH |
| Research scopes | Documented = implemented | HIGH |
| No overlap | Scope lists have zero intersection | MEDIUM |
| Description | Agent descriptions match behavior | HIGH |

### 3.2 Parallel Execution
| Check | Requirement | Severity |
|-------|-------------|----------|
| Single message | Multiple Task() in one assistant message | HIGH |
| Model selection | analyze/research = haiku, apply = opus | HIGH |
| Result merge | Parent combines agent outputs correctly | HIGH |
| Context prop | Agents receive context.md summary | MEDIUM |

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

### 4.3 Context Generation
`/cco-config` must produce:

| Check | Requirement | Severity |
|-------|-------------|----------|
| Context created | File exists after /cco-config | CRITICAL |
| Detections | All auto-detected values recorded | HIGH |
| User choices | All AskUserQuestion responses recorded | HIGH |
| Learnings | `## Learnings` header present | MEDIUM |

---

## Category 5: Token Efficiency (11 checks)

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
| Context pre-collect | Load once in Step 1, reuse | HIGH |
| Batch reads | Multiple Read() in single message | MEDIUM |
| Parallel agents | Independent analyses parallel | HIGH |
| Quick mode | Minimal output | MEDIUM |

---

## Category 6: UX/DX Standards (13 checks)

### 6.1 Progress Visibility
| Check | When Required | Severity |
|-------|---------------|----------|
| TodoWrite | IF 5+ steps | MEDIUM |
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
| All commands | {actual_commands} `## /cco-*` headers | HIGH |
| Step tables | Each has `\| Step \|` table | MEDIUM |
| Examples | Each has usage code block | MEDIUM |

### 7.3 docs/agents.md
| Check | Requirement | Severity |
|-------|-------------|----------|
| All agents | {actual_agents} `## cco-agent-*` headers | HIGH |
| Scopes | Every scope documented | HIGH |
| Triggers | TRIGGERS section per agent | MEDIUM |

### 7.4 docs/rules.md
| Check | Requirement | Severity |
|-------|-------------|----------|
| Categories | Core, AI, Adaptive sections | HIGH |
| Triggers | Detection → Rule mapping | HIGH |
| Adaptive list | All rules listed | MEDIUM |
| Export | AGENTS.md vs CLAUDE.md explained | MEDIUM |

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
| No force | Zero `--force` without explicit request | CRITICAL |

---

## Category 9: Release Readiness (10 checks)

### 9.1 Version Consistency
| Check | Requirement | Severity |
|-------|-------------|----------|
| pyproject.toml | Version matches CHANGELOG | CRITICAL |
| CHANGELOG | Latest version matches pyproject | HIGH |
| SemVer | `\d+\.\d+\.\d+` format | HIGH |
| Breaking | MAJOR bumps list breaking changes | MEDIUM |

### 9.2 Install/Uninstall
| Check | Requirement | Severity |
|-------|-------------|----------|
| Install | `cco-install` creates all files | CRITICAL |
| Uninstall | `cco-uninstall` removes all files | CRITICAL |
| No orphans | Zero CCO files after uninstall | HIGH |
| Upgrade | context.md preserved | HIGH |

### 9.3 Cross-Platform
| Check | Requirement | Severity |
|-------|-------------|----------|
| Paths | Forward slashes only | HIGH |
| No hardcode | Zero C:\, /home/specific refs | HIGH |
| Line endings | LF only, no CRLF | MEDIUM |

---

## Category 10: Best Practices (13 checks)

### 10.1 Claude 4 Alignment
| Check | Requirement | Severity |
|-------|-------------|----------|
| Positive | "Do X" not "Don't do Y" | HIGH |
| Schemas | JSON output format specified | HIGH |
| CoT | CRITICAL-HIGH use 4-step reasoning | MEDIUM |
| Self-consistency | CRITICAL uses multi-path validation | MEDIUM |
| Placeholders | All examples use `{placeholder}` | HIGH |
| Read-First | Commands read files before editing | CRITICAL |
| No-Hallucination | Verify APIs/methods exist before use | CRITICAL |
| Plan-Before-Act | Complex operations have planning phase | HIGH |

### 10.2 Model Selection
| Check | Requirement | Severity |
|-------|-------------|----------|
| Opus for coding | cco-optimize, cco-commit | HIGH |
| Haiku for scanning | cco-agent-analyze | MEDIUM |
| Documented | Each command shows model in docs | MEDIUM |

### 10.3 Anti-Overengineering
| Check | Requirement | Severity |
|-------|-------------|----------|
| No BC hacks | Zero `backward`, `compat`, `legacy` | HIGH |
| No fallbacks | Zero `fallback`, `deprecated` | HIGH |
| No TODOs | Zero `TODO`, `FIXME`, `XXX` | MEDIUM |
| Purpose | Each component has documented purpose | MEDIUM |
| Simplicity | Simple commands remain simple | HIGH |

---

## Reasoning Strategies

### Step-Back (Before Each Category)
Ask: "What is the purpose of this component type?"

### Chain of Thought (Each Finding)
```
1. Identify: What exactly is the issue?
2. Impact: What does this affect?
3. Evidence: What confirms this?
4. Severity: Based on evidence, what level?
```

### Self-Consistency (CRITICAL Only)
```
Path A: Analyze as if CCO is broken
Path B: Analyze as if CCO works correctly
Consensus: Both agree → confirm CRITICAL. Disagree → downgrade to HIGH
```

---

## Output Format

```
═══════════════════════════════════════════════════════════
                     CCO FULL REVIEW
═══════════════════════════════════════════════════════════

Detected:
  Commands: {n}  Agents: {n}  Rules: {n} (C:{n} + A:{n} + Ad:{n})

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
│ TOTAL (129 checks)      │   {n}  │   {n}  │  {st}  │
└─────────────────────────┴────────┴────────┴────────┘

{if findings}
## 80/20 Prioritized Findings

### Do Now (CRITICAL + HIGH, auto-fixable)
  [{SEVERITY}] {category}.{check}: {issue}
    Location: {file}:{line}
    Fix: {action}

### Plan (HIGH, manual intervention needed)
  ...

### Consider (MEDIUM)
  ...

### Backlog (LOW)
  ...

Summary: C:{n} H:{n} M:{n} L:{n}
Accounting: doNow:{n} + plan:{n} + consider:{n} + backlog:{n} = total:{n}
{/if}
═══════════════════════════════════════════════════════════
```

---

## Flags

| Flag | Effect |
|------|--------|
| `--quick` | CRITICAL and HIGH only, haiku model, skip MEDIUM/LOW |
| `--focus=X` | Single category: 1-10 or name |
| `--fix` | Auto-apply safe fixes (doc count updates, terminology) |
| `--fix-all` | Apply all fixes including manual ones (with confirmation) |
| `--report` | Report only, no fixes applied |

### Apply Modes

```javascript
if (args.includes("--fix-all")) {
  // Everything mode: apply all findings
  toApply = [...doNow, ...plan, ...consider, ...backlog]
} else if (args.includes("--fix")) {
  // Safe mode: auto-fixable only
  toApply = doNow.filter(f => f.autoFixable)
} else {
  // Report mode: no fixes
  toApply = []
}
```

---

## Anti-Overengineering Guard

Before flagging ANY missing element:
1. Does absence break something?
2. Does absence confuse users?
3. Is adding it worth complexity cost?

**All NO → not a finding.**

NON-findings:
- Simple command without TodoWrite
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

1. **Context first** - Verify CCO repo accessible before analysis
2. **Parallel batches** - Categories 1-5 and 6-10 run in parallel
3. **Dynamic counts** - Detect actual counts, never hardcode
4. **80/20 prioritization** - Do Now before Plan before Consider
5. **Evidence required** - Every finding needs file:line reference
6. **Anti-overengineering** - Apply 3-question test before flagging
7. **Self-consistency** - CRITICAL findings need dual-path validation

---

## Accounting

**Invariant:** `passed + failed = total` (per category and overall)

```javascript
// Verify at end of each category
assert(category.passed + category.failed === category.totalChecks,
  `Category ${name}: ${passed} + ${failed} != ${totalChecks}`)

// Verify overall
assert(allCategories.reduce((sum, c) => sum + c.passed, 0) +
       allCategories.reduce((sum, c) => sum + c.failed, 0) === 129,
  "Total checks must equal 129")
```
