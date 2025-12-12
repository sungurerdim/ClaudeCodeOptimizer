---
name: cco-status
description: Project health dashboard
allowed-tools: Read(*), Grep(*), Glob(*), Bash(git:*), Bash(pytest:*), Bash(npm:*), Task(*), TodoWrite
---

# /cco-status

**Health Dashboard** - Single view of project health with trends and actionable next steps.

Read-only metrics collection and visualization.

**Rules:** User Input | Output Format | Conservative Scoring | Task Tracking

## Context

- Context check: !`test -f ./.claude/rules/cco/context.md && echo "1" || echo "0"`

**Static context (Applicable, Scale, Type, Team, Data, Coverage) is read from ./CLAUDE.md already in context.**

## Context Requirement [CRITICAL]

**This command requires CCO context in ./.claude/rules/cco/context.md.**

If context check returns "0":
```
CCO context not found.

Run /cco-config first to configure project context, then restart CLI.
```
**Stop execution immediately.**

## Context Application

| Field | Effect |
|-------|--------|
| Applicable | Only show scores for applicable categories from context |
| Scale | <100 → relaxed thresholds; 100-10K → moderate; 10K+ → strict |
| Type | API: response time; CLI: startup time; Library: coverage + API stability |
| Team | Solo → simplified view; 6+ → add collaboration metrics |
| Maturity | Legacy → weight stability higher; Greenfield → weight velocity higher |
| Priority | Speed → highlight blockers only; Quality → show all metrics |
| Data | PII/Regulated → security score weight ×2 |

## Execution Optimization

<use_parallel_tool_calls>
When calling multiple tools with no dependencies between them, make all independent
calls in a single message. For example:
- Multiple cco-agent-analyze scopes → launch simultaneously
- Multiple file reads → batch in parallel
- Multiple grep searches → parallel calls

Never use placeholders or guess missing parameters.
</use_parallel_tool_calls>

## Agent Integration

| Phase | Agent | Scope | Purpose |
|-------|-------|-------|---------|
| Metrics | `cco-agent-analyze` | `scan` | Collect current metrics |
| Trends | `cco-agent-analyze` | `trends` | Historical comparison |

**Trend Tracking:** Use `cco-agent-analyze` with `scope: trends` to get historical metrics and delta indicators (↑↓→⚠). Trends are derived from git history and tags.

## Flow

Per Command Flow rule (read-only, no fixes).

## Score Categories (0-100)

### Security
- Vulnerabilities (OWASP, CVEs)
- Secrets exposure
- Dependency health
- Input validation coverage

### Tests
- Line coverage percentage
- Branch coverage
- Test quality (assertions, mocks)
- Edge case coverage

### Tech Debt
- Complexity score (cyclomatic)
- Dead code percentage
- TODO/FIXME count
- Hardcoded values
- Type coverage

### Cleanliness
- Orphan count (files, functions, imports)
- Stale reference count
- Duplicate percentage
- Redundancy score

### Documentation
- README completeness
- Docstring coverage
- Example validity
- API documentation (if applicable)

### Self-Compliance
- Standards adherence
- Convention consistency
- Guideline violations

## Trends

Track changes over time:

| Metric | Tracking |
|--------|----------|
| Last run | Previous health check results |
| Week over week | 7-day comparison |
| Degradation alerts | Score drops >5% flagged |
| Velocity | Issues fixed per period |

Storage: Git tags and commit history (no separate files)

### Trend Indicators

| Symbol | Meaning |
|--------|---------|
| `↑` | Improved since last check |
| `↓` | Degraded since last check |
| `→` | Unchanged |
| `⚠` | Significant degradation (>5%) |

## Fix First

Top 3 actionable items prioritized by:
- Highest impact
- Lowest effort
- Specific file:line locations
- Estimated fix time

## Comparisons

### vs Thresholds

| Score | Status | Meaning |
|-------|--------|---------|
| 90-100 | OK | Excellent |
| 70-89 | WARN | Needs attention |
| 50-69 | FAIL | Action required |
| 0-49 | CRITICAL | Immediate action |

### vs Benchmarks (when available)

Compare against:
- Industry averages (by project type)
- Similar projects (by stack/scale)
- Project's own historical best

## Output

**Follow output formats precisely.**

