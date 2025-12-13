---
name: cco-optimize
description: Security and code quality analysis with auto-fix
allowed-tools: Read(*), Grep(*), Glob(*), Edit(*), Bash(git:*), Bash(ruff:*), Bash(mypy:*), Bash(pip:*), Task(*), TodoWrite, AskUserQuestion
---

# /cco-optimize

**Full-Stack Optimization** - Detect and fix ALL issues, leave nothing behind.

## Core Principle [CRITICAL]

**Fix everything that can be fixed.** There is no "manual review" category. All issues fall into:
1. **Auto-fix**: Safe to apply without asking
2. **Approval Required**: Ask user, then fix if approved

If an issue can be fixed by editing code, it MUST be fixed (with approval if needed).

## Context Requirement

```
test -f ./.claude/rules/cco/context.md && echo "OK" || echo "Run /cco-config first"
```

If not found: Stop immediately with message to run /cco-config.

## User Input

When called without flags:

| Question | Options | MultiSelect |
|----------|---------|-------------|
| Scope? | Security (Recommended); Quality (Recommended); Hygiene; Best Practices | true |
| Action? | Report Only; Auto-fix (Recommended); Interactive | false |

## Progress Tracking [CRITICAL]

**Use TodoWrite to track progress.** Create todo list at start, update status for each step.

```
TodoWrite([
  { content: "Spawn parallel agents", status: "in_progress", activeForm: "Spawning parallel agents" },
  { content: "Collect results", status: "pending", activeForm: "Collecting results" },
  { content: "Merge & deduplicate", status: "pending", activeForm: "Merging & deduplicating" },
  { content: "Apply safe fixes", status: "pending", activeForm: "Applying safe fixes" },
  { content: "Request approval for remaining", status: "pending", activeForm: "Requesting approval" },
  { content: "Show summary", status: "pending", activeForm: "Showing summary" }
])
```

**Update status:** Mark `completed` immediately after each step finishes, mark next `in_progress`.

## Execution Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ Spawn parallel agents (single message with selected scopes)                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ Task(cco-agent-analyze, scope=security)       ──┐                           │
│ Task(cco-agent-analyze, scope=quality)        ──┼──→ Run simultaneously     │
│ Task(cco-agent-analyze, scope=hygiene)        ──┤                           │
│ Task(cco-agent-analyze, scope=best-practices) ──┘                           │
├─────────────────────────────────────────────────────────────────────────────┤
│ Collect JSON results from all agents                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ Merge findings, deduplicate by root cause                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ Apply safe fixes via Task(cco-agent-apply)                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ AskUserQuestion for approval-required fixes (paginated)                      │
│ → If approved, apply fixes                                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ Show summary                                                                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

**CRITICAL:** Parallel agents MUST be spawned in a single message with multiple Task tool calls.

## Agent Scopes

| Agent | Scope | Returns |
|-------|-------|---------|
| cco-agent-analyze | `security` | OWASP, secrets, CVEs, input validation |
| cco-agent-analyze | `quality` | Tech debt, type errors, test gaps |
| cco-agent-analyze | `hygiene` | Orphans, stale refs, duplicates |
| cco-agent-analyze | `best-practices` | Patterns, efficiency, consistency |
| cco-agent-apply | `fix` | Execute approved fixes |

## Step 5: Approval Flow [CRITICAL]

When approval-required issues exist, present them in **paginated format** (max 4 per page):

### AskUserQuestion Format

```
| Question | Options (max 4) | MultiSelect |
|----------|-----------------|-------------|
| Fix {category}? | {issue1}; {issue2}; {issue3}; {issue4} | true |
```

**Pagination:** If >4 issues in a category, add pages:
- Page 1: Issues 1-4
- Page 2: Issues 5-8
- Continue until all issues shown

**Each option format:**
```
label: "{ID}: {short_title}"
description: "{location} - {fix_description}"
```

### Example

```
Question: "Fix security issues? (Page 1/2)"
Options:
  - "{SCOPE}-001: {title}" → "{file}:{line} - {fix_description}"
  - "{SCOPE}-002: {title}" → "{file}:{line} - {fix_description}"
  - "{SCOPE}-003: {title}" → "{file}:{line} - {fix_description}"
  - "{SCOPE}-004: {title}" → "{file}:{line} - {fix_description}"

Question: "Fix security issues? (Page 2/2)"
Options:
  - "{SCOPE}-005: {title}" → "{file}:{line} - {fix_description}"
```

### After Approval

For each approved issue:
1. Task(cco-agent-apply) to fix
2. Verify fix applied
3. Run relevant linter/type checker
4. If new errors introduced, fix those too

## Context Application

| Field | Effect |
|-------|--------|
| Data | PII/Regulated → security weight ×2 |
| Scale | 10K+ → stricter thresholds |
| Maturity | Legacy → safe fixes only |
| Priority | Speed → critical only; Quality → all levels |

## Output

```
┌─ OPTIMIZATION SUMMARY ───────────────────────────────────────┐
│ Category        │ Score │ Issues │ Fixed │ Status            │
├─────────────────┼───────┼────────┼───────┼───────────────────┤
│ Security        │ {n}%  │ {n}    │ {n}   │ {OK|WARN|FAIL}    │
│ Quality         │ {n}%  │ {n}    │ {n}   │ {OK|WARN|FAIL}    │
│ Hygiene         │ {n}%  │ {n}    │ {n}   │ {OK|WARN|FAIL}    │
│ Best Practices  │ {n}%  │ {n}    │ {n}   │ {OK|WARN|FAIL}    │
├─────────────────┼───────┼────────┼───────┼───────────────────┤
│ OVERALL         │ {n}%  │ {n}    │ {n}   │ {status}          │
└─────────────────┴───────┴────────┴───────┴───────────────────┘

Applied: {n} | Declined: {n}

Verification:
- ruff check: {PASS|FAIL}
- mypy --strict: {PASS|FAIL}
```

**No "Manual" category.** All issues either fixed or declined by user.

## Flags

| Flag | Effect |
|------|--------|
| `--security` | Security scope only |
| `--quality` | Quality scope only |
| `--hygiene` | Hygiene scope only |
| `--best-practices` | Best practices scope only |
| `--report` | No fixes |
| `--fix` | Auto-fix safe, ask for approval on rest (default) |
| `--fix-all` | Fix everything with approval |
| `--critical` | Security + tests only |
| `--pre-release` | All scopes, strict verification |
