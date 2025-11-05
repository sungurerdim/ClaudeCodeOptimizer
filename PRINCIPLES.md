# Development Principles for ClaudeCodeOptimizer

**Generated:** 2025-11-07 15:14:32
**Applicable Principles:** 33/70
**Coverage:** 47.1%

---

## Your Configuration

- **Team Size:** solo
- **Code Quality:** strict
- **Security Stance:** balanced
- **Test Coverage Target:** 90
- **Compliance:** none

---

## Statistics

- **Critical:** 13 principles
- **High:** 20 principles
- **Medium:** 0 principles
- **Low:** 0 principles

---

## CRITICAL Principles ⚠️

### P001: Fail-Fast Error Handling

**Enforcement:** SHOULD - Requires justification
**Category:** Code Quality

Errors must cause immediate, visible failure. No silent fallbacks, no swallowed exceptions.

**Check Patterns:**
- No bare except: clauses (python)
  - Pattern: `except:\\s*$`
- No empty catch blocks (javascript, typescript, java)
  - Pattern: `catch\\s*\\([^)]*\\)\\s*\\{\\s*\\}`

**❌ Bad Example:**
```
try:\n    result = risky()\nexcept:\n    pass
```

**✅ Good Example:**
```
try:\n    result = risky()\nexcept SpecificError as e:\n    logger.error(f'Failed: {e}')\n    raise
```

---

### P005: Schema-First Validation

**Enforcement:** SHOULD - Requires justification
**Category:** Security Privacy

Use schema-based validation (Pydantic/Joi) for all external inputs.

**Check Patterns:**
- Validate data at API entry points (python)
  - Pattern: `@app\\.(post|put|patch).*\\ndef\\s+\\w+\\([^)]*\\)\\s*:(?!.*validate)`

**❌ Bad Example:**
```
@app.post('/api')\ndef create(data: dict):  # No validation!
```

**✅ Good Example:**
```
@app.post('/api')\ndef create(data: ResourceSchema):  # Validated
```

---

### P011: Event-Driven Architecture

**Enforcement:** SHOULD - Requires justification
**Category:** Architecture

Use async, event-driven patterns for scalability - communicate via events.

**Check Patterns:**
- No blocking calls in async functions (python)
  - Pattern: `async def.*\n.*time\.sleep|requests\.get`

**❌ Bad Example:**
```
@app.post('/api')\ndef create(data):\n    result = blocking_call()  # Blocks!
```

**✅ Good Example:**
```
@app.post('/api')\nasync def create(data):\n    queue.enqueue(process_job, data)  # Non-blocking
```

---

### P019: Privacy-First by Default

**Enforcement:** SHOULD - Requires justification
**Category:** Security Privacy

PII explicitly managed, cleaned from memory after use.

**Check Patterns:**
- PII variables must have cleanup (python)
  - Pattern: `audio_data|patient_record(?!.*secure_zero|.*del.*gc)`

**❌ Bad Example:**
```
data = load_pii()\nprocess(data)  # Lingers in memory!
```

**✅ Good Example:**
```
data = load_pii()\ntry:\n    process(data)\nfinally:\n    secure_zero(data)
```

---

### P021: Encryption Everywhere

**Enforcement:** SHOULD - Requires justification
**Category:** Security Privacy

All sensitive data at rest MUST be encrypted (AES-256-GCM).

**Check Patterns:**
- No plaintext in cache (python)
  - Pattern: `redis\.set(?!.*encrypt)`

**❌ Bad Example:**
```
redis.set('sensitive', data)  # Plaintext!
```

**✅ Good Example:**
```
redis.set('sensitive', encrypt_aes_gcm(data))
```

---

### P022: Zero Disk Touch

**Enforcement:** SHOULD - Requires justification
**Category:** Security Privacy

Sensitive data never touches filesystem - RAM and secure storage only.

**Check Patterns:**
- No temp files for sensitive data (python)
  - Pattern: `NamedTemporaryFile|mktemp|/tmp/`

