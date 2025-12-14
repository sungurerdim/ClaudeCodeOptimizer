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

## Dynamic Context (Pre-collected)

- Context check: !`test -f ./.claude/rules/cco/context.md && echo "1" || echo "0"`
- Git status: !`git status --short`

**DO NOT re-run these commands. Use the pre-collected values above.**
**Static context (Tools, Stack, Maturity) is read from ./CLAUDE.md already in context.**

## Context Requirement [CRITICAL]

**This command requires CCO context in ./.claude/rules/cco/context.md.**

If context check returns "0":
```
CCO context not found.

Run /cco-config first to configure project context, then restart CLI.
```
**Stop execution immediately.**

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
  { content: "Analyze codebase", status: "in_progress", activeForm: "Analyzing codebase" },
  { content: "Apply safe fixes", status: "pending", activeForm: "Applying safe fixes" },
  { content: "Request approval", status: "pending", activeForm: "Requesting approval" },
  { content: "Show summary", status: "pending", activeForm: "Showing summary" }
])
```

**Update status:** Mark `completed` immediately after each step finishes, mark next `in_progress`.

## Token Efficiency [CRITICAL]

| Rule | Implementation |
|------|----------------|
| **Single agent** | One analyze agent with all scopes, one apply agent with all fixes |
| **Linter-first** | Run linters before grep - skip patterns linters catch |
| **Batch calls** | Multiple tool calls in single message |
| **Targeted reads** | Use offset/limit for large files |

## Execution Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. Spawn SINGLE analyze agent with ALL selected scopes                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ Task(cco-agent-analyze, scopes=[security, quality, hygiene, best-practices]) │
│ → Agent runs linters first, then targeted greps per scope                    │
│ → Returns combined JSON with all findings                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. Deduplicate findings by root cause                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. Spawn SINGLE apply agent with ALL safe fixes                              │
│ Task(cco-agent-apply, fixes=[...all safe fixes...])                          │
│ → Agent applies all in parallel batches, verifies after each                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. AskUserQuestion for approval-required fixes (paginated, max 4 per page)   │
│ → If any approved, Task(cco-agent-apply, fixes=[...approved...])             │
├─────────────────────────────────────────────────────────────────────────────┤
│ 5. Show summary                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**CRITICAL:** Use ONE analyze agent and ONE apply agent. Never spawn per-scope or per-fix agents.

## Agent Usage

| Agent | Input | Output |
|-------|-------|--------|
| cco-agent-analyze | `scopes: [security, quality, ...]` | Combined findings JSON |
| cco-agent-apply | `fixes: [finding1, finding2, ...]` | Results + verification |

### Scope Coverage

| Scope | Checks |
|-------|--------|
| `security` | OWASP, secrets, CVEs, input validation |
| `quality` | Tech debt, type errors, test gaps |
| `hygiene` | Orphans, stale refs, duplicates |
| `best-practices` | Patterns, efficiency, consistency |

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
- {lint_command}: {PASS|FAIL}
- {type_command}: {PASS|FAIL}
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

## Strategy Evolution

After optimization, update `.claude/rules/cco/context.md` Learnings section:

| Pattern | Action |
|---------|--------|
| Same issue in 3+ files | Add to `Systemic`: root cause + recommendation |
| Fix caused cascade errors | Add to `Avoid`: pattern + what works instead |
| Effective fix pattern | Add to `Prefer`: pattern + impact level |

**Max items:** 5 per category (remove oldest when full)
