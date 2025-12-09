---
name: cco-research
description: Multi-source research with reliability scoring and AI synthesis
allowed-tools: WebSearch(*), WebFetch(*), Read(*), Grep(*), Glob(*), Task(*), TodoWrite
---

# /cco-research

**Smart Research** - Search → score → synthesize → recommend.

End-to-end: Searches multiple sources, scores reliability, synthesizes findings.

**Standards:** Command Flow | User Input | Output Formatting

## Context

- Context check: !`grep -c "CCO_ADAPTIVE_START" ./CLAUDE.md 2>/dev/null || echo "0"`
- Current date: !`date +%Y-%m-%d`

**Static context (Stack, Type, Priority, Data) is read from ./CLAUDE.md already in context.**

## Context Requirement [CRITICAL]

**This command requires CCO_ADAPTIVE in ./CLAUDE.md.**

If context check returns "0":
```
CCO_ADAPTIVE not found in ./CLAUDE.md

Run /cco-tune first to configure project context, then restart CLI.
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
| Depth? | Standard (Recommended), Quick, Deep | false |

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
┌─ RESEARCH REPORT ────────────────────────────────────────────┐
│ Query: {question}                                            │
│ Date: {date} | Sources: {N} | Depth: {mode}                  │
└──────────────────────────────────────────────────────────────┘

┌─ KEY FINDINGS ───────────────────────────────────────────────┐
│ # │ Finding                    │ Score │ Sources │ Fresh     │
├───┼────────────────────────────┼───────┼─────────┼───────────┤
│ 1 │ {main finding}             │ 95    │ T1x2    │ Current   │
│ 2 │ {supporting finding}       │ 82    │ T2,T3   │ Recent    │
└───┴────────────────────────────┴───────┴─────────┴───────────┘

┌─ AI RECOMMENDATION ──────────────────────────────────────────┐
│ Confidence: {HIGH|MEDIUM|LOW} ({%})                          │
├──────────────────────────────────────────────────────────────┤
│ {Synthesized recommendation}                                  │
│                                                               │
│ Caveats: {when this might not apply}                         │
│ Alternatives: {other valid approaches}                        │
└──────────────────────────────────────────────────────────────┘
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

- `/cco-audit --security` - For security checks
- `/cco-review` - For architecture decisions
