---
name: cco-help
description: Command reference
---

# /cco-help

## Commands

| Command | Purpose |
|---------|---------|
| `/cco-calibrate` | **Project calibration** - calibrate AI recommendations to project context |
| `/cco-audit` | **Quality gates** - standardized checks, prioritized fixes |
| `/cco-review` | **Strategic review** - architecture analysis, fresh perspective, apply improvements |
| `/cco-generate` | **Generation** - convention-following, verified |
| `/cco-health` | **Visibility** - actionable metrics dashboard |
| `/cco-refactor` | **Risk mitigation** - verified transformations |
| `/cco-optimize` | **Efficiency** - measurable improvements |
| `/cco-commit` | **Change management** - quality gates, atomic commits |
| `/cco-config` | **Settings** - statusline, permissions (global/local) |
| `/cco-status` | Installation check |

## Quick Start

```bash
/cco-calibrate           # Set project context for calibrated AI recommendations
/cco-audit --smart       # Quality gates → offer fixes
/cco-review              # Strategic review → apply improvements
/cco-health              # Metrics dashboard
/cco-refactor rename x y # Verified rename
/cco-commit              # Quality gates → atomic commits
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

## Review Flags

```bash
/cco-review                    # Full review → approve → apply
/cco-review --quick            # Gap analysis only
/cco-review --focus=structure  # Focus on organization
/cco-review --report-only      # Just show findings
```

## Self-Compliance SSOT

When docs↔code mismatch found:
- **SSOT=docs** - Align code to documentation
- **SSOT=code** - Align docs to code
- **SSOT=discuss** - Choose direction
