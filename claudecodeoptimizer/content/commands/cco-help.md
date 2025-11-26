---
name: cco-help
description: Quick command reference
---

# /cco-help

**CCO command reference**

---

## Commands

| Command | Purpose | Common Usage |
|---------|---------|--------------|
| /cco-audit | Find issues | `--smart`, `--security`, `--all` |
| /cco-fix | Fix issues | `--security`, `--tech-debt` |
| /cco-generate | Create files | `--tests`, `--openapi`, `--cicd` |
| /cco-commit | Smart commits | (interactive) |
| /cco-optimize | Optimize | `--context`, `--code-quality` |
| /cco-status | Health check | (no args) |
| /cco-help | This guide | (no args) |

---

## Quick Start

```bash
/cco-audit --smart    # Auto-detect, top checks
/cco-fix --security   # Fix security issues
/cco-generate --tests # Create missing tests
/cco-commit           # Semantic commits
```

---

## Workflows

**Security hardening:**
```bash
/cco-audit --security → /cco-fix --security → /cco-commit
```

**Quality improvement:**
```bash
/cco-audit --tech-debt → /cco-fix --tech-debt → /cco-generate --tests
```

**Full health check:**
```bash
/cco-audit --all → /cco-fix --all → /cco-generate --all → /cco-commit
```

---

## Tips

- Add context: `/cco-audit --security "auth endpoints"`
- Combine flags: `/cco-audit --security --tests`
- Meta-flags: `--ai`, `--critical`, `--production-ready`
