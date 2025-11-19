---
name: cco-audit
description: Comprehensive codebase audit with full transparency and real-time progress
action_type: audit
parameters:
  security:
    keywords: [security audit, owasp scan, xss check, sqli scan, csrf check, secrets scan, vulnerability scan]
    category: security
    pain_points: [1]
  tech-debt:
    keywords: [tech debt audit, dead code scan, complexity check, duplication scan]
    category: quality
    pain_points: [2]
  ai-security:
    keywords: [ai security audit, prompt injection scan, llm security, ai vulnerability]
    category: security
    pain_points: [3]
  tests:
    keywords: [test audit, coverage check, test quality, test isolation, test pyramid]
    category: testing
    pain_points: [4]
  integration:
    keywords: [integration audit, dependency check, import scan, conflict detection]
    category: infrastructure
    pain_points: [6]
  code-quality:
    keywords: [code quality audit, syntax check, type check, error handling scan]
    category: quality
    pain_points: [2]
  docs:
    keywords: [documentation audit, docstring check, api docs scan, readme check]
    category: docs
    pain_points: [7]
  database:
    keywords: [database audit, n+1 scan, index check, query optimization, db performance]
    category: database
    pain_points: [5]
  observability:
    keywords: [observability audit, logging check, metrics scan, tracing check]
    category: observability
    pain_points: [5]
  monitoring:
    keywords: [monitoring audit, dashboard check, alert scan, prometheus check]
    category: observability
    pain_points: [5]
  cicd:
    keywords: [cicd audit, pipeline check, quality gates scan, deployment audit]
    category: infrastructure
    pain_points: [6]
  containers:
    keywords: [container audit, dockerfile scan, k8s check, container security]
    category: infrastructure
    pain_points: [6]
  supply-chain:
    keywords: [supply chain audit, dependency scan, cve check, sbom scan, license check]
    category: security
    pain_points: [1]
  migrations:
    keywords: [migration audit, schema check, rollback scan, data migration check]
    category: database
    pain_points: [5]
  performance:
    keywords: [performance audit, caching check, bundle scan, response time check]
    category: performance
    pain_points: [5]
  architecture:
    keywords: [architecture audit, coupling check, pattern scan, design review]
    category: architecture
    pain_points: [5]
  git:
    keywords: [git audit, commit quality, branching check, pr process scan]
    category: infrastructure
    pain_points: [5]
---

# CCO Audit Command

**Comprehensive codebase analysis with full transparency, flexible selection, and real-time progress.**

---

## Design Principles

1. **Full Transparency** - User sees exactly what will run, why, and how long
2. **Progressive Disclosure** - Simple start, detail on demand
3. **Zero Surprises** - Pre-flight shows everything before execution
4. **Real-time Feedback** - Streaming results, not batch output
5. **Actionable Output** - Every finding has a clear next step
6. **100% Honesty** - Report exact truth, no false positives or negatives
7. **No Hardcoded Examples** - All examples use placeholders, never fake data

---

## CRITICAL: No Hardcoded Examples

**AI models may interpret hardcoded examples as real data and use them literally.**

### Rules

```python
# ❌ BAD: Hardcoded example (AI might use as-is)
"file": "src/auth/login.py"
"line": 45
"issue": "SQL injection in authenticate()"

# ✅ GOOD: Dynamic placeholders
"file": "{FILE_PATH}"
"line": "{LINE_NUMBER}"
"issue": "{ISSUE_DESCRIPTION}"
```

### Template Format

All examples in this document use:
- `{VARIABLE_NAME}` - To be replaced with actual values
- `{COUNT}`, `{TIME}`, `{PCT}` - Numeric placeholders
- `{file}`, `{line}`, `{code}` - Context-specific placeholders

### Implementation

```python
def format_finding(finding: Finding) -> str:
    """Format finding with REAL data, never hardcoded examples."""

    # ❌ NEVER: Return template as-is
    # return "SQL Injection in auth.py:45"

    # ✅ ALWAYS: Use actual finding data
    return f"{finding.issue} in {finding.file}:{finding.line}"
```

---

## Execution Flow

```
/cco-audit
    │
    ├─► Mode Selection (Quick/Standard/Full)
    │
    ├─► Project Context (optional, recommended)
    │
    ├─► Discovery Phase (tech detection, applicability)
    │
    ├─► Selection (based on mode)
    │
    ├─► Pre-Flight Summary (confirm before run)
    │
    ├─► Execution Dashboard (real-time progress)
    │
    ├─► Streaming Results (findings as discovered)
    │
    └─► Final Report (prioritized, actionable)
```

---

## Component 1: Mode Selection

**Always start here. Let user choose control level.**

```python
AskUserQuestion({
  questions: [{
    question: "What level of control do you need?",
    header: "Audit Mode",
    multiSelect: false,
    options: [
      {
        label: "Quick Presets",
        description: "Use-case based (Pre-commit, Security, etc.) - Fastest start"
      },
      {
        label: "Category Mode",
        description: "Select from 9 category groups - Balanced control"
      },
      {
        label: "Full Control",
        description: "See all {TOTAL_CHECKS} checks, select individually - Maximum control"
      }
    ]
  }]
})
```

**Then proceed to Discovery Phase (same for all modes).**

---

## Component 1.5: Project Context Discovery (Optional)

**Ask user if they want project documentation analyzed for better alignment.**

```python
AskUserQuestion({
  questions: [{
    question: "Extract context from project documentation?",
    header: "Project Context",
    multiSelect: false,
    options: [
      {
        label: "Yes (recommended)",
        description: "Extract project goals and conventions from README/CONTRIBUTING, analysis aligns with objectives"
      },
      {
        label: "No",
        description: "Code analysis only (faster, documentation-independent)"
      }
    ]
  }]
})
```

### If User Selects "Yes"

```python
# Phase 0: Extract project context via Haiku sub-agent
context_result = Task({
    subagent_type: "Explore",
    model: "haiku",
    prompt: """
    Extract project context summary (MAX 200 tokens).
    
    Search for files in priority order (stop after 3-4 relevant ones):
    - README.md, README.rst, README.txt
    - CONTRIBUTING.md, .github/CONTRIBUTING.md
    - ARCHITECTURE.md, DESIGN.md, docs/architecture.md
    - docs/ADR/*.md, ROADMAP.md, CHANGELOG.md
    
    Return structured summary:
    
    ## Project Context
    
    **Purpose**: {1-2 sentences}
    **Goals**: {3 bullets max}
    **Tech Stack**: {languages, frameworks}
    **Conventions**: {naming, testing, formatting}
    **Architecture Notes**: {2 key decisions}
    
    If no documentation found: "No project documentation found."
    """
})

# Store for use in analysis phases
project_context = context_result
```

