---
name: cco-health
description: Actionable metrics dashboard
---

# /cco-health

**Process visibility** - Single view of project health with actionable next steps.

**Standards:** Context Read | Approval Flow | Error Format

## Context Application
- **Applicable** - Only show relevant scores from Operational section
- **Scale** - Adjust thresholds: <100 (relaxed), 100-10K (standard), 10K+ (strict)
- **Type** - Emphasize relevant metrics: API (response time), CLI (startup), library (coverage)

## Scores (0-100)

- **Security** - Based on vulnerabilities found
- **Tests** - Coverage percentage + quality
- **Tech Debt** - Complexity, dead code, duplication
- **Hygiene** - TODOs, orphans, hardcoded values
- **AI Quality** - AI code patterns (if applicable)
- **Self-Compliance** - Alignment with stated rules

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
/cco-health --focus security    # Focus on specific score
/cco-health --focus tests
/cco-health --focus tech-debt
```
