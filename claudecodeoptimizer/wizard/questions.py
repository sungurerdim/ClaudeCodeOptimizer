"""
Question Definitions - CCO 2.5 Wizard

ALL CHOICES ARE DERIVED FROM SCHEMAS - NO DUPLICATION!
Conditional logic to skip irrelevant questions based on user answers.
"""

from typing import Any, Dict, List

from ..core.constants import (
    LARGE_CODEBASE_THRESHOLD,
    MEDIUM_CODEBASE_THRESHOLD,
    SMALL_CODEBASE_THRESHOLD,
)

# Import all choice types from schema (SINGLE SOURCE OF TRUTH)
from ..schemas.preferences import (
    APIDocChoice,
    ArchitectureDiagramsChoice,
    AuditLoggingChoice,
    BreakingChangesChoice,
    BusinessDomainChoice,
    CachingStrategyChoice,
    ChangelogChoice,
    CICDTriggerChoice,
    CodeCommentChoice,
    CodeOwnershipChoice,
    CodePhilosophyChoice,
    CodeReviewChoice,
    CommitConventionChoice,
    ComplianceChoice,
    DatabaseQueriesChoice,
    DependencyScanningChoice,
    DeploymentFrequencyChoice,
    DeploymentTargetChoice,
    DevelopmentPaceChoice,
    DocAudienceChoice,
    DocStyleChoice,
    DocVerbosityChoice,
    DRYEnforcementChoice,
    DuplicationForPerfChoice,
    EncryptionScopeChoice,
    EnvironmentChoice,
    ExpectedScaleChoice,
    FeatureFlagsChoice,
    GitWorkflowChoice,
    ImportOrganizationChoice,
    InfrastructureChoice,
    InlineDocChoice,
    InputValidationChoice,
    LicenseChoice,
    LineLengthChoice,
    LintingStrictnessChoice,
    MagicNumberChoice,
    MockingChoice,
    MonitoringChoice,
    MutationTestingChoice,
    NamingConventionChoice,
    OptimizationPriorityChoice,
    PairProgrammingChoice,
    PrematureOptimizationChoice,
    ProjectMaturityChoice,
    ProjectTypeChoice,
    PropertyTestingChoice,
    PRSizeChoice,
    ReadmeLengthChoice,
    RefactoringChoice,
    RollbackStrategyChoice,
    SecretManagementChoice,
    SecurityStanceChoice,
    TDDAdherenceChoice,
    TeamSizeChoice,
    TestCoverageChoice,
    TestIsolationChoice,
    TestNamingChoice,
    TestPyramidChoice,
    TypeCoverageChoice,
    get_literal_choices,
)

# ============================================================================
# CONDITIONAL LOGIC - Skip irrelevant questions
# ============================================================================


def should_ask_question(question_id: str, answers: Dict[str, Any]) -> bool:
    """
    Determine if a question should be asked based on previous answers.

    Returns True if question should be asked, False to skip.
    """

    # Team-related questions - skip if solo
    team_questions = [
        "code_review_strictness",
        "pair_programming",
        "pr_size_limit",
        "code_ownership",
        "git_workflow",
        "commit_convention",
    ]
    if question_id in team_questions:
        team_size = answers.get("team_trajectory", "solo")
        if team_size == "solo":
            return False  # Skip team questions for solo devs

    # Testing detail questions - skip if no tests
    if question_id in ["mutation_testing", "property_based_testing", "test_pyramid_ratio"]:
        coverage = answers.get("coverage_target", "90")
        if coverage in ["none", "not-set", "0"]:
            return False

    # Type checking questions - skip if language doesn't use types
    if question_id == "type_coverage_target":
        lang = answers.get("primary_language", "").lower()
        if lang in ["javascript", "python", "ruby", "php"]:
            # These languages have optional typing, ask the question
            return True
        elif lang in ["java", "c", "c++", "rust", "go", "typescript"]:
            # Statically typed, definitely ask
            return True
        # For unknown/dynamic languages, still ask
        return True

    # CI/CD setup questions - skip if manual
    if question_id in ["deployment_frequency", "rollback_strategy"]:
        cicd = answers.get("ci_cd_trigger", "every-pr")
        if cicd == "manual":
            return False

    # Monitoring questions - skip if no monitoring
    if question_id == "monitoring":
        infra = answers.get("infrastructure", [])
        if not infra or "bare-metal" in infra:
            # Still ask but user can select "none"
            return True
        return True

    # Compliance detail questions - skip if no compliance
    if question_id == "audit_logging":
        compliance = answers.get("compliance_requirements", ["none"])
        if compliance == ["none"] or "none" in compliance:
            # Still ask for non-compliance auditing
            return True

    # Documentation questions - skip if minimal docs preference
    if question_id in ["architecture_diagrams", "changelog_detail"]:
        verbosity = answers.get("verbosity", "concise")
        if verbosity == "minimal":
            return False

    # API documentation - skip if not API project
    if question_id == "api_documentation":
        types = answers.get("types", [])
        if not any(t in ["api", "backend", "microservice"] for t in types):
            return False

    # Default: ask the question
    return True


