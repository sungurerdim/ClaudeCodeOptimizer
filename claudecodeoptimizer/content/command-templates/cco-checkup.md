---
name: cco-checkup
description: Regular maintenance routine
allowed-tools: Read(*), Grep(*), Glob(*), Edit(*), Bash(git:*), Bash(pytest:*), Task(*), TodoWrite
---

# /cco-checkup

**Maintenance Routine** - Health check → smart audit → quick cleanup.

Meta command for regular project maintenance (weekly recommended).

**Rules:** User Input | Orchestration | Progress Tracking

## Context

- Context check: !`test -f ./.claude/rules/cco/context.md && echo "1" || echo "0"`
- Last health tag: !`git tag -l "health-*" --sort=-creatordate | head -1 || echo "None"`
- Git status: !`git status --short`
- Recent activity: !`git log --oneline -5`

**Static context (Applicable) is read from ./CLAUDE.md already in context.**

## Context Requirement [CRITICAL]

**This command requires CCO context in ./.claude/rules/cco/context.md.**

If context check returns "0":
```
CCO context not found.

Run /cco-config first to configure project context, then restart CLI.
```
**Stop execution immediately.**

## Phase Selection

When called without flags → **AskUserQuestion** (mandatory):

| Question | Options | multiSelect |
|----------|---------|-------------|
| Which phases to run? | Health Dashboard (Recommended); Quality Audit (Recommended) | true |

*MultiSelect: User can select multiple phases. All selected = Full checkup.*

Flags `--health-only`, `--audit-only` skip this question.

## Progress Tracking [CRITICAL]

**Use TodoWrite to track progress.** Create todo list at start, update status for each phase.

```
TodoWrite([
  { content: "Run health dashboard", status: "in_progress", activeForm: "Running health dashboard" },
  { content: "Run quality audit", status: "pending", activeForm: "Running quality audit" },
  { content: "Show summary", status: "pending", activeForm: "Showing summary" }
])
```

**Update status:** Mark `completed` immediately after each phase finishes, mark next `in_progress`.

## Flow

### Phase 1: Health Dashboard

Orchestrates: `/cco-status --brief`

Quick overview of project health scores.

```
┌─ HEALTH CHECK ───────────────────────────────────────────────┐
│ → Running: /cco-status --brief                               │
├──────────────────────────────────────────────────────────────┤
│ Category      │ Score │ Trend │ Status                       │
├───────────────┼───────┼───────┼──────────────────────────────┤
│ Security      │ {n}   │ {t}   │ {status}                     │
│ Tests         │ {n}   │ {t}   │ {status}                     │
│ Tech Debt     │ {n}   │ {t}   │ {status}                     │
│ Cleanliness   │ {n}   │ {t}   │ {status}                     │
│ Documentation │ {n}   │ {t}   │ {status}                     │
├───────────────┼───────┼───────┼──────────────────────────────┤
│ OVERALL       │ {n}   │ {t}   │ {status}                     │
└───────────────┴───────┴───────┴──────────────────────────────┘
```

### Phase 2: Quality Audit

Orchestrates: `/cco-optimize --fix`

Runs all applicable checks (security, quality, hygiene, best-practices) from context.

```
┌─ QUALITY AUDIT ──────────────────────────────────────────────┐
│ → Running: /cco-optimize --fix                               │
├──────────────────────────────────────────────────────────────┤
│ Scopes: Security │ Quality │ Hygiene │ Best Practices        │
│ Issues found: {n} | Fixed: {n} | Declined: {n}               │
├──────────────────────────────────────────────────────────────┤
│ Orphans: {n} │ Stale refs: {n} │ Duplicates: {n}             │
└──────────────────────────────────────────────────────────────┘
```

### Summary

```
┌─ CHECKUP SUMMARY ────────────────────────────────────────────┐
│ Duration: {duration}                                         │
│ Last checkup: {time_ago}                                     │
├──────────────────────────────────────────────────────────────┤
│ Changes since last:                                          │
│   • {n} commits                                              │
│   • {n} files changed                                        │
│   • Health: {before} → {after} ({delta})                    │
├──────────────────────────────────────────────────────────────┤
│ Fixed: {n} issues | Declined: {n} issues                     │
├──────────────────────────────────────────────────────────────┤
│ Next recommended checkup: {date}                             │
└──────────────────────────────────────────────────────────────┘
```

## Comparison with Other Commands

| Need | Use |
|------|-----|
| Quick weekly maintenance | `/cco-checkup` |
| Pre-release checks | `/cco-preflight` |
| Deep quality audit | `/cco-optimize` |
| Strategic review | `/cco-review` |

## Flags

| Flag | Effect |
|------|--------|
| `--dry-run` | Show what would be done |
| `--no-fix` | Report only, don't fix |
| `--deep` | Run full audit + optimize instead of smart/hygiene |
| `--trends` | Show detailed trend history |

## Usage

```bash
/cco-checkup                   # Standard maintenance
/cco-checkup --dry-run         # Preview without changes
/cco-checkup --no-fix          # Report only
/cco-checkup --deep            # Thorough checkup
/cco-checkup --trends          # With trend history
```

## Scheduling Recommendation

| Frequency | Use Case |
|-----------|----------|
| Weekly | Active development |
| Bi-weekly | Stable projects |
| Before PR | Quality gate |
| Monthly | Maintenance mode |

## Related Commands

- `/cco-status` - Health dashboard only
- `/cco-optimize` - Full quality audit and optimization
- `/cco-preflight` - Pre-release workflow

---

## Behavior Rules

*Inherits: User Input rules from cco-tools.md*

### Orchestration

- **Delegate**: Run sub-commands, collect results
- **Aggregate**: Combine outputs into unified report
- **No-Duplicate**: Don't repeat work already done by sub-commands

### Progress Tracking

*See Progress Tracking section above. Use TodoWrite for all phases.*
