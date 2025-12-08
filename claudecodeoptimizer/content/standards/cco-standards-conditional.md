<!-- CCO_CONDITIONALS_START -->
# Project-Specific Standards
*Dynamically selected by /cco-tune based on project analysis*
*Written to local ./CLAUDE.md - included in CLAUDE.md and AGENTS.md exports*

---

## Security & Compliance
**When:** Data: PII/Regulated OR Scale: 10K+ OR Compliance != None
- Input Validation: Pydantic/Zod/JSON Schema
- SQL Safety: parameterized queries, ORM safe methods
- XSS Prevention: sanitize output, CSP headers
- Auth: OAuth2/OIDC + RBAC, verify every request
- Rate Limit: all endpoints, per-user/IP
- Encryption: AES-256 at rest for sensitive data
- Audit Log: security events, immutable
- CORS: explicit origins, no wildcard in prod
- License: track deps, review GPL
- Compliance: implement required controls
- Data Classification: by sensitivity level
- Retention: documented, enforced

---

## Scale Standards

### Scale > Small (100-1K)
**When:** Scale: 100-1K OR Scale: 1K-10K OR Scale: 10K+
- Caching: TTL, invalidation, cache-aside
- Lazy Load: defer non-critical resources

### Scale > Medium (1K-10K)
**When:** Scale: 1K-10K OR Scale: 10K+
- Connection Pool: reuse, appropriate sizing
- Async I/O: no blocking in async context

### Scale > Large (10K+)
**When:** Scale: 10K+ OR Architecture: Microservices
- Circuit Breaker: fail fast on unhealthy downstream
- Idempotency: safe to retry
- API Versioning: explicit, backward compatible
- DI: inject dependencies for testing
- Event-Driven: async between services
- Bounded Contexts: own models per domain
- Compression: gzip/brotli responses
- Indexing: proper indexes, query optimization

---

## Backend Standards

### Backend > API
**When:** API: REST OR API: GraphQL OR API: gRPC
- REST: proper methods, status codes, resource naming
- Pagination: cursor-based for large datasets
- OpenAPI/AsyncAPI: spec with examples, synced
- Errors: consistent format, no stack traces in prod

### Backend > API GraphQL
**When:** API: GraphQL
- GraphQL: complexity limits, depth limits, persisted queries

### Backend > API gRPC
**When:** API: gRPC
- gRPC: proto versioning, backward compatibility

### Backend > Data
**When:** DB != None
- Backup: automated, tested restore, RPO/RTO
- Migrations: versioned, backward compatible, rollback
- N+1 Prevention: batch queries, eager loading
- Transactions: ACID or eventual consistency
- Connection Pool: reuse, appropriate sizing

### Backend > Operations
**When:** CI/CD detected AND Type != CLI AND Type != Library
- Config as Code: versioned, validated, env-aware
- Health Endpoints: /health + /ready
- Graceful Shutdown: drain connections on SIGTERM
- Observability: metrics, logs, traces
- CI Gates: lint + test + coverage before merge
- Blue/Green or Canary: zero-downtime deploys
- Feature Flags: decouple deploy from release

### Backend > CI Only
**When:** CI/CD detected AND (Type: CLI OR Type: Library)
- Config as Code: versioned, validated
- CI Gates: lint + test + coverage before merge

---

## Frontend Standards
**When:** Frontend detected (React/Vue/Angular/Svelte/Next/Nuxt/etc.)

### Frontend > Accessibility
- WCAG 2.2 AA: perceivable, operable, understandable
- Semantic HTML: native elements
- Keyboard Nav: all interactive accessible
- Contrast: 4.5:1 normal, 3:1 large

### Frontend > Performance
- Core Web Vitals: LCP <2.5s, INP <200ms, CLS <0.1
- Bundle Size: code splitting, tree shaking, lazy load
- Responsive: mobile-first, fluid layouts

### Frontend > Quality
- State Management: predictable, single source
- AI Slop Prevention: unique design, no generic patterns
- Progressive Enhancement: core works without JS

---

## App Standards

### Apps > Mobile
**When:** iOS/Android/React Native/Flutter detected
- Offline-First: local storage, sync when connected
- Battery: minimize background, batch operations
- Deep Linking: universal/app links
- Push: permission handling, payload optimization
- Platform: iOS HIG, Material Design compliance
- App Size: asset optimization, on-demand resources

### Apps > Desktop
**When:** Electron/Tauri/native desktop detected
- Auto-Update: secure update mechanism
- Native: OS notifications, file associations
- Multi-Window: proper management
- Memory: prevent leaks, proper cleanup

### Apps > CLI
**When:** Type: CLI
- Help: --help with examples for every command
- Exit Codes: 0 success, non-zero with meaning
- Signals: handle SIGINT/SIGTERM gracefully
- Output: human-readable default, --json for scripts
- Config: env > config file > CLI args > defaults

---

## Library Standards
**When:** Type: Library
- Minimal Deps: reduce transitive burden
- Tree-Shakeable: ES modules, no side effects
- Type Definitions: TypeScript or JSDoc
- Deprecation: warn before removal, migration path

---

## Infrastructure Standards

### Infra > Container
**When:** Docker detected (NOT in examples/, benchmarks/, test/)
- Image Size: multi-stage, distroless base
- Security: non-root user, CVE scanning
- Resource Limits: CPU/memory limits and requests
- Secrets: external, not in images

