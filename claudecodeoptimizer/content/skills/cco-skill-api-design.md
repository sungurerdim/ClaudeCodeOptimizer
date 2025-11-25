---
name: cco-skill-api-design
description: Design robust, scalable APIs following REST, GraphQL, and gRPC best practices. Covers versioning strategies, backward compatibility, rate limiting, authentication patterns, and OpenAPI documentation.
keywords: [api, rest, restful, graphql, grpc, openapi, swagger, versioning, rate limiting, pagination, hateoas, api gateway, endpoint, http methods, status codes, api security]
category: architecture
related_commands:
  action_types: [audit, fix, generate]
  categories: [architecture, security, documentation]
pain_points: [1, 5, 6, 7]
---

# API Design - REST, GraphQL, gRPC Best Practices

> **Standards:** Format defined in [cco-standards.md](../cco-standards.md)
> **Discovery:** See [cco-standards.md](../cco-standards.md#18-command-discovery-protocol)


## Purpose

Design and implement production-ready APIs that are secure, scalable, maintainable, and developer-friendly.

**Solves**:
- **Inconsistent API Design**: Ad-hoc endpoint naming, inconsistent response formats
- **Breaking Changes**: Lack of versioning strategy causes client breakage
- **Security Gaps**: Missing rate limiting, improper authentication, injection vulnerabilities
- **Performance Issues**: N+1 queries in GraphQL, inefficient pagination, no caching
- **Poor Documentation**: Missing or outdated API docs, no contract testing

**Impact**: High

---

---

## Domain

API architecture, web services, microservices communication, client-server contracts.

---

## Core Techniques

### 1. RESTful API Design Principles

**Resource Naming:**
```python
# ✅ GOOD: Nouns for resources, plural for collections
GET    /api/v1/users           # List users
GET    /api/v1/users/{id}      # Get single user
POST   /api/v1/users           # Create user
PUT    /api/v1/users/{id}      # Replace user
PATCH  /api/v1/users/{id}      # Partial update
DELETE /api/v1/users/{id}      # Delete user

# ✅ GOOD: Nested resources for relationships
GET    /api/v1/users/{id}/orders        # User's orders
GET    /api/v1/users/{id}/orders/{oid}  # Specific order
POST   /api/v1/users/{id}/orders        # Create order for user

# ❌ BAD: Verbs in URLs
GET    /api/v1/getUsers
POST   /api/v1/createUser
POST   /api/v1/deleteUser/{id}

# ❌ BAD: Inconsistent naming
GET    /api/v1/user             # Singular
GET    /api/v1/order-items      # Kebab-case
GET    /api/v1/productCategories # camelCase
```

**HTTP Methods & Status Codes:**
```python
# HTTP Methods
GET     # Retrieve (idempotent, cacheable)
POST    # Create (not idempotent)
PUT     # Replace entire resource (idempotent)
PATCH   # Partial update (not idempotent)
DELETE  # Remove (idempotent)
HEAD    # Get headers only (for caching)
OPTIONS # Get allowed methods (CORS preflight)

# Success Codes (2xx)
200 OK              # GET, PUT, PATCH success
201 Created         # POST success (include Location header)
202 Accepted        # Async operation started
204 No Content      # DELETE success, no body

# Client Error Codes (4xx)
400 Bad Request     # Invalid input
401 Unauthorized    # Authentication required
403 Forbidden       # Authenticated but not authorized
404 Not Found       # Resource doesn't exist
405 Method Not Allowed
409 Conflict        # Resource conflict (duplicate, version mismatch)
422 Unprocessable Entity  # Validation failed
429 Too Many Requests     # Rate limit exceeded

# Server Error Codes (5xx)
500 Internal Server Error  # Unexpected error
502 Bad Gateway           # Upstream service error
503 Service Unavailable   # Maintenance/overload
504 Gateway Timeout       # Upstream timeout
```

**Response Format Consistency:**
```python
# ✅ GOOD: Consistent envelope format
{
    "status": "success",
    "data": {
        "id": 123,
        "name": "John Doe",
        "email": "john@example.com"
    },
    "meta": {
        "request_id": "req_abc123",
        "timestamp": "2025-01-15T10:30:00Z"
    }
}

# ✅ GOOD: Error response format
{
    "status": "error",
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid input data",
        "details": [
            {
                "field": "email",
                "message": "Invalid email format"
            },
            {
                "field": "age",
                "message": "Must be a positive integer"
            }
        ]
    },
    "meta": {
        "request_id": "req_def456",
        "timestamp": "2025-01-15T10:30:00Z"
    }
}

# ✅ GOOD: Collection response with pagination
{
    "status": "success",
    "data": [
        {"id": 1, "name": "Item 1"},
        {"id": 2, "name": "Item 2"}
    ],
    "pagination": {
        "total": 100,
        "page": 1,
        "per_page": 20,
        "total_pages": 5,
        "has_next": true,
        "has_prev": false
    },
    "links": {
        "self": "/api/v1/items?page=1",
        "next": "/api/v1/items?page=2",
        "last": "/api/v1/items?page=5"
    }
}
```

**Flask/FastAPI Implementation:**
```python
from flask import Flask, jsonify, request, abort
from functools import wraps

app = Flask(__name__)

# ✅ GOOD: Consistent response helper
def api_response(data=None, status="success", meta=None, code=200):
    response = {
        "status": status,
        "data": data,
        "meta": {
            "request_id": request.headers.get("X-Request-ID"),
            "timestamp": datetime.utcnow().isoformat()
        }
    }
    if meta:
        response["meta"].update(meta)
    return jsonify(response), code


def api_error(message, code, error_code=None, details=None):
    return jsonify({
        "status": "error",
        "error": {
            "code": error_code or f"HTTP_{code}",
            "message": message,
            "details": details
        },
        "meta": {
            "request_id": request.headers.get("X-Request-ID"),
            "timestamp": datetime.utcnow().isoformat()
        }
    }), code


# ✅ GOOD: RESTful resource endpoints
@app.route('/api/v1/users', methods=['GET'])
@require_auth
def list_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    # Validate pagination
    per_page = min(per_page, 100)  # Max 100 items

    users = User.query.paginate(page=page, per_page=per_page)

    return api_response(
        data=[u.to_dict() for u in users.items],
        meta={
            "pagination": {
                "total": users.total,
                "page": users.page,
                "per_page": users.per_page,
                "total_pages": users.pages,
                "has_next": users.has_next,
                "has_prev": users.has_prev
            }
        }
    )


@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
@require_auth
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return api_error("User not found", 404, "USER_NOT_FOUND")

    return api_response(data=user.to_dict())


@app.route('/api/v1/users', methods=['POST'])
@require_auth
def create_user():
    data = request.get_json()

    # Validate input
    errors = validate_user_input(data)
    if errors:
        return api_error(
            "Validation failed",
            422,
            "VALIDATION_ERROR",
            details=errors
        )

    user = User(**data)
    db.session.add(user)
    db.session.commit()

    response = api_response(data=user.to_dict(), code=201)
    response[0].headers['Location'] = f'/api/v1/users/{user.id}'
    return response


@app.route('/api/v1/users/<int:user_id>', methods=['PATCH'])
@require_auth
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return api_error("User not found", 404, "USER_NOT_FOUND")

    data = request.get_json()
    allowed_fields = {'name', 'email', 'phone'}

    for key, value in data.items():
        if key in allowed_fields:
            setattr(user, key, value)

    db.session.commit()
    return api_response(data=user.to_dict())


@app.route('/api/v1/users/<int:user_id>', methods=['DELETE'])
@require_auth
@require_role('admin')
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return api_error("User not found", 404, "USER_NOT_FOUND")

    db.session.delete(user)
    db.session.commit()
    return '', 204
```

---

### 2. API Versioning Strategies

**URL Path Versioning (Recommended):**
```python
# ✅ GOOD: Version in URL path
GET /api/v1/users
GET /api/v2/users

# Flask Blueprint implementation
from flask import Blueprint

api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')
api_v2 = Blueprint('api_v2', __name__, url_prefix='/api/v2')

@api_v1.route('/users')
def get_users_v1():
    # V1 returns flat structure
    return jsonify([{"id": u.id, "name": u.name} for u in users])

@api_v2.route('/users')
def get_users_v2():
    # V2 returns enhanced structure with metadata
    return jsonify({
        "data": [{"id": u.id, "name": u.name, "profile": u.profile} for u in users],
        "meta": {"version": "2.0"}
    })

app.register_blueprint(api_v1)
app.register_blueprint(api_v2)
```

**Header Versioning:**
```python
# ✅ GOOD: Version in Accept header
GET /api/users
Accept: application/vnd.myapi.v2+json

# Implementation
@app.route('/api/users')
def get_users():
    version = parse_version_from_accept_header(request.headers.get('Accept'))

    if version == 2:
        return get_users_v2()
    else:
        return get_users_v1()


def parse_version_from_accept_header(accept_header: str) -> int:
    """Extract version from Accept header."""
    if not accept_header:
        return 1  # Default to v1

    # Pattern: application/vnd.myapi.v{N}+json
    match = re.search(r'vnd\.myapi\.v(\d+)', accept_header)
    if match:
        return int(match.group(1))
    return 1
```

**Query Parameter Versioning:**
```python
# ⚠️ ACCEPTABLE: Version as query param
GET /api/users?version=2

@app.route('/api/users')
def get_users():
    version = request.args.get('version', 1, type=int)

    if version == 2:
        return get_users_v2()
    return get_users_v1()
```

**Versioning Strategy Comparison:**

| Strategy | Pros | Cons | Best For |
|----------|------|------|----------|
| **URL Path** | Clear, cacheable, easy routing | URL changes between versions | Public APIs |
| **Header** | Clean URLs, content negotiation | Hidden, harder to test | Internal APIs |
| **Query Param** | Simple, visible | Can be cached incorrectly | Simple APIs |

---

### 3. Pagination Patterns

**Offset-Based Pagination:**
```python
# ✅ GOOD: Traditional pagination
GET /api/v1/users?page=2&per_page=20

@app.route('/api/v1/users')
def list_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)

    # SQLAlchemy pagination
    pagination = User.query.order_by(User.created_at.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return jsonify({
        "data": [u.to_dict() for u in pagination.items],
        "pagination": {
            "total": pagination.total,
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total_pages": pagination.pages
        },
        "links": {
            "self": url_for('list_users', page=page, per_page=per_page),
            "first": url_for('list_users', page=1, per_page=per_page),
            "last": url_for('list_users', page=pagination.pages, per_page=per_page),
            "next": url_for('list_users', page=page+1, per_page=per_page) if pagination.has_next else None,
            "prev": url_for('list_users', page=page-1, per_page=per_page) if pagination.has_prev else None
        }
    })
```

**Cursor-Based Pagination (Better for Large Datasets):**
```python
# ✅ GOOD: Cursor pagination (no offset performance issues)
GET /api/v1/users?cursor=eyJpZCI6MTAwfQ&limit=20

import base64
import json

def encode_cursor(data: dict) -> str:
    """Encode cursor data to base64 string."""
    return base64.urlsafe_b64encode(json.dumps(data).encode()).decode()

def decode_cursor(cursor: str) -> dict:
    """Decode cursor from base64 string."""
    try:
        return json.loads(base64.urlsafe_b64decode(cursor.encode()))
    except:
        return {}


@app.route('/api/v1/users')
def list_users_cursor():
    cursor = request.args.get('cursor')
    limit = min(request.args.get('limit', 20, type=int), 100)

    query = User.query.order_by(User.id.desc())

    if cursor:
        cursor_data = decode_cursor(cursor)
        if 'id' in cursor_data:
            query = query.filter(User.id < cursor_data['id'])

    users = query.limit(limit + 1).all()  # Fetch one extra to check has_next

    has_next = len(users) > limit
    users = users[:limit]

    next_cursor = None
    if has_next and users:
        next_cursor = encode_cursor({"id": users[-1].id})

    return jsonify({
        "data": [u.to_dict() for u in users],
        "pagination": {
            "limit": limit,
            "has_next": has_next,
            "next_cursor": next_cursor
        }
    })
```

**Keyset Pagination (Most Efficient):**
```python
# ✅ GOOD: Keyset pagination for consistent ordering
GET /api/v1/orders?after_id=1000&after_date=2025-01-01&limit=20

@app.route('/api/v1/orders')
def list_orders():
    after_id = request.args.get('after_id', type=int)
    after_date = request.args.get('after_date')
    limit = min(request.args.get('limit', 20, type=int), 100)

    query = Order.query.order_by(Order.created_at.desc(), Order.id.desc())

    if after_id and after_date:
        # Keyset condition: (created_at, id) < (after_date, after_id)
        query = query.filter(
            db.or_(
                Order.created_at < after_date,
                db.and_(
                    Order.created_at == after_date,
                    Order.id < after_id
                )
            )
        )

    orders = query.limit(limit + 1).all()
    has_next = len(orders) > limit
    orders = orders[:limit]

    return jsonify({
        "data": [o.to_dict() for o in orders],
        "pagination": {
            "limit": limit,
            "has_next": has_next,
            "next_params": {
                "after_id": orders[-1].id,
                "after_date": orders[-1].created_at.isoformat()
            } if has_next else None
        }
    })
```

**Pagination Comparison:**

| Method | Pros | Cons | Best For |
|--------|------|------|----------|
| **Offset** | Simple, total count | Slow for large offsets, data shifts | Small datasets |
| **Cursor** | Consistent, no duplicates | Can't jump to page | Infinite scroll |
| **Keyset** | Very fast, stable | Complex for multi-column sort | Large datasets |

---

### 4. Rate Limiting

**Token Bucket Implementation:**
```python
import time
from functools import wraps
from flask import request, jsonify
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)


class RateLimiter:
    """Token bucket rate limiter with Redis backend."""

    def __init__(
        self,
        key_prefix: str = "ratelimit",
        rate: int = 100,
        per: int = 60,
        burst: int = 10
    ):
        self.key_prefix = key_prefix
        self.rate = rate      # Requests per period
        self.per = per        # Period in seconds
        self.burst = burst    # Burst allowance

    def get_key(self, identifier: str) -> str:
        return f"{self.key_prefix}:{identifier}"

    def is_allowed(self, identifier: str) -> tuple[bool, dict]:
        """
        Check if request is allowed.

        Returns:
            (allowed: bool, info: dict with remaining, reset_at)
        """
        key = self.get_key(identifier)
        now = time.time()

        pipe = redis_client.pipeline()

        # Get current state
        pipe.hgetall(key)
        pipe.execute()

        # Token bucket algorithm
        data = redis_client.hgetall(key)
        tokens = float(data.get(b'tokens', self.rate + self.burst))
        last_update = float(data.get(b'last_update', now))

        # Refill tokens based on time passed
        elapsed = now - last_update
        tokens = min(
            self.rate + self.burst,
            tokens + (elapsed * (self.rate / self.per))
        )

        allowed = tokens >= 1
        if allowed:
            tokens -= 1

        # Update state
        pipe = redis_client.pipeline()
        pipe.hset(key, mapping={
            'tokens': tokens,
            'last_update': now
        })
        pipe.expire(key, self.per * 2)  # Expire after 2 periods
        pipe.execute()

        reset_at = int(now + ((self.rate - tokens) * (self.per / self.rate)))

        return allowed, {
            "remaining": int(tokens),
            "limit": self.rate,
            "reset_at": reset_at
        }


# ✅ GOOD: Rate limit decorator
def rate_limit(limiter: RateLimiter, key_func=None):
    """
    Rate limiting decorator.

    Args:
        limiter: RateLimiter instance
        key_func: Function to extract identifier (default: IP address)
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # Get identifier
            if key_func:
                identifier = key_func()
            else:
                # Default: use IP or user ID
                identifier = (
                    getattr(g, 'current_user_id', None) or
                    request.headers.get('X-Forwarded-For', request.remote_addr)
                )

            allowed, info = limiter.is_allowed(identifier)

            # Add rate limit headers
            response_headers = {
                'X-RateLimit-Limit': str(info['limit']),
                'X-RateLimit-Remaining': str(info['remaining']),
                'X-RateLimit-Reset': str(info['reset_at'])
            }

            if not allowed:
                response = jsonify({
                    "status": "error",
                    "error": {
                        "code": "RATE_LIMIT_EXCEEDED",
                        "message": "Too many requests. Please retry later.",
                        "retry_after": info['reset_at'] - int(time.time())
                    }
                })
                response.status_code = 429
                for header, value in response_headers.items():
                    response.headers[header] = value
                response.headers['Retry-After'] = str(info['reset_at'] - int(time.time()))
                return response

            # Execute function
            response = f(*args, **kwargs)

            # Add headers to successful response
            if hasattr(response, 'headers'):
                for header, value in response_headers.items():
                    response.headers[header] = value

            return response
        return wrapped
    return decorator


# ✅ GOOD: Different rate limits for different endpoints
api_limiter = RateLimiter(rate=100, per=60)  # 100 req/min
auth_limiter = RateLimiter(rate=5, per=60)   # 5 req/min for auth
search_limiter = RateLimiter(rate=30, per=60)  # 30 req/min for search


@app.route('/api/v1/users')
@rate_limit(api_limiter)
def list_users():
    # ...
    pass


@app.route('/api/v1/auth/login', methods=['POST'])
@rate_limit(auth_limiter)
def login():
    # Stricter rate limit for auth endpoints
    pass


@app.route('/api/v1/search')
@rate_limit(search_limiter)
def search():
    # Moderate rate limit for search
    pass
```

**Tiered Rate Limiting:**
```python
# ✅ GOOD: Different limits per user tier
RATE_LIMITS = {
    "free": {"rate": 100, "per": 3600},      # 100/hour
    "basic": {"rate": 1000, "per": 3600},    # 1000/hour
    "premium": {"rate": 10000, "per": 3600}, # 10000/hour
    "enterprise": {"rate": 100000, "per": 3600}  # 100000/hour
}

def get_user_rate_limit():
    """Get rate limit based on user tier."""
    user = g.get('current_user')
    if not user:
        return RATE_LIMITS["free"]

    tier = user.subscription_tier or "free"
    return RATE_LIMITS.get(tier, RATE_LIMITS["free"])
```

---

### 5. GraphQL Best Practices

**Schema Design:**
```graphql
# ✅ GOOD: Well-designed GraphQL schema

# Types with clear naming
type User {
  id: ID!
  email: String!
  name: String!
  profile: UserProfile
  orders(first: Int, after: String): OrderConnection!
  createdAt: DateTime!
  updatedAt: DateTime!
}

type UserProfile {
  avatar: String
  bio: String
  location: String
}

# Relay-style pagination
type OrderConnection {
  edges: [OrderEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type OrderEdge {
  node: Order!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

type Order {
  id: ID!
  user: User!
  items: [OrderItem!]!
  total: Money!
  status: OrderStatus!
  createdAt: DateTime!
}

# Custom scalars
scalar DateTime
scalar Money

# Enums for fixed values
enum OrderStatus {
  PENDING
  PROCESSING
  SHIPPED
  DELIVERED
  CANCELLED
}

# Input types for mutations
input CreateUserInput {
  email: String!
  name: String!
  password: String!
}

input UpdateUserInput {
  name: String
  profile: UpdateProfileInput
}

input UpdateProfileInput {
  avatar: String
  bio: String
  location: String
}

# Queries
type Query {
  user(id: ID!): User
  users(first: Int, after: String, filter: UserFilter): UserConnection!
  me: User
  order(id: ID!): Order
  orders(first: Int, after: String, status: OrderStatus): OrderConnection!
}

# Mutations with clear naming
type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
  updateUser(id: ID!, input: UpdateUserInput!): UpdateUserPayload!
  deleteUser(id: ID!): DeleteUserPayload!
  createOrder(input: CreateOrderInput!): CreateOrderPayload!
}

# Mutation payloads with errors
type CreateUserPayload {
  user: User
  errors: [UserError!]!
}

type UserError {
  field: String
  message: String!
  code: String!
}
```

**N+1 Query Prevention with DataLoader:**
```python
from promise import Promise
from promise.dataloader import DataLoader
import graphene
from graphene import relay

# ✅ GOOD: DataLoader to batch database queries
class UserLoader(DataLoader):
    def batch_load_fn(self, user_ids):
        users = User.query.filter(User.id.in_(user_ids)).all()
        user_map = {u.id: u for u in users}
        return Promise.resolve([user_map.get(uid) for uid in user_ids])


class OrderLoader(DataLoader):
    def batch_load_fn(self, user_ids):
        # Batch load orders for multiple users
        orders = Order.query.filter(Order.user_id.in_(user_ids)).all()

        # Group by user_id
        orders_by_user = {}
        for order in orders:
            if order.user_id not in orders_by_user:
                orders_by_user[order.user_id] = []
            orders_by_user[order.user_id].append(order)

        return Promise.resolve([
            orders_by_user.get(uid, []) for uid in user_ids
        ])


# Context with loaders
def get_context():
    return {
        'user_loader': UserLoader(),
        'order_loader': OrderLoader()
    }


# ✅ GOOD: Use DataLoader in resolvers
class UserType(graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node,)

    id = graphene.ID(required=True)
    email = graphene.String(required=True)
    name = graphene.String(required=True)
    orders = graphene.List(lambda: OrderType)

    def resolve_orders(self, info):
        # Uses DataLoader - batches multiple user.orders queries
        return info.context['order_loader'].load(self.id)


class OrderType(graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node,)

    id = graphene.ID(required=True)
    user = graphene.Field(lambda: UserType)
    total = graphene.Float(required=True)

    def resolve_user(self, info):
        # Uses DataLoader - batches multiple order.user queries
        return info.context['user_loader'].load(self.user_id)
```

**Query Complexity & Depth Limiting:**
```python
from graphql import GraphQLError
from graphene import ObjectType, Schema

# ✅ GOOD: Limit query depth and complexity
class QueryDepthLimiter:
    """Middleware to limit query depth."""

    def __init__(self, max_depth: int = 10):
        self.max_depth = max_depth

    def resolve(self, next, root, info, **kwargs):
        depth = self._get_depth(info.field_nodes[0])
        if depth > self.max_depth:
            raise GraphQLError(
                f"Query depth {depth} exceeds maximum allowed depth {self.max_depth}"
            )
        return next(root, info, **kwargs)

    def _get_depth(self, node, depth=0):
        if not hasattr(node, 'selection_set') or not node.selection_set:
            return depth

        max_child_depth = depth
        for selection in node.selection_set.selections:
            child_depth = self._get_depth(selection, depth + 1)
            max_child_depth = max(max_child_depth, child_depth)

        return max_child_depth


class QueryComplexityLimiter:
    """Middleware to limit query complexity."""

    def __init__(self, max_complexity: int = 100):
        self.max_complexity = max_complexity

    def resolve(self, next, root, info, **kwargs):
        complexity = self._calculate_complexity(info.field_nodes[0])
        if complexity > self.max_complexity:
            raise GraphQLError(
                f"Query complexity {complexity} exceeds maximum {self.max_complexity}"
            )
        return next(root, info, **kwargs)

    def _calculate_complexity(self, node, multiplier=1):
        base_cost = 1 * multiplier
        total = base_cost

        if hasattr(node, 'selection_set') and node.selection_set:
            # Check for list arguments (first, last)
            child_multiplier = 1
            for arg in getattr(node, 'arguments', []):
                if arg.name.value in ('first', 'last'):
                    child_multiplier = int(arg.value.value)

            for selection in node.selection_set.selections:
                total += self._calculate_complexity(selection, child_multiplier)

        return total


# Apply middleware
schema = Schema(
    query=Query,
    mutation=Mutation,
    middleware=[
        QueryDepthLimiter(max_depth=10),
        QueryComplexityLimiter(max_complexity=100)
    ]
)
```

---

### 6. gRPC Patterns

**Protocol Buffer Definition:**
```protobuf
// user_service.proto
syntax = "proto3";

package userservice;

option go_package = "github.com/myorg/userservice/pb";

import "google/protobuf/timestamp.proto";
import "google/protobuf/empty.proto";

// Service definition
service UserService {
  // Unary RPC
  rpc GetUser(GetUserRequest) returns (User);
  rpc CreateUser(CreateUserRequest) returns (User);
  rpc UpdateUser(UpdateUserRequest) returns (User);
  rpc DeleteUser(DeleteUserRequest) returns (google.protobuf.Empty);

  // Server streaming
  rpc ListUsers(ListUsersRequest) returns (stream User);

  // Client streaming
  rpc BatchCreateUsers(stream CreateUserRequest) returns (BatchCreateResponse);

  // Bidirectional streaming
  rpc SyncUsers(stream UserSyncRequest) returns (stream UserSyncResponse);
}

// Messages
message User {
  int64 id = 1;
  string email = 2;
  string name = 3;
  UserProfile profile = 4;
  google.protobuf.Timestamp created_at = 5;
  google.protobuf.Timestamp updated_at = 6;
}

message UserProfile {
  string avatar = 1;
  string bio = 2;
  string location = 3;
}

message GetUserRequest {
  int64 user_id = 1;
}

message CreateUserRequest {
  string email = 1;
  string name = 2;
  string password = 3;
  UserProfile profile = 4;
}

message UpdateUserRequest {
  int64 user_id = 1;
  optional string name = 2;
  optional UserProfile profile = 3;
}

message DeleteUserRequest {
  int64 user_id = 1;
}

message ListUsersRequest {
  int32 page_size = 1;
  string page_token = 2;
  UserFilter filter = 3;
}

message UserFilter {
  optional string email_contains = 1;
  optional string name_contains = 2;
}

message BatchCreateResponse {
  int32 created_count = 1;
  int32 failed_count = 2;
  repeated string errors = 3;
}

message UserSyncRequest {
  oneof action {
    User upsert = 1;
    int64 delete_id = 2;
  }
}

message UserSyncResponse {
  bool success = 1;
  string message = 2;
  User user = 3;
}
```

**Python gRPC Server:**
```python
import grpc
from concurrent import futures
import user_service_pb2
import user_service_pb2_grpc


class UserServicer(user_service_pb2_grpc.UserServiceServicer):
    """gRPC User Service implementation."""

    def GetUser(self, request, context):
        user = db.query(User).get(request.user_id)
        if not user:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"User {request.user_id} not found")
            return user_service_pb2.User()

        return self._user_to_proto(user)

    def CreateUser(self, request, context):
        # Validate
        if not request.email:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Email is required")
            return user_service_pb2.User()

        # Check duplicate
        if db.query(User).filter_by(email=request.email).first():
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details("User with this email already exists")
            return user_service_pb2.User()

        user = User(
            email=request.email,
            name=request.name,
            password_hash=hash_password(request.password)
        )
        db.add(user)
        db.commit()

        return self._user_to_proto(user)

    def ListUsers(self, request, context):
        """Server streaming: yield users one by one."""
        query = db.query(User)

        if request.filter.email_contains:
            query = query.filter(
                User.email.contains(request.filter.email_contains)
            )

        page_size = request.page_size or 100
        offset = self._decode_page_token(request.page_token)

        users = query.offset(offset).limit(page_size).all()

        for user in users:
            yield self._user_to_proto(user)

    def BatchCreateUsers(self, request_iterator, context):
        """Client streaming: receive users and batch create."""
        created = 0
        failed = 0
        errors = []

        for request in request_iterator:
            try:
                user = User(
                    email=request.email,
                    name=request.name,
                    password_hash=hash_password(request.password)
                )
                db.add(user)
                db.commit()
                created += 1
            except Exception as e:
                failed += 1
                errors.append(str(e))
                db.rollback()

        return user_service_pb2.BatchCreateResponse(
            created_count=created,
            failed_count=failed,
            errors=errors
        )

    def SyncUsers(self, request_iterator, context):
        """Bidirectional streaming: sync users in real-time."""
        for request in request_iterator:
            if request.HasField('upsert'):
                user_data = request.upsert
                existing = db.query(User).get(user_data.id)

                if existing:
                    existing.name = user_data.name
                    existing.email = user_data.email
                    action = "updated"
                else:
                    user = User(
                        id=user_data.id,
                        name=user_data.name,
                        email=user_data.email
                    )
                    db.add(user)
                    action = "created"

                db.commit()
                yield user_service_pb2.UserSyncResponse(
                    success=True,
                    message=f"User {action}",
                    user=user_data
                )

            elif request.HasField('delete_id'):
                user = db.query(User).get(request.delete_id)
                if user:
                    db.delete(user)
                    db.commit()
                    yield user_service_pb2.UserSyncResponse(
                        success=True,
                        message="User deleted"
                    )
                else:
                    yield user_service_pb2.UserSyncResponse(
                        success=False,
                        message="User not found"
                    )

    def _user_to_proto(self, user):
        return user_service_pb2.User(
            id=user.id,
            email=user.email,
            name=user.name,
            created_at=timestamp_pb2.Timestamp(seconds=int(user.created_at.timestamp()))
        )


# Server setup
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_service_pb2_grpc.add_UserServiceServicer_to_server(
        UserServicer(), server
    )

    # Enable reflection for debugging
    from grpc_reflection.v1alpha import reflection
    SERVICE_NAMES = (
        user_service_pb2.DESCRIPTOR.services_by_name['UserService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()
```

---

### 7. API Security Patterns

**Authentication Patterns:**
```python
# ✅ GOOD: JWT with refresh tokens
import jwt
from datetime import datetime, timedelta
from functools import wraps

SECRET_KEY = os.getenv('JWT_SECRET')
REFRESH_SECRET = os.getenv('JWT_REFRESH_SECRET')


def create_tokens(user_id: int) -> dict:
    """Create access and refresh token pair."""
    access_payload = {
        'user_id': user_id,
        'type': 'access',
        'exp': datetime.utcnow() + timedelta(minutes=15),
        'iat': datetime.utcnow()
    }

    refresh_payload = {
        'user_id': user_id,
        'type': 'refresh',
        'exp': datetime.utcnow() + timedelta(days=30),
        'iat': datetime.utcnow()
    }

    return {
        'access_token': jwt.encode(access_payload, SECRET_KEY, algorithm='HS256'),
        'refresh_token': jwt.encode(refresh_payload, REFRESH_SECRET, algorithm='HS256'),
        'token_type': 'Bearer',
        'expires_in': 900  # 15 minutes in seconds
    }


def require_auth(f):
    """Authentication decorator."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return api_error("Missing authorization header", 401, "UNAUTHORIZED")

        try:
            scheme, token = auth_header.split()
            if scheme.lower() != 'bearer':
                return api_error("Invalid auth scheme", 401, "INVALID_SCHEME")

            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

            if payload.get('type') != 'access':
                return api_error("Invalid token type", 401, "INVALID_TOKEN_TYPE")

            g.current_user_id = payload['user_id']
            g.current_user = User.query.get(payload['user_id'])

        except jwt.ExpiredSignatureError:
            return api_error("Token expired", 401, "TOKEN_EXPIRED")
        except jwt.InvalidTokenError:
            return api_error("Invalid token", 401, "INVALID_TOKEN")

        return f(*args, **kwargs)
    return decorated


# ✅ GOOD: Token refresh endpoint
@app.route('/api/v1/auth/refresh', methods=['POST'])
def refresh_token():
    data = request.get_json()
    refresh_token = data.get('refresh_token')

    if not refresh_token:
        return api_error("Refresh token required", 400, "MISSING_REFRESH_TOKEN")

    try:
        payload = jwt.decode(refresh_token, REFRESH_SECRET, algorithms=['HS256'])

        if payload.get('type') != 'refresh':
            return api_error("Invalid token type", 401, "INVALID_TOKEN_TYPE")

        # Optionally: check if refresh token is revoked
        if is_token_revoked(refresh_token):
            return api_error("Token revoked", 401, "TOKEN_REVOKED")

        # Generate new token pair
        tokens = create_tokens(payload['user_id'])
        return api_response(data=tokens)

    except jwt.ExpiredSignatureError:
        return api_error("Refresh token expired", 401, "REFRESH_TOKEN_EXPIRED")
    except jwt.InvalidTokenError:
        return api_error("Invalid refresh token", 401, "INVALID_REFRESH_TOKEN")
```

**API Key Authentication:**
```python
# ✅ GOOD: API key authentication for service-to-service
import hashlib
import secrets

def generate_api_key() -> tuple[str, str]:
    """Generate API key and hash."""
    key = secrets.token_urlsafe(32)
    key_hash = hashlib.sha256(key.encode()).hexdigest()
    return key, key_hash


def require_api_key(f):
    """API key authentication decorator."""
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')

        if not api_key:
            return api_error("API key required", 401, "MISSING_API_KEY")

        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        api_client = APIClient.query.filter_by(key_hash=key_hash, active=True).first()

        if not api_client:
            return api_error("Invalid API key", 401, "INVALID_API_KEY")

        # Check rate limits for this client
        if api_client.is_rate_limited():
            return api_error("Rate limit exceeded", 429, "RATE_LIMIT_EXCEEDED")

        g.api_client = api_client
        return f(*args, **kwargs)
    return decorated
```

**Input Validation:**
```python
from marshmallow import Schema, fields, validate, ValidationError

# ✅ GOOD: Schema-based validation
class CreateUserSchema(Schema):
    email = fields.Email(required=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    password = fields.Str(
        required=True,
        validate=validate.Length(min=8, max=128),
        load_only=True  # Never serialize back
    )
    age = fields.Int(validate=validate.Range(min=0, max=150))


def validate_request(schema_class):
    """Request validation decorator."""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            schema = schema_class()
            try:
                validated_data = schema.load(request.get_json())
                g.validated_data = validated_data
            except ValidationError as err:
                return api_error(
                    "Validation failed",
                    422,
                    "VALIDATION_ERROR",
                    details=[
                        {"field": field, "message": msgs[0]}
                        for field, msgs in err.messages.items()
                    ]
                )
            return f(*args, **kwargs)
        return decorated
    return decorator


@app.route('/api/v1/users', methods=['POST'])
@require_auth
@validate_request(CreateUserSchema)
def create_user():
    data = g.validated_data
    # data is now validated and safe to use
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return api_response(data=user.to_dict(), code=201)
```

---

### 8. OpenAPI/Swagger Documentation

**Flask-RESTX Auto-Documentation:**
```python
from flask import Flask
from flask_restx import Api, Resource, fields, Namespace

app = Flask(__name__)
api = Api(
    app,
    version='1.0',
    title='User Service API',
    description='API for user management',
    doc='/docs'  # Swagger UI at /docs
)

# Namespaces for organization
users_ns = Namespace('users', description='User operations')
auth_ns = Namespace('auth', description='Authentication operations')

api.add_namespace(users_ns, path='/api/v1/users')
api.add_namespace(auth_ns, path='/api/v1/auth')

# Models for documentation
user_model = api.model('User', {
    'id': fields.Integer(readonly=True, description='User ID'),
    'email': fields.String(required=True, description='Email address'),
    'name': fields.String(required=True, description='Full name'),
    'created_at': fields.DateTime(readonly=True, description='Creation timestamp')
})

user_input_model = api.model('UserInput', {
    'email': fields.String(required=True, description='Email address'),
    'name': fields.String(required=True, description='Full name'),
    'password': fields.String(required=True, description='Password (min 8 chars)')
})

error_model = api.model('Error', {
    'status': fields.String(description='Status'),
    'error': fields.Nested(api.model('ErrorDetail', {
        'code': fields.String(description='Error code'),
        'message': fields.String(description='Error message'),
        'details': fields.List(fields.Raw, description='Validation details')
    }))
})

pagination_model = api.model('Pagination', {
    'total': fields.Integer(description='Total items'),
    'page': fields.Integer(description='Current page'),
    'per_page': fields.Integer(description='Items per page'),
    'total_pages': fields.Integer(description='Total pages')
})


@users_ns.route('/')
class UserList(Resource):
    @users_ns.doc('list_users')
    @users_ns.param('page', 'Page number', type=int, default=1)
    @users_ns.param('per_page', 'Items per page', type=int, default=20)
    @users_ns.marshal_list_with(user_model, envelope='data')
    @users_ns.response(401, 'Unauthorized', error_model)
    def get(self):
        """List all users"""
        # Implementation
        pass

    @users_ns.doc('create_user')
    @users_ns.expect(user_input_model, validate=True)
    @users_ns.marshal_with(user_model, code=201, envelope='data')
    @users_ns.response(422, 'Validation Error', error_model)
    def post(self):
        """Create a new user"""
        # Implementation
        pass


@users_ns.route('/<int:user_id>')
@users_ns.param('user_id', 'User ID')
class UserResource(Resource):
    @users_ns.doc('get_user')
    @users_ns.marshal_with(user_model, envelope='data')
    @users_ns.response(404, 'User not found', error_model)
    def get(self, user_id):
        """Get user by ID"""
        pass

    @users_ns.doc('update_user')
    @users_ns.expect(user_input_model)
    @users_ns.marshal_with(user_model, envelope='data')
    def patch(self, user_id):
        """Update user"""
        pass

    @users_ns.doc('delete_user')
    @users_ns.response(204, 'User deleted')
    def delete(self, user_id):
        """Delete user"""
        pass
```

**OpenAPI Spec Generation:**
```yaml
# openapi.yaml (manually maintained or generated)
openapi: 3.0.3
info:
  title: User Service API
  description: API for user management
  version: 1.0.0
  contact:
    name: API Support
    email: api@example.com
  license:
    name: MIT

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://staging-api.example.com/v1
    description: Staging
  - url: http://localhost:5000/api/v1
    description: Local development

paths:
  /users:
    get:
      summary: List users
      operationId: listUsers
      tags:
        - Users
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: per_page
          in: query
          schema:
            type: integer
            default: 20
            maximum: 100
      responses:
        '200':
          description: List of users
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    example: success
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
                  pagination:
                    $ref: '#/components/schemas/Pagination'
        '401':
          $ref: '#/components/responses/Unauthorized'

    post:
      summary: Create user
      operationId: createUser
      tags:
        - Users
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserInput'
      responses:
        '201':
          description: User created
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                  data:
                    $ref: '#/components/schemas/User'
        '422':
          $ref: '#/components/responses/ValidationError'

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
          readOnly: true
        email:
          type: string
          format: email
        name:
          type: string
        created_at:
          type: string
          format: date-time
          readOnly: true

    UserInput:
      type: object
      required:
        - email
        - name
        - password
      properties:
        email:
          type: string
          format: email
        name:
          type: string
          minLength: 1
          maxLength: 100
        password:
          type: string
          minLength: 8
          maxLength: 128
          writeOnly: true

    Pagination:
      type: object
      properties:
        total:
          type: integer
        page:
          type: integer
        per_page:
          type: integer
        total_pages:
          type: integer

    Error:
      type: object
      properties:
        status:
          type: string
          example: error
        error:
          type: object
          properties:
            code:
              type: string
            message:
              type: string
            details:
              type: array
              items:
                type: object
                properties:
                  field:
                    type: string
                  message:
                    type: string

  responses:
    Unauthorized:
      description: Authentication required
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

    ValidationError:
      description: Validation failed
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - bearerAuth: []
```

---

### 9. Backward Compatibility Strategies

**Additive Changes (Safe):**
```python
# ✅ SAFE: Adding new optional fields
# V1 Response
{
    "id": 1,
    "name": "John"
}

# V1.1 Response (backward compatible)
{
    "id": 1,
    "name": "John",
    "email": "john@example.com"  # New optional field
}


# ✅ SAFE: Adding new endpoints
# V1 had: GET /api/v1/users
# V1.1 adds: GET /api/v1/users/{id}/orders (new endpoint)


# ✅ SAFE: Adding new optional query parameters
# V1: GET /api/v1/users?page=1
# V1.1: GET /api/v1/users?page=1&include_inactive=true (new param)
```

**Breaking Changes (Require Version Bump):**
```python
# ❌ BREAKING: Removing fields
# V1: {"id": 1, "name": "John", "legacy_field": "value"}
# V2: {"id": 1, "name": "John"}  # legacy_field removed

# ❌ BREAKING: Changing field types
# V1: {"count": "100"}  # String
# V2: {"count": 100}    # Integer

# ❌ BREAKING: Renaming fields
# V1: {"user_name": "john"}
# V2: {"username": "john"}

# ❌ BREAKING: Changing required fields
# V1: email optional
# V2: email required
```

**Deprecation Pattern:**
```python
# ✅ GOOD: Gradual deprecation with warnings
@app.route('/api/v1/users')
def get_users_v1():
    response = jsonify(get_users_data())

    # Add deprecation headers
    response.headers['Deprecation'] = 'true'
    response.headers['Sunset'] = 'Sat, 01 Jun 2025 00:00:00 GMT'
    response.headers['Link'] = '</api/v2/users>; rel="successor-version"'

    # Log deprecation usage
    logger.warning(
        "Deprecated API v1 called",
        extra={
            "endpoint": "/api/v1/users",
            "client_id": g.get("api_client_id"),
            "sunset_date": "2025-06-01"
        }
    )

    return response


# ✅ GOOD: Field-level deprecation
class UserSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    email = fields.Email()

    # Deprecated field - still returned but marked
    user_name = fields.String(
        dump_only=True,
        metadata={'deprecated': True, 'replacement': 'name'}
    )

    @post_dump
    def add_deprecation_warnings(self, data, **kwargs):
        # Copy deprecated field value from new field
        data['user_name'] = data.get('name')
        return data
```

**API Evolution Guidelines:**
```python
# ✅ GOOD: Version negotiation middleware
@app.before_request
def check_api_version():
    # Get requested version
    version = request.headers.get('API-Version', '1')

    # Check minimum supported version
    if version < MIN_SUPPORTED_VERSION:
        return api_error(
            f"API version {version} is no longer supported. "
            f"Minimum version: {MIN_SUPPORTED_VERSION}",
            410,
            "VERSION_GONE"
        )

    # Check if version is deprecated
    if version in DEPRECATED_VERSIONS:
        g.api_deprecated = True
        g.api_sunset = DEPRECATED_VERSIONS[version]

    g.api_version = version


@app.after_request
def add_version_headers(response):
    if getattr(g, 'api_deprecated', False):
        response.headers['Deprecation'] = 'true'
        response.headers['Sunset'] = g.api_sunset

    response.headers['API-Version'] = g.get('api_version', '1')
    return response
```

---

## Detection Patterns

```python
def detect_api_design_issues(code: str) -> List[dict]:
    """Detect common API design anti-patterns."""
    issues = []

    # Pattern 1: Verbs in URL paths
    verb_urls = re.finditer(
        r'@app\.route\([\'"].*?(get|create|update|delete|fetch|retrieve).*?[\'"]',
        code,
        re.IGNORECASE
    )
    for match in verb_urls:
        issues.append({
            'type': 'api_design',
            'subtype': 'verb_in_url',
            'severity': 'LOW',
            'line': code[:match.start()].count('\n') + 1,
            'message': 'URL contains verb - use HTTP methods instead'
        })

    # Pattern 2: Inconsistent response format
    jsonify_calls = re.findall(r'return jsonify\((.*?)\)', code, re.DOTALL)
    formats = set()
    for call in jsonify_calls:
        if 'status' in call:
            formats.add('envelope')
        elif call.startswith('[') or call.startswith('{'):
            formats.add('raw')
    if len(formats) > 1:
        issues.append({
            'type': 'api_design',
            'subtype': 'inconsistent_response',
            'severity': 'MEDIUM',
            'message': 'Inconsistent response format (mix of envelope and raw)'
        })

    # Pattern 3: Missing pagination
    list_endpoints = re.finditer(
        r'@app\.route\([\'"].*?s[\'"].*?GET.*?def.*?\):(.*?)(?=@app\.route|$)',
        code,
        re.DOTALL
    )
    for match in list_endpoints:
        body = match.group(1)
        if '.all()' in body and 'page' not in body.lower():
            issues.append({
                'type': 'api_design',
                'subtype': 'missing_pagination',
                'severity': 'HIGH',
                'line': code[:match.start()].count('\n') + 1,
                'message': 'List endpoint without pagination'
            })

    # Pattern 4: No rate limiting
    if '@rate_limit' not in code and 'RateLimiter' not in code:
        if '@app.route' in code:
            issues.append({
                'type': 'api_design',
                'subtype': 'no_rate_limiting',
                'severity': 'HIGH',
                'message': 'No rate limiting configured'
            })

    # Pattern 5: Missing input validation
    post_routes = re.finditer(
        r'@app\.route.*?POST.*?def.*?\):(.*?)(?=@app\.route|def |$)',
        code,
        re.DOTALL
    )
    for match in post_routes:
        body = match.group(1)
        has_validation = any(kw in body for kw in [
            'validate', 'schema', 'ValidationError', 'marshmallow'
        ])
        if not has_validation and 'request.get_json()' in body:
            issues.append({
                'type': 'api_design',
                'subtype': 'missing_validation',
                'severity': 'HIGH',
                'line': code[:match.start()].count('\n') + 1,
                'message': 'POST endpoint without input validation'
            })

    # Pattern 6: GraphQL N+1 risk
    if 'graphene' in code or 'graphql' in code:
        if 'DataLoader' not in code and '.query.' in code:
            issues.append({
                'type': 'api_design',
                'subtype': 'graphql_n_plus_1',
                'severity': 'HIGH',
                'message': 'GraphQL resolvers without DataLoader (N+1 risk)'
            })

    return issues
```

---

## Checklist

### REST API Design
- [ ] Resources use plural nouns (e.g., /users not /user)
- [ ] HTTP methods used correctly (GET/POST/PUT/PATCH/DELETE)
- [ ] Appropriate HTTP status codes returned
- [ ] Consistent response envelope format
- [ ] Error responses include code, message, and details
- [ ] Request ID in all responses for debugging

### Versioning
- [ ] API versioning strategy defined
- [ ] Version in URL path (recommended) or header
- [ ] Deprecation headers for old versions
- [ ] Sunset dates communicated to clients
- [ ] Breaking changes only in major versions

### Pagination
- [ ] All list endpoints paginated
- [ ] Maximum page size enforced
- [ ] Cursor/keyset pagination for large datasets
- [ ] Total count available when needed
- [ ] HATEOAS links for navigation

### Rate Limiting
- [ ] Rate limits on all endpoints
- [ ] Stricter limits for auth endpoints
- [ ] Rate limit headers in responses
- [ ] Tiered limits for different user types
- [ ] 429 responses with Retry-After header

### Authentication & Security
- [ ] JWT with short expiration (15min)
- [ ] Refresh token mechanism
- [ ] API key auth for service-to-service
- [ ] Input validation on all endpoints
- [ ] HTTPS enforced
- [ ] CORS configured properly

### GraphQL
- [ ] DataLoader for batching queries
- [ ] Query depth limiting
- [ ] Query complexity limiting
- [ ] Proper error handling in resolvers
- [ ] Relay-style pagination

### gRPC
- [ ] Clear service and message definitions
- [ ] Proper use of streaming types
- [ ] Error codes used correctly
- [ ] Reflection enabled for debugging

### Documentation
- [ ] OpenAPI/Swagger spec maintained
- [ ] Examples for all endpoints
- [ ] Error codes documented
- [ ] Authentication documented
- [ ] Changelog maintained

### Backward Compatibility
- [ ] Additive changes only when possible
- [ ] Deprecated fields maintained
- [ ] Migration guide for breaking changes
- [ ] Feature flags for gradual rollout

---

## References

- [REST API Design Best Practices](https://restfulapi.net/)
- [Microsoft REST API Guidelines](https://github.com/microsoft/api-guidelines)
- [Google API Design Guide](https://cloud.google.com/apis/design)
- [GraphQL Best Practices](https://graphql.org/learn/best-practices/)
- [gRPC Documentation](https://grpc.io/docs/)
- [OpenAPI Specification](https://swagger.io/specification/)
- [JSON:API Specification](https://jsonapi.org/)
- [HATEOAS](https://restfulapi.net/hateoas/)
