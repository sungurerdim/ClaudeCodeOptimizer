---
name: cco-config
description: Configure project context and AI behavior
allowed-tools: Read(*), Write(*), Edit(*), Bash(cco-install:*), Task(*), TodoWrite, AskUserQuestion
---

# /cco-config (v2 - Agent-Based)

**Project tuning** - Lightweight orchestrator using sub-agents for heavy work.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ /cco-config (this command) - Orchestrator                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. Quick Status    → Read existing files only (no detection)                │
│ 2. User Questions  → AskUserQuestion for all choices                        │
│ 3. Detection       → Task(cco-agent-analyze, scope=config) - returns JSON   │
│ 4. Review          → Show detection results, ask approval                   │
│ 5. Apply           → Task(cco-agent-apply) OR cco-install --local           │
│ 6. Report          → Summary of changes                                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Benefits:**
- Main session: ~3K tokens (vs ~15K before)
- Detection runs in isolated agent
- Parallel execution within agent
- Faster, less context pollution

## Progress Tracking [CRITICAL]

**Use TodoWrite to track progress.** Create todo list at start, update status for each step.

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

**Update status:** Mark `completed` immediately after each step finishes, mark next `in_progress`.

---

## Step 1: Quick Status

Read existing files only - no detection, no Bash commands for counting.

**Read in parallel:**
- `.claude/rules/cco/context.md` → Extract context values
- `.claude/settings.json` → Extract env values, statusline config
- List `.claude/rules/cco/*.md` files

**Display:**
```
╔══════════════════════════════════════════════════════════════════════════════╗
║                           CCO PROJECT STATUS                                 ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ PROJECT: {basename of cwd}                                                   ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ Context:     {Configured|Not configured}                                     ║
║ AI Perf:     {tokens|Not configured}                                         ║
║ Statusline:  {Full|Minimal|Broken|None}                                      ║
║ Permissions: {level|None}                                                    ║
║ Rules:       {list of .md files or "None"}                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## Step 2: User Questions (Multi-Step)

### Question 1: Action Type

**AskUserQuestion** (mandatory):

| Question | Options | MultiSelect |
|----------|---------|-------------|
| What do you want to do? | Configure (Recommended); Remove; Export | false |

### Question 2: Scope Selection (based on Q1 answer)

**If Configure selected:**

| Question | Options | MultiSelect |
|----------|---------|-------------|
| What to configure? | Detection & Rules (Recommended); AI Performance; Statusline; Permissions | true |

**If Remove selected:**

| Question | Options | MultiSelect |
|----------|---------|-------------|
| What to remove? | Rules; AI Performance; Statusline; Permissions | true |

**If Export selected:**

| Question | Options | MultiSelect |
|----------|---------|-------------|
| Export format? | CLAUDE.md (Recommended); AGENTS.md; Both | false |

### Question 3: Detail Options (only if applicable)

| Selection | Question | Options | MultiSelect |
|-----------|----------|---------|-------------|
| Statusline | Mode? | Full (Recommended); Minimal | false |
| AI Performance | Thinking tokens? | Standard 5K; Medium 8K (Recommended); High 10K | false |
| AI Performance | MCP Output tokens? | Standard 25K; Large 35K (Recommended); Very Large 50K | false |
| Permissions | Level? | Safe; Balanced (Recommended); Permissive; Full | false |

---

## Step 3: Detection (if selected)

**Spawn analyze agent with config scope:**

```
Task(cco-agent-analyze, prompt="scope=config - Detect project configuration")
```

Agent returns JSON with:
- `status`: Current state
- `detections`: All detected elements with confidence
- `context`: Generated context.md content
- `aiPerf`: Calculated AI performance values
- `rules`: Generated rule files with content
- `guidelines`: Generated guidelines

---

## Step 4: Review

Show detection results table from agent output:

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                           DETECTION RESULTS                                  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  # │ Element       │ Value              │ Conf │ Source              │ Action║
╠════╪═══════════════╪════════════════════╪══════╪═════════════════════╪═══════╣
║  1 │ Purpose       │ {from agent}       │ ●●●  │ {source}            │ ...   ║
║ .. │ ...           │ ...                │ ...  │ ...                 │ ...   ║
╚══════════════════════════════════════════════════════════════════════════════╝

Rules: {list from agent.rules[].file}
AI Performance: {agent.aiPerf.thinking}/{agent.aiPerf.mcpOutput} tokens
```

**Approval → AskUserQuestion** (mandatory):

| Question | Options | MultiSelect |
|----------|---------|-------------|
| Apply this configuration? | Accept; Edit; Cancel | false |

---

## Step 5: Apply

### Rules & Context
Write files from agent output:
- `.claude/rules/cco/context.md` ← agent.context
- `.claude/rules/cco/{file}.md` ← agent.rules[]

### Statusline & Permissions
Use cco-install CLI (reads from package templates):
```bash
cco-install --local . --statusline {mode} --permissions {level}
```

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
- Remove Statusline: `rm .claude/statusline.js`, remove `statusLine` from settings.json
- Remove Permissions: Remove `permissions` from settings.json

---

## Step 6: Report

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                           CCO TUNE COMPLETE                                  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ CHANGES                                                                      ║
├──────────────┬───────────────────┬───────────────────┬───────────────────────┤
║ Setting      │ Before            │ After             │ Reason                ║
├──────────────┼───────────────────┼───────────────────┼───────────────────────┤
║ Context      │ {before}          │ {after}           │ {reason}              ║
║ AI Perf      │ {before}          │ {after}           │ complexity: {score}   ║
║ Statusline   │ {before}          │ {after}           │ {reason}              ║
║ Permissions  │ {before}          │ {after}           │ {reason}              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ FILES WRITTEN                                                                ║
├──────────────────────────────────────────────────────────────────────────────┤
║ {list of written files}                                                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ Restart Claude Code for changes to take effect                               ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## Export Mode

Export reads from existing `.claude/rules/cco/` files (no agent needed):

1. Read global rules: `~/.claude/rules/cco/core.md`, `~/.claude/rules/cco/ai.md`
2. Read project rules: `.claude/rules/cco/*.md`
3. Combine based on user selection
4. Write to `./CLAUDE.export.md` or `./AGENTS.md`

---

## Rules

1. **Agent for detection** - Never run detection commands directly, use Task(cco-agent-detect)
2. **cco-install for templates** - Statusline/permissions via CLI, not generated
3. **Parallel reads** - Read existing files in parallel for status
4. **Minimal orchestration** - This command is coordinator only
5. **JSON handoff** - Agent returns structured data, command displays it

---

## Reference: Question Formatting

| Rule | Description |
|------|-------------|
| `[current]` | Matches existing config (priority 1) |
| `[detected]` | Auto-detected, not in config (priority 2) |
| `(Recommended)` | Best practice, max 1/question (priority 3) |
| Precedence | If detected AND current → show `[current]` only |

---

## Reference: Permissions Levels

| Level | Description |
|-------|-------------|
| Safe | Read-only auto-approved |
| Balanced | Read + lint/test auto-approved |
| Permissive | Most operations auto-approved |
| Full | All operations auto-approved (Solo + Public only) |
