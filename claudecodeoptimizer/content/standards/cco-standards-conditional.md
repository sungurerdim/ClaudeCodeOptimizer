<!-- CCO_CONDITIONALS_START -->
# Project-Specific Standards
*Selected by /cco-tune based on project detection*
*Written to local ./CLAUDE.md, filtered by triggers*
*AGENTS.md compatible - selected standards are exported*

## Security Enhanced
**When:** Data: PII/Regulated OR Scale: 10K+
- Input Validation: Pydantic (Python), Zod (JS/TS), JSON Schema
- SQL Safety: parameterized queries, ORM safe methods
- XSS Prevention: sanitize output, CSP headers
- Auth: OAuth2/OIDC + RBAC, verify every request
- Rate Limit: all endpoints, per-user/IP with headers
- Encryption: AES-256 for sensitive data at rest
- Audit Log: security events, immutable, queryable
- CORS: explicit origins, no wildcard in production

## Architecture
**When:** Scale: 10K+ OR Type: microservices
- Circuit Breaker: fail fast on unhealthy downstream
- Idempotency: safe to retry without side effects
- API Versioning: explicit versions, backward compatible
- DI: inject dependencies, enable testing
- Event-Driven: async communication between services
- Bounded Contexts: own models/rules per domain

## Operations
**When:** CI/CD detected
- Config as Code: versioned, validated, env-aware
- Health Endpoints: /health + /ready
- Graceful Shutdown: drain connections on SIGTERM
- Observability: metrics, logs, traces (OpenTelemetry)
- CI Gates: lint + test + coverage before merge
- Blue/Green or Canary: zero-downtime deployments
- Feature Flags: decouple deploy from release

## Performance
**When:** Scale: 100+
- Caching: TTL, invalidation strategy, cache-aside pattern
- Async I/O: no blocking in async context
- Connection Pool: reuse connections, appropriate sizing
- Lazy Load: defer non-critical resources
- Compression: gzip/brotli for responses
- Indexing: proper indexes, query optimization

## Data
**When:** DB detected
- Backup: automated, tested restore, defined RPO/RTO
- Migrations: versioned, backward compatible, rollback
- N+1 Prevention: batch queries, eager loading
- Retention: defined periods, auto-cleanup
- Transactions: ACID where needed, eventual consistency where acceptable

## API
**When:** REST/GraphQL/gRPC detected
- REST: proper methods, status codes, resource naming
- Pagination: cursor-based for large datasets
- OpenAPI/AsyncAPI: spec with examples, synced with code
- Errors: consistent format, no stack traces in prod
- GraphQL: complexity limits, depth limits, persisted queries
- gRPC: proto versioning, backward compatibility

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

## Mobile
**When:** iOS/Android/React Native/Flutter detected
- Offline-First: local storage, sync when connected
- Battery Efficiency: minimize background work, batch operations
- Deep Linking: universal links, app links
- Push Notifications: permission handling, payload optimization
- Platform Guidelines: iOS HIG, Material Design compliance
- App Size: asset optimization, on-demand resources

## Desktop
**When:** Electron/Tauri/native desktop detected
- Auto-Update: secure update mechanism
- Native Integration: OS notifications, file associations
- Multi-Window: proper window management
- Memory Management: prevent memory leaks, proper cleanup

## CLI
**When:** CLI tool detected
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

## ML/AI Projects
**When:** ML/AI stack detected (PyTorch, TensorFlow, scikit-learn, etc.)
- Reproducibility: seed everything, version data + code + model
- Experiment Tracking: log hyperparameters, metrics, artifacts
- Data Versioning: DVC or similar for dataset management
- Model Registry: versioned models with metadata
- Inference Optimization: quantization, batching, caching
- Bias Monitoring: fairness metrics, drift detection

## Game Development
**When:** Game engine detected (Unity, Unreal, Godot, etc.)
- Frame Budget: 16ms for 60fps, profile regularly
- Asset Pipeline: LOD, compression, streaming
- Input Handling: responsive, rebindable controls
- Save System: versioned saves, corruption recovery

## Serverless
**When:** Lambda/Functions/Cloud Functions detected
- Cold Start: minimize bundle size, lazy init
- Timeout Handling: graceful timeout, cleanup
- Stateless: no local state between invocations
- Cost Optimization: right-size memory, avoid over-provisioning

## Monorepo
**When:** Monorepo detected (nx, turborepo, lerna, pnpm workspaces)
- Workspace Management: clear package boundaries
- Selective Testing: only test affected packages
- Shared Dependencies: consistent versions, hoisting
- Build Caching: incremental builds, remote cache

## Container/K8s
**When:** Docker/Kubernetes detected
- Image Size: multi-stage builds, distroless base
- Security: non-root user, CVE scanning (Trivy)
- Resource Limits: CPU/memory limits and requests
- Pod Security: SecurityContext, NetworkPolicy
- Secrets: external secrets, not in images

## Team Collaboration
**When:** Team: 2+
- ADR: decisions + context + consequences
- Local Parity: match production environment
- Golden Paths: recommended approaches documented
- Code Owners: CODEOWNERS for review assignment
- Onboarding: documented setup, first-task guides
- Branch Protection: require reviews, status checks
- PR Templates: consistent PR descriptions
- Atomic Commits: one logical change per commit

## Compliance
**When:** Compliance != None (SOC2, HIPAA, PCI-DSS, GDPR)
- License: track deps, no GPL without review
- Frameworks: implement required controls
- Data Classification: by sensitivity level
- Retention Policy: documented, enforced

## i18n
**When:** Multi-language requirement detected
- Externalized: no hardcoded user text
- Unicode: UTF-8 everywhere
- RTL: support Arabic, Hebrew layouts
- Locale: date/time/number/currency formatting
- Pluralization: proper rules per language
<!-- CCO_CONDITIONALS_END -->
