---
name: cco-status
description: CCO installation health check
---

# /cco-status

**Check CCO installation**

---

## Flow: Check → Show

### Check
1. Count files in ~/.claude/commands/cco-*.md
2. Count files in ~/.claude/agents/cco-*.md
3. Verify CLAUDE.md has CCO_RULES markers

### Show
```markdown
# CCO Status

**Health:** OK ✓
**Location:** ~/.claude/

## Components
- Commands: {count} (cco-audit, cco-fix, ...)
- Agents: {count} (cco-agent-scan, cco-agent-action)
- Rules: inline in CLAUDE.md

## Quick Start
/cco-audit --smart
/cco-help
```

---

## Usage

```bash
/cco-status
```
