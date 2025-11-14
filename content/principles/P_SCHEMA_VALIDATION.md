---
id: P_SCHEMA_VALIDATION
title: Schema-First Validation
category: security_privacy
severity: critical
weight: 10
applicability:
  project_types: ['api', 'web', 'ml']
  languages: ['python', 'javascript', 'typescript']
---

# P_SCHEMA_VALIDATION: Schema-First Validation 🔴

**Severity**: Critical

Use schema-based validation (Pydantic/Joi) for all external inputs.

**Why**: Reduces ambiguity and edge cases by using exact types instead of loose ones

**Enforcement**: Skills required - verification_protocol, test_first, root_cause_analysis

**Project Types**: api, web, ml
**Languages**: python, javascript, typescript

**Rules**:
- **Validate At Entry**: Validate data at API entry points

**❌ Bad**:
```
@app.post('/api')
def create(data: dict):  # No validation!
```

**✅ Good**:
```
@app.post('/api')
def create(data: ResourceSchema):  # Validated
```
