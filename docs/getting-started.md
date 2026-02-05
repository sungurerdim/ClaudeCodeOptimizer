# Getting Started

Your first 10 minutes with CCO.

---

## Installation

**macOS / Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/sungurerdim/ClaudeCodeOptimizer/main/install.sh | bash
```

**Windows (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/sungurerdim/ClaudeCodeOptimizer/main/install.ps1 | iex
```

**Restart Claude Code** after installation.

### What Gets Installed

```
~/.claude/
├── rules/
│   └── cco-rules.md          # Core rules (auto-loaded)
├── commands/
│   ├── cco-optimize.md        # 7 slash commands
│   ├── cco-align.md
│   ├── cco-commit.md
│   ├── cco-research.md
│   ├── cco-preflight.md
│   ├── cco-docs.md
│   └── cco-update.md
└── agents/
    ├── cco-agent-analyze.md   # 3 subagents
    ├── cco-agent-apply.md
    └── cco-agent-research.md
```

### Update

```
/cco-update
```

Or re-run the install script.

### Uninstall

Remove the CCO files from `~/.claude/`:

```bash
rm ~/.claude/rules/cco-rules.md
rm ~/.claude/commands/cco-*.md
rm ~/.claude/agents/cco-agent-*.md
```

---

## First 10 Minutes

### Step 1: Quick Wins

```
/cco-optimize
```

Auto-fixes safe issues:
- Unused imports
- Missing type hints
- Simple security fixes
- Formatting issues

**Risky changes** (auth, schema, API) will ask for approval. Use `--auto` for unattended mode or `--scope=security` for a specific scope.

### Step 2: Architecture Check (Optional)

```
/cco-align
```

Shows gap analysis between current state and ideal architecture. Use `--preview` for analysis without changes.

---

## Rule Loading

CCO rules are auto-loaded from `~/.claude/rules/cco-rules.md`. Claude Code automatically reads all `.md` files in `~/.claude/rules/` at session start. See [Rules](rules.md) for full documentation.

---

## Understanding the Rules

### Core Rules (Always Active, BLOCKER)

Auto-loaded at session start from `~/.claude/rules/cco-rules.md`. These are **enforceable constraints**, not suggestions:

| Category | Key Rules |
|----------|-----------|
| **Foundation** | Uncertainty Protocol (stop & ask), Complexity Limits (method ≤50 lines), Change Scope (only requested changes) |
| **Safety** | Security Violations (no secrets in source, no bare except, no eval), Validation Boundaries |
| **Workflow** | Read-Before-Edit (must read before editing), Accounting (applied + failed + needs_approval = total) |

**Hard Limits (exceeding = STOP):**
- Cyclomatic complexity ≤ 15
- Method lines ≤ 50
- File lines ≤ 500
- Nesting depth ≤ 3
- Parameters ≤ 4

These apply to **all projects** automatically and cannot be overridden.


---

## Common Questions

### "How do I see what rules are active?"

See [docs/rules.md](rules.md) — all CCO rules are documented there.

### "Can I add custom rules?"

Yes. Add `.md` files to `.claude/rules/` in your project. Claude Code loads them automatically.

---

## Troubleshooting

### Commands not appearing

1. **Restart Claude Code** after installation
2. Verify files are installed: `ls ~/.claude/commands/cco-*.md`
3. Try re-running the install script (see [Installation](#installation))

---

## Next Steps

| Goal | Command |
|------|---------|
| Full security audit | `/cco-optimize --scope=security` |
| Architecture review | `/cco-align` |
| Quality-gated commit | `/cco-commit` |
| Pre-release check | `/cco-preflight` |
| Research a topic | `/cco-research "your question"` |
| Update CCO | `/cco-update` |

See [Commands](commands.md) for full documentation.

---

*Back to [README](../README.md)*
