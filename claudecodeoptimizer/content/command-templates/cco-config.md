---
name: cco-config
description: Configure project context and AI behavior
allowed-tools: Read(*), Write(*), Edit(*), Bash(cco-install:*), Task(*), TodoWrite, AskUserQuestion
---

# /cco-config

**Project Setup** - Background detection + combined questions for fast configuration.

## Args

- `--auto` or `--unattended`: Skip all questions and visual steps, use recommended defaults
  - Context: Setup/Update
  - Statusline: Skip (keep unchanged)
  - Permissions: Skip (keep unchanged)
  - Thinking: Enabled
  - Budget: AI-recommended based on project complexity
  - Output: AI-recommended based on project complexity
  - Data: Public
  - Compliance: None
  - **Skip visual steps:** No summary display, no detection report, direct file writes only
- `--target-dir <path>`: Write config files to specified directory instead of `.claude`
  - Example: `--target-dir .claude` (explicit default)
  - Example: `--target-dir /tmp/project/.claude` (absolute path)
  - Useful for: benchmarks, testing, custom project layouts

**Usage:**
- `/cco-config --auto`
- `/cco-config --target-dir .claude`
- `/cco-config --auto --target-dir /custom/path/.claude`

## Context

- Context exists: !`test -f ./.claude/rules/cco/context.md && echo "1" || echo "0"`
- Existing rules: !`test -d .claude/rules/cco && ls .claude/rules/cco/*.md | xargs -I{} basename {} | tr '\n' ' ' | grep . || echo "None"`
- Settings exists: !`test -f ./.claude/settings.json && echo "1" || echo "0"`
- Args: $ARGS

## Mode Detection

```javascript
// Parse arguments
const args = "$ARGS"
const isUnattended = args.includes("--auto") || args.includes("--unattended")

// Parse --target-dir argument
let targetDir = ".claude"  // Default
const targetDirMatch = args.match(/--target-dir\s+(\S+)/)
if (targetDirMatch) {
  targetDir = targetDirMatch[1]
}

if (isUnattended) {
  // Skip to Step-1 with defaults, no questions
  // Statusline/Permissions = "Skip" to keep unchanged (non-invasive)
  setupConfig = {
    context: "Setup/Update",
    statusline: "Skip",
    permissions: "Skip",
    thinking: "Enabled"
  }
  // Skip Q1, Q2 - proceed directly to detection and apply
}
```

## Architecture

| Step | Name | Action | Optimization |
|------|------|--------|--------------|
| 1 | Pre-detect | cco-agent-analyze (background) | Parallel with Q1 |
| 2 | Setup | Q1: Combined setup tabs | Single question |
| 3 | Context | Q2: Context details (conditional) | Only if Setup/Update |
| 4 | Apply | Write files | Background |
| 5 | Report | Summary | Instant |

---

## Progress Tracking [CRITICAL]

```javascript
TodoWrite([
  { content: "Step-1: Pre-detect (background)", status: "in_progress", activeForm: "Running pre-detection" },
  { content: "Step-2: Setup configuration", status: "pending", activeForm: "Getting setup options" },
  { content: "Step-3: Context details", status: "pending", activeForm: "Getting context details" },
  { content: "Step-4: Apply configuration", status: "pending", activeForm: "Applying configuration" },
  { content: "Step-5: Show report", status: "pending", activeForm: "Showing final report" }
])
```

---

## Step-1: Pre-detect [BACKGROUND]

**Launch detection in background while Q1 is asked:**

```javascript
// Start detection immediately - runs while user answers Q1
detectTask = Task("cco-agent-analyze", `
  scopes: ["config"]
  phase: "detect"

  Auto-detect from manifest files and code:
  - Language, framework, runtime, packageManager
  - Infrastructure: containerized, ci, cloud, deployment
  - Testing: testFramework, coverage, linters, typeChecker
  - Metadata: license, teamSize, maturity, lastActivity
  - Project complexity (for AI Performance recommendations)

  [CRITICAL] Extract projectCritical from documentation:
  - Read README.md, CONTRIBUTING.md, CLAUDE.md, AGENTS.md in PARALLEL
  - Extract purpose (first paragraph or package description)
  - Extract constraints (MUST, REQUIRED, NEVER, ALWAYS statements)
  - Extract invariants (properties that must always hold)
  - Extract nonNegotiables (rules that cannot be overridden)

  Return in output:
  - detections: { language, type, api, database, frontend, infra, dependencies }
  - complexity: { loc, files, frameworks, hasTests, hasCi, isMonorepo }
  - projectCritical: { purpose, constraints[], invariants[], nonNegotiables[] }
  - sources: [{ file, confidence }]
