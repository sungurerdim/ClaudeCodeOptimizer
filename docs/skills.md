# CCO Skills

All CCO slash commands (skills) with flags, scopes, and examples.

---

## Quick Reference

| Skill | Purpose | Key Flags |
|-------|---------|-----------|
| `/cco-optimize` | Fix code issues | `--auto`, `--preview`, `--scope=X`, `--loop` |
| `/cco-align` | Architecture gaps | `--auto`, `--preview` |
| `/cco-commit` | Quality-gated commits | `--preview`, `--single`, `--staged-only` |
| `/cco-research` | Multi-source research | `--quick`, `--deep` |
| `/cco-docs` | Documentation gaps | `--auto`, `--preview`, `--scope=X`, `--update` |
| `/cco-blueprint` | Project health + memory cleanup | `--auto`, `--preview`, `--init`, `--refresh`, `--scope=X` |
| `/cco-pr` | Release-please PRs | `--auto`, `--no-auto-merge`, `--preview`, `--draft` |
| `/cco-update` | Update CCO | `--auto`, `--check` |

6 skills auto-invoke on natural language. 2 require explicit `/command` invocation (blueprint, update).

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

### Args

| Flag | Description |
|------|-------------|
| `--auto` | Unattended: fix all, no questions |
| `--preview` | Report only, no fixes |
| `--scope=X` | Focus on specific scope |
| `--loop` | Re-run until clean or max 3 iterations. Combines with `--auto`. |

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
| Monorepo | <35% | >70% | <12 | 75%+ |
| Mobile | <55% | >65% | <12 | 65%+ |
| Infra/IaC | <45% | >70% | <10 | 60%+ |

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

Co-Authored-By: {model} <noreply@anthropic.com>
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

## /cco-blueprint

Profile-based project health assessment, transformation, and progress tracking.

```bash
/cco-blueprint                     # Full flow: profile + assess + transform
/cco-blueprint --init              # Create/refresh profile only
/cco-blueprint --preview           # Analyze and show dashboard, no changes
/cco-blueprint --auto              # Unattended: all phases, no questions
/cco-blueprint --refresh           # Re-scan profile (preserves decisions)
/cco-blueprint --scope=security    # Focus on specific area
```

### How It Works

1. **Profile** — Creates a profile in CLAUDE.md (between markers) with project config, ideal metrics, and scores
2. **Assess** — Runs optimize, align, docs, and audit scopes in parallel (preview mode)
3. **Dashboard** — Shows Project Map + health scores with current vs target gaps
4. **Transform** — Applies fixes based on priorities and constraints from profile
5. **Memory** — Cleans stale auto-memory entries using project context (deleted file refs, outdated commands, contradictions)
6. **Track** — Updates scores in profile for incremental improvement

### Health Dimensions (6)

| Dimension | Weight | Source |
|-----------|--------|--------|
| Security | 25% | optimize: security + privacy + robustness |
| Code Quality | 20% | optimize: hygiene + types + simplify + performance |
| Architecture | 20% | align: architecture + patterns + maintainability |
| Stack Health | 15% | audit: stack-assessment + dependency-health |
| DX | 10% | audit: dx-quality + project-structure |
| Documentation | 10% | docs results |

### Profile Questions (6)

Two rounds: Project Identity (type, quality target, data sensitivity) → Strategy (priorities, constraints, audience).

In --auto mode: all questions use auto-detected defaults.

---

## /cco-pr

Create pull requests with conventional commit titles for clean release-please changelogs.

```bash
/cco-pr                 # Interactive PR creation
/cco-pr --auto          # Auto-detect everything, create PR directly
/cco-pr --preview       # Show PR plan without creating
/cco-pr --draft         # Create as draft PR
```

### How It Works

1. Analyzes ALL commits on the branch (not just latest)
2. Determines conventional commit type from commit history (`feat` → minor, `fix` → patch, others → no bump)
3. Generates PR title in conventional commit format (≤70 chars)
4. Creates clean body with summary, changes, and test plan
5. Single Co-Authored-By trailer (not per-commit duplication)

### Release-Please Integration

Designed for squash merge workflows:
- PR title becomes the squash commit message on main
- Release-please reads that one clean commit
- Result: 1 changelog entry per PR, no co-author duplication

**Required repo setting:** Settings → Pull Requests → Squash merge → "Default to PR title and description"

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
/cco-blueprint --auto   # Same exit codes
```

### Accounting

Per CCO Rules: `applied + failed + needs_approval = total` (no silent skips)

### Recovery

| Situation | Command |
|-----------|---------|
| Revert file | `git checkout -- {file}` |
| Revert all | `git checkout .` |
| Review changes | `git diff` |
| Undo commit | `git reset --soft HEAD~1` |

---

*Back to [README](../README.md)*
