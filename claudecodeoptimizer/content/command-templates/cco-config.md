---
name: cco-config
description: Configure project context and AI behavior
allowed-tools: Read(*), Write(*), Edit(*), Bash(cco-install:*), Task(*), TodoWrite, AskUserQuestion
---

# /cco-config

**Project Setup** - Background detection + combined questions for fast configuration.

## Args

- `--auto` or `--unattended`: Skip all questions, use recommended defaults
  - Context: Setup/Update
  - Statusline: Full
  - Permissions: Balanced
  - Thinking: Enabled
  - Budget: AI-recommended based on project complexity
  - Output: AI-recommended based on project complexity
  - Data: Public
  - Compliance: None

**Usage:** `/cco-config --auto` or `Skill("cco-config", args: "--auto")`

## Context

- Context exists: !`test -f ./.claude/rules/cco/context.md && echo "1" || echo "0"`
- Existing rules: !`test -d .claude/rules/cco && ls .claude/rules/cco/*.md | xargs -I{} basename {} | tr '\n' ' ' | grep . || echo "None"`
- Settings exists: !`test -f ./.claude/settings.json && echo "1" || echo "0"`
- Args: $ARGS

## Mode Detection

```javascript
// Check if running in unattended mode
const isUnattended = "$ARGS".includes("--auto") || "$ARGS".includes("--unattended")

if (isUnattended) {
  // Skip to Step-1 with defaults, no questions
  setupConfig = {
    context: "Setup/Update",
    statusline: "Full",
    permissions: "Balanced",
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
`, { model: "haiku", run_in_background: true })

// Don't wait - proceed to Q1 immediately
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

