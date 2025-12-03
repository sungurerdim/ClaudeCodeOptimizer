<!-- CCO_CONDITIONALS_START -->
# Conditional Standards
*Domain-specific standards - selected by /cco-tune based on project detection*
*These are written to local ./CLAUDE.md, NOT global ~/.claude/CLAUDE.md*

## Security Implementation
**When:** Based on detected stack (implements Universal Security principles)
- Input Validation: Pydantic (Python), Zod/Joi (JS/TS), JSON Schema (API)
- SQL Injection: parameterized queries, ORM safe methods
- XSS Prevention: sanitize output, CSP headers, template escaping
- OWASP API: Top 10 compliance checklist

## Security Extended
**When:** Container/K8s detected OR Scale: 10K+ OR Data: PII/Regulated
- Privacy-First: PII managed, cleaned from memory, GDPR/CCPA
- Encryption: AES-256-GCM for data at rest
- Zero Disk: sensitive data in RAM only
- Auth: OAuth2 + RBAC + mTLS, verify every request (Zero Trust)
- Rate Limit: all endpoints, per-user/IP, return headers
- Supply Chain: SBOM, SLSA L2+, Sigstore signing, lockfiles
- AI Security: validate prompts/outputs, prevent injection
- Container: distroless, non-root, CVE scan (Trivy)
- K8s: RBAC least privilege, NetworkPolicy, PodSecurity
- Policy-as-Code: OPA/Sentinel
- Audit Log: all security events, immutable
- Incident Response: IR plan, SIEM, DR tested

## Architecture
**When:** Scale: 10K+ OR Type: backend-api with microservices
- Event-Driven: async patterns, communicate via events
- Service Mesh: Istio/Linkerd for mTLS, observability
- DI: inject dependencies, enable testing
- Dependency Rule: inward only toward business logic
- Circuit Breaker: fail fast on unhealthy downstream
- Bounded Contexts: DDD, own models/rules per context
- API Versioning: explicit versions, backward compatible
- Idempotency: safe to retry without side effects
- Event Sourcing: state as event sequence

## Operations
**When:** Scale: 10K+ OR CI/CD detected
- Zero Maintenance: auto-manage lifecycle
- Config as Code: versioned, validated, env-aware
- IaC + GitOps: Terraform/Pulumi + ArgoCD/Flux
- Observability: OpenTelemetry (metrics, traces, logs)
- Health: /health + /ready endpoints
- Graceful Shutdown: SIGTERM → drain → close
- Blue/Green: zero downtime, instant rollback
- Canary: progressive rollout, auto-rollback on errors
- Feature Flags: decouple deploy from release
- Incremental Safety: stash → change → test → rollback on fail

## Performance
**When:** Scale: 100-10K+ OR Performance applicable
- DB: indexing, N+1 prevention, explain plans
- Async I/O: no blocking in async context
- Caching: cache-aside/write-through, TTL, invalidation
- Cache Hit: >80% target
- Connection Pool: reuse, size based on load
- Lazy Load: defer non-critical resources until needed
- Compression: gzip/brotli responses

## Data
**When:** DB detected
- Backup: automated, defined RPO/RTO, tested restore
- Migrations: versioned, backward compatible, rollback
- Retention: defined periods, auto-cleanup

## API
**When:** API detected (REST/GraphQL endpoints)
- REST: proper methods, status codes, resource naming
- Pagination: cursor-based for large datasets
- OpenAPI: spec with examples, synced with code
- Errors: consistent format, no stack traces in prod
- GraphQL: complexity limits, depth limits, persisted queries
- Contract: verify API contracts between services
- CORS: allowed origins/methods, credentials handling

## Frontend
**When:** Frontend detected

### AI Generation Quality
Avoid AI slop - create distinctive designs:
- Typography: unique fonts; avoid Arial, Inter, Roboto, system defaults
- Color: CSS variables; dominant colors with sharp accents
- Motion: high-impact moments; orchestrated page load with staggered reveals
- Backgrounds: atmosphere and depth; avoid solid color defaults
- Avoid: purple gradients, predictable layouts, generic AI patterns

### Accessibility
- WCAG 2.2 AA: perceivable, operable, understandable, robust
- Semantic HTML: native elements (button, nav, form)
- ARIA: only when HTML insufficient
- Keyboard: all interactive elements accessible
- Screen Reader: alt text, heading hierarchy, labels
- Contrast: 4.5:1 normal, 3:1 large text
- Focus: logical order, trap in modals
- A11y Testing: axe-core/pa11y in CI, zero critical violations

### Performance
- Core Web Vitals: LCP, FID, CLS targets
- Bundle Size: code splitting, tree shaking

## i18n
**When:** i18n detected OR multi-language requirement
- Externalized: no hardcoded user text
- Unicode: UTF-8 everywhere
- RTL: support Arabic, Hebrew
- Locale: date/time/number formatting
- Pluralization: proper rules per language

## Reliability
**When:** Scale: 10K+ OR Type: backend-api with SLA
- Chaos: inject failures in production
- Resilience: validate failure scenarios
- Bulkhead: isolate failures
- Fallback: graceful degradation

## Cost
**When:** Cloud/Container detected
- FinOps: monitor, right-size, spot instances
- Tagging: all cloud resources
- Auto-Scale: scale to zero when idle
- Green: energy-efficient, carbon-aware

## DX
**When:** Team: 2-5+
- Local Parity: match production
- Build Speed: quick builds, fast tests
- Self-Service: provision without tickets
- Golden Paths: recommended approaches
- Runbooks: ops procedures

## Compliance
**When:** Compliance: not None
- License: track deps, no GPL without review
- Frameworks: SOC2/HIPAA/PCI-DSS as applicable
- Classification: data by sensitivity
<!-- CCO_CONDITIONALS_END -->
