---
title: Security - OWASP, XSS, SQLi, CSRF
category: security
description: XSS, SQL injection, CSRF, auth vulnerability prevention
metadata:
  name: "Security - OWASP, XSS, SQLi, CSRF"
  activation_keywords: ["security", "XSS", "SQL injection", "CSRF", "auth", "sanitize", "escape", "validate", "injection"]
  category: "security"
principles: ['P_XSS_PREVENTION', 'P_SQL_INJECTION', 'P_AUTH_AUTHZ', 'P_API_SECURITY', 'P_ZERO_TRUST']
use_cases:
  development_philosophy: [quality_first, security_critical]
  project_maturity: [active-dev, production]
---

# Security - OWASP, XSS, SQLi, CSRF

Prevent XSS, SQL injection, CSRF, auth vulnerabilities via secure coding and OWASP compliance.

<!-- INSTRUCTIONS: Load when activated -->
## Detailed Instructions

**XSS Prevention:**
- Escape user input in HTML (auto-escaping templates)
- CSP headers
- Never innerHTML with user input

**SQL Injection:**
- Parameterized queries/prepared statements ONLY
- NEVER concatenate SQL + user input
- Use ORM

**CSRF:**
- CSRF tokens for POST/PUT/DELETE
- SameSite cookies
- Framework built-ins

**Auth:**
- bcrypt/argon2 for passwords
- JWT <15min expiration
- RBAC, secure cookies

**Input Validation:**
- Whitelist validation
- Type/length validation
- Rate limiting

<!-- RESOURCES: Load on explicit request -->
## Examples & Resources

**XSS:**
```python
# ✅ Auto-escaped
return render_template('profile.html', bio=user.bio)
# ❌ BAD
return f"<div>{user.bio}</div>"
```

**SQLi:**
```python
# ❌ BAD
query = f"SELECT * FROM users WHERE email='{email}'"
# ✅ GOOD
cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
```

**CSRF:**
```python
@csrf_protect
def reset_password(request):
    user.set_password(request.POST['password'])
```

**Auth:**
```python
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

@require_role('admin')
def admin_panel():
    return render_template('admin.html')
```
