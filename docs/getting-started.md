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

### Step 1: Configure Your Project (2 min)

Open Claude Code in your project directory and run:

```
/cco:config
```

This will:

1. **Auto-detect** your stack (language, framework, database, tools)
2. **Ask questions** about your context (team size, data sensitivity, compliance)
3. **Generate rules** specific to your project in `.claude/rules/`

<details>
<summary>Example detection output</summary>

```
Detected:
├── Language: Python 3.12
├── Framework: FastAPI
├── Database: PostgreSQL (SQLAlchemy)
├── Testing: 82% coverage
├── CI/CD: GitHub Actions
└── Type: API Service

Generated rules in .claude/rules/:
├── cco-context.md (YAML project metadata)
├── cco-{language}.md (language best practices)
├── cco-{framework}.md (framework patterns)
└── cco-{operation}.md (if PII/regulated data)
```

</details>

### Step 2: Check Project Health (1 min)

```
/cco:status
```

Shows:

| Score | Meaning |
|-------|---------|
| Security | Vulnerabilities, secrets, CVE exposure |
| Quality | Tech debt, type coverage, complexity |
| Hygiene | Dead code, orphan files, unused imports |
| Tests | Coverage percentage, test quality |

**Thresholds:** 80+ = OK | 60-79 = WARN | 40-59 = FAIL | <40 = CRITICAL

### Step 3: Quick Wins (5 min)

```
/cco:optimize --quick
```

Auto-fixes safe issues:

- Unused imports
- Missing type hints
- Simple security fixes
- Formatting issues

**Risky changes** (auth, schema, API) will ask for approval.

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
| Languages | 21 | `cco-{language}.md` (python, typescript, go, etc.) |
| Frameworks | 8 | `cco-{framework}.md` (backend, frontend, api, etc.) |
| Operations | 12 | `cco-{operation}.md` (cicd, testing, infrastructure, etc.) |

Selected by `/cco:config` based on your stack detection.

---

## Common Questions

### "Do I need to run /cco:config for every project?"

Yes. Each project gets its own rules based on its specific stack and context.

### "Can I customize the generated rules?"

Yes. Edit `.claude/rules/cco-context.md` directly. Your changes persist until the next `/cco:config` run.

### "How do I see what rules are active?"

Run `/cco:status` or check `.claude/rules/` in your project.

### "What if /cco:config detects something wrong?"

The detection is a starting point. You can:
1. Answer the clarifying questions differently
2. Edit the generated rules directly
3. Run `/cco:config` again to reconfigure

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

Most commands require project configuration first:

```
/cco:config
```

---

## Next Steps

| Goal | Command |
|------|---------|
| Full security audit | `/cco:optimize --security` |
| Architecture review | `/cco:review` |
| Quality-gated commit | `/cco:commit` |
| Pre-release check | `/cco:preflight` |
| Research a topic | `/cco:research "your question"` |

See [Commands](commands.md) for full documentation.

---

*Back to [README](../README.md)*
