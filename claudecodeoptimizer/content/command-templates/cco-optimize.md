---
name: cco-optimize
description: Code cleanliness and efficiency optimization with auto-fix
allowed-tools: Read(*), Grep(*), Glob(*), Edit(*), Bash(git:*), Bash(wc:*), Task(*), TodoWrite
---

# /cco-optimize

**Cleanliness & Efficiency** - Analyze → clean → optimize → verify.

End-to-end: Detects waste (orphans, duplicates, stale refs) AND removes/optimizes them.

**Rules:** User Input | Safety | Classification | Approval Flow | Skip Criteria | Task Tracking

## Context

- Context check: !`test -f ./.claude/rules/cco/context.md && echo "1" || echo "0"`
- File count: !`find . -type f \( -name "*.py" -o -name "*.ts" -o -name "*.js" \) 2>/dev/null | wc -l`
- Git status: !`git status --short`

**Static context (Scale, Maturity, Type, Breaking) is read from ./CLAUDE.md already in context.**

## Context Requirement [CRITICAL]

**This command requires CCO context in ./.claude/rules/cco/context.md.**

If context check returns "0":
```
CCO context not found.

Run /cco-tune first to configure project context, then restart CLI.
```
**Stop execution immediately.**

## Context Application

| Field | Effect |
|-------|--------|
| Scale | <100 → clarity over performance; 10K+ → performance critical |
| Type | CLI: startup time; API: response time; Library: memory; Frontend: bundle size |
| Maturity | Legacy → safe optimizations only; Greenfield → aggressive restructuring OK |
| Breaking | Never → preserve all interfaces; Allowed → simplify APIs, remove compat |
| Data | PII → no caching user data, careful with logging; Regulated → audit trail |
| Priority | Speed → quick wins only; Quality → comprehensive analysis |

## Agent Integration

| Phase | Agent | Scope | Purpose |
|-------|-------|-------|---------|
| Scan | `cco-agent-analyze` | `scan` | Detect orphans, duplicates, stale refs |
| Deps | `cco-agent-research` | `dependency` | Check versions, breaking changes, CVEs |
| Optimize | `cco-agent-apply` | `optimize` | Execute approved cleanups |

### Parallel Scan Pattern [REQUIRED]

When scanning multiple categories, launch **parallel agents** in a single message:

```
Launch simultaneously:
- Agent 1: cco-agent-analyze scope=orphans
- Agent 2: cco-agent-analyze scope=duplicates
- Agent 3: cco-agent-analyze scope=stale-refs
```

### Dependency Check Pattern [REQUIRED]

For `--deps` flag, launch research agents per ecosystem:

```
Launch simultaneously:
- Agent 1: cco-agent-research mode=dependency ecosystem=python
- Agent 2: cco-agent-research mode=dependency ecosystem=node
- Agent 3: cco-agent-research mode=dependency ecosystem=rust
(only for detected ecosystems)
```

### Agent Propagation

When spawning agents, include:
```
Context: {Scale, Maturity, Breaking from CCO_ADAPTIVE}
Rules: Safe vs risky classification, exact output format
Output: [CATEGORY] {type}: {name} in {file:line}
Note: Make a todo list first, process systematically
```

## Default Behavior

When called without flags:

**Use AskUserQuestion:**
| Question | Options | MultiSelect |
|----------|---------|-------------|
| Focus? | Hygiene (Recommended); Efficiency; All | true |
| Mode? | Conservative; Balanced (Recommended); Aggressive | false |

Explicit flags skip questions.

## Categories

### Orphans (`--orphans`)

Detect and remove unreferenced code:

| Type | Detection | Action |
|------|-----------|--------|
| Orphan file | No imports pointing to it | Delete with confirmation |
| Orphan function | Defined but never called | Delete or flag |
| Orphan export | Exported but never imported | Remove export |
| Orphan import | Imported but never used | Remove import |
| Orphan config | Config key not referenced | Remove or flag |

Report: `[ORPHAN] {type}: {name} in {file:line} (last modified: {date})`

**Resolution - Use AskUserQuestion:**
| Question | Options | MultiSelect |
|----------|---------|-------------|
| Orphan: {name} in {file:line}. Action? | Delete; Keep (add reference); Skip | false |

### Stale References (`--stale-refs`)

