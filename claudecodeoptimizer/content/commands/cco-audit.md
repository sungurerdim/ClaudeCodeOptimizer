---
name: cco-audit
description: Comprehensive codebase audit with full transparency and real-time progress
action_type: audit
principles: [U_EVIDENCE_BASED_ANALYSIS, U_CHANGE_VERIFICATION, U_MINIMAL_TOUCH]
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
  ai-quality:
    keywords: [ai quality audit, ai hallucination scan, api hallucination check, code bloat scan, vibe coding check, copilot quality]
    category: quality
    pain_points: [3, 8, 9]
  ai-debt:
    keywords: [ai debt audit, ai generated debt, ai code quality, ai technical debt]
    category: quality
    pain_points: [2, 3]
  code-review:
    keywords: [code review audit, pr quality check, review quality scan, commit quality check, dora metrics]
    category: quality
    pain_points: [11, 12]
  platform:
    keywords: [platform audit, cicd maturity, test automation check, iac scan, dx audit, ai readiness]
    category: infrastructure
    pain_points: [4, 6, 10]
  ai:
    keywords: [ai audit, complete ai scan, ai security and quality, ai comprehensive check]
    category: meta
    pain_points: [2, 3, 8, 9]
    meta_flags: [ai-quality, ai-debt, ai-security]
  critical:
    keywords: [critical audit, essential checks, must-fix, high priority scan]
    category: meta
    pain_points: [1, 3, 4, 5]
    meta_flags: [security, ai-security, database, tests]
  production-ready:
    keywords: [production ready audit, deploy readiness, pre-deploy check, production checklist]
    category: meta
    pain_points: [1, 4, 5, 7]
    meta_flags: [security, performance, database, tests, docs]
  code-health:
    keywords: [code health audit, quality focus, maintainability check, code cleanliness]
    category: meta
    pain_points: [2, 4, 7]
    meta_flags: [tech-debt, code-quality, tests, docs]
  team-metrics:
    keywords: [team metrics audit, collaboration check, platform maturity, team performance]
    category: meta
    pain_points: [6, 10, 11, 12]
    meta_flags: [code-review, platform, cicd]
---

# CCO Audit Command

**Comprehensive codebase analysis with full transparency, flexible selection, and real-time progress.**

---

## Execution Guarantee

**This command WILL execute fully without requiring user presence during processing.**

**What Happens:**
1. **Step 0**: Introduction and mode selection (user input required)
2. **Step 0.5**: Project context discovery (optional, user choice)
3. **Discovery**: Tech detection and check applicability (automated)
4. **Selection**: Check selection based on mode (automated or user input)
5. **Pre-Flight**: Summary and confirmation (user input required)
6. **Execution**: Run selected checks with real-time progress (fully automated)
7. **Final Report**: Prioritized findings with action plan (automated)

**User Interaction Points:**
- Mode selection (Quick/Category/Full Control)
- Project context discovery (optional)
- Check selection (if Category/Full Control modes)
- Pre-flight confirmation
- Agent error handling (if failures occur)

**Automation:**
- All checks run without interruption
- Streaming results displayed in real-time
- Complete accounting enforced (total issues = reported + verified)
- Agents handle audit execution in parallel

**Time Estimate:**
- Quick Mode: 3-8 minutes
- Category Mode: 5-15 minutes
- Full Control: 10-30 minutes (depends on checks selected)

**Verification:**
- All findings verified (no false positives)
- File-level accounting enforced
- Complete transparency into execution progress

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

**AI models interpret hardcoded examples as real data. Use placeholders: `{FILE_PATH}`, `{LINE_NUMBER}`, `{ISSUE_DESCRIPTION}`**

```python
# ✅ GOOD: Use placeholders, render real data at runtime
return f"{finding.issue} in {finding.file}:{finding.line}"
```

---

## Execution Flow

