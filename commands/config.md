---
description: Configure project-specific CCO rules
argument-hint: [--auto]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, AskUserQuestion
---

# /config

**Project Setup** - Detects stack, asks questions, creates YAML context and copies rules.

## Overview

Creates flat `.claude/rules/` structure with:
- `cco-context.md` - YAML frontmatter with project metadata (auto-loaded)
- `cco-*.md` - Rule files (auto-loaded by Claude Code)

**Single flat directory. No subdirectories. No complexity.**

## Args

- `--auto`: Unattended mode - no questions, uses detected defaults
- `--reset`: Remove existing CCO files (`cco-*.md`) and start fresh

## How It Works

```
1. Detect project stack (languages, frameworks, tools, commands)
2. Ask 2 question groups (skip if --auto)
3. Show auto-detect results for confirmation
4. Create cco-context.md with YAML frontmatter
5. Copy relevant cco-*.md rule files
6. Done - Claude Code auto-loads everything from .claude/rules/
```

## File Structure

```
project/.claude/rules/
├── cco-context.md        # YAML frontmatter - project metadata
├── cco-{language}.md     # Language rules (detected)
├── cco-{framework}.md    # Framework rules (detected)
├── cco-{operation}.md    # Operations rules (detected)
└── user-custom.md        # User's own rules (never touched)
```

**All CCO files use `cco-` prefix** - user files without prefix are never modified.

---

## Step 1: Auto-Detection

Run parallel detection for all auto-detectable fields:

