# Security & Privacy
**Encryption, zero-disk, privacy-first, auth, secrets, input validation**

**Total Principles:** 19

---

## P005: Schema-First Validation

**Severity:** CRITICAL

Use schema-based validation (Pydantic/Joi) for all external inputs.

### Examples

**✅ Good:**
```
@app.post('/api')
def create(data: ResourceSchema):  # Validated
```

**❌ Bad:**
```
@app.post('/api')
def create(data: dict):  # No validation!
```

**Why:** Reduces ambiguity and edge cases by using exact types instead of loose ones

---

## P019: Privacy-First by Default

**Severity:** CRITICAL

PII explicitly managed, cleaned from memory after use.

### Examples

**✅ Good:**
```
data = load_pii()
try:
    process(data)
finally:
    secure_zero(data)
```

**❌ Bad:**
```
data = load_pii()
process(data)  # Lingers in memory!
```

**Why:** Protects sensitive data by encrypting it at rest and in transit

---

## P020: TTL-Based Cleanup

**Severity:** HIGH

Temporary data auto-expires via TTL - no manual cleanup.

### Examples

**✅ Good:**
```
redis.setex('key', 3600, value)  # Auto-expires in 1h
```

**❌ Bad:**
```
redis.set('key', value)  # No TTL, leaks memory!
```

**Why:** Maximizes privacy by never writing sensitive data to disk or logs

---

## P021: Encryption Everywhere

**Severity:** CRITICAL

All sensitive data at rest MUST be encrypted (AES-256-GCM).

### Examples

**✅ Good:**
```
redis.set('sensitive', encrypt_aes_gcm(data))
```

**❌ Bad:**
```
redis.set('sensitive', data)  # Plaintext!
```

**Why:** Minimizes data collection by only storing what's absolutely necessary for functionality

---

## P022: Zero Disk Touch

**Severity:** CRITICAL

Sensitive data never touches filesystem - RAM and secure storage only.

### Examples

**✅ Good:**
```
process = subprocess.Popen(['ffmpeg', '-i', 'pipe:0'], stdin=PIPE)  # In-memory
```

**❌ Bad:**
```
with open('/tmp/audio.wav', 'wb') as f:  # Disk touch!
```

**Why:** Protects user privacy by anonymizing data before collection and storage

---

## P024: Authentication & Authorization

**Severity:** CRITICAL

OAuth2 + RBAC, verify permissions on every request.

### Examples

**✅ Good:**
```
@app.get('/admin')
@require_role('admin')
def admin():
```

**❌ Bad:**
```
@app.get('/admin')
def admin():  # No auth check!
```

**Why:** Prevents unauthorized access through proper authentication and session management

---

## P025: SQL Injection Prevention

**Severity:** CRITICAL

Always use parameterized queries, never string concatenation.

### Examples

**✅ Good:**
```
cursor.execute('SELECT * FROM users WHERE id=%s', (user_id,))  # Parameterized
```

**❌ Bad:**
```
cursor.execute(f'SELECT * FROM users WHERE id={user_id}')  # SQL injection!
```

**Why:** Prevents credential leaks by storing secrets outside code in secure vaults

---

## P026: Secret Management with Rotation

**Severity:** CRITICAL

Use secret managers (Vault, AWS/Azure/GCP), never hardcode. Implement rotation policies and audit logging.

### Examples

**✅ Good:**
```
# HashiCorp Vault
```
```
import hvac
```
```
client = hvac.Client(url='https://vault.example.com')
```
```
secret = client.secrets.kv.v2.read_secret_version(path='myapp/config')
```
```
API_KEY = secret['data']['data']['api_key']
```
```

```
```
# AWS Secrets Manager with rotation
```
```
import boto3
```
```
client = boto3.client('secretsmanager')
```
```
secret = client.get_secret_value(SecretId='prod/api/key')
```
```

```
```
# Kubernetes Sealed Secrets
```
```
apiVersion: bitnami.com/v1alpha1
```
```
kind: SealedSecret
```
```
metadata:
```
```
  name: mysecret
```
```
spec:
```
```
  encryptedData:
```
```
    password: AgBy3i4OJSWK+PiTySYZZA9rO43cGDEq...
```

**❌ Bad:**
```
# Hardcoded secret (CRITICAL violation)
```
```
API_KEY = '<hardcoded-api-key-value>'
```
```
DB_PASSWORD = '<hardcoded-password-value>'
```
```

```
```
# Plain env var without rotation
```
```
SECRET = os.getenv('SECRET')  # No rotation policy
```