### Header
```
┌─ PROJECT HEALTH ─────────────────────────────────────────────┐
│ Project: {project} {version}                                 │
│ Team: {team} | Scale: {scale} | Type: {type}                 │
│ Last Check: {date} {time} | Trend: {trend_icon} {trend_text} │
└──────────────────────────────────────────────────────────────┘
```

### Scores Dashboard
```
┌─ HEALTH SCORES ──────────────────────────────────────────────┐
│ Category      │ Score │ Bar        │ Trend │ Status          │
├───────────────┼───────┼────────────┼───────┼─────────────────┤
│ Security      │ {n}   │ {bar}      │ {t}   │ {status}        │
│ Tests         │ {n}   │ {bar}      │ {t}   │ {status}        │
│ Tech Debt     │ {n}   │ {bar}      │ {t}   │ {status}        │
│ Cleanliness   │ {n}   │ {bar}      │ {t}   │ {status}        │
│ Documentation │ {n}   │ {bar}      │ {t}   │ {status}        │
│ Self-Compliance│ {n}  │ {bar}      │ {t}   │ {status}        │
├───────────────┼───────┼────────────┼───────┼─────────────────┤
│ OVERALL       │ {n}   │ {bar}      │ {t}   │ {status}        │
└───────────────┴───────┴────────────┴───────┴─────────────────┘
```

### Category Breakdown (when --focus used)
```
┌─ {CATEGORY} BREAKDOWN ───────────────────────────────────────┐
│ Metric          │ Value    │ Threshold │ Status              │
├─────────────────┼──────────┼───────────┼─────────────────────┤
│ {metric_name}   │ {value}  │ {thresh}  │ {status}            │
│ ...             │ ...      │ ...       │ ...                 │
└─────────────────┴──────────┴───────────┴─────────────────────┘
```

### Fix First
```
┌─ FIX FIRST (highest impact, lowest effort) ──────────────────┐
│ # │ Issue                    │ Location      │ Effort │ Impact│
├───┼──────────────────────────┼───────────────┼────────┼───────┤
│ 1 │ {issue_description}      │ {file}:{line} │ {time} │ {imp} │
│ 2 │ {issue_description}      │ {file}:{line} │ {time} │ {imp} │
│ ...                                                           │
└───┴──────────────────────────┴───────────────┴────────┴───────┘
```

### Trend History (when --trends used)
```
┌─ TREND HISTORY ──────────────────────────────────────────────┐
│ Date       │ Overall │ Security │ Tests │ Debt │ Clean      │
├────────────┼─────────┼──────────┼───────┼──────┼────────────┤
│ {date}     │ {n} {t} │ {n} {t}  │ {n}{t}│ {n}{t}│ {n} {t}   │
│ ...        │ ...     │ ...      │ ...   │ ...  │ ...        │
└────────────┴─────────┴──────────┴───────┴──────┴────────────┘
```

## Flags

| Flag | Effect |
|------|--------|
| `--focus=X` | Detailed breakdown for category (security, tests, debt, clean, docs) |
| `--trends` | Show historical trends |
| `--json` | Output as JSON for scripting |
| `--brief` | Summary only, no breakdown |

## Usage

```bash
/cco-status                     # Full dashboard
/cco-status --focus=security    # Security breakdown
/cco-status --focus=tests       # Test coverage breakdown
/cco-status --focus=debt        # Tech debt breakdown
/cco-status --focus=clean       # Cleanliness breakdown
/cco-status --trends            # Show trend history
/cco-status --brief             # Quick summary
```

## Related Commands

- `/cco-optimize` - Fix security and quality issues
- `/cco-optimize` - Fix cleanliness issues
- `/cco-checkup` - Full maintenance routine

---

## Behavior Rules

### User Input [CRITICAL]

- **AskUserQuestion**: ALL user decisions MUST use this tool
- **Separator**: Use semicolon (`;`) to separate options
- **Prohibited**: Never use plain text questions ("Would you like...", "Should I...")

### Output Format

- **Scores**: 0-100 range, right-aligned
- **Status**: OK (≥80) | WARN (60-79) | FAIL (<60)
- **Progress**: `████░░░░` (8 chars, filled = score/100*8)
- **No modification**: This is READ-ONLY analysis

### Conservative Scoring

- **Lower**: When uncertain, score conservatively
- **Evidence**: Require explicit metrics, not inference
- **Trends**: Show improvement/degradation objectively

### Task Tracking

- **Create**: TODO list with analysis categories
- **Status**: pending → in_progress → completed
- **Accounting**: analyzed + skipped = total
