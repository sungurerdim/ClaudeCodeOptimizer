---
name: cco-research
description: Multi-source research with reliability scoring
allowed-tools: WebSearch(*), WebFetch(*), Read(*), Grep(*), Glob(*), Task(*), TodoWrite
---

# /cco-research

**Smart Research** - Search → score → synthesize → recommend.

End-to-end: Searches multiple sources, scores reliability, synthesizes findings.

**Rules:** User Input | Source Reliability | Quick Mode | Task Tracking

## Context

- Context check: !`test -f ./.claude/rules/cco/context.md && echo "1" || echo "0"`
- Current date: !`date +%Y-%m-%d`

**Static context (Stack, Type, Priority, Data) is read from ./CLAUDE.md already in context.**

## Context Requirement [CRITICAL]

**This command requires CCO context in ./.claude/rules/cco/context.md.**

If context check returns "0":
```
CCO context not found.

Run /cco-config first to configure project context, then restart CLI.
```
**Stop execution immediately.**

## Context Application

| Field | Effect |
|-------|--------|
| Stack | Prioritize stack-specific sources (Python → docs.python.org, JS → MDN) |
| Type | API → focus on official API docs; CLI → man pages, --help; Library → README, changelog |
| Priority | Speed → quick mode default; Quality → deep mode default |
| Data | PII/Regulated → include compliance/security sources in research |

## Agent Integration

| Phase | Agent | Scope | Purpose |
|-------|-------|-------|---------|
| Search | `cco-agent-research` | `search` | Multi-source discovery with tiering |
| Analyze | `cco-agent-research` | `analyze` | Deep source analysis, contradiction detection |
| Synthesize | `cco-agent-research` | `synthesize` | Generate weighted recommendation |
| Full | `cco-agent-research` | `full` | All phases combined (standard flow) |

### Parallel Search Pattern [REQUIRED]

For deep research, launch **5 parallel agents** with diverse search strategies:

```
Launch simultaneously:
- Agent 1: Official docs search (site:docs.*, site:*.dev)
- Agent 2: GitHub issues/discussions search
- Agent 3: Stack Overflow/community search
- Agent 4: Blog/article search (Medium, Dev.to)
- Agent 5: Alternative keyword variations
```

### Agent Propagation

When spawning search agents, include:
```
Context: {Stack, Type from CCO_ADAPTIVE}
Rules: Source reliability tiers, freshness scoring
Output: {url} | {tier} | {score} | {key_claim}
Note: Make a todo list first, use diverse keywords
```

**Local Mode:** For `--local` flag, uses `cco-agent-analyze` with `scope: scan` instead (codebase-only search).

## Default Behavior

When called without query:

**Use AskUserQuestion:**
| Question | Options | MultiSelect |
|----------|---------|-------------|
| Depth? | Standard (Recommended); Quick; Deep | false |

*Note: Research topic is free text - use AskUserQuestion with text input option.*

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

## Research Quality [CRITICAL]

### Adaptive Source Replacement [CRITICAL]

**Do NOT stop at a fixed source count.** Quality over quantity.

| Source Evaluation | Action |
|-------------------|--------|
| Score < 50 | **DISCARD** - Search for replacement |
| Irrelevant to query | **DISCARD** - Refine search terms |
| Duplicate information | **SKIP** - Already covered |
| Outdated (>2y for tech) | **FLAG** - Seek newer alternative |

**Replacement Loop:**
```
FOR each source:
  IF score < 50 OR irrelevant:
    DISCARD source
    SEARCH with refined keywords
    CONTINUE until quality source found
  END
END

GOAL: {N} HIGH-QUALITY sources, not just {N} sources
```

**Never declare "research complete" with insufficient quality sources.**

### Hypothesis Tracking

Maintain competing hypotheses throughout research:

```
H1: [Primary hypothesis] - Confidence: {%}
  Evidence: {sources supporting}
  Counter: {sources against}
H2: [Alternative hypothesis] - Confidence: {%}
  Evidence: {sources supporting}
  Counter: {sources against}
```

### Self-Critique Loop

After gathering sources, explicitly ask:
1. What evidence would **disprove** my current conclusion?
2. Which sources **contradict** each other and why?
3. Am I missing a **major perspective** or source type?

### Cross-Verification Rule

| Confidence | Requirement |
|------------|-------------|
| HIGH (85%+) | Confirmed by 2+ T1-T2 sources |
| MEDIUM (60-84%) | Confirmed by T1-T3, or single T1 |
| LOW (<60%) | Single source or T4-T6 only |

**Never report HIGH confidence without cross-verification.**

## Iterative Deepening Strategy [DEEP MODE]

### Round 1: Seed Search
- Execute 5 parallel searches (existing pattern)
- Collect initial 10-15 sources

### Round 2: Backward Snowballing
- Extract references from Round 1's T1-T2 sources
- Identify "frequently cited" foundational sources
- Add high-value references to source pool

