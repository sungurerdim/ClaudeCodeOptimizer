---
name: cco-skill-architecture
description: Distributed system architecture including microservices patterns (CQRS, Saga, DDD), resilience patterns (Circuit Breaker, Retry, Bulkhead), service mesh, and event-driven communication for scalable, fault-tolerant systems.
keywords: [architecture, microservices, CQRS, saga, circuit breaker, retry, bulkhead, resilience, event-driven, service mesh, DDD, bounded context, distributed systems, fault tolerance]
category: architecture
related_commands:
  action_types: [audit, fix, generate, optimize]
  categories: [architecture, infrastructure]
pain_points: [2, 5, 6, 10]
---

# Skill: Distributed Architecture & Resilience

> **Standards:** Format defined in [cco-standards.md](../cco-standards.md)
> **Discovery:** See [cco-standards.md](../cco-standards.md#18-command-discovery-protocol)


## Purpose

Design and implement scalable, fault-tolerant distributed systems.

**Solves**: Cascading failures (95% of distributed outages), tight coupling, resource exhaustion, unpredictable recovery, distributed transaction failures

**Impact**: Critical

---

## Guidance Areas

- **Microservices Patterns** - CQRS, Saga, DDD bounded contexts
- **Resilience Patterns** - Circuit Breaker, Retry, Bulkhead
- **Service Mesh** - Traffic management, mTLS, observability
- **Event-Driven** - Async communication, message brokers, DLQ

---

## Part 1: Microservices Architecture

### Service Decomposition (DDD)

**Bounded Context**: Define clear service boundaries based on business domains.

```python
# E-commerce bounded contexts
ORDER_CONTEXT = {
    "aggregates": ["Order", "OrderItem"],
    "events": ["OrderCreated", "OrderShipped", "OrderCancelled"],
    "commands": ["CreateOrder", "CancelOrder", "UpdateOrderStatus"]
}

INVENTORY_CONTEXT = {
    "aggregates": ["Product", "StockItem", "Reservation"],
    "events": ["StockReserved", "StockReleased", "LowStockAlert"],
    "commands": ["ReserveStock", "ReleaseStock", "UpdateStock"]
}

PAYMENT_CONTEXT = {
    "aggregates": ["Payment", "Refund"],
    "events": ["PaymentProcessed", "PaymentFailed", "RefundIssued"],
    "commands": ["ProcessPayment", "RefundPayment"]
}
```

**Rule**: Each context owns its data - no shared databases.

### CQRS Pattern

Separate write (commands) and read (queries) models for scalability.

**Command Handler** (Write Side):

```python
class CreateOrderHandler:
    def __init__(self, order_repo, event_bus, inventory_service):
        self.order_repo = order_repo
        self.event_bus = event_bus
        self.inventory_service = inventory_service

    async def handle(self, command: CreateOrderCommand):
        # Reserve inventory
        reservation_id = await self.inventory_service.reserve_stock(command.items)

        # Create order aggregate
        order = Order.create(command.user_id, command.items, reservation_id)
        await self.order_repo.save(order)

        # Publish event
        await self.event_bus.publish(OrderCreated(order.id, order.user_id))
        return order
```

**Query Handler** (Read Side):

```python
class GetOrderHandler:
    def __init__(self, read_model_repo):
        self.read_model = read_model_repo

    async def handle(self, query: GetOrderQuery):
        # Read from denormalized model - optimized for reads
        return await self.read_model.get_order(query.order_id)
```

**Why CQRS**: Write models optimize for consistency, read models optimize for query performance.

### Saga Pattern

Handle distributed transactions with compensation logic.

```python
class OrderSaga:
    """Orchestration-based saga for order creation."""

    async def execute(self, command: CreateOrderCommand):
        compensation_stack = []

        try:
            # Step 1: Reserve inventory
            reservation = await self.inventory.reserve_stock(command.items)
            compensation_stack.append(
                lambda: self.inventory.release(reservation.id)
            )

            # Step 2: Process payment
            payment = await self.payment.charge(command.user_id, command.total)
            compensation_stack.append(
                lambda: self.payment.refund(payment.id)
            )

            # Step 3: Create order
            order = await self.order.create(command, reservation.id, payment.id)
            return order

        except Exception as e:
            # Compensate in reverse order
            for compensate in reversed(compensation_stack):
                try:
                    await compensate()
                except Exception as comp_error:
                    logger.error(f"Compensation failed: {comp_error}")
            raise
```

**Choreography Alternative**:

```python
# Event-driven saga (no central orchestrator)
class InventoryService:
    @event_handler("OrderCreated")
    async def handle_order_created(self, event):
        try:
            await self.reserve_stock(event.order_id, event.items)
            await self.publish(StockReserved(event.order_id))
        except InsufficientStock:
            await self.publish(StockReservationFailed(event.order_id))

class PaymentService:
    @event_handler("StockReserved")
    async def handle_stock_reserved(self, event):
        try:
            await self.process_payment(event.order_id)
            await self.publish(PaymentProcessed(event.order_id))
        except PaymentFailed:
            await self.publish(PaymentFailed(event.order_id))
            # Triggers compensation in InventoryService
```

### Dependency Injection

Interface-based design for testability.

```python
from dependency_injector import containers, providers

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    # Infrastructure
    database = providers.Singleton(
        Database,
        connection_string=config.db.url
    )

    event_bus = providers.Singleton(
        RabbitMQEventBus,
        host=config.mq.host
    )

    # Repositories
    order_repository = providers.Factory(
        MongoOrderRepository,
        database=database
    )

    # Handlers
    create_order_handler = providers.Factory(
        CreateOrderHandler,
        order_repository=order_repository,
        event_bus=event_bus
    )


# Usage with FastAPI
@app.post("/orders")
async def create_order(
    command: CreateOrderCommand,
    handler: CreateOrderHandler = Depends(Provide[Container.create_order_handler])
):
    return await handler.handle(command)
```

---

## Part 2: Resilience Patterns

### Circuit Breaker

Stop calling a failing service after N failures.

```python
from circuitbreaker import circuit

@circuit(failure_threshold=5, recovery_timeout=60, expected_exception=ServiceError)
def call_payment_service(order_id: str, amount: float):
    response = requests.post(
        f"{PAYMENT_URL}/charge",
        json={"order_id": order_id, "amount": amount},
        timeout=5
    )
    response.raise_for_status()
    return response.json()
```

**States**:
- **CLOSED**: Normal operation, requests pass through
- **OPEN**: Requests fail immediately (after threshold breached)
- **HALF-OPEN**: After recovery timeout, allow test request

**Implementation with Metrics**:

```python
class CircuitBreaker:
    def __init__(self, name: str, failure_threshold: int = 5,
                 recovery_timeout: int = 60):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures = 0
        self.state = "CLOSED"
        self.last_failure_time = None

    async def call(self, func, *args, **kwargs):
        if self.state == "OPEN":
            if self._should_attempt_recovery():
                self.state = "HALF-OPEN"
            else:
                raise CircuitOpenError(f"Circuit {self.name} is OPEN")

        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise

    def _on_success(self):
        self.failures = 0
        self.state = "CLOSED"

    def _on_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()
        if self.failures >= self.failure_threshold:
            self.state = "OPEN"
            logger.warning(f"Circuit {self.name} OPENED")
```

### Retry with Exponential Backoff

Handle transient failures with increasing delays.

```python
import backoff

@backoff.on_exception(
    backoff.expo,
    requests.RequestException,
    max_tries=5,
    max_time=30,
    jitter=backoff.full_jitter
)
def fetch_user_data(user_id: str):
    response = requests.get(
        f"{USER_SERVICE_URL}/users/{user_id}",
        timeout=5
    )
    response.raise_for_status()
    return response.json()
```

**Manual Implementation**:

```python
import random
import asyncio

async def retry_with_backoff(
    func,
    max_retries: int = 5,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    retryable_exceptions: tuple = (Exception,)
):
    for attempt in range(max_retries):
        try:
            return await func()
        except retryable_exceptions as e:
            if attempt == max_retries - 1:
                raise

            # Exponential backoff with full jitter
            delay = min(base_delay * (2 ** attempt), max_delay)
            jittered_delay = random.uniform(0, delay)

            logger.warning(
                f"Attempt {attempt + 1} failed: {e}. "
                f"Retrying in {jittered_delay:.2f}s"
            )
            await asyncio.sleep(jittered_delay)
```

**Jitter Types**:
- **Full Jitter**: `random(0, delay)` - Best for reducing thundering herd
- **Equal Jitter**: `delay/2 + random(0, delay/2)`
- **Decorrelated Jitter**: `min(cap, random(base, prev_delay * 3))`

### Bulkhead Pattern

Isolate resources to prevent cascade failures.

```python
from concurrent.futures import ThreadPoolExecutor

class BulkheadedServices:
    def __init__(self):
        # Critical services get more resources
        self.payment_pool = ThreadPoolExecutor(
            max_workers=20,
            thread_name_prefix="payment"
        )
        # Non-critical services get fewer
        self.notification_pool = ThreadPoolExecutor(
            max_workers=5,
            thread_name_prefix="notification"
        )
        self.analytics_pool = ThreadPoolExecutor(
            max_workers=3,
            thread_name_prefix="analytics"
        )

    async def process_payment(self, order_id: str):
        # Runs in payment pool - won't be blocked by analytics
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.payment_pool,
            self._sync_process_payment,
            order_id
        )

    async def send_notification(self, user_id: str, message: str):
        # Runs in notification pool
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.notification_pool,
            self._sync_send_notification,
            user_id,
            message
        )
```

**Semaphore-based Bulkhead**:

```python
import asyncio

class SemaphoreBulkhead:
    def __init__(self, name: str, max_concurrent: int):
        self.name = name
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.rejected = 0

    async def execute(self, func, *args, timeout: float = 30.0, **kwargs):
        try:
            async with asyncio.timeout(0.1):  # Wait max 100ms for slot
                await self.semaphore.acquire()
        except asyncio.TimeoutError:
            self.rejected += 1
            raise BulkheadFullError(f"Bulkhead {self.name} full")

        try:
            async with asyncio.timeout(timeout):
                return await func(*args, **kwargs)
        finally:
            self.semaphore.release()


# Usage
payment_bulkhead = SemaphoreBulkhead("payment", max_concurrent=20)
notification_bulkhead = SemaphoreBulkhead("notification", max_concurrent=5)

async def process_order(order):
    payment = await payment_bulkhead.execute(
        charge_payment, order.id, order.total
    )
    # Non-critical - don't fail order if notification fails
    try:
        await notification_bulkhead.execute(
            send_confirmation, order.user_id
        )
    except BulkheadFullError:
        logger.warning("Notification bulkhead full, skipping")
```

### Graceful Degradation

Provide fallback responses when dependencies fail.

```python
class RecommendationService:
    def __init__(self, ml_client, cache, db):
        self.ml_client = ml_client
        self.cache = cache
        self.db = db

    async def get_recommendations(self, user_id: str) -> list:
        """Multi-level fallback chain."""

        # Level 1: ML service (personalized)
        try:
            return await self.ml_client.get_recommendations(
                user_id, timeout=2.0
            )
        except (ServiceUnavailable, TimeoutError) as e:
            logger.warning(f"ML service unavailable: {e}")

        # Level 2: Cached recommendations
        cached = await self.cache.get(f"rec:{user_id}")
        if cached:
            return cached

        # Level 3: User's purchase history
        try:
            history = await self.db.get_user_purchases(user_id, limit=10)
            if history:
                return self._recommendations_from_history(history)
        except DatabaseError as e:
            logger.warning(f"DB unavailable: {e}")

        # Level 4: Popular items (always available)
        return await self._get_popular_items()

    async def _get_popular_items(self) -> list:
        # Hardcoded fallback - always works
        return [
            {"id": "popular-1", "name": "Best Seller"},
            {"id": "popular-2", "name": "Top Rated"},
        ]
```

### Timeout Configuration

Always set explicit timeouts on external calls.

```python
import httpx

# Connection timeout: time to establish connection
# Read timeout: time to receive response
TIMEOUT_CONFIG = httpx.Timeout(
    connect=3.0,    # 3 seconds to connect
    read=10.0,      # 10 seconds to read response
    write=5.0,      # 5 seconds to send request
    pool=2.0        # 2 seconds to get connection from pool
)

async def call_external_api(endpoint: str):
    async with httpx.AsyncClient(timeout=TIMEOUT_CONFIG) as client:
        response = await client.get(f"{BASE_URL}{endpoint}")
        response.raise_for_status()
        return response.json()
```

**Timeout Budget Pattern**:

```python
class TimeoutBudget:
    """Track remaining time across multiple operations."""

    def __init__(self, total_seconds: float):
        self.deadline = time.monotonic() + total_seconds

    @property
    def remaining(self) -> float:
        return max(0, self.deadline - time.monotonic())

    @property
    def expired(self) -> bool:
        return self.remaining <= 0


async def process_order(order, budget: TimeoutBudget):
    # Each step uses remaining budget
    inventory = await reserve_stock(order, timeout=budget.remaining)

    if budget.expired:
        await rollback(inventory)
        raise TimeoutError("Order processing budget exceeded")

    payment = await process_payment(order, timeout=budget.remaining)
    return order


# Usage
budget = TimeoutBudget(total_seconds=30)
result = await process_order(order, budget)
```

### Dead Letter Queue

Preserve failed messages for later processing.

```python
class MessageProcessor:
    def __init__(self, main_queue, dlq, max_retries: int = 3):
        self.main_queue = main_queue
        self.dlq = dlq
        self.max_retries = max_retries

    async def process(self, message):
        retry_count = message.headers.get("x-retry-count", 0)

        try:
            await self._handle_message(message)
            await message.ack()
        except RecoverableError as e:
            if retry_count < self.max_retries:
                # Requeue with incremented retry count
                await self.main_queue.publish(
                    message.body,
                    headers={"x-retry-count": retry_count + 1}
                )
                await message.ack()
            else:
                await self._send_to_dlq(message, str(e))
        except UnrecoverableError as e:
            # Immediately send to DLQ
            await self._send_to_dlq(message, str(e))

    async def _send_to_dlq(self, message, error: str):
        await self.dlq.publish(
            message.body,
            headers={
                "x-original-queue": self.main_queue.name,
                "x-error": error,
                "x-failed-at": datetime.utcnow().isoformat(),
                "x-retry-count": message.headers.get("x-retry-count", 0)
            }
        )
        await message.ack()
        logger.error(f"Message sent to DLQ: {error}")
```

---

## Part 3: Service Mesh

### Istio Circuit Breaker

```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: payment-service-circuit-breaker
spec:
  host: payment-service
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        h2UpgradePolicy: UPGRADE
        http1MaxPendingRequests: 100
        http2MaxRequests: 1000
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 10s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
```

### Traffic Management

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: order-service
spec:
  hosts:
  - order-service
  http:
  - match:
    - headers:
        x-canary:
          exact: "true"
    route:
    - destination:
        host: order-service
        subset: canary
      weight: 100
  - route:
    - destination:
        host: order-service
        subset: stable
      weight: 95
    - destination:
        host: order-service
        subset: canary
      weight: 5
    retries:
      attempts: 3
      perTryTimeout: 2s
    timeout: 10s
```

---

## Anti-Patterns

### Shared Database

```python
# OrderService and InventoryService both access same DB
class OrderService:
    def create_order(self):
        self.db.orders.insert(order)
        self.db.inventory.update(product_id, -quantity)  # Direct access!
```

**Problem**: Creates distributed monolith, tight coupling, no service autonomy.

### Synchronous Chains

```python
async def create_order(command):
    user = await http_get(f"http://user-service/users/{command.user_id}")
    stock = await http_get(f"http://inventory-service/stock/{command.product_id}")
    payment = await http_post("http://payment-service/charge", data)
    # Blocks on 3 services, cascading failures likely
```

**Problem**: Latency multiplication, cascading failures.

### Missing Timeouts

```python
# Never do this
response = requests.get("http://external-api.com/data")
```

**Problem**: Request may hang forever, exhausting connection pool.

---

## Checklist

### Microservices
- [ ] Services have clear bounded contexts (DDD)
- [ ] Database per service (no shared DB)
- [ ] Commands separated from queries (CQRS)
- [ ] Read models denormalized for performance
- [ ] Events published for cross-service communication
- [ ] Saga pattern for distributed transactions
- [ ] DI container manages dependencies
- [ ] API gateway for unified entry point

### Resilience
- [ ] All external calls have explicit timeouts
- [ ] Circuit breakers on critical dependencies
- [ ] Retry with exponential backoff + jitter
- [ ] Separate resource pools (bulkhead)
- [ ] Fallback strategy per dependency
- [ ] Dead letter queue for failed messages

### Service Mesh
- [ ] mTLS enabled between services
- [ ] Circuit breakers configured
- [ ] Retry policies defined
- [ ] Traffic management rules
- [ ] Observability (traces, metrics)

