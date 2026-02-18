# Getting Started

Your first 10 minutes with CCO.

---

## Installation

### Using Go Binary (Recommended)

**macOS / Linux:**
```bash
mkdir -p ~/.local/bin && curl -fsSL https://github.com/sungurerdim/ClaudeCodeOptimizer/releases/latest/download/cco-$(uname -s | tr A-Z a-z)-$(uname -m) -o ~/.local/bin/cco && chmod +x ~/.local/bin/cco && ~/.local/bin/cco install
```

**Windows (PowerShell):**
```powershell
$b="$HOME\.local\bin"; New-Item $b -ItemType Directory -Force >$null; irm https://github.com/sungurerdim/ClaudeCodeOptimizer/releases/latest/download/cco-windows-amd64.exe -OutFile "$b\cco.exe"; & "$b\cco.exe" install
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
├── skills/                        # 8 skills
│   ├── cco-optimize/SKILL.md
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
cco uninstall
```

Manual removal:
```bash
rm -f ~/.claude/rules/cco-rules.md
rm -rf ~/.claude/skills/cco-*/
rm -f ~/.claude/agents/cco-agent-*.md
```

---

## First 10 Minutes

### Step 1: Create a Project Profile

```
/cco-blueprint
```

Creates a project profile in CLAUDE.md — priorities, constraints, targets, and current scores. If no profile exists, starts the init flow automatically.

### Step 2: Architecture Gap Analysis

```
/cco-align
```

Shows gap analysis between current state and ideal architecture. Use `--preview` for analysis without changes.

### Step 3: Scan and Fix Issues

```
/cco-optimize
```

Auto-fixes safe issues: unused imports, missing type hints, simple security fixes, formatting.

Risky changes (auth, schema, API) ask for approval. Use `--auto` for unattended mode or `--scope=security` for a specific scope.

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

See [Skills](skills.md) for full documentation.

---

*Back to [README](../README.md)*
