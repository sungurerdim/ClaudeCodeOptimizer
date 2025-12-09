<!-- CCO_ADAPTIVE_START -->
# Adaptive Rules
*Project-specific rules selected by /cco-tune*

## Application [CRITICAL]

### Trigger Evaluation [REQUIRED]
Evaluate triggers in order. Apply ALL matching rules.

| Symbol | Meaning | Example |
|--------|---------|---------|
| `D:` | Data classification | D:PII, D:Regulated |
| `S:` | Scale (users/requests) | S:100+, S:1K+, S:10K+ |
| `T:` | Application type | T:CLI, T:Library, T:API |
| `A:` | Architecture | A:Microservices, A:Monolith |
| `C:` | Compliance | C:HIPAA, C:SOC2, C:GDPR |
| `+` | Inherits previous tier | All lower tier rules apply |

### Inheritance [STRICT]
Cumulative sections (marked `[cumulative]`) inherit ALL lower tiers.
- S:10K+ includes S:1K+ AND S:100+ rules
- Testing:Full includes Testing:Standard+ AND Testing:Basics+

---

## Security & Compliance
**Triggers:** `D:PII` | `D:Regulated` | `S:10K+` | `C:*`

| Category | Rules |
|----------|-------|
| * Input | Pydantic/Zod/JSON Schema validation |
| * SQL | Parameterized queries, ORM safe methods |
| * XSS | Sanitize output, CSP headers |
| * Auth | OAuth2/OIDC+RBAC, verify every request |
| * Rate-Limit | All endpoints, per-user/IP |
| * Encryption | AES-256 at rest for sensitive data |
| * Audit | Security events, immutable log |
| * CORS | Explicit origins, no wildcard in prod |
| * License | Track deps, review GPL |
| * Compliance | Implement required controls |
| * Data-Class | By sensitivity level |
| * Retention | Documented, enforced |

---

## Scale [cumulative]

| Tier | Trigger | Rules |
|------|---------|-------|
| * Small | S:100+ | Caching (TTL, invalidation, cache-aside), LazyLoad |
| * Medium | S:1K+ | +ConnPool (reuse, sizing), +AsyncIO (no blocking) |
| * Large | S:10K+ \| A:Microservices | +CircuitBreaker, +Idempotency, +APIVersion, +DI, +EventDriven, +BoundedContexts, +Compression, +Indexing |

**Inheritance Example:**
- Project with S:10K+ gets: Small + Medium + Large rules (all 3 tiers)

---

## Backend

### API
**Triggers:** `API:REST` | `API:GraphQL` | `API:gRPC`

| Rule | Description |
|------|-------------|
| * REST | Proper methods, status codes, resource naming |
| * Pagination | Cursor-based for large datasets |
| * OpenAPI/AsyncAPI | Spec with examples, synced |
| * Errors | Consistent format, no stack traces in prod |

### API Extensions

| Type | Trigger | Rules |
|------|---------|-------|
| * GraphQL | API:GraphQL | Complexity limits, depth limits, persisted queries |
| * gRPC | API:gRPC | Proto versioning, backward compatibility |

### Data
**Triggers:** `DB:*`

| Rule | Description |
|------|-------------|
| * Backup | Automated, tested restore, RPO/RTO |
| * Migrations | Versioned, backward compatible, rollback |
| * N+1 | Batch queries, eager loading |
| * Transactions | ACID or eventual consistency |
| * ConnPool | Reuse, appropriate sizing |

### Operations

| Type | Trigger | Rules |
|------|---------|-------|
| * Full | CI/CD & T:!CLI & T:!Library | Config-as-Code, /health+/ready, GracefulShutdown, Observability, CI-Gates, Blue/Green, FeatureFlags |
| * CI-Only | CI/CD & (T:CLI \| T:Library) | Config-as-Code (versioned), CI-Gates (lint+test+coverage) |

---

## Frontend
**Triggers:** React/Vue/Angular/Svelte/Next/Nuxt detected

| Category | Rules |
|----------|-------|
| * A11y | WCAG 2.2 AA, semantic HTML, keyboard nav, contrast 4.5:1/3:1 |
| * Perf | LCP<2.5s, INP<200ms, CLS<0.1, code-split, tree-shake, lazy |
| * Quality | Predictable state, unique design (no AI slop), progressive enhancement |

---

## Apps