**❌ Bad Example:**
```
with open('/tmp/audio.wav', 'wb') as f:  # Disk touch!
```

**✅ Good Example:**
```
process = subprocess.Popen(['ffmpeg', '-i', 'pipe:0'], stdin=PIPE)  # In-memory
```

---

### P024: Authentication & Authorization

**Enforcement:** SHOULD - Requires justification
**Category:** Security Privacy

OAuth2 + RBAC, verify permissions on every request.

**❌ Bad Example:**
```
@app.get('/admin')\ndef admin():  # No auth check!
```

**✅ Good Example:**
```
@app.get('/admin')\n@require_role('admin')\ndef admin():
```

---

### P025: SQL Injection Prevention

**Enforcement:** SHOULD - Requires justification
**Category:** Security Privacy

Always use parameterized queries, never string concatenation.

**Check Patterns:**
- No string concatenation in SQL (python)
  - Pattern: `execute\\(.*f['\"]|execute\\(.*\\+`

**❌ Bad Example:**
```
cursor.execute(f'SELECT * FROM users WHERE id={user_id}')  # SQL injection!
```

**✅ Good Example:**
```
cursor.execute('SELECT * FROM users WHERE id=%s', (user_id,))  # Parameterized
```

---

### P026: Secret Management with Rotation

**Enforcement:** SHOULD - Requires justification
**Category:** Security Privacy

Use secret managers (Vault, AWS/Azure/GCP), never hardcode. Implement rotation policies and audit logging.

**Check Patterns:**
- No hardcoded API keys/passwords/tokens (all)
  - Pattern: `api_key.*=.*['\"][a-zA-Z0-9]{20,}|password.*=.*['\"]`
- Use secret manager (Vault, AWS Secrets Manager, etc.) (all)
  - Pattern: `vault|secretmanager|keyvault|sealed.?secret`
- Implement secret rotation (30-90 days) (all)
  - Pattern: `rotate|rotation.?policy`

**❌ Bad Example:**
```
# Hardcoded secret (CRITICAL violation)
```

**✅ Good Example:**
```
# HashiCorp Vault
```

---

### P029: Input Sanitization (XSS Prevention)

**Enforcement:** SHOULD - Requires justification
**Category:** Security Privacy

Escape/sanitize all user input before rendering.

**❌ Bad Example:**
```
innerHTML = user_input  # XSS!
```

**✅ Good Example:**
```
textContent = user_input  # Safe
```

---

### P054: Supply Chain Security

**Enforcement:** SHOULD - Requires justification
**Category:** Security Privacy

Verify software supply chain integrity through SBOM, provenance, and attestations

**Check Patterns:**
- Generate SBOM for all releases (all)
  - Pattern: `sbom|cyclonedx|spdx`
- Sign artifacts with Sigstore/cosign (all)
  - Pattern: `cosign|sigstore`
- Use dependency lockfiles (python, javascript, rust, go)
  - Pattern: `requirements\.txt\.lock|package-lock\.json|Cargo\.lock|go\.sum`

**❌ Bad Example:**
```
# No SBOM, unsigned artifacts, no lockfiles
```

**✅ Good Example:**
```
# Generate SBOM: cyclonedx-py\n# Sign: cosign sign image\n# Use: requirements.txt.lock
```

---

### P055: AI/ML Security

**Enforcement:** SHOULD - Requires justification
**Category:** Security Privacy

Protect AI/ML systems from prompt injection, model poisoning, and data leakage

**Check Patterns:**
- Validate and sanitize prompts (python)
  - Pattern: `(?!.*sanitize.*prompt|.*validate.*input)`
- Sanitize model outputs (python)
  - Pattern: `(?!.*sanitize.*output)`
- Sign and verify models (python)
  - Pattern: `model\.save|torch\.save(?!.*sign|.*verify)`

