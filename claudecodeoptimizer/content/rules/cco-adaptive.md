# Adaptive Rules
*Selected by /cco-config based on detection. Each rule evaluated individually.*
*Used as template pool for generating .claude/rules/ files with path-specific frontmatter.*

**[CRITICAL - Single Source Architecture]**
This file is the **ONLY source** for all rule content. Separate rule files do **NOT exist** in the CCO package. When generating rules:
1. Read THIS file (`cco-adaptive.md`)
2. Extract relevant sections based on detections (e.g., `{Lang} (L:{Lang})` section → `{lang}.md`)
3. Generate rule files with extracted content + YAML frontmatter
**Source:** Read only this file (`cco-adaptive.md`) for all rule content.

## Detection System

### Trigger Reference (SSOT)

**All trigger patterns defined in cco-triggers.md** - the single source of truth.
Reference format: `{trigger_name}` maps to values in cco-triggers.md.

### Auto-Detect (Manifest/Code Scan)

Detection organized by category. Trigger values in `{placeholders}` are defined in cco-triggers.md.

| Category | Key Triggers | Output |
|----------|--------------|--------|
| **Languages** |||
| L:Python | {py_manifest}, {py_lock}, {py_ext} | `python.md` |
| L:TypeScript | {js_manifest}, {ts_config}, {ts_ext} | `typescript.md` |
| L:JavaScript | {js_manifest} (no TS), {js_ext} | `javascript.md` |
| L:Go | {go_manifest}, {go_lock}, {go_ext} | `go.md` |
| L:Rust | {rust_manifest}, {rust_lock}, {rust_ext} | `rust.md` |
| L:Java | {java_manifest}, {java_ext} | `java.md` |
| L:Kotlin | {kotlin_ext}, {kotlin_config} | `kotlin.md` |
| L:Swift | {swift_manifest}, {swift_ext} | `swift.md` |
| L:CSharp | {csharp_project}, {csharp_ext} | `csharp.md` |
| L:Ruby | {ruby_manifest}, {ruby_ext} | `ruby.md` |
| L:PHP | {php_manifest}, {php_ext} | `php.md` |
| L:Elixir | {elixir_manifest}, {elixir_ext} | `elixir.md` |
| L:Gleam | {gleam_manifest}, {gleam_ext} | `gleam.md` |
| L:Scala | {scala_manifest}, {scala_ext} | `scala.md` |
| L:Zig | {zig_manifest}, {zig_ext} | `zig.md` |
| L:Dart | {dart_manifest}, {dart_ext} | `dart.md` |
| L:C | {c_manifest}, {c_ext} | `c.md` |
| L:Cpp | {cpp_manifest}, {cpp_ext} | `cpp.md` |
| L:Lua | {lua_manifest}, {lua_ext} | `lua.md` |
| L:Haskell | {haskell_manifest}, {haskell_lock} | `haskell.md` |
| L:FSharp | {fsharp_project}, {fsharp_ext} | `fsharp.md` |
| L:OCaml | {ocaml_manifest}, {ocaml_lock} | `ocaml.md` |
| L:R | {r_manifest}, {r_ext} | `r.md` |
| L:Julia | {julia_manifest}, {julia_lock} | `julia.md` |
| L:Perl | {perl_manifest}, {perl_ext} | `perl.md` |
| L:Clojure | {clojure_manifest}, {clojure_ext} | `clojure.md` |
| L:Erlang | {erlang_manifest}, {erlang_ext} | `erlang.md` |
| **Project Types** |||
| T:CLI | {entry_points}, {cli_deps}, {bin_dir} | `cli.md` |
| T:Library | {export_markers}, {lib_markers} | `library.md` |
| T:Service | {container}, {ports}, {daemon_patterns} | `service.md` |
| **API Styles** |||
| API:REST | {routes_dir}, {rest_decorators} | `api.md` |
| API:GraphQL | {schema_files}, {graphql_deps} | `api.md` |
| API:gRPC | {proto_files}, {grpc_deps} | `api.md` |
| API:WebSocket | {websocket_deps}, {websocket_decorators} | `api.md` |
| API:OpenAPI | {openapi_files}, {openapi_dir} | `api.md` |
| API:AsyncAPI | {asyncapi_files} | `api.md` |
| **Database** |||
| DB:SQL | {sql_drivers}, {migrations_dir} | `database.md` |
| DB:ORM | {orm_deps} | `database.md` |
| DB:NoSQL | {nosql_deps} | `database.md` |
| DB:Vector | {vector_deps} | `database.md` |
| DB:Edge | {edge_db_deps} | `database.md` |
| ORM:Exposed | {exposed_deps} | `orm.md` |
| DB:Operations | DB:* (auto) | `backend-data.md` |
| **Backend Operations** |||
| Ops:Full | T:Service + CI:* | `backend-ops.md` |
| Ops:Basic | T:CLI + CI:* | `backend-ops.md` |
| **Frontend** |||
| Frontend:React | {react_deps}, {react_ext} | `frontend.md` |
| Frontend:Vue | {vue_deps}, {vue_ext} | `frontend.md` |
| Frontend:Svelte | {svelte_deps}, {svelte_ext} | `frontend.md` |
| Frontend:Angular | {angular_deps}, {angular_ext} | `frontend.md` |
| Frontend:Solid | {solid_deps} | `frontend.md` |
| Frontend:Astro | {astro_deps}, {astro_ext} | `frontend.md` |
| Frontend:HTMX | {htmx_deps}, {htmx_attrs} | `frontend.md` |
| Frontend:Qwik | {qwik_deps} | `frontend.md` |
| Frontend:Blazor | {blazor_deps} | `frontend.md` |
| **Mobile** |||
| Mobile:Flutter | {flutter_manifest}, {dart_ext} | `mobile.md` |
| Mobile:ReactNative | {rn_deps}, {rn_config} | `mobile.md` |
| Mobile:iOS | {ios_project}, {swift_ext} | `mobile.md` |
| Mobile:Android | {android_build}, {android_manifest} | `mobile.md` |
| Mobile:KMP | {kmp_config}, {kmp_dirs} | `mobile.md` |
| **Infrastructure** |||
| Infra:Docker | {container_files} | `container.md` |
| Infra:Podman | {podman_files} | `container.md` |
| Infra:K8s | {k8s_dirs}, {k8s_configs} | `k8s.md` |
| Infra:Terraform | {tf_files} | `terraform.md` |
| Infra:Pulumi | {pulumi_config} | `pulumi.md` |
| Infra:CDK | {cdk_config}, {cdk_stack_files} | `cdk.md` |
| Infra:Edge | {edge_configs} | `edge.md` |
| Infra:WASM | {wasm_ext}, {wasm_config} | `wasm.md` |
| Infra:Serverless | {serverless_configs} | `serverless.md` |
| **ML/AI** |||
| ML:Training | {ml_training_deps} | `ml.md` |
| ML:LLM | {llm_orchestration_deps} | `ml.md` |
| ML:Inference | {inference_deps} | `ml.md` |
| ML:SDK | {ai_sdk_deps} | `ml.md` |
| **Build** |||
| Build:Monorepo | {monorepo_configs} | `monorepo.md` |
| Build:Bundler | {bundler_configs} | `bundler.md` |
| Build:Linter | {linter_configs} | `linter.md` |
| Build:Formatter | {formatter_configs} | `formatter.md` |
| Build:TypeChecker | {typechecker_configs} | `typechecker.md` |
| Build:Make | {makefile} | `taskrunner.md` |
| Build:Just | {justfile} | `taskrunner.md` |
| Build:Task | {taskfile} | `taskrunner.md` |
| Build:Mise | {mise_config} | `taskrunner.md` |
| **Backend Frameworks** |||
| Backend:Django | {django_markers} | `backend.md` |
| Backend:Flask | {flask_markers} | `backend.md` |
| Backend:FastAPI | {fastapi_markers} | `backend.md` |
| Backend:Express | {express_deps} | `backend.md` |
| Backend:Fastify | {fastify_deps} | `backend.md` |
| Backend:NestJS | {nestjs_deps} | `backend.md` |
| Backend:Spring | {spring_boot_deps} | `backend.md` |
| Backend:Rails | {rails_markers} | `backend.md` |
| Backend:Laravel | {laravel_markers} | `backend.md` |
| Backend:Phoenix | {phoenix_deps} | `backend.md` |
| Backend:Hapi | {hapi_deps} | `backend.md` |
| Backend:Koa | {koa_deps} | `backend.md` |
| Backend:Sinatra | {sinatra_deps} | `backend.md` |
| Backend:Symfony | {symfony_deps} | `backend.md` |
| Backend:Quarkus | {quarkus_deps} | `backend.md` |
| Backend:Micronaut | {micronaut_deps} | `backend.md` |
| Backend:Gin | {gin_deps} | `backend.md` |
| Backend:Echo | {echo_deps} | `backend.md` |
| Backend:Fiber | {fiber_deps} | `backend.md` |
| Backend:Actix | {actix_deps} | `backend.md` |
| Backend:Axum | {axum_deps} | `backend.md` |
| Backend:Rocket | {rocket_deps} | `backend.md` |
| Backend:Warp | {warp_deps} | `backend.md` |
| Backend:Chi | {chi_deps} | `backend.md` |
| Backend:Gorilla | {gorilla_deps} | `backend.md` |
| Backend:AspNetCore | {aspnet_markers} | `backend.md` |
| Backend:Ktor | {ktor_deps} | `backend.md` |
| Backend:Vapor | {vapor_deps} | `backend.md` |
| **Message Queues** |||
| MQ:Kafka | {kafka_deps}, {kafka_config} | `messagequeue.md` |
| MQ:RabbitMQ | {rabbitmq_deps}, {rabbitmq_config} | `messagequeue.md` |
| MQ:NATS | {nats_deps} | `messagequeue.md` |
| MQ:SQS | {sqs_deps} | `messagequeue.md` |
| MQ:PubSub | {pubsub_deps} | `messagequeue.md` |
| **Observability** |||
| Observability:Prometheus | {prometheus_config} | `observability.md` |
| Observability:Grafana | {grafana_config} | `observability.md` |
| Observability:Datadog | {datadog_config} | `observability.md` |
| Observability:ELK | {elk_config} | `observability.md` |
| Observability:Jaeger | {jaeger_config} | `observability.md` |
| Observability:OpenTelemetry | {otel_deps} | `observability.md` |
| Observability:Sentry | {sentry_deps} | `observability.md` |
| Observability:NewRelic | {newrelic_config}, {newrelic_deps} | `observability.md` |
| Observability:Splunk | {splunk_config}, {splunk_deps} | `observability.md` |
| Observability:Dynatrace | {dynatrace_config}, {dynatrace_deps} | `observability.md` |
| **Documentation** |||
| Docs:Docusaurus | {docusaurus_config} | `documentation.md` |
| Docs:VitePress | {vitepress_config} | `documentation.md` |
| Docs:Sphinx | {sphinx_config} | `documentation.md` |
| Docs:MkDocs | {mkdocs_config} | `documentation.md` |
| **Deployment** |||
| Deploy:Fly | {fly_config} | `deployment.md` |
| Deploy:Railway | {railway_config} | `deployment.md` |
| Deploy:Render | {render_config} | `deployment.md` |
| Deploy:Heroku | {heroku_config} | `deployment.md` |
| Deploy:Vercel | {vercel_config} | `deployment.md` |
| Deploy:Netlify | {netlify_config} | `deployment.md` |
| Deploy:CloudRun | {gcp_cloudrun} | `deployment.md` |
| Deploy:AzureWebApp | {azure_webapp} | `deployment.md` |
| Deploy:AppRunner | {aws_apprunner} | `deployment.md` |
| **Infrastructure Tools** |||
| Infra:Ansible | {ansible_config}, {ansible_patterns} | `infra-tools.md` |
| Infra:Consul | {consul_config}, {consul_patterns} | `infra-tools.md` |
| Infra:Vault | {vault_config}, {vault_patterns} | `infra-tools.md` |
| **Desktop** |||
| Desktop:Electron | {electron_deps}, {electron_config} | `desktop.md` |
| Desktop:Tauri | {tauri_deps}, {tauri_config} | `desktop.md` |
| **Runtimes** |||
| R:Node | {node_markers} | `node.md` |
| R:Bun | {bun_markers} | `bun.md` |
| R:Deno | {deno_markers} | `deno.md` |
| **Testing** |||
| Test:Unit | {unit_test_deps}, {test_dirs} | `testing.md` |
| Test:E2E | {e2e_deps}, {e2e_dirs} | `testing.md` |
| Test:Coverage | {coverage_configs} | `testing.md` |
| **CI/CD** |||
| CI:GitHub | {github_workflow_dir} | `ci-cd.md` |
| CI:GitLab | {gitlab_config} | `ci-cd.md` |
| CI:Jenkins | {jenkins_config} | `ci-cd.md` |
| CI:CircleCI | {circleci_config} | `ci-cd.md` |
| CI:Azure | {azure_config} | `ci-cd.md` |
| CI:ArgoCD | {argocd_dir}, {argocd_config} | `ci-cd.md` |
| **Meta-Frameworks** |||
| Framework:Next | {nextjs_deps}, {nextjs_config} | `nextjs.md` |
| Framework:Nuxt | {nuxt_deps}, {nuxt_config} | `nuxt.md` |
| Framework:SvelteKit | {sveltekit_deps}, {sveltekit_config} | `sveltekit.md` |
| Framework:Remix | {remix_deps}, {remix_patterns} | `remix.md` |
| **Specialized** |||
| Game:Unity | {unity_markers} | `game.md` |
| Game:Unreal | {unreal_markers} | `game.md` |
| Game:Godot | {godot_markers} | `game.md` |
| i18n | {i18n_dirs}, {i18n_deps} | `i18n.md` |
| RT:Basic | {websocket_deps}, {sse_patterns} | `realtime.md` |
| RT:LowLatency | {binary_protocol_deps}, {realtime_patterns} | `realtime.md` |
| **DEP:* (55 categories)** | See Dependency-Based Rules section below ||
| DEP:CLI | {cli_framework_deps} | `dep-cli.md` |
| DEP:TUI | {tui_deps} | `dep-tui.md` |
| DEP:Validation | {validation_deps} | `dep-validation.md` |
| DEP:Config | {config_deps} | `dep-config.md` |
| DEP:Testing | {testing_framework_deps} | `dep-testing.md` |
| DEP:Edge | {edge_runtime_deps} | `dep-edge.md` |
| DEP:EdgeFramework | {edge_framework_deps} | `dep-edgeframework.md` |
| DEP:WASM | {wasm_toolchain_deps} | `dep-wasm.md` |
| DEP:HTTP | {http_client_deps} | `dep-http.md` |
| DEP:ORM | {orm_deps} | `dep-orm.md` |
| DEP:Auth | {auth_deps} | `dep-auth.md` |
| DEP:Cache | {cache_deps} | `dep-cache.md` |
| DEP:Queue | {queue_deps} | `dep-queue.md` |
| DEP:Workflow | {workflow_deps} | `dep-workflow.md` |
| DEP:Search | {search_deps} | `dep-search.md` |
| DEP:GPU | {gpu_deps} | `dep-gpu.md` |
| DEP:HeavyModel | {heavy_model_deps} | `dep-heavymodel.md` |
| DEP:DataHeavy | {data_processing_deps} | `dep-data.md` |
| DEP:Image | {image_processing_deps} | `dep-image.md` |
| DEP:Audio | {audio_processing_deps} | `dep-audio.md` |
| DEP:Video | {video_processing_deps} | `dep-video.md` |
| DEP:Logging | {logging_deps} | `dep-logging.md` |
| DEP:ObjectStore | {object_storage_deps} | `dep-storage.md` |
| DEP:Payment | {payment_deps} | `dep-payment.md` |
| DEP:Email | {email_deps} | `dep-email.md` |
| DEP:SMS | {sms_deps} | `dep-sms.md` |
| DEP:Notification | {notification_deps} | `dep-notification.md` |
| DEP:PDF | {pdf_deps} | `dep-pdf.md` |
| DEP:Excel | {excel_deps} | `dep-excel.md` |
| DEP:Scraping | {scraping_deps} | `dep-scraping.md` |
| DEP:Blockchain | {blockchain_deps} | `dep-blockchain.md` |
| DEP:SmartContractEVM | {solidity_deps}, {solidity_config} | `dep-smartcontract-evm.md` |
| DEP:SmartContractSolana | {anchor_deps}, {anchor_config} | `dep-smartcontract-solana.md` |
| DEP:Crypto | {crypto_deps} | `dep-crypto.md` |
| DEP:GamePython | {python_game_deps} | `dep-game-python.md` |
| DEP:GameJS | {js_game_deps} | `dep-game-js.md` |
| DEP:GameEngine | {game_engine_markers} | `dep-gameengine.md` |
| DEP:ARVR | {arvr_deps} | `dep-arvr.md` |
| DEP:IoT | {iot_deps} | `dep-iot.md` |
| DEP:APITest | {api_test_deps} | `dep-apitest.md` |
| DEP:TypeSafeAPI | {typesafe_api_deps} | `dep-typesafe-api.md` |
| DEP:DataQuery | {data_query_deps} | `dep-data-query.md` |
| DEP:CSS | {css_deps} | `dep-css.md` |
| DEP:WebSocket | {websocket_deps} | `dep-websocket.md` |
| DEP:StateManagement | {state_mgmt_deps} | `dep-state.md` |
| DEP:AIAgent | {ai_agent_deps} | `dep-ai-agent.md` |
| DEP:CDC | {cdc_deps} | `dep-cdc.md` |
| DEP:DBMigrations | {db_migration_deps} | `dep-dbmigrations.md` |
| DEP:ErrorTracking | {error_tracking_deps} | `dep-errortracking.md` |
| DEP:FeatureFlags | {feature_flag_deps} | `dep-featureflags.md` |
| DEP:GraphQLTools | {graphql_tools_deps} | `dep-graphql.md` |
| DEP:HeadlessCMS | {headless_cms_deps} | `dep-headlesscms.md` |
| DEP:IncidentMgmt | {incident_deps} | `dep-incident.md` |
| DEP:LocalFirst | {local_first_deps} | `dep-localfirst.md` |
| DEP:SchemaRegistry | {schema_registry_deps} | `dep-schemaregistry.md` |
| DEP:Effect | {effect_deps} | `dep-effect.md` |
| DEP:AISDK | {ai_sdk_deps} | `dep-aisdk.md` |
| DEP:FormValidation | {form_validation_deps} | `dep-formvalidation.md` |
| DEP:TanStack | {tanstack_deps} | `dep-tanstack.md` |
| **Infra:* (3 categories)** |||
| Infra:APIGateway | {api_gateway_config}, {api_gateway_deps} | `infra-apigateway.md` |
| Infra:ServiceMesh | {service_mesh_config}, {service_mesh_deps} | `infra-servicemesh.md` |
| Infra:BuildCache | {build_cache_config} | `infra-buildcache.md` |

