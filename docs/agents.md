# CCO Agents

Specialized subagents for analysis, fixes, and research.

---

## Overview

| Agent | Purpose | Model | Isolation | Tools |
|-------|---------|-------|-----------|-------|
| **cco-agent-analyze** | Codebase analysis with severity scoring | Haiku/Sonnet/Opus* | — | Glob, Read, Grep, Bash |
| **cco-agent-apply** | Verified write operations + accounting | Inherited | — | Grep, Read, Glob, Bash, Edit, Write, NotebookEdit, AskUserQuestion |
| **cco-agent-research** | Multi-source research with CRAAP+ scoring | Haiku | — | WebSearch, WebFetch, Read, Grep, Glob |

**Model rationale:** Per CCO Rules: Model Routing. Agent frontmatter defaults to Haiku. Skills override via Task tool's `model` parameter: auto → Haiku, review → Sonnet, CRITICAL escalation → Opus. Apply agent inherits the session model.

## When to Use

```
Need information?
├── Single URL/fact → WebSearch/WebFetch
└── Multiple sources/verification → cco-agent-research

Need analysis?
├── Find file/pattern → Glob/Grep/Read
└── Structured findings/metrics → cco-agent-analyze

Need changes?
├── Single file edit → Edit/Write
└── Multiple files/verification → cco-agent-apply
```

---

## cco-agent-analyze

Read-only analysis agent. Returns structured JSON with findings, scores, and metrics. No worktree isolation — read-only parallel access is safe.

- **9 optimize scopes** (97 checks) — see agents/cco-agent-analyze.md
- **8 review scopes** (92 checks) — see agents/cco-agent-analyze.md
- **4 audit scopes** (40 checks) — see agents/cco-agent-analyze.md
- Context-aware filtering by project type, cross-scope dedup, negative evidence checks
- Standardized score calculation formula (penalty-based with severity caps)
- Per CCO Rules: Confidence Scoring, Severity Levels, Skip Patterns, Fix Quality

## cco-agent-apply

Write agent. Applies fixes with verification and cascade handling.

- Batch edits with parallel execution
- Post-change verification (lint/type/test)
- Cascade fixing (max 3 iterations)
- Per CCO Rules: Accounting, Auto Mode
- Educational output (why/avoid/prefer)
- Docs scope for documentation generation

## cco-agent-research

Research agent. Multi-source with CRAAP+ reliability scoring.

- 6 scopes: local, search, analyze, synthesize, full, dependency
- T1-T6 source tiers with modifiers
- Contradiction detection and resolution
- Saturation detection (auto-stop)
- Dependency mode with registry API integration

---

## Agent Selection by Skill

| Skill | Analyze | Apply | Research |
|-------|---------|-------|----------|
| `/cco-optimize` | security, hygiene, types, etc. | Yes | dependency |
| `/cco-align` | architecture, patterns, etc. | Yes | dependency |
| `/cco-commit` | (quality gates only) | No | No |
| `/cco-research` | - | No | full |
| `/cco-docs` | docs scope | Yes | No |
| `/cco-blueprint` | all scopes (optimize + review + audit) | Yes | No |
| `/cco-pr` | - | No | No |
| `/cco-update` | - | No | No |

---

*Back to [README](../README.md)*
