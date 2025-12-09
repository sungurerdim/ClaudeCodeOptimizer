---
name: cco-health
description: Project health dashboard with trends and actionable insights
allowed-tools: Read(*), Grep(*), Glob(*), Bash(git:*), Bash(pytest:*), Bash(npm:*), Task(*)
---

# /cco-health

**Health Dashboard** - Single view of project health with trends and actionable next steps.

Read-only metrics collection and visualization.

**Standards:** Command Flow | Output Formatting

## Context

- Context check: !`grep -c "CCO_ADAPTIVE_START" ./CLAUDE.md 2>/dev/null || echo "0"`

**Static context (Applicable, Scale, Type, Team, Data, Coverage) is read from ./CLAUDE.md already in context.**

## Context Requirement [CRITICAL]

**This command requires CCO_ADAPTIVE in ./CLAUDE.md.**

If context check returns "0":
```
CCO_ADAPTIVE not found in ./CLAUDE.md

Run /cco-tune first to configure project context, then restart CLI.
```
**Stop execution immediately.**

## Context Application

| Field | Effect |
|-------|--------|
| Applicable | Only show scores for applicable categories from context |
| Scale | <100 → relaxed thresholds; 100-10K → standard; 10K+ → strict |
| Type | API: response time; CLI: startup time; Library: coverage + API stability |
| Team | Solo → simplified view; 6+ → add collaboration metrics |
| Maturity | Legacy → weight stability higher; Greenfield → weight velocity higher |
| Priority | Speed → highlight blockers only; Quality → show all metrics |
| Data | PII/Regulated → security score weight ×2 |

## Agent Integration

| Phase | Agent | Scope | Purpose |
|-------|-------|-------|---------|
| Metrics | `cco-agent-analyze` | `scan` | Collect current metrics |
| Trends | `cco-agent-analyze` | `trends` | Historical comparison |

**Trend Tracking:** Use `cco-agent-analyze` with `scope: trends` to get historical metrics and delta indicators (↑↓→⚠). Trends are derived from git history and tags.

## Flow

Per Command Flow standard (read-only, no fixes).

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

### Header
```
┌─ PROJECT HEALTH ─────────────────────────────────────────────┐
│ Project: my-project v1.2.3                                   │
│ Team: Solo | Scale: Small | Type: CLI                        │
│ Last Check: 2025-12-07 14:30 | Trend: ↑ improving            │
└──────────────────────────────────────────────────────────────┘
```

### Scores Dashboard
```
┌─ HEALTH SCORES ──────────────────────────────────────────────┐
│ Category      │ Score │ Bar        │ Trend │ Status          │
├───────────────┼───────┼────────────┼───────┼─────────────────┤
│ Security      │ 95    │ █████████░ │ →     │ OK              │
│ Tests         │ 88    │ ████████░░ │ ↑     │ WARN            │
│ Tech Debt     │ 72    │ ███████░░░ │ ↓     │ WARN            │
│ Cleanliness   │ 85    │ ████████░░ │ ↑     │ WARN            │
│ Documentation │ 78    │ ███████░░░ │ →     │ WARN            │
│ Self-Compliance│ 90   │ █████████░ │ →     │ OK              │
├───────────────┼───────┼────────────┼───────┼─────────────────┤
│ OVERALL       │ 85    │ ████████░░ │ ↑     │ WARN            │
└───────────────┴───────┴────────────┴───────┴─────────────────┘
```

### Category Breakdown (when --focus used)
```
┌─ TECH DEBT BREAKDOWN ────────────────────────────────────────┐
│ Metric          │ Value    │ Threshold │ Status              │
├─────────────────┼──────────┼───────────┼─────────────────────┤
│ Avg Complexity  │ 8.2      │ <10       │ OK                  │
│ Max Complexity  │ 15       │ <15       │ WARN                │
│ Dead Code       │ 2.3%     │ <5%       │ OK                  │
│ TODOs           │ 12       │ <20       │ OK                  │
│ Hardcoded       │ 5        │ <10       │ OK                  │
│ Type Coverage   │ 78%      │ >80%      │ WARN                │
└─────────────────┴──────────┴───────────┴─────────────────────┘
```

### Fix First
```
┌─ FIX FIRST (highest impact, lowest effort) ──────────────────┐
│ # │ Issue                    │ Location      │ Effort │ Impact│
├───┼──────────────────────────┼───────────────┼────────┼───────┤
│ 1 │ High complexity (15)     │ utils.py:42   │ 30min  │ HIGH  │
│ 2 │ Missing type annotations │ api.py:15-30  │ 15min  │ MEDIUM│
│ 3 │ Orphan function          │ helpers.py:88 │ 5min   │ LOW   │
└───┴──────────────────────────┴───────────────┴────────┴───────┘
```

### Trend History (when --trends used)
```
┌─ TREND HISTORY ──────────────────────────────────────────────┐
│ Date       │ Overall │ Security │ Tests │ Debt │ Clean      │
├────────────┼─────────┼──────────┼───────┼──────┼────────────┤
│ 2025-12-08 │ 85 ↑    │ 95 →     │ 88 ↑  │ 72 ↓ │ 85 ↑       │
│ 2025-12-01 │ 82      │ 95       │ 85    │ 75   │ 80         │
│ 2025-11-24 │ 80      │ 92       │ 82    │ 78   │ 78         │
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
/cco-health                     # Full dashboard
/cco-health --focus=security    # Security breakdown
/cco-health --focus=tests       # Test coverage breakdown
/cco-health --focus=debt        # Tech debt breakdown
/cco-health --focus=clean       # Cleanliness breakdown
/cco-health --trends            # Show trend history
/cco-health --brief             # Quick summary
```

## Related Commands

- `/cco-audit` - Fix security and quality issues
- `/cco-optimize` - Fix cleanliness issues
- `/cco-checkup` - Full maintenance routine
