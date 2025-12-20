---
name: cco-config
description: Configure project context and AI behavior
allowed-tools: Read(*), Write(*), Edit(*), Bash(cco-install:*), Task(*), TodoWrite, AskUserQuestion
---

# /cco-config

**Project tuning** - Pre-detection reduces questions, parallel apply.

## Context

- Context exists: !`test -f ./.claude/rules/cco/context.md && echo "1" || echo "0"`
- Existing rules: !`test -d .claude/rules/cco && ls .claude/rules/cco/*.md | xargs -I{} basename {} | tr '\n' ' ' | grep . || echo "None"`
- Settings exists: !`test -f ./.claude/settings.json && echo "1" || echo "0"`

## Architecture

| Step | Name | Action | Optimization |
|------|------|--------|--------------|
| 1 | Pre-detect | cco-agent-analyze (config scope) | Skip questions |
| 2 | Status | Show detected + existing | Instant |
| 3 | Action | Ask what to do | Skip if --configure |
| 4 | Scope | Ask what to configure | Skip detected |
| 5 | Context | Only LOW confidence items | Fewer questions |
| 6 | Review | Show + ask approval | Instant |
| 7 | Apply | Write files | Background |
| 8 | Report | Summary | Instant |

---

## Progress Tracking [CRITICAL]

**Initialize at start. Update status after each step completes.**

```javascript
TodoWrite([
  { content: "Step-1: Pre-detect (parallel)", status: "in_progress", activeForm: "Running pre-detection" },
  { content: "Step-2: Show status", status: "pending", activeForm: "Showing status" },
  { content: "Step-3: Ask action", status: "pending", activeForm: "Asking action type" },
  { content: "Step-4: Ask scope + context", status: "pending", activeForm: "Asking scope and context" },
  { content: "Step-5: Review results", status: "pending", activeForm: "Reviewing results" },
  { content: "Step-6: Apply configuration", status: "pending", activeForm: "Applying configuration" },
  { content: "Step-7: Show report", status: "pending", activeForm: "Showing final report" }
])
```

---

## Step-1: Pre-detect [PARALLEL]

**Launch cco-agent-analyze with config scope to auto-detect project context:**

```javascript
// CRITICAL: Single cco-agent-analyze call with config scope
// Agent handles all detection internally with parallelization

Task("cco-agent-analyze", `
  scopes: ["config"]

  Auto-detect from manifest files and code:
  - Language, framework, runtime, packageManager
  - Infrastructure: containerized, ci, cloud, deployment
  - Testing: testFramework, coverage, linters, typeChecker
  - Metadata: license, teamSize, maturity, lastActivity

  Return: {
    detections: {
      language: ["{language}"],
      type: ["{type}"],
      api: "{api|null}",
      database: "{db|null}",
      frontend: "{frontend|null}",
      infra: ["{infra}"],
      dependencies: ["{deps}"]
    },
    sources: [{ file: "{file}", confidence: "{HIGH|MEDIUM|LOW}" }]
  }
`, { model: "haiku" })
```

**Result: Pre-fill answers based on detection confidence**

| Confidence | Action |
|------------|--------|
| HIGH (90%+) | Auto-apply, don't ask |
| MEDIUM (70-89%) | Pre-fill with `[detected]` label |
| LOW (<70%) | Ask user |

### Validation
```
[x] All 4 detection agents completed
[x] Confidence levels assigned
→ Proceed to Step-2
```

---

## Step-2: Status

Display detected + existing configuration:

```
## Project Status

### Auto-Detected (HIGH confidence - won't ask)
| Element | Value | Source |
|---------|-------|--------|
| Language | {language} | {source_file} |
| Framework | {framework} | {source_file} |
| Test Framework | {test_framework} | {source_file} |
| CI | {ci} | {source_file} |

### Needs Confirmation (MEDIUM confidence)
| Element | Value | Source |
|---------|-------|--------|
| Coverage | {coverage}% | {source_file} [detected] |
| Team Size | {team_size} | git contributors |

### Will Ask (LOW confidence)
- Data sensitivity
- Compliance requirements
- SLA commitment

### Existing Configuration
| File | Status |
|------|--------|
| .claude/rules/cco/context.md | {exists/missing} |
| .claude/settings.json | {exists/missing} |
```

