---
name: cco-status
description: CCO installation and config health check
---

# /cco-status

Check CCO installation and configuration health.

## Agent Delegation

| Phase | Agent | Purpose |
|-------|-------|---------|
| Validate | `cco-agent-scan` | Check files, validate configs |

### MANDATORY Agent Rules

1. **ALWAYS use `cco-agent-scan`** for validation
2. Do NOT use direct file reads for config validation
3. Agent handles JSON parsing and pattern checking

### Error Recovery

On validation errors:
1. Delegate to `cco-agent-scan` for fresh validation
2. Report issues with specific file:line references

## Installation Check

1. Count files in ~/.claude/commands/cco-*.md
2. Count files in ~/.claude/agents/cco-*.md
3. Verify CLAUDE.md has CCO_RULES markers

## Config Health Check

Check both global (~/.claude/) and local (./.claude/) scopes:

### settings.json Validation
- [ ] JSON syntax valid (parseable)
- [ ] No unknown top-level keys (warn only)
- [ ] allow/deny/ask arrays are valid format
- [ ] No conflicting rules (same pattern in both allow and deny)
- [ ] Dangerous commands properly denied

### statusline.js Validation
- [ ] JavaScript syntax valid
- [ ] Exports expected function signature

### Cross-Scope Check
- [ ] No conflicting rules between global and local
- [ ] Warn if local overrides global completely

## Output

```
CCO Status: OK
Location: ~/.claude/
Commands: 9
Agents: 3
Rules: inline

Config Health:
  Global settings.json: OK
  Global statusline.js: not configured
  Local settings.json: OK (overrides global)
  Local statusline.js: not configured

Quick start: /cco-audit --smart
```

### If Issues Found

```
CCO Status: WARNING
Location: ~/.claude/

Config Issues:
  ⚠ Global settings.json: "rm -rf" in allow list (security risk)
  ⚠ Local settings.json: invalid JSON at line 15
  ⚠ Conflict: "Bash(npm:*)" in global deny, local allow

Run /cco-config to fix issues
```

## Usage

```bash
/cco-status          # Full health check
/cco-status --quick  # Installation only, skip config validation
```
