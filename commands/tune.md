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

  Detect and populate ALL required fields:

  ## Auto-Detection Rules (mode: auto)

  | Field | Source | Fallback |
  |-------|--------|----------|
  | project.name | package.json/pyproject.toml/Cargo.toml "name" | Directory name |
  | project.purpose | README.md first paragraph or description field | "Software project" |
  | stack.languages | File extensions (.py→Python, .ts→TypeScript, etc.) | [] |
  | stack.frameworks | Dependencies (react, fastapi, django, etc.) | [] |
  | maturity | Git history + test coverage + docs presence | "development" |
  | commands.format | package.json scripts, Makefile, pyproject.toml | null |
  | commands.lint | Same sources | null |
  | commands.test | Same sources | null |
  | commands.build | Same sources | null |

  ## Detection Steps

  1. Read manifest files: package.json, pyproject.toml, Cargo.toml, go.mod, pom.xml
  2. Scan file extensions in src/, lib/, app/ directories
  3. Parse README.md for project description
  4. Check for test directories and coverage config
  5. Extract scripts/commands from manifest

  ## Maturity Detection

  | Indicator | Score |
  |-----------|-------|
  | Has tests | +1 |
  | Has CI config (.github/workflows, .gitlab-ci) | +1 |
  | Has docs/ or README >500 chars | +1 |
  | Git history >100 commits | +1 |
  | Has changelog | +1 |

  Score: 0-1 → "prototype", 2-3 → "development", 4-5 → "production"

  ${config.mode === "auto" ?
    "Return { detected, answers: defaults } - NO questions asked" :
    "Ask user to confirm/override each detected value"
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

## Profile Schema [CRITICAL]

The generated `cco-profile.md` must have this exact structure:

```yaml
---
# CCO Profile - Auto-generated by /cco:tune
project:
  name: "project-name"           # REQUIRED
  purpose: "Brief description"   # REQUIRED
  type: "api|cli|library|web"    # Optional

stack:
  languages:                     # REQUIRED (at least one)
    - Python
    - TypeScript
  frameworks:                    # REQUIRED (can be empty [])
    - FastAPI
    - React

maturity: "prototype|development|production"  # REQUIRED

commands:                        # REQUIRED (section must exist)
  format: "black . --check"      # Optional
  lint: "ruff check ."           # Optional
  test: "pytest tests/ -v"       # Optional
  build: "npm run build"         # Optional
  type: "mypy src/"              # Optional
---

# Project Profile

Additional context about the project...
```

**Validation:** All 6 required fields must be present and non-empty.

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
