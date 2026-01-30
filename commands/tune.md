---
description: Configure CCO for this project - analyze stack, create profile, load rules
argument-hint: "[--auto] [--preview] [--update]"
allowed-tools: Read, Grep, Glob, Task, AskUserQuestion
model: haiku
---

# /cco:tune

**Configure CCO** - Orchestrate project analysis and profile creation.

> **SoC Principle:** This command handles user interaction and orchestration only.
> Detection is done by `cco-agent-analyze`, file writes by `cco-agent-apply`.

## Args

- `--preview`: Silent validation only, return status (for other commands)
- `--update`: Skip confirmation, update even if profile exists
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
| 2 | Detect project stack (FIRST) | analyze agent |
| 3 | Ask questions with "(Detected)" labels | tune (AskUserQuestion) |
| 4 | Merge answers + detection | tune |
| 5 | Write files | apply agent |

**Key principle:** Detection runs BEFORE questions so we can dynamically label detected values.

---

## Step-1: Profile Validation + Before State

<!-- NOTE: tune uses direct Read() for profile because it is the profile creator/updater,
     not a consumer. Other commands delegate validation to tune via Skill("tune", "--preview"). -->

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

### Preview Mode (--preview)

```javascript
if (args.includes("--preview")) {
  if (validationResult.valid) {
    return { status: "ok", profile: profile }
  }
  // Continue to setup, return status after
}
```

### Mode Detection

```javascript
const isUnattended = args.includes("--auto")
const updateMode = args.includes("--update")

// Unattended mode: never ask questions, always use auto detection
if (isUnattended) {
  config.mode = "auto"
  // Proceed directly to detection, skip all questions
}
```

### Profile Exists - Ask Update (Interactive Only)

```javascript
if (!isUnattended && profile && validationResult.valid && !updateMode) {
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

## Step-2: Detection First

**Detection runs BEFORE questions to enable dynamic labeling.**

```javascript
console.log("Analyzing project...")

// ALWAYS run detection first (for both auto and interactive modes)
let detected
try {
  detected = await Task("cco-agent-analyze", `
    scope: tune
    mode: auto
  `, { model: "haiku" })
} catch (detectionError) {
  console.error("Detection failed:", detectionError.message)
  console.log("Rolling back - no profile changes made.")
  return { status: "error", reason: "Detection failed: " + detectionError.message }
}