Detect and fix broken references:

| Type | Detection | Action |
|------|-----------|--------|
| Broken import | Import path doesn't exist | Remove or fix path |
| Dead link | URL returns 404 | Update or remove |
| Missing ref | Code references undefined | Fix or remove |
| Obsolete comment | Comment references deleted code | Update comment |
| Phantom test | Test for non-existent function | Remove test |

Report: `[STALE-REF] {type}: {reference} → {missing_target} in {file:line}`

### Duplicates (`--duplicates`)

Detect and consolidate duplicate content:

| Type | Similarity | Action |
|------|------------|--------|
| Exact duplicate | 100% | Consolidate → single source + re-export |
| Near-duplicate | >80% | Review → merge or justify differences |
| Semantic duplicate | Same logic | Extract shared abstraction |

Detection methods:
- Content hash (MD5/SHA256) for exact matches
- Fuzzy match (Levenshtein, Jaccard) for near-duplicates
- AST comparison for semantic duplicates

Report: `[DUPLICATE] {type} ({similarity}%): {file1}:{line} ↔ {file2}:{line}`

### Redundancy (`--redundancy`)

Detect and eliminate redundant content:

| Type | Detection | Action |
|------|-----------|--------|
| Redundant code | Same functionality in different places | Keep best, redirect others |
| Redundant config | Same value in multiple configs | Single source + reference |
| Redundant docs | Same info in multiple places | Consolidate or cross-reference |

### Context (`--context`)

Optimize AI context files:

| Target | Optimization |
|--------|-------------|
| CLAUDE.md | Remove duplicates, compress verbose patterns |
| Prompts | Implicit info removal, format efficiency |
| Agent configs | Dead instruction removal |

### Docs (`--docs`)

Optimize documentation:

| Target | Optimization |
|--------|-------------|
| Stale content | Update or remove outdated sections |
| Redundant sections | Merge overlapping content |
| Verbose explanations | Trim to essential |
| Broken examples | Fix or remove |

### Code Efficiency (`--code`)

Optimize code performance:

| Category | Optimizations |
|----------|---------------|
| Loops | Unnecessary iterations, early exits |
| Conditionals | Simplification, guard clauses |
| Algorithms | Better complexity alternatives |
| N+1 queries | Batch database calls |
| Memory | Reduce allocations, streaming |
| Imports | Tree-shaking hints, lazy loading |

### Cross-File (`--cross-file`)

Full codebase analysis combining all above:

| Analysis | Scope |
|----------|-------|
| Dependency graph | All imports/exports |
| Duplication map | All files |
| Orphan detection | All code |
| Stale ref scan | All references |

### Dependencies (`--deps`)

Analyze dependency freshness and suggest safe updates.

**IMPORTANT:** No auto-fix for this category. Every version change requires explicit user approval.

#### Supported Ecosystems

