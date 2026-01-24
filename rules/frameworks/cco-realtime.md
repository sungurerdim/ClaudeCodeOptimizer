# Real-time
*Real-time communication rules*

**Inheritance:** Higher tiers include lower.

## Basic (RT:Basic)
**Trigger:** WebSocket/SSE detected

- **Reconnect-Logic**: Automatic reconnection with exponential backoff (1s, 2s, 4s, max 30s)
- **Heartbeat**: Connection health monitoring (ping/pong every 30s)
- **Stale-Data**: Handle disconnection gracefully, show stale data indicators
- **Message-Queue**: Queue messages during reconnection, replay on connect
- **State-Sync**: Sync state on reconnection to avoid missed updates

## Low-Latency (RT:LowLatency)
- **Binary-Protocol**: Protobuf/msgpack for performance (smaller payloads)
- **Edge-Compute**: Edge deployment for global users
- **Connection-Pooling**: Reuse connections where possible
- **Delta-Updates**: Send deltas instead of full state for efficiency