### Benefits

- **Zero main context cost** - Sub-agent uses separate context
- **Always fresh** - Extracted each run, no stale data
- **Better alignment** - Findings match project goals
- **Convention compliance** - Fixes follow project style

---

## Component 2: Discovery Phase

**Run BEFORE showing any selection options. Required for applicability.**

### Step 1: Tech Stack Detection

```python
# Detect project technologies
detected = {
    "languages": [],
    "frameworks": [],
    "databases": [],
    "devops": [],
    "testing": []
}

# Detection rules
if Glob("**/*.py"):
    detected["languages"].append("Python")

    # Check for frameworks
    req_content = Read("requirements.txt") or Read("pyproject.toml")
    if "flask" in req_content.lower():
        detected["frameworks"].append("Flask")
    if "django" in req_content.lower():
        detected["frameworks"].append("Django")
    if "fastapi" in req_content.lower():
        detected["frameworks"].append("FastAPI")
    if "sqlalchemy" in req_content.lower():
        detected["databases"].append("SQLAlchemy")

if Glob("**/*.js") or Glob("**/*.ts"):
    detected["languages"].append("JavaScript/TypeScript")

if Glob("**/Dockerfile"):
    detected["devops"].append("Docker")

if Glob("**/.github/workflows/*.yml"):
    detected["devops"].append("GitHub Actions")

if Glob("**/pytest.ini") or Glob("**/conftest.py"):
    detected["testing"].append("pytest")
```

### Step 2: Calculate Applicability

```python
# For each check, determine if applicable
applicable_checks = []
not_applicable = []

for check in ALL_CHECKS:
    if check.is_applicable(detected):
        applicable_checks.append(check)
    else:
        not_applicable.append((check, check.reason_not_applicable(detected)))
```

### Step 3: Display Discovery Results

```markdown
## Discovery Complete

**Tech Stack:**
```
Languages:   Python 3.11
Frameworks:  Flask 2.3, SQLAlchemy 2.0
Database:    PostgreSQL
DevOps:      Docker, GitHub Actions
Testing:     pytest, coverage
```

**Applicability:** {APPLICABLE_COUNT}/{TOTAL_CHECKS} checks ({APPLICABILITY_PCT}%)

**Files to scan:** {FILE_COUNT} files in {DIR_COUNT} directories
```

---

## Component 3: Full Checklist

**Only shown in Full Control Mode. Complete list of all available checks.**

### Check Categories

