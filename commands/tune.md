---
description: Configure CCO for this project - analyze stack, create profile, load rules
argument-hint: [--check] [--force]
allowed-tools: Read(*), Grep(*), Glob(*), Task(*), AskUserQuestion
model: haiku
---

# /cco:tune

**Configure CCO** - Orchestrate project analysis and profile creation.

> **SoC Principle:** This command handles user interaction and orchestration only.
> Detection is done by `cco-agent-analyze`, file writes by `cco-agent-apply`.

## Args

- `--check`: Silent validation only, return status (for other commands)
- `--force`: Skip confirmation, update even if profile exists
- `--auto`: Fully unattended mode - no questions, auto-detect everything

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         /cco:tune (orchestrator)                     │
│                                                                  │
│  Responsibilities:                                               │
│  ✓ User interaction (AskUserQuestion)                           │
│  ✓ Flow control (which mode, what to do)                        │
│  ✓ Merge data from different sources                            │
│  ✓ Call agents with specific instructions                       │
│                                                                  │
│  Does NOT:                                                       │
│  ✗ Detection logic (delegated to cco-agent-analyze)             │
│  ✗ File writes (delegated to cco-agent-apply)                   │
└─────────────────────────────────────────────────────────────────┘
         │                                    │
         ▼                                    ▼
┌─────────────────────┐          ┌─────────────────────┐
│ cco-agent-analyze   │          │ cco-agent-apply     │
│                     │          │                     │
│ - Read files        │          │ - Delete old files  │
│ - Detect stack      │          │ - Write new files   │
│ - Smart inference   │          │ - Copy rules        │
│ - Return data ONLY  │          │ - Execute ops list  │
└─────────────────────┘          └─────────────────────┘
```

## Execution Flow

| Step | Action | Responsible |
|------|--------|-------------|
| 1 | Validate existing profile | tune (Read) |
| 2a | Ask user questions | tune (AskUserQuestion) |
| 2b | Detect project stack | analyze agent |
| 3 | Merge answers + detection | tune |
| 4 | Write files | apply agent |

---

## Step-1: Profile Validation + Before State

```javascript
const profilePath = ".claude/rules/cco-profile.md"
let profile = null
let validationResult = { valid: false, missing: [] }
let beforeState = null  // For before/after comparison

try {
  const content = await Read(profilePath)
  profile = parseYamlFrontmatter(content)

  const requiredFields = [
    "project.name", "project.purpose",
    "stack.languages", "maturity", "commands"
  ]

  validationResult.missing = requiredFields.filter(f => !getNestedValue(profile, f))
  validationResult.valid = validationResult.missing.length === 0

  // Store BEFORE state for comparison (always fresh detect, ignore old values)
  if (profile) {
    beforeState = {
      languages: profile.stack?.languages || [],
      frameworks: profile.stack?.frameworks || [],
      maturity: profile.maturity,
      documentation: profile.documentation?.analysis || null
    }
  }
} catch (e) {
  validationResult.valid = false
  validationResult.missing = ["entire profile"]
  beforeState = null  // No previous state
}
```

### Check Mode (--check)

```javascript
if (args.includes("--check")) {
  if (validationResult.valid) {
    return { status: "ok", profile: profile }
  }
  // Continue to setup, return status after
}
```

### Mode Detection

```javascript
const isUnattended = args.includes("--auto")
const forceUpdate = args.includes("--force")

// Unattended mode: never ask questions, always use auto detection
if (isUnattended) {
  config.mode = "auto"
  // Proceed directly to detection, skip all questions
}
```

### Profile Exists - Ask Update (Interactive Only)

```javascript
if (!isUnattended && profile && validationResult.valid && !forceUpdate) {
  const answer = await AskUserQuestion([{
    question: "CCO profile exists. Update it?",
    header: "Profile",
    options: [
      { label: "Keep current", description: "No changes needed" },
      { label: "Quick update (Recommended)", description: "Re-detect stack automatically" },
      { label: "Full update", description: "Answer questions to customize" }
    ],
    multiSelect: false
  }])

  if (answer === "Keep current") {
    return { status: "ok", profile: profile }
  }
  config.mode = answer.includes("Quick") ? "auto" : "interactive"
}
```

### Profile Missing - Ask Mode (Interactive Only)

```javascript
if (!isUnattended && !validationResult.valid) {
  const answer = await AskUserQuestion([{
    question: `CCO profile ${profile ? "incomplete" : "not found"}. Configure?`,
    header: "Setup",
    options: [
      { label: "Auto-setup (Recommended)", description: "Detect stack automatically" },
      { label: "Interactive", description: "Answer questions to customize" },
      { label: "Skip", description: "Don't configure CCO" }
    ],
    multiSelect: false
  }])

  if (answer === "Skip") return { status: "skipped" }
  config.mode = answer.includes("Auto") ? "auto" : "interactive"
}
```

---

## Step-2: Parallel Execution

**Interactive: User answers questions, then detection runs.**
**Auto/Unattended: Detection only, no questions.**

```javascript
console.log("Analyzing project...")

