---
name: cco-config
description: |
  Configure project context, rules, and AI settings.
  TRIGGERS: "config", "setup", "configure", "rules", "settings"
  USE WHEN: First setup OR changing project context/rules
  FLAGS: --auto (unattended), --target-dir
  CREATES: context.md, language rules, settings.json, statusline
allowed-tools: Read(*), Write(*), Edit(*), Bash(*), Task(*), AskUserQuestion
---

# /cco-config

**Project Setup** - Background detection + combined questions for fast configuration.

## Args

- `--auto` or `--unattended`: Fully unattended mode for CI/CD and benchmarks
  - **No questions asked** - uses optimal defaults
  - **No progress output** - silent execution
  - **Only final summary** - single status line at end
  - Defaults:
    - Context: Setup/Update
    - Statusline: Skip (keep unchanged)
    - Permissions: Skip (keep unchanged)
    - Thinking: Enabled
    - Budget: AI-recommended based on project complexity
    - Output: AI-recommended based on project complexity
    - Data: Public
    - Compliance: None
- `--target-dir <path>`: Write config files to specified directory instead of `.claude`
  - Example: `--target-dir .claude` (explicit default)
  - Example: `--target-dir /tmp/project/.claude` (absolute path)
  - Useful for: benchmarks, testing, custom project layouts

**Usage:**
- `/cco-config --auto` - Silent setup with optimal defaults
- `/cco-config --auto --target-dir .claude` - Silent setup to specific directory
- `/cco-config --target-dir /custom/path/.claude` - Interactive with custom target

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
  // SILENT MODE: No TodoWrite, no progress output, no intermediate messages
  // Skip Q1, Q2 - proceed directly with defaults

  setupConfig = {
    context: "Setup/Update",
    statusline: "Skip",           // Non-invasive: keep unchanged
    permissions: "Skip",          // Non-invasive: keep unchanged
    thinking: "Enabled"
  }

  // Execute silently:
  // 1. Run detection (no output)
  // 2. Generate rules (no output)
  // 3. Write files (no output)
  // 4. Show ONLY final summary line

  // → Jump directly to Step-1 detection, skip all UX output
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

## Step-1: Pre-detect [BACKGROUND]

**Launch detection in background while Q1 is asked:**

```javascript
// Start detection immediately - runs while user answers Q1
// NOTE: This only does DETECTION. Rule generation happens in Step-4 after user input.
detectTask = Task("cco-agent-analyze", `
  scopes: ["config"]

  [DETECTION ONLY - No rule generation yet]
  Auto-detect from manifest files and code using PARALLEL tool calls:

  Step 1 (PARALLEL):
  - Glob("{manifest}")              // Language manifests (pyproject.toml, package.json, etc.)
  - Glob("Dockerfile*", ".github/workflows/*")
  - Read("README.md"), Read("CLAUDE.md"), Read("{manifest}")
  - Bash(find . -name '{ext}' | wc -l)

  Extract:
  - detections: { language, type, api, database, frontend, infra, dependencies }
  - complexity: { loc, files, frameworks, hasTests, hasCi, isMonorepo }
  - projectCritical: { purpose, constraints[], invariants[], nonNegotiables[] }
  - sources: [{ file, confidence }]

  [CRITICAL] projectCritical extraction:
  - purpose: README.md first paragraph or {manifest} description
  - constraints: "MUST", "REQUIRED", "NEVER", "ALWAYS" from CLAUDE.md
  - invariants: "zero dependencies", "100% coverage" patterns
  - nonNegotiables: Rules in ## Rules sections
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
→ If statusline = "Full" or "Minimal": Ask scope question (Step-2.5)
→ Proceed to Step-3
```

---

## Step-2.5: Scope Questions [CONDITIONAL]

**Ask scope when install or remove is selected for statusline/permissions:**

```javascript
// Build scope questions dynamically based on Q1 selections
scopeQuestions = []

// Statusline: Install scope (Full or Minimal)
if (setupConfig.statusline === "Full" || setupConfig.statusline === "Minimal") {
  scopeQuestions.push({
    question: "Where to install statusline?",
    header: "Statusline",
    options: [
      { label: "Global (Recommended)", description: "~/.claude - applies to all projects on this machine" },
      { label: "Local", description: "./.claude - this project only" }
    ],
    multiSelect: false
  })
}