```javascript
// ═══════════════════════════════════════════════════════════════
// LANGUAGES - File extension and manifest detection
// ═══════════════════════════════════════════════════════════════
const languages = []
if (await fileExists(['tsconfig.json']) || await hasFiles('**/*.ts')) languages.push('typescript')
if (await fileExists(['pyproject.toml', 'requirements.txt', 'setup.py'])) languages.push('python')
if (await fileExists(['go.mod'])) languages.push('go')
if (await fileExists(['Cargo.toml'])) languages.push('rust')
if (await fileExists(['pom.xml', 'build.gradle'])) languages.push('java')
if (await fileExists(['Gemfile'])) languages.push('ruby')
if (await fileExists(['composer.json'])) languages.push('php')
if (await hasFiles('**/*.csproj')) languages.push('csharp')
if (await fileExists(['Package.swift'])) languages.push('swift')
if (await fileExists(['build.gradle.kts']) || await hasFiles('**/*.kt')) languages.push('kotlin')

// ═══════════════════════════════════════════════════════════════
// FRAMEWORKS - Dependency analysis
// ═══════════════════════════════════════════════════════════════
const manifest = await readManifest()  // package.json, pyproject.toml, etc.
const frameworks = []
if (manifest.hasDep(['fastapi', 'flask', 'express', 'django', 'nestjs', 'hono'])) frameworks.push('backend')
if (manifest.hasDep(['fastapi', 'flask', 'express', 'hono']) || await hasFiles('**/routes/**')) frameworks.push('api')
if (manifest.hasDep(['react', 'vue', 'svelte', 'angular', 'solid'])) frameworks.push('frontend')
if (manifest.hasDep(['pytest', 'jest', 'vitest', 'mocha', 'playwright'])) frameworks.push('testing')
if (manifest.hasDep(['sqlalchemy', 'prisma', '@prisma/client', 'typeorm', 'drizzle'])) frameworks.push('orm')
if (manifest.hasDep(['torch', 'tensorflow', 'langchain', 'transformers', 'openai'])) frameworks.push('ml')
if (manifest.hasDep(['react-native', 'flutter', 'expo'])) frameworks.push('mobile')
if (manifest.hasDep(['socket.io', 'ws', 'pusher'])) frameworks.push('realtime')

// ═══════════════════════════════════════════════════════════════
// OPERATIONS - Infrastructure detection
// ═══════════════════════════════════════════════════════════════
const operations = []
if (await fileExists(['Dockerfile', 'docker-compose.yml', 'docker-compose.yaml'])) operations.push('infrastructure')
if (await fileExists(['.github/workflows', '.gitlab-ci.yml', 'Jenkinsfile'])) operations.push('cicd')
if (await fileExists(['k8s/', 'kubernetes/', 'helm/'])) operations.push('deployment')
if (manifest.hasDep(['pg', 'mysql2', 'mongodb', 'redis', '@prisma/client'])) operations.push('database')
if (await fileExists(['.env.example', 'vault.yml']) || await grepFiles('process.env', '**/*.ts')) operations.push('security')

// ═══════════════════════════════════════════════════════════════
// PROJECT INFO - README and manifest analysis
// ═══════════════════════════════════════════════════════════════
const purpose = await extractFirstParagraph('README.md') || 'No description found'

// ═══════════════════════════════════════════════════════════════
// PROJECT TYPE - Heuristic detection
// ═══════════════════════════════════════════════════════════════
const detectedTypes = []
if (manifest.bin || await fileExists(['src/cli.ts', 'src/cli.py', 'cmd/'])) detectedTypes.push('cli')
if (frameworks.includes('api') || await hasFiles('**/routes/**')) detectedTypes.push('api')
if (frameworks.includes('frontend')) detectedTypes.push('web')
if (manifest.main && !manifest.bin) detectedTypes.push('library')
if (frameworks.includes('mobile')) detectedTypes.push('mobile')
if (await fileExists(['electron.config.js', 'tauri.conf.json'])) detectedTypes.push('desktop')

// ═══════════════════════════════════════════════════════════════
// COMMANDS - Config file detection
// ═══════════════════════════════════════════════════════════════
const commands = {
  format: null,
  lint: null,
  typecheck: null,
  test: null,
  build: null,
  dev: null
}

// Detect from package.json scripts
if (manifest.scripts) {
  commands.format = manifest.scripts.format || (await fileExists(['.prettierrc', 'prettier.config.js']) ? 'prettier --write .' : null)
  commands.lint = manifest.scripts.lint || (await fileExists(['eslint.config.js', '.eslintrc']) ? 'eslint .' : null)
  commands.typecheck = manifest.scripts.typecheck || manifest.scripts['type-check'] || (languages.includes('typescript') ? 'tsc --noEmit' : null)
  commands.test = manifest.scripts.test
  commands.build = manifest.scripts.build
  commands.dev = manifest.scripts.dev || manifest.scripts.start
}

// Python detection
if (languages.includes('python')) {
  if (await fileExists(['ruff.toml', 'pyproject.toml'])) {
    commands.format = commands.format || 'ruff format .'
    commands.lint = commands.lint || 'ruff check .'
  }
  commands.typecheck = commands.typecheck || (await fileExists(['mypy.ini', 'pyproject.toml']) ? 'mypy .' : null)
  commands.test = commands.test || (await fileExists(['pytest.ini', 'pyproject.toml']) ? 'pytest' : null)
}

// Go detection
if (languages.includes('go')) {
  commands.format = commands.format || 'go fmt ./...'
  commands.lint = commands.lint || (await fileExists(['.golangci.yml']) ? 'golangci-lint run' : 'go vet ./...')
  commands.test = commands.test || 'go test ./...'
  commands.build = commands.build || 'go build ./...'
}

// ═══════════════════════════════════════════════════════════════
// OTHER AUTO-DETECTIONS
// ═══════════════════════════════════════════════════════════════
const detected = {
  structure: await fileExists(['pnpm-workspace.yaml', 'lerna.json', 'packages/']) ? 'monorepo' : 'single',
  hooks: await fileExists(['.husky/', '.pre-commit-config.yaml']) ?
    (await fileExists(['.husky/']) ? ['husky'] : ['pre-commit']) : [],
  license: await detectLicense('LICENSE'),  // MIT, Apache-2.0, etc.
  ci: await fileExists(['.github/workflows/']) ? 'github-actions' :
      await fileExists(['.gitlab-ci.yml']) ? 'gitlab-ci' : null,
  coverage: await fileExists(['coverage/', '.nyc_output/', 'htmlcov/'])
}

// Conventions detection
let conventions = null
if (await fileExists(['commitlint.config.js', '.commitlintrc'])) conventions = 'conventional'
else if (await grepFiles('gitmoji', '.git/COMMIT_EDITMSG')) conventions = 'gitmoji'

// Release detection
let release = null
if (await fileExists(['.releaserc', 'release.config.js'])) release = 'semantic'
else if (await fileExists(['CHANGELOG.md']) && await grepFiles(/\d{4}\.\d{2}/, 'CHANGELOG.md')) release = 'calver'

// Database detection
let database = null
if (await fileExists(['prisma/schema.prisma'])) {
  const schema = await Read('prisma/schema.prisma')
  if (schema.includes('postgresql')) database = 'postgresql'
  else if (schema.includes('mysql')) database = 'mysql'
  else if (schema.includes('sqlite')) database = 'sqlite'
  else if (schema.includes('mongodb')) database = 'mongodb'
}
```

