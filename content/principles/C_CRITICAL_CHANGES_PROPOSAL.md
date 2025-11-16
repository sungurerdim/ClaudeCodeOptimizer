---
id: C_CRITICAL_CHANGES_PROPOSAL
title: Critical Changes Require Proposal
category: claude-guidelines
severity: high
weight: 8
applicability:
  project_types: ['all']
  languages: ['all']
---

# C_CRITICAL_CHANGES_PROPOSAL: Critical Changes Require Proposal 🔴

**Severity**: High

Always submit proposals before making critical changes like adding dependencies, modifying infrastructure, affecting many files, or implementing security features. Give users decision control and opportunity to discuss alternatives before implementation.

**Enforcement**: MUST

**Project Types**: all
**Languages**: all

---

## Why

### The Problem

**Critical changes without proposals waste time and create risk:**

- **Wrong Direction** - Implementing wrong solution wastes hours; proposal catches mistakes early
- **Wasted Effort** - User may have different preferred approach; implementation effort lost
- **Missed Alternatives** - Better solutions exist but not considered; opportunity missed
- **Lack of Oversight** - Critical decisions made without user knowledge or approval
- **Technical Debt** - Suboptimal architectural choices locked in without discussion
- **Team Misalignment** - Changes conflict with undocumented team plans or preferences
- **Resource Waste** - Dependencies, infrastructure changes, or architecture decisions require careful consideration

### Core Techniques

**1. Identify Critical Changes Before Implementation**

```python
# ❌ BAD: Add dependency without proposal
# User: "Speed up JSON processing"
Bash("pip install orjson")  # Added dependency without asking!
Edit("requirements.txt", ..., new_string="...\norjson==3.9.0")

# ✅ GOOD: Propose dependency addition first
# User: "Speed up JSON processing"

"""
CRITICAL CHANGE PROPOSAL:

**Change**: Add orjson library for faster JSON parsing
**Reason**: Current json.loads() is bottleneck (profiling shows 45% of request time)

**Impact**:
- Files: 3 (requirements.txt, api.py, serializers.py)
- New dependency: orjson==3.9.0 (170KB, maintained by active project)
- Breaking: no (drop-in replacement for json.loads/dumps)

**Alternatives considered**:
1. Use orjson (5-10x faster) ← Recommended
2. Use ujson (3-5x faster, less maintained)
3. Optimize current code (limited gains)

**Risks**:
- New dependency to maintain
- Slightly different error messages (minor compatibility)

**Benefits**:
- 5-10x faster JSON parsing
- Reduced CPU usage
- Better response times

Proceed with adding orjson? (yes/no)
"""
```

**2. Use Proposal Template for Consistency**

```markdown
# ✅ GOOD: Complete proposal template

CRITICAL CHANGE PROPOSAL:

**Change**: [One sentence description]
**Reason**: [Why is this needed? What problem does it solve?]

**Impact**:
- Files affected: [X files: list main ones]
- Dependencies: [New/updated dependencies]
- Infrastructure: [Environment changes, new services]
- Breaking: [yes/no]

**Alternatives Considered**:
1. [Option 1] ← Recommended
2. [Option 2]
3. [Option 3]

**Risks**:
- [Risk 1]
- [Risk 2]

**Benefits**:
- [Benefit 1]
- [Benefit 2]

**Testing Strategy**:
- [How will this be tested?]

**Rollback Plan**:
- [How to rollback if needed?]

Proceed? (yes/no)
```

**3. Propose Alternatives with Trade-offs**

```python
# ✅ GOOD: Propose multiple options with trade-offs

# User: "Add caching to improve performance"

"""
CRITICAL CHANGE PROPOSAL: Caching Strategy

**Problem**: Database queries slow (500ms avg), need caching

**Option 1: Redis (Recommended)**
- Pros: Fast (1-5ms), distributed, persistent, battle-tested
- Cons: New infrastructure dependency, ~100MB memory minimum
- Impact: Add Redis container, update 4 files
- Cost: ~$10/month (managed Redis) or free (self-hosted)

**Option 2: In-Memory (Python dict)**
- Pros: Zero dependencies, instant setup, simple
- Cons: Lost on restart, not shared across workers, memory limited
- Impact: Update 2 files only
- Cost: Free (uses existing memory)

**Option 3: Memcached**
- Pros: Fast, lightweight, simple
- Cons: Not persistent, less feature-rich than Redis
- Impact: Add Memcached service, update 4 files
- Cost: ~$5/month or free (self-hosted)

**Recommendation**: Redis (Option 1)
- Best for multi-worker deployments
- Persistence prevents cold starts
- Industry standard, widely supported

Which option do you prefer?
"""
```

