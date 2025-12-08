---
name: cco-research
description: Multi-source research with reliability scoring and AI synthesis
---

# /cco-research

**Research assistant** - Search multiple sources, score reliability, detect contradictions, synthesize AI recommendation.

**Standards:** Command Flow | Output Formatting | Question Formatting

## Context Application

| Field | Effect |
|-------|--------|
| Stack | Prioritize stack-specific sources (Python → docs.python.org, JS → MDN) |
| Type | API → focus on official API docs; CLI → man pages, --help; Library → README, changelog |
| Priority | Speed → quick mode default; Quality → deep mode default |
| Data | PII/Regulated → include compliance/security sources in research |

## Default Behavior

When called without query, ask:

| Question | Options |
|----------|---------|
| Research topic? | Free text input required |
| Depth? | Quick, Standard `[recommended]`, Deep |

Explicit flags skip questions.

## Source Reliability Tiers

| Tier | Score | Source Type | Examples |
|------|-------|-------------|----------|
| **T1** | 95-100 | Official Documentation | docs.python.org, react.dev, MDN, RFC |
| **T2** | 85-94 | Official Repo/Changelog | GitHub releases, CHANGELOG.md, migration guides |
| **T3** | 70-84 | Recognized Experts | Core contributors, library authors, RFCs |
| **T4** | 55-69 | Community Curated | Stack Overflow (high votes), verified Medium |
| **T5** | 40-54 | General Community | Dev.to, Hashnode, Reddit, blog posts |
| **T6** | 0-39 | Unverified | AI-generated, outdated (>12mo), unknown source |

### Dynamic Score Modifiers

| Modifier | Condition | Effect |
|----------|-----------|--------|
| **Freshness** | 0-3 months | +10 |
| **Freshness** | 3-12 months | 0 |
| **Freshness** | >12 months | -15 |
| **Engagement** | High stars/votes | +5 |
| **Author** | Core maintainer | +10 |
| **Cross-verified** | Confirmed by T1-T2 | +10 |
| **Bias detected** | Vendor blog about own product | -5 |
| **Bias detected** | Sponsored content | -15 |
| **Conflict** | Competing product comparison | -10 |

## Flow

### Phase 1: Query Understanding

1. Parse user query for key concepts
2. Detect current date context (use for temporal searches)
3. Identify technology/framework mentioned
4. Extract comparison intent (A vs B)
5. Determine scope: factual, opinion, best-practice, troubleshooting

Output: **Parsed Query** with search strategy

### Phase 2: Multi-Source Search

Execute parallel searches across source categories:

| Category | Sources | Search Strategy |
|----------|---------|-----------------|
| **Official** | Docs, GitHub repos, RFCs | `site:` operator + exact terms |
| **Discussion** | GitHub Issues/Discussions | Problem context, edge cases |
| **Articles** | Medium, Dev.to, blogs | Best practices, tutorials |
| **Q&A** | Stack Overflow, Reddit | Real-world problems, solutions |
| **Academic** | ArXiv, papers | Cutting-edge research (when relevant) |

Search query construction:
- Include current month/year for freshness: `"{topic} December 2025"`
- Use technology-specific sites: `site:react.dev` or `site:docs.python.org`
- Include version when relevant: `"React 19"` or `"Python 3.12"`

### Phase 3: Source Scoring

For each source found:
1. Determine base tier (T1-T6)
2. Apply dynamic modifiers
3. Calculate final score (0-100)
4. Extract key claims/findings
5. Note publication date

### Phase 4: Contradiction Detection

Compare findings across sources:
1. Identify same-topic claims with different answers
2. Map contradictions: `Topic | View A (score) | View B (score)`
3. Analyze why contradiction exists:
   - Version difference
   - Context difference
   - Opinion vs fact
   - Outdated information
4. Determine resolution or note unresolved

### Phase 5: Consensus Mapping

Calculate agreement across sources:
```
View A: X% sources (weighted by tier)
View B: Y% sources (weighted by tier)
Undecided: Z%
```

Weight formula: `T1=5x, T2=4x, T3=3x, T4=2x, T5=1x, T6=0.5x`

### Phase 6: AI Synthesis