`, { model: "haiku", run_in_background: true })

// Proceed to Q1 immediately (detection runs in background)
```

### Validation
```
[x] Detection launched in background
→ Proceed to Step-2 immediately (don't wait)
```

---

## Step-2: Setup [Q1 - SKIP IF UNATTENDED]

**Combined setup in single question with 4 tabs:**

```javascript
// Load existing config for [current] labels
existingConfig = loadExistingConfig()  // From .claude/settings.json

// Helper: Generate label with [current] or (Recommended) suffix
function configLabel(value, field, recommended = false, defaultSuffix = "") {
  if (existingConfig[field] === value) return `${value} [current]`
  if (recommended) return `${value} (Recommended)`
  return defaultSuffix ? `${value} ${defaultSuffix}` : value
}

// UNATTENDED MODE: Skip Q1, use defaults
if (isUnattended) {
  setupConfig = {
    context: "Setup/Update",
    statusline: "Skip",      // Non-invasive: keep unchanged
    permissions: "Skip",     // Non-invasive: keep unchanged
    thinking: "Enabled"
  }
  // Proceed directly to Step-3
} else {
  AskUserQuestion([
  {
    question: "Project context action?",
    header: "Context",
    options: [
      { label: existingConfig.context ? "Setup/Update [current]" : "Setup/Update (Recommended)", description: "Configure or update project context and rules" },
      { label: "Remove", description: "Remove all CCO configuration" },
      { label: "Export", description: "Export rules to AGENTS.md or CLAUDE.md" }
    ],
    multiSelect: false
  },
  {
    question: "Statusline display?",
    header: "Statusline",
    options: [
      { label: configLabel("Full", "statusline", true), description: "User, model, context %, git status, file changes" },
      { label: configLabel("Minimal", "statusline"), description: "User, model, context % only" },
      { label: "Skip", description: "Keep current statusline unchanged" },
      { label: configLabel("Remove", "statusline"), description: "Use Claude Code default statusline" }
    ],
    multiSelect: false
  },
  {
    question: "Permission approval level?",
    header: "Permissions",
    options: [
      { label: configLabel("Permissive", "permissions"), description: "Auto-approve most operations (except force push)" },
      { label: configLabel("Balanced", "permissions", true), description: "Auto-approve read + lint/test, ask for writes" },
      { label: "Skip", description: "Keep current permissions unchanged" },
      { label: "Remove", description: "Remove permissions, use Claude Code defaults" }
    ],
    multiSelect: false
  },
  {
    question: "Enable extended thinking?",
    header: "Thinking",
    options: [
      { label: configLabel("Enabled", "thinking", true), description: "Better for complex code, architecture decisions" },
      { label: configLabel("Disabled", "thinking", false, "(CC default)"), description: "Faster responses, better prompt caching" }
    ],
    multiSelect: false
  }
  ])
}
```

### Validation
```
[x] User completed Q1 (or unattended defaults applied)
→ Store as: setupConfig = { context, statusline, permissions, thinking }
→ If context = "Remove": Skip to Step-4 (removal)
→ If context = "Export": Skip to Step-4 (export)
→ If thinking = "Disabled": Skip Budget tab in Q2
→ Proceed to Step-3
```

---

## Step-3: Context Details [Q2 - SKIP IF UNATTENDED]

**Only ask if "Setup/Update" selected in Q1.**

**First: Wait for detection results and calculate recommendations:**

```javascript
// Now collect detection results
detectResult = await TaskOutput(detectTask.id)

// Calculate AI recommendations based on project complexity
// Detection returns: { complexity: { loc, files, frameworks, hasTests, hasCi } }
aiRecommendations = calculateRecommendations(detectResult.complexity)
```

