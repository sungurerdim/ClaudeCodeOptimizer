# Getting Started

Your first 10 minutes with CCO.

---

## Installation

**In Claude Code:**
```
/plugin marketplace add sungurerdim/ClaudeCodeOptimizer
```

```
/plugin install cco@ClaudeCodeOptimizer
```

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

### Step 1: Run /cco:tune

Configure CCO for your project:

```
/cco:tune
```

This will:
1. **Auto-detect** your stack (language, framework, database, tools)
2. **Ask questions** about team size, data sensitivity, priorities
3. **Generate rules** specific to your project in `.claude/rules/`

**Quick mode** (skip questions):
```
/cco:tune --auto
```

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
├── cco-profile.md (YAML project metadata)
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

## Rule Loading

CCO automatically loads rules via the SessionStart hook. Core rules are injected into context, and project rules are loaded from `.claude/rules/*.md`. For technical details on the rule loading mechanism, see [Rules Reference](rules.md#zero-config-loading-mechanism).

---

## Understanding the Rules

### Core Rules (Always Active, BLOCKER)

Injected automatically at session start via hook. These are **enforceable constraints**, not suggestions:

| Category | Key Rules |
|----------|-----------|
| **Foundation** | Uncertainty Protocol (stop & ask), Complexity Limits (method ≤50 lines), Change Scope (only requested changes) |
| **Safety** | Security Violations (no secrets in source, no bare except, no eval), Validation Boundaries |
| **Workflow** | Read-Before-Edit (must read before editing), Accounting (applied + failed + deferred = total) |

**Hard Limits (exceeding = STOP):**
- Cyclomatic complexity ≤ 15
- Method lines ≤ 50
- Nesting depth ≤ 3

These apply to **all projects** automatically and cannot be overridden.

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

CCO stores project config in `.claude/rules/cco-profile.md`. Run `/cco:tune` to create or update it.

### "Can I customize the generated rules?"

Yes. Edit `.claude/rules/cco-profile.md` directly. Your changes persist. Re-run setup anytime to reconfigure.

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

### "CCO profile not found"

Run `/cco:tune` to configure CCO for your project, or any CCO command will offer setup options.

---

## Next Steps

| Goal | Command |
|------|---------|
| Full security audit | `/cco:optimize --scope=security` |
| Architecture review | `/cco:align` |
| Quality-gated commit | `/cco:commit` |
| Pre-release check | `/cco:preflight` |
| Research a topic | `/cco:research "your question"` |

See [Commands](commands.md) for full documentation.

---

*Back to [README](../README.md)*