```
/cco-audit
    │
    ├─► Step 0: Introduction & Confirmation
    │
    ├─► Mode Selection (Quick/Standard/Full)
    │
    ├─► Project Context (optional, recommended)
    │
    ├─► Discovery Phase (tech detection, applicability, file filtering)
    │
    ├─► Selection (based on mode)
    │
    ├─► Pre-Flight Summary (confirm before run)
    │
    ├─► Execution Dashboard (real-time progress)
    │
    ├─► Streaming Results (findings as discovered)
    │
    └─► Final Report (prioritized, actionable, concise)
```

---


## Step 0: Introduction and Confirmation

**Welcome to cco-audit - Comprehensive Codebase Audit**

This command analyzes your codebase for security, quality, performance, and infrastructure issues.

### What This Command Does

**Audit Categories:**
- **Security**: OWASP Top 10, secrets, AI security, supply chain
- **Quality**: Tech debt, code quality, AI-generated code issues
- **Testing**: Coverage, isolation, test pyramid
- **Performance**: N+1 queries, caching, bundle size
- **Infrastructure**: CI/CD, containers, monitoring

### What You'll Be Asked

1. **Audit Mode** (Quick/Category/Full Control)
2. **Project Context** (Optional: Extract goals/conventions from README/docs)
3. **Check Selection** (Automated or manual depending on mode)
4. **Pre-Flight Confirmation** (Review checks before running)

### Time Commitment

- **Quick Mode**: 3-8 minutes (automated check selection)
- **Category Mode**: 5-15 minutes (select category groups)
- **Full Control**: 10-30 minutes (select individual checks)

### What You'll Get

**Findings Report:**
- Prioritized issues (Critical → High → Medium → Low)
- Exact file and line locations
- Clear fix recommendations
- Comparison to ideal state

**Action Plan:**
- Immediate fixes (quick wins)
- Short-term improvements (1-2 weeks)
- Long-term investments (architecture changes)

```python
AskUserQuestion({
  questions: [{
    question: "Ready to start codebase audit?",
    header: "Confirm Start",
    multiSelect: false,
    options: [
      {
        label: "Start Audit",
        description: "Proceed with comprehensive codebase analysis (recommended)"
      },
      {
        label: "Learn More",
        description: "Show detailed explanation of audit categories and checks"
      },
      {
        label: "Cancel",
        description: "Exit cco-audit"
      }
    ]
  }]
})
```

**If user selects "Learn More":**
Display complete check catalog, severity levels, and example findings before asking again.

**If user selects "Cancel":**
Exit immediately with message: "cco-audit cancelled. No analysis performed."

**If user selects "Start Audit":**
Continue to Component 1 (Mode Selection).

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
        label: "Quick Mode",
        description: "Fast health assessment with scores, ideal comparison, and action plan (~5 min)"
      },
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

### Quick Mode

**When user selects "Quick Mode" or uses `--quick` flag, execute fast health assessment:**

```python
# Quick mode bypasses detailed check selection
# Instead, performs rapid analysis across all 8 areas

def quick_assessment():
    """
    Fast project health assessment with:
    - Score calculation (0-100) for each area
    - Ideal scenario comparison
    - Prioritized action plan
    """

    # Analyze 8 areas (pain-point priority order)
    areas = [
        ("Security", analyze_security_quick),      # Pain #1
        ("Tech Debt", analyze_tech_debt_quick),    # Pain #2
        ("Testing", analyze_testing_quick),        # Pain #4
        ("Documentation", analyze_docs_quick),     # Pain #7
        ("Database", analyze_database_quick),      # Pain #5
        ("CI/CD", analyze_cicd_quick),            # Pain #6
        ("Observability", analyze_observability_quick),  # Pain #5
        ("Tech Stack", analyze_stack_appropriateness),   # Fitness
    ]

    scores = {}
    for area, analyzer in areas:
        scores[area] = analyzer()  # Returns 0-100 score

    # Generate report
    return generate_quick_report(scores)
```

**Quick Mode Output Format:**