**AI Recommendation Logic [CRITICAL - MUST ALWAYS EXECUTE]:**

Calculate `aiRecommendations` using complexity data from detection. Every Q2 question for Budget and Output includes exactly ONE option labeled "(Recommended)" based on these calculations. This step runs before Q2 is displayed.

```javascript
function calculateRecommendations(complexity) {
  // Default for small/unknown projects
  let budget = 8000
  let output = 25000

  // Medium complexity: 10K+ LOC or 100+ files or multiple frameworks
  if (complexity.loc > 10000 || complexity.files > 100 || complexity.frameworks > 2) {
    budget = 16000
    output = 35000
  }

  // Large complexity: 50K+ LOC or 500+ files or monorepo
  if (complexity.loc > 50000 || complexity.files > 500 || complexity.isMonorepo) {
    budget = 32000
    output = 35000
  }

  // Simple projects: <1000 LOC and <20 files
  if (complexity.loc < 1000 && complexity.files < 20) {
    budget = 4000
    output = 10000
  }

  return { budget, output }
}
```

**UNATTENDED MODE: Use AI recommendations directly:**

```javascript
if (isUnattended) {
  contextConfig = {
    budget: aiRecommendations.budget,
    output: aiRecommendations.output,
    data: "Public",
    compliance: []
  }
  // Skip Q2, proceed directly to Step-4
} else {
  // Interactive mode: Build Q2 with AI-recommended options marked
```

**Build Q2 dynamically (max 4 tabs):**

**[CRITICAL] Q2 Label Requirements:**
- Budget tab: Exactly ONE option has "(Recommended)" based on `aiRecommendations.budget`
- Output tab: Exactly ONE option has "(Recommended)" based on `aiRecommendations.output`
- When current equals recommended, show both: `[current] (Recommended)`
- Every tab includes exactly one "(Recommended)" option

```javascript
  // Helper: Generate label with appropriate suffix
  // Priority: [current] > (Recommended) > (CC default) > (none)
  function optionLabel(value, field, defaultSuffix = "") {
    const current = existingConfig[field]
    const recommended = aiRecommendations[field]  // MUST be set from calculateRecommendations()

    // If this value matches existing config
    if (current === value) {
      // If also recommended, show both
      if (recommended === value) return `${value} [current] (Recommended)`
      return `${value} [current]`
    }

    // If this value is AI-recommended (MUST show for exactly one option)
    if (recommended === value) return `${value} (Recommended)`

    // Otherwise show default suffix or nothing
    return defaultSuffix ? `${value} ${defaultSuffix}` : `${value}`
  }

  questions = []

  // Tab 1: Thinking Budget (only if Thinking Enabled)
  // MUST have exactly one option with (Recommended) based on aiRecommendations.budget
  if (setupConfig.thinking === "Enabled") {
    questions.push({
      question: "Thinking token budget?",
      header: "Budget",
      options: [
        { label: optionLabel(4000, "budget"), description: "Simple tasks, faster responses" },
        { label: optionLabel(8000, "budget"), description: "Good balance for most tasks" },
        { label: optionLabel(16000, "budget"), description: "Complex multi-file refactoring" },
        { label: optionLabel(32000, "budget"), description: "Architecture design, large codebases" }
      ],
      multiSelect: false
    })
  }

  // Tab 2: Output Limits
  // MUST have exactly one option with (Recommended) based on aiRecommendations.output
  questions.push({
    question: "Tool output limits?",
    header: "Output",
    options: [
      { label: optionLabel(10000, "output"), description: "Save context, reduced output" },
      { label: optionLabel(25000, "output", "(CC default)"), description: "Standard output limits" },
      { label: optionLabel(35000, "output"), description: "Large outputs, big codebases" }
    ],
    multiSelect: false
  })

  // Tab 3: Data Sensitivity
  questions.push({
    question: "Most sensitive data handled?",
    header: "Data",
    options: [
      { label: "Public (Recommended)", description: "Open data, no sensitivity" },
      { label: "PII", description: "Personal identifiable information" },
      { label: "Regulated", description: "Healthcare, finance, regulated data" }
    ],
    multiSelect: false
  })

  // Tab 4: Compliance (multiselect, none = no requirements)
  questions.push({
    question: "Compliance requirements?",
    header: "Compliance",
    options: [
      { label: "SOC2", description: "B2B SaaS, enterprise customers" },
      { label: "GDPR/CCPA", description: "Privacy regulations" },
      { label: "HIPAA/PCI", description: "Healthcare or payments" }
    ],
    multiSelect: true
  })

  AskUserQuestion(questions)
}
```

