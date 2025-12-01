<!-- CCO_STANDARDS_START -->
## Workflow

### Pre-Operation Safety
1. Check `git status` for uncommitted changes
2. If dirty: AskUserQuestion → Commit (cco-commit) / Stash / Continue
3. Clean state enables safe rollback

### Context Read
1. Read `CCO_CONTEXT_START` from `./CLAUDE.md` (NOT `.claude/`)
2. If missing → suggest `/cco-tune`
3. Apply: Guidelines, Thresholds, AI Performance, Applicable checks

### Safety Classification
| Safe (auto-apply) | Risky (require approval) |
|-------------------|--------------------------|
| Remove unused imports | Auth/CSRF changes |
| Parameterize SQL | DB schema changes |
| Move secrets to env | API contract changes |
| Fix linting issues | Delete files |
| Add type annotations | Rename public APIs |

## Core
- Paths: forward slash (/), relative, quote spaces
- Reference Integrity: find ALL refs → update in order → verify (grep old=0, new=expected)
- Verification: total = done + skip + fail + cannot_do, no "fixed" without Read proof
- Error Format: `❌ {What} → ↳ {Why} → → {Fix}` (consistent across all commands)

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

## AI-Assisted (2025)
- Review AI Code: treat as junior output, verify
- Workflow: Plan → Act → Review → Repeat
- Test AI Output: unit tests before integration
- Decompose: break complex tasks for AI
- No Vibe Coding: avoid rare langs/new frameworks
- Human-AI: humans architect, AI implements, humans review
- Challenge: "are you sure?" for perfect-looking solutions
- No Example Fixation: use placeholders, avoid anchoring bias from hardcoded examples

## Context Management
- Thinking Budget: match to complexity (off → simple, 8K → medium, 32K+ → complex)
- MCP Limits: 25K default, increase for large tool responses
- Compact Focus: use /compact with instructions for what to preserve/discard
- Session Hygiene: /clear between unrelated tasks, /context to monitor
- Context Files: CLAUDE.md (project), plan.md (task), arch docs (reference)

## Quality (always apply, thresholds from context)

### Code Quality
- Fail-Fast: immediate visible failure, no silent fallbacks
- DRY: single source of truth, zero duplicates
- No Orphans: every function called, every import used
- Type Safety: annotations + strict static analysis
- Complexity: cyclomatic <10 per function (context may override)
- Tech Debt: ratio <5%
- Maintainability: index >65
- Evidence-Based: command output + exit code proof
- No Overengineering: minimum for current task, no hypotheticals
- Clean Code: meaningful names, single responsibility
- Immutability: prefer immutable, mutate only for performance
- Profile First: measure before optimize
- Version: single source, SemVer (MAJOR.MINOR.PATCH)

### Testing
- Coverage: 80% min (context may adjust: solo 60%, enterprise 90%)
- Integration: e2e for critical workflows
- CI Gates: lint + test + coverage + security before merge
- Isolation: no dependencies between tests
- TDD: tests first, code satisfies

### Security Core (always apply)
- Input Validation: Pydantic/Joi/Zod at all entry points
- SQL: parameterized queries only
- Secrets: never hardcode, use env vars or vault
- XSS: sanitize all user input
- OWASP: API Top 10 compliance
- Dependencies: Dependabot, scan in CI

## Docs
- README: description, setup, usage, contributing
- API Docs: complete, accurate, auto-generated
- ADR: decisions + context + consequences
- Comments: why not what

## Conditional (apply when applicable)

### Security Extended
**When:** Container/K8s detected OR Scale: 10K+ OR Data: PII/Regulated
- Privacy-First: PII managed, cleaned from memory, GDPR/CCPA
- Encryption: AES-256-GCM for data at rest
- Zero Disk: sensitive data in RAM only
- Auth: OAuth2 + RBAC + mTLS, verify every request (Zero Trust)
- Rate Limit: all endpoints, per-user/IP, return headers
- Supply Chain: SBOM, Sigstore signing, lockfiles
- AI Security: validate prompts/outputs, prevent injection
- Container: distroless, non-root, CVE scan (Trivy)
- K8s: RBAC least privilege, NetworkPolicy, PodSecurity
- Policy-as-Code: OPA/Sentinel
- Audit Log: all security events, immutable
- Incident Response: IR plan, SIEM, DR tested

### Architecture
**When:** Scale: 10K+ OR Type: backend-api with microservices
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

### Operations
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

### Performance
**When:** Scale: 100-10K+ OR Performance applicable
- DB: indexing, N+1 prevention, explain plans
- Async I/O: no blocking in async context
- Caching: cache-aside/write-through, TTL, invalidation
- Cache Hit: >80% target
- Connection Pool: reuse, size based on load
- Lazy Load: defer until needed
- Compression: gzip/brotli responses

### Data
**When:** DB detected
- Backup: automated, defined RPO/RTO, tested restore
- Migrations: versioned, backward compatible, rollback
- Retention: defined periods, auto-cleanup

### API
**When:** API detected (REST/GraphQL endpoints)
- REST: proper methods, status codes, resource naming
- Pagination: cursor-based for large datasets
- Docs: OpenAPI spec, examples, synced with code
- Errors: consistent format, no stack traces in prod
- GraphQL: complexity limits, depth limits, persisted queries
- Contract: verify API contracts between services

### Frontend
**When:** Frontend detected
- WCAG 2.2 AA: perceivable, operable, understandable, robust
- Semantic HTML: native elements (button, nav, form)
- ARIA: only when HTML insufficient
- Keyboard: all interactive elements accessible
- Screen Reader: alt text, heading hierarchy, labels
- Contrast: 4.5:1 normal, 3:1 large text
- Focus: logical order, trap in modals

### i18n
**When:** i18n detected OR multi-language requirement
- Externalized: no hardcoded user text
- Unicode: UTF-8 everywhere
- RTL: support Arabic, Hebrew
- Locale: date/time/number formatting
- Pluralization: proper rules per language

### Reliability
**When:** Scale: 10K+ OR Type: backend-api with SLA
- Chaos: inject failures in production
- Resilience: validate failure scenarios
- Timeouts: explicit for all external calls
- Retry: exponential backoff + jitter
- Bulkhead: isolate failures
- Fallback: graceful degradation

### Cost
**When:** Cloud/Container detected
- FinOps: monitor, right-size, spot instances
- Tagging: all cloud resources
- Auto-Scale: scale to zero when idle
- Green: energy-efficient, carbon-aware

### DX
**When:** Team: 2-5+
- Local Parity: match production
- Fast Feedback: quick builds, fast tests
- Self-Service: provision without tickets
- Golden Paths: recommended approaches
- Runbooks: ops procedures

### Compliance
**When:** Compliance: not None
- License: track deps, no GPL without review
- Frameworks: SOC2/HIPAA/PCI-DSS as applicable
- Classification: data by sensitivity
- CORS: configure allowed origins/methods
<!-- CCO_STANDARDS_END -->
