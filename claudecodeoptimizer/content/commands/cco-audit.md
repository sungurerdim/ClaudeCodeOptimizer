---
name: cco-audit
description: Standardized quality gates with prioritized fixes
requires: detection
---

# /cco-audit

**Quality gates** - Detect stack → run standardized checks → prioritize → offer fixes.

## Pre-Operation Safety

Before starting:
1. Check `git status` for uncommitted changes
2. If dirty, AskUserQuestion: → Commit first (cco-commit) / Stash / Continue anyway
3. This ensures safe rollback if needed

## Project Context

**Run context check first:** See `/cco-context`

Context calibrates quality gate thresholds and issue prioritization.

## Flow

1. **Detect** - Identify stack, filter applicable checks
2. **Extract Rules** - Find project docs, extract stated principles/rules
3. **Scan** - Run checks including self-compliance
4. **Report** - Scores, issues with file:line, priority
5. **Fix** - Offer fixes via AskUserQuestion

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

Detect project documentation:
- README.md, CLAUDE.md, CONTRIBUTING.md
- docs/, .github/, pyproject.toml, package.json

Extract stated:
- Principles, goals, design decisions
- Rules, standards, constraints
- Required patterns, forbidden patterns

Check all files against extracted rules:
- Code matches stated principles?
- No violations of stated rules?
- Missing implementations of stated features?
- Excess/unused code vs stated scope?

Report as: `[SELF-COMPLIANCE] <rule> violated in <file:line>`

## SSOT Resolution

When mismatches found, AskUserQuestion for Single Source of Truth:

**SSOT=docs** - Align code to documentation
- Code is wrong, docs are right
- Update code to match stated rules

**SSOT=code** - Align documentation to code
- Code is right, docs are outdated
- Update docs to match actual implementation

**SSOT=discuss** - Need to decide
- Show both sides, ask user to choose direction

## Meta-flags

- `--smart` - Auto-detect and run applicable (includes self-compliance)
- `--critical` - security + ai-security + database + tests
- `--weekly` - security + tech-debt + hygiene + tests + self-compliance
- `--pre-release` - security + api-contract + docs + tests
- `--all` - Everything applicable
- `--auto-fix` - Skip asking, auto-fix safe issues

## Priority Scoring

Each issue gets priority based on impact/effort ratio:
- **CRITICAL** - Security vulnerabilities, data exposure (fix immediately)
- **HIGH** - High impact, low effort (fix first)
- **MEDIUM** - Balanced impact/effort
- **LOW** - Low impact or high effort (fix if time permits)

Output sorted by priority, grouped by category.

## Fix Approval Process

After analysis, present all issues in a **single AskUserQuestion call** with up to 4 questions (one per priority level). This provides granular control without multiple interruptions:

```
AskUserQuestion (single call, multiple questions):

Question 1 - header: "Critical"
"Found X critical issues. Which to fix?"
multiSelect=true
- "All" (first option per CCO rules)
- Individual critical issues...

Question 2 - header: "High"
"Found X high priority issues. Which to fix?"
multiSelect=true
- "All"
- Individual high issues...

Question 3 - header: "Medium"
"Found X medium priority issues. Which to fix?"
multiSelect=true
- "All"
- Individual medium issues...

Question 4 - header: "Low"
"Found X low priority issues. Which to fix?"
multiSelect=true
- "All"
- Individual low issues...
```

**Rules:**
- Only include questions for priority levels that have issues
- Skip empty priority levels (don't ask about priorities with 0 issues)
- If only 1 priority level has issues, use single question
- Max 4 options per question - group if needed ("5 more medium issues...")

## Fix Behavior

**Safe (auto-apply with --auto-fix):**
- Parameterize SQL queries
- Remove unused imports/code
- Move secrets to env vars
- Fix linting issues

**Risky (always require approval):**
- Auth/CSRF changes
- DB schema changes
- API contract changes
- Self-compliance fixes (may need design decision)

## Verification

After fixes: done + skip + fail + cannot_do = total

## Usage

```bash
/cco-audit --smart
/cco-audit --self-compliance
/cco-audit --critical --auto-fix
```