### Pre-Q2 Validation [CRITICAL]

Before calling AskUserQuestion for Q2, verify:
```
[x] aiRecommendations calculated from detectResult.complexity
[x] aiRecommendations.budget is one of: 4000, 8000, 16000, 32000
[x] aiRecommendations.output is one of: 10000, 25000, 35000
[x] Budget options contain exactly ONE "(Recommended)" label
[x] Output options contain exactly ONE "(Recommended)" label
```

**Example for ~10K LOC project (like ClaudeCodeOptimizer):**
```javascript
// Complexity: { loc: 9621, files: 32, frameworks: 3 }
// → aiRecommendations = { budget: 8000, output: 25000 }

// Budget options should be:
{ label: "4000", ... }
{ label: "8000 (Recommended)", ... }  // ← AI recommendation
{ label: "16000", ... }
{ label: "32000", ... }

// Output options should be:
{ label: "10000", ... }
{ label: "25000 (Recommended) (CC default)", ... }  // ← AI recommendation
{ label: "35000", ... }

// If current config has 35000:
{ label: "35000 [current]", ... }  // Just [current], not recommended
```

### Post-Q2 Validation
```
[x] User completed Q2 (or unattended defaults applied)
→ Store as: contextConfig = { budget?, output, data, compliance }
→ Proceed to Step-4
```

---

## Step-4: Apply [MANDATORY - NO SKIP]

**CRITICAL: You MUST call cco-agent-apply. Never skip based on "files already match" or similar reasoning.**

### 4.0: Orchestrator Checklist [CRITICAL]

| Operation | Method | Mode |
|-----------|--------|------|
| Rule extraction | cco-agent-analyze (generate phase) | - |
| File writes | cco-agent-apply | overwrite (rules), merge (settings.json) |
| Statusline scripts | Copy from package | overwrite |
| Pre-write cleanup | Delete `rules/cco/*.md` | delete_contents |

**Single Rule:** All rule generation goes through cco-agent-analyze. All file writes go through cco-agent-apply. Execute unconditionally - agents handle idempotency.

### 4.1: Generate Rules

**CRITICAL:** Call cco-agent-analyze with config scope (generate phase) to create rules.

**Write Modes (see cco-agent-apply.md for implementation):**

| Mode | Target | When | Behavior |
|------|--------|------|----------|
| `overwrite` | `context.md` | Setup/Update | Always replace, never skip |
| `overwrite` | Rule files (`*.md`) | Setup/Update | Always replace, never skip |
| `overwrite` | Statusline (`cco-*.js`) | Setup/Update | Always copy from package |
| `merge` | `settings.json` | Setup/Update | Add/update CCO keys, preserve others |
| `delete_contents` | `rules/cco/*.md` | Remove | Delete all files, keep directory |
| `unmerge` | `settings.json` | Remove | Remove only CCO keys |

**CRITICAL:** All files except settings.json are OVERWRITTEN every run. Execute writes regardless of existing file state or content.

**[IMPORTANT] Rule Source Architecture:**
- All rules are defined as **sections within `cco-adaptive.md`** (single file)
- Rule content is extracted from cco-adaptive.md sections, not from separate files
- The agent reads cco-adaptive.md and extracts relevant sections based on detections
- Source file: `cco-adaptive.md` only (separate `{category}.md` files do not exist in CCO package)

