# Commands Reference

Complete parameter and flag documentation for all CCO commands.

---

## Quick Reference

| Command | Purpose | Model | Flags |
|---------|---------|-------|-------|
| `/cco:tune` | Configure project | Haiku | `--auto`, `--check`, `--force` |
| `/cco:optimize` | Fix code issues | Opus | `--auto`, `--security`, `--fix-all`, `--score` |
| `/cco:align` | Architecture gaps | Opus | `--auto`, `--preview`, `--intensity=X` |
| `/cco:commit` | Quality-gated commits | Opus | `--preview`, `--single`, `--staged-only` |
| `/cco:research` | Multi-source research | Opus | `--quick`, `--deep`, `--local` |
| `/cco:preflight` | Pre-release checks | Opus | `--auto`, `--strict`, `--skip-tests` |
| `/cco:docs` | Documentation gaps | Opus | `--auto`, `--check`, `--scope=X` |

---

## /cco:tune

Configure CCO for a project. Detects stack, creates profile, loads rules.

### Parameters

| Flag | Effect |
|------|--------|
| `--auto` | Unattended mode - auto-detect everything, skip questions |
| `--check` | Silent validation only, return status |
| `--force` | Update even if profile exists |

### Interactive Questions (8 total)

**Round 1: Team & Policy**

| Question | Options |
|----------|---------|
| Team size | Solo, Small (2-5), Medium (6-15), Large (15+) |
| Data sensitivity | No, Internal, User data, Regulated |
| Top priority | Security, Performance, Readability, Ship fast |
| Breaking changes | Never, Major only, With warning, When needed |

**Round 2: Development & Deployment**

| Question | Options |
|----------|---------|
| API consumers | No, Internal, Partners, Public |
| Testing approach | Minimal, Target-based, Test first, Everything |
| Documentation | Code only, Basic, Detailed, Comprehensive |
| Deployment | Dev only, Cloud, Self-hosted, Serverless |

### Generated Files

| File | Purpose |
|------|---------|
| `.claude/rules/cco-profile.md` | Project metadata (YAML frontmatter) |
| `.claude/rules/cco-{language}.md` | Language-specific rules |
| `.claude/rules/cco-{framework}.md` | Framework-specific rules |

### Examples

```bash
/cco:tune              # Interactive setup
/cco:tune --auto       # Auto-detect everything
/cco:tune --check      # Validate existing profile
/cco:tune --force      # Force update
```

---

## /cco:optimize

Fix security, quality, and hygiene issues.

### Parameters

| Flag | Effect |
|------|--------|
| `--auto` | Unattended mode - all scopes, full fix, no questions |
| `--security` | Security scope only (SEC-01 to SEC-12) |
| `--hygiene` | Hygiene scope only (HYG-01 to HYG-15) |
| `--types` | Types scope only (TYP-01 to TYP-10) |
| `--lint` | Lint scope only (LNT-01 to LNT-08) |
| `--performance` | Performance scope only (PRF-01 to PRF-10) |
| `--ai-hygiene` | AI hygiene scope only (AIH-01 to AIH-08) |
| `--robustness` | Robustness scope only (ROB-01 to ROB-10) |
| `--doc-sync` | Doc-code sync scope only (DOC-01 to DOC-08) |
| `--report` | Report only, no fixes |
| `--fix-all` | Full fix intensity without approval |
| `--score` | Quality score only (0-100) |
| `--intensity=X` | Set intensity: quick-wins, standard, full-fix, report-only |
| `--plan` | Show detailed fix plan before applying |

### Scope Coverage (81 Checks)

| Scope | ID Range | Focus |
|-------|----------|-------|
| Security | SEC-01-12 | Secrets, injection, validation |
| Hygiene | HYG-01-15 | Unused code, dead code, imports |
| Types | TYP-01-10 | Type errors, annotations |
| Lint | LNT-01-08 | Format, naming, style |
| Performance | PRF-01-10 | N+1, caching, async |
| AI Hygiene | AIH-01-08 | Hallucinated APIs, orphan abstractions |
| Robustness | ROB-01-10 | Timeouts, retries, validation |
| Doc Sync | DOC-01-08 | Documentation-code consistency |

