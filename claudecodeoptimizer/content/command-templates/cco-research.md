---
name: cco-research
description: Multi-source research with reliability scoring
allowed-tools: WebSearch(*), WebFetch(*), Read(*), Grep(*), Glob(*), Task(*), TodoWrite
---

# /cco-research

**Smart Research** - Search → score → synthesize → recommend.

End-to-end: Searches multiple sources, scores reliability, synthesizes findings.

**Rules:** User Input | Source Reliability | Quick Mode | Progress Tracking

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

## Progress Tracking [CRITICAL]

**Use TodoWrite to track progress.** Create todo list at start, update status for each phase.

```
TodoWrite([
  { content: "Search sources", status: "in_progress", activeForm: "Searching sources" },
  { content: "Score reliability", status: "pending", activeForm: "Scoring reliability" },
  { content: "Detect contradictions", status: "pending", activeForm: "Detecting contradictions" },
  { content: "Synthesize findings", status: "pending", activeForm: "Synthesizing findings" },
  { content: "Generate recommendation", status: "pending", activeForm: "Generating recommendation" }
])
```

**Update status:** Mark `completed` immediately after each phase finishes, mark next `in_progress`.

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

When called without query → **AskUserQuestion** (mandatory):

| Question | Options | MultiSelect |
|----------|---------|-------------|
| Depth? | Standard (Recommended); Quick; Deep | false |

*Research topic: free text via AskUserQuestion.*

Explicit flags skip questions.

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

*Analysis/scoring rules in cco-agent-research. Orchestration rules here.*

### Quick Mode

When `--quick` flag:
- **No-Questions**: Use smart defaults
- **T1-T2 Only**: Skip lower tier sources
- **Brief-Output**: Summary only

### Progress Tracking

*Use TodoWrite for research phases: search → analyze → synthesize.*
