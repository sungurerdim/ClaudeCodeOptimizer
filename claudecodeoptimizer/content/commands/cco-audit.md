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

## Fix Behavior

**Safe (auto-apply):**
- Parameterize SQL queries
- Remove unused imports/code
- Move secrets to env vars
- Fix linting issues

**Risky (approval via AskUserQuestion):**
- Auth/CSRF changes
- DB schema changes
- API contract changes
- Self-compliance fixes (may need design decision)

## Priority Scoring

Each issue gets priority based on impact/effort ratio:
- **HIGH** - High impact, low effort (fix first)
- **MED** - Balanced
- **LOW** - Low impact or high effort

Output sorted by priority, grouped by category.

## Verification

After fixes: done + skip + fail + cannot_do = total

## Usage

```bash
/cco-audit --smart
/cco-audit --self-compliance
/cco-audit --critical --auto-fix
```
