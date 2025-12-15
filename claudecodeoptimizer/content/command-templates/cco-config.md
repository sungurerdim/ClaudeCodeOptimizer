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

## Step 2: User Questions (All in Command)

**All user interaction happens here.** Agent only does detection, no questions.

### Q1: Action Type

```
AskUserQuestion([
  { question: "What would you like to do?", header: "Action",
    options: [
      { label: "Configure", description: "Set up or update project configuration" },
      { label: "Remove", description: "Remove existing CCO configuration" },
      { label: "Export", description: "Export rules to AGENTS.md or CLAUDE.md" }
    ], multiSelect: false }
])
```

**Dynamic labels:** AI adds `(Recommended)` based on context (e.g., no existing config → Configure recommended).

### Q2: Scope (based on Q1 answer)

**If Configure:**
```
AskUserQuestion([
  { question: "What to configure?", header: "Scope",
    options: [
      { label: "Detection & Rules", description: "Auto-detect stack, generate rules" },
      { label: "AI Performance", description: "Extended thinking, tool output limits" },
      { label: "Statusline", description: "Custom status bar display" },
      { label: "Permissions", description: "Tool approval settings" }
    ], multiSelect: true }
])
```

**If Remove:**
```
AskUserQuestion([
  { question: "What to remove?", header: "Scope",
    options: [
      { label: "Rules", description: "Remove .claude/rules/cco/" },
      { label: "AI Performance", description: "Remove env settings" },
      { label: "Statusline", description: "Remove cco-statusline.js" },
      { label: "Permissions", description: "Remove permissions from settings" }
    ], multiSelect: true }
])
```

**If Export:**
```
AskUserQuestion([
  { question: "Export format?", header: "Format",
    options: [
      { label: "AGENTS.md", description: "Universal, works with Codex/Cursor" },
      { label: "CLAUDE.md", description: "Claude Code specific format" }
    ], multiSelect: false }
])
```

### Q3: Details (based on Q2 selections)

**If Statusline selected:**
```
AskUserQuestion([
  { question: "Statusline mode?", header: "Mode",
    options: [
      { label: "cco-full", description: "Full status with all metrics" },
      { label: "cco-minimal", description: "Compact single-line display" }
    ], multiSelect: false }
])
```

**If AI Performance selected:**
```
AskUserQuestion([
  { question: "Extended thinking token limit?", header: "Thinking",
    options: [
      { label: "8K", description: "Standard projects" },
      { label: "5K", description: "Simple CLI tools" },
      { label: "10K", description: "Complex/large projects" }
    ], multiSelect: false },
  { question: "Tool output token limit?", header: "Output",
    options: [
      { label: "35K", description: "Standard projects" },
      { label: "25K", description: "Simple projects" },
      { label: "50K", description: "Large codebases" }
    ], multiSelect: false }
])
```

**Dynamic labels:** AI adds `(Recommended)` based on project Scale/Type from context.

**If Permissions selected:**
```
AskUserQuestion([
  { question: "Permission level?", header: "Level",
    options: [
      { label: "Safe", description: "Read-only operations" },
      { label: "Balanced", description: "Read + lint/test auto-approved" },
      { label: "Permissive", description: "Most operations auto-approved" },
      { label: "Full", description: "All operations (Solo + Public only)" }
    ], multiSelect: false }
])
```

**Dynamic labels:** AI adds `(Recommended)` based on Team/Data context.

**AI Performance Recommendations** (AI uses this table to determine recommendations):

| Context | Thinking | Tool Output |
|---------|----------|-------------|
| Small + Simple CLI | 5K | 25K |
| Small-Medium + Standard | 8K | 35K |
| Medium-Large OR Complex | 10K | 50K |

### Q4: Project Context (if "Detection & Rules" selected)

**Batch 1 - Team & Data (4 questions, single AskUserQuestion call):**