---

## Step 2: Questions (Skip if --auto)

### Question Group 1: Project Profile

```javascript
if (!args.includes('--auto')) {
  const profile = await AskUserQuestion({
    questions: [
      {
        question: "Bu proje ne tür bir uygulama?",
        header: "Type",
        multiSelect: true,
        options: [
          { label: "CLI", description: "Komut satırı aracı" },
          { label: "API", description: "Backend servis" },
          { label: "Web", description: "Frontend uygulama" },
          { label: "Library", description: "Yeniden kullanılabilir paket" }
        ]
      },
      {
        question: "Ekip büyüklüğü?",
        header: "Team",
        multiSelect: false,
        options: [
          { label: "Solo", description: "Tek geliştirici" },
          { label: "Small", description: "2-5 kişi" },
          { label: "Medium", description: "6-15 kişi" },
          { label: "Large", description: "15+ kişi" }
        ]
      },
      {
        question: "En hassas veri türü?",
        header: "Data",
        multiSelect: false,
        options: [
          { label: "Public", description: "Hassas veri yok" },
          { label: "Internal", description: "Şirket içi veriler" },
          { label: "PII", description: "Kişisel veriler" },
          { label: "Regulated", description: "Finans/Sağlık" }
        ]
      },
      {
        question: "Mimari yaklaşım?",
        header: "Arch",
        multiSelect: false,
        options: [
          { label: "Monolith", description: "Tek uygulama" },
          { label: "Modular", description: "Modüler monolith" },
          { label: "Micro", description: "Microservices" },
          { label: "Serverless", description: "FaaS tabanlı" }
        ]
      }
    ]
  })
```

### Question Group 2: Policies

```javascript
  const policies = await AskUserQuestion({
    questions: [
      {
        question: "Proje olgunluğu?",
        header: "Maturity",
        multiSelect: false,
        options: [
          { label: "Prototype", description: "Deneysel, hızlı değişim" },
          { label: "MVP", description: "İlk kullanıcılar var" },
          { label: "Stable", description: "Production, aktif geliştirme" },
          { label: "Mature", description: "Kararlı, az değişim" }
        ]
      },
      {
        question: "Breaking change politikası?",
        header: "Breaking",
        multiSelect: false,
        options: [
          { label: "Allowed", description: "Serbest, hızlı iterasyon" },
          { label: "Warn", description: "Deprecation süreci uygula" },
          { label: "Forbidden", description: "Kesinlikle yasak" },
          { label: "N/A", description: "Public API yok" }
        ]
      },
      {
        question: "Geliştirme önceliği?",
        header: "Priority",
        multiSelect: false,
        options: [
          { label: "Speed", description: "Hızlı ship öncelikli" },
          { label: "Balance", description: "Hız-kalite dengesi" },
          { label: "Quality", description: "Kalite her şeyden önce" },
          { label: "Context", description: "Scope'a göre değişir" }
        ]
      },
      {
        question: "Uyumluluk gereksinimleri?",
        header: "Compliance",
        multiSelect: true,
        options: [
          { label: "None", description: "Özel gereksinim yok" },
          { label: "GDPR", description: "AB veri koruma" },
          { label: "HIPAA", description: "Sağlık verileri" },
          { label: "SOC2", description: "Güvenlik sertifikası" }
        ]
      }
    ]
  })
}
```

---

## Step 3: Show Detection Summary

```javascript
console.log(`
═══════════════════════════════════════════════════════════════
 CCO Auto-Detection Results
═══════════════════════════════════════════════════════════════

 Languages:   ${languages.join(', ') || 'None detected'}
 Frameworks:  ${frameworks.join(', ') || 'None detected'}
 Operations:  ${operations.join(', ') || 'None detected'}

 Commands:
   format:    ${commands.format || '(not detected)'}
   lint:      ${commands.lint || '(not detected)'}
   typecheck: ${commands.typecheck || '(not detected)'}
   test:      ${commands.test || '(not detected)'}
   build:     ${commands.build || '(not detected)'}

 Other:
   Structure:   ${detected.structure}
   Database:    ${database || 'None detected'}
   CI:          ${detected.ci || 'None detected'}
   Conventions: ${conventions || 'Not detected'}
   Release:     ${release || 'Not detected'}

