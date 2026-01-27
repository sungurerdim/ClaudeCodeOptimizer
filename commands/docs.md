---
description: Documentation gap analysis - compare ideal vs current docs, generate missing content
argument-hint: [--auto] [--check] [--report] [--preview] [--scope=<scope>] [--plan] [--force]
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Task, AskUserQuestion
model: opus
---

# /docs

**Documentation Gap Analysis** - Identify missing docs, generate what's needed.

> **Implementation Note:** Code blocks use JavaScript-like pseudocode for clarity. Actual execution uses Claude Code tools with appropriate parameters.

**Philosophy:** "What documentation does this project need?" → "What exists?" → "Fill the gap."

**Purpose:** Strategic documentation management. Not encyclopedic - focused, actionable, human-readable.

## Documentation Principles [CRITICAL]

All generated documentation MUST follow these principles:

### Efficiency First
- **Brevity > verbosity**: Every sentence must earn its place
- **No filler**: Skip "This document explains..." - just explain
- **Action-oriented**: Focus on what reader needs to DO, not history
- **Examples > prose**: Show, don't tell

### Human-Readable
- **Scan-friendly**: Headers, bullets, tables for quick scanning
- **Plain language**: 8th grade reading level, avoid jargon
- **Context-aware**: Assume reader's time is limited
- **No boilerplate**: Skip legal disclaimers, version history preambles

### UX/DX Focused
- **Task-driven**: Organize by "I want to..." not "This system..."
- **Copy-pasteable**: Commands should work when pasted
- **Progressive disclosure**: Essential first, details later
- **Troubleshooting**: Include common issues and solutions

### What NOT to Generate
- Academic-style comprehensive documentation
- Marketing language or promotional content
- Obvious information (e.g., "This is a README file")
- Version history in body (use CHANGELOG)
- Author credits in every file
- Duplicate information across files

## Args

- `--auto`: Fully unattended mode - detect, analyze, generate all missing docs
- `--check`: Validation only, return status (for other commands)
- `--report`: Analyze gaps only, no generation (alias: `--dry-run`)
- `--scope=X`: Single scope: readme, api, dev, user, ops, changelog
- `--plan`: Show detailed plan before generating (auto-enabled for >3 docs)
- `--force`: Regenerate even if docs exist (update mode)

## Scopes

