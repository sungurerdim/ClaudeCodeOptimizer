# Security Incident Response

**Load on-demand when:** Security operations, vulnerability scanning, security audits

---

## Philosophy

**Shift-left security approach:** Integrate security analysis into the development loop, not as a final gate.

---

## Pre-Commit Security Review

**Always scan before commits:**

- ✅ SQL injection and ORM security
- ✅ Cross-site scripting (XSS) vulnerabilities
- ✅ Authentication/authorization gaps
- ✅ Sensitive data exposure
- ✅ Third-party package vulnerabilities

**Commands**:
```bash
# Scan for secrets
/cco-scan-secrets

# Security audit
/cco-audit security

# Fix security issues
/cco-fix security
```

---

## Security Analysis Workflow

### Quick Triage (Claude.ai)

Use for immediate analysis:

- Paste code snippets for vulnerability assessment
- Get threat modeling for new features before implementation
- Transform scanner reports into ranked, actionable steps
- Ask specific questions:
  - "Is this API key storage secure?"
  - "How should I handle file uploads safely?"
  - "Is this authentication flow secure?"

### System-Wide Analysis (Claude Code)

Use for comprehensive analysis:

- Analyze authentication flows across entire codebase
- Identify specific files/line numbers with vulnerabilities
- Implement targeted fixes integrated with existing security architecture
- Examine dependencies and trace security issues systematically

**Commands**:
```bash
# Comprehensive security audit
/cco-audit security

# Analyze authentication patterns
/cco-analyze --focus=auth

# Check dependencies for vulnerabilities
/cco-optimize-deps --security
```

---

## Native Sandboxing

**Two essential isolation mechanisms (both required):**

### 1. Filesystem Isolation

- Restrict access to specific directories only
- Allow read/write to current working directory
- Block external modifications
- Prevents compromised agents from modifying sensitive system files

**Implementation**:
```python
# Sandbox configuration
sandbox_config = {
    "allowed_paths": [
        os.getcwd(),  # Current project
        "~/.cco/",    # CCO data
    ],
    "blocked_paths": [
        "/etc/",      # System config
        "~/.ssh/",    # SSH keys
        "~/.aws/",    # Cloud credentials
    ]
}
```

### 2. Network Isolation

- Limit connections to approved servers only
- Use proxy server to enforce domain restrictions
- Handle user confirmations for new requests
- Prevents data exfiltration and malware downloads

**Implementation**:
```python
# Allowed domains
allowed_domains = [
    "github.com",
    "pypi.org",
    "npmjs.com",
    "claude.ai",
]

# Require approval for new domains
def check_domain(domain: str) -> bool:
    if domain not in allowed_domains:
        return ask_user_approval(domain)
    return True
```

### Benefits

- **Reduced friction**: Fewer approval delays
- **Maintained security**: Compromised processes remain isolated
- **Improved transparency**: Boundary violations trigger immediate alerts

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

**Before deploying**:
- [ ] No hardcoded secrets (scan with `/cco-scan-secrets`)
- [ ] All inputs validated and sanitized
- [ ] Authentication/authorization implemented correctly
- [ ] HTTPS enforced for all external communication
- [ ] Dependencies scanned for vulnerabilities (`/cco-optimize-deps --security`)
- [ ] Security headers configured (CSP, HSTS, etc.)
- [ ] Error messages don't leak sensitive information
- [ ] File upload restrictions in place (type, size, location)
- [ ] Rate limiting implemented for public APIs
- [ ] Logging includes security events (failed logins, access denials)

---

## Incident Response Plan

### 1. Detection

**Indicators**:
- Vulnerability scanner alerts
- Failed authentication attempts spike
- Unusual network traffic
- Data access anomalies
- Security tool notifications

**Commands**:
```bash
# Immediate scan
/cco-audit security --emergency

# Check for exposed secrets
/cco-scan-secrets

# Review recent changes
git log --since="24 hours ago" --oneline
```

### 2. Containment

**Immediate actions**:
1. Isolate affected systems
2. Rotate compromised credentials
3. Block malicious IPs/users
4. Preserve evidence (logs, snapshots)

**Commands**:
```bash
# Identify vulnerability location
/cco-audit security --verbose

# Generate incident report
/cco-status --security-report
```

### 3. Remediation

**Fix process**:
1. Identify root cause
2. Implement fix
3. Test fix thoroughly
4. Deploy to production
5. Verify fix in production

**Commands**:
```bash
# Auto-fix if possible
/cco-fix security

# Otherwise, manual fix with verification
# [implement fix]
pytest tests/security/ -v
/cco-audit security
```

### 4. Post-Incident

**Follow-up**:
1. Document incident (what, when, how, impact)
2. Update security policies
3. Improve detection mechanisms
4. Team training on lessons learned
5. Update CCO security principles if needed

---

## Principle References

- **P019-P037**: Security & Privacy Principles

See: [@~/.cco/principles/security.md](../principles/security.md)

---

*Part of CCO Documentation System*
*Load when needed: @~/.cco/guides/security-response.md*
