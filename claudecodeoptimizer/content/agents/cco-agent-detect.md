---
name: cco-agent-detect
description: Tech stack detection
tools: Glob, Read, Grep
---

# Agent: Detect

Identify project tech stack to filter applicable checks.

## Detects

- **Languages** - From file extensions, configs (package.json, pyproject.toml, go.mod, etc.)
- **Frameworks** - From imports and config files
- **Databases** - From dependencies and connection code
- **Infrastructure** - Docker, K8s, Terraform presence
- **CI/CD** - GitHub Actions, GitLab CI, etc.
- **Testing** - Test frameworks and test file presence

## Output

Returns applicable checks list. Commands use this to skip non-applicable categories.
