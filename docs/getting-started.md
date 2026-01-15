# Getting Started

Your first 10 minutes with CCO.

---

## Installation

```
/plugin marketplace add sungurerdim/ClaudeCodeOptimizer
/plugin install cco
```

**Restart Claude Code** after installation.

<details>
<summary>What gets installed</summary>

The plugin installs:

1. `commands/` — 8 slash commands
2. `agents/` — 3 specialized agents
3. `rules/` — 62 rule files (1364 rules total)

**Structure:**
```
.claude-plugin/cco/
├── commands/
│   ├── cco-checkup.md
│   ├── cco-commit.md
│   ├── cco-config.md
│   ├── cco-optimize.md
│   ├── cco-preflight.md
│   ├── cco-research.md
│   ├── cco-review.md
│   └── cco-status.md
├── agents/
│   ├── cco-agent-analyze.md
│   ├── cco-agent-apply.md
│   └── cco-agent-research.md
└── rules/
    ├── core.md (141 rules)
    ├── ai.md (68 rules)
    └── ... (60 adaptive rule files)
```

</details>

### Update

```
/plugin marketplace update
```

### Uninstall

```
/plugin uninstall cco
```

---

## First 10 Minutes

### Step 1: Configure Your Project (2 min)

Open Claude Code in your project directory and run:

```
/cco-config
```

This will:

1. **Auto-detect** your stack (language, framework, database, tools)
2. **Ask questions** about your context (team size, data sensitivity, compliance)
3. **Generate rules** specific to your project in `.claude/cco.md`

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

Generated rules:
├── python.md (Python best practices)
├── api.md (REST API patterns)
├── security.md (PII data rules)
└── context.md (project metadata)
```

</details>

### Step 2: Check Project Health (1 min)

```
/cco-status
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
/cco-optimize --quick
```

Auto-fixes safe issues:

- Unused imports
- Missing type hints
- Simple security fixes
- Formatting issues

**Risky changes** (auth, schema, API) will ask for approval.

---

## What Changed?

### Before CCO

- Claude uses generic patterns
- No pre-action safety checks
- Silent changes, no tracking
- No approval flow for risky operations

### After CCO

- Domain-specific best practices for your stack
- Git status verified before every operation
- Full accounting: `Applied: N | Failed: N | Total: N`
- Risky changes require explicit approval

---

## Understanding the Rules

### Global Rules (Always Active)

| File | Rules | Purpose |
|------|-------|---------|
| `core.md` | 141 | Fundamental principles (SSOT, DRY, YAGNI, Fail-Fast) |
| `ai.md` | 68 | AI behavior patterns (Read-First, Verify-APIs) |

These apply to **all projects** automatically.

### Adaptive Rules (Per-Project)

| Category | Files | Examples |
|----------|-------|----------|
| Languages | 27 | python.md, typescript.md, go.md |
| Domains | 35 | api.md, security.md, testing.md |

Selected by `/cco-config` based on your stack detection.

---

## Common Questions

### "Do I need to run /cco-config for every project?"

Yes. Each project gets its own rules based on its specific stack and context.

### "Can I customize the generated rules?"

Yes. Edit `.claude/cco.md` directly. Your changes persist until the next `/cco-config` run.

### "How do I see what rules are active?"

Run `/cco-status` or check `.claude/cco.md` in your project.

### "What if /cco-config detects something wrong?"

The detection is a starting point. You can:
1. Answer the clarifying questions differently
2. Edit the generated rules directly
3. Run `/cco-config` again to reconfigure

---

## Troubleshooting

### Commands not appearing

1. **Restart Claude Code** after installation
2. Verify plugin is installed: `/plugin list`
3. Try reinstalling: `/plugin uninstall cco && /plugin install cco`

### "CCO context not found"

Most commands require project configuration first:

```
/cco-config
```

---

## Next Steps

| Goal | Command |
|------|---------|
| Full security audit | `/cco-optimize --security` |
| Architecture review | `/cco-review` |
| Quality-gated commit | `/cco-commit` |
| Pre-release check | `/cco-preflight` |
| Research a topic | `/cco-research "your question"` |

See [Commands](commands.md) for full documentation.

---

*Back to [README](../README.md)*
