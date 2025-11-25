# CCO Tech Stack Detection & Pre-Filtering Standards

**Purpose:** Fast tech stack detection (<2 seconds) to filter irrelevant checks/options BEFORE showing to user. Improves UX by reducing decision fatigue 40-60%.

**Critical Principle:** Detection MUST be fast (Glob only, no Read for large files). Filtering MUST happen BEFORE user sees options, not after.

---

## Fast Detection Algorithm

### Performance Requirements

- **Speed:** < 2 seconds total
- **Accuracy:** ≥95% for common tech stacks
- **Method:** Glob-only for files, single Read for small dependency files (<50KB)
- **No Agents:** Direct tool use only (Glob + Read)

### Detection Implementation

```python
from dataclasses import dataclass, field
from typing import List, Dict
import time

@dataclass
class TechStack:
    """Project technology stack."""
    languages: List[str] = field(default_factory=list)
    frameworks: List[str] = field(default_factory=list)
    databases: List[str] = field(default_factory=list)
    devops: List[str] = field(default_factory=list)
    frontend: List[str] = field(default_factory=list)
    testing: List[str] = field(default_factory=list)
    detected_at: float = field(default_factory=time.time)

    def has_docker(self) -> bool:
        return "Docker" in self.devops

    def has_database(self) -> bool:
        return len(self.databases) > 0

    def has_frontend(self) -> bool:
        return len(self.frontend) > 0

    def has_python(self) -> bool:
        return "Python" in self.languages

    def has_javascript(self) -> bool:
        return "JavaScript/TypeScript" in self.languages

def detect_tech_stack_fast(root_path: str = ".") -> TechStack:
    """
    Fast tech stack detection using Glob + selective Read.

    Performance: <2 seconds for projects with <10K files

    Returns:
        TechStack object with detected technologies
    """
    start_time = time.time()
    tech = TechStack()

    # ═══════════════════════════════════════════════════════════
    # PHASE 1: Language Detection (Glob only - Fast)
    # ═══════════════════════════════════════════════════════════

    if Glob("**/*.py", path=root_path):
        tech.languages.append("Python")

    if Glob("**/*.js", path=root_path) or Glob("**/*.ts", path=root_path):
        tech.languages.append("JavaScript/TypeScript")

    if Glob("**/*.go", path=root_path):
        tech.languages.append("Go")

    if Glob("**/*.rs", path=root_path):
        tech.languages.append("Rust")

    if Glob("**/*.java", path=root_path):
        tech.languages.append("Java")

    if Glob("**/*.cs", path=root_path):
        tech.languages.append("C#")

    if Glob("**/*.rb", path=root_path):
        tech.languages.append("Ruby")

    if Glob("**/*.php", path=root_path):
        tech.languages.append("PHP")

    # ═══════════════════════════════════════════════════════════
    # PHASE 2: Framework Detection (Selective Read - Fast)
    # ═══════════════════════════════════════════════════════════

    # Python Frameworks
    if "Python" in tech.languages:
        # Check dependency files (small, fast to read)
        dep_files = Glob("requirements.txt", path=root_path) or \
                    Glob("pyproject.toml", path=root_path) or \
                    Glob("Pipfile", path=root_path)

        if dep_files:
            # Read ONLY first found file (small, <50KB typically)
            deps_content = Read(dep_files[0]).lower()

            if "flask" in deps_content:
                tech.frameworks.append("Flask")
            if "django" in deps_content:
                tech.frameworks.append("Django")
            if "fastapi" in deps_content:
                tech.frameworks.append("FastAPI")
            if "sqlalchemy" in deps_content:
                tech.databases.append("SQLAlchemy")
            if "psycopg2" in deps_content or "asyncpg" in deps_content:
                tech.databases.append("PostgreSQL")
            if "pymongo" in deps_content:
                tech.databases.append("MongoDB")
            if "redis" in deps_content:
                tech.databases.append("Redis")

    # JavaScript/TypeScript Frameworks
    if "JavaScript/TypeScript" in tech.languages:
        package_json_files = Glob("package.json", path=root_path)

        if package_json_files:
            # Read ONLY first package.json
            pkg_content = Read(package_json_files[0]).lower()

            if "react" in pkg_content:
                tech.frontend.append("React")
            if "vue" in pkg_content:
                tech.frontend.append("Vue")
            if "angular" in pkg_content:
                tech.frontend.append("Angular")
            if "next" in pkg_content:
                tech.frontend.append("Next.js")
            if "express" in pkg_content:
                tech.frameworks.append("Express")
            if "nest" in pkg_content:
                tech.frameworks.append("NestJS")

    # Ruby Frameworks
    if "Ruby" in tech.languages:
        if Glob("config/routes.rb", path=root_path):
            tech.frameworks.append("Rails")
        elif Glob("config.ru", path=root_path):
            tech.frameworks.append("Sinatra")

    # Java Frameworks (Glob-only - config file presence)
    if "Java" in tech.languages:
        if Glob("**/application.properties", path=root_path) or \
           Glob("**/application.yml", path=root_path):
            tech.frameworks.append("Spring Boot")

    # ═══════════════════════════════════════════════════════════
    # PHASE 3: DevOps Detection (Glob only - Fast)
    # ═══════════════════════════════════════════════════════════

    if Glob("**/Dockerfile", path=root_path) or \
       Glob("**/docker-compose.yml", path=root_path):
        tech.devops.append("Docker")

    if Glob("**/.github/workflows/*.yml", path=root_path) or \
       Glob("**/.github/workflows/*.yaml", path=root_path):
        tech.devops.append("GitHub Actions")

    if Glob("**/.gitlab-ci.yml", path=root_path):
        tech.devops.append("GitLab CI")

    if Glob("**/Jenkinsfile", path=root_path):
        tech.devops.append("Jenkins")

    if Glob("**/*.tf", path=root_path) or Glob("**/terraform.tfvars", path=root_path):
        tech.devops.append("Terraform")

    if Glob("**/Pulumi.yaml", path=root_path):
        tech.devops.append("Pulumi")

    # Kubernetes
    if Glob("**/k8s/**/*.yaml", path=root_path) or \
       Glob("**/kubernetes/**/*.yaml", path=root_path) or \
       Glob("**/deployment.yaml", path=root_path):
        tech.devops.append("Kubernetes")

    # ═══════════════════════════════════════════════════════════
    # PHASE 4: Testing Frameworks (Glob only - Fast)
    # ═══════════════════════════════════════════════════════════

    if Glob("**/pytest.ini", path=root_path) or \
       Glob("**/conftest.py", path=root_path):
        tech.testing.append("pytest")

    if Glob("**/jest.config.*", path=root_path):
        tech.testing.append("Jest")

    if Glob("**/karma.conf.*", path=root_path):
        tech.testing.append("Karma")

    if Glob("**/mocha.opts", path=root_path) or Glob("**/*.spec.js", path=root_path):
        tech.testing.append("Mocha")

    if Glob("**/*_spec.rb", path=root_path) or Glob("**/.rspec", path=root_path):
        tech.testing.append("RSpec")

    # ═══════════════════════════════════════════════════════════
    # PHASE 5: Database Detection (Glob + pattern matching)
    # ═══════════════════════════════════════════════════════════

    if Glob("**/*.sqlite", path=root_path) or Glob("**/*.db", path=root_path):
        tech.databases.append("SQLite")

    # Check for DB-specific config files
    if Glob("**/mongod.conf", path=root_path):
        tech.databases.append("MongoDB")

    if Glob("**/redis.conf", path=root_path):
        tech.databases.append("Redis")

    # ═══════════════════════════════════════════════════════════
    # PHASE 6: Report Duration
    # ═══════════════════════════════════════════════════════════

    duration = time.time() - start_time
    print(f"Tech stack detection completed in {duration:.2f}s")

    if duration > 2.0:
        print(f"⚠️  Warning: Detection took longer than 2s threshold")

    return tech
```

