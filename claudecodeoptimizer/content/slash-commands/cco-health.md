---
name: cco-health
description: Actionable metrics dashboard
---

# /cco-health

**Metrics dashboard** - Single view of project health with actionable next steps.

**Standards:** Command Flow | Output Formatting

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

## Flow

Per Command Flow standard (read-only, no fixes).

## Scores (0-100)

- **Security** - Vulnerabilities, secrets, dependencies, AI security
- **Tests** - Coverage percentage + quality
- **Tech Debt** - Complexity, dead code, duplication, orphans, TODOs, AI patterns
- **Self-Compliance** - Alignment with stated standards

## Fix First Indicator

After scores, show top 3 actionable items:
- Highest impact, lowest effort
- With specific file:line locations

## Output

**Standards:** Output Formatting

Tables:
1. **Header** - Project name, version, team/scale/type
2. **Scores** - Category | Score | Bar + Summary (per applicable category + OVERALL)
3. **Breakdown** - Metric | Value | Status (nested under categories)
4. **Fix First** - # | Issue | Location | Effort (top 3 actionable)

## Usage

```bash
/cco-health                     # Full dashboard
/cco-health --focus=security    # Focus on security score
/cco-health --focus=tests       # Focus on test coverage
/cco-health --focus=tech-debt   # Focus on tech debt
```