# ============================================================================
# AI HINT GENERATORS
# ============================================================================


def get_project_type_hint(report: Dict[str, Any]) -> str:
    """Generate AI hint for project types"""
    detected_types = [pt["detected_value"] for pt in report.get("project_types", [])]
    if detected_types:
        return f"Detected: {', '.join(detected_types)}"
    return "No project types auto-detected"


def get_language_hint(report: Dict[str, Any]) -> str:
    """Generate AI hint for primary language"""
    languages = report.get("languages", [])
    if languages:
        primary = languages[0]["detected_value"]
        return f"Detected: {primary}"
    return "No languages auto-detected"


def get_framework_hint(report: Dict[str, Any]) -> str:
    """Generate AI hint for frameworks"""
    frameworks = [fw["detected_value"] for fw in report.get("frameworks", [])]
    if frameworks:
        return f"Detected: {', '.join(frameworks)}"
    return "No frameworks detected"


def get_deployment_hint(report: Dict[str, Any]) -> str:
    """Generate AI hint for deployment target"""
    tools = [t["detected_value"] for t in report.get("tools", [])]
    if "docker" in tools or "kubernetes" in tools:
        return "Detected Docker/K8s - likely cloud deployment"
    return "Inferred from tooling"


def get_scale_hint(report: Dict[str, Any]) -> str:
    """Generate AI hint for expected scale"""
    patterns = report.get("codebase_patterns", {})
    total_files = patterns.get("total_files", 0)
    if total_files > LARGE_CODEBASE_THRESHOLD:
        return "Large codebase suggests enterprise scale"
    elif total_files > MEDIUM_CODEBASE_THRESHOLD:
        return "Medium codebase suggests growth scale"
    elif total_files > SMALL_CODEBASE_THRESHOLD:
        return "Small codebase suggests startup scale"
    return "Small project suggests hobby/startup scale"


def get_compliance_hint(report: Dict[str, Any]) -> str:
    """Generate AI hint for compliance requirements"""
    tools = [t["detected_value"] for t in report.get("tools", [])]
    if any(t in ["vault", "kms", "security"] for t in tools):
        return "Security tools detected - consider compliance needs"
    return "No compliance indicators detected"


def get_maturity_hint(report: Dict[str, Any]) -> str:
    """Generate AI hint for project maturity"""
    patterns = report.get("codebase_patterns", {})
    has_tests = patterns.get("has_tests", False)
    has_ci = patterns.get("has_ci_cd", False)

    if has_tests and has_ci:
        return "Tests and CI detected - mature project"
    elif has_tests or has_ci:
        return "Some infrastructure detected - active development"
    return "Minimal infrastructure - early stage"


def get_team_size_hint(report: Dict[str, Any]) -> str:
    """Generate AI hint for team size"""
    return "Unable to detect team size - select based on current/expected team"


def get_linting_hint(report: Dict[str, Any]) -> str:
    """Generate AI hint for linting strictness"""
    tools = [t["detected_value"] for t in report.get("tools", [])]
    linters = [t for t in tools if any(lint in t for lint in ["lint", "ruff", "eslint", "clippy"])]
    if linters:
        return f"Detected: {', '.join(linters)}"
    return "No linters detected"