```javascript
// Phase 2: Generate rules using detections from Step-1 + user input from Steps 2-3
generateResult = Task("cco-agent-analyze", `
  scopes: ["config"]
  phase: "generate"

  Input:
  - detections: ${JSON.stringify(detectResult.detections)}
  - projectCritical: ${JSON.stringify(detectResult.projectCritical)}
  - complexity: ${JSON.stringify(detectResult.complexity)}
  - setupConfig: ${JSON.stringify(setupConfig)}
  - contextConfig: ${JSON.stringify(contextConfig)}

  [CRITICAL] Generate Phase Execution:
  1. Read cco-adaptive.md: Bash(cco-install --cat rules/cco-adaptive.md)
  2. Extract rule sections matching detections
  3. Generate context.md with Project Critical section (from projectCritical input)
  4. Generate rule files with extracted content

  [MANDATORY] context.md MUST include Project Critical at top:
  ## Project Critical
  Purpose: {projectCritical.purpose}
  Constraints: {projectCritical.constraints | join(", ")}
  Invariants: {projectCritical.invariants | join(", ")}
  Non-negotiables: {projectCritical.nonNegotiables | join(", ")}

  Return: { context, rules[], triggeredCategories[] }
`, { model: "haiku" })

// Agent returns (config scope, generate phase):
// generateResult = {
//   context: "{generated_context_md_content}",
//   rules: [
//     { file: "{category}.md", content: "{content_from_adaptive}" },
//     ...
//   ],
//   triggeredCategories: [{ category, trigger, rule, source }]
// }
```

### 4.2: Write Files [MANDATORY]

**CRITICAL: Always call this step. Never skip.**

**[CRITICAL] Clean Before Write:**
For Setup/Update, ALWAYS clean existing rule files first to ensure stale rules are removed:
1. Delete ALL existing `*.md` files in `rules/cco/` directory
2. Then write the new context.md and rule files

This ensures:
- Old rules from previous detections are removed (e.g., go.md if no longer detected)
- Fresh rules are always written based on current detections
- No stale configuration remains

```javascript
Task("cco-agent-apply", `
  action: "${setupConfig.context}"  // "Setup/Update" or "Remove"
  targetDir: "${targetDir}"

  // For Setup/Update:
  // Step 1: CLEAN - Delete all existing rule files first
  cleanRules: {
    path: "rules/cco/",
    pattern: "*.md",
    action: "delete_all"  // Delete ALL .md files before writing new ones
  }

  // Step 2: WRITE - Write fresh files (all files are overwritten):
  files: [
    // Context - ALWAYS overwrite
    { path: "rules/cco/context.md", mode: "overwrite", content: generateResult.context },

    // Rules - ALWAYS overwrite each rule file
    // For each rule in generateResult.rules:
    { path: "rules/cco/{rule.file}", mode: "overwrite", content: "{rule.content}" },

    // Statusline - ALWAYS overwrite (copy from CCO package)
    // If user selected Full or Minimal:
    { path: "cco-{mode}.js", mode: "overwrite", source: "$CCO_PATH/cco-{mode}.js" },

    // Settings - MERGE (only file that preserves existing content)
    { path: "settings.json", mode: "merge", content: {settings_object} }
  ]

  // For Remove:
  files: [
    { path: "rules/cco/", mode: "delete_contents", pattern: "*.md" },
    { path: "settings.json", mode: "unmerge" }
  ]
`, { run_in_background: true })
```

### Detection → Rule Mapping

**SSOT References (no duplication here):**
- **Trigger patterns & values:** `cco-triggers.md` (1176 lines, complete reference)
- **Detection → Rule File mapping:** `cco-agent-analyze.md` config scope (lines 353-386)
- **Rule content:** Extracted from `cco-adaptive.md` sections by agent

The cco-agent-analyze agent handles all detection-to-rule mapping internally using these SSOT sources. Pattern: `{Category}:{type}` → `{type}.md` or `{category}.md`

### Settings.json Structure

**Merge these settings into `${targetDir}/settings.json`:**

