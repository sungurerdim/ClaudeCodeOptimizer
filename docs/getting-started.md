# Getting Started with CCO

Step-by-step guide for new users.

---

## Installation

```bash
pip install claudecodeoptimizer && cco-install
```

**What happens:**
- 8 slash commands installed to `~/.claude/commands/`
- 3 specialized agents installed to `~/.claude/agents/`
- 87 core + 49 AI rules installed to `~/.claude/rules/cco/`

**Restart Claude Code** for changes to take effect.

---

## Your First 5 Minutes

### Step 1: Configure Your Project (30 sec)

In Claude Code, run:
```
/cco-config
```

This will:
1. **Auto-detect** your stack (language, framework, database, etc.)
2. **Ask questions** about team size, data sensitivity, compliance needs
3. **Generate** project-specific rules in `.claude/rules/cco/`

### Step 2: Check Project Health (10 sec)

```
/cco-status
```

Shows:
- Security score
- Quality score
- Hygiene score
- Recommended next actions

### Step 3: Quick Wins (2 min)

```
/cco-optimize --quick
```

Auto-fixes safe issues:
- Unused imports
- Simple type hints
- Basic security fixes
- Code formatting

---

## What Changed After Installation?

| Before | After |
|--------|-------|
| Claude uses generic patterns | Claude uses domain-specific best practices |
| No pre-action checks | Git status check before changes |
| Silent operations | Full accounting: `Applied: N | Skipped: N | Failed: N` |
| No approval flow | Risky changes require confirmation |

---

## Understanding the Rules

### Global Rules (Always Active)

Located in `~/.claude/rules/cco/`:

| File | Purpose |
|------|---------|
| `core.md` | 87 fundamental principles (SSOT, DRY, YAGNI, etc.) |
| `ai.md` | 49 AI behavior patterns (Read-First, No-Hallucination, etc.) |

### Project Rules (After /cco-config)

Located in `.claude/rules/cco/`:

| File | Purpose |
|------|---------|
| `context.md` | Project metadata (stack, team, scale, etc.) |
| `{language}.md` | Language-specific rules (Python, TypeScript, etc.) |
| `{category}.md` | Category-specific rules (security, compliance, etc.) |

---

## Common First-Time Questions

### "What does /cco-config actually do?"

1. Runs `cco-agent-analyze` to detect your stack
2. Asks clarifying questions (team size, data sensitivity, etc.)
3. Selects relevant rules from 1563 adaptive rules
4. Writes rules to `.claude/rules/cco/`
5. Optionally configures statusline and permissions

### "Do I need to run /cco-config for every project?"

Yes. Each project gets its own rules based on its specific stack and requirements.

### "Can I customize the generated rules?"

Yes. Edit files in `.claude/rules/cco/` directly. Your changes persist until next `/cco-config` run.

### "How do I see what rules are active?"

Check `~/.claude/rules/cco/` (global) and `.claude/rules/cco/` (project).

---

## Next Steps

| Goal | Command |
|------|---------|
| Full security audit | `/cco-optimize --security` |
| Architecture review | `/cco-review` |
| Quality-gated commit | `/cco-commit` |
| Pre-release check | `/cco-preflight` |

See [Commands](commands.md) for full reference.

---

*Back to [README](../README.md)*