### Validation
```
[x] Detection results displayed
[x] Existing config shown
→ Proceed to Step-3
```

---

## Step-3: Action

**Ask what user wants to do.**

```javascript
AskUserQuestion([{
  question: "What would you like to do?",
  header: "Action",
  options: [
    { label: "Configure (Recommended)", description: "Apply detected settings + ask remaining" },
    { label: "Remove", description: "Remove existing CCO configuration" },
    { label: "Export", description: "Export rules to AGENTS.md or CLAUDE.md" }
  ],
  multiSelect: false
}])
```

**Flags override:** `--configure`, `--remove`, `--export` skip this question.

### Validation
```
[x] User selected: Configure | Remove | Export
→ Store as: action = {selection}
→ If Remove or Export: Skip to Step-6
→ Proceed to Step-4
```

---

## Step-4: Scope + Context [ONLY LOW CONFIDENCE ITEMS]

**Only ask questions for items NOT auto-detected or LOW confidence:**

### 4.1: Statusline Setup [ALWAYS ASK - MANDATORY QUESTION]

**CRITICAL: This question MUST always be asked. Statusline is optional but the question is mandatory.**

```javascript
// Statusline question is MANDATORY - never skip
AskUserQuestion([{
  question: "Install CCO statusline?",
  header: "Statusline",
  options: [
    { label: "Full (Recommended)", description: "All metrics: tokens, cost, session time, model" },
    { label: "Compact", description: "Essential metrics only" },
    { label: "Minimal", description: "Token count only" },
    { label: "No", description: "Skip statusline installation" }
  ],
  multiSelect: false
}])
```

### 4.2: Other Settings [OPTIONAL]

```javascript
// Additional settings - optional
AskUserQuestion([{
  question: "Configure additional settings?",
  header: "Settings",
  options: [
    { label: "Permissions", description: "Tool approval levels: safe, balanced, permissive, full" },
    { label: "AI Performance", description: "Extended thinking, tool output limits" },
    { label: "Skip", description: "Only apply detected context rules" }
  ],
  multiSelect: true
}])
```

### 4.3: Context Questions (LOW confidence only)

**Only ask what wasn't detected:**

```javascript
// Build question list dynamically based on detection confidence
lowConfidenceQuestions = []

if (detected.data.confidence < 70) {
  lowConfidenceQuestions.push({
    question: "Most sensitive data handled?",
    header: "Data",
    options: [
      { label: "Public", description: "Open data, no sensitivity" },
      { label: "PII", description: "Personal identifiable information" },
      { label: "Regulated", description: "Healthcare, finance, regulated data" }
    ],
    multiSelect: false
  })
}

if (detected.compliance.confidence < 70) {
  lowConfidenceQuestions.push({
    question: "Compliance requirements?",
    header: "Compliance",
    options: [
      { label: "None", description: "No compliance requirements" },
      { label: "SOC2", description: "B2B SaaS, enterprise customers" },
      { label: "GDPR/CCPA", description: "Privacy regulations" },
      { label: "HIPAA/PCI", description: "Healthcare or payments" }
    ],
    multiSelect: true
  })
}

if (detected.sla.confidence < 70) {
  lowConfidenceQuestions.push({
    question: "Uptime commitment (SLA)?",
    header: "SLA",
    options: [
      { label: "None", description: "Best effort" },
      { label: "99%+", description: "Production SLA" }
    ],
    multiSelect: false
  })
}

// Ask all low-confidence questions in one batch (max 4)
if (lowConfidenceQuestions.length > 0) {
  AskUserQuestion(lowConfidenceQuestions.slice(0, 4))
}
```

