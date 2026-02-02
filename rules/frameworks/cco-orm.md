# ORM Frameworks
*Cross-ORM gotchas that cause production incidents*

## N+1 Query Detection

- **The trap**: Accessing a relation in a loop fires one query per row. This is the #1 ORM performance killer
- **Prisma**: `findMany()` returns no relations by default (safe), but `include: { posts: true }` inside a loop still N+1s. Use nested `include` in the top-level query
- **TypeORM/Sequelize**: Lazy-loaded relations (`@ManyToOne(() => User)`) trigger on property access. Use `relations: ['user']` in find options or `leftJoinAndSelect` in QueryBuilder
- **SQLAlchemy**: Default `lazy='select'` fires per-access. Fix with `joinedload()`, `selectinload()`, or set `lazy='selectin'` on the relationship. Use `echo=True` or SQLAlchemy event hooks to count queries in tests
- **Drizzle**: Explicit by design (no lazy loading), but `db.query.*.findMany({ with: {} })` in a loop still causes N+1. Restructure to single query with `with` clause
- **Diesel**: Compile-time safe -- no implicit lazy loading. But `.load()` in a loop is still N+1. Use `belonging_to()` for batch loading associations

## Migration Footguns

- **Data loss on column rename**: Most ORMs generate DROP + ADD instead of RENAME. Always review generated SQL. Prisma: check `migrate diff`. Alembic: manually write `op.alter_column()`
- **Lock contention on large tables**: `ALTER TABLE ADD COLUMN` with a default value locks the entire table in PostgreSQL <11 and MySQL. Add column as nullable first, backfill, then add constraint
- **Concurrent index creation**: `CREATE INDEX` locks writes. Use `CREATE INDEX CONCURRENTLY` (Postgres) or `ALGORITHM=INPLACE` (MySQL). Most ORMs don't generate this -- write the migration manually
- **Migration ordering in teams**: Two developers create migration 005. Merge conflict in migration history causes "migration already applied" errors. Use timestamp-based naming (Alembic default) instead of sequential numbering
- **Don't sync schema to prod**: TypeORM `synchronize: true`, Prisma `db push` -- these skip migration history and may drop columns silently. Migrations only in production

## Connection Pool Exhaustion

- **Singleton client**: Create ONE client/pool instance per process. Prisma: single `PrismaClient`. SQLAlchemy: single `engine`. Multiple instances = multiple pools = connection leak
- **Long transactions hold connections**: A transaction open during an HTTP request holds a pool connection for the entire request lifetime. Keep transactions short; don't do external API calls inside them
- **Pool size vs database limit**: Default pool sizes (Prisma: 5 per instance, SQLAlchemy: 5) multiply across instances. 20 serverless functions x 5 connections = 100 connections. Use `pgbouncer` or similar pooler for serverless
- **Unreturned connections**: Forgetting `session.close()` / not using `with` blocks leaks connections. Always use context managers: `with Session(engine) as session:`

## Lazy Loading Surprises

- **Serialization triggers all relations**: `JSON.stringify(entity)` or returning an entity from an API triggers lazy-loaded getters, firing dozens of queries. Always map to DTOs with explicit fields
- **Lazy load outside session/context**: SQLAlchemy `DetachedInstanceError`, TypeORM queries after connection close. Either eagerly load what you need, or keep the session alive through serialization
- **Implicit lazy in nested relations**: Loading `user.posts` eagerly but `post.comments` lazily -- the N+1 moves one level deeper. Audit the full object graph you're serializing