**4. Quantify Impact for Large Changes**

```python
# ✅ GOOD: Quantify impact when affecting many files

# User: "Refactor authentication to use new AuthService class"

# Step 1: Analyze impact
Grep("authenticate", output_mode="files_with_matches")
# Found in 12 files

Grep("login", output_mode="files_with_matches")
# Found in 8 files

# Step 2: Propose with quantified impact
"""
CRITICAL CHANGE PROPOSAL:

**Change**: Refactor authentication to centralized AuthService
**Reason**: Authentication logic scattered across 12 files; hard to maintain

**Impact Analysis**:
- Files to modify: 12 (api.py, handlers.py, views.py, admin.py, ...)
- Functions to update: ~25 authenticate/login calls
- New files: 1 (auth_service.py)
- Lines of code: ~500 lines affected
- Breaking: no (internal refactor, API unchanged)

**Before**:
```python
# Scattered auth logic
if user.password == hash_password(pwd):
    session.create(user)
```

**After**:
```python
# Centralized
auth_service.authenticate(user, pwd)
```

**Benefits**:
- Single source of truth for auth logic
- Easier to add MFA, OAuth later
- Testable in isolation

**Risks**:
- Large change (12 files)
- Requires comprehensive testing
- Merge conflicts if others working on auth

**Testing Strategy**:
- Unit tests for AuthService
- Integration tests for all 12 affected files
- Manual testing of login/logout flows

Proceed with this refactor? (yes/no)
"""
```

**5. Security Changes Always Need Proposals**

```python
# ❌ BAD: Implement security change without proposal
Edit("auth.py",
     old_string="return jwt.encode(payload, SECRET_KEY)",
     new_string="return jwt.encode(payload, SECRET_KEY, algorithm='HS256')")

# ✅ GOOD: Propose security changes
"""
SECURITY CRITICAL CHANGE PROPOSAL:

**Change**: Explicitly specify JWT algorithm as HS256
**Reason**: Security best practice; prevents algorithm confusion attacks

**Current State**:
- JWT library auto-selects algorithm (security risk)
- Vulnerable to algorithm substitution attack (CVE-2015-9235)

**Proposed State**:
- Explicitly set algorithm='HS256'
- Reject tokens with different algorithms

**Security Impact**:
- Fixes: Algorithm confusion vulnerability
- Risk level: High (prevents auth bypass)
- Breaking: No (existing tokens still work)

**Files Affected**:
- auth.py (JWT encoding)
- middleware.py (JWT decoding)

**References**:
- CVE-2015-9235
- OWASP JWT Best Practices

**Testing**:
- Verify existing tokens still decode
- Test rejection of manipulated algorithm tokens

This is a security fix. Proceed? (yes/no)
"""
```

**6. Infrastructure Changes Need Detailed Proposals**

```python
# ✅ GOOD: Infrastructure proposal with operational details

"""
CRITICAL INFRASTRUCTURE PROPOSAL:

**Change**: Add PostgreSQL database (replace SQLite)
**Reason**: SQLite hitting limits (1000+ concurrent users, 10GB+ data)

**Current Setup**:
- SQLite file-based database
- Single-process only
- No concurrent writes
- 10GB database file

**Proposed Setup**:
- PostgreSQL 14 container
- Multi-process support
- Concurrent writes
- Proper indexing and query optimization

**Impact**:
- New dependency: PostgreSQL container
- Migration required: SQLite → PostgreSQL data export/import
- Configuration: DATABASE_URL environment variable
- Files affected: 8 (models, migrations, config, docker-compose)

**Migration Plan**:
1. Setup PostgreSQL container in development
2. Create migration script (SQLite export → PostgreSQL import)
3. Test migration with production data snapshot
4. Schedule downtime window (estimated 30 minutes)
5. Run migration, verify data integrity
6. Rollback plan: Keep SQLite backup for 7 days

**Costs**:
- Development: Free (local container)
- Production: ~$25/month (managed PostgreSQL) or $0 (self-hosted)
- Engineering time: 8 hours (setup + migration + testing)

**Risks**:
- Data migration complexity (10GB data)
- Downtime during migration (~30 min)
- Different SQL dialect (minor query adjustments needed)

**Benefits**:
- Supports 10,000+ concurrent users
- Better performance (indexed queries)
- Industry-standard, widely supported
- Proper backup/restore capabilities

Proceed with PostgreSQL migration? (yes/no)
"""
```

