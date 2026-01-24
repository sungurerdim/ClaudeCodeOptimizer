---
description: Configure project-specific CCO rules
argument-hint: [--auto]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, AskUserQuestion
---

# /config

**Project Setup** - Detects stack, copies relevant rules to `.claude/rules/` for auto-context.

## Overview

Creates `.claude/` folder structure with:
- `context.md` - Project metadata and stack summary
- `rules/` - Copied rule files with `cco-` prefix (auto-loaded by Claude Code)

**No @import, no PLUGIN_ROOT, no hallucination risk.**

## Args

- `--auto`: Unattended mode - no questions, uses detected defaults
- `--reset`: Remove existing CCO rules (`cco-*.md`) and start fresh

## How It Works

```
1. Detect project stack (language, frameworks, tools)
2. Copy PROJECT-SPECIFIC rules to LOCAL ./.claude/rules/ (cco-*.md files)
3. Create context.md with project metadata
4. Done - Claude Code auto-loads project rules

Note: Core rules are automatically injected into context on every session
start via SessionStart hook (no file copying, direct context injection).
```

## Auto-Context Mechanism

**CRITICAL: Claude Code automatically loads:**
- `~/.claude/rules/*.md` (global/user level) - CCO core rules here
- `./.claude/rules/**/*.md` (project level) - project-specific rules here

**All CCO rules use `cco-` prefix** for safe identification and updates.

This means:
- NO @import syntax needed
- NO environment variables needed
- Core rules auto-installed globally via SessionStart hook
- Project rules portable with the repo
- User's own rules (without `cco-` prefix) never touched

## Rules Distribution

| Rule Type | Location | Prefix | Installed By |
|-----------|----------|--------|--------------|
| Core (foundation, safety, workflow) | Context (injected) | `cco-` | SessionStart hook |
| Languages (python, typescript, etc.) | `./.claude/rules/languages/` | `cco-` | `/config` |
| Frameworks (backend, api, etc.) | `./.claude/rules/frameworks/` | `cco-` | `/config` |
| Operations (database, cicd, etc.) | `./.claude/rules/operations/` | `cco-` | `/config` |

---

## Trigger Definitions

| Detection | Rule File | Triggers |
|-----------|-----------|----------|
| **Languages** | | |
| Python | `cco-python.md` | `pyproject.toml`, `requirements.txt`, `*.py` |
| TypeScript | `cco-typescript.md` | `tsconfig.json`, `*.ts`, `*.tsx` |
| Go | `cco-go.md` | `go.mod`, `*.go` |
| Rust | `cco-rust.md` | `Cargo.toml`, `*.rs` |
| Java | `cco-java.md` | `pom.xml`, `build.gradle`, `*.java` |
| Ruby | `cco-ruby.md` | `Gemfile`, `*.rb` |
| PHP | `cco-php.md` | `composer.json`, `*.php` |
| C# | `cco-csharp.md` | `*.csproj`, `*.cs` |
| Swift | `cco-swift.md` | `Package.swift`, `*.swift` |
| Kotlin | `cco-kotlin.md` | `build.gradle.kts`, `*.kt` |
| **Domains** | | |
| API | `cco-api.md` | `routes/`, `@app.get`, `@router` |
| Database | `cco-database.md` | `sqlalchemy`, `prisma`, `migrations/` |
| Testing | `cco-testing.md` | `pytest`, `jest`, `vitest`, `tests/` |
| Frontend | `cco-frontend.md` | `react`, `vue`, `svelte` in deps |
| Backend | `cco-backend.md` | `fastapi`, `django`, `express` in deps |
| Infrastructure | `cco-infrastructure.md` | `Dockerfile`, `docker-compose.yml` |
| CI/CD | `cco-cicd.md` | `.github/workflows/`, `.gitlab-ci.yml` |
| Security | `cco-security.md` | PII/Regulated data selected |
| Mobile | `cco-mobile.md` | `flutter`, `react-native` in deps |
| ML | `cco-ml.md` | `torch`, `tensorflow`, `langchain` in deps |

