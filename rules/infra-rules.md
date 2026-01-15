# Infrastructure Rules
*Advanced infrastructure patterns*

## Infra:APIGateway
**Trigger:** {api_gateway_config}, {api_gateway_deps}

- **Rate-Limit-Config**: Per-route rate limiting with burst allowance
- **Auth-Plugin**: Centralized authentication at gateway
- **Route-Versioning**: API version routing (header or path)
- **Circuit-Breaker-Route**: Per-upstream circuit breaker
- **Logging-Structured**: Structured request/response logging
- **CORS-Config**: Centralized CORS configuration
- **Timeout-Upstream**: Upstream timeout configuration

## Infra:ServiceMesh
**Trigger:** {service_mesh_config}, {service_mesh_deps}

- **mTLS-Enable**: Enable mutual TLS between services
- **Retry-Policy**: Service-level retry policies
- **Timeout-Budget**: Request timeout budgets
- **Traffic-Split**: Traffic splitting for canary deployments
- **Observability-Auto**: Auto-inject observability sidecars
- **Auth-Policy**: Service-to-service authorization policies

## Infra:BuildCache
**Trigger:** {build_cache_config}

- **Cache-Key**: Deterministic cache key generation
- **Remote-Cache**: Enable remote cache for CI
- **Artifact-Share**: Share build artifacts across pipelines
- **Invalidation-Explicit**: Explicit cache invalidation rules
- **Size-Limit**: Cache size limits per project
- **TTL-Set**: Set cache TTL based on artifact type
