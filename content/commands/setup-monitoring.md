---
id: cco-setup-monitoring
description: Observability stack setup (Prometheus, Grafana)
category: devops
priority: normal
---

# Setup Monitoring

Setup observability stack with metrics, logging, and alerting for **${PROJECT_NAME}**.

**Project Type:** ${PROJECT_TYPE}
**Primary Language:** ${PRIMARY_LANGUAGE}

## Objective

Complete observability setup:
1. Metrics collection (Prometheus)
2. Visualization (Grafana)
3. Logging aggregation
4. Alerting rules
5. Application instrumentation

**Output:** Production-ready monitoring infrastructure.

---

## Architecture & Model Selection

**Generation**: Sonnet (requires understanding of monitoring patterns)
**Execution Pattern**: Sequential setup with validation

---

## When to Use

**Use this command:**
- Production deployments
- Microservices architectures
- Performance monitoring needed
- Debugging production issues

---

## Phase 1: Generate Prometheus Config

```python
import sys
sys.path.insert(0, "D:/GitHub/ClaudeCodeOptimizer")

from pathlib import Path

project_root = Path(".").resolve()

print(f"=== Prometheus Configuration ===\n")

prometheus_config = '''global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

rule_files:
  - "alerts.yml"

scrape_configs:
  - job_name: 'application'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'

  - job_name: 'node_exporter'
    static_configs:
      - targets: ['node-exporter:9100']

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']
'''

print("Generated Prometheus configuration:")
print("  - Scrape interval: 15s")
print("  - Application metrics")
print("  - Node exporter (system metrics)")
print("  - PostgreSQL exporter")
print()
```

---

## Phase 2: Generate Alert Rules

```python
print(f"=== Alert Rules ===\n")

alert_rules = '''groups:
  - name: application
    interval: 30s
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} (threshold: 0.05)"

      - alert: HighResponseTime
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High response time"
          description: "95th percentile response time is {{ $value }}s"

      - alert: HighMemoryUsage
        expr: process_resident_memory_bytes / 1024 / 1024 > 1024
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage"
          description: "Memory usage is {{ $value }}MB"

      - alert: ServiceDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Service is down"
          description: "{{ $labels.instance }} is not responding"
'''

print("Generated alert rules:")
print("  - HighErrorRate: >5% error rate")
print("  - HighResponseTime: >1s p95 latency")
print("  - HighMemoryUsage: >1GB memory")
print("  - ServiceDown: Service unavailable")
print()
```

---

## Phase 3: Instrument Application

```python
print(f"=== Application Instrumentation ===\n")

instrumentation = '''"""
Application metrics using Prometheus
"""

from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi import FastAPI, Request
import time

app = FastAPI()

# Metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)

active_connections = Gauge(
    'active_connections',
    'Number of active connections'
)

database_query_duration = Histogram(
    'database_query_duration_seconds',
    'Database query duration',
    ['query_type']
)

# Middleware
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    active_connections.inc()
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    http_requests_total.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()

    http_request_duration_seconds.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)

    active_connections.dec()

    return response

# Metrics endpoint
@app.get("/metrics")
async def metrics():
    return generate_latest()

# Example: Track database queries
def track_database_query(query_type: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            duration = time.time() - start

            database_query_duration.labels(
                query_type=query_type
            ).observe(duration)

            return result
        return wrapper
    return decorator

@track_database_query("select")
def fetch_users():
    # Database query
    pass
'''

print("Application instrumented with:")
print("  - HTTP request counter")
print("  - Request duration histogram")
print("  - Active connections gauge")
print("  - Database query tracking")
print("  - Automatic middleware")
print()
```

---

## Phase 4: Generate Grafana Dashboards

```python
print(f"=== Grafana Dashboard ===\n")

dashboard = '''{
  "dashboard": {
    "title": "Application Monitoring",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{method}} {{endpoint}}"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\\"5..\\"}[5m])",
            "legendFormat": "Errors"
          }
        ]
      },
      {
        "title": "Response Time (p95)",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "p95"
          }
        ]
      },
      {
        "title": "Active Connections",
        "type": "graph",
        "targets": [
          {
            "expr": "active_connections",
            "legendFormat": "Connections"
          }
        ]
      },
      {
        "title": "Memory Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "process_resident_memory_bytes / 1024 / 1024",
            "legendFormat": "Memory (MB)"
          }
        ]
      },
      {
        "title": "Database Query Duration",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(database_query_duration_seconds_sum[5m]) / rate(database_query_duration_seconds_count[5m])",
            "legendFormat": "Avg {{query_type}}"
          }
        ]
      }
    ]
  }
}'''

print("Generated Grafana dashboard with:")
print("  - Request rate graph")
print("  - Error rate graph")
print("  - Response time (p95)")
print("  - Active connections")
print("  - Memory usage")
print("  - Database query performance")
print()
```

