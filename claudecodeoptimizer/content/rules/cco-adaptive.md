# Adaptive Rules
*Selected by /cco-config based on detection. Each rule evaluated individually.*
*Used as template pool for generating .claude/rules/ files with path-specific frontmatter.*

## Detection System

### Auto-Detect (Manifest/Code Scan)

Detection organized by category. See cco-agent-analyze.md for detailed trigger patterns.

| Category | Key Triggers | Output |
|----------|--------------|--------|
| **Languages** |||
| L:Python | pyproject.toml, requirements*.txt, *.py | `python.md` |
| L:TypeScript | tsconfig.json, *.ts/*.tsx | `typescript.md` |
| L:JavaScript | package.json (no TS), *.js | `javascript.md` |
| L:Go | go.mod, *.go | `go.md` |
| L:Rust | Cargo.toml, *.rs | `rust.md` |
| L:Java | pom.xml, build.gradle, *.java | `java.md` |
| L:Kotlin | *.kt, kotlin in gradle | `kotlin.md` |
| L:Swift | Package.swift, *.swift | `swift.md` |
| L:CSharp | *.csproj, *.sln, *.cs | `csharp.md` |
| L:Ruby | Gemfile, *.gemspec, *.rb | `ruby.md` |
| L:PHP | composer.json, *.php | `php.md` |
| L:Elixir | mix.exs, *.ex | `elixir.md` |
| L:Gleam | gleam.toml, *.gleam | `gleam.md` |
| L:Scala | build.sbt, *.scala | `scala.md` |
| L:Zig | build.zig, *.zig | `zig.md` |
| L:Dart | pubspec.yaml, *.dart | `dart.md` |
| **Project Types** |||
| T:CLI | [project.scripts], typer/click/cobra, bin/ | `cli.md` |
| T:Library | exports, __all__, [lib] | `library.md` |
| T:Service | Dockerfile + ports, long-running | `service.md` |
| **API Styles** |||
| API:REST | routes/, FastAPI/Express/Gin routes | `api.md` |
| API:GraphQL | *.graphql, apollo/type-graphql | `api.md` |
| API:gRPC | *.proto, grpc deps | `api.md` |
| **Database** |||
| DB:SQL | sqlite3/psycopg2/pg, migrations/ | `database.md` |
| DB:ORM | sqlalchemy/prisma/drizzle/gorm | `database.md` |
| DB:NoSQL | pymongo/redis/dynamodb | `database.md` |
| DB:Vector | pgvector/pinecone/chroma | `database.md` |
| **Frontend** |||
| Frontend:React | react deps, *.jsx/*.tsx | `frontend.md` |
| Frontend:Vue | vue deps, *.vue | `frontend.md` |
| Frontend:Svelte | svelte deps, *.svelte | `frontend.md` |
| Frontend:Angular | @angular deps, *.component.ts | `frontend.md` |
| Frontend:Solid | solid-js deps | `frontend.md` |
| Frontend:Astro | astro deps, *.astro | `frontend.md` |
| Frontend:HTMX | htmx deps, hx-* in HTML | `frontend.md` |
| **Mobile** |||
| Mobile:Flutter | pubspec.yaml, *.dart | `mobile.md` |
| Mobile:ReactNative | react-native/expo deps | `mobile.md` |
| Mobile:iOS | *.xcodeproj, Podfile, *.swift | `mobile.md` |
| Mobile:Android | build.gradle, AndroidManifest.xml | `mobile.md` |
| Mobile:KMP | kotlin-multiplatform, shared/ | `mobile.md` |
| **Infrastructure** |||
| Infra:Docker | Dockerfile, docker-compose.yml | `container.md` |
| Infra:K8s | k8s/, helm/, kustomization.yaml | `k8s.md` |
| Infra:Terraform | *.tf files | `terraform.md` |
| Infra:Pulumi | Pulumi.yaml | `pulumi.md` |
| Infra:CDK | cdk.json, *-stack.ts | `cdk.md` |
| Infra:Edge | wrangler.toml, vercel edge, deno deploy | `edge.md` |
| Infra:WASM | *.wasm, wasm-pack, wit-bindgen | `wasm.md` |
| Infra:Serverless | serverless.yml, sam.yaml | `serverless.md` |
| **ML/AI** |||
| ML:Training | torch/tensorflow/sklearn | `ml.md` |
| ML:LLM | langchain/llamaindex/haystack | `ml.md` |
| ML:Inference | transformers/onnxruntime/vllm | `ml.md` |
| ML:SDK | openai/anthropic/cohere | `ml.md` |
| **Build** |||
| Build:Monorepo | nx.json, turbo.json, workspaces | `monorepo.md` |
| Build:Bundler | vite/webpack/esbuild/tsup | `bundler.md` |
| Build:Linter | .eslintrc*, biome.json, ruff.toml | `linter.md` |
| Build:Formatter | .prettierrc*, biome.json | `formatter.md` |
| Build:TypeChecker | tsconfig.json, mypy.ini | `typechecker.md` |
| **Desktop** |||
| Desktop:Electron | electron deps, electron-builder | `desktop.md` |
| Desktop:Tauri | tauri deps, tauri.conf.json | `desktop.md` |
| **Runtimes** |||
| R:Node | package.json, node_modules/ | `node.md` |
| R:Bun | bun.lockb, bunfig.toml | `bun.md` |
| R:Deno | deno.json, deno.lock | `deno.md` |
| **Testing** |||
| Test:Unit | pytest/jest/vitest, tests/ | `testing.md` |
| Test:E2E | playwright/cypress, e2e/ | `testing.md` |
| Test:Coverage | [tool.coverage], .nycrc | `testing.md` |
| **CI/CD** |||
| CI:GitHub | .github/workflows/ | `ci-cd.md` |
| CI:GitLab | .gitlab-ci.yml | `ci-cd.md` |
| CI:Jenkins | Jenkinsfile | `ci-cd.md` |
| CI:CircleCI | .circleci/config.yml | `ci-cd.md` |
| CI:Azure | azure-pipelines.yml | `ci-cd.md` |
| CI:ArgoCD | argocd/, Application.yaml | `ci-cd.md` |
| **Specialized** |||
| Game:Unity | *.csproj + Unity, Assets/ | `game.md` |
| Game:Unreal | *.uproject, Source/ | `game.md` |
| Game:Godot | project.godot, *.gd | `game.md` |
| i18n | locales/, react-i18next | `i18n.md` |
| RT:Basic | ws/socket.io/websockets | `realtime.md` |
| RT:LowLatency | protobuf + ws, msgpack | `realtime.md` |
| API:WebSocket | ws/socket.io/websockets | `api.md` |
| **DEP:* (37 categories)** |||
| DEP:CLI | typer/click/argparse/cobra | `dep-cli.md` |
| DEP:TUI | rich/textual/urwid | `dep-tui.md` |
| DEP:Validation | pydantic/zod/joi | `dep-validation.md` |
| DEP:Config | pydantic-settings/dotenv | `dep-config.md` |
| DEP:Testing | pytest/jest/playwright | `dep-testing.md` |
| DEP:Edge | @cloudflare/workers/wrangler | `dep-edge.md` |
| DEP:EdgeFramework | hono/elysia/h3/nitro | `dep-edgeframework.md` |
| DEP:WASM | wasm-pack/wasm-bindgen | `dep-wasm.md` |
| DEP:HTTP | requests/axios/httpx | `dep-http.md` |
| DEP:ORM | sqlalchemy/prisma/drizzle | `dep-orm.md` |
| DEP:Auth | passlib/passport/lucia | `dep-auth.md` |
| DEP:Cache | redis/memcached/keyv | `dep-cache.md` |
| DEP:Queue | celery/bull/dramatiq | `dep-queue.md` |
| DEP:Search | elasticsearch/meilisearch | `dep-search.md` |
| DEP:GPU | cuda/torch+cuda/jax | `dep-gpu.md` |
| DEP:HeavyModel | transformers/langchain | `dep-heavymodel.md` |
| DEP:DataHeavy | pandas/polars/dask | `dep-data.md` |
| DEP:Image | pillow/opencv/imageio | `dep-image.md` |
| DEP:Audio | pydub/librosa/whisper | `dep-audio.md` |
| DEP:Video | ffmpeg/moviepy/decord | `dep-video.md` |
| DEP:Logging | loguru/structlog/pino | `dep-logging.md` |
| DEP:ObjectStore | boto3/minio/cloudinary | `dep-storage.md` |
| DEP:Payment | stripe/paypal/braintree | `dep-payment.md` |
| DEP:Email | sendgrid/resend/nodemailer | `dep-email.md` |
| DEP:SMS | twilio/vonage/messagebird | `dep-sms.md` |
| DEP:Notification | firebase/onesignal/pusher | `dep-notification.md` |
| DEP:PDF | reportlab/weasyprint/pdfkit | `dep-pdf.md` |
| DEP:Excel | openpyxl/xlsxwriter/sheetjs | `dep-excel.md` |
| DEP:Scraping | scrapy/beautifulsoup/crawlee | `dep-scraping.md` |
| DEP:Blockchain | web3/ethers/hardhat | `dep-blockchain.md` |
| DEP:Crypto | cryptography/nacl/argon2 | `dep-crypto.md` |
| DEP:GamePython | pygame/arcade/panda3d | `dep-game-python.md` |
| DEP:GameJS | phaser/three.js/pixi.js | `dep-game-js.md` |
| DEP:GameEngine | Unity/Unreal/Godot | `dep-gameengine.md` |
| DEP:ARVR | openxr/webxr/ar-foundation | `dep-arvr.md` |
| DEP:IoT | micropython/paho-mqtt/esphome | `dep-iot.md` |

### User-Input (AskUserQuestion) [MANDATORY]

**CRITICAL:** These questions MUST be asked. Cannot be skipped or auto-inferred.

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

When generating rule files, use YAML frontmatter:

```markdown
---
paths: **/*.py
---
# Python Rules