═══════════════════════════════════════════════════════════════
`)
```

---

## Step 4: Clean Existing (if --reset)

```javascript
if (args.includes('--reset')) {
  // Remove all cco-*.md files, preserve user's own rules
  const ccoFiles = await Glob('.claude/rules/cco-*.md')
  for (const file of ccoFiles) {
    await Bash(`rm "${file}"`)
  }
  console.log(`Removed ${ccoFiles.length} existing CCO files`)
}
```

---

## Step 5: Create Directory

```javascript
await Bash('mkdir -p .claude/rules')
```

---

## Step 6: Generate cco-context.md (YAML Frontmatter)

```javascript
// Merge detected + user answers
const type = profile?.Type || detectedTypes
const team = profile?.Team?.toLowerCase() || 'solo'
const data = profile?.Data?.toLowerCase() || 'public'
const architecture = profile?.Arch?.toLowerCase() || 'monolith'
const maturity = policies?.Maturity?.toLowerCase() || 'stable'
const breaking = policies?.Breaking?.toLowerCase() || 'warn'
const priority = policies?.Priority?.toLowerCase() || 'balance'
const compliance = policies?.Compliance || ['none']

// Generate guidelines based on maturity/breaking/priority
const guidelines = generateGuidelines(maturity, breaking, priority)

// Build YAML content
const contextYaml = `---
cco: true

# ═══════════════════════════════════════════════════════════════
# PROJECT
# ═══════════════════════════════════════════════════════════════
project:
  purpose: "${purpose.replace(/"/g, '\\"')}"
  type: [${type.map(t => t.toLowerCase()).join(', ')}]

# ═══════════════════════════════════════════════════════════════
# CONTEXT
# ═══════════════════════════════════════════════════════════════
context:
  team: ${team}
  data: ${data}
  compliance: [${compliance.map(c => c.toLowerCase()).join(', ')}]

# ═══════════════════════════════════════════════════════════════
# STACK
# ═══════════════════════════════════════════════════════════════
stack:
  languages: [${languages.join(', ')}]
  frameworks: [${frameworks.join(', ')}]
  database: ${database || 'null'}

# ═══════════════════════════════════════════════════════════════
# ARCHITECTURE
# ═══════════════════════════════════════════════════════════════
architecture:
  style: ${architecture}
  deployment: ${detected.ci ? 'container' : 'manual'}

# ═══════════════════════════════════════════════════════════════
# MATURITY
# ═══════════════════════════════════════════════════════════════
maturity:
  level: ${maturity}
  breaking: ${breaking}
  priority: ${priority}

# ═══════════════════════════════════════════════════════════════
# GUIDELINES (auto-generated from maturity settings)
# ═══════════════════════════════════════════════════════════════
guidelines:
${guidelines.map(g => `  - "${g}"`).join('\n')}

# ═══════════════════════════════════════════════════════════════
# COMMANDS
# ═══════════════════════════════════════════════════════════════
commands:
  format: ${commands.format ? `"${commands.format}"` : 'null'}
  lint: ${commands.lint ? `"${commands.lint}"` : 'null'}
  typecheck: ${commands.typecheck ? `"${commands.typecheck}"` : 'null'}
  test: ${commands.test ? `"${commands.test}"` : 'null'}
  build: ${commands.build ? `"${commands.build}"` : 'null'}
  dev: ${commands.dev ? `"${commands.dev}"` : 'null'}

conventions: ${conventions || 'null'}
release: ${release || 'null'}

# ═══════════════════════════════════════════════════════════════
# DETECTED (read-only, for reference)
# ═══════════════════════════════════════════════════════════════
detected:
  structure: ${detected.structure}
  hooks: [${detected.hooks.join(', ')}]
  license: ${detected.license || 'null'}
  ci: ${detected.ci || 'null'}

# ═══════════════════════════════════════════════════════════════
# ACTIVE RULES (auto-managed by CCO)
# ═══════════════════════════════════════════════════════════════
rules:
${matchedRules.map(r => `  - ${r}`).join('\n')}
---
`

await Write('.claude/rules/cco-context.md', contextYaml)
```

