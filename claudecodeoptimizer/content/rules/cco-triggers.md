# CCO Trigger Registry
*SSOT for all detection patterns. Referenced by cco-adaptive.md and cco-agent-analyze.md.*
*Updated: 2025-12-21*

## Purpose

This file defines ALL trigger patterns for project detection. Other files reference these definitions to ensure:
- **SSOT**: Single source of truth for trigger values
- **DRY**: No duplicate trigger definitions
- **Consistency**: Same patterns used across detection and rule generation

## Usage

In other CCO files, reference triggers as `{trigger_name}` where `trigger_name` matches definitions below.

---

## Generic Triggers (Cross-Category)

These generic placeholders are used across multiple categories. Each category section below defines specific values.

| Trigger | Description | Resolution |
|---------|-------------|------------|
| `{manifest}` | Language manifest file | Use specific: `{py_manifest}`, `{js_manifest}`, etc. |
| `{lock}` | Lock file | Use specific: `{py_lock}`, `{js_lock}`, etc. |
| `{code_ext}` | Source code extension | Use specific: `{py_ext}`, `{ts_ext}`, etc. |
| `{project_file}` | Project configuration | Use specific: `{csharp_project}`, `{ios_project}`, etc. |
| `{component_ext}` | Component file extension | Use specific: `{vue_ext}`, `{svelte_ext}`, `{astro_ext}` |
| `{framework_deps}` | Framework dependencies | Use specific: `{react_deps}`, `{vue_deps}`, etc. |

**Note:** Always prefer specific triggers over generic ones for accuracy.

---

## Language Detection

### Python (L:Python)
| Trigger | Values |
|---------|--------|
| `{py_manifest}` | `pyproject.toml`, `setup.py`, `requirements.txt`, `Pipfile`, `setup.cfg` |
| `{py_lock}` | `poetry.lock`, `Pipfile.lock`, `requirements.lock`, `uv.lock`, `pdm.lock` |
| `{py_ext}` | `*.py`, `*.pyi`, `*.pyw` |
| `{py_config}` | `pyrightconfig.json`, `mypy.ini`, `ruff.toml`, `.ruff.toml`, `pyproject.toml[tool.ruff]` |

