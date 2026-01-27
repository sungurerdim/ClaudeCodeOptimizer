# API Rules
*Specific formats and limits*

## Error Format (RFC 7807) [CRITICAL]

Content-Type: `application/problem+json`

```json
{
  "type": "https://api.example.com/errors/validation",
  "title": "Validation Failed",
  "status": 422,
  "detail": "Request validation failed",
  "instance": "/api/users/123",
  "request_id": "req_12345",
  "errors": [{"field": "email", "message": "Invalid format"}]
}
```

**Required**: type, title, status

---

## Pagination (Cursor-Based)

```json
{
  "data": [...],
  "pagination": {
    "limit": 20,
    "next_cursor": "base64_encoded",
    "has_more": true
  }
}
```

| Parameter | Value |
|-----------|-------|
| Default limit | 20 |
| Max limit | 100 |
| Cursor format | Opaque base64 |

---

## Rate Limit Headers

```
RateLimit-Limit: 1000
RateLimit-Remaining: 999
RateLimit-Reset: 1705335000
Retry-After: 60  # On 429 only
```

---

## CORS Security

- NEVER `*` with credentials
- Whitelist specific origins
- No auth for OPTIONS preflight

```
Access-Control-Allow-Origin: https://trusted.com
Access-Control-Allow-Credentials: true
Access-Control-Max-Age: 86400
```

---

## GraphQL Limits [CRITICAL]

| Limit | Value |
|-------|-------|
| Max Depth | 10-15 |
| Max Complexity | 1000 |
| Query Timeout | 5-30s |
| Introspection | Disabled (prod) |

**Required**: DataLoader (N+1 prevention)

---

## API Deprecation Timeline

| Time | Action |
|------|--------|
| T+0 | Add `Deprecation: true` header |
| T+3mo | Email with migration guide |
| T+6mo | SDK warnings |
| T+12mo | Return 410 Gone |

```
Deprecation: true
Sunset: Sun, 31 Dec 2025 23:59:59 GMT
```