```markdown
## Project Health Report

**Stack:** {Detected stack}
**Type:** {Detected project type}
**Overall Score:** {Average}/100 {Emoji}

### Strategic Recommendations

**Platform Maturity:** {Score}/100 {Emoji}
- CI/CD: {Status} ({Details})
- Test Automation: {Coverage}%
- IaC Presence: {Yes/No/Partial}
- Deployment Frequency: {X}/week
➜ Improvement: /cco-audit --platform

**AI Readiness:** {Low/Medium/High} {Emoji}
- Foundation Quality: {Score}/100
- Test Coverage: {Percentage}%
- Platform Stability: {DORA Tier}
- Recommendation: {Action}
➜ {If Low: "Strengthen foundation before AI adoption"}
➜ {If Medium: "Ready for limited AI use with oversight"}
➜ {If High: "AI will amplify your strong foundation"}

**DORA Metrics Overview:**
1. Deployment Frequency: {X}/week ({Elite/High/Medium/Low})
2. Lead Time for Changes: {Hours/Days} ({Tier})
3. MTTR: {Minutes/Hours} ({Tier})
4. Change Failure Rate: {Percentage}% ({Tier})
5. Rework Rate (2025): {Percentage}% ({Tier})
➜ Overall DORA Tier: {Elite/High/Medium/Low}
➜ Deep Dive: /cco-audit --platform

### Scores by Area (Pain-Point Ordered)

{Emoji} #1 AI Quality Crisis: {Score}/100 ({Status})
   - {Key findings}
   ➜ Fix: /cco-audit --ai-quality

{Emoji} #2 AI Tech Debt: {Score}/100 ({Status})
   - {Key findings}
   ➜ Fix: /cco-audit --ai-debt

{Emoji} #3 Security: {Score}/100 ({Status})
   - {Key findings}
   ➜ Fix: /cco-audit --security

[Repeat for all 12 pain points]

### Tech Stack Evaluation

{✅/⚠️/❌} {Framework} - {Assessment}
{Recommendations for improvements}

**AI Code Detection:**
- Estimated AI-generated code: {Percentage}%
- AI signatures found: {ChatGPT/Copilot/Claude patterns}
- Quality score: {AI_Quality_Score}/100
➜ Detailed analysis: /cco-audit --ai

### Ideal Scenario Comparison

For {Project Type}:
- Security: {Current} vs {Target}
- Testing: {Current} vs {Target}
- [Other comparisons]

### Action Plan (Prioritized by Pain-Point Impact)

**Phase 1: {Name} ({Time} - {Impact})**
Command: /cco-audit --{category}
➜ {What it does}
➜ Impact: {Score change}
➜ Addresses Pain #{X}

[Repeat for all phases]

**Projected Score: {Current} → {After}/100 ✅**

Start Phase 1 now? (yes/no/customize)
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

**Run BEFORE selection. Detects tech stack to show only applicable checks.**

### Step 0: File Discovery with Exclusions (CRITICAL - FIRST)

**Built-in Agent Behavior:**
Agent automatically handles file exclusion with standard filters.

**What the agent does:**
- Excludes standard directories (`.git`, `node_modules`, `venv`, `__pycache__`, `dist`, `build`, etc.)
- Excludes standard files (`package-lock.json`, `yarn.lock`, `*.min.js`, `*.min.css`, `*.map`, `*.pyc`, `*.log`, etc.)
- Reports included/excluded counts

**User sees:**
```
Discovered {to_scan} files (excluded {excluded} files, {percentage_excluded}%)
```

**No configuration needed** - agent knows what to do.

### Step 1: Tech Stack Detection

**Use Glob + Read on FILTERED files only:**
- **Languages**: `**/*.py` → Python, `**/*.{js,ts}` → JavaScript/TypeScript
- **Frameworks**: Parse requirements.txt/pyproject.toml/package.json for Flask/Django/FastAPI/React/etc.
- **Databases**: Check for SQLAlchemy/Sequelize/Prisma patterns
- **DevOps**: `Dockerfile` → Docker, `.github/workflows/` → GitHub Actions
- **Testing**: `pytest.ini`/`conftest.py` → pytest, `jest.config.js` → Jest

**Result:** `detected` dict with tech categories

### Step 2: Calculate Applicability

**Filter checks by tech stack:**
- For each check in ALL_CHECKS, evaluate `is_applicable(detected)`
- Split into `applicable_checks[]` and `not_applicable[]` with reasons

### Step 3: Display Discovery

**Concise summary:**
- **Tech Stack:** {Languages}, {Frameworks}, {Database}
- **Checks:** {APPLICABLE_COUNT}/{TOTAL_CHECKS} applicable ({PCT}%)
- **Files:** {FILE_COUNT} to scan (excluded {EXCLUDED_PCT}%)

---

## Component 3: Full Checklist

**Only shown in Full Control Mode. Complete list of all available checks.**

### Check Categories

```markdown
## All Available Checks ({TOTAL_CHECKS} total)