### TypeScript (L:TypeScript)
| Trigger | Values |
|---------|--------|
| `{ts_config}` | `tsconfig.json`, `tsconfig.*.json` |
| `{ts_ext}` | `*.ts`, `*.tsx`, `*.mts`, `*.cts` |
| `{js_manifest}` | `package.json` |
| `{js_lock}` | `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `bun.lockb` |

### JavaScript (L:JavaScript)
| Trigger | Values |
|---------|--------|
| `{js_ext}` | `*.js`, `*.jsx`, `*.mjs`, `*.cjs` |
| `{js_manifest}` | `package.json` |

### Go (L:Go)
| Trigger | Values |
|---------|--------|
| `{go_manifest}` | `go.mod` |
| `{go_lock}` | `go.sum` |
| `{go_ext}` | `*.go` |

### Rust (L:Rust)
| Trigger | Values |
|---------|--------|
| `{rust_manifest}` | `Cargo.toml` |
| `{rust_lock}` | `Cargo.lock` |
| `{rust_ext}` | `*.rs` |

### Java (L:Java)
| Trigger | Values |
|---------|--------|
| `{java_manifest}` | `pom.xml`, `build.gradle`, `build.gradle.kts` |
| `{java_ext}` | `*.java` |

### Kotlin (L:Kotlin)
| Trigger | Values |
|---------|--------|
| `{kotlin_config}` | `build.gradle.kts` with `kotlin`, `settings.gradle.kts` |
| `{kotlin_ext}` | `*.kt`, `*.kts` |

### Swift (L:Swift)
| Trigger | Values |
|---------|--------|
| `{swift_manifest}` | `Package.swift` |
| `{swift_lock}` | `Package.resolved` |
| `{swift_ext}` | `*.swift` |
| `{ios_project}` | `*.xcodeproj`, `*.xcworkspace` |

### C# (L:CSharp)
| Trigger | Values |
|---------|--------|
| `{csharp_project}` | `*.csproj`, `*.sln` |
| `{csharp_lock}` | `packages.lock.json` |
| `{csharp_ext}` | `*.cs` |

### Ruby (L:Ruby)
| Trigger | Values |
|---------|--------|
| `{ruby_manifest}` | `Gemfile`, `*.gemspec` |
| `{ruby_lock}` | `Gemfile.lock` |
| `{ruby_ext}` | `*.rb`, `*.rake` |

### PHP (L:PHP)
| Trigger | Values |
|---------|--------|
| `{php_manifest}` | `composer.json` |
| `{php_lock}` | `composer.lock` |
| `{php_ext}` | `*.php` |

### Elixir (L:Elixir)
| Trigger | Values |
|---------|--------|
| `{elixir_manifest}` | `mix.exs` |
| `{elixir_lock}` | `mix.lock` |
| `{elixir_ext}` | `*.ex`, `*.exs` |

### Gleam (L:Gleam)
| Trigger | Values |
|---------|--------|
| `{gleam_manifest}` | `gleam.toml` |
| `{gleam_lock}` | `manifest.toml` |
| `{gleam_ext}` | `*.gleam` |

### Scala (L:Scala)
| Trigger | Values |
|---------|--------|
| `{scala_manifest}` | `build.sbt`, `build.sc` |
| `{scala_ext}` | `*.scala`, `*.sc` |

### Zig (L:Zig)
| Trigger | Values |
|---------|--------|
| `{zig_manifest}` | `build.zig`, `build.zig.zon` |
| `{zig_lock}` | `zig.lock` |
| `{zig_ext}` | `*.zig` |

### Dart (L:Dart)
| Trigger | Values |
|---------|--------|
| `{dart_manifest}` | `pubspec.yaml` |
| `{dart_lock}` | `pubspec.lock` |
| `{dart_ext}` | `*.dart` |

---

## Runtime Detection

### Node.js (R:Node)
| Trigger | Values |
|---------|--------|
| `{node_markers}` | `package.json`, `package-lock.json`, `node_modules/`, `.nvmrc`, `.node-version` |
| `{node_engine}` | `package.json[engines.node]` |

### Bun (R:Bun)
| Trigger | Values |
|---------|--------|
| `{bun_markers}` | `bun.lockb`, `bunfig.toml`, `.bunfig.toml` |
| `{bun_version}` | `1.1+` preferred |

### Deno (R:Deno)
| Trigger | Values |
|---------|--------|
| `{deno_markers}` | `deno.json`, `deno.jsonc`, `deno.lock` |
| `{deno_version}` | `2.0+` preferred |

---

## Project Type Detection

### CLI (T:CLI)
| Trigger | Values |
|---------|--------|
| `{entry_points}` | `pyproject.toml[project.scripts]`, `package.json[bin]`, `main.go`, `cmd/` |
| `{cli_deps}` | `typer`, `click`, `argparse`, `fire`, `cobra`, `urfave/cli`, `clap`, `argh` |
| `{bin_dir}` | `bin/`, `scripts/`, `cmd/` |

### Library (T:Library)
| Trigger | Values |
|---------|--------|
| `{export_markers}` | `__all__`, `exports` in package.json, `pub use` |
| `{lib_markers}` | `[lib]` in Cargo.toml, `[project.name]` without scripts |

### Service (T:Service)
| Trigger | Values |
|---------|--------|
| `{container}` | `Dockerfile`, `docker-compose.yml`, `docker-compose.yaml` |
| `{ports}` | `EXPOSE` in Dockerfile, `ports:` in compose |
| `{daemon_patterns}` | `uvicorn`, `gunicorn`, `express().listen`, `http.createServer` |

---

## API Style Detection

### REST (API:REST)
| Trigger | Values |
|---------|--------|
| `{routes_dir}` | `routes/`, `api/`, `endpoints/` |
| `{rest_decorators}` | `@app.get`, `@app.post`, `@router`, `app.use`, `@Get()`, `@Post()` |
| `{rest_patterns}` | `router.get`, `router.post`, `.route()` |

### GraphQL (API:GraphQL)
| Trigger | Values |
|---------|--------|
| `{schema_files}` | `*.graphql`, `*.gql`, `schema.graphql` |
| `{graphql_deps}` | `graphql`, `apollo-server`, `@apollo/server`, `type-graphql`, `strawberry-graphql`, `ariadne`, `graphene` |
| `{graphql_decorators}` | `@Query`, `@Mutation`, `@Resolver` |

### gRPC (API:gRPC)
| Trigger | Values |
|---------|--------|
| `{proto_files}` | `*.proto`, `proto/` |
| `{grpc_deps}` | `grpcio`, `grpc`, `@grpc/grpc-js`, `protobuf` |
| `{proto_patterns}` | `service `, `rpc `, `message ` in .proto |

### WebSocket (API:WebSocket)
| Trigger | Values |
|---------|--------|
| `{websocket_deps}` | `ws`, `socket.io`, `websockets`, `@fastify/websocket`, `uWebSockets.js` |
| `{websocket_decorators}` | `@WebSocket`, `@SubscribeMessage` |

---

## Database Detection

### SQL (DB:SQL)
| Trigger | Values |
|---------|--------|
| `{sql_drivers}` | `sqlite3`, `psycopg2`, `psycopg`, `asyncpg`, `mysql-connector-python`, `pymysql`, `pg`, `mysql2`, `better-sqlite3` |
| `{sql_files}` | `*.sql`, `migrations/`, `alembic/` |
| `{migrations_dir}` | `migrations/`, `alembic/`, `db/migrate/`, `prisma/migrations/` |
| `{sql_patterns}` | `CREATE TABLE`, `SELECT`, `INSERT INTO` |

### ORM (DB:ORM)
| Trigger | Values |
|---------|--------|
| `{orm_deps}` | `sqlalchemy`, `prisma`, `drizzle-orm`, `typeorm`, `sequelize`, `tortoise-orm`, `peewee`, `gorm`, `diesel`, `mikro-orm`, `kysely` |

### NoSQL (DB:NoSQL)
| Trigger | Values |
|---------|--------|
| `{nosql_deps}` | `pymongo`, `motor`, `redis`, `ioredis`, `dynamodb`, `@aws-sdk/client-dynamodb`, `firebase-admin`, `mongoose`, `cassandra-driver` |

### Vector (DB:Vector)
| Trigger | Values |
|---------|--------|
| `{vector_deps}` | `pgvector`, `pinecone-client`, `chromadb`, `qdrant-client`, `weaviate-client`, `milvus`, `faiss`, `lancedb` |

---

## Frontend Framework Detection

### React (Frontend:React)
| Trigger | Values |
|---------|--------|
| `{react_deps}` | `react`, `react-dom`, `@types/react` |
| `{react_ext}` | `*.jsx`, `*.tsx` |
| `{react_patterns}` | `import React`, `from 'react'`, `useState`, `useEffect` |
| `{react_19}` | `use()` hook, Server Components, `useFormStatus`, `useOptimistic` |

### Vue (Frontend:Vue)
| Trigger | Values |
|---------|--------|
| `{vue_deps}` | `vue`, `@vue/core`, `nuxt` |
| `{vue_ext}` | `*.vue` |
| `{vue_patterns}` | `<template>`, `<script setup>`, `defineComponent` |
| `{vue_35}` | `defineModel`, Vapor mode, `useTemplateRef` |

### Angular (Frontend:Angular)
| Trigger | Values |
|---------|--------|
| `{angular_deps}` | `@angular/core`, `@angular/common`, `@angular/cli` |
| `{angular_ext}` | `*.component.ts`, `*.module.ts`, `*.service.ts` |
| `{angular_patterns}` | `@Component`, `@Injectable`, `@NgModule` |
| `{angular_18}` | `signal()`, `inject()`, standalone components |

### Svelte (Frontend:Svelte)
| Trigger | Values |
|---------|--------|
| `{svelte_deps}` | `svelte`, `@sveltejs/kit` |
| `{svelte_ext}` | `*.svelte` |
| `{svelte_5}` | `$state`, `$derived`, `$effect` (Svelte 5 runes) |

### Solid (Frontend:Solid)
| Trigger | Values |
|---------|--------|
| `{solid_deps}` | `solid-js`, `@solidjs/router` |
| `{solid_patterns}` | `createSignal`, `createEffect`, `createMemo` |

### Astro (Frontend:Astro)
| Trigger | Values |
|---------|--------|
| `{astro_deps}` | `astro`, `@astrojs/` |
| `{astro_ext}` | `*.astro` |
| `{astro_patterns}` | `---` frontmatter, `client:*` directives |

### HTMX (Frontend:HTMX)
| Trigger | Values |
|---------|--------|
| `{htmx_deps}` | `htmx.org` |
| `{htmx_attrs}` | `hx-get`, `hx-post`, `hx-swap`, `hx-target`, `hx-trigger` |

---

## Meta-Framework Detection

### Next.js (Framework:Next)
| Trigger | Values |
|---------|--------|
| `{nextjs_deps}` | `next` |
| `{nextjs_config}` | `next.config.js`, `next.config.mjs`, `next.config.ts` |
| `{nextjs_dirs}` | `app/`, `pages/`, `src/app/` |
| `{nextjs_15}` | Server Actions, `use server`, App Router, Turbopack |

### Nuxt (Framework:Nuxt)
| Trigger | Values |
|---------|--------|
| `{nuxt_deps}` | `nuxt`, `@nuxt/` |
| `{nuxt_config}` | `nuxt.config.ts`, `nuxt.config.js` |
| `{nuxt_4}` | `defineNuxtConfig`, Nitro, auto-imports |

### SvelteKit (Framework:SvelteKit)
| Trigger | Values |
|---------|--------|
| `{sveltekit_deps}` | `@sveltejs/kit` |
| `{sveltekit_config}` | `svelte.config.js` |

### Remix (Framework:Remix)
| Trigger | Values |
|---------|--------|
| `{remix_deps}` | `@remix-run/` |
| `{remix_patterns}` | `loader`, `action`, `meta` exports |

---

## Mobile Detection

### Flutter (Mobile:Flutter)
| Trigger | Values |
|---------|--------|
| `{flutter_manifest}` | `pubspec.yaml` with `flutter` |
| `{flutter_entry}` | `lib/main.dart` |

### React Native (Mobile:ReactNative)
| Trigger | Values |
|---------|--------|
| `{rn_deps}` | `react-native`, `expo` |
| `{rn_config}` | `app.json`, `app.config.js`, `metro.config.js` |

### iOS (Mobile:iOS)
| Trigger | Values |
|---------|--------|
| `{ios_project}` | `*.xcodeproj`, `*.xcworkspace` |
| `{ios_deps}` | `Podfile`, `Package.swift` |

### Android (Mobile:Android)
| Trigger | Values |
|---------|--------|
| `{android_build}` | `build.gradle`, `build.gradle.kts`, `settings.gradle` |
| `{android_manifest}` | `AndroidManifest.xml` |

### Kotlin Multiplatform (Mobile:KMP)
| Trigger | Values |
|---------|--------|
| `{kmp_config}` | `kotlin-multiplatform` plugin in gradle |
| `{kmp_dirs}` | `shared/`, `commonMain/`, `iosMain/`, `androidMain/` |

---

## Desktop Detection

### Electron (Desktop:Electron)
| Trigger | Values |
|---------|--------|
| `{electron_deps}` | `electron`, `electron-builder` |
| `{electron_config}` | `electron-builder.yml`, `electron-builder.json` |

### Tauri (Desktop:Tauri)
| Trigger | Values |
|---------|--------|
| `{tauri_deps}` | `@tauri-apps/api`, `tauri` |
| `{tauri_config}` | `tauri.conf.json`, `src-tauri/` |

---

## Infrastructure Detection

### Docker (Infra:Docker)
| Trigger | Values |
|---------|--------|
| `{container_files}` | `Dockerfile`, `Dockerfile.*`, `docker-compose.yml`, `docker-compose.yaml`, `compose.yml`, `compose.yaml`, `.dockerignore` |
| `{container_exclude}` | Not in `examples/`, `test/`, `tests/`, `e2e/` |

### Kubernetes (Infra:K8s)
| Trigger | Values |
|---------|--------|
| `{k8s_dirs}` | `k8s/`, `kubernetes/`, `helm/`, `charts/` |
| `{k8s_configs}` | `kustomization.yaml`, `Chart.yaml`, `values.yaml` |
| `{k8s_patterns}` | `apiVersion:`, `kind: Deployment`, `kind: Service` |

### Terraform (Infra:Terraform)
| Trigger | Values |
|---------|--------|
| `{tf_files}` | `*.tf`, `*.tf.json` |
| `{tf_state}` | `terraform.tfstate`, `.terraform/` |

### Pulumi (Infra:Pulumi)
| Trigger | Values |
|---------|--------|
| `{pulumi_config}` | `Pulumi.yaml`, `Pulumi.*.yaml` |

### CDK (Infra:CDK)
| Trigger | Values |
|---------|--------|
| `{cdk_config}` | `cdk.json` |
| `{cdk_stack_files}` | `lib/*-stack.ts`, `*Stack.ts` |

### Serverless (Infra:Serverless)
| Trigger | Values |
|---------|--------|
| `{serverless_configs}` | `serverless.yml`, `serverless.yaml`, `sam.yaml`, `template.yaml`, `netlify.toml`, `vercel.json` |

### Edge (Infra:Edge)
| Trigger | Values |
|---------|--------|
| `{edge_configs}` | `wrangler.toml`, `wrangler.jsonc`, `vercel.json` with edge |

### WASM (Infra:WASM)
| Trigger | Values |
|---------|--------|
| `{wasm_ext}` | `*.wasm`, `*.wat` |
| `{wasm_config}` | `wasm-pack.toml` |
| `{wasm_crate_type}` | `crate-type = ["cdylib"]` in Cargo.toml |

---

## Build Tool Detection

### Monorepo (Build:Monorepo)
| Trigger | Values |
|---------|--------|
| `{monorepo_configs}` | `nx.json`, `turbo.json`, `lerna.json`, `rush.json` |
| `{workspace_markers}` | `pnpm-workspace.yaml`, `package.json[workspaces]` |

### Bundler (Build:Bundler)
| Trigger | Values |
|---------|--------|
| `{bundler_configs}` | `vite.config.*`, `webpack.config.*`, `rollup.config.*`, `esbuild.config.*`, `rspack.config.*`, `turbopack` |

### Linter (Build:Linter)
| Trigger | Values |
|---------|--------|
| `{linter_configs}` | `.eslintrc*`, `eslint.config.*`, `biome.json`, `biome.jsonc`, `ruff.toml`, `.ruff.toml`, `oxlint.*`, `.oxlintrc.json` |

### Formatter (Build:Formatter)
| Trigger | Values |
|---------|--------|
| `{formatter_configs}` | `.prettierrc*`, `prettier.config.*`, `biome.json`, `.editorconfig`, `ruff.toml[format]` |

### TypeChecker (Build:TypeChecker)
| Trigger | Values |
|---------|--------|
| `{typechecker_configs}` | `tsconfig.json`, `jsconfig.json`, `mypy.ini`, `pyproject.toml[tool.mypy]`, `pyrightconfig.json` |

---

## Testing Detection

### Unit Testing (Test:Unit)
| Trigger | Values |
|---------|--------|
| `{unit_test_deps}` | `pytest`, `jest`, `vitest`, `mocha`, `ava`, `tap`, `uvu`, `go test` |
| `{test_dirs}` | `tests/`, `test/`, `__tests__/`, `spec/`, `*_test.go` |
| `{test_patterns}` | `test_*.py`, `*_test.py`, `*.test.ts`, `*.spec.ts` |

### E2E Testing (Test:E2E)
| Trigger | Values |
|---------|--------|
| `{e2e_deps}` | `playwright`, `cypress`, `selenium`, `webdriverio`, `puppeteer`, `testcafe` |
| `{e2e_dirs}` | `e2e/`, `cypress/`, `playwright/` |

### Coverage (Test:Coverage)
| Trigger | Values |
|---------|--------|
| `{coverage_configs}` | `[tool.coverage]`, `.nycrc*`, `jest.config.*[coverage]`, `vitest.config.*[coverage]`, `.coveragerc` |

---

## CI/CD Detection

### GitHub Actions (CI:GitHub)
| Trigger | Values |
|---------|--------|
| `{github_workflow_dir}` | `.github/workflows/` |
| `{github_patterns}` | `*.yml`, `*.yaml` in workflows |

### GitLab CI (CI:GitLab)
| Trigger | Values |
|---------|--------|
| `{gitlab_config}` | `.gitlab-ci.yml` |

### Jenkins (CI:Jenkins)
| Trigger | Values |
|---------|--------|
| `{jenkins_config}` | `Jenkinsfile`, `jenkins/` |

### CircleCI (CI:CircleCI)
| Trigger | Values |
|---------|--------|
| `{circleci_config}` | `.circleci/config.yml` |

### Azure DevOps (CI:Azure)
| Trigger | Values |
|---------|--------|
| `{azure_config}` | `azure-pipelines.yml` |

### ArgoCD (CI:ArgoCD)
| Trigger | Values |
|---------|--------|
| `{argocd_dir}` | `argocd/` |
| `{argocd_config}` | `Application.yaml`, `ApplicationSet.yaml` |

---

## ML/AI Detection

### Training (ML:Training)
| Trigger | Values |
|---------|--------|
| `{ml_training_deps}` | `torch`, `pytorch`, `tensorflow`, `keras`, `sklearn`, `scikit-learn`, `jax`, `flax` |
| `{notebook_ext}` | `*.ipynb` |
| `{ml_dirs}` | `models/`, `notebooks/`, `experiments/` |

### LLM Orchestration (ML:LLM)
| Trigger | Values |
|---------|--------|
| `{llm_orchestration_deps}` | `langchain`, `llamaindex`, `llama-index`, `haystack`, `autogen`, `dspy`, `guidance`, `outlines`, `instructor` |
| `{llm_dirs}` | `prompts/`, `chains/`, `agents/` |

### Inference (ML:Inference)
| Trigger | Values |
|---------|--------|
| `{inference_deps}` | `transformers`, `onnxruntime`, `vllm`, `text-generation-inference`, `triton`, `llama.cpp`, `mlx` |

### ML SDK (ML:SDK)
| Trigger | Values |
|---------|--------|
| `{ai_sdk_deps}` | `openai`, `anthropic`, `cohere`, `google-generativeai`, `mistralai`, `together`, `replicate`, `groq` |

---

## Game Detection

### Unity (Game:Unity)
| Trigger | Values |
|---------|--------|
| `{unity_markers}` | `ProjectSettings/`, `Assets/`, `*.unity`, `Assembly-CSharp.csproj` |

### Unreal (Game:Unreal)
| Trigger | Values |
|---------|--------|
| `{unreal_markers}` | `*.uproject`, `Source/`, `Config/DefaultEngine.ini`, `*.Build.cs` |

### Godot (Game:Godot)
| Trigger | Values |
|---------|--------|
| `{godot_markers}` | `project.godot`, `*.gd`, `*.tscn`, `*.tres` |

---

## Specialized Detection

### i18n
| Trigger | Values |
|---------|--------|
| `{i18n_dirs}` | `locales/`, `i18n/`, `translations/`, `lang/` |
| `{i18n_deps}` | `react-i18next`, `i18next`, `vue-i18n`, `formatjs`, `fluent` |

### Real-time (RT:Basic)
| Trigger | Values |
|---------|--------|
| `{websocket_deps}` | (See API:WebSocket) |
| `{sse_patterns}` | `EventSource`, `text/event-stream` |

### Real-time Low-Latency (RT:LowLatency)
| Trigger | Values |
|---------|--------|
| `{binary_protocol_deps}` | `protobuf`, `msgpack`, `flatbuffers`, `capnproto` |
| `{realtime_patterns}` | Binary WebSocket, UDP, WebRTC DataChannel |

---

## Dependency-Based Detection (DEP:*)

### CLI Frameworks (DEP:CLI)
| Trigger | Values |
|---------|--------|
| `{cli_framework_deps}` | `typer`, `click`, `argparse`, `fire`, `argh`, `docopt`, `cement`, `cliff`, `plac`, `cobra`, `urfave/cli`, `clap`, `structopt` |

### TUI (DEP:TUI)
| Trigger | Values |
|---------|--------|
| `{tui_deps}` | `rich`, `textual`, `urwid`, `blessed`, `npyscreen`, `prompt-toolkit`, `questionary`, `inquirer`, `ink`, `bubbletea`, `ratatui` |

### Validation (DEP:Validation)
| Trigger | Values |
|---------|--------|
| `{validation_deps}` | `pydantic`, `attrs`, `marshmallow`, `cerberus`, `voluptuous`, `schema`, `typeguard`, `beartype`, `zod`, `valibot`, `yup`, `joi`, `class-validator`, `effect` |

### Config (DEP:Config)
| Trigger | Values |
|---------|--------|
| `{config_deps}` | `pydantic-settings`, `python-dotenv`, `dynaconf`, `configparser`, `toml`, `omegaconf`, `hydra-core`, `dotenv`, `envalid`, `convict` |

### Testing Frameworks (DEP:Testing)
| Trigger | Values |
|---------|--------|
| `{testing_framework_deps}` | `pytest`, `unittest`, `nose2`, `hypothesis`, `ward`, `robot`, `behave`, `lettuce`, `jest`, `vitest`, `mocha`, `playwright`, `cypress`, `testing-library` |

### Edge Runtime (DEP:Edge)
| Trigger | Values |
|---------|--------|
| `{edge_runtime_deps}` | `@cloudflare/workers-types`, `wrangler`, `@vercel/edge`, `@deno/deploy` |

### Edge Framework (DEP:EdgeFramework)
| Trigger | Values |
|---------|--------|
| `{edge_framework_deps}` | `hono`, `elysia`, `h3`, `nitro`, `itty-router` |

### WASM Toolchain (DEP:WASM)
| Trigger | Values |
|---------|--------|
| `{wasm_toolchain_deps}` | `wasm-pack`, `wasm-bindgen`, `wit-bindgen`, `wasmtime`, `wasmer`, `wazero` |

### HTTP Clients (DEP:HTTP)
| Trigger | Values |
|---------|--------|
| `{http_client_deps}` | `requests`, `httpx`, `aiohttp`, `urllib3`, `axios`, `got`, `ky`, `node-fetch`, `ofetch`, `undici` |

### ORM (DEP:ORM)
| Trigger | Values |
|---------|--------|
| `{orm_deps}` | (See DB:ORM) |

### Auth (DEP:Auth)
| Trigger | Values |
|---------|--------|
| `{auth_deps}` | `authlib`, `python-jose`, `passlib`, `bcrypt`, `passport`, `lucia`, `next-auth`, `auth.js`, `clerk`, `auth0`, `supabase-auth`, `better-auth`, `arctic` |

### Cache (DEP:Cache)
| Trigger | Values |
|---------|--------|
| `{cache_deps}` | `redis`, `ioredis`, `memcached`, `aiocache`, `diskcache`, `keyv`, `cacheable`, `node-cache` |

### Queue (DEP:Queue)
| Trigger | Values |
|---------|--------|
| `{queue_deps}` | `celery`, `rq`, `dramatiq`, `huey`, `bull`, `bullmq`, `bee-queue`, `agenda`, `temporal` |

### Search (DEP:Search)
| Trigger | Values |
|---------|--------|
| `{search_deps}` | `elasticsearch`, `opensearch`, `meilisearch`, `algolia`, `typesense`, `sonic`, `lunr` |

### GPU (DEP:GPU)
| Trigger | Values |
|---------|--------|
| `{gpu_deps}` | `cuda-python`, `cupy`, `torch` with cuda, `tensorflow-gpu`, `numba`, `pycuda`, `triton`, `jax` with gpu |

### Heavy Model (DEP:HeavyModel)
| Trigger | Values |
|---------|--------|
| `{heavy_model_deps}` | `transformers`, `sentence-transformers`, `langchain`, `llama-cpp-python`, `vllm`, `ollama`, `openai`, `anthropic`, `mlx`, `llama-index` |

### Data Processing (DEP:DataHeavy)
| Trigger | Values |
|---------|--------|
| `{data_processing_deps}` | `pandas`, `polars`, `dask`, `pyspark`, `ray`, `vaex`, `modin`, `pyarrow`, `duckdb` |

### Image Processing (DEP:Image)
| Trigger | Values |
|---------|--------|
| `{image_processing_deps}` | `opencv-python`, `pillow`, `PIL`, `scikit-image`, `imageio`, `albumentations`, `kornia`, `sharp` |

### Audio Processing (DEP:Audio)
| Trigger | Values |
|---------|--------|
| `{audio_processing_deps}` | `faster-whisper`, `whisper`, `openai-whisper`, `pydub`, `librosa`, `soundfile`, `pyaudio`, `speechrecognition`, `pedalboard`, `torchaudio` |

### Video Processing (DEP:Video)
| Trigger | Values |
|---------|--------|
| `{video_processing_deps}` | `ffmpeg-python`, `moviepy`, `opencv-video`, `decord`, `av`, `imageio-ffmpeg`, `vidgear` |

### Logging (DEP:Logging)
| Trigger | Values |
|---------|--------|
| `{logging_deps}` | `loguru`, `structlog`, `winston`, `pino`, `bunyan`, `log4js`, `roarr` |

### Object Storage (DEP:ObjectStore)
| Trigger | Values |
|---------|--------|
| `{object_storage_deps}` | `boto3`, `s3`, `minio`, `cloudinary`, `uploadthing`, `google-cloud-storage`, `@aws-sdk/client-s3` |

### Payment (DEP:Payment)
| Trigger | Values |
|---------|--------|
| `{payment_deps}` | `stripe`, `paypal`, `square`, `braintree`, `paddle`, `lemon-squeezy`, `lemonsqueezy`, `adyen` |

### Email (DEP:Email)
| Trigger | Values |
|---------|--------|
| `{email_deps}` | `sendgrid`, `mailgun`, `resend`, `nodemailer`, `postmark`, `ses`, `@aws-sdk/client-ses`, `react-email` |

### SMS (DEP:SMS)
| Trigger | Values |
|---------|--------|
| `{sms_deps}` | `twilio`, `vonage`, `messagebird`, `plivo`, `sinch` |

### Notification (DEP:Notification)
| Trigger | Values |
|---------|--------|
| `{notification_deps}` | `firebase-admin`, `onesignal`, `pusher`, `novu`, `ably`, `knock` |

### PDF (DEP:PDF)
| Trigger | Values |
|---------|--------|
| `{pdf_deps}` | `reportlab`, `weasyprint`, `pdfkit`, `puppeteer`, `playwright`, `fpdf2`, `pdf-lib`, `react-pdf` |

### Excel (DEP:Excel)
| Trigger | Values |
|---------|--------|
| `{excel_deps}` | `openpyxl`, `xlsxwriter`, `pandas` with excel, `exceljs`, `sheetjs`, `xlsx` |

### Scraping (DEP:Scraping)
| Trigger | Values |
|---------|--------|
| `{scraping_deps}` | `scrapy`, `beautifulsoup4`, `bs4`, `selenium`, `playwright`, `puppeteer`, `crawlee`, `cheerio`, `colly` |

### Blockchain (DEP:Blockchain)
| Trigger | Values |
|---------|--------|
| `{blockchain_deps}` | `web3`, `ethers`, `hardhat`, `brownie`, `ape`, `solana-py`, `anchor`, `foundry`, `wagmi`, `viem` |

### Crypto (DEP:Crypto)
| Trigger | Values |
|---------|--------|
| `{crypto_deps}` | `cryptography`, `pycryptodome`, `nacl`, `pynacl`, `jose`, `argon2-cffi`, `bcrypt`, `libsodium` |

### Python Games (DEP:GamePython)
| Trigger | Values |
|---------|--------|
| `{python_game_deps}` | `pygame`, `arcade`, `ursina`, `panda3d`, `pyglet`, `raylib-py` |

### JS Games (DEP:GameJS)
| Trigger | Values |
|---------|--------|
| `{js_game_deps}` | `phaser`, `three`, `three.js`, `pixi.js`, `babylon.js`, `kaboom`, `excalibur`, `playcanvas` |

### Game Engines (DEP:GameEngine)
| Trigger | Values |
|---------|--------|
| `{game_engine_markers}` | (See Game:Unity, Game:Unreal, Game:Godot) |

### AR/VR (DEP:ARVR)
| Trigger | Values |
|---------|--------|
| `{arvr_deps}` | `openxr`, `webxr`, `ar-foundation`, `ar-js`, `a-frame`, `react-xr`, `meta-quest` |

### IoT (DEP:IoT)
| Trigger | Values |
|---------|--------|
| `{iot_deps}` | `micropython`, `paho-mqtt`, `esphome`, `homeassistant`, `aiocoap`, `bleak`, `pyserial`, `node-red` |

---

## API Testing (DEP:APITest)
| Trigger | Values |
|---------|--------|
| `{api_test_deps}` | `bruno`, `httpie`, `insomnia`, `hurl`, `rest-client` |

---

## Type-Safe API (DEP:TypeSafeAPI)
| Trigger | Values |
|---------|--------|
| `{typesafe_api_deps}` | `trpc`, `@trpc/server`, `zodios`, `ts-rest`, `hono/rpc`, `elysia/eden`, `effect` |

---

## Data Query (DEP:DataQuery)
| Trigger | Values |
|---------|--------|
| `{data_query_deps}` | `tanstack-query`, `@tanstack/react-query`, `swr`, `react-query`, `apollo-client`, `urql` |

---

## CSS Solutions (DEP:CSS)
| Trigger | Values |
|---------|--------|
| `{css_deps}` | `tailwindcss`, `unocss`, `styled-components`, `emotion`, `vanilla-extract`, `panda-css`, `open-props` |

---

## State Management (DEP:StateManagement)
| Trigger | Values |
|---------|--------|
| `{state_mgmt_deps}` | `zustand`, `jotai`, `valtio`, `nanostores`, `@tanstack/store`, `xstate`, `recoil`, `effector`, `mobx`, `redux`, `@reduxjs/toolkit`, `pinia`, `vuex` |

---

## Backend Framework Detection

### Python Frameworks (Backend:Python)
| Trigger | Values |
|---------|--------|
| `{django_markers}` | `django`, `django-admin`, `manage.py`, `settings.py`, `urls.py` |
| `{flask_markers}` | `flask`, `Flask(__name__)`, `app.route` |
| `{fastapi_markers}` | `fastapi`, `FastAPI()`, `@app.get`, `@app.post` |

### Node.js Frameworks (Backend:Node)
| Trigger | Values |
|---------|--------|
| `{express_deps}` | `express` |
| `{fastify_deps}` | `fastify`, `@fastify/*` |
| `{hapi_deps}` | `@hapi/hapi` |
| `{koa_deps}` | `koa`, `@koa/*` |
| `{nestjs_deps}` | `@nestjs/core`, `@nestjs/common` |

### Java Frameworks (Backend:Java)
| Trigger | Values |
|---------|--------|
| `{spring_boot_deps}` | `spring-boot-starter*`, `org.springframework.boot` |
| `{quarkus_deps}` | `io.quarkus`, `quarkus-*` |
| `{micronaut_deps}` | `io.micronaut`, `micronaut-*` |

### Ruby Frameworks (Backend:Ruby)
| Trigger | Values |
|---------|--------|
| `{rails_markers}` | `rails`, `config/routes.rb`, `app/controllers/`, `ActiveRecord` |
| `{sinatra_deps}` | `sinatra` |

### PHP Frameworks (Backend:PHP)
| Trigger | Values |
|---------|--------|
| `{laravel_markers}` | `laravel/framework`, `artisan`, `app/Http/Controllers/` |
| `{symfony_deps}` | `symfony/*`, `bin/console` |

### Elixir Frameworks (Backend:Elixir)
| Trigger | Values |
|---------|--------|
| `{phoenix_deps}` | `phoenix`, `phoenix_html`, `phoenix_live_view` |

---

## Observability Detection

### Metrics (Observability:Metrics)
| Trigger | Values |
|---------|--------|
| `{prometheus_config}` | `prometheus.yml`, `prometheus.yaml`, `prometheus/` |
| `{grafana_config}` | `grafana/`, `dashboards/`, `provisioning/` |
| `{datadog_config}` | `datadog.yaml`, `datadog-agent`, `dd-trace` |

### Logging (Observability:Logging)
| Trigger | Values |
|---------|--------|
| `{elk_config}` | `elasticsearch.yml`, `logstash.conf`, `filebeat.yml` |
| `{loki_config}` | `loki-config.yaml`, `promtail-config.yaml` |

### Tracing (Observability:Tracing)
| Trigger | Values |
|---------|--------|
| `{jaeger_config}` | `jaeger-agent`, `jaeger-collector`, `opentelemetry` |
| `{otel_deps}` | `opentelemetry-*`, `@opentelemetry/*`, `otel-*` |

### APM (Observability:APM)
| Trigger | Values |
|---------|--------|
| `{newrelic_config}` | `newrelic.ini`, `newrelic.yml`, `newrelic-agent` |
| `{sentry_deps}` | `sentry-sdk`, `@sentry/*`, `sentry` |

---

## Documentation Detection

### Static Site Generators (Docs:SSG)
| Trigger | Values |
|---------|--------|
| `{docusaurus_config}` | `docusaurus.config.js`, `docusaurus.config.ts`, `sidebars.js` |
| `{vitepress_config}` | `.vitepress/config.ts`, `.vitepress/config.js` |
| `{sphinx_config}` | `conf.py`, `docs/source/`, `_build/` |
| `{mkdocs_config}` | `mkdocs.yml`, `mkdocs.yaml` |
| `{astro_docs}` | `astro.config.*` with `@astrojs/starlight` |

---

## API Specification Detection

### OpenAPI (API:OpenAPI)
| Trigger | Values |
|---------|--------|
| `{openapi_files}` | `openapi.yaml`, `openapi.json`, `swagger.yaml`, `swagger.json`, `*.openapi.yml` |
| `{openapi_dir}` | `openapi/`, `swagger/`, `api-docs/` |

### AsyncAPI (API:AsyncAPI)
| Trigger | Values |
|---------|--------|
| `{asyncapi_files}` | `asyncapi.yaml`, `asyncapi.json`, `asyncapi.yml` |

---

## Task Runner Detection

### Make (Build:Make)
| Trigger | Values |
|---------|--------|
| `{makefile}` | `Makefile`, `makefile`, `GNUmakefile` |

### Just (Build:Just)
| Trigger | Values |
|---------|--------|
| `{justfile}` | `justfile`, `.justfile`, `Justfile` |

### Task (Build:Task)
| Trigger | Values |
|---------|--------|
| `{taskfile}` | `Taskfile.yml`, `Taskfile.yaml`, `taskfile.yml` |

### Mise (Build:Mise)
| Trigger | Values |
|---------|--------|
| `{mise_config}` | `.mise.toml`, `.mise.local.toml`, `mise.toml` |

---

## Deployment Platform Detection

### PaaS (Deploy:PaaS)
| Trigger | Values |
|---------|--------|
| `{fly_config}` | `fly.toml` |
| `{railway_config}` | `railway.json`, `railway.toml` |
| `{render_config}` | `render.yaml`, `render.yml` |
| `{heroku_config}` | `Procfile`, `heroku.yml`, `app.json` |

---

## Container Alternative Detection

### Podman (Infra:Podman)
| Trigger | Values |
|---------|--------|
| `{podman_files}` | `Containerfile`, `podman-compose.yml`, `podman-compose.yaml` |

---

## Conflict Resolution Triggers

*Specific triggers for conflict resolution logic in detection.*

| Trigger | Values | Used For |
|---------|--------|----------|
| `{vitest_config}` | `vitest.config.*`, `vitest.workspace.*` | Jest vs Vitest |
| `{oxlint_config}` | `.oxlintrc.json`, `oxlint.json` | ESLint vs Oxlint |
| `{biome_config}` | `biome.json`, `biome.jsonc` | ESLint/Prettier vs Biome |
| `{ruff_format_config}` | `ruff.toml[format]`, `pyproject.toml[tool.ruff.format]` | Prettier vs ruff |
| `{yarn_lock}` | `yarn.lock` | Package manager detection |
| `{pnpm_lock}` | `pnpm-lock.yaml` | Package manager detection |
| `{bun_lock}` | `bun.lockb` | Package manager detection |

---

## Notes

- Trigger values are case-insensitive for package names
- File patterns use glob syntax
- Multiple values are checked in order (first match wins for conflict resolution)
- Presence of lock file increases confidence by 0.2
- Files in test/example/vendor directories decrease confidence by 0.3
