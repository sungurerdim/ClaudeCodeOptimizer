---
name: cco-checkup
description: Regular maintenance routine
allowed-tools: Read(*), Grep(*), Glob(*), Edit(*), Bash(git:*), Bash(pytest:*), Task(*), TodoWrite
---

# /cco-checkup

**Maintenance Routine** - Health check → smart audit → quick cleanup.

Meta command for regular project maintenance (weekly recommended).

**Rules:** User Input | Orchestration | Task Tracking

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
| Which phases to run? | Health Dashboard (Recommended); Quality Audit (Recommended); Quick Cleanup | true |

*MultiSelect: Kullanıcı birden fazla faz seçebilir. Tümü seçilirse = Full checkup.*

Flags `--health-only`, `--audit-only`, `--cleanup-only` skip this question.

## Phase Announcements [CRITICAL]

**Before starting each phase, announce:** `▶ Phase X/3: Phase Name`

| Phase | Name |
|-------|------|
| 1 | Health Dashboard |
| 2 | Quality Audit |
| 3 | Quick Cleanup |

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

Orchestrates: `/cco-optimize --auto-fix`

Runs all applicable checks from context.

```
┌─ QUALITY AUDIT ──────────────────────────────────────────────┐
│ → Running: /cco-optimize --auto-fix                          │
├──────────────────────────────────────────────────────────────┤
│ Applicable: {applicable_categories}                          │
│ Issues found: {n} | Auto-fixed: {n} | Manual: {n}            │
├──────────────────────────────────────────────────────────────┤
│ Manual action needed:                                        │
│   • {priority}: {issue} in {file}:{line}                    │
└──────────────────────────────────────────────────────────────┘
```

### Phase 3: Quick Cleanup

Orchestrates: `/cco-optimize --hygiene --auto-fix`

Removes orphans, stale refs, and duplicates.

```
┌─ QUICK CLEANUP ──────────────────────────────────────────────┐
│ → Running: /cco-optimize --hygiene --auto-fix                │
├──────────────────────────────────────────────────────────────┤
│ Orphans removed: {n} ({files})                               │
│ Stale refs fixed: {n}                                        │
│ Duplicates merged: {n}                                       │
├──────────────────────────────────────────────────────────────┤
│ Space saved: {n} lines                                       │
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
│ Auto-fixed: {n} issues                                       │
│ Manual needed: {n} issues                                    │
├──────────────────────────────────────────────────────────────┤
│ Next recommended checkup: {date}                             │
└──────────────────────────────────────────────────────────────┘
```

## Comparison with Other Commands

| Need | Use |
|------|-----|
| Quick weekly maintenance | `/cco-checkup` |
| Pre-release checks | `/cco-preflight` |
| Deep quality audit | `/cco-optimize --all` |
| Thorough cleanup | `/cco-optimize --deep` |
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
- `/cco-optimize` - Full quality audit
- `/cco-optimize` - Full optimization
- `/cco-preflight` - Pre-release workflow

---

## Behavior Rules

*Inherits: User Input rules from cco-tools.md*

### Orchestration

- **Delegate**: Run sub-commands, collect results
- **Aggregate**: Combine outputs into unified report
- **No-Duplicate**: Don't repeat work already done by sub-commands

### Task Tracking

- **Create**: TODO list with checkup phases
- **Status**: pending → in_progress → completed
- **Accounting**: health + audit + optimize = total