```json
{
  "statusLine": {
    "type": "command",
    "command": "node -e \"require('child_process').spawnSync('node',[require('path').join(process.cwd(),'.claude','cco-${statusline_mode}.js')],{stdio:'inherit'})\"",
    "padding": 1
  },
  "permissions": {
    "allow": ${permissions_allow},
    "deny": ${permissions_deny}
  },
  "alwaysThinkingEnabled": ${thinking_enabled},
  "env": {
    "ENABLE_LSP_TOOL": "${lsp_enabled ? '1' : '0'}",
    "MAX_THINKING_TOKENS": "${thinking_budget}",
    "MAX_MCP_OUTPUT_TOKENS": "${mcp_output_tokens}",
    "BASH_MAX_OUTPUT_LENGTH": "${bash_output_length}"
  }
}
```

**Note:** `${permissions_allow}` and `${permissions_deny}` are populated from the "Permissions Levels" table based on user selection + detected language tools.

**LSP Configuration:**

| Setting | Value | Effect |
|---------|-------|--------|
| `ENABLE_LSP_TOOL=1` | Enabled | go-to-definition, find-references, hover (+500 tokens) |
| `ENABLE_LSP_TOOL=0` | Disabled | Text-based search only |
| `permissions.allow: ["LSP"]` | Permission | Auto-approve LSP tool calls |

**Statusline Mapping:**

| Mode | Action |
|------|--------|
| Full | Copy `cco-full.js` from CCO package → `${targetDir}/cco-full.js` |
| Minimal | Copy `cco-minimal.js` from CCO package → `${targetDir}/cco-minimal.js` |
| No | Skip statusLine key in settings.json |

```bash
# Copy from package (never generate)
CCO_PATH=$(python3 -c "from claudecodeoptimizer.config import get_content_path; print(get_content_path('statusline'))")
cp "$CCO_PATH/cco-{mode}.js" "${targetDir}/cco-{mode}.js"
```

### If action = Remove

```javascript
Task("cco-agent-apply", `
  action: "Remove"
  targetDir: "${targetDir}"

  files: [
    { path: "rules/cco/", mode: "delete_contents", pattern: "*.md" },
    { path: "settings.json", mode: "unmerge" }
  ]
`)
// Uses unmerge mode: removes only CCO keys, preserves user settings
```

### If action = Export

