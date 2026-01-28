# Deployment
*Common patterns across all platforms*

## Universal Requirements

| Requirement | Implementation |
|-------------|----------------|
| Health Check | `/health` endpoint returning 200 |
| Graceful Shutdown | Handle SIGTERM, drain connections |
| Environment Config | Secrets via env vars or secrets manager |
| Auto-scaling | Configure min/max instances |
| Custom Domain | SSL/TLS with auto-renewal |

## Platform Gotchas

### Serverless (Vercel, Netlify, Lambda)
- **Cold Start**: Minimize dependencies, consider provisioned concurrency
- **Timeout**: Default 10s, configure explicitly for long operations
- **Stateless**: No local file storage between invocations

### Container (Cloud Run, App Runner, Fly.io)
- **Memory**: Set appropriate limits (OOM kills are silent)
- **CPU Allocation**: "Always-on" vs "request-based" affects cold start
- **Health Probes**: Configure liveness AND readiness separately

### PaaS (Heroku, Railway, Render)
- **Procfile/Config**: Explicit process types and commands
- **Release Phase**: Run migrations before traffic switch
- **Ephemeral Storage**: Use externalized state storage

## Traffic Management

| Strategy | Use Case |
|----------|----------|
| Blue-Green | Zero-downtime with instant rollback |
| Canary | Gradual rollout (1% → 10% → 100%) |
| Feature Flags | Decouple deploy from release |
