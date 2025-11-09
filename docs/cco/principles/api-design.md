# API Design Principles

**Generated**: 2025-11-09
**Principle Count**: 2

---

### P052: RESTful API Conventions 🟡

**Severity**: Medium

Resource-based URLs, proper HTTP verbs, status codes.

**Project Types**: api

**❌ Bad**:
```
/getUser?id=123  # Not RESTful
```

**✅ Good**:
```
GET /users/123  # RESTful
```

---

### P062: API Security Best Practices 🟠

**Severity**: High

Secure APIs against OWASP API Security Top 10 threats

**Project Types**: api, web

**Rules**:
- Require authentication on all endpoints
- Rate limit per user/IP

**❌ Bad**:
```
@app.post('/api/transfer')\ndef transfer(amount):  # No auth!
```

**✅ Good**:
```
@app.post('/api/transfer')\n@require_auth\n@limiter.limit('10/minute')\ndef transfer(amount):
```

---

---

**Loading**: These principles load automatically when running relevant commands

**Reference**: Use `@PRINCIPLES.md` to load core principles, or reference this file directly