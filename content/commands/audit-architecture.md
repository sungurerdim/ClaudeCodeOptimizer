---
description: Architectural patterns, design principles compliance audit
category: audit
cost: 2
principles: ['P_SEPARATION_OF_CONCERNS', 'P_MICROSERVICES_SERVICE_MESH', 'P_CQRS_PATTERN', 'P_DEPENDENCY_INJECTION', 'P_CIRCUIT_BREAKER_PATTERN', 'P_EVENT_DRIVEN', 'P_SINGLETON_EXPENSIVE_RESOURCES', 'C_AGENT_ORCHESTRATION_PATTERNS', 'P_API_VERSIONING_STRATEGY', 'P_RESTFUL_API_CONVENTIONS']
---

# cco-audit-architecture - Architecture & Design Patterns Audit

**Validate architectural patterns, design principles, and API design compliance.**

---

## Architecture & Model Selection

**Data Gathering**: Haiku (Explore agent, medium)
- Pattern detection and architecture analysis
- API design validation
- Dependency analysis
- Cost-effective for structure evaluation

**Analysis**: Sonnet (Plan agent)
- Architectural debt assessment
- Design pattern recommendations
- Refactoring strategy planning

**Execution Pattern**:
1. Launch 2 parallel Haiku agents:
   - Agent 1: Application architecture (patterns, separation of concerns)
   - Agent 2: API design (RESTful conventions, versioning)
2. Aggregate with Sonnet for architectural recommendations
3. Generate prioritized refactoring plan

**Model Requirements**:
- Haiku for scanning (15-20 seconds)
- Sonnet for architectural analysis

---

## Action

Use Task tool to launch parallel architecture audit agents.

### Step 1: Parallel Architecture Scans

**CRITICAL**: Launch BOTH agents in PARALLEL in a SINGLE message.

#### Agent 1: Application Architecture Scan

**Agent 1 Prompt:**
```
Subagent Type: Explore
Model: haiku
Description: Application architecture audit

MUST LOAD FIRST:
1. @CLAUDE.md (Architecture section)
2. @~/.cco/principles/architecture.md
3. Print: "✓ Loaded 2 docs (~2,200 tokens)"

Audit principles:
- P_SEPARATION_OF_CONCERNS: Layered architecture, clear boundaries
- P_MICROSERVICES_SERVICE_MESH: Microservices patterns (if applicable)
- P_CQRS_PATTERN: Command Query Responsibility Segregation (if applicable)
- P_DEPENDENCY_INJECTION: Dependency Injection pattern
- P_CIRCUIT_BREAKER_PATTERN: Circuit Breaker for resilience
- P_EVENT_DRIVEN: Event-Driven Architecture (if applicable)
- P_SINGLETON_EXPENSIVE_RESOURCES: Singleton for expensive resources
- C_AGENT_ORCHESTRATION_PATTERNS: Agent orchestration (if applicable)

Scan for:
- Mixed concerns (business logic in controllers, database queries in views)
- Tight coupling (hard dependencies instead of interfaces)
- Missing dependency injection (direct instantiation)
- No circuit breakers for external services (resilience gaps)
- Synchronous coupling where async/event-driven would be better
- Missing abstractions (code depends on concrete implementations)
- God objects (classes doing too much)
- Lack of layering (no clear presentation/business/data layers)

Check for:
- Dependency direction (do dependencies flow inward?)
- Interface usage (are contracts defined?)
- Service boundaries (are services well-defined?)
- Error handling patterns (are failures isolated?)

Report with file:line references and architectural issues.
```

#### Agent 2: API Design Scan

