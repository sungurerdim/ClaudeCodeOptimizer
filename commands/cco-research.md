---
description: Multi-source research with CRAAP+ reliability scoring
argument-hint: "[--quick] [--deep]"
allowed-tools: WebSearch, WebFetch, Read, Grep, Glob, Task, AskUserQuestion
model: opus
---

# /cco-research

**Smart Research** — Parallel search → tier → synthesize → recommend.

Hybrid research: Local (Glob/Grep) + Web (cco-agent-research).

## Context

- Current date: !`date +%Y-%m-%d`

## Args

| Flag | Effect |
|------|--------|
| `--quick` | T1-T2 sources only |
| `--deep` | All tiers, resumable |

Without flags: ask depth question.

## Execution Flow

Setup → Parse Query → Research [PARALLEL] → Synthesize → Output

### Phase 1: Setup [SKIP with flags]

```javascript
AskUserQuestion([
  {
    question: "How deep should the research go?",
    header: "Depth",
    options: [
      { label: "Quick", description: "T1-T2 sources only, fast results" },
      { label: "Standard (Recommended)", description: "T1-T4 sources, good balance" },
      { label: "Deep", description: "All tiers, 20+ sources, resumable" }
    ],
    multiSelect: false
  },
  {
    question: "What areas should be searched?",
    header: "Focus",
    options: [
      { label: "Local codebase", description: "Search project files for answers" },
      { label: "Security/CVE", description: "Vulnerability databases and advisories" },
      { label: "Changelog/releases", description: "Version history and breaking changes" },
      { label: "Dependencies", description: "Package registry and compatibility info" }
    ],
    multiSelect: true
  }
])
```

### Phase 2: Parse Query

Extract from $ARGS: concepts, date context, tech domain, comparison mode, search mode (troubleshoot/changelog/security).

### Phase 3: Research [PARALLEL: up to 7 calls]

Launch all search agents in single message via parallel Task calls to cco-agent-research:

| Track | Scope | When |
|-------|-------|------|
| Local codebase | scope: local | If focus includes local |
| T1: Official docs | scope: search, official domains | Always |
| T2: GitHub/changelogs | scope: search, GitHub domains | Always |
| T3: Technical blogs | scope: search, tutorials | Standard+ |
| T4: Community | scope: search, SO/Reddit/dev.to | Standard+ |
| Security | scope: search, NVD/CVE/Snyk | If security query |
| Comparison A/B | scope: search, per option | If comparison detected |

### Phase 4: Synthesize

- T1-T2 sources → cco-agent-research for conflict resolution
- T3+ sources → aggregate locally

Early saturation: 3+ T1/T2 sources agree → stop searching.

### Phase 5: Output

Display: Executive summary, evidence hierarchy (primary T1-T2, supporting T3-T4), contradictions resolved, knowledge gaps, recommendation (DO/DON'T/CONSIDER), sources with tier/score, metadata.

## Source Tiers

| Tier | Sources | Score |
|------|---------|-------|
| T1 | Official docs, specs | 90-100 |
| T2 | GitHub, changelogs | 80-90 |
| T3 | Major blogs, tutorials | 70-80 |
| T4 | Stack Overflow, forums | 60-70 |
| T5 | Personal blogs | 50-60 |
| T6 | Unknown | Skip |