def get_type_coverage_hint(report: Dict[str, Any]) -> str:
    """Generate AI hint for type coverage"""
    languages = report.get("languages", [])
    if languages:
        lang = languages[0]["detected_value"]
        if lang in ["typescript", "rust", "haskell"]:
            return "Type-safe language detected - recommend 100% coverage"
        elif lang in ["python", "javascript"]:
            tools = [t["detected_value"] for t in report.get("tools", [])]
            if "mypy" in tools or "flow" in tools:
                return "Type checker detected - recommend 90%+ coverage"
    return "Recommend 80-90% for most projects"


def get_testing_coverage_hint(report: Dict[str, Any]) -> str:
    """Generate AI hint for test coverage"""
    tools = [t["detected_value"] for t in report.get("tools", [])]
    if "coverage" in tools or "pytest-cov" in tools:
        return "Coverage tool detected - recommend 90%+"
    return "Recommend 80-90% for production projects"


def get_security_stance_hint(report: Dict[str, Any]) -> str:
    """Generate AI hint for security stance"""
    tools = [t["detected_value"] for t in report.get("tools", [])]
    security_tools = [t for t in tools if any(sec in t for sec in ["security", "vault", "crypto"])]
    if security_tools:
        return "Security tools detected - recommend paranoid stance"
    return "Recommend balanced for most projects"


def get_infrastructure_hint(report: Dict[str, Any]) -> str:
    """Generate AI hint for infrastructure"""
    tools = [t["detected_value"] for t in report.get("tools", [])]
    if "kubernetes" in tools:
        return "Kubernetes detected"
    elif "docker" in tools or "docker-compose" in tools:
        return "Docker detected"
    return "No containerization detected"


def get_monitoring_hint(report: Dict[str, Any]) -> str:
    """Generate AI hint for monitoring"""
    tools = [t["detected_value"] for t in report.get("tools", [])]
    monitoring_tools = [
        t
        for t in tools
        if any(mon in t for mon in ["prometheus", "grafana", "datadog", "newrelic"])
    ]
    if monitoring_tools:
        return f"Detected: {', '.join(monitoring_tools)}"
    return "No monitoring tools detected"


def no_hint(report: Dict[str, Any]) -> str:
    """Default hint - no AI recommendation"""
    return ""


# ============================================================================
# DEFAULT VALUE GENERATORS
# ============================================================================


def default_project_types(report: Dict[str, Any]) -> List[str]:
    """Get default project types from detection"""
    return [pt["detected_value"] for pt in report.get("project_types", [])] or ["backend"]


def default_primary_language(report: Dict[str, Any]) -> str:
    """Get default primary language from detection"""
    languages = report.get("languages", [])
    return languages[0]["detected_value"] if languages else "python"


def default_secondary_languages(report: Dict[str, Any]) -> List[str]:
    """Get default secondary languages from detection"""
    languages = report.get("languages", [])
    return [lang["detected_value"] for lang in languages[1:3]]


def default_frameworks(report: Dict[str, Any]) -> List[str]:
    """Get default frameworks from detection"""
    return [fw["detected_value"] for fw in report.get("frameworks", [])]


def default_deployment_target(report: Dict[str, Any]) -> List[str]:
    """Get default deployment target from detection"""
    tools = [t["detected_value"] for t in report.get("tools", [])]
    if "kubernetes" in tools:
        return ["kubernetes"]
    elif "docker" in tools:
        return ["docker"]
    return ["cloud-other"]


def default_scale(report: Dict[str, Any]) -> str:
    """Get default expected scale from codebase size"""
    patterns = report.get("codebase_patterns", {})
    total_files = patterns.get("total_files", 0)
    if total_files > LARGE_CODEBASE_THRESHOLD:
        return "enterprise"
    elif total_files > MEDIUM_CODEBASE_THRESHOLD:
        return "growth"
    elif total_files > SMALL_CODEBASE_THRESHOLD:
        return "startup"
    return "startup"