**Agent 2 Prompt:**
```
Subagent Type: Explore
Model: haiku
Description: API design audit

MUST LOAD FIRST:
1. @CLAUDE.md (API Design section)
2. @~/.cco/principles/api-design.md
3. Print: "✓ Loaded 2 docs (~1,800 tokens)"

Audit principles:
- P_API_VERSIONING_STRATEGY: API Versioning Strategy
- P_RESTFUL_API_CONVENTIONS: RESTful API Conventions
- P_SCHEMA_VALIDATION: Schema-First Validation

Scan for:
- Non-RESTful endpoints (POST for reads, GET for writes)
- Inconsistent naming (camelCase vs snake_case, plural vs singular)
- Missing API versioning (/v1/, /v2/)
- No versioning strategy (breaking changes without version bump)
- Missing HTTP status codes (always 200, wrong codes)
- Inconsistent response formats (mixed structures)
- Missing pagination (returning all results)
- No request validation (accepting invalid input)
- Missing API documentation (no OpenAPI/Swagger)
- Inconsistent error responses (different error formats)

Check for:
- REST conventions: GET (read), POST (create), PUT/PATCH (update), DELETE (delete)
- Resource naming: plural nouns (/users, /posts)
- HTTP status codes: 200 (OK), 201 (Created), 400 (Bad Request), 404 (Not Found), 500 (Error)
- Response consistency: all responses have same structure
- API versioning: how are versions managed?

Report with endpoint examples and violations.
```

### Step 2: Architecture Analysis & Recommendations

**After both agents complete**, use Sonnet Plan agent:

**Agent 3 Prompt:**
```
Subagent Type: Plan
Model: sonnet
Description: Architecture refactoring analysis

Task: Analyze architecture findings and provide refactoring recommendations.

Input:
- Agent 1 findings (application architecture)
- Agent 2 findings (API design)

Analysis steps:
1. Merge all architecture findings
2. Assess architectural debt (cost of poor design)
3. Identify systemic patterns (not just individual issues)
4. Prioritize by: Impact × Spread × Effort
   - Impact: Maintainability, testability, scalability
   - Spread: How many areas affected?
   - Effort: How hard to refactor?
5. Provide specific refactoring commands
6. Consider migration strategies (incremental refactoring)
7. Calculate architectural debt (hours to fix)
8. Recommend patterns to adopt

Output format:
- Findings by impact (CRITICAL > HIGH > MEDIUM > LOW)
- Each finding includes: principle, file:line, architectural issue, refactoring plan
- Master refactoring roadmap with priority tiers
- Architectural debt estimate (total hours)

Focus on incremental, safe refactoring strategies.
```

---

## Output Format

Report architectural issues with design impact:

```
Architecture Audit Results
==========================

CRITICAL (architectural debt):
  - P_SEPARATION_OF_CONCERNS: Business logic in controllers (src/controllers/)
    Impact: Hard to test, hard to reuse
    Spread: 15 controller files
    Issue: Business logic mixed with HTTP handling
    Command: /cco-refactor extract-service --files src/controllers/* --target src/services/

  - P_DEPENDENCY_INJECTION: Direct instantiation throughout (src/)
    Impact: Tight coupling, hard to test
    Spread: 45 files
    Issue: No dependency injection container
    Command: /cco-generate di-container --framework dependency-injector

HIGH (design issues):
  - P_CIRCUIT_BREAKER_PATTERN: No circuit breaker for external API (src/integrations/payment.py)
    Impact: Cascading failures
    Issue: Direct calls to payment API without resilience
    Command: /cco-generate circuit-breaker --file src/integrations/payment.py --library circuitbreaker

  - P_RESTFUL_API_CONVENTIONS: Non-RESTful endpoints (src/api/routes.py)
    Impact: Confusing API, hard to maintain
    Issues:
      - POST /get-user (should be GET /users/:id)
      - GET /delete-user (should be DELETE /users/:id)
      - POST /update-profile (should be PUT /users/:id/profile)
    Command: /cco-fix api-design --file src/api/routes.py --standard rest

MEDIUM (improvement needed):
  - P_API_VERSIONING_STRATEGY: No API versioning (src/api/)
    Impact: Breaking changes break clients
    Issue: All endpoints at root path
    Command: /cco-generate api-versioning --strategy url-path --version v1

  - P_EVENT_DRIVEN: Synchronous coupling should be async (src/notifications.py:45)
    Impact: Slower response times
    Issue: Sending emails synchronously in request handler
    Command: /cco-refactor async-event --file src/notifications.py:45 --pattern event-queue

LOW (best practice):
  - P_SINGLETON_EXPENSIVE_RESOURCES: Multiple database connections (src/)
    Impact: Resource waste
    Issue: Creating connection per request
    Command: /cco-refactor singleton-db --pattern connection-pool
```

