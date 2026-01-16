---
description: Configure project-specific CCO rules
argument-hint: [--auto]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, AskUserQuestion
---

# /config

**Project Setup** - Detects stack, creates `.claude/cco.md` with adaptive rules.

## Overview

Creates a single `.claude/cco.md` file with @imports to plugin rules. No file copying, no extra folders.

## Args

- `--auto`: Unattended mode - no questions, uses detected defaults

## What It Does

```
1. Detect project stack (language, frameworks, tools)
2. Create .claude/cco.md with:
   - Project context (inline)
   - Global rules (@imports)
   - Adaptive rules (@imports based on detection)
3. Inject @.claude/cco.md into CLAUDE.md
```

## Plugin Path

```javascript
// Available in slash command context
const PLUGIN_ROOT = process.env.CLAUDE_PLUGIN_ROOT
// Rules at: ${PLUGIN_ROOT}/rules/*.md
```

---

## Trigger Definitions

**Maps detections → rule files in plugin.**

| Detection | Rule File | Triggers |
|-----------|-----------|----------|
| **Languages** | | |
| Python | `python.md` | `pyproject.toml`, `requirements.txt`, `*.py` |
| TypeScript | `typescript.md` | `tsconfig.json`, `*.ts`, `*.tsx` |
| JavaScript | `javascript.md` | `package.json` (no tsconfig), `*.js` |
| Go | `go.md` | `go.mod`, `*.go` |
| Rust | `rust.md` | `Cargo.toml`, `*.rs` |
| Java | `java.md` | `pom.xml`, `build.gradle`, `*.java` |
| Ruby | `ruby.md` | `Gemfile`, `*.rb` |
| PHP | `php.md` | `composer.json`, `*.php` |
| C# | `csharp.md` | `*.csproj`, `*.cs` |
| Swift | `swift.md` | `Package.swift`, `*.swift` |
| Kotlin | `kotlin.md` | `build.gradle.kts`, `*.kt` |
| **Domains** | | |
| API | `api.md` | `routes/`, `@app.get`, `@router` |
| Database | `database.md` | `sqlalchemy`, `prisma`, `migrations/` |
| Testing | `testing.md` | `pytest`, `jest`, `vitest`, `tests/` |
| Frontend | `frontend.md` | `react`, `vue`, `svelte` in deps |
| Backend | `backend.md` | `fastapi`, `django`, `express` in deps |
| Infrastructure | `infrastructure.md` | `Dockerfile`, `docker-compose.yml` |
| CI/CD | `cicd.md` | `.github/workflows/`, `.gitlab-ci.yml` |
| Security | `security.md` | PII/Regulated data selected |
| Mobile | `mobile.md` | `flutter`, `react-native` in deps |
| ML | `ml.md` | `torch`, `tensorflow`, `langchain` in deps |

---

## Step 1: Detection

```javascript
// Run detection in background
detectTask = Task("cco-agent-analyze", `
  scopes: ["config"]

  Detect from manifest files using PARALLEL Glob/Read:
  - Language: pyproject.toml, package.json, go.mod, Cargo.toml...
  - Frameworks: Check dependencies in manifests
  - Tools: Check for config files (tsconfig, ruff.toml, etc.)
  - Infra: Dockerfile, .github/workflows/, k8s/

  Return:
  {
    detections: {
      languages: ["python"],
      frameworks: ["fastapi", "sqlalchemy"],
      tools: ["pytest", "ruff", "mypy"],
      infra: ["docker", "github-actions"]
    },
    matchedRules: ["python.md", "backend.md", "api.md", "database.md", "testing.md", "cicd.md"],
    projectInfo: {
      purpose: "...",  // From README.md or manifest description
      stack: "Python, FastAPI, PostgreSQL"
    }
  }
`, { model: "haiku", run_in_background: true })
```

---

## Step 2: Questions (Skip if --auto)

```javascript
if (!isAuto) {
  AskUserQuestion([
    {
      question: "Most sensitive data handled?",
      header: "Data",
      options: [
        { label: "Public", description: "No sensitive data" },
        { label: "PII", description: "Personal data - adds security.md" },
        { label: "Regulated", description: "Healthcare/Finance - adds security.md + compliance.md" }
      ]
    }
  ])
}
```

---

## Step 3: Create cco.md

**Marker Format Rules:**
- Marker START/END flush with content (no blank lines between)
- Each @import on separate line
- One blank line between sections

```javascript
// Get detection results
const detectResult = await TaskOutput(detectTask.id)
const PLUGIN_ROOT = process.env.CLAUDE_PLUGIN_ROOT

// Build rule @imports (each on separate line)
const globalRules = [
  `@${PLUGIN_ROOT}/rules/core.md`,
  `@${PLUGIN_ROOT}/rules/ai.md`
].join('\n')

const adaptiveRules = detectResult.matchedRules
  .map(rule => `@${PLUGIN_ROOT}/rules/${rule}`)
  .join('\n')

// Build context (line by line)
const context = [
  `Purpose: ${detectResult.projectInfo.purpose}`,
  `Stack: ${detectResult.projectInfo.stack}`,
  `Data: ${userAnswers.data || 'Public'}`
].join('\n')

// Create cco.md - EXACT FORMAT
const ccoMd = `# CCO Rules