Generate recommendation based on:
1. Weighted consensus from high-tier sources
2. Contradiction resolution (prefer T1-T2 when conflicting)
3. Freshness priority (prefer recent for fast-moving tech)
4. Context applicability (user's stack/constraints)

Include:
- **Confidence level**: HIGH (85%+) | MEDIUM (60-84%) | LOW (<60%)
- **Reasoning**: Why this recommendation
- **Caveats**: When this might not apply
- **Alternatives**: Other valid approaches with trade-offs

### Phase 7: Report Generation

Structure per Output Formatting standard.

## Output Format

```
+-- RESEARCH REPORT ------------------------------------------------+
| Query: {user question}                                            |
| Date: {current date} | Sources: {N} | Depth: {quick|standard|deep}|
+-------------------------------------------------------------------+

+-- SOURCE SUMMARY -------------------------------------------------+
| Tier | Count | Avg Score | Key Sources                           |
+------+-------+-----------+---------------------------------------+
| T1   | {n}   | {score}   | {source names}                        |
| T2   | {n}   | {score}   | {source names}                        |
| ...  | ...   | ...       | ...                                   |
+------+-------+-----------+---------------------------------------+

+-- KEY FINDINGS ---------------------------------------------------+
| # | Finding                        | Score | Sources  | Fresh    |
+---+--------------------------------+-------+----------+----------+
| 1 | {main finding}                 | {95}  | T1x2     | Current  |
| 2 | {supporting finding}           | {82}  | T2x1,T3  | Recent   |
| 3 | {alternative view}             | {68}  | T4x2     | Recent   |
+---+--------------------------------+-------+----------+----------+

+-- CONTRADICTIONS (if any) ----------------------------------------+
| Topic           | View A (Score)      | View B (Score)           |
+-----------------+---------------------+--------------------------+
| {topic}         | {view} ({score})    | {view} ({score})         |
+-----------------+---------------------+--------------------------+
| Resolution: {explanation of which is correct and why}            |
+-------------------------------------------------------------------+

+-- CONSENSUS MAP --------------------------------------------------+
| View                          | Support | Tier Weight | Status   |
+-------------------------------+---------+-------------+----------+
| {majority view}               | 65%     | T1-T2 heavy | STRONG   |
| {minority view}               | 25%     | T4-T5 heavy | WEAK     |
| {edge case view}              | 10%     | Mixed       | NICHE    |
+-------------------------------+---------+-------------+----------+

+-- AI RECOMMENDATION ----------------------------------------------+
| Confidence: {HIGH|MEDIUM|LOW} ({percentage}%)                     |
+-------------------------------------------------------------------+
| {Synthesized recommendation based on all evidence}                |
|                                                                   |
| Reasoning:                                                        |
| - {why this is recommended}                                       |
| - {key supporting evidence}                                       |
|                                                                   |
| Caveats:                                                          |
| - {when this might not apply}                                     |
| - {edge cases to consider}                                        |
|                                                                   |
| Alternatives:                                                     |
| - {option B}: {when to use instead}                               |
| - {option C}: {trade-offs}                                        |
+-------------------------------------------------------------------+

+-- SOURCES --------------------------------------------------------+
| [1] {Title} - {URL}                                               |
|     Tier: T1 | Score: 97 | Fresh: Current                        |
|     Key: "{relevant quote or summary}"                            |
|                                                                   |
| [2] {Title} - {URL}                                               |
|     Tier: T2 | Score: 85 | Fresh: Recent                         |
|     Key: "{relevant quote or summary}"                            |
+-------------------------------------------------------------------+
```

### Freshness Indicators

| Symbol | Meaning | Age |
|--------|---------|-----|
| `Current` | Very fresh | 0-3 months |
| `Recent` | Reasonably current | 3-12 months |
| `Dated` | May be outdated | 12-24 months |
| `Stale` | Likely outdated | >24 months |

## Depth Modes

| Mode | Sources | Tiers | Time |
|------|---------|-------|------|
| `--quick` | 5 max | T1-T2 only | Fast |
| `--standard` | 10 max | T1-T4 | Balanced |
| `--deep` | 20+ | All tiers | Thorough |

## Flags

| Flag | Effect |
|------|--------|
| `--quick` | T1-T2 only, 5 sources max, skip contradiction analysis |
| `--standard` | T1-T4, 10 sources, full analysis (default) |
| `--deep` | All tiers, 20+ sources, comprehensive analysis |
| `--focus=official` | Only T1-T2 official sources |
| `--focus=community` | Include T4-T5 community perspectives |
| `--compare` | A vs B comparison mode |
| `--json` | JSON output for scripting |
| `--no-ai` | Skip AI recommendation, sources only |
| `--sources-only` | List sources without analysis |

## Special Modes

### Comparison Mode (`--compare`)

When query contains "vs", "or", "compared to":

```
+-- COMPARISON: {A} vs {B} -----------------------------------------+
| Aspect          | {A}              | {B}              | Winner   |
+-----------------+------------------+------------------+----------+
| Performance     | {finding}        | {finding}        | {A|B|Tie}|
| Ease of Use     | {finding}        | {finding}        | {A|B|Tie}|
| Community       | {finding}        | {finding}        | {A|B|Tie}|
| Documentation   | {finding}        | {finding}        | {A|B|Tie}|
+-----------------+------------------+------------------+----------+
| OVERALL         | {summary}        | {summary}        | {verdict}|
+-------------------------------------------------------------------+
| AI Verdict: {recommendation based on user's context}              |
+-------------------------------------------------------------------+
```

### Troubleshooting Mode

When query contains "error", "not working", "fix", "issue":

1. Search for error message in GitHub Issues
2. Check Stack Overflow for solutions
3. Verify if known bug in release notes
4. Prioritize solutions with confirmed success

## Bias Detection

Flag and adjust scores for:

| Bias Type | Detection | Adjustment |
|-----------|-----------|------------|
| Vendor self-promotion | Company blog about own product | -5 |
| Sponsored content | Disclosure present | -15 |
| Competitor comparison | Single vendor comparing rivals | -10 |
| Outdated advocacy | Old article promoting deprecated | -20 |
| AI-generated | Detected patterns | -25 |

## Evidence Chain

For each key finding, show evidence trail:

```
Claim: "{finding}"
  <- Source 1 (T1, 95) confirms
  <- Source 2 (T2, 88) confirms
  <- Source 3 (T4, 62) contradicts (reason: outdated)
  = Strong evidence (2 T1-T2 confirmations)
```

## Usage

```bash
/cco-research "React 19 best practices for server components"
/cco-research "Python async vs threading 2025" --deep
/cco-research "Bun vs Node.js production performance" --compare
/cco-research "TypeScript 5.3 new features" --focus=official
/cco-research "Next.js 14 app router migration" --quick
/cco-research --json "GraphQL vs REST API design"
```

## Integration Notes

- Uses WebSearch for source discovery
- Uses WebFetch for content extraction
- Respects domain allowlist from settings
- Caches results for 15 minutes (same query)
- Falls back gracefully if sources unavailable
