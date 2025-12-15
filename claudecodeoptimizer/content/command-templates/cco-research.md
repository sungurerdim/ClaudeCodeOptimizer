---
name: cco-research
description: Multi-source research with reliability scoring
allowed-tools: WebSearch(*), WebFetch(*), Read(*), Grep(*), Glob(*), Task(*), TodoWrite, AskUserQuestion
---

# /cco-research

**Smart Research** - Search → score → synthesize → recommend.

End-to-end: Searches multiple sources, scores reliability, synthesizes findings.

## Context

- Context check: !`test -f ./.claude/rules/cco/context.md && echo "1" || echo "0"`
- Current date: !`date +%Y-%m-%d`

**DO NOT re-run these commands. Use the pre-collected values above.**

## Context Requirement [CRITICAL]

If context check returns "0":
```
CCO context not found.

Run /cco-config first to configure project context, then restart CLI.
```
**Stop immediately.**

## Architecture

| Step | Name | Action |
|------|------|--------|
| 1 | Depth | Ask research depth |
| 2 | Query | Parse and understand query |
| 3 | Research | Run agent with query |
| 4 | Synthesize | Process agent results |
| 5 | Output | Show structured findings |

---

## Progress Tracking [CRITICAL]

```javascript
TodoWrite([
  { content: "Step-1: Select depth", status: "in_progress", activeForm: "Selecting depth" },
  { content: "Step-2: Parse query", status: "pending", activeForm: "Parsing query" },
  { content: "Step-3: Run research", status: "pending", activeForm: "Running research" },
  { content: "Step-4: Synthesize findings", status: "pending", activeForm: "Synthesizing findings" },
  { content: "Step-5: Show output", status: "pending", activeForm: "Showing output" }
])
```

---

## Step-1: Depth Selection

```javascript
AskUserQuestion([{
  question: "Research depth?",
  header: "Depth",
  options: [
    { label: "Quick", description: "T1-T2 sources only, 5 max" },
    { label: "Standard", description: "T1-T4 sources, 10 max" },
    { label: "Deep", description: "All tiers, 20+ sources" }
  ],
  multiSelect: false
}])
```

**Dynamic labels:** Add `(Recommended)` based on query complexity.

**Flags override:** `--quick`, `--standard`, `--deep` skip this question.

### Validation
```
[x] User selected depth
→ Store as: depth = {selection}
→ Proceed to Step-2
```

---

## Step-2: Parse Query

Parse query for:
- Concepts: main topics
- Date context: version, release date
- Tech/framework: specific technologies
- Comparison intent: "vs", "or", "compared to"
- Mode detection: troubleshooting, changelog, security

### Validation
```
[x] Query parsed
→ Store as: parsedQuery = { concepts, date, tech, comparison, mode }
→ Proceed to Step-3
```

---

## Step-3: Research

```javascript
agentResponse = Task("cco-agent-research", `
  scope: full
  query: "${userQuery}"
  depth: ${depth}
  parsedQuery: ${JSON.stringify(parsedQuery)}

  Multi-source search → Tiering → Synthesis → Structured recommendation
`)
```

**CRITICAL:** ONE research agent. Never per-source or per-strategy.

**Local Mode (`--local`):** Uses `cco-agent-analyze` with `scope: scan`.

### Validation
```
[x] Agent returned results
[x] results.sources exists
[x] results.synthesis exists
→ Proceed to Step-4
```

---

## Step-4: Synthesize

Process agent results:
- Weight by tier and score
- Resolve contradictions
- Identify knowledge gaps
- Generate recommendation

### Validation
```
[x] Synthesis complete
→ Store as: synthesis = { summary, evidence, contradictions, gaps, recommendation }
→ Proceed to Step-5
```

---

## Step-5: Output

Display structured output:

1. **Executive Summary** - TL;DR + confidence score + saturation indicator
2. **Evidence Hierarchy** - Primary (85+) / Supporting (70-84) with scores
3. **Contradictions Resolved** - Claim A vs B → Winner with reason
4. **Knowledge Gaps** - Topics with no/limited sources
5. **Actionable Recommendation** - DO / DON'T / CONSIDER with caveats
6. **Source Citations** - [N] title | url | tier | score | date
7. **Metadata** - Iterations, discards, saturation status

### Validation
```
[x] Output displayed
[x] All todos marked completed
→ Done
```

---

## Reference

### Context Application

| Field | Effect |
|-------|--------|
| Stack | Prioritize stack-specific sources |
| Type | API → API docs; CLI → man pages |
| Priority | Speed → quick; Quality → deep |
| Data | PII/Regulated → include compliance |

### Special Modes

| Mode | Focus |
|------|-------|
| `--local` | Codebase only |
| `--changelog` | Breaking changes, migration |
| `--security` | CVEs, advisories |
| `--dependency` | Package versions, CVEs |
| `--compare` | Side-by-side comparison |

### Flags

| Flag | Effect |
|------|--------|
| `--quick` | T1-T2 only, 5 sources |
| `--standard` | T1-T4, 10 sources (default) |
| `--deep` | All tiers, 20+ sources |
| `--local` | Codebase only |
| `--changelog` | Breaking changes |
| `--security` | CVEs/advisories |
| `--dependency` | Package versions |
| `--compare` | A vs B mode |
| `--json` | JSON output |
| `--sources-only` | No synthesis |

### Source Tiers

| Tier | Sources | Score Range |
|------|---------|-------------|
| T1 | Official docs, specs | 90-100 |
| T2 | GitHub, changelogs | 80-90 |
| T3 | Major blogs, tutorials | 70-80 |
| T4 | Stack Overflow, forums | 60-70 |
| T5 | Personal blogs | 50-60 |
| T6 | Unknown | 40-50 |

---

## Rules

1. **Sequential execution** - Complete each step before proceeding
2. **Validation gates** - Check validation block before next step
3. **ONE research agent** - Never spawn multiple agents
4. **Early saturation** - Stop when 3+ sources agree
5. **Stack-aware** - Prioritize context-relevant sources
