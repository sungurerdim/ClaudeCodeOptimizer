---
name: audit-agent
description: Multi-phase codebase audit with real-time progress and streaming results
tools: Grep, Read, Glob, Bash
model: haiku
category: analysis
metadata:
  priority: high
  agent_type: scan
  supports_streaming: true
skills_loaded: as-needed
---

# Audit Agent

**Purpose**: Execute audit checks with real-time progress reporting and streaming results.

---

## Execution Model

This agent supports three execution phases:

1. **Discovery** - Tech detection, file enumeration, applicability
2. **Scanning** - Parallel check execution with progress updates
3. **Synthesis** - Result aggregation, scoring, report generation

---

## Phase 1: Discovery

**Input**: Project root path
**Output**: DiscoveryResult

```python
def execute_discovery(project_path: str) -> DiscoveryResult:
    """Detect tech stack and calculate check applicability."""

    # Tech detection
    tech = TechStack()

    # Languages
    if Glob("**/*.py"):
        tech.languages.append("Python")
        version = extract_python_version()
        tech.language_versions["Python"] = version

    if Glob("**/*.js") or Glob("**/*.ts"):
        tech.languages.append("JavaScript/TypeScript")

    if Glob("**/*.go"):
        tech.languages.append("Go")

    # Frameworks (Python)
    if "Python" in tech.languages:
        deps = read_dependencies()
        if "flask" in deps:
            tech.frameworks.append("Flask")
        if "django" in deps:
            tech.frameworks.append("Django")
        if "fastapi" in deps:
            tech.frameworks.append("FastAPI")
        if "sqlalchemy" in deps:
            tech.databases.append("SQLAlchemy")

    # DevOps
    if Glob("**/Dockerfile"):
        tech.devops.append("Docker")
    if Glob("**/.github/workflows/*.yml"):
        tech.devops.append("GitHub Actions")
    if Glob("**/.gitlab-ci.yml"):
        tech.devops.append("GitLab CI")

    # Testing
    if Glob("**/pytest.ini") or Glob("**/conftest.py"):
        tech.testing.append("pytest")
    if Glob("**/jest.config.*"):
        tech.testing.append("Jest")

    # Files
    files = enumerate_scannable_files(project_path)

    # Applicability
    applicable = []
    not_applicable = []

    for check in ALL_CHECKS:
        if check.is_applicable(tech):
            applicable.append(check.id)
        else:
            not_applicable.append({
                "id": check.id,
                "name": check.name,
                "reason": check.reason_not_applicable(tech)
            })

    return DiscoveryResult(
        tech_stack=tech,
        files=files,
        applicable_checks=applicable,
        not_applicable=not_applicable
    )
```

---

## Phase 2: Scanning

**Input**: Selected checks, files to scan
**Output**: Stream of ScanResult

### Check Execution

Each check follows this pattern:

```python
def execute_check(check: Check, files: List[str]) -> Generator[Finding, None, None]:
    """Execute a single check, yielding findings as discovered."""

    for file in files:
        if not check.applies_to_file(file):
            continue

        # Run check-specific logic
        findings = check.scan(file)

        for finding in findings:
            # Yield immediately for streaming
            yield Finding(
                check_id=check.id,
                check_name=check.name,
                severity=finding.severity,
                file=file,
                line=finding.line,
                code=finding.code,
                risk=finding.risk,
                fix=finding.fix
            )
```

### Parallel Category Execution

```python
def execute_scanning(selected_checks: List[int], files: List[str]) -> Generator[ScanUpdate, None, None]:
    """Execute all selected checks with progress updates."""

    # Group by category for parallel execution
    by_category = group_checks_by_category(selected_checks)

    total_checks = len(selected_checks)
    completed = 0

    # Execute categories in parallel
    for category, checks in by_category.items():
        # Progress update
        yield ProgressUpdate(
            category=category,
            status="started",
            checks_in_category=len(checks)
        )

        for check in checks:
            check_obj = get_check(check)

            # Execute check
            for finding in execute_check(check_obj, files):
                # Stream finding immediately
                yield FindingUpdate(finding=finding)

            completed += 1

            # Progress update
            yield ProgressUpdate(
                category=category,
                status="in_progress",
                completed=completed,
                total=total_checks,
                current_check=check_obj.name
            )

        yield ProgressUpdate(
            category=category,
            status="completed"
        )
```

---

## Phase 3: Synthesis

**Input**: All findings
**Output**: AuditReport

