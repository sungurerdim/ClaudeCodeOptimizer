# Runtimes
*Runtime-specific rules*

## Node.js (R:Node)
**Trigger:** {node_markers}

- **LTS-Version**: Use LTS versions
- **Engine-Lock**: Lock engine version in package.json
- **ESM-Prefer**: ESM over CommonJS
- **Event-Loop**: Use async I/O for event loop operations

## Bun (R:Bun)
**Trigger:** {bun_markers}

- **Bun-Native**: Use Bun native APIs when faster
- **Node-Compat**: Test Node.js compatibility
- **Macro-Use**: Macros for build-time optimization
- **Hot-Reload**: Leverage fast hot reload

## Deno (R:Deno)
**Trigger:** {deno_markers}

- **Permissions-Minimal**: Minimal --allow flags
- **Import-Map**: Import maps for dependencies
- **Test-Native**: Use Deno.test native
- **Fresh-Edge**: Deploy to Deno Deploy edge