| Type | Trigger | Rules |
|------|---------|-------|
| * Mobile | iOS/Android/RN/Flutter | Offline-first, battery-optimize, deep-links, push, platform-guidelines, app-size |
| * Desktop | Electron/Tauri/native | Auto-update, native-integration, multi-window, memory-cleanup |
| * CLI | T:CLI | --help+examples, exit-codes, SIGINT/SIGTERM, human+json output, config-precedence |

---

## Library
**Triggers:** `T:Library`

| Rule | Description |
|------|-------------|
| * Minimal-Deps | Reduce transitive burden |
| * Tree-Shakeable | ES modules, no side effects |
| * Types | TypeScript or JSDoc |
| * Deprecation | Warn before removal, migration path |

---

## Infrastructure

| Type | Trigger | Rules |
|------|---------|-------|
| * Container | Docker (not in examples/benchmarks/test) | Multi-stage, distroless, non-root, CVE-scan, resource-limits, external-secrets |
| * K8s | Kubernetes/Helm | SecurityContext, NetworkPolicy, probes, ResourceQuotas |
| * Serverless | Lambda/Functions/Vercel/Netlify | Minimize-bundle, graceful-timeout, stateless, right-size-memory |
| * Monorepo | nx/turbo/lerna/pnpm-workspace | Package-boundaries, selective-test, shared-deps, build-cache |

---

## Specialized

| Domain | Trigger | Rules |
|--------|---------|-------|
| * ML/AI | torch/tf/sklearn/transformers/langchain | Reproducibility (seed+version), experiment-tracking, data-versioning, model-registry, inference-optimize, bias-detection |
| * Game | Unity/Unreal/Godot | 16ms-frame-budget, LOD+compression+streaming, rebindable-input, versioned-saves |

---

## Team [cumulative]

| Size | Trigger | Rules |
|------|---------|-------|
| * Small | Team:2+ | Async-PR-review, README+CONTRIBUTING, Slack/Discord, feature-branches |
| * Large | Team:6+ | +ADR, +local-parity, +golden-paths, +CODEOWNERS, +onboarding, +branch-protection, +PR-templates, +atomic-commits |

---

## i18n
**Triggers:** locales/i18n/messages/translations detected | i18n deps

| Rule | Description |
|------|-------------|
| * Strings | Externalized |
| * Encoding | UTF-8 |
| * RTL | Support enabled |
| * Formatting | Locale-aware |
| * Pluralization | Rules implemented |

---

## Real-time [cumulative]

| Tier | Trigger | Rules |
|------|---------|-------|
| * Basic | WebSocket/SSE/socket.io | Reconnect-logic, heartbeat, stale-data-handling |
| * Standard | RT:Standard+ | +handshake, +event-ordering, +backpressure, +polling-fallback |
| * Low-latency | RT:Low-latency | +binary (protobuf/msgpack), +edge-compute, +sticky-sessions, +pre-warm, +zero-copy, +jitter-control, +geo-endpoints |

---

## Testing [cumulative]

| Tier | Trigger | Rules |
|------|---------|-------|
| * Basics | Testing:Basics+ | Unit (isolated, fast, deterministic), mocking, coverage>60% |
| * Standard | Testing:Standard+ | +integration, +fixtures, +coverage>80%, +CI-on-PR |
| * Standard+UI | Standard+ & Frontend | +snapshot-testing |
| * Full | Testing:Full | +e2e, +visual-regression, +contract, +mutation, +coverage>90%, +flaky-detection, +parallel, +test-data-factories |
| * Perf | Perf-required \| S:10K+ | Load, stress, benchmark, profiling |

---

## Observability [cumulative]

| Tier | Trigger | Rules |
|------|---------|-------|
| * Basics | SLA:* | Error-tracking (Sentry), critical-alerting |
| * Standard | SLA:Standard+ | +structured-logs (JSON+correlationID), +RED-metrics, +distributed-tracing, +tiered-alerting |
| * HA | SLA:High+ | +redundancy, +auto-failover, +load-balancing, +auto-scaling, +runbooks |
| * Critical | SLA:Critical | +multi-region, +chaos-engineering, +DR-tested, +global-LB, +data-replication, +capacity-planning, +SLO/SLI, +post-mortem, +on-call, +status-page, +dependency-mapping |
<!-- CCO_ADAPTIVE_END -->
