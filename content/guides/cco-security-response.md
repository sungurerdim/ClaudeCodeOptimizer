---
title: Security Incident Response
category: security
tags: [security, incident, production, vulnerability]
description: Security incident response and remediation plan
use_cases:
  security_stance: [production, high]
  project_maturity: [production]
  project_purpose: [backend, web-app, microservice, spa]
---

# Security Incident Response

**Load on-demand when:** Security operations, vulnerability scanning, security audits

---

## Philosophy

Shift-left security: Integrate security analysis into development loop, not as final gate.

## Pre-Commit Security Review

Always scan before commits:
- `/cco-scan-secrets` - Check for exposed secrets
- `/cco-audit security` - Security audit
- `/cco-fix security` - Fix identified issues

---

## Security Analysis Workflow

### Quick Analysis
- Vulnerability assessment via code snippets
- Threat modeling for new features
- Specific security questions

### System-Wide Analysis
- `/cco-audit security` - Comprehensive audit
- `/cco-analyze --focus=auth` - Auth flow analysis
- `/cco-optimize-deps --security` - Dependency vulnerabilities

---

## Native Sandboxing

**Two essential isolation mechanisms:**

1. **Filesystem Isolation**: Restrict access to current project directory only. Block system config and credentials.
2. **Network Isolation**: Limit connections to approved domains (github.com, pypi.org, npmjs.com, claude.ai). Require approval for new domains.

Benefits: Reduced friction, maintained security, improved transparency.

---

## Common Vulnerabilities & Fixes

### SQL Injection


**❌ Vulnerable**:
```python
# Bad: String concatenation
query = f"SELECT * FROM users WHERE id = {user_id}"
db.execute(query)
```

**✅ Secure**:
```python
# Good: Parameterized query
query = "SELECT * FROM users WHERE id = ?"
db.execute(query, (user_id,))
```

### XSS (Cross-Site Scripting)


**❌ Vulnerable**:
```javascript
// Bad: Direct HTML insertion
element.innerHTML = userInput;
```

**✅ Secure**:
```javascript
// Good: Text content only
element.textContent = userInput;

// Or: Sanitize HTML
element.innerHTML = DOMPurify.sanitize(userInput);
```

### Authentication Bypass


**❌ Vulnerable**:
```python
# Bad: Client-side auth check only
if request.headers.get("X-User-Role") == "admin":
    allow_access()
```

**✅ Secure**:
```python
# Good: Server-side validation with JWT
token = request.headers.get("Authorization")
user = verify_jwt_token(token)
if user.role == "admin":
    allow_access()
```

### Sensitive Data Exposure


**❌ Vulnerable**:
```python
# Bad: Hardcoded secrets
API_KEY = "sk-1234567890abcdef"
DATABASE_URL = "postgres://user:pass@localhost/db"
```

**✅ Secure**:
```python
# Good: Environment variables
import os
API_KEY = os.environ.get("API_KEY")
DATABASE_URL = os.environ.get("DATABASE_URL")

# Even better: Secret management service
from secret_manager import get_secret
API_KEY = get_secret("api_key")
```

---

## Security Checklist

Before deploying:
- No hardcoded secrets, inputs validated/sanitized
- Auth implemented correctly, HTTPS enforced
- Dependencies scanned, security headers configured
- No sensitive info in errors, upload restrictions in place
- Rate limiting and security logging implemented

---

## Incident Response Plan

### 1. Detection
- Scanner alerts, failed auth spikes, unusual traffic, data anomalies
- Commands: `/cco-audit security --emergency`, `/cco-scan-secrets`

### 2. Containment
- Isolate systems, rotate credentials, block malicious access, preserve evidence
- Commands: `/cco-audit security --verbose`, `/cco-status --security-report`

### 3. Remediation
- Identify root cause, implement fix, test thoroughly, deploy, verify
- Commands: `/cco-fix security`, then `pytest tests/security/ -v && /cco-audit security`

### 4. Post-Incident
- Document incident, update policies, improve detection, team training
