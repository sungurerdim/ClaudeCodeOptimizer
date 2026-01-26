# Getting Started

Your first 10 minutes with CCO.

---

## Installation

**In Claude Code:**
```
/plugin marketplace add sungurerdim/ClaudeCodeOptimizer
```

Then run `/plugin`, go to **Discover** tab, select **cco**, and click **Install**.

<details>
<summary>Alternative: Direct command</summary>

```
/plugin install cco@ClaudeCodeOptimizer
```

</details>

<details>
<summary>Alternative: From terminal</summary>

```bash
claude plugin marketplace add sungurerdim/ClaudeCodeOptimizer
claude plugin install cco@ClaudeCodeOptimizer
```

</details>

**Restart Claude Code** after installation.

### Update

```
/plugin marketplace update ClaudeCodeOptimizer
```

### Uninstall

```
/plugin uninstall cco@ClaudeCodeOptimizer
/plugin marketplace remove ClaudeCodeOptimizer
```

---

## First 10 Minutes

### Step 1: Auto-Setup (Automatic)

When you start a new session in a project without CCO configured, CCO automatically offers setup:

```
🔧 CCO is not configured for this project.

[Auto-setup] Detect stack and create rules automatically
[Interactive] Ask me questions to customize setup
[Skip] Don't configure CCO for this project
```

**Auto-setup** will:
1. **Auto-detect** your stack (language, framework, database, tools)
2. **Generate rules** specific to your project in `.claude/rules/`

**Interactive** will also ask questions about:
- Team size
- Data sensitivity
- Compliance requirements
- Development priorities

<details>
<summary>Example detection output</summary>

```
Detected:
├── Language: Python 3.12
├── Framework: FastAPI
├── Database: PostgreSQL (SQLAlchemy)
├── Testing: pytest with 82% coverage
├── CI/CD: GitHub Actions
└── Type: API Service

Generated rules in .claude/rules/:
├── cco-context.md (YAML project metadata)
├── cco-python.md (language best practices)
├── cco-backend.md (API patterns)
└── cco-testing.md (test standards)
```

</details>

### Step 2: Quick Wins (5 min)

```
/cco:optimize --quick
```

Auto-fixes safe issues:
- Unused imports
- Missing type hints
- Simple security fixes
- Formatting issues

**Risky changes** (auth, schema, API) will ask for approval.

### Step 3: Architecture Check (Optional)

```
/cco:align --quick
```

Shows gap analysis between current state and ideal architecture.

---

## Understanding the Rules

### Core Rules (Always Active)

Injected automatically at session start via hook:

| File | Purpose |
|------|---------|
| `cco-foundation.md` | Design principles (SSOT, DRY, YAGNI, KISS) |
| `cco-safety.md` | Security standards (OWASP, input validation) |
| `cco-workflow.md` | AI behavior patterns (Read-First, Verify-APIs) |

These apply to **all projects** automatically.

### Adaptive Rules (Per-Project)

| Category | Files | Examples |
|----------|-------|----------|
| Languages | 21 | `cco-python.md`, `cco-typescript.md`, `cco-go.md` |
| Frameworks | 8 | `cco-backend.md`, `cco-frontend.md`, `cco-api.md` |
| Operations | 12 | `cco-cicd.md`, `cco-testing.md`, `cco-infrastructure.md` |

Selected automatically based on your stack detection.

---

## Common Questions

### "How does CCO know about my project?"

CCO auto-detects at session start by checking if `cco: true` marker exists in your context. If not, it offers setup options.

### "Can I customize the generated rules?"

Yes. Edit `.claude/rules/cco-context.md` directly. Your changes persist. Re-run setup anytime to reconfigure.

### "How do I see what rules are active?"

Check `.claude/rules/` in your project. All `cco-*.md` files are managed by CCO.

### "What if detection is wrong?"

Choose "Interactive" during setup to answer questions manually. You can also edit generated rules directly.

---

## Troubleshooting

### Commands not appearing

1. **Restart Claude Code** after installation
2. Verify plugin is installed: `/plugin` → **Installed** tab
3. Try reinstalling:
   ```
   /plugin uninstall cco@ClaudeCodeOptimizer
   /plugin install cco@ClaudeCodeOptimizer
   ```

### "CCO context not found"

CCO should auto-detect and offer setup. If this doesn't happen:
- Check if `.claude/rules/cco-context.md` exists
- If not, any CCO command will trigger setup

---

## Next Steps

| Goal | Command |
|------|---------|
| Full security audit | `/cco:optimize --security` |
| Architecture review | `/cco:align` |
| Quality-gated commit | `/cco:commit` |
| Pre-release check | `/cco:preflight` |
| Research a topic | `/cco:research "your question"` |

See [Commands](commands.md) for full documentation.

---

*Back to [README](../README.md)*