def default_maturity(report: Dict[str, Any]) -> str:
    """Get default project maturity from infrastructure"""
    patterns = report.get("codebase_patterns", {})
    has_tests = patterns.get("has_tests", False)
    has_ci = patterns.get("has_ci_cd", False)

    if has_tests and has_ci:
        return "active-dev"
    elif has_tests or has_ci:
        return "active-dev"
    return "greenfield"


def default_infrastructure(report: Dict[str, Any]) -> List[str]:
    """Get default infrastructure from detection"""
    tools = [t["detected_value"] for t in report.get("tools", [])]
    result = []
    if "kubernetes" in tools:
        result.append("kubernetes")
    if "docker" in tools or "docker-compose" in tools:
        result.append("docker-compose")
    return result or ["docker-compose"]


# ============================================================================
# QUESTION DEFINITIONS (Choices from Schema)
# ============================================================================

QUESTIONS = [
    # ========================================================================
    # CATEGORY 1: Project Identity (12 questions)
    # ========================================================================
    {
        "category": "project_identity",
        "field": "name",
        "type": "text",
        "prompt": "What is your project name?",
        "ai_hint": lambda report: f"Detected from: {report.get('project_root', 'current directory')}",
        "default": lambda report: report.get("project_root", "").split("/")[-1] or "my-project",
        "required": True,
    },
    {
        "category": "project_identity",
        "field": "types",
        "type": "multi_choice",
        "prompt": "What type(s) of project is this? (select multiple)",
        "choices": get_literal_choices(ProjectTypeChoice),  # ← FROM SCHEMA!
        "ai_hint": get_project_type_hint,
        "default": default_project_types,
    },
    {
        "category": "project_identity",
        "field": "primary_language",
        "type": "text",
        "prompt": "What is the primary programming language?",
        "ai_hint": get_language_hint,
        "default": default_primary_language,
        "required": True,
    },
    {
        "category": "project_identity",
        "field": "secondary_languages",
        "type": "multi_text",
        "prompt": "Any secondary languages? (comma-separated, or blank)",
        "ai_hint": lambda report: f"Detected: {', '.join([l['detected_value'] for l in report.get('languages', [])[1:]])}",
        "default": default_secondary_languages,
    },
    {
        "category": "project_identity",
        "field": "frameworks",
        "type": "multi_text",
        "prompt": "What frameworks are you using? (comma-separated, or blank)",
        "ai_hint": get_framework_hint,
        "default": default_frameworks,
    },
    {
        "category": "project_identity",
        "field": "deployment_target",
        "type": "multi_choice",
        "prompt": "Where will this be deployed? (select all that apply)",
        "choices": get_literal_choices(DeploymentTargetChoice),  # ← FROM SCHEMA!
        "ai_hint": get_deployment_hint,
        "default": default_deployment_target,
    },
    {
        "category": "project_identity",
        "field": "expected_scale",
        "type": "choice",
        "prompt": "What is the expected traffic/usage scale?",
        "choices": get_literal_choices(ExpectedScaleChoice),  # ← FROM SCHEMA!
        "ai_hint": get_scale_hint,
        "default": default_scale,
    },
    {
        "category": "project_identity",
        "field": "business_domain",
        "type": "multi_choice",
        "prompt": "What business domain(s) does this project serve? (select all that apply)",
        "choices": get_literal_choices(BusinessDomainChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: ["general-purpose"],
    },
    {
        "category": "project_identity",
        "field": "compliance_requirements",
        "type": "multi_choice",
        "prompt": "Any regulatory compliance requirements? (select all that apply)",
        "choices": get_literal_choices(ComplianceChoice),  # ← FROM SCHEMA!
        "ai_hint": get_compliance_hint,
        "default": lambda report: ["none"],
    },
    {
        "category": "project_identity",
        "field": "project_maturity",
        "type": "choice",
        "prompt": "What is the current project stage?",
        "choices": get_literal_choices(ProjectMaturityChoice),  # ← FROM SCHEMA!
        "ai_hint": get_maturity_hint,
        "default": default_maturity,
    },
    {
        "category": "project_identity",
        "field": "team_trajectory",
        "type": "choice",
        "prompt": "What is your current and expected team size?",
        "choices": get_literal_choices(TeamSizeChoice),  # ← FROM SCHEMA!
        "ai_hint": get_team_size_hint,
        "default": lambda report: "solo",
    },
    {
        "category": "project_identity",
        "field": "license_model",
        "type": "choice",
        "prompt": "What is your licensing strategy?",
        "choices": get_literal_choices(LicenseChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: "proprietary",
    },
    # ========================================================================
    # CATEGORY 2: Development Style (8 questions)
    # ========================================================================
    {
        "category": "development_style",
        "field": "code_philosophy",
        "type": "choice",
        "prompt": "What is your code philosophy?",
        "choices": get_literal_choices(CodePhilosophyChoice),  # ← FROM SCHEMA!
        "ai_hint": lambda report: "Recommend balanced for most projects",
        "default": lambda report: "balanced",
    },
    {
        "category": "development_style",
        "field": "development_pace",
        "type": "choice",
        "prompt": "What is your development pace preference?",
        "choices": get_literal_choices(DevelopmentPaceChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: "balanced",
    },
    {
        "category": "development_style",
        "field": "tdd_adherence",
        "type": "choice",
        "prompt": "What is your test-driven development approach?",
        "choices": get_literal_choices(TDDAdherenceChoice),  # ← FROM SCHEMA!
        "ai_hint": lambda report: "Most teams benefit from pragmatic-tests",
        "default": lambda report: "pragmatic-tests",
    },
    {
        "category": "development_style",
        "field": "refactoring_frequency",
        "type": "choice",
        "prompt": "How often do you refactor?",
        "choices": get_literal_choices(RefactoringChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: "when-needed",
    },
    {
        "category": "development_style",
        "field": "breaking_changes_policy",
        "type": "choice",
        "prompt": "What is your policy for breaking changes?",
        "choices": get_literal_choices(BreakingChangesChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: "semver-major",
    },
    {
        "category": "development_style",
        "field": "code_review_strictness",
        "type": "choice",
        "prompt": "What are your code review requirements?",
        "choices": get_literal_choices(CodeReviewChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: "mandatory-all",
        "skip_if": lambda answers: answers.get("team_trajectory") == "solo",
    },
    {
        "category": "development_style",
        "field": "pair_programming",
        "type": "choice",
        "prompt": "How often do you pair program?",
        "choices": get_literal_choices(PairProgrammingChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: "complex-tasks",
        "skip_if": lambda answers: answers.get("team_trajectory") == "solo",
    },
    {
        "category": "development_style",
        "field": "feature_flags",
        "type": "choice",
        "prompt": "How do you use feature flags?",
        "choices": get_literal_choices(FeatureFlagsChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: "major-features",
    },
    # ========================================================================
    # CATEGORY 3: Code Quality Standards (10 questions)
    # ========================================================================
    {
        "category": "code_quality",
        "field": "linting_strictness",
        "type": "choice",
        "prompt": "What is your linter strictness level?",
        "choices": get_literal_choices(LintingStrictnessChoice),  # ← FROM SCHEMA!
        "ai_hint": get_linting_hint,
        "default": lambda report: "strict",
    },
    {
        "category": "code_quality",
        "field": "type_coverage_target",
        "type": "choice",
        "prompt": "What is your type annotation coverage target?",
        "choices": get_literal_choices(TypeCoverageChoice),  # ← FROM SCHEMA!
        "ai_hint": get_type_coverage_hint,
        "default": lambda report: "90",
    },
    {
        "category": "code_quality",
        "field": "cyclomatic_complexity_limit",
        "type": "int",
        "prompt": "Max cyclomatic complexity (5-50, or 0 for no limit)?",
        "ai_hint": no_hint,
        "default": lambda report: 10,
        "min": 0,
        "max": 50,
    },
    {
        "category": "code_quality",
        "field": "function_length_limit",
        "type": "int",
        "prompt": "Max function length in lines (20-200, or 0 for no limit)?",
        "ai_hint": no_hint,
        "default": lambda report: 50,
        "min": 0,
        "max": 200,
    },
    {
        "category": "code_quality",
        "field": "dry_enforcement",
        "type": "choice",
        "prompt": "What is your DRY (Don't Repeat Yourself) enforcement level?",
        "choices": get_literal_choices(DRYEnforcementChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: "pragmatic",
    },
    {
        "category": "code_quality",
        "field": "code_comment_density",
        "type": "choice",
        "prompt": "What is your expected code comment frequency?",
        "choices": get_literal_choices(CodeCommentChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: "moderate",
    },
    {
        "category": "code_quality",
        "field": "naming_convention_strictness",
        "type": "choice",
        "prompt": "What is your naming convention enforcement?",
        "choices": get_literal_choices(NamingConventionChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: "enforced",
    },
    {
        "category": "code_quality",
        "field": "magic_number_tolerance",
        "type": "choice",
        "prompt": "What is your magic number policy?",
        "choices": get_literal_choices(MagicNumberChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: "named-constants",
    },
    {
        "category": "code_quality",
        "field": "import_organization",
        "type": "choice",
        "prompt": "How should import statements be organized?",
        "choices": get_literal_choices(ImportOrganizationChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: "grouped-logical",
    },
    {
        "category": "code_quality",
        "field": "line_length_limit",
        "type": "choice",
        "prompt": "What is your max line length?",
        "choices": get_literal_choices(LineLengthChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: "100",
    },
    # ========================================================================
    # CATEGORY 4: Documentation Preferences (8 questions)
    # ========================================================================
    {
        "category": "documentation",
        "field": "verbosity",
        "type": "choice",
        "prompt": "What is your documentation detail level?",
        "choices": get_literal_choices(DocVerbosityChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: "concise",
    },
    {
        "category": "documentation",
        "field": "target_audience",
        "type": "choice",
        "prompt": "What is your primary documentation audience?",
        "choices": get_literal_choices(DocAudienceChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: "intermediate",
    },
    {
        "category": "documentation",
        "field": "documentation_style",
        "type": "choice",
        "prompt": "What is your documentation approach?",
        "choices": get_literal_choices(DocStyleChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: "hybrid",
    },
    {
        "category": "documentation",
        "field": "inline_documentation",
        "type": "choice",
        "prompt": "What is your inline docstring coverage?",
        "choices": get_literal_choices(InlineDocChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: "public-api",
    },
    {
        "category": "documentation",
        "field": "changelog_detail",
        "type": "choice",
        "prompt": "What is your changelog detail level?",
        "choices": get_literal_choices(ChangelogChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: "notable-changes",
        "skip_if": lambda answers: answers.get("verbosity") == "minimal",
    },
    {
        "category": "documentation",
        "field": "architecture_diagrams",
        "type": "choice",
        "prompt": "When should you include architecture diagrams?",
        "choices": get_literal_choices(ArchitectureDiagramsChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: "complex-areas",
        "skip_if": lambda answers: answers.get("verbosity") == "minimal",
    },
    {
        "category": "documentation",
        "field": "api_documentation",
        "type": "choice",
        "prompt": "What is your API documentation format?",
        "choices": get_literal_choices(APIDocChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: "openapi-spec",
        "skip_if": lambda answers: not any(
            t in answers.get("types", []) for t in ["api", "backend", "microservice"]
        ),
    },
    {
        "category": "documentation",
        "field": "readme_length",
        "type": "choice",
        "prompt": "What is your README.md target length?",
        "choices": get_literal_choices(ReadmeLengthChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: "concise",
    },
    # ========================================================================
    # CATEGORY 5: Testing Strategy (7 questions)
    # ========================================================================
    {
        "category": "testing",
        "field": "coverage_target",
        "type": "choice",
        "prompt": "What is your test coverage target?",
        "choices": get_literal_choices(TestCoverageChoice),  # ← FROM SCHEMA!
        "ai_hint": get_testing_coverage_hint,
        "default": lambda report: "90",
    },
    {
        "category": "testing",
        "field": "test_pyramid_ratio",
        "type": "choice",
        "prompt": "What is your Unit/Integration/E2E test ratio?",
        "choices": get_literal_choices(TestPyramidChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: "70-20-10",
        "skip_if": lambda answers: answers.get("coverage_target") in ["none", "not-set", "0"],
    },
    {
        "category": "testing",
        "field": "mutation_testing",
        "type": "choice",
        "prompt": "What is your mutation testing usage?",
        "choices": get_literal_choices(MutationTestingChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: "optional",
        "skip_if": lambda answers: answers.get("coverage_target") in ["none", "not-set", "0"],
    },
    {
        "category": "testing",
        "field": "property_based_testing",
        "type": "choice",
        "prompt": "What is your property-based testing approach?",
        "choices": get_literal_choices(PropertyTestingChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: "complex-logic",
        "skip_if": lambda answers: answers.get("coverage_target") in ["none", "not-set", "0"],
    },
    {
        "category": "testing",
        "field": "test_isolation",
        "type": "choice",
        "prompt": "What are your test isolation requirements?",
        "choices": get_literal_choices(TestIsolationChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: "pragmatic-fixtures",
    },
    {
        "category": "testing",
        "field": "test_naming",
        "type": "choice",
        "prompt": "What is your test naming convention?",
        "choices": get_literal_choices(TestNamingChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: "descriptive-sentences",
    },
    {
        "category": "testing",
        "field": "mocking_philosophy",
        "type": "choice",
        "prompt": "What is your mocking approach?",
        "choices": get_literal_choices(MockingChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: "balanced",
    },
    # ========================================================================
    # CATEGORY 6: Security Posture (6 questions)
    # ========================================================================
    {
        "category": "security",
        "field": "security_stance",
        "type": "choice",
        "prompt": "What is your overall security approach?",
        "choices": get_literal_choices(SecurityStanceChoice),  # ← FROM SCHEMA!
        "ai_hint": get_security_stance_hint,
        "default": lambda report: "balanced",
    },
    {
        "category": "security",
        "field": "secret_management",
        "type": "multi_choice",
        "prompt": "What secret management methods do you use? (select all that apply)",
        "choices": get_literal_choices(SecretManagementChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: ["env-vars"],
    },
    {
        "category": "security",
        "field": "encryption_scope",
        "type": "multi_choice",
        "prompt": "What data do you encrypt? (select all that apply)",
        "choices": get_literal_choices(EncryptionScopeChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: ["at-rest-sensitive", "in-transit-external"],
    },
    {
        "category": "security",
        "field": "audit_logging",
        "type": "multi_choice",
        "prompt": "What events do you log for audit purposes? (select all that apply)",
        "choices": get_literal_choices(AuditLoggingChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: ["authentication", "authorization", "data-modification"],
    },
    {
        "category": "security",
        "field": "input_validation",
        "type": "choice",
        "prompt": "What is your input validation strategy?",
        "choices": get_literal_choices(InputValidationChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: "external-only",
    },
    {
        "category": "security",
        "field": "dependency_scanning",
        "type": "choice",
        "prompt": "How often do you scan for dependency vulnerabilities?",
        "choices": get_literal_choices(DependencyScanningChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: "every-pr",
    },
    # ========================================================================
    # CATEGORY 7: Performance vs Maintainability (5 questions)
    # ========================================================================
    {
        "category": "performance",
        "field": "optimization_priority",
        "type": "choice",
        "prompt": "What is your optimization philosophy?",
        "choices": get_literal_choices(OptimizationPriorityChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: "balanced",
    },
    {
        "category": "performance",
        "field": "caching_strategy",
        "type": "choice",
        "prompt": "What is your caching approach?",
        "choices": get_literal_choices(CachingStrategyChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: "selective",
    },
    {
        "category": "performance",
        "field": "database_queries",
        "type": "choice",
        "prompt": "What is your database query approach?",
        "choices": get_literal_choices(DatabaseQueriesChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: "orm-with-indexes",
    },
    {
        "category": "performance",
        "field": "premature_optimization",
        "type": "choice",
        "prompt": "What is your premature optimization policy?",
        "choices": get_literal_choices(PrematureOptimizationChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: "profile-first",
    },
    {
        "category": "performance",
        "field": "duplication_for_performance",
        "type": "choice",
        "prompt": "Do you allow code duplication for performance?",
        "choices": get_literal_choices(DuplicationForPerfChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: "contextual",
    },
    # ========================================================================
    # CATEGORY 8: Team Collaboration (4 questions)
    # ========================================================================
    {
        "category": "collaboration",
        "field": "git_workflow",
        "type": "choice",
        "prompt": "What is your Git branching strategy?",
        "choices": get_literal_choices(GitWorkflowChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: "github-flow",
        "skip_if": lambda answers: answers.get("team_trajectory") == "solo",
    },
    {
        "category": "collaboration",
        "field": "commit_convention",
        "type": "choice",
        "prompt": "What is your commit message format?",
        "choices": get_literal_choices(CommitConventionChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: "conventional-suggested",
        "skip_if": lambda answers: answers.get("team_trajectory") == "solo",
    },
    {
        "category": "collaboration",
        "field": "pr_size_limit",
        "type": "choice",
        "prompt": "What is your pull request size limit?",
        "choices": get_literal_choices(PRSizeChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: "medium-500",
        "skip_if": lambda answers: answers.get("team_trajectory") == "solo",
    },
    {
        "category": "collaboration",
        "field": "code_ownership",
        "type": "choice",
        "prompt": "What is your code ownership model?",
        "choices": get_literal_choices(CodeOwnershipChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: "team-ownership",
        "skip_if": lambda answers: answers.get("team_trajectory") == "solo",
    },
    # ========================================================================
    # CATEGORY 9: DevOps Automation (6 questions)
    # ========================================================================
    {
        "category": "devops",
        "field": "ci_cd_trigger",
        "type": "choice",
        "prompt": "When should CI/CD execute?",
        "choices": get_literal_choices(CICDTriggerChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: "every-pr",
    },
    {
        "category": "devops",
        "field": "deployment_frequency",
        "type": "choice",
        "prompt": "What is your deployment cadence?",
        "choices": get_literal_choices(DeploymentFrequencyChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: "manual",
        "skip_if": lambda answers: answers.get("ci_cd_trigger") == "manual",
    },
    {
        "category": "devops",
        "field": "rollback_strategy",
        "type": "choice",
        "prompt": "What is your rollback approach?",
        "choices": get_literal_choices(RollbackStrategyChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: "manual-approval",
        "skip_if": lambda answers: answers.get("ci_cd_trigger") == "manual",
    },
    {
        "category": "devops",
        "field": "infrastructure",
        "type": "multi_choice",
        "prompt": "What infrastructure platforms do you use? (select all that apply)",
        "choices": get_literal_choices(InfrastructureChoice),  # ← FROM SCHEMA!
        "ai_hint": get_infrastructure_hint,
        "default": default_infrastructure,
    },
    {
        "category": "devops",
        "field": "monitoring",
        "type": "multi_choice",
        "prompt": "What monitoring and observability tools do you use? (select all that apply)",
        "choices": get_literal_choices(MonitoringChoice),  # ← FROM SCHEMA!
        "ai_hint": get_monitoring_hint,
        "default": lambda report: ["prometheus", "grafana"],
    },
    {
        "category": "devops",
        "field": "environment_count",
        "type": "multi_choice",
        "prompt": "What environments do you maintain? (select all that apply)",
        "choices": get_literal_choices(EnvironmentChoice),  # ← FROM SCHEMA!
        "ai_hint": no_hint,
        "default": lambda report: ["dev", "prod"],
    },
]


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================


def get_filtered_questions(answers: Dict[str, Any]) -> List[Dict]:
    """
    Get list of questions to ask, filtering based on conditional logic.

    Args:
        answers: Dictionary of answers collected so far

    Returns:
        List of questions that should be asked
    """
    filtered = []
    for q in QUESTIONS:
        # Check if question has skip condition
        if "skip_if" in q:
            try:
                if q["skip_if"](answers):
                    continue  # Skip this question
            except Exception:
                pass  # If skip check fails, ask the question anyway

        filtered.append(q)

    return filtered


def count_questions_for_answers(answers: Dict[str, Any]) -> int:
    """Count how many questions will be asked given current answers"""
    return len(get_filtered_questions(answers))
