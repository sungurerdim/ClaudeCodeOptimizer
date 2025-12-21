---
name: cco-config
description: Configure project context and AI behavior
allowed-tools: Read(*), Write(*), Edit(*), Bash(cco-install:*), Task(*), TodoWrite, AskUserQuestion
---

# /cco-config

**Project tuning** - Pre-detection reduces questions, parallel apply.

## Context

- Context exists: !`test -f ./.claude/rules/cco/context.md && echo "1" || echo "0"`
- Existing rules: !`test -d .claude/rules/cco && ls .claude/rules/cco/*.md | xargs -I{} basename {} | tr '\n' ' ' | grep . || echo "None"`
- Settings exists: !`test -f ./.claude/settings.json && echo "1" || echo "0"`

## Architecture

| Step | Name | Action | Optimization |
|------|------|--------|--------------|
| 1 | Pre-detect | cco-agent-analyze (config scope) | Skip questions |
| 2 | Status | Show detected + existing | Instant |
| 3 | Action | Ask what to do | Skip if --configure |
| 4 | Scope | Ask what to configure | Skip detected |
| 5 | Context | Only LOW confidence items | Fewer questions |
| 6 | Review | Show + ask approval | Instant |
| 7 | Apply | Write files | Background |
| 8 | Report | Summary | Instant |

---

## Progress Tracking [CRITICAL]

**Initialize at start. Update status after each step completes.**

```javascript
TodoWrite([
  { content: "Step-1: Pre-detect (parallel)", status: "in_progress", activeForm: "Running pre-detection" },
  { content: "Step-2: Show status", status: "pending", activeForm: "Showing status" },
  { content: "Step-3: Ask action", status: "pending", activeForm: "Asking action type" },
  { content: "Step-4: Ask scope + context", status: "pending", activeForm: "Asking scope and context" },
  { content: "Step-5: Review results", status: "pending", activeForm: "Reviewing results" },
  { content: "Step-6: Apply configuration", status: "pending", activeForm: "Applying configuration" },
  { content: "Step-7: Show report", status: "pending", activeForm: "Showing final report" }
])
```

---

## Step-1: Pre-detect [PARALLEL]

**Launch cco-agent-analyze with config scope (detection phase):**

```javascript
// CRITICAL: Config scope has TWO phases
// Phase 1 (Step-1): Detection only - returns detections + sources
// Phase 2 (Step-6): Rule generation - receives userInput, returns rules

detectResult = Task("cco-agent-analyze", `
  scopes: ["config"]
  phase: "detect"

  Auto-detect from manifest files and code:
  - Language, framework, runtime, packageManager
  - Infrastructure: containerized, ci, cloud, deployment
  - Testing: testFramework, coverage, linters, typeChecker
  - Metadata: license, teamSize, maturity, lastActivity
`, { model: "haiku" })

// Agent returns (config scope, detect phase):
// detectResult = {
//   detections: {
//     language: ["{lang}"],
//     type: ["{type}"],
//     api: "{api|null}",
//     database: "{db|null}",
//     frontend: "{frontend|null}",
//     infra: ["{infra}"],
//     dependencies: ["{deps}"]
//   },
//   sources: [{ file: "{file}", confidence: "HIGH|MEDIUM|LOW" }]
// }
```

**Result: Pre-fill answers based on detection confidence**

| Confidence | Action |
|------------|--------|
| HIGH (90%+) | Auto-apply, don't ask |
| MEDIUM (70-89%) | Pre-fill with `[detected]` label |
| LOW (<70%) | Ask user |

### Validation
```
[x] Detection completed
[x] Confidence levels assigned
→ Proceed to Step-2
```

---

## Step-2: Status

Display detected + existing configuration:

```
## Project Status

### Auto-Detected (HIGH confidence - won't ask)
| Element | Value | Source |
|---------|-------|--------|
| Language | {language} | {source_file} |
| Framework | {framework} | {source_file} |
| Test Framework | {test_framework} | {source_file} |
| CI | {ci} | {source_file} |

### Needs Confirmation (MEDIUM confidence)
| Element | Value | Source |
|---------|-------|--------|
| Coverage | {coverage}% | {source_file} [detected] |
| Team Size | {team_size} | git contributors |

### Will Ask (LOW confidence)
- Data sensitivity
- Compliance requirements
- SLA commitment

### Existing Configuration
| File | Status |
|------|--------|
| .claude/rules/cco/context.md | {exists/missing} |
| .claude/settings.json | {exists/missing} |
```

### Validation
```
[x] Detection results displayed
[x] Existing config shown
→ Proceed to Step-3
```

---

## Step-3: Action

**Ask what user wants to do.**

```javascript
AskUserQuestion([{
  question: "What would you like to do?",
  header: "Action",
  options: [
    { label: "Configure (Recommended)", description: "Apply detected settings + ask remaining" },
    { label: "Remove", description: "Remove existing CCO configuration" },
    { label: "Export", description: "Export rules to AGENTS.md or CLAUDE.md" }
  ],
  multiSelect: false
}])
```

**Flags override:** `--configure`, `--remove`, `--export` skip this question.

### Validation
```
[x] User selected: Configure | Remove | Export
→ Store as: action = {selection}
→ If Remove or Export: Skip to Step-6
→ Proceed to Step-4
```

---

## Step-4: Scope + Context [ONLY LOW CONFIDENCE ITEMS]

**Only ask questions for items NOT auto-detected or LOW confidence:**

### 4.1: Statusline Setup [ALWAYS ASK - MANDATORY QUESTION]

**CRITICAL: This question MUST always be asked. Statusline is optional but the question is mandatory.**

```javascript
// Statusline question is MANDATORY - never skip
AskUserQuestion([{
  question: "Install CCO statusline?",
  header: "Statusline",
  options: [
    { label: "Full (Recommended)", description: "User, model, context %, git status, file changes" },
    { label: "Minimal", description: "User, model, context % only" },
    { label: "No", description: "Use Claude Code default statusline" }
  ],
  multiSelect: false
}])
```

### 4.2: Other Settings [OPTIONAL]

```javascript
// Additional settings - optional
AskUserQuestion([{
  question: "Configure additional settings?",
  header: "Settings",
  options: [
    { label: "Permissions", description: "Tool approval levels: safe, balanced, permissive, full" },
    { label: "AI Performance", description: "Extended thinking, tool output limits" },
    { label: "Skip", description: "Only apply detected context rules" }
  ],
  multiSelect: true
}])
```

### 4.3: Context Questions (LOW confidence only)

**Only ask what wasn't detected:**

```javascript
// Build question list dynamically based on detection confidence
lowConfidenceQuestions = []

if (detected.data.confidence < 70) {
  lowConfidenceQuestions.push({
    question: "Most sensitive data handled?",
    header: "Data",
    options: [
      { label: "Public", description: "Open data, no sensitivity" },
      { label: "PII", description: "Personal identifiable information" },
      { label: "Regulated", description: "Healthcare, finance, regulated data" }
    ],
    multiSelect: false
  })
}

if (detected.compliance.confidence < 70) {
  lowConfidenceQuestions.push({
    question: "Compliance requirements?",
    header: "Compliance",
    options: [
      { label: "None", description: "No compliance requirements" },
      { label: "SOC2", description: "B2B SaaS, enterprise customers" },
      { label: "GDPR/CCPA", description: "Privacy regulations" },
      { label: "HIPAA/PCI", description: "Healthcare or payments" }
    ],
    multiSelect: true
  })
}

if (detected.sla.confidence < 70) {
  lowConfidenceQuestions.push({
    question: "Uptime commitment (SLA)?",
    header: "SLA",
    options: [
      { label: "None", description: "Best effort" },
      { label: "99%+", description: "Production SLA" }
    ],
    multiSelect: false
  })
}

// Ask all low-confidence questions in one batch (max 4)
if (lowConfidenceQuestions.length > 0) {
  AskUserQuestion(lowConfidenceQuestions.slice(0, 4))
}
```