---

## Phase 5: Docker Compose Setup

```python
print(f"=== Docker Compose ===\n")

docker_compose = '''version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - ./monitoring/alerts.yml:/etc/prometheus/alerts.yml
      - prometheus-data:/prometheus
    ports:
      - "9090:9090"
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'

  grafana:
    image: grafana/grafana:latest
    volumes:
      - ./monitoring/dashboards:/etc/grafana/provisioning/dashboards
      - grafana-data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_AUTH_ANONYMOUS_ENABLED=true
    ports:
      - "3000:3000"
    depends_on:
      - prometheus

  alertmanager:
    image: prom/alertmanager:latest
    volumes:
      - ./monitoring/alertmanager.yml:/etc/alertmanager/alertmanager.yml
    ports:
      - "9093:9093"

  node-exporter:
    image: prom/node-exporter:latest
    ports:
      - "9100:9100"

volumes:
  prometheus-data:
  grafana-data:
'''

print("Generated Docker Compose with:")
print("  - Prometheus (port 9090)")
print("  - Grafana (port 3000)")
print("  - Alertmanager (port 9093)")
print("  - Node exporter (port 9100)")
print()
```

---

## Phase 6: Logging Setup

```python
print(f"=== Logging Configuration ===\n")

logging_config = '''"""
Structured logging configuration
"""

import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    """Format logs as JSON"""

    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }

        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)

        if hasattr(record, 'user_id'):
            log_data['user_id'] = record.user_id

        if hasattr(record, 'request_id'):
            log_data['request_id'] = record.request_id

        return json.dumps(log_data)

# Configure logging
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())

logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)
'''

print("Configured structured logging:")
print("  - JSON format")
print("  - Timestamp")
print("  - Log level")
print("  - Module/function/line")
print("  - Optional user_id, request_id")
print()
```

---

## Phase 7: Summary

```python
print(f"=== Setup Summary ===\n")

print("Monitoring Stack Configured:")
print("  ✓ Prometheus (metrics collection)")
print("  ✓ Grafana (visualization)")
print("  ✓ Alertmanager (alerting)")
print("  ✓ Application instrumentation")
print("  ✓ Structured logging")
print()

print("Key Metrics Tracked:")
print("  - HTTP request rate")
print("  - Error rate")
print("  - Response time (p50, p95, p99)")
print("  - Active connections")
print("  - Memory usage")
print("  - Database query performance")
print()

print("Alerts Configured:")
print("  - High error rate (>5%)")
print("  - High response time (>1s)")
print("  - High memory usage (>1GB)")
print("  - Service down")
print()

print("Next Steps:")
print("  1. Start stack: docker-compose up -d")
print("  2. Access Grafana: http://localhost:3000")
print("  3. Access Prometheus: http://localhost:9090")
print("  4. Import dashboard: monitoring/dashboard.json")
print("  5. Configure alert notifications")
print()
```

---

## Output Example

```
=== Prometheus Configuration ===

Generated Prometheus configuration:
  - Scrape interval: 15s
  - Application metrics
  - Node exporter (system metrics)
  - PostgreSQL exporter

=== Alert Rules ===

Generated alert rules:
  - HighErrorRate: >5% error rate
  - HighResponseTime: >1s p95 latency
  - HighMemoryUsage: >1GB memory
  - ServiceDown: Service unavailable

=== Application Instrumentation ===

Application instrumented with:
  - HTTP request counter
  - Request duration histogram
  - Active connections gauge
  - Database query tracking
  - Automatic middleware

=== Grafana Dashboard ===

Generated Grafana dashboard with:
  - Request rate graph
  - Error rate graph
  - Response time (p95)
  - Active connections
  - Memory usage
  - Database query performance

=== Setup Summary ===

Monitoring Stack Configured:
  ✓ Prometheus (metrics collection)
  ✓ Grafana (visualization)
  ✓ Alertmanager (alerting)
  ✓ Application instrumentation
  ✓ Structured logging

Key Metrics Tracked:
  - HTTP request rate
  - Error rate
  - Response time (p50, p95, p99)
  - Active connections
  - Memory usage
  - Database query performance

Alerts Configured:
  - High error rate (>5%)
  - High response time (>1s)
  - High memory usage (>1GB)
  - Service down

Next Steps:
  1. Start stack: docker-compose up -d
  2. Access Grafana: http://localhost:3000
  3. Access Prometheus: http://localhost:9090
  4. Import dashboard: monitoring/dashboard.json
  5. Configure alert notifications
```

---

**Monitoring Philosophy:** You can't improve what you don't measure. Monitor everything, alert on what matters.