### Intensity Levels

| Level | Severities | Use Case |
|-------|------------|----------|
| quick-wins | High impact + low effort | Fast 80/20 improvement |
| standard | CRITICAL + HIGH + MEDIUM | Normal operation |
| full-fix | ALL severities | Comprehensive cleanup |
| report-only | ALL (analysis) | Review without changes |

### Examples

```bash
/cco:optimize                    # Interactive selection
/cco:optimize --auto             # Silent full optimization
/cco:optimize --security         # Security only
/cco:optimize --fix-all          # Fix everything
/cco:optimize --score            # Quick quality score
```

---

## /cco:align

Architecture and pattern analysis. Compare current state to ideal.

### Parameters

| Flag | Effect |
|------|--------|
| `--auto` | Unattended mode - all scopes, full intensity |
| `--preview` | Analyze only, show gaps, don't apply |
| `--intensity=X` | Set intensity level |
| `--plan` | Show architectural plan before applying |

### Scope Coverage (71 Checks)

| Scope | ID Range | Focus |
|-------|----------|-------|
| Architecture | ARC-01-15 | Coupling, cohesion, layers |
| Patterns | PAT-01-12 | SOLID, DRY, consistency |
| Testing | TST-01-10 | Coverage, quality, gaps |
| Maintainability | MNT-01-12 | Complexity, readability |
| AI Architecture | AIA-01-10 | Over-engineering, drift |
| Functional | FUN-01-12 | CRUD, pagination, edge cases |

### Ideal Metrics by Project Type

| Type | Coupling | Cohesion | Complexity | Coverage |
|------|----------|----------|------------|----------|
| CLI | <40% | >75% | <10 | 70%+ |
| Library | <30% | >80% | <8 | 85%+ |
| API | <50% | >70% | <12 | 80%+ |
| Web | <60% | >65% | <15 | 70%+ |

### Examples

```bash
/cco:align                       # Interactive review
/cco:align --auto                # Full review, no questions
/cco:align --preview             # Analysis only
/cco:align --intensity=full-fix  # Fix all findings
```

---

## /cco:commit

Quality-gated atomic commits.

### Parameters

| Flag | Effect |
|------|--------|
| `--preview` | Show commit plan only, don't execute |
| `--single` | Force single commit |
| `--split` | Auto-split by scope |
| `--skip-tests` | Skip test gate |
| `--amend` | Amend last commit |
| `--staged-only` | Commit only staged changes |

### Quality Gates (Parallel)

| Gate | Command | Action |
|------|---------|--------|
| Secrets | Pattern detection | BLOCK if found |
| Large Files | Size check | WARN >1MB, BLOCK >10MB |
| Format | `{format_cmd}` | Auto-fix, re-stage |
| Lint | `{lint_cmd}` | STOP on unfixable |
| Types | `{type_cmd}` | STOP on failure |
| Tests | `{test_cmd}` | STOP on failure |

### Commit Message Format

