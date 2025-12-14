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

## Context

- Context check: !`test -f ./.claude/rules/cco/context.md && echo "1" || echo "0"`
- Git status: !`git status --short`

**Static context (Tools, Stack, Maturity) from ./CLAUDE.md already in context.**

## Context Requirement [CRITICAL]

If context check returns "0": `CCO context not found. Run /cco-config first.` **Stop immediately.**

## User Input

| Question | Options | MultiSelect |
|----------|---------|-------------|
| Scope? | Security (Recommended); Quality (Recommended); Hygiene; Best Practices | true |
| Action? | Report Only; Auto-fix (Recommended); Interactive | false |

## Progress Tracking [CRITICAL]

```
TodoWrite([
  { content: "Analyze codebase", status: "in_progress", activeForm: "Analyzing codebase" },
  { content: "Apply safe fixes", status: "pending", activeForm: "Applying safe fixes" },
  { content: "Request approval", status: "pending", activeForm: "Requesting approval" },
  { content: "Show summary", status: "pending", activeForm: "Showing summary" }
])
```

## Token Efficiency [CRITICAL]

Single analyze agent │ Single apply agent │ Linter-first │ Batch calls │ Targeted reads

## Execution Flow

| Step | Action |
|------|--------|
| 1. Analyze | `Task(cco-agent-analyze, scopes=[...])` → Combined findings JSON |
| 2. Deduplicate | Group by root cause |
| 3. Apply safe | `Task(cco-agent-apply, fixes=[...safe...])` → Parallel batches |
| 4. Approval | AskUserQuestion for approval-required (paginated, max 4/page) |
| 5. Summary | Applied + Declined counts, verification status |

**CRITICAL:** ONE analyze agent, ONE apply agent. Never per-scope or per-fix.

## Scope Coverage

| Scope | Checks |
|-------|--------|
| `security` | OWASP, secrets, CVEs, input validation |
| `quality` | Tech debt, type errors, test gaps |
| `hygiene` | Orphans, stale refs, duplicates |
| `best-practices` | Patterns, efficiency, consistency |

## Approval Flow [CRITICAL]

**Paginated AskUserQuestion (max 4 per page):**
```
Question: "Fix {category}? (Page 1/2)"
Options: "{ID}: {title}" → "{file}:{line} - {fix}"
MultiSelect: true
```

After approval: Apply → Verify → Fix cascade errors if any

## Context Application

| Field | Effect |
|-------|--------|
| Data | PII/Regulated → security ×2 |
| Scale | 10K+ → stricter |
| Maturity | Legacy → safe only |
| Priority | Speed → critical; Quality → all |

## Flags

| Flag | Effect |
|------|--------|
| `--security` | Security only |
| `--quality` | Quality only |
| `--hygiene` | Hygiene only |
| `--best-practices` | Best practices only |
| `--report` | No fixes |
| `--fix` | Auto-fix safe (default) |
| `--fix-all` | Fix all with approval |
| `--critical` | Security + tests |
| `--pre-release` | All scopes, strict |

## Strategy Evolution

| Pattern | Action |
|---------|--------|
| Same issue 3+ files | Add to `Systemic` |
| Fix caused cascade | Add to `Avoid` |
| Effective pattern | Add to `Prefer` |