**Result: Typically 0-2 questions instead of 8+**

### 4.4: Permission Details [IF SELECTED IN 4.2]

```javascript
// If user selected Permissions in 4.2
if (selectedSettings.includes("Permissions")) {
  AskUserQuestion([{
    question: "Permission approval level?",
    header: "Permissions",
    options: [
      { label: "Balanced (Recommended)", description: "Auto-approve read + lint/test, ask for writes" },
      { label: "Safe", description: "Auto-approve read-only operations" },
      { label: "Permissive", description: "Auto-approve most operations" },
      { label: "Full", description: "Auto-approve all (Solo + Public projects only)" }
    ],
    multiSelect: false
  }])
}
```

### Validation
```
[x] Statusline question asked (mandatory)
[x] Other settings offered
[x] Low confidence context items asked
[x] Permission details collected (if selected)
→ Proceed to Step-5
```

---

## Step-5: Review

**Show merged detection + user input results:**

```
## Configuration Preview

### Auto-Detected (applied automatically)
| Element | Value | Confidence |
|---------|-------|------------|
| Language | {language} | {confidence} |
| Framework | {framework} | {confidence} |
| Test Framework | {test_framework} | {confidence} |
| Coverage | {coverage}% | {confidence} |
| Team Size | {team_size} | {confidence} |

### User Confirmed
| Element | Value |
|---------|-------|
| Data | {data} |
| Compliance | {compliance} |

### Rules Selected
- core.md (always)
- {language}.md (detected)
- {scale}.md (based on context)
- {additional}.md (based on context)

### Settings
| Setting | Value |
|---------|-------|
| AI Thinking | {thinking} (auto: {reason}) |
| Permissions | {permissions} |
```

```javascript
AskUserQuestion([{
  question: "Apply this configuration?",
  header: "Apply",
  options: [
    { label: "Accept (Recommended)", description: "Apply all settings" },
    { label: "Edit", description: "Modify before applying" },
    { label: "Cancel", description: "Discard and exit" }
  ],
  multiSelect: false
}])
```

### Validation
```
[x] Preview displayed
[x] User approved
→ If Cancel: Exit
→ If Edit: Return to Step-4
→ Proceed to Step-6
```

---

## Step-6: Apply [BACKGROUND]

**Write all files in background:**

```javascript
// Launch file writes in parallel
Task("cco-agent-apply", `
  Write files:
  - .claude/rules/cco/context.md ← ${JSON.stringify(context)}
  - .claude/rules/cco/${language}.md ← from template
  - .claude/settings.json ← merge with existing
`, { model: "sonnet", run_in_background: true })

// CLI for statusline/permissions
Bash("cco-install --local . --statusline ${mode} --permissions ${level}")
```

### If action = Remove

```javascript
// Parallel removal
Bash("rm -rf .claude/rules/cco/")
// Edit settings.json to remove CCO entries
```

### If action = Export

```javascript
Task("cco-agent-apply", `
  Export rules to ${format}:
  - Read all .claude/rules/cco/*.md
  - Filter for target format
  - Write to ./${format}
`, { model: "sonnet" })
```

### Validation
```
[x] Files written/removed
[x] No errors
→ Proceed to Step-7
```

---

## Step-7: Report

```
## Configuration Applied

### Files Written
| File | Action |
|------|--------|
| .claude/rules/cco/context.md | {action} |
| .claude/rules/cco/{language}.md | {action} |
| .claude/settings.json | {action} |

### Detection Summary
- Auto-detected: {n} elements
- User confirmed: {n} elements
- Questions asked: {n} (vs {n}+ traditional)

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

1. **Use cco-agent-analyze** - Agent handles detection with config scope
2. **Skip HIGH confidence** - Don't ask what's already detected
3. **Batch LOW confidence** - Ask remaining questions in single batch
4. **Use cco-agent-apply** - Agent handles file writing with verification
5. **Background apply** - Write files while user sees report
