---
name: cco-skill-database-optimization
description: Eliminate database bottlenecks through profiling, eager loading, strategic caching, and proper indexing. Includes N+1 detection, Redis caching patterns, connection pooling, EXPLAIN ANALYZE, and index optimization strategies.
keywords: [database, DB, query, slow query, performance, caching, profiling, N+1, index, optimization, Redis, query performance, database bottleneck, connection pool]
category: performance
related_commands:
  action_types: [audit, optimize, fix]
  categories: [performance, database]
pain_points: [5, 7]
---

# Database Optimization & Caching

> **Standards:** Format defined in [cco-standards.md](../cco-standards.md)  
> **Discovery:** See [cco-standards.md](../cco-standards.md#18-command-discovery-protocol)


## Domain
Query optimization, caching, N+1 detection, profiling, indexing strategies.

## Purpose
Eliminate database bottlenecks through profiling, eager loading, strategic caching, and proper indexing.
---

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

## Advanced Index Strategies

### Index Types by Use Case

| Index Type | Use Case | PostgreSQL | MySQL |
|------------|----------|------------|-------|
| **B-tree** | Equality, range, sorting | DEFAULT | DEFAULT |
| **Hash** | Equality only (=) | `USING HASH` | N/A (InnoDB uses B-tree) |
| **GIN** | Full-text, arrays, JSONB | `USING GIN` | FULLTEXT |
| **GiST** | Geometric, range types | `USING GIST` | SPATIAL |
| **BRIN** | Large sequential data | `USING BRIN` | N/A |

### B-tree Index (Default)
```sql
-- Best for: equality (=), range (<, >, BETWEEN), sorting (ORDER BY)
-- Column order matters for composite indexes

-- Good: leftmost columns used
CREATE INDEX idx_orders_user_status ON orders(user_id, status, created_at);

-- ✅ Uses index (leftmost prefix)
SELECT * FROM orders WHERE user_id = 123;
SELECT * FROM orders WHERE user_id = 123 AND status = 'active';
SELECT * FROM orders WHERE user_id = 123 ORDER BY created_at;

-- ❌ Doesn't use index (skips leftmost)
SELECT * FROM orders WHERE status = 'active';
SELECT * FROM orders WHERE created_at > '2024-01-01';
```

### Hash Index (Equality Only)
```sql
-- Best for: exact match lookups only
-- NOT for: range queries, sorting

CREATE INDEX idx_users_email_hash ON users USING HASH (email);

-- ✅ Uses hash index
SELECT * FROM users WHERE email = 'user@example.com';

-- ❌ Cannot use hash index
SELECT * FROM users WHERE email LIKE '%@example.com';
SELECT * FROM users ORDER BY email;
```

### GIN Index (Arrays, JSONB, Full-text)
```sql
-- Best for: containment queries, full-text search, JSONB

-- Array containment
CREATE INDEX idx_posts_tags ON posts USING GIN (tags);
SELECT * FROM posts WHERE tags @> ARRAY['python', 'database'];

-- JSONB queries
CREATE INDEX idx_users_metadata ON users USING GIN (metadata jsonb_path_ops);
SELECT * FROM users WHERE metadata @> '{"role": "admin"}';

-- Full-text search
CREATE INDEX idx_articles_content ON articles USING GIN (to_tsvector('english', content));
SELECT * FROM articles WHERE to_tsvector('english', content) @@ to_tsquery('database & optimization');
```

### GiST Index (Geometric, Range)
```sql
-- Best for: range types, geometric data, nearest neighbor

-- Range queries
CREATE INDEX idx_events_during ON events USING GIST (during);
SELECT * FROM events WHERE during && '[2024-01-01, 2024-01-31]'::daterange;

-- Geographic data (PostGIS)
CREATE INDEX idx_locations_geom ON locations USING GIST (geom);
SELECT * FROM locations WHERE ST_DWithin(geom, ST_MakePoint(-73.9857, 40.7484), 1000);
```

### BRIN Index (Large Sequential Data)
```sql
-- Best for: large tables with natural ordering (time-series, logs)
-- Much smaller than B-tree, good for append-only tables

CREATE INDEX idx_logs_created ON logs USING BRIN (created_at);

-- Effective when data is physically ordered by indexed column
-- Less effective for random access patterns
```

### Partial Indexes
```sql
-- Index only subset of rows (smaller, faster)

-- Only active users
CREATE INDEX idx_users_active ON users(email) WHERE status = 'active';

-- Only recent orders
CREATE INDEX idx_orders_recent ON orders(user_id, created_at)
WHERE created_at > CURRENT_DATE - INTERVAL '90 days';

-- Only non-null values
CREATE INDEX idx_users_phone ON users(phone) WHERE phone IS NOT NULL;
```

### Expression Indexes
```sql
-- Index computed expressions

CREATE INDEX idx_users_lower_email ON users(LOWER(email));
SELECT * FROM users WHERE LOWER(email) = 'user@example.com';

CREATE INDEX idx_orders_year ON orders(EXTRACT(YEAR FROM created_at));
SELECT * FROM orders WHERE EXTRACT(YEAR FROM created_at) = 2024;
```

### Covering Indexes (Index-Only Scans)
```sql
-- Include non-indexed columns to avoid table lookup

CREATE INDEX idx_orders_user_covering ON orders(user_id) INCLUDE (status, total);

-- Query can be satisfied from index alone (no heap fetch)
SELECT status, total FROM orders WHERE user_id = 123;
```

---

## Connection Pooling Deep Dive

### Why Connection Pooling?
- **Problem**: Opening DB connection = 10-50ms overhead
- **Solution**: Reuse existing connections from pool
- **Benefit**: Requests use < 1ms to acquire connection

### Pool Configuration

```python
# SQLAlchemy (Python)
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://user:pass@localhost/db",

    # Core pool settings
    pool_size=20,          # Maintained connections
    max_overflow=10,       # Extra connections under load
    pool_timeout=30,       # Wait time for connection
    pool_recycle=1800,     # Recycle connections after 30min
    pool_pre_ping=True,    # Verify connection health

    # Performance
    echo=False,            # Disable SQL logging in production
    echo_pool=False,       # Disable pool logging
)

# Connection lifecycle
with engine.connect() as conn:
    result = conn.execute(text("SELECT 1"))
    # Connection automatically returned to pool
```

```javascript
// Node.js (pg-pool)
const { Pool } = require('pg');

const pool = new Pool({
    host: 'localhost',
    database: 'mydb',
    user: 'user',
    password: 'pass',

    // Pool settings
    max: 20,                    // Maximum connections
    min: 5,                     // Minimum idle connections
    idleTimeoutMillis: 30000,   // Close idle after 30s
    connectionTimeoutMillis: 2000, // Acquire timeout
    maxUses: 7500,              // Close after N queries
});

// Usage
const result = await pool.query('SELECT * FROM users WHERE id = $1', [userId]);
```

```go
// Go (database/sql)
import (
    "database/sql"
    _ "github.com/lib/pq"
)

db, err := sql.Open("postgres", connStr)

// Pool configuration
db.SetMaxOpenConns(25)           // Max open connections
db.SetMaxIdleConns(5)            // Max idle connections
db.SetConnMaxLifetime(5 * time.Minute) // Max connection age
db.SetConnMaxIdleTime(1 * time.Minute) // Max idle time
```

### Pool Sizing Formula

```
Optimal Pool Size = (core_count * 2) + effective_spindle_count

For SSD/NVMe: core_count * 2 to 4
For HDD: core_count * 2 + spindle_count
```

**Common recommendations:**
- **Small app**: 5-10 connections
- **Medium app**: 20-50 connections
- **High traffic**: 50-100 connections per instance
- **Microservices**: 5-20 per service (many services share DB)

### Connection Pool Monitoring

```sql
-- PostgreSQL: Active connections
SELECT state, COUNT(*)
FROM pg_stat_activity
GROUP BY state;

-- Waiting connections
SELECT COUNT(*) FROM pg_stat_activity WHERE wait_event_type IS NOT NULL;

-- Connection limits
SHOW max_connections;
```

### Connection Pool Anti-Patterns

```python
# ❌ BAD: Creating connection per request
def get_user(user_id):
    conn = psycopg2.connect(...)  # New connection each time!
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    return cursor.fetchone()

# ✅ GOOD: Use connection pool
def get_user(user_id):
    with pool.connection() as conn:  # Reuse from pool
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        return cursor.fetchone()
```

---

## Query Analysis with EXPLAIN

### EXPLAIN Basics

```sql
-- Basic plan
EXPLAIN SELECT * FROM users WHERE email = 'user@example.com';

-- With execution statistics (actually runs query)
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'user@example.com';

-- Full details
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM users WHERE email = 'user@example.com';

-- JSON format for tooling
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT * FROM users WHERE email = 'user@example.com';
```

### Understanding EXPLAIN Output

```sql
EXPLAIN ANALYZE SELECT * FROM orders o
JOIN users u ON o.user_id = u.id
WHERE u.status = 'active' AND o.created_at > '2024-01-01';

-- Output:
Hash Join  (cost=123.45..567.89 rows=100 width=200) (actual time=1.234..5.678 rows=95 loops=1)
  Hash Cond: (o.user_id = u.id)
  ->  Index Scan using idx_orders_created on orders o  (cost=0.42..300.00 rows=1000 width=100) (actual time=0.020..2.000 rows=950 loops=1)
        Index Cond: (created_at > '2024-01-01'::timestamp)
  ->  Hash  (cost=100.00..100.00 rows=50 width=100) (actual time=1.000..1.000 rows=48 loops=1)
        Buckets: 1024  Batches: 1  Memory Usage: 10kB
        ->  Seq Scan on users u  (cost=0.00..100.00 rows=50 width=100) (actual time=0.010..0.900 rows=48 loops=1)
              Filter: (status = 'active')
              Rows Removed by Filter: 952
Planning Time: 0.150 ms
Execution Time: 5.800 ms
```

### Key Metrics to Watch

| Metric | Good | Bad | Action |
|--------|------|-----|--------|
| **Seq Scan** | Small tables | Large tables | Add index |
| **rows** estimate vs actual | Within 10x | Off by 100x+ | ANALYZE table |
| **Buffers** shared hit vs read | High hit ratio | Many reads | Increase shared_buffers |
| **Sort Method** | quicksort | external merge | Increase work_mem |

### Common Plan Nodes

```
Seq Scan          → Full table scan (no index)
Index Scan        → Index + table lookup
Index Only Scan   → Index only (covering index)
Bitmap Index Scan → Multiple index ranges combined
Nested Loop       → Loop join (good for small right table)
Hash Join         → Hash table join (good for equality)
Merge Join        → Sorted join (good for pre-sorted data)
Sort              → Sorting (may spill to disk)
Aggregate         → GROUP BY, COUNT, SUM
```

### EXPLAIN Checklist

- [ ] No Seq Scan on large tables (add index)
- [ ] Row estimates close to actual (run ANALYZE)
- [ ] No external merge sorts (increase work_mem)
- [ ] Buffer hit ratio > 99% (check shared_buffers)
- [ ] No excessive loops in nested loop joins

---

## Advanced Caching Patterns

### Cache-Aside (Lazy Loading)

```python
def get_user(user_id: int) -> dict:
    """Standard cache-aside pattern."""
    cache_key = f"user:{user_id}"

    # Check cache first
    cached = redis.get(cache_key)
    if cached:
        return json.loads(cached)

    # Cache miss: fetch from DB
    user = db.query("SELECT * FROM users WHERE id = %s", [user_id])
    if user:
        redis.setex(cache_key, 300, json.dumps(user))  # TTL: 5 min

    return user
```

### Write-Through Cache

```python
def update_user(user_id: int, data: dict) -> dict:
    """Write to DB and cache simultaneously."""
    # Update database
    db.execute("UPDATE users SET ... WHERE id = %s", [user_id])

    # Update cache immediately
    cache_key = f"user:{user_id}"
    updated_user = db.query("SELECT * FROM users WHERE id = %s", [user_id])
    redis.setex(cache_key, 300, json.dumps(updated_user))

    return updated_user
```

### Write-Behind (Write-Back) Cache

```python
# For high-write scenarios: buffer writes in cache, batch to DB

class WriteBackCache:
    def __init__(self, flush_interval=5):
        self.buffer = {}
        self.flush_interval = flush_interval

    def set(self, key: str, value: dict):
        """Buffer write in cache."""
        redis.set(key, json.dumps(value))
        self.buffer[key] = value

    async def flush(self):
        """Batch flush to database."""
        if not self.buffer:
            return

        # Bulk insert/update
        db.bulk_upsert("users", list(self.buffer.values()))
        self.buffer.clear()
```

### Cache Stampede Prevention

```python
import threading

class StampedeProtectedCache:
    def __init__(self):
        self.locks = {}

    def get_or_set(self, key: str, fetch_func, ttl: int = 300):
        """Prevent cache stampede with locking."""
        cached = redis.get(key)
        if cached:
            return json.loads(cached)

        # Acquire lock for this key
        lock_key = f"lock:{key}"
        lock = self.locks.setdefault(key, threading.Lock())

        with lock:
            # Double-check after acquiring lock
            cached = redis.get(key)
            if cached:
                return json.loads(cached)

            # Only one thread fetches from DB
            result = fetch_func()
            redis.setex(key, ttl, json.dumps(result))
            return result
```

### Distributed Caching with Redis Cluster

```python
from redis.cluster import RedisCluster

# Redis Cluster for horizontal scaling
rc = RedisCluster(
    startup_nodes=[
        {"host": "redis1", "port": 6379},
        {"host": "redis2", "port": 6379},
        {"host": "redis3", "port": 6379},
    ],
    decode_responses=True,
    skip_full_coverage_check=True,
)

# Keys automatically sharded across nodes
rc.set("user:123", json.dumps(user_data))
```

### Cache Invalidation Patterns

```python
# 1. Direct invalidation
def delete_user(user_id: int):
    db.execute("DELETE FROM users WHERE id = %s", [user_id])
    redis.delete(f"user:{user_id}")

# 2. Pattern invalidation (careful - can be slow)
def invalidate_user_caches(user_id: int):
    keys = redis.keys(f"user:{user_id}:*")  # All user-related keys
    if keys:
        redis.delete(*keys)

# 3. Tag-based invalidation
def set_with_tags(key: str, value: dict, tags: list, ttl: int = 300):
    redis.setex(key, ttl, json.dumps(value))
    for tag in tags:
        redis.sadd(f"tag:{tag}", key)

def invalidate_tag(tag: str):
    keys = redis.smembers(f"tag:{tag}")
    if keys:
        redis.delete(*keys)
    redis.delete(f"tag:{tag}")
```

---

## Bulk Operations

### Batch Inserts

```python
# ❌ BAD: Individual inserts (slow)
for user in users:
    db.execute("INSERT INTO users (name, email) VALUES (%s, %s)",
               [user['name'], user['email']])

# ✅ GOOD: Batch insert
def batch_insert(users: list, batch_size: int = 1000):
    for i in range(0, len(users), batch_size):
        batch = users[i:i + batch_size]
        values = [(u['name'], u['email']) for u in batch]
        execute_values(cursor,
            "INSERT INTO users (name, email) VALUES %s", values)
        conn.commit()
```

### COPY for Large Data Loads

```python
# PostgreSQL COPY - fastest bulk load
import io

def bulk_load_users(users: list):
    # Create CSV-like buffer
    buffer = io.StringIO()
    for user in users:
        buffer.write(f"{user['name']}\t{user['email']}\n")
    buffer.seek(0)

---

## Checklist

### Query Optimization
- [ ] N+1 queries detected and fixed (eager loading)
- [ ] EXPLAIN ANALYZE on slow queries
- [ ] Proper indexes for WHERE clauses
- [ ] No SELECT * (specify columns)

### Indexing
- [ ] Foreign keys indexed
- [ ] Frequent WHERE columns indexed
- [ ] Composite indexes for multi-column queries
- [ ] EXPLAIN shows index usage (no seq scan)

### Caching
- [ ] Hot data cached (Redis/Memcached)
- [ ] Cache invalidation strategy
- [ ] TTL set appropriately
- [ ] Cache stampede prevention

### Connection Pooling
- [ ] Pool configured (not per-request connections)
- [ ] Pool size tuned for workload
- [ ] Idle connection timeout set
- [ ] Connection pool monitoring