## Project Context
<!-- CCO:CONTEXT:START -->
${context}
<!-- CCO:CONTEXT:END -->

## Global Rules
<!-- CCO:GLOBAL:START -->
${globalRules}
<!-- CCO:GLOBAL:END -->

## Adaptive Rules
<!-- CCO:ADAPTIVE:START -->
${adaptiveRules}
<!-- CCO:ADAPTIVE:END -->
`

Write(".claude/cco.md", ccoMd)
```

---

## Step 4: Inject into CLAUDE.md

```javascript
const claudeMdPath = "CLAUDE.md"  // Project root
const injection = "@.claude/cco.md"

if (fileExists(claudeMdPath)) {
  const content = Read(claudeMdPath)
  if (!content.includes(injection)) {
    Edit(claudeMdPath, {
      append: `\n\n${injection}`
    })
  }
} else {
  Write(claudeMdPath, `# Project Instructions\n\n${injection}`)
}
```

---

## Example Output

**.claude/cco.md:** (marker-content flush, one blank line between sections)
```markdown
# CCO Rules

## Project Context
<!-- CCO:CONTEXT:START -->
Purpose: User management API service
Stack: Python, FastAPI, PostgreSQL
Data: PII
<!-- CCO:CONTEXT:END -->

## Global Rules
<!-- CCO:GLOBAL:START -->
@/home/user/.cache/claude-plugins/cco-abc123/rules/core.md
@/home/user/.cache/claude-plugins/cco-abc123/rules/ai.md
<!-- CCO:GLOBAL:END -->

## Adaptive Rules
<!-- CCO:ADAPTIVE:START -->
@/home/user/.cache/claude-plugins/cco-abc123/rules/python.md
@/home/user/.cache/claude-plugins/cco-abc123/rules/backend.md
@/home/user/.cache/claude-plugins/cco-abc123/rules/api.md
@/home/user/.cache/claude-plugins/cco-abc123/rules/database.md
@/home/user/.cache/claude-plugins/cco-abc123/rules/security.md
<!-- CCO:ADAPTIVE:END -->
```

**CLAUDE.md:**
```markdown
# Project Instructions

[User's existing content...]

@.claude/cco.md
```

---

## Marker Operations

### Update Existing cco.md

If `.claude/cco.md` exists, update only the specified marker:

```javascript
function updateMarker(content, markerName, newContent) {
  // Regex: START tag, any content, END tag
  // newContent flush with markers (no blank lines)
  const regex = new RegExp(
    `<!-- CCO:${markerName}:START -->[\\s\\S]*?<!-- CCO:${markerName}:END -->`,
    'g'
  )
  return content.replace(
    regex,
    `<!-- CCO:${markerName}:START -->\n${newContent}\n<!-- CCO:${markerName}:END -->`
  )
}

// Usage:
content = updateMarker(content, 'CONTEXT', newContext)
content = updateMarker(content, 'GLOBAL', newGlobal)
content = updateMarker(content, 'ADAPTIVE', newAdaptive)
```

### Clear Marker Content

```javascript
function clearMarker(content, markerName) {
  const regex = new RegExp(
    `<!-- CCO:${markerName}:START -->[\\s\\S]*?<!-- CCO:${markerName}:END -->`,
    'g'
  )
  return content.replace(
    regex,
    `<!-- CCO:${markerName}:START -->\n<!-- CCO:${markerName}:END -->`
  )
}
```

### Check If Marker Exists

```javascript
function hasMarker(content, markerName) {
  return content.includes(`<!-- CCO:${markerName}:START -->`)
}
```

### Get Marker Content

```javascript
function getMarkerContent(content, markerName) {
  const regex = new RegExp(
    `<!-- CCO:${markerName}:START -->\\n([\\s\\S]*?)\\n<!-- CCO:${markerName}:END -->`,
    ''
  )
  const match = content.match(regex)
  return match ? match[1] : null
}
```

---

## Remove

```javascript
// Delete cco.md and remove injection from CLAUDE.md
Bash("rm -f .claude/cco.md")

const claudeMd = Read("CLAUDE.md")
const cleaned = claudeMd.replace(/\n*@\.claude\/cco\.md\n*/g, '\n')
Write("CLAUDE.md", cleaned)
```

---

## Summary

| Step | Action |
|------|--------|
| 1 | Detect stack (parallel Glob/Read) |
| 2 | Ask data sensitivity (skip if --auto) |
| 3 | Create/update `.claude/cco.md` with 3 markers |
| 4 | Inject `@.claude/cco.md` into CLAUDE.md |

**Result:** Single file, no copies, direct @import to plugin rules.
