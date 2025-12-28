---
name: cco-research
description: Multi-source research with reliability scoring
allowed-tools: WebSearch(*), WebFetch(*), Read(*), Grep(*), Glob(*), Task(*), TodoWrite, AskUserQuestion
model: opus
---

# /cco-research

**Smart Research** - Parallel search → tier → synthesize → recommend with minimal questions.

Hybrid research: Local (Glob/Grep) + Web (cco-agent-research) with tiered model strategy.

## Context

- Current date: !`date +%Y-%m-%d`

**DO NOT re-run these commands. Use the pre-collected values above.**

## Architecture

| Step | Name | Action | Optimization |
|------|------|--------|--------------|
| 1 | Setup | Q1: Depth selection (skip with flags) | Optional question |
| 2 | Query | Parse and understand | Instant |
| 3 | Research | Parallel: Local + Web sources | Fast |
| 4 | Synthesize | Tiered model strategy | Accurate |
| 5 | Output | Progressive display | Real-time |

---

## Progress Tracking [CRITICAL]

```javascript
TodoWrite([
  { content: "Step-1: Select depth", status: "in_progress", activeForm: "Selecting depth" },
  { content: "Step-2: Parse query", status: "pending", activeForm: "Parsing query" },
  { content: "Step-3: Run parallel research", status: "pending", activeForm: "Running research" },
  { content: "Step-4: Synthesize findings", status: "pending", activeForm: "Synthesizing" },
  { content: "Step-5: Show output", status: "pending", activeForm: "Showing output" }
])
```

---

## Step-1: Depth Selection [Q1 - SKIP WITH FLAGS]

**Default: Standard depth. Only ask if no flag provided.**

```javascript
// Check for flags
if (flags.quick || flags.standard || flags.deep) {
  depth = flags.quick ? "Quick" : flags.deep ? "Deep" : "Standard"
  // Skip question, proceed to Step-2
} else {
  AskUserQuestion([{
    question: "Research depth?",
    header: "Depth",
    options: [
      { label: "Quick", description: "T1-T2 sources, 3 parallel searches" },
      { label: "Standard (Recommended)", description: "T1-T4 sources, 5 parallel searches" },
      { label: "Deep", description: "All tiers, 7+ parallel searches, resumable" }
    ],
    multiSelect: false
  }])
}
```

| Depth | Parallel Agents | Model Strategy |
|-------|-----------------|----------------|
| Quick | 3 | All Haiku |
| Standard | 5 | Haiku search, Sonnet synthesis |
| Deep | 7+ | Haiku search, Opus synthesis |

### Validation
```
[x] Depth determined (from flag or user)
→ Store as: depth = {selection}
→ Proceed to Step-2
```

---

## Step-2: Parse Query

**Parse query for search strategy:**

| Element | Detection | Effect |
|---------|-----------|--------|
| Concepts | Main topics, keywords | Primary search terms |
| Date | Version, year, "latest" | Add year to queries |
| Tech | Framework, language | Domain filter |
| Comparison | "vs", "or", "compared" | Multi-track search |
| Mode | Troubleshoot, changelog, security | Specialized sources |

```javascript
parsedQuery = parseQuery(userQuery)
// Returns: { concepts, date, tech, comparison, mode }
```

### Validation
```
[x] Query parsed
→ Proceed to Step-3
```

---

## Step-3: Research [PARALLEL]

**Launch all search agents in a SINGLE message:**

### 3.1 Local Codebase Search (Always)

```javascript
// Parallel pattern searches in ONE message (use project-specific extensions from context)
Glob("**/*.{py,ts,js,go,rs,md}")
Grep(queryKeywords, { output_mode: "content", "-C": 3 })
Read(relevantFiles)
```

### 3.2 Web Search (Parallel by Source Type)

```javascript
// T1: Official Documentation
Task("cco-agent-research", `
  scope: search
  query: "${parsedQuery.concepts} official documentation ${parsedQuery.date}"
  allowed_domains: [docs.*, official.*, *.io/docs, *.dev/docs]
`, { model: "haiku", run_in_background: depth === "deep" })

// T2: GitHub & Changelogs
Task("cco-agent-research", `
  scope: search
  query: "${parsedQuery.concepts} github changelog release notes"
  allowed_domains: [github.com, gitlab.com, bitbucket.org]