### 🔴 CRITICAL IMPACT

#### Security (15 checks)
| Check | Slug | Status |
|-------|------|--------|
| SQL Injection, XSS, CSRF, Secrets, Auth Bypass, Authz Flaws | sec-* | Applicable |
| CVE Scan, SSRF, XXE, Path Traversal, Command Injection | sec-* | Applicable |
| Insecure Deserial, Weak Crypto, Security Headers | sec-* | Applicable |

**[See full checklist: /cco-status --checks]**

Full coverage of 92 critical checks across 9 categories:
- **Security** (15): OWASP Top 10, secrets, CVEs
- **Database** (10): N+1, indexes, optimization
- **Tests** (12): Coverage, isolation, pyramid
- **Code Quality** (15): Complexity, duplication, smells
- **Performance** (10): Slow ops, caching, algorithms
- **CI/CD** (8): Pipeline, gates, deploy
- **Documentation** (8): Docstrings, ADRs, examples
- **Containers** (6): Dockerfile, security, optimization
- **Tech Debt** (8): Deprecated, coupling, refactoring

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
      question: "Select Critical Impact categories:? (Space: select, Enter: confirm)",
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
      question: "Select High Impact categories:? (Space: select, Enter: confirm)",
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
      question: "Select Medium Impact categories:? (Space: select, Enter: confirm)",
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

## Component 6: State Management & Count Tracking**CRITICAL: Maintain single source of truth for all counts and status.**### AuditState Pattern**Create central state object:**```python@dataclassclass AuditState:    phase: int = 0    total_findings: int = 0    findings: List[Finding] = field(default_factory=list)    critical: int = 0    high: int = 0    medium: int = 0    low: int = 0    def add_finding(self, finding: Finding) -> None:        self.findings.append(finding)        if finding.severity == "critical": self.critical += 1        elif finding.severity == "high": self.high += 1        elif finding.severity == "medium": self.medium += 1        else: self.low += 1    def get_counts_string(self) -> str:        return f"Issues: {len(self.findings)} ({self.critical}C, {self.high}H, {self.medium}M, {self.low}L)"```**Rules:**- NEVER derive counts (always update explicitly)- ALWAYS use get_counts_string() for display consistency- Global state: `AUDIT_STATE` initialized once

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

## Component 7.5: Agent Execution Strategy

**Built-in Agent Behavior:**
Agent automatically optimizes execution:
- Chooses appropriate model per check (Haiku for patterns, Sonnet for analysis, Opus rarely)
- Runs independent category checks in parallel (fan-out pattern)

**What happens:**
- Pattern matching checks (secrets, syntax) → Haiku (fast, cheap)
- Semantic checks (SQL injection, XSS, N+1) → Sonnet (balanced)
- Independent categories run in parallel for speed
- Example: `--security --tests --database` → 3 parallel agents

**User sees:**
```
Phase 2: Scanning (3 categories in parallel)
- Security: 8 checks
- Testing: 5 checks
- Database: 4 checks
```

**No manual configuration needed** - agent optimizes automatically.

### Agent Prompt Optimization

```python
# ❌ BAD: Verbose, wastes tokens
prompt = """
Please carefully analyze the codebase for SQL injection vulnerabilities.
Look through all Python files and check if user input is being passed
to database queries without proper sanitization or parameterization.
Give me a detailed report of all findings...
""" # 200+ tokens

# ✅ GOOD: Concise, structured
prompt = """
Find SQL injection in Python files.
Check: raw string formatting in queries, user input without sanitization.
Return: file:line format only, brief description.
""" # 25 tokens
```