// UNATTENDED MODE: Skip all questions, use auto detection with smart inference
if (isUnattended || config.mode === "auto") {
  const detected = await Task("cco-agent-analyze", `
    scope: config
    mode: auto
  `, { model: "haiku" })

  configData = { detected: detected, answers: detected.inferred }
  // Proceed directly to Step-3 (no questions)

} else if (config.mode === "interactive") {
  // Questions Part 1: Team & Policy (4 questions)
  const answers1 = await AskUserQuestion([
    {
      question: "Team size?",
      header: "Team",
      multiSelect: false,
      options: [
        { label: "Solo", description: "Single developer" },
        { label: "Small (2-5)", description: "Code review helpful" },
        { label: "Medium (6-15)", description: "Code review required" },
        { label: "Large (15+)", description: "Strict review + docs" }
      ]
    },
    {
      question: "Data sensitivity?",
      header: "Data",
      multiSelect: false,
      options: [
        { label: "Public", description: "No sensitive data" },
        { label: "Internal", description: "Company internal" },
        { label: "PII", description: "Personal data - GDPR" },
        { label: "Regulated", description: "SOC2/HIPAA" }
      ]
    },
    {
      question: "Top priority?",
      header: "Priority",
      multiSelect: false,
      options: [
        { label: "Security", description: "Security-first" },
        { label: "Performance", description: "Speed focus" },
        { label: "Maintainability", description: "Clean, testable" },
        { label: "Velocity", description: "Ship fast" }
      ]
    },
    {
      question: "Breaking changes policy?",
      header: "Breaking",
      multiSelect: false,
      options: [
        { label: "Never", description: "Always backwards compatible" },
        { label: "Major only", description: "Only in major versions" },
        { label: "Semver", description: "Follow semantic versioning" },
        { label: "Flexible", description: "With deprecation notices" }
      ]
    }
  ])

  // Questions Part 2: Development & Deployment (4 questions)
  const answers2 = await AskUserQuestion([
    {
      question: "Who consumes your API?",
      header: "API",
      multiSelect: false,
      options: [
        { label: "Internal only", description: "Same team/org" },
        { label: "Partners", description: "Known external consumers" },
        { label: "Public", description: "Open API, unknown consumers" },
        { label: "No API", description: "Not an API project" }
      ]
    },
    {
      question: "Testing approach?",
      header: "Testing",
      multiSelect: false,
      options: [
        { label: "Minimal", description: "Critical paths only" },
        { label: "Coverage targets", description: "Meet coverage thresholds" },
        { label: "TDD", description: "Tests before code" },
        { label: "Comprehensive", description: "Full coverage + integration" }
      ]
    },
    {
      question: "Documentation level?",
      header: "Docs",
      multiSelect: false,
      options: [
        { label: "Code only", description: "Self-documenting code" },
        { label: "README essential", description: "README + inline comments" },
        { label: "API docs", description: "OpenAPI/Swagger required" },
        { label: "Full docs", description: "Guides, examples, tutorials" }
      ]
    },
    {
      question: "Deployment target?",
      header: "Deploy",
      multiSelect: false,
      options: [
        { label: "Local/Dev", description: "Development only" },
        { label: "Cloud managed", description: "AWS/GCP/Azure services" },
        { label: "Self-hosted", description: "Own infrastructure" },
        { label: "Serverless", description: "Lambda/Functions/Edge" }
      ]
    }
  ])

  // Merge all answers
  const answers = { ...answers1, ...answers2 }

  // Run detection after questions
  console.log("Analyzing project...")
  const detected = await Task("cco-agent-analyze", `
    scope: config
    mode: detect-only
  `, { model: "haiku" })

  configData = { detected: detected, answers: answers }
}
```

---

## Step-3: Merge Results

```javascript
const finalProfile = {
  project: configData.detected.project,
  stack: configData.detected.stack,
  maturity: configData.detected.maturity,
  // Part 1: Team & Policy
  team: config.mode === "interactive"
    ? { size: answers.Team }
    : configData.detected.inferred.team,
  data: config.mode === "interactive"
    ? { sensitivity: answers.Data }
    : configData.detected.inferred.data,
  priority: config.mode === "interactive"
    ? answers.Priority
    : configData.detected.inferred.priority,
  breaking_changes: config.mode === "interactive"
    ? answers.Breaking
    : configData.detected.inferred.breaking_changes,
  // Part 2: Development & Deployment
  api: config.mode === "interactive"
    ? { consumers: answers.API }
    : configData.detected.inferred.api,
  testing: config.mode === "interactive"
    ? { approach: answers.Testing }
    : configData.detected.inferred.testing,
  docs: config.mode === "interactive"
    ? { level: answers.Docs }
    : configData.detected.inferred.docs,
  deployment: config.mode === "interactive"
    ? { target: answers.Deploy }
    : configData.detected.inferred.deployment,
  // Auto-detected
  commands: configData.detected.commands,
  patterns: configData.detected.patterns,
  documentation: configData.detected.documentation
}

