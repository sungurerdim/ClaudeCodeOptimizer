# CCO Rules

**Single Source of Truth** for all CCO rules organized by category.

## Summary

| Category | Files | Location | Loading |
|----------|-------|----------|---------|
| Core | 3 | Context (injected) | Always (SessionStart hook) |
| Languages | 21 | `./.claude/rules/` | Per-project |
| Frameworks | 8 | `./.claude/rules/` | Per-project |
| Operations | 12 | `./.claude/rules/` | Per-project |
| **Total** | **44** | | |

**All CCO rules use `cco-` prefix** for safe identification and updates.

---

## Rules Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  CORE (injected into context on every session start)            │
├─────────────────────────────────────────────────────────────────┤
│  SessionStart hook reads from plugin and injects:               │
│    → cco-foundation.md    Design principles, code quality       │
│    → cco-safety.md        Non-negotiable security standards     │
│    → cco-workflow.md      AI execution patterns                 │
│  (No files copied - direct context injection via hook output)   │
├─────────────────────────────────────────────────────────────────┤
│  PROJECT-SPECIFIC (installed via /cco:tune)                     │
├─────────────────────────────────────────────────────────────────┤
│  ./.claude/rules/                                               │
│    ├── cco-profile.md       Project metadata (YAML)             │
│    ├── cco-{language}.md    Language-specific rules             │
│    ├── cco-{framework}.md   Framework-specific rules            │
│    └── cco-{operation}.md   Operations rules                    │
└─────────────────────────────────────────────────────────────────┘
```

**Context Loading:**
- Core rules: Injected via SessionStart hook (`additionalContext`)
- Project rules: Auto-loaded from `./.claude/rules/*.md`

**Safe Updates:** Only `cco-*.md` files are managed. User's own rules (without prefix) are never touched.

---

## Core Rules (3 files)

*Injected into context on every session start via SessionStart hook.*

### cco-foundation.md
- Design principles (SSOT, DRY, YAGNI, KISS)
- Code quality standards
- Complexity thresholds
- Refactoring safety rules
- UX/DX guidelines

### cco-safety.md
- Non-negotiable standards (7 critical rules)
- Security priority enforcement
- OWASP A01-A10 base security
- Data protection requirements

### cco-workflow.md
- AI execution order (Read-First, Plan-Before-Act)
- Agent delegation guidelines
- Decision making rules
- Reasoning strategies
- Output standards

---

## Language Rules (21 files)

*Copied to project `.claude/rules/` based on detection.*

### Mainstream Languages (10)

| File | Trigger | Key Rules |
|------|---------|-----------|
| `cco-python.md` | pyproject.toml, *.py | Type hints, async patterns, Pydantic |
| `cco-typescript.md` | tsconfig.json, *.ts | Strict mode, Zod validation, ESM |
| `cco-go.md` | go.mod, *.go | Error wrapping, context, interfaces |
| `cco-rust.md` | Cargo.toml, *.rs | Result propagation, ownership, clippy |
| `cco-java.md` | pom.xml, *.java | Virtual threads, records, streams |
| `cco-ruby.md` | Gemfile, *.rb | Rails patterns, RSpec conventions |
| `cco-php.md` | composer.json, *.php | Laravel patterns, PSR standards |
| `cco-csharp.md` | *.csproj, *.cs | .NET patterns, async/await, LINQ |
| `cco-swift.md` | Package.swift, *.swift | iOS patterns, SwiftUI, Combine |
| `cco-kotlin.md` | build.gradle.kts, *.kt | Coroutines, Android patterns |

### Niche Languages (11)

| File | Trigger | Key Rules |
|------|---------|-----------|
| `cco-elixir.md` | mix.exs | OTP supervision, Phoenix, GenServer |
| `cco-erlang.md` | rebar.config | OTP patterns, fault tolerance |
| `cco-scala.md` | build.sbt | Functional patterns, Cats/ZIO |
| `cco-haskell.md` | *.cabal, stack.yaml | Monads, type classes, lazy evaluation |
| `cco-fsharp.md` | *.fsproj | Railway-oriented, computation expressions |
| `cco-ocaml.md` | dune, *.opam | Module system, pattern matching |
| `cco-gleam.md` | gleam.toml | Type-safe Erlang VM, pipelines |
| `cco-clojure.md` | deps.edn, project.clj | Immutability, REPL-driven, specs |
| `cco-r.md` | DESCRIPTION, *.R | Data frames, tidyverse, vectors |
| `cco-julia.md` | Project.toml | Multiple dispatch, scientific computing |
| `cco-perl.md` | cpanfile, *.pl | Regex, one-liners, CPAN patterns |

---

## Framework Rules (8 files)

*Copied to project `.claude/rules/` based on detection.*

| File | Trigger | Coverage |
|------|---------|----------|
| `cco-backend.md` | Framework deps | Express, FastAPI, Django, Rails, Spring, NestJS, Gin, Fiber, Echo, Phoenix, Actix, Axum, Rocket, Warp, Vapor, Ktor, ASP.NET, Flask, Hono, etc. |
| `cco-frontend.md` | UI framework deps | React, Vue, Svelte, Angular, SolidJS, Qwik, Astro, Next.js, Nuxt, SvelteKit + i18n |
| `cco-api.md` | routes/, decorators | REST, GraphQL, gRPC, OpenAPI, RFC 7807 errors |
| `cco-testing.md` | Test framework deps | pytest, Jest, Vitest, RSpec, JUnit + coverage tiers (60/80/90%) |
| `cco-orm.md` | ORM deps | Prisma, SQLAlchemy, TypeORM, Drizzle, ActiveRecord, Entity Framework |
| `cco-mobile.md` | Mobile deps | Flutter, React Native, iOS (Swift), Android (Kotlin) |
| `cco-ml.md` | ML deps | PyTorch, TensorFlow, LangChain, RAG patterns, prompt engineering |
| `cco-realtime.md` | WebSocket deps | WebSocket, SSE, Socket.IO patterns |

---

## Operations Rules (12 files)

*Copied to project `.claude/rules/` based on detection.*

| File | Trigger | Coverage |
|------|---------|----------|
| `cco-infrastructure.md` | Dockerfile, K8s | Docker multi-stage, K8s security, Terraform, IaC patterns, API Gateway, Service Mesh, Build Cache |
| `cco-deployment.md` | Deploy configs | Fly.io, Railway, Render, Vercel, Netlify, AWS, GCP, Azure |
| `cco-cicd.md` | CI configs | GitHub Actions, GitLab CI, Jenkins, CircleCI |
| `cco-observability.md` | Monitoring deps | Prometheus, Grafana, OpenTelemetry, Sentry |
| `cco-scale.md` | Scale indicators | Circuit breaker, retry patterns, rate limiting, caching + SLA tiers |
| `cco-database.md` | DB deps | SQL, NoSQL, migrations, connection pools, indexing |
| `cco-build.md` | Build tools | Monorepo (Nx, Turbo), bundlers, linters |
| `cco-messagequeue.md` | Queue deps | Kafka, RabbitMQ, NATS, SQS, Redis queues |
| `cco-runtimes.md` | Runtime indicators | Node.js, Bun, Deno patterns |
| `cco-project-types.md` | Project structure | CLI, Library, Service patterns |
| `cco-compliance.md` | Compliance selected | GDPR, HIPAA, PCI-DSS, SOC2, ISO27001 |
| `cco-security.md` | PII/Regulated data | OWASP, input validation, encryption, audit logging |

---

## Detection & Installation

### Auto-Detection (via /cco:tune)

| Detection Type | Method | Example |
|----------------|--------|---------|
| Language | Manifest files | pyproject.toml → `cco-python.md` |
| Framework | Dependencies | react in package.json → `cco-frontend.md` |
| Infrastructure | Config files | Dockerfile → `cco-infrastructure.md` |
| Domain | Code patterns | @app.get → `cco-api.md` |

### User-Input (via interactive setup)

| Question | Options | Effect |
|----------|---------|--------|
| Data Sensitivity | Public, PII, Regulated | Adds `cco-security.md`, `cco-compliance.md` |

---

## File Locations

### Every Session (via SessionStart hook)

```
# Core rules are injected directly into context (no files created)
→ cco-foundation.md content
→ cco-safety.md content
→ cco-workflow.md content
```

### After /cco:tune

```
project/.claude/rules/
├── cco-profile.md        ← YAML project metadata
├── cco-{language}.md     ← Based on detection
├── cco-{framework}.md    ← Based on detection
└── cco-{operation}.md    ← Based on detection
```

**Note:** All project rules are stored in flat structure directly under `.claude/rules/` (not in subdirectories).

---

## Sources

- [Claude Code Memory Management](https://code.claude.com/docs/en/memory)
- [Claude Code Plugins Reference](https://code.claude.com/docs/en/plugins-reference)
- [Claude Code Discover Plugins](https://code.claude.com/docs/en/discover-plugins)