```
{type}({scope}): {title}  (max 50 chars total)

{body}

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Examples

```bash
/cco:commit                 # Full flow
/cco:commit --preview       # Preview only
/cco:commit --single        # One commit for all
/cco:commit --staged-only   # Only staged changes
```

---

## /cco:research

Multi-source research with reliability scoring.

### Parameters

| Flag | Effect |
|------|--------|
| `--quick` | T1-T2 sources only, 5 sources max |
| `--deep` | All tiers, 20+ sources, resumable |
| `--local` | Codebase-only search |
| `--security` | Security advisories focus |
| `--compare` | Comparison mode (A vs B) |
| `--json` | JSON output format |
| `--resume=ID` | Resume previous deep session |

### Source Tiers

| Tier | Score | Sources |
|------|-------|---------|
| T1 | 90-100 | Official docs, specs |
| T2 | 80-90 | GitHub, changelogs |
| T3 | 70-80 | Major blogs, tutorials |
| T4 | 60-70 | Stack Overflow, forums |
| T5 | 50-60 | Personal blogs |
| T6 | 40-50 | Unknown/unverified |

### Depth Levels

| Depth | Sources | Model Strategy |
|-------|---------|----------------|
| Quick | T1-T2 | Haiku only |
| Standard | T1-T4 | Haiku search, Opus synthesis |
| Deep | All tiers | Haiku search, Opus synthesis |

### Examples

```bash
/cco:research "best auth library for Node"
/cco:research "Flask vs FastAPI" --compare
/cco:research "CVE-2024-1234" --security
/cco:research "our auth implementation" --local
```

---

## /cco:preflight

Pre-release verification gate.

### Parameters

| Flag | Effect |
|------|--------|
| `--auto` | Unattended mode - full checks, no questions |
| `--preview` | Run all checks, show results, don't release |
| `--strict` | Treat warnings as blockers |
| `--skip-tests` | Skip test suite |
| `--skip-docs` | Skip documentation updates |

### Checks (14 total)

**Blockers (must fix):**

| ID | Check |
|----|-------|
| PRE-01 | Dirty git state |
| PRE-03 | Version mismatch |
| VER-01 | Tests fail |
| VER-02 | Build fail |
| VER-03 | Type errors |
| DEP-SEC | Security CVE |

**Warnings (can override):**

| ID | Check |
|----|-------|
| PRE-02 | Wrong branch |
| PRE-04 | TODO/FIXME markers |
| VER-04 | Lint warnings |
| DEP-OUT | Outdated deps |

### Examples

```bash
/cco:preflight              # Full release workflow
/cco:preflight --auto       # Unattended checks
/cco:preflight --strict     # Warnings = blockers
/cco:preflight --preview    # Check without releasing
```

---

## /cco:docs

Documentation gap analysis and generation.

### Parameters

| Flag | Effect |
|------|--------|
| `--auto` | Generate all missing docs |
| `--check` | Validation only, return status |
| `--report` | Show gaps only, don't generate |
| `--scope=X` | Single scope: readme, api, dev, user, ops, changelog |
| `--plan` | Show plan before generating |
| `--force` | Regenerate even if docs exist |

### Documentation Scopes

| Scope | Target Files | Purpose |
|-------|--------------|---------|
| readme | README.md | Project overview |
| api | docs/api/*.md | API reference |
| dev | CONTRIBUTING.md | Developer onboarding |
| user | docs/user/*.md | End-user guides |
| ops | docs/ops/*.md | Deployment, operations |
| changelog | CHANGELOG.md | Version history |

### Ideal Docs by Project Type

| Type | Required | Optional |
|------|----------|----------|
| CLI | README, usage | contributing |
| Library | README, API, dev | guides |
| API | README, API, dev, ops | user |
| Web | README, dev, ops | components |

### Examples

```bash
/cco:docs                   # Interactive selection
/cco:docs --auto            # Generate all missing
/cco:docs --check           # Validate only
/cco:docs --scope=readme    # README only
```

---

## Common Patterns

### Unattended Mode

All commands support `--auto` for CI/CD:

```bash
/cco:optimize --auto    # Exit 0=OK, 1=WARN, 2=FAIL
/cco:align --auto       # Same exit codes
/cco:preflight --auto   # Same exit codes
```

### Accounting Invariant

All operations report: `Applied: N | Failed: M | Total: N+M`

Formula: `applied + failed = total` (no silent skips)

### Recovery

| Situation | Command |
|-----------|---------|
| Revert file | `git checkout -- {file}` |
| Revert all | `git checkout .` |
| Review changes | `git diff` |
| Undo commit | `git reset --soft HEAD~1` |

---

*Back to [README](../README.md)*