- **Type-Hints**: Type annotations for public APIs
```

---

## Language Rules

### Python (L:Python)
**Trigger:** pyproject.toml | setup.py | requirements.txt | *.py

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

### TypeScript (L:TypeScript)
**Trigger:** tsconfig.json | *.ts/*.tsx

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
**Trigger:** package.json without TS | *.js/*.jsx only

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
**Trigger:** go.mod | *.go

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
**Trigger:** Cargo.toml | *.rs

- **Result-Propagate**: Use ? operator for error propagation
- **Ownership-Clear**: Clear ownership patterns, minimize clones
- **Clippy-Clean**: No clippy warnings in CI
- **Unsafe-Minimize**: Minimize unsafe blocks, document when necessary
- **Async-Traits**: Use async fn in traits (Rust 1.75+)
- **Let-Chains**: Use let chains for complex conditionals
- **Error-Thiserror**: Use thiserror for library errors, anyhow for applications

### Java (L:Java)
**Trigger:** pom.xml | build.gradle | *.java

- **Null-Safety**: Use Optional<T> for nullable returns
- **Resource-Try**: try-with-resources for AutoCloseable
- **Immutable-Prefer**: Prefer immutable objects, final fields
- **Stream-API**: Use Stream API for collection transformations
- **Records**: Use records for immutable data carriers (Java 14+)
- **Pattern-Switch**: Use pattern matching in switch (Java 21+)
- **Virtual-Threads**: Use virtual threads for high-concurrency I/O (Java 21+)
- **Sealed-Classes**: Use sealed classes for controlled inheritance

### Kotlin (L:Kotlin)
**Trigger:** build.gradle.kts + kotlin | *.kt

- **Null-Safe**: Use nullable types (?), avoid !! operator
- **Data-Class**: Data classes for DTOs and value objects
- **Coroutine-Structured**: Structured concurrency with coroutineScope
- **Extension-Limit**: Extension functions for utility, not core logic

### Swift (L:Swift)
**Trigger:** Package.swift | *.xcodeproj | *.swift

- **Optional-Guard**: Use guard let for early exits
- **Protocol-Oriented**: Protocol-oriented design over inheritance
- **Value-Type**: Prefer structs over classes when possible
- **Actor-Concurrency**: Use actors for shared mutable state
- **Async-Await**: Use async/await for asynchronous code
- **Observation**: Use @Observable macro for reactive state (iOS 17+)
- **Result-Builder**: Use result builders for DSLs

### C# (L:CSharp)
**Trigger:** *.csproj | *.sln | *.cs

- **Nullable-Enable**: Enable nullable reference types
- **Async-Await**: async/await for I/O operations
- **Dispose-Pattern**: IDisposable with using statements
- **Record-Type**: Records for immutable data transfer
- **Primary-Constructors**: Use primary constructors for DI (C# 12+)
- **Collection-Expressions**: Use collection expressions [...] (C# 12+)
- **Pattern-Matching**: Use pattern matching for type checks and deconstruction

### Ruby (L:Ruby)
**Trigger:** Gemfile | *.gemspec | *.rb

- **Freeze-Strings**: Use frozen_string_literal pragma
- **Block-Yield**: Prefer yield over block.call
- **Method-Visibility**: Explicit private/protected declarations
- **Type-Check**: Static type checking (Sorbet or RBS) for public APIs
- **Pattern-Match**: Use pattern matching for complex conditionals (Ruby 3.0+)
- **Ractor-Thread-Safe**: Use Ractor for thread-safe parallelism (Ruby 3.0+)
- **Data-Class**: Use Data.define for immutable value objects (Ruby 3.2+)

### PHP (L:PHP)
**Trigger:** composer.json | *.php

- **Type-Declare**: Strict type declarations (declare(strict_types=1))
- **PSR-Standards**: Follow PSR-4 autoloading, PSR-12 style
- **Null-Safe**: Use null coalescing (??) and null-safe operator (?->)
- **Constructor-Promotion**: Property promotion in constructors (8.0+)
- **Enums**: Use native enums for fixed value sets (8.1+)
- **Readonly-Properties**: Use readonly for immutable properties (8.1+)
- **Attributes**: Use attributes instead of docblock annotations (8.0+)

### Elixir (L:Elixir)
**Trigger:** mix.exs | *.ex | *.exs

- **Pattern-Match**: Pattern matching over conditionals
- **Pipe-Operator**: Use |> for data transformations
- **GenServer-State**: Stateful processes via GenServer
- **Dialyzer-Types**: Typespecs for public functions

### Gleam (L:Gleam)
**Trigger:** gleam.toml | *.gleam

- **Result-Type**: Use Result(a, e) for fallible operations
- **Pattern-Exhaustive**: Exhaustive pattern matching
- **Pipeline-Style**: Use |> for function composition
- **Label-Args**: Use labelled arguments for clarity

### Scala (L:Scala)
**Trigger:** build.sbt | *.scala

- **Option-Not-Null**: Option[T] instead of null
- **Case-Class**: Case classes for immutable data
- **For-Comprehension**: For-comprehensions for monadic operations
- **Implicit-Minimal**: Minimize implicit conversions

### Zig (L:Zig)
**Trigger:** build.zig | *.zig

- **Error-Union**: Use error unions for fallible functions
- **Comptime**: Leverage comptime for zero-cost abstractions
- **No-Hidden-Alloc**: Explicit allocator passing
- **Defer-Cleanup**: defer/errdefer for cleanup

### Dart (L:Dart)
**Trigger:** pubspec.yaml | *.dart

- **Null-Safety**: Sound null safety with ? and !
- **Async-Await**: async/await for Future operations
- **Named-Params**: Named parameters for readability
- **Immutable-Widget**: StatelessWidget when state not needed

---

## Security Rules
**Trigger:** D:PII | D:Regulated | Scale:Large | Compliance:*

- **Input-Validation**: Validate ALL user input at system boundaries. Use schema validation. Reject invalid, don't sanitize-and-continue
- **Input-Bounds**: Set max lengths, max sizes, max items on ALL user inputs. Prevent resource exhaustion
- **Input-Whitespace**: Normalize whitespace (strip, reject whitespace-only). Common injection vector
- **SQL-Safe**: Parameterized queries only, no string concatenation
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
- **Deserialize-Safe**: Never deserialize untrusted data. Use safe alternatives (JSON over pickle/yaml)
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
- **PCI-No-Storage**: Never store CVV/CVC
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

## Observability Rules
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

## Backend > API
**Trigger:** API:REST | API:GraphQL | API:gRPC

- **REST-Methods**: Proper HTTP verbs and status codes
- **Pagination**: Cursor-based pagination for lists
- **OpenAPI-Spec**: Synced spec with examples
- **Error-Format**: Consistent format, no stack traces in prod

### GraphQL Extension
**Trigger:** API:GraphQL

- **GQL-Limits**: Query depth and complexity limits
- **GQL-Persisted**: Persisted queries in production

### gRPC Extension
**Trigger:** API:gRPC

- **Proto-Version**: Backward compatible proto changes

---

## Backend > Data
**Trigger:** DB:*

- **Backup-Strategy**: Automated backups with tested restore
- **Schema-Versioned**: Migration files with rollback plan
- **Connection-Secure**: SSL/TLS, credentials in env vars
- **Query-Timeout**: Prevent runaway queries

---

## Backend > Operations
**Trigger:** CI/CD detected

### Full Operations (T:API | T:Frontend | Architecture:Microservices)
- **Config-as-Code**: Versioned, environment-aware config
- **Health-Endpoints**: /health + /ready endpoints
- **Graceful-Shutdown**: Drain connections on SIGTERM
- **Observability**: Metrics + logs + traces
- **CI-Gates**: lint + test + coverage gates
- **Zero-Downtime**: Blue-green or canary deployments
- **Feature-Flags**: Decouple deploy from release

### CI-Only Operations (T:CLI | T:Library)
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
**Trigger:** react/react-dom deps, *.jsx/*.tsx

- **Hooks-Rules**: Rules of Hooks (top-level, same order)
- **Memo-Strategic**: useMemo/useCallback for expensive ops only
- **Key-Stable**: Stable keys for lists (not index)
- **Effect-Cleanup**: Cleanup in useEffect return
- **Server-Components**: Use Server Components for data fetching, Client for interactivity (Next.js/RSC)
- **Use-Hook**: Use use() hook for promises and context (React 19+)
- **Suspense-Boundary**: Wrap async components in Suspense with fallback
- **Actions**: Use Server Actions for mutations (Next.js 14+)

### Vue (Frontend:Vue)
**Trigger:** vue deps, *.vue

- **Composition-API**: Composition API over Options API (Vue 3+)
- **Reactive-Unwrap**: .value access for refs in script
- **Provide-Inject**: Provide/inject for deep prop drilling
- **SFC-Style**: Scoped styles in single-file components
- **Script-Setup**: Use <script setup> for cleaner syntax
- **Definemodel**: Use defineModel for v-model with props (Vue 3.4+)
- **Vapor-Mode**: Consider Vapor mode for performance-critical components (Vue 3.5+)

### Angular (Frontend:Angular)
**Trigger:** @angular deps, *.component.ts

- **Standalone-Components**: Standalone components (Angular 14+)
- **Signals-Reactive**: Signals for reactive state (Angular 16+)
- **OnPush-Strategy**: OnPush change detection for performance
- **Lazy-Modules**: Lazy load feature modules

### Svelte (Frontend:Svelte)
**Trigger:** svelte deps, *.svelte

- **Reactivity-Native**: Use framework reactivity (Svelte 5: runes, Svelte 4: stores)
- **Store-Subscribe**: Auto-subscribe with $ prefix (stores) or $state (runes)
- **Transitions-Native**: Use built-in transitions
- **Actions-Reusable**: Reusable actions for DOM behavior

### Solid (Frontend:Solid)
**Trigger:** solid-js deps

- **Signal-Fine-Grained**: Fine-grained reactivity with signals
- **Memo-Derived**: createMemo for derived computations
- **Effect-Track**: Track dependencies explicitly
- **No-Destructure**: Don't destructure props (breaks reactivity)

### Astro (Frontend:Astro)
**Trigger:** astro deps, *.astro

- **Islands-Minimal**: client:* directives only when needed
- **Content-Collections**: Content collections for markdown/MDX
- **Static-Default**: Static by default, SSR when needed
- **Partial-Hydration**: Selective hydration strategies

### HTMX (Frontend:HTMX)
**Trigger:** htmx deps, hx-* attributes in HTML

- **Hypermedia-API**: Return HTML fragments, not JSON
- **Target-Precise**: Precise hx-target selectors
- **Swap-Strategy**: Appropriate hx-swap (innerHTML, outerHTML, etc)
- **Indicator-Feedback**: Loading indicators with hx-indicator

---

## Desktop
**Trigger:** Electron/Tauri detected

### Base Desktop Rules
- **IPC-Secure**: Validate all IPC messages
- **Auto-Update**: Built-in update mechanism
- **Native-Feel**: Platform-appropriate UI/UX
- **Offline-First**: Graceful offline handling

### Electron (Desktop:Electron)
**Trigger:** electron deps, electron-builder.yml

- **Context-Isolation**: contextIsolation: true always
- **Sandbox-Enable**: sandbox: true for renderers
- **Preload-Bridge**: Expose APIs via preload scripts only
- **CSP-Strict**: Content Security Policy in HTML

### Tauri (Desktop:Tauri)
**Trigger:** tauri deps, tauri.conf.json

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
**Trigger:** pubspec.yaml, *.dart

- **Widget-Const**: Use const constructors
- **State-Provider**: Provider/Riverpod for state
- **Platform-Channel**: Platform channels for native APIs
- **Build-Modes**: Different configs for debug/release

### React Native (Mobile:ReactNative)
**Trigger:** react-native/expo deps

- **Native-Modules**: TurboModules/New Architecture for performance
- **Metro-Optimize**: Optimize Metro bundler config
- **Hermes-Enable**: Hermes engine for Android
- **Workflow-Match**: Choose managed (Expo) or bare based on native module needs

### iOS Native (Mobile:iOS)
**Trigger:** *.xcodeproj, Podfile, *.swift

- **SwiftUI-Modern**: SwiftUI over UIKit when possible
- **Combine-Reactive**: Combine for reactive patterns
- **App-Privacy**: Privacy manifest and descriptions
- **TestFlight-Beta**: TestFlight for beta testing

### Android Native (Mobile:Android)
**Trigger:** build.gradle, AndroidManifest.xml

- **Compose-Modern**: Jetpack Compose over XML layouts
- **ViewModel-State**: ViewModel + StateFlow for state
- **WorkManager-Background**: WorkManager for background work
- **R8-Shrink**: Enable R8 code shrinking

### Kotlin Multiplatform (Mobile:KMP)
**Trigger:** kotlin-multiplatform, shared/

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
**Trigger:** Dockerfile, docker-compose.yml

- **Multi-Stage**: Multi-stage builds for smaller images
- **Layer-Cache**: Order commands for optimal layer caching
- **Non-Root**: Run as non-root user
- **Health-Check**: HEALTHCHECK instruction for orchestrators
- **Env-Inject**: Environment variables for configuration
- **Buildkit-Secrets**: Use --mount=type=secret for sensitive build args
- **Cache-Mounts**: Use --mount=type=cache for package managers
- **Distroless**: Use distroless or alpine for production images

### Kubernetes (Infra:K8s)
**Trigger:** k8s/, helm/, kustomization.yaml

- **Resource-Limits**: CPU/memory requests and limits
- **Liveness-Readiness**: Health probes configured
- **Config-Secrets**: ConfigMaps and Secrets, not hardcoded
- **RBAC-Minimal**: Least privilege service accounts
- **HPA-Defined**: Horizontal Pod Autoscaler for scaling
- **Gateway-API**: Use Gateway API over Ingress for advanced routing (K8s 1.27+)
- **Pod-Disruption**: PodDisruptionBudget for availability during updates
- **Security-Context**: runAsNonRoot, readOnlyRootFilesystem, drop capabilities

### Terraform (Infra:Terraform)
**Trigger:** *.tf files

- **State-Remote**: Remote state backend (S3, GCS, etc.)
- **Modules-Reuse**: Reusable modules for common patterns
- **Variables-Type**: Typed variables with descriptions
- **Output-Document**: Outputs for cross-module references
- **Plan-Before-Apply**: Always plan before apply
- **Moved-Blocks**: Use moved blocks for refactoring without recreation
- **Import-Blocks**: Use import blocks for existing resources (TF 1.5+)
- **Check-Blocks**: Use check blocks for post-apply validation (TF 1.5+)

### Pulumi (Infra:Pulumi)
**Trigger:** Pulumi.yaml

- **Stack-Per-Env**: Separate stacks per environment
- **Config-Secrets**: Encrypted secrets in config
- **Type-Safe**: Leverage language type system
- **Preview-Always**: Preview before up

### CDK (Infra:CDK)
**Trigger:** cdk.json, lib/*-stack.ts

- **Construct-Library**: Reusable L3 constructs
- **Stack-Separation**: Logical stack boundaries
- **Context-Values**: Environment-specific context
- **Synth-Test**: Test synthesized templates
- **Aspects-Cross-Cut**: Use Aspects for cross-cutting concerns

### Serverless (Infra:Serverless)
**Trigger:** serverless.yml, sam.yaml

- **Cold-Start**: Minimize cold start time
- **Timeout-Set**: Explicit function timeouts
- **Memory-Tune**: Right-size memory allocation
- **Event-Validate**: Validate event payloads

### Edge (Infra:Edge)
**Trigger:** wrangler.toml, vercel.json edge

- **Size-Minimal**: Bundle size under limits
- **Stateless**: No persistent in-memory state
- **KV-Access**: Edge KV for data persistence
- **Geo-Route**: Geographic routing when needed

### WASM (Infra:WASM)
**Trigger:** *.wasm, wasm-pack.toml

- **Size-Optimize**: Optimize for size (-Os, wasm-opt)
- **Memory-Linear**: Manage linear memory explicitly
- **Interface-Types**: Use interface types for interop
- **Streaming**: Stream instantiation for large modules

---

## Build Tools

### Monorepo (Build:Monorepo)
**Trigger:** nx.json, turbo.json, pnpm-workspace.yaml

- **Affected-Only**: Build only affected packages
- **Cache-Remote**: Remote build cache enabled
- **Deps-Graph**: Explicit dependency graph
- **Consistent-Versions**: Shared dependency versions

### Bundler (Build:Bundler)
**Trigger:** vite.config.*, webpack.config.*, esbuild

- **Tree-Shake**: Enable tree shaking
- **Code-Split**: Split by route/feature
- **Source-Maps**: Source maps for debugging
- **Minify-Prod**: Minify in production only

### Linter (Build:Linter)
**Trigger:** .eslintrc*, biome.json, ruff.toml

- **CI-Enforce**: Lint in CI pipeline
- **Auto-Fix**: Auto-fix where safe
- **Ignore-Explicit**: Explicit ignore patterns
- **Severity-Config**: Error vs warning levels

### Formatter (Build:Formatter)
**Trigger:** .prettierrc*, biome.json

- **Pre-Commit**: Format on commit
- **Config-Share**: Shared config across team
- **Editor-Integrate**: Editor integration

### TypeChecker (Build:TypeChecker)
**Trigger:** tsconfig.json, mypy.ini

- **Strict-Enable**: Enable strict mode
- **Incremental**: Incremental compilation
- **CI-Check**: Type check in CI

---

## Testing

### Unit Testing (Test:Unit)
**Trigger:** pytest, jest, vitest, mocha

- **Isolation**: No shared state between tests
- **Fast-Feedback**: Tests complete in seconds
- **Mock-Boundaries**: Mock at system boundaries
- **Assertions-Clear**: One concept per test

### E2E Testing (Test:E2E)
**Trigger:** playwright, cypress, selenium

- **Critical-Paths**: Cover critical user journeys
- **Stable-Selectors**: data-testid attributes
- **Retry-Flaky**: Retry for network flakiness
- **Parallel-Run**: Parallel execution where possible

### Coverage (Test:Coverage)
**Trigger:** [tool.coverage], .nycrc

- **Threshold-Set**: Minimum coverage threshold
- **Branch-Cover**: Branch coverage, not just line
- **Exclude-Generated**: Exclude generated code
- **Trend-Track**: Track coverage trends

---

## CI/CD

### GitHub Actions (CI:GitHub)
**Trigger:** .github/workflows/

- **Matrix-Test**: Matrix for multiple versions
- **Cache-Deps**: Cache dependencies
- **Secrets-Safe**: Use GitHub Secrets
- **Concurrency-Limit**: Cancel redundant runs

### GitLab CI (CI:GitLab)
**Trigger:** .gitlab-ci.yml

- **Stage-Order**: Logical stage ordering
- **Cache-Key**: Proper cache key strategy
- **Artifacts-Expire**: Artifact expiration
- **Rules-Conditional**: Conditional job execution

### Jenkins (CI:Jenkins)
**Trigger:** Jenkinsfile

- **Pipeline-Declarative**: Declarative over scripted
- **Agent-Label**: Specific agent labels
- **Credentials-Bind**: Credentials binding
- **Parallel-Stages**: Parallel where independent

### CircleCI (CI:CircleCI)
**Trigger:** .circleci/config.yml

- **Orbs-Reuse**: Use orbs for common tasks
- **Workspace-Persist**: Persist between jobs
- **Resource-Class**: Appropriate resource class

### Azure DevOps (CI:Azure)
**Trigger:** azure-pipelines.yml

- **Templates-Share**: Shared YAML templates
- **Variable-Groups**: Variable groups for secrets
- **Environments-Deploy**: Environment approvals

### ArgoCD (CI:ArgoCD)
**Trigger:** argocd/, Application.yaml

- **Sync-Policy**: Auto-sync vs manual
- **Health-Check**: Custom health checks
- **Diff-Strategy**: Appropriate diff strategy

---

## ML/AI Specialized

### Training (ML:Training)
**Trigger:** torch, tensorflow, sklearn, keras

- **Seed-All**: Reproducible random seeds
- **Checkpoint-Save**: Regular checkpoints
- **Metrics-Log**: Log training metrics
- **GPU-Utilize**: Efficient GPU utilization

### LLM Orchestration (ML:LLM)
**Trigger:** langchain, llamaindex, haystack

- **Prompt-Template**: Versioned prompt templates
- **Token-Limit**: Respect context limits
- **Retry-Backoff**: Retry with exponential backoff
- **Cost-Track**: Track API costs
- **RAG-Chunk**: Chunk documents appropriately for retrieval (512-1024 tokens typical)
- **Structured-Output**: Use structured outputs/JSON mode for reliable parsing
- **Function-Calling**: Use tool/function calling for actions, not string parsing
- **Prompt-Cache**: Cache identical prompts for cost savings

### Inference (ML:Inference)
**Trigger:** transformers, onnxruntime, vllm

- **Batch-Infer**: Batch for throughput
- **Quantize-Prod**: Quantization for production
- **Timeout-Guard**: Inference timeout limits
- **Memory-Manage**: Clear model memory

### ML SDK (ML:SDK)
**Trigger:** openai, anthropic, cohere

- **Key-Rotate**: API key rotation
- **Rate-Limit**: Handle rate limits gracefully
- **Response-Validate**: Validate API responses
- **Fallback-Model**: Fallback to alternative models

---

## Runtimes

### Node.js (R:Node)
**Trigger:** package.json, node_modules/

- **LTS-Version**: Use LTS versions
- **Engine-Lock**: Lock engine version in package.json
- **ESM-Prefer**: ESM over CommonJS
- **Event-Loop**: Avoid blocking event loop

### Bun (R:Bun)
**Trigger:** bun.lockb, bunfig.toml

- **Bun-Native**: Use Bun native APIs when faster
- **Node-Compat**: Test Node.js compatibility
- **Macro-Use**: Macros for build-time optimization
- **Hot-Reload**: Leverage fast hot reload

### Deno (R:Deno)
**Trigger:** deno.json, deno.lock

- **Permissions-Minimal**: Minimal --allow flags
- **Import-Map**: Import maps for dependencies
- **Test-Native**: Use Deno.test native
- **Fresh-Edge**: Deploy to Deno Deploy edge

---

## Database Specialized

### SQL (DB:SQL)
**Trigger:** sqlite3, psycopg2, mysql-connector

- **Parameterized**: Parameterized queries always
- **Connection-Pool**: Connection pooling
- **Transaction-Explicit**: Explicit transactions
- **Index-Query**: Index for common queries

### NoSQL (DB:NoSQL)
**Trigger:** pymongo, redis, dynamodb

- **Schema-Validate**: Application-level schema validation
- **TTL-Set**: TTL for expiring data
- **Consistency-Choose**: Choose consistency level
- **Batch-Ops**: Batch operations when possible

### Vector DB (DB:Vector)
**Trigger:** pgvector, pinecone, chroma

- **Embed-Model**: Consistent embedding model
- **Dimension-Match**: Dimension consistency
- **Index-Type**: Appropriate index type (HNSW, IVF)
- **Similarity-Metric**: Correct similarity metric

---

## API Specialized

### WebSocket (API:WebSocket)
**Trigger:** ws, socket.io, websockets

- **Reconnect-Auto**: Automatic reconnection
- **Heartbeat-Ping**: Ping/pong for health
- **Message-Queue**: Queue during disconnect
- **Binary-Efficient**: Binary for large payloads

---

## Specialized > Game
**Trigger:** Unity/Unreal/Godot detected

- **Frame-Budget**: 16ms (60fps) or 8ms (120fps) target
- **Asset-LOD**: Level of detail + streaming
- **Save-Versioned**: Migration support for old saves
- **Determinism**: Fixed timestep for multiplayer/replay

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

### Low-Latency (RT:Low-latency)
- **Binary-Protocol**: Protobuf/msgpack for performance
- **Edge-Compute**: Edge deployment for global users

---

## Dependency-Based Rules

### DEP:CLI
**Trigger:** typer, click, argparse, fire, argh, docopt, cement, cliff, plac

- **Help-Comprehensive**: --help with examples, subcommand help
- **Exit-Codes**: Documented exit codes (0=success, 1=error, 2=usage)
- **Error-Messages**: Clear, actionable error messages to stderr
- **Completion-Support**: Shell completion scripts (bash/zsh/fish)
- **Config-Layers**: CLI args > env vars > config file > defaults
- **Progress-Feedback**: Progress bars/spinners for long operations
- **Color-Support**: Respect NO_COLOR, --no-color flag

### DEP:TUI
**Trigger:** rich, textual, urwid, blessed, npyscreen, prompt-toolkit, questionary, inquirer

- **Terminal-Compat**: Graceful fallback for dumb terminals
- **Color-Detect**: Auto-detect color support, respect NO_COLOR
- **Unicode-Safe**: ASCII fallback for non-unicode terminals
- **Resize-Handle**: Handle terminal resize events
- **Keyboard-Nav**: Full keyboard navigation
- **Screen-Clear**: Clean exit, restore terminal state

### DEP:Validation
**Trigger:** pydantic, attrs, marshmallow, cerberus, voluptuous, schema, typeguard, beartype, zod, valibot, yup, joi

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
**Trigger:** @cloudflare/workers-types, wrangler, vercel/edge, @deno/deploy, hono, elysia, itty-router

- **Cold-Start**: Minimize cold start (avoid heavy imports at top)
- **Bundle-Size**: Keep bundle <1MB, prefer tree-shakeable deps
- **Stateless-Default**: No in-memory state between requests
- **KV-Cache**: Use edge KV for persistence (Workers KV, Vercel Edge Config)
- **Geo-Aware**: Leverage request.cf or geo headers for localization
- **Timeout-Aware**: Edge functions have short timeouts (30s-60s)
- **Streaming**: Use streaming responses for large payloads

### DEP:WASM
**Trigger:** wasm-pack, wasm-bindgen, wit-bindgen, wasmtime, wasmer, wazero

- **Init-Once**: Initialize WASM module once, reuse instance
- **Memory-Manage**: Explicit memory allocation/deallocation
- **Type-Boundary**: Clear types at JS/WASM boundary
- **Error-Propagate**: Handle panics gracefully (Rust: catch_unwind)
- **Size-Optimize**: Use wasm-opt, enable LTO
- **Async-Bridge**: Use async for long operations to avoid blocking

### DEP:EdgeFramework
**Trigger:** hono, elysia, h3, nitro, itty-router

- **Middleware-Light**: Minimal middleware chain
- **Context-Pass**: Pass context through handlers, not globals
- **Route-Tree**: Efficient route matching (radix tree)
- **Type-Safe-Routes**: End-to-end type safety (Elysia Eden, Hono RPC)
- **Multi-Runtime**: Test on target runtime (Bun, Deno, CF Workers)

### DEP:Config
**Trigger:** pydantic-settings, python-dotenv, dynaconf, configparser, toml, omegaconf, hydra

- **Env-Override**: Environment variables override config files
- **Secrets-Separate**: Secrets in env vars or vault, not config
- **Type-Coerce**: String to int/bool/list coercion
- **Validation-Early**: Validate on load, fail fast
- **Defaults-Document**: Document all defaults
- **Reload-Support**: Hot reload for long-running apps

### DEP:Testing
**Trigger:** pytest, unittest, nose2, hypothesis, ward, robot, behave, lettuce

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
**Trigger:** cuda-python, cupy, torch+cuda, tensorflow-gpu, numba, pycuda, triton, jax

- **Device-Selection**: Explicit CUDA_VISIBLE_DEVICES
- **Memory-Management**: Clear cache, use context managers
- **Batch-Sizing**: Dynamic batch based on VRAM
- **Mixed-Precision**: FP16/BF16 where applicable
- **Fallback-CPU**: Graceful CPU fallback
- **Stream-Async**: CUDA streams for parallelism

### DEP:Audio
**Trigger:** faster-whisper, whisper, pydub, librosa, soundfile, pyaudio, speechrecognition, pedalboard

- **Chunk-Processing**: Stream in chunks, don't load all
- **Sample-Rate**: Normalize sample rates
- **Format-Agnostic**: Support wav, mp3, m4a, etc.
- **Memory-Stream**: Use file handles, not full load
- **Silence-Detection**: VAD before heavy processing
- **Progress-Callback**: Report progress for long operations

### DEP:Video
**Trigger:** ffmpeg-python, moviepy, opencv-video, decord, av, imageio-ffmpeg

- **Frame-Iterator**: Yield frames, don't load all
- **Codec-Fallback**: Multiple codec support
- **Resolution-Aware**: Scale before heavy processing
- **Temp-Cleanup**: Auto-cleanup intermediate files
- **Seek-Efficient**: Keyframe seeking for random access
- **Hardware-Accel**: NVENC/VAAPI when available

### DEP:HeavyModel
**Trigger:** transformers, sentence-transformers, langchain, llama-cpp-python, vllm, ollama, openai, anthropic

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
**Trigger:** opencv-python, pillow, scikit-image, imageio, albumentations, kornia

- **Lazy-Decode**: Decode on access
- **Size-Validate**: Max dimensions check
- **Format-Preserve**: Maintain original format/quality
- **EXIF-Handle**: Rotation, metadata handling
- **Memory-Map**: mmap for huge files

### DEP:DataHeavy
**Trigger:** pandas, polars, dask, pyspark, ray, vaex, modin, arrow

- **Chunk-Read**: chunksize parameter for large files
- **Lazy-Eval**: Defer until needed (polars/dask)
- **Type-Optimize**: Downcast dtypes
- **Index-Usage**: Set appropriate indexes
- **Parallel-Process**: Use available cores
- **Spill-Disk**: Allow disk spillover

### DEP:GamePython
**Trigger:** pygame, arcade, ursina, panda3d, pyglet, raylib

- **Game-Loop**: Fixed timestep, variable render
- **Asset-Preload**: Load screens, progress bars
- **Input-Mapping**: Configurable keybindings
- **State-Machine**: Clean state transitions
- **Delta-Time**: Frame-independent movement

### DEP:GameJS
**Trigger:** phaser, three.js, pixi.js, babylon.js, kaboom, excalibur

- **Sprite-Atlas**: Texture packing
- **Object-Pool**: Reuse frequently created objects
- **RAF-Loop**: requestAnimationFrame
- **WebGL-Fallback**: Canvas 2D fallback
- **Audio-Context**: Single AudioContext

### DEP:GameEngine
**Trigger:** Unity (.csproj), Unreal (*.uproject), Godot (project.godot)

- **Scene-Organization**: Clear hierarchy, naming convention
- **Prefab-Reuse**: Prefabs/scenes over copies
- **Build-Profiles**: Platform-specific settings
- **Asset-LFS**: Git LFS for binary assets
- **Input-System**: Input actions, rebindable keys
- **Platform-Optimize**: Quality presets per platform

### DEP:HTTP
**Trigger:** requests, httpx, aiohttp, axios, got, ky, node-fetch

- **Timeout-Always**: Explicit timeouts
- **Retry-Transient**: Exponential backoff
- **Session-Reuse**: Connection pooling
- **Error-Handle**: Status code handling
- **Response-Validate**: Schema validation

### DEP:ORM
**Trigger:** sqlalchemy, prisma, drizzle, typeorm, sequelize, tortoise-orm, peewee

- **N+1-Prevent**: Eager load or batch queries
- **Query-Optimize**: EXPLAIN analysis
- **Loading-Strategy**: Explicit eager/lazy per use case
- **Transaction-Boundary**: Clear scope, rollback on error
- **Index-Design**: Indexes for WHERE/JOIN columns
- **Bulk-Operations**: Use bulk insert/update APIs

### DEP:Auth
**Trigger:** authlib, python-jose, passlib, bcrypt, next-auth, clerk, auth0, supabase-auth

- **Token-Secure**: HttpOnly, Secure flags
- **Refresh-Flow**: Refresh token rotation
- **RBAC-Clear**: Role-based permissions
- **Session-Invalidate**: Clear all sessions option
- **MFA-Support**: Optional 2FA for sensitive ops

### DEP:Payment
**Trigger:** stripe, paypal, square, braintree, paddle, lemon-squeezy

- **Webhook-Verify**: Signature validation
- **Idempotency-Key**: Prevent duplicate charges
- **Amount-Server**: Server-side price calculation
- **Payment-Error-Handle**: User-friendly payment errors
- **Audit-Trail**: Complete payment logs

### DEP:Email
**Trigger:** sendgrid, mailgun, resend, nodemailer, postmark, ses

- **Template-System**: Reusable templates
- **Queue-Async**: Background sending
- **Bounce-Handle**: Process bounces/complaints
- **Rate-Aware**: Respect provider limits
- **Unsubscribe**: One-click unsubscribe

### DEP:SMS
**Trigger:** twilio, vonage, messagebird, plivo

- **Delivery-Status**: Track delivery callbacks
- **Rate-Throttle**: Respect carrier limits
- **Opt-Out**: Honor STOP requests
- **Fallback-Provider**: Secondary provider
- **Message-Template**: Pre-approved templates

### DEP:Notification
**Trigger:** firebase-admin, onesignal, pusher, novu

- **Channel-Preference**: User-configurable channels
- **Batch-Send**: Batch API calls
- **Silent-Push**: Background updates
- **Token-Refresh**: Handle token rotation
- **Fallback-Channel**: Email if push fails

### DEP:Search
**Trigger:** elasticsearch, meilisearch, algolia, typesense, opensearch

- **Index-Strategy**: Separate vs combined indexes
- **Sync-Mechanism**: Real-time vs batch sync
- **Relevance-Tune**: Custom ranking
- **Typo-Tolerance**: Fuzzy matching
- **Facet-Design**: Efficient faceting

### DEP:Queue
**Trigger:** celery, rq, dramatiq, huey, bull, bee-queue, bullmq

- **Idempotent-Tasks**: Same input = same result
- **Result-Backend**: Configure result storage
- **Timeout-Task**: Per-task time limits
- **Dead-Letter**: DLQ for inspection
- **Priority-Queues**: Separate by priority

### DEP:Cache
**Trigger:** redis, memcached, aiocache, diskcache, keyv, ioredis

- **TTL-Strategy**: Explicit expiration
- **Key-Namespace**: Prefixed keys
- **Serialization**: Consistent serializer
- **Cache-Aside**: Load on miss pattern
- **Invalidation**: Clear related keys

### DEP:Logging
**Trigger:** loguru, structlog, winston, pino, bunyan

- **Structured-Format**: JSON logging in production
- **Level-Config**: Configurable log level
- **Context-Inject**: Request ID, user ID
- **Sensitive-Redact**: Mask PII
- **Rotation-Strategy**: Size/time rotation

### DEP:ObjectStore
**Trigger:** boto3/s3, minio, cloudinary, uploadthing, google-cloud-storage

- **Presigned-URLs**: Time-limited URLs
- **Content-Type**: Validate MIME type
- **Size-Limit**: Max file size
- **Path-Structure**: Organized paths
- **Lifecycle-Rules**: Auto-expiry for temp files

### DEP:PDF
**Trigger:** reportlab, weasyprint, pdfkit, puppeteer, playwright, fpdf2

- **Template-Based**: HTML/template generation
- **Async-Generate**: Background processing
- **Stream-Output**: Stream don't buffer
- **Font-Embed**: Embed for consistency
- **Accessibility**: Tagged PDF when possible

### DEP:Excel
**Trigger:** openpyxl, xlsxwriter, pandas-excel, exceljs, sheetjs

- **Stream-Write**: Write in chunks
- **Formula-Safe**: Escape formula injection
- **Style-Template**: Reusable styles
- **Memory-Optimize**: Write-only mode
- **Sheet-Naming**: Valid sheet names

### DEP:Scraping
**Trigger:** scrapy, beautifulsoup4, selenium, playwright, puppeteer, crawlee

- **Politeness-Delay**: Respectful delays
- **Robots-Respect**: Honor robots.txt
- **User-Agent-Honest**: Identify your bot
- **Selector-Resilient**: Handle structure changes
- **Headless-Default**: Headless unless debugging
- **Anti-Block**: Rotate IPs/proxies if needed

### DEP:Blockchain
**Trigger:** web3, ethers, hardhat, brownie, ape, solana-py

- **Gas-Estimate**: Pre-estimate gas
- **Nonce-Manage**: Track nonce locally
- **Event-Listen**: Indexed event handling
- **Testnet-First**: Test before mainnet
- **Key-Security**: Never in code/logs

### DEP:ARVR
**Trigger:** openxr, webxr, ar-foundation, arvr-toolkit

- **XR-Frame-Budget**: 90fps minimum
- **Comfort-Settings**: Teleport/snap turn options
- **Fallback-Mode**: Non-XR fallback
- **Input-Abstract**: Abstract input layer
- **Performance-Tier**: Quality presets per device

### DEP:IoT
**Trigger:** micropython, paho-mqtt, esphome, homeassistant, aiocoap

- **IoT-Reconnect**: Auto-reconnect
- **Power-Aware**: Sleep modes for battery
- **OTA-Update**: Remote updates
- **Data-Buffer**: Local buffer for unreliable network
- **Watchdog**: Hardware watchdog

### DEP:Crypto
**Trigger:** cryptography, pycryptodome, nacl, jose, argon2

- **Algorithm-Modern**: AES-256-GCM, ChaCha20
- **Key-Rotation**: Scheduled rotation
- **IV-Unique**: Never reuse IV/nonce
- **Timing-Safe**: Constant-time compare
- **Key-Derivation**: Argon2/scrypt, not MD5/SHA1

---

## Trigger Reference

| Symbol | Meaning | Detection Source | Output |
|--------|---------|------------------|--------|
| L: | Language | Manifest, lock files, code | `{lang}.md` |
| R: | Runtime | Lock file type, config | `bun.md`, `deno.md` |
| T: | App Type | Entry points, exports | `cli.md`, `library.md`, `service.md` |
| API: | API Style | Routes, decorators, proto | `api.md` |
| DB: | Database | ORM deps, migrations | `database.md` |
| Frontend: | Frontend | Framework deps, components | `frontend.md` |
| Mobile: | Mobile | SDK deps, native configs | `mobile.md` |
| Desktop: | Desktop | Electron/Tauri deps | `desktop.md` |
| Infra: | Infrastructure | Dockerfile, *.tf, k8s/ | `container.md`, `k8s.md`, `edge.md` |
| ML: | Machine Learning | ML framework deps | `ml.md` |
| Build: | Build Tools | Bundler, monorepo configs | `monorepo.md`, `bundler.md` |
| Test: | Testing | Test framework, tests/ | `testing.md` |
| CI: | CI/CD | Workflow files | `ci-cd.md` |
| DEP: | Dependency | Specific package deps | `dep-{category}.md` |
