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

**Detection is IDENTICAL for both modes. Only user interaction differs.**

```javascript
console.log("Analyzing project...")

const configData = await Task("cco-agent-analyze", `
  scope: config
  mode: ${config.mode}

  ## Detection Rules [SAME FOR BOTH MODES]

  **CRITICAL: Only use REAL DATA from files. No guessing, no assumptions.**

  All detection is file-based and question-free:

  | Field | Source Files | Detection Method | If Not Found |
  |-------|--------------|------------------|--------------|
  | project.name | package.json, pyproject.toml, Cargo.toml, go.mod | Read "name" field | Use directory name |
  | project.purpose | README.md, package.json "description" | First paragraph or description field | "Not specified" |
  | stack.languages | All source files | Count file extensions | [] empty |
  | stack.frameworks | package.json deps, requirements.txt, Cargo.toml | Match known framework names | [] empty |
  | maturity | .github/, tests/, docs/, CHANGELOG, git log | Score-based calculation | "unknown" |
  | commands.format | package.json scripts, Makefile, pyproject.toml | Match "format", "fmt", "prettier" | null |
  | commands.lint | Same | Match "lint", "eslint", "ruff" | null |
  | commands.test | Same | Match "test", "pytest", "jest" | null |
  | commands.build | Same | Match "build", "compile" | null |

  ## Detection Steps (All File-Based, No Questions)

  1. **Glob** manifest files: package.json, pyproject.toml, Cargo.toml, go.mod, pom.xml
  2. **Read** each manifest, extract name/version/dependencies
  3. **Glob** source files: **/*.{py,ts,js,go,rs,java,rb,php,c,cpp,h}
  4. **Count** extensions to determine languages
  5. **Match** dependencies against known framework list
  6. **Read** README.md for description (first non-header paragraph)
  7. **Check** indicator files for maturity scoring

  ## Language Detection (File Extension Based)

  | Extension | Language |
  |-----------|----------|
  | .py | Python |
  | .ts, .tsx | TypeScript |
  | .js, .jsx | JavaScript |
  | .go | Go |
  | .rs | Rust |
  | .java | Java |
  | .rb | Ruby |
  | .php | PHP |
  | .c, .h | C |
  | .cpp, .hpp | C++ |
  | .cs | C# |
  | .swift | Swift |
  | .kt | Kotlin |

  ## Framework Detection (Dependency Based)

  | Dependency Pattern | Framework |
  |--------------------|-----------|
  | react, react-dom | React |
  | vue | Vue |
  | @angular/core | Angular |
  | fastapi | FastAPI |
  | flask | Flask |
  | django | Django |
  | express | Express |
  | nextjs, next | Next.js |
  | spring-boot | Spring Boot |
  | rails | Ruby on Rails |

  ## Maturity Scoring

  | Indicator | Score |
  |-----------|-------|
  | Has tests directory or test files | +1 |
  | Has CI config (.github/workflows, .gitlab-ci) | +1 |
  | Has docs/ or README >500 chars | +1 |
  | Git history >100 commits | +1 |
  | Has CHANGELOG | +1 |

  Score: 0-1 → "prototype", 2-3 → "development", 4-5 → "production"

  ## Mode-Specific Behavior

  **Auto Mode (mode: auto):**
  - Run detection using file reads only
  - NO questions asked by agent
  - Use detected values directly (with fallbacks for missing)
  - Return: { detected: {...}, final: detected }

  **Interactive Mode (mode: interactive):**
  - Run SAME detection as auto mode
  - Agent shows detected values and asks confirmation
  - Agent handles all questions internally (tune.md does not define questions)
  - User can accept or modify each field
  - Return: { detected: {...}, final: userConfirmed }

  **Question Flow (handled by agent in interactive mode):**
  - Q1: Show detected project name + purpose → Confirm/Edit
  - Q2: Show detected languages + frameworks → Confirm/Edit
  - Q3: Show detected maturity + commands → Confirm/Edit

  NOTE: All questions are defined and asked BY THE AGENT, not by tune.md.
  tune.md only passes mode parameter to agent.
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
