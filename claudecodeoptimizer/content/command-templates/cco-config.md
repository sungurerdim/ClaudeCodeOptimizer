---
name: cco-config
description: Configure project context and AI behavior
allowed-tools: Read(*), Write(*), Edit(*), Bash(cco-install:*), Task(*), TodoWrite, AskUserQuestion
---

# /cco-config

**Project tuning** - Lightweight orchestrator using sub-agents for heavy work.

## Context

- Context exists: !`test -f ./.claude/rules/cco/context.md && echo "1" || echo "0"`
- Existing rules: !`test -d .claude/rules/cco && ls .claude/rules/cco/*.md | xargs -I{} basename {} | tr '\n' ' ' | grep . || echo "None"`
- Settings exists: !`test -f ./.claude/settings.json && echo "1" || echo "0"`

## Architecture

| Step | Name | Action |
|------|------|--------|
| 1 | Status | Read existing files |
| 2 | Action | Ask what to do |
| 3 | Scope | Ask what to configure/remove/export |
| 4 | Details | Ask specific options (if applicable) |
| 5 | Context | Ask project context (if Detection selected) |
| 6 | Detection | Run agent with userInput |
| 7 | Review | Show results, ask approval |
| 8 | Apply | Write files via agent/CLI |
| 9 | Report | Summary of changes |

---

## Progress Tracking [CRITICAL]

**Initialize at start. Update status after each step completes.**

```javascript
TodoWrite([
  { content: "Step-1: Read status", status: "in_progress", activeForm: "Reading project status" },
  { content: "Step-2: Ask action type", status: "pending", activeForm: "Asking action type" },
  { content: "Step-3: Ask scope", status: "pending", activeForm: "Asking scope selection" },
  { content: "Step-4: Ask detail options", status: "pending", activeForm: "Asking detail options" },
  { content: "Step-5: Ask project context", status: "pending", activeForm: "Asking project context" },
  { content: "Step-6: Run detection", status: "pending", activeForm: "Running detection agent" },
  { content: "Step-7: Review results", status: "pending", activeForm: "Reviewing detection results" },
  { content: "Step-8: Apply configuration", status: "pending", activeForm: "Applying configuration" },
  { content: "Step-9: Show report", status: "pending", activeForm: "Showing final report" }
])
```

---

## Step-1: Status

Read existing files in parallel: context.md, settings.json, rules list.

Display status box with: Project, Context, AI Perf, Statusline, Permissions, Rules.

### Validation
```
[x] Files read: context.md, settings.json
[x] Status displayed to user
→ Proceed to Step-2
```

---

## Step-2: Action

**Ask what user wants to do.**

```javascript
AskUserQuestion([{
  question: "What would you like to do?",
  header: "Action",
  options: [
    { label: "Configure", description: "Set up or update project configuration" },
    { label: "Remove", description: "Remove existing CCO configuration" },
    { label: "Export", description: "Export rules to AGENTS.md or CLAUDE.md" }
  ],
  multiSelect: false
}])
```

**Dynamic labels:** Add `(Recommended)` if no existing config → Configure recommended.

### Validation
```
[x] User selected: Configure | Remove | Export
→ Store as: action = {selection}
→ Proceed to Step-3
```

---

## Step-3: Scope

**Ask what to configure/remove/export based on Step-2 answer.**

### If action = Configure

```javascript
AskUserQuestion([{
  question: "What to configure?",
  header: "Scope",
  options: [
    { label: "Detection & Rules", description: "Auto-detect stack, generate rules" },
    { label: "AI Performance", description: "Extended thinking, tool output limits" },
    { label: "Statusline", description: "Custom status bar display" },
    { label: "Permissions", description: "Tool approval settings" }
  ],
  multiSelect: true
}])
```

### If action = Remove

```javascript
AskUserQuestion([{
  question: "What to remove?",
  header: "Scope",
  options: [
    { label: "Rules", description: "Remove .claude/rules/cco/" },
    { label: "AI Performance", description: "Remove env settings" },
    { label: "Statusline", description: "Remove cco-statusline.js" },
    { label: "Permissions", description: "Remove permissions from settings" }
  ],
  multiSelect: true
}])
```

### If action = Export

```javascript
AskUserQuestion([{
  question: "Export format?",
  header: "Format",
  options: [
    { label: "AGENTS.md", description: "Universal, works with Codex/Cursor" },
    { label: "CLAUDE.md", description: "Claude Code specific format" }
  ],
  multiSelect: false
}])
```

