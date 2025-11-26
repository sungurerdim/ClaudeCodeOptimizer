---
name: cco-help
description: Command reference
---

# /cco-help

## Commands

| Command | Purpose |
|---------|---------|
| `/cco-audit` | **Quality gates** - standardized checks, prioritized fixes |
| `/cco-generate` | **Generation** - convention-following, verified |
| `/cco-health` | **Visibility** - actionable metrics dashboard |
| `/cco-refactor` | **Risk mitigation** - verified transformations |
| `/cco-optimize` | **Efficiency** - measurable improvements |
| `/cco-commit` | **Change management** - atomic, traceable commits |
| `/cco-config` | **Settings** - statusline, permissions (global/local) |
| `/cco-status` | Installation check |

## Quick Start

```bash
/cco-audit --smart       # Quality gates → offer fixes
/cco-health              # Metrics dashboard
/cco-refactor rename x y # Verified rename
/cco-commit              # Atomic commits
/cco-config              # Configure statusline & permissions
```

## Config Scope

```bash
/cco-config --global           # Apply to all projects (~/.claude/)
/cco-config --local            # This project only (./.claude/)
```

## Permission Levels

```bash
/cco-config --permissions safe       # Read-only, maximum security
/cco-config --permissions balanced   # Normal workflow (recommended)
/cco-config --permissions permissive # Minimal prompts
```

## Audit Flags

```bash
/cco-audit --security        # Security checks
/cco-audit --tech-debt       # Dead code, complexity
/cco-audit --self-compliance # Check against project's own rules
/cco-audit --critical        # security + ai-security + database + tests
/cco-audit --auto-fix        # Auto-fix safe issues
```

## Self-Compliance SSOT

When docs↔code mismatch found:
- **SSOT=docs** - Align code to documentation
- **SSOT=code** - Align docs to code
- **SSOT=discuss** - Choose direction