---

## Recommended Actions

**Analyze architecture findings and provide refactoring roadmap:**

```
🏗️ Architecture Refactoring Plan (Impact-Based Priority)
=========================================================

IMMEDIATE (High Debt):
──────────────────────
1. Extract business logic to service layer
   Command: /cco-refactor extract-service --files src/controllers/* --target src/services/
   Impact: CRITICAL - Testability, reusability
   Effort: 8 hours
   Spread: 15 files
   Benefits: Clean separation, easier testing

2. Implement dependency injection
   Command: /cco-generate di-container --framework dependency-injector
   Impact: CRITICAL - Loose coupling, testability
   Effort: 6 hours
   Spread: 45 files
   Benefits: Easy mocking, better testing

THIS WEEK (High Impact):
─────────────────────────
3. Add circuit breaker for payment API
   Command: /cco-generate circuit-breaker --file src/integrations/payment.py --library circuitbreaker
   Impact: HIGH - Resilience, fault tolerance
   Effort: 2 hours
   Benefits: Prevents cascading failures

4. Fix RESTful API conventions
   Command: /cco-fix api-design --file src/api/routes.py --standard rest
   Impact: HIGH - API clarity, maintainability
   Effort: 3 hours
   Changes:
     - POST /get-user → GET /users/:id
     - GET /delete-user → DELETE /users/:id
     - POST /update-profile → PUT /users/:id/profile

THIS SPRINT (Important):
────────────────────────
5. Add API versioning
   Command: /cco-generate api-versioning --strategy url-path --version v1
   Impact: MEDIUM - Supports breaking changes
   Effort: 4 hours
   Benefits: Client compatibility, safe evolution

6. Convert to event-driven notifications
   Command: /cco-refactor async-event --file src/notifications.py:45 --pattern event-queue
   Impact: MEDIUM - Faster response times
   Effort: 3 hours
   Benefits: Async processing, better UX

BACKLOG (Nice to Have):
───────────────────────
7. Implement connection pooling
   Command: /cco-refactor singleton-db --pattern connection-pool
   Impact: LOW - Resource optimization
   Effort: 2 hours
   Benefits: Fewer connections, better performance

Architectural Debt: 28 hours | Maintainability: 40% → 85%
```

**Command Generation Logic:**
1. **Architectural Impact = Maintainability × Testability × Scalability**
   - Maintainability: How hard to change?
   - Testability: How hard to test?
   - Scalability: Can it scale?

2. **Priority Tiers:**
   - IMMEDIATE: High debt, affects many areas (fix now)
   - THIS WEEK: Design issues, localized impact (fix this week)
   - THIS SPRINT: Improvements, best practices (fix this sprint)
   - BACKLOG: Optimizations, minor issues (fix when convenient)

3. **Command Features:**
   - Refactoring type: `extract-service`, `async-event`
   - Target patterns: `--pattern connection-pool`
   - Framework/library: `--framework`, `--library`
   - Migration strategy: Incremental, safe refactoring

4. **Refactoring Strategy:**
   - Start with highest impact (most files affected)
   - Incremental refactoring (not big bang)
   - Test after each step
   - Backward compatibility where possible

---

## Related Commands

- `/cco-refactor` - Apply architectural refactoring
- `/cco-generate` - Generate architectural patterns
- `/cco-audit-code-quality` - Code quality audit
- `/cco-audit-comprehensive` - Full comprehensive audit