---

## Step 1: Detection

Run stack detection using parallel file checks:

```javascript
// Detect languages
const langDetections = {
  python: await fileExists(['pyproject.toml', 'requirements.txt', 'setup.py']),
  typescript: await fileExists(['tsconfig.json']) || await hasFiles('*.ts'),
  go: await fileExists(['go.mod']),
  rust: await fileExists(['Cargo.toml']),
  java: await fileExists(['pom.xml', 'build.gradle']),
  ruby: await fileExists(['Gemfile']),
  php: await fileExists(['composer.json']),
  csharp: await hasFiles('*.csproj'),
  swift: await fileExists(['Package.swift']),
  kotlin: await fileExists(['build.gradle.kts'])
}

// Detect frameworks from manifest dependencies
const manifest = await readManifest()  // package.json, pyproject.toml, etc.
const frameworkDetections = {
  api: manifest.hasDep(['fastapi', 'flask', 'express', 'django']),
  database: manifest.hasDep(['sqlalchemy', 'prisma', '@prisma/client', 'typeorm']),
  testing: manifest.hasDep(['pytest', 'jest', 'vitest', 'mocha']),
  frontend: manifest.hasDep(['react', 'vue', 'svelte', 'angular']),
  backend: manifest.hasDep(['fastapi', 'django', 'express', 'nestjs']),
  ml: manifest.hasDep(['torch', 'tensorflow', 'langchain', 'transformers'])
}

// Detect infrastructure
const infraDetections = {
  docker: await fileExists(['Dockerfile', 'docker-compose.yml']),
  cicd: await fileExists(['.github/workflows', '.gitlab-ci.yml']),
  k8s: await fileExists(['k8s/', 'kubernetes/'])
}

// Build matched rules list (with cco- prefix)
const matchedRules = []
for (const [lang, detected] of Object.entries(langDetections)) {
  if (detected) matchedRules.push({ name: `cco-${lang}.md`, category: 'languages' })
}
for (const [domain, detected] of Object.entries({...frameworkDetections, ...infraDetections})) {
  if (detected) {
    const category = ['api', 'database', 'testing', 'frontend', 'backend', 'ml'].includes(domain)
      ? 'frameworks' : 'operations'
    matchedRules.push({ name: `cco-${domain}.md`, category })
  }
}

// Extract project info from README or manifest
const projectInfo = {
  purpose: await extractPurpose(),  // From README.md first paragraph
  stack: Object.keys(langDetections).filter(k => langDetections[k]).join(', ')
}
```

---

## Step 2: Questions (Skip if --auto)

```javascript
if (!args.includes('--auto')) {
  const answers = await AskUserQuestion([
    {
      question: "Most sensitive data handled?",
      header: "Data",
      options: [
        { label: "Public", description: "No sensitive data" },
        { label: "PII", description: "Personal data - adds cco-security.md" },
        { label: "Regulated", description: "Healthcare/Finance - adds cco-security.md + cco-compliance.md" }
      ],
      multiSelect: false
    }
  ])

  if (answers.data === 'PII' || answers.data === 'Regulated') {
    matchedRules.push({ name: 'cco-security.md', category: 'operations' })
  }
  if (answers.data === 'Regulated') {
    matchedRules.push({ name: 'cco-compliance.md', category: 'operations' })
  }
}
```

---

## Step 3: Clean Existing CCO Rules (if --reset)

```javascript
if (args.includes('--reset')) {
  // Only remove cco-*.md files, preserve user's own rules
  await Bash('find .claude/rules -name "cco-*.md" -delete 2>/dev/null || true')
  console.log('Removed existing CCO rules')
}
```

---

## Step 4: Create Project Rules Directory

```javascript
// LOCAL: Project-specific rules organized by category
await Bash('mkdir -p .claude/rules/languages')
await Bash('mkdir -p .claude/rules/frameworks')
await Bash('mkdir -p .claude/rules/operations')
```