---

## Applicability Rules

### Check/Option Applicability

```python
@dataclass
class ApplicabilityRule:
    """Rule for determining if check/option is applicable."""
    check_id: str
    check_name: str
    requires_languages: List[str] = field(default_factory=list)
    requires_frameworks: List[str] = field(default_factory=list)
    requires_databases: List[str] = field(default_factory=list)
    requires_devops: List[str] = field(default_factory=list)
    requires_frontend: List[str] = field(default_factory=list)
    requires_any: bool = False  # True = OR logic, False = AND logic

# ═══════════════════════════════════════════════════════════
# Security Checks Applicability
# ═══════════════════════════════════════════════════════════

SECURITY_RULES = [
    ApplicabilityRule(
        check_id="sql_injection",
        check_name="SQL Injection Detection",
        requires_databases=["PostgreSQL", "MySQL", "SQLAlchemy", "SQLite"],
        requires_any=True  # Any database
    ),
    ApplicabilityRule(
        check_id="xss",
        check_name="XSS Detection",
        requires_frontend=["React", "Vue", "Angular", "Next.js"],
        requires_any=True  # Any frontend
    ),
    ApplicabilityRule(
        check_id="secrets_scan",
        check_name="Hardcoded Secrets Scan",
        # Always applicable (no requirements)
    ),
    ApplicabilityRule(
        check_id="csrf",
        check_name="CSRF Protection Check",
        requires_frameworks=["Flask", "Django", "Express", "Rails"],
        requires_any=True
    ),
]

# ═══════════════════════════════════════════════════════════
# Database Checks Applicability
# ═══════════════════════════════════════════════════════════

DATABASE_RULES = [
    ApplicabilityRule(
        check_id="n_plus_one",
        check_name="N+1 Query Detection",
        requires_databases=["SQLAlchemy", "PostgreSQL", "MySQL"],
        requires_any=True
    ),
    ApplicabilityRule(
        check_id="missing_indexes",
        check_name="Missing Index Detection",
        requires_databases=["PostgreSQL", "MySQL"],
        requires_any=True
    ),
    ApplicabilityRule(
        check_id="unsafe_migrations",
        check_name="Unsafe Migration Detection",
        requires_frameworks=["Django", "Rails", "SQLAlchemy"],
        requires_any=True
    ),
]

# ═══════════════════════════════════════════════════════════
# Container/DevOps Checks Applicability
# ═══════════════════════════════════════════════════════════

DEVOPS_RULES = [
    ApplicabilityRule(
        check_id="dockerfile_security",
        check_name="Dockerfile Security Scan",
        requires_devops=["Docker"]
    ),
    ApplicabilityRule(
        check_id="k8s_security",
        check_name="Kubernetes Security Scan",
        requires_devops=["Kubernetes"]
    ),
    ApplicabilityRule(
        check_id="cicd_security",
        check_name="CI/CD Security Check",
        requires_devops=["GitHub Actions", "GitLab CI", "Jenkins"],
        requires_any=True
    ),
]

# ═══════════════════════════════════════════════════════════
# Frontend Checks Applicability
# ═══════════════════════════════════════════════════════════

FRONTEND_RULES = [
    ApplicabilityRule(
        check_id="bundle_size",
        check_name="Bundle Size Analysis",
        requires_frontend=["React", "Vue", "Angular", "Next.js"],
        requires_any=True
    ),
    ApplicabilityRule(
        check_id="accessibility",
        check_name="Accessibility (a11y) Check",
        requires_frontend=["React", "Vue", "Angular"],
        requires_any=True
    ),
]

# Combine all rules
ALL_APPLICABILITY_RULES = (
    SECURITY_RULES +
    DATABASE_RULES +
    DEVOPS_RULES +
    FRONTEND_RULES
)
```

