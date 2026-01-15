# Observability Tools
*Monitoring and observability tool rules*

**Trigger:** Observability tool detected

*Note: These rules are specific to each observability tool. For SLA-based observability practices, see Observability Rules section.*

---

## Core Metrics Frameworks

### RED Metrics (User-Facing Services)

| Metric | Definition | Alert Threshold |
|--------|------------|-----------------|
| Rate | Requests per second | < 80% of baseline |
| Errors | Non-2xx / Total | > 0.1% |
| Duration (p50) | 50th percentile latency | > 200ms |
| Duration (p95) | 95th percentile latency | > 500ms |
| Duration (p99) | 99th percentile latency | > 1000ms |

**Use for**: APIs, web servers, microservices

### USE Metrics (Infrastructure)

| Metric | Definition | Alert Threshold |
|--------|------------|-----------------|
| Utilization | Resource usage % | > 80% sustained |
| Saturation | Queue depth | > 0 (tasks waiting) |
| Errors | Error count | > 0 |

**Use for**: CPU, memory, disk, network, connection pools

---

## Structured Logging Format

```json
{
  "timestamp": "2025-01-15T10:30:00.123Z",
  "level": "INFO",
  "message": "User login successful",
  "service": "auth-service",
  "trace_id": "abc123def456",
  "span_id": "span789",
  "user_id": "user-123",
  "duration_ms": 45,
  "metadata": {}
}
```

**Rules**:
- JSON format always (machine-parseable)
- Include `trace_id` for correlation
- Timestamp in ISO 8601 UTC
- Level as string (INFO, WARN, ERROR, DEBUG)
- NEVER log: passwords, tokens, PII, credit cards

---

## Alert Configuration

### Alert Fatigue Prevention

| Metric | Target | Action |
|--------|--------|--------|
| Actionable rate | 30-50% | Tune thresholds weekly |
| Alert consolidation | Group related | Batch within 5 min window |
| Escalation | Sustained only | Alert after 5 min sustained |

**Alert Structure**:
```yaml
primary_condition: "> threshold for 5 minutes"
recovery_condition: "< threshold for 2 minutes"
notification_chain:
  - 0min: email
  - 15min: slack
  - 30min: page
```

**Auto-resolve**: Clear alert when condition resolves

---

## Prometheus (Observability:Prometheus)
**Trigger:** {prometheus_config}

- **Scrape-Config**: Target scrape configuration
- **Alert-Rules**: Alert rule definition and evaluation
- **Service-Discovery**: Dynamic service discovery
- **Remote-Storage**: Long-term data retention configuration
- **Metric-Relabeling**: Metric relabeling for normalization
- **High-Availability**: HA deployment with replication

## Grafana (Observability:Grafana)
**Trigger:** {grafana_config}

- **Dashboard-Provisioning**: Dashboard as code
- **DataSource-Config**: Prometheus, Loki, and other datasource setup
- **Alert-Manager**: Alert routing and notification
- **Plugin-Management**: Community plugins installation
- **RBAC-Setup**: Role-based access control
- **Authentication**: LDAP, SAML, OAuth integration

## Datadog (Observability:Datadog)
**Trigger:** {datadog_config}

- **Agent-Configuration**: Datadog agent configuration
- **Custom-Metrics**: Custom metric reporting
- **Log-Collection**: Log collection and parsing
- **APM-Instrumentation**: APM instrumentation for tracing
- **Monitor-Creation**: Monitor definition for alerting
- **Synthetic-Tests**: Synthetic monitoring for uptime checks

## ELK Stack (Observability:ELK)
**Trigger:** {elk_config}

- **Elasticsearch-Config**: Elasticsearch cluster setup
- **Logstash-Pipelines**: Pipeline configuration for log parsing
- **Kibana-Dashboards**: Dashboard creation and visualization
- **Index-Lifecycle**: Index lifecycle management
- **Security-TLS**: TLS and authentication setup
- **Performance-Tuning**: Performance optimization for scale

## Jaeger (Observability:Jaeger)
**Trigger:** {jaeger_config}

- **Sampler-Config**: Sampling strategy configuration
- **Collector-Setup**: Collector deployment and configuration
- **Backend-Storage**: Storage backend selection (Elasticsearch)
- **Query-Service**: Query service for trace retrieval
- **Instrumentation**: OpenTelemetry instrumentation
- **Retention-Policy**: Trace retention and cleanup

## OpenTelemetry (Observability:OpenTelemetry)
**Trigger:** {otel_deps}

- **Instrumentation-Libraries**: Use standardized instrumentation
- **Exporter-Selection**: Exporter for backend (Prometheus, Jaeger)
- **Context-Propagation**: Trace context propagation across services
- **Resource-Attributes**: Resource attributes for identification
- **Sampling-Strategy**: Sampling configuration for cost management
- **Collector-Deployment**: OTel Collector for collection and processing

## Sentry (Observability:Sentry)
**Trigger:** {sentry_deps}

- **Project-Configuration**: Project setup and DSN management
- **Source-Maps**: Source map upload for JavaScript
- **Release-Tracking**: Release tracking for error grouping
- **Custom-Context**: Custom context for debugging
- **Integration-Setup**: Platform integrations (GitHub, Slack)
- **Performance-Monitoring**: Performance monitoring configuration

## New Relic (Observability:NewRelic)
**Trigger:** {newrelic_config}, {newrelic_deps}

- **Agent-Configuration**: Language-specific agent configuration
- **Custom-Instrumentation**: Custom instrumentation for business transactions
- **Distributed-Tracing**: Distributed tracing across services
- **Custom-Metrics**: Custom metrics for business KPIs
- **Alert-Policies**: Alert policies and notification channels
- **Workloads**: Workload grouping for related services
- **Synthetics**: Synthetic monitoring for availability

## Splunk (Observability:Splunk)
**Trigger:** {splunk_config}, {splunk_deps}

- **Log-Forwarding**: Configure log forwarding (Universal Forwarder, HEC)
- **Index-Strategy**: Index strategy for data organization
- **Search-Optimization**: Optimize searches with field extraction
- **Dashboard-Creation**: Create operational dashboards
- **Alert-Configuration**: Real-time alerting configuration
- **OTEL-Integration**: OpenTelemetry integration for traces/metrics
- **RBAC-Setup**: Role-based access control setup

## Dynatrace (Observability:Dynatrace)
**Trigger:** {dynatrace_config}, {dynatrace_deps}

- **OneAgent-Deployment**: OneAgent deployment and configuration
- **Auto-Discovery**: Automatic topology discovery
- **Custom-Services**: Custom service detection rules
- **Synthetic-Monitors**: Synthetic browser and HTTP monitors
- **Davis-AI**: Leverage Davis AI for root cause analysis
- **Metric-Ingestion**: Custom metric ingestion via API
- **Session-Replay**: Session replay for user experience analysis
