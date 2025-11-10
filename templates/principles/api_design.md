# API Design
**RESTful conventions, versioning, error handling**

**Total Principles:** 2

---

## P052: RESTful API Conventions

**Severity:** MEDIUM

Resource-based URLs, proper HTTP verbs, status codes.

### Examples

**✅ Good:**
```
GET /users/123  # RESTful
```

**❌ Bad:**
```
/getUser?id=123  # Not RESTful
```

**Why:** Makes APIs intuitive through RESTful conventions and proper HTTP verbs

---

## P062: API Security Best Practices

**Severity:** HIGH

Secure APIs against OWASP API Security Top 10 threats

### Examples

**✅ Good:**
```
@app.post('/api/transfer')
@require_auth
@limiter.limit('10/minute')
def transfer(amount):
```

**❌ Bad:**
```
@app.post('/api/transfer')
def transfer(amount):  # No auth!
```

**Why:** Prevents API-specific attacks through defense-in-depth security controls

---
