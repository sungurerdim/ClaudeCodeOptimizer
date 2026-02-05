# CCO Commands

All CCO slash commands with flags, scopes, and examples.

---

## Quick Reference

| Command | Purpose | Model | Key Flags |
|---------|---------|-------|-----------|
| `/cco-optimize` | Fix code issues | Opus | `--auto`, `--preview`, `--scope=X` |
| `/cco-align` | Architecture gaps | Opus | `--auto`, `--preview` |
| `/cco-commit` | Quality-gated commits | Opus | `--preview`, `--single`, `--staged-only` |
| `/cco-research` | Multi-source research | Opus | `--quick`, `--deep` |
| `/cco-preflight` | Pre-release checks | Opus | `--auto`, `--preview` |
| `/cco-docs` | Documentation gaps | Opus | `--auto`, `--preview`, `--scope=X`, `--update` |
| `/cco-update` | Update CCO | Opus | `--auto`, `--check` |

**Model Rationale:** Opus for coding commands (fewer errors), Haiku for analysis agents (fast).

---

## /cco-optimize

Fix security, quality, and hygiene issues.

```bash
/cco-optimize                      # Interactive selection
/cco-optimize --scope=security     # Security focus only
/cco-optimize --preview            # Report only, no fixes
/cco-optimize --auto               # Unattended: fix all, no questions
```

### Scopes (9 scopes, 97 checks)

| Scope | Checks |
|-------|--------|
| Security | OWASP, secrets, CVEs, input validation |
| Hygiene | Orphans, stale refs, duplicates |
| Types | Type annotations, mypy/pyright errors |
| Performance | N+1, blocking I/O, missing caching |
| AI-Hygiene | Hallucinated APIs, orphan abstractions |
| Robustness | Timeouts, retries, validation |
| Privacy | PII exposure, data masking, consent |
| Doc-Sync | README outdated, comment-code drift |
| Simplify | Nested conditionals, god functions |

### Flow

Setup → Analyze (parallel scopes) → Plan Review → Apply → Summary

---

## /cco-align

Strategic architecture analysis — current vs ideal state.

```bash
/cco-align                         # Full review
/cco-align --preview               # Analyze only, show gaps
/cco-align --auto                  # Unattended mode
```

### Scopes (6 scopes, 77 checks)

| Scope | Focus |
|-------|-------|
| Architecture | Coupling, cohesion, layers, dependencies |
| Patterns | SOLID, DRY, design patterns, consistency |
| Testing | Coverage, quality, gaps |
| Maintainability | Complexity, readability, naming |
| AI-Architecture | Over-engineering, drift, premature abstraction |
| Functional-Completeness | CRUD, pagination, edge cases, validation |

### Gap Analysis

| Type | Coupling | Cohesion | Complexity | Coverage |
|------|----------|----------|------------|----------|
| CLI | <40% | >75% | <10 | 70%+ |
| Library | <30% | >80% | <8 | 85%+ |
| API | <50% | >70% | <12 | 80%+ |
| Web | <60% | >65% | <15 | 70%+ |

---

## /cco-commit

Quality-gated atomic commits.

```bash
/cco-commit                 # Full flow
/cco-commit --preview       # Show plan without committing
/cco-commit --single        # One commit for all
/cco-commit --staged-only   # Only staged changes
```

### Quality Gates (Parallel)

| Gate | Action |
|------|--------|
| Secrets | Block if found |
| Large Files | Warn >1MB, Block >10MB |
| Format | Auto-fix, re-stage |
| Lint | Stop on unfixable |
| Types | Stop on failure |
| Tests | Stop on failure |

### Commit Format

```
{type}({scope}): {title}  (max 50 chars total)

{body}

Co-Authored-By: Claude <noreply@anthropic.com>
```

---

## /cco-research

Multi-source research with reliability scoring.

```bash
/cco-research "query"               # Standard research
/cco-research "query" --quick       # T1-T2 only
/cco-research "query" --deep        # All tiers, 20+ sources
```

### Source Tiers

| Tier | Score | Sources |
|------|-------|---------|
| T1 | 90-100 | Official docs, specs |
| T2 | 80-90 | GitHub, changelogs |
| T3 | 70-80 | Major blogs, tutorials |
| T4 | 60-70 | Stack Overflow, forums |
| T5 | 50-60 | Personal blogs |
| T6 | Skip | Unknown/unverified |

---

## /cco-preflight

Pre-release verification gate.

```bash
/cco-preflight              # Full release workflow
/cco-preflight --auto       # Unattended checks
/cco-preflight --preview    # Check without releasing
```

### Checks (14 total)

**Blockers:** Dirty git, version mismatch, tests fail, build fail, type errors, security CVE

**Warnings:** Wrong branch, TODO markers, lint warnings, outdated deps

---

## /cco-docs

Documentation gap analysis and generation.

```bash
/cco-docs                    # Interactive selection
/cco-docs --auto             # Generate all missing docs
/cco-docs --preview          # Show gaps only
/cco-docs --scope=readme     # Single scope
/cco-docs --update           # Regenerate existing
```

### Scopes

| Scope | Purpose |
|-------|---------|
| readme | Project overview |
| api | API reference |
| dev | Developer onboarding |
| user | End-user guides |
| ops | Deployment, operations |
| changelog | Version history |
| refine | Quality improvement |
| verify | Claims vs source code |

---

## /cco-update

Update CCO to the latest version.

```bash
/cco-update             # Check and upgrade interactively
/cco-update --check     # Version check only
/cco-update --auto      # Silent upgrade
```

---

## Common Patterns

### Unattended Mode

```bash
/cco-optimize --auto    # Exit 0=OK, 1=WARN, 2=FAIL
/cco-align --auto       # Same exit codes
/cco-preflight --auto   # Same exit codes
```

### Accounting

All operations report: `Applied: N | Failed: M | Needs Approval: D | Total: N+M+D`

Formula: `applied + failed + needs_approval = total` (no silent skips)

### Recovery

| Situation | Command |
|-----------|---------|
| Revert file | `git checkout -- {file}` |
| Revert all | `git checkout .` |
| Review changes | `git diff` |
| Undo commit | `git reset --soft HEAD~1` |

---

*Back to [README](../README.md)*