```markdown
## All Available Checks ({TOTAL_CHECKS} total)

### 🔴 CRITICAL IMPACT

#### Security (15 checks)
| #  | Check | Slug | Status | Time |
|----|-------|------|--------|------|
| 1  | SQL Injection | sql-injection | ✅ SQLAlchemy | 2m |
| 2  | XSS | xss | ✅ Jinja templates | 2m |
| 3  | CSRF | csrf | ⊘ No forms | - |
| 4  | Hardcoded Secrets | secrets | ✅ Always | 1m |
| 5  | Auth Bypass | auth-bypass | ✅ Auth found | 2m |
| 6  | Authz Flaws | authz-flaws | ✅ Routes | 2m |
| 7  | CVE Scan | cve-scan | ✅ Deps found | 2m |
| 8  | AI Prompt Injection | ai-injection | ⊘ No AI | - |
| 9  | SSRF | ssrf | ✅ HTTP calls | 1m |
| 10 | XXE | xxe | ⊘ No XML | - |
| 11 | Path Traversal | path-traversal | ✅ File ops | 1m |
| 12 | Command Injection | cmd-injection | ✅ subprocess | 1m |
| 13 | Insecure Deserial | deserial | ✅ pickle | 1m |
| 14 | Weak Crypto | weak-crypto | ✅ crypto | 1m |
| 15 | Security Headers | sec-headers | ✅ Flask | 1m |

#### Database (10 checks)
| #  | Check | Slug | Status | Time |
|----|-------|------|--------|------|
| 16 | N+1 Queries | n1-queries | ✅ ORM | 3m |
| 17 | Missing Indexes | missing-indexes | ✅ DB | 2m |
| 18 | Slow Queries | slow-queries | ✅ Queries | 2m |
| 19 | Connection Pooling | conn-pooling | ✅ DB conn | 1m |
| 20 | Query Optimization | query-optim | ✅ Complex | 2m |
| 21 | Transaction Issues | tx-issues | ✅ TX found | 1m |
| 22 | Deadlock Risk | deadlock | ✅ Concurrent | 1m |
| 23 | Migration Safety | migration-safety | ✅ Alembic | 1m |
| 24 | Raw SQL Risks | raw-sql | ✅ execute() | 1m |
| 25 | DB Credentials | db-creds | ✅ Always | 1m |

#### Tests (12 checks)
| #  | Check | Slug | Status | Time |
|----|-------|------|--------|------|
| 26 | Coverage Analysis | coverage | ✅ pytest-cov | 2m |
| 27 | Untested Functions | untested | ✅ Always | 3m |
| 28 | Test Isolation | isolation | ✅ fixtures | 2m |
| 29 | Test Pyramid | pyramid | ✅ structure | 1m |
| 30 | Edge Cases | edge-cases | ✅ Always | 2m |
| 31 | Flaky Tests | flaky | ✅ patterns | 2m |
| 32 | Test Naming | test-naming | ✅ Always | 1m |
| 33 | Assertion Quality | assertions | ✅ Always | 1m |
| 34 | Mock Overuse | mock-overuse | ✅ mock | 1m |
| 35 | Test Data Mgmt | test-data | ✅ fixtures | 1m |
| 36 | Integration Tests | integration | ✅ structure | 1m |
| 37 | E2E Tests | e2e | ⊘ No e2e | - |

### 🟡 HIGH IMPACT

#### Code Quality (15 checks)
| #  | Check | Slug | Status | Time |
|----|-------|------|--------|------|
| 38 | Dead Code | dead-code | ✅ Always | 2m |
| 39 | Complexity | complexity | ✅ Always | 2m |
| 40 | Duplication | duplication | ✅ Always | 2m |
| 41 | Type Errors | type-errors | ✅ hints | 2m |
| 42 | Linting | linting | ✅ Always | 1m |
| 43 | Code Smells | smells | ✅ Always | 2m |
| 44 | Long Functions | long-funcs | ✅ Always | 1m |
| 45 | Long Files | long-files | ✅ Always | 1m |
| 46 | Deep Nesting | deep-nesting | ✅ Always | 1m |
| 47 | Magic Numbers | magic-nums | ✅ Always | 1m |
| 48 | TODO Comments | todos | ✅ Always | 1m |
| 49 | Commented Code | commented | ✅ Always | 1m |
| 50 | Import Order | imports | ✅ Always | 1m |
| 51 | Naming | naming | ✅ Always | 1m |
| 52 | Error Handling | error-handling | ✅ Always | 2m |

#### Performance (10 checks)
| #  | Check | Slug | Status | Time |
|----|-------|------|--------|------|
| 53 | Slow Operations | slow-ops | ✅ Always | 2m |
| 54 | Bundle Size | bundle | ⊘ No frontend | - |
| 55 | Missing Cache | no-cache | ✅ Always | 2m |
| 56 | Circuit Breakers | circuit | ✅ HTTP | 1m |
| 57 | Memory Leaks | mem-leaks | ✅ Always | 2m |
| 58 | Bad Algorithms | algorithms | ✅ Always | 2m |
| 59 | Large Loops | large-loops | ✅ Always | 1m |
| 60 | File I/O | file-io | ✅ File ops | 1m |
| 61 | Network in Loops | net-loops | ✅ HTTP | 1m |
| 62 | Lazy Loading | lazy | ⊘ No frontend | - |

#### CI/CD (8 checks)
| #  | Check | Slug | Status | Time |
|----|-------|------|--------|------|
| 63 | Pipeline Exists | pipeline | ✅ GH Actions | 1m |
| 64 | Quality Gates | gates | ✅ Pipeline | 1m |
| 65 | Secret Management | ci-secrets | ✅ Pipeline | 1m |
| 66 | Build Optimization | build-optim | ✅ Pipeline | 1m |
| 67 | Test Automation | test-auto | ✅ Pipeline | 1m |
| 68 | Deploy Automation | deploy-auto | ✅ Pipeline | 1m |
| 69 | Rollback Strategy | rollback | ✅ Deploy | 1m |
| 70 | Env Parity | env-parity | ✅ Envs | 1m |

### 🟢 MEDIUM IMPACT

#### Documentation (8 checks)
| #  | Check | Slug | Status | Time |
|----|-------|------|--------|------|
| 71 | Missing Docstrings | docstrings | ✅ Always | 1m |
| 72 | API Docs | api-docs | ✅ Routes | 1m |
| 73 | README Quality | readme | ✅ Always | 1m |
| 74 | Doc Drift | doc-drift | ✅ docs/ | 1m |
| 75 | Code Comments | comments | ✅ Always | 1m |
| 76 | Examples | examples | ✅ docs/ | 1m |
| 77 | ADRs | adrs | ✅ Always | 1m |
| 78 | Runbooks | runbooks | ✅ Prod app | 1m |

#### Containers (6 checks)
| #  | Check | Slug | Status | Time |
|----|-------|------|--------|------|
| 79 | Dockerfile Best Practices | dockerfile | ✅ Docker | 1m |
| 80 | Multi-stage Builds | multistage | ✅ Dockerfile | 1m |
| 81 | Non-root User | nonroot | ✅ Dockerfile | 1m |
| 82 | Image Size | image-size | ✅ Dockerfile | 1m |
| 83 | Base Image CVEs | base-cves | ✅ Dockerfile | 2m |
| 84 | Layer Optimization | layers | ✅ Dockerfile | 1m |

#### Tech Debt (8 checks)
| #  | Check | Slug | Status | Time |
|----|-------|------|--------|------|
| 85 | Deprecated APIs | deprecated | ✅ Always | 2m |
| 86 | Legacy Code | legacy | ✅ Always | 2m |
| 87 | Hard Dependencies | hard-deps | ✅ Always | 1m |
| 88 | Tight Coupling | coupling | ✅ Always | 2m |
| 89 | God Objects | god-objects | ✅ Classes | 2m |
| 90 | Feature Envy | feature-envy | ✅ Classes | 1m |
| 91 | Data Clumps | data-clumps | ✅ Always | 1m |
| 92 | Shotgun Surgery | shotgun | ✅ Always | 2m |

---

**Summary:** {TOTAL_CHECKS} total, {APPLICABLE_COUNT} applicable (✅), {NA_COUNT} not applicable (⊘)
```

---

## Component 4: Selection Input

### Quick Presets Mode

```python
AskUserQuestion({
  questions: [{
    question: "Select a preset audit:",
    header: "Presets",
    multiSelect: false,
    options: [
      {
        label: "Pre-Commit",
        description: "Quick checks (secrets, linting, TODOs) - 5 min"
      },
      {
        label: "Security Scan",
        description: "All security checks - 15 min"
      },
      {
        label: "Pre-Deploy",
        description: "Security + Performance + DB - 25 min"
      },
      {
        label: "Full Weekly",
        description: "All applicable checks - 60+ min"
      }
    ]
  }]
})
```

**Preset Definitions:**

```yaml
presets:
  # === Quick Single-Purpose ===
  lint-only:
    checks: [42]
    time: "1 min"
    description: "Linting issues only"

  types-only:
    checks: [41]
    time: "1 min"
    description: "Type errors only"

  secrets-only:
    checks: [4, 25]
    time: "1 min"
    description: "Hardcoded secrets only"

  complexity-only:
    checks: [39, 44, 45, 46]
    time: "2 min"
    description: "Complexity issues only"

  # === Workflow-Based ===
  pre-commit:
    checks: [4, 41, 42, 48, 49, 50, 51]
    time: "3-5 min"
    description: "Quick checks before commit (secrets, lint, types, TODOs)"

  pre-push:
    checks: [1, 2, 4, 5, 6, 16, 17, 41, 42]
    time: "8-10 min"
    description: "Thorough check before push (security basics, DB issues, quality)"

  pre-deploy:
    categories: [security, database, performance]
    time: "20-25 min"
    description: "Production readiness (security, DB, performance)"

  pre-merge:
    checks: [1-15, 38-52]
    time: "15-20 min"
    description: "PR review checks (security + code quality)"

  # === Domain-Focused ===
  security:
    checks: [1-15]
    time: "12-15 min"
    description: "All security checks"

  database:
    checks: [16-25]
    time: "10-12 min"
    description: "All database checks"

  tests:
    checks: [26-37]
    time: "10-12 min"
    description: "All test quality checks"

  quality:
    checks: [38-52]
    time: "12-15 min"
    description: "All code quality checks"

  performance:
    checks: [53-62]
    time: "8-10 min"
    description: "All performance checks"

  # === Comprehensive ===
  critical:
    categories: [security, database, tests]
    time: "30-35 min"
    description: "All critical categories"

  weekly:
    selection: "all"
    time: "60-90 min"
    description: "Comprehensive full review"
```

