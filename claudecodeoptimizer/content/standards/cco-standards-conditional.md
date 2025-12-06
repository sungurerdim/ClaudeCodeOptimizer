<!-- CCO_CONDITIONALS_START -->
# Project-Specific Standards
*Dynamically selected by /cco-tune based on project analysis*
*Written to local ./CLAUDE.md, only triggered standards load*
*Included in both CLAUDE.md and AGENTS.md exports*

## Security & Compliance
**When:** Data: PII/Regulated OR Scale: 10K+ OR Compliance != None
- Input Validation: Pydantic (Python), Zod (JS/TS), JSON Schema
- SQL Safety: parameterized queries, ORM safe methods
- XSS Prevention: sanitize output, CSP headers
- Auth: OAuth2/OIDC + RBAC, verify every request
- Rate Limit: all endpoints, per-user/IP with headers
- Encryption: AES-256 for sensitive data at rest
- Audit Log: security events, immutable, queryable
- CORS: explicit origins, no wildcard in production
- License: track deps, no GPL without review
- Frameworks: implement required controls (SOC2/HIPAA/PCI/GDPR)
- Data Classification: by sensitivity level
- Retention Policy: documented, enforced

## Scale & Architecture
**When:** Scale: 10K+ OR Type: microservices OR Scale: 100+
- Circuit Breaker: fail fast on unhealthy downstream
- Idempotency: safe to retry without side effects
- API Versioning: explicit versions, backward compatible
- DI: inject dependencies, enable testing
- Event-Driven: async communication between services
- Bounded Contexts: own models/rules per domain
- Caching: TTL, invalidation strategy, cache-aside pattern
- Async I/O: no blocking in async context
- Connection Pool: reuse connections, appropriate sizing
- Lazy Load: defer non-critical resources
- Compression: gzip/brotli for responses
- Indexing: proper indexes, query optimization

## Backend Services
**When:** REST/GraphQL/gRPC detected OR DB detected OR CI/CD detected
### API
- REST: proper methods, status codes, resource naming
- Pagination: cursor-based for large datasets
- OpenAPI/AsyncAPI: spec with examples, synced with code
- Errors: consistent format, no stack traces in prod
- GraphQL: complexity limits, depth limits, persisted queries
- gRPC: proto versioning, backward compatibility

### Data
- Backup: automated, tested restore, defined RPO/RTO
- Migrations: versioned, backward compatible, rollback
- N+1 Prevention: batch queries, eager loading
- Retention: defined periods, auto-cleanup
- Transactions: ACID where needed, eventual consistency where acceptable

### Operations
- Config as Code: versioned, validated, env-aware
- Health Endpoints: /health + /ready
- Graceful Shutdown: drain connections on SIGTERM
- Observability: metrics, logs, traces (OpenTelemetry)
- CI Gates: lint + test + coverage before merge
- Blue/Green or Canary: zero-downtime deployments
- Feature Flags: decouple deploy from release

## Frontend
**When:** Frontend detected (React, Vue, Angular, Svelte, etc.)

### Accessibility
- WCAG 2.2 AA: perceivable, operable, understandable, robust
- Semantic HTML: native elements (button, nav, form)
- Keyboard Nav: all interactive elements accessible
- Contrast: 4.5:1 normal, 3:1 large text

### Performance
- Core Web Vitals: LCP <2.5s, FID <100ms, CLS <0.1
- Bundle Size: code splitting, tree shaking, lazy loading
- Responsive: mobile-first, fluid layouts

### Quality
- State Management: predictable state, single source of truth
- AI Slop Prevention: unique typography, intentional design, no generic patterns
- Progressive Enhancement: core functionality without JS

## Apps
**When:** iOS/Android/React Native/Flutter OR Electron/Tauri/native desktop OR CLI tool detected

### Mobile
- Offline-First: local storage, sync when connected
- Battery Efficiency: minimize background work, batch operations
- Deep Linking: universal links, app links
- Push Notifications: permission handling, payload optimization
- Platform Guidelines: iOS HIG, Material Design compliance
- App Size: asset optimization, on-demand resources

### Desktop
- Auto-Update: secure update mechanism
- Native Integration: OS notifications, file associations
- Multi-Window: proper window management
- Memory Management: prevent memory leaks, proper cleanup

### CLI
- Help: --help with examples for every command
- Exit Codes: 0 success, non-zero failure with meaning
- Signals: handle SIGINT/SIGTERM gracefully
- Output Modes: human-readable default, --json for scripts
- Config Precedence: env vars > config file > CLI args > defaults

## Library
**When:** Library/package detected
- Minimal Dependencies: reduce transitive dependency burden
- Tree-Shakeable: ES modules, no side effects in imports
- Type Definitions: TypeScript types or JSDoc
- Changelog: document breaking changes clearly
- Deprecation: warn before removal, provide migration path

## Infrastructure
**When:** Docker/Kubernetes OR Lambda/Functions OR Monorepo detected

### Container/K8s
- Image Size: multi-stage builds, distroless base
- Security: non-root user, CVE scanning (Trivy)
- Resource Limits: CPU/memory limits and requests
- Pod Security: SecurityContext, NetworkPolicy
- Secrets: external secrets, not in images