### Guidelines Generator

```javascript
function generateGuidelines(maturity, breaking, priority) {
  const guidelines = []

  // Maturity-based guidelines
  switch (maturity) {
    case 'prototype':
      guidelines.push('Hız öncelikli, teknik borç kabul edilebilir')
      guidelines.push('Kapsamlı test gereksiz, happy path yeterli')
      break
    case 'mvp':
      guidelines.push('Temel hata yönetimi gerekli')
      guidelines.push('Kritik yollar test edilmeli')
      break
    case 'stable':
      guidelines.push('Kod kalitesi ve test coverage önemli')
      guidelines.push('Refactoring için zaman ayrılmalı')
      break
    case 'mature':
      guidelines.push('Değişiklikler dikkatli planlanmalı')
      guidelines.push('Backward compatibility kritik')
      break
  }

  // Breaking change guidelines
  switch (breaking) {
    case 'allowed':
      guidelines.push('Breaking change serbestçe yapılabilir')
      break
    case 'warn':
      guidelines.push('Breaking change için deprecation süreci uygulanmalı')
      break
    case 'forbidden':
      guidelines.push('Breaking change kesinlikle yasak')
      break
  }

  // Priority guidelines
  switch (priority) {
    case 'speed':
      guidelines.push('Hızlı teslimat öncelikli')
      break
    case 'balance':
      guidelines.push('Hız ve kalite dengeli tutulmalı')
      break
    case 'quality':
      guidelines.push('Kalite her şeyden önce gelir')
      break
  }

  return guidelines
}
```

---

## Step 7: Copy Rule Files

```javascript
// Build rules list based on detections
const matchedRules = []

// Language rules
for (const lang of languages) {
  matchedRules.push(`cco-${lang}.md`)
}

// Framework rules
for (const fw of frameworks) {
  matchedRules.push(`cco-${fw}.md`)
}

// Operations rules
for (const op of operations) {
  matchedRules.push(`cco-${op}.md`)
}

// Security rule if sensitive data
if (data === 'pii' || data === 'regulated') {
  matchedRules.push('cco-security.md')
}

// Compliance rule if regulated
if (compliance.includes('hipaa') || compliance.includes('gdpr') ||
    compliance.includes('soc2') || data === 'regulated') {
  matchedRules.push('cco-compliance.md')
}

// Copy rules from plugin to project
const pluginRoot = process.env.CLAUDE_PLUGIN_ROOT || findPluginRoot()

for (const rule of matchedRules) {
  // Find rule in plugin (check all categories)
  const categories = ['languages', 'frameworks', 'operations']
  for (const cat of categories) {
    const src = `${pluginRoot}/rules/${cat}/${rule}`
    if (await fileExists(src)) {
      const content = await Read(src)
      await Write(`.claude/rules/${rule}`, content)
      break
    }
  }
}

console.log(`Copied ${matchedRules.length} rule files to .claude/rules/`)
```

---

## Result

After `/config` completes:

```
project/.claude/rules/
├── cco-context.md        # YAML frontmatter with all project metadata
├── cco-{language}.md     # Detected language rules
├── cco-{framework}.md    # Detected framework rules
├── cco-{operation}.md    # Detected operation rules
└── cco-security.md       # Added if data=pii or data=regulated
```

**Context check for other commands:**
```javascript
// Check if CCO is configured
if (!contextContains('cco: true')) {
  console.log('CCO not configured. Run /config first.')
  return
}
```

---

## Summary

| Step | Action |
|------|--------|
| 1 | Auto-detect languages, frameworks, operations, commands |
| 2 | Ask 2 question groups (8 questions total) - skip if --auto |
| 3 | Show detection summary |
| 4 | Clean existing cco-*.md files (if --reset) |
| 5 | Create .claude/rules/ directory |
| 6 | Generate cco-context.md with YAML frontmatter |
| 7 | Copy relevant rule files from plugin |

**Key changes from previous version:**
- Flat structure: All files in `.claude/rules/` (no subdirectories)
- YAML format: `cco-context.md` uses frontmatter, not markdown
- Context marker: `cco: true` in YAML for existence check
- 2 question groups instead of 1
- Auto-detect for commands, conventions, release, database