### Category Mode

```python
AskUserQuestion({
  questions: [
    {
      question: "Select Critical Impact categories:",
      header: "🔴 Critical",
      multiSelect: true,
      options: [
        {label: "All Critical", description: "Select all critical impact categories"},
        {label: "Security", description: "Security checks - SQLi, XSS, secrets, CVEs"},
        {label: "Database", description: "Database checks - N+1, indexes, queries"},
        {label: "Tests", description: "Test checks - coverage, isolation, pyramid"}
      ]
    },
    {
      question: "Select High Impact categories:",
      header: "🟡 High",
      multiSelect: true,
      options: [
        {label: "All High", description: "Select all high impact categories"},
        {label: "Code Quality", description: "Quality checks - complexity, dead code"},
        {label: "Performance", description: "Performance checks - caching, algorithms"},
        {label: "CI/CD", description: "CI/CD checks - pipeline, gates, deploy"}
      ]
    },
    {
      question: "Select Medium Impact categories:",
      header: "🟢 Medium",
      multiSelect: true,
      options: [
        {label: "All Medium", description: "Select all medium impact categories"},
        {label: "Documentation", description: "Doc checks - docstrings, API docs"},
        {label: "Containers", description: "Container checks - Dockerfile, security"},
        {label: "Tech Debt", description: "Debt checks - coupling, legacy code"}
      ]
    }
  ]
})
```

### Full Control Mode

**Display full checklist (Component 3), then:**

```markdown
## Selection Syntax

**Simple:**
```
all                 All applicable checks
critical            Security + Database + Tests
security            All security checks
```

**Presets:**
```
@pre-commit         Quick pre-commit (5 min)
@pre-deploy         Pre-deployment (25 min)
@weekly             Full review (60+ min)
```

**By category:**
```
security            Single category
security,database   Multiple categories
```

**By number:**
```
1,2,4,16            Specific checks
1-15                Range
1-15,26-37          Multiple ranges
```

**By slug:**
```
sql-injection       Single check
n1-queries,xss      Multiple checks
```

**Exclusions:**
```
all -3 -8           All except #3 and #8
security -csrf      Security except CSRF
```

**Combined:**
```
security,16-25      Category + range
@critical -8        Preset minus check
```

---

Enter your selection: _
```

### Selection Parser

```python
def parse_selection(input_str: str, checks: List[Check]) -> SelectionResult:
    """Parse flexible selection syntax into check list."""

    tokens = input_str.lower().split(',')
    selected = set()
    excluded = set()
    errors = []

    for token in tokens:
        token = token.strip()

        # Exclusion
        if token.startswith('-'):
            excluded.update(resolve(token[1:], checks))
            continue

        # Preset
        if token.startswith('@'):
            preset = PRESETS.get(token[1:])
            if preset:
                selected.update(preset.checks)
            else:
                errors.append(f"Unknown preset: {token}")
            continue

        # Keywords
        if token == 'all':
            selected.update(c.id for c in checks if c.applicable)
            continue
        if token == 'critical':
            selected.update(c.id for c in checks if c.category in ['security', 'database', 'tests'])
            continue

        # Category name
        if token in CATEGORIES:
            selected.update(c.id for c in checks if c.category == token)
            continue

        # Range: 1-15
        if '-' in token and token[0].isdigit():
            try:
                start, end = map(int, token.split('-'))
                selected.update(range(start, end + 1))
            except:
                errors.append(f"Invalid range: {token}")
            continue

        # Single number
        if token.isdigit():
            num = int(token)
            if 1 <= num <= TOTAL_CHECKS:
                selected.add(num)
            else:
                errors.append(f"Invalid number: {token}")
            continue

        # Slug name
        check = next((c for c in checks if c.slug == token), None)
        if check:
            selected.add(check.id)
        else:
            errors.append(f"Unknown: {token}")

    # Apply exclusions
    final = selected - excluded

    # Filter to applicable only
    final = {n for n in final if checks[n-1].applicable}

    return SelectionResult(
        selected=sorted(final),
        excluded=sorted(excluded),
        errors=errors
    )
```

---

## Component 5: Pre-Flight Summary

**Show EXACTLY what will happen before execution. No surprises.**

```markdown
## Pre-Flight Summary

### Selection Overview

┌─────────────────────────────────────────────────┐
│ SELECTED: {COUNT} checks                        │
├─────────────────────────────────────────────────┤
│ 🔴 Security        {SELECTED}/{CATEGORY_TOTAL} checks    ~{T} min    │
│    └─ {list of check numbers}                   │
│                                                 │
│ 🔴 Database        {SELECTED}/{CATEGORY_TOTAL} checks    ~{T} min    │
│    └─ {list of check numbers}                   │
│                                                 │
│ 🔴 Tests           {SELECTED}/{CATEGORY_TOTAL} checks    ~{T} min    │
│    └─ {list of check numbers}                   │
├─────────────────────────────────────────────────┤
│ Total time: {MIN}-{MAX} minutes                 │
└─────────────────────────────────────────────────┘

### What's NOT Running

**Not Applicable ({COUNT}):**
- #{N} {Name} - {Reason}
- #{N} {Name} - {Reason}
...

**Manually Excluded ({COUNT}):**
- #{N} {Name}
...

**Other Categories ({COUNT}):**
- Code Quality, Performance, CI/CD, etc.

### Execution Plan

**Phase 1: Setup** (~30s)
- Load skills: {list}
- Discover files: {count} files
- Initialize tools: {list}

**Phase 2: Scanning** (~{TIME} min)
- {Category}: {count} checks (parallel)
- {Category}: {count} checks (parallel)
...

**Phase 3: Synthesis** (~2 min)
- Aggregate findings
- Calculate scores
- Generate report

### Confirmation
```

