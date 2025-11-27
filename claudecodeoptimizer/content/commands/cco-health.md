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


### MANDATORY Agent Rules

1. **NEVER use direct Bash/Grep tools** - delegate to agents
2. **ALWAYS use agents as first choice**, not fallback after errors
3. Detect phase → `cco-agent-detect`
4. Scan phase → `cco-agent-scan`

### Error Recovery

On tool errors:
1. Do NOT retry with direct tools
2. Immediately delegate to appropriate agent
3. Report agent results to user

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
