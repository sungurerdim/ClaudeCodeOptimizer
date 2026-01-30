# Project Types
*Rules specific to application types*

## CLI (T:CLI)
**Trigger:** {entry_points}, {cli_deps}, {bin_dir}

- **Help-Examples**: --help with usage examples
- **Exit-Codes**: 0=success, N=specific error codes
- **Signal-Handle**: Graceful SIGINT/SIGTERM handling
- **Output-Modes**: Human-readable output
- **Config-Precedence**: env > file > args > defaults
- **NO_COLOR-Respect**: Check NO_COLOR env var before ANSI output, use isatty() to detect terminal
- **Unicode-Fallback**: Use ASCII alternatives for box-drawing chars when terminal encoding uncertain
- **Batch-UTF8**: In .bat/.cmd files, use `chcp 65001` for UTF-8 and avoid Unicode box characters

## Library (T:Library)
**Trigger:** {export_markers}, {lib_markers}

- **Minimal-Deps**: Minimize transitive dependencies
- **Tree-Shakeable**: ESM with no side effects (JS/TS)
- **Types-Included**: TypeScript types or JSDoc
- **Deprecation-Path**: Warn before removing APIs

## Service (T:Service)
**Trigger:** {container}, {ports}, {daemon_patterns}

- **Health-Endpoints**: /health + /ready endpoints for orchestrators
- **Graceful-Shutdown-Service**: Handle SIGTERM, drain connections before exit
- **Config-External**: Configuration via env vars or config files, not hardcoded
- **Logging-Structured**: JSON logging with correlation IDs
- **Metrics-Export**: Prometheus-compatible metrics endpoint
- **Connection-Pool**: Reuse database/HTTP connections
- **Timeout-Set**: Explicit timeouts on all external calls
- **Retry-Backoff**: Exponential backoff for transient failures

## Mobile (T:Mobile)
**Trigger:** {ios_project}, {android_build}, {rn_deps}, {flutter_manifest}

- **Offline-First**: Local-first with sync capability
- **Battery-Optimize**: Minimize background work and wake locks
- **Deep-Links**: Universal links / app links
- **Platform-Guidelines**: iOS HIG / Material Design compliance

## Desktop (T:Desktop)
**Trigger:** {electron_deps}, {tauri_deps}

- **Auto-Update**: Silent updates with manual option
- **Native-Integration**: System tray, notifications
- **Memory-Cleanup**: Prevent memory leaks in long-running apps
