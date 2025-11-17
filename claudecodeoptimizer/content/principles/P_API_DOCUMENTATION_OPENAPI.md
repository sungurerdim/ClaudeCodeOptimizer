# P_API_DOCUMENTATION_OPENAPI: API Documentation with OpenAPI/Swagger

**Severity**: High

 Manual docs diverge from implementation; clients use wrong parameters Developers write code to outdated API specs; fails in production API logic documented in code AND separate documentation; mainten.

---

## Rules

- *No rules extracted*

---

## Examples

### ✅ Good
```yaml
# openapi.yaml - Single source of truth
openapi: 3.0.0
info:
  title: User Management API
  version: 2.0.0
  description: Comprehensive user management service
  contact:
    name: API Support
    url: https://api.example.com/support
  license:
    name: Apache 2.0

servers:
  - url: https://api.example.com/v2
    description: Production
  - url: https://staging-api.example.com/v2
```
**Why right**: **Why it's good:**

### ❌ Bad
```markdown
# ❌ BAD: Separate documentation document
## User Management API

### Get User
- Endpoint: GET /api/users/{id}
- Parameters: id (string, user ID)
- Response: { user: { id, name, email } }

### Create User
- Endpoint: POST /api/users
- Body: { name, email, password }
```
**Why wrong**: **Why it's bad:**

---

## Checklist

- [ ] OpenAPI spec exists - openapi.yaml or openapi.json in repo root
- [ ] Spec version-controlled - Tracked in git, changes reviewed
- [ ] All endpoints documented - Every route has path, parameters, responses
- [ ] Schema validation - Request/response bodies validated against spec
- [ ] Auto-generated docs - Swagger UI or ReDoc available
- [ ] Breaking change detection - CI fails on breaking changes
- [ ] Client SDK generation - Generated clients from spec
