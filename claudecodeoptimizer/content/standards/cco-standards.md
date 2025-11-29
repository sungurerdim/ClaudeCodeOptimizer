<!-- CCO_STANDARDS_START -->
## Core
- Paths: forward slash (/), relative, quote spaces
- Reference Integrity: find ALL refs → update in order → verify (grep old=0, new=expected)
- Verification: total = done + skip + fail + cannot_do, no "fixed" without Read proof

## Approval Flow (all commands)
- Single call, 4 tabs: one AskUserQuestion with 4 questions max (Critical/High/Medium/Low)
- Each priority = one tab: user sees all levels at once, selects per-tab
- Header format: "{Priority} ({count})" - e.g., "Critical (2)", "High (5)"
- Options per tab (max 4):
  - Option 1: "All ({N})" - always first, includes all items in this priority
  - Options 2-4: top 3 individual items by impact, format: "{desc} [{loc}] [{risk}]"
  - If >3 items: remaining are included in "All" (count shows total)
- Risk labels: [safe], [risky], or [extensive] per item
- MultiSelect: true - "All" + individual items can be combined
- Skip empty tabs: don't show priority levels with 0 items
- Summary before apply: "Applying {selected}/{total} items"
- No silent skipping: ALL items accessible via "All ({N})" option
- Apply all selected: user selection = commitment, fix everything chosen
- Blocked items: report as "cannot_do" with reason after attempt

## Code Quality
- Fail-Fast: immediate visible failure, no silent fallbacks
- DRY: single source of truth, zero duplicates
- No Orphans: every function called, every import used
- Type Safety: annotations + strict static analysis (mypy/pyright)
- Complexity: cyclomatic <10 per function
- Tech Debt: ratio <5%, track via SonarQube
- Maintainability: index >65
- Linting: ruff/eslint + SAST (Semgrep/CodeQL)
- Evidence-Based: command output + exit code proof
- No Overengineering: minimum for current task, no hypotheticals
- Clean Code: meaningful names, single responsibility
- Code Review: standardized checklist
- Immutability: prefer immutable, mutate only for performance
- Profile First: measure before optimize
- Version: single source, SemVer (MAJOR.MINOR.PATCH)

## Security
- Input Validation: Pydantic/Joi/Zod at all entry points
- Privacy-First: PII managed, cleaned from memory, GDPR/CCPA
- Encryption: AES-256-GCM for data at rest
- Zero Disk: sensitive data in RAM only
- Auth: OAuth2 + RBAC + mTLS, verify every request (Zero Trust)
- SQL: parameterized queries only
- Secrets: Vault/AWS, rotate 30-90 days, never hardcode
- Rate Limit: all endpoints, per-user/IP, return headers
- XSS: sanitize all user input
- Supply Chain: SBOM, Sigstore signing, lockfiles
- AI Security: validate prompts/outputs, prevent injection
- Container: distroless, non-root, CVE scan (Trivy)
- K8s: RBAC least privilege, NetworkPolicy, PodSecurity
- Policy-as-Code: OPA/Sentinel
- CORS: configure allowed origins/methods
- Audit Log: all security events, immutable
- OWASP: API Top 10 compliance
- Dependencies: Dependabot, scan in CI
- Incident Response: IR plan, SIEM, DR tested

## AI-Assisted (2025)
- Review AI Code: treat as junior output, verify
- Workflow: Plan → Act → Review → Repeat
- Test AI Output: unit tests before integration
- Decompose: break complex tasks for AI
- No Vibe Coding: avoid rare langs/new frameworks
- Context Files: CLAUDE.md, plan.md, arch docs
- Human-AI: humans architect, AI implements, humans review
- Challenge: "are you sure?" for perfect-looking solutions
- No Example Fixation: use placeholders, avoid anchoring bias from hardcoded examples

## Architecture
- Event-Driven: async patterns, communicate via events
- Service Mesh: Istio/Linkerd for mTLS, observability
- Separation: one aspect per module/class
- DI: inject dependencies, enable testing
- Dependency Rule: inward only toward business logic
- Circuit Breaker: fail fast on unhealthy downstream
- Bounded Contexts: DDD, own models/rules per context
- API Versioning: explicit versions, backward compatible
- Idempotency: safe to retry without side effects
- Event Sourcing: state as event sequence

## Operations
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

## Testing
- Coverage: 80% min, 100% critical paths
- Integration: e2e for critical workflows
- CI Gates: lint + test + coverage + security before merge
- Isolation: no dependencies between tests
- TDD: tests first, code satisfies
- Contract: verify API contracts between services

## Performance
- DB: indexing, N+1 prevention, explain plans
- Async I/O: no blocking in async context
- Caching: cache-aside/write-through, TTL, invalidation
- Cache Hit: >80% target
- Connection Pool: reuse, size based on load
- Lazy Load: defer until needed
- Compression: gzip/brotli responses

## Data
- Backup: automated, defined RPO/RTO, tested restore
- Migrations: versioned, backward compatible, rollback
- Retention: defined periods, auto-cleanup

## API
- REST: proper methods, status codes, resource naming
- Pagination: cursor-based for large datasets
- Docs: OpenAPI spec, examples, synced with code
- Errors: consistent format, no stack traces in prod
- GraphQL: complexity limits, depth limits, persisted queries

## Accessibility
- WCAG 2.2 AA: perceivable, operable, understandable, robust
- Semantic HTML: native elements (button, nav, form)
- ARIA: only when HTML insufficient
- Keyboard: all interactive elements accessible
- Screen Reader: alt text, heading hierarchy, labels
- Contrast: 4.5:1 normal, 3:1 large text
- Focus: logical order, trap in modals

## i18n
- Externalized: no hardcoded user text
- Unicode: UTF-8 everywhere
- RTL: support Arabic, Hebrew
- Locale: date/time/number formatting
- Pluralization: proper rules per language

## Reliability
- Chaos: inject failures in production
- Resilience: validate failure scenarios
- Timeouts: explicit for all external calls
- Retry: exponential backoff + jitter
- Bulkhead: isolate failures
- Fallback: graceful degradation

## Cost
- FinOps: monitor, right-size, spot instances
- Tagging: all cloud resources
- Auto-Scale: scale to zero when idle
- Green: energy-efficient, carbon-aware

## Docs
- README: description, setup, usage, contributing
- API Docs: complete, accurate, auto-generated
- ADR: decisions + context + consequences
- Comments: why not what
- Runbooks: ops procedures

## DX
- Local Parity: match production
- Fast Feedback: quick builds, fast tests
- Self-Service: provision without tickets
- Golden Paths: recommended approaches

## Compliance
- License: track deps, no GPL without review
- Frameworks: SOC2/HIPAA/PCI-DSS as applicable
- Classification: data by sensitivity
<!-- CCO_STANDARDS_END -->
