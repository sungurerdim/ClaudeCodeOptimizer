# Getting Started

Your first 10 minutes with CCO.

---

## Installation

```bash
pip install claudecodeoptimizer && cco-install
```

**Restart Claude Code** after installation.

<details>
<summary>What happens during installation</summary>

The `cco-install` command:

1. Creates `~/.claude/commands/` with 8 slash commands
2. Creates `~/.claude/agents/` with 3 specialized agents
3. Creates `~/.claude/rules/cco/` with core (87) + AI (60) rules
4. Optionally configures statusline in `~/.claude/settings.json`

**Files created:**
```
~/.claude/
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
└── rules/cco/
    ├── core.md (87 rules)
    └── ai.md (60 rules)
```

</details>

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
3. **Generate rules** specific to your project in `.claude/rules/cco/`

<details>
<summary>Example detection output</summary>

```
Detected:
├── Language: Python 3.12
├── Framework: FastAPI
├── Database: PostgreSQL (SQLAlchemy)
├── Testing: pytest (82% coverage)
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

Located in `~/.claude/rules/cco/`:

| File | Rules | Purpose |
|------|-------|---------|
| `core.md` | 87 | Fundamental principles (SSOT, DRY, YAGNI, Fail-Fast) |
| `ai.md` | 60 | AI behavior patterns (Read-First, No-Hallucination) |

These apply to **all projects** automatically.

### Project Rules (After /cco-config)

Located in `.claude/rules/cco/`:

| File | Purpose |
|------|---------|
| `context.md` | Project metadata (stack, team, scale, priority) |
| `{language}.md` | Language-specific rules |
| `{category}.md` | Category-specific rules (security, compliance) |

These are **generated per-project** based on detection.

---

## Common Questions

### "Do I need to run /cco-config for every project?"

Yes. Each project gets its own rules based on its specific stack and context.

### "Can I customize the generated rules?"

Yes. Edit files in `.claude/rules/cco/` directly. Your changes persist until the next `/cco-config` run.

### "How do I see what rules are active?"

Check:
- `~/.claude/rules/cco/` (global rules, always active)
- `.claude/rules/cco/` (project rules, if configured)

### "What if /cco-config detects something wrong?"

The detection is a starting point. You can:
1. Answer the clarifying questions differently
2. Edit the generated rules directly
3. Run `/cco-config` again to reconfigure

---

## Troubleshooting

### Commands not appearing

1. **Restart Claude Code** after installation
2. Check if files exist: `ls ~/.claude/commands/`
3. Verify installation: `cco-install --dry-run`

### "CCO context not found"

Most commands require project configuration first:

```
/cco-config
```

### Permission errors during installation

Try installing with pipx for isolation:

```bash
pipx install claudecodeoptimizer && cco-install
```

### Statusline not showing

Run installation with explicit statusline option:

```bash
cco-install --statusline cco-full
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

## Local Mode

For project-specific settings without affecting global installation:

```bash
cco-install --local . --statusline cco-full --permissions balanced
```

| Option | Values |
|--------|--------|
| `--statusline` | `cco-full` (all info) / `cco-minimal` (project + branch) |
| `--permissions` | `safe` / `balanced` / `permissive` / `full` |

This creates `.claude/` in your project directory instead of `~/.claude/`.

---

*Back to [README](../README.md)*
