# Project: Real-time Chat Server

Build a real-time chat server using Go with WebSocket support.

---

## Autonomous Operation

**Execute this task completely without user interaction:**

1. **Proceed autonomously** - Make reasonable decisions without asking
2. **Implement all requirements** - Complete every feature listed below
3. **Write working code** - WebSocket connections must work
4. **Include tests** - Test coverage for core functionality
5. **Handle errors gracefully** - Proper error codes and messages

**Prioritized execution order:**
1. Project structure and basic HTTP server
2. WebSocket upgrade and connection handling
3. Room creation and management
4. Message routing within rooms
5. User presence tracking
6. REST endpoints for room listing
7. Rate limiting and moderation
8. Tests

---

## Requirements

### Core Features

1. **Room Management**
   - Create room (name, max_users, is_private)
   - Join room (with optional password for private rooms)
   - Leave room
   - List active rooms with user counts
   - Room auto-cleanup when empty (after 5 min)

2. **Messaging**
   - Send message to room
   - Message format: `{ sender, content, timestamp, room_id, type }`
   - Message types: text, system (join/leave), typing
   - Message history (last 100 per room, in-memory)
   - Typing indicators

3. **User Management**
   - Connect with username (unique within room)
   - Presence tracking (online/offline)
   - User list per room
   - Ban user from room (moderator only)
   - Room creator is auto-moderator

4. **WebSocket Protocol**
   ```json
   // Client -> Server
   { "action": "join", "room": "general", "username": "alice" }
   { "action": "message", "room": "general", "content": "Hello!" }
   { "action": "typing", "room": "general" }
   { "action": "leave", "room": "general" }

   // Server -> Client
   { "type": "joined", "room": "general", "users": [...] }
   { "type": "message", "sender": "bob", "content": "Hi!", "ts": 1234567890 }
   { "type": "user_joined", "username": "charlie" }
   { "type": "typing", "username": "bob" }
   { "type": "error", "code": "room_full", "message": "Room is full" }
   ```

5. **REST Endpoints**
   - GET /rooms - List all public rooms
   - GET /rooms/{id} - Room details
   - POST /rooms - Create room
   - GET /health - Health check

### Technical Requirements

- Go 1.21+
- gorilla/websocket or nhooyr/websocket
- Chi or Gin for REST routes
- In-memory storage (no database)
- Graceful shutdown
- Connection heartbeat/ping-pong
- Rate limiting (max 10 messages/second per user)
- Tests with go test

### Project Structure

```
chatserver/
├── cmd/
│   └── server/
│       └── main.go
├── internal/
│   ├── server/
│   │   └── server.go
│   ├── hub/
│   │   ├── hub.go        # Central message hub
│   │   └── room.go       # Room management
│   ├── client/
│   │   └── client.go     # WebSocket client
│   ├── message/
│   │   └── types.go      # Message types
│   └── handler/
│       ├── websocket.go
│       └── rest.go
├── pkg/
│   └── protocol/
│       └── protocol.go   # Message encoding/decoding
├── go.mod
└── go.sum
```

### Error Codes

```
room_not_found   - Room doesn't exist
room_full        - Room at capacity
username_taken   - Username already in use in room
not_authorized   - Action requires moderator
rate_limited     - Too many messages
invalid_message  - Malformed message
```

---

## Success Criteria

| Priority | Requirement | Validation |
|----------|-------------|------------|
| P0 | WebSocket connections work | Client connects successfully |
| P0 | Messages delivered to room members | All users receive message |
| P1 | Multiple rooms work simultaneously | Create and use 2+ rooms |
| P1 | User presence updates correctly | Join/leave broadcasted |
| P2 | Rate limiting enforced | Rapid messages blocked |
| P2 | Graceful disconnect handling | No crashes on disconnect |
| P2 | Tests cover main scenarios | go test passes |

**Deliverables:** Working WebSocket server, REST API, test suite.
