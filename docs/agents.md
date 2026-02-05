# CCO Agents

Specialized subagents for analysis, fixes, and research.

---

## Overview

| Agent | Purpose | Model | Tools |
|-------|---------|-------|-------|
| **cco-agent-analyze** | Codebase analysis with severity scoring | Haiku | Glob, Read, Grep, Bash |
| **cco-agent-apply** | Verified write operations + accounting | Opus | Grep, Read, Glob, Bash, Edit, Write, NotebookEdit, AskUserQuestion |
| **cco-agent-research** | Multi-source research with CRAAP+ scoring | Haiku | WebSearch, WebFetch, Read, Grep, Glob |

**Model Rationale:** Haiku for read-only agents (fast, cost-effective). Opus for apply agent (fewer tool errors, coding accuracy).

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

Read-only analysis agent. Returns structured JSON with findings, scores, and metrics.

- **15 optimize scopes** (97 checks): security, hygiene, types, performance, ai-hygiene, robustness, privacy, doc-sync, simplify
- **6 review scopes** (77 checks): architecture, patterns, testing, maintainability, ai-architecture, functional-completeness
- Platform filtering, skip patterns, false positive handling
- Confidence threshold ≥80

## cco-agent-apply

Write agent. Applies fixes with verification and cascade handling.

- Batch edits with parallel execution
- Post-change verification (lint/type/test)
- Cascade fixing (max 3 iterations)
- Accounting: `applied + failed + needs_approval = total`
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

## Agent Selection by Command

| Command | Analyze | Apply | Research |
|---------|---------|-------|----------|
| `/cco-optimize` | security, hygiene, types, etc. | Yes | dependency |
| `/cco-align` | architecture, patterns, etc. | Yes | dependency |
| `/cco-commit` | (quality gates only) | No | No |
| `/cco-research` | - | No | full |
| `/cco-preflight` | (orchestrates optimize + align) | (orchestrates) | dependency |
| `/cco-docs` | docs scope | Yes | No |
| `/cco-update` | - | No | No |

---

*Back to [README](../README.md)*
