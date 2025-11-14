---
id: P_OBSERVABILITY_WITH_OTEL
title: Observability with OpenTelemetry
category: project-specific
severity: high
weight: 9
applicability:
  project_types: ['api', 'microservices']
  languages: ['all']
---

# P_OBSERVABILITY_WITH_OTEL: Observability with OpenTelemetry 🔴

**Severity**: High

Use OpenTelemetry (OTel) for unified metrics, traces, logs, and profiles. Vendor-neutral instrumentation.

**Why**: Enables fast debugging through centralized, structured, searchable logs

**Enforcement**: Skills required - verification_protocol, test_first, root_cause_analysis

**Project Types**: api, microservices
**Languages**: all

**Rules**:
- **Otel Instrumentation**: Use OpenTelemetry SDK for all instrumentation
- **Structured Logs**: Structured JSON logs with trace context
- **Distributed Tracing**: Distributed tracing with W3C Trace Context
- **Metrics Collection**: RED metrics (Rate, Errors, Duration) for services

**❌ Bad**:
```
# No instrumentation, plain text logs
print('User logged in')
# No trace context propagation
```

**✅ Good**:
```
# OpenTelemetry instrumentation
from opentelemetry import trace, metrics
tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)

with tracer.start_as_current_span('process_request') as span:
span.set_attribute('user.id', user_id)
request_counter.add(1, {'endpoint': '/api/users'})
logger.info('Request processed', extra={'trace_id': span.get_span_context().trace_id})
```
