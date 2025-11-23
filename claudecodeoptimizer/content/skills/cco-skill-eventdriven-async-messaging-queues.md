---
name: eventdriven-async-messaging-queues
description: Decouple services via event-driven patterns, async I/O, and message queues to prevent cascading failures, enable horizontal scaling, and process background jobs reliably. Includes RabbitMQ/Kafka patterns, dead letter queues, event sourcing, and idempotent processing.
keywords: [event-driven, async, messaging, queue, RabbitMQ, Kafka, event sourcing, pub/sub, dead letter queue, idempotent, EventEmitter]
category: architecture
related_commands:
  action_types: [audit, generate, optimize]
  categories: [architecture]
pain_points: [5, 6]
---

# Event-Driven Architecture & Async Messaging

**Domain:** Architecture | **Complexity:** High
---

## Standard Structure

**This skill follows [STANDARDS_SKILLS.md](../STANDARDS_SKILLS.md):**

- **Standard sections** - Domain, Purpose, Core Techniques, Anti-Patterns, Checklist
- **Code example format** - Bad/Good pattern with specific examples
- **Detection pattern format** - Python functions with Finding objects
- **Checklist format** - Specific, verifiable items

**See STANDARDS_SKILLS.md for format details. Only skill-specific content is documented below.**

---

## Purpose

Decouple services via event-driven patterns, async I/O, and message queues to prevent cascading failures, enable horizontal scaling, and process background jobs reliably.

---

## Core Techniques

### 1. Event-Driven Architecture

**Emit events, don't call services:**
```javascript
class OrderService extends EventEmitter {
  async createOrder(orderData) {
    const order = await db.orders.create(orderData);
    this.emit('orderCreated', { orderId: order.id, userId: order.userId, total: order.total });
    return order;
  }
}

// Subscribers decoupled
orderService.on('orderCreated', async (e) => await emailService.send(e.userId));
orderService.on('orderCreated', async (e) => await inventoryService.reserve(e.orderId));
```

### 2. Async I/O

```javascript
// ❌ BAD: Blocking
function process() {
  const orders = db.getOrders(); // Blocks!
  orders.forEach(o => sendEmail(o)); // Blocks!
}

// ✅ GOOD: Parallel async
async function process() {
  const orders = await db.getOrders();
  await Promise.all(orders.map(async o => await sendEmail(o)));
}
```

### 3. Message Queues (Bull)

```javascript
const queue = new Queue('email', 'redis://localhost:6379');

// Producer
await queue.add('welcome', { userId }, {
  attempts: 3,
  backoff: { type: 'exponential', delay: 2000 }
});

// Consumer
queue.process('welcome', async (job) => {
  const user = await db.users.findById(job.data.userId);
  await emailService.send({ to: user.email, subject: 'Welcome!' });
});
```

### 4. Dead Letter Queue

```javascript
mainQueue.process(async (job) => {
  try {
    await processOrder(job.data);
  } catch (error) {
    if (job.attemptsMade >= job.opts.attempts) {
      await dlq.add({ originalJob: job.data, error: error.message, timestamp: Date.now() });
    }
    throw error;
  }
});
```

---

## Patterns

### RabbitMQ Pub/Sub
```javascript
// Publish
channel.publish(exchange, 'order.created', Buffer.from(JSON.stringify(event)), { persistent: true });

// Subscribe
channel.consume(queue, async (msg) => {
  try {
    await handler(JSON.parse(msg.content));
    channel.ack(msg);
  } catch (error) {
    channel.nack(msg, false, true); // Requeue
  }
});
```

### Kafka Producer/Consumer
```javascript
// Produce
await producer.send({
  topic: 'orders',
  messages: [{ key: event.id, value: JSON.stringify(event) }]
});

// Consume
await consumer.run({
  eachMessage: async ({ message }) => {
    const event = JSON.parse(message.value);
    await handleEvent(event);
  }
});
```

### Event Sourcing
```javascript
class OrderAggregate {
  apply(event) {
    this.events.push(event);
    switch (event.type) {
      case 'OrderCreated': this.state.status = 'created'; break;
      case 'OrderPaid': this.state.status = 'paid'; break;
    }
  }

  async save() {
    await eventStore.appendEvents(this.orderId, this.events);
  }

  static async load(orderId) {
    const events = await eventStore.getEvents(orderId);
    const order = new OrderAggregate(orderId);
    events.forEach(e => order.apply(e));
    return order;
  }
}
```

---

## Checklist

- [ ] Events immutable, publishers don't call subscribers directly
- [ ] Async/await with Promise.all for parallelism
- [ ] Retry logic with exponential backoff configured
- [ ] Dead letter queue for failures after max retries
- [ ] Message acknowledgment (ack/nack) implemented
- [ ] Idempotent message processing
- [ ] Circuit breakers for external services
- [ ] Queue depth monitoring/alerting

## Command Discovery Protocol

When this skill is active, find relevant commands by searching `~/.claude/commands/` metadata:

```yaml
# Search criteria for this skill's domain
action_types: [audit, generate, optimize]
keywords: [event-driven, async, messaging, queue, Kafka, RabbitMQ, event sourcing]
category: architecture
pain_points: [5, 6]
```

**How Claude finds commands:**
1. Grep command files for `keywords:.*[pattern]` in frontmatter
2. Match `category: architecture`
3. Present matching commands with their parameters

This ensures commands are always current even when renamed or updated.
