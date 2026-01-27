---
description: Configure CCO for this project - analyze stack, create profile, load rules
argument-hint: [--check] [--force]
allowed-tools: Read(*), Grep(*), Glob(*), Task(*), AskUserQuestion
model: haiku
---

# /tune

**Configure CCO** - Analyze project, create profile, load appropriate rules.

> **Implementation Note:** This command orchestrates the setup process. Heavy lifting is done by agents.

## Args

- `--check`: Silent validation only, return status (for other commands)
- `--force`: Skip confirmation, update even if profile exists

## Context

- Profile path: `.claude/rules/cco-profile.md`

## Architecture

| Step | Action | Tool |
|------|--------|------|
| 1 | Validate existing profile | Read + field check |
| 2 | Ask user (if needed) | AskUserQuestion |
| 3 | Analyze project | Task(cco-agent-analyze) |
| 4 | Write profile + rules | Task(cco-agent-apply) |

**Fast operation** - typically completes in under 30 seconds.

---

## Step-1: Profile Validation

```javascript
// Read existing profile if exists
const profilePath = ".claude/rules/cco-profile.md"
let profile = null
let validationResult = { valid: false, missing: [], outdated: false }

try {
  const content = await Read(profilePath)
  profile = parseYamlFrontmatter(content)

  // Required fields check
  const requiredFields = [
    "project.name",
    "project.purpose",
    "stack.languages",
    "stack.frameworks",
    "maturity",
    "commands"
  ]

  validationResult.missing = requiredFields.filter(field => !getNestedValue(profile, field))
  validationResult.valid = validationResult.missing.length === 0

} catch (e) {
  // Profile doesn't exist
  validationResult.valid = false
  validationResult.missing = ["entire profile"]
}
```

### Check Mode (--check)

```javascript
if (args.includes("--check")) {
  // Silent mode for other commands
  if (validationResult.valid) {
    return { status: "ok", profile: profile }
  }
  // Profile invalid - continue to setup flow (Step-2, Step-3)
  // After setup completes: return { status: "ok" }
  // If user selects Skip: return { status: "skipped" }
}
```

### Profile Exists - Ask Update

```javascript
if (profile && validationResult.valid && !args.includes("--force")) {
  const answer = await AskUserQuestion([{
    question: "CCO profile already exists and is valid. Update it?",
    header: "Profile",
    options: [
      { label: "Keep current", description: "No changes needed" },
      { label: "Update", description: "Re-analyze project and refresh profile (~30s)" }
    ],
    multiSelect: false
  }])

  if (answer === "Keep current") {
    console.log("Profile unchanged.")
    return { status: "ok", profile: profile }
  }
}
```

### Profile Missing or Incomplete

```javascript
if (!validationResult.valid) {
  const missingInfo = validationResult.missing.join(", ")

  const answer = await AskUserQuestion([{
    question: `CCO profile ${profile ? "is incomplete" : "not found"}. Configure now?`,
    header: "Setup",
    options: [
      { label: "Auto-setup (Recommended)", description: "Detect stack automatically (~30s)" },
      { label: "Interactive", description: "Answer questions to customize" },
      { label: "Skip", description: "Don't configure CCO for this project" }
    ],
    multiSelect: false
  }])

  if (answer === "Skip") {
    return { status: "skipped" }
  }

  config.mode = answer.includes("Auto") ? "auto" : "interactive"
}
```

---

## Step-2: Analyze Project

```javascript
console.log("Analyzing project...")

const configData = await Task("cco-agent-analyze", `
  scope: config
  mode: ${config.mode}

  ${config.mode === "auto" ?
    "Detect stack without questions. Return { detected, answers: defaults }" :
    "Ask questions while detecting. Return { detected, answers }"
  }
`, { model: "haiku" })
```

---

## Step-3: Write Profile & Rules

```javascript
console.log("Writing profile and rules...")

await Task("cco-agent-apply", `
  scope: config
  input: ${JSON.stringify(configData)}

  1. Delete existing cco-*.md files in .claude/rules/
  2. Write cco-profile.md with detected config
  3. Copy relevant rule files from plugin
  4. Output profile summary for immediate use
`, { model: "opus" })
```

---

## Step-4: Summary

```javascript
console.log(`
## CCO Configured

Profile: .claude/rules/cco-profile.md
Rules: ${configData.rulesNeeded.length} files loaded

Stack detected:
- Languages: ${configData.detected.languages.join(", ")}
- Frameworks: ${configData.detected.frameworks.join(", ")}

Run /cco:optimize or /cco:align to start improving your code.
`)
```

---

## Output Schema

```json
{
  "status": "ok|skipped|error",
  "profile": { ... },
  "rulesLoaded": ["cco-typescript.md", "cco-react.md", ...]
}
```

---

## Usage Examples

```bash
/cco:tune              # Interactive setup or update
/cco:tune --check      # Silent validation (for other commands)
/cco:tune --force      # Force update without confirmation
```

---

## Integration with Other Commands

Other commands call `/cco:tune --check` at start:

```javascript
// In /optimize, /align, /preflight:
const tuneResult = await Skill("tune", "--check")

if (tuneResult.status === "skipped") {
  return  // User declined setup
}

// Continue with command...
```
