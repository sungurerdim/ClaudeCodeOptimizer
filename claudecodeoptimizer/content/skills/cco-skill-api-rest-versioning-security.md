---
title: RESTful API Design & Security
category: api
description: REST conventions, versioning, authentication, rate limiting, CORS, schema validation
metadata:
  name: "RESTful API Design & Security"
  activation_keywords: ["API", "REST", "endpoint", "versioning", "API security", "rate limiting", "authentication", "authorization", "CORS", "schema validation", "API gateway", "OpenAPI"]
  category: "api"
principles: ['P_RESTFUL_API_CONVENTIONS', 'P_API_VERSIONING_STRATEGY', 'P_API_SECURITY', 'P_CORS_POLICY', 'P_SCHEMA_VALIDATION']
use_cases:
  development_philosophy: [quality_first, balanced]
  project_maturity: [active-dev, production]
---

# RESTful API Design & Security

## Domain
REST API design, versioning, auth, rate limiting, CORS, validation

## Purpose
Secure, versioned REST APIs with proper conventions

## Core Techniques

### REST
- Resources: plural nouns (`/users`)
- Verbs: GET/POST/PUT/PATCH/DELETE
- Status: 200/201/400/401/404/500
- Pagination: `?page=1&limit=20`

### Versioning
- URL: `/api/v1/users`
- Support N + N-1
- Sunset headers

### Security
- Auth: JWT/OAuth2/API keys
- Rate: 1000/hr user, 100/min IP
- Schema validation
- HTTPS, TLS 1.2+

### CORS
- Whitelist origins
- Methods: GET/POST/PUT/PATCH/DELETE
- Headers: Content-Type, Authorization

## Patterns

### CRUD + Validation
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator

class UserCreate(BaseModel):
    email: str
    password: str
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 12: raise ValueError('Min 12')
        return v

@app.post("/api/v1/users", status_code=201)
async def create(user: UserCreate):
    if db.user_exists(user.email): raise HTTPException(400)
    return db.create_user(user.email, user.password)

@app.get("/api/v1/users/{id}")
async def get(id: int):
    if not (u := db.get_user(id)): raise HTTPException(404)
    return u
```

### JWT Auth
```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
import jwt

security = HTTPBearer()

def get_user(cred = Depends(security)):
    try:
        p = jwt.decode(cred.credentials, SECRET, algorithms=["HS256"])
        if not (u := db.get_user(p.get("user_id"))):
            raise HTTPException(401)
        return u
    except jwt.ExpiredSignatureError:
        raise HTTPException(401)
```

### Rate Limiting
```python
from slowapi import Limiter
limiter = Limiter(key_func=lambda r: r.client.host)

@app.get("/api/v1/users")
@limiter.limit("100/minute")
async def list_users(r: Request):
    return db.list_users()
```

### CORS
```python
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(CORSMiddleware,
    allow_origins=["https://app.example.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Content-Type", "Authorization"])
```

### Versioning
```python
@app.get("/api/v1/users/{id}")
async def v1(id: int, r: Response):
    r.headers["Sunset"] = "2024-12-31"
    return {"id": u.id, "email_address": u.email}

@app.get("/api/v2/users/{id}")
async def v2(id: int):
    return {"id": u.id, "email": u.email}
```

### Schema
```python
from pydantic import BaseModel, Field, validator

class Order(BaseModel):
    items: List[int] = Field(..., min_items=1, max_items=100)
    addr: str = Field(..., min_length=10, max_length=500)
    @validator('items')
    def validate(cls, v):
        if not all(i > 0 for i in v): raise ValueError()
        return v
```

## Checklist
- [ ] REST: plural nouns, verbs, status
- [ ] Versioning: URL, N + N-1
- [ ] Auth: JWT/OAuth2
- [ ] Rate: user + IP
- [ ] CORS: whitelist
- [ ] Schema: validation
- [ ] HTTPS, TLS 1.2+
- [ ] Pagination
- [ ] Errors
- [ ] Deprecation
