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

**DO NOT re-run these commands. Use the pre-collected values above.**
**Static context (Tools, Stack, Maturity) from ./CLAUDE.md already in context.**

## Context Requirement [CRITICAL]

If context check returns "0":
```
CCO context not found.

Run /cco-config first to configure project context, then restart CLI.
```
**Stop immediately.**

## User Input

| Question | Options | MultiSelect |
|----------|---------|-------------|
| Scope? | Security; Quality; Hygiene; Best Practices | true |
| Action? | Report Only; Auto-fix; Interactive | false |

**Dynamic labels:** AI adds `(Recommended)` based on project Data/Priority context.

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
| 1. Analyze | `Task(cco-agent-analyze, scopes=[...])` → findings JSON |
| 2. Show | Display findings summary to user (counts by scope/severity) |
| 3. Apply safe | `Task(cco-agent-apply, fixes=[...auto-fixable...])` |
| 4. Approval | **AskUserQuestion** for approval-required items (paginated) |
| 5. Apply approved | `Task(cco-agent-apply, fixes=[...user-approved...])` |
| 6. Summary | Applied + Declined counts, verification status |

**CRITICAL:**
- Agent returns findings → Command decides what to show/ask
- Auto-fix items: applied without asking (safe changes)
- Approval-required items: Command asks user via AskUserQuestion
- ONE analyze agent, ONE apply agent

## Scope Coverage

| Scope | Checks |
|-------|--------|
| `security` | OWASP, secrets, CVEs, input validation |
| `quality` | Tech debt, type errors, test gaps |
| `hygiene` | Orphans, stale refs, duplicates |
| `best-practices` | Patterns, efficiency, consistency |

## Impact Preview

For each fix, show impact before approval:
- **Direct**: Files to modify
- **Dependents**: Files that import/use
- **Tests**: Coverage of affected code
- **Risk**: LOW (auto-fix) / MEDIUM / HIGH (approval required)

## Approval Flow [CRITICAL]

When approval-required issues exist, present them in **paginated format** (max 4 per page):

```
Question: "Fix {category}? (Page 1/2)"
Options:
  - "{SCOPE}-001: {title}" → "{file}:{line} - {fix_description}"
  - "{SCOPE}-002: {title}" → "{file}:{line} - {fix_description}"
  ...
MultiSelect: true
```

**Pagination:** If >4 issues in category → add pages (Page 2/N, etc.)

**After user responds:**
- Selected items → `Task(cco-agent-apply, fixes=[...approved...])`
- Not selected → marked as `declined` in summary
- Agent verifies each fix → cascades if new errors introduced

## Context Application

| Field | Effect |
|-------|--------|
| Data | PII/Regulated → security ×2 |
| Scale | 10K+ → stricter |
| Maturity | Legacy → safe only |
| Priority | Speed → critical; Quality → all |

## Safety

| Check | Action |
|-------|--------|
| Dirty working tree | Prompt: Commit / Stash / Continue |
| Uncommitted changes | Warn before applying |
| Rollback | Clean git state enables `git checkout` |

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
