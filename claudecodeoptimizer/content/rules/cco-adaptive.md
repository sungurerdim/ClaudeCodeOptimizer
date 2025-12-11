# Adaptive Rules
*Selected by /cco-tune based on detection. Each rule evaluated individually.*
*Used as template pool for generating .claude/rules/ files with path-specific frontmatter.*

## Path Pattern Templates

When cco-tune generates project-level rules, it creates separate files with YAML frontmatter:

| Category | Output File | Paths Pattern | Trigger |
|----------|-------------|---------------|---------|
| **Language (ALWAYS evaluate)** ||||
| L:Python | `python.md` | `**/*.py` | pyproject.toml, setup.py, requirements.txt |
| L:TypeScript | `typescript.md` | `**/*.{ts,tsx}` | tsconfig.json |
| L:JavaScript | `javascript.md` | `**/*.{js,jsx}` | package.json (no TS) |
| L:Go | `go.md` | `**/*.go` | go.mod |
| L:Rust | `rust.md` | `**/*.rs` | Cargo.toml |
| **Application Type** ||||
| T:CLI | `cli.md` | `**/__main__.py, **/cli/**/*` | __main__.py, bin/, cli/ |
| T:Library | `library.md` | `**/src/**/*` | exports in package.json, __init__.py |
| **Scale (ALWAYS evaluate)** ||||
| S:Small+ | `scale.md` | `**/*` | Default for non-prototype |
| **Infrastructure** ||||
| API:REST | `api.md` | `**/routes/**/*`, `**/api/**/*` | routes/, @Get/@Post decorators |
| CI/CD | `operations.md` | `.github/**/*` | .github/workflows/ |
| Testing | `testing.md` | `tests/**/*`, `**/*.test.*` | pytest/jest/vitest config |
| Frontend | `frontend.md` | `**/components/**/*`, `**/pages/**/*` | react/vue/angular in deps |
| DB:* | `database.md` | `**/models/**/*`, `**/migrations/**/*` | ORM deps, migrations/ |
| **DEP: Compute & Processing** ||||
| DEP:GPU | `gpu.md` | `**/*` | cuda-python, cupy, torch+cuda |
| DEP:Audio | `audio.md` | `**/*` | faster-whisper, pydub, librosa |
| DEP:Video | `video.md` | `**/*` | ffmpeg-python, moviepy |
| DEP:Image | `image.md` | `**/*` | opencv-python, pillow |
| DEP:HeavyModel | `heavy-model.md` | `**/*` | transformers, langchain |
| DEP:DataHeavy | `data-heavy.md` | `**/*` | pandas, polars, dask |
| **DEP: Game Development** ||||
| DEP:GamePython | `game-python.md` | `**/*` | pygame, arcade, ursina |
| DEP:GameJS | `game-js.md` | `**/*` | phaser, three.js, pixi.js |
| DEP:GameEngine | `game-engine.md` | `**/*` | Unity, Unreal, Godot |
| **DEP: Web & API** ||||
| DEP:HTTP | `http-client.md` | `**/*` | requests, httpx, axios |
| DEP:ORM | `orm.md` | `**/*` | sqlalchemy, prisma, typeorm |
| DEP:Auth | `auth.md` | `**/*` | next-auth, clerk, auth0 |
| DEP:Payment | `payment.md` | `**/*` | stripe, paypal, paddle |
| **DEP: Communication** ||||
| DEP:Email | `email.md` | `**/*` | sendgrid, resend, nodemailer |
| DEP:SMS | `sms.md` | `**/*` | twilio, vonage |
| DEP:Notification | `notification.md` | `**/*` | firebase-admin, onesignal |
| DEP:Search | `search.md` | `**/*` | elasticsearch, meilisearch |
| **DEP: Infrastructure** ||||
| DEP:Queue | `queue.md` | `**/*` | celery, bull, dramatiq |
| DEP:Cache | `cache.md` | `**/*` | redis, memcached |
| DEP:Logging | `logging.md` | `**/*` | loguru, winston, pino |
| DEP:ObjectStore | `object-store.md` | `**/*` | boto3, minio, cloudinary |
| **DEP: Documents** ||||
| DEP:PDF | `pdf.md` | `**/*` | reportlab, weasyprint |
| DEP:Excel | `excel.md` | `**/*` | openpyxl, exceljs |
| **DEP: Emerging Tech** ||||
| DEP:Blockchain | `blockchain.md` | `**/*` | web3, ethers, hardhat |
| DEP:ARVR | `arvr.md` | `**/*` | openxr, webxr |
| DEP:IoT | `iot.md` | `**/*` | micropython, paho-mqtt |
| **DEP: Security** ||||
| DEP:Crypto | `crypto.md` | `**/*` | cryptography, pycryptodome |
| DEP:Scraping | `scraping.md` | `**/*` | scrapy, selenium, playwright |

