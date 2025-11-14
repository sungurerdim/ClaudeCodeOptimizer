---
id: P_MICROSERVICES_SERVICE_MESH
title: Microservices with Service Mesh
category: architecture
severity: high
weight: 8
applicability:
  project_types: ['microservices']
  languages: ['all']
---

# P_MICROSERVICES_SERVICE_MESH: Microservices with Service Mesh 🔴

**Severity**: High

Use Service Mesh (Istio/Linkerd) for mTLS, traffic management, observability. API Gateway + Event Bus for communication.

**Why**: Provides secure, observable, resilient service-to-service communication with mTLS and traffic management

**Enforcement**: Skills required - verification_protocol, test_first, root_cause_analysis

**Project Types**: microservices
**Languages**: all

**Rules**:
- **Service Mesh**: Use service mesh for 3+ services (Istio, Linkerd, Consul)
- **Mtls Enabled**: Enable mTLS between services
- **Api Gateway**: Use API Gateway for external access
- **Event Driven**: Event bus for async communication (Kafka, NATS, RabbitMQ)
- **Circuit Breaker**: Circuit breaker for resilience

**❌ Bad**:
```
# Direct service-to-service HTTP calls (no mTLS, no retries)
response = requests.get('http://service-b:8080/api/users')

# No circuit breaker - cascading failures possible
```

**✅ Good**:
```
# Istio Service Mesh - mTLS + observability
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
name: default
spec:
mtls:
mode: STRICT

# Circuit breaker with Istio
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
name: service-b
spec:
trafficPolicy:
connectionPool:
tcp:
maxConnections: 100
outlierDetection:
consecutiveErrors: 5
interval: 30s

# Event-driven async communication
await event_bus.publish('order.created', {
'order_id': order.id,
'user_id': user.id
})
```