### User-Input (AskUserQuestion) [MANDATORY]

**CRITICAL:** Ask these questions explicitly. User input is required for accurate configuration.

| Element | Options (hint = AskUserQuestion description) | Default | Affects | Ask |
|---------|-----------------------------------------------|---------|---------|-----|
| Team | Solo (no review); 2-5 (async PR); 6+ (ADR/CODEOWNERS) | Solo | Team rules | **MUST** |
| Scale | Prototype (<100, dev only); Small (100+, basic cache); Medium (1K+, pools/async); Large (10K+, circuit breakers) | Small | Scale rules | **MUST** |
| Data | Public (open); PII (personal data); Regulated (healthcare/finance) | Public | Security rules | **MUST** |
| Compliance | None; SOC2; HIPAA; PCI; GDPR; CCPA; ISO27001; FedRAMP; DORA; HITRUST | None | Compliance rules | **MUST** |
| Testing | Basics (60%, unit); Standard (80%, +integration); Full (90%, +E2E) | Standard | Testing rules | Confirm `[detected]` |
| SLA | None (best effort); 99% (~7h/mo); 99.9% (~43min/mo); 99.99% (~4min/mo) | None | Observability rules | **MUST** |
| Maturity | Prototype (may discard); Active (regular releases); Stable (maintenance); Legacy (minimal changes) | Active | Guidelines | **MUST** |
| Breaking | Allowed (v0.x); Minimize (deprecate first); Never (enterprise) | Minimize | Guidelines | **MUST** |
| Priority | Speed (ship fast); Balanced (standard); Quality (thorough); Security (security-first) | Balanced | Guidelines | **MUST** |

**Execution:** Split into 2 AskUserQuestion calls (max 4 questions each).

#### User-Input Descriptions

**Team:** How many people actively contribute?
- Solo: Single developer, no review process needed
- 2-5: Small team, async PR reviews work well
- 6+: Large team, needs ADR, CODEOWNERS, formal process

**Scale:** Expected concurrent users or requests/second?
- Prototype (<100): Dev/testing only, no production traffic
- Small (100+): Early production, basic caching helps
- Medium (1K+): Growth stage, connection pooling and async needed
- Large (10K+): High traffic, circuit breakers and API versioning required

**Data:** Most sensitive data your system handles?
- Public: Open data, no login required
- PII: Personal data (names, emails, addresses) - activates security rules
- Regulated: Healthcare (HIPAA), financial (PCI), government - strictest rules

**Compliance:** Required compliance frameworks? (multi-select)
- SOC2: B2B SaaS with enterprise customers
- HIPAA: US healthcare data (PHI)
- PCI: Payment card processing
- GDPR: EU user data, privacy rights
- CCPA: California consumer privacy
- ISO27001: International security standard
- FedRAMP: US government cloud
- DORA: EU financial services (2025+)
- HITRUST: Healthcare + security combined

**Testing:** Test coverage level?
- Basics (60%): Unit tests, basic mocking
- Standard (80%): + Integration tests, fixtures, CI gates
- Full (90%): + E2E, contract testing, mutation testing

**SLA:** Uptime commitment?
- None: Best effort, no formal SLA
- 99%: ~7h downtime/month, basic monitoring
- 99.9%: ~43min/month, needs redundancy
- 99.99%: ~4min/month, multi-region, chaos testing

**Maturity:** Project development stage? (guideline only)
- Prototype: Proof of concept, may be discarded
- Active: Ongoing development, regular releases
- Stable: Feature-complete, maintenance mode
- Legacy: Old codebase, minimal changes

**Breaking:** How to handle breaking changes? (guideline only)
- Allowed: OK in any release (v0.x projects)
- Minimize: Deprecate first, provide migration path (v1.x+)
- Never: Zero breaking changes (enterprise libraries)

**Priority:** Primary development focus? (guideline only)
- Speed: Ship fast, iterate quickly
- Balanced: Standard practices, reasonable coverage
- Quality: Thorough testing, extensive review
- Security: Security-first, threat modeling

**Maturity/Breaking/Priority** are guidelines stored in context.md, not separate rule files.

---

## Dependency Sources

| Language | Manifest Files | Parse Method |
|----------|---------------|--------------|
| Python | pyproject.toml, requirements.txt, setup.py, Pipfile | TOML/text |
| Node | package.json | JSON (dependencies + devDependencies) |
| Go | go.mod | require block |
| Rust | Cargo.toml | [dependencies] section |

---

## Path Pattern Templates

When generating rule files, use YAML frontmatter with `paths:` for conditional loading.

### Tier 1: Always Apply (No Frontmatter)

These rules apply universally - no `paths:` needed:

| File | Reason |
|------|--------|
| `context.md` | Project context, tools, conventions |
| `core.md` | SSOT, DRY, YAGNI, KISS - universal principles |
| `ai.md` | Read-First, Parallel - AI behavior rules |

### Tier 2: Language Rules

| Output | Paths |
|--------|-------|
| `python.md` | `"**/*.py"` |
| `typescript.md` | `"**/*.{ts,tsx,mts,cts}"` |
| `javascript.md` | `"**/*.{js,jsx,mjs,cjs}"` |
| `go.md` | `"**/*.go"` |
| `rust.md` | `"**/*.rs"` |
| `java.md` | `"**/*.java"` |
| `kotlin.md` | `"**/*.{kt,kts}"` |
| `swift.md` | `"**/*.swift"` |
| `csharp.md` | `"**/*.{cs,csx}"` |
| `ruby.md` | `"**/*.rb"` |
| `php.md` | `"**/*.php"` |
| `elixir.md` | `"**/*.{ex,exs}"` |
| `gleam.md` | `"**/*.gleam"` |
| `scala.md` | `"**/*.{scala,sc}"` |
| `zig.md` | `"**/*.zig"` |
| `dart.md` | `"**/*.dart"` |
| `c.md` | `"**/*.{c,h}"` |
| `cpp.md` | `"**/*.{cpp,hpp,cc,hh,cxx,hxx}"` |
| `lua.md` | `"**/*.lua"` |
| `haskell.md` | `"**/*.{hs,lhs}"` |
| `fsharp.md` | `"**/*.{fs,fsi,fsx}"` |
| `ocaml.md` | `"**/*.{ml,mli}"` |
| `r.md` | `"**/*.{r,R}"` |
| `julia.md` | `"**/*.jl"` |
| `perl.md` | `"**/*.{pl,pm}"` |
| `clojure.md` | `"**/*.{clj,cljs,cljc,edn}"` |
| `erlang.md` | `"**/*.{erl,hrl}"` |

### Tier 3: Frontend Frameworks (No Frontmatter)

Framework patterns apply beyond component files (hooks, composables, stores, context):

| File | Reason |
|------|--------|
| `react.md` | Hooks, Context, state patterns in *.ts files |
| `vue.md` | Composables, Pinia stores, Provide/Inject in *.ts files |
| `svelte.md` | Stores, runes, actions in *.ts files |
| `angular.md` | Services, DI, RxJS patterns in *.ts files |
| `solid.md` | Signals, createEffect, stores in *.ts files |
| `astro.md` | Island architecture, data fetching patterns |
| `qwik.md` | Resumability, QRL patterns, useTask in *.ts files |
| `htmx.md` | Server response patterns, hypermedia API design |

### Tier 4: Infrastructure

| Output | Paths |
|--------|-------|
| `container.md` | `"**/Dockerfile*, **/docker-compose*.{yml,yaml}, **/compose*.{yml,yaml}"` |
| `k8s.md` | `"**/k8s/**/*.{yml,yaml}, **/*.k8s.{yml,yaml}, **/kubernetes/**/*"` |
| `terraform.md` | `"**/*.tf, **/*.tfvars"` |
| `pulumi.md` | `"**/Pulumi.{yml,yaml}, **/Pulumi*.ts"` |
| `serverless.md` | `"**/serverless.{yml,yaml}, **/serverless/**/*"` |
| `cdk.md` | `"**/cdk.json, **/lib/*-stack.ts"` |

### Tier 5: Cross-Cutting (No Frontmatter)

These apply across file types - no `paths:` restriction:

| File | Reason |
|------|--------|
| `api.md` | Applies to route handlers in any language |
| `database.md` | Applies to data layer in any language |
| `mobile.md` | Platform-specific, complex file patterns |
| `cli.md` | Entry points vary by language |
| `library.md` | Export patterns vary by language |
| `service.md` | Service patterns are cross-cutting |
| `backend.md` | Django/FastAPI/Express patterns span views, models, services, middleware |
| `ml.md` | Training, inference, data patterns span multiple file types |
| `messagequeue.md` | Producer/consumer patterns in any service file |
| `observability.md` | Tracing, logging, metrics patterns affect all code |
| `next.md` | App Router, Server Actions patterns beyond components |
| `nuxt.md` | Nitro, auto-imports, composables patterns everywhere |
| `sveltekit.md` | Load functions, hooks patterns beyond .svelte |
| `remix.md` | Loader/action patterns beyond components |

### Tier 6: Testing & CI

| Output | Paths |
|--------|-------|
| `testing.md` | `"**/*.{test,spec}.*, **/test_*.*, **/*_test.*, **/tests/**/*"` |
| `ci-cd.md` | `"**/.github/**/*.{yml,yaml}, **/.gitlab-ci.yml, **/azure-pipelines.yml, **/.circleci/**/*"` |

### Tier 7: Config-Specific (With Paths)

These are truly file-specific - config or content files only:

| Output | Paths |
|--------|-------|
| `monorepo.md` | `"**/turbo.json, **/pnpm-workspace.yaml, **/lerna.json, **/nx.json"` |
| `bundler.md` | `"**/vite.config.*, **/webpack.config.*, **/rollup.config.*"` |
| `game.md` | No paths (engine-specific, complex detection) |
| `wasm.md` | `"**/*.{wat,wasm}, **/wasm/**/*"` |
| `documentation.md` | `"**/docs/**/*.{md,mdx}, **/docusaurus.config.*, **/mkdocs.yml"` |
| `deployment.md` | `"**/fly.toml, **/render.yaml, **/vercel.json, **/netlify.toml"` |

### Example Generated File

```markdown
---
paths: "**/*.py"
---
# Python Rules
*Trigger: L:Python*

- **Modern-Types**: Use `str | None` (3.10+), `list[str]` (3.9+)
- **Async-Await**: async/await for I/O operations
...
```

---

## Language Rules

### Python (L:Python)
**Trigger:** {py_manifest}, {py_ext}

- **Modern-Types**: Use `str | None` (3.10+), `list[str]` (3.9+). Avoid `Optional`, `List`, `Dict` from typing
- **Async-Await**: async/await for I/O operations, avoid blocking in async context
- **Context-Managers**: Use `with` statement for resource management (files, connections)
- **Import-Order**: stdlib > third-party > local (isort compatible)
- **Exception-Chain**: Use `raise X from Y` for exception chaining
- **F-Strings**: Prefer f-strings over .format() or % formatting
- **Dataclasses**: Use dataclasses, attrs, or Pydantic for data containers. Use slots=True for memory efficiency
- **Comprehensions**: Prefer list/dict comprehensions for simple transformations
- **Pydantic-Validators**: Use `@field_validator` for custom validation, `BeforeValidator` for normalization
- **Pydantic-Bounds**: Always set Field(min_length=1, max_length=N) for strings
- **Pydantic-Strict**: Use strict=True on models for no implicit coercion where appropriate
- **Enum-StrEnum**: Use StrEnum for string enums with auto case handling
- **Match-Case**: Use match-case for complex conditionals (3.10+)
- **Walrus-Operator**: Use := for assignment expressions where it improves readability
- **Subprocess-Encoding**: Always use `encoding='utf-8', errors='replace'` in subprocess.run() for cross-platform output handling

### TypeScript (L:TypeScript)
**Trigger:** {ts_config}, {ts_ext}

- **Strict-Mode**: Enable strict in tsconfig.json
- **Explicit-Return**: Return types on public functions
- **No-Any**: Avoid any, use unknown for truly unknown types
- **Null-Safety**: Strict null checks enabled
- **Index-Access**: Enable noUncheckedIndexedAccess for array/object safety
- **Utility-Types**: Use Partial, Pick, Omit, Required for type transformations
- **Discriminated-Unions**: Use discriminated unions for type-safe state management
- **Satisfies-Operator**: Use satisfies for type validation without widening (TS 4.9+)
- **Const-Type-Params**: Use const type parameters for literal inference (TS 5.0+)
- **Using-Keyword**: Use using for explicit resource management (TS 5.2+)
- **Branded-Types**: Use branded types for validated primitives (UserId, Email)

### JavaScript (L:JavaScript)
**Trigger:** {js_manifest}, {js_ext}

- **JSDoc-Types**: Type hints via JSDoc for public APIs
- **ES-Modules**: ESM over CommonJS (import/export)
- **Const-Default**: const > let > never var
- **Async-Handling**: Proper Promise handling, always catch rejections
- **Array-Methods**: Prefer map/filter/reduce over manual loops
- **Optional-Chain**: Use ?. and ?? for safe property access
- **Destructuring**: Destructure objects/arrays for clarity
- **Top-Level-Await**: Use top-level await in modules
- **Private-Fields**: Use # for private class fields
- **Modern-Array**: Use Array.at(), Object.hasOwn(), Array.findLast()

### Go (L:Go)
**Trigger:** {go_manifest}, {go_ext}

- **Error-Wrap**: Wrap errors with context (fmt.Errorf %w)
- **Interface-Small**: Small, focused interfaces (1-3 methods)
- **Context-Pass**: Pass context.Context as first parameter for cancellation
- **Goroutine-Safe**: Channel or sync primitives for concurrency
- **Defer-Cleanup**: defer for cleanup operations
- **Table-Tests**: Table-driven tests for comprehensive coverage
- **Generics**: Use generics for type-safe collections and utilities (Go 1.18+)
- **Slog-Logging**: Use slog for structured logging (Go 1.21+)
- **Range-Int**: Use range over integers for simple loops (Go 1.22+)

### Rust (L:Rust)
**Trigger:** {rust_manifest}, {rust_ext}

- **Result-Propagate**: Use ? operator for error propagation
- **Ownership-Clear**: Clear ownership patterns, minimize clones
- **Clippy-Clean**: No clippy warnings in CI
- **Unsafe-Minimize**: Minimize unsafe blocks, document when necessary
- **Async-Traits**: Use async fn in traits (Rust 1.75+)
- **Let-Chains**: Use let chains for complex conditionals
- **Error-Thiserror**: Use thiserror for library errors, anyhow for applications

### Java (L:Java)
**Trigger:** {java_manifest}, {java_ext}

- **Null-Safety**: Use Optional<T> for nullable returns
- **Resource-Try**: try-with-resources for AutoCloseable
- **Immutable-Prefer**: Prefer immutable objects, final fields
- **Stream-API**: Use Stream API for collection transformations
- **Records**: Use records for immutable data carriers (Java 14+)
- **Pattern-Switch**: Use pattern matching in switch (Java 21+)
- **Virtual-Threads**: Use virtual threads for high-concurrency I/O (Java 21+)
- **Sealed-Classes**: Use sealed classes for controlled inheritance

### Kotlin (L:Kotlin)
**Trigger:** {kotlin_config}, {kotlin_ext}

- **Null-Safe**: Use nullable types (?), avoid !! operator
- **Data-Class**: Data classes for DTOs and value objects
- **Coroutine-Structured**: Structured concurrency with coroutineScope
- **Extension-Limit**: Extension functions for utility, not core logic

### Swift (L:Swift)
**Trigger:** {swift_manifest}, {ios_project}, {swift_ext}

- **Optional-Guard**: Use guard let for early exits
- **Protocol-Oriented**: Protocol-oriented design over inheritance
- **Value-Type**: Prefer structs over classes when possible
- **Actor-Concurrency**: Use actors for shared mutable state
- **Async-Await**: Use async/await for asynchronous code
- **Observation**: Use @Observable macro for reactive state (iOS 17+)
- **Result-Builder**: Use result builders for DSLs

### C# (L:CSharp)
**Trigger:** {csharp_project}, {csharp_ext}

