---
name: cco-audit
description: Standardized quality gates with prioritized fixes
---

# /cco-audit

**Quality gates** - Read context → run applicable checks → prioritize → offer fixes.

**Standards:** Pre-Operation Safety | Context Read | Approval Flow | Safety Classification | Verification | Error Format

## Context Application
- **Guidelines** - Follow listed guidelines
- **Applicable** - Only run applicable checks
- **Data** - If PII/Regulated → prioritize security issues higher
- **Scale** - If 10K+ → prioritize performance issues higher
- **Priority** - If Speed → focus on critical only; if Quality → flag all issues
- **Maturity** - If Legacy → conservative fixes; if Greenfield → can suggest restructuring

## Default Behavior

When called without flags, AskUserQuestion:

```
header: "Scope"
question: "What scope to audit?"
options:
  - Quick: "{base_description} {labels}"
  - Smart: "{base_description} {labels}" [recommended]
  - Full: "{base_description} {labels}"

header: "Auto-fix"
question: "Auto-fix safe issues?"
options:
  - Yes: "{base_description} {labels}" [recommended]
  - No: "{base_description} {labels}"
```

Explicit flags (`--smart`, `--security`, etc.) skip these questions.

## Flow

1. **Read Context** - Get applicable checks from Operational section
2. **Extract Rules** - Find project docs, extract stated principles/rules
3. **Scan** - Run checks including self-compliance
4. **Report** - Scores, issues with file:line, priority
5. **Fix** - Offer fixes via approval flow

## Categories

**Core (always run):**
- `--security` - OWASP, secrets, CVEs
- `--tech-debt` - Dead code, complexity, duplication
- `--hygiene` - Old TODOs, orphans, hardcoded values
- `--self-compliance` - Check against project's own stated rules

**Stack-dependent (auto-skip if not applicable):**
- `--ai-security` - Prompt injection, PII exposure
- `--ai-quality` - Hallucinated APIs, AI patterns
- `--database` - N+1, indexes, queries
- `--tests` - Coverage, isolation, flaky
- `--performance` - Caching, algorithms
- `--docs` - Docstrings, API docs
- `--cicd` - Pipeline, quality gates
- `--containers` - Dockerfile, K8s
- `--supply-chain` - Dependency CVEs
- `--dora` - Deploy frequency, lead time, MTTR
- `--compliance` - GDPR, licenses
- `--api-contract` - Breaking changes

## Self-Compliance Check

Detect project documentation (README.md, CLAUDE.md, CONTRIBUTING.md, docs/).

Extract stated: Principles, goals, rules, constraints, required/forbidden patterns.

Check all files against extracted rules. Report as: `[SELF-COMPLIANCE] <rule> violated in <file:line>`

## SSOT Resolution

When mismatches found, AskUserQuestion for Single Source of Truth:
- **SSOT=docs** - Align code to documentation
- **SSOT=code** - Align documentation to code
- **SSOT=discuss** - Need to decide

## Meta-flags

- `--smart` - Auto-detect and run applicable (includes self-compliance)
- `--critical` - security + ai-security + database + tests
- `--weekly` - security + tech-debt + hygiene + tests + self-compliance
- `--pre-release` - security + api-contract + docs + tests
- `--all` - Everything applicable
- `--auto-fix` - Skip asking, auto-fix safe issues

## Priority Scoring

- **CRITICAL** - Security vulnerabilities, data exposure (fix immediately)
- **HIGH** - High impact, low effort (fix first)
- **MEDIUM** - Balanced impact/effort
- **LOW** - Low impact or high effort (fix if time permits)

## Verification

After fixes: done + skip + fail + cannot_do = total

## Usage

```bash
/cco-audit                   # Interactive: ask scope + auto-fix
/cco-audit --smart           # Auto-detect applicable
/cco-audit --self-compliance # Check against project's own rules
/cco-audit --critical --auto-fix
```
