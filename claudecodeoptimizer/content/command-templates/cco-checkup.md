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

- Context check: !`grep -c "CCO_ADAPTIVE_START" ./CLAUDE.md 2>/dev/null || echo "0"`
- Last health tag: !`git tag -l "health-*" --sort=-creatordate | head -1 || echo "None"`
- Git status: !`git status --short`
- Recent activity: !`git log --oneline -5`

**Static context (Applicable) is read from ./CLAUDE.md already in context.**

## Context Requirement [CRITICAL]

**This command requires CCO_ADAPTIVE in ./CLAUDE.md.**

If context check returns "0":
```
CCO_ADAPTIVE not found in ./CLAUDE.md

Run /cco-tune first to configure project context, then restart CLI.
```
**Stop execution immediately.**

## Flow

### Phase 1: Health Dashboard

Orchestrates: `/cco-health --brief`

Quick overview of project health scores.

```
┌─ HEALTH CHECK ───────────────────────────────────────────────┐
│ → Running: /cco-health --brief                               │
├──────────────────────────────────────────────────────────────┤
│ Category      │ Score │ Trend │ Status                       │
├───────────────┼───────┼───────┼──────────────────────────────┤
│ Security      │ 95    │ →     │ OK                           │
│ Tests         │ 88    │ ↑     │ WARN                         │
│ Tech Debt     │ 82    │ ↓     │ WARN                         │
│ Cleanliness   │ 90    │ ↑     │ OK                           │
│ Documentation │ 78    │ →     │ WARN                         │
├───────────────┼───────┼───────┼──────────────────────────────┤
│ OVERALL       │ 87    │ →     │ WARN                         │
└───────────────┴───────┴───────┴──────────────────────────────┘
```

### Phase 2: Quality Audit

Orchestrates: `/cco-audit --auto-fix`

Runs all applicable checks from context.

```
┌─ QUALITY AUDIT ──────────────────────────────────────────────┐
│ → Running: /cco-audit --auto-fix                             │
├──────────────────────────────────────────────────────────────┤
│ Applicable: security, tech-debt, tests, self-compliance     │
│ Issues found: 3 | Auto-fixed: 2 | Manual: 1                 │
├──────────────────────────────────────────────────────────────┤
│ Manual action needed:                                        │
│   • HIGH: Complexity 12 in utils.py:42 (refactor needed)    │
└──────────────────────────────────────────────────────────────┘
```

### Phase 3: Quick Cleanup

Orchestrates: `/cco-optimize --hygiene --auto-fix`

Removes orphans, stale refs, and duplicates.

```
┌─ QUICK CLEANUP ──────────────────────────────────────────────┐
│ → Running: /cco-optimize --hygiene --auto-fix                │
├──────────────────────────────────────────────────────────────┤
│ Orphans removed: 1 (unused_helper.py)                       │
│ Stale refs fixed: 2                                          │
│ Duplicates merged: 0                                         │
├──────────────────────────────────────────────────────────────┤
│ Space saved: 45 lines                                        │
└──────────────────────────────────────────────────────────────┘
```

### Summary

```
┌─ CHECKUP SUMMARY ────────────────────────────────────────────┐
│ Duration: 45 seconds                                         │
│ Last checkup: 7 days ago                                     │
├──────────────────────────────────────────────────────────────┤
│ Changes since last:                                          │
│   • 12 commits                                               │
│   • 8 files changed                                          │
│   • Health: 85 → 87 (+2)                                    │
├──────────────────────────────────────────────────────────────┤
│ Auto-fixed: 3 issues                                         │
│ Manual needed: 1 issue                                       │
├──────────────────────────────────────────────────────────────┤
│ Next recommended checkup: 2025-12-15                        │
└──────────────────────────────────────────────────────────────┘
```

## Comparison with Other Commands

| Need | Use |
|------|-----|
| Quick weekly maintenance | `/cco-checkup` |
| Pre-release checks | `/cco-release` |
| Deep quality audit | `/cco-audit --all` |
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

- `/cco-health` - Health dashboard only
- `/cco-audit` - Full quality audit
- `/cco-optimize` - Full optimization
- `/cco-release` - Pre-release workflow

---

## Behavior Rules

### User Input [CRITICAL]

- **AskUserQuestion**: ALL user decisions MUST use this tool
- **Separator**: Use semicolon (`;`) to separate options
- **Prohibited**: Never use plain text questions ("Would you like...", "Should I...")

### Orchestration

- **Delegate**: Run sub-commands, collect results
- **Aggregate**: Combine outputs into unified report
- **No-Duplicate**: Don't repeat work already done by sub-commands

### Task Tracking

- **Create**: TODO list with checkup phases
- **Status**: pending → in_progress → completed
- **Accounting**: health + audit + optimize = total
