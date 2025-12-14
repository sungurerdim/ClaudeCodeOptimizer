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

**Static context (Stack, Type, Priority, Data) from ./CLAUDE.md already in context.**

## Context Requirement [CRITICAL]

If context check returns "0": `CCO context not found. Run /cco-config first.` **Stop immediately.**

## Progress Tracking [CRITICAL]

```
TodoWrite([
  { content: "Research topic", status: "in_progress", activeForm: "Researching topic" },
  { content: "Synthesize findings", status: "pending", activeForm: "Synthesizing findings" },
  { content: "Generate recommendation", status: "pending", activeForm: "Generating recommendation" }
])
```

## Context Application

| Field | Effect |
|-------|--------|
| Stack | Prioritize stack-specific (Python → docs.python.org, JS → MDN) |
| Type | API → API docs; CLI → man pages; Library → README/changelog |
| Priority | Speed → quick; Quality → deep |
| Data | PII/Regulated → include compliance/security |

## Token Efficiency [CRITICAL]

Single research agent │ Parallel fetches │ Targeted extraction │ Early saturation (3×)

## Agent Integration

```
Task(cco-agent-research, mode=full, query="...")
→ Multi-source search → Tiering → Synthesis → Structured recommendation
```

**CRITICAL:** ONE research agent. Never per-source or per-strategy.

**Local Mode (`--local`):** Uses `cco-agent-analyze` with `scope: scan` (codebase-only).

## Default Behavior

| Question | Options | MultiSelect |
|----------|---------|-------------|
| Depth? | Standard (Recommended); Quick; Deep | false |

Explicit flags skip questions.

## Flow

| Phase | Action |
|-------|--------|
| 1. Query | Parse concepts, date, tech/framework, comparison intent |
| 2. Search | Parallel: Official (docs, GitHub) │ Discussion │ Articles │ Q&A │ Local |
| 3. Score | Tier (T1-T6) + modifiers → final score (0-100) + claims + date |
| 4. Contradictions | Identify → Map with scores → Analyze why → Resolve/note |
| 5. Synthesize | Weighted consensus + contradiction resolution + freshness |

## Special Modes

| Mode | Focus |
|------|-------|
| `--local` | Codebase only: existing impl, patterns, local solutions |
| `--changelog` | Breaking changes: release notes, migration, deprecation |
| `--security` | CVEs, advisories, vulnerabilities, patches |
| `--dependency` | Package versions, breaking changes, CVE checks |
| `--compare` | Side-by-side comparison ("vs", "or", "compared to") |
| Troubleshooting | Auto-detect: GitHub Issues, SO, known bugs |

## Output Format

**Sections:** Executive Summary (TL;DR + confidence) → Evidence Hierarchy (Primary 85+ / Supporting 70-84) → Contradictions Resolved → Knowledge Gaps → Actionable Recommendation (DO/DON'T/CONSIDER) → Source Citations → Metadata

## Flags

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
| `--focus=official` | T1-T2 only |
| `--focus=community` | Include T4-T5 |
| `--json` | JSON output |
| `--sources-only` | No synthesis |

## Quick Mode

No questions │ T1-T2 only │ Brief output

## Rules

Use TodoWrite for phases │ Analysis/scoring in cco-agent-research