### Error Handling Template

```python
try:
    result = Task({
        subagent_type: "audit-agent",
        model: "sonnet",
        prompt: audit_prompt
    })
except Exception as e:
    # Ask user how to proceed
    AskUserQuestion({
        questions: [{
            question: "Audit agent failed. How to proceed?",
            header: "Error Recovery",
            multiSelect: false,
            options: [
                {label: "Retry", description: "Run agent task again"},
                {label: "Skip", description: "Continue without this check"},
                {label: "Abort", description: "Stop entire audit"}
            ]
        }]
    })
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
## Component 9: Honesty & Accurate Reporting**CRITICAL PRINCIPLE: Always report the exact truth. No optimistic claims, no false limitations.**### Accurate Outcome Categories```python@dataclassclass FixOutcome:    FIXED = "fixed"                          # File modified, verified    NEEDS_DECISION = "needs_decision"        # Multiple valid approaches    IMPOSSIBLE_EXTERNAL = "impossible_external"  # Third-party codedef categorize_fix(finding: Finding) -> Tuple[str, str]:    if finding.file.startswith("node_modules/"):        return (FixOutcome.IMPOSSIBLE_EXTERNAL,                "Issue in third-party code - update package or report upstream")    if finding.check_id == 16 and is_intentional_eager_load(finding):        return (FixOutcome.NEEDS_DECISION,                "Pattern appears intentional - verify before changing")    return (FixOutcome.FIXED, "Applied automated fix")```### Verification Requirements```pythondef report_fix(finding: Finding, outcome: str):    if outcome == FixOutcome.FIXED:        file_content = Read(finding.file)        if not verify_fix_applied(file_content, finding):            raise AssertionError(f"HONESTY VIOLATION: Claimed fixed but change not found")```### Honest Reporting Templates**When truly fixed:**✅ Fixed: {ISSUE_TYPE} in {FILE_PATH}:{LINE_NUMBER}   Applied: {FIX_DESCRIPTION}   Verified: File updated, syntax valid**When needs human decision:**⚠️ Needs Decision: {ISSUE_TYPE} in {FILE_PATH}:{LINE_NUMBER}   Options: A) {OPTION_A}, B) {OPTION_B}**When impossible:**❌ Cannot Auto-Fix: {ISSUE_TYPE} in {EXTERNAL_COMPONENT}   Why impossible: {REASON}

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

**Concise, actionable findings with clear next steps.**

```markdown
═══════════════════════════════════════════════════════════════
                    AUDIT REPORT
═══════════════════════════════════════════════════════════════

## Executive Summary

**Total Findings:** {total_findings}
- Critical: {critical_count}
- High: {high_count}
- Medium: {medium_count}
- Low: {low_count}

**Accounting Verification:** {total_findings} = {critical_count} + {high_count} + {medium_count} + {low_count} ✓

## Findings by Category

| Category | Critical | High | Medium | Low | Total |
|----------|----------|------|--------|-----|-------|
| Security | {count} | {count} | {count} | {count} | {total} |
| Database | {count} | {count} | {count} | {count} | {total} |
| Tests | {count} | {count} | {count} | {count} | {total} |

## Top Priority Fixes

### Critical Issues ({critical_count})

{for finding in critical_findings[:10]}
**{finding.category}**: {finding.issue}
- **File**: {finding.file}:{finding.line}
- **Fix**: {finding.recommendation}
{endfor}

{if critical_count > 10}
... and {critical_count - 10} more critical issues (see full report)
{endif}

## Action Plan

### Immediate (Today)
1. Fix {quick_fix_count} critical issues (estimated 1-2 hours)
2. Review {high_priority_count} high-priority security findings

### Short-term (This Week)
1. Address remaining high-priority issues
2. Improve test coverage to {target_coverage}%

### Long-term (Next Month)
1. Refactor {complexity_count} high-complexity modules
2. Implement monitoring for {observability_gaps} areas

═══════════════════════════════════════════════════════════════
```

---
## CLI Usage

### Interactive (Default)
```bash
/cco-audit
```