**Result: Typically 0-2 questions instead of 8+**

### 4.4: Permission Details [IF SELECTED IN 4.2]

```javascript
// If user selected Permissions in 4.2
if (selectedSettings.includes("Permissions")) {
  AskUserQuestion([
    {
      question: "Permission approval level?",
      header: "Permissions",
      options: [
        { label: "Balanced (Recommended)", description: "Auto-approve read + lint/test, ask for writes" },
        { label: "Safe", description: "Auto-approve read-only operations" },
        { label: "Permissive", description: "Auto-approve most operations" },
        { label: "Full", description: "Auto-approve all (Solo + Public projects only)" }
      ],
      multiSelect: false
    },
    {
      question: "Enable LSP (code intelligence)?",
      header: "LSP",
      options: [
        { label: "Yes (Recommended)", description: "go-to-definition, find-references, hover docs (+500 tokens)" },
        { label: "No", description: "Use text-based search only" }
      ],
      multiSelect: false
    }
  ])
}
```

### 4.5: AI Performance Details [IF SELECTED IN 4.2]

```javascript
// If user selected AI Performance in 4.2
if (selectedSettings.includes("AI Performance")) {
  AskUserQuestion([
    {
      question: "Enable extended thinking for complex reasoning?",
      header: "Thinking",
      options: [
        { label: "Enabled (Recommended)", description: "Better for complex code, architecture decisions" },
        { label: "Disabled", description: "Faster responses, better prompt caching" }
      ],
      multiSelect: false
    },
    {
      question: "Thinking token budget?",
      header: "Budget",
      options: [
        { label: "8K (Recommended)", description: "Good balance for most tasks" },
        { label: "16K", description: "Complex multi-file refactoring" },
        { label: "32K", description: "Architecture design, large codebases" },
        { label: "4K", description: "Simple tasks, faster responses" }
      ],
      multiSelect: false
    },
    {
      question: "Tool output limits?",
      header: "Output",
      options: [
        { label: "Default", description: "25K MCP tokens, standard bash output" },
        { label: "Extended", description: "35K MCP tokens, 100K bash chars for large outputs" },
        { label: "Minimal", description: "10K MCP tokens, reduced context usage" }
      ],
      multiSelect: false
    }
  ])
}
```

**AI Performance settings map:**

| Selection | Setting |
|-----------|---------|
| Thinking: Enabled | `alwaysThinkingEnabled: true` |
| Thinking: Disabled | `alwaysThinkingEnabled: false` |
| Budget: 8K | `env.MAX_THINKING_TOKENS: "8000"` |
| Budget: 16K | `env.MAX_THINKING_TOKENS: "16000"` |
| Budget: 32K | `env.MAX_THINKING_TOKENS: "32000"` |
| Budget: 4K | `env.MAX_THINKING_TOKENS: "4000"` |
| Output: Default | `env.MAX_MCP_OUTPUT_TOKENS: "25000"`, `env.BASH_MAX_OUTPUT_LENGTH: "30000"` |
| Output: Extended | `env.MAX_MCP_OUTPUT_TOKENS: "35000"`, `env.BASH_MAX_OUTPUT_LENGTH: "100000"` |
| Output: Minimal | `env.MAX_MCP_OUTPUT_TOKENS: "10000"`, `env.BASH_MAX_OUTPUT_LENGTH: "15000"` |

### Validation
```
[x] Statusline question asked (mandatory)
[x] Other settings offered
[x] Low confidence context items asked
[x] Permission details collected (if selected)
→ Proceed to Step-5
```

---

## Step-5: Review

**Show merged detection + user input results:**

