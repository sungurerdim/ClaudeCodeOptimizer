---
name: cco-status
description: CCO installation and config health check
---

# /cco-status

Check CCO installation and configuration health.

## Installation Check

1. Count files in ~/.claude/commands/cco-*.md
2. Count files in ~/.claude/agents/cco-*.md
3. Verify CLAUDE.md has CCO_STANDARDS markers

## Calibration Check

Check for project calibration context:

1. Check ./CLAUDE.md for CCO_CONTEXT markers (project-specific)
2. If no context found, suggest running `/cco-calibrate`

**Note:** CCO_CONTEXT is always local (project root), never global. Each project has its own calibration.

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
Commands: 11
Agents: 3
Standards: inline

Calibration:
  Project context: OK (Team: solo, Scale: <100, Type: cli)

Config Health:
  Global settings.json: OK
  Global statusline.js: not configured
  Local settings.json: OK (overrides global)
  Local statusline.js: not configured

Quick start: /cco-calibrate → /cco-audit --smart
```

### If Issues Found

```
CCO Status: WARNING
Location: ~/.claude/

Calibration Issues:
  ⚠ No project context found - AI recommendations not calibrated
  → Run /cco-calibrate to set project context

Config Issues:
  ⚠ Global settings.json: "rm -rf" in allow list (security risk)
  ⚠ Local settings.json: invalid JSON at line 15
  ⚠ Conflict: "Bash(npm:*)" in global deny, local allow

Run /cco-calibrate to set context, /cco-config to fix config issues
```

## Usage

```bash
/cco-status          # Full health check
/cco-status --quick  # Installation only, skip config validation
```