### Quick Overview (Health Assessment)
```bash
/cco-audit --quick
```
Fast health assessment with scores, ideal comparison, and action plan (~5 min).
Replaces the former /cco-overview command.

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

**With Additional Context (Optional Prompt):**
```bash
/cco-audit --security "Focus on authentication endpoints"
/cco-audit --database "Prioritize payment-related queries"
/cco-audit --all "Check for recent vulnerability patterns from OWASP 2025"
```

Any text after the flags is treated as additional context/instruction for the audit. This allows you to:
- Focus analysis on specific areas
- Provide domain-specific context
- Reference recent security advisories
- Guide the audit based on recent changes

The AI will read and incorporate this context when performing the audit.

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

## Agent Error Handling

**If audit agent execution fails:**

AskUserQuestion({
  questions: [{
    question: "audit-agent (Sonnet) failed: {error_message}. How to proceed?",
    header: "audit-agent (Sonnet) Error",
    multiSelect: false,
    options: [
      {label: "Retry", description: "Run agent again with same parameters"},
      {label: "Retry with different model", description: "Try Sonnet/Haiku/Opus"},
      {label: "Manual audit", description: "Guide manual audit process"},
      {label: "Skip this audit category", description: "Continue with next category"},
      {label: "Cancel", description: "Stop entire command"}
    ]
  }]
})

**Model selection if user chooses "Retry with different model":**

AskUserQuestion({
  questions: [{
    question: "Which model to try?",
    header: "Model Selection",
    multiSelect: false,
    options: [
      {label: "Sonnet", description: "Balanced performance and cost (recommended)"},
      {label: "Haiku", description: "Faster, more affordable"},
      {label: "Opus", description: "Most capable, higher cost"}
    ]
  }]
})

---

## Next Steps: Calling Other Commands (C_COMMAND_CONTEXT_PASSING)

### If Issues Found: Calling /cco-fix or /cco-generate

When audit finds fixable issues or missing components:

**ALWAYS provide context before calling another command:**

#### Calling /cco-fix

```markdown
CONTEXT FOR /cco-fix:
Audit found {COUNT} {SEVERITY} issues across {CATEGORY_COUNT} categories:
- {CATEGORY_1}: {COUNT}x {ISSUE_TYPE} ({FILE_PATHS})
- {CATEGORY_2}: {COUNT}x {ISSUE_TYPE} ({FILE_PATHS})
All issues are {FIXABILITY} with {APPROACH}.

[Then immediately call SlashCommand]
```

**Example:**

```markdown
CONTEXT FOR /cco-fix:
Audit found 12 critical security issues: 5x SQL injection (api/db.py:45, 67, 89; models/user.py:123, 145), 4x XSS (templates/profile.html:23, 45; api/render.py:67, 89), 3x hardcoded secrets (.env.example:12, config.py:34, utils/aws.py:56). All are safe-fixable with parameterized queries, HTML escaping, and environment variables.

SlashCommand({command: "/cco-fix security"})
```

#### Calling /cco-generate

```markdown
CONTEXT FOR /cco-generate:
Audit found {COUNT} missing components:
- {COMPONENT_TYPE}: {COUNT} {ITEMS} ({DETAILS})
- Pattern: {EXISTING_PATTERN_REFERENCE}
- Expected: {EXPECTED_STRUCTURE}

[Then immediately call SlashCommand]
```

**Example:**

```markdown
CONTEXT FOR /cco-generate:
Audit found 8 critical files with zero test coverage: src/payments/processor.py (0%), src/auth/jwt_validator.py (0%), src/api/webhooks.py (0%), +5 others. Existing test pattern in tests/test_auth.py uses pytest with fixtures. Generate comprehensive test suites for these 8 files following project conventions.

SlashCommand({command: "/cco-generate tests"})
```

**Why This Matters:**
- Called command receives specific issue list, file paths, line numbers
- No duplicate scanning/analysis
- Faster execution
- Consistent findings across commands

**DON'T:**
```markdown
# ❌ BAD: No context
Found some security issues.
SlashCommand({command: "/cco-fix"})
```