| Ecosystem | Manifest Files | Registry | Version Source |
|-----------|----------------|----------|----------------|
| **Python** | `requirements.txt`, `pyproject.toml`, `setup.py`, `Pipfile` | pypi.org | `info.version` |
| **Node.js** | `package.json`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml` | npmjs.com | `dist-tags.latest` |
| **Rust** | `Cargo.toml`, `Cargo.lock` | crates.io | `max_stable_version` |
| **Go** | `go.mod`, `go.sum` | pkg.go.dev | latest tag |
| **Ruby** | `Gemfile`, `Gemfile.lock` | rubygems.org | `version` |
| **PHP** | `composer.json`, `composer.lock` | packagist.org | `version` |

#### Detection Flow

1. **Scan** - Detect manifest files in project
2. **Parse** - Extract package names and current versions
3. **Fetch** - Query registries for latest stable versions (web search)
4. **Compare** - SemVer analysis (patch/minor/major)
5. **Analyze** - Changelog/release notes for breaking changes
6. **Report** - Present findings with risk classification
7. **Approve** - User selects which updates to apply
8. **Apply** - Update manifest files

#### Risk Classification

| Type | SemVer Change | Risk | Indicator |
|------|---------------|------|-----------|
| **Patch** | `x.y.Z` → `x.y.Z+n` | 🟢 Safe | Bug fixes only |
| **Minor** | `x.Y.z` → `x.Y+n.z` | 🟡 Low | New features, backward compatible |
| **Major** | `X.y.z` → `X+n.y.z` | 🔴 Breaking | API changes, migration needed |
| **Security** | CVE exists in current | 🔴 Critical | Vulnerability fix available |
| **Deprecated** | Package EOL/archived | ⚫ Replace | Find alternative |
| **Pinned** | Exact version constraint | 🔵 Intentional | Skip unless security |

#### Breaking Change Detection

For Major updates, perform changelog analysis:

| Source | Priority | Check For |
|--------|----------|-----------|
| GitHub Releases | T1 | Breaking changes section |
| CHANGELOG.md | T1 | `BREAKING:` prefixed entries |
| Migration Guide | T1 | Required code changes |
| Release Notes | T2 | Deprecation notices |
| GitHub Issues | T3 | Common upgrade problems |

#### Approval Flow [REQUIRED]

**Every update requires explicit user approval:**

```
┌─ PENDING UPDATE ─────────────────────────────────────────────┐
│ Package: pytest                                               │
│ Current: 7.4.0 → Latest: 8.3.4                               │
│ Type: MAJOR (breaking)                                        │
├───────────────────────────────────────────────────────────────┤
│ Breaking Changes Detected:                                    │
│ • pytest.fixture scope parameter default changed              │
│ • Python 3.7 support dropped                                  │
│ • Several deprecated APIs removed                             │
├───────────────────────────────────────────────────────────────┤
│ Migration: https://docs.pytest.org/en/8.0.x/changelog.html   │
└───────────────────────────────────────────────────────────────┘
```

**Use AskUserQuestion for each update:**
| Question | Options | MultiSelect |
|----------|---------|-------------|
| Update {pkg} {current} → {latest}? | Update; Skip; Details | false |

**Batch approval option:**
| Question | Options | MultiSelect |
|----------|---------|-------------|
| Apply selected updates? | Confirm; Review again; Cancel all | false |

#### Sub-flags

| Flag | Effect |
|------|--------|
| `--deps` | All dependency checks |
| `--deps-patch` | Only patch updates (safest) |
| `--deps-minor` | Patch + minor updates |
| `--deps-major` | Include major updates |
| `--deps-security` | Only security-related updates |
| `--deps-outdated` | Show outdated without updating |

Report: `[DEP] {risk}: {package} {current} → {latest} ({type}) in {manifest}`

## Meta-flags

| Flag | Includes |
|------|----------|
| `--hygiene` | orphans + stale-refs + duplicates (quick cleanup) |
| `--efficiency` | code + context + docs (optimization focus) |
| `--freshness` | deps + outdated checks (dependency health) |
| `--deep` | All categories, thorough analysis |
| `--prune` | Focus on removal (orphans + stale-refs + dead content) |
| `--all` | Everything applicable (excludes deps, requires explicit flag) |
| `--auto-fix` | Apply safe fixes without asking (NOT applicable to --deps) |

## Resolution Actions

| Finding | Safe (auto-apply) | Risky (approval needed) |
|---------|-------------------|-------------------------|
| Exact duplicate | Consolidate + re-export | Delete one copy |
| Near-duplicate | Show diff, suggest merge | Auto-merge |
| Semantic duplicate | Suggest extraction | Refactor both |
| Orphan file | Warn, suggest deletion | Delete file |
| Orphan function | Remove from exports | Delete function |
| Stale ref | Flag for review | Remove reference |
| Broken import | Fix path if obvious | Remove import |
| Config redundancy | Single source + env ref | Merge configs |
| Dep patch update | — | Always ask (no auto) |
| Dep minor update | — | Always ask (no auto) |
| Dep major update | — | Always ask + show breaking |
| Dep security fix | — | Always ask (urgent flag) |

## Output

**Follow output formats precisely.**

### Cleanliness Summary
```
┌─ CLEANLINESS SUMMARY ────────────────────────────────────────┐
│ Category      │ Found │ Fixed │ Skipped │ Status            │
├───────────────┼───────┼───────┼─────────┼───────────────────┤
│ Orphans       │ 5     │ 4     │ 1       │ WARN              │
│ Stale-Refs    │ 3     │ 3     │ 0       │ OK                │
│ Duplicates    │ 2     │ 2     │ 0       │ OK                │
│ Redundancy    │ 1     │ 1     │ 0       │ OK                │
├───────────────┼───────┼───────┼─────────┼───────────────────┤
│ TOTAL         │ 11    │ 10    │ 1       │ WARN              │
└───────────────┴───────┴───────┴─────────┴───────────────────┘
```

### Optimization Results
```
┌─ OPTIMIZATION RESULTS ───────────────────────────────────────┐
│ File              │ Before │ After  │ Change │ Status        │
├───────────────────┼────────┼────────┼────────┼───────────────┤
│ utils.py          │ 245 L  │ 198 L  │ -19%   │ Consolidated  │
│ helpers.py        │ 180 L  │ 12 L   │ -93%   │ Re-exports    │
│ README.md         │ 420 L  │ 385 L  │ -8%    │ Deduplicated  │
│ old_api.py        │ 89 L   │ 0 L    │ -100%  │ Deleted       │
├───────────────────┼────────┼────────┼────────┼───────────────┤
│ TOTAL             │ 934 L  │ 595 L  │ -36%   │               │
└───────────────────┴────────┴────────┴────────┴───────────────┘
```

### Metrics Summary
```
Before: 2,450 lines | 48,200 tokens | 156 KB
After:  1,890 lines | 37,100 tokens | 121 KB
Saved:  560 lines (23%) | 11,100 tokens (23%) | 35 KB (22%)
```

### Dependency Freshness Report
```
┌─ DEPENDENCY FRESHNESS ───────────────────────────────────────┐
│ Scanned: package.json, requirements.txt                       │
│ Date: 2025-12-09 | Packages: 24 | Outdated: 8                │
└───────────────────────────────────────────────────────────────┘