// UNATTENDED MODE: Skip Q1, use defaults
if (isUnattended) {
  setupConfig = {
    context: "Setup/Update",
    statusline: "Full",
    permissions: "Balanced",
    thinking: "Enabled"
  }
  // Proceed directly to Step-3
} else {
  AskUserQuestion([
  {
    question: "Project context action?",
    header: "Context",
    options: [
      {
        label: existingConfig.context ? "Setup/Update [current]" : "Setup/Update (Recommended)",
        description: "Configure or update project context and rules"
      },
      { label: "Remove", description: "Remove all CCO configuration" },
      { label: "Export", description: "Export rules to AGENTS.md or CLAUDE.md" }
    ],
    multiSelect: false
  },
  {
    question: "Statusline display?",
    header: "Statusline",
    options: [
      {
        label: existingConfig.statusline === "full" ? "Full [current]" : "Full (Recommended)",
        description: "User, model, context %, git status, file changes"
      },
      {
        label: existingConfig.statusline === "minimal" ? "Minimal [current]" : "Minimal",
        description: "User, model, context % only"
      },
      {
        label: "Skip",
        description: "Keep current statusline unchanged"
      },
      {
        label: existingConfig.statusline === "none" ? "Remove [current]" : "Remove",
        description: "Use Claude Code default statusline"
      }
    ],
    multiSelect: false
  },
  {
    question: "Permission approval level?",
    header: "Permissions",
    options: [
      {
        label: existingConfig.permissions === "permissive" ? "Permissive [current]" : "Permissive",
        description: "Auto-approve most operations (except force push)"
      },
      {
        label: existingConfig.permissions === "balanced" ? "Balanced [current]" : "Balanced (Recommended)",
        description: "Auto-approve read + lint/test, ask for writes"
      },
      {
        label: "Skip",
        description: "Keep current permissions unchanged"
      },
      {
        label: "Remove",
        description: "Remove permissions, use Claude Code defaults"
      }
    ],
    multiSelect: false
  },
  {
    question: "Enable extended thinking?",
    header: "Thinking",
    options: [
      {
        label: existingConfig.thinking === true ? "Enabled [current]" : "Enabled (Recommended)",
        description: "Better for complex code, architecture decisions"
      },
      {
        label: existingConfig.thinking === false ? "Disabled [current]" : "Disabled (CC default)",
        description: "Faster responses, better prompt caching"
      }
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

**First: Wait for detection results:**

```javascript
// Now collect detection results
detectResult = await TaskOutput(detectTask.id)

// Determine AI recommendations based on project complexity
aiRecommendations = calculateRecommendations(detectResult.complexity)
// complexity: simple → 8000, medium → 16000, complex → 32000
```

**UNATTENDED MODE: Use AI recommendations directly:**

```javascript
if (isUnattended) {
  // Use AI-recommended values based on project complexity
  contextConfig = {
    budget: aiRecommendations.budget,
    output: aiRecommendations.output,
    data: "Public",
    compliance: []  // No compliance requirements
  }
  // Skip Q2, proceed directly to Step-4
} else {
  // Interactive mode: Build Q2 dynamically (max 4 tabs)
```

**Build Q2 dynamically (max 4 tabs):**

```javascript
  questions = []

  // Tab 1: Thinking Budget (only if Thinking Enabled)
  // Claude Code: No default (disabled), minimum 1024 when enabled
  if (setupConfig.thinking === "Enabled") {
    questions.push({
      question: "Thinking token budget?",
      header: "Budget",
      options: [
        {
          label: existingConfig.budget === 4000 ? "4000 [current]" : "4000",
          description: "Simple tasks, faster responses"
        },
        {
          label: existingConfig.budget === 8000 ? "8000 [current]" :
                 aiRecommendations.budget === 8000 ? "8000 (Recommended)" : "8000",
          description: "Good balance for most tasks"
        },
        {
          label: existingConfig.budget === 16000 ? "16000 [current]" :
                 aiRecommendations.budget === 16000 ? "16000 (Recommended)" : "16000",
          description: "Complex multi-file refactoring"
        },
        {
          label: existingConfig.budget === 32000 ? "32000 [current]" :
                 aiRecommendations.budget === 32000 ? "32000 (Recommended)" : "32000",
          description: "Architecture design, large codebases"
        }
      ],
      multiSelect: false
    })
  }

  // Tab 2: Output Limits (always)
  // Claude Code defaults: MCP=25000, Bash=30000
  questions.push({
    question: "Tool output limits?",
    header: "Output",
    options: [
      {
        label: existingConfig.output === 10000 ? "10000 [current]" : "10000",
        description: "Save context, reduced output"
      },
      {
        label: existingConfig.output === 25000 ? "25000 [current]" :
               aiRecommendations.output === 25000 ? "25000 (Recommended)" : "25000 (CC default)",
        description: "Standard output limits"
      },
      {
        label: existingConfig.output === 35000 ? "35000 [current]" :
               aiRecommendations.output === 35000 ? "35000 (Recommended)" : "35000",
        description: "Large outputs, big codebases"
      }
    ],
    multiSelect: false
  })

  // Tab 3: Data Sensitivity (always)
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

  // Tab 4: Compliance (always, multiselect)
  questions.push({
    question: "Compliance requirements?",
    header: "Compliance",
    options: [
      { label: "SOC2", description: "B2B SaaS, enterprise customers" },
      { label: "GDPR/CCPA", description: "Privacy regulations" },
      { label: "HIPAA/PCI", description: "Healthcare or payments" }
    ],
    multiSelect: true  // None selected = No compliance
  })

  AskUserQuestion(questions)
}
```

**AI Recommendation Logic:**

```javascript
function calculateRecommendations(complexity) {
  if (complexity.loc > 50000 || complexity.files > 500) {
    return { budget: 32000, output: 35000 }
  } else if (complexity.loc > 10000 || complexity.files > 100) {
    return { budget: 16000, output: 35000 }
  } else {
    return { budget: 8000, output: 25000 }
  }
}
```

### Validation
```
[x] User completed Q2 (or unattended defaults applied)
→ Store as: contextConfig = { budget?, output, data, compliance }
→ Proceed to Step-4
```

---

## Step-4: Apply [BACKGROUND]

**Write all files from detection + user input:**

### 4.1: Generate Rules

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
  - setupConfig: ${JSON.stringify(setupConfig)}
  - contextConfig: ${JSON.stringify(contextConfig)}

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

### 4.2: Write Files

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
`, { run_in_background: true })
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
`)
```

### Validation
```
[x] Files written/removed
[x] No errors
→ Proceed to Step-7
```

---

## Step-5: Report

```
## Configuration Applied

### Files Written
| File | Action |
|------|--------|
| .claude/rules/cco/context.md | {action} |
| .claude/rules/cco/{language}.md | {action} |
| .claude/settings.json | {action} |
| .claude/cco-{mode}.js | Copied from CCO template |

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
| Settings.json corrupted | Delete `.claude/settings.json`, re-run `/cco-config` |
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
6. **Explicit defaults** - Always write ALL settings to files, even when default values are selected. Never omit a setting just because it's the default. Exception: statusLine "Remove" = don't write (preserves global config).