### Round 3: Forward Snowballing
- Find newer sources citing Round 1 results
- Discover recent developments and updates
- Capture latest perspectives

### Round 4: Keyword Expansion
- Extract new terms from collected sources
- Example: "React hooks" → "useEffect cleanup", "stale closure"
- Search with expanded vocabulary

### Saturation Detection

| Indicator | Detection | Action |
|-----------|-----------|--------|
| **Thematic Saturation** | Last 3 sources repeat same themes | Stop searching |
| **Code Saturation** | No new terms/concepts emerging | Stop expanding |
| **Information Redundancy** | 80%+ overlap with existing | Skip source |

**Stopping Criterion:**
1. Collect minimum sources (Quick=5, Standard=10, Deep=15)
2. After each new source: "Does this add new information?"
3. Three consecutive "no" → Research saturated

**Report:** "Saturation reached after {N} sources, {M} unique findings"

## CRAAP+ Scoring Framework

Multi-dimensional source evaluation:

| Dimension | Weight | Scoring |
|-----------|--------|---------|
| **Currency** | 20% | <3mo: 100, 3-12mo: 70, 1-2y: 40, >2y: 10 |
| **Relevance** | 25% | Direct: 100, Related: 70, Tangential: 30 |
| **Authority** | 25% | T1: 100, T2: 85, T3: 70, T4: 50, T5: 30 |
| **Accuracy** | 20% | Cross-verified: 100, Single: 60, Unverified: 30 |
| **Purpose** | 10% | Educational: 100, Info: 80, Commercial: 40 |

**Final Score = Σ(dimension × weight)**

| Quality Band | Score | Usage |
|--------------|-------|-------|
| ⭐⭐⭐ Primary | 85-100 | Core evidence |
| ⭐⭐ Supporting | 70-84 | Supplementary |
| ⭐ Supplementary | 50-69 | Background only |
| ⚠️ Caution | <50 | **REPLACE** |

## Contradiction Resolution

When contradictions detected:

### Step 1: Classify Type

| Type | Example | Resolution |
|------|---------|------------|
| **Version-based** | "Use X" vs "X deprecated" | Newer wins |
| **Context-based** | "Always X" vs "Never X" | Identify contexts |
| **Opinion-based** | Expert A vs B | Weight by authority |
| **Factual error** | One source wrong | Cross-verify T1 |

### Step 2: Resolution Hierarchy

1. Official docs (T1) override all
2. Newer source wins (if both T1-T2)
3. Higher engagement wins (if same tier/date)
4. Note as "Unresolved - context dependent"

### Step 3: Report Format

```
⚠️ RESOLVED CONTRADICTION
Claim A: "{claim}" ({source} {date})
Claim B: "{claim}" ({source} {date})
Resolution: {A|B} wins - {reason}
Context: {when other might apply}
```

## Knowledge Gap Detection

After research, explicitly identify:

| Gap Type | Question | Report As |
|----------|----------|-----------|
| **Unanswered** | Which sub-questions remain? | "No sources addressed {X}" |
| **Edge cases** | What scenarios not covered? | "Limited info on {Y}" |
| **Limitations** | When might this not apply? | "May not apply to {Z}" |

## Flow

### Phase 1: Query Understanding
1. Parse user query for key concepts
2. Detect current date context
3. Identify technology/framework
4. Extract comparison intent (A vs B)
5. Determine scope: factual, opinion, best-practice, troubleshooting

### Phase 2: Multi-Source Search
Execute parallel searches:

| Category | Sources | Strategy |
|----------|---------|----------|
| Official | Docs, GitHub, RFCs | `site:` operator + exact terms |
| Discussion | GitHub Issues | Problem context, edge cases |
| Articles | Medium, Dev.to | Best practices, tutorials |
| Q&A | Stack Overflow, Reddit | Real-world problems |
| Local | Project codebase | Existing implementations |

### Phase 3: Source Scoring
For each source:
1. Determine base tier (T1-T6)
2. Apply dynamic modifiers
3. Calculate final score (0-100)
4. Extract key claims
5. Note publication date

### Phase 4: Contradiction Detection
1. Identify conflicting claims
2. Map contradictions with scores
3. Analyze why (version, context, outdated)
4. Resolve or note unresolved

### Phase 5: AI Synthesis
Generate recommendation based on:
- Weighted consensus from high-tier sources
- Contradiction resolution
- Freshness priority
- Context applicability

## Special Modes

### Local Mode (`--local`)
Search within current codebase only:
- Find existing implementations
- Discover patterns in use
- Check if already solved locally

### Changelog Mode (`--changelog`)
Focus on breaking changes and migrations:
- Official release notes
- Migration guides
- Upgrade paths
- Deprecation notices

### Security Mode (`--security`)
Focus on security advisories:
- CVE databases
- Security advisories
- Vulnerability disclosures
- Patch availability

### Dependency Mode (`--dependency`)
Focus on package version research:
- Registry version queries (pypi, npm, crates.io, etc.)
- Breaking change detection
- Migration guide discovery
- CVE checks for specific versions