```javascript
Task("cco-agent-apply", `
  Export rules to ${format}:
  - Read all ${targetDir}/rules/cco/*.md
  - Filter for target format
  - Write to ./${format}
`)
```

### Validation
```
[x] Files written/removed
[x] No errors
→ Proceed to Step-7
```

---

## Step-5: Report [SKIP IF --auto]

**If `--auto` flag: Skip this step entirely. No visual output.**

```
## Configuration Complete

| Metric | Value |
|--------|-------|
| Files written | {n} |
| Auto-detected | {n} elements |
| Questions asked | {n} |

Status: OK | Applied: {files_written} | Declined: 0 | Failed: 0

Restart Claude Code to apply new rules.
```

### Files Written Detail
| File | Action |
|------|--------|
| ${targetDir}/rules/cco/context.md | {Created\|Updated} |
| ${targetDir}/rules/cco/{language}.md | {Created\|Updated} |
| ${targetDir}/settings.json | {Merged} |
| ${targetDir}/cco-{mode}.js | {Copied} |

### Validation
```
[x] Report displayed (or skipped if --auto)
[x] All todos marked completed
→ Done
```

---

## Reference

### Question Flow Summary

| Scenario | Q1 | Q2 | Total |
|----------|----|----|-------|
| Setup/Update + Thinking Enabled | 4 tabs | 4 tabs | 2 questions |
| Setup/Update + Thinking Disabled | 4 tabs | 3 tabs | 2 questions |
| Remove | 4 tabs | - | 1 question |
| Export | 4 tabs | 1 tab (format) | 2 questions |

### Label Priority

| Label | When | Priority |
|-------|------|----------|
| `[current]` | Matches existing config | 1 (highest) |
| `(Recommended)` | AI recommendation or best practice | 2 |
| (none) | Other options | 3 |

**Rule:** Each tab has exactly ONE recommended option (either [current] or (Recommended), not both on same option unless current IS recommended).

### Permissions Levels

| Level | `permissions.allow` | `permissions.deny` |
|-------|---------------------|-------------------|
| Permissive | `["Read", "Glob", "Grep", "LSP", "Edit", "Write", "Bash", "Task"]` | `["Bash(git push -f:*)"]` |
| Balanced | `["Read", "Glob", "Grep", "LSP", {detected_lint_tools}, {detected_test_tools}]` | `[]` |
| Remove | Remove permissions key from settings.json | - |

### Balanced Tools by Language (from detection)

| Language | Lint Tools | Test Tools |
|----------|------------|------------|
| Python | `Bash(ruff:*)`, `Bash(mypy:*)` | `Bash(pytest:*)` |
| TypeScript | `Bash(eslint:*)`, `Bash(tsc:*)` | `Bash(vitest:*)`, `Bash(jest:*)` |
| JavaScript | `Bash(eslint:*)` | `Bash(vitest:*)`, `Bash(jest:*)` |
| Go | `Bash(golangci-lint:*)`, `Bash(go vet:*)` | `Bash(go test:*)` |
| Rust | `Bash(cargo clippy:*)`, `Bash(cargo check:*)` | `Bash(cargo test:*)` |
| Java | `Bash(checkstyle:*)`, `Bash(spotbugs:*)` | `Bash(mvn test:*)`, `Bash(gradle test:*)` |
| Ruby | `Bash(rubocop:*)` | `Bash(rspec:*)`, `Bash(minitest:*)` |
| PHP | `Bash(phpstan:*)`, `Bash(phpcs:*)` | `Bash(phpunit:*)` |
| C# | `Bash(dotnet build:*)` | `Bash(dotnet test:*)` |
| Swift | `Bash(swiftlint:*)` | `Bash(swift test:*)` |
| Kotlin | `Bash(ktlint:*)`, `Bash(detekt:*)` | `Bash(gradle test:*)` |
| Elixir | `Bash(mix credo:*)`, `Bash(mix dialyzer:*)` | `Bash(mix test:*)` |
| Dart | `Bash(dart analyze:*)` | `Bash(dart test:*)`, `Bash(flutter test:*)` |

**Note:** Detection merges tools from all detected languages. If project has both Python and TypeScript, include tools for both.

### LSP Features (v2.0.74+)

| Operation | Description | Use Case |
|-----------|-------------|----------|
| goToDefinition | Jump to symbol definition | Navigate to function/class source |
| findReferences | Find all usages | Understand impact of changes |
| hover | Get type/documentation | Quick info without opening file |
| documentSymbol | List symbols in file | File structure overview |
| workspaceSymbol | Search symbols globally | Find any symbol in codebase |

---

## Recovery

If something goes wrong during configuration:

| Situation | Recovery |
|-----------|----------|
| Wrong rules generated | Re-run `/cco-config`, select "Setup/Update", adjust answers |
| Want to start fresh | Run `/cco-config` → Remove, then Setup again |
| Settings.json corrupted | Delete `${targetDir}/settings.json`, re-run `/cco-config` |
| Detection crashed | Re-run `/cco-config` - detection is stateless |
| Wrong AI Performance | `/cco-config` → Setup/Update, change Thinking/Budget/Output |
| Applied wrong permissions | Re-run `/cco-config`, select different Permissions level |

**Safe pattern:** CCO config files are additive. Removing and re-creating is always safe.

---

## Rules

1. **Background detection** - Start detection while asking Q1
2. **Max 2 questions** - Q1 always, Q2 only if Setup/Update
3. **Dynamic tabs** - Show only relevant tabs based on previous answers
4. **Single Recommended** - Each tab has exactly one recommended option
5. **AI-driven defaults** - Budget/Output based on project complexity
6. **Explicit defaults** - Write ALL settings to files, including default values. Exception: statusLine "Remove" preserves global config.
7. **[CRITICAL] Agent-only extraction** - NEVER use grep/sed/awk on cco-adaptive.md. ALWAYS use cco-agent-analyze (generate phase)
8. **[CRITICAL] projectCritical flow** - detect phase extracts → generate phase receives → context.md includes at top
9. **[CRITICAL] No duplication** - Purpose appears in Project Critical section ONLY, not in Strategic Context
