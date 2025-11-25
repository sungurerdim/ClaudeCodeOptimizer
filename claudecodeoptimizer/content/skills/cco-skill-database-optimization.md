---
name: cco-skill-database-optimization
description: Eliminate database bottlenecks through profiling, eager loading, strategic caching, and proper indexing. Includes N+1 detection, Redis caching patterns, connection pooling, EXPLAIN ANALYZE, and index optimization strategies.
keywords: [database, DB, query, slow query, performance, caching, profiling, N+1, index, optimization, Redis, query performance, database bottleneck, connection pool]
category: performance
related_commands:
  action_types: [audit, optimize, fix]
  categories: [performance, database]
pain_points: [7, 8]
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

    cursor.copy_from(buffer, 'users', columns=('name', 'email'))
    conn.commit()
```

### Batch Updates

```python
# ❌ BAD: Individual updates
for user_id, status in updates:
    db.execute("UPDATE users SET status = %s WHERE id = %s", [status, user_id])

# ✅ GOOD: Batch with VALUES
def batch_update(updates: list):
    """Updates: [(id, status), ...]"""
    query = """
    UPDATE users AS u
    SET status = v.status
    FROM (VALUES %s) AS v(id, status)
    WHERE u.id = v.id
    """
    execute_values(cursor, query, updates)
```

### Upsert (INSERT ON CONFLICT)

```sql
-- PostgreSQL upsert
INSERT INTO users (email, name, updated_at)
VALUES ('user@example.com', 'New Name', NOW())
ON CONFLICT (email)
DO UPDATE SET
    name = EXCLUDED.name,
    updated_at = EXCLUDED.updated_at;

-- MySQL upsert
INSERT INTO users (email, name, updated_at)
VALUES ('user@example.com', 'New Name', NOW())
ON DUPLICATE KEY UPDATE
    name = VALUES(name),
    updated_at = VALUES(updated_at);
```

---

## Database Partitioning

### Range Partitioning (Time-based)

```sql
-- PostgreSQL range partitioning by date
CREATE TABLE orders (
    id SERIAL,
    user_id INTEGER,
    created_at TIMESTAMP,
    total DECIMAL
) PARTITION BY RANGE (created_at);

-- Create partitions
CREATE TABLE orders_2024_q1 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

CREATE TABLE orders_2024_q2 PARTITION OF orders
    FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');

-- Queries automatically route to correct partition
SELECT * FROM orders WHERE created_at BETWEEN '2024-02-01' AND '2024-02-28';
```

### List Partitioning (By Category)

```sql
CREATE TABLE orders (
    id SERIAL,
    region TEXT,
    total DECIMAL
) PARTITION BY LIST (region);

CREATE TABLE orders_us PARTITION OF orders FOR VALUES IN ('us-east', 'us-west');
CREATE TABLE orders_eu PARTITION OF orders FOR VALUES IN ('eu-west', 'eu-central');
CREATE TABLE orders_asia PARTITION OF orders FOR VALUES IN ('ap-east', 'ap-south');
```

### Hash Partitioning (Even Distribution)

```sql
CREATE TABLE users (
    id SERIAL,
    email TEXT,
    data JSONB
) PARTITION BY HASH (id);

-- Create 4 partitions for even distribution
CREATE TABLE users_p0 PARTITION OF users FOR VALUES WITH (MODULUS 4, REMAINDER 0);
CREATE TABLE users_p1 PARTITION OF users FOR VALUES WITH (MODULUS 4, REMAINDER 1);
CREATE TABLE users_p2 PARTITION OF users FOR VALUES WITH (MODULUS 4, REMAINDER 2);
CREATE TABLE users_p3 PARTITION OF users FOR VALUES WITH (MODULUS 4, REMAINDER 3);
```

### Partition Maintenance

```sql
-- Drop old partitions (archive first if needed)
DROP TABLE orders_2022_q1;

-- Detach partition (keeps data, removes from partitioned table)
ALTER TABLE orders DETACH PARTITION orders_2023_q1;

-- Attach existing table as partition
ALTER TABLE orders ATTACH PARTITION orders_2024_q3
    FOR VALUES FROM ('2024-07-01') TO ('2024-10-01');
```

---

## Lock Management

### Understanding Locks

```sql
-- PostgreSQL: View current locks
SELECT
    locktype,
    relation::regclass,
    mode,
    granted,
    pid
FROM pg_locks
WHERE relation IS NOT NULL;

-- View blocking queries
SELECT
    blocked.pid AS blocked_pid,
    blocked.query AS blocked_query,
    blocking.pid AS blocking_pid,
    blocking.query AS blocking_query
FROM pg_stat_activity blocked
JOIN pg_locks blocked_locks ON blocked.pid = blocked_locks.pid
JOIN pg_locks blocking_locks ON blocked_locks.relation = blocking_locks.relation
JOIN pg_stat_activity blocking ON blocking_locks.pid = blocking.pid
WHERE NOT blocked_locks.granted AND blocking_locks.granted;
```

### Avoiding Deadlocks

```python
# ✅ GOOD: Consistent lock ordering
def transfer_funds(from_id: int, to_id: int, amount: Decimal):
    # Always lock in consistent order (by ID)
    first_id, second_id = sorted([from_id, to_id])

    with db.transaction():
        # Lock accounts in order
        db.execute("SELECT * FROM accounts WHERE id = %s FOR UPDATE", [first_id])
        db.execute("SELECT * FROM accounts WHERE id = %s FOR UPDATE", [second_id])

        # Perform transfer
        db.execute("UPDATE accounts SET balance = balance - %s WHERE id = %s",
                   [amount, from_id])
        db.execute("UPDATE accounts SET balance = balance + %s WHERE id = %s",
                   [amount, to_id])
```

### Advisory Locks

```python
# Application-level locking for distributed systems
def process_with_lock(resource_id: int):
    lock_id = hash(f"process:{resource_id}") % (2**31)

    # Acquire advisory lock
    cursor.execute("SELECT pg_try_advisory_lock(%s)", [lock_id])
    if not cursor.fetchone()[0]:
        raise Exception("Could not acquire lock")

    try:
        # Do work...
        process_resource(resource_id)
    finally:
        cursor.execute("SELECT pg_advisory_unlock(%s)", [lock_id])
```

### Optimistic Locking

```python
# Version-based optimistic locking
def update_user_optimistic(user_id: int, data: dict, expected_version: int):
    result = db.execute("""
        UPDATE users
        SET data = %s, version = version + 1
        WHERE id = %s AND version = %s
    """, [json.dumps(data), user_id, expected_version])

    if result.rowcount == 0:
        raise ConcurrentModificationError("User was modified by another process")
```

---

## Monitoring & Alerting

### Key Metrics to Monitor

```sql
-- PostgreSQL: Slow queries
SELECT query, calls, mean_exec_time, total_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC LIMIT 10;

-- Index usage
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read
FROM pg_stat_user_indexes
ORDER BY idx_scan ASC;

-- Table bloat
SELECT schemaname, tablename,
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size,
       n_dead_tup, n_live_tup
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC;

-- Connection stats
SELECT state, COUNT(*) FROM pg_stat_activity GROUP BY state;
```

### Alert Thresholds

| Metric | Warning | Critical |
|--------|---------|----------|
| Query time | > 1s | > 5s |
| Connection pool utilization | > 70% | > 90% |
| Cache hit ratio | < 95% | < 90% |
| Replication lag | > 1s | > 10s |
| Deadlock rate | > 0.1/min | > 1/min |
| Long-running transactions | > 5min | > 30min |

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