// Determine which rules to install based on detected stack
const rulesNeeded = determineRules(configData.detected)
```

---

## Step-4: Write Files (via apply agent)

**Delegate all file operations to apply agent.**

```javascript
// Prepare write operations
const operations = [
  // Step 1: Clean existing CCO files
  { action: "delete_pattern", path: ".claude/rules/", pattern: "cco-*.md" },

  // Step 2: Write profile
  { action: "write", path: ".claude/rules/cco-profile.md", content: generateProfileYaml(finalProfile) },

  // Step 3: Copy rule files from plugin
  ...rulesNeeded.map(rule => ({
    action: "copy",
    source: `$PLUGIN_ROOT/rules/${rule}`,
    dest: `.claude/rules/${rule}`
  }))
]

// Execute via apply agent
const result = await Task("cco-agent-apply", `
  scope: config
  operations: ${JSON.stringify(operations)}
  outputContext: true
`, { model: "haiku" })

// Report result with before/after comparison
const docAnalysis = configData.detected.documentation?.analysis || {}
const criticalMissing = docAnalysis.criticalMissing || []

// Calculate changes
const changes = calculateChanges(beforeState, {
  languages: finalProfile.stack.languages,
  frameworks: finalProfile.stack.frameworks,
  maturity: finalProfile.maturity,
  documentation: docAnalysis
})

console.log(`
## CCO Configured

Profile: .claude/rules/cco-profile.md
Rules: ${rulesNeeded.length} files loaded

### Configuration Summary

| Category | Value |
|----------|-------|
| Languages | ${finalProfile.stack.languages.join(", ")} |
| Frameworks | ${finalProfile.stack.frameworks.join(", ") || "none"} |
| Maturity | ${finalProfile.maturity} |

| Setting | Value | Impact |
|---------|-------|--------|
| Team | ${finalProfile.team.size} | Review requirements |
| Data | ${finalProfile.data.sensitivity} | Security level |
| Priority | ${finalProfile.priority} | Check ordering |
| Breaking | ${finalProfile.breaking_changes} | API rules |
| API | ${finalProfile.api.consumers} | Doc requirements |
| Testing | ${finalProfile.testing.approach} | Commit gates |
| Docs | ${finalProfile.docs.level} | Generation scope |
| Deploy | ${finalProfile.deployment.target} | Ops rules |

### Documentation Status

| Category | Found |
|----------|-------|
| Core (README, LICENSE, etc.) | ${docAnalysis.categories?.core || "0/9"} |
| API schemas | ${docAnalysis.categories?.api || "0/7"} |
| Config docs | ${docAnalysis.categories?.config || "0/5"} |
| Platform (GitHub, etc.) | ${docAnalysis.categories?.platform || "0/7"} |
| CI/CD | ${docAnalysis.categories?.ci || "0/9"} |
| Doc infrastructure | ${docAnalysis.categories?.infrastructure || "0/11"} |
| docs/ directory | ${docAnalysis.docsDirectory?.exists ? `${docAnalysis.docsDirectory.fileCount} files` : "not found"} |

${criticalMissing.length > 0 ? `**Critical missing:** ${criticalMissing.join(", ")}` : "**No critical gaps**"}

${beforeState ? `
### Changes from Previous Profile

${changes.length > 0 ? changes.map(c => `- ${c}`).join('\n') : "- No changes detected (fresh detection matched previous)"}
` : ""}

### Next Steps

${criticalMissing.length > 0 ? `- Run \`/cco:docs\` to generate missing documentation` : ""}
- Run \`/cco:optimize\` to fix code issues
- Run \`/cco:align\` for architecture review
`)

