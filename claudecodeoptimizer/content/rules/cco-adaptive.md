# Adaptive Rules
*Selected by /cco-config based on detection. Each rule evaluated individually.*
*Used as template pool for generating .claude/rules/ files with path-specific frontmatter.*

## Detection System

### Auto-Detect (Manifest/Code Scan)

| Category | Trigger Files | Output |
|----------|--------------|--------|
| L:Python | pyproject.toml, setup.py, requirements.txt, *.py | `python.md` |
| L:TypeScript | tsconfig.json, *.ts/*.tsx | `typescript.md` |
| L:JavaScript | package.json (no TS), *.js/*.jsx | `javascript.md` |
| L:Go | go.mod, *.go | `go.md` |
| L:Rust | Cargo.toml, *.rs | `rust.md` |
| T:CLI | __main__.py, bin/, cli/, "bin" in package.json | `cli.md` |
| T:Library | exports in package.json, __init__.py with __all__ | `library.md` |
| API:REST | routes/, @Get/@Post decorators, express.Router | `api.md` |
| API:GraphQL | graphql deps, schema.graphql, resolvers/ | `api.md` |
| API:gRPC | *.proto files, grpc deps | `api.md` |
| DB:* | ORM deps, migrations/, prisma/schema.prisma | `database.md` |
| Frontend | react/vue/angular/svelte in deps | `frontend.md` |
| Mobile | Podfile, build.gradle, pubspec.yaml | `mobile.md` |
| Desktop | electron/tauri in deps | `desktop.md` |
| Container | Dockerfile (not in examples/test/) | `container.md` |
| K8s | k8s/, helm/, kustomization.yaml | `k8s.md` |
| Serverless | serverless.yml, sam.yaml, vercel.json, netlify.toml | `serverless.md` |
| Monorepo | nx.json, turbo.json, lerna.json, pnpm-workspace.yaml | `monorepo.md` |
| ML/AI | torch/tensorflow/sklearn/transformers/langchain | `ml.md` |
| Game | Unity (.csproj), Unreal (*.uproject), Godot (project.godot) | `game.md` |
| i18n | locales/, i18n/, messages/, translations/ | `i18n.md` |
| RT:* | websocket/socket.io/sse deps | `realtime.md` |
| DEP:* | See Dependency Categories below | `{dep}.md` |

### User-Input (AskUserQuestion)

| Element | Options | Default | Affects |
|---------|---------|---------|---------|
| Team | Solo; 2-5; 6+ | Solo | Team rules |
| Scale | Prototype (<100); Small (100+); Medium (1K+); Large (10K+) | Small | Scale rules |
| Data | Public; PII; Regulated | Public | Security rules |
| Compliance | None; SOC2; HIPAA; PCI; GDPR; CCPA; ISO27001; FedRAMP; DORA; HITRUST | None | Compliance rules |
| Testing | Basics (60%); Standard (80%); Full (90%) | Standard | Testing rules |
| SLA | None; 99%; 99.9%; 99.99% | None | Observability rules |
| Maturity | Prototype; Active; Stable; Legacy | Active | Guidelines |
| Breaking | Allowed; Minimize; Never | Minimize | Guidelines |
| Priority | Speed; Balanced; Quality; Security | Balanced | Guidelines |

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

- **Python-Type-Hints**: Type annotations for public APIs (functions, methods, classes)
- **Docstrings**: Google-style docstrings for public functions/classes
- **Import-Order**: stdlib > third-party > local (isort compatible)
- **Exception-Context**: Use `raise X from Y` for exception chaining

### TypeScript (L:TypeScript)
**Trigger:** tsconfig.json | *.ts/*.tsx

- **Strict-Mode**: Enable strict in tsconfig.json
- **Explicit-Return**: Return types on public functions
- **No-Any**: Avoid any, use unknown for truly unknown types
- **Null-Safety**: Strict null checks enabled

### JavaScript (L:JavaScript)
**Trigger:** package.json without TS | *.js/*.jsx only

- **JSDoc-Types**: Type hints via JSDoc for public APIs
- **ES-Modules**: ESM over CommonJS (import/export)
- **Const-Default**: const > let > var preference

### Go (L:Go)
**Trigger:** go.mod | *.go

- **Error-Wrap**: Wrap errors with context (fmt.Errorf %w)
- **Interface-Small**: Small, focused interfaces (1-3 methods)
- **Goroutine-Safe**: Channel or sync primitives for concurrency
- **Defer-Cleanup**: defer for cleanup operations

### Rust (L:Rust)
**Trigger:** Cargo.toml | *.rs

- **Result-Propagate**: Use ? operator for error propagation
- **Ownership-Clear**: Clear ownership patterns, minimize clones
- **Clippy-Clean**: No clippy warnings in CI
- **Unsafe-Minimize**: Minimize unsafe blocks, document when necessary

---

## Security Rules
**Trigger:** D:PII | D:Regulated | Scale:Large | Compliance:*

- **Input-Validation**: Validate at system entry points (Pydantic/Zod/JSON Schema)
- **SQL-Safe**: Parameterized queries only, no string concatenation
- **XSS-Prevent**: Sanitize output + CSP headers
- **Auth-Verify**: Verify authentication on every request
- **Rate-Limit**: Per-user/IP limits on public endpoints
- **Encrypt-Rest**: AES-256 for PII/sensitive data at rest
- **Audit-Log**: Immutable logging for security-critical actions
- **CORS-Strict**: Explicit origins, no wildcard in production
- **License-Track**: Review GPL/AGPL deps before adding

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

### Full (Testing:90%)
- **E2E**: End-to-end tests for critical user flows
- **Contract**: Consumer-driven contract testing
- **Mutation**: Mutation testing for test effectiveness
- **Coverage-90**: Minimum 90% line coverage

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
**Trigger:** React/Vue/Angular/Svelte detected

- **A11y-WCAG**: WCAG 2.2 AA, keyboard navigation
- **Perf-Core-Vitals**: LCP<2.5s, INP<200ms, CLS<0.1
- **State-Predictable**: Single source of truth for state
- **Code-Split**: Lazy load routes and heavy components

---

## Specialized > ML/AI
**Trigger:** torch/tensorflow/sklearn/transformers/langchain detected

- **Reproducibility**: Seed everything, pin versions
- **Experiment-Track**: MLflow/W&B for experiments
- **Model-Registry**: Versioned model artifacts
- **Bias-Detection**: Fairness metrics for user-facing AI

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

| Symbol | Meaning | Detection Source |
|--------|---------|------------------|
| L: | Language | Manifest files, code files |
| T: | App Type | Entry points, exports |
| API: | API Style | Routes, decorators, proto |
| DB: | Database | ORM deps, migrations |
| DEP: | Dependency | Dependencies in manifests |
| D: | Data Class | Auth patterns, encryption |
| S: | Scale | HPA, replicas, user input |
| A: | Architecture | Service count, structure |
| C: | Compliance | User input |
| RT: | Real-time | WebSocket/SSE deps |
