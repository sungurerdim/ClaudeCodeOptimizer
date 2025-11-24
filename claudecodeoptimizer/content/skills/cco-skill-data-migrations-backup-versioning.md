---
name: data-migrations-backup-versioning
description: Execute zero-downtime schema changes, implement comprehensive backup/DR strategies, manage data lifecycle. Includes 5-phase migration approach, PITR backup, soft deletes, GDPR compliance, and online DDL patterns.
keywords: [migration, database migration, schema change, backup, disaster recovery, zero downtime, rollback, RTO, RPO, GDPR, soft delete, retention]
category: database
related_commands:
  action_types: [generate, audit, fix]
  categories: [database]
pain_points: [7, 8, 10]
---

# Data Migrations, Backup & Versioning

> **Standards:** Format defined in [STANDARDS_SKILLS.md](../STANDARDS_SKILLS.md)  
> **Discovery:** See [STANDARDS_COMMANDS.md](../STANDARDS_COMMANDS.md#18-command-discovery-protocol)


---

---

## Domain
Production database migrations, backup/disaster recovery, retention policies, schema versioning.

## Purpose
Execute zero-downtime schema changes, implement comprehensive backup/DR strategies, manage data lifecycle.

## Core Techniques

### Zero-Downtime Migrations
**5-Phase Approach (Column Rename):**
1. Add new column (keep old)
2. Dual-write both columns
3. Backfill old → new
4. Switch reads to new
5. Drop old column

**Rules:**
- Additive only (never drop directly)
- Backward compatible (old code works)
- Online DDL (no table locks)
- Rollback script always
- Sequential versioning (001_*, 002_*)

### Backup Strategy
- **Full**: Daily snapshot (2 AM)
- **Incremental**: Hourly changes
- **PITR**: WAL/binlog archives
- **Verification**: Monthly restore tests
- **Off-Site**: Different region/cloud
- **Retention**: 30d daily, 12mo monthly, 7yr annual

### Disaster Recovery
- **RTO**: Max downtime (e.g., 1 hour)
- **RPO**: Max data loss (e.g., 15 min)
- **Hot Standby**: Real-time replica (failover ready)
- **DR Testing**: Quarterly drills
- **Runbook**: Step-by-step recovery

### Data Retention
- **Soft Deletes**: deleted_at timestamp (audit trail)
- **Archival**: Old data → cold storage (S3)
- **TTL Cleanup**: Auto-delete expired (sessions)
- **GDPR**: Hard delete PII after retention period
- **Audit Logs**: Immutable, 7yr compliance

## Patterns

### Zero-Downtime Column Rename
```sql
-- Phase 1: Add
ALTER TABLE users ADD COLUMN email_address VARCHAR(255);

-- Phase 2: Dual-write (app code)
-- user.email = val; user.email_address = val

-- Phase 3: Backfill
UPDATE users SET email_address = email WHERE email_address IS NULL;

-- Phase 4: Switch reads (app code)
-- return user.email_address

-- Phase 5: Drop (after monitoring)
ALTER TABLE users DROP COLUMN email;
```

### Backup Script (PostgreSQL)
```bash
#!/bin/bash
DB="production"
DIR="/backups/postgres"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup + compress
pg_dump -U postgres -d $DB -F c -f "$DIR/full_$DATE.dump"
gzip "$DIR/full_$DATE.dump"

# Upload off-site
aws s3 cp "$DIR/full_$DATE.dump.gz" s3://backups/postgres/

# Cleanup (30 days)
find $DIR -name "full_*.dump.gz" -mtime +30 -delete

# Verify
pg_restore --list "$DIR/full_$DATE.dump.gz" > /dev/null || \
  echo "BACKUP FAILED!" | mail -s "Alert" {ONCALL_EMAIL}
```

### Soft Delete Pattern
```python
class User(db.Model):
    deleted_at = db.Column(db.DateTime, nullable=True)

    def soft_delete(self):
        self.deleted_at = datetime.utcnow()
        db.session.commit()

    @classmethod
    def active(cls):
        return cls.query.filter(cls.deleted_at.is_(None))
```

### TTL-Based Cleanup
```python
# Hourly cleanup job
def cleanup_expired_sessions():
    deleted = Session.query.filter(Session.expires_at < datetime.utcnow()).delete()
    db.session.commit()
```

### GDPR Erasure
```python
def erase_user_data(user_id: int):
    user = User.query.get(user_id)
    if datetime.utcnow() - user.deleted_at < timedelta(days=30):
        raise ValueError("Retention period not elapsed")

    user.email = f"deleted_{user.id}@{DOMAIN}"
    user.name = "Deleted User"
    AuditLog.create(action="gdpr_erasure", user_id=user_id)
    db.session.commit()
```

### Online DDL (No Locks)
```sql
-- PostgreSQL: CONCURRENTLY
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);

-- MySQL: ALGORITHM=INPLACE, LOCK=NONE
ALTER TABLE users ADD COLUMN email VARCHAR(255), ALGORITHM=INPLACE, LOCK=NONE;
```

## Anti-Patterns
```sql
-- ❌ Direct drop (breaking change)
ALTER TABLE users DROP COLUMN email;

-- ❌ Table lock on large table
ALTER TABLE users ADD COLUMN email VARCHAR(255);  -- Locks for hours!

-- ❌ No rollback script

-- ❌ Editing applied migration (breaks checksum)

-- ✅ Use online DDL
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
```

## Checklist

### Pre-Migration
- [ ] Backward-compatible (old code works)
- [ ] Tested on staging (production-size data)
- [ ] Online DDL (no locks)
- [ ] Rollback script tested
- [ ] Monitoring ready (duration, errors)
- [ ] Backup taken before migration

### Backup/DR
- [ ] Daily full backups automated
- [ ] PITR enabled (WAL archiving)
- [ ] Off-site replication configured
- [ ] Monthly restore tests
- [ ] RTO/RPO documented
- [ ] DR tested quarterly

### Retention
- [ ] Soft deletes implemented
- [ ] Retention policies documented
- [ ] GDPR compliance (PII deletion)
- [ ] Audit logs immutable

