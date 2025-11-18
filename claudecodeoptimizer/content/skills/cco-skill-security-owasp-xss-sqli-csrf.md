---
name: security-owasp-xss-sqli-csrf
description: Prevent XSS, SQL injection, CSRF, and auth vulnerabilities via secure coding and OWASP compliance. Includes input validation, parameterized queries, CSRF tokens, bcrypt/argon2 password hashing, JWT configuration, and CSP headers.
keywords: [security, XSS, SQL injection, CSRF, auth, sanitize, escape, validate, injection, OWASP, bcrypt, JWT, rate limiting]
category: security
related_commands:
  action_types: [audit, fix, generate]
  categories: [security]
pain_points: [1, 2, 6]
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

## Command Discovery Protocol

When this skill is active, find relevant commands by searching `~/.claude/commands/` metadata:

```yaml
# Search criteria for this skill's domain
action_types: [audit, fix, generate]
keywords: [security, XSS, injection, CSRF, auth, OWASP, vulnerability]
category: security
pain_points: [1, 2, 6]
```

**How Claude finds commands:**
1. Grep command files for `keywords:.*[pattern]` in frontmatter
2. Match `category: security`
3. Present matching commands with their parameters

This ensures commands are always current even when renamed or updated.