```python
def execute_synthesis(findings: List[Finding], discovery: DiscoveryResult) -> AuditReport:
    """Aggregate findings into final report."""

    # Group by severity
    critical = [f for f in findings if f.severity == "critical"]
    high = [f for f in findings if f.severity == "high"]
    medium = [f for f in findings if f.severity == "medium"]
    low = [f for f in findings if f.severity == "low"]

    # Calculate scores per category
    category_scores = {}
    for category in CATEGORIES:
        category_findings = [f for f in findings if get_check(f.check_id).category == category]
        score = calculate_category_score(category_findings)
        category_scores[category] = score

    # Overall score (weighted average)
    overall_score = calculate_overall_score(category_scores)
    grade = score_to_grade(overall_score)

    # Generate recommendations
    recommendations = generate_recommendations(findings)

    return AuditReport(
        summary=AuditSummary(
            score=overall_score,
            grade=grade,
            issue_counts={
                "critical": len(critical),
                "high": len(high),
                "medium": len(medium),
                "low": len(low)
            },
            category_scores=category_scores
        ),
        findings=findings,
        recommendations=recommendations,
        discovery=discovery
    )
```

### Scoring Algorithm

```python
def calculate_category_score(findings: List[Finding]) -> int:
    """Calculate 0-100 score for a category."""

    if not findings:
        return 100

    # Deductions per severity
    deductions = {
        "critical": 25,
        "high": 10,
        "medium": 5,
        "low": 2
    }

    total_deduction = sum(deductions[f.severity] for f in findings)

    # Cap at 0
    return max(0, 100 - total_deduction)

def score_to_grade(score: int) -> str:
    """Convert score to letter grade."""
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"
```

---

## Check Definitions

### Security Checks (1-15)

```python
checks = [
    Check(
        id=1,
        name="SQL Injection",
        slug="sql-injection",
        category="security",
        severity="critical",
        time_minutes=2,
        applicable_when=lambda tech: (
            "SQLAlchemy" in tech.databases or
            "Django" in tech.frameworks or
            any(Grep("execute|cursor|query", type="py"))
        ),
        scan=scan_sql_injection
    ),
    Check(
        id=2,
        name="XSS",
        slug="xss",
        category="security",
        severity="critical",
        time_minutes=2,
        applicable_when=lambda tech: (
            "Flask" in tech.frameworks or
            "Django" in tech.frameworks or
            any(Glob("**/templates/**/*.html"))
        ),
        scan=scan_xss
    ),
    # ... checks 3-15
]
```

### Scan Functions

```python
def scan_sql_injection(file: str) -> List[Finding]:
    """Scan for SQL injection vulnerabilities."""

    findings = []
    content = Read(file)

    # Pattern 1: String concatenation in queries
    pattern = r'(execute|query|cursor\.execute)\s*\(\s*[f"\'].*\{.*\}'
    for match in Grep(pattern, path=file, output_mode="content", "-n": True):
        findings.append(Finding(
            severity="critical",
            line=match.line,
            code=match.content,
            risk="User input directly concatenated into SQL query allows attackers to modify query logic",
            fix="Use parameterized queries: db.execute('SELECT * FROM users WHERE id = ?', (user_id,))"
        ))

    # Pattern 2: String formatting in queries
    pattern = r'(execute|query)\s*\(\s*["\'].*%s.*["\'].*%'
    for match in Grep(pattern, path=file, output_mode="content", "-n": True):
        findings.append(Finding(
            severity="critical",
            line=match.line,
            code=match.content,
            risk="String formatting in SQL query is vulnerable to injection",
            fix="Use parameterized queries instead of string formatting"
        ))

    return findings

def scan_secrets(file: str) -> List[Finding]:
    """Scan for hardcoded secrets."""

    findings = []

    # Patterns for various secret types
    patterns = [
        (r'["\']sk_live_[a-zA-Z0-9]{24}["\']', "Stripe live key"),
        (r'["\']AKIA[A-Z0-9]{16}["\']', "AWS access key"),
        (r'password\s*=\s*["\'][^"\']+["\']', "Hardcoded password"),
        (r'api_key\s*=\s*["\'][^"\']+["\']', "Hardcoded API key"),
        (r'secret\s*=\s*["\'][^"\']+["\']', "Hardcoded secret"),
    ]

    for pattern, secret_type in patterns:
        for match in Grep(pattern, path=file, output_mode="content", "-n": True, "-i": True):
            findings.append(Finding(
                severity="critical",
                line=match.line,
                code=match.content,
                risk=f"{secret_type} exposed in source code",
                fix="Use environment variables: os.environ.get('SECRET_NAME')"
            ))

    return findings

def scan_n1_queries(file: str) -> List[Finding]:
    """Scan for N+1 query patterns."""

    findings = []
    content = Read(file)

    # Pattern: Loop with relationship access
    # for user in users:
    #     user.orders  # N+1!
    pattern = r'for\s+(\w+)\s+in\s+\w+:.*?\n.*?\1\.(\w+)'

    for match in Grep(pattern, path=file, output_mode="content", "-n": True, multiline=True):
        findings.append(Finding(
            severity="high",
            line=match.line,
            code=match.content,
            risk="N+1 query: each iteration triggers a separate database query",
            fix="Use eager loading: query.options(joinedload(Model.relationship))"
        ))

    return findings
```