| Scope | Target Files | Purpose |
|-------|--------------|---------|
| `readme` | README.md | Project overview, quick start |
| `api` | docs/api/*.md, API.md | Endpoint/function reference |
| `dev` | CONTRIBUTING.md, docs/dev/*.md | Developer onboarding |
| `user` | docs/user/*.md, USAGE.md | End-user guides |
| `ops` | docs/ops/*.md, DEPLOY.md | Deployment, operations |
| `changelog` | CHANGELOG.md | Version history |

## Context

- Git status: !`git status --short`
- Args: $ARGS

**DO NOT re-run these commands. Use the pre-collected values above.**

## Profile Requirement [CRITICAL]

CCO profile is auto-loaded from `.claude/rules/cco-profile.md` via Claude Code's auto-context mechanism.

**Sync with /cco:tune:** The profile's `documentation` section is populated by tune's detection phase. This includes:
- 50+ documentation file patterns (README, API specs, CI/CD, etc.)
- docs/ directory analysis
- Critical missing docs based on project type

This data is reused by docs command - no duplicate detection needed.

**Check:** Delegate to `/cco:tune --check` for profile validation:

```javascript
// Delegate profile check to tune command
const tuneResult = await Skill("tune", "--check")

if (tuneResult.status === "skipped") {
  // User declined setup - exit gracefully
  console.log("CCO setup skipped. Run /cco:tune when ready.")
  return
}

// Profile is now valid - continue with command
// NOTE: Profile may be minimal for new projects - handle gracefully
```

**After tune completes → continue to Mode Detection**

---

## Mode Detection

```javascript
const args = "$ARGS"
const isUnattended = args.includes("--auto")
const isCheckOnly = args.includes("--check")
const isReportOnly = args.includes("--report") || args.includes("--dry-run")
const forceUpdate = args.includes("--force")
const showPlan = args.includes("--plan")

// Parse scope filter
const scopeArg = args.match(/--scope=(\w+)/)?.[1]
const validScopes = ["readme", "api", "dev", "user", "ops", "changelog"]
const scopeFilter = scopeArg && validScopes.includes(scopeArg) ? [scopeArg] : null

if (isUnattended) {
  config = {
    scopes: scopeFilter || validScopes,  // All scopes if not filtered
    mode: "generate",                     // Generate missing docs
    planReview: false                     // Skip plan in auto mode
  }
  // → Skip Q1, proceed directly to Step-1b
}
```

---

## Architecture

| Step | Name | Action | Optimization | Dependency |
|------|------|--------|--------------|------------|
| 0 | Mode | Detect --auto or interactive | Instant | - |
| 1a | Q1 | Scope selection | Single question | [PARALLEL] with 1b |
| 1b | Analysis | Scan existing docs + detect needs | Parallel | [PARALLEL] with 1a |
| 2 | Gap Analysis | Ideal vs current comparison | Progressive | [SEQUENTIAL] after 1b |
| 3 | Plan Review | Show what will be generated (conditional) | User decision | [SEQUENTIAL] after 2 |
| 4 | Generate | Create missing documentation | Verified | [SEQUENTIAL] after 3 |
| 5 | Summary | Show results | Instant | [SEQUENTIAL] after 4 |

**Execution Flow:** Step-0 → (1a ‖ 1b) → 2 → [3 if plan mode] → 4 → 5

**Plan Review triggers automatically when:**
- `--plan` flag is passed
- >3 documents to generate
- API documentation scope selected

**Skipped when:** `--auto` mode (unless `--auto --plan`)

---

## Step-1a: Scope Selection [Q1] [SKIP IF --auto]

```javascript
if (!isUnattended) {
  AskUserQuestion([
    {
      question: "Which documentation to check?",
      header: "Areas",
      options: [
        { label: "Core (Recommended)", description: "README, CHANGELOG - every project needs" },
        { label: "Technical (Recommended)", description: "API reference, developer guide" },
        { label: "User-facing", description: "User guide, operations/deployment" }
      ],
      multiSelect: true
    },
    {
      question: "What to do with gaps?",
      header: "Mode",
      options: [
        { label: "Fill Gaps (Recommended)", description: "Generate only missing docs" },
        { label: "Update All", description: "Refresh outdated docs too" }
      ],
      multiSelect: false
    }
  ])

  // Map selections to config
  config.scopes = mapScopeGroups(answers["Areas"])
  config.mode = answers["Mode"].includes("Update") ? "update" : "generate"
}
```

### Validation
```
[x] User completed Q1 (or skipped if --auto)
→ Store as: config = { scopes, mode }
→ Proceed to Step-1b
```

---

## Step-1b: Background Analysis

```javascript
// Scan existing documentation structure
analysisTask = Task("cco-agent-analyze", `
  scope: docs

  ## Analysis Tasks

  1. **Scan existing docs:**
     - README.md existence and completeness
     - docs/ folder structure
     - CHANGELOG.md, CONTRIBUTING.md, API.md
     - Inline code comments quality

  2. **Detect project type from code:**
     - CLI → needs usage examples, flags reference
     - Library → needs API reference, installation
     - API → needs endpoint docs, auth guide
     - Web → needs component docs, routing

  3. **Detect documentation needs:**
     - Public APIs without docs
     - Complex functions without comments
     - Configuration without examples
     - Scripts without usage info

  4. **Handle minimal/empty profile:**
     - If profile is minimal, infer from code:
       - package.json/pyproject.toml for project type
       - Source files for language/framework
       - Existing docs for conventions

  Return: {
    existing: {
      readme: { exists, completeness, sections },
      api: { exists, coverage, endpoints },
      dev: { exists, completeness },
      user: { exists, guides },
      ops: { exists, sections },
      changelog: { exists, format }
    },
    detected: {
      projectType: "CLI|Library|API|Web",
      publicAPIs: [{ name, file, documented }],
      configFiles: [{ name, documented }],
      scripts: [{ name, documented }]
    },
    inferred: {
      languages: [],
      frameworks: [],
      buildTool: null
    }
  }
`, { model: "haiku" })  // Synchronous - results returned directly
// NOTE: Do NOT use run_in_background: true for Task (agent) calls
```

---

## Step-2: Gap Analysis [IDEAL vs CURRENT]

```javascript
// agentResponse is already set from Step-1 (synchronous Task call)
agentResponse = analysisTask  // Task returns results directly when synchronous
existing = agentResponse.existing
detected = agentResponse.detected
inferred = agentResponse.inferred

// Use profile if available, fallback to inferred
projectType = profile?.project?.type || detected.projectType || "API"
```

### Define Ideal Documentation (by Project Type)

```javascript
// Ideal docs structure by project type
const idealDocs = {
  CLI: {
    readme: ["description", "installation", "quick-start", "flags", "examples"],
    api: [],  // CLIs rarely need API docs
    dev: ["setup", "testing", "releasing"],
    user: ["usage", "configuration", "troubleshooting"],
    ops: [],  // Usually not needed
    changelog: ["format:keepachangelog"]
  },
  Library: {
    readme: ["description", "installation", "quick-start", "api-overview"],
    api: ["functions", "types", "examples"],
    dev: ["setup", "testing", "contributing", "architecture"],
    user: ["guides", "recipes"],
    ops: ["publishing"],
    changelog: ["format:keepachangelog"]
  },
  API: {
    readme: ["description", "quick-start", "auth", "endpoints-overview"],
    api: ["endpoints", "request-response", "errors", "rate-limits"],
    dev: ["setup", "testing", "database", "architecture"],
    user: ["getting-started", "authentication", "examples"],
    ops: ["deployment", "configuration", "monitoring"],
    changelog: ["format:keepachangelog"]
  },
  Web: {
    readme: ["description", "quick-start", "tech-stack"],
    api: ["components", "state", "routing"],
    dev: ["setup", "testing", "styling", "architecture"],
    user: ["features", "navigation"],
    ops: ["deployment", "environment-vars", "build"],
    changelog: ["format:keepachangelog"]
  }
}

const ideal = idealDocs[projectType]
```

### Calculate Gaps

```javascript
const gaps = {}

for (const scope of config.scopes) {
  const current = existing[scope]
  const required = ideal[scope]

  if (required.length === 0) {
    gaps[scope] = { needed: false, reason: "Not required for this project type" }
    continue
  }

  if (!current.exists) {
    gaps[scope] = {
      needed: true,
      priority: "HIGH",
      sections: required,
      reason: "Does not exist"
    }
  } else if (current.completeness < 70) {
    const missingSections = required.filter(s => !current.sections?.includes(s))
    gaps[scope] = {
      needed: config.mode === "update",
      priority: "MEDIUM",
      sections: missingSections,
      reason: `Missing sections: ${missingSections.join(", ")}`
    }
  } else {
    gaps[scope] = { needed: false, reason: "Complete" }
  }
}

// Count gaps
const gapCount = Object.values(gaps).filter(g => g.needed).length
```

### Display Gap Analysis

```markdown
## Documentation Gap Analysis

Project Type: {projectType} | Mode: {config.mode}

| Scope | Status | Priority | Missing |
|-------|--------|----------|---------|
{config.scopes.map(s => {
  const g = gaps[s]
  const status = g.needed ? "MISSING" : (g.reason === "Complete" ? "OK" : "SKIP")
  return `| ${s} | ${status} | ${g.priority || "-"} | ${g.sections?.join(", ") || g.reason} |`
})}

**Summary:** {gapCount} scopes need documentation
```

### Check Mode (--check)

```javascript
if (isCheckOnly) {
  const status = gapCount === 0 ? "ok" : "warn"
  return {
    status: status,
    gaps: gapCount,
    missing: Object.entries(gaps).filter(([k, v]) => v.needed).map(([k]) => k)
  }
}
```

### Validation
```
[x] Gap analysis complete
→ If --report: Skip to Step-5
→ If gapCount === 0: Skip to Step-5
→ Check Plan Review triggers → Step-3 or Step-4
```

---

## Step-3: Plan Review [CONDITIONAL]

### Trigger Conditions

```javascript
const planMode = showPlan ||
  (gapCount > 3) ||
  (config.scopes.includes("api"))

const skipPlan = isUnattended && !args.includes("--plan")

if (planMode && !skipPlan && !isReportOnly) {
  // → Enter Plan Review
} else {
  // → Skip to Step-4
}
```

### Generate Documentation Plan

```javascript
const docPlans = Object.entries(gaps)
  .filter(([scope, gap]) => gap.needed)
  .map(([scope, gap]) => ({
    scope: scope,
    priority: gap.priority,
    sections: gap.sections,

    plan: {
      file: getTargetFile(scope),              // README.md, docs/api/index.md, etc.
      format: getFormat(scope, projectType),   // markdown, structured
      length: estimateLength(scope, detected), // ~50 lines, ~200 lines
      sources: detectSources(scope, detected), // Code to extract from
      style: "concise"                         // Always concise
    }
  }))
```

### Display Plan

```markdown
## Documentation Generation Plan

> All docs will be concise, action-oriented, and copy-pasteable.

| # | Scope | Target File | Sections | Est. Lines |
|---|-------|-------------|----------|------------|
{docPlans.map((p, i) => `| ${i+1} | ${p.scope} | ${p.plan.file} | ${p.sections.join(", ")} | ~${p.plan.length} |`)}

### Source Information

{docPlans.map(p => `
**${p.scope}:**
- Target: \`${p.plan.file}\`
- Will extract from: ${p.plan.sources.join(", ")}
- Style: ${p.plan.style}
`)}

### Documentation Principles Applied

All generated docs will:
- Skip obvious information
- Use examples over explanations
- Be scannable (headers, bullets, tables)
- Include troubleshooting sections
- Have copy-pasteable commands
```

### User Decision

```javascript
AskUserQuestion([{
  question: "Generate these documents?",
  header: "Plan",
  options: [
    { label: "Generate All (Recommended)", description: `Create all ${docPlans.length} documents` },
    { label: "High Priority Only", description: "Only missing/critical docs" },
    { label: "Abort", description: "Cancel, no changes" }
  ],
  multiSelect: false
}])

switch (planDecision) {
  case "Generate All":
    toGenerate = docPlans
    break
  case "High Priority Only":
    toGenerate = docPlans.filter(p => p.priority === "HIGH")
    break
  case "Abort":
    console.log("Aborted. No documentation generated.")
    return
}
```

---

## Step-4: Generate Documentation

```javascript
if (toGenerate.length === 0 || isReportOnly) {
  // Nothing to generate
  // → Skip to Step-5
}

// Generate docs via apply agent
generateResults = Task("cco-agent-apply", `
  scope: docs
  operations: ${JSON.stringify(toGenerate.map(p => ({
    action: "generate",
    scope: p.scope,
    file: p.plan.file,
    sections: p.sections,
    sources: p.plan.sources,
    projectType: projectType
  })))}

  ## Generation Rules [CRITICAL]

  For each document:

  1. **Extract from code:**
     - Read source files listed in 'sources'
     - Extract function signatures, endpoints, configs
     - Use actual code examples, not made-up ones

  2. **Apply principles:**
     - Brevity: Remove every unnecessary word
     - Examples: Show, don't explain
     - Scannable: Use headers, bullets, tables
     - Actionable: Focus on what to DO

  3. **Format:**
     - README: Description → Install → Quick Start → Usage → Contributing
     - API: Endpoints table → Auth → Request/Response → Errors
     - Dev: Prerequisites → Setup → Testing → Architecture
     - User: Getting Started → Features → Troubleshooting
     - Ops: Deploy → Config → Monitor → Troubleshoot
     - Changelog: Keep a Changelog format

  4. **Anti-patterns to avoid:**
     - "This document explains..." (just explain)
     - "As mentioned above..." (restructure instead)
     - Long paragraphs (use bullets)
     - Obvious statements ("README is a file...")
     - Version history in body (use CHANGELOG)

  Return: {
    generated: [{ scope, file, linesWritten }],
    failed: [{ scope, file, reason }],
    accounting: { done, fail, total }
  }
`, { model: "opus" })
```

---

## Step-5: Summary

### Calculate Results

```javascript
// Agent returns done/fail, translate to user-friendly applied/failed
const results = generateResults || { accounting: { done: 0, fail: 0, total: 0 } }
const applied = results.accounting.done
const failed = results.accounting.fail
```

### Interactive Mode Output

```markdown
## Documentation Complete

### Gap Summary
| Scope | Before | After | Status |
|-------|--------|-------|--------|
{config.scopes.map(scope => {
  const gap = gaps[scope]
  const generated = results.generated?.find(g => g.scope === scope)
  const before = gap.needed ? "Missing" : "OK"
  const after = generated ? "Created" : (gap.needed ? "Failed" : "OK")
  return `| ${scope} | ${before} | ${after} | ${generated ? "NEW" : "-"} |`
})}

### Files Generated
{results.generated?.map(g => `- \`${g.file}\` (~${g.linesWritten} lines)`).join('\n') || "No files generated"}

### Accounting
| Metric | Value |
|--------|-------|
| Generated | {applied} |
| Failed | {failed} |
| Total | {toGenerate?.length || 0} |

Status: {failed > 0 ? "WARN" : "OK"}

Run \`git diff\` to review generated documentation.
```

### Unattended Mode Output (--auto)

```
cco-docs: {OK|WARN|FAIL} | Generated: {applied} | Failed: {failed} | Scopes: {config.scopes.length}
```

---

## Reference

### Question Flow Summary

| Scenario | Questions | Total |
|----------|-----------|-------|
| --auto mode | 0 | 0 |
| --check mode | 0 | 0 |
| Interactive | Q1 (Scopes + Mode) | 1 |

### Output Schema (when called as sub-command)

```json
{
  "status": "OK|WARN|FAIL",
  "gaps": {
    "readme": { "needed": true, "sections": ["installation", "quick-start"] },
    "api": { "needed": false, "reason": "Complete" }
  },
  "generated": [
    { "scope": "readme", "file": "README.md", "linesWritten": 45 }
  ],
  "accounting": {
    "applied": 3,
    "failed": 0,
    "total": 3
  }
}
```

### Flags

| Flag | Effect |
|------|--------|
| `--auto` | Unattended mode: all areas, generate all missing |
| `--check` | Validation only, return gap status |
| `--preview` | Show gaps only, don't generate |
| `--force` | Regenerate even if docs exist |

### Scope Groups

| Group | Scopes Included | Files |
|-------|-----------------|-------|
| **Core** | readme + changelog | README.md, CHANGELOG.md |
| **Technical** | api + dev | API.md, CONTRIBUTING.md, docs/api/, docs/dev/ |
| **User-facing** | user + ops | docs/user/, DEPLOY.md, docs/ops/ |

### Ideal Documentation by Project Type

| Type | README | API | Dev | User | Ops | Changelog |
|------|--------|-----|-----|------|-----|-----------|
| CLI | Full | - | Basic | Full | - | Yes |
| Library | Full | Full | Full | Guides | Publish | Yes |
| API | Full | Full | Full | Full | Full | Yes |
| Web | Full | Components | Full | Basic | Full | Yes |

### Documentation Templates

**README Structure:**
```markdown
# Project Name

One-line description.

## Install
\`\`\`bash
npm install package-name
\`\`\`

## Quick Start
\`\`\`javascript
import { thing } from 'package-name'
thing.do()
\`\`\`

## Usage
[Most common use cases with examples]

## API
[Brief overview, link to full docs]

## Contributing
[Link to CONTRIBUTING.md]

## License
MIT
```

**API Endpoint Structure:**
```markdown
## POST /api/users

Create a new user.

**Request:**
\`\`\`json
{ "email": "user@example.com", "name": "User" }
\`\`\`

**Response:** `201 Created`
\`\`\`json
{ "id": "123", "email": "user@example.com" }
\`\`\`

**Errors:**
- `400` - Invalid email format
- `409` - Email already exists
```

---

## Recovery

| Situation | Recovery |
|-----------|----------|
| Generated doc is wrong | `git checkout -- {file}` |
| Want to review first | Use `--report` flag |
| Update existing | Use `--force` flag |

---

## Empty Profile Handling

When profile is minimal or empty (new project):

1. **Infer from code:**
   - `package.json` → Node.js project type, name, version
   - `pyproject.toml` → Python project type
   - Source files → languages, frameworks

2. **Infer from existing docs:**
   - README sections → documentation style
   - Existing API docs → format preferences

3. **Use sensible defaults:**
   - Project type: API (most common)
   - Style: Concise, scannable
   - Format: CommonMark

4. **Generate minimal but complete:**
   - README with placeholders for unknowns
   - Mark sections needing human review with `<!-- TODO: ... -->`

---

## Accounting

**Invariant:** `applied + failed = total` (count documents, not sections)

**No "declined" category:** AI has no option to decline. Generate or fail with technical reason.

| Status | Meaning |
|--------|---------|
| `applied` | Document successfully generated |
| `failed` | Technical impossibility (must include reason) |

**Valid fail reasons:**
- `Technical: No source files found for extraction`
- `Technical: Project type could not be determined`
- `Technical: File write permission denied`

---

## Rules

1. **Gap-first** - Analyze what's missing before generating
2. **Code-driven** - Extract docs from actual code, not imagination
3. **Concise always** - Every word must earn its place
4. **Human-readable** - 8th grade reading level
5. **Scannable** - Headers, bullets, tables for quick parsing
6. **Copy-pasteable** - Commands should work when pasted
7. **No filler** - Skip "This document explains..."
8. **Examples > prose** - Show, don't tell
9. **Accounting invariant** - applied + failed = total always holds