```python
AskUserQuestion({
  questions: [{
    question: "Ready to start audit?",
    header: "Confirm",
    multiSelect: false,
    options: [
      {
        label: "Start Audit",
        description: f"Run {count} checks (~{time} min)"
      },
      {
        label: "Modify Selection",
        description: "Change selected checks"
      },
      {
        label: "Cancel",
        description: "Exit without running"
      }
    ]
  }]
})
```

---

## Component 6: State Management & Count Tracking

**CRITICAL: All UX issues stem from inconsistent state and count management.**

### Single Source of Truth

```python
@dataclass
class AuditState:
    """Central state object - ONLY source for all counts and status."""

    # Phase tracking
    current_phase: int = 0  # 0=not started, 1=setup, 2=scanning, 3=synthesis
    phase_start_times: Dict[int, datetime] = field(default_factory=dict)
    phase_end_times: Dict[int, datetime] = field(default_factory=dict)

    # Count tracking - NEVER derive these, always update explicitly
    total_findings: int = 0
    findings_by_severity: Dict[str, int] = field(default_factory=lambda: {
        "critical": 0, "high": 0, "medium": 0, "low": 0
    })

    # Complete accounting - track ALL items
    all_findings: List[Finding] = field(default_factory=list)

    def add_finding(self, finding: Finding):
        """Single method to add findings - maintains consistency."""
        self.all_findings.append(finding)
        self.total_findings += 1
        self.findings_by_severity[finding.severity] += 1

    def get_counts_string(self) -> str:
        """ALWAYS use this for displaying counts - ensures consistency."""
        return (f"{self.total_findings} issues "
                f"({self.findings_by_severity['critical']} critical, "
                f"{self.findings_by_severity['high']} high, "
                f"{self.findings_by_severity['medium']} medium)")

# Global state - initialized once, used everywhere
AUDIT_STATE = AuditState()
```

### Phase State Machine

**RULE: Every phase transition MUST be explicitly announced.**

```python
def transition_phase(state: AuditState, new_phase: int):
    """Explicit phase transition with required announcements."""

    old_phase = state.current_phase

    # End current phase
    if old_phase > 0:
        state.phase_end_times[old_phase] = datetime.now()
        duration = state.phase_end_times[old_phase] - state.phase_start_times[old_phase]

        # MUST announce phase completion
        print(format_phase_complete(old_phase, duration))

    # Start new phase
    state.current_phase = new_phase
    state.phase_start_times[new_phase] = datetime.now()

    # MUST announce phase start
    print(format_phase_start(new_phase))

def format_phase_start(phase: int) -> str:
    """Format phase start announcement."""
    phase_names = {1: "Setup", 2: "Scanning", 3: "Synthesis"}
    return f"""
───────────────────────────────────────────────────
### Phase {phase}/3: {phase_names[phase]} ▶ STARTED
───────────────────────────────────────────────────
"""

def format_phase_complete(phase: int, duration: timedelta) -> str:
    """Format phase completion announcement."""
    phase_names = {1: "Setup", 2: "Scanning", 3: "Synthesis"}
    return f"""
### Phase {phase}/3: {phase_names[phase]} ✓ COMPLETE ({format_duration(duration)})
"""
```

---

## Component 7: Execution Dashboard

**Real-time visibility with EXPLICIT phase transitions.**

### Initial Display

```markdown
## Audit Execution

**Started:** {TIME}
**Selection:** {COUNT} checks ({CATEGORIES})

───────────────────────────────────────────────────
### Phase 1/3: Setup ▶ STARTED
───────────────────────────────────────────────────

⠋ Loading skills...
⠋ Discovering files...
⠋ Initializing scanners...
```

### Phase 1 Complete → Phase 2 Start

**CRITICAL: Must show BOTH completion AND start.**

```markdown
### Phase 1/3: Setup ✓ COMPLETE (12s)

Skills loaded: {count}
Files discovered: {count}
Scanners initialized: {count}

───────────────────────────────────────────────────
### Phase 2/3: Scanning ▶ STARTED
───────────────────────────────────────────────────

Elapsed: 0:00 | Estimated: ~{TIME}

{Category}  ░░░░░░░░░░░░ 0% (0/{Y} checks)
{Category}  ░░░░░░░░░░░░ queued
{Category}  ░░░░░░░░░░░░ queued

Current: Initializing {first_category}...
```

### During Scanning (Progress Updates)

```markdown
### Phase 2/3: Scanning (in progress)

Elapsed: {TIME} | Remaining: ~{TIME}

Security     ████████████ 100% (15/15 checks) ✓
Database     ████████░░░░  67% (7/10 checks)
Tests        ░░░░░░░░░░░░   0% (queued)

Current: Checking {CHECK_NAME} in {FILE_PATH}

### Findings So Far: {TOTAL}

🔴 CRITICAL ({COUNT}):
├─ {ISSUE_TYPE} in {FILE_PATH}:{LINE_NUMBER}
└─ {ISSUE_TYPE} in {FILE_PATH}:{LINE_NUMBER}

🟡 HIGH ({COUNT}):
├─ {ISSUE_TYPE} in {FILE_PATH}:{LINE_NUMBER}
└─ {ISSUE_TYPE} on {TABLE_NAME}.{COLUMN_NAME}
```

### Phase 2 Complete → Phase 3 Start

```markdown
### Phase 2/3: Scanning ✓ COMPLETE (8m 32s)

Checks completed: {X}/{Y}
Files scanned: {count}
Issues found: {total} ({critical} critical, {high} high, {medium} medium)

───────────────────────────────────────────────────
### Phase 3/3: Synthesis ▶ STARTED
───────────────────────────────────────────────────

⠋ Aggregating findings...
⠋ Calculating scores...
⠋ Generating report...
```

### Phase 3 Complete → Audit Complete

```markdown
### Phase 3/3: Synthesis ✓ COMPLETE (45s)

───────────────────────────────────────────────────
## Audit Complete
───────────────────────────────────────────────────

**Total Duration:** {TOTAL_TIME}
**Checks Run:** {COUNT}
**Issues Found:** {TOTAL} ({critical} critical, {high} high, {medium} medium)
**Score:** {SCORE}/100 (Grade: {GRADE})
```

