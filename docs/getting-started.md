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

```
/plugin update cco@ClaudeCodeOptimizer
```

### Uninstall

```
/plugin uninstall cco@ClaudeCodeOptimizer
```

```
/plugin marketplace remove ClaudeCodeOptimizer
```

---

## First 10 Minutes

### Step 1: Quick Wins

```
/cco:optimize
```

Auto-fixes safe issues:
- Unused imports
- Missing type hints
- Simple security fixes
- Formatting issues

**Risky changes** (auth, schema, API) will ask for approval. Use `--auto` for unattended mode or `--scope=security` for a specific scope.

### Step 2: Architecture Check (Optional)

```
/cco:align
```

Shows gap analysis between current state and ideal architecture. Use `--preview` for analysis without changes.

---

## Rule Loading

CCO rules are injected automatically via the SessionStart hook from `hooks/core-rules.json`. See [Rules](rules.md) for full documentation.

---

## Understanding the Rules

### Core Rules (Always Active, BLOCKER)

Injected automatically at session start via hook. These are **enforceable constraints**, not suggestions:

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
2. Verify plugin is installed: `/plugin` → **Installed** tab
3. Try reinstalling:
   ```
   /plugin uninstall cco@ClaudeCodeOptimizer
   /plugin install cco@ClaudeCodeOptimizer
   ```

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
