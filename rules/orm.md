# ORM Frameworks
*Object-Relational Mapping framework rules*

## Prisma (ORM:Prisma)
**Trigger:** {prisma_deps}

- **Schema-Single**: Single schema.prisma file as source of truth
- **Client-Generate**: Run prisma generate after schema changes
- **Client-Singleton**: Single PrismaClient instance
- **Select-Fields**: Use select/include to limit fields
- **Batch-Transactions**: Use $transaction for batching

## Drizzle (ORM:Drizzle)
**Trigger:** {drizzle_deps}

- **Schema-TypeSafe**: Define schema with full TypeScript
- **Query-Builder**: Prefer query builder over raw SQL
- **Migrations-Generate**: Use drizzle-kit for migrations
- **Relations-Explicit**: Define relations explicitly
- **Prepared-Statements**: Use prepared statements for performance

## TypeORM (ORM:TypeORM)
**Trigger:** {typeorm_deps}

- **Entities-Decorators**: Use decorator-based entities
- **Repository-Pattern**: Use repository pattern
- **Migrations-Generate**: Generate migrations, don't sync in prod
- **Relations-Lazy**: Consider lazy relations for performance
- **Query-Builder**: Use QueryBuilder for complex queries

## Sequelize (ORM:Sequelize)
**Trigger:** {sequelize_deps}

- **Models-Define**: Define models with sequelize.define or class
- **Associations-Setup**: Setup associations in associate method
- **Migrations-Umzug**: Use umzug for production migrations
- **Scopes-Use**: Use scopes for reusable queries
- **Hooks-Lifecycle**: Use hooks for lifecycle events

## SQLAlchemy (ORM:SQLAlchemy)
**Trigger:** {sqlalchemy_deps}

- **Session-Scoped**: Use scoped_session for web apps
- **Engine-Pool**: Configure connection pool size
- **Declarative-Base**: Use declarative_base for models
- **Alembic-Migrate**: Use Alembic for migrations
- **Lazy-Load-Aware**: Be aware of N+1 with lazy loading

## Diesel (ORM:Diesel)
**Trigger:** {diesel_deps}

- **Schema-Infer**: Use diesel print-schema for schema.rs
- **Migrations-Embed**: Embed migrations with embed_migrations!
- **Derive-Queryable**: Use #[derive(Queryable)] for structs
- **Connection-Pool**: Use r2d2 for connection pooling
- **Type-Safe**: Leverage Rust's type system for query safety
