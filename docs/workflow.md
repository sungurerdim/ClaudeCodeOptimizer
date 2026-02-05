# Workflow Guide

How to integrate CCO into your development workflow.

---

## Quick Reference

| I want to... | Command |
|--------------|---------|
| Fix issues | `/cco-optimize` |
| Review architecture | `/cco-align` |
| Commit with quality gates | `/cco-commit` |
| Prepare for release | `/cco-preflight` |
| Research a topic | `/cco-research` |
| Update CCO | `/cco-update` |

---

## Daily Development

```
Start session
     │
     ▼
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
| Ready to commit | `/cco-commit` |
| Quick cleanup | `/cco-optimize --quick` |
| Full optimization | `/cco-optimize` |

---

## Pre-PR Workflow

```
Feature complete
     │
     ▼
┌────────────────┐
│  /cco-align    │  Architecture check
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
| Quick architecture check | `/cco-align --quick` |
| Full architecture review | `/cco-align` |
| Security focus | `/cco-optimize --scope=security` |
| Full optimization | `/cco-optimize` |

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
| Daily | Before important commits | `/cco-commit` |
| Weekly | Active development | `/cco-optimize` |
| Before PR | Quality gate | `/cco-align` + `/cco-optimize` |
| Monthly | Stable projects | `/cco-align --focus=dependencies` |
| Before release | Full validation | `/cco-preflight` |

---

## Command Relationships

```
                   /cco-preflight
                  (release workflow)
                         │
         ┌───────────────┴───────────────┐
         ▼                               ▼
   /cco-optimize                   /cco-align
   (fix issues)                    (architecture)
         │                               │
         └───────────────┬───────────────┘
                         ▼
                   /cco-commit
                  (quality gates)
```

**Orchestration:**
- `/cco-preflight` runs optimize + align + verification in parallel

---

## Research Workflow

When you need to make a decision:

```
/cco-research "Which ORM should I use?"
```

| Mode | Use Case |
|------|----------|
| Standard | `/cco-research "query"` |
| Quick | `/cco-research "query" --quick` |
| Deep | `/cco-research "query" --deep` |

---

*Back to [README](../README.md)*
