---
name: cco-optimize
description: Security and code quality analysis with auto-fix
allowed-tools: Read(*), Grep(*), Glob(*), Edit(*), Bash(git:*), Task(*), TodoWrite, AskUserQuestion
---

# /cco-optimize

**Full-Stack Optimization** - Security + Quality + Hygiene via parallel agents.

## Context Requirement

```
test -f ./.claude/rules/cco/context.md && echo "OK" || echo "Run /cco-config first"
```

If not found: Stop immediately with message to run /cco-config.

## User Input

When called without flags:

| Question | Options | MultiSelect |
|----------|---------|-------------|
| Scope? | Security; Quality; Hygiene; All (Recommended) | true |
| Action? | Report Only; Auto-fix (Recommended); Interactive | false |

## Execution Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 1: Spawn parallel agents (single message with 3 Task calls)            │
├─────────────────────────────────────────────────────────────────────────────┤
│ Task(cco-agent-analyze, scope=security)  ──┐                                │
│ Task(cco-agent-analyze, scope=quality)   ──┼──→ All run simultaneously      │
│ Task(cco-agent-analyze, scope=hygiene)   ──┘                                │
├─────────────────────────────────────────────────────────────────────────────┤
│ STEP 2: Collect JSON results from all agents                                │
├─────────────────────────────────────────────────────────────────────────────┤
│ STEP 3: Merge findings, deduplicate by root cause                           │
├─────────────────────────────────────────────────────────────────────────────┤
│ STEP 4: Apply fixes via Task(cco-agent-apply) or show report                │
├─────────────────────────────────────────────────────────────────────────────┤
│ STEP 5: Show summary                                                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

**CRITICAL:** Step 1 MUST be a single message with multiple Task tool calls.

## Agent Scopes

| Agent | Scope | Returns |
|-------|-------|---------|
| cco-agent-analyze | `security` | OWASP, secrets, CVEs, input validation |
| cco-agent-analyze | `quality` | Tech debt, consistency, test gaps |
| cco-agent-analyze | `hygiene` | Orphans, stale refs, duplicates |
| cco-agent-apply | `fix` | Execute approved fixes |

## Context Application

| Field | Effect |
|-------|--------|
| Data | PII/Regulated → security weight ×2 |
| Scale | 10K+ → stricter thresholds |
| Maturity | Legacy → safe fixes only |
| Priority | Speed → critical only; Quality → all levels |

## Findings Processing

### Deduplication
- Same CWE + Same File → merge
- Same CWE + Related Files → group by root cause

### Priority (OWASP Risk Rating)
```
Risk = Likelihood × Impact
P0 (90-100): Fix within 24h
P1 (70-89): Fix within 1 week
P2 (50-69): Fix within 1 month
P3 (<50): Backlog
```

## Fix Modes

| Mode | Behavior |
|------|----------|
| Report Only | No changes |
| Auto-fix | Fix safe issues, ask for risky |
| Interactive | Ask for each |

**Safe fixes:** Formatting, unused imports, simple refactors
**Risky fixes:** Deletions, API changes, security patches

## Output

```
┌─ OPTIMIZATION SUMMARY ───────────────────────────────────────┐
│ Category      │ Score │ Issues │ Fixed │ Status              │
├───────────────┼───────┼────────┼───────┼─────────────────────┤
│ Security      │ {n}%  │ {n}    │ {n}   │ {OK|WARN|FAIL}      │
│ Quality       │ {n}%  │ {n}    │ {n}   │ {OK|WARN|FAIL}      │
│ Hygiene       │ {n}%  │ {n}    │ {n}   │ {OK|WARN|FAIL}      │
├───────────────┼───────┼────────┼───────┼─────────────────────┤
│ OVERALL       │ {n}%  │ {n}    │ {n}   │ {status}            │
└───────────────┴───────┴────────┴───────┴─────────────────────┘

Applied: {n} | Skipped: {n} | Manual: {n}
```

## Flags

| Flag | Effect |
|------|--------|
| `--security` | Security scope only |
| `--quality` | Quality scope only |
| `--hygiene` | Hygiene scope only |
| `--report` | No fixes |
| `--fix` | Auto-fix safe (default) |
| `--critical` | Security + tests only |
| `--pre-release` | Security + quality + consistency |
