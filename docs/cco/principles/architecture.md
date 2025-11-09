# Architecture Principles

**Generated**: 2025-11-09
**Principle Count**: 10

---

### P011: Event-Driven Architecture 🔴

**Severity**: Critical

Use async, event-driven patterns for scalability - communicate via events.

**Project Types**: api, microservices

**Rules**:
- No blocking calls in async functions

**❌ Bad**:
```
@app.post('/api')\ndef create(data):\n    result = blocking_call()  # Blocks!
```

**✅ Good**:
```
@app.post('/api')\nasync def create(data):\n    queue.enqueue(process_job, data)  # Non-blocking
```

---

### P012: Singleton Pattern for Expensive Resources 🟠

**Severity**: High

DB connections, ML models, config must be singleton.

**Rules**:
- No repeated expensive resource creation

**❌ Bad**:
```
def get_data():\n    client = Redis()  # Creates new each time!
```

**✅ Good**:
```
@lru_cache(maxsize=1)\ndef get_redis():\n    return Redis()  # Singleton
```

---

### P013: Separation of Concerns 🟠

**Severity**: High

Each layer/service has ONE responsibility - no mixing.

**Rules**:
- No business logic in API layer

**❌ Bad**:
```
@app.post('/api')\ndef create(data):\n    result = complex_calc(data)  # Business logic in API!
```

**✅ Good**:
```
@app.post('/api')\ndef create(data):\n    return business_layer.process(data)  # Delegated
```

---

### P014: Microservices with Service Mesh 🟠

**Severity**: High

Use Service Mesh (Istio/Linkerd) for mTLS, traffic management, observability. API Gateway + Event Bus for communication.

**Project Types**: microservices

**Rules**:
- Use service mesh for 3+ services (Istio, Linkerd, Consul)
- Enable mTLS between services
- Use API Gateway for external access
- Event bus for async communication (Kafka, NATS, RabbitMQ)
- Circuit breaker for resilience

**❌ Bad**:
```
# Direct service-to-service HTTP calls (no mTLS, no retries)
```

**✅ Good**:
```
# Istio Service Mesh - mTLS + observability
```

---

### P015: CQRS Pattern 🟡

**Severity**: Medium

Separate Command (write) and Query (read) models for complex domains.

**Project Types**: microservices, api

**❌ Bad**:
```
# Same model for read and write
```

**✅ Good**:
```
# WriteModel for commands\n# ReadModel (denormalized) for queries
```

---

### P016: Dependency Injection 🟡

**Severity**: Medium

Explicit dependencies via DI, no globals, easier testing.

**Rules**:
- No global variables

**❌ Bad**:
```
db = Database()  # Global\ndef query():\n    return db.execute()
```

**✅ Good**:
```
def query(db: Database):\n    return db.execute()  # Injected
```

---

### P017: Circuit Breaker Pattern 🟡

**Severity**: Medium

Fail fast on external failures, prevent cascade failures.

**Project Types**: microservices, api

**❌ Bad**:
```
# No circuit breaker, retries forever
```

**✅ Good**:
```
@circuit_breaker(failure_threshold=5, timeout=60)\ndef call_external_api():
```

---

### P018: API Versioning Strategy 🟠

**Severity**: High

Support N and N-1 versions, never break existing clients.

**Project Types**: api, library

**❌ Bad**:
```
# No versioning, changes break clients
```

**✅ Good**:
```
/api/v1/resource  # Old version\n/api/v2/resource  # New version
```

---

### P066: Agent Orchestration Patterns 🟠

**Severity**: High

Optimize AI agent execution through parallel processing, appropriate model selection, and cost-effective workflows

**Rules**:
- Launch parallel agents in single message
- Use appropriate model for task complexity
- Optimize for cost and performance

**❌ Bad**:
```
# Sequential agent launches (slow)\nagent1 = Task("search files")\n# Wait for agent1...\nagent2 = Task("analyze data")\n\n# Wrong model selection\nTask("simple grep", model="opus")  # Expensive!
```

**✅ Good**:
```
# Parallel agents in SINGLE message\nTask("search files", model="haiku")\nTask("analyze data", model="haiku")\n# Both run simultaneously\n\n# Appropriate model selection\nTask("simple grep", model="haiku")\nTask("complex analysis", model="sonnet")
```

---

### P070: Context Window Management 🟡

**Severity**: Medium

Optimize AI context usage through model selection, targeted reads, and query format standardization

**Rules**:
- Use query format [file:line] → [action]
- Select model by task complexity
- Parallel independent operations

**❌ Bad**:
```
# Vague request\n"Fix authentication bugs"\n\n# Reading full files unnecessarily\nRead("auth.py")  # 800 lines\nRead("api.py")   # 1200 lines\n\n# Sequential dependent ops\nresult1 = operation1()\nresult2 = operation2()
```

**✅ Good**:
```
# Specific query format\n"auth.py:127-145 → Add JWT refresh token support"\n\n# Targeted reads\nRead("auth.py", offset=120, limit=30)\n\n# Parallel independent ops (in single message)\nTask("analyze module1", model="haiku")\nTask("analyze module2", model="haiku")
```

---

---

**Loading**: These principles load automatically when running relevant commands

**Reference**: Use `@PRINCIPLES.md` to load core principles, or reference this file directly