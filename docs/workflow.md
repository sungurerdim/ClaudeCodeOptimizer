# Workflow Guide

How to integrate CCO into your development workflow.

---

## Quick Reference

| I want to... | Command |
|--------------|---------|
| See project health | `/cco-status` |
| Fix issues | `/cco-optimize` |
| Review architecture | `/cco-review` |
| Commit with quality gates | `/cco-commit` |
| Prepare for release | `/cco-preflight` |
| Regular maintenance | `/cco-checkup` |
| Research a topic | `/cco-research` |
| Configure project | `/cco-config` |

---

## Daily Development

```
Start session
     │
     ▼
┌────────────────┐
│  /cco-status   │  Quick health check
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

| Situation | Command |
|-----------|---------|
| Starting work | `/cco-status` |
| Ready to commit | `/cco-commit` |
| Cleaning up | `/cco-checkup` |

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
   [Issues?] ──yes──► Fix issues
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

| Goal | Command |
|------|---------|
| Quick review | `/cco-review --quick` |
| Full review | `/cco-review` |
| Security focus | `/cco-optimize --security` |
| Everything | `/cco-optimize` |

---

## Pre-Release Workflow

```
Release candidate
        │
        ▼
┌────────────────┐
│ /cco-preflight │  Full release check
└───────┬────────┘
        │
   [Blockers?] ──yes──► Fix blockers
        │
       no
        │
   [Warnings?] ──yes──► Fix or override
        │
       no
        │
        ▼
   Tag + Release
```

| Check | Type | Action if Failed |
|-------|------|------------------|
| Clean working directory | BLOCKER | Cannot release |
| Version synced | BLOCKER | Cannot release |
| On main/release branch | WARN | Can override |
| No TODO/FIXME markers | WARN | Can override |
| Tests pass | BLOCKER | Cannot release |

---

## Maintenance Schedule

| Frequency | Use Case | Command |
|-----------|----------|---------|
| Daily | Start of session | `/cco-status` |
| Weekly | Active development | `/cco-checkup` |
| Before PR | Quality gate | `/cco-checkup` |
| Monthly | Stable projects | `/cco-review --focus=dependencies` |
| Before release | Full validation | `/cco-preflight` |

---

## Command Relationships

```
                    /cco-preflight
                   (release workflow)
                          │
          ┌───────────────┴───────────────┐
          ▼                               ▼
    /cco-optimize                   /cco-review
    (fix issues)                    (architecture)
          │                               │
          └───────────────┬───────────────┘
                          ▼
                    /cco-checkup
                   (maintenance)
                          │
                          ▼
                    /cco-status
                   (health check)
```

**Orchestration:**
- `/cco-preflight` runs optimize + review + verification
- `/cco-checkup` runs status + optimize

---

## Research Workflow

When you need to make a decision:

```
/cco-research "Which ORM should I use?"
```

| Mode | Use Case |
|------|----------|
| Standard | `/cco-research "query"` |
| Compare | `/cco-research "A vs B" --compare` |
| Security | `/cco-research "query" --security` |
| Local only | `/cco-research "query" --local` |

---

*Back to [README](../README.md)*
