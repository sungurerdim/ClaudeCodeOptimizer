---
name: devex-onboarding
description: Optimize developer onboarding (< 1hr to first commit), local/prod parity, reproducible builds, fast feedback loops. Includes Docker Compose setup, one-command setup scripts, pre-commit hooks, hot reload, and seed data generation.
keywords: [developer experience, DevEx, onboarding, local development, dev environment, tooling, parity, docker-compose, hot reload, pre-commit, reproducible builds]
category: infrastructure
related_commands:
  action_types: [generate, audit, optimize]
  categories: [infrastructure, quality]
pain_points: [11, 12]
---

# Skill: Developer Experience

**Domain**: Developer Productivity
**Purpose**: Optimize onboarding (< 1hr to first commit), local/prod parity, reproducible builds, fast feedback loops.

---

## Standard Structure

**This skill follows [STANDARDS_SKILLS.md](../STANDARDS_SKILLS.md):**

- **Standard sections** - Domain, Purpose, Core Techniques, Anti-Patterns, Checklist
- **Code example format** - Bad/Good pattern with specific examples
- **Detection pattern format** - Python functions with Finding objects
- **Checklist format** - Specific, verifiable items

**See STANDARDS_SKILLS.md for format details. Only skill-specific content is documented below.**

---

## Core Techniques

- **One-Command Setup**: Single script installs deps, starts services, seeds data, runs tests
- **Local/Prod Parity**: Docker Compose with pinned versions matching production
- **Reproducible Builds**: Lock files, version pinning, multi-stage Docker
- **Fast Feedback**: Hot reload, pre-commit hooks, < 10s unit tests, < 10min CI
- **Debugging**: IDE integration, structured logs, helpful errors

## Patterns

### ✅ Good: One-Command Setup
```bash
#!/bin/bash
# setup.sh
set -e
npm install
docker-compose up -d
until docker-compose exec -T postgres pg_isready; do sleep 1; done
npm run migrate && npm run seed && npm test
echo "✅ Setup complete! Run: npm run dev"
```
**Why**: New dev from clone to first commit in < 1hr

### ✅ Good: Local/Prod Parity
```yaml
# docker-compose.yml
services:
  postgres:
    image: postgres:15.4  # Match prod version
  redis:
    image: redis:7.2      # Match prod version
  app:
    volumes:
      - .:/app  # Hot reload
```
**Why**: Eliminates "works on my machine" bugs

### ✅ Good: Reproducible Build
```dockerfile
FROM node:20.10.0-alpine AS deps  # Pinned
COPY package.json package-lock.json ./
RUN npm ci --only=production       # Lock file
```
**Why**: Same code + deps → identical binary

### ✅ Good: Fast Feedback
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    hooks:
      - id: black
```
**Why**: Catch issues before CI (< 5s feedback)

### ✅ Good: Seed Data
```python
# scripts/seed.py
from faker import Faker
fake = Faker()
for i in range(10):
    User(email=fake.email(), name=fake.name()).save()
```
**Why**: Realistic data for testing immediately

### ❌ Bad: Manual Setup
```bash
# Install PostgreSQL, configure it, install Redis, create DB...
```
**Why**: Takes hours, error-prone, inconsistent

### ❌ Bad: Version Mismatch
```yaml
# Local: postgres:14, Prod: postgres:15
```
**Why**: Causes bugs from environment differences

### ❌ Bad: No Lock Files
```json
{"dependencies": {"express": "^4.0.0"}}  // Floating version
```
**Why**: Non-reproducible builds

### ❌ Bad: Slow Tests
```bash
npm test  # Takes 5 minutes
```
**Why**: Kills productivity, discourages testing

## Checklist

- [ ] One-command setup script (< 5min)
- [ ] Docker Compose with pinned versions
- [ ] Lock files committed
- [ ] Seed script with realistic data
- [ ] Pre-commit hooks configured
- [ ] Hot reload enabled (< 1s)
- [ ] Unit tests < 10s
- [ ] CI pipeline < 10min
- [ ] README with quick start
- [ ] IDE config committed (.vscode/)

## Command Discovery Protocol

When this skill is active, find relevant commands by searching `~/.claude/commands/` metadata:

```yaml
# Search criteria for this skill's domain
action_types: [generate, audit, optimize]
keywords: [onboarding, devex, docker, setup, reproducible]
category: infrastructure
pain_points: [11, 12]
```

**How Claude finds commands:**
1. Grep command files for `keywords:.*[pattern]` in frontmatter
2. Match `category: infrastructure`
3. Present matching commands with their parameters

This ensures commands are always current even when renamed or updated.