### Filtering Algorithm

```python
def filter_applicable_checks(
    all_checks: List[dict],
    tech_stack: TechStack
) -> Tuple[List[dict], List[Tuple[dict, str]]]:
    """
    Filter checks based on tech stack applicability.

    Returns:
        (applicable_checks, filtered_checks_with_reasons)
    """
    applicable = []
    filtered = []

    for check in all_checks:
        # Find rule for this check
        rule = next(
            (r for r in ALL_APPLICABILITY_RULES if r.check_id == check["id"]),
            None
        )

        # If no rule, assume always applicable
        if rule is None:
            applicable.append(check)
            continue

        # Check applicability
        reason = check_applicability(rule, tech_stack)

        if reason:
            # Not applicable - add to filtered list
            filtered.append((check, reason))
        else:
            # Applicable
            applicable.append(check)

    return applicable, filtered

def check_applicability(rule: ApplicabilityRule, tech: TechStack) -> str:
    """
    Check if rule requirements are met.

    Returns:
        Empty string if applicable, reason string if not applicable
    """
    # Check languages
    if rule.requires_languages:
        if rule.requires_any:
            # At least one language must match
            if not any(lang in tech.languages for lang in rule.requires_languages):
                return f"Not using: {', '.join(rule.requires_languages)}"
        else:
            # All languages must match
            missing = [lang for lang in rule.requires_languages if lang not in tech.languages]
            if missing:
                return f"Missing languages: {', '.join(missing)}"

    # Check frameworks
    if rule.requires_frameworks:
        if rule.requires_any:
            if not any(fw in tech.frameworks for fw in rule.requires_frameworks):
                return f"Not using: {', '.join(rule.requires_frameworks)}"
        else:
            missing = [fw for fw in rule.requires_frameworks if fw not in tech.frameworks]
            if missing:
                return f"Missing frameworks: {', '.join(missing)}"

    # Check databases
    if rule.requires_databases:
        if rule.requires_any:
            if not any(db in tech.databases for db in rule.requires_databases):
                return f"Not using: {', '.join(rule.requires_databases)}"
        else:
            missing = [db for db in rule.requires_databases if db not in tech.databases]
            if missing:
                return f"Missing databases: {', '.join(missing)}"

    # Check devops
    if rule.requires_devops:
        if rule.requires_any:
            if not any(tool in tech.devops for tool in rule.requires_devops):
                return f"Not using: {', '.join(rule.requires_devops)}"
        else:
            missing = [tool for tool in rule.requires_devops if tool not in tech.devops]
            if missing:
                return f"Missing devops tools: {', '.join(missing)}"

    # Check frontend
    if rule.requires_frontend:
        if rule.requires_any:
            if not any(fe in tech.frontend for fe in rule.requires_frontend):
                return f"Not using: {', '.join(rule.requires_frontend)}"
        else:
            missing = [fe for fe in rule.requires_frontend if fe not in tech.frontend]
            if missing:
                return f"Missing frontend: {', '.join(missing)}"

    # All requirements met
    return ""
```

