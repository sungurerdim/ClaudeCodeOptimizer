# Message Queues
*Message queue and event streaming patterns*

**Trigger:** Message queue detected

## Kafka (MQ:Kafka)
**Trigger:** {kafka_deps}

- **Consumer-Groups**: Use consumer groups for scaling
- **Offset-Management**: Commit offsets explicitly for reliability
- **Exactly-Once**: Enable idempotent producer for exactly-once
- **Partition-Strategy**: Partition key strategy for ordering
- **Schema-Registry**: Use schema registry for message schemas
- **Dead-Letter**: Dead letter topics for failed messages
- **Replication-Factor**: Set replication factor for durability
- **Retention-Policy**: Configure retention based on use case

## RabbitMQ (MQ:RabbitMQ)
**Trigger:** {rabbitmq_deps}

- **Exchange-Types**: Use appropriate exchange types (direct, topic, fanout)
- **Queue-Durability**: Durable queues for persistence
- **Prefetch-Count**: Set prefetch for fair dispatch
- **Dead-Letter-Exchange**: DLX for failed messages
- **Acknowledgements**: Manual acks for reliability
- **Connection-Pool**: Pool connections, not channels
- **TTL-Messages**: Message TTL for expiration

## NATS (MQ:NATS)
**Trigger:** {nats_deps}

- **Subject-Hierarchy**: Use hierarchical subjects
- **JetStream-Persistence**: JetStream for persistence
- **Queue-Groups**: Queue groups for load balancing
- **Request-Reply**: Request-reply for RPC pattern
- **Stream-Retention**: Configure stream retention
- **Consumer-Durable**: Durable consumers for reliability

## AWS SQS (MQ:SQS)
**Trigger:** {sqs_deps}

- **Visibility-Timeout**: Set appropriate visibility timeout
- **Dead-Letter-Queue**: Configure DLQ for failed messages
- **Batch-Operations**: Use batch send/receive for efficiency
- **Long-Polling**: Enable long polling to reduce costs
- **FIFO-Ordering**: FIFO queues for ordering requirements
- **Message-Dedup**: Deduplication for exactly-once

## Google Pub/Sub (MQ:PubSub)
**Trigger:** {pubsub_deps}

- **Subscription-Types**: Push vs pull subscriptions
- **Acknowledgement-Deadline**: Set appropriate ack deadline
- **Dead-Letter-Topic**: Configure dead letter topic
- **Ordering-Keys**: Ordering keys for message ordering
- **Filter-Messages**: Use subscription filters
- **Snapshot-Seek**: Snapshots for replay capability
