---
name: cco-config
description: Configure project context and AI behavior
allowed-tools: Read(*), Write(*), Edit(*), Bash(cco-install:*), Task(*), TodoWrite, AskUserQuestion
---

# /cco-config (v2 - Agent-Based)

**Project tuning** - Lightweight orchestrator using sub-agents for heavy work.

## Context

- Context exists: !`test -f ./.claude/rules/cco/context.md && echo "1" || echo "0"`
- Existing rules: !`test -d .claude/rules/cco && ls .claude/rules/cco/*.md | xargs -I{} basename {} | tr '\n' ' ' | grep . || echo "None"`
- Settings exists: !`test -f ./.claude/settings.json && echo "1" || echo "0"`

## Architecture

| Step | Action |
|------|--------|
| 1. Status | Read existing files only |
| 2. Questions | AskUserQuestion for choices |
| 3. Detection | `Task(cco-agent-analyze, "scope=config")` → JSON |
| 4. Review | Show results, ask approval |
| 5. Apply | `Task(cco-agent-apply)` OR `cco-install --local` |
| 6. Report | Summary of changes |

**Benefits:** ~3K tokens (vs ~15K) │ Isolated detection │ Parallel within agent

## Progress Tracking [CRITICAL]

```
TodoWrite([
  { content: "Show quick status", status: "in_progress", activeForm: "Showing quick status" },
  { content: "Ask user questions", status: "pending", activeForm: "Asking user questions" },
  { content: "Run detection", status: "pending", activeForm: "Running detection" },
  { content: "Review results", status: "pending", activeForm: "Reviewing results" },
  { content: "Apply configuration", status: "pending", activeForm: "Applying configuration" },
  { content: "Show report", status: "pending", activeForm: "Showing report" }
])
```

---

## Step 1: Quick Status

Read existing files in parallel: context.md, settings.json, rules list
Display: Project, Context, AI Perf, Statusline, Permissions, Rules

---

## Step 2: User Questions

### Q1: Action Type

| Question | Options | MultiSelect |
|----------|---------|-------------|
| What to do? | Configure (Recommended); Remove; Export | false |

### Q2: Scope (based on Q1)

| Action | Options |
|--------|---------|
| Configure | Detection & Rules (Recommended); AI Performance; Statusline; Permissions |
| Remove | Rules; AI Performance; Statusline; Permissions |
| Export | AGENTS.md (Recommended); CLAUDE.md |

### Q3: Details (if applicable)

| Selection | Question | Options |
|-----------|----------|---------|
| Statusline | Mode? | cco-full (Recommended); cco-minimal |
| AI Perf | Thinking? | 5K; 8K (Recommended); 10K |
| AI Perf | MCP Output? | 25K; 35K (Recommended); 50K |
| Permissions | Level? | Safe; Balanced (Recommended); Permissive; Full |

---

## Step 3: Detection & User Questions

```
Task(cco-agent-analyze, prompt="scope=config")
```

Agent handles all detection and user-input:
1. **Auto-detect** from manifest/code/config/docs
2. **Ask user** about Team, Scale, Data, Compliance, Testing, SLA, Maturity, Breaking, Priority
3. **Read adaptive.md** via `cco-install --cat rules/cco-adaptive.md` (pip package)
4. **Select rules** based on detections + user input
5. **Return** detections, userInput, context, rules, guidelines, sources

See `cco-agent-analyze.md` for full detection categories and question details.

---

## Step 4: Review

Show detection results table, then:

| Question | Options | MultiSelect |
|----------|---------|-------------|
| Apply configuration? | Accept; Edit; Cancel | false |

---

## Step 5: Apply

### Rules & Context
Write files from agent output:
- `.claude/rules/cco/context.md` ← agent.context
- `.claude/rules/cco/{file}.md` ← agent.rules[]

### Statusline & Permissions
**CRITICAL: Use cco-install CLI only. Do NOT use Task(statusline-setup) or write statusline files directly.**

```bash
cco-install --local . --statusline {mode} --permissions {level}
```

This copies pre-built templates from package. Never generate statusline code.

### AI Performance
Write to `.claude/settings.json`:
```json
{
  "env": {
    "MAX_THINKING_TOKENS": "{value}",
    "MAX_MCP_OUTPUT_TOKENS": "{value}",
    "DISABLE_PROMPT_CACHING": "0"
  }
}
```

### Remove Operations
- Remove Rules: `rm -rf .claude/rules/cco/`
- Remove AI Perf: Remove `env` from settings.json
- Remove Statusline: `rm .claude/cco-statusline.js`, remove `statusLine` from settings.json
- Remove Permissions: Remove `permissions` from settings.json

---

## Step 6: Report

Shows: Changes (before/after), Files written, Restart reminder

---

## Export Mode

No agent needed. Read global + project rules.

| Format | Target | Rules | Output |
|--------|--------|-------|--------|
| AGENTS.md | Universal (Codex, Cursor, etc.) | Core + AI | ./AGENTS.md |
| CLAUDE.md | Claude Code only | Core + AI + Tools | ./CLAUDE.export.md |

**AGENTS.md filtering:** Remove tool names, paths, product refs, CCO-specific. Keep principles, behavior rules, formats.

---

## Reference

### Question Formatting

| Rule | Description |
|------|-------------|
| `[current]` | Matches existing (priority 1) |
| `[detected]` | Auto-detected (priority 2) |
| `(Recommended)` | Best practice (priority 3) |

### Permissions Levels

| Level | Auto-approved |
|-------|---------------|
| Safe | Read-only |
| Balanced | Read + lint/test |
| Permissive | Most operations |
| Full | All (Solo + Public only) |

## Rules

1. **Agent for detection** - Use Task(cco-agent-analyze) for detection
2. **cco-install for templates** - Statusline/permissions via CLI only, never Task(statusline-setup)
3. **Parallel reads** - Read existing files in parallel for status
4. **Minimal orchestration** - This command is coordinator only
5. **JSON handoff** - Agent returns structured data, command displays it