// Statusline: Remove scope
if (setupConfig.statusline === "Remove") {
  scopeQuestions.push({
    question: "Where to remove statusline from?",
    header: "Statusline",
    options: [
      { label: "Local (Recommended)", description: "./.claude - remove from this project only" },
      { label: "Global", description: "~/.claude - remove from all projects" }
    ],
    multiSelect: false
  })
}

// Permissions: Remove scope
if (setupConfig.permissions === "Remove") {
  scopeQuestions.push({
    question: "Where to remove permissions from?",
    header: "Permissions",
    options: [
      { label: "Local (Recommended)", description: "./.claude - remove from this project only" },
      { label: "Global", description: "~/.claude - remove from all projects" }
    ],
    multiSelect: false
  })
}

// Ask scope questions if any
if (scopeQuestions.length > 0) {
  if (!isUnattended) {
    AskUserQuestion(scopeQuestions)
    // Store results:
    // setupConfig.statuslineScope = "Global" | "Local"
    // setupConfig.permissionsScope = "Global" | "Local"
  } else {
    // Unattended: default to Local (non-invasive)
    setupConfig.statuslineScope = "Local"
    setupConfig.permissionsScope = "Local"
  }
}
```

### Scope Behavior

| Action | Scope | Target Directory | Settings File |
|--------|-------|------------------|---------------|
| Install statusline | Global | `~/.claude/` | `~/.claude/settings.json` |
| Install statusline | Local | `./.claude/` | `./.claude/settings.json` |
| Remove statusline | Global | `~/.claude/` | `~/.claude/settings.json` |
| Remove statusline | Local | `./.claude/` | `./.claude/settings.json` |
| Remove permissions | Global | - | `~/.claude/settings.json` |
| Remove permissions | Local | - | `./.claude/settings.json` |

**Global Installation:**
```bash
# Copy statusline script to global config
CCO_PATH=$(python3 -c "from claudecodeoptimizer.config import get_content_path; print(get_content_path('statusline'))")
cp "$CCO_PATH/cco-{mode}.js" ~/.claude/cco-statusline.js

# Update global settings.json (merge statusLine key only)
# Other global settings preserved
```

**Local Installation:**
```bash
# Copy to project .claude (existing behavior)
cp "$CCO_PATH/cco-{mode}.js" ./.claude/cco-statusline.js
# Update ./.claude/settings.json
```

**Global Removal:**
```bash
# Remove statusline from global config
rm -f ~/.claude/cco-statusline.js
# Remove statusLine key from ~/.claude/settings.json

# Remove permissions from global config
# Remove permissions key from ~/.claude/settings.json
```

**Local Removal:**
```bash
# Remove statusline from project
rm -f ./.claude/cco-statusline.js
# Remove statusLine key from ./.claude/settings.json

# Remove permissions from project
# Remove permissions key from ./.claude/settings.json
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

**Tab Philosophy:**
| Tab | Source | Recommendation |
|-----|--------|----------------|
| Budget | AI (complexity detection) | AI-calculated from LOC/files/frameworks |
| Output | AI (complexity detection) | AI-calculated from project size |
| Data | User knowledge | No AI recommendation - user must choose |
| Compliance | User knowledge | No AI recommendation - multiselect |