```
AskUserQuestion([
  { question: "How many active contributors?", header: "Team",
    options: [
      { label: "Solo", description: "Single developer, no formal review" },
      { label: "Small (2-5)", description: "Small team with async PR reviews" },
      { label: "Large (6+)", description: "Large team requiring ADR/CODEOWNERS" }
    ], multiSelect: false },
  { question: "Expected scale (concurrent users)?", header: "Scale",
    options: [
      { label: "Prototype (<100)", description: "Development only" },
      { label: "Small (100-1K)", description: "Basic caching needed" },
      { label: "Medium (1K-10K)", description: "Connection pools, async required" },
      { label: "Large (10K+)", description: "Circuit breakers, advanced patterns" }
    ], multiSelect: false },
  { question: "Most sensitive data handled?", header: "Data",
    options: [
      { label: "Public", description: "Open data, no sensitivity" },
      { label: "PII", description: "Personal identifiable information" },
      { label: "Regulated", description: "Healthcare, finance, regulated data" }
    ], multiSelect: false },
  { question: "Required compliance frameworks?", header: "Compliance",
    options: [
      { label: "None", description: "No specific requirements" },
      { label: "SOC2", description: "Service Organization Control 2" },
      { label: "HIPAA", description: "Healthcare data protection" },
      { label: "GDPR", description: "EU data privacy regulation" }
    ], multiSelect: true }
])
```

**Batch 2 - Operations & Policy (4 questions, single AskUserQuestion call):**

```
AskUserQuestion([
  { question: "Uptime commitment (SLA)?", header: "SLA",
    options: [
      { label: "None", description: "Best effort, no commitment" },
      { label: "99%", description: "~7 hours/month downtime" },
      { label: "99.9%", description: "~43 minutes/month downtime" },
      { label: "99.99%", description: "~4 minutes/month downtime" }
    ], multiSelect: false },
  { question: "Current development stage?", header: "Maturity",
    options: [
      { label: "Prototype", description: "May be discarded, rapid iteration" },
      { label: "Active", description: "Regular releases, growing features" },
      { label: "Stable", description: "Maintenance mode, bug fixes only" },
      { label: "Legacy", description: "Minimal changes, keeping alive" }
    ], multiSelect: false },
  { question: "Breaking change policy?", header: "Breaking",
    options: [
      { label: "Allowed", description: "Pre-1.0, breaking changes OK" },
      { label: "Minimize", description: "Deprecate first, migration path" },
      { label: "Never", description: "Enterprise, strict compatibility" }
    ], multiSelect: false },
  { question: "Primary development focus?", header: "Priority",
    options: [
      { label: "Speed", description: "Ship fast, iterate quickly" },
      { label: "Balanced", description: "Standard practices" },
      { label: "Quality", description: "Thorough testing and review" },
      { label: "Security", description: "Security-first development" }
    ], multiSelect: false }
])
```

**Store all answers as `userInput` object for agent.**

---

## Step 3: Agent Detection (Detection Only)

**Only runs if "Detection & Rules" selected in Step 2.**

### Agent Invocation

```
agentResponse = Task(cco-agent-analyze, prompt=`
  scope=config
  userInput: ${JSON.stringify(userInput)}

  Detection only - do NOT ask user questions (already collected).
  Return detections, rules, context based on provided userInput.
`)
```

### Agent Responsibilities (No User Interaction)

1. **Auto-detect** from manifest/code/config/docs (Language, DB, Infra, etc.)
2. **Read adaptive.md** via `cco-install --cat rules/cco-adaptive.md`
3. **Select rules** based on detections + provided userInput
4. **Return** JSON with detections, rules, triggeredCategories

### Confirm Questions (Command asks after agent returns)

**If agent returns MEDIUM confidence detections, ask user to confirm:**

```
// After agent returns - command builds confirmation questions dynamically
// Labels with [detected] or [current] are added by AI based on agent response
AskUserQuestion([
  // For {category} (if MEDIUM confidence)
  { question: "Confirm {category}?", header: "{Category}",
    options: [
      { label: "{detected_value}", description: "{detection_source}" },
      { label: "{alternative_1}", description: "{alt_1_description}" },
      { label: "{alternative_2}", description: "{alt_2_description}" }
    ], multiSelect: false }
])
```