// Helper: Calculate what changed
function calculateChanges(before, after) {
  if (!before) return ["First-time setup (no previous profile)"]

  const changes = []

  // Language changes
  const newLangs = after.languages.filter(l => !before.languages.includes(l))
  const removedLangs = before.languages.filter(l => !after.languages.includes(l))
  if (newLangs.length) changes.push(`New languages detected: ${newLangs.join(", ")}`)
  if (removedLangs.length) changes.push(`Languages no longer detected: ${removedLangs.join(", ")}`)

  // Framework changes
  const newFw = after.frameworks.filter(f => !before.frameworks.includes(f))
  const removedFw = before.frameworks.filter(f => !after.frameworks.includes(f))
  if (newFw.length) changes.push(`New frameworks detected: ${newFw.join(", ")}`)
  if (removedFw.length) changes.push(`Frameworks no longer detected: ${removedFw.join(", ")}`)

  // Maturity change
  if (before.maturity !== after.maturity) {
    changes.push(`Maturity: ${before.maturity} → ${after.maturity}`)
  }

  // Documentation changes
  if (before.documentation && after.documentation) {
    const beforeTotal = before.documentation.totalFiles || 0
    const afterTotal = after.documentation.totalFiles || 0
    if (afterTotal !== beforeTotal) {
      changes.push(`Documentation files: ${beforeTotal} → ${afterTotal}`)
    }
  }

  return changes
}

return { status: "ok", profile: finalProfile, rulesLoaded: rulesNeeded }
```

---

## Profile Schema

The profile has 11 sections:

| Section | Fields | Source |
|---------|--------|--------|
| project | name, purpose, type | Auto-detect |
| stack | languages, frameworks, testing, build | Auto-detect |
| maturity | prototype/active/stable/legacy | Auto-detect (scoring) |
| team | size | User Q1 or inference |
| data | sensitivity | User Q2 or inference |
| priority | security/performance/maintainability/velocity | User Q3 or inference |
| breaking_changes | never/major/semver/flexible | User Q4 or inference |
| api | consumers (internal/partners/public/none) | User Q5 or inference |
| testing | approach (minimal/coverage/tdd/comprehensive) | User Q6 or inference |
| docs | level (code/readme/api/full) | User Q7 or inference |
| deployment | target (local/cloud/self-hosted/serverless) | User Q8 or inference |
| commands | format, lint, test, build, type | Auto-detect |
| patterns | error_handling, logging, api_style, etc. | Auto-detect |
| documentation | core, technical, developer, operations, analysis | Auto-detect (50+ patterns) |

**Documentation detection covers:**
- Core: README, LICENSE, CHANGELOG, CONTRIBUTING, SECURITY, CODE_OF_CONDUCT
- Technical: API docs, OpenAPI/Swagger, Architecture, ADRs, Database schemas
- Developer: Setup guides, Testing docs, CI/CD, Docker, Kubernetes
- Operations: Deployment, Runbooks, Monitoring, Troubleshooting
- Specialized: Privacy, Compliance, i18n, Accessibility, Migrations
- Infrastructure: Doc site generators, Generated docs, Diagrams

**Full schema in `cco-agent-analyze` documentation.**

---

## Output Schema

```json
{
  "status": "ok|skipped|error",
  "profile": { ... },
  "rulesLoaded": ["cco-typescript.md", ...]
}
```

---

## Usage

```bash
/cco:tune              # Interactive or auto setup
/cco:tune --check      # Silent validation
/cco:tune --force      # Force update
```

---

## Integration

Other commands call `--check` at start:

```javascript
const tuneResult = await Skill("tune", "--check")
if (tuneResult.status === "skipped") return
```
