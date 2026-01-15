# Project: Task Management GraphQL API

Build a GraphQL API for task management using Python and Strawberry.

---

## Autonomous Operation

**Execute this task completely without user interaction:**

1. **Proceed autonomously** - Make reasonable decisions without asking
2. **Implement all requirements** - Complete every feature listed below
3. **Write working code** - All queries and mutations must be functional
4. **Include tests** - Test coverage for core functionality
5. **Handle errors gracefully** - Proper GraphQL error responses
6. **No slash commands** - Do NOT use `/help`, `/commit`, or any `/` commands (not available in this execution mode)

**Prioritized execution order:**
1. Project structure and database setup
2. User authentication (register, login, JWT)
3. Project CRUD operations
4. Task CRUD operations
5. Comments and activity log
6. Subscriptions (real-time)
7. DataLoaders for N+1 prevention
8. Tests

---

## Requirements

### Core Features

1. **User Management**
   - Register user (email, password, name)
   - Login (returns JWT token)
   - Get current user profile
   - Update profile
   - Password change

2. **Project Management**
   - CRUD operations for projects
   - Project fields: name, description, status (active/archived), owner, members
   - Add/remove project members
   - Project-level permissions (owner, admin, member, viewer)

3. **Task Management**
   - CRUD for tasks within projects
   - Task fields: title, description, status, priority, assignee, due_date, labels
   - Status: todo, in_progress, review, done
   - Priority: low, medium, high, urgent
   - Task comments (add, edit, delete)
   - Task activity log (automatic: created, status_changed, assigned, etc.)

4. **Queries**
   ```graphql
   query {
     me { id, name, email }
     project(id: ID!) { ... }
     projects(status: ProjectStatus) { ... }
     task(id: ID!) { ... }
     tasks(projectId: ID!, status: TaskStatus, assignee: ID) { ... }
   }
   ```

5. **Mutations**
   ```graphql
   mutation {
     register(input: RegisterInput!) { user, token }
     login(email: String!, password: String!) { user, token }
     createProject(input: CreateProjectInput!) { project }
     updateTask(id: ID!, input: UpdateTaskInput!) { task }
     addComment(taskId: ID!, content: String!) { comment }
     # ... etc
   }
   ```

6. **Subscriptions**
   ```graphql
   subscription {
     taskUpdated(projectId: ID!) { task }
     commentAdded(taskId: ID!) { comment }
   }
   ```

### Technical Requirements

- Strawberry GraphQL
- FastAPI integration
- SQLAlchemy async with SQLite
- JWT authentication
- DataLoader for N+1 prevention
- Input validation
- Pagination (cursor-based)
- Tests with pytest

### Project Structure

```
taskql/
├── src/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/           # SQLAlchemy
│   ├── schema/           # Strawberry types
│   │   ├── types.py
│   │   ├── queries.py
│   │   ├── mutations.py
│   │   └── subscriptions.py
│   ├── resolvers/
│   ├── auth/
│   │   ├── jwt.py
│   │   └── permissions.py
│   └── loaders/          # DataLoaders
├── tests/
└── pyproject.toml
```

### Permission Rules

- Only project owner can delete project
- Only owner/admin can manage members
- Members can create/edit tasks
- Viewers can only read
- Users can only edit own comments

---

## Success Criteria

| Priority | Requirement | Validation |
|----------|-------------|------------|
| P0 | Authentication works (register/login) | JWT token returned |
| P0 | All queries return data | GraphQL responses valid |
| P0 | All mutations modify data | Database updated correctly |
| P1 | Permissions enforced | Unauthorized actions blocked |
| P1 | N+1 queries eliminated | DataLoaders reduce queries |
| P2 | Subscriptions deliver updates | Real-time events work |
| P2 | Input validation with clear errors | Invalid input rejected |

**Deliverables:** Working GraphQL API, authentication system, test suite.