`, { model: "haiku", run_in_background: depth === "deep" })

// T3: Technical Blogs (Standard+)
if (depth !== "quick") {
  Task("cco-agent-research", `
    scope: search
    query: "${parsedQuery.concepts} tutorial guide best practices"
  `, { model: "haiku", run_in_background: true })
}

// T4: Community (Standard+)
if (depth !== "quick") {
  Task("cco-agent-research", `
    scope: search
    query: "${parsedQuery.concepts} stackoverflow discussion"
    allowed_domains: [stackoverflow.com, reddit.com, dev.to, hashnode.com]
  `, { model: "haiku", run_in_background: true })
}

// Security Track (if --security or security-related query)
if (parsedQuery.mode === "security") {
  Task("cco-agent-research", `
    scope: search
    query: "${parsedQuery.concepts} CVE vulnerability advisory"
    allowed_domains: [nvd.nist.gov, cve.mitre.org, snyk.io, github.com/advisories]
  `, { model: "haiku" })
}
```

### 3.3 Comparison Mode (if detected)

```javascript
if (parsedQuery.comparison) {
  // Split into separate tracks for A vs B comparison
  Task("cco-agent-research", `
    scope: search
    query: "${parsedQuery.comparison.optionA} features pros cons"
  `, { model: "haiku", run_in_background: true })

  Task("cco-agent-research", `
    scope: search
    query: "${parsedQuery.comparison.optionB} features pros cons"
  `, { model: "haiku", run_in_background: true })
}
```

### 3.4 Deep Mode: Resumable Research

```javascript
if (depth === "Deep") {
  // Save agent IDs for potential resume
  researchSession = {
    id: generateSessionId(),
    agents: [agent1.id, agent2.id, ...],
    completedSources: [],
    pendingSources: []
  }
  // Can resume with: Task(..., { resume: researchSession.agents[0] })
}
```

### Validation
```
[x] All search agents launched in parallel
[x] Results collected (wait for all or timeout after 30s)
[x] Sources deduplicated and tiered
→ Proceed to Step-4
```

---

## Step-4: Synthesize [TIERED MODEL]

**Model selection by source tier:**

```javascript
// Collect all search results
allSources = searchResults.flatMap(r => r.sources)

// Filter by tier
t1t2Sources = allSources.filter(s => s.tier === "T1" || s.tier === "T2")
t3PlusSources = allSources.filter(s => ["T3", "T4", "T5"].includes(s.tier))

// High-value synthesis (T1-T2) → Better model for conflict resolution
synthesis = Task("cco-agent-research", `
  scope: synthesize
  sources: ${JSON.stringify(t1t2Sources)}
`, { model: "opus" })

// Supporting evidence (T3+) → aggregate locally
supportingEvidence = aggregateByTier(t3PlusSources)
```

### Synthesis Process

| Step | Action | Model |
|------|--------|-------|
| Dedupe | Remove duplicate sources | None (logic) |
| Tier | Assign confidence by source | None (rules) |
| Conflict | Resolve contradictions | Opus/Sonnet |
| Gaps | Identify missing info | Sonnet |
| Recommend | Generate actionable advice | Opus/Sonnet |

### Early Saturation

```javascript
// Stop searching when confident enough
// Saturation criteria: 3+ T1/T2 sources independently confirm same conclusion
const agreeing = sources.filter(s =>
  s.tier <= 2 &&
  s.conclusion === majorityConclusion
).length

if (agreeing >= 3) {
  saturation = "HIGH"  // Can skip remaining background agents
} else if (agreeing >= 2 && noContradictions) {
  saturation = "MEDIUM"  // Continue but deprioritize
} else {
  saturation = "LOW"  // Keep searching
}
```

### Validation
```
[x] All sources tiered and weighted
[x] Contradictions resolved
[x] Recommendation generated
→ Proceed to Step-5
```

---

## Step-5: Output [PROGRESSIVE]

**Show sections as they complete:**