**❌ Bad Example:**
```
# Direct prompt to LLM\nresponse = llm(user_input)  # No validation!
```

**✅ Good Example:**
```
# Validate input\nif not is_safe_prompt(user_input):\n    raise ValueError\nresponse = llm(user_input)
```

---

### P067: Evidence-Based Verification

**Enforcement:** SHOULD - Requires justification
**Category:** Code Quality

Never claim completion without command execution proof. All verification requires fresh command output with exit codes

**Check Patterns:**
- Completion claims must include command output (all)
  - Pattern: `\[Runs.*\].*\[Shows:.*\]`
- Avoid uncertainty language (all)
  - Pattern: `(?!.*should work|looks correct|appears to|seems like)`

**❌ Bad Example:**
```
"Tests should pass now"\n"Build looks correct"\n"Appears to be working"
```

**✅ Good Example:**
```
[Runs: pytest]\n[Output: 34/34 passed]\n[Exit code: 0]\n"All tests pass"\n\n[Runs: npm run build]\n[Output: Build successful in 2.3s]\n[Exit code: 0]\n"Build succeeds"
```

---

## HIGH PRIORITY Principles 🔴

### P002: DRY Enforcement

**Enforcement:** SHOULD - Requires justification
**Category:** Code Quality

Single source of truth for all data, logic, configuration. Zero duplicate definitions.

**Check Patterns:**
- No duplicate function definitions (python)
  - Pattern: `def\\s+(\\w+).*:\\s*\\n.*def\\s+\\1`
- No magic numbers except 0, 1, -1 (all)
  - Pattern: `(?<![\\w\\.])([2-9]|[1-9]\\d+)(?![\\w\\.])`

**❌ Bad Example:**
```
MAX_RETRIES = 3  # file1\nMAX_RETRIES = 3  # file2 - duplicate!
```

**✅ Good Example:**
```
# shared/constants.py\nMAX_RETRIES = 3\n\n# Other files\nfrom shared.constants import MAX_RETRIES
```

---

### P003: Complete Integration Check

**Enforcement:** SHOULD - Requires justification
**Category:** Code Quality

Zero orphaned code. Every function called, every import used, every file referenced.

**Check Patterns:**
- No unused imports (python, javascript, typescript)
  - Pattern: `import\\s+(\\w+)(?!.*\\1)`

**❌ Bad Example:**
```
import unused_module  # Never referenced
```

**✅ Good Example:**
```
from utils import used_func\nresult = used_func()
```

---

### P009: Linting & SAST Enforcement

**Enforcement:** SHOULD - Requires justification
**Category:** Code Quality

Use linters (ruff/eslint) AND SAST tools (Semgrep/CodeQL/Snyk) with strict rules, enforce in CI.

**Check Patterns:**
- Project has linter configuration (all)
  - Pattern: `pyproject.toml|.pylintrc|.eslintrc|.ruff.toml`
- Use SAST tools (Semgrep, CodeQL, Snyk Code) (all)
  - Pattern: `semgrep|codeql|snyk.?code|sonarqube`
- Linting + SAST enforced in CI pipeline (all)
  - Pattern: `ci|github.?actions|gitlab.?ci|jenkins`

**❌ Bad Example:**
```
# No linter config, no SAST
```

**✅ Good Example:**
```
# pyproject.toml - Linting with security
```

---

### P014: Microservices with Service Mesh

**Enforcement:** SHOULD - Requires justification
**Category:** Architecture

Use Service Mesh (Istio/Linkerd) for mTLS, traffic management, observability. API Gateway + Event Bus for communication.

**Check Patterns:**
- Use service mesh for 3+ services (Istio, Linkerd, Consul) (all)
  - Pattern: `istio|linkerd|consul.?connect|service.?mesh`
- Enable mTLS between services (all)
  - Pattern: `mtls|mutual.?tls|peerAuthentication`
- Use API Gateway for external access (all)
  - Pattern: `gateway|ingress|kong|ambassador`

