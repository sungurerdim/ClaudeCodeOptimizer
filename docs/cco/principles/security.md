# Security & Privacy Principles

**Generated**: 2025-11-09
**Principle Count**: 19

---

### P005: Schema-First Validation 🔴

**Severity**: Critical

Use schema-based validation (Pydantic/Joi) for all external inputs.

**Project Types**: api, web, ml

**Languages**: python, javascript, typescript

**Rules**:
- Validate data at API entry points

**❌ Bad**:
```
@app.post('/api')\ndef create(data: dict):  # No validation!
```

**✅ Good**:
```
@app.post('/api')\ndef create(data: ResourceSchema):  # Validated
```

---

### P019: Privacy-First by Default 🔴

**Severity**: Critical

PII explicitly managed, cleaned from memory after use.

**Rules**:
- PII variables must have cleanup

**❌ Bad**:
```
data = load_pii()\nprocess(data)  # Lingers in memory!
```

**✅ Good**:
```
data = load_pii()\ntry:\n    process(data)\nfinally:\n    secure_zero(data)
```

---

### P020: TTL-Based Cleanup 🟠

**Severity**: High

Temporary data auto-expires via TTL - no manual cleanup.

**Rules**:
- Cache sets must have TTL

**❌ Bad**:
```
redis.set('key', value)  # No TTL, leaks memory!
```

**✅ Good**:
```
redis.setex('key', 3600, value)  # Auto-expires in 1h
```

---

### P021: Encryption Everywhere 🔴

**Severity**: Critical

All sensitive data at rest MUST be encrypted (AES-256-GCM).

**Rules**:
- No plaintext in cache

**❌ Bad**:
```
redis.set('sensitive', data)  # Plaintext!
```

**✅ Good**:
```
redis.set('sensitive', encrypt_aes_gcm(data))
```

---

### P022: Zero Disk Touch 🔴

**Severity**: Critical

Sensitive data never touches filesystem - RAM and secure storage only.

**Rules**:
- No temp files for sensitive data

**❌ Bad**:
```
with open('/tmp/audio.wav', 'wb') as f:  # Disk touch!
```

**✅ Good**:
```
process = subprocess.Popen(['ffmpeg', '-i', 'pipe:0'], stdin=PIPE)  # In-memory
```

---

### P024: Authentication & Authorization 🔴

**Severity**: Critical

OAuth2 + RBAC, verify permissions on every request.

**Project Types**: api, web

**❌ Bad**:
```
@app.get('/admin')\ndef admin():  # No auth check!
```

**✅ Good**:
```
@app.get('/admin')\n@require_role('admin')\ndef admin():
```

---

### P025: SQL Injection Prevention 🔴

**Severity**: Critical

Always use parameterized queries, never string concatenation.

**Rules**:
- No string concatenation in SQL

**❌ Bad**:
```
cursor.execute(f'SELECT * FROM users WHERE id={user_id}')  # SQL injection!
```

**✅ Good**:
```
cursor.execute('SELECT * FROM users WHERE id=%s', (user_id,))  # Parameterized
```

---

### P026: Secret Management with Rotation 🔴

**Severity**: Critical

Use secret managers (Vault, AWS/Azure/GCP), never hardcode. Implement rotation policies and audit logging.

**Rules**:
- No hardcoded API keys/passwords/tokens
- Use secret manager (Vault, AWS Secrets Manager, etc.)
- Implement secret rotation (30-90 days)
- Audit all secret access
- Never commit secrets to git

**❌ Bad**:
```
# Hardcoded secret (CRITICAL violation)
```

**✅ Good**:
```
# HashiCorp Vault
```

---

### P027: Rate Limiting & Throttling 🟠

**Severity**: High

Prevent abuse with rate limiting on all public endpoints.

**Project Types**: api, web

**❌ Bad**:
```
@app.post('/api')  # No rate limiting
```

**✅ Good**:
```
@limiter.limit('100/minute')\n@app.post('/api')
```

---

### P028: CORS Policy 🟠

**Severity**: High

Principle of least privilege - only allow required origins.

**Project Types**: api, web

**❌ Bad**:
```
CORS(app, origins='*')  # Allows anyone!
```