**Generated file format:**
```markdown
---
paths: **/*.py
---
# Python Rules

| Rule | Description |
|------|-------------|
| * Type-Hints | Type annotations for public APIs |
```

## Trigger Reference

| Symbol | Meaning | Detection Source |
|--------|---------|------------------|
| L: | Language/Stack | package.json, pyproject.toml, go.mod, Cargo.toml |
| DEP: | Dependency category | Dependencies in manifest files |
| D: | Data classification | Auth patterns, encryption usage |
| S: | Scale (users/RPS) | Replicas, HPA, load balancer config |
| T: | Application type | Entry points, exports analysis |
| A: | Architecture | Service count, Dockerfile patterns |
| C: | Compliance | SECURITY.md, audit logs, keywords |
| DB: | Database | ORM deps, migrations/, prisma/schema |
| API: | API style | Routes, decorators, proto files |
| RT: | Real-time | WebSocket/SSE deps |

---

## Dependency-Based Detection [CRITICAL]

**ALWAYS scan project dependencies** from manifest files and trigger matching categories.

### Dependency Sources by Language

| Language | Manifest Files | Parse Method |
|----------|---------------|--------------|
| Python | pyproject.toml, requirements.txt, setup.py, Pipfile | TOML/text parse |
| Node | package.json | JSON parse dependencies + devDependencies |
| Go | go.mod | require block |
| Rust | Cargo.toml | [dependencies] section |

### Dependency Categories

| Category | Trigger Dependencies | Output File |
|----------|---------------------|-------------|
| **Compute & Processing** |||
| DEP:GPU | cuda-python, cupy, torch+cuda, tensorflow-gpu, numba, pycuda, triton, jax | `gpu.md` |
| DEP:Audio | faster-whisper, openai-whisper, pydub, librosa, soundfile, pyaudio, speechrecognition, pedalboard | `audio.md` |
| DEP:Video | ffmpeg-python, moviepy, opencv (VideoCapture), decord, av, imageio-ffmpeg | `video.md` |
| DEP:Image | opencv-python, pillow, scikit-image, imageio, albumentations, kornia | `image.md` |
| DEP:HeavyModel | transformers, sentence-transformers, langchain, llama-cpp-python, vllm, ollama, openai, anthropic | `heavy-model.md` |
| DEP:DataHeavy | pandas, polars, dask, pyspark, ray, vaex, modin, arrow | `data-heavy.md` |
| **Game Development** |||
| DEP:GamePython | pygame, arcade, ursina, panda3d, pyglet, raylib | `game-python.md` |
| DEP:GameJS | phaser, three.js, pixi.js, babylon.js, kaboom, excalibur | `game-js.md` |
| DEP:GameEngine | Unity (detected via .csproj), Unreal (*.uproject), Godot (project.godot) | `game-engine.md` |
| **Web & API** |||
| DEP:HTTP | requests, httpx, aiohttp, axios, got, ky, node-fetch | `http-client.md` |
| DEP:ORM | sqlalchemy, prisma, drizzle, typeorm, sequelize, tortoise-orm, peewee | `orm.md` |
| DEP:Auth | authlib, python-jose, passlib, bcrypt, next-auth, clerk, auth0, supabase-auth | `auth.md` |
| DEP:Payment | stripe, paypal, square, braintree, paddle, lemon-squeezy | `payment.md` |
| **Communication** |||
| DEP:Email | sendgrid, mailgun, resend, nodemailer, postmark, ses | `email.md` |
| DEP:SMS | twilio, vonage, messagebird, plivo | `sms.md` |
| DEP:Notification | firebase-admin, onesignal, pusher, novu | `notification.md` |
| **Search & Storage** |||
| DEP:Search | elasticsearch, meilisearch, algolia, typesense, opensearch | `search.md` |
| DEP:ObjectStore | boto3/s3, minio, cloudinary, uploadthing, google-cloud-storage | `object-store.md` |
| **Infrastructure** |||
| DEP:Queue | celery, rq, dramatiq, huey, bull, bee-queue, bullmq | `queue.md` |
| DEP:Cache | redis, memcached, aiocache, diskcache, keyv, ioredis | `cache.md` |
| DEP:Logging | loguru, structlog, winston, pino, bunyan | `logging.md` |
| **Documents & Output** |||
| DEP:PDF | reportlab, weasyprint, pdfkit, puppeteer (pdf), playwright (pdf), fpdf2 | `pdf.md` |
| DEP:Excel | openpyxl, xlsxwriter, pandas (excel), exceljs, sheetjs | `excel.md` |
| **Emerging Tech** |||
| DEP:Blockchain | web3, ethers, hardhat, brownie, ape, solana-py | `blockchain.md` |
| DEP:ARVR | openxr, arvr-toolkit, ar-foundation, webxr | `arvr.md` |
| DEP:IoT | micropython, esphome, homeassistant, paho-mqtt, aiocoap | `iot.md` |
| **Security** |||
| DEP:Crypto | cryptography, pycryptodome, nacl, jose, argon2 | `crypto.md` |
| DEP:Scraping | scrapy, beautifulsoup4, selenium, playwright, puppeteer, crawlee | `scraping.md` |