### Validation
```
[x] User selected scope items
→ Store as: scope = {selections[]}
→ If action=Export: Skip to Step-8
→ If action=Remove: Skip to Step-8
→ Proceed to Step-4
```

---

## Step-4: Details

**Ask specific options for selected scope items. Skip if nothing applicable.**

### If "Statusline" in scope

```javascript
AskUserQuestion([{
  question: "Statusline mode?",
  header: "Mode",
  options: [
    { label: "cco-full", description: "Full status with all metrics" },
    { label: "cco-minimal", description: "Compact single-line display" }
  ],
  multiSelect: false
}])
```

### If "AI Performance" in scope

```javascript
AskUserQuestion([
  {
    question: "Extended thinking token limit?",
    header: "Thinking",
    options: [
      { label: "5K", description: "Simple CLI tools" },
      { label: "8K", description: "Standard projects" },
      { label: "10K", description: "Complex/large projects" }
    ],
    multiSelect: false
  },
  {
    question: "Tool output token limit?",
    header: "Output",
    options: [
      { label: "25K", description: "Simple projects" },
      { label: "35K", description: "Standard projects" },
      { label: "50K", description: "Large codebases" }
    ],
    multiSelect: false
  }
])
```

**Recommendation table (for dynamic labels):**

| Context | Thinking | Output |
|---------|----------|--------|
| Small + Simple CLI | 5K | 25K |
| Small-Medium + Standard | 8K | 35K |
| Medium-Large OR Complex | 10K | 50K |

### If "Permissions" in scope

```javascript
AskUserQuestion([{
  question: "Permission level?",
  header: "Level",
  options: [
    { label: "Safe", description: "Read-only operations" },
    { label: "Balanced", description: "Read + lint/test auto-approved" },
    { label: "Permissive", description: "Most operations auto-approved" },
    { label: "Full", description: "All operations (Solo + Public only)" }
  ],
  multiSelect: false
}])
```

### Validation
```
[x] Detail options collected (or skipped if none applicable)
→ Store as: details = { statusline?, aiPerf?, permissions? }
→ If "Detection & Rules" NOT in scope: Skip to Step-8
→ Proceed to Step-5
```

---

## Step-5: Project Context [MANDATORY if "Detection & Rules" in scope]

**Collect userInput for detection agent. Two batches, 4 questions each.**

### Step-5.1: Team & Data

```javascript
AskUserQuestion([
  {
    question: "How many active contributors?",
    header: "Team",
    options: [
      { label: "Solo", description: "Single developer, no formal review" },
      { label: "Small (2-5)", description: "Small team with async PR reviews" },
      { label: "Large (6+)", description: "Large team requiring ADR/CODEOWNERS" }
    ],
    multiSelect: false
  },
  {
    question: "Expected scale (concurrent users)?",
    header: "Scale",
    options: [
      { label: "Prototype (<100)", description: "Development only" },
      { label: "Small (100-1K)", description: "Basic caching needed" },
      { label: "Medium (1K-10K)", description: "Connection pools, async required" },
      { label: "Large (10K+)", description: "Circuit breakers, advanced patterns" }
    ],
    multiSelect: false
  },
  {
    question: "Most sensitive data handled?",
    header: "Data",
    options: [
      { label: "Public", description: "Open data, no sensitivity" },
      { label: "PII", description: "Personal identifiable information" },
      { label: "Regulated", description: "Healthcare, finance, regulated data" }
    ],
    multiSelect: false
  },
  {
    question: "Compliance requirements? (1/3: Common)",
    header: "Compliance",
    options: [
      { label: "None", description: "No compliance requirements - skip remaining" },
      { label: "SOC2", description: "B2B SaaS, enterprise customers" },
      { label: "HIPAA", description: "US healthcare data (PHI)" },
      { label: "PCI", description: "Payment card processing" }
    ],
    multiSelect: true
  }
])
```

### Step-5.1b: Compliance (Privacy) - Skip if "None" selected above

```javascript
AskUserQuestion([{
  question: "Compliance requirements? (2/3: Privacy)",
  header: "Compliance",
  options: [
    { label: "GDPR", description: "EU data privacy, user rights" },
    { label: "CCPA", description: "California consumer privacy" },
    { label: "ISO27001", description: "International security standard" },
    { label: "Skip", description: "No additional privacy requirements" }
  ],
  multiSelect: true
}])
```