**❌ Bad Example:**
```
# Direct service-to-service HTTP calls (no mTLS, no retries)
```

**✅ Good Example:**
```
# Istio Service Mesh - mTLS + observability
```

---

### P023: Type Safety & Static Analysis

**Enforcement:** SHOULD - Requires justification
**Category:** Code Quality

All code MUST have type annotations, pass mypy/pyright strict mode.

**Check Patterns:**
- Functions without type hints (python)
  - Pattern: `^def .*\\([^)]*\\)\\s*:(?!.*->)`

**❌ Bad Example:**
```
def calculate(x, y):  # No types!
```

**✅ Good Example:**
```
def calculate(x: int, y: int) -> int:
```

---

### P027: Rate Limiting & Throttling

**Enforcement:** SHOULD - Requires justification
**Category:** Security Privacy

Prevent abuse with rate limiting on all public endpoints.

**❌ Bad Example:**
```
@app.post('/api')  # No rate limiting
```

**✅ Good Example:**
```
@limiter.limit('100/minute')\n@app.post('/api')
```

---

### P030: Audit Logging

**Enforcement:** SHOULD - Requires justification
**Category:** Security Privacy

Log all security events (auth, access, changes) for audit trail.

**❌ Bad Example:**
```
# No logging for sensitive operations
```

**✅ Good Example:**
```
audit_logger.info('User {user_id} accessed resource {resource_id}')
```

---

### P037: Test Coverage Targets

**Enforcement:** SHOULD - Requires justification
**Category:** Testing

Minimum 80% line coverage, 100% for critical paths.

**❌ Bad Example:**
```
# 30% coverage
```

**✅ Good Example:**
```
# pytest-cov shows 85% coverage
```

---

### P039: Integration Tests for Critical Paths

**Enforcement:** SHOULD - Requires justification
**Category:** Testing

Test service-to-service workflows end-to-end.

**❌ Bad Example:**
```
# Only unit tests, no integration
```

**✅ Good Example:**
```
def test_job_workflow():\n    # POST /jobs -> Queue -> Worker -> Result
```

---

### P041: CI Gates

**Enforcement:** SHOULD - Requires justification
**Category:** Testing

All PRs must pass CI (lint, test, coverage) before merge.

**❌ Bad Example:**
```
# No CI, manual testing
```

**✅ Good Example:**
```
# GitHub Actions: lint -> test -> coverage check
```

---

### P049: Database Query Optimization

**Enforcement:** SHOULD - Requires justification
**Category:** Performance

Proper indexing, N+1 prevention, query analysis.

**❌ Bad Example:**
```
SELECT * FROM large_table  # No index, full scan
```

**✅ Good Example:**
```
CREATE INDEX idx_user_id ON jobs(user_id)  # Indexed query
```

---

### P051: Async I/O (Non-Blocking Operations)

**Enforcement:** SHOULD - Requires justification
**Category:** Performance

Use async/await for I/O-bound operations, no blocking calls.

**❌ Bad Example:**
```
response = requests.get(url)  # Blocks!
```

**✅ Good Example:**
```
response = await http_client.get(url)  # Async
```

---

### P053: Centralized Version Management

**Enforcement:** SHOULD - Requires justification
**Category:** Code Quality

Single source of truth for version number - no fallbacks, fail-fast on import errors.

**Check Patterns:**
- Version defined in single location (__init__.py, package.json, Cargo.toml) (python, javascript, rust)
  - Pattern: `^(__version__|"version")\s*=\s*['"]\d+\.\d+\.\d+['"]`
- All modules import version from central source (python)
  - Pattern: `from \.+ import __version__`
- No version fallbacks - fail hard on import error (all)
  - Pattern: `(?!.*except.*__version__|.*getattr.*__version__|.*default.*version)`

**❌ Bad Example:**
```
# Multiple version definitions
__version__ = '1.0.0'
# In another file:
VERSION = '1.0.0'

# Fallback pattern (anti-pattern)
try:
    from . import __version__
except:
    __version__ = '0.0.0'
```