┌─ UPDATES AVAILABLE ──────────────────────────────────────────┐
│ Package         │ Current │ Latest  │ Type   │ Risk │ Status │
├─────────────────┼─────────┼─────────┼────────┼──────┼────────┤
│ pytest          │ 7.4.0   │ 8.3.4   │ MAJOR  │ 🔴   │ REVIEW │
│ ruff            │ 0.6.0   │ 0.8.4   │ MINOR  │ 🟡   │ REVIEW │
│ requests        │ 2.31.0  │ 2.32.3  │ PATCH  │ 🟢   │ REVIEW │
│ lodash          │ 4.17.20 │ 4.17.21 │ PATCH  │ 🟢   │ REVIEW │
│ express         │ 4.18.2  │ 4.21.2  │ MINOR  │ 🟡   │ REVIEW │
│ django (CVE)    │ 4.2.0   │ 4.2.17  │ PATCH  │ 🔴   │ URGENT │
├─────────────────┼─────────┼─────────┼────────┼──────┼────────┤
│ Up-to-date: 16  │ Patch: 2│ Minor: 2│ Major:1│ CVE:1│        │
└─────────────────┴─────────┴─────────┴────────┴──────┴────────┘

┌─ BREAKING CHANGES (Major Updates) ───────────────────────────┐
│ pytest 7.4.0 → 8.3.4                                          │
│ ├─ Python 3.7 support dropped                                 │
│ ├─ pytest.fixture scope default changed                       │
│ └─ Migration: https://docs.pytest.org/en/8.0.x/changelog     │
└───────────────────────────────────────────────────────────────┘

┌─ SECURITY ADVISORIES ────────────────────────────────────────┐
│ django 4.2.0 - CVE-2024-XXXXX (HIGH)                         │
│ └─ SQL injection in QuerySet.values() - Fixed in 4.2.17      │
└───────────────────────────────────────────────────────────────┘
```

### Dependency Update Summary
```
┌─ UPDATE SUMMARY ─────────────────────────────────────────────┐
│ Action          │ Count │ Packages                           │
├─────────────────┼───────┼────────────────────────────────────┤
│ Updated         │ 4     │ requests, lodash, ruff, django     │
│ Skipped         │ 1     │ pytest (user choice)               │
│ Skipped         │ 1     │ express (user choice)              │
├─────────────────┼───────┼────────────────────────────────────┤
│ TOTAL           │ 6     │ 4 updated, 2 skipped               │
└─────────────────┴───────┴────────────────────────────────────┘

Modified files:
- requirements.txt (3 packages)
- package.json (1 package)