### Step-5.1c: Compliance (Specialized) - Skip if "None" selected in 5.1

```javascript
AskUserQuestion([{
  question: "Compliance requirements? (3/3: Specialized)",
  header: "Compliance",
  options: [
    { label: "FedRAMP", description: "US government cloud" },
    { label: "DORA", description: "EU financial services (2025+)" },
    { label: "HITRUST", description: "Healthcare + security combined" },
    { label: "Skip", description: "No specialized requirements" }
  ],
  multiSelect: true
}])
```

### Step-5.1d: Testing

```javascript
AskUserQuestion([{
  question: "Test coverage level?",
  header: "Testing",
  options: [
    { label: "Basics (60%)", description: "Unit tests, basic mocking" },
    { label: "Standard (80%)", description: "+ Integration tests, fixtures, CI gates" },
    { label: "Full (90%)", description: "+ E2E, contract testing, mutation testing" }
  ],
  multiSelect: false
}])
```

**Dynamic label:** Add `[detected]` if coverage config found in CI/package.json.

### Step-5.2: Operations & Policy

```javascript
AskUserQuestion([
  {
    question: "Uptime commitment (SLA)?",
    header: "SLA",
    options: [
      { label: "None", description: "Best effort, no commitment" },
      { label: "99%", description: "~7 hours/month downtime" },
      { label: "99.9%", description: "~43 minutes/month downtime" },
      { label: "99.99%", description: "~4 minutes/month downtime" }
    ],
    multiSelect: false
  },
  {
    question: "Current development stage?",
    header: "Maturity",
    options: [
      { label: "Prototype", description: "May be discarded, rapid iteration" },
      { label: "Active", description: "Regular releases, growing features" },
      { label: "Stable", description: "Maintenance mode, bug fixes only" },
      { label: "Legacy", description: "Minimal changes, keeping alive" }
    ],
    multiSelect: false
  },
  {
    question: "Breaking change policy?",
    header: "Breaking",
    options: [
      { label: "Allowed", description: "Pre-1.0, breaking changes OK" },
      { label: "Minimize", description: "Deprecate first, migration path" },
      { label: "Never", description: "Enterprise, strict compatibility" }
    ],
    multiSelect: false
  },
  {
    question: "Primary development focus?",
    header: "Priority",
    options: [
      { label: "Speed", description: "Ship fast, iterate quickly" },
      { label: "Balanced", description: "Standard practices" },
      { label: "Quality", description: "Thorough testing and review" },
      { label: "Security", description: "Security-first development" }
    ],
    multiSelect: false
  }
])
```

### Validation
```
[x] Step-5.1 completed: Team, Scale, Data collected
[x] Step-5.1 Compliance (1/3): Common frameworks collected
[x] Step-5.1b Compliance (2/3): Privacy frameworks collected (skipped if "None" in 5.1)
[x] Step-5.1c Compliance (3/3): Specialized frameworks collected (skipped if "None" in 5.1)
[x] Step-5.1d completed: Testing level collected
[x] Step-5.2 completed: SLA, Maturity, Breaking, Priority collected
→ Store as: userInput = { team, scale, data, compliance[], testing, sla, maturity, breaking, priority }
→ Proceed to Step-6
```

---

## Step-6: Detection

**Run agent with collected userInput. Agent does NOT ask questions.**

```javascript
agentResponse = Task("cco-agent-analyze", `
  scope=config
  userInput: ${JSON.stringify(userInput)}

  Detection only - do NOT ask user questions (already collected).
  Return detections, rules, context based on provided userInput.
`)
```

### Agent Responsibilities

1. **Auto-detect** from manifest/code/config/docs (Language, DB, Infra, etc.)
2. **Read adaptive.md** via `cco-install --cat rules/cco-adaptive.md`
3. **Select rules** based on detections + provided userInput
4. **Return** JSON with detections, rules, context, triggeredCategories

### Confidence Handling (after agent returns)

| Confidence | Action |
|------------|--------|
| HIGH | Trust, don't ask |
| MEDIUM | AskUserQuestion with `[detected]` label |
| LOW | AskUserQuestion, no marker |

### Validation
```
[x] Agent returned valid response
[x] response.detections.language exists
[x] response.rules.length > 0
[x] MEDIUM confidence items confirmed with user (if any)
→ Proceed to Step-7
```

