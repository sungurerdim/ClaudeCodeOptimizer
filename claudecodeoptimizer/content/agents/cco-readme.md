# CCO Agents

**Two specialized agents for all CCO operations**

---

## Built-in Agents

### scan-agent
**Read-only analysis** - Safe, never modifies files

- Security scanning (OWASP, secrets, CVEs)
- Code quality analysis (complexity, dead code)
- Performance detection (N+1, missing indexes)
- Tech stack detection

**Used by:** `/cco-audit`

**File:** `cco-agent-scan.md`

---

### action-agent
**Write operations** - Modifies files with verification

- Fix issues (security, quality, performance)
- Generate files (tests, docs, configs)
- Optimize content (context, code, performance)
- Commit changes (atomic, semantic)

**Used by:** `/cco-fix`, `/cco-generate`, `/cco-optimize`, `/cco-commit`

**File:** `cco-agent-action.md`

---

## Agent Selection

Opus 4.5 handles model selection automatically via effort parameter. No manual model specification needed.

---

## Custom Agents

Create custom agents in `~/.claude/agents/`:

```markdown
---
name: my-agent
description: What it does
tools: Read, Grep, Glob
---

# My Agent
**Purpose**: One sentence

## Capabilities
- Capability 1
- Capability 2

## Flow
1. Step 1
2. Step 2
3. Step 3
```