**Why:** Prevents credential leaks and enables rotation without code changes

---

## P027: Rate Limiting & Throttling

**Severity:** HIGH

Prevent abuse with rate limiting on all public endpoints.

### Examples

**✅ Good:**
```
@limiter.limit('100/minute')
@app.post('/api')
```

**❌ Bad:**
```
@app.post('/api')  # No rate limiting
```

**Why:** Prevents injection attacks by using parameterized queries instead of string concatenation

---

## P028: CORS Policy

**Severity:** HIGH

Principle of least privilege - only allow required origins.

### Examples

**✅ Good:**
```
CORS(app, origins=['https://example.com'])
```

**❌ Bad:**
```
CORS(app, origins='*')  # Allows anyone!
```

**Why:** Protects APIs from abuse through rate limiting and request throttling

---

## P029: Input Sanitization (XSS Prevention)

**Severity:** CRITICAL

Escape/sanitize all user input before rendering.

### Examples

**✅ Good:**
```
textContent = user_input  # Safe
```

**❌ Bad:**
```
innerHTML = user_input  # XSS!
```

**Why:** Prevents XSS attacks by sanitizing all user input before display

---

## P030: Audit Logging

**Severity:** HIGH

Log all security events (auth, access, changes) for audit trail.

### Examples

**✅ Good:**
```
audit_logger.info('User {user_id} accessed resource {resource_id}')
```

**❌ Bad:**
```
# No logging for sensitive operations
```

**Why:** Enables security incident investigation through comprehensive audit logging

---

## P054: Supply Chain Security

**Severity:** CRITICAL

Verify software supply chain integrity through SBOM, provenance, and attestations

### Examples

**✅ Good:**
```
# Generate SBOM: cyclonedx-py
# Sign: cosign sign image
# Use: requirements.txt.lock
```

**❌ Bad:**
```
# No SBOM, unsigned artifacts, no lockfiles
```

**Why:** Prevents supply chain attacks by verifying artifact integrity and dependency provenance

---

## P055: AI/ML Security

**Severity:** CRITICAL

Protect AI/ML systems from prompt injection, model poisoning, and data leakage

### Examples

**✅ Good:**
```
# Validate input
if not is_safe_prompt(user_input):
    raise ValueError
response = llm(user_input)
```

**❌ Bad:**
```
# Direct prompt to LLM
response = llm(user_input)  # No validation!
```

**Why:** Prevents AI-specific attacks like prompt injection and model poisoning

---

## P056: Container Security

**Severity:** HIGH

Secure container images and runtime with minimal attack surface

### Examples

**✅ Good:**
```
FROM gcr.io/distroless/python3
USER 1000:1000  # Non-root, minimal
```

**❌ Bad:**
```
FROM ubuntu:latest
RUN apt-get install...  # Root user, full OS
```

**Why:** Reduces container attack surface through minimal images and runtime restrictions

---

## P057: Kubernetes Security

**Severity:** HIGH

Harden Kubernetes clusters with RBAC, network policies, and admission control

### Examples

**✅ Good:**
```
apiVersion: policy/v1
kind: PodSecurityPolicy
spec:
  runAsUser:
    rule: MustRunAsNonRoot
```

**❌ Bad:**
```
# No RBAC, no network policies, root containers
```

**Why:** Hardens Kubernetes against attacks through defense-in-depth controls

---

## P058: Zero Trust Architecture

**Severity:** HIGH

Never trust, always verify - authenticate and authorize every request

### Examples

**✅ Good:**
```
token = verify_jwt(request.headers['Authorization'])
if has_permission(token, resource):
    allow()
```

**❌ Bad:**
```
if request.from_internal_network:
    allow()  # Implicit trust!
```

**Why:** Eliminates implicit trust by verifying every access request regardless of source

---

## P061: Privacy Compliance

**Severity:** HIGH

Comply with GDPR, CCPA, and other privacy regulations

### Examples

**✅ Good:**
```
@app.delete('/user/{id}/data')
def delete_user_data(id):
    # GDPR Article 17
```

**❌ Bad:**
```
# Collect everything, no deletion support
```

**Why:** Avoids regulatory fines through comprehensive privacy compliance

---

## P063: Dependency Management

**Severity:** HIGH

Keep dependencies updated and scan for vulnerabilities

### Examples

**✅ Good:**
```
# .github/dependabot.yml exists
# CI: snyk test || exit 1
```

**❌ Bad:**
```
# Dependencies never updated, no scanning
```

**Why:** Prevents exploitation of known vulnerabilities through proactive dependency management

---