---

### Implementation Patterns

#### ✅ Good: Dependency Addition Proposal

```python
# User: "Add user authentication"

# Analyze requirements first
"""
Need to add authentication. Several library options:

1. Django-built-in auth (if using Django)
2. Flask-Login (if using Flask)
3. PyJWT + custom implementation
4. Third-party: Authlib, python-jose

Let me check what framework we're using...
"""

Read("requirements.txt")
# Found: Flask==2.3.0

# Propose dependency
"""
CRITICAL CHANGE PROPOSAL:

**Change**: Add Flask-Login for user authentication
**Reason**: Need user login/logout/session management for multi-user app

**Dependency Details**:
- Library: Flask-Login==0.6.2
- Size: 50KB
- Maintenance: Active (last update 2 months ago)
- Dependencies: Werkzeug (already have via Flask)
- License: MIT

**Impact**:
- Files: 4 (requirements.txt, app.py, models.py, routes.py)
- Breaking: No (new feature addition)

**Alternatives**:
1. Flask-Login (Recommended) - Most popular, well-maintained
2. Custom JWT - More control, more code to maintain
3. Flask-Security-Too - More features but heavier (500KB)

**Benefits**:
- Battle-tested by thousands of Flask apps
- Simple API, good documentation
- Session management built-in
- "Remember me" functionality

**Risks**:
- New dependency to maintain (low risk - stable library)

Proceed with Flask-Login? (yes/no)
"""
```

---

#### ✅ Good: Large Refactor Proposal

```python
# User: "Improve error handling across the application"

# Analyze current state
Grep("try:", output_mode="count")
# 45 try/except blocks

Grep("except Exception", output_mode="files_with_matches")
# 18 files with broad exception catching

# Propose refactor
"""
CRITICAL CHANGE PROPOSAL: Error Handling Refactor

**Change**: Standardize error handling with custom exception hierarchy
**Reason**: Current error handling inconsistent; 18 files catch generic Exception

**Current State**:
- 45 try/except blocks
- 18 files use bare "except Exception"
- No custom exceptions
- Inconsistent error logging

**Proposed State**:
- Custom exception hierarchy (BaseAppError, ValidationError, DatabaseError, APIError)
- Standardized error handling middleware
- Consistent error logging
- Proper error responses

**Impact**:
- Files to modify: 18 (all files with exception handling)
- New files: 1 (exceptions.py)
- Lines changed: ~300
- Breaking: No (internal change, API responses unchanged)

**Implementation Plan**:
1. Create exceptions.py with custom exception hierarchy
2. Update error handling middleware
3. Replace broad "except Exception" with specific exceptions
4. Add proper logging to all exception handlers
5. Update tests

**Benefits**:
- Easier debugging (specific exception types)
- Better error messages for users
- Consistent error logging
- Proper error categorization

**Risks**:
- Large change (18 files, ~300 lines)
- Requires comprehensive testing
- May reveal hidden bugs (currently masked by broad catches)

**Testing Strategy**:
- Unit tests for each exception type
- Integration tests for error handling paths
- Manual testing of common error scenarios

**Time Estimate**: 6-8 hours (implementation + testing)

Proceed with error handling refactor? (yes/no)
"""
```

---

#### ✅ Good: Database Migration Proposal

