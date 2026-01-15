# API Rules
*API design patterns and best practices*

## REST (API:REST)
**Trigger:** {routes_dir}, {rest_decorators}

### HTTP Standards
- **REST-Methods**: Proper HTTP verbs (GET=read, POST=create, PUT=update, PATCH=partial, DELETE=remove)
- **Status-Codes**: Appropriate codes (200=OK, 201=Created, 400=Bad Request, 401=Unauthenticated, 403=Forbidden, 404=Not Found, 409=Conflict, 422=Unprocessable, 500=Server Error)
- **Idempotency**: PUT/DELETE must be idempotent, POST with idempotency keys for safe retries

### Error Format (RFC 7807)

Use `application/problem+json` content type:

```json
{
  "type": "https://api.example.com/errors/validation",
  "title": "Validation Failed",
  "status": 422,
  "detail": "Request validation failed",
  "instance": "/api/users/123",
  "timestamp": "2025-01-15T10:30:00Z",
  "request_id": "req_12345",
  "errors": [
    {"field": "email", "message": "Invalid format", "code": "INVALID_EMAIL"}
  ]
}
```

**Required fields**: `type`, `title`, `status`
**Recommended**: `detail`, `instance`, `request_id`

### Cursor-Based Pagination

```json
{
  "data": [...],
  "pagination": {
    "limit": 20,
    "next_cursor": "xyz789uvw012",
    "prev_cursor": "abc000def111",
    "has_more": true
  }
}
```

| Parameter | Value | Purpose |
|-----------|-------|---------|
| Default limit | 20 | Reasonable default |
| Max limit | 100 | Prevent abuse |
| Cursor format | Opaque, base64 | Hide implementation |

**Rules**:
- O(1) performance (vs O(n) for offset)
- Use keyset pagination: `?after_id=123&after_created=...`
- Cursor encodes position, not just ID

### Rate Limit Headers

Include on all responses:
```
RateLimit-Limit: 1000
RateLimit-Remaining: 999
RateLimit-Reset: 1705335000
```

On 429 responses, add:
```
Retry-After: 60
```

### CORS Configuration

**Security Rules**:
- NEVER use `Access-Control-Allow-Origin: *` with credentials
- Whitelist specific origins
- Always respond to OPTIONS with 200/204 + CORS headers
- Don't require auth for OPTIONS (preflight)

**Headers**:
```
Access-Control-Allow-Origin: https://trusted-domain.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Allow-Credentials: true
Access-Control-Max-Age: 86400
```

---

## GraphQL (API:GraphQL)
**Trigger:** {schema_files}, {graphql_deps}

### Security Limits

| Limit | Value | Purpose |
|-------|-------|---------|
| Max Depth | 10-15 | Prevent nested DoS |
| Max Complexity | 1000 | Prevent expensive queries |
| Query Timeout | 5-30s | Prevent hanging |
| Introspection | Disabled (prod) | Prevent schema exposure |

**Required Patterns**:
- DataLoader: Required to prevent N+1 queries
- Persisted Queries: Recommended for first-party clients
- Query Complexity Analysis: Calculate before execution

### Response Design
- **Pagination**: Cursor-based pagination (Relay connection spec)
- **Error-Format**: Consistent format, no stack traces in prod

---

## gRPC (API:gRPC)
**Trigger:** {proto_files}, {grpc_deps}

- **Proto-Version**: Backward compatible proto changes
- **Error-Format**: Use standard gRPC status codes with details
- **Deadline-Propagation**: Propagate deadlines across service calls

---

## API Evolution (API:Evolution)
**Trigger:** API:* + T:Library

### Deprecation Timeline

| Time | Action |
|------|--------|
| T+0 | Announce, add `Deprecation: true` header |
| T+3mo | Email consumers with migration guide |
| T+6mo | Add warning to SDK, increase logging |
| T+12mo | Sunset date, return 410 Gone |

**Minimum notice**: 12 months for breaking changes

### Deprecation Headers

```
Deprecation: true
Sunset: Sun, 31 Dec 2025 23:59:59 GMT
Link: <https://api.example.com/v2/users>; rel="successor-version"
```

### Version Management
- **Version-Boundary**: Breaking changes only in major versions (unless v0.x)
- **Alias-Bridge**: Provide aliases/redirects during transition period
- **Migration-Guide**: Breaking changes include migration instructions