```
## Executive Summary
{summary}
Confidence: {confidence} ({n} T1 sources agree) | Saturation: {saturation}%

## Evidence Hierarchy

### Primary (T1-T2, Score 85+)
| # | Source | Tier | Score | Key Finding |
|---|--------|------|-------|-------------|
| {n} | {source} | {tier} | {score} | {finding} |

### Supporting (T3-T4, Score 70-84)
| # | Source | Tier | Score | Key Finding |
|---|--------|------|-------|-------------|
| {n} | {source} | {tier} | {score} | {finding} |

## Contradictions Resolved
- **{claim_a}** ({source_a}): {approach_a}
- **{claim_b}** ({source_b}): {approach_b}
- **Resolution**: {resolution}

## Knowledge Gaps
- No sources found for: {gap}
- Limited coverage: {limitation}

## Recommendation
**DO**: {recommendation}
**DON'T**: {anti_pattern}
**CONSIDER**: {consideration}

## Sources
[{n}] {title} | {url} | {tier} | {score} | {date}

## Metadata
- Parallel searches: {n}
- Sources found: {n}
- Sources used: {n}
- Discarded (low quality): {n}
- Saturation: {saturation}%
- Research time: {n}s
```

### Validation
```
[x] Output displayed with all sections
[x] Sources properly cited
[x] All todos marked completed
→ Done
```

---

## Reference

### Question Flow Summary

| Scenario | Questions |
|----------|-----------|
| With `--quick`, `--standard`, or `--deep` flag | 0 |
| Without flag | 1 (Depth) |

**Key optimization:** Default to Standard, flags skip the only question.

### Context Application

| Field | Effect |
|-------|--------|
| Stack | Prioritize stack-specific sources |
| Type | API → API docs; CLI → man pages |
| Priority | Speed → quick; Quality → deep |
| Data | PII/Regulated → include compliance |

### Special Modes

| Mode | Focus | Extra Agents |
|------|-------|--------------|
| `--local` | Codebase only | Glob/Grep only |
| `--changelog` | Breaking changes | GitHub releases track |
| `--security` | CVEs, advisories | Security DB track |
| `--dependency` | Package versions | npm/PyPI track |
| `--compare` | Side-by-side | Dual track search |

### Flags

| Flag | Effect |
|------|--------|
| `--quick` | 3 parallel, T1-T2, Haiku only, no question |
| `--standard` | 5 parallel, T1-T4, Sonnet synthesis, no question |
| `--deep` | 7+ parallel, all tiers, Opus synthesis, resumable, no question |
| `--local` | Local Glob/Grep only, no web |
| `--changelog` | Focus on releases |
| `--security` | Include CVE databases |
| `--dependency` | Package registry search |
| `--compare` | A vs B dual track |
| `--json` | JSON output |
| `--sources-only` | No synthesis |
| `--resume=ID` | Resume previous deep research |

### Source Tiers

| Tier | Sources | Score | Model |
|------|---------|-------|-------|
| T1 | Official docs, specs | 90-100 | Opus (deep) |
| T2 | GitHub, changelogs | 80-90 | Opus (deep) |
| T3 | Major blogs, tutorials | 70-80 | Sonnet |
| T4 | Stack Overflow, forums | 60-70 | Haiku |
| T5 | Personal blogs | 50-60 | Haiku |
| T6 | Unknown | 40-50 | Skip |

### Model Strategy

| Task | Depth: Quick | Depth: Standard | Depth: Deep |
|------|--------------|-----------------|-------------|
| Search | Haiku | Haiku | Haiku |
| Fetch | Haiku | Haiku | Haiku |
| T1-T2 Synthesis | Haiku | Sonnet | Opus |
| Recommendation | Haiku | Sonnet | Opus |

---

## Rules

1. **Flag-driven** - Depth flags skip the only question
2. **Parallel-first** - Launch all search agents in single message
3. **Tiered synthesis** - Better model for higher-tier sources
4. **Early saturation** - Stop when 3+ T1/T2 sources agree
5. **Progressive display** - Show results as agents complete
6. **Resumable** - Deep research saves state for continuation
7. **Stack-aware** - Prioritize context-relevant sources
8. **Conservative confidence** - When sources conflict → LOW confidence; uncertain → choose lower tier
