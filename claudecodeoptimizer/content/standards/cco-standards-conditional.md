<!-- CCO_CONDITIONALS_START -->
# Project-Specific Standards
*Dynamically selected by /cco-tune - written to ./CLAUDE.md*

## Trigger Legend
`D`=Data | `S`=Scale | `T`=Type | `A`=Arch | `C`=Compliance | `+`=inherits previous tier

---

## Security & Compliance [D:PII/Regulated | S:10K+ | C:*]
- Input: Pydantic/Zod/JSON Schema validation
- SQL: parameterized queries, ORM safe methods
- XSS: sanitize output, CSP headers
- Auth: OAuth2/OIDC+RBAC, verify every request
- Rate Limit: all endpoints, per-user/IP
- Encrypt: AES-256 at rest for sensitive data
- Audit: security events, immutable log
- CORS: explicit origins, no wildcard in prod
- License: track deps, review GPL
- Compliance: implement required controls
- Data Class: by sensitivity level
- Retention: documented, enforced

---

## Scale [cumulative]
| Tier | Trigger | Standards |
|------|---------|-----------|
| Small | S:100+ | Caching(TTL,invalidation,cache-aside), LazyLoad |
| Medium | S:1K+ | +ConnPool(reuse,sizing), +AsyncIO(no blocking) |
| Large | S:10K+ \| A:Microservices | +CircuitBreaker, +Idempotency, +APIVersion, +DI, +EventDriven, +BoundedContexts, +Compression(gzip/brotli), +Indexing |

---

## Backend

### API [API:REST | API:GraphQL | API:gRPC]
- REST: proper methods, status codes, resource naming
- Pagination: cursor-based for large datasets
- OpenAPI/AsyncAPI: spec with examples, synced
- Errors: consistent format, no stack traces in prod

### API Extensions
| Type | Trigger | Standards |
|------|---------|-----------|
| GraphQL | API:GraphQL | complexity limits, depth limits, persisted queries |
| gRPC | API:gRPC | proto versioning, backward compatibility |

### Data [DB:*]
- Backup: automated, tested restore, RPO/RTO
- Migrations: versioned, backward compatible, rollback
- N+1: batch queries, eager loading
- Transactions: ACID or eventual consistency
- ConnPool: reuse, appropriate sizing

### Operations
| Type | Trigger | Standards |
|------|---------|-----------|
| Full | CI/CD & T:!CLI & T:!Library | Config-as-Code, /health+/ready, GracefulShutdown, Observability, CI-Gates, Blue/Green, FeatureFlags |
| CI-Only | CI/CD & (T:CLI \| T:Library) | Config-as-Code(versioned), CI-Gates(lint+test+coverage) |

---

## Frontend [React/Vue/Angular/Svelte/Next/Nuxt detected]

| Category | Standards |
|----------|-----------|
| A11y | WCAG 2.2 AA, semantic HTML, keyboard nav, contrast 4.5:1/3:1 |
| Perf | LCP<2.5s, INP<200ms, CLS<0.1, code-split, tree-shake, lazy |
| Quality | predictable state, unique design (no AI slop), progressive enhancement |

---

## Apps

| Type | Trigger | Standards |
|------|---------|-----------|
| Mobile | iOS/Android/RN/Flutter | Offline-first, battery-optimize, deep-links, push, platform-guidelines, app-size |
| Desktop | Electron/Tauri/native | Auto-update, native-integration, multi-window, memory-cleanup |
| CLI | T:CLI | --help+examples, exit-codes, SIGINT/SIGTERM, human+json output, config-precedence |

---

## Library [T:Library]
- Minimal Deps: reduce transitive burden
- Tree-Shakeable: ES modules, no side effects
- Types: TypeScript or JSDoc
- Deprecation: warn before removal, migration path

---

## Infrastructure

| Type | Trigger | Standards |
|------|---------|-----------|
| Container | Docker (not in examples/benchmarks/test) | multi-stage, distroless, non-root, CVE-scan, resource-limits, external-secrets |
| K8s | Kubernetes/Helm | SecurityContext, NetworkPolicy, probes, ResourceQuotas |
| Serverless | Lambda/Functions/Vercel/Netlify | minimize-bundle, graceful-timeout, stateless, right-size-memory |
| Monorepo | nx/turbo/lerna/pnpm-workspace | package-boundaries, selective-test, shared-deps, build-cache |

---

## Specialized

| Domain | Trigger | Standards |
|--------|---------|-----------|
| ML/AI | torch/tf/sklearn/transformers/langchain | reproducibility(seed+version), experiment-tracking, data-versioning, model-registry, inference-optimize, bias-detection |
| Game | Unity/Unreal/Godot | 16ms-frame-budget, LOD+compression+streaming, rebindable-input, versioned-saves |

---

## Team [cumulative]
| Size | Trigger | Standards |
|------|---------|-----------|
| Small | Team:2+ | async-PR-review, README+CONTRIBUTING, Slack/Discord, feature-branches |
| Large | Team:6+ | +ADR, +local-parity, +golden-paths, +CODEOWNERS, +onboarding, +branch-protection, +PR-templates, +atomic-commits |

---

## i18n [locales/i18n/messages/translations detected | i18n deps]
Externalized strings | UTF-8 | RTL support | locale formatting | pluralization rules

---

## Real-time [cumulative]
| Tier | Trigger | Standards |
|------|---------|-----------|
| Basic | WebSocket/SSE/socket.io | reconnect-logic, heartbeat, stale-data-handling |
| Standard | RT:Standard+ | +handshake, +event-ordering, +backpressure, +polling-fallback |
| Low-latency | RT:Low-latency | +binary(protobuf/msgpack), +edge-compute, +sticky-sessions, +pre-warm, +zero-copy, +jitter-control, +geo-endpoints |

---

## Testing [cumulative]
| Tier | Trigger | Standards |
|------|---------|-----------|
| Basics | Testing:Basics+ | unit(isolated,fast,deterministic), mocking, coverage>60% |
| Standard | Testing:Standard+ | +integration, +fixtures, +coverage>80%, +CI-on-PR |
| Standard+UI | Standard+ & Frontend | +snapshot-testing |
| Full | Testing:Full | +e2e, +visual-regression, +contract, +mutation, +coverage>90%, +flaky-detection, +parallel, +test-data-factories |
| Perf | Perf-required \| S:10K+ | load, stress, benchmark, profiling |

---

## Observability [cumulative]
| Tier | Trigger | Standards |
|------|---------|-----------|
| Basics | SLA:* | error-tracking(Sentry), critical-alerting |
| Standard | SLA:Standard+ | +structured-logs(JSON+correlationID), +RED-metrics, +distributed-tracing, +tiered-alerting |
| HA | SLA:High+ | +redundancy, +auto-failover, +load-balancing, +auto-scaling, +runbooks |
| Critical | SLA:Critical | +multi-region, +chaos-engineering, +DR-tested, +global-LB, +data-replication, +capacity-planning, +SLO/SLI, +post-mortem, +on-call, +status-page, +dependency-mapping |
<!-- CCO_CONDITIONALS_END -->
