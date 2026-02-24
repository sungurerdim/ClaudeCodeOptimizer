---
description: Multi-source research with CRAAP+ reliability scoring and tiered synthesis. Use when researching a topic, comparing technologies, or investigating solutions.
argument-hint: "[--quick] [--deep]"
allowed-tools: WebSearch, WebFetch, Read, Grep, Glob, Task, AskUserQuestion
---

# /cco-research

**Smart Research** — Parallel search → tier → synthesize → recommend.

Hybrid: Local (Glob/Grep) + Web (cco-agent-research).

**Current date:** Use `currentDate` from system-reminder context. Include it in every sub-agent prompt to prevent stale search results.

## Args

| Flag | Effect |
|------|--------|
| `--quick` | T1-T2 sources only |
| `--deep` | All tiers, resumable |

Without flags: ask depth question.

**Do NOT:** Fabricate sources or URLs, present T5/T6 sources without confidence caveat, skip contradiction resolution when sources disagree, or synthesize without citing specific source tiers.

## Execution Flow

Setup → Parse Query → Research [PARALLEL] → Synthesize → Output

### Phase 1: Setup [SKIP with flags]

```javascript
AskUserQuestion([
  {
    question: "How deep should the research go?",
    header: "Depth",
    options: [
      { label: "Quick", description: "T1-T2 sources only" },
      { label: "Standard (Recommended)", description: "T1-T4 sources" },
      { label: "Deep", description: "All tiers, 20+ sources, resumable" }
    ],
    multiSelect: false
  },
  {
    question: "What areas should be searched?",
    header: "Focus",
    options: [
      { label: "Local codebase", description: "Search project files" },
      { label: "Security/CVE", description: "Vulnerability databases and advisories" },
      { label: "Changelog/releases", description: "Version history and breaking changes" },
      { label: "Dependencies", description: "Package registry and compatibility" }
    ],
    multiSelect: true
  }
])
```

### Phase 2: Parse Query

Extract from $ARGUMENTS: concepts, tech domain, comparison mode, search mode (troubleshoot/changelog/security). Resolve current date from system-reminder `currentDate` — pass it explicitly to every cco-agent-research Task prompt (e.g., "Current date: 2026-02-19. Search for...").

### Phase 3: Research [BATCHED: max 2 per batch]

Launch Task calls to cco-agent-research in batches of max 2 per message (runtime concurrency limit). Do NOT use `run_in_background` for Task calls.

| Track | Agent scope | When |
|-------|------------|------|
| Local codebase | scope: local, patterns: [...] | If focus includes local |
| T1: Official docs | scope: search, allowed_domains: [official sites] | Always |
| T2: GitHub/changelogs | scope: search, allowed_domains: [github.com] | Always |
| T3: Technical blogs | scope: search | Standard+ |
| T4: Community (SO/Reddit) | scope: search, allowed_domains: [stackoverflow.com, reddit.com] | Standard+ |
| Security (NVD/CVE/Snyk) | scope: dependency | If security query |
| Comparison A/B | scope: full | If comparison detected |

**Batching order:** Group active tracks into pairs and launch sequentially. Example for Standard+ with security: Batch 1 (Local+T1) → Batch 2 (T2+T3) → Batch 3 (T4+Security) → Batch 4 (Comparison if needed). Apply saturation gate after each batch.

### Phase 4: Synthesize

Validate agent outputs. Malformed → retry once, exclude on second failure.

T1-T2 sources → cco-agent-research (scope: synthesize) for conflict resolution. T3+ → aggregate locally.

**Mandatory saturation gate:** After each search batch: if 3+ T1/T2 sources agree → skip remaining lower-tier searches, proceed to synthesis. This check is not optional.

### Phase 5: Output

Executive summary, evidence hierarchy (primary T1-T2, supporting T3-T4), contradictions resolved, knowledge gaps, recommendation (DO/DON'T/CONSIDER), sources with tier/score.

## Source Tiers

Per cco-agent-research: Source Tiers & CRAAP+ Scoring. T1 (official docs, 95-100) through T6 (unknown, <40 discard). Score <50 → discard.
