# Architecture
**Event-driven, microservices, singleton, separation of concerns, patterns**

**Total Principles:** 10

---

## P011: Event-Driven Architecture

**Severity:** CRITICAL

Use async, event-driven patterns for scalability - communicate via events.

### Examples

**✅ Good:**
```
@app.post('/api')
async def create(data):
    queue.enqueue(process_job, data)  # Non-blocking
```

**❌ Bad:**
```
@app.post('/api')
def create(data):
    result = blocking_call()  # Blocks!
```

**Why:** Prevents resource leaks by ensuring cleanup always happens even when errors occur

---

## P012: Singleton Pattern for Expensive Resources

**Severity:** HIGH

DB connections, ML models, config must be singleton.

### Examples

**✅ Good:**
```
@lru_cache(maxsize=1)
def get_redis():
    return Redis()  # Singleton
```

**❌ Bad:**
```
def get_data():
    client = Redis()  # Creates new each time!
```

**Why:** Reduces system coupling by using events instead of direct function calls

---

## P013: Separation of Concerns

**Severity:** HIGH

Each layer/service has ONE responsibility - no mixing.

### Examples

**✅ Good:**
```
@app.post('/api')
def create(data):
    return business_layer.process(data)  # Delegated
```

**❌ Bad:**
```
@app.post('/api')
def create(data):
    result = complex_calc(data)  # Business logic in API!
```

**Why:** Makes systems scalable by breaking monoliths into independent, deployable services

---

## P014: Microservices with Service Mesh

**Severity:** HIGH

Use Service Mesh (Istio/Linkerd) for mTLS, traffic management, observability. API Gateway + Event Bus for communication.

### Examples

**✅ Good:**
```
# Istio Service Mesh - mTLS + observability
```
```
apiVersion: security.istio.io/v1beta1
```
```
kind: PeerAuthentication
```
```
metadata:
```
```
  name: default
```
```
spec:
```
```
  mtls:
```
```
    mode: STRICT
```
```

```
```
# Circuit breaker with Istio
```
```
apiVersion: networking.istio.io/v1beta1
```
```
kind: DestinationRule
```
```
metadata:
```
```
  name: service-b
```
```
spec:
```
```
  trafficPolicy:
```
```
    connectionPool:
```
```
      tcp:
```
```
        maxConnections: 100
```
```
    outlierDetection:
```
```
      consecutiveErrors: 5
```
```
      interval: 30s
```
```

```
```
# Event-driven async communication
```
```
await event_bus.publish('order.created', {
```
```
  'order_id': order.id,
```
```
  'user_id': user.id
```
```
})
```

**❌ Bad:**
```
# Direct service-to-service HTTP calls (no mTLS, no retries)
```
```
response = requests.get('http://service-b:8080/api/users')
```
```

```
```
# No circuit breaker - cascading failures possible
```

**Why:** Provides secure, observable, resilient service-to-service communication with mTLS and traffic management

---

## P015: CQRS Pattern

**Severity:** MEDIUM

Separate Command (write) and Query (read) models for complex domains.

### Examples

**✅ Good:**
```
# WriteModel for commands
# ReadModel (denormalized) for queries
```

**❌ Bad:**
```
# Same model for read and write
```

**Why:** Catches bugs before merge through peer code review and knowledge sharing

---

## P016: Dependency Injection

**Severity:** MEDIUM

Explicit dependencies via DI, no globals, easier testing.

### Examples

**✅ Good:**
```
def query(db: Database):
    return db.execute()  # Injected
```

**❌ Bad:**
```
db = Database()  # Global
def query():
    return db.execute()
```

**Why:** Maintains code quality through consistent PR templates and review checklists

---

## P017: Circuit Breaker Pattern

**Severity:** MEDIUM

Fail fast on external failures, prevent cascade failures.

### Examples

**✅ Good:**
```
@circuit_breaker(failure_threshold=5, timeout=60)
def call_external_api():
```

**❌ Bad:**
```
# No circuit breaker, retries forever
```

**Why:** Enables parallel development through isolated feature branches and clear merge strategy

---

## P018: API Versioning Strategy

**Severity:** HIGH

Support N and N-1 versions, never break existing clients.

### Examples

**✅ Good:**
```
/api/v1/resource  # Old version
/api/v2/resource  # New version
```

**❌ Bad:**
```
# No versioning, changes break clients
```

**Why:** Prevents breaking existing clients by supporting multiple API versions simultaneously

---

## P066: Agent Orchestration Patterns

**Severity:** HIGH

Optimize AI agent execution through parallel processing, appropriate model selection, and cost-effective workflows

### Examples

**✅ Good:**
```
# Parallel agents in SINGLE message
Task("search files", model="haiku")
Task("analyze data", model="haiku")
# Both run simultaneously

# Appropriate model selection
Task("simple grep", model="haiku")
Task("complex analysis", model="sonnet")
```

**❌ Bad:**
```
# Sequential agent launches (slow)
agent1 = Task("search files")
# Wait for agent1...
agent2 = Task("analyze data")

# Wrong model selection
Task("simple grep", model="opus")  # Expensive!
```

**Why:** Maximizes performance and minimizes cost through intelligent agent orchestration

---

## P070: Context Window Management

**Severity:** MEDIUM

Optimize AI context usage through model selection, targeted reads, and query format standardization

### Examples

**✅ Good:**
```
# Specific query format
"auth.py:127-145 → Add JWT refresh token support"

# Targeted reads
Read("auth.py", offset=120, limit=30)

# Parallel independent ops (in single message)
Task("analyze module1", model="haiku")
Task("analyze module2", model="haiku")
```

**❌ Bad:**
```
# Vague request
"Fix authentication bugs"

# Reading full files unnecessarily
Read("auth.py")  # 800 lines
Read("api.py")   # 1200 lines

# Sequential dependent ops
result1 = operation1()
result2 = operation2()
```

**Why:** Maximizes context efficiency through structured requests and optimized model usage

---