- **Nullable-Enable**: Enable nullable reference types
- **Async-Await**: async/await for I/O operations
- **Dispose-Pattern**: IDisposable with using statements
- **Record-Type**: Records for immutable data transfer
- **Primary-Constructors**: Use primary constructors for DI (C# 12+)
- **Collection-Expressions**: Use collection expressions [...] (C# 12+)
- **Pattern-Matching**: Use pattern matching for type checks and deconstruction

### Ruby (L:Ruby)
**Trigger:** {ruby_manifest}, {ruby_ext}

- **Freeze-Strings**: Use frozen_string_literal pragma
- **Block-Yield**: Prefer yield over block.call
- **Method-Visibility**: Explicit private/protected declarations
- **Type-Check**: Static type checking (Sorbet or RBS) for public APIs
- **Pattern-Match**: Use pattern matching for complex conditionals (Ruby 3.0+)
- **Ractor-Thread-Safe**: Use Ractor for thread-safe parallelism (Ruby 3.0+)
- **Data-Class**: Use Data.define for immutable value objects (Ruby 3.2+)

### PHP (L:PHP)
**Trigger:** {php_manifest}, {php_ext}

- **Type-Declare**: Strict type declarations (declare(strict_types=1))
- **PSR-Standards**: Follow PSR-4 autoloading, PSR-12 style
- **Null-Safe**: Use null coalescing (??) and null-safe operator (?->)
- **Constructor-Promotion**: Property promotion in constructors (8.0+)
- **Enums**: Use native enums for fixed value sets (8.1+)
- **Readonly-Properties**: Use readonly for immutable properties (8.1+)
- **Attributes**: Use attributes instead of docblock annotations (8.0+)

### Elixir (L:Elixir)
**Trigger:** {elixir_manifest}, {elixir_ext}

- **Pattern-Match**: Pattern matching over conditionals
- **Pipe-Operator**: Use |> for data transformations
- **GenServer-State**: Stateful processes via GenServer
- **Dialyzer-Types**: Typespecs for public functions

### Gleam (L:Gleam)
**Trigger:** {gleam_manifest}, {gleam_ext}

- **Result-Type**: Use Result(a, e) for fallible operations
- **Pattern-Exhaustive**: Exhaustive pattern matching
- **Pipeline-Style**: Use |> for function composition
- **Label-Args**: Use labelled arguments for clarity

### Scala (L:Scala)
**Trigger:** {scala_manifest}, {scala_ext}

- **Option-Not-Null**: Option[T] instead of null
- **Case-Class**: Case classes for immutable data
- **For-Comprehension**: For-comprehensions for monadic operations
- **Implicit-Minimal**: Minimize implicit conversions

### Zig (L:Zig)
**Trigger:** {zig_manifest}, {zig_ext}

- **Error-Union**: Use error unions for fallible functions
- **Comptime**: Leverage comptime for zero-cost abstractions
- **No-Hidden-Alloc**: Explicit allocator passing
- **Defer-Cleanup**: defer/errdefer for cleanup

### Dart (L:Dart)
**Trigger:** {dart_manifest}, {dart_ext}

- **Null-Safety**: Sound null safety with ? and !
- **Async-Await**: async/await for Future operations
- **Named-Params**: Named parameters for readability
- **Immutable-Widget**: StatelessWidget when state not needed

### C (L:C)
**Trigger:** {c_manifest}, {c_ext}

- **Memory-Manual**: Explicit malloc/free, check null returns
- **Buffer-Safe**: Use safe string functions (strncpy, snprintf)
- **Const-Correct**: const for read-only parameters and returns
- **Header-Guards**: Include guards or #pragma once
- **Static-Analysis**: Use clang-tidy, cppcheck in CI
- **Valgrind-Test**: Memory leak detection in tests
- **Compiler-Warnings**: Enable -Wall -Wextra -Werror

### C++ (L:Cpp)
**Trigger:** {cpp_manifest}, {cpp_ext}

- **RAII-Pattern**: Resource acquisition is initialization
- **Smart-Pointers**: unique_ptr/shared_ptr over raw pointers
- **Move-Semantics**: std::move for efficient transfers
- **Const-Ref**: const& for read-only parameters
- **Modern-Features**: Use modern standards features (concepts, ranges, modules)
- **STL-Algorithms**: Prefer STL algorithms over manual loops
- **Exception-Safe**: Strong exception safety guarantee
- **Static-Analysis**: Use clang-tidy, cppcheck in CI

### Lua (L:Lua)
**Trigger:** {lua_manifest}, {lua_ext}

- **Local-Variables**: local by default, minimize globals
- **Module-Pattern**: Use module pattern for encapsulation
- **Table-Pool**: Reuse tables to reduce GC pressure
- **Metatables**: Use metatables for OOP patterns
- **Error-Handling**: pcall/xpcall for error handling
- **LuaJIT-Compat**: Write LuaJIT-compatible code when targeting it

### Haskell (L:Haskell)
**Trigger:** {haskell_manifest}, {haskell_ext}

- **Pure-Functions**: Prefer pure functions, isolate IO
- **Type-Signatures**: Explicit type signatures for top-level
- **Monad-Transform**: Monad transformers for effect stacking
- **Lazy-Strict**: Use strict where appropriate (BangPatterns, seq)
- **Lens-Optics**: Use lens/optics for nested data
- **Property-Tests**: QuickCheck for property-based testing

### F# (L:FSharp)
**Trigger:** {fsharp_project}, {fsharp_ext}

- **Immutable-Default**: Prefer immutable data
- **Pipeline-Style**: Use |> for function composition
- **Pattern-Match**: Pattern matching over conditionals
- **Async-Workflows**: Use async workflows for I/O
- **Type-Inference**: Leverage type inference, explicit when needed
- **Interop-Safe**: Safe C# interop patterns

### OCaml (L:OCaml)
**Trigger:** {ocaml_manifest}, {ocaml_ext}

- **Module-System**: Leverage module system for encapsulation
- **Functors**: Use functors for parameterized modules
- **Pattern-Complete**: Complete pattern matching
- **Result-Type**: Use Result for error handling
- **Dune-Build**: Use dune for build system
- **PPX-Derive**: Use ppx_deriving for boilerplate

### R (L:R)
**Trigger:** {r_manifest}, {r_ext}

- **Tidyverse-Style**: Follow tidyverse style guide
- **Vector-Ops**: Vectorized operations over loops
- **Package-Namespace**: Explicit namespace (pkg::func)
- **Renv-Manage**: Use renv for reproducible environments
- **Roxygen-Docs**: roxygen2 for documentation
- **Testthat-Tests**: Use testthat for testing

### Julia (L:Julia)
**Trigger:** {julia_manifest}, {julia_ext}

- **Type-Stability**: Write type-stable functions for performance
- **Multiple-Dispatch**: Leverage multiple dispatch
- **Broadcasting**: Use dot syntax for broadcasting
- **Pkg-Environment**: Project-specific environments
- **Docstrings**: Triple-quoted docstrings
- **Precompile**: Use precompilation for packages

### Perl (L:Perl)
**Trigger:** {perl_manifest}, {perl_ext}

- **Strict-Warnings**: Always use strict; use warnings;
- **Modern-Perl**: Use modern Perl features (say, given/when)
- **CPAN-Modules**: Prefer CPAN modules over reinventing
- **POD-Docs**: POD for documentation
- **Taint-Mode**: Taint mode for untrusted input
- **Test-More**: Test::More for testing

### Clojure (L:Clojure)
**Trigger:** {clojure_manifest}, {clojure_ext}

- **Immutable-First**: Leverage immutable data structures by default
- **Pure-Functions**: Pure functions over side effects, isolate I/O
- **REPL-Driven**: REPL-driven development workflow
- **Spec-Validate**: Use clojure.spec for data validation and documentation
- **Namespaces**: Namespace per file, clear require/import
- **Threading-Macros**: Use -> and ->> for readability
- **Protocols-Multimethods**: Protocols for polymorphism, multimethods for open dispatch
- **Atoms-Refs**: Atoms for uncoordinated state, refs for coordinated transactions
- **Core-Async**: core.async for async programming patterns
- **Deps-Edn**: Prefer deps.edn over Leiningen for new projects

### Erlang (L:Erlang)
**Trigger:** {erlang_manifest}, {erlang_ext}

- **OTP-Patterns**: Use OTP behaviors (gen_server, gen_statem, supervisor)
- **Let-It-Crash**: Fail fast, let supervisors handle recovery
- **Message-Passing**: Message passing for process communication
- **Pattern-Match**: Pattern matching in function heads
- **Tail-Recursion**: Tail-recursive functions for loops
- **Hot-Code**: Design for hot code reloading
- **ETS-Mnesia**: ETS for fast lookups, Mnesia for distributed state
- **Dialyzer-Types**: Type specs for Dialyzer analysis
- **Rebar3-Build**: Use rebar3 for build management
- **PropEr-Test**: Property-based testing with PropEr or EQC

---

## Security Rules
**Trigger:** D:PII | D:Regulated | Scale:Large | Compliance:*

- **Input-Validation**: Validate ALL user input at system boundaries. Use schema validation. Reject invalid, don't sanitize-and-continue
- **Input-Bounds**: Set max lengths, max sizes, max items on ALL user inputs. Prevent resource exhaustion
- **Input-Whitespace**: Normalize whitespace (strip, reject whitespace-only). Common injection vector
- **SQL-Safe**: Parameterized queries only, no string concatenation
- **Command-Safe**: Never shell=True with user input. Use subprocess with list args, escape with shlex.quote
- **XSS-Prevent**: Sanitize output + CSP headers
- **CSRF-Protect**: CSRF tokens for state-changing operations
- **Auth-Verify**: Verify authentication on every request
- **Rate-Limit**: Per-user/IP limits on public endpoints
- **Secure-Headers**: X-Frame-Options, X-Content-Type-Options, HSTS
- **Encrypt-Rest**: AES-256 for PII/sensitive data at rest
- **Encrypt-Transit**: TLS 1.2+ for all network communication
- **Deps-Scan**: Automated dependency vulnerability scanning in CI
- **Audit-Log**: Immutable logging for security-critical actions
- **CORS-Strict**: Explicit origins, no wildcard in production
- **Path-Validate**: Validate file paths, prevent traversal (../, symlinks)
- **Enum-Validate**: Validate enum values server-side, don't trust client
- **SSRF-Prevent**: Validate URLs, block internal IPs, use allowlists for external calls
- **Deserialize-Safe**: Deserialize only trusted data using safe formats (JSON, not pickle/yaml)
- **JWT-Validate**: Validate signature, issuer, audience, expiry. Use asymmetric keys for public APIs
- **Upload-Validate**: Validate file type, size, content. Store outside webroot, generate new filenames

---

## Compliance Rules
**Trigger:** Compliance != None (multi-select, cumulative)

### Base Compliance (Any)
- **Data-Classification**: Classify data by sensitivity level
- **Access-Control**: Role-based access with least privilege
- **Incident-Response**: Documented incident response plan

### SOC2
- **SOC2-Audit-Trail**: Complete audit trail for all data access
- **SOC2-Change-Mgmt**: Documented change management process
- **SOC2-Access-Review**: Quarterly access reviews

### HIPAA
- **HIPAA-PHI-Encrypt**: Encrypt PHI at rest and in transit
- **HIPAA-BAA**: Business Associate Agreements for vendors
- **HIPAA-Access-Log**: Log all PHI access with user, time, purpose
- **HIPAA-Minimum**: Minimum necessary access to PHI

### PCI-DSS
- **PCI-Card-Mask**: Mask PAN (show only last 4 digits)
- **PCI-No-Storage**: Store only masked payment data, exclude CVV/CVC
- **PCI-Network-Seg**: Network segmentation for cardholder data
- **PCI-Key-Mgmt**: Cryptographic key management procedures

### GDPR
- **GDPR-Consent**: Explicit consent with purpose specification
- **GDPR-Right-Access**: Implement data subject access requests
- **GDPR-Right-Delete**: Implement right to erasure
- **GDPR-Data-Portability**: Export user data in portable format
- **GDPR-Breach-Notify**: 72-hour breach notification procedure

### CCPA
- **CCPA-Opt-Out**: "Do Not Sell" opt-out mechanism
- **CCPA-Disclosure**: Disclose categories of data collected
- **CCPA-Delete**: Honor deletion requests within 45 days

### ISO27001
- **ISO-Risk-Assess**: Regular risk assessments
- **ISO-Asset-Inventory**: Maintain information asset inventory
- **ISO-Policy-Docs**: Documented security policies

### FedRAMP
- **FedRAMP-Boundary**: Documented system boundary
- **FedRAMP-Continuous**: Continuous monitoring implementation
- **FedRAMP-FIPS**: FIPS 140-2 validated cryptography

### DORA (EU Financial)
- **DORA-ICT-Risk**: ICT risk management framework
- **DORA-Incident**: Major ICT incident reporting
- **DORA-Resilience**: Digital operational resilience testing

### HITRUST
- **HITRUST-CSF**: Align with HITRUST CSF controls
- **HITRUST-Inherit**: Leverage inherited controls from providers

---

## Scale Rules
**Inheritance:** Higher tiers include all lower tier rules.

### Small (Scale:100+)
- **Caching**: TTL + invalidation strategy for data fetching
- **Lazy-Load**: Defer loading of non-critical resources

### Medium (Scale:1K+)
- **Conn-Pool**: Connection pooling with appropriate sizing
- **Async-IO**: Non-blocking I/O operations

### Large (Scale:10K+ | Architecture:Microservices)
- **Circuit-Breaker**: Fail-fast pattern for external services
- **Idempotency**: Safe retries for write operations
- **API-Version**: Version in URL or header for public APIs
- **Compression**: gzip/brotli for large responses

---

## Team Rules
**Inheritance:** Larger teams include smaller team rules.

### Small (Team:2-5)
- **PR-Review**: Async code review on all changes
- **README-Contributing**: Clear contribution guidelines

### Large (Team:6+)
- **ADR**: Architecture Decision Records for significant decisions
- **CODEOWNERS**: Clear ownership via CODEOWNERS file
- **PR-Templates**: Standardized PR descriptions
- **Branch-Protection**: Require reviews before merge

---

## Testing Rules
**Inheritance:** Higher tiers include lower.

### Basics (Testing:60%)
- **Unit-Isolated**: Fast, deterministic unit tests
- **Mocking**: Isolate tests from external dependencies
- **Coverage-60**: Minimum 60% line coverage

### Standard (Testing:80%)
- **Integration**: Test component interactions
- **Fixtures**: Reusable, maintainable test data
- **Coverage-80**: Minimum 80% line coverage
- **CI-on-PR**: Tests run on every PR
- **Edge-Cases-Standard**: Test empty, None, single item, typical, boundary values

### Full (Testing:90%)
- **E2E**: End-to-end tests for critical user flows
- **Contract**: Consumer-driven contract testing (if Architecture:Microservices)
- **Mutation**: Mutation testing for test effectiveness (if Priority:Quality)
- **Coverage-90**: Minimum 90% line coverage
- **Edge-Cases-Full**: Test whitespace-only, unicode, max+1, state combinations, concurrent access

### Edge Case Checklist [MANDATORY - ALL TIERS]
When generating tests, always include:
- **Empty/None**: empty string, None, empty list/dict
- **Whitespace**: spaces, tabs, newlines, whitespace-only strings
- **Boundaries**: 0, 1, max, max+1, negative (if applicable)
- **Type Variations**: string vs int representations, case variations for strings
- **State Combinations**: all valid state pairs where multiple states can interact
- **Unicode**: emojis, RTL text, special characters (if string handling)
- **Timing**: expired dates, future dates, boundary timestamps

---

## SLA-Based Observability (Observability:SLA)
**Trigger:** SLA level selected in user input
**Inheritance:** Higher SLA includes lower.

### Basics (SLA:Any)
- **Error-Tracking**: Sentry or similar error tracking
- **Critical-Alerts**: Immediate notification for critical errors

### Standard (SLA:99%+)
- **Correlation-ID**: Request tracing across services
- **RED-Metrics**: Rate, Error, Duration dashboards
- **Distributed-Trace**: OpenTelemetry/Jaeger for multi-service

### HA (SLA:99.9%+)
- **Redundancy**: No single point of failure
- **Auto-Failover**: Automatic recovery mechanisms
- **Runbooks**: Documented incident response

### Critical (SLA:99.99%+)
- **Multi-Region**: Geographic redundancy
- **Chaos-Engineering**: Fault injection testing
- **DR-Tested**: Disaster recovery procedures tested

---

## Backend Frameworks
**Trigger:** Backend framework detected

### Express (Backend:Express)
**Trigger:** {express_deps}

- **Middleware-Order**: Middleware order matters, error handlers last
- **Router-Modular**: Use express.Router for modular routes
- **Request-Validation**: Validate request body with middleware
- **Error-Handler**: Centralized error handling middleware
- **Security-Headers**: Use helmet for security headers
- **CORS-Config**: Explicit CORS configuration

### Fastify (Backend:Fastify)
**Trigger:** {fastify_deps}

- **Plugin-System**: Leverage plugin system for modularity
- **Schema-Validation**: JSON schema for request/response validation
- **Hooks-Lifecycle**: Use lifecycle hooks for cross-cutting concerns
- **Reply-Type**: Set reply type for automatic serialization
- **Decorator-Register**: Register reusable decorators

### Hapi (Backend:Hapi)
**Trigger:** {hapi_deps}

- **Plugin-Structure**: Plugins for feature organization
- **Validation-Joi**: Joi schemas for request validation
- **Auth-Strategies**: Multiple auth strategies support
- **Lifecycle-Ext**: Lifecycle extensions for middleware-like behavior
- **Pre-Handlers**: Pre-handlers for request preprocessing

### Koa (Backend:Koa)
**Trigger:** {koa_deps}

- **Middleware-Cascade**: Composition over configuration via middleware
- **Context-Object**: Pass context through middleware chain
- **Async-Await**: Native async/await support
- **Error-Handling**: Centralized error handling middleware
- **Body-Parsing**: Body parsing middleware configuration

### NestJS (Backend:NestJS)
**Trigger:** {nestjs_deps}

- **Module-Dependency**: Dependency injection via modules
- **Controller-Service**: Clear separation of controllers and services
- **Guard-Interceptor**: Guards for authorization, interceptors for transformation
- **Exception-Filter**: Custom exception filters
- **Decorator-Custom**: Custom decorators for validation/transformation

### Django (Backend:Django)
**Trigger:** {django_markers}

- **MTV-Pattern**: Model-Template-View pattern
- **ORM-Queries**: Optimize QuerySets, avoid N+1
- **Middleware-Order**: Middleware order matters
- **Settings-Split**: Split settings by environment
- **Management-Commands**: Custom management commands
- **Signals-Sparingly**: Use signals sparingly, prefer explicit

### Flask (Backend:Flask)
**Trigger:** {flask_markers}

- **Blueprint-Modular**: Blueprints for modular routes
- **Factory-Pattern**: Application factory pattern
- **Extension-Config**: Configure extensions properly
- **Context-Locals**: Understand application and request context
- **Error-Handler**: Centralized error handlers

### FastAPI (Backend:FastAPI)
**Trigger:** {fastapi_markers}

- **Pydantic-Models**: Pydantic for request/response validation
- **Dependency-Injection**: Use Depends for DI
- **Async-Endpoints**: async def for I/O-bound endpoints
- **OpenAPI-Auto**: Automatic OpenAPI documentation
- **Background-Tasks**: Background tasks for non-blocking ops

### Spring Boot (Backend:Spring)
**Trigger:** {spring_boot_deps}

- **Starter-Deps**: Use spring-boot-starter-* for curated dependencies
- **Properties-Config**: application.properties or application.yml
- **Component-Scan**: Component scanning for automatic bean discovery
- **AOP-Aspects**: Aspect-oriented programming for cross-cutting concerns
- **Actuator-Monitoring**: Spring Boot Actuator for monitoring endpoints

### Quarkus (Backend:Quarkus)
**Trigger:** {quarkus_deps}

- **Native-First**: Build native image for fast startup
- **Config-Externalize**: Externalized configuration via properties
- **Extension-Model**: Leverage Quarkus extensions for integration
- **GraalVM-Compatible**: Ensure GraalVM compatibility
- **Dev-Mode**: Fast iterative development mode

### Micronaut (Backend:Micronaut)
**Trigger:** {micronaut_deps}

- **Compile-Time-DI**: Compile-time dependency injection (no reflection)
- **Http-Client**: Declarative HTTP client
- **Config-Management**: Configuration management and environment properties
- **Bean-Introspection**: Compile-time bean introspection
- **Build-Time-Optimization**: Optimized for serverless/microservices

### Rails (Backend:Rails)
**Trigger:** {rails_markers}

- **Convention-Config**: Convention over configuration
- **Active-Record**: Active Record patterns and queries
- **Concerns-Extract**: Extract shared behavior to concerns
- **Strong-Params**: Strong parameters for mass assignment protection
- **Background-Jobs**: Active Job for background processing
- **Turbo-Hotwire**: Modern frontend with Turbo/Hotwire

### Laravel (Backend:Laravel)
**Trigger:** {laravel_markers}

- **Eloquent-ORM**: Eloquent patterns and relationships
- **Service-Container**: Leverage service container for DI
- **Middleware-Auth**: Middleware for authentication/authorization
- **Queue-Jobs**: Queued jobs for background processing
- **Artisan-Commands**: Custom artisan commands
- **Blade-Templates**: Blade templating best practices

### Phoenix (Backend:Phoenix)
**Trigger:** {phoenix_deps}

- **Context-Module**: Contexts for business logic organization
- **LiveView-First**: LiveView for real-time UI
- **Channels-Realtime**: Channels for WebSocket communication
- **Ecto-Queries**: Ecto for database operations
- **Pub-Sub**: PubSub for event broadcasting

### Sinatra (Backend:Sinatra)
**Trigger:** {sinatra_deps}

- **Route-Definition**: Simple route DSL
- **Middleware-Stack**: Middleware stack for request handling
- **Template-Engine**: Template engine selection and configuration
- **Error-Handling**: Error handlers and error templates
- **Helper-Methods**: Helper methods for view/route logic

### Symfony (Backend:Symfony)
**Trigger:** {symfony_deps}

- **Bundle-Organization**: Bundles for code organization
- **Console-Commands**: Symfony Console for CLI commands
- **Service-Container**: Service container for dependency injection
- **Event-System**: Event system for loose coupling
- **Doctrine-ORM**: Doctrine ORM integration

### Gin (Backend:Gin)
**Trigger:** {gin_deps}

- **Middleware-Chain**: Middleware for logging, auth, recovery
- **Group-Routes**: Route groups for API versioning
- **Binding-Validation**: ShouldBind for request validation
- **Context-Values**: Use c.Set/c.Get for request-scoped values
- **Graceful-Shutdown**: os.Signal for graceful shutdown
- **Recovery-Middleware**: Use gin.Recovery for panic handling

### Echo (Backend:Echo)
**Trigger:** {echo_deps}

- **Middleware-Stack**: Built-in middleware for common needs
- **Validator-Integration**: Use echo.Validator for validation
- **Binder-Custom**: Custom binders for complex requests
- **Context-Extension**: Extend context for custom data
- **Static-Files**: Static file serving with cache headers

### Fiber (Backend:Fiber)
**Trigger:** {fiber_deps}

- **Fasthttp-Based**: Leverage fasthttp performance
- **Middleware-Use**: Use built-in middleware stack
- **Prefork-Mode**: Prefork for multi-core utilization
- **Storage-Drivers**: Session storage with multiple drivers
- **Rate-Limiter**: Built-in rate limiting middleware

### Chi (Backend:Chi)
**Trigger:** {chi_deps}

- **Context-Native**: Use chi.URLParam with stdlib context
- **Middleware-Chain**: Compose middleware with Use/With
- **Route-Groups**: Group routes with common middleware
- **Pattern-Routing**: URL parameters with {param} syntax
- **Graceful-Shutdown**: Built-in graceful shutdown support
- **Lightweight**: Minimal dependencies, stdlib compatible

### Gorilla Mux (Backend:Gorilla)
**Trigger:** {gorilla_deps}

- **Route-Matching**: Path variables with {name} or {name:pattern}
- **Method-Matching**: Methods().Handler() for HTTP method routing
- **Subrouters**: PathPrefix() for route grouping
- **Middleware-Wrapper**: Use() for middleware registration
- **Host-Matching**: Host() for virtual host routing
- **Query-Matching**: Queries() for query parameter matching

### Actix-web (Backend:Actix)
**Trigger:** {actix_deps}

- **Actor-System**: Use actors for concurrent state
- **Extractors-Type**: Type-safe extractors for requests
- **Middleware-Wrap**: Wrap services with middleware
- **State-Shared**: Web::Data for shared application state
- **Error-Handling**: Implement ResponseError for custom errors
- **Async-Handlers**: async fn for all request handlers

### Axum (Backend:Axum)
**Trigger:** {axum_deps}

- **Tower-Based**: Leverage tower middleware ecosystem
- **Extractors-Order**: Extractor order matters (body last)
- **State-Extension**: Extension for request-local state
- **Router-Nest**: Nest routers for modularity
- **Error-Into-Response**: Implement IntoResponse for errors
- **Layer-Stack**: Layer stack for cross-cutting concerns

### Rocket (Backend:Rocket)
**Trigger:** {rocket_deps}

- **Fairings-Lifecycle**: Fairings for lifecycle hooks
- **Guards-Request**: Request guards for validation
- **Responders-Custom**: Custom responders for responses
- **Managed-State**: Managed state for application data
- **Config-Environment**: Environment-based configuration
- **Catchers-Error**: Error catchers for custom error pages

### Warp (Backend:Warp)
**Trigger:** {warp_deps}

- **Filter-Composition**: Compose filters with and/or/map
- **Rejection-Handling**: Custom rejection handlers for errors
- **Path-Extraction**: Type-safe path parameter extraction
- **Body-Parsing**: JSON/form body parsing with filters
- **TLS-Support**: Built-in TLS with rustls
- **Streaming**: Stream responses with hyper integration

### ASP.NET Core (Backend:AspNetCore)
**Trigger:** {aspnet_markers}

- **Dependency-Injection**: Built-in DI container
- **Middleware-Pipeline**: Request pipeline configuration
- **Minimal-API**: Minimal APIs for simple endpoints
- **Options-Pattern**: IOptions for configuration
- **Health-Checks**: Built-in health check endpoints
- **Logging-Structured**: Structured logging with ILogger
- **EF-Core**: Entity Framework Core for data access
- **Identity-Auth**: ASP.NET Identity for authentication

### Blazor (Frontend:Blazor)
**Trigger:** {blazor_deps}

- **Render-Mode**: Choose Server vs WebAssembly vs Auto based on use case
- **Component-Parameters**: Use [Parameter] for component inputs
- **Cascading-Values**: Use CascadingParameter for deep prop passing
- **JS-Interop**: IJSRuntime for JavaScript calls, minimize usage
- **State-Container**: Scoped services for state management
- **Virtualize**: Use Virtualize component for large lists
- **EditForm-Validation**: EditForm with DataAnnotations validation
- **Auth-State**: AuthenticationStateProvider for auth handling
- **Streaming-Rendering**: Use streaming rendering for slow data

### Ktor (Backend:Ktor)
**Trigger:** {ktor_deps}

- **Plugins-System**: Install plugins for features
- **Routing-DSL**: Type-safe routing DSL
- **Serialization-Content**: Content negotiation for serialization
- **Authentication-Plugins**: Authentication via plugins
- **Client-Same-API**: Same API for client and server
- **Coroutines-Native**: Native coroutines support

### Exposed (ORM:Exposed)
**Trigger:** {exposed_deps}

- **DSL-vs-DAO**: Use DSL for complex queries, DAO for simple CRUD
- **Transaction-Block**: Wrap operations in transaction {} block
- **Lazy-Loading**: Configure lazy loading for relationships
- **Batch-Insert**: Use batchInsert for bulk operations
- **Schema-Generation**: Use SchemaUtils for DDL generation
- **Coroutines-Support**: Use newSuspendedTransaction for coroutines

### Vapor (Backend:Vapor)
**Trigger:** {vapor_deps}

- **Fluent-ORM**: Fluent ORM for database operations
- **Middleware-Chain**: Middleware for request processing
- **Leaf-Templates**: Leaf templating engine
- **Async-Await**: Swift async/await for handlers
- **Validation-Request**: Request validation with Validatable
- **Environment-Config**: Environment-based configuration

---

## Message Queues
**Trigger:** Message queue detected

### Kafka (MQ:Kafka)
**Trigger:** {kafka_deps}

- **Consumer-Groups**: Use consumer groups for scaling
- **Offset-Management**: Commit offsets explicitly for reliability
- **Exactly-Once**: Enable idempotent producer for exactly-once
- **Partition-Strategy**: Partition key strategy for ordering
- **Schema-Registry**: Use schema registry for message schemas
- **Dead-Letter**: Dead letter topics for failed messages
- **Replication-Factor**: Set replication factor for durability
- **Retention-Policy**: Configure retention based on use case

### RabbitMQ (MQ:RabbitMQ)
**Trigger:** {rabbitmq_deps}

- **Exchange-Types**: Use appropriate exchange types (direct, topic, fanout)
- **Queue-Durability**: Durable queues for persistence
- **Prefetch-Count**: Set prefetch for fair dispatch
- **Dead-Letter-Exchange**: DLX for failed messages
- **Acknowledgements**: Manual acks for reliability
- **Connection-Pool**: Pool connections, not channels
- **TTL-Messages**: Message TTL for expiration

### NATS (MQ:NATS)
**Trigger:** {nats_deps}

- **Subject-Hierarchy**: Use hierarchical subjects
- **JetStream-Persistence**: JetStream for persistence
- **Queue-Groups**: Queue groups for load balancing
- **Request-Reply**: Request-reply for RPC pattern
- **Stream-Retention**: Configure stream retention
- **Consumer-Durable**: Durable consumers for reliability

### AWS SQS (MQ:SQS)
**Trigger:** {sqs_deps}

- **Visibility-Timeout**: Set appropriate visibility timeout
- **Dead-Letter-Queue**: Configure DLQ for failed messages
- **Batch-Operations**: Use batch send/receive for efficiency
- **Long-Polling**: Enable long polling to reduce costs
- **FIFO-Ordering**: FIFO queues for ordering requirements
- **Message-Dedup**: Deduplication for exactly-once

### Google Pub/Sub (MQ:PubSub)
**Trigger:** {pubsub_deps}

- **Subscription-Types**: Push vs pull subscriptions
- **Acknowledgement-Deadline**: Set appropriate ack deadline
- **Dead-Letter-Topic**: Configure dead letter topic
- **Ordering-Keys**: Ordering keys for message ordering
- **Filter-Messages**: Use subscription filters
- **Snapshot-Seek**: Snapshots for replay capability

---

## Backend > API
**Trigger:** API:REST | API:GraphQL | API:gRPC

- **REST-Methods**: Proper HTTP verbs and status codes
- **Pagination**: Cursor-based pagination for lists
- **OpenAPI-Spec**: Synced spec with examples
- **Error-Format**: Consistent format, no stack traces in prod
- **Contract-Minimal**: Expose only what consumers need. Small, focused endpoints over catch-all APIs

### GraphQL Extension
**Trigger:** API:GraphQL

- **GQL-Limits**: Query depth and complexity limits
- **GQL-Persisted**: Persisted queries in production

### gRPC Extension
**Trigger:** API:gRPC

- **Proto-Version**: Backward compatible proto changes

### OpenAPI Extension (API:OpenAPI)
**Trigger:** {openapi_files}, {openapi_dir}

- **Schema-Sync**: Keep OpenAPI spec in sync with actual implementation
- **Version-Path**: Support multiple API versions in spec (v1, v2)
- **Examples-Complete**: Include request/response examples for all endpoints
- **Validation-Tooling**: Use schema validation in CI pipeline
- **Docs-Generation**: Auto-generate docs from spec (Swagger UI, ReDoc)

### AsyncAPI Extension (API:AsyncAPI)
**Trigger:** {asyncapi_files}

- **Event-Schema**: Keep AsyncAPI spec in sync with actual events
- **Version-Evolution**: Track schema evolution across message versions
- **Payload-Examples**: Include message payload examples
- **Bindings-Defined**: Define protocol bindings (Kafka, AMQP, WebSocket)
- **Docs-Generation**: Generate documentation from spec

### API Evolution
**Trigger:** API:REST | API:GraphQL | API:gRPC | T:Library

- **Deprecate-Before-Remove**: Mark deprecated for 1+ versions before removal
- **Migration-Guide**: Breaking changes include migration instructions in changelog
- **Version-Boundary**: Breaking changes only in major versions (unless v0.x)
- **Alias-Bridge**: Provide aliases/redirects during transition period
- **Sunset-Header**: Include Sunset header for deprecated endpoints

---

## Database Operations (DB:Operations)
**Trigger:** DB:* (auto-applied when any DB:* detected)

- **Backup-Strategy**: Automated backups with tested restore
- **Schema-Versioned**: Migration files with rollback plan
- **Connection-Secure**: SSL/TLS, credentials in env vars
- **Query-Timeout**: Prevent runaway queries

---

## Backend Operations (Ops:*)
**Trigger:** T:Service + CI:* | T:CLI + CI:*

### Full Operations (Ops:Full)
**Trigger:** T:Service + CI:*
- **Config-as-Code**: Versioned, environment-aware config
- **Health-Endpoints**: /health + /ready endpoints
- **Graceful-Shutdown**: Drain connections on SIGTERM
- **Observability**: Metrics + logs + traces
- **CI-Gates**: lint + test + coverage gates
- **Zero-Downtime**: Blue-green or canary deployments
- **Feature-Flags**: Decouple deploy from release

### Basic Operations (Ops:Basic)
**Trigger:** T:CLI + CI:*
- **Config-as-Code**: Versioned configuration
- **CI-Gates**: lint + test + coverage gates

---

## Apps > CLI
**Trigger:** T:CLI

- **Help-Examples**: --help with usage examples
- **Exit-Codes**: 0=success, N=specific error codes
- **Signal-Handle**: Graceful SIGINT/SIGTERM handling
- **Output-Modes**: Human-readable + --json option
- **Config-Precedence**: env > file > args > defaults
- **NO_COLOR-Respect**: Check NO_COLOR env var before ANSI output, use isatty() to detect terminal
- **Unicode-Fallback**: Use ASCII alternatives for box-drawing chars (╔═╗ → +--+) when terminal encoding uncertain
- **Batch-UTF8**: In .bat/.cmd files, use `chcp 65001` for UTF-8 and avoid Unicode box characters

---

## Apps > Library
**Trigger:** T:Library

- **Minimal-Deps**: Minimize transitive dependencies
- **Tree-Shakeable**: ESM with no side effects (JS/TS)
- **Types-Included**: TypeScript types or JSDoc
- **Deprecation-Path**: Warn before removing APIs

---

## Apps > Service
**Trigger:** T:Service (Dockerfile + ports, long-running process)

- **Health-Endpoints**: /health + /ready endpoints for orchestrators
- **Graceful-Shutdown**: Handle SIGTERM, drain connections before exit
- **Config-External**: Configuration via env vars or config files, not hardcoded
- **Logging-Structured**: JSON logging with correlation IDs
- **Metrics-Export**: Prometheus-compatible metrics endpoint
- **Connection-Pool**: Reuse database/HTTP connections
- **Timeout-Set**: Explicit timeouts on all external calls
- **Retry-Backoff**: Exponential backoff for transient failures

---

## Apps > Mobile
**Trigger:** iOS/Android/RN/Flutter detected

- **Offline-First**: Local-first with sync capability
- **Battery-Optimize**: Minimize background work and wake locks
- **Deep-Links**: Universal links / app links
- **Platform-Guidelines**: iOS HIG / Material Design compliance

---

## Apps > Desktop
**Trigger:** Electron/Tauri detected

- **Auto-Update**: Silent updates with manual option
- **Native-Integration**: System tray, notifications
- **Memory-Cleanup**: Prevent memory leaks in long-running apps

---

## Infrastructure > Container
**Trigger:** Dockerfile detected (not in examples/test/)

- **Multi-Stage**: Separate build and runtime stages
- **Non-Root**: Run as non-root user
- **CVE-Scan**: Automated scanning in CI
- **Resource-Limits**: CPU/memory bounds
- **Distroless**: Minimal attack surface for production

---

## Infrastructure > K8s
**Trigger:** Kubernetes/Helm detected

- **Security-Context**: Non-root, read-only filesystem
- **Network-Policy**: Explicit allow rules
- **Probes**: liveness + readiness probes
- **Resource-Quotas**: Namespace resource limits

---

## Infrastructure > Serverless
**Trigger:** Lambda/Functions/Vercel/Netlify detected

- **Minimize-Bundle**: Reduce cold start time
- **Graceful-Timeout**: Clean shutdown before timeout
- **Stateless**: No local state between invocations
- **Right-Size**: Memory optimization

---

## Infrastructure > Monorepo
**Trigger:** nx/turbo/lerna/pnpm-workspace detected

- **Package-Boundaries**: Clear ownership per package
- **Selective-Test**: Test only affected packages
- **Shared-Deps**: Hoisted and versioned dependencies
- **Build-Cache**: Remote build cache

---

## Frontend
**Trigger:** React/Vue/Angular/Svelte/Solid/Astro detected

### Base Frontend Rules
- **A11y-WCAG**: WCAG 2.2 AA, keyboard navigation
- **Perf-Core-Vitals**: LCP<2.5s, INP<200ms, CLS<0.1
- **State-Predictable**: Single source of truth for state
- **Code-Split**: Lazy load routes and heavy components

### React (Frontend:React)
**Trigger:** {react_deps}, {react_ext}

- **Hooks-Rules**: Rules of Hooks (top-level, same order)
- **Memo-Strategic**: useMemo/useCallback for expensive ops only
- **Key-Stable**: Stable keys for lists (not index)
- **Effect-Cleanup**: Cleanup in useEffect return
- **Server-Components**: Use Server Components for data fetching, Client for interactivity (Next.js/RSC)
- **Use-Hook**: Use use() hook for promises and context (React 19+)
- **Suspense-Boundary**: Wrap async components in Suspense with fallback
- **Actions**: Use Server Actions for mutations (Next.js 14+)
- **React-Compiler** [EXPERIMENTAL]: Let React Compiler handle memoization automatically (React 19+)
- **Ref-As-Prop**: Pass ref as regular prop, no forwardRef needed (React 19+)
- **Form-Actions**: Use form action prop with useActionState for form handling (React 19+)
- **Optimistic-UI**: Use useOptimistic for instant UI feedback during mutations

### Vue (Frontend:Vue)
**Trigger:** {vue_deps}, {vue_ext}

- **Composition-API**: Composition API over Options API (Vue 3+)
- **Reactive-Unwrap**: .value access for refs in script
- **Provide-Inject**: Provide/inject for deep prop drilling
- **SFC-Style**: Scoped styles in single-file components
- **Script-Setup**: Use <script setup> for cleaner syntax
- **Definemodel**: Use defineModel for v-model with props (Vue 3.4+)
- **Vapor-Mode** [EXPERIMENTAL]: Consider Vapor mode for performance-critical components (Vue 3.5+)

### Angular (Frontend:Angular)
**Trigger:** {angular_deps}, {angular_ext}

- **Standalone-Components**: Standalone components as default (Angular 17+)
- **Signals-Reactive**: Signals for reactive state (Angular 16+)
- **OnPush-Strategy**: OnPush change detection for performance
- **Lazy-Modules**: Lazy load feature modules
- **Zoneless-Detection**: Use zoneless change detection for performance (Angular 18+)
- **Input-Signal**: Use input() and model() signal functions (Angular 17.1+)
- **Output-Function**: Use output() function instead of @Output (Angular 17.1+)
- **Deferrable-Views**: Use @defer for lazy loading components (Angular 17+)
- **Control-Flow**: Use @if/@for/@switch over *ngIf/*ngFor (Angular 17+)

### Svelte (Frontend:Svelte)
**Trigger:** {svelte_deps}, {svelte_ext}

- **Reactivity-Native**: Use framework reactivity (Svelte 5: runes, Svelte 4: stores)
- **Store-Subscribe**: Auto-subscribe with $ prefix (stores) or $state (runes)
- **Transitions-Native**: Use built-in transitions
- **Actions-Reusable**: Reusable actions for DOM behavior
- **Runes-State**: Use $state for reactive state, $derived for computed (Svelte 5+)
- **Runes-Effect**: Use $effect for side effects instead of reactive statements (Svelte 5+)
- **Props-Rune**: Use $props() instead of export let for props (Svelte 5+)
- **Snippets**: Use {#snippet} for reusable markup within components (Svelte 5+)
- **Event-Handlers**: Use onclick instead of on:click syntax (Svelte 5+)

### Solid (Frontend:Solid)
**Trigger:** {solid_deps}

- **Signal-Fine-Grained**: Fine-grained reactivity with signals
- **Memo-Derived**: createMemo for derived computations
- **Effect-Track**: Track dependencies explicitly
- **Props-Direct**: Access props directly via `props.name` (preserves reactivity)

### Astro (Frontend:Astro)
**Trigger:** {astro_deps}, {astro_ext}

- **Islands-Minimal**: client:* directives only when needed
- **Content-Collections**: Content collections for markdown/MDX
- **Static-Default**: Static by default, SSR when needed
- **Partial-Hydration**: Selective hydration strategies

### HTMX (Frontend:HTMX)
**Trigger:** {htmx_deps}, {htmx_attrs}

- **Hypermedia-API**: Return HTML fragments, not JSON
- **Target-Precise**: Precise hx-target selectors
- **Swap-Strategy**: Appropriate hx-swap (innerHTML, outerHTML, etc)
- **Indicator-Feedback**: Loading indicators with hx-indicator

### Qwik (Frontend:Qwik)
**Trigger:** {qwik_deps}

- **Resumability-First**: Leverage resumability, avoid eager hydration
- **Dollar-Sign**: Use $() for lazy-loaded code boundaries
- **Task-Types**: useTask$ for server, useVisibleTask$ for client-only
- **Signal-State**: Signals for fine-grained reactivity
- **Component-Lazy**: component$() for automatic code splitting
- **Serialization-Aware**: Keep state serializable for resumability
- **Event-QRL**: QRL-based event handlers for optimal loading
- **City-Routing**: Use Qwik City for routing and data loading

---

## Meta-Frameworks

### Next.js (Framework:Next)
**Trigger:** {nextjs_deps}, {nextjs_config}

- **App-Router**: Use App Router for new projects (Next.js 13+)
- **Server-Actions**: Server Actions for mutations, not API routes (Next.js 14+)
- **Streaming-SSR**: Use streaming with Suspense for faster TTFB
- **Route-Handlers**: Use Route Handlers (route.ts) instead of API routes for App Router
- **Metadata-API**: Use Metadata API for SEO, not manual head tags
- **Image-Component**: Use next/image for automatic optimization
- **Font-Optimization**: Use next/font for zero-layout-shift fonts
- **Turbopack** [EXPERIMENTAL]: Enable Turbopack for faster dev builds (Next.js 15+)
- **Parallel-Routes**: Use parallel routes for complex layouts
- **Intercepting-Routes**: Use intercepting routes for modals/sheets

### Nuxt (Framework:Nuxt)
**Trigger:** {nuxt_deps}, {nuxt_config}

- **Nitro-Server**: Use Nitro for server API routes
- **Auto-Imports**: Leverage auto-imports, don't manual import
- **Composables**: Use composables/ for shared logic
- **Server-Directory**: Use server/ for API endpoints
- **TypeScript-Native**: Full TypeScript support out of box
- **Layers**: Use Nuxt Layers for shared config
- **State-useState**: Use useState for SSR-safe state

### SvelteKit (Framework:SvelteKit)
**Trigger:** {sveltekit_deps}, {sveltekit_config}

- **Load-Functions**: Use +page.ts/+page.server.ts for data loading
- **Form-Actions**: Use form actions for mutations
- **Hooks**: Use hooks.server.ts for middleware
- **Adapter-Select**: Choose adapter based on deployment target
- **Prerender**: Prerender static pages where possible
- **SSR-First**: SSR by default, disable only when necessary

### Remix (Framework:Remix)
**Trigger:** {remix_deps}, {remix_patterns}

- **Loader-Action**: Use loader for GET, action for mutations
- **Nested-Routes**: Leverage nested routing for UI composition
- **ErrorBoundary**: Define error boundaries per route
- **Defer-Streaming**: Use defer for streaming large data
- **Form-Component**: Use Remix Form for progressive enhancement
- **Meta-Function**: Use meta function for route-specific SEO

---

## Desktop
**Trigger:** Electron/Tauri detected

### Base Desktop Rules
- **IPC-Secure**: Validate all IPC messages
- **Auto-Update**: Built-in update mechanism
- **Native-Feel**: Platform-appropriate UI/UX
- **Offline-First**: Graceful offline handling

### Electron (Desktop:Electron)
**Trigger:** {electron_deps}, {electron_config}

- **Context-Isolation**: contextIsolation: true always
- **Sandbox-Enable**: sandbox: true for renderers
- **Preload-Bridge**: Expose APIs via preload scripts only
- **CSP-Strict**: Content Security Policy in HTML

### Tauri (Desktop:Tauri)
**Trigger:** {tauri_deps}, {tauri_config}

- **Allowlist-Minimal**: Minimal API allowlist
- **Command-Validate**: Validate all command inputs in Rust
- **Bundle-Optimize**: Optimize bundle size (no unused APIs)
- **Sidecar-Safe**: Secure sidecar binaries

---

## Mobile
**Trigger:** Flutter/ReactNative/iOS/Android detected

### Base Mobile Rules
- **Offline-Cache**: Offline-first with local storage
- **Deep-Link**: Handle deep links properly
- **Push-Permission**: Request permissions gracefully
- **Battery-Aware**: Minimize battery drain

### Flutter (Mobile:Flutter)
**Trigger:** {flutter_manifest}, {dart_ext}

- **Widget-Const**: Use const constructors
- **State-Provider**: Provider/Riverpod for state
- **Platform-Channel**: Platform channels for native APIs
- **Build-Modes**: Different configs for debug/release

### React Native (Mobile:ReactNative)
**Trigger:** {rn_deps}

- **Native-Modules**: TurboModules/New Architecture for performance
- **Metro-Optimize**: Optimize Metro bundler config
- **Hermes-Enable**: Hermes engine for Android
- **Workflow-Match**: Choose managed (Expo) or bare based on native module needs

### iOS Native (Mobile:iOS)
**Trigger:** {ios_project}, {ios_deps}, {swift_ext}

- **SwiftUI-Modern**: SwiftUI over UIKit when possible
- **Combine-Reactive**: Combine for reactive patterns
- **App-Privacy**: Privacy manifest and descriptions
- **TestFlight-Beta**: TestFlight for beta testing

### Android Native (Mobile:Android)
**Trigger:** {android_build}, {android_manifest}

- **Compose-Modern**: Jetpack Compose over XML layouts
- **ViewModel-State**: ViewModel + StateFlow for state
- **WorkManager-Background**: WorkManager for background work
- **R8-Shrink**: Enable R8 code shrinking

### Kotlin Multiplatform (Mobile:KMP)
**Trigger:** {kmp_config}, {kmp_dirs}

- **Expect-Actual**: Shared expect/actual declarations
- **Ktor-Networking**: Ktor for shared networking
- **SqlDelight-DB**: SqlDelight for shared database
- **KMM-Modules**: Separate shared and platform modules

---

## Specialized > ML/AI
**Trigger:** torch/tensorflow/sklearn/transformers/langchain detected

- **Reproducibility**: Seed everything, pin versions
- **Experiment-Track**: Track experiments with logging (MLflow/W&B for Scale:Medium+)
- **Model-Version**: Version model artifacts and checkpoints
- **Bias-Detection**: Fairness metrics for user-facing AI

---

## Infrastructure

### Docker (Infra:Docker)
**Trigger:** {container_files}

- **Multi-Stage**: Multi-stage builds for smaller images
- **Layer-Cache**: Order commands for optimal layer caching
- **Non-Root**: Run as non-root user
- **Health-Check**: HEALTHCHECK instruction for orchestrators
- **Env-Inject**: Environment variables for configuration
- **Buildkit-Secrets**: Use --mount=type=secret for sensitive build args
- **Cache-Mounts**: Use --mount=type=cache for package managers
- **Distroless**: Use distroless or alpine for production images

### Kubernetes (Infra:K8s)
**Trigger:** {k8s_dirs}, {k8s_configs}

- **Resource-Limits**: CPU/memory requests and limits
- **Liveness-Readiness**: Health probes configured
- **Config-Secrets**: ConfigMaps and Secrets, not hardcoded
- **RBAC-Minimal**: Least privilege service accounts
- **HPA-Defined**: Horizontal Pod Autoscaler for scaling
- **Gateway-API**: Use Gateway API over Ingress for advanced routing (K8s 1.27+)
- **Pod-Disruption**: PodDisruptionBudget for availability during updates
- **Security-Context**: runAsNonRoot, readOnlyRootFilesystem, drop capabilities

### Terraform (Infra:Terraform)
**Trigger:** {tf_files}

- **State-Remote**: Remote state backend (S3, GCS, etc.)
- **Modules-Reuse**: Reusable modules for common patterns
- **Variables-Type**: Typed variables with descriptions
- **Output-Document**: Outputs for cross-module references
- **Plan-Before-Apply**: Always plan before apply
- **Moved-Blocks**: Use moved blocks for refactoring without recreation
- **Import-Blocks**: Use import blocks for existing resources (TF 1.5+)
- **Check-Blocks**: Use check blocks for post-apply validation (TF 1.5+)

### Pulumi (Infra:Pulumi)
**Trigger:** {pulumi_config}

- **Stack-Per-Env**: Separate stacks per environment
- **Config-Secrets**: Encrypted secrets in config
- **Type-Safe**: Leverage language type system
- **Preview-Always**: Preview before up

### CDK (Infra:CDK)
**Trigger:** {cdk_config}, {cdk_stack_files}

- **Construct-Library**: Reusable L3 constructs
- **Stack-Separation**: Logical stack boundaries
- **Context-Values**: Environment-specific context
- **Synth-Test**: Test synthesized templates
- **Aspects-Cross-Cut**: Use Aspects for cross-cutting concerns

### Serverless (Infra:Serverless)
**Trigger:** {serverless_configs}

- **Cold-Start**: Minimize cold start time
- **Timeout-Set**: Explicit function timeouts
- **Memory-Tune**: Right-size memory allocation
- **Event-Validate**: Validate event payloads

### Edge (Infra:Edge)
**Trigger:** {edge_configs}

- **Size-Minimal**: Bundle size under limits
- **Stateless**: No persistent in-memory state
- **KV-Access**: Edge KV for data persistence
- **Geo-Route**: Geographic routing when needed

### WASM (Infra:WASM)
**Trigger:** {wasm_ext}, {wasm_config}

- **Size-Optimize**: Optimize for size (-Os, wasm-opt)
- **Memory-Linear**: Manage linear memory explicitly
- **Interface-Types**: Use interface types for interop
- **Streaming**: Stream instantiation for large modules

---

## Build Tools

### Monorepo (Build:Monorepo)
**Trigger:** {monorepo_configs}

- **Affected-Only**: Build only affected packages
- **Cache-Remote**: Remote build cache enabled
- **Deps-Graph**: Explicit dependency graph
- **Consistent-Versions**: Shared dependency versions

### Bundler (Build:Bundler)
**Trigger:** {bundler_configs}

- **Tree-Shake**: Enable tree shaking
- **Code-Split**: Split by route/feature
- **Source-Maps**: Source maps for debugging
- **Minify-Prod**: Minify in production only

### Linter (Build:Linter)
**Trigger:** {linter_configs}

- **CI-Enforce**: Lint in CI pipeline
- **Auto-Fix**: Auto-fix where safe
- **Ignore-Explicit**: Explicit ignore patterns
- **Severity-Config**: Error vs warning levels

### Formatter (Build:Formatter)
**Trigger:** {formatter_configs}

- **Pre-Commit**: Format on commit
- **Config-Share**: Shared config across team
- **Editor-Integrate**: Editor integration

### TypeChecker (Build:TypeChecker)
**Trigger:** {typechecker_configs}

- **Strict-Enable**: Enable strict mode
- **Incremental**: Incremental compilation
- **CI-Check**: Type check in CI

---

## Testing

### Unit Testing (Test:Unit)
**Trigger:** {unit_test_deps}

- **Isolation**: No shared state between tests
- **Fast-Feedback**: Tests complete in seconds
- **Mock-Boundaries**: Mock at system boundaries
- **Assertions-Clear**: One concept per test

### E2E Testing (Test:E2E)
**Trigger:** {e2e_deps}

- **Critical-Paths**: Cover critical user journeys
- **Stable-Selectors**: data-testid attributes
- **Retry-Flaky**: Retry for network flakiness
- **Parallel-Run**: Parallel execution where possible

### Coverage (Test:Coverage)
**Trigger:** {coverage_configs}

- **Threshold-Set**: Minimum coverage threshold
- **Branch-Cover**: Branch coverage, not just line
- **Exclude-Generated**: Exclude generated code
- **Trend-Track**: Track coverage trends

---

## CI/CD

### GitHub Actions (CI:GitHub)
**Trigger:** {github_workflow_dir}

- **Matrix-Test**: Matrix for multiple versions
- **Cache-Deps**: Cache dependencies
- **Secrets-Safe**: Use GitHub Secrets
- **Concurrency-Limit**: Cancel redundant runs

### GitLab CI (CI:GitLab)
**Trigger:** {gitlab_config}

- **Stage-Order**: Logical stage ordering
- **Cache-Key**: Proper cache key strategy
- **Artifacts-Expire**: Artifact expiration
- **Rules-Conditional**: Conditional job execution

### Jenkins (CI:Jenkins)
**Trigger:** {jenkins_config}

- **Pipeline-Declarative**: Declarative over scripted
- **Agent-Label**: Specific agent labels
- **Credentials-Bind**: Credentials binding
- **Parallel-Stages**: Parallel where independent

### CircleCI (CI:CircleCI)
**Trigger:** {circleci_config}

- **Orbs-Reuse**: Use orbs for common tasks
- **Workspace-Persist**: Persist between jobs
- **Resource-Class**: Appropriate resource class

### Azure DevOps (CI:Azure)
**Trigger:** {azure_config}

- **Templates-Share**: Shared YAML templates
- **Variable-Groups**: Variable groups for secrets
- **Environments-Deploy**: Environment approvals

### ArgoCD (CI:ArgoCD)
**Trigger:** {argocd_dir}, {argocd_config}

- **Sync-Policy**: Auto-sync vs manual
- **Health-Check**: Custom health checks
- **Diff-Strategy**: Appropriate diff strategy

---

## ML/AI Specialized

### Training (ML:Training)
**Trigger:** {ml_training_deps}

- **Seed-All**: Reproducible random seeds
- **Checkpoint-Save**: Regular checkpoints
- **Metrics-Log**: Log training metrics
- **GPU-Utilize**: Efficient GPU utilization

### LLM Orchestration (ML:LLM)
**Trigger:** {llm_orchestration_deps}

- **Prompt-Template**: Versioned prompt templates
- **Token-Limit**: Respect context limits
- **Retry-Backoff**: Retry with exponential backoff
- **Cost-Track**: Track API costs
- **RAG-Chunk**: Chunk documents appropriately for retrieval (512-1024 tokens typical)
- **Structured-Output**: Use structured outputs/JSON mode for reliable parsing
- **Function-Calling**: Use tool/function calling for actions, not string parsing
- **Prompt-Cache**: Cache identical prompts for cost savings

### Inference (ML:Inference)
**Trigger:** {inference_deps}

- **Batch-Infer**: Batch for throughput
- **Quantize-Prod**: Quantization for production
- **Timeout-Guard**: Inference timeout limits
- **Memory-Manage**: Clear model memory

### ML SDK (ML:SDK)
**Trigger:** {ai_sdk_deps}

- **Key-Rotate**: API key rotation
- **Rate-Limit**: Handle rate limits gracefully
- **Response-Validate**: Validate API responses
- **Fallback-Model**: Fallback to alternative models

---

## Runtimes

### Node.js (R:Node)
**Trigger:** {node_markers}

- **LTS-Version**: Use LTS versions
- **Engine-Lock**: Lock engine version in package.json
- **ESM-Prefer**: ESM over CommonJS
- **Event-Loop**: Use async I/O for event loop operations

### Bun (R:Bun)
**Trigger:** {bun_markers}

- **Bun-Native**: Use Bun native APIs when faster
- **Node-Compat**: Test Node.js compatibility
- **Macro-Use**: Macros for build-time optimization
- **Hot-Reload**: Leverage fast hot reload

### Deno (R:Deno)
**Trigger:** {deno_markers}

- **Permissions-Minimal**: Minimal --allow flags
- **Import-Map**: Import maps for dependencies
- **Test-Native**: Use Deno.test native
- **Fresh-Edge**: Deploy to Deno Deploy edge

---

## Database Specialized

### SQL (DB:SQL)
**Trigger:** {sql_drivers}

- **Parameterized**: Parameterized queries always
- **Connection-Pool**: Connection pooling
- **Transaction-Explicit**: Explicit transactions
- **Index-Query**: Index for common queries

### NoSQL (DB:NoSQL)
**Trigger:** {nosql_deps}

- **Schema-Validate**: Application-level schema validation
- **TTL-Set**: TTL for expiring data
- **Consistency-Choose**: Choose consistency level
- **Batch-Ops**: Batch operations when possible

### Vector DB (DB:Vector)
**Trigger:** {vector_deps}

- **Embed-Model**: Consistent embedding model
- **Dimension-Match**: Dimension consistency
- **Index-Type**: Appropriate index type (HNSW, IVF)
- **Similarity-Metric**: Correct similarity metric

### Edge/Embedded DB (DB:Edge)
**Trigger:** {edge_db_deps}

- **Sync-Strategy**: Configure sync strategy (local-first, server-authoritative)
- **Offline-Capable**: Handle offline reads and writes gracefully
- **Conflict-Resolution**: Define conflict resolution for concurrent writes
- **Connection-Mode**: Choose embedded vs remote connection mode
- **Migration-Portable**: Portable migration scripts across environments
- **Query-Local**: Optimize for local query latency
- **Replica-Sync**: Configure replica synchronization interval

---

## API Specialized

### WebSocket (API:WebSocket)
**Trigger:** {websocket_deps}

- **Reconnect-Auto**: Automatic reconnection
- **Heartbeat-Ping**: Ping/pong for health
- **Message-Queue**: Queue during disconnect
- **Binary-Efficient**: Binary for large payloads

---

## Specialized > Game
**Trigger:** Unity/Unreal/Godot detected

### Base Game Rules (All Engines)
- **Frame-Budget**: 16ms (60fps) or 8ms (120fps) target
- **Asset-LOD**: Level of detail + streaming
- **Save-Versioned**: Migration support for old saves
- **Determinism**: Fixed timestep for multiplayer/replay
- **Input-System**: Input actions, rebindable keys
- **Object-Pool**: Reuse frequently spawned objects

### Unity (Game:Unity)
**Trigger:** {unity_markers}

- **Prefab-Usage**: Use prefabs for reusable objects, avoid scene-only objects
- **ScriptableObjects**: Use ScriptableObjects for data containers and configuration
- **Assembly-Definition**: Split code into assemblies for faster compilation
- **Addressables**: Use Addressables for asset management (not Resources.Load)
- **ECS-Performance**: Use ECS/DOTS for performance-critical systems (Unity 6+)
- **IL2CPP**: Use IL2CPP for production builds (better performance, obfuscation)
- **UI-Toolkit**: Use UI Toolkit for runtime UI (Unity 2023+), UGUI for legacy
- **Input-System**: Use new Input System, not legacy Input.GetKey
- **Async-Await**: Use UniTask for async/await (faster than coroutines)
- **Serialization**: [SerializeField] for private fields, avoid public fields

### Unreal (Game:Unreal)
**Trigger:** {unreal_markers}

- **Blueprint-Cpp-Balance**: Gameplay logic in Blueprint, performance in C++
- **UPROPERTY-Always**: All reflected properties use UPROPERTY macro
- **GC-Aware**: Use TWeakObjectPtr for non-owning references to avoid GC issues
- **Asset-Soft-Refs**: Use soft references for large assets to avoid memory bloat
- **Data-Assets**: Use Data Assets for configuration, not hardcoded values
- **Enhanced-Input**: Use Enhanced Input System (UE5+), not legacy input
- **Niagara**: Use Niagara for particles (not Cascade)
- **Common-UI**: Use Common UI for cross-platform UI
- **Live-Coding**: Enable Live Coding for faster iteration
- **Gameplay-Abilities**: Use Gameplay Ability System for complex abilities

### Godot (Game:Godot)
**Trigger:** {godot_markers}

- **Scene-Composition**: Composition over inheritance via scene instancing
- **Signal-Decoupling**: Use signals for loose coupling between nodes
- **Autoload-Minimal**: Minimal autoloads, prefer dependency injection
- **Resource-Custom**: Custom resources for data (not dictionaries)
- **Export-Vars**: Use @export for inspector-editable variables
- **Typed-GDScript**: Use static typing for performance and IDE support
- **Node-Groups**: Use groups for batch operations
- **Scene-Unique**: Use %NodeName for scene-unique node access (Godot 4+)
- **Tween-Animation**: Use Tweens for procedural animation
- **Physics-Layers**: Configure collision layers/masks properly

---

## i18n
**Trigger:** locales/i18n/translations detected

- **Strings-External**: No hardcoded user-facing text
- **UTF8-Encoding**: Consistent UTF-8 encoding
- **RTL-Support**: Bidirectional layout for RTL languages
- **Locale-Format**: Culture-aware date/time/number formatting

---

## Real-time
**Inheritance:** Higher tiers include lower.

### Basic (RT:Basic)
**Trigger:** WebSocket/SSE detected

- **Reconnect-Logic**: Automatic reconnection with backoff
- **Heartbeat**: Connection health monitoring
- **Stale-Data**: Handle disconnection gracefully

### Low-Latency (RT:LowLatency)
- **Binary-Protocol**: Protobuf/msgpack for performance
- **Edge-Compute**: Edge deployment for global users

---

## Documentation Generators
**Trigger:** Documentation generator detected

### Docusaurus (Docs:Docusaurus)
**Trigger:** {docusaurus_config}

- **Versioning**: Enable docs versioning for multiple versions
- **Search-Integration**: Algolia or local search configuration
- **Nav-Sidebar**: Navigation and sidebar configuration
- **Blog-Setup**: Blog functionality with categories/tags
- **Plugin-System**: Leverage plugin system for extensions
- **Deploy-Ready**: Pre-configured for static hosting deployment

### VitePress (Docs:VitePress)
**Trigger:** {vitepress_config}

- **Theme-Config**: Built-in light/dark theme configuration
- **Navigation**: Sidebar and navbar navigation setup
- **Search-Local**: Local search with multiple strategies
- **Component-Markdown**: Vue component integration in markdown
- **Build-Optimization**: Optimized Vite build configuration
- **Deployment-Static**: Static site hosting ready

### Sphinx (Docs:Sphinx)
**Trigger:** {sphinx_config}

- **ReStructuredText**: RST markup conventions
- **Theme-Selection**: Sphinx theme configuration (PyData, Furo)
- **Extension-Management**: Extension configuration for features
- **API-Documentation**: Autodoc for automatic code documentation
- **Build-Multiple-Formats**: HTML, PDF, ePub output support
- **Deploy-ReadTheDocs**: ReadTheDocs deployment preparation

### MkDocs (Docs:MkDocs)
**Trigger:** {mkdocs_config}

- **Markdown-Structure**: Directory structure reflecting navigation
- **Theme-Customization**: Material for MkDocs theme configuration
- **Plugin-System**: Plugin ecosystem for extended functionality
- **Search-Configuration**: Built-in search optimization
- **Build-Performance**: Incremental builds for fast iteration
- **Deploy-GhPages**: GitHub Pages deployment setup

---

## Deployment Platforms
**Trigger:** Deployment platform detected

### Fly.io (Deploy:Fly)
**Trigger:** {fly_config}

- **App-Configuration**: fly.toml configuration and secrets
- **Regions-Selection**: Multi-region deployment strategy
- **Volumes-Storage**: Persistent volume management
- **Health-Checks**: Health check configuration
- **Auto-Scaling**: Autoscaling rules per region
- **Custom-Domain**: Custom domain and SSL setup

### Railway (Deploy:Railway)
**Trigger:** {railway_config}

- **Services-Connect**: Multi-service deployments and connections
- **Environment-Variables**: Environment variable management across environments
- **Database-Integration**: Built-in database provisioning
- **Custom-Domain**: Custom domain and auto-SSL configuration
- **Deployment-Triggers**: Git-based auto-deployment
- **Plugin-Ecosystem**: Railway plugins for third-party services

### Render (Deploy:Render)
**Trigger:** {render_config}

- **Service-Discovery**: Service-to-service communication
- **Environment-Specific**: Different configurations per environment
- **Build-Command**: Custom build and start commands
- **Cron-Jobs**: Scheduled background jobs
- **Static-Site**: Static site deployment with redirects
- **Custom-Domain**: Custom domains with auto-renewal SSL

### Heroku (Deploy:Heroku)
**Trigger:** {heroku_config}

- **Procfile-Types**: Process types and scaling
- **Buildpack-Selection**: Buildpack for language runtime
- **Add-on-Management**: Add-ons for databases and services
- **Config-Vars**: Config variables for secrets and configuration
- **Dyno-Types**: Dyno type selection and cost optimization
- **Release-Phase**: Release phase scripts for migrations

### Vercel (Deploy:Vercel)
**Trigger:** {vercel_config}

- **Framework-Detection**: Automatic framework detection and optimization
- **Serverless-Functions**: Serverless functions in api/ directory
- **Edge-Functions**: Edge functions for global low-latency
- **Environment-Variables**: Environment variables per deployment
- **Preview-Deployments**: Preview deployments for PRs
- **Build-Cache**: Build caching for faster deploys
- **Rewrites-Redirects**: Rewrites and redirects configuration
- **Analytics-Integration**: Web analytics integration

### Netlify (Deploy:Netlify)
**Trigger:** {netlify_config}

- **Build-Configuration**: Build command and publish directory
- **Serverless-Functions**: Functions in netlify/functions
- **Edge-Functions**: Deno-based edge functions
- **Deploy-Contexts**: Deploy contexts (production, deploy-preview, branch-deploy)
- **Redirects-Headers**: _redirects and _headers files
- **Forms-Handling**: Built-in form handling
- **Identity-Auth**: Netlify Identity for authentication
- **Split-Testing**: A/B testing with branch deploys

### Google Cloud Run (Deploy:CloudRun)
**Trigger:** {gcp_cloudrun}

- **Container-Based**: Container-based deployment
- **Concurrency-Settings**: Concurrency and scaling settings
- **CPU-Allocation**: CPU allocation (always-on vs request-based)
- **Secrets-Manager**: Secret Manager integration
- **VPC-Connector**: VPC connector for private resources
- **Traffic-Splitting**: Traffic splitting for gradual rollouts
- **Min-Instances**: Minimum instances for cold start mitigation
- **Domain-Mapping**: Custom domain mapping

### Azure Web Apps (Deploy:AzureWebApp)
**Trigger:** {azure_webapp}

- **App-Service-Plan**: App Service plan selection
- **Deployment-Slots**: Deployment slots for staging
- **Configuration-Settings**: Application settings and connection strings
- **Managed-Identity**: Managed identity for Azure resources
- **Continuous-Deployment**: GitHub/Azure DevOps integration
- **Health-Probes**: Health check probes configuration
- **Auto-Scale**: Autoscale rules configuration
- **VNet-Integration**: VNet integration for private access

### AWS App Runner (Deploy:AppRunner)
**Trigger:** {aws_apprunner}

- **Source-Connection**: Source connection (ECR or code repo)
- **Auto-Deployment**: Automatic deployments on push
- **Instance-Configuration**: CPU and memory configuration
- **Auto-Scaling**: Auto scaling configuration
- **VPC-Connector**: VPC connector for private resources
- **Secrets-Environment**: Secrets Manager integration
- **Custom-Domain**: Custom domain configuration
- **Observability-Config**: X-Ray tracing and CloudWatch logs

---

## Observability Tools
**Trigger:** Observability tool detected

*Note: These rules are specific to each observability tool. For SLA-based observability practices, see Observability Rules section.*

### Prometheus (Observability:Prometheus)
**Trigger:** {prometheus_config}

- **Scrape-Config**: Target scrape configuration
- **Alert-Rules**: Alert rule definition and evaluation
- **Service-Discovery**: Dynamic service discovery
- **Remote-Storage**: Long-term data retention configuration
- **Metric-Relabeling**: Metric relabeling for normalization
- **High-Availability**: HA deployment with replication

### Grafana (Observability:Grafana)
**Trigger:** {grafana_config}

- **Dashboard-Provisioning**: Dashboard as code
- **DataSource-Config**: Prometheus, Loki, and other datasource setup
- **Alert-Manager**: Alert routing and notification
- **Plugin-Management**: Community plugins installation
- **RBAC-Setup**: Role-based access control
- **Authentication**: LDAP, SAML, OAuth integration

### Datadog (Observability:Datadog)
**Trigger:** {datadog_config}

- **Agent-Configuration**: Datadog agent configuration
- **Custom-Metrics**: Custom metric reporting
- **Log-Collection**: Log collection and parsing
- **APM-Instrumentation**: APM instrumentation for tracing
- **Monitor-Creation**: Monitor definition for alerting
- **Synthetic-Tests**: Synthetic monitoring for uptime checks

### ELK Stack (Observability:ELK)
**Trigger:** {elk_config}

- **Elasticsearch-Config**: Elasticsearch cluster setup
- **Logstash-Pipelines**: Pipeline configuration for log parsing
- **Kibana-Dashboards**: Dashboard creation and visualization
- **Index-Lifecycle**: Index lifecycle management
- **Security-TLS**: TLS and authentication setup
- **Performance-Tuning**: Performance optimization for scale

### Jaeger (Observability:Jaeger)
**Trigger:** {jaeger_config}

- **Sampler-Config**: Sampling strategy configuration
- **Collector-Setup**: Collector deployment and configuration
- **Backend-Storage**: Storage backend selection (Elasticsearch)
- **Query-Service**: Query service for trace retrieval
- **Instrumentation**: OpenTelemetry instrumentation
- **Retention-Policy**: Trace retention and cleanup

### OpenTelemetry (Observability:OpenTelemetry)
**Trigger:** {otel_deps}

- **Instrumentation-Libraries**: Use standardized instrumentation
- **Exporter-Selection**: Exporter for backend (Prometheus, Jaeger)
- **Context-Propagation**: Trace context propagation across services
- **Resource-Attributes**: Resource attributes for identification
- **Sampling-Strategy**: Sampling configuration for cost management
- **Collector-Deployment**: OTel Collector for collection and processing

### Sentry (Observability:Sentry)
**Trigger:** {sentry_deps}

- **Project-Configuration**: Project setup and DSN management
- **Source-Maps**: Source map upload for JavaScript
- **Release-Tracking**: Release tracking for error grouping
- **Custom-Context**: Custom context for debugging
- **Integration-Setup**: Platform integrations (GitHub, Slack)
- **Performance-Monitoring**: Performance monitoring configuration

### New Relic (Observability:NewRelic)
**Trigger:** {newrelic_config}, {newrelic_deps}

- **Agent-Configuration**: Language-specific agent configuration
- **Custom-Instrumentation**: Custom instrumentation for business transactions
- **Distributed-Tracing**: Distributed tracing across services
- **Custom-Metrics**: Custom metrics for business KPIs
- **Alert-Policies**: Alert policies and notification channels
- **Workloads**: Workload grouping for related services
- **Synthetics**: Synthetic monitoring for availability

### Splunk (Observability:Splunk)
**Trigger:** {splunk_config}, {splunk_deps}

- **Log-Forwarding**: Configure log forwarding (Universal Forwarder, HEC)
- **Index-Strategy**: Index strategy for data organization
- **Search-Optimization**: Optimize searches with field extraction
- **Dashboard-Creation**: Create operational dashboards
- **Alert-Configuration**: Real-time alerting configuration
- **OTEL-Integration**: OpenTelemetry integration for traces/metrics
- **RBAC-Setup**: Role-based access control setup

### Dynatrace (Observability:Dynatrace)
**Trigger:** {dynatrace_config}, {dynatrace_deps}

- **OneAgent-Deployment**: OneAgent deployment and configuration
- **Auto-Discovery**: Automatic topology discovery
- **Custom-Services**: Custom service detection rules
- **Synthetic-Monitors**: Synthetic browser and HTTP monitors
- **Davis-AI**: Leverage Davis AI for root cause analysis
- **Metric-Ingestion**: Custom metric ingestion via API
- **Session-Replay**: Session replay for user experience analysis

---

## Infrastructure Tools
**Trigger:** Infrastructure tool detected

### Ansible (Infra:Ansible)
**Trigger:** {ansible_config}, {ansible_patterns}

- **Inventory-Dynamic**: Use dynamic inventory for cloud resources
- **Role-Organization**: Organize playbooks into roles
- **Vault-Secrets**: Ansible Vault for sensitive data
- **Idempotency**: Ensure tasks are idempotent
- **Handler-Notify**: Use handlers for service restarts
- **Tags-Selective**: Tags for selective execution
- **Molecule-Testing**: Test roles with Molecule
- **Collections-Reuse**: Use Ansible Galaxy collections

### Consul (Infra:Consul)
**Trigger:** {consul_config}, {consul_patterns}

- **Service-Registration**: Auto-register services with health checks
- **KV-Store**: Use KV store for dynamic configuration
- **Service-Mesh**: Connect for service mesh
- **ACL-Policies**: ACL policies for security
- **Prepared-Queries**: Prepared queries for failover
- **Watch-Handlers**: Watches for configuration updates
- **Datacenter-Federation**: Multi-datacenter federation

### Vault (Infra:Vault)
**Trigger:** {vault_config}, {vault_patterns}

- **Secrets-Engines**: Use appropriate secrets engines
- **Authentication-Methods**: Configure auth methods per use case
- **Policies-Minimal**: Minimal policies (least privilege)
- **Dynamic-Secrets**: Dynamic secrets for databases
- **Token-TTL**: Short-lived tokens with renewal
- **Audit-Logging**: Enable audit logging
- **Seal-Unseal**: Secure seal/unseal procedures
- **Agent-Injection**: Vault Agent for Kubernetes injection

---

## Dependency-Based Rules

### DEP:CLI
**Trigger:** {cli_framework_deps}

- **Help-Comprehensive**: --help with examples, subcommand help
- **Exit-Codes**: Documented exit codes (0=success, 1=error, 2=usage)
- **Error-Messages**: Clear, actionable error messages to stderr
- **Completion-Support**: Shell completion scripts (bash/zsh/fish)
- **Config-Layers**: CLI args > env vars > config file > defaults
- **Progress-Feedback**: Progress bars/spinners for long operations
- **Color-Support**: Respect NO_COLOR, --no-color flag

### DEP:TUI
**Trigger:** {tui_deps}

- **Terminal-Compat**: Graceful fallback for dumb terminals
- **Color-Detect**: Auto-detect color support, respect NO_COLOR
- **Unicode-Safe**: ASCII fallback for non-unicode terminals
- **Resize-Handle**: Handle terminal resize events
- **Keyboard-Nav**: Full keyboard navigation
- **Screen-Clear**: Clean exit, restore terminal state

### DEP:Validation
**Trigger:** {validation_deps}

- **Error-Collect**: Collect all errors, not just first
- **Error-Messages**: Human-readable, field-specific, actionable validation errors
- **Coercion-Explicit**: Document type coercion behavior. Prefer explicit over magic
- **Optional-Defaults**: Sensible defaults for optional fields
- **Custom-Validators**: Reusable validator functions with `@field_validator` or equivalent
- **Schema-Export**: Export schema for documentation/API
- **Whitespace-Handle**: Strip leading/trailing whitespace. Reject whitespace-only as empty
- **Bounds-Define**: Always set min_length/max_length for strings, ge/le for numbers, max_items for lists
- **State-Validate**: Validate field combinations (related fields must be consistent, mutually exclusive states handled)
- **Enum-String-Parse**: Support case-insensitive string-to-enum conversion with clear error on invalid
- **None-vs-Empty**: Distinguish None (field absent) vs empty string/list (field present but empty)
- **Immutable-Prefer**: Use frozen=True for data classes when mutability not needed

### DEP:Edge
**Trigger:** {edge_runtime_deps}, {edge_framework_deps}

*These rules EXTEND Infra:Edge rules. Apply both sets when edge infrastructure is detected.*

- **Cold-Start**: Minimize cold start (avoid heavy imports at top)
- **Bundle-Size**: Keep bundle <1MB, prefer tree-shakeable deps
- **Stateless-Default**: No in-memory state between requests
- **KV-Cache**: Use edge KV for persistence (Workers KV, Vercel Edge Config)
- **Geo-Aware**: Leverage request.cf or geo headers for localization
- **Timeout-Aware**: Edge functions have short timeouts (30s-60s)
- **Streaming**: Use streaming responses for large payloads

### DEP:WASM
**Trigger:** {wasm_toolchain_deps}

- **Init-Once**: Initialize WASM module once, reuse instance
- **Memory-Manage**: Explicit memory allocation/deallocation
- **Type-Boundary**: Clear types at JS/WASM boundary
- **Error-Propagate**: Handle panics gracefully (Rust: catch_unwind)
- **Size-Optimize**: Use wasm-opt, enable LTO
- **Async-Bridge**: Use async for long operations to avoid blocking

### DEP:EdgeFramework
**Trigger:** {edge_framework_deps}

*These rules are specific to edge framework choices. Apply with Infra:Edge and DEP:Edge rules.*

- **Middleware-Light**: Minimal middleware chain
- **Context-Pass**: Pass context through handlers, not globals
- **Route-Tree**: Efficient route matching (radix tree)
- **Type-Safe-Routes**: End-to-end type safety (Elysia Eden, Hono RPC)
- **Multi-Runtime**: Test on target runtime (Bun, Deno, CF Workers)

### DEP:Config
**Trigger:** {config_deps}

- **Env-Override**: Environment variables override config files
- **Secrets-Separate**: Secrets in env vars or vault, not config
- **Type-Coerce**: String to int/bool/list coercion
- **Validation-Early**: Validate on load, fail fast
- **Defaults-Document**: Document all defaults
- **Reload-Support**: Hot reload for long-running apps

### DEP:Testing
**Trigger:** {testing_framework_deps}

- **Fixtures-Scoped**: Appropriate fixture scope (function/class/module/session)
- **Mocks-Minimal**: Mock at boundaries, not internals
- **Assertions-Clear**: One assertion concept per test
- **Names-Descriptive**: Test names describe behavior (test_X_when_Y_should_Z)
- **Parametrize-Similar**: Parametrize similar test cases
- **Cleanup-Always**: Cleanup in fixtures, not tests
- **Edge-Parametrize**: Always include edge cases in parametrized tests: empty, None, whitespace, boundaries
- **State-Coverage**: Test all valid state transitions and combinations
- **Property-Based**: Use hypothesis/fast-check for input fuzzing on validators
- **Regression-Pattern**: Every bug fix gets a regression test

### DEP:GPU
**Trigger:** {gpu_deps}

- **Device-Selection**: Explicit CUDA_VISIBLE_DEVICES
- **Memory-Management**: Clear cache, use context managers
- **Batch-Sizing**: Dynamic batch based on VRAM
- **Mixed-Precision**: FP16/BF16 where applicable
- **Fallback-CPU**: Graceful CPU fallback
- **Stream-Async**: CUDA streams for parallelism

### DEP:Audio
**Trigger:** {audio_processing_deps}

- **Chunk-Processing**: Stream in chunks, don't load all
- **Sample-Rate**: Normalize sample rates
- **Format-Agnostic**: Support wav, mp3, m4a, etc.
- **Memory-Stream**: Use file handles, not full load
- **Silence-Detection**: VAD before heavy processing
- **Progress-Callback**: Report progress for long operations

### DEP:Video
**Trigger:** {video_processing_deps}

- **Frame-Iterator**: Yield frames, don't load all
- **Codec-Fallback**: Multiple codec support
- **Resolution-Aware**: Scale before heavy processing
- **Temp-Cleanup**: Auto-cleanup intermediate files
- **Seek-Efficient**: Keyframe seeking for random access
- **Hardware-Accel**: NVENC/VAAPI when available

### DEP:HeavyModel
**Trigger:** {heavy_model_deps}

- **Lazy-Model-Load**: Load on first use, not import
- **Model-Singleton**: Single instance, reuse
- **Quantization-Aware**: Support INT8/INT4 variants
- **Batch-Inference**: Batch for throughput
- **Timeout-Guard**: Max time limits on inference
- **Model-Memory-Cleanup**: Explicit GC after heavy ops
- **Download-Cache**: Cache models locally
- **Streaming-Response**: Use streaming for long generations
- **Context-Window**: Track and respect model context limits
- **Fallback-Chain**: Multiple model fallbacks for reliability

### DEP:Image
**Trigger:** {image_processing_deps}

- **Lazy-Decode**: Decode on access
- **Size-Validate**: Max dimensions check
- **Format-Preserve**: Maintain original format/quality
- **EXIF-Handle**: Rotation, metadata handling
- **Memory-Map**: mmap for huge files

### DEP:DataHeavy
**Trigger:** {data_processing_deps}

- **Chunk-Read**: chunksize parameter for large files
- **Lazy-Eval**: Defer until needed (polars/dask)
- **Type-Optimize**: Downcast dtypes
- **Index-Usage**: Set appropriate indexes
- **Parallel-Process**: Use available cores
- **Spill-Disk**: Allow disk spillover

### DEP:GamePython
**Trigger:** {python_game_deps}

- **Game-Loop**: Fixed timestep, variable render
- **Asset-Preload**: Load screens, progress bars
- **Input-Mapping**: Configurable keybindings
- **State-Machine**: Clean state transitions
- **Delta-Time**: Frame-independent movement

### DEP:GameJS
**Trigger:** {js_game_deps}

- **Sprite-Atlas**: Texture packing
- **Object-Pool**: Reuse frequently created objects
- **RAF-Loop**: requestAnimationFrame
- **WebGL-Fallback**: Canvas 2D fallback
- **Audio-Context**: Single AudioContext

### DEP:GameEngine
**Trigger:** {game_engine_markers}

- **Scene-Organization**: Clear hierarchy, naming convention
- **Prefab-Reuse**: Prefabs/scenes over copies
- **Build-Profiles**: Platform-specific settings
- **Asset-LFS**: Git LFS for binary assets
- **Input-System**: Input actions, rebindable keys
- **Platform-Optimize**: Quality presets per platform

### DEP:HTTP
**Trigger:** {http_client_deps}

- **Timeout-Always**: Explicit timeouts
- **Retry-Transient**: Exponential backoff
- **Session-Reuse**: Connection pooling
- **Error-Handle**: Status code handling
- **Response-Validate**: Schema validation

### DEP:ORM
**Trigger:** {orm_deps}

*These rules EXTEND DB:ORM rules. Apply both sets when ORM is detected.*

- **N+1-Prevent**: Eager load or batch queries
- **Query-Optimize**: EXPLAIN analysis
- **Loading-Strategy**: Explicit eager/lazy per use case
- **Transaction-Boundary**: Clear scope, rollback on error
- **Index-Design**: Indexes for WHERE/JOIN columns
- **Bulk-Operations**: Use bulk insert/update APIs

### DEP:Auth
**Trigger:** {auth_deps}

- **Token-Secure**: HttpOnly, Secure flags
- **Refresh-Flow**: Refresh token rotation
- **RBAC-Clear**: Role-based permissions
- **Session-Invalidate**: Clear all sessions option
- **MFA-Support**: Optional 2FA for sensitive ops

### DEP:Payment
**Trigger:** {payment_deps}

- **Webhook-Verify**: Signature validation
- **Idempotency-Key**: Prevent duplicate charges
- **Amount-Server**: Server-side price calculation
- **Payment-Error-Handle**: User-friendly payment errors
- **Audit-Trail**: Complete payment logs

### DEP:Email
**Trigger:** {email_deps}

- **Template-System**: Reusable templates
- **Queue-Async**: Background sending
- **Bounce-Handle**: Process bounces/complaints
- **Rate-Aware**: Respect provider limits
- **Unsubscribe**: One-click unsubscribe

### DEP:SMS
**Trigger:** {sms_deps}

- **Delivery-Status**: Track delivery callbacks
- **Rate-Throttle**: Respect carrier limits
- **Opt-Out**: Honor STOP requests
- **Fallback-Provider**: Secondary provider
- **Message-Template**: Pre-approved templates

### DEP:Notification
**Trigger:** {notification_deps}

- **Channel-Preference**: User-configurable channels
- **Batch-Send**: Batch API calls
- **Silent-Push**: Background updates
- **Token-Refresh**: Handle token rotation
- **Fallback-Channel**: Email if push fails

### DEP:Search
**Trigger:** {search_deps}

- **Index-Strategy**: Separate vs combined indexes
- **Sync-Mechanism**: Real-time vs batch sync
- **Relevance-Tune**: Custom ranking
- **Typo-Tolerance**: Fuzzy matching
- **Facet-Design**: Efficient faceting

### DEP:Queue
**Trigger:** {queue_deps}

- **Idempotent-Tasks**: Same input = same result
- **Result-Backend**: Configure result storage
- **Timeout-Task**: Per-task time limits
- **Dead-Letter**: DLQ for inspection
- **Priority-Queues**: Separate by priority

### DEP:Workflow
**Trigger:** {workflow_deps}

- **Durability-First**: Use durable execution for long-running workflows
- **Activity-Retry**: Configure retry policies per activity type
- **Timeout-Hierarchy**: Set workflow, activity, and schedule-to-close timeouts
- **Signal-Events**: Use signals/events for external communication
- **Versioning-Strategy**: Version workflows for backward compatibility
- **Observability**: Enable tracing and metrics for workflow debugging
- **Compensation-Logic**: Define compensating actions for failures
- **Cron-Schedules**: Use cron expressions for recurring workflows

### DEP:Cache
**Trigger:** {cache_deps}

- **TTL-Strategy**: Explicit expiration
- **Key-Namespace**: Prefixed keys
- **Serialization**: Consistent serializer
- **Cache-Aside**: Load on miss pattern
- **Invalidation**: Clear related keys

### DEP:Logging
**Trigger:** {logging_deps}

- **Structured-Format**: JSON logging in production
- **Level-Config**: Configurable log level
- **Context-Inject**: Request ID, user ID
- **Sensitive-Redact**: Mask PII
- **Rotation-Strategy**: Size/time rotation

### DEP:ObjectStore
**Trigger:** {object_storage_deps}

- **Presigned-URLs**: Time-limited URLs
- **Content-Type**: Validate MIME type
- **Size-Limit**: Max file size
- **Path-Structure**: Organized paths
- **Lifecycle-Rules**: Auto-expiry for temp files

### DEP:PDF
**Trigger:** {pdf_deps}

- **Template-Based**: HTML/template generation
- **Async-Generate**: Background processing
- **Stream-Output**: Stream don't buffer
- **Font-Embed**: Embed for consistency
- **Accessibility**: Tagged PDF when possible

### DEP:Excel
**Trigger:** {excel_deps}

- **Stream-Write**: Write in chunks
- **Formula-Safe**: Escape formula injection
- **Style-Template**: Reusable styles
- **Memory-Optimize**: Write-only mode
- **Sheet-Naming**: Valid sheet names

### DEP:Scraping
**Trigger:** {scraping_deps}

- **Politeness-Delay**: Respectful delays
- **Robots-Respect**: Honor robots.txt
- **User-Agent-Honest**: Identify your bot
- **Selector-Resilient**: Handle structure changes
- **Headless-Default**: Headless unless debugging
- **Anti-Block**: Rotate IPs/proxies if needed

### DEP:Blockchain
**Trigger:** {blockchain_deps}

- **Gas-Estimate**: Pre-estimate gas before transactions
- **Nonce-Manage**: Track nonce locally, handle race conditions
- **Event-Listen**: Indexed event handling with proper filtering
- **Testnet-First**: Test on testnet before mainnet deployment
- **Key-Security**: Store keys in vault or env vars only
- **Fork-Test**: Test against mainnet forks for realistic conditions
- **Multi-Sig**: Use multi-sig for admin operations
- **Tx-Simulation**: Simulate transactions before broadcasting

### DEP:SmartContractEVM
**Trigger:** {solidity_deps}, foundry, hardhat, forge, anvil

*Smart contract development for EVM chains (Ethereum, Polygon, Arbitrum, etc.)*

- **CEI-Pattern**: Checks-Effects-Interactions pattern for all external calls
- **Reentrancy-Guard**: Use ReentrancyGuard for state-changing functions with external calls
- **Overflow-Safe**: Use Solidity 0.8+ for built-in overflow checks
- **Access-Control**: Use OpenZeppelin AccessControl or Ownable patterns
- **Pausable**: Implement emergency pause mechanism for critical functions
- **Upgradeable-Proxy**: Use transparent or UUPS proxy for upgradeability when needed
- **Gas-Optimize**: Optimize storage layout, use calldata over memory for read-only
- **Events-Complete**: Emit events for all state changes
- **NatSpec-Docs**: Document all public functions with NatSpec comments
- **Slither-Check**: Run Slither static analysis before deployment
- **Fuzz-Test**: Use Foundry fuzzing for edge case testing
- **Invariant-Test**: Define and test protocol invariants
- **Formal-Verify**: Use Certora or Halmos for critical functions
- **Oracle-Validate**: Validate oracle data freshness and bounds
- **Flash-Loan-Safe**: Protect against flash loan attacks in DeFi
- **Front-Run-Mitigate**: Use commit-reveal or other anti-frontrunning patterns
- **Audit-Ready**: Follow audit checklist before external audit

### DEP:SmartContractSolana
**Trigger:** {anchor_deps}, solana-sdk, solana-program, anchor-lang

*Smart contract development for Solana (Anchor framework)*

- **Account-Validate**: Validate all accounts with Anchor constraints
- **Signer-Check**: Verify signer authority for privileged operations
- **PDA-Derive**: Validate PDA derivation with correct seeds and bump
- **Type-Discriminator**: Use Anchor discriminators for account type safety
- **CPI-Reload**: Call reload() after CPI to refresh account state
- **CPI-Depth**: Respect CPI depth limit (max 4 levels)
- **Compute-Budget**: Stay within 200K compute units per instruction
- **Checked-Math**: Use checked_* operations for all arithmetic
- **Overflow-Release**: Set overflow-checks = true in Cargo.toml release profile
- **Account-Close**: Properly close accounts to reclaim rent
- **Rent-Exempt**: Ensure accounts are rent-exempt
- **Zero-Copy**: Use zero_copy for large accounts (>10KB)
- **Seeds-Unique**: Use unique, deterministic seeds for PDAs
- **Authority-Pattern**: Single authority account for admin operations
- **Upgrade-Authority**: Secure program upgrade authority

### DEP:ARVR
**Trigger:** {arvr_deps}

- **XR-Frame-Budget**: 90fps minimum
- **Comfort-Settings**: Teleport/snap turn options
- **Fallback-Mode**: Non-XR fallback
- **Input-Abstract**: Abstract input layer
- **Performance-Tier**: Quality presets per device

### DEP:IoT
**Trigger:** {iot_deps}

- **IoT-Reconnect**: Auto-reconnect
- **Power-Aware**: Sleep modes for battery
- **OTA-Update**: Remote updates
- **Data-Buffer**: Local buffer for unreliable network
- **Watchdog**: Hardware watchdog

### DEP:Crypto
**Trigger:** {crypto_deps}

- **Algorithm-Modern**: AES-256-GCM, ChaCha20
- **Key-Rotation**: Scheduled rotation
- **IV-Unique**: Generate unique IV/nonce for each operation
- **Timing-Safe**: Constant-time compare
- **Key-Derivation**: Argon2/scrypt, not MD5/SHA1

### DEP:APITest
**Trigger:** {api_test_deps}

- **Collections-Organized**: Organize requests by feature/endpoint
- **Environment-Variables**: Use environment variables for base URLs, tokens
- **Pre-Request-Scripts**: Setup authentication, dynamic data
- **Assertions-Comprehensive**: Status code, response time, schema validation
- **CI-Integration**: Run API tests in CI pipeline

### DEP:TypeSafeAPI
**Trigger:** {typesafe_api_deps}

- **Schema-Share**: Single source of truth for client/server types
- **Type-Inference**: Leverage type inference, minimize explicit types
- **Error-Typed**: Type-safe error handling
- **Validation-Runtime**: Zod/Valibot at boundaries
- **Procedure-Naming**: Consistent naming (create/get/update/delete)

### DEP:DataQuery
**Trigger:** {data_query_deps}

- **Query-Keys**: Structured query keys for cache management
- **Stale-Time**: Configure staleTime based on data volatility
- **Prefetch**: Prefetch on hover/route transition
- **Optimistic-Updates**: Optimistic mutations with rollback
- **Infinite-Queries**: Use infinite queries for pagination
- **Suspense-Mode**: Use Suspense mode for cleaner loading states

### DEP:CSS
**Trigger:** {css_deps}

- **Utility-First**: Utility classes for common patterns
- **Component-Extraction**: Extract component classes for repeated patterns
- **Design-Tokens**: Use CSS variables/tokens for consistency
- **Dark-Mode**: Support dark mode with theme variables
- **Responsive-Mobile-First**: Mobile-first responsive design
- **Build-Purge**: Purge unused styles in production

### DEP:WebSocket
**Trigger:** {websocket_deps}

*These rules EXTEND API:WebSocket rules. Apply both sets when WebSocket is detected.*

- **Reconnect-Auto**: Automatic reconnection with exponential backoff
- **Heartbeat-Ping**: Ping/pong for connection health
- **Message-Queue**: Queue messages during disconnect
- **Binary-Efficient**: Binary for large payloads
- **Auth-Token**: Authenticate via token in connection

### DEP:StateManagement
**Trigger:** {state_mgmt_deps}

- **Atomic-Updates**: Atomic state updates, avoid nested mutations
- **Selector-Memoize**: Memoized selectors for derived state
- **Actions-Named**: Named actions for debugging
- **DevTools-Enable**: Enable devtools in development
- **Persistence**: Persist critical state to storage
- **Hydration-SSR**: Handle SSR hydration correctly

### DEP:AIAgent
**Trigger:** {ai_agent_deps}

- **Agent-Orchestration**: Multi-agent coordination with clear ownership boundaries
- **Memory-Management**: Conversation history limits, context window awareness
- **Tool-Definition**: Structured tool schemas with input/output validation
- **Retry-Strategy**: Agent failure recovery with exponential backoff
- **Cost-Control**: Token usage monitoring, budget limits per operation
- **Observability-Trace**: Trace agent decisions, tool calls, and reasoning steps
- **Timeout-Guard**: Set max execution time per agent task
- **Human-Loop**: Escalation path for uncertain decisions

### DEP:CDC
**Trigger:** {cdc_deps}

- **Idempotent-Apply**: Idempotent change application (handle replays)
- **Schema-Evolution**: Support schema changes without downtime
- **Ordering-Guarantee**: Preserve event ordering within partition
- **Offset-Commit**: Commit offsets after successful processing
- **Backpressure-Handle**: Handle consumer lag gracefully
- **Dead-Letter**: Route failed events to dead-letter queue

### DEP:DBMigrations
**Trigger:** {db_migration_deps}

- **Version-Order**: Sequential version numbering
- **Reversible-Prefer**: Prefer reversible migrations (up/down)
- **Atomic-Migration**: Single atomic transaction per migration
- **Lock-Short**: Use short-duration locks, batch large table operations
- **Data-Separate**: Data migrations separate from schema changes
- **Test-Migration**: Test migrations on production-like data

### DEP:ErrorTracking
**Trigger:** {error_tracking_deps}

- **Context-Rich**: Include user, request, environment context
- **Grouping-Smart**: Configure error grouping rules
- **Source-Maps**: Upload source maps for readable stack traces
- **PII-Scrub**: Scrub PII before sending
- **Rate-Limit**: Rate limit error reporting
- **Release-Track**: Tag errors with release version

### DEP:FeatureFlags
**Trigger:** {feature_flag_deps}

- **Flag-Naming**: Consistent naming convention (feature_name_enabled)
- **Targeting-Rules**: User/segment targeting with clear precedence
- **Gradual-Rollout**: Percentage-based rollout with monitoring
- **Kill-Switch**: Emergency disable without deployment
- **Stale-Cleanup**: Remove old flags regularly (30-90 days)
- **Default-Safe**: Safe defaults when flag service unavailable

### DEP:GraphQLTools
**Trigger:** {graphql_tools_deps}

- **Schema-First**: Schema-first design with code generation
- **Resolver-Efficient**: Use DataLoader pattern to batch database queries
- **Depth-Limit**: Limit query depth to prevent abuse
- **Cost-Analysis**: Query cost analysis before execution
- **Persisted-Queries**: Use persisted queries in production
- **Federation-Ready**: Design for future federation

### DEP:HeadlessCMS
**Trigger:** {headless_cms_deps}

- **Preview-Mode**: Draft content preview before publish
- **Webhook-Subscribe**: Subscribe to content change webhooks
- **Cache-Invalidate**: Invalidate cache on content change
- **Asset-Optimize**: Optimize media assets at edge
- **Locale-Support**: Multi-locale content structure
- **Fallback-Content**: Fallback for missing translations

### DEP:IncidentMgmt
**Trigger:** {incident_deps}

- **Alert-Severity**: Clear severity levels (P0-P3)
- **Escalation-Path**: Defined escalation paths
- **Runbook-Link**: Link alerts to runbooks
- **Ack-Timeout**: Auto-escalate unacknowledged alerts
- **Dedup-Rules**: Deduplicate related alerts
- **Postmortem-Template**: Standardized postmortem template

### DEP:LocalFirst
**Trigger:** {local_first_deps}

- **Offline-First**: Full functionality without network
- **Conflict-Resolution**: Clear conflict resolution strategy (LWW, CRDT)
- **Sync-Incremental**: Incremental sync, not full refresh
- **Storage-Quota**: Handle storage quota exceeded
- **Migration-Local**: Local schema migration strategy
- **Encryption-At-Rest**: Encrypt local data at rest

### DEP:SchemaRegistry
**Trigger:** {schema_registry_deps}

- **Compatibility-Check**: Check schema compatibility before deploy
- **Version-Immutable**: Schema versions are immutable
- **Evolution-Rules**: Define allowed evolution (backward/forward/full)
- **Schema-ID-Header**: Include schema ID in message headers
- **Cache-Schemas**: Cache schemas locally for performance
- **Dead-Letter-Invalid**: Route schema-invalid messages to DLQ

### DEP:Effect
**Trigger:** {effect_deps}

- **Effect-Composition**: Compose effects with pipe/flow for flat, readable chains
- **Schema-Validation**: Use Effect.Schema for runtime validation with type inference
- **Error-Typed**: Define explicit typed error channels for each failure mode
- **Generator-Style**: Prefer Effect.gen for async-like syntax
- **Context-Layers**: Use Layers for dependency injection
- **Resource-Scoped**: Use Scope for resource lifecycle management
- **Fiber-Concurrency**: Use fibers for structured concurrency
- **Retry-Schedule**: Use Schedule for retry and repeat policies
- **Stream-Processing**: Use Stream for incremental data processing
- **Config-Provider**: Use Config for type-safe configuration

### DEP:AISDK
**Trigger:** {ai_sdk_deps}

- **Provider-Abstract**: Use provider abstraction for model switching
- **Stream-Default**: Prefer streaming responses for better UX
- **Tool-Calling**: Use structured tool calling with typed schemas
- **Message-History**: Manage conversation history with proper context limits
- **Error-Boundary**: Wrap AI calls in error boundaries for graceful fallback
- **Rate-Limit-Handle**: Handle rate limits with exponential backoff
- **Token-Count**: Track token usage for cost management
- **Abort-Controller**: Support request cancellation with AbortController
- **Cache-Responses**: Cache identical requests where appropriate
- **Type-Safe-Output**: Use generateObject for structured outputs

### DEP:FormValidation
**Trigger:** {form_validation_deps}

- **Schema-First**: Define schema once, derive types and validation
- **Progressive-Enhance**: Work without JavaScript, enhance with client validation
- **Error-Display**: Field-level errors with clear messages
- **Server-Validate**: Always validate on server, client is convenience
- **Type-Inference**: Leverage type inference from schema
- **Constraint-Validation**: Use HTML5 constraints where applicable
- **Accessibility**: Associate errors with fields using aria-describedby
- **Nested-Forms**: Support nested objects and arrays
- **Custom-Validators**: Reusable validation functions
- **Transform-Coerce**: Handle type coercion explicitly

### DEP:TanStack
**Trigger:** {tanstack_deps}

- **File-Routes**: Use file-based routing with type-safe paths
- **Loader-Data**: Use loaders for data fetching with automatic caching
- **Search-Params**: Type-safe search params with validation
- **Pending-UI**: Show pending UI during navigation
- **Error-Boundary**: Route-level error boundaries
- **Prefetch-Links**: Prefetch on intent for faster navigation
- **SSR-Ready**: Configure for SSR with streaming support
- **Router-Context**: Use router context for shared data
- **Code-Split**: Automatic code splitting per route
- **Devtools**: Enable devtools in development

## Infrastructure Rules

### Infra:APIGateway
**Trigger:** {api_gateway_config}, {api_gateway_deps}

- **Rate-Limit-Config**: Per-route rate limiting with burst allowance
- **Auth-Plugin**: Centralized authentication at gateway
- **Route-Versioning**: API version routing (header or path)
- **Circuit-Breaker-Route**: Per-upstream circuit breaker
- **Logging-Structured**: Structured request/response logging
- **CORS-Config**: Centralized CORS configuration
- **Timeout-Upstream**: Upstream timeout configuration

### Infra:ServiceMesh
**Trigger:** {service_mesh_config}, {service_mesh_deps}

- **mTLS-Enable**: Enable mutual TLS between services
- **Retry-Policy**: Service-level retry policies
- **Timeout-Budget**: Request timeout budgets
- **Traffic-Split**: Traffic splitting for canary deployments
- **Observability-Auto**: Auto-inject observability sidecars
- **Auth-Policy**: Service-to-service authorization policies

### Infra:BuildCache
**Trigger:** {build_cache_config}

- **Cache-Key**: Deterministic cache key generation
- **Remote-Cache**: Enable remote cache for CI
- **Artifact-Share**: Share build artifacts across pipelines
- **Invalidation-Explicit**: Explicit cache invalidation rules
- **Size-Limit**: Cache size limits per project
- **TTL-Set**: Set cache TTL based on artifact type

---

## Trigger Reference

| Symbol | Meaning | Detection Source | Output |
|--------|---------|------------------|--------|
| L: | Language | Manifest, lock files, code | `{lang}.md` |
| R: | Runtime | Lock file type, config | `{runtime}.md` |
| T: | App Type | Entry points, exports | `{type}.md` |
| API: | API Style | Routes, decorators, proto | `api.md` |
| DB: | Database | ORM deps, migrations | `database.md` |
| Backend: | Backend Framework | Framework deps, patterns | `backend.md` |
| Frontend: | Frontend | Framework deps, components | `frontend.md` |
| Framework: | Meta-Framework | Next/Nuxt/SvelteKit/Remix | `{framework}.md` |
| Mobile: | Mobile | SDK deps, native configs | `mobile.md` |
| Desktop: | Desktop | Electron/Tauri deps | `desktop.md` |
| Infra: | Infrastructure | Dockerfile, *.tf, k8s/, gateway/mesh configs | `infra-{category}.md` |
| ML: | Machine Learning | ML framework deps | `ml.md` |
| Build: | Build Tools | Bundler, monorepo configs | `{build}.md` |
| Test: | Testing | Test framework, tests/ | `testing.md` |
| CI: | CI/CD | Workflow files | `ci-cd.md` |
| MQ: | Message Queues | Queue deps, configs | `mq.md` |
| ORM: | ORM Specific | ORM deps (Exposed, etc.) | `orm.md` |
| DEP: | Dependency | Specific package deps | `dep-{category}.md` |
| Game: | Game Engines | Unity/Unreal/Godot markers | `game.md` |
| RT: | Real-time | WebSocket/SSE patterns | `realtime.md` |
| Observability: | Monitoring | APM/Logging/Tracing deps | `observability-tools.md` |
| Deploy: | Deployment | Platform configs | `deploy.md` |
| Docs: | Documentation | SSG configs | `docs.md` |
