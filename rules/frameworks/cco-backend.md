# Backend Frameworks
*Common patterns across all backend frameworks*

**Trigger:** Backend framework detected

## Universal Patterns

These apply regardless of framework:

| Pattern | Implementation |
|---------|----------------|
| Validation | Schema-based input validation at entry point |
| Error Handler | Centralized error handling, consistent format |
| Health Endpoint | `/health` or `/healthz` returning 200 |
| Graceful Shutdown | Drain connections on SIGTERM |
| Request Context | Correlation ID propagation |
| Middleware Order | Auth → Validation → Business → Error Handler |

## Framework-Specific Gotchas

### Node.js Frameworks
- **Express**: Error handlers MUST be last middleware (4 params: `err, req, res, next`)
- **Fastify**: Schema validation is compile-time - define schemas upfront
- **NestJS**: Circular dependencies require `forwardRef()`

### Python Frameworks
- **FastAPI**: Use `async def` for I/O, `def` for CPU-bound (thread pool)
- **Django**: `select_related()` / `prefetch_related()` to avoid N+1
- **Flask**: Application context required outside requests

### JVM Frameworks
- **Spring**: `@Transactional` doesn't work on private methods
- **Quarkus**: Ensure GraalVM native-image compatibility (no reflection)
- **Micronaut**: DI is compile-time - no runtime bean discovery

### Go Frameworks
- **Gin**: `c.Abort()` doesn't return - always follow with `return`
- **Echo/Fiber**: Body can only be read once - use `c.Request().Body`

### Rust Frameworks
- **Axum**: Extractor order matters - body extractors must be last
- **Actix**: Actor state requires `Arc` for sharing across threads

## Operations Checklist

**Before Production:**
- [ ] Health endpoint implemented
- [ ] Graceful shutdown configured
- [ ] Request logging with correlation ID
- [ ] Error responses use consistent schema
- [ ] Timeouts set on all external calls
