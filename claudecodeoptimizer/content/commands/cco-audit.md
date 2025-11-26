---
name: cco-audit
description: Codebase analysis with prioritized findings
categories:
  security: [owasp, xss, sqli, csrf, secrets, cve]
  ai-security: [prompt-injection, pii, llm-security]
  database: [n+1, indexes, queries, connections]
  tests: [coverage, isolation, pyramid]
  tech-debt: [dead-code, complexity, duplication]
  code-quality: [syntax, types, error-handling]
  performance: [caching, algorithms, bottlenecks]
  docs: [docstrings, api-docs, readme]
  cicd: [pipeline, quality-gates, deployment]
  containers: [dockerfile, k8s, security]
  supply-chain: [dependencies, cve, sbom]
meta-flags:
  ai: [ai-security, ai-quality, ai-debt]
  critical: [security, ai-security, database, tests]
  production-ready: [security, performance, database, tests, docs]
---

# /cco-audit

**Find issues in your codebase**

---

## Flow: Confirm → Detect → Scan → Report

### Confirm
Ask user what to audit. Options:
- **Smart**: Auto-detect stack, run top 5-8 checks (recommended)
- **Quick**: Health scores only (~5 min)
- **Category**: Select categories (security, tests, etc.)
- **Full**: All checks

### Detect
1. Identify tech stack (languages, frameworks, databases)
2. Filter applicable checks
3. Report: "{X} checks applicable, {Y} filtered"

### Scan
1. Run checks in parallel by category
2. Stream findings as discovered
3. Track progress with TodoWrite

### Report
1. Summary: score, grade, finding counts
2. Critical issues first (with file:line)
3. Recommendations prioritized
4. Next steps: `/cco-fix --{category}`

---

## Categories

| Category | Checks | Severity |
|----------|--------|----------|
| security | OWASP Top 10, secrets, CVEs | Critical |
| ai-security | Prompt injection, PII | Critical |
| database | N+1, indexes, connections | High |
| tests | Coverage, isolation, pyramid | High |
| tech-debt | Dead code, complexity | Medium |
| code-quality | Types, error handling | Medium |
| performance | Caching, algorithms | Medium |
| docs | Docstrings, API docs | Low |
| cicd | Pipeline, quality gates | Low |
| containers | Dockerfile, K8s | Low |
| supply-chain | CVEs, SBOM | Medium |

---

## Meta-flags

- `--ai` = ai-security + ai-quality + ai-debt
- `--critical` = security + ai-security + database + tests
- `--production-ready` = security + performance + database + tests + docs

---

## Output Format

```markdown
# Audit Results

**Score:** {score}/100 ({grade})
**Findings:** {total} ({critical}C / {high}H / {medium}M / {low}L)

## Critical Issues
1. {file}:{line} - {issue} ({category})
   Fix: {recommendation}

## Scores by Category
| Category | Score | Issues |
|----------|-------|--------|
| security | 85/100 | 2 |

## Recommendations
1. [Immediate] Fix {X} critical issues
2. [Short-term] Address {Y} high priority
3. [Long-term] Improve {Z} coverage

## Next Steps
→ /cco-fix --security
→ /cco-generate --tests
```

---

## Context Passing

After audit, pass context to other commands:

```markdown
CONTEXT FOR /cco-fix:
Audit found {count} {severity} issues:
- {category}: {count}x {issue} ({files})
All fixable with {approach}.
```

---

## Usage

```bash
/cco-audit                    # Interactive
/cco-audit --smart            # Auto-detect, top checks
/cco-audit --quick            # Health scores
/cco-audit --security         # Single category
/cco-audit --security --tests # Multiple categories
/cco-audit --critical         # Meta-flag
/cco-audit --all              # Everything
/cco-audit --security "auth"  # With focus context
```
