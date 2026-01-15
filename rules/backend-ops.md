# Backend Operations
*Operational rules for backend services and CLI applications*

**Trigger:** T:Service + CI:* | T:CLI + CI:*

## Full Operations (Ops:Full)
**Trigger:** T:Service + CI:*

- **Config-as-Code**: Versioned, environment-aware config
- **Health-Endpoints**: /health + /ready endpoints
- **Graceful-Shutdown-Ops**: Drain connections on SIGTERM
- **Observability**: Metrics + logs + traces
- **CI-Gates**: lint + test + coverage gates
- **Zero-Downtime**: Blue-green or canary deployments
- **Feature-Flags**: Decouple deploy from release

## Basic Operations (Ops:Basic)
**Trigger:** T:CLI + CI:*

- **Config-as-Code**: Versioned configuration
