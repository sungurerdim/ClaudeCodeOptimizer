---
name: cco-health
description: Actionable metrics dashboard
requires: detection
---

# /cco-health

**Process visibility** - Single view of project health with actionable next steps.

## Agent Delegation

| Phase | Agent | Purpose |
|-------|-------|---------|
| Detect | `cco-agent-detect` | Identify stack for applicable metrics |
| Scan | `cco-agent-scan` | Collect metrics, identify top issues |

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
- One-click fix option via AskUserQuestion

## Output

Dashboard with scores → critical issues → "Fix first" items → next actions.

## Usage

```bash
/cco-health
/cco-health --focus security
```