```
## Configuration Preview

### Auto-Detected (applied automatically)
| Element | Value | Confidence |
|---------|-------|------------|
| Language | {language} | {confidence} |
| Framework | {framework} | {confidence} |
| Test Framework | {test_framework} | {confidence} |
| Coverage | {coverage}% | {confidence} |
| Team Size | {team_size} | {confidence} |

### User Confirmed
| Element | Value |
|---------|-------|
| Data | {data} |
| Compliance | {compliance} |

### Rules Selected
- core.md (always)
- {language}.md (detected)
- {scale}.md (based on context)
- {additional}.md (based on context)

### Settings
| Setting | Value |
|---------|-------|
| Statusline | {statusline_mode} |
| Permissions | {permissions} |
| LSP | {lsp_enabled} |
| Extended Thinking | {thinking_enabled} |
| Thinking Budget | {thinking_budget} |
| Tool Output Limits | {output_limits} |
```

```javascript
AskUserQuestion([{
  question: "Apply this configuration?",
  header: "Apply",
  options: [
    { label: "Accept (Recommended)", description: "Apply all settings" },
    { label: "Edit", description: "Modify before applying" },
    { label: "Cancel", description: "Discard and exit" }
  ],
  multiSelect: false
}])
```

### Validation
```
[x] Preview displayed
[x] User approved
→ If Cancel: Exit
→ If Edit: Return to Step-4
→ Proceed to Step-6
```

---

## Step-6: Apply [BACKGROUND]

**Write all files from detection results:**

### 6.1: Generate Rules from Detection + User Input

**CRITICAL:** Call cco-agent-analyze with config scope (generate phase) to create rules.

**[IMPORTANT] Rule Source Architecture:**
- All rules are defined as **sections within `cco-adaptive.md`** (single file)
- Separate `{category}.md` rule files do **NOT exist** in CCO package
- The agent must **read cco-adaptive.md** and **extract relevant sections** based on detections
- **NEVER try to read separate `{category}.md` files** - they will error with "file not found"

```javascript
// Phase 2: Generate rules using detections from Step-1 + user input from Steps 3-4
generateResult = Task("cco-agent-analyze", `
  scopes: ["config"]
  phase: "generate"

  Input:
  - detections: ${JSON.stringify(detectResult.detections)}
  - userInput: ${JSON.stringify(collectedUserInput)}

  Generate (from cco-adaptive.md sections, NOT separate files):
  1. Read cco-adaptive.md via: Bash(cco-install --cat rules/cco-adaptive.md)
  2. Extract sections matching detections (e.g., "{Lang} (L:{Lang})" section → {lang}.md)
  3. Generate context.md with project context
  4. Generate rule files with extracted section content
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

### 6.2: Write Files

```javascript
Task("cco-agent-apply", `
  Write ALL files from generateResult:

  1. Context file:
     - .claude/rules/cco/context.md ← generateResult.context

  2. ALL rule files (from generateResult.rules array):
     Loop: for each rule in generateResult.rules:
       - .claude/rules/cco/{rule.file} ← {rule.content}

  3. Settings:
     - .claude/settings.json ← merge with existing

  4. Statusline (if user selected Full or Minimal):
     - Get CCO package path: python3 -c "from claudecodeoptimizer.config import get_content_path; print(get_content_path('statusline'))"
     - Copy template: cp $CCO_PATH/cco-{mode}.js .claude/cco-{mode}.js
     - Do NOT generate statusline code - ALWAYS copy from CCO package

  Total files: generateResult.rules.length + 2 + (statusline ? 1 : 0)
`, { model: "sonnet", run_in_background: true })
```

### Detection → Rule Mapping (Complete Reference)

**CRITICAL:** All detections from cco-adaptive.md must map to rule files. No orphan detections.