---

## Component 8: Count Consistency Rules

**CRITICAL: These rules prevent the 30+ vs 50+ inconsistency.**

### Rule 1: Single Count Source
```python
# ❌ BAD: Deriving counts differently
print(f"Found {len(critical_findings)} critical")  # One place
print(f"Critical: {state.critical_count}")          # Another place

# ✅ GOOD: Always use state method
print(state.get_counts_string())  # SAME everywhere
```

### Rule 2: No Filtering Without Explanation
```python
# ❌ BAD: Silently filter
displayed = [f for f in findings if f.severity != "low"]
print(f"Issues: {len(displayed)}")  # User sees 30

# Later...
print(f"Total: {len(all_findings)}")  # User sees 50 - CONFUSION!

# ✅ GOOD: Explain any filtering
print(f"Issues: {len(all_findings)} total")
print(f"  Showing: {len(displayed)} (hiding {len(low)} low-severity)")
```

### Rule 3: Complete Accounting in Summary
```markdown
## Final Count Summary

**Total Issues Found:** 50

By Severity:
- 🔴 Critical: 5
- 🟡 High: 12
- 🟢 Medium: 18
- ⚪ Low: 15 (not shown in detail)

**Note:** Low-severity issues are counted but not detailed.
Run with `--include-low` to see all.
```

### Rule 4: Fix Process Accounting

**When user says "fix all", show complete accounting:**

```markdown
## Fix Summary

**Total Issues:** 50

### Fixed Successfully: 35
- 5 critical (100%)
- 10 high (83%)
- 15 medium (83%)
- 5 low (33%)

### Skipped: 10
- 3 require manual review (complex logic)
- 4 need user decision (multiple fix options)
- 3 already fixed by earlier fixes

### Cannot Fix Automatically: 5
- 2 require database migration
- 2 need external service configuration
- 1 requires architectural change

───────────────────────────────────────────────────

**Verification:** 35 fixed + 10 skipped + 5 cannot-fix = 50 total ✓
```

---

## Component 9: Honesty & Accurate Reporting

**CRITICAL PRINCIPLE: Always report the exact truth. No optimistic claims, no false limitations.**

### Core Rules

```python
# ❌ NEVER: Claim something fixed when not fixed
"Fixed {ISSUE_TYPE} in {FILE_PATH}:{LINE_NUMBER}"  # But file unchanged

# ✅ ALWAYS: Report actual outcome
f"Applied fix to {finding.file}:{finding.line} - {fix_description}"
# Then VERIFY: Read file, confirm change exists

# ❌ NEVER: Say "not possible" when technically possible
"Cannot fix: Complex regex pattern"  # It's possible, just needs care

# ✅ ALWAYS: Distinguish difficulty from impossibility
"Requires careful review: Complex regex with edge cases"
"Recommendation: Manual fix with test coverage"

# ❌ NEVER: Imply fixability when truly impossible
"Can fix: Database migration needed"  # Can't auto-migrate production

# ✅ ALWAYS: Be clear about actual limitations
"Requires manual action: Database schema change needs migration"
"This tool cannot modify production databases"
```

### Accurate Categorization

```python
@dataclass
class FixOutcome:
    """Strictly accurate outcome categories."""

    # Truly fixed - file modified, verified
    FIXED = "fixed"

    # Technically possible but needs human decision
    NEEDS_DECISION = "needs_decision"  # Multiple valid approaches
    NEEDS_REVIEW = "needs_review"      # Complex, risk of regression

    # Technically possible but outside tool scope
    REQUIRES_MIGRATION = "requires_migration"   # DB schema change
    REQUIRES_CONFIG = "requires_config"         # External system config
    REQUIRES_INFRA = "requires_infra"           # Infrastructure change

    # Truly impossible to auto-fix
    IMPOSSIBLE_DESIGN = "impossible_design"     # Architectural flaw
    IMPOSSIBLE_EXTERNAL = "impossible_external" # Third-party code
    IMPOSSIBLE_RUNTIME = "impossible_runtime"   # Runtime-only issue

def categorize_fix(finding: Finding) -> Tuple[str, str]:
    """Return accurate category and honest explanation."""

    # Example: Type error in third-party library
    if finding.file.startswith("node_modules/"):
        return (FixOutcome.IMPOSSIBLE_EXTERNAL,
                "Issue in third-party code - update package or report upstream")

    # Example: N+1 query that's actually intentional
    if finding.check_id == 16 and is_intentional_eager_load(finding):
        return (FixOutcome.NEEDS_REVIEW,
                "Pattern appears intentional - verify before changing")

    # Example: Complex regex
    if finding.check_id == 42 and "regex" in finding.code.lower():
        return (FixOutcome.NEEDS_DECISION,
                "Multiple valid regex patterns - choose based on requirements")

    # Default: actually fixable
    return (FixOutcome.FIXED, "Applied automated fix")
```

### Honest Reporting Templates

**When truly fixed:**
```markdown
✅ **Fixed:** {ISSUE_TYPE} in {FILE_PATH}:{LINE_NUMBER}
   Applied: {FIX_DESCRIPTION}
   Verified: File updated, syntax valid
```

**When needs human decision:**
```markdown
⚠️ **Needs Decision:** {ISSUE_TYPE} in {FILE_PATH}:{LINE_NUMBER}
   Issue: {ISSUE_DESCRIPTION}
   Options:
   - Option A: {OPTION_A_DESCRIPTION}
   - Option B: {OPTION_B_DESCRIPTION}
   Action: Choose option based on user requirements
```

**When outside tool scope:**
```markdown
🔧 **Requires Manual Action:** {ISSUE_TYPE} on {TABLE_NAME}.{COLUMN_NAME}
   Issue: {ISSUE_DESCRIPTION}
   Why not auto-fixed: {REASON}
   Action: {MANUAL_ACTION_DESCRIPTION}
```

**When truly impossible:**
```markdown
❌ **Cannot Auto-Fix:** {ISSUE_TYPE} in {EXTERNAL_COMPONENT}
   Issue: {ISSUE_DESCRIPTION}
   Why impossible: {REASON}
   Action: {RECOMMENDED_ACTION}
```

### Verification Requirements