| Confidence | Action |
|------------|--------|
| HIGH | Trust, don't ask (e.g., language from manifest) |
| MEDIUM | **AskUserQuestion** - AI adds `[detected]` to detected option |
| LOW | **AskUserQuestion** - no marker, needs user input |

### Response Validation

```
// Minimal validation - no questionsAsked check needed
function validateAgentResponse(response) {
  if (!response.detections?.language?.length) {
    return { valid: false, reason: "No language detected" }
  }
  if (!response.rules?.length) {
    return { valid: false, reason: "No rules generated" }
  }
  return { valid: true }
}
```

---

## Step 4: Review

**Show detection results table to user**, then ask for approval:

```
AskUserQuestion([
  { question: "Apply this configuration?", header: "Apply",
    options: [
      { label: "Accept", description: "Apply all detected settings and rules" },
      { label: "Edit", description: "Modify some settings before applying" },
      { label: "Cancel", description: "Discard and exit" }
    ], multiSelect: false }
])
```

**If Edit selected:** Return to relevant question batch for modification.

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

| Variable | Purpose | Values |
|----------|---------|--------|
| `MAX_THINKING_TOKENS` | Extended thinking budget | 5000, 8000, 10000 |
| `MAX_MCP_OUTPUT_TOKENS` | Tool output limit | 25000, 35000, 50000 |

### Remove Operations
- Remove Rules: `rm -rf .claude/rules/cco/`
- Remove AI Perf: Remove `env` from settings.json
- Remove Statusline: `rm .claude/cco-statusline.js`, remove `statusLine` from settings.json
- Remove Permissions: Remove `permissions` from settings.json

---

## Step 6: Report

Shows: Changes (before/after), Files written, Triggered Rules, Restart reminder

### Report Format

```
## Configuration Applied

### Files Written
| File | Action |
|------|--------|
| .claude/rules/cco/context.md | {created|updated} |
| .claude/rules/cco/{language}.md | {created|updated} |
| .claude/rules/cco/{type}.md | {created|updated} |
| .claude/settings.json | {created|updated} |

### Triggered Rule Categories
| Category | Trigger | Rules | Source |
|----------|---------|-------|--------|
| Language | L:{language} | {language}.md | auto |
| Type | T:{type} | {type}.md | auto |
| Scale | {scale} | scale.md ({tier}) | user |
| Team | {team} | {team_rule|"-"} | user |
| Testing | {testing} | testing.md ({tier}) | user |
| Data | {data} | {security_rule|"-"} | user |
| Compliance | {compliance} | {compliance_rules|"-"} | user |

### User Inputs Applied
| Element | Value | Effect |
|---------|-------|--------|
| Team | {team} | {team_effect} |
| Scale | {scale} | {scale_effect} |
| Data | {data} | {data_effect} |
| Compliance | {compliance} | {compliance_effect} |
| Testing | {testing} | {testing_effect} |
| SLA | {sla} | {sla_effect} |
| Maturity | {maturity} | {maturity_guideline} |
| Breaking | {breaking} | {breaking_guideline} |
| Priority | {priority} | {priority_guideline} |

### Next Steps
- Restart Claude Code to apply new rules
- Run /cco-status to verify configuration
```

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

### Dynamic Label Rules

**AI applies these labels dynamically based on context - never hardcode in templates:**

| Label | When AI Applies | Priority |
|-------|-----------------|----------|
| `[current]` | Option matches existing config value | 1 (highest) |
| `[detected]` | Option matches agent detection result | 2 |
| `(Recommended)` | Option matches best practice for context | 3 |

**Label application logic:**
- Read existing settings → mark matching option with `[current]`
- Check agent detections → mark matching option with `[detected]`
- Apply recommendation table → mark best option with `(Recommended)`
- If multiple apply, use highest priority label only

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