---

## User Presentation

### Filtered Results Display

```python
def present_filtered_selection(
    all_checks: List[dict],
    applicable: List[dict],
    filtered: List[Tuple[dict, str]],
    tech_stack: TechStack
):
    """Present intelligently filtered options to user."""

    print(f"""
╔═══════════════════════════════════════════════════════════════╗
║  INTELLIGENT CHECK SELECTION                                  ║
╠═══════════════════════════════════════════════════════════════╣
║  Tech Stack: {', '.join(tech_stack.languages[:3])}            ║
║                                                               ║
║  Total Checks: {len(all_checks)}                             ║
║  ✅ Applicable: {len(applicable)} (shown below)              ║
║  ⏭️  Filtered: {len(filtered)} (not relevant)                ║
╚═══════════════════════════════════════════════════════════════╝

""")

    # Group filtered by category
    filtered_by_category = {}
    for check, reason in filtered:
        category = check.get("category", "Other")
        if category not in filtered_by_category:
            filtered_by_category[category] = []
        filtered_by_category[category].append((check["name"], reason))

    # Show filtered summary
    if filtered:
        print("Filtered Checks (use --show-all to override):\n")
        for category, items in filtered_by_category.items():
            print(f"  {category}: {len(items)} checks")
            for name, reason in items[:2]:  # Show first 2
                print(f"    • {name}: {reason}")
            if len(items) > 2:
                print(f"    ... and {len(items) - 2} more")
        print()

    print(f"💡 Showing only {len(applicable)} applicable checks based on your tech stack")
    print(f"   Use --show-all flag to see all {len(all_checks)} checks\n")
```

