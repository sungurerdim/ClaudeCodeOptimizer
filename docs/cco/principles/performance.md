# Performance Principles

**Generated**: 2025-11-09
**Principle Count**: 5

---

### P048: Caching Strategy 🟡

**Severity**: Medium

Redis + CDN, appropriate TTL, cache invalidation.

**Project Types**: api, web

**❌ Bad**:
```
# No caching, DB hit every time
```

**✅ Good**:
```
@cache(ttl=3600)\ndef expensive_query():
```

---

### P049: Database Query Optimization 🟠

**Severity**: High

Proper indexing, N+1 prevention, query analysis.

**❌ Bad**:
```
SELECT * FROM large_table  # No index, full scan
```

**✅ Good**:
```
CREATE INDEX idx_user_id ON jobs(user_id)  # Indexed query
```

---

### P050: Lazy Loading & Pagination 🟡

**Severity**: Medium

Don't load all data at once, paginate large result sets.

**Project Types**: api, web

**❌ Bad**:
```
SELECT * FROM users  # Returns 1M rows!
```

**✅ Good**:
```
SELECT * FROM users LIMIT 100 OFFSET 0  # Paginated
```

---

### P051: Async I/O (Non-Blocking Operations) 🟠

**Severity**: High

Use async/await for I/O-bound operations, no blocking calls.

**Project Types**: api, web

**Languages**: python, javascript, typescript

**❌ Bad**:
```
response = requests.get(url)  # Blocks!
```

**✅ Good**:
```
response = await http_client.get(url)  # Async
```

---

### P064: Continuous Profiling 🟡

**Severity**: Medium

Use continuous profiling to identify performance bottlenecks in production

**Languages**: python, go, rust

**Rules**:
- Enable continuous profiling

**❌ Bad**:
```
# No profiling in production
```

**✅ Good**:
```
# Pyroscope agent enabled\n# CPU, memory, I/O profiles collected
```

---

---

**Loading**: These principles load automatically when running relevant commands

**Reference**: Use `@PRINCIPLES.md` to load core principles, or reference this file directly