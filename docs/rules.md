# CCO Rules

**Single Source of Truth** for all CCO rules organized by category.

## Summary

| Category | Files | Rules | Location | Loading |
|----------|-------|-------|----------|---------|
| Core | 4 | 30 | 3 injected + 1 reference | Always (SessionStart hook) |
| Languages | 21 | 121 | `./.claude/rules/` | Per-project |
| Frameworks | 8 | 36 | `./.claude/rules/` | Per-project |
| Operations | 12 | 66 | `./.claude/rules/` | Per-project |
| **Total** | **45** | **253** | | |

**All CCO rules use `cco-` prefix** for safe identification and updates.

---

## Zero-Config Loading Mechanism

CCO leverages Claude Code's native rule loading — no custom loaders, no CLI wrappers:

### How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│  EVERY SESSION START (automatic)                                │
├─────────────────────────────────────────────────────────────────┤
│  1. SessionStart hook fires (Claude Code native feature)        │
│     └─→ Core rules injected via additionalContext               │
│                                                                 │
│  2. Claude Code reads .claude/rules/*.md (native behavior)      │
│     └─→ Project rules loaded automatically                      │
│                                                                 │
│  Result: All rules active, zero user action required            │
└─────────────────────────────────────────────────────────────────┘
```

### Why This Matters

| Traditional Approach | CCO Approach |
|---------------------|--------------|
| Custom CLI wrapper (`mytool --with-rules`) | Native Claude Code |
| Manual rule activation | Automatic on session start |
| Rules in separate config files | Rules in Claude Code's native `.claude/rules/` |
| Breaks with Claude Code updates | Uses official plugin API |

**Key Insight:** Claude Code automatically reads all `.md` files from `.claude/rules/`. CCO writes rules there → rules load automatically. No magic, just leveraging native behavior.

---

## Rules Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  CORE (injected into context on every session start)            │
├─────────────────────────────────────────────────────────────────┤
│  SessionStart hook reads from plugin and injects:               │
│    → Foundation rules   Uncertainty, Complexity, Scope          │
│    → Safety rules       Security violations, Validation         │
│    → Workflow rules     Read-Before-Edit, Accounting            │
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

## Core Rules (4 files · 30 rules)

*3 files (foundation, safety, workflow) injected into context via SessionStart hook. Thresholds is a reference file.*

### Foundation Rules [BLOCKER]

Enforceable constraints with measurable thresholds:

| Rule | Enforcement |
|------|-------------|
| **Uncertainty Protocol** | Ambiguous task → STOP and ask. Signal confidence: "~90% sure", "uncertain about X" |
| **Complexity Limits** | Method >50 lines, nesting >3, cyclomatic >15 → STOP and refactor |
| **File Creation** | Creating new files without explicit request → BLOCKED |
| **Change Scope** | Every changed line must trace to user's request. Unrelated → revert |
| **Code Volume** | Single-use abstractions, 100+ lines that could be 50 → rewrite |
| **Validation Boundaries** | Numbers need min/max, strings need max length, external calls need timeout |

**Hard Complexity Limits:**

| Metric | Limit |
|--------|-------|
| Cyclomatic Complexity | ≤ 15 |
| Method Lines | ≤ 50 |
| File Lines | ≤ 500 |
| Nesting Depth | ≤ 3 |
| Parameters | ≤ 4 |

### Safety Rules [BLOCKER]

Security violations = STOP. Fix before continuing:

| Pattern | Fix |
|---------|-----|
| Secrets in source | Move to env vars |
| Bare `except:`/`catch` | Catch specific types |
| Empty catch blocks | Add handling |
| Unsanitized external data | Add validation |
| `eval()`, `pickle.load()`, `yaml.load()` | Use safe alternatives |

**Safe vs Unsafe Patterns:**

| Safe | Unsafe |
|------|--------|
| `json.loads()` | `pickle.load()`, `eval()` |
| bcrypt, argon2 | MD5, SHA1, plaintext |
| TLS 1.2+ | HTTP, TLS 1.0/1.1 |

### Workflow Rules [BLOCKER]

Execution patterns that enforce discipline:

| Rule | Enforcement |
|------|-------------|
| **Read-Before-Edit** | Edit file not yet read → BLOCKED |
| **Task Completion** | No stopping early due to perceived limits. Every 20 steps: progress check |
| **Severity Levels** | CRITICAL (security/crash) → HIGH (broken) → MEDIUM (suboptimal) → LOW (style) |
| **No Deferrals** | In `--auto` mode: no "too complex", "might break", "consider later" — fix NOW |
| **Accounting** | Every operation ends with: `Applied: N | Failed: M | Needs Approval: D | Total: N+M+D` |

### Thresholds (Reference Only)

**File:** `cco-thresholds.md` — Not injected via hook, used as reference by agents.

Documents all hardcoded thresholds with rationale and sources:
- Complexity limits (cyclomatic, lines, nesting, parameters)
- Test coverage targets
- Architecture metrics (coupling, cohesion)
- Confidence scoring thresholds

---

## Language Rules (21 files · 121 rules)

*Copied to project `.claude/rules/` based on detection.*

### Mainstream Languages (10 files · 53 rules)

| File | Rules | Trigger | Key Rules |
|------|-------|---------|-----------|
| `cco-python.md` | 4 | pyproject.toml, *.py | Type hints, async patterns, Pydantic |
| `cco-typescript.md` | 4 | tsconfig.json, *.ts | Strict mode, Zod validation, ESM |
| `cco-go.md` | 3 | go.mod, *.go | Error wrapping, context, interfaces |
| `cco-rust.md` | 4 | Cargo.toml, *.rs | Result propagation, ownership, clippy |
| `cco-java.md` | 8 | pom.xml, *.java | Virtual threads, records, streams |
| `cco-ruby.md` | 7 | Gemfile, *.rb | Rails patterns, RSpec conventions |
| `cco-php.md` | 7 | composer.json, *.php | Laravel patterns, PSR standards |
| `cco-csharp.md` | 6 | *.csproj, *.cs | .NET patterns, async/await, LINQ |
| `cco-swift.md` | 6 | Package.swift, *.swift | iOS patterns, SwiftUI, Combine |
| `cco-kotlin.md` | 4 | build.gradle.kts, *.kt | Coroutines, Android patterns |

### Niche Languages (11 files · 68 rules)

| File | Rules | Trigger | Key Rules |
|------|-------|---------|-----------|
| `cco-elixir.md` | 4 | mix.exs | OTP supervision, Phoenix, GenServer |
| `cco-erlang.md` | 10 | rebar.config | OTP patterns, fault tolerance |
| `cco-scala.md` | 4 | build.sbt | Functional patterns, Cats/ZIO |
| `cco-haskell.md` | 6 | *.cabal, stack.yaml | Monads, type classes, lazy evaluation |
| `cco-fsharp.md` | 6 | *.fsproj | Railway-oriented, computation expressions |
| `cco-ocaml.md` | 6 | dune, *.opam | Module system, pattern matching |
| `cco-gleam.md` | 4 | gleam.toml | Type-safe Erlang VM, pipelines |
| `cco-clojure.md` | 10 | deps.edn, project.clj | Immutability, REPL-driven, specs |
| `cco-r.md` | 6 | DESCRIPTION, *.R | Data frames, tidyverse, vectors |
| `cco-julia.md` | 6 | Project.toml | Multiple dispatch, scientific computing |
| `cco-perl.md` | 6 | cpanfile, *.pl | Regex, one-liners, CPAN patterns |

---

## Framework Rules (8 files · 36 rules)

*Copied to project `.claude/rules/` based on detection.*

| File | Rules | Trigger | Coverage |
|------|-------|---------|----------|
| `cco-backend.md` | 3 | Framework deps | Express, FastAPI, Django, Rails, Spring, NestJS, Gin, Fiber, Echo, Phoenix, Actix, Axum, Rocket, Warp, Vapor, Ktor, ASP.NET, Flask, Hono, etc. |
| `cco-frontend.md` | 3 | UI framework deps | React, Vue, Svelte, Angular, SolidJS, Qwik, Astro, Next.js, Nuxt, SvelteKit + i18n |
| `cco-api.md` | 6 | routes/, decorators | REST, GraphQL, gRPC, OpenAPI, RFC 7807 errors |
| `cco-testing.md` | 6 | Test framework deps | pytest, Jest, Vitest, RSpec, JUnit + coverage tiers (60/80/90%) |
| `cco-orm.md` | 6 | ORM deps | Prisma, SQLAlchemy, TypeORM, Drizzle, ActiveRecord, Entity Framework |
| `cco-mobile.md` | 6 | Mobile deps | Flutter, React Native, iOS (Swift), Android (Kotlin) |
| `cco-ml.md` | 4 | ML deps | PyTorch, TensorFlow, LangChain, RAG patterns, prompt engineering |
| `cco-realtime.md` | 2 | WebSocket deps | WebSocket, SSE, Socket.IO patterns |

---

## Operations Rules (12 files · 66 rules)

*Copied to project `.claude/rules/` based on detection.*

| File | Rules | Trigger | Coverage |
|------|-------|---------|----------|
| `cco-infrastructure.md` | 5 | Dockerfile, K8s | Docker multi-stage, K8s security, Terraform, IaC patterns, API Gateway, Service Mesh, Build Cache |
| `cco-deployment.md` | 3 | Deploy configs | Fly.io, Railway, Render, Vercel, Netlify, AWS, GCP, Azure |
| `cco-cicd.md` | 6 | CI configs | GitHub Actions, GitLab CI, Jenkins, CircleCI |
| `cco-observability.md` | 4 | Monitoring deps | Prometheus, Grafana, OpenTelemetry, Sentry |
| `cco-scale.md` | 7 | Scale indicators | Circuit breaker, retry patterns, rate limiting, caching + SLA tiers |
| `cco-database.md` | 4 | DB deps | SQL, NoSQL, migrations, connection pools, indexing |
| `cco-build.md` | 9 | Build tools | Monorepo (Nx, Turbo), bundlers, linters |
| `cco-messagequeue.md` | 5 | Queue deps | Kafka, RabbitMQ, NATS, SQS, Redis queues |
| `cco-runtimes.md` | 3 | Runtime indicators | Node.js, Bun, Deno patterns |
| `cco-project-types.md` | 5 | Project structure | CLI, Library, Service patterns |
| `cco-compliance.md` | 10 | Compliance selected | GDPR, HIPAA, PCI-DSS, SOC2, ISO27001 |
| `cco-security.md` | 5 | PII/Regulated data | OWASP, input validation, encryption, audit logging |

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