**[CRITICAL] Q2 Label Requirements:**
- Budget tab: Exactly ONE option has "(Recommended)" based on `aiRecommendations.budget`
- Output tab: Exactly ONE option has "(Recommended)" based on `aiRecommendations.output`
- Data tab: No (Recommended) - user must explicitly choose
- Compliance tab: No (Recommended) - optional multiselect
- When current equals recommended, show both: `[current] (Recommended)`

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
  // No AI recommendation - user must explicitly choose based on their data
  questions.push({
    question: "Most sensitive data handled?",
    header: "Data",
    options: [
      { label: "Public", description: "Open data, no sensitivity constraints" },
      { label: "PII", description: "Personal identifiable information - stricter validation" },
      { label: "Regulated", description: "Healthcare, finance - compliance-level security" }
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

**Example for ~10K LOC project:**
```javascript
// Complexity: { loc: {n}, files: {n}, frameworks: {n} }
// → aiRecommendations = { budget: {budget_value}, output: {output_value} }

// Budget options should be:
{ label: "4000", ... }
{ label: "{budget_value} (Recommended)", ... }  // ← AI recommendation
{ label: "16000", ... }
{ label: "32000", ... }

// Output options should be:
{ label: "10000", ... }
{ label: "{output_value} (Recommended) (CC default)", ... }  // ← AI recommendation
{ label: "35000", ... }

// If current config has different value:
{ label: "{current_value} [current]", ... }  // Just [current], not recommended
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
| Rule extraction | cco-agent-analyze (targeted extraction) | sed patterns |
| File writes | cco-agent-apply | overwrite (rules), merge (settings.json) |
| Statusline scripts | Copy from package | overwrite |
| Pre-write cleanup | Delete `rules/cco/*.md` | delete_contents |

**Single Rule:** All rule generation goes through cco-agent-analyze with targeted extraction. All file writes go through cco-agent-apply. Execute unconditionally - agents handle idempotency.

### 4.1: Generate Rules

**CRITICAL:** Generate rules using targeted section extraction (NOT full file read).

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

**[IMPORTANT] Targeted Extraction Architecture:**
- All rules defined in single `cco-adaptive.md` file (3142 lines)
- Extract ONLY needed sections using sed patterns (saves ~90% tokens)
- Each section ~20-50 lines instead of reading entire file

```javascript
// Generate rules using TARGETED extraction (not full file read)
generateResult = Task("cco-agent-analyze", `
  scopes: ["config"]

  Input:
  - detections: ${JSON.stringify(detectResult.detections)}
  - projectCritical: ${JSON.stringify(detectResult.projectCritical)}
  - complexity: ${JSON.stringify(detectResult.complexity)}
  - setupConfig: ${JSON.stringify(setupConfig)}
  - contextConfig: ${JSON.stringify(contextConfig)}

  [CRITICAL] Targeted Section Extraction:
  1. Get CCO path: CCO_PATH=$(python3 -c "from claudecodeoptimizer.config import get_content_path; print(get_content_path('rules'))")
  2. For each detection, extract matching section using sed patterns:
     Examples (concrete):
     - L:Python → sed -n '/^### Python (L:Python)/,/^###\|^---\|^## /p' "$CCO_PATH/cco-adaptive.md"
     - L:TypeScript → sed -n '/^### TypeScript (L:TypeScript)/,/^###\|^---\|^## /p' "$CCO_PATH/cco-adaptive.md"
     - Backend:FastAPI → sed -n '/^### FastAPI/,/^###\|^---\|^## /p' "$CCO_PATH/cco-adaptive.md"
     - Frontend:React → sed -n '/^### React/,/^###\|^---\|^## /p' "$CCO_PATH/cco-adaptive.md"
     Pattern (generic): sed -n '/^### {SectionHeader}/,/^###\|^---\|^## /p' "$CCO_PATH/cco-adaptive.md"
  3. Run ALL extractions in PARALLEL using: command1 & command2 & wait
  4. Generate context.md from projectCritical + userInput
  5. Generate rule files from extracted sections

  [MANDATORY] context.md MUST include Project Critical at top:
  ## Project Critical
  Purpose: {projectCritical.purpose}
  Constraints: {projectCritical.constraints | join(", ")}
  Invariants: {projectCritical.invariants | join(", ")}
  Non-negotiables: {projectCritical.nonNegotiables | join(", ")}

  Return: { context, rules[], triggeredCategories[] }
`, { model: "haiku" })

// Agent returns:
// generateResult = {
//   context: "{generated_context_md_content}",
//   rules: [
//     { file: "{category}.md", content: "{extracted_via_sed}" },
//     ...
//   ],
//   triggeredCategories: [{ category, trigger, rule, source }]
// }
```

**Token Savings Comparison:**

| Approach | Lines Read | Tokens |
|----------|------------|--------|
| Full file read | 3142 | ~12,000 |
| Targeted extraction (5 sections) | ~200 | ~800 |
| **Savings** | **~94%** | **~94%** |

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
    { path: "cco-statusline.js", mode: "overwrite", source: "$CCO_PATH/cco-{mode}.js" },

    // Settings - MERGE (only file that preserves existing content)
    { path: "settings.json", mode: "merge", content: {settings_object} }
  ]

  // For Remove:
  files: [
    { path: "rules/cco/", mode: "delete_contents", pattern: "*.md" },
    { path: "settings.json", mode: "unmerge" }
  ]
`, { model: "haiku", run_in_background: true })
```

### Detection → Rule Mapping

**Quick Reference (common patterns):**

| Detection | Rule File | Example Trigger |
|-----------|-----------|-----------------|
| L:Python | python.md | pyproject.toml, *.py |
| L:TypeScript | typescript.md | tsconfig.json, *.ts |
| Backend:FastAPI | backend.md | fastapi in deps |
| Frontend:React | frontend.md | react in deps |
| Infra:Docker | container.md | Dockerfile |
| CI:GitHub | ci-cd.md | .github/workflows/ |
| Test:pytest | testing.md | pytest in deps |

**Full SSOT Sources:**
- **Trigger patterns:** `cco-triggers.md` (1176 lines, all file/pattern mappings)
- **All detections:** `cco-adaptive.md` Detection System section (lines 19-291)
- **Rule content:** Extracted from `cco-adaptive.md` by cco-agent-analyze

**Mapping Pattern:** `{Category}:{Type}` → `{type}.md` or `{category}.md`

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

| Mode | Scope | Target | Settings File |
|------|-------|--------|---------------|
| Full | Global | `~/.claude/cco-statusline.js` | `~/.claude/settings.json` |
| Full | Local | `${targetDir}/cco-statusline.js` | `${targetDir}/settings.json` |
| Minimal | Global | `~/.claude/cco-statusline.js` | `~/.claude/settings.json` |
| Minimal | Local | `${targetDir}/cco-statusline.js` | `${targetDir}/settings.json` |
| Skip | - | No action | No change |
| Remove | Global | Delete `~/.claude/cco-statusline.js` | Remove statusLine from `~/.claude/settings.json` |
| Remove | Local | Delete `${targetDir}/cco-statusline.js` | Remove statusLine from `${targetDir}/settings.json` |

**Permissions Mapping:**

| Action | Scope | Settings File |
|--------|-------|---------------|
| Permissive | Local | `${targetDir}/settings.json` |
| Balanced | Local | `${targetDir}/settings.json` |
| Skip | - | No change |
| Remove | Global | Remove permissions from `~/.claude/settings.json` |
| Remove | Local | Remove permissions from `${targetDir}/settings.json` |

```bash
# Determine target based on scope
if [ "${statuslineScope}" = "Global" ]; then
  STATUSLINE_DIR=~/.claude
else
  STATUSLINE_DIR="${targetDir}"
fi

# Copy from package (never generate)
CCO_PATH=$(python3 -c "from claudecodeoptimizer.config import get_content_path; print(get_content_path('statusline'))")
cp "$CCO_PATH/cco-${mode}.js" "$STATUSLINE_DIR/cco-statusline.js"

# Update settings.json in the same directory
# Merge statusLine key into $STATUSLINE_DIR/settings.json
```

**Settings.json statusLine path:**
```json
{
  "statusLine": {
    "type": "command",
    "command": "node -e \"require('child_process').spawnSync('node',[require('path').join('${STATUSLINE_DIR}','cco-statusline.js')],{stdio:'inherit'})\"",
    "padding": 1
  }
}
```

**Note:** When scope is Global, the statusLine command uses absolute path `~/.claude/cco-statusline.js`. When Local, it uses relative path `.claude/cco-statusline.js`.

### If action = Remove (Context)

```javascript
Task("cco-agent-apply", `
  action: "Remove"
  targetDir: "${targetDir}"

  files: [
    { path: "rules/cco/", mode: "delete_contents", pattern: "*.md" },
    { path: "settings.json", mode: "unmerge" }
  ]
`, { model: "haiku" })
// Uses unmerge mode: removes only CCO keys, preserves user settings
```

### Statusline Remove (scope-aware)

```javascript
if (setupConfig.statusline === "Remove") {
  const statuslineDir = setupConfig.statuslineScope === "Global" ? "~/.claude" : "${targetDir}"

  Task("cco-agent-apply", `
    action: "RemoveStatusline"
    targetDir: "${statuslineDir}"

    files: [
      { path: "cco-*.js", mode: "delete" },
      { path: "settings.json", mode: "unmerge", keys: ["statusLine"] }
    ]
  `, { model: "haiku" })
}
```

### Permissions Remove (scope-aware)

```javascript
if (setupConfig.permissions === "Remove") {
  const permissionsDir = setupConfig.permissionsScope === "Global" ? "~/.claude" : "${targetDir}"

  Task("cco-agent-apply", `
    action: "RemovePermissions"
    targetDir: "${permissionsDir}"

    files: [
      { path: "settings.json", mode: "unmerge", keys: ["permissions"] }
    ]
  `, { model: "haiku" })
}
```

### If action = Export

```javascript
Task("cco-agent-apply", `
  Export rules to ${format}:
  - Read all ${targetDir}/rules/cco/*.md
  - Filter for target format
  - Write to ./${format}
`, { model: "haiku" })
```

### Validation
```
[x] Files written/removed
[x] No errors
→ Proceed to Step-5
```

---

## Step-5: Report

### Unattended Mode Output [--auto]

**Single line summary only:**

```javascript
if (isUnattended) {
  // ONLY output - single status line
  console.log(`cco-config: OK | Files: ${filesWritten} | Rules: ${rulesGenerated}`)
  // No tables, no details, no "restart" message
  return
}
```

### Interactive Mode Output

```
## Configuration Complete

| Metric | Value |
|--------|-------|
| Files written | {n} |
| Auto-detected | {n} elements |
| Questions asked | {n} |

Status: OK | Applied: {files_written} | Failed: 0

Restart Claude Code to apply new rules.
```

### Files Written Detail (Interactive only)
| File | Action |
|------|--------|
| ${targetDir}/rules/cco/context.md | {Created\|Updated} |
| ${targetDir}/rules/cco/{language}.md | {Created\|Updated} |
| ${targetDir}/settings.json | {Merged} |
| ${targetDir}/cco-{mode}.js | {Copied} |

### Recommended Next Steps (Interactive only)

Based on detected stack and configuration, show relevant next steps:

```javascript
// Build recommendations from detection + config
nextSteps = []

// Security-first if PII/Regulated data
if (contextConfig.data === "PII" || contextConfig.data === "Regulated") {
  nextSteps.push("1. `/cco-optimize --security` - Run security audit first")
}

// Quick wins for any project
nextSteps.push(`${nextSteps.length + 1}. \`/cco-status\` - See project health dashboard`)
nextSteps.push(`${nextSteps.length + 1}. \`/cco-optimize --quick\` - Auto-fix safe issues`)

// Show formatted
console.log("\n### Recommended Next Steps\n")
nextSteps.forEach(step => console.log(step))
```

### Common Pitfalls for Your Stack (Interactive only)

Show 2-3 stack-specific pitfalls based on detected language/framework:

```javascript
// Select pitfalls based on detection
pitfalls = detectResult.detections.map(d => PITFALL_DB[d]).flat().slice(0, 3)

// PITFALL_DB examples (not exhaustive):
PITFALL_DB = {
  "L:Python": [
    "N+1 queries with SQLAlchemy - use `selectinload()` for relationships",
    "Missing `encoding='utf-8'` in file operations"
  ],
  "L:TypeScript": [
    "Using `any` instead of `unknown` for truly unknown types",
    "Missing `strict: true` in tsconfig.json"
  ],
  "Backend:FastAPI": [
    "Missing rate limiting on public endpoints",
    "Sync I/O in async route handlers"
  ],
  "Backend:Django": [
    "DEBUG=True in production settings",
    "Missing CSRF protection on forms"
  ],
  "D:PII": [
    "Logging PII without redaction",
    "Missing encryption at rest for sensitive fields"
  ],
  "Infra:Docker": [
    "Running as root in container",
    "Missing multi-stage build for smaller images"
  ]
}

// Show formatted (only if pitfalls found)
if (pitfalls.length > 0) {
  console.log("\n### Common Pitfalls for Your Stack\n")
  pitfalls.forEach((p, i) => console.log(`${i + 1}. ${p}`))
}
```

### Validation
```
[x] Report displayed (single line if --auto, full if interactive)
[x] All todos marked completed (skipped if --auto)
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
7. **[CRITICAL] Targeted extraction** - Use sed patterns to extract ONLY needed sections from cco-adaptive.md (~94% token savings)
8. **[CRITICAL] projectCritical flow** - detection extracts → generation receives → context.md includes at top
9. **[CRITICAL] No duplication** - Purpose appears in Project Critical section ONLY, not in Strategic Context
