---
name: cco-health
description: Actionable metrics dashboard
---

# /cco-health

**Process visibility** - Single view of project health with actionable next steps.

## Project Context

**First:** Run `/cco-calibrate` to ensure context is loaded.

Read `CCO_CONTEXT_START` block from project root `CLAUDE.md` (NOT `.claude/CLAUDE.md`):
- **Applicable** - Only show relevant scores from Operational section
- **Scale** - Adjust thresholds: <100 (relaxed), 100-10K (standard), 10K+ (strict)
- **Type** - Emphasize relevant metrics: API (response time), CLI (startup), library (coverage)

## Scores (0-100)

- **Security** - Based on vulnerabilities found
- **Tests** - Coverage percentage + quality
- **Tech Debt** - Complexity, dead code, duplication
- **AI Quality** - AI code patterns (if detected)
- **Hygiene** - TODOs, orphans, hardcoded values
- **DORA** - DevOps performance metrics
- **Self-Compliance** - Alignment with stated rules

## Fix First Indicator

After scores, show top 3 actionable items:
- Highest impact, lowest effort
- With specific file:line locations

**Follow CCO Approval Flow standard from cco-standards.**

Apply to: "Fix First" actionable items.

## Output

Dashboard with scores → critical issues → "Fix first" items → next actions.

## Usage

```bash
/cco-health
/cco-health --focus security
```