---

## Step 5: Copy Project-Specific Rules

```javascript
// Find CCO plugin location
const pluginLocations = [
  // Windows
  process.env.APPDATA + '/claude/plugins/claude-code-optimizer',
  process.env.LOCALAPPDATA + '/claude/plugins/claude-code-optimizer',
  // macOS
  process.env.HOME + '/.claude/plugins/claude-code-optimizer',
  process.env.HOME + '/Library/Application Support/claude/plugins/claude-code-optimizer',
  // Linux
  process.env.HOME + '/.config/claude/plugins/claude-code-optimizer',
  process.env.HOME + '/.local/share/claude/plugins/claude-code-optimizer'
]

let ccoPath = null
for (const loc of pluginLocations) {
  if (await fileExists(loc + '/rules/languages/cco-python.md')) {
    ccoPath = loc
    break
  }
}

if (!ccoPath) {
  console.log('CCO plugin not found. Please ensure claude-code-optimizer is installed.')
  return
}

// ═══════════════════════════════════════════════════════════════
// PROJECT-SPECIFIC RULES (copied to ./.claude/rules/)
// Only cco-*.md files are touched, user rules preserved
// ═══════════════════════════════════════════════════════════════
console.log('Installing project-specific rules...')

for (const rule of matchedRules) {
  const src = `${ccoPath}/rules/${rule.category}/${rule.name}`
  const dest = `.claude/rules/${rule.category}/${rule.name}`
  await copyFile(src, dest)
}

console.log(`Installed ${matchedRules.length} project rules to ./.claude/rules/`)
```

---

## Step 6: Create context.md

```javascript
const contextContent = `# Project Context
*Auto-generated by CCO - edit as needed*

## Project Info
- **Purpose:** ${projectInfo.purpose}
- **Stack:** ${projectInfo.stack}
- **Data Sensitivity:** ${answers?.data || 'Public'}

## Detected Stack
${Object.entries(langDetections).filter(([k,v]) => v).map(([k]) => `- ${k}`).join('\n')}

## Active Rules
${matchedRules.map(r => `- ${r.name}`).join('\n')}

## Operational Commands
*Fill in your project's commands:*

- **Format:** \`ruff format .\` or \`prettier --write .\`
- **Lint:** \`ruff check .\` or \`eslint .\`
- **Type Check:** \`mypy .\` or \`tsc --noEmit\`
- **Test:** \`pytest\` or \`npm test\`
`

await Write('.claude/context.md', contextContent)
```

---

## Result

After `/config` completes:

```
# CORE (injected via SessionStart hook - no files created)
→ cco-foundation.md content injected into context
→ cco-safety.md content injected into context
→ cco-workflow.md content injected into context

# LOCAL (installed via /cco:config, project-specific)
project/.claude/
├── context.md           # Project metadata
└── rules/
    ├── languages/
    │   └── cco-python.md    # (detected)
    ├── frameworks/
    │   ├── cco-backend.md   # (detected)
    │   └── cco-api.md       # (detected)
    └── operations/
        ├── cco-database.md  # (detected)
        └── cco-cicd.md      # (detected)
```

**Context loading:**
- Core rules: Injected directly via SessionStart hook (no file copying)
- Project rules: Auto-loaded from `./.claude/rules/**/*.md`

**Safe updates:** Only `cco-*.md` files are managed. User's own rules without the prefix are never touched.

---

## Summary

| Step | Action |
|------|--------|
| 1 | Detect stack (parallel file checks) |
| 2 | Ask data sensitivity (skip if --auto) |
| 3 | Clean existing CCO rules (if --reset) |
| 4 | Create .claude/rules/ folder structure |
| 5 | Copy project-specific rules from CCO plugin |
| 6 | Create context.md with project metadata |

**Result:**
- Core rules injected into context via SessionStart hook (no files)
- Project rules in `./.claude/rules/` (local, portable)
- All CCO rules prefixed with `cco-` for safe identification
- Zero @import, zero hallucination risk