```python
def report_fix(finding: Finding, outcome: str, explanation: str):
    """Report fix outcome with verification."""

    if outcome == FixOutcome.FIXED:
        # MUST verify before claiming fixed
        file_content = Read(finding.file)
        if not verify_fix_applied(file_content, finding):
            raise AssertionError(
                f"HONESTY VIOLATION: Claimed fixed but change not found in {finding.file}"
            )

    # Report with accurate category
    return format_outcome(finding, outcome, explanation)
```

---

## Component 10: Fix Integration Accounting

**When /cco-fix is called after audit, maintain complete accountability with honest reporting.**

### Fix Request Flow

```python
@dataclass
class FixState:
    """Track all fix outcomes."""

    total_issues: int = 0

    # Dispositions - MUST sum to total_issues
    fixed: List[Finding] = field(default_factory=list)
    skipped: List[Tuple[Finding, str]] = field(default_factory=list)  # (finding, reason)
    cannot_fix: List[Tuple[Finding, str]] = field(default_factory=list)  # (finding, reason)

    def verify_accounting(self) -> bool:
        """Verify all issues are accounted for."""
        accounted = len(self.fixed) + len(self.skipped) + len(self.cannot_fix)
        return accounted == self.total_issues

    def get_summary(self) -> str:
        """Get complete accounting summary."""
        assert self.verify_accounting(), "Accounting mismatch!"

        return f"""
## Fix Summary

**Total Issues:** {self.total_issues}

### ✅ Fixed: {len(self.fixed)}
{self._format_list(self.fixed)}

### ⏭️ Skipped: {len(self.skipped)}
{self._format_with_reasons(self.skipped)}

### ❌ Cannot Fix Automatically: {len(self.cannot_fix)}
{self._format_with_reasons(self.cannot_fix)}

───────────────────────────────────────────────────
**Verification:** {len(self.fixed)} + {len(self.skipped)} + {len(self.cannot_fix)} = {self.total_issues} ✓
"""
```

### "Fix All" Response Template

```markdown
## Fixing All Issues

**Source:** audit-2025-01-15.json
**Total Issues:** 50

───────────────────────────────────────────────────

### Analyzing fixability...

**Auto-fixable:** 35 issues
**Requires review:** 10 issues
**Cannot auto-fix:** 5 issues

───────────────────────────────────────────────────

### Proceed with auto-fixes?

This will fix 35 of 50 issues automatically.
The remaining 15 will be listed with reasons.

[Fix 35 Auto-fixable] [Review All First] [Cancel]
```

### After Fixes Complete

```markdown
## Fix Complete

### ✅ Fixed Successfully: 35

By severity:
- 🔴 Critical: 5/5 (100%)
- 🟡 High: 10/12 (83%)
- 🟢 Medium: 15/18 (83%)
- ⚪ Low: 5/15 (33%)

### ⏭️ Skipped: {SKIPPED_COUNT}

| Issue | File | Reason |
|-------|------|--------|
| {ISSUE_TYPE} | {FILE_PATH}:{LINE_NUMBER} | {SKIP_REASON} |
| {ISSUE_TYPE} | {FILE_PATH}:{LINE_NUMBER} | {SKIP_REASON} |
| ... | ... | ... |

### ❌ Cannot Fix Automatically: {CANNOT_FIX_COUNT}

| Issue | File | Reason | Manual Action |
|-------|------|--------|---------------|
| {ISSUE_TYPE} | {FILE_PATH}:{LINE_NUMBER} | {REASON} | {MANUAL_ACTION} |
| {ISSUE_TYPE} | {FILE_PATH}:{LINE_NUMBER} | {REASON} | {MANUAL_ACTION} |
| ... | ... | ... | ... |

───────────────────────────────────────────────────

## Next Steps

1. **Review skipped issues:** 10 items need your decision
2. **Handle manual fixes:** 5 items need manual action
3. **Re-run audit:** Verify fixes with `/cco-audit --checks="{affected_checks}"`

**Projected Score After Manual Fixes:** [BEFORE] → [AFTER] (+[DELTA] points)
```

---

## Component 7: Final Report

**Actionable, prioritized results with clear next steps.**

```markdown
═══════════════════════════════════════════════════════════════
                         AUDIT REPORT
═══════════════════════════════════════════════════════════════

## Executive Summary

**Score:** {SCORE}/100 (Grade: {GRADE})
**Risk Level:** {LEVEL} - {DESCRIPTION}

| Category | Score | Issues | Status |
|----------|-------|--------|--------|
| Security | {X}/100 | {N} | {STATUS} |
| Database | {X}/100 | {N} | {STATUS} |
| Tests | {X}/100 | {N} | {STATUS} |

**Top Concerns:**
1. {Issue description}
2. {Issue description}
3. {Issue description}

───────────────────────────────────────────────────────────────

## Critical Issues ({COUNT})

### {N}. {Issue Type} - {file}:{line}

**Severity:** 🔴 CRITICAL
**Category:** {Category}
**Check:** #{N} {Check Name}

**Vulnerable Code:**
```{lang}
# {file}:{line}
{actual code snippet}
```

**Risk:** {Explanation of what could go wrong}

**Fix:**
```{lang}
{corrected code}
```

**Command:** `/cco-fix --check={N} --file={file}`

---

[Repeat for each critical issue]

───────────────────────────────────────────────────────────────

## High Priority Issues ({COUNT})

### {N}. {Issue Type} - {file}:{line}
```{lang}
{code snippet}
```
**Fix:** {Brief fix description}
**Command:** `/cco-fix --check={N} --file={file}`

[Repeat for each high issue]

───────────────────────────────────────────────────────────────

## Medium Priority Issues ({COUNT})

### {N}. {Issue Type} - {file}:{line}
**Fix:** {Brief description}
**Command:** `/cco-fix --check={N} --file={file}`

[Repeat for each medium issue]

───────────────────────────────────────────────────────────────

## Recommended Actions

### P0 - Fix Now (Critical)
**Issues:** {count} critical vulnerabilities
**Time:** ~{time}
**Command:**
```bash
/cco-fix --critical
```

### P1 - Fix This Week (High)
**Issues:** {count} high priority
**Time:** ~{time}
**Command:**
```bash
/cco-fix --high
```

### P2 - Fix This Sprint (Medium)
**Issues:** {count} medium priority
**Time:** ~{time}
**Command:**
```bash
/cco-fix --medium
```

───────────────────────────────────────────────────────────────

## Score Improvement

| Action | Issues | Impact |
|--------|--------|--------|
| Fix critical | {N} | +{X} pts |
| Fix high | {N} | +{X} pts |
| Fix medium | {N} | +{X} pts |
| **Total** | **{N}** | **{X} → {Y}** |

───────────────────────────────────────────────────────────────

## Re-run Audit

After fixes, verify:
```bash
/cco-audit --checks="{list of check numbers that had issues}"
```

Expected: 0 issues → Score: {projected}/100

═══════════════════════════════════════════════════════════════
```