Next steps:
- Run tests to verify compatibility
- Review pytest changelog before major upgrade
```

## Verification

After optimization:
- [ ] Tests pass (no regressions)
- [ ] Same behavior (functional equivalence)
- [ ] No broken imports (all refs valid)
- [ ] Metrics improved (lines/tokens reduced)
- [ ] No new orphans created (consolidation complete)

After dependency updates:
- [ ] Lock files regenerated (pip freeze, npm install, etc.)
- [ ] Tests pass with new versions
- [ ] No breaking API changes in codebase
- [ ] CI/CD pipeline passes

## Follow-up Actions [CRITICAL]

When optimization reveals actionable recommendations (e.g., pinning versions, refactoring complex functions), ALWAYS use AskUserQuestion - never ask as plain text.

**Use AskUserQuestion:**
| Question | Options | MultiSelect |
|----------|---------|-------------|
| Follow-up actions? | Apply recommendations; Create issues; Skip | true |

## Usage

```bash
/cco-optimize                    # Interactive
/cco-optimize --hygiene          # Quick cleanup (orphans + stale-refs + duplicates)
/cco-optimize --orphans          # Find and remove unreferenced code
/cco-optimize --stale-refs       # Find and fix broken references
/cco-optimize --duplicates       # Find and consolidate duplicates
/cco-optimize --code             # Code efficiency optimization
/cco-optimize --cross-file       # Full cross-file analysis
/cco-optimize --prune            # Remove all dead content
/cco-optimize --all --auto-fix   # Everything, auto-apply safe fixes

# Dependency Freshness (always requires approval)
/cco-optimize --deps             # Check all dependencies
/cco-optimize --deps-patch       # Only safe patch updates
/cco-optimize --deps-minor       # Patch + minor updates
/cco-optimize --deps-major       # Include breaking changes analysis
/cco-optimize --deps-security    # Only security-related updates
/cco-optimize --deps-outdated    # Report only, no update prompts
/cco-optimize --freshness        # Full dependency health check
```

## Related Commands

- `/cco-audit` - For security and quality checks
- `/cco-refactor` - For structural transformations (rename, move, extract)
- `/cco-checkup` - For regular maintenance routine

---

## Behavior Rules

### User Input [CRITICAL]

- **AskUserQuestion**: ALL user decisions MUST use this tool
- **Separator**: Use semicolon (`;`) to separate options
- **Prohibited**: Never use plain text questions ("Would you like...", "Should I...")

### Safety

- **Pre-op**: Check git status before any modifications
- **Dirty**: If uncommitted changes → prompt: `Commit; Stash; Continue anyway`
- **Rollback**: Clean git state enables `git checkout` on failure

### Classification

| Type | Examples | Action |
|------|----------|--------|
| Safe | Remove unused imports, dead code, stale refs | Auto-apply |
| Risky | Consolidate duplicates, dependency updates | Require approval |

### Approval Flow

- **Batch**: First option = "All (N)" for bulk approval
- **Priority**: CRITICAL → HIGH → MEDIUM → LOW
- **Format**: `{description} [{file:line}] [{safe|risky}]`

### Skip Criteria

- **Inline**: `// cco-ignore` or `# cco-ignore` skips line
- **File**: `// cco-ignore-file` skips entire file
- **Paths**: fixtures/, testdata/, examples/, benchmarks/

### Conservative Judgment [CRITICAL]

| Keyword | Severity | Confidence Required |
|---------|----------|---------------------|
| crash, data loss, security breach | CRITICAL | HIGH |
| broken, blocked, cannot use | HIGH | HIGH |
| error, fail, incorrect | MEDIUM | MEDIUM |
| style, minor, cosmetic | LOW | LOW |

- **Lower**: When uncertain between two severities, choose lower
- **Evidence**: Require explicit evidence, not inference
- **No-Escalate**: Style issues → never CRITICAL or HIGH

### Batch Approval

- **MultiSelect**: true for batch approvals
- **All-Option**: First option = "All ({N})" for bulk
- **Priority-Order**: CRITICAL → HIGH → MEDIUM → LOW
- **Item-Format**: `{description} [{file:line}] [{safe|risky}]`

### Task Tracking

- **Create**: TODO list with all items before starting
- **Status**: pending → in_progress → completed
- **Accounting**: done + skip + fail = total