### Integration with AskUserQuestion

```python
# Generate options ONLY from applicable checks
options = [
    {
        "label": "All Applicable",
        "description": f"Select all {len(applicable)} applicable checks"
    }
]

for check in applicable:
    options.append({
        "label": check["name"],
        "description": f"{check['description']} ({check['severity']})"
    })

# Present to user
AskUserQuestion({
    "questions": [{
        "question": "Select checks to run:",
        "header": "Audit Selection",
        "multiSelect": True,
        "options": options[:4]  # First 4 options (AskUserQuestion limit)
    }]
})
```

---

## Performance Optimization

### Caching Detection Results

```python
# Session-level cache (conversation context)
_TECH_STACK_CACHE = None

def get_or_detect_tech_stack(root_path: str = ".") -> TechStack:
    """
    Get cached tech stack or detect fresh.

    Uses conversation context for session-level caching.
    """
    global _TECH_STACK_CACHE

    if _TECH_STACK_CACHE is not None:
        print("✓ Using cached tech stack from session")
        return _TECH_STACK_CACHE

    print("Detecting project tech stack...")
    tech_stack = detect_tech_stack_fast(root_path)

    # Cache for session
    _TECH_STACK_CACHE = tech_stack

    # Write to conversation for visibility
    print_tech_stack_context(tech_stack)

    return tech_stack

def print_tech_stack_context(tech: TechStack):
    """Print tech stack to conversation context for session caching."""
    print(f"""
════════════════════════════════════════════════════════════════
TECH STACK DETECTED (cached for this session):

Languages: {', '.join(tech.languages) if tech.languages else 'None'}
Frameworks: {', '.join(tech.frameworks) if tech.frameworks else 'None'}
Databases: {', '.join(tech.databases) if tech.databases else 'None'}
DevOps: {', '.join(tech.devops) if tech.devops else 'None'}
Frontend: {', '.join(tech.frontend) if tech.frontend else 'None'}
Testing: {', '.join(tech.testing) if tech.testing else 'None'}

Detection time: {time.time() - tech.detected_at:.2f}s
════════════════════════════════════════════════════════════════
""")
```

---

## Command Integration

### Step 0.5: Tech Detection (After User Confirmation)

```markdown
### Step 0.5: Tech Stack Detection

**Run AFTER user confirms starting command, BEFORE showing options.**

\`\`\`python
# Detect tech stack
tech_stack = get_or_detect_tech_stack()

# Filter checks based on applicability
applicable_checks, filtered_checks = filter_applicable_checks(
    all_checks=ALL_AUDIT_CHECKS,
    tech_stack=tech_stack
)

# Present filtered selection to user
present_filtered_selection(
    all_checks=ALL_AUDIT_CHECKS,
    applicable=applicable_checks,
    filtered=filtered_checks,
    tech_stack=tech_stack
)

# Generate options from applicable checks only
options = generate_options_from_checks(applicable_checks)

# Show to user via AskUserQuestion
AskUserQuestion({...})
\`\`\`
```

---

## Verification Checklist

Before integrating tech detection:

- [ ] Detection completes in <2 seconds
- [ ] Only small files read (<50KB each)
- [ ] Glob used for file discovery (not Read)
- [ ] Applicability rules defined for all checks
- [ ] Filtered checks shown with reasons
- [ ] Session-level caching implemented
- [ ] `--show-all` flag supported
- [ ] Clear messaging about filtering

---

## References

- **Pattern Library:** `cco-patterns.md` (Pattern 10)
- **Efficient File Operations:** `C_EFFICIENT_FILE_OPERATIONS` principle
- **Context Window Management:** `C_CONTEXT_WINDOW_MGMT` principle

---

**Last Updated:** 2025-01-24
**Status:** Active - All commands with selection UIs MUST use tech filtering
