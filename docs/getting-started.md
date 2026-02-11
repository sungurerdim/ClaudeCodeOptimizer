# Getting Started

Your first 10 minutes with CCO.

---

## Installation

### Using Go Binary (Recommended)

**macOS / Linux:**
```bash
curl -fsSL https://github.com/sungurerdim/ClaudeCodeOptimizer/releases/latest/download/cco-$(uname -s | tr A-Z a-z)-$(uname -m) -o cco && chmod +x cco && ./cco install
```

**Windows (PowerShell):**
```powershell
irm https://github.com/sungurerdim/ClaudeCodeOptimizer/releases/latest/download/cco-windows-amd64.exe -OutFile cco.exe; .\cco.exe install
```

### Using /cco-update

If you already have CCO installed, update to v4:
```
/cco-update
```

**Restart Claude Code** after installation.

### What Gets Installed

```
~/.claude/
├── rules/
│   └── cco-rules.md            # Core rules (auto-loaded)
├── skills/
│   ├── cco-optimize/SKILL.md   # 8 skills
│   ├── cco-align/SKILL.md
│   ├── cco-commit/SKILL.md
│   ├── cco-research/SKILL.md
│   ├── cco-docs/SKILL.md
│   ├── cco-blueprint/SKILL.md
│   ├── cco-pr/SKILL.md
│   └── cco-update/SKILL.md
└── agents/
    ├── cco-agent-analyze.md     # 3 subagents
    ├── cco-agent-apply.md
    └── cco-agent-research.md
```

### Update

```
/cco-update
```

Or re-run the Go installer binary.

### Uninstall

Using Go binary:
```bash
./cco uninstall
```

Manual removal:
```bash
rm ~/.claude/rules/cco-rules.md
rm -rf ~/.claude/skills/cco-*/
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
| **Production Standards** | Production-ready baseline for all output |
| **Verification** | Read Before Write, Edit Discipline |
| **Uncertainty Protocol** | Surface Uncertainty (stop & ask), Scope Creep Guard |
| **Session Resilience** | Anchor to Artifacts, Error Recovery |
| **Process Discipline** | Task Awareness, Goal Anchoring, Completion Verification |
| **Security Baseline** | Security Patterns (no secrets in source, no bare except, no eval) |
| **CCO Operations** | Accounting, Auto Mode, Severity Levels, Skip Patterns |

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

### Skills not appearing

1. **Restart Claude Code** after installation
2. Verify files are installed: `ls ~/.claude/skills/cco-*/SKILL.md`
3. Try re-running the installer (see [Installation](#installation))

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