```python
# User: "Add email notifications feature"

# Realize this requires DB schema change
"""
CRITICAL CHANGE PROPOSAL: Add Email Notifications

**Change**: Add notification preferences to User model + notification queue table
**Reason**: Users need email notifications for key events (password reset, activity alerts)

**Database Changes**:
- Add column: user.email_notifications (boolean, default=true)
- New table: notification_queue (id, user_id, type, message, sent_at)

**Impact**:
- Files: 5 (models.py, migrations/, notification_service.py, email_service.py, api.py)
- Migration: Yes (DB schema change)
- Breaking: No (additive changes only)

**Migration Plan**:
1. Create migration: add user.email_notifications column
2. Create migration: add notification_queue table
3. Default all existing users to email_notifications=true
4. Run migrations in development/staging before production

**Rollback Plan**:
- Migrations are reversible (drop column, drop table)
- No data loss (new feature, no existing data affected)

**Benefits**:
- User control over notifications
- Async notification delivery (queue)
- Audit trail (notification history)

**Risks**:
- Database schema change (requires migration)
- New background job needed (process notification queue)

**Additional Requirements**:
- Email service configuration (SMTP or SendGrid)
- Background worker for queue processing

Should I proceed with this implementation? It will require:
1. Database migrations
2. Email service setup
3. Background worker

Do you want me to continue? (yes/no)
"""
```

---

#### ❌ Bad: Adding Dependency Without Proposal

```python
# ❌ BAD: Just add dependency without asking

# User: "Speed up the image processing"

Bash("pip install Pillow-SIMD")
Edit("requirements.txt",
     old_string="Pillow==9.5.0",
     new_string="Pillow-SIMD==9.5.0")

Edit("image_processor.py", ...)

# Problems:
# - Added dependency without proposal
# - User doesn't know Pillow-SIMD has different installation requirements
# - May not work on all platforms (SIMD optimizations)
# - No discussion of alternatives (could use existing Pillow better)
```

---

#### ❌ Bad: Large Change Without Proposal

```python
# ❌ BAD: Refactor 15 files without proposal

# User: "Improve the code quality"

# Immediately refactor everything
Edit("models.py", ...)  # Refactor 1
Edit("views.py", ...)   # Refactor 2
Edit("api.py", ...)     # Refactor 3
# ... 12 more files

# Problems:
# - No proposal for this critical change
# - User might not want this approach
# - Alternative refactoring strategies not discussed
# - High risk of introducing bugs
# - No testing strategy proposed
```

---

#### ❌ Bad: Infrastructure Change Without Details

```python
# ❌ BAD: Vague infrastructure proposal

"""
I'm going to add Docker for easier deployment. OK?
"""

# Problems:
# - No details on what gets Dockerized
# - No migration plan from current deployment
# - No cost/resource analysis
# - No discussion of alternatives (other containerization, VMs, etc.)
# - User can't make informed decision
```

---

## Anti-Patterns

### ❌ Anti-Pattern 1: "Quick Fix" Dependency Addition

**Problem**: Adding dependencies for small problems without considering alternatives.

```python
# ❌ BAD: Add library for simple task

# User: "Parse dates from user input"

# Add library immediately
Bash("pip install python-dateutil")
Edit("requirements.txt", ..., new_string="...\npython-dateutil==2.8.2")

# Problems:
# - Didn't check if stdlib datetime can handle it
# - Added 250KB dependency for simple task
# - No proposal, no alternative consideration

# ✅ GOOD: Consider stdlib first, then propose if needed

# Check if datetime.strptime() sufficient
"""
For date parsing, we have options:

OPTION 1: Use stdlib datetime.strptime()
- Pros: No dependencies, fast
- Cons: Requires exact format specification
- Works if: Input format is consistent

OPTION 2: Add python-dateutil
- Pros: Flexible parsing (handles many formats)
- Cons: 250KB dependency
- Works if: Input formats vary

What date formats do users provide?
"""
```

**Impact:**
- Unnecessary dependencies increase bundle size
- More libraries to maintain and update
- Security surface area increased
- Deployment complexity increased

---

### ❌ Anti-Pattern 2: Silent Architectural Changes

**Problem**: Making architectural changes without proposal or discussion.

```python
# ❌ BAD: Change architecture without proposal

# User: "Improve API response times"

# Silently introduce caching layer
Write("cache.py", redis_caching_implementation)
Edit("api.py", add_caching_decorators)
Edit("docker-compose.yml", add_redis_service)

# Problems:
# - Added Redis infrastructure without proposal
# - Changed architecture (added caching layer) without discussion
# - May conflict with user's plans (they might have different caching strategy)
# - Infrastructure costs not discussed

# ✅ GOOD: Propose architectural change
"""
CRITICAL ARCHITECTURAL PROPOSAL:

Current bottleneck: Database queries (500ms per request)

Proposed solution: Add Redis caching layer
- Cache database query results
- 1-hour TTL for most data
- Invalidate on updates

Impact:
- New infrastructure: Redis container
- Files: 4 (cache.py, api.py, docker-compose.yml, config.py)
- Cost: $10/month (managed) or free (self-hosted)

Alternative: Database query optimization
- Add indexes, optimize queries
- No new infrastructure
- May not achieve same performance gains

Which approach do you prefer?
"""
```

