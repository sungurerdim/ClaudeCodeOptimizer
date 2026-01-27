# Database Rules
*Security and performance essentials*

## SQL [CRITICAL]

| Requirement | Implementation |
|-------------|----------------|
| Queries | Parameterized ALWAYS (no string concat) |
| Connection Pool | Size = (connections / app instances) |
| Statement Timeout | Set explicit timeout |
| Indexes | On WHERE, JOIN, ORDER BY columns |

### Transactions
- Explicit for multi-statement operations
- Default: READ COMMITTED isolation
- Consistent lock ordering (prevent deadlock)

### Migrations
- Forward-only in production
- Atomic and reversible in development
- Track schema version in database

---

## NoSQL

- Application-level schema validation
- TTL for expiring data
- Batch operations when possible

---

## Vector DB

| Parameter | Consideration |
|-----------|---------------|
| Embedding Model | Must match index and query |
| Index Type | HNSW (fast), IVF (scalable) |
| Similarity | Cosine (normalized), L2 (raw) |

---

## Edge/Embedded

- Sync strategy: local-first vs server-authoritative
- Conflict resolution for concurrent writes
- Offline read/write capability
