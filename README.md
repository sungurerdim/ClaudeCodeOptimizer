# ClaudeCodeOptimizer

Project-aware commands for Claude Code.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## What is CCO?

CCO is a **process orchestration and quality standards** tool for Claude Code. It provides consistent quality gates, verified change management, and measurable efficiency improvements.

**Covers 25 pain points from 2025 developer surveys:**

| Category | Issues |
|----------|--------|
| Security | OWASP vulnerabilities, secret exposure, dependency CVEs |
| AI Code | Hallucinated APIs, prompt injection, PII exposure |
| Quality | Dead code, complexity, duplication, missing tests |
| Database | N+1 queries, missing indexes, query optimization |
| Operations | DORA metrics, CI/CD gaps, container issues |
| Maintenance | Old TODOs, orphan files, hardcoded values, API breaking changes |

---

## Installation

```bash
pip install git+https://github.com/sungurerdim/ClaudeCodeOptimizer.git
cco-setup
```

---

## Commands

| Command | Purpose |
|---------|---------|
| `/cco-audit` | **Quality gates** - standardized checks, prioritized fixes |
| `/cco-generate` | **Generation** - convention-following, verified |
| `/cco-health` | **Visibility** - actionable metrics dashboard |
| `/cco-refactor` | **Risk mitigation** - verified transformations |
| `/cco-optimize` | **Efficiency** - measurable improvements |
| `/cco-commit` | **Change management** - atomic, traceable commits |
| `/cco-config` | **Settings** - statusline, permissions (global/local) |
| `/cco-status` | Installation check |
| `/cco-help` | Command reference |

---

## Usage Examples

**Find and fix issues:**
```bash
/cco-audit --smart              # Auto-detect stack, find issues, offer fixes
/cco-audit --security --auto-fix  # Auto-fix safe security issues
/cco-audit --critical           # security + ai-security + database + tests
```

**Generate missing components:**
```bash
/cco-generate --tests           # Unit/integration tests
/cco-generate --openapi         # API documentation
/cco-generate --cicd            # CI/CD pipelines
```

**Safe refactoring:**
```bash
/cco-refactor rename oldName newName
```
Finds ALL references, updates in order, verifies with grep.

**Optimize context:**
```bash
/cco-optimize --context         # Reduce CLAUDE.md tokens
/cco-optimize --code-quality    # Remove dead code, unused imports
```

**Configure settings:**
```bash
/cco-config                     # Interactive (scope, statusline, permissions)
/cco-config --global            # Apply to all projects (~/.claude/)
/cco-config --local             # This project only (./.claude/)
```

---

## Audit Categories

| Flag | Checks |
|------|--------|
| `--security` | OWASP, secrets, CVEs |
| `--ai-security` | Prompt injection, PII |
| `--ai-quality` | Hallucinated APIs, AI patterns |
| `--database` | N+1, indexes, queries |
| `--tests` | Coverage, isolation, flaky |
| `--tech-debt` | Dead code, complexity |
| `--performance` | Caching, algorithms |
| `--hygiene` | TODOs, orphans, hardcoded |
| `--self-compliance` | Check against project's own stated rules |
| `--dora` | Deploy frequency, MTTR |
| `--compliance` | GDPR, licenses |
| `--api-contract` | Breaking changes |
| `--docs` | Docstrings, API docs |
| `--cicd` | Pipeline, quality gates |
| `--containers` | Dockerfile, K8s |
| `--supply-chain` | Dependency CVEs |

**Meta-flags:** `--smart`, `--critical`, `--weekly`, `--pre-release`, `--all`, `--auto-fix`

---

## Design Principles

CCO provides 9 commands, 3 agents, and rules added to `~/.claude/`.

**Core principles:**
- Perfect UX/DX, maximum efficiency
- Maximum output quality, maximum simplicity
- Zero overengineering, zero overlap with AI capabilities

**What this means:**
- CCO tells AI WHAT, not HOW (Opus 4.5 already knows how)
- Workflow orchestration only (detect → scan → fix)
- Verification patterns only (accounting, grep checks)
- Project-specific context only (conventions, thresholds)

**Key behaviors:**
- Pre-operation safety: offer commit before major changes
- Self-compliance: check code against project's stated rules
- Auto-detects stack, skips non-applicable checks
- Safe fixes auto-apply, risky ones need approval
- Verification: `done + skip + fail + cannot_do = total`
- Reference integrity: find ALL refs → update → verify
- Priority scoring: impact/effort ratio for actionability

---

## Enforced Standards

CCO injects **118 standards across 17 categories** into `CLAUDE.md`:

| Category | What it enforces |
|----------|------------------|
| **Core** | Forward slash paths, find-all-refs before rename, verification accounting |
| **Code Quality** | Cyclomatic <10, tech debt <5%, no orphans, type annotations, SemVer |
| **Security** | Input validation (Pydantic/Zod), Zero Trust auth, secrets rotation, OWASP Top 10 |
| **AI-Assisted** | Treat AI output as junior code, Plan→Act→Review workflow, test before integrate |
| **Architecture** | Async event-driven, dependency injection, circuit breakers, bounded contexts |
| **Operations** | Infrastructure as Code, GitOps deploys, OpenTelemetry observability, feature flags |
| **Testing** | 80% coverage minimum, CI gates before merge, contract testing between services |
| **Performance** | DB indexing, N+1 prevention, cache-aside pattern, async I/O only |
| **Data** | Automated backups with RPO/RTO, versioned migrations, retention policies |
| **API** | RESTful conventions, cursor pagination, OpenAPI docs, consistent error format |
| **Accessibility** | WCAG 2.2 AA compliance, semantic HTML, keyboard navigation, screen reader support |
| **i18n** | UTF-8 everywhere, RTL support, locale-aware formatting, proper pluralization |
| **Reliability** | Chaos engineering, explicit timeouts, exponential backoff, graceful degradation |
| **Cost** | FinOps monitoring, resource tagging, auto-scale to zero, carbon-aware scheduling |
| **Docs** | README structure, OpenAPI specs, Architecture Decision Records, runbooks |
| **DX** | Local-prod parity, fast feedback loops, self-service infra, golden paths |
| **Compliance** | License tracking, SOC2/HIPAA/PCI-DSS controls, data classification |

---

## Structure

After `cco-setup`, the following is added to `~/.claude/`:

```
~/.claude/
├── commands/
│   └── cco-*.md          # 9 slash commands
├── agents/
│   └── cco-*.md          # 3 specialized agents
└── CLAUDE.md             # 118 standards (17 categories)
```

---

## Verification

```bash
cco-status     # Terminal
/cco-status    # Claude Code
```

---

## Uninstallation

```bash
cco-remove
pip uninstall claudecodeoptimizer
```

---

## Requirements

- Python 3.11+
- Claude Code

---

## License

MIT License - see [LICENSE](LICENSE)

---

**Created by Sungur Zahid Erdim** | [Issues](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues)
