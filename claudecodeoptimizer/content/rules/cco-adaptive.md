# Adaptive Rules
*Selected by /cco-tune based on detection. Each rule evaluated individually.*

## Trigger Reference

| Symbol | Meaning | Detection Source |
|--------|---------|------------------|
| D: | Data classification | Auth patterns, encryption usage |
| S: | Scale (users/RPS) | Replicas, HPA, load balancer config |
| T: | Application type | Entry points, exports analysis |
| A: | Architecture | Service count, Dockerfile patterns |
| C: | Compliance | SECURITY.md, audit logs, keywords |
| DB: | Database | ORM deps, migrations/, prisma/schema |
| API: | API style | Routes, decorators, proto files |
| RT: | Real-time | WebSocket/SSE deps |

## Granular Selection [CRITICAL]

Each rule has an **Applicability Check**. Only include rules where check passes.

**Format in context:**
```markdown
### {Category} - {Trigger reason}
| Standard | Rule |
|----------|------|
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

| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Backup-Strategy | Has database | Automated + tested restore |
| * Migration-Safe | Has schema | Versioned + rollback |
| * N+1-Prevent | Has ORM | Batch/eager loading |
| * Transaction-Safe | Multi-write ops | ACID or eventual |

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

| Rule | Applicability Check | Concise |
|------|---------------------|---------|
| * Frame-Budget | Always | 16ms target |
| * Asset-Streaming | Large assets | LOD + compression |
| * Input-Rebind | Has controls | User customizable |
| * Save-Versioned | Has saves | Migration support |

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
| * Structured-Logs | Always | JSON + correlationID |
| * RED-Metrics | Has API | Rate, Error, Duration |
| * Distributed-Trace | Multi-service | Request tracing |

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