### Comparison Mode (`--compare`)
When query contains "vs", "or", "compared to":
- Side-by-side comparison
- Per-aspect winner
- Overall verdict

### Troubleshooting Mode
Auto-detected when query contains "error", "not working", "fix":
- GitHub Issues priority
- Stack Overflow solutions
- Known bugs in release notes

## Output Format

```
┌─ EXECUTIVE SUMMARY ─────────────────────────────────────────┐
│ Query: {question}                                            │
│ Confidence: {HIGH|MEDIUM|LOW} ({%}) | Saturation: {✓|○}     │
│ Sources: {N} analyzed | {M} high-quality | {K} replaced     │
├─────────────────────────────────────────────────────────────┤
│ TL;DR: {One sentence definitive answer}                      │
└─────────────────────────────────────────────────────────────┘

┌─ EVIDENCE HIERARCHY ────────────────────────────────────────┐
│ ⭐⭐⭐ PRIMARY EVIDENCE (Score 85+)                           │
│ • {Finding} [source] [CRAAP: {score}] [{date}]               │
│ • {Finding} [source] [CRAAP: {score}] [{date}]               │
├─────────────────────────────────────────────────────────────┤
│ ⭐⭐ SUPPORTING EVIDENCE (Score 70-84)                        │
│ • {Finding} [source] [CRAAP: {score}] [{date}]               │
├─────────────────────────────────────────────────────────────┤
│ ⚠️ CONTRADICTIONS RESOLVED                                   │
│ • {Claim A} vs {Claim B} → {Winner}: {reason}                │
├─────────────────────────────────────────────────────────────┤
│ ❓ KNOWLEDGE GAPS                                            │
│ • No sources addressed: {topic}                              │
│ • Limited information on: {topic} (only {N} T4+ sources)     │
└─────────────────────────────────────────────────────────────┘

┌─ ACTIONABLE RECOMMENDATION ─────────────────────────────────┐
│ ✅ DO: {specific action with confidence}                     │
│ ❌ DON'T: {what to avoid and why}                            │
│ 🤔 CONSIDER: {context-dependent alternatives}                │
│                                                              │
│ Caveats: {when this recommendation doesn't apply}           │
│ Next Steps: {if user needs deeper research}                  │
└─────────────────────────────────────────────────────────────┘

┌─ SOURCE CITATIONS ──────────────────────────────────────────┐
│ [1] {title} | {url}                                          │
│     T{tier} | CRAAP: {score} | {date} | {quality_band}       │
│ [2] ...                                                      │
└─────────────────────────────────────────────────────────────┘

┌─ RESEARCH METADATA ─────────────────────────────────────────┐
│ Iterations: {N} | Sources discarded: {M} | Saturation: {Y/N}│
│ Search strategy: {keywords used}                             │
│ Time context: Research valid as of {date}                    │
└─────────────────────────────────────────────────────────────┘
```

## Flags

| Flag | Effect |
|------|--------|
| `--quick` | T1-T2 only, 5 sources max |
| `--standard` | T1-T4, 10 sources (default) |
| `--deep` | All tiers, 20+ sources |
| `--local` | Search in codebase only |
| `--changelog` | Focus on breaking changes |
| `--security` | Focus on CVEs and advisories |
| `--dependency` | Package version and breaking change research |
| `--compare` | A vs B comparison mode |
| `--focus=official` | Only T1-T2 sources |
| `--focus=community` | Include T4-T5 sources |
| `--json` | JSON output |
| `--sources-only` | List sources without synthesis |

## Usage

```bash
/cco-research "React 19 server components"
/cco-research "Python async best practices" --deep
/cco-research "Bun vs Node.js" --compare
/cco-research "TypeScript 5.3 features" --focus=official
/cco-research "log4j vulnerability" --security
/cco-research "config parsing" --local
/cco-research "Next.js 14 migration" --changelog
```

## Related Commands

- `/cco-optimize --security` - For security checks
- `/cco-review` - For architecture decisions

---

## Behavior Rules

### User Input [CRITICAL]

- **AskUserQuestion**: ALL user decisions MUST use this tool
- **Separator**: Use semicolon (`;`) to separate options
- **Prohibited**: Never use plain text questions ("Would you like...", "Should I...")

### Source Reliability

| Tier | Sources | Weight |
|------|---------|--------|
| T1 | Official docs | 1.0 |
| T2 | GitHub repos | 0.9 |
| T3 | Stack Overflow | 0.7 |
| T4 | Blog posts | 0.5 |
| T5 | Forums | 0.3 |

### Quick Mode

When `--quick` flag:
- **No-Questions**: Use smart defaults
- **T1-T2 Only**: Skip lower tier sources
- **Brief-Output**: Summary only

### Task Tracking

- **Create**: TODO list with research phases
- **Status**: pending → in_progress → completed
- **Accounting**: sources + findings = total