**Impact:**
- Unexpected infrastructure costs
- Operational complexity without buy-in
- May conflict with team's architectural direction
- Difficult to roll back after implementation

---

### ❌ Anti-Pattern 3: Bundling Multiple Critical Changes

**Problem**: Combining multiple critical changes in one proposal, making it hard to evaluate.

```python
# ❌ BAD: Bundle multiple critical changes

"""
PROPOSAL:
I'll add Redis for caching, switch to PostgreSQL, add Docker support,
and refactor the authentication system. OK?
"""

# Problems:
# - 4 critical changes bundled together
# - Can't approve/reject individually
# - Each needs separate evaluation
# - Testing strategy unclear

# ✅ GOOD: Separate proposals for each critical change

"""
I've identified 4 improvements needed:

1. Add Redis caching (performance)
2. Migrate SQLite → PostgreSQL (scalability)
3. Add Docker support (deployment)
4. Refactor authentication (maintainability)

These are independent changes. Should I propose them one at a time,
or do you want to discuss all four together first?
"""
```

**Impact:**
- User can't make granular decisions
- All-or-nothing approval (inflexible)
- Risks compounded (all changes at once)
- Testing complexity multiplied

---

## Implementation Checklist

### Identify Critical Changes (Any "Yes" = Needs Proposal)

- [ ] **New dependency** - Adding library or framework not currently used
- [ ] **Dependency upgrade** - Major version bump (e.g., 2.x → 3.x)
- [ ] **Infrastructure change** - New service, container, database, cache
- [ ] **Multi-file change** - Affects 5+ files
- [ ] **Architectural change** - New layer, pattern, or significant refactor
- [ ] **Security change** - Authentication, authorization, encryption, validation
- [ ] **Database migration** - Schema changes, new tables, column modifications
- [ ] **Configuration change** - New environment variables, config file structure
- [ ] **Breaking change** - Changes that break existing functionality (also use C_BREAKING_CHANGES_APPROVAL)
- [ ] **Performance optimization** - Significant algorithmic or architectural changes
- [ ] **External service integration** - APIs, webhooks, third-party services

### Proposal Components (Must Include All)

- [ ] **Change description** - One sentence: what are you proposing?
- [ ] **Reason** - Why is this needed? What problem does it solve?
- [ ] **Impact analysis** - Files affected, dependencies, infrastructure
- [ ] **Breaking or not** - Clearly state if breaking change
- [ ] **Alternatives** - At least 2-3 alternative approaches considered
- [ ] **Trade-offs** - Pros and cons of each alternative
- [ ] **Recommendation** - Which alternative you recommend and why
- [ ] **Risks** - What could go wrong?
- [ ] **Benefits** - What improvements will this bring?
- [ ] **Testing strategy** - How will this be tested?
- [ ] **Rollback plan** - How to undo if needed (for infrastructure changes)
- [ ] **Approval question** - "Proceed? (yes/no)" or "Which option?"

### After User Approval

- [ ] **Implement exactly as proposed** - Don't add scope
- [ ] **Follow testing strategy** - Execute proposed testing plan
- [ ] **Document decision** - Add comments referencing why this approach chosen
- [ ] **Report completion** - Summarize what was implemented

---

## Summary

**Critical Changes Require Proposal** means always proposing dependencies, infrastructure changes, multi-file refactors, security changes, and architectural modifications before implementation. Give users decision control and opportunity to discuss alternatives.

**Core Rules:**

- **Identify critical changes** - Use checklist to detect proposal-worthy changes
- **Complete proposals** - Include change, reason, impact, alternatives, risks, benefits
- **Quantify impact** - Specific file counts, dependency sizes, infrastructure costs
- **Offer alternatives** - Present 2-3 options with trade-offs
- **Wait for approval** - Don't implement until user approves
- **Security always** - All security changes need proposals with CVE references if applicable
