# Desktop
*Desktop application development rules*

**Trigger:** Electron/Tauri detected

## Base Desktop Rules
- **IPC-Secure**: Validate all IPC messages
- **Auto-Update**: Built-in update mechanism
- **Native-Feel**: Platform-appropriate UI/UX
- **Offline-First**: Graceful offline handling

## Electron (Desktop:Electron)
**Trigger:** {electron_deps}, {electron_config}

- **Context-Isolation**: contextIsolation: true always
- **Sandbox-Enable**: sandbox: true for renderers
- **Preload-Bridge**: Expose APIs via preload scripts only
- **CSP-Strict**: Content Security Policy in HTML

## Tauri (Desktop:Tauri)
**Trigger:** {tauri_deps}, {tauri_config}

- **Allowlist-Minimal**: Minimal API allowlist
- **Command-Validate**: Validate all command inputs in Rust
- **Bundle-Optimize**: Optimize bundle size (no unused APIs)
- **Sidecar-Safe**: Secure sidecar binaries