// UNATTENDED MODE: Skip questions, use detected.inferred directly
if (isUnattended || config.mode === "auto") {
  configData = { detected: detected, answers: detected.inferred }
  // Proceed directly to Step-4 (no questions)

} else if (config.mode === "interactive") {
  // Helper: Add "(Detected)" or "(Recommended)" suffix to matching option label
  // - Detected: Value was inferred from actual project signals
  // - Recommended: No detection possible, using best-practices default
  function labelOption(options, detectedValue, source) {
    if (!detectedValue) return options

    // Normalize: "user-data" → "user", "ship-fast" → "ship", "with-warning" → "with"
    const normalizedDetected = detectedValue.toLowerCase().split('-')[0]

    return options.map(opt => {
      // Extract first word from label: "Small (2-5)" → "small", "Ship fast" → "ship"
      const firstWord = opt.label.toLowerCase().split(/[\s(]/)[0]
      const isMatch = firstWord === normalizedDetected

      if (!isMatch) return opt

      // Label based on source: detected from code, or best-practices recommendation
      const suffix = source === "detected" ? "(Detected)" : "(Recommended)"
      return { ...opt, label: `${opt.label} ${suffix}` }
    })
  }

  // Questions Part 1: Team & Policy (4 questions)
  // Descriptions explain WHEN to choose each option (best practices guidance)
  const answers1 = await AskUserQuestion([
    {
      question: "How many people work on this project?",
      header: "Team",
      multiSelect: false,
      options: labelOption([
        { label: "Solo", description: "Personal projects, learning, prototypes → no formal review needed" },
        { label: "Small (2-5)", description: "Startups, side projects → code review helpful but informal" },
        { label: "Medium (6-15)", description: "Growing teams → code review required, PR process" },
        { label: "Large (15+)", description: "Enterprise → strict review, CODEOWNERS, documentation" }
      ], detected.inferred?.team, detected.inferred?.team_source)
    },
    {
      question: "Does the project handle sensitive data?",
      header: "Data",
      multiSelect: false,
      options: labelOption([
        { label: "No", description: "Open source, demos, public tools → standard security sufficient" },
        { label: "Internal", description: "Company tools, internal APIs → access control, basic encryption" },
        { label: "User data", description: "User accounts, profiles → GDPR/privacy compliance needed" },
        { label: "Regulated", description: "Finance, health, legal → SOC2/HIPAA/PCI compliance required" }
      ], detected.inferred?.data, detected.inferred?.data_source)
    },
    {
      question: "What matters most when writing code?",
      header: "Priority",
      multiSelect: false,
      options: labelOption([
        { label: "Security", description: "Auth systems, payment, sensitive data → security-first" },
        { label: "Performance", description: "Real-time, games, high-traffic → optimize hot paths" },
        { label: "Readability", description: "Long-term projects, team codebases → maintainability focus" },
        { label: "Ship fast", description: "MVPs, experiments, time-sensitive → speed over perfection" }
      ], detected.inferred?.priority, detected.inferred?.priority_source)
    },
    {
      question: "Can you make changes that break older versions?",
      header: "Compat",
      multiSelect: false,
      options: labelOption([
        { label: "Never", description: "Public libraries, many consumers → strict backwards compat" },
        { label: "Major only", description: "Versioned products → breaking changes in v2, v3 only" },
        { label: "With warning", description: "Internal tools, few consumers → deprecate then remove" },
        { label: "When needed", description: "Early stage, experimental → flexibility over stability" }
      ], detected.inferred?.breaking_changes, detected.inferred?.breaking_changes_source)
    }
  ])

  // Questions Part 2: Development & Deployment (4 questions)
  const answers2 = await AskUserQuestion([
    {
      question: "Does this project provide a service that other software connects to?",
      header: "Service",
      multiSelect: false,
      options: labelOption([
        { label: "No", description: "CLI tools, desktop apps, plugins → no external API consumers" },
        { label: "Internal", description: "Microservices, internal APIs → same team/company uses it" },
        { label: "Partners", description: "B2B integrations → documented contracts, versioning needed" },
        { label: "Public", description: "Public APIs → OpenAPI spec, rate limiting, auth required" }
      ], detected.inferred?.api, detected.inferred?.api_source)
    },
    {
      question: "What is your testing approach?",
      header: "Testing",
      multiSelect: false,
      options: labelOption([
        { label: "Minimal", description: "Prototypes, scripts → test critical paths only" },
        { label: "Target-based", description: "Production apps → meet coverage thresholds (e.g., 80%)" },
        { label: "Test first", description: "Critical systems, TDD → write tests before code" },
        { label: "Everything", description: "High-reliability → unit + integration + e2e tests" }
      ], detected.inferred?.testing, detected.inferred?.testing_source)
    },
    {
      question: "How much documentation do you expect?",
      header: "Docs",
      multiSelect: false,
      options: labelOption([
        { label: "Code is enough", description: "Internal tools, simple logic → self-documenting code" },
        { label: "Basic", description: "Most projects → README + comments where needed" },
        { label: "Detailed", description: "Libraries, APIs → all public functions documented" },
        { label: "Comprehensive", description: "Open source, complex → guides, tutorials, examples" }
      ], detected.inferred?.docs, detected.inferred?.docs_source)
    },
    {
      question: "Where will the project run?",
      header: "Deploy",
      multiSelect: false,
      options: labelOption([
        { label: "Dev only", description: "Early stage → not deployed to production yet" },
        { label: "Cloud", description: "Most web apps → AWS/GCP/Azure managed services" },
        { label: "Self-hosted", description: "Enterprise, compliance → own servers, full control" },
        { label: "Serverless", description: "Event-driven, variable load → auto-scale, pay-per-use" }
      ], detected.inferred?.deployment, detected.inferred?.deployment_source)
    }
  ])

  // Merge all answers
  const answers = { ...answers1, ...answers2 }
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
    ? { size: answers["Team"] }
    : configData.detected.inferred.team,
  data: config.mode === "interactive"
    ? { sensitivity: answers["Data"] }
    : configData.detected.inferred.data,
  priority: config.mode === "interactive"
    ? answers["Priority"]
    : configData.detected.inferred.priority,
  breaking_changes: config.mode === "interactive"
    ? answers["Compat"]
    : configData.detected.inferred.breaking_changes,
  // Part 2: Development & Deployment
  api: config.mode === "interactive"
    ? { consumers: answers["Service"] }
    : configData.detected.inferred.api,
  testing: config.mode === "interactive"
    ? { approach: answers["Testing"] }
    : configData.detected.inferred.testing,
  docs: config.mode === "interactive"
    ? { level: answers["Docs"] }
    : configData.detected.inferred.docs,
  deployment: config.mode === "interactive"
    ? { target: answers["Deploy"] }
    : configData.detected.inferred.deployment,
  // Auto-detected
  commands: configData.detected.commands,
  patterns: configData.detected.patterns,
  documentation: configData.detected.documentation
}

// Validate profile data types before writing
function validateProfile(profile) {
  if (!profile.project?.name || typeof profile.project.name !== "string") {
    throw new Error("profile.project.name must be a non-empty string")
  }
  if (!profile.project?.purpose || typeof profile.project.purpose !== "string") {
    throw new Error("profile.project.purpose must be a non-empty string")
  }
  if (!Array.isArray(profile.stack?.languages) || profile.stack.languages.length === 0) {
    throw new Error("profile.stack.languages must be a non-empty array")
  }
  if (!profile.maturity || typeof profile.maturity !== "string") {
    throw new Error("profile.maturity must be a non-empty string")
  }
}
validateProfile(finalProfile)

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
  scope: tune
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

| Section | Fields | Source | Detection Signals |
|---------|--------|--------|-------------------|
| project | name, purpose, type | Auto-detect | Manifests, README |
| stack | languages, frameworks, testing, build | Auto-detect | File extensions, dependencies |
| maturity | prototype/active/stable/legacy | Auto-detect | Git history, test coverage |
| team | size | Q1 or inference | CODEOWNERS, CONTRIBUTING, git contributors |
| data | sensitivity | Q2 or inference | SECURITY.md, .env.example, PII patterns |
| priority | security/performance/readability/ship-fast | Q3 or inference | Security middleware, cache patterns, test ratio |
| breaking_changes | never/major-only/with-warning/when-needed | Q4 or inference | CHANGELOG format, semver tags, deprecations |
| api | no/internal/partners/public | Q5 or inference | OpenAPI/GraphQL specs, route definitions |
| testing | minimal/target-based/test-first/everything | Q6 or inference | Coverage config, test thresholds, test ratio |
| docs | code-only/basic/detailed/comprehensive | Q7 or inference | docs/ structure, doc site config |
| deployment | dev-only/cloud/self-hosted/serverless | Q8 or inference | Dockerfile, k8s/, serverless.yml, CI/CD |
| commands | format, lint, test, build, type | Auto-detect | package.json scripts, Makefile |
| patterns | error_handling, logging, api_style, etc. | Auto-detect | Code patterns |
| documentation | core, technical, developer, operations, analysis | Auto-detect | 50+ file patterns |

**Detection Signal Details:**

| Question | Primary Signals | Secondary Signals |
|----------|-----------------|-------------------|
| Team | git shortlog contributors | CODEOWNERS, AUTHORS.md |
| Data | SECURITY.md, regulated keywords | .env.example secrets, encryption patterns |
| Priority | @auth decorators, @cache patterns | Test file ratio, performance benchmarks |
| Compat | CHANGELOG.md, @deprecated | Semver git tags, major version bumps |
| Service | openapi.yaml, schema.graphql | @app.route patterns, Router() usage |
| Testing | .coveragerc thresholds, codecov.yml | Test file count, fixture patterns |
| Docs | mkdocs.yml, docusaurus.config.js | docs/ file count, README completeness |
| Deploy | serverless.yml, k8s/ | Dockerfile, terraform/, CI workflows |

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
/cco:tune --auto       # Fully unattended, auto-detect everything
/cco:tune --preview    # Silent validation
/cco:tune --update     # Update existing profile
```

---

## Integration

Other commands call `--preview` at start:

```javascript
const tuneResult = await Skill("tune", "--preview")
if (tuneResult.status === "skipped") return
```
