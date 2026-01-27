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

  ### Section 1: Project Identity (Auto-detect)

  | Field | Source | Method | Fallback |
  |-------|--------|--------|----------|
  | name | package.json, pyproject.toml, Cargo.toml | "name" field | Directory name |
  | purpose | README.md, manifest description | First paragraph | "Not specified" |
  | type | Import patterns + structure | See Type Detection | ["unknown"] |

  ### Section 2: Tech Stack (Auto-detect)

  | Field | Source | Method | Fallback |
  |-------|--------|--------|----------|
  | languages | **/*.{py,ts,js,go,rs,...} | Count extensions | [] |
  | frameworks | Dependencies in manifests | Pattern match | [] |
  | testing | Dependencies | Match test frameworks | [] |
  | build | Dependencies + Dockerfile | Match build tools | [] |

  ### Section 3: Maturity (Auto-detect with scoring)

  | Indicator | Check | Points |
  |-----------|-------|--------|
  | Has tests/ or test files | Glob("**/test*") | +1 |
  | Has CI config | .github/workflows/, .gitlab-ci.yml | +1 |
  | Has documentation | docs/ or README >1000 chars | +1 |
  | Git history depth | >100 commits | +1 |
  | Has CHANGELOG | CHANGELOG.md exists | +1 |
  | Has version tags | git tag | +1 |

  Score → Maturity: 0-1=prototype, 2-3=active, 4-5=stable, 6=legacy

  ### Section 4: Team & Process (MUST ASK - cannot detect)

  | Field | Why Can't Detect | Default (auto mode) |
  |-------|------------------|---------------------|
  | team.size | Git contributors ≠ team size | "solo" |
  | data.sensitivity | Cannot infer from code | "internal" |
  | priority | Business decision | "maintainability" |
  | release.cadence | Cannot infer | "continuous" |
  | breaking_changes | Policy, not code | "major" |

  ### Section 5: Commands (Auto-detect)

  | Command | Sources | Patterns |
  |---------|---------|----------|
  | format | package.json, Makefile, pyproject.toml | "format", "fmt", "prettier", "black" |
  | lint | Same | "lint", "eslint", "ruff", "pylint" |
  | test | Same | "test", "pytest", "jest", "mocha" |
  | build | Same | "build", "compile", "webpack", "vite" |
  | type | Same | "typecheck", "mypy", "tsc" |

  ### Section 6: Patterns (Auto-detect, informational)

  | Pattern | Detection Method |
  |---------|------------------|
  | error_handling | try/except vs Result vs match |
  | logging | print vs logging vs structlog |
  | api_style | REST routes vs GraphQL schema vs gRPC proto |
  | db_type | Dependencies (psycopg2→postgres, pymongo→mongo) |
  | has_ci | .github/workflows/ or .gitlab-ci.yml exists |
  | has_docker | Dockerfile exists |
  | has_monorepo | workspaces in package.json or multiple manifests |

  ## Detection Mappings

  ### Language Detection (File Extension)

  | Extension | Language |
  |-----------|----------|
  | .py | Python |
  | .ts, .tsx | TypeScript |
  | .js, .jsx, .mjs | JavaScript |
  | .go | Go |
  | .rs | Rust |
  | .java | Java |
  | .rb | Ruby |
  | .php | PHP |
  | .c, .h | C |
  | .cpp, .hpp, .cc | C++ |
  | .cs | C# |
  | .swift | Swift |
  | .kt, .kts | Kotlin |
  | .scala | Scala |
  | .ex, .exs | Elixir |
  | .hs | Haskell |
  | .lua | Lua |
  | .r, .R | R |
  | .jl | Julia |
  | .pl, .pm | Perl |
  | .sh, .bash | Shell |

  ### Framework Detection (Dependency Pattern)

  | Pattern | Framework | Type |
  |---------|-----------|------|
  | react, react-dom | React | web |
  | vue | Vue | web |
  | @angular/core | Angular | web |
  | svelte | Svelte | web |
  | next | Next.js | web |
  | nuxt | Nuxt | web |
  | fastapi | FastAPI | api |
  | flask | Flask | api |
  | django | Django | api |
  | express | Express | api |
  | nestjs, @nestjs | NestJS | api |
  | spring-boot | Spring Boot | api |
  | rails | Ruby on Rails | api |
  | gin | Gin | api |
  | echo | Echo | api |
  | actix-web | Actix | api |
  | axum | Axum | api |
  | click, typer, argparse | CLI framework | cli |
  | cobra | Cobra | cli |
  | clap | Clap | cli |

  ### Project Type Detection

  | Indicators | Type |
  |------------|------|
  | CLI framework deps OR argparse/click imports OR bin/ entry | cli |
  | API framework deps OR routes/endpoints structure | api |
  | Frontend framework deps OR public/index.html | web |
  | setup.py with packages OR pyproject.toml [project] OR lib/ structure | library |
  | workspaces in package.json OR multiple root manifests | monorepo |

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
  - Run ALL detection (Sections 1-6)
  - NO questions asked
  - Use safe defaults for Section 4 (Team & Process):
    - team.size: "solo"
    - data.sensitivity: "internal"
    - priority: "maintainability"
    - release.cadence: "continuous"
    - breaking_changes: "major"
  - Return: { detected: {...}, final: {...} }

  **Interactive Mode (mode: interactive):**
  - Run SAME detection as auto mode FIRST
  - THEN ask Section 4 questions (cannot be detected):

  ## Interactive Questions [4 questions × 4 options = 16 total]

  ```javascript
  AskUserQuestion([
    {
      question: "Team size?",
      header: "Team",
      options: [
        { label: "Solo", description: "Single developer - minimal process" },
        { label: "Small (2-5)", description: "Code review helpful" },
        { label: "Medium (6-15)", description: "Code review required" },
        { label: "Large (15+)", description: "Strict review + docs" }
      ],
      multiSelect: false
    },
    {
      question: "Data sensitivity?",
      header: "Data",
      options: [
        { label: "Public", description: "No sensitive data" },
        { label: "Internal", description: "Company internal only" },
        { label: "PII", description: "Personal data - GDPR applies" },
        { label: "Regulated", description: "Finance/Healthcare - SOC2/HIPAA" }
      ],
      multiSelect: false
    },
    {
      question: "Top priority?",
      header: "Priority",
      options: [
        { label: "Security", description: "Security-first decisions" },
        { label: "Performance", description: "Speed and efficiency focus" },
        { label: "Maintainability", description: "Clean, documented, testable" },
        { label: "Velocity", description: "Ship fast, iterate quickly" }
      ],
      multiSelect: false
    },
    {
      question: "Breaking changes policy?",
      header: "Breaking",
      options: [
        { label: "Never", description: "Backwards compatible always" },
        { label: "Major only", description: "Only in major versions" },
        { label: "Semver", description: "Follow semantic versioning" },
        { label: "Allowed", description: "OK with deprecation notice" }
      ],
      multiSelect: false
    }
  ])
  ```

  ## How Profile Affects Claude Decisions

  | Field | Impact on Claude Behavior |
  |-------|---------------------------|
  | team.size=solo | Skip review reminders, minimal docs |
  | team.size=large | Require docs, suggest PR templates |
  | data.sensitivity=pii | Flag any logging of user data |
  | data.sensitivity=regulated | Enforce audit trails, encryption |
  | priority=security | Prioritize security fixes over features |
  | priority=velocity | Suggest simpler solutions, skip optimizations |
  | breaking_changes=never | Warn on any API signature change |
  | breaking_changes=allowed | Suggest clean breaks over hacks |
  | maturity=prototype | Allow shortcuts, skip tests |
  | maturity=stable | Require tests, careful refactoring |

  - Return: { detected: {...}, answers: {...}, final: merged }
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
# CCO Profile - Generated by /cco:tune
# This profile informs ALL Claude Code decisions for this project

