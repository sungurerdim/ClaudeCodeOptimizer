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
│   └── cco-rules.md            # Core rules (auto-loaded)
├── commands/
│   ├── cco-optimize.md          # 8 slash commands
│   ├── cco-align.md
│   ├── cco-commit.md
│   ├── cco-research.md
│   ├── cco-docs.md
│   ├── cco-blueprint.md
│   ├── cco-pr.md
│   └── cco-update.md
└── agents/
    ├── cco-agent-analyze.md     # 3 subagents
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

Auto-fixes safe issues: unused imports, missing type hints, simple security fixes, formatting.

Risky changes (auth, schema, API) ask for approval. Use `--auto` for unattended mode or `--scope=security` for a specific scope.

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

### Rule Categories

| Category | Key Rules |
|----------|-----------|
| **Scope Control** | Minimal Footprint, Exploration Budget, Decide and Execute |
| **Code Integrity** | Complexity Limits (method ≤50 lines, nesting ≤3), Anti-Overengineering |
| **Verification** | Read Before Write, Edit Discipline |
| **Uncertainty Protocol** | Surface Uncertainty (stop & ask), Scope Creep Guard |
| **Session Resilience** | Anchor to Artifacts, Error Recovery |
| **Security Baseline** | Security Patterns (no secrets in source, no bare except, no eval) |
| **Development Standards** | Respect Intent Markers, Issue Prioritization |

### Hard Limits

| Metric | Limit |
|--------|-------|
| Cyclomatic Complexity | ≤ 15 |
| Method Lines | ≤ 50 |
| File Lines | ≤ 500 |
| Nesting Depth | ≤ 3 |
| Parameters | ≤ 4 |

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
| Project health | `/cco-blueprint` |
| Create PR | `/cco-pr` |
| Research a topic | `/cco-research "your question"` |
| Update CCO | `/cco-update` |

See [Commands](commands.md) for full documentation.

---

*Back to [README](../README.md)*
