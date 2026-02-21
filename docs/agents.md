# CCO Agents

Specialized subagents for analysis, fixes, and research.

---

## Overview

| Agent | Purpose | Model | Isolation | Tools |
|-------|---------|-------|-----------|-------|
| **cco-agent-analyze** | Codebase analysis with severity scoring | Haiku | worktree | Glob, Read, Grep, Bash |
| **cco-agent-apply** | Verified write operations + accounting | Inherited | — | Grep, Read, Glob, Bash, Edit, Write, NotebookEdit, AskUserQuestion |
| **cco-agent-research** | Multi-source research with CRAAP+ scoring | Haiku | — | WebSearch, WebFetch, Read, Grep, Glob |

**Model rationale:** Haiku for read-only agents (fast, cost-effective). Apply agent inherits the session model (matches user's quality/cost tradeoff). Agent models are specified in frontmatter.

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

Read-only analysis agent with `isolation: worktree`. Runs on an isolated git worktree snapshot, preventing interference between parallel agents and the working directory. Returns structured JSON with findings, scores, and metrics.

- **9 optimize scopes** (97 checks): security, hygiene, types, performance, ai-hygiene, robustness, privacy, doc-sync, simplify
- **8 review scopes** (92 checks): architecture, patterns, cross-cutting, testing, maintainability, ai-architecture, functional-completeness, production-readiness
- **4 audit scopes** (40 checks): stack-assessment, dependency-health, dx-quality, project-structure
- Platform filtering, skip patterns, false positive handling
- Per CCO Rules: Confidence Scoring, Severity Levels, Skip Patterns

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