### Serverless
- Cold Start: minimize bundle size, lazy init
- Timeout Handling: graceful timeout, cleanup
- Stateless: no local state between invocations
- Cost Optimization: right-size memory, avoid over-provisioning

### Monorepo
- Workspace Management: clear package boundaries
- Selective Testing: only test affected packages
- Shared Dependencies: consistent versions, hoisting
- Build Caching: incremental builds, remote cache

## Specialized
**When:** ML/AI stack detected OR Game engine detected

### ML/AI Projects
- Reproducibility: seed everything, version data + code + model
- Experiment Tracking: log hyperparameters, metrics, artifacts
- Data Versioning: DVC or similar for dataset management
- Model Registry: versioned models with metadata
- Inference Optimization: quantization, batching, caching
- Bias Monitoring: fairness metrics, drift detection

### Game Development
- Frame Budget: 16ms for 60fps, profile regularly
- Asset Pipeline: LOD, compression, streaming
- Input Handling: responsive, rebindable controls
- Save System: versioned saves, corruption recovery

## Collaboration
**When:** Team: 2+ OR Multi-language requirement detected

### Team Basics (2-5)
- Informal Review: async PR reviews acceptable
- Shared Docs: README, CONTRIBUTING, basic docs
- Communication: Slack/Discord for quick decisions
- Git Flow: feature branches, clean history

### Team Full (6+)
- ADR: decisions + context + consequences
- Local Parity: match production environment
- Golden Paths: recommended approaches documented
- Code Owners: CODEOWNERS for review assignment
- Onboarding: documented setup, first-task guides
- Branch Protection: require reviews, status checks
- PR Templates: consistent PR descriptions
- Atomic Commits: one logical change per commit

### i18n
- Externalized: no hardcoded user text
- Unicode: UTF-8 everywhere
- RTL: support Arabic, Hebrew layouts
- Locale: date/time/number/currency formatting
- Pluralization: proper rules per language

## Real-time
**When:** WebSocket/SSE detected OR Real-time requirement selected

### Basic Real-time
- Connection Management: reconnect logic, heartbeat
- State Sync: handle stale data gracefully

### Standard Real-time
- WebSocket: proper handshake, ping/pong
- Event Ordering: sequence numbers, causality
- Backpressure: handle slow consumers
- Graceful Degradation: fallback to polling
- Connection Pooling: reuse connections

### Low-latency
- Binary Protocols: protobuf, msgpack
- Edge Compute: minimize round trips
- Connection Affinity: sticky sessions
- Pre-warming: eliminate cold starts
- Memory Optimization: zero-copy where possible
- Jitter Reduction: consistent latency
- Geographic Distribution: regional endpoints
- Hardware Acceleration: DPDK, kernel bypass

## Testing
**When:** Testing strategy selected

### Testing Basics
- Unit Tests: isolated, fast, deterministic
- Mocking: external dependencies mocked
- Coverage Target: >60% line coverage

### Testing Standard
- Integration Tests: test component interactions
- Test Fixtures: reusable, maintainable
- Coverage Target: >80% line coverage
- CI Integration: tests run on every PR
- Snapshot Testing: UI component stability

### Testing Full
- E2E Tests: critical user journeys
- Visual Regression: catch UI changes
- Contract Testing: API compatibility
- Mutation Testing: test quality validation
- Coverage Target: >90% line coverage
- Flaky Test Detection: quarantine unreliable tests
- Test Parallelization: fast feedback loops
- Test Data Management: factories, fixtures

### Performance Testing
- Load Testing: expected traffic patterns
- Stress Testing: breaking point identification
- Benchmark Suite: track regressions
- Profiling: identify bottlenecks

## Observability
**When:** SLA level selected

### Monitoring Basics
- Health Checks: /health endpoint
- Error Tracking: Sentry or equivalent
- Basic Alerting: critical failures only

### Observability Standard
- Structured Logging: JSON, correlation IDs
- Metrics: RED method (Rate, Errors, Duration)
- Distributed Tracing: request flow visibility
- Alerting: tiered severity levels

### High Availability
- Redundancy: no single points of failure
- Failover: automatic recovery
- Health Probes: liveness + readiness
- Circuit Breakers: prevent cascade failures
- Load Balancing: distribute traffic
- Auto-scaling: respond to demand
- Backup Strategy: RPO/RTO defined
- Incident Response: runbooks documented

### Full Resilience
- Multi-region: geographic redundancy
- Chaos Engineering: regular failure injection
- Disaster Recovery: tested DR plans
- Global Load Balancing: anycast, GeoDNS
- Data Replication: synchronous/async based on requirements
- Zero Downtime Deploys: blue/green, canary
- Capacity Planning: proactive scaling
- SLO/SLI Tracking: error budgets
- Post-mortem Culture: blameless analysis
- On-call Rotation: defined escalation
- Status Page: public incident communication
- Dependency Mapping: understand blast radius
<!-- CCO_CONDITIONALS_END -->