### Infra > Kubernetes
**When:** Kubernetes/Helm detected
- Pod Security: SecurityContext, NetworkPolicy
- Health Probes: liveness + readiness configured
- Resource Quotas: namespace limits defined

### Infra > Serverless
**When:** Lambda/Functions/Vercel/Netlify detected
- Cold Start: minimize bundle, lazy init
- Timeout: graceful handling, cleanup
- Stateless: no local state between invocations
- Cost: right-size memory

### Infra > Monorepo
**When:** nx.json/turbo.json/lerna.json/pnpm-workspace.yaml detected
- Workspace: clear package boundaries
- Selective Testing: only affected packages
- Shared Deps: consistent versions, hoisting
- Build Cache: incremental, remote cache

---

## Specialized Standards

### ML/AI Projects
**When:** torch/tensorflow/sklearn/transformers/langchain detected
- Reproducibility: seed everything, version data+code+model
- Experiment Tracking: log params, metrics, artifacts
- Data Versioning: DVC or similar
- Model Registry: versioned with metadata
- Inference: quantization, batching, caching
- Bias: fairness metrics, drift detection

### Game Development
**When:** Unity/Unreal/Godot detected
- Frame Budget: 16ms for 60fps, profile regularly
- Asset Pipeline: LOD, compression, streaming
- Input: responsive, rebindable controls
- Save System: versioned, corruption recovery

---

## Team Standards

### Team > Small (2-5)
**When:** Team: 2-5 OR Team: 6+
- Review: async PR reviews acceptable
- Docs: README, CONTRIBUTING
- Communication: Slack/Discord for quick decisions
- Git Flow: feature branches, clean history

### Team > Medium-Large (6+)
**When:** Team: 6+
- ADR: decisions + context + consequences
- Local Parity: match production environment
- Golden Paths: recommended approaches documented
- Code Owners: CODEOWNERS for review assignment
- Onboarding: documented setup, first-task guides
- Branch Protection: require reviews, status checks
- PR Templates: consistent descriptions
- Atomic Commits: one logical change per commit

---

## i18n Standards
**When:** locales/i18n/messages/translations/ detected OR i18n deps
- Externalized: no hardcoded user text
- Unicode: UTF-8 everywhere
- RTL: support Arabic, Hebrew layouts
- Locale: date/time/number/currency formatting
- Pluralization: proper rules per language

---

## Real-time Standards

### Real-time > Basic
**When:** WebSocket/SSE/socket.io detected
- Connection: reconnect logic, heartbeat
- State Sync: handle stale data gracefully

### Real-time > Standard
**When:** Real-time: Standard OR Real-time: Low-latency selected
- WebSocket: proper handshake, ping/pong
- Event Ordering: sequence numbers, causality
- Backpressure: handle slow consumers
- Fallback: degrade to polling

### Real-time > Low-latency
**When:** Real-time: Low-latency selected
- Binary Protocols: protobuf, msgpack
- Edge Compute: minimize round trips
- Connection Affinity: sticky sessions
- Pre-warming: eliminate cold starts
- Memory: zero-copy where possible
- Jitter: consistent latency
- Geographic: regional endpoints

---

## Testing Standards

### Testing > Basics
**When:** Testing: Basics OR Testing: Standard OR Testing: Full selected
- Unit Tests: isolated, fast, deterministic
- Mocking: external deps mocked
- Coverage: >60% line

### Testing > Standard
**When:** Testing: Standard OR Testing: Full selected
- Integration: test component interactions
- Fixtures: reusable, maintainable
- Coverage: >80% line
- CI: tests run on every PR

### Testing > Standard + UI
**When:** (Testing: Standard OR Testing: Full) AND Frontend detected
- Snapshot: UI component stability

### Testing > Full
**When:** Testing: Full selected
- E2E: critical user journeys
- Visual Regression: catch UI changes
- Contract Testing: API compatibility
- Mutation Testing: test quality validation
- Coverage: >90% line
- Flaky Detection: quarantine unreliable
- Parallelization: fast feedback
- Test Data: factories, fixtures

### Testing > Performance
**When:** Performance testing required OR Scale: 10K+
- Load: expected traffic patterns
- Stress: breaking point identification
- Benchmark: track regressions
- Profiling: identify bottlenecks

---

## Observability Standards

### Observability > Basics
**When:** SLA: None OR SLA: Standard OR SLA: High OR SLA: Critical
- Error Tracking: Sentry or equivalent
- Alerting: critical failures only

### Observability > Standard
**When:** SLA: Standard OR SLA: High OR SLA: Critical
- Structured Logging: JSON, correlation IDs
- Metrics: RED method (Rate, Errors, Duration)
- Distributed Tracing: request flow visibility
- Alerting: tiered severity

### Observability > High Availability
**When:** SLA: High OR SLA: Critical
- Redundancy: no single points of failure
- Failover: automatic recovery
- Load Balancing: distribute traffic
- Auto-scaling: respond to demand
- Incident Response: runbooks documented

### Observability > Full Resilience
**When:** SLA: Critical
- Multi-region: geographic redundancy
- Chaos Engineering: regular failure injection
- Disaster Recovery: tested DR plans
- Global LB: anycast, GeoDNS
- Data Replication: sync/async per requirements
- Capacity Planning: proactive scaling
- SLO/SLI: error budgets
- Post-mortem: blameless analysis
- On-call: defined escalation
- Status Page: public incident communication
- Dependency Mapping: understand blast radius
<!-- CCO_CONDITIONALS_END -->
