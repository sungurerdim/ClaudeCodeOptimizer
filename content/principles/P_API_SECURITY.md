---
id: P_API_SECURITY
title: API Security Best Practices
category: api_design
severity: high
weight: 8
applicability:
  project_types: ['api', 'web', 'microservice']
  languages: ['all']
---

# P_API_SECURITY: API Security Best Practices 🔴

**Severity**: High

Secure APIs against OWASP API Security Top 10 threats

**Why**: Prevents API-specific attacks through defense-in-depth security controls

**Enforcement**: Skills required - verification_protocol, test_first, root_cause_analysis

**Project Types**: api, web
**Languages**: all

**Rules**:
- **Api Authentication**: Require authentication on all endpoints
- **Api Rate Limiting**: Rate limit per user/IP

**❌ Bad**:
```
@app.post('/api/transfer')
def transfer(amount):  # No auth!
```

**✅ Good**:
```
@app.post('/api/transfer')
@require_auth
@limiter.limit('10/minute')
def transfer(amount):
```
