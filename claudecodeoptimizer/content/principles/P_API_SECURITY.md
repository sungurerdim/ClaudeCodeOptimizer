---
name: api_security
description: Prevent OWASP API Top 10 threats through authentication and input validation
type: project
severity: critical
keywords: [security, api, authentication, rate-limiting, injection]
category: [security]
related_skills: []
---
# P_API_SECURITY: API Security Best Practices

**Severity**: Critical

Prevent OWASP API Top 10 threats: broken auth causes most API breaches; lack of rate limiting enables DoS; insufficient input validation leads to injection attacks.

---

## Rules

- **Authentication required** - JWT/OAuth on all endpoints
- **Input validation** - Schema validation on all inputs
- **Rate limiting** - Per user/IP limits (prevent DoS)
- **Parameterized queries** - Prevent SQL injection
- **HTTPS only** - Reject HTTP requests
- **Authorization checks** - Verify user can access resource

---

## Examples

### ✅ Good
```python
@app.post('/api/transfer')
@require_auth  # Authentication
@limiter.limit('10 per minute')  # Rate limiting
@validate_input(TransferSchema)  # Input validation
def transfer_funds():
    data = request.get_json()
    # Parameterized query (prevent SQL injection)
    db.execute("INSERT INTO transfers VALUES (?, ?, ?)",
               (data['from'], data['to'], data['amount']))
```
**Why right**: Auth + validation + rate limiting + parameterized queries

### ❌ Bad
```python
@app.post('/api/transfer')
def transfer_funds():
    data = request.get_json()
    # SQL injection!
    db.execute(f"INSERT INTO transfers VALUES ('{data['from']}', '{data['to']}', {data['amount']})")
```
**Why wrong**: No auth, no validation, no rate limiting, SQL injection vulnerable

---

## Anti-Patterns

**❌ No Rate Limiting**: Enables DoS - 100K requests can cost $1000+
**❌ Weak Authentication**: API keys in URL logged everywhere (access logs, browser history, proxies)
**❌ No Input Validation**: Attacker can set `is_admin=True`, `balance=1000000`

---

## Checklist

- [ ] Authentication on all endpoints
- [ ] Input validation with schema
- [ ] Rate limiting (per user/IP)
- [ ] Parameterized queries only
- [ ] HTTPS only
- [ ] CORS whitelist
- [ ] Don't leak errors