#### Languages (L:*)
| Detection | Rule File | Triggers |
|-----------|-----------|----------|
| L:Python | `{lang}.md` | pyproject.toml, setup.py, requirements*.txt, *.py |
| L:TypeScript | `{lang}.md` | tsconfig.json, *.ts/*.tsx |
| L:JavaScript | `{lang}.md` | package.json (no TS), *.js |
| L:Go | `{lang}.md` | go.mod, *.go |
| L:Rust | `{lang}.md` | Cargo.toml, *.rs |
| L:Java | `{lang}.md` | pom.xml, build.gradle, *.java |
| L:Kotlin | `{lang}.md` | *.kt, kotlin in gradle |
| L:Swift | `{lang}.md` | Package.swift, *.swift |
| L:CSharp | `{lang}.md` | *.csproj, *.sln, *.cs |
| L:Ruby | `{lang}.md` | Gemfile, *.gemspec, *.rb |
| L:PHP | `{lang}.md` | composer.json, *.php |
| L:Elixir | `{lang}.md` | mix.exs, *.ex |
| L:Gleam | `{lang}.md` | gleam.toml, *.gleam |
| L:Scala | `{lang}.md` | build.sbt, *.scala |
| L:Zig | `{lang}.md` | build.zig, *.zig |
| L:Dart | `{lang}.md` | pubspec.yaml, *.dart |

#### Runtimes (R:*)
| Detection | Rule File | Triggers |
|-----------|-----------|----------|
| R:Node | `node.md` | package.json, node_modules/ |
| R:Bun | `bun.md` | bun.lockb, bunfig.toml |
| R:Deno | `deno.md` | deno.json, deno.lock |

#### App Types (T:*)
| Detection | Rule File | Triggers |
|-----------|-----------|----------|
| T:CLI | `cli.md` | [project.scripts], typer/click/cobra |
| T:Library | `library.md` | exports, __all__, [lib] |
| T:Service | `service.md` | Dockerfile + ports |

#### API Styles (API:*)
| Detection | Rule File | Triggers |
|-----------|-----------|----------|
| API:REST | `api.md` | routes/, FastAPI/Express |
| API:GraphQL | `api.md` | *.graphql, apollo |
| API:gRPC | `api.md` | *.proto, grpc deps |

#### Database (DB:*)
| Detection | Rule File | Triggers |
|-----------|-----------|----------|
| DB:SQL | `database.md` | sqlite3/psycopg2, migrations/ |
| DB:ORM | `database.md` | sqlalchemy/prisma/drizzle |
| DB:NoSQL | `database.md` | pymongo/redis/dynamodb |
| DB:Vector | `database.md` | pgvector/pinecone/chroma |

#### Frontend
| Detection | Rule File | Triggers |
|-----------|-----------|----------|
| Frontend:React | `frontend.md` | react deps, *.jsx/*.tsx |
| Frontend:Vue | `frontend.md` | vue deps, *.vue |
| Frontend:Svelte | `frontend.md` | svelte deps, *.svelte |
| Frontend:Angular | `frontend.md` | @angular deps |
| Frontend:Solid | `frontend.md` | solid-js deps |
| Frontend:Astro | `frontend.md` | astro deps, *.astro |
| Frontend:HTMX | `frontend.md` | htmx deps, hx-* in HTML |

#### Mobile
| Detection | Rule File | Triggers |
|-----------|-----------|----------|
| Mobile:Flutter | `mobile.md` | pubspec.yaml, *.dart |
| Mobile:ReactNative | `mobile.md` | react-native/expo deps |
| Mobile:iOS | `mobile.md` | *.xcodeproj, Podfile, *.swift |
| Mobile:Android | `mobile.md` | build.gradle, AndroidManifest.xml |
| Mobile:KMP | `mobile.md` | kotlin-multiplatform, shared/ |

#### Desktop
| Detection | Rule File | Triggers |
|-----------|-----------|----------|
| Desktop:Electron | `desktop.md` | electron deps |
| Desktop:Tauri | `desktop.md` | tauri.conf.json |

#### Infrastructure (Infra:*)
| Detection | Rule File | Triggers |
|-----------|-----------|----------|
| Infra:Docker | `container.md` | Dockerfile, docker-compose.yml |
| Infra:K8s | `k8s.md` | k8s/, helm/, kustomization.yaml |
| Infra:Terraform | `terraform.md` | *.tf files |
| Infra:Pulumi | `pulumi.md` | Pulumi.yaml |
| Infra:CDK | `cdk.md` | cdk.json |
| Infra:Edge | `edge.md` | wrangler.toml, vercel edge |
| Infra:WASM | `wasm.md` | *.wasm, wasm-pack |
| Infra:Serverless | `serverless.md` | serverless.yml, sam.yaml |

#### ML/AI
| Detection | Rule File | Triggers |
|-----------|-----------|----------|
| ML:Training | `ml.md` | torch/tensorflow/sklearn |
| ML:LLM | `ml.md` | langchain/llamaindex/haystack |
| ML:Inference | `ml.md` | transformers/onnxruntime/vllm |
| ML:SDK | `ml.md` | openai/anthropic/cohere deps |

#### Build Tools
| Detection | Rule File | Triggers |
|-----------|-----------|----------|
| Build:Monorepo | `monorepo.md` | nx.json, turbo.json, pnpm-workspace.yaml |
| Build:Bundler | `bundler.md` | vite.config.*, webpack.config.*, esbuild |
| Build:Linter | `linter.md` | .eslintrc*, biome.json, ruff.toml |
| Build:Formatter | `formatter.md` | .prettierrc*, biome.json |
| Build:TypeChecker | `typechecker.md` | tsconfig.json, mypy.ini, pyproject.toml[mypy] |

#### Testing (Test:*)
| Detection | Rule File | Triggers |
|-----------|-----------|----------|
| Test:Unit | `testing.md` | pytest/jest/vitest, tests/ |
| Test:E2E | `testing.md` | playwright/cypress, e2e/ |
| Test:Coverage | `testing.md` | [tool.coverage], .nycrc, jest --coverage |

#### CI/CD
| Detection | Rule File | Triggers |
|-----------|-----------|----------|
| CI:GitHub | `ci-cd.md` | .github/workflows/ |
| CI:GitLab | `ci-cd.md` | .gitlab-ci.yml |
| CI:Jenkins | `ci-cd.md` | Jenkinsfile |
| CI:CircleCI | `ci-cd.md` | .circleci/config.yml |
| CI:Azure | `ci-cd.md` | azure-pipelines.yml |
| CI:ArgoCD | `ci-cd.md` | argocd/, Application.yaml |

#### Meta-Frameworks
| Detection | Rule File | Triggers |
|-----------|-----------|----------|
| Framework:Next | `nextjs.md` | {nextjs_deps}, {nextjs_config} |
| Framework:Nuxt | `nuxt.md` | {nuxt_deps}, {nuxt_config} |
| Framework:SvelteKit | `sveltekit.md` | {sveltekit_deps}, {sveltekit_config} |
| Framework:Remix | `remix.md` | {remix_deps}, {remix_patterns} |

#### Specialized
| Detection | Rule File | Triggers |
|-----------|-----------|----------|
| Game:Unity | `game.md` | {unity_markers} |
| Game:Unreal | `game.md` | {unreal_markers} |
| Game:Godot | `game.md` | {godot_markers} |
| i18n | `i18n.md` | {i18n_dirs}, {i18n_deps} |
| RT:Basic | `realtime.md` | {websocket_deps}, {sse_patterns} |
| RT:LowLatency | `realtime.md` | {binary_protocol_deps}, {realtime_patterns} |

#### User Input (from Step-4)
| Input | Rule File | Source |
|-------|-----------|--------|
| Scale:* | `scale.md` | User selection |
| Team:* | `team.md` | User selection |
| Testing:* | `testing.md` | User selection (merged with detected) |
| Security | `security.md` | Data:PII/Regulated triggers |
| Compliance:* | `compliance.md` | User selection |
| SLA:* | `observability.md` | User selection |

#### Dependency-Specific (DEP:*)

| Detection | Rule File | Trigger Reference |
|-----------|-----------|-------------------|
| DEP:CLI | `dep-cli.md` | {cli_framework_deps} |
| DEP:TUI | `dep-tui.md` | {tui_deps} |
| DEP:Validation | `dep-validation.md` | {validation_deps} |
| DEP:Config | `dep-config.md` | {config_deps} |
| DEP:Testing | `dep-testing.md` | {testing_framework_deps} |
| DEP:HTTP | `dep-http.md` | {http_client_deps} |
| DEP:ORM | `dep-orm.md` | {orm_deps} |
| DEP:Auth | `dep-auth.md` | {auth_deps} |
| DEP:Cache | `dep-cache.md` | {cache_deps} |
| DEP:Queue | `dep-queue.md` | {queue_deps} |
| DEP:Search | `dep-search.md` | {search_deps} |
| DEP:GPU | `dep-gpu.md` | {gpu_deps} |
| DEP:HeavyModel | `dep-heavymodel.md` | {heavy_model_deps} |
| DEP:DataHeavy | `dep-data.md` | {data_processing_deps} |
| DEP:Image | `dep-image.md` | {image_processing_deps} |
| DEP:Audio | `dep-audio.md` | {audio_processing_deps} |
| DEP:Video | `dep-video.md` | {video_processing_deps} |
| DEP:Logging | `dep-logging.md` | {logging_deps} |
| DEP:ObjectStore | `dep-storage.md` | {object_storage_deps} |
| DEP:Payment | `dep-payment.md` | {payment_deps} |
| DEP:Email | `dep-email.md` | {email_deps} |
| DEP:SMS | `dep-sms.md` | {sms_deps} |
| DEP:Notification | `dep-notification.md` | {notification_deps} |
| DEP:PDF | `dep-pdf.md` | {pdf_deps} |
| DEP:Excel | `dep-excel.md` | {excel_deps} |
| DEP:Scraping | `dep-scraping.md` | {scraping_deps} |
| DEP:Blockchain | `dep-blockchain.md` | {blockchain_deps} |
| DEP:Crypto | `dep-crypto.md` | {crypto_deps} |
| DEP:Edge | `dep-edge.md` | {edge_runtime_deps} |
| DEP:EdgeFramework | `dep-edgeframework.md` | {edge_framework_deps} |
| DEP:WASM | `dep-wasm.md` | {wasm_toolchain_deps} |
| DEP:GamePython | `dep-game-python.md` | {python_game_deps} |
| DEP:GameJS | `dep-game-js.md` | {js_game_deps} |
| DEP:GameEngine | `dep-gameengine.md` | {game_engine_markers} |
| DEP:ARVR | `dep-arvr.md` | {arvr_deps} |
| DEP:IoT | `dep-iot.md` | {iot_deps} |
| DEP:APITest | `dep-apitest.md` | {api_test_deps} |
| DEP:TypeSafeAPI | `dep-typesafe-api.md` | {typesafe_api_deps} |
| DEP:DataQuery | `dep-data-query.md` | {data_query_deps} |
| DEP:CSS | `dep-css.md` | {css_deps} |
| DEP:WebSocket | `dep-websocket.md` | {websocket_deps} |
| DEP:StateManagement | `dep-state.md` | {state_mgmt_deps} |

**Pattern:** `dep-{category}.md` where `{category}` matches detected dependency categories

**Trigger values:** Defined in cco-triggers.md (SSOT)

### Settings.json Structure

**Merge these settings into `.claude/settings.json`:**

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

**Statusline mode mapping:**

**[CRITICAL - NO CODE GENERATION]** Statusline scripts are pre-built in CCO package. NEVER generate JavaScript code for statusline. ALWAYS copy from package templates.

| Mode | Script | Action |
|------|--------|--------|
| Full | `cco-full.js` | Copy from CCO package → `.claude/cco-full.js` |
| Minimal | `cco-minimal.js` | Copy from CCO package → `.claude/cco-minimal.js` |
| No | (none) | Do not write statusLine key to settings.json |

**Command format:** All statusline modes use dynamic path resolution:
```
node -e "require('child_process').spawnSync('node',[require('path').join(process.cwd(),'.claude','cco-{mode}.js')],{stdio:'inherit'})"
```
This ensures the script runs from the correct project directory regardless of where Claude Code is launched.

**Note:** Statusline scripts require Node.js. If not available, select "No" to use default statusline.

**Copy statusline script to project:**

```bash
# Get CCO package path and copy statusline template
CCO_STATUSLINE_DIR=$(python3 -c "from claudecodeoptimizer.config import get_content_path; print(get_content_path('statusline'))")

# Copy the selected template (Full → cco-full.js, Minimal → cco-minimal.js)
if [ "{statusline_mode}" != "No" ]; then
  cp "$CCO_STATUSLINE_DIR/cco-{statusline_mode_lower}.js" .claude/cco-{statusline_mode_lower}.js
fi
```

**Alternative using Read/Write tools:**
```
# 1. First get the package path
Bash: CCO_PATH=$(python3 -c "from claudecodeoptimizer.config import get_content_path; print(get_content_path('statusline'))")

# 2. Read the template from package
Read: $CCO_PATH/cco-{full|minimal}.js

# 3. Write to project
Write: .claude/cco-{full|minimal}.js (exact copy, no modifications)
```

**CRITICAL:** Do NOT generate statusline code from scratch. ALWAYS copy from CCO package templates.

### If action = Remove

```javascript
// Parallel removal
Bash("rm -rf .claude/rules/cco/")
// Edit settings.json to remove CCO entries
```

### If action = Export

```javascript
Task("cco-agent-apply", `
  Export rules to ${format}:
  - Read all .claude/rules/cco/*.md
  - Filter for target format
  - Write to ./${format}
`, { model: "sonnet" })
```

### Validation
```
[x] Files written/removed
[x] No errors
→ Proceed to Step-7
```

---

## Step-7: Report

```
## Configuration Applied

### Files Written
| File | Action |
|------|--------|
| .claude/rules/cco/context.md | {action} |
| .claude/rules/cco/{language}.md | {action} |
| .claude/settings.json | {action} |

### Detection Summary
- Auto-detected: {n} elements
- User confirmed: {n} elements
- Questions asked: {n} (vs {n}+ traditional)

### Next Steps
- Restart Claude Code to apply new rules
- Run /cco-status to verify configuration
```

### Validation
```
[x] Report displayed
[x] All todos marked completed
→ Done
```

---

## Reference

### Dynamic Label Rules

| Label | When to Apply | Priority |
|-------|---------------|----------|
| `[current]` | Option matches existing config | 1 (highest) |
| `[detected]` | Option matches agent detection | 2 |
| `(Recommended)` | Option is best practice | 3 |

### Permissions Levels (explicit settings.json values)

| Level | `permissions.allow` | `permissions.deny` |
|-------|---------------------|-------------------|
| Safe | `["Read", "Glob", "Grep"]` | `[]` |
| Balanced | `["Read", "Glob", "Grep", "LSP", {detected_lint_tools}, {detected_test_tools}]` | `[]` |
| Permissive | `["Read", "Glob", "Grep", "LSP", "Edit", "Write", "Bash"]` | `["Bash(rm -rf:*)", "Bash(git push -f:*)"]` |
| Full | `["Read", "Glob", "Grep", "LSP", "Edit", "Write", "Bash", "Task"]` | `[]` |

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
| Wrong rules generated | Re-run `/cco-config`, select "Detection & Rules", adjust answers |
| Want to start fresh | Run `/cco-config` → Remove → Rules, then Configure again |
| Settings.json corrupted | Delete `.claude/settings.json`, re-run `/cco-config` |
| Detection crashed | Re-run `/cco-config` - detection is stateless |
| Wrong AI Performance | `/cco-config` → Configure → AI Performance, select new values |
| Applied wrong permissions | `cco-install --local . --permissions {correct-level}` |

**Safe pattern:** CCO config files are additive. Removing and re-creating is always safe.

---

## Rules

1. **Use cco-agent-analyze** - Agent handles detection with config scope
2. **Skip HIGH confidence** - Don't ask what's already detected
3. **Batch LOW confidence** - Ask remaining questions in single batch
4. **Use cco-agent-apply** - Agent handles file writing with verification
5. **Background apply** - Write files while user sees report
6. **Explicit defaults** - Always write ALL settings to files, even when default values are selected. Never omit a setting just because it's the default. Exception: statusLine "No" = don't write (preserves global config).