**✅ Good Example:**
```
# __init__.py - single source
__version__ = '1.0.0'

# Other modules
from .. import __version__

# pyproject.toml
[tool.setuptools.dynamic]
version = {attr = 'package.__version__'}
```

---

### P056: Container Security

**Enforcement:** SHOULD - Requires justification
**Category:** Security Privacy

Secure container images and runtime with minimal attack surface

**Check Patterns:**
- Use distroless or minimal base images (dockerfile)
  - Pattern: `FROM.*alpine|FROM.*distroless|FROM scratch`
- Run containers as non-root (dockerfile)
  - Pattern: `USER [^r]`
- Scan images for CVEs (all)
  - Pattern: `trivy|grype|snyk`

**❌ Bad Example:**
```
FROM ubuntu:latest\nRUN apt-get install...  # Root user, full OS
```

**✅ Good Example:**
```
FROM gcr.io/distroless/python3\nUSER 1000:1000  # Non-root, minimal
```

---

### P057: Kubernetes Security

**Enforcement:** SHOULD - Requires justification
**Category:** Security Privacy

Harden Kubernetes clusters with RBAC, network policies, and admission control

**Check Patterns:**
- Use RBAC with least privilege (yaml)
  - Pattern: `kind:\s*Role|kind:\s*ClusterRole`
- Define network policies (yaml)
  - Pattern: `kind:\s*NetworkPolicy`
- Use Pod Security Standards (restricted) (yaml)
  - Pattern: `securityContext:|runAsNonRoot: true`

**❌ Bad Example:**
```
# No RBAC, no network policies, root containers
```

**✅ Good Example:**
```
apiVersion: policy/v1\nkind: PodSecurityPolicy\nspec:\n  runAsUser:\n    rule: MustRunAsNonRoot
```

---

### P058: Zero Trust Architecture

**Enforcement:** SHOULD - Requires justification
**Category:** Security Privacy

Never trust, always verify - authenticate and authorize every request

**Check Patterns:**
- No trust based on network location (all)
  - Pattern: `(?!.*verify|.*authenticate)`
- Use mTLS for service-to-service (all)
  - Pattern: `mtls|mutual.*tls`

**❌ Bad Example:**
```
if request.from_internal_network:\n    allow()  # Implicit trust!
```

**✅ Good Example:**
```
token = verify_jwt(request.headers['Authorization'])\nif has_permission(token, resource):\n    allow()
```

---

### P061: Privacy Compliance

**Enforcement:** SHOULD - Requires justification
**Category:** Security Privacy

Comply with GDPR, CCPA, and other privacy regulations

**Check Patterns:**
- Collect only necessary data (all)
  - Pattern: `(?!.*minimize|.*necessary)`
- Support automated data deletion (all)
  - Pattern: `delete.*user.*data|gdpr.*delete`

**❌ Bad Example:**
```
# Collect everything, no deletion support
```

**✅ Good Example:**
```
@app.delete('/user/{id}/data')\ndef delete_user_data(id):\n    # GDPR Article 17
```

---

### P062: API Security Best Practices

**Enforcement:** SHOULD - Requires justification
**Category:** Api Design

Secure APIs against OWASP API Security Top 10 threats

**Check Patterns:**
- Require authentication on all endpoints (python)
  - Pattern: `@app\.(get|post|put|delete)(?!.*@require_auth|.*@authenticated)`
- Rate limit per user/IP (python)
  - Pattern: `@limiter\.limit`

**❌ Bad Example:**
```
@app.post('/api/transfer')\ndef transfer(amount):  # No auth!
```

**✅ Good Example:**
```
@app.post('/api/transfer')\n@require_auth\n@limiter.limit('10/minute')\ndef transfer(amount):
```

---

### P063: Dependency Management

**Enforcement:** SHOULD - Requires justification
**Category:** Security Privacy