**✅ Good**:
```
CORS(app, origins=['https://example.com'])
```

---

### P029: Input Sanitization (XSS Prevention) 🔴

**Severity**: Critical

Escape/sanitize all user input before rendering.

**Project Types**: web

**Languages**: javascript, typescript, python

**❌ Bad**:
```
innerHTML = user_input  # XSS!
```

**✅ Good**:
```
textContent = user_input  # Safe
```

---

### P030: Audit Logging 🟠

**Severity**: High

Log all security events (auth, access, changes) for audit trail.

**❌ Bad**:
```
# No logging for sensitive operations
```

**✅ Good**:
```
audit_logger.info('User {user_id} accessed resource {resource_id}')
```

---

### P054: Supply Chain Security 🔴

**Severity**: Critical

Verify software supply chain integrity through SBOM, provenance, and attestations

**Rules**:
- Generate SBOM for all releases
- Sign artifacts with Sigstore/cosign
- Use dependency lockfiles

**❌ Bad**:
```
# No SBOM, unsigned artifacts, no lockfiles
```

**✅ Good**:
```
# Generate SBOM: cyclonedx-py\n# Sign: cosign sign image\n# Use: requirements.txt.lock
```

---

### P055: AI/ML Security 🔴

**Severity**: Critical

Protect AI/ML systems from prompt injection, model poisoning, and data leakage

**Project Types**: ml, api, all

**Languages**: python, all

**Rules**:
- Validate and sanitize prompts
- Sanitize model outputs
- Sign and verify models

**❌ Bad**:
```
# Direct prompt to LLM\nresponse = llm(user_input)  # No validation!
```

**✅ Good**:
```
# Validate input\nif not is_safe_prompt(user_input):\n    raise ValueError\nresponse = llm(user_input)
```

---

### P056: Container Security 🟠

**Severity**: High

Secure container images and runtime with minimal attack surface

**Rules**:
- Use distroless or minimal base images
- Run containers as non-root
- Scan images for CVEs

**❌ Bad**:
```
FROM ubuntu:latest\nRUN apt-get install...  # Root user, full OS
```

**✅ Good**:
```
FROM gcr.io/distroless/python3\nUSER 1000:1000  # Non-root, minimal
```

---

### P057: Kubernetes Security 🟠

**Severity**: High

Harden Kubernetes clusters with RBAC, network policies, and admission control

**Rules**:
- Use RBAC with least privilege
- Define network policies
- Use Pod Security Standards (restricted)

**❌ Bad**:
```
# No RBAC, no network policies, root containers
```

**✅ Good**:
```
apiVersion: policy/v1\nkind: PodSecurityPolicy\nspec:\n  runAsUser:\n    rule: MustRunAsNonRoot
```

---

### P058: Zero Trust Architecture 🟠

**Severity**: High

Never trust, always verify - authenticate and authorize every request

**Project Types**: microservices, api

**Rules**:
- No trust based on network location
- Use mTLS for service-to-service

**❌ Bad**:
```
if request.from_internal_network:\n    allow()  # Implicit trust!
```

**✅ Good**:
```
token = verify_jwt(request.headers['Authorization'])\nif has_permission(token, resource):\n    allow()
```

---

### P061: Privacy Compliance 🟠

**Severity**: High

Comply with GDPR, CCPA, and other privacy regulations

**Rules**:
- Collect only necessary data
- Support automated data deletion

**❌ Bad**:
```
# Collect everything, no deletion support
```

**✅ Good**:
```
@app.delete('/user/{id}/data')\ndef delete_user_data(id):\n    # GDPR Article 17
```

---

### P063: Dependency Management 🟠

**Severity**: High

Keep dependencies updated and scan for vulnerabilities

**Rules**:
- Use Dependabot or Renovate
- Scan dependencies in CI

**❌ Bad**:
```
# Dependencies never updated, no scanning
```

**✅ Good**:
```
# .github/dependabot.yml exists\n# CI: snyk test || exit 1
```

---

---

**Loading**: These principles load automatically when running relevant commands

**Reference**: Use `@PRINCIPLES.md` to load core principles, or reference this file directly