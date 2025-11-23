---
name: database-optimization-caching
description: Eliminate database bottlenecks through profiling, eager loading, strategic caching, and proper indexing. Includes N+1 detection, Redis caching patterns, connection pooling, EXPLAIN ANALYZE, and index optimization strategies.
keywords: [database, DB, query, slow query, performance, caching, profiling, N+1, index, optimization, Redis, query performance, database bottleneck, connection pool]
category: performance
related_commands:
  action_types: [audit, optimize, fix]
  categories: [performance, database]
pain_points: [7, 8]
---

# Database Optimization & Caching

## Domain
Query optimization, caching, N+1 detection, profiling, indexing strategies.

## Purpose
Eliminate database bottlenecks through profiling, eager loading, strategic caching, and proper indexing.
---

## Standard Structure

**This skill follows [STANDARDS_SKILLS.md](../STANDARDS_SKILLS.md):**

- **Standard sections** - Domain, Purpose, Core Techniques, Anti-Patterns, Checklist
- **Code example format** - Bad/Good pattern with specific examples
- **Detection pattern format** - Python functions with Finding objects
- **Checklist format** - Specific, verifiable items

**See STANDARDS_SKILLS.md for format details. Only skill-specific content is documented below.**

---

## Core Techniques

### Query Optimization
- **Profile first**: Measure before optimizing (EXPLAIN ANALYZE)
- **Indexes**: Add on WHERE, JOIN, ORDER BY columns
- **Eager loading**: Prevent N+1 (JOIN, prefetch_related)
- **Pagination**: LIMIT + OFFSET for large datasets
- **Specific columns**: SELECT only needed fields
- **Connection pooling**: Reuse connections (20-50 pool size)

### Caching Strategy
- **Layers**: Browser → CDN → App cache (Redis) → Query cache
- **TTL**: 1min (volatile) to 1hr (stable) based on update frequency
- **Cache-aside**: Check cache → miss → fetch DB → populate cache
- **Invalidation**: Delete cache on writes

### N+1 Detection
- **Problem**: 1 query + N queries in loop (1000 users = 1001 queries)
- **Detection**: Query count grows with data size
- **Solution**: Eager loading (1 query with JOIN)

### Indexing
- **Single-column**: Filtered columns (user_id, email, status)
- **Composite**: Multi-column queries (user_id, created_at)
- **Partial**: Subset only (WHERE status = 'active')
- **Monitor**: Check idx_scan in pg_stat_user_indexes

---

## Patterns

### N+1 Fix
```python
# ❌ BAD: 1001 queries
users = User.objects.all()
for user in users:
    orders = user.orders.all()  # N queries

# ✅ GOOD: 1 query
users = User.objects.prefetch_related('orders')
for user in users:
    orders = user.orders.all()  # No query
```

### Indexing
```sql
-- Slow queries
SELECT query, mean_exec_time FROM pg_stat_statements
WHERE mean_exec_time > 100 ORDER BY mean_exec_time DESC LIMIT 10;

-- Add indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_user_created ON orders(user_id, created_at DESC);
CREATE INDEX idx_users_active ON users(email) WHERE status = 'active';
```

### Redis Caching
```python
def cache(ttl=300):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = f"{func.__name__}:{json.dumps(args)}"
            cached = redis_client.get(key)
            if cached:
                return json.loads(cached)
            result = func(*args, **kwargs)
            redis_client.setex(key, ttl, json.dumps(result))
            return result
        return wrapper
    return decorator

@cache(ttl=300)
def get_user_stats(user_id):
    return db.query("SELECT COUNT(*), SUM(total) FROM orders WHERE user_id = %s", user_id)
```

### Cache Invalidation
```python
def update_user(user_id, data):
    db.execute("UPDATE users SET ... WHERE id = %s", user_id)
    redis_client.delete(f"user:{user_id}")
```

### Connection Pooling
```python
engine = create_engine(
    "postgresql://user:pass@localhost/db",
    pool_size=20, max_overflow=10, pool_timeout=30, pool_pre_ping=True
)
```

---

## Checklist

### Before Optimization
- [ ] Profile queries (EXPLAIN ANALYZE, slow query log)
- [ ] Identify N+1 (query count grows with data)
- [ ] Check index usage (pg_stat_user_indexes)

### Optimization
- [ ] Add indexes on filtered/joined columns
- [ ] Use eager loading (prefetch_related, joinedload)
- [ ] Implement caching (Redis with TTL)
- [ ] Add connection pooling
- [ ] Paginate large results

### Validation
- [ ] Verify query count reduced
- [ ] Check index usage (idx_scan > 0)
- [ ] Measure response time improvement
- [ ] Monitor cache hit rate

## Command Discovery Protocol

When this skill is active, find relevant commands by searching `~/.claude/commands/` metadata:

```yaml
# Search criteria for this skill's domain
action_types: [audit, optimize, fix]
keywords: [database, query, N+1, cache, index, performance]
category: performance
pain_points: [7, 8]
```

**How Claude finds commands:**
1. Grep command files for `keywords:.*[pattern]` in frontmatter
2. Match `category: performance`
3. Present matching commands with their parameters

This ensures commands are always current even when renamed or updated.
