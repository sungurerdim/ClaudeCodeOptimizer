---
name: microservices-architecture
description: Implement microservices with CQRS pattern, service mesh, dependency injection, event-driven communication, and saga pattern for distributed transactions in scalable systems
keywords: [microservices, CQRS, service mesh, dependency injection, event-driven, saga pattern, DDD, bounded context, circuit breaker, Istio]
category: architecture
related_commands:
  action_types: [audit, fix, generate, optimize]
  categories: [architecture]
pain_points: [2, 6, 10]
---

# Skill: Microservices, CQRS, Service Mesh & DI
**Domain**: Distributed Systems
**Purpose**: Implement microservices with CQRS pattern, service mesh, dependency injection, and event-driven communication for scalable distributed systems.

## Core Techniques
- **Service Decomposition**: Use DDD bounded contexts to define service boundaries
- **CQRS Pattern**: Separate write (commands) and read (queries) models
- **Service Mesh**: Traffic management, mTLS, circuit breakers via Istio/Linkerd
- **Dependency Injection**: Interface-based design with DI containers
- **Event-Driven**: Async communication via events and message brokers
- **Saga Pattern**: Distributed transactions with compensation logic

## Patterns

### ✅ CQRS Command Handler
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
**Why**: Commands modify state, publish events, handle business logic

### ✅ CQRS Query Handler
```python
class GetOrderHandler:
    def __init__(self, read_model_repo):
        self.read_model = read_model_repo

    async def handle(self, query: GetOrderQuery):
        # Read from denormalized model
        return await self.read_model.get_order(query.order_id)
```
**Why**: Queries read from optimized, denormalized read models

### ✅ Service Mesh Circuit Breaker
```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: payment-circuit-breaker
spec:
  host: payment-service
  trafficPolicy:
    connectionPool:
      http:
        http1MaxPendingRequests: 1
    outlierDetection:
      consecutive5xxErrors: 3
      interval: 10s
      baseEjectionTime: 30s
```
**Why**: Prevent cascading failures, auto-eject unhealthy instances

### ✅ Dependency Injection Container
```python
from dependency_injector import containers, providers

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    database = providers.Singleton(Database, connection_string=config.db.url)
    order_repository = providers.Factory(MongoOrderRepository, database=database)
    event_bus = providers.Singleton(RabbitMQEventBus, host=config.mq.host)

    create_order_handler = providers.Factory(
        CreateOrderHandler,
        order_repository=order_repository,
        event_bus=event_bus
    )

@app.post("/orders")
async def create_order(
    command: CreateOrderCommand,
    handler: CreateOrderHandler = Depends(Provide[Container.create_order_handler])
):
    return await handler.handle(command)
```
**Why**: Testable, decoupled, interface-based design

### ✅ Saga Pattern with Compensation
```python
class OrderSaga:
    async def execute(self, command: CreateOrderCommand):
        compensation_stack = []
        try:
            # Step 1: Reserve inventory
            reservation = await self.inventory.reserve_stock(command.items)
            compensation_stack.append(lambda: self.inventory.release(reservation.id))

            # Step 2: Process payment
            payment = await self.payment.charge(command.user_id, command.total)
            compensation_stack.append(lambda: self.payment.refund(payment.id))

            # Step 3: Create order
            return await self.order.create(command, reservation.id, payment.id)
        except Exception as e:
            # Compensate in reverse
            for compensate in reversed(compensation_stack):
                await compensate()
            raise
```
**Why**: Handle distributed transactions with automatic rollback

### ❌ Shared Database
```python
# OrderService and InventoryService both query same DB
class OrderService:
    def create_order(self):
        self.db.orders.insert(order)
        self.db.inventory.update(product_id, -quantity)  # Direct DB access!
```
**Why**: Creates distributed monolith, tight coupling, no service autonomy

### ❌ No Read Model
```python
class GetOrderHandler:
    async def handle(self, query: GetOrderQuery):
        # Query normalized write model with joins
        order = await self.db.orders.find_one(query.order_id)
        user = await self.db.users.find_one(order.user_id)
        items = await self.db.items.find({"order_id": query.order_id})
        return self.merge(order, user, items)  # Slow!
```
**Why**: Read queries shouldn't hit write model, use denormalized read model

### ❌ Synchronous Inter-Service Calls
```python
async def create_order(command):
    user = await http_get(f"http://user-service/users/{command.user_id}")
    stock = await http_get(f"http://inventory-service/stock/{command.product_id}")
    payment = await http_post("http://payment-service/charge", data)
    # Blocks on 3 services, cascading failures
```
**Why**: Creates tight coupling, latency multiplication, cascading failures

## Checklist
- [ ] Services have clear bounded contexts (DDD)
- [ ] Database per service (no shared DB)
- [ ] Commands separated from queries (CQRS)
- [ ] Read models denormalized for performance
- [ ] Events published for cross-service communication
- [ ] Service mesh enforces mTLS
- [ ] Circuit breakers configured
- [ ] DI container manages dependencies
- [ ] Saga pattern for distributed transactions
- [ ] API gateway for unified entry point
- [ ] Service discovery (Consul/Istio)
- [ ] No circular service dependencies

---

## Command Discovery Protocol

When this skill is active, find relevant commands by searching `~/.claude/commands/` metadata:

```yaml
# Search criteria for microservices architecture domain
action_types: [audit, fix, generate, optimize]
keywords: [microservices, CQRS, service mesh, DDD, saga, event-driven]
category: architecture
pain_points: [2, 6, 10]
```

**How Claude finds commands:**
1. Grep command files for `keywords:.*[pattern]` in frontmatter
2. Match `category: architecture`
3. Present matching commands with their parameters

This ensures commands are always current even when renamed or updated.
