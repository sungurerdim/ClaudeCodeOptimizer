# Performance
**Caching, DB optimization, lazy loading, async I/O**

**Total Principles:** 5

---

## P048: Caching Strategy

**Severity:** MEDIUM

Redis + CDN, appropriate TTL, cache invalidation.

### Examples

**✅ Good:**
```
@cache(ttl=3600)
def expensive_query():
```

**❌ Bad:**
```
# No caching, DB hit every time
```

**Why:** Speeds up repeated requests through intelligent caching at multiple system layers

---

## P049: Database Query Optimization

**Severity:** HIGH

Proper indexing, N+1 prevention, query analysis.

### Examples

**✅ Good:**
```
CREATE INDEX idx_user_id ON jobs(user_id)  # Indexed query
```

**❌ Bad:**
```
SELECT * FROM large_table  # No index, full scan
```

**Why:** Prevents slow queries through proper database indexing and query optimization

---

## P050: Lazy Loading & Pagination

**Severity:** MEDIUM

Don't load all data at once, paginate large result sets.

### Examples

**✅ Good:**
```
SELECT * FROM users LIMIT 100 OFFSET 0  # Paginated
```

**❌ Bad:**
```
SELECT * FROM users  # Returns 1M rows!
```

**Why:** Reduces memory usage by loading data only when needed instead of upfront

---

## P051: Async I/O (Non-Blocking Operations)

**Severity:** HIGH

Use async/await for I/O-bound operations, no blocking calls.

### Examples

**✅ Good:**
```
response = await http_client.get(url)  # Async
```

**❌ Bad:**
```
response = requests.get(url)  # Blocks!
```

**Why:** Improves responsiveness through non-blocking async operations for I/O tasks

---

## P064: Continuous Profiling

**Severity:** MEDIUM

Use continuous profiling to identify performance bottlenecks in production

### Examples

**✅ Good:**
```
# Pyroscope agent enabled
# CPU, memory, I/O profiles collected
```

**❌ Bad:**
```
# No profiling in production
```

**Why:** Identifies production performance issues through always-on profiling

---
