---
description: Multi-source research with CRAAP+ reliability scoring
argument-hint: "[--quick] [--deep]"
allowed-tools: WebSearch, WebFetch, Read, Grep, Glob, Task, AskUserQuestion
model: opus
---

# /cco:research

**Smart Research** - Parallel search → tier → synthesize → recommend with minimal questions.

> **Implementation Note:** Code blocks use JavaScript-like pseudocode for clarity. Actual execution uses Claude Code tools with appropriate parameters.

Hybrid research: Local (Glob/Grep) + Web (cco-agent-research) with tiered model strategy.

## Context

- Current date: !`date +%Y-%m-%d`

**DO NOT re-run these commands. Use the pre-collected values above.**

## Architecture

| Step | Name | Action | Optimization | Dependency |
|------|------|--------|--------------|------------|
| 1 | Setup | Q1: Depth selection (skip with flags) | Optional question | - |
| 2 | Query | Parse and understand | Instant | [SEQUENTIAL] after 1 |
| 3 | Research | Parallel: Local + Web sources | Fast | [SEQUENTIAL] after 2 |
| 4 | Synthesize | Tiered model strategy | Accurate | [SEQUENTIAL] after 3 |
| 5 | Output | Progressive display | Real-time | [SEQUENTIAL] after 4 |

**Execution Flow:** 1 → 2 → 3 (internal parallelism) → 4 → 5

---

## Step-1: Research Settings [Q1]

```javascript
AskUserQuestion([
  {
    question: "How thorough?",
    header: "Depth",
    options: [
      { label: "Quick", description: "Fast - official docs only (T1-T2)" },
      { label: "Standard (Recommended)", description: "Comprehensive - blogs, forums (T1-T4)" },
      { label: "Deep", description: "Exhaustive - all sources, resumable" }
    ],
    multiSelect: false
  },
  {
    question: "Special focus areas?",
    header: "Focus",
    options: [
      { label: "Local codebase", description: "Search this project's code too" },
      { label: "Security/CVE", description: "Include vulnerability databases" },
      { label: "Changelog/releases", description: "Focus on version changes" },
      { label: "Dependencies", description: "Package registry search" }
    ],
    multiSelect: true
  }
])
```

| Depth | Parallel Agents | Model Strategy |
|-------|-----------------|----------------|
| Quick | 3 | All Haiku |
| Standard | 5 | Haiku search, Opus synthesis |
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

> **Architecture:** Command only orchestrates. All search (local + web) delegated to agents.

### 3.1 Local Codebase Search (via Agent)

```javascript
// Delegate local search to research agent (NOT analyze agent)
// Purpose: Find examples, understand existing implementations
// analyze agent is for quality/security scanning, not information research
localResults = Task("cco-agent-research", `
  scope: local
  query: "${parsedQuery.concepts}"
  patterns: ["**/*.{py,ts,js,go,rs,md}"]
  context_lines: 3
`, { model: "haiku" })  // Synchronous - results returned directly
// NOTE: Do NOT use run_in_background: true for Task (agent) calls
// Multiple Task calls in same message execute in parallel automatically
```

### 3.2 Web Search (via Agent)

```javascript
// PARALLEL EXECUTION: Multiple Task calls in same message run in parallel
// Each Task returns results directly (synchronous)

// T1: Official Documentation
docsResults = Task("cco-agent-research", `
  scope: search
  query: "${parsedQuery.concepts} official documentation ${parsedQuery.date}"
  allowed_domains: [docs.*, official.*, *.io/docs, *.dev/docs]
`, { model: "haiku" })

// T2: GitHub & Changelogs
githubResults = Task("cco-agent-research", `
  scope: search
  query: "${parsedQuery.concepts} github changelog release notes"
  allowed_domains: [github.com, gitlab.com, bitbucket.org]
`, { model: "haiku" })

// T3: Technical Blogs (Standard+)
let blogResults = null
if (depth !== "quick") {
  blogResults = Task("cco-agent-research", `
    scope: search
    query: "${parsedQuery.concepts} tutorial guide best practices"
  `, { model: "haiku" })
}

// T4: Community (Standard+)
let communityResults = null
if (depth !== "quick") {
  communityResults = Task("cco-agent-research", `
    scope: search
    query: "${parsedQuery.concepts} stackoverflow discussion"
    allowed_domains: [stackoverflow.com, reddit.com, dev.to, hashnode.com]
  `, { model: "haiku" })
}

// Security Track (if security-related query detected)
let securityResults = null
if (parsedQuery.mode === "security") {
  securityResults = Task("cco-agent-research", `
    scope: search
    query: "${parsedQuery.concepts} CVE vulnerability advisory"
    allowed_domains: [nvd.nist.gov, cve.mitre.org, snyk.io, github.com/advisories]
  `, { model: "haiku" })
}
```

### 3.3 Comparison Mode (if detected)

```javascript
if (parsedQuery.comparison) {
  // PARALLEL: Multiple Task calls in same message
  optionAResults = Task("cco-agent-research", `
    scope: search
    query: "${parsedQuery.comparison.optionA} features pros cons"
  `, { model: "haiku" })

  optionBResults = Task("cco-agent-research", `
    scope: search
    query: "${parsedQuery.comparison.optionB} features pros cons"
  `, { model: "haiku" })
}
```

### 3.4 Deep Mode: Resumable Research

```javascript
if (depth === "Deep") {
  // Save agent IDs for potential resume
  researchSession = {
    id: `research-${Date.now()}`,  // Simple timestamp-based ID
    agents: [agent1.id, agent2.id],
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
| Conflict | Resolve contradictions | Opus |
| Gaps | Identify missing info | Haiku |
| Recommend | Generate actionable advice | Opus |

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

### Depth Levels

| Depth | Sources | Parallel | Model |
|-------|---------|----------|-------|
| **Quick** | T1-T2 (official docs) | 3 | Haiku |
| **Standard** | T1-T4 (blogs, forums) | 5 | Haiku + Opus |
| **Deep** | All tiers | 7+ | Haiku + Opus |

### Focus Areas

| Focus | Effect |
|-------|--------|
| **Local codebase** | Include Glob/Grep on project files |
| **Security/CVE** | Add NVD, CVE, Snyk databases |
| **Changelog/releases** | Prioritize GitHub releases, changelogs |
| **Dependencies** | Search npm, PyPI, crates.io |

### Source Tiers

| Tier | Sources | Score | Model |
|------|---------|-------|-------|
| T1 | Official docs, specs | 90-100 | Opus |
| T2 | GitHub, changelogs | 80-90 | Opus |
| T3 | Major blogs, tutorials | 70-80 | Haiku |
| T4 | Stack Overflow, forums | 60-70 | Haiku |
| T5 | Personal blogs | 50-60 | Haiku |
| T6 | Unknown | 40-50 | Skip |

### Model Strategy

| Task | Depth: Quick | Depth: Standard | Depth: Deep |
|------|--------------|-----------------|-------------|
| Search | Haiku | Haiku | Haiku |
| Fetch | Haiku | Haiku | Haiku |
| T1-T2 Synthesis | Haiku | Opus | Opus |
| Recommendation | Haiku | Opus | Opus |

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