---

## Agent Orchestration

### 6-Aspect Parallel Audit

For comprehensive audits (`--all`, `--preset=weekly`, `--preset=critical`), use 6 specialized parallel agents:

```python
# Launch 6 aspect-focused agents in parallel
Task({
    subagent_type: "audit-agent",
    model: "sonnet",
    description: "Security audit",
    prompt: """
    Focus: Security vulnerabilities
    Checks: SQL injection, XSS, CSRF, secrets, auth, CVEs
    Skill: cco-skill-security-owasp
    Return: Findings with severity, file:line, risk, fix
    """
})

Task({
    subagent_type: "audit-agent",
    model: "haiku",
    description: "Performance audit",
    prompt: """
    Focus: Performance bottlenecks
    Checks: N+1 queries, missing indexes, no caching, slow algorithms
    Skill: cco-skill-database-optimization
    Return: Findings with impact metrics, file:line, optimization
    """
})

Task({
    subagent_type: "audit-agent",
    model: "sonnet",
    description: "Test coverage audit",
    prompt: """
    Focus: Testing gaps
    Checks: Coverage, untested functions, isolation, pyramid
    Skill: cco-skill-test-pyramid
    Return: Findings with coverage %, critical untested paths
    """
})

Task({
    subagent_type: "audit-agent",
    model: "haiku",
    description: "Code quality audit",
    prompt: """
    Focus: Code quality issues
    Checks: Complexity, dead code, duplication, smells
    Skill: cco-skill-code-quality
    Return: Findings with metrics (CC, LOC), file:line, refactor suggestion
    """
})

Task({
    subagent_type: "audit-agent",
    model: "sonnet",
    description: "Architecture audit",
    prompt: """
    Focus: Architecture concerns
    Checks: Coupling, patterns, boundaries, dependencies
    Skill: cco-skill-microservices-cqrs
    Return: Findings with design issue, impact, restructure suggestion
    """
})

Task({
    subagent_type: "audit-agent",
    model: "haiku",
    description: "Documentation audit",
    prompt: """
    Focus: Documentation gaps
    Checks: Docstrings, API docs, README, ADRs
    Skill: cco-skill-docs-api-openapi
    Return: Findings with missing doc type, file:line, template
    """
})

# Synthesis agent (waits for all 6 to complete)
Task({
    subagent_type: "audit-agent",
    model: "sonnet",
    description: "Synthesize findings",
    prompt: """
    Aggregate all 6 aspect findings:
    - Deduplicate overlapping issues
    - Calculate overall score
    - Prioritize by severity and impact
    - Generate unified report
    """
})
```

**Benefits of 6-Aspect Approach:**
- Parallel = faster (6 agents simultaneously vs sequential)
- Specialized = more accurate (each agent focuses on one domain)
- Complete = nothing missed (all aspects covered)

### Model Selection by Aspect

| Aspect | Model | Rationale |
|--------|-------|-----------|
| Security | Sonnet | Semantic analysis, context-aware vulnerability detection |
| Performance | Haiku | Pattern matching, metrics collection |
| Testing | Sonnet | Coverage analysis, critical path identification |
| Quality | Haiku | Metrics calculation, pattern detection |
| Architecture | Sonnet | Design pattern recognition, coupling analysis |
| Documentation | Haiku | Presence checks, template matching |

### Single-Category Execution

For single-category audits (`--preset=security`, `--preset=database`), use direct execution:

```python
# Single category = one focused agent
Task({
    subagent_type: "audit-agent",
    model: "sonnet",  # or haiku based on category
    description: f"{category} audit",
    prompt: generate_category_prompt(category, checks)
})
```

### Cost Optimization

```
6-Aspect Parallel (comprehensive):
├── Haiku agents: lower cost
├── Sonnet agents: balanced cost
├── Sonnet synthesis
└── Total: cost-efficient

vs All-Sonnet Sequential:
└── Total: significantly more expensive and slower
```

---

## CLI Usage

### Interactive (Default)
```bash
/cco-audit
```

### Parametrized (Power Users)

**Presets:**
```bash
/cco-audit --preset=pre-commit
/cco-audit --preset=security
/cco-audit --preset=pre-deploy
/cco-audit --preset=weekly
```

**Categories:**
```bash
/cco-audit --security
/cco-audit --security --database --tests
/cco-audit --all
```

**Specific checks:**
```bash
/cco-audit --checks="1,2,4,16-25"
/cco-audit --checks="sql-injection,n1-queries"
```

**Exclusions:**
```bash
/cco-audit --all --exclude="3,8,10"
```

---

## Error Handling

### Selection Errors

```markdown
## Selection Error

**Input:** `security,99,unknown`

**Issues:**
- `99` - Invalid (max: {TOTAL_CHECKS})
- `unknown` - Check not found

**Try:**
- `security` - Category
- `1-15` - Range
- `sql-injection` - Slug

Enter selection: _
```

### Empty Selection

```markdown
## No Checks Selected

Selection resulted in 0 checks.

**Reason:** All selected checks not applicable

**Try:**
- `all` - All applicable
- `@pre-commit` - Quick preset
- Remove exclusions

Enter selection: _
```

### Long Execution Warning

```markdown
## Long Execution

**Selected:** {SELECTED_COUNT} checks (~{TIME_ESTIMATE})

Consider smaller selection:
- `@critical` - 35 min
- `@pre-deploy` - 25 min

[Continue] [Smaller Selection]
```

---

## Success Criteria

- [ ] Mode selection presented
- [ ] Discovery phase completed
- [ ] Full checklist shown (Full Control mode)
- [ ] Selection parsed correctly
- [ ] Pre-flight summary displayed
- [ ] User confirmed execution
- [ ] Execution dashboard showed real-time progress
- [ ] Findings streamed as discovered
- [ ] Final report generated with all sections
- [ ] Next action commands provided
