# Database Specialized
*Database-specific rules and patterns*

## SQL (DB:SQL)
**Trigger:** {sql_drivers}

### Security & Performance
- **Parameterized**: Parameterized queries always (prevent SQL injection)
- **Connection-Pool**: Connection pooling with appropriate pool size
- **Index-Query**: Index for common queries, composite indexes for multi-column filters

### Transactions
- **Transaction-Explicit**: Explicit transactions for multi-statement operations
- **Isolation-Level**: Choose appropriate isolation level (READ COMMITTED default)
- **Deadlock-Prevent**: Consistent lock ordering to prevent deadlocks
- **Timeout-Set**: Set statement timeout to prevent long-running queries

### Migrations
- **Migration-Forward**: Forward-only migrations, no rollback in production
- **Migration-Atomic**: Each migration should be atomic and reversible in development
- **Schema-Version**: Track schema version in database

## NoSQL (DB:NoSQL)
**Trigger:** {nosql_deps}

- **Schema-Validate**: Application-level schema validation
- **TTL-Set**: TTL for expiring data
- **Consistency-Choose**: Choose consistency level
- **Batch-Ops**: Batch operations when possible

## Vector DB (DB:Vector)
**Trigger:** {vector_deps}

- **Embed-Model**: Consistent embedding model
- **Dimension-Match**: Dimension consistency
- **Index-Type**: Appropriate index type (HNSW, IVF)
- **Similarity-Metric**: Correct similarity metric

## Edge/Embedded DB (DB:Edge)
**Trigger:** {edge_db_deps}

- **Sync-Strategy**: Configure sync strategy (local-first, server-authoritative)
- **Offline-Capable**: Handle offline reads and writes gracefully
- **Conflict-Resolution**: Define conflict resolution for concurrent writes
- **Connection-Mode**: Choose embedded vs remote connection mode
- **Migration-Portable**: Portable migration scripts across environments
- **Query-Local**: Optimize for local query latency
- **Replica-Sync**: Configure replica synchronization interval

---

## Database Operations
**Trigger:** DB:* (auto-applied when any DB:* detected)

- **Backup-Strategy**: Automated backups with tested restore
- **Schema-Versioned**: Migration files with rollback plan
- **Connection-Secure**: SSL/TLS, credentials in env vars
- **Query-Timeout**: Prevent runaway queries