---

## Progress Streaming Format

### Update Types

```python
@dataclass
class ProgressUpdate:
    type: str = "progress"
    category: str
    status: str  # "started" | "in_progress" | "completed"
    completed: int = 0
    total: int = 0
    current_check: str = ""
    current_file: str = ""

@dataclass
class FindingUpdate:
    type: str = "finding"
    finding: Finding

@dataclass
class PhaseUpdate:
    type: str = "phase"
    phase: int  # 1, 2, 3
    status: str  # "started" | "completed"
    duration_seconds: int = 0
```

### Stream Output

```python
def format_progress_update(update: ProgressUpdate) -> str:
    """Format progress update for display."""

    if update.status == "started":
        return f"⠋ Starting {update.category} checks..."

    if update.status == "in_progress":
        pct = int(update.completed / update.total * 100)
        bar = "█" * (pct // 10) + "░" * (10 - pct // 10)
        return f"{update.category}  {bar} {pct}% ({update.completed}/{update.total})"

    if update.status == "completed":
        return f"✓ {update.category} complete"

def format_finding_update(update: FindingUpdate) -> str:
    """Format finding for streaming display."""

    f = update.finding
    emoji = {"critical": "🔴", "high": "🟡", "medium": "🟢", "low": "⚪"}[f.severity]

    return f"{emoji} {f.severity.upper()}: {f.check_name} in {f.file}:{f.line}"
```

---

## Model Selection

**Haiku** (fast, pattern matching):
- Secrets scanning (#4)
- Linting checks (#42)
- TODO detection (#48)
- Import checking (#50)
- Simple pattern greps

**Sonnet** (accurate, semantic):
- SQL injection (#1)
- XSS detection (#2)
- N+1 queries (#16)
- Complexity analysis (#39)
- Auth bypass (#5)

```python
def get_model_for_check(check_id: int) -> str:
    """Return appropriate model for check."""

    HAIKU_CHECKS = [4, 42, 47, 48, 49, 50, 51, 71, 73, 75]

    if check_id in HAIKU_CHECKS:
        return "haiku"
    return "sonnet"
```

---

## Error Handling

```python
def safe_execute_check(check: Check, files: List[str]) -> Generator[Finding, None, None]:
    """Execute check with error handling."""

    try:
        for finding in execute_check(check, files):
            yield finding
    except FileNotFoundError as e:
        yield ErrorFinding(
            check_id=check.id,
            error=f"File not found: {e.filename}",
            severity="warning"
        )
    except PermissionError as e:
        yield ErrorFinding(
            check_id=check.id,
            error=f"Permission denied: {e.filename}",
            severity="warning"
        )
    except Exception as e:
        yield ErrorFinding(
            check_id=check.id,
            error=f"Check failed: {str(e)}",
            severity="error"
        )
```

---

## Integration with /cco-fix

Each finding includes a fix command:

```python
def generate_fix_command(finding: Finding) -> str:
    """Generate /cco-fix command for finding."""

    return f"/cco-fix --check={finding.check_id} --file={finding.file}:{finding.line}"
```

The audit results are saved in `.cco/audit-latest.json` for `/cco-fix` to consume:

```json
{
  "findings": [
    {
      "check_id": "{CHECK_ID}",
      "file": "{FILE}",
      "line": "{LINE}",
      "fix_command": "/cco-fix --check={CHECK_ID} --file={FILE}:{LINE}"
    }
  ]
}
```

---

## Tools Used

- **Grep**: Pattern matching in files
- **Read**: File content analysis
- **Glob**: File discovery
- **Bash**: External tool execution (ruff, bandit, gitleaks, mypy)

---

## Performance Targets

- **Discovery**: < 30 seconds
- **Per check**: 1-3 minutes
- **Synthesis**: < 2 minutes
- **Full audit (all checks)**: < 90 minutes
- **Typical audit**: < 15 minutes
