# CCO Workflow Guide

How to integrate CCO commands into your development workflow.

---

## Daily Development

```
Start session
     │
     ▼
┌────────────────┐
│  /cco-status   │  Quick health check (10 sec)
└───────┬────────┘
        │
   [Write code]
        │
        ▼
┌────────────────┐
│  /cco-commit   │  Quality-gated commit
└───────┬────────┘
        │
   [More changes?] ──yes──► [Write code]
        │
       no
        │
        ▼
      Done
```

### When to Use Each Command

| Situation | Command | Why |
|-----------|---------|-----|
| Starting work | `/cco-status` | See current health, know what needs attention |
| Ready to commit | `/cco-commit` | Quality gates catch issues before they're committed |
| Cleaning up | `/cco-checkup` | Batch maintenance (status + optimize) |

---

## Pre-PR Workflow

```
Feature complete
        │
        ▼
┌────────────────┐
│  /cco-review   │  Architecture check
└───────┬────────┘
        │
   [Issues found?] ──yes──► Fix issues
        │
       no
        │
        ▼
┌────────────────┐
│ /cco-optimize  │  Full quality pass
└───────┬────────┘
        │
        ▼
┌────────────────┐
│  /cco-commit   │  Final commit
└───────┬────────┘
        │
        ▼
   Create PR
```

### Command Selection

| Goal | Command | Flags |
|------|---------|-------|
| Quick review | `/cco-review --quick` | Report only, smart defaults |
| Full review | `/cco-review` | Interactive, with apply option |
| Security focus | `/cco-optimize --security` | Security scope only |
| Everything | `/cco-optimize` | All scopes |

---

## Pre-Release Workflow

```
Release candidate
        │
        ▼
┌────────────────┐
│ /cco-preflight │  Orchestrates: optimize + review + verify
└───────┬────────┘
        │
   [Blockers?] ──yes──► Fix blockers
        │
       no
        │
        ▼
   [Warnings?] ──yes──► Decide: fix or override
        │
       no
        │
        ▼
┌────────────────┐
│    Release     │  Tag + push
└────────────────┘
```

### Preflight Checks

| Check | Type | Action if Failed |
|-------|------|------------------|
| Clean working directory | BLOCKER | Cannot release |
| Version synced | BLOCKER | Cannot release |
| On main/release branch | WARN | Can override |
| No TODO/FIXME markers | WARN | Can override |
| Tests pass | BLOCKER | Cannot release |

---

## Maintenance Routine

### Weekly (Active Development)

```
/cco-checkup
```

Runs:
1. `/cco-status` — Health dashboard
2. `/cco-optimize --quick` — Safe auto-fixes

### Monthly (Stable Projects)

```
/cco-review --focus=dependencies
/cco-optimize --security
```

Checks:
- Outdated dependencies
- Security advisories
- Accumulated tech debt

---

## Command Relationships

```
┌─────────────────────────────────────────────────────┐
│                    /cco-preflight                   │
│  (Orchestrates optimize + review for releases)      │
└───────────────────────┬─────────────────────────────┘
                        │
          ┌─────────────┴─────────────┐
          │                           │
          ▼                           ▼
┌─────────────────┐         ┌─────────────────┐
│  /cco-optimize  │         │   /cco-review   │
│ (Fix issues)    │         │ (Analyze arch)  │
└─────────────────┘         └─────────────────┘
          │                           │
          └─────────────┬─────────────┘
                        │
                        ▼
              ┌─────────────────┐
              │  /cco-checkup   │
              │ (status + opt)  │
              └─────────────────┘
```

---

## Research Workflow

When you need to make a decision:

```
"Which library should I use?"
         │
         ▼
┌────────────────┐
│ /cco-research  │  Multi-source research
└───────┬────────┘
         │
         ▼
   [T1-T6 scored sources]
   [Contradictions resolved]
   [Recommendation]
```

### Research Modes

| Mode | Use When |
|------|----------|
| `/cco-research "query"` | Standard research |
| `/cco-research "A vs B" --compare` | Comparing options |
| `/cco-research "query" --security` | Security/CVE focus |
| `/cco-research "query" --local` | Codebase-only search |

---

## Quick Reference

| I want to... | Use |
|--------------|-----|
| See project health | `/cco-status` |
| Fix issues | `/cco-optimize` |
| Review architecture | `/cco-review` |
| Commit with quality gates | `/cco-commit` |
| Prepare for release | `/cco-preflight` |
| Regular maintenance | `/cco-checkup` |
| Research a topic | `/cco-research` |
| Configure project | `/cco-config` |

---

*Back to [README](../README.md)*