---

## Language-Specific Rules
**Trigger:** Stack detection (pyproject.toml, package.json, go.mod, Cargo.toml)

### Python (L:Python)
**Trigger:** pyproject.toml | setup.py | requirements.txt | *.py files
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Type-Hints | Public APIs | Type annotations for functions, methods, classes |
| * Docstrings | Public functions/classes | Google-style docstrings |
| * Import-Order | Always | stdlib > third-party > local (isort) |
| * Exception-Context | Exception handling | Use `raise X from Y` for chaining |

### TypeScript (L:TypeScript)
**Trigger:** tsconfig.json | *.ts/*.tsx files
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Strict-Mode | Always | Enable strict in tsconfig |
| * Explicit-Return | Public APIs | Return types on public functions |
| * No-Any | Always | Avoid any, use unknown |
| * Null-Safety | Always | Strict null checks |

### JavaScript (L:JavaScript)
**Trigger:** package.json without TS | *.js/*.jsx files only
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * JSDoc-Types | Public APIs | Type hints via JSDoc |
| * ES-Modules | Always | ESM over CommonJS |
| * Const-Default | Always | const > let > var |

### Go (L:Go)
**Trigger:** go.mod | *.go files
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Error-Wrap | Error handling | Wrap with context |
| * Interface-Small | Always | Small, focused interfaces |
| * Goroutine-Safe | Concurrency | Channel or sync primitives |
| * Defer-Cleanup | Resource handling | defer for cleanup |

### Rust (L:Rust)
**Trigger:** Cargo.toml | *.rs files
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Result-Propagate | Error handling | Use ? operator |
| * Ownership-Clear | Always | Clear ownership patterns |
| * Clippy-Clean | Always | No clippy warnings |
| * Unsafe-Minimize | Always | Minimize unsafe blocks |

## Granular Selection [CRITICAL]

Each rule has an **Applicability Check**. Only include rules where check passes.

**Format in context:**
```markdown
### {Category} - {Trigger reason}
| Rule | Description |
|------|-------------|
| * {Name} | {Concise description} |
```

---

## Security
**Trigger:** D:PII | D:Regulated | C:*

| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Input-Validation | Has user input entry points | Validate at boundaries |
| * SQL-Safe | Has DB queries | Parameterized only |
| * XSS-Prevent | Outputs HTML/web | Sanitize + CSP |
| * Auth-Verify | Has auth system | Verify every request |
| * Rate-Limit | Has public endpoints | Per-user/IP limits |
| * Encrypt-Rest | Stores sensitive data | AES-256 for PII |
| * Audit-Log | Security-critical actions | Immutable logging |
| * CORS-Strict | Web server with API | Explicit origins |
| * License-Track | Has dependencies | Review GPL/AGPL |

---

## Scale

**Inheritance:** Higher tiers include all lower tier rules.

### Small (S:100+)
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Caching | Has data fetching | TTL + invalidation |
| * Lazy-Load | Has non-critical resources | Defer loading |

### Medium (S:1K+)
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Conn-Pool | Has DB/external connections | Reuse + sizing |
| * Async-IO | Has I/O operations | Non-blocking |

### Large (S:10K+ | A:Microservices)
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Circuit-Breaker | Calls external services | Fail-fast pattern |
| * Idempotency | Has write operations | Safe retries |
| * API-Version | Has public API | Version in URL/header |
| * Compression | Large responses | gzip/brotli |

---

## Backend > API
**Trigger:** API:REST | API:GraphQL | API:gRPC

| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * REST-Methods | REST API | Proper verbs + status |
| * Pagination | List endpoints exist | Cursor-based |
| * OpenAPI-Spec | REST API | Synced with examples |
| * Error-Format | Any API | Consistent, no stack trace |

### GraphQL Extension
**Trigger:** API:GraphQL
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * GQL-Limits | Always | Depth + complexity limits |
| * GQL-Persisted | Production | Persisted queries |

### gRPC Extension
**Trigger:** API:gRPC
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Proto-Version | Always | Backward compatible |

---

## Backend > Data
**Trigger:** DB:*
**Note:** For ORM-specific rules (queries, relationships), see DEP:ORM section.

| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Backup-Strategy | Has database | Automated + tested restore |
| * Schema-Versioned | Has schema | Migration files + rollback plan |
| * Connection-Secure | Production DB | SSL/TLS, credentials in env |
| * Query-Timeout | All queries | Prevent runaway queries |

---

## Backend > Operations
**Trigger:** CI/CD detected

### Full Operations (T:API | T:Frontend | A:Microservices)
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Config-as-Code | Always | Versioned, env-aware |
| * Health-Endpoints | Has server | /health + /ready |
| * Graceful-Shutdown | Long-running process | Drain on SIGTERM |
| * Observability | Production deployment | Metrics + logs + traces |
| * CI-Gates | Always | lint + test + coverage |
| * Zero-Downtime | Has deployment | Blue-green or canary |
| * Feature-Flags | Needs deploy/release separation | Decouple deploy |

### CI-Only Operations (T:CLI | T:Library)
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Config-as-Code | Always | Versioned config |
| * CI-Gates | Always | lint + test + coverage |

---

## Apps > CLI
**Trigger:** T:CLI

| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Help-Examples | Has commands | --help with usage |
| * Exit-Codes | Always | 0=success, N=specific |
| * Signal-Handle | Long-running commands | SIGINT/SIGTERM graceful |
| * Output-Modes | User-facing | Human + --json |
| * Config-Precedence | Has config | env > file > args |

---

## Apps > Library
**Trigger:** T:Library

| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Minimal-Deps | Always | Reduce transitive |
| * Tree-Shakeable | JS/TS library | ESM, no side effects |
| * Types-Included | Always | TS or JSDoc |
| * Deprecation-Path | Has public API | Warn before remove |

---

## Apps > Mobile
**Trigger:** iOS/Android/RN/Flutter detected

| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Offline-First | Has data sync | Local-first + sync |
| * Battery-Optimize | Background work | Minimize wake locks |
| * Deep-Links | Has navigation | Universal/app links |
| * Platform-Guidelines | Always | iOS HIG / Material |

---

## Apps > Desktop
**Trigger:** Electron/Tauri detected

| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Auto-Update | Distributed app | Silent + manual option |
| * Native-Integration | Always | System tray, notifications |
| * Memory-Cleanup | Long-running | Prevent leaks |

---

## Infrastructure > Container
**Trigger:** Dockerfile detected (not in examples/test/benchmarks)

| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Multi-Stage | Always | Separate build/runtime |
| * Non-Root | Always | Least privilege |
| * CVE-Scan | Always | Automated in CI |
| * Resource-Limits | Always | CPU/memory bounds |
| * Distroless | Production | Minimal attack surface |

---

## Infrastructure > K8s
**Trigger:** Kubernetes/Helm detected

| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Security-Context | Always | Non-root, read-only fs |
| * Network-Policy | Always | Explicit allow rules |
| * Probes | Always | liveness + readiness |
| * Resource-Quotas | Always | Namespace limits |

---

## Infrastructure > Serverless
**Trigger:** Lambda/Functions/Vercel/Netlify detected

| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Minimize-Bundle | Always | Reduce cold start |
| * Graceful-Timeout | Always | Clean shutdown |
| * Stateless | Always | No local state |
| * Right-Size | Always | Memory optimization |

---

## Infrastructure > Monorepo
**Trigger:** nx/turbo/lerna/pnpm-workspace detected

| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Package-Boundaries | Always | Clear ownership |
| * Selective-Test | Always | Affected only |
| * Shared-Deps | Always | Hoisted + versioned |
| * Build-Cache | Always | Remote cache |

---

## Frontend
**Trigger:** React/Vue/Angular/Svelte detected

| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * A11y-WCAG | Always | AA level, keyboard nav |
| * Perf-Core-Vitals | Always | LCP<2.5s, INP<200ms |
| * State-Predictable | Has state management | Single source |
| * Code-Split | Multiple routes | Lazy load routes |

---

## Specialized > ML/AI
**Trigger:** torch/tf/sklearn/langchain detected

| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Reproducibility | Has training | Seed + version pin |
| * Experiment-Track | Has training | MLflow/W&B |
| * Model-Registry | Has models | Versioned artifacts |
| * Bias-Detection | User-facing AI | Fairness metrics |

---

## Specialized > Game
**Trigger:** Unity/Unreal/Godot detected
**Note:** For engine-specific rules, see DEP:GameEngine. For Python/JS game libs, see DEP:GamePython/DEP:GameJS.

| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Frame-Budget | Always | 16ms (60fps) or 8ms (120fps) target |
| * Asset-LOD | Large assets | Level of detail + streaming |
| * Save-Versioned | Has saves | Migration support for old saves |
| * Determinism | Multiplayer/replay | Fixed timestep, no floats in logic |

---

## Team

**Inheritance:** Larger teams include smaller team rules.

### Small (Team:2-5)
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * PR-Review | Always | Async review |
| * README-Contributing | Always | Clear guidelines |

### Large (Team:6+)
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * ADR | Always | Architecture decisions |
| * CODEOWNERS | Always | Clear ownership |
| * PR-Templates | Always | Standardized PRs |
| * Branch-Protection | Always | Enforce reviews |

---

## i18n
**Trigger:** locales/i18n/translations detected

| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Strings-External | Always | No hardcoded text |
| * UTF8-Encoding | Always | Consistent encoding |
| * RTL-Support | Multi-language | Bidirectional layout |
| * Locale-Format | Dates/numbers | Culture-aware |

---

## Real-time

**Inheritance:** Higher tiers include lower.

### Basic (RT:Basic)
**Trigger:** WebSocket/SSE detected
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Reconnect-Logic | Always | Auto-reconnect |
| * Heartbeat | Always | Connection health |
| * Stale-Data | Always | Handle disconnects |

### Low-Latency (RT:Low-latency)
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Binary-Protocol | Performance critical | Protobuf/msgpack |
| * Edge-Compute | Global users | Reduce latency |

---

## Testing

**Inheritance:** Higher tiers include lower.

### Basics
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Unit-Isolated | Always | Fast, deterministic |
| * Mocking | External deps | Isolate tests |
| * Coverage-60 | Always | >60% line coverage |

### Standard
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Integration | Component boundaries | Test interactions |
| * Fixtures | Reusable data | Maintainable setup |
| * Coverage-80 | Always | >80% line coverage |
| * CI-on-PR | Has CI | Tests on every PR |

### Full
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * E2E | User flows | Critical paths |
| * Contract | API consumers | Consumer-driven |
| * Mutation | High coverage | Test effectiveness |
| * Coverage-90 | Always | >90% line coverage |

---

## Observability

**Inheritance:** Higher SLA includes lower.

### Basics (SLA:Any)
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Error-Tracking | Always | Sentry or similar |
| * Critical-Alerts | Always | Immediate notify |

### Standard (SLA:99%+)
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Correlation-ID | Always | Request tracing across services |
| * RED-Metrics | Has API | Rate, Error, Duration dashboards |
| * Distributed-Trace | Multi-service | OpenTelemetry/Jaeger |

### HA (SLA:99.9%+)
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Redundancy | Always | No single point |
| * Auto-Failover | Always | Automatic recovery |
| * Runbooks | Always | Incident response |

### Critical (SLA:99.99%+)
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Multi-Region | Always | Geographic redundancy |
| * Chaos-Engineering | Always | Fault injection |
| * DR-Tested | Always | Disaster recovery |

---

## Dependency-Based Rules

### GPU (DEP:GPU)
**Trigger:** cuda-python, cupy, torch (cuda), tensorflow-gpu, numba, pycuda, triton
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Device-Selection | Multiple GPUs possible | Explicit CUDA_VISIBLE_DEVICES |
| * Memory-Management | Large tensors | Clear cache, use context managers |
| * Batch-Sizing | Training/inference | Dynamic batch based on VRAM |
| * Mixed-Precision | Performance critical | FP16/BF16 where applicable |
| * Fallback-CPU | Not all users have GPU | Graceful CPU fallback |
| * Stream-Async | Multiple operations | CUDA streams for parallelism |

### Audio (DEP:Audio)
**Trigger:** faster-whisper, whisper, pydub, librosa, soundfile, pyaudio
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Chunk-Processing | Long audio files | Stream in chunks, don't load all |
| * Sample-Rate | Multiple sources | Normalize sample rates |
| * Format-Agnostic | User uploads | Support common formats (wav, mp3, m4a) |
| * Memory-Stream | Large files | Use file handles, not full load |
| * Silence-Detection | Pre-processing | VAD before heavy processing |
| * Progress-Callback | Long operations | Report progress to user |

### Video (DEP:Video)
**Trigger:** ffmpeg-python, moviepy, opencv (video), decord, av
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Frame-Iterator | Large videos | Yield frames, don't load all |
| * Codec-Fallback | Various inputs | Multiple codec support |
| * Resolution-Aware | Processing | Scale before heavy ops |
| * Temp-Cleanup | Intermediate files | Auto-cleanup temp files |
| * Seek-Efficient | Random access | Use keyframe seeking |
| * Hardware-Accel | Supported GPUs | NVENC/VAAPI when available |

### Heavy Models (DEP:HeavyModel)
**Trigger:** transformers, sentence-transformers, langchain, llama-cpp, vllm
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Lazy-Model-Load | CLI/API startup | Load on first use, not import |
| * Model-Singleton | Multiple calls | Single instance, reuse |
| * Quantization-Aware | Memory constrained | Support INT8/INT4 variants |
| * Batch-Inference | Multiple inputs | Batch for throughput |
| * Timeout-Guard | Inference calls | Max time limits |
| * Memory-Cleanup | After heavy ops | Explicit garbage collection |
| * Download-Cache | Model files | Cache models locally |

### Image Processing (DEP:Image)
**Trigger:** opencv-python, pillow, scikit-image, albumentations
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Lazy-Decode | Multiple images | Decode on access |
| * Size-Validate | User uploads | Max dimensions check |
| * Format-Preserve | Editing | Maintain original format/quality |
| * EXIF-Handle | Photos | Rotation, metadata handling |
| * Memory-Map | Large images | mmap for huge files |

### Data Heavy (DEP:DataHeavy)
**Trigger:** pandas, polars, dask, pyspark, ray, vaex
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Chunk-Read | Large CSVs | chunksize parameter |
| * Lazy-Eval | Transformations | Defer until needed (polars/dask) |
| * Type-Optimize | Memory usage | Downcast dtypes |
| * Index-Usage | Lookups | Set appropriate indexes |
| * Parallel-Process | Multi-core | Use available cores |
| * Spill-Disk | Memory limits | Allow disk spillover |

### Web Scraping (DEP:Scraping)
**Trigger:** scrapy, beautifulsoup4, selenium, playwright, puppeteer
**Note:** For HTTP basics (retry, timeout, session), see DEP:HTTP. These are scraping-specific.
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Politeness-Delay | External sites | Respectful delays between requests |
| * Robots-Respect | Public sites | Check and honor robots.txt |
| * User-Agent-Honest | All requests | Identify your bot properly |
| * Selector-Resilient | HTML parsing | Handle structure changes gracefully |
| * Headless-Default | Browser automation | Headless unless debugging |
| * Anti-Block | Production | Rotate IPs/proxies if needed |

### Queue/Workers (DEP:Queue)
**Trigger:** celery, rq, dramatiq, huey, bull
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Idempotent-Tasks | Retries possible | Same input = same result |
| * Result-Backend | Need results | Configure result storage |
| * Timeout-Task | Long tasks | Per-task time limits |
| * Dead-Letter | Failed tasks | DLQ for inspection |
| * Priority-Queues | Mixed workloads | Separate by priority |

### Cache (DEP:Cache)
**Trigger:** redis, memcached, aiocache, diskcache
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * TTL-Strategy | All cached data | Explicit expiration |
| * Key-Namespace | Multiple apps | Prefixed keys |
| * Serialization | Complex objects | Consistent serializer |
| * Cache-Aside | Read-heavy | Load on miss pattern |
| * Invalidation | Data changes | Clear related keys |

### Game Python (DEP:GamePython)
**Trigger:** pygame, arcade, ursina, panda3d, pyglet
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Game-Loop | Always | Fixed timestep, variable render |
| * Asset-Preload | Has assets | Load screens, progress bars |
| * Input-Mapping | Has controls | Configurable keybindings |
| * State-Machine | Multiple screens | Clean state transitions |
| * Delta-Time | Movement/physics | Frame-independent movement |

### Game JS (DEP:GameJS)
**Trigger:** phaser, three.js, pixi.js, babylon.js, kaboom
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Sprite-Atlas | Multiple sprites | Texture packing |
| * Object-Pool | Frequent create/destroy | Reuse objects |
| * RAF-Loop | Animation | requestAnimationFrame |
| * WebGL-Fallback | 3D content | Canvas 2D fallback |
| * Audio-Context | Sound effects | Single AudioContext |

### Game Engine (DEP:GameEngine)
**Trigger:** Unity (.csproj), Unreal (*.uproject), Godot (project.godot)
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Scene-Organization | Multiple scenes | Clear hierarchy, naming convention |
| * Prefab-Reuse | Reusable objects | Prefabs/scenes over copies |
| * Build-Profiles | Multiple platforms | Platform-specific settings |
| * Asset-LFS | Team project | Git LFS for binary assets |
| * Input-System | Has controls | Input actions, rebindable keys |
| * Platform-Optimize | Target platform | Quality presets per platform |

### HTTP Client (DEP:HTTP)
**Trigger:** requests, httpx, aiohttp, axios, got
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Timeout-Always | External calls | Explicit timeouts |
| * Retry-Transient | Network calls | Exponential backoff |
| * Session-Reuse | Multiple requests | Connection pooling |
| * Error-Handle | All requests | Status code handling |
| * Response-Validate | API responses | Schema validation |

### ORM (DEP:ORM)
**Trigger:** sqlalchemy, prisma, drizzle, typeorm, sequelize
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * N+1-Prevent | Has relations | Eager load or batch queries |
| * Query-Optimize | Complex queries | Analyze query plans, use EXPLAIN |
| * Loading-Strategy | Has relations | Explicit eager/lazy per use case |
| * Transaction-Boundary | Multi-write | Clear scope, rollback on error |
| * Index-Design | Query patterns | Indexes for WHERE/JOIN columns |
| * Bulk-Operations | Many records | Use bulk insert/update APIs |

### Auth (DEP:Auth)
**Trigger:** authlib, next-auth, clerk, auth0, supabase-auth
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Token-Secure | JWT/sessions | HttpOnly, Secure flags |
| * Refresh-Flow | Long sessions | Refresh token rotation |
| * RBAC-Clear | Multiple roles | Role-based permissions |
| * Session-Invalidate | Logout/revoke | Clear all sessions option |
| * MFA-Support | Sensitive ops | Optional 2FA |

### Payment (DEP:Payment)
**Trigger:** stripe, paypal, square, paddle
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Webhook-Verify | Payment events | Signature validation |
| * Idempotency-Key | Create operations | Prevent duplicates |
| * Amount-Server | Prices | Server-side price calculation |
| * Error-Handle | All payments | User-friendly errors |
| * Audit-Trail | Transactions | Complete payment logs |

### Email (DEP:Email)
**Trigger:** sendgrid, mailgun, resend, nodemailer
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Template-System | Multiple emails | Reusable templates |
| * Queue-Async | Bulk/triggered | Background sending |
| * Bounce-Handle | Production | Process bounces/complaints |
| * Rate-Aware | Bulk sending | Respect provider limits |
| * Unsubscribe | Marketing | One-click unsubscribe |

### Search (DEP:Search)
**Trigger:** elasticsearch, meilisearch, algolia, typesense
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Index-Strategy | Document types | Separate vs combined |
| * Sync-Mechanism | Data updates | Real-time vs batch |
| * Relevance-Tune | User search | Custom ranking |
| * Typo-Tolerance | User input | Fuzzy matching |
| * Facet-Design | Filters | Efficient faceting |

### PDF (DEP:PDF)
**Trigger:** reportlab, weasyprint, pdfkit, puppeteer
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Template-Based | Multiple docs | HTML/template generation |
| * Async-Generate | Large PDFs | Background processing |
| * Stream-Output | Downloads | Stream don't buffer |
| * Font-Embed | Custom fonts | Embed for consistency |
| * Accessibility | Public docs | Tagged PDF when possible |

### Blockchain (DEP:Blockchain)
**Trigger:** web3, ethers, hardhat, brownie
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Gas-Estimate | Transactions | Pre-estimate gas |
| * Nonce-Manage | Multiple tx | Track nonce locally |
| * Event-Listen | Contract events | Indexed event handling |
| * Testnet-First | Development | Test before mainnet |
| * Key-Security | Private keys | Never in code/logs |

### AR/VR (DEP:ARVR)
**Trigger:** openxr, webxr, ar-foundation
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Frame-Budget | XR rendering | 90fps minimum |
| * Comfort-Settings | VR | Teleport/snap turn options |
| * Fallback-Mode | Device support | Non-XR fallback |
| * Input-Abstract | Controllers | Abstract input layer |
| * Performance-Tier | Device range | Quality presets |

### IoT (DEP:IoT)
**Trigger:** micropython, paho-mqtt, esphome
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Reconnect-Logic | Network devices | Auto-reconnect |
| * Power-Aware | Battery devices | Sleep modes |
| * OTA-Update | Deployed devices | Remote updates |
| * Data-Buffer | Unreliable network | Local buffer |
| * Watchdog | Long-running | Hardware watchdog |

### Logging (DEP:Logging)
**Trigger:** loguru, structlog, winston, pino
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Structured-Format | Production | JSON logging |
| * Level-Config | Environments | Configurable log level |
| * Context-Inject | Request handling | Request ID, user ID |
| * Sensitive-Redact | User data | Mask PII |
| * Rotation-Strategy | File logs | Size/time rotation |

### Object Store (DEP:ObjectStore)
**Trigger:** boto3, minio, cloudinary, uploadthing
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Presigned-URLs | Client uploads | Time-limited URLs |
| * Content-Type | File uploads | Validate MIME type |
| * Size-Limit | User uploads | Max file size |
| * Path-Structure | Many files | Organized paths |
| * Lifecycle-Rules | Temp files | Auto-expiry |

### SMS (DEP:SMS)
**Trigger:** twilio, vonage, messagebird, plivo
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Delivery-Status | Critical messages | Track delivery callbacks |
| * Rate-Throttle | Bulk sending | Respect carrier limits |
| * Opt-Out | Marketing | Honor STOP requests |
| * Fallback-Provider | High availability | Secondary provider |
| * Message-Template | Multiple messages | Pre-approved templates |

### Notification (DEP:Notification)
**Trigger:** firebase-admin, onesignal, pusher, novu
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Channel-Preference | Multiple channels | User-configurable channels |
| * Batch-Send | Many recipients | Batch API calls |
| * Silent-Push | Data sync | Background updates |
| * Token-Refresh | Mobile push | Handle token rotation |
| * Fallback-Channel | Critical alerts | Email if push fails |

### Excel (DEP:Excel)
**Trigger:** openpyxl, xlsxwriter, exceljs, sheetjs
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Stream-Write | Large files | Write in chunks |
| * Formula-Safe | User data | Escape formula injection |
| * Style-Template | Multiple reports | Reusable styles |
| * Memory-Optimize | Large datasets | Use write-only mode |
| * Sheet-Naming | Multiple sheets | Valid sheet names |

### Crypto (DEP:Crypto)
**Trigger:** cryptography, pycryptodome, nacl, jose
| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Algorithm-Modern | Encryption | AES-256-GCM, ChaCha20 |
| * Key-Rotation | Long-lived keys | Scheduled rotation |
| * IV-Unique | Each encryption | Never reuse IV/nonce |
| * Timing-Safe | Comparisons | Constant-time compare |
| * Key-Derivation | Passwords | Argon2/scrypt, not MD5/SHA1 |