Keep dependencies updated and scan for vulnerabilities

**Check Patterns:**
- Use Dependabot or Renovate (all)
  - Pattern: `\.github/dependabot\.yml|renovate\.json`
- Scan dependencies in CI (all)
  - Pattern: `snyk|npm audit|pip.*check`

**❌ Bad Example:**
```
# Dependencies never updated, no scanning
```

**✅ Good Example:**
```
# .github/dependabot.yml exists\n# CI: snyk test || exit 1
```

---

### P066: Agent Orchestration Patterns

**Enforcement:** SHOULD - Requires justification
**Category:** Architecture

Optimize AI agent execution through parallel processing, appropriate model selection, and cost-effective workflows

**Check Patterns:**
- Launch parallel agents in single message (all)
  - Pattern: `Task.*Task.*in single message|parallel.*agent`
- Use appropriate model for task complexity (all)
  - Pattern: `model.*haiku.*simple|model.*sonnet.*complex`
- Optimize for cost and performance (all)
  - Pattern: `lru_cache|@cache|memoize`

**❌ Bad Example:**
```
# Sequential agent launches (slow)\nagent1 = Task("search files")\n# Wait for agent1...\nagent2 = Task("analyze data")\n\n# Wrong model selection\nTask("simple grep", model="opus")  # Expensive!
```

**✅ Good Example:**
```
# Parallel agents in SINGLE message\nTask("search files", model="haiku")\nTask("analyze data", model="haiku")\n# Both run simultaneously\n\n# Appropriate model selection\nTask("simple grep", model="haiku")\nTask("complex analysis", model="sonnet")
```

---

## Skipped Principles

The following principles **do not apply** to your project:

- ❌ **P004: No Backward Compatibility Debt**
  - Reason: Does not match project preferences

- ❌ **P006: Precision in Calculations**
  - Reason: Does not match project preferences

- ❌ **P007: Immutability by Default**
  - Reason: Does not match project preferences

- ❌ **P008: Code Review Checklist Compliance**
  - Reason: Does not match project preferences

- ❌ **P010: Performance Profiling Before Optimization**
  - Reason: Does not match project preferences

- ❌ **P012: Singleton Pattern for Expensive Resources**
  - Reason: Does not match project preferences

- ❌ **P013: Separation of Concerns**
  - Reason: Does not match project preferences

- ❌ **P015: CQRS Pattern**
  - Reason: Solo developer (team_trajectory = 'solo')

- ❌ **P016: Dependency Injection**
  - Reason: Solo developer (team_trajectory = 'solo')

- ❌ **P017: Circuit Breaker Pattern**
  - Reason: Solo developer (team_trajectory = 'solo')

- ❌ **P018: API Versioning Strategy**
  - Reason: Solo developer (team_trajectory = 'solo')

- ❌ **P020: TTL-Based Cleanup**
  - Reason: Does not match project preferences

- ❌ **P028: CORS Policy**
  - Reason: Does not match project preferences

- ❌ **P031: Minimal Responsibility (Zero Maintenance)**
  - Reason: Does not match project preferences

- ❌ **P032: Configuration as Code**
  - Reason: Does not match project preferences

---

## Using These Principles

### In Claude Code

Reference this file in any conversation:
```
@PRINCIPLES.md Check if this code follows our principles
```

### In Commands

All CCO commands use these principles:
- `/cco-audit-code` - Check critical code quality principles
- `/cco-audit-principles` - Check all applicable principles
- `/cco-fix-code` - Auto-fix violations

### Updating Principles

To update your principles:
1. Change preferences: Edit `~/.cco/projects/{project}.json`
2. Regenerate: `/cco-generate-principles`
3. Review: `git diff .claude/PRINCIPLES.md`

---

*Auto-generated by ClaudeCodeOptimizer v{cco_version}*
*Principle Database: 70 total principles*
*Reference with: @PRINCIPLES.md*