---

## Step-7: Review

**Show detection results table, then ask approval.**

Display table with: Element, Value, Confidence, Source columns.

```javascript
AskUserQuestion([{
  question: "Apply this configuration?",
  header: "Apply",
  options: [
    { label: "Accept", description: "Apply all detected settings and rules" },
    { label: "Edit", description: "Modify some settings before applying" },
    { label: "Cancel", description: "Discard and exit" }
  ],
  multiSelect: false
}])
```

### Validation
```
[x] Results displayed to user
[x] User selected: Accept | Edit | Cancel
→ If Cancel: Exit with no changes
→ If Edit: Return to relevant step (Step-4 or Step-5)
→ If Accept: Proceed to Step-8
```

---

## Step-8: Apply

### If action = Configure

**Rules & Context** (from agent output):
- `.claude/rules/cco/context.md` ← agent.context
- `.claude/rules/cco/{file}.md` ← agent.rules[]

**Statusline & Permissions** (via CLI only):
```bash
cco-install --local . --statusline {mode} --permissions {level}
```

**AI Performance** (write to settings.json):
```json
{
  "env": {
    "MAX_THINKING_TOKENS": "{value}",
    "MAX_MCP_OUTPUT_TOKENS": "{value}",
    "DISABLE_PROMPT_CACHING": "0"
  }
}
```

### If action = Remove

| Selection | Action |
|-----------|--------|
| Rules | `rm -rf .claude/rules/cco/` |
| AI Perf | Remove `env` from settings.json |
| Statusline | `rm .claude/cco-*.js`, remove `statusLine` from settings.json |
| Permissions | Remove `permissions` from settings.json |

### If action = Export

Read global + project rules, apply format:

| Format | Target | Rules | Output |
|--------|--------|-------|--------|
| AGENTS.md | Universal | Core + AI (filtered) | ./AGENTS.md |
| CLAUDE.md | Claude Code | Core + AI + Tools | ./CLAUDE.export.md |

**AGENTS.md filtering:** Remove tool names, paths, product refs, CCO-specific.

### Validation
```
[x] Files written/removed as specified
[x] No errors during apply
→ Proceed to Step-9
```

---

## Step-9: Report

### Format

```
## Configuration Applied

### Files Written
| File | Action |
|------|--------|
| .claude/rules/cco/context.md | {created|updated} |
| .claude/rules/cco/{language}.md | {created|updated} |
| .claude/settings.json | {created|updated} |

### User Inputs Applied
| Element | Value | Effect |
|---------|-------|--------|
| Team | {team} | {effect} |
| Scale | {scale} | {effect} |
| ... | ... | ... |

### Next Steps
- Restart Claude Code to apply new rules
- Run /cco-status to verify configuration
```

### Validation
```
[x] Report displayed
[x] All todos marked completed
→ Done
```

---

## Reference

### Dynamic Label Rules

| Label | When to Apply | Priority |
|-------|---------------|----------|
| `[current]` | Option matches existing config | 1 (highest) |
| `[detected]` | Option matches agent detection | 2 |
| `(Recommended)` | Option is best practice | 3 |

### Permissions Levels

| Level | Auto-approved |
|-------|---------------|
| Safe | Read-only |
| Balanced | Read + lint/test |
| Permissive | Most operations |
| Full | All (Solo + Public only) |

---

## Recovery

If something goes wrong during configuration:

| Situation | Recovery |
|-----------|----------|
| Wrong rules generated | Re-run `/cco-config`, select "Detection & Rules", adjust answers |
| Want to start fresh | Run `/cco-config` → Remove → Rules, then Configure again |
| Settings.json corrupted | Delete `.claude/settings.json`, re-run `/cco-config` |
| Detection crashed | Re-run `/cco-config` - detection is stateless |
| Wrong AI Performance | `/cco-config` → Configure → AI Performance, select new values |
| Applied wrong permissions | `cco-install --local . --permissions {correct-level}` |

**Safe pattern:** CCO config files are additive. Removing and re-creating is always safe.

---

## Rules

1. **Sequential execution** - Complete each step before proceeding
2. **Validation gates** - Check validation block before next step
3. **Agent for detection** - Use Task(cco-agent-analyze), never detect directly
4. **cco-install for templates** - Statusline/permissions via CLI only
5. **No skipping** - Step-5 is MANDATORY when "Detection & Rules" selected