# ============================================================
# SECTION 1: PROJECT IDENTITY (Auto-detected)
# ============================================================
project:
  name: "project-name"                    # From manifest or directory
  purpose: "Brief description"            # From README or manifest description
  type:                                   # Detected from imports/structure
    - api                                 # fastapi/flask/express → api
    - web                                 # react/vue/angular → web
    # Options: cli, api, web, library, monorepo

# ============================================================
# SECTION 2: TECH STACK (Auto-detected)
# ============================================================
stack:
  languages:                              # From file extensions
    - Python
    - TypeScript
  frameworks:                             # From dependencies
    - FastAPI
    - React
  testing:                                # From dependencies
    - pytest
    - jest
  build:                                  # From dependencies
    - webpack
    - docker

# ============================================================
# SECTION 3: PROJECT MATURITY (Auto-detected from indicators)
# ============================================================
maturity: "active"                        # prototype|active|stable|legacy
# Detection: tests existence, CI config, docs, git history, changelog

# ============================================================
# SECTION 4: TEAM & PROCESS (Asked in interactive, defaults in auto)
# ============================================================
team:
  size: "small"                           # solo|small|medium|large
  # Affects: code review requirements, documentation level

data:
  sensitivity: "internal"                 # public|internal|pii|regulated
  # Affects: security checks, compliance requirements, logging rules

priority: "maintainability"               # security|performance|maintainability|velocity
  # Affects: trade-off decisions, optimization focus

release:
  cadence: "continuous"                   # continuous|scheduled|versioned
  # Affects: changelog generation, version bumping

breaking_changes: "major"                 # never|major|allowed
  # Affects: API design, deprecation strategy

# ============================================================
# SECTION 5: COMMANDS (Auto-detected from manifests)
# ============================================================
commands:
  format: "black . && prettier --write ."
  lint: "ruff check . && eslint ."
  test: "pytest tests/ -v"
  build: "npm run build"
  type: "mypy src/ && tsc --noEmit"

# ============================================================
# SECTION 6: DETECTED PATTERNS (Auto-detected, informational)
# ============================================================
patterns:
  error_handling: "exceptions"            # exceptions|result|either
  logging: "structured"                   # print|logging|structured
  api_style: "rest"                       # rest|graphql|grpc
  db_type: "postgres"                     # postgres|mysql|mongo|sqlite|none
  has_ci: true
  has_docker: true
  has_monorepo: false
---

# Project Context

Additional context that helps Claude understand this project...
```

## Required vs Optional Fields

| Section | Field | Required | Auto-Detect | Ask User |
|---------|-------|----------|-------------|----------|
| project | name | ✓ | ✓ | - |
| project | purpose | ✓ | ✓ | - |
| project | type | ✓ | ✓ | confirm |
| stack | languages | ✓ | ✓ | - |
| stack | frameworks | ✓ | ✓ | - |
| maturity | - | ✓ | ✓ | confirm |
| team | size | ✓ | - | ✓ |
| data | sensitivity | ✓ | - | ✓ |
| priority | - | ✓ | - | ✓ |
| release | cadence | - | partial | ✓ |
| breaking_changes | - | - | - | ✓ |
| commands | * | - | ✓ | - |
| patterns | * | - | ✓ | - |

**Validation:** Sections 1-5 must have all required fields populated.

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
