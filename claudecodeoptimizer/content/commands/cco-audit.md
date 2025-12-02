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
- `--consistency` - Doc-code mismatch detection (features, APIs, configs, behaviors)

**Stack-dependent (auto-skip if not applicable):**
- `--tests` - Coverage, isolation, flaky
- `--database` - N+1, indexes, queries
- `--performance` - Caching, algorithms
- `--ai-security` - Prompt injection, PII exposure
- `--ai-quality` - Hallucinated APIs, AI patterns
- `--docs` - Docstrings, API docs
- `--cicd` - Pipeline, quality gates
- `--containers` - Dockerfile, K8s
- `--supply-chain` - Dependency CVEs
- `--compliance` - GDPR, licenses
- `--api-contract` - Breaking changes

## Self-Compliance Check

Detect project documentation (README.md, CLAUDE.md, CONTRIBUTING.md, docs/).

Extract stated: Principles, goals, rules, constraints, required/forbidden patterns.

Check all files against extracted rules. Report as: `[SELF-COMPLIANCE] <rule> violated in <file:line>`

## Doc-Code Mismatch Detection

### Mismatch Categories

| Category | Doc Source | Code Source | Example |
|----------|------------|-------------|---------|
| **Feature Claims** | README features list | Actual implementation | "Supports X" but X not implemented |
| **API Signatures** | OpenAPI/JSDoc/docstrings | Function signatures | Param types/names differ |
| **Config Values** | README/docs defaults | Actual defaults in code | "Default: 100" but code uses 50 |
| **Behavior Descriptions** | Comments/docs | Actual logic | "Returns null on error" but throws |
| **Examples/Samples** | README code blocks | Working code | Example uses deprecated API |
| **Dependencies** | README requirements | package.json/pyproject | Version mismatches |

### Detection Flow

1. **Extract Claims** - Parse docs for: features, API signatures, defaults, behaviors
2. **Map to Code** - Find corresponding implementations
3. **Compare** - Semantic comparison (not just string match)
4. **Report** - `[DOC-CODE MISMATCH] {category}: {doc_claim} ≠ {code_reality} in {file:line}`

## SSOT Resolution

For each mismatch, AskUserQuestion:

```
header: "SSOT: {category}"
question: "{doc_claim} ≠ {code_reality} — Which is correct?"
options:
  - Docs: "Update code to match documentation"
  - Code: "Update documentation to match code"
  - Discuss: "Need to decide the intended behavior"
```

Group related mismatches when possible (e.g., all API signature mismatches in one question).

## Meta-flags

- `--smart` - Auto-detect and run applicable (includes self-compliance + consistency)
- `--critical` - security + ai-security + database + tests
- `--weekly` - security + tech-debt + hygiene + tests + self-compliance + consistency
- `--pre-release` - security + api-contract + docs + tests + consistency
- `--all` - Everything applicable
- `--auto-fix` - Skip asking, auto-fix safe issues

## Priority Scoring

- **CRITICAL** - Security vulnerabilities, data exposure (fix immediately)
- **HIGH** - High impact, low effort (fix first)
- **MEDIUM** - Balanced impact/effort
- **LOW** - Low impact or high effort (fix if time permits)

## Output

**Standards:** Output Formatting

Tables:
1. **Audit Results** - Category | Score | Bar + Summary (per category + OVERALL)
2. **Issues Found** - Priority | Issue | Location | Status (grouped by CRITICAL/HIGH/MEDIUM/LOW)
3. **Verification** - Inline: {done} done + {skip} skip + {fail} fail = {total}

## Usage

```bash
/cco-audit                   # Interactive: ask scope + auto-fix
/cco-audit --smart           # Auto-detect applicable (includes consistency)
/cco-audit --consistency     # Doc-code mismatch detection
/cco-audit --self-compliance # Check against project's own rules
/cco-audit --critical --auto-fix
```
