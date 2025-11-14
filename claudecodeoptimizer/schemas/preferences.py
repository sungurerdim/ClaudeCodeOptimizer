"""
Universal Preference Schema - CCO

SINGLE SOURCE OF TRUTH for all choices.
All question choices are derived from Literal types here.
100% generic - works for any programming language, framework, or project type.
"""

from datetime import datetime
from typing import List, Literal, Optional, get_args

from pydantic import BaseModel, Field

from .. import __version__ as cco_version

# ============================================================================
# TYPE DEFINITIONS (Single Source of Truth)
# ============================================================================

# Project Identity Types
ProjectTypeChoice = Literal[
    "api",
    "backend",
    "frontend",
    "fullstack",
    "web-app",
    "spa",
    "ssr",
    "microservice",
    "monolith",
    "serverless",
    "ml",
    "ml-training",
    "ml-inference",
    "data-pipeline",
    "etl",
    "analytics",
    "cli",
    "library",
    "sdk",
    "framework",
    "desktop",
    "mobile",
    "mobile-native",
    "mobile-hybrid",
    "embedded",
    "iot",
    "game",
    "blockchain",
    "devtools",
    "testing-framework",
    "automation",
]

DeploymentTargetChoice = Literal[
    "cloud-aws",
    "cloud-gcp",
    "cloud-azure",
    "cloud-alibaba",
    "cloud-other",
    "on-prem",
    "hybrid",
    "edge",
    "cdn",
    "desktop",
    "mobile",
    "embedded",
    "kubernetes",
    "docker",
    "serverless",
    "paas",
    "bare-metal",
    "containers",
]

ExpectedScaleChoice = Literal[
    "hobby",
    "personal",
    "startup",
    "small-business",
    "growth",
    "scale-up",
    "enterprise",
    "unicorn",
    "global-scale",
    "fortune-500",
]

BusinessDomainChoice = Literal[
    "fintech",
    "banking",
    "payments",
    "insurance",
    "trading",
    "healthcare",
    "medtech",
    "biotech",
    "telemedicine",
    "e-commerce",
    "retail",
    "marketplace",
    "saas",
    "paas",
    "education",
    "edtech",
    "lms",
    "social-media",
    "messaging",
    "communication",
    "entertainment",
    "gaming",
    "streaming",
    "media",
    "logistics",
    "supply-chain",
    "transportation",
    "real-estate",
    "proptech",
    "energy",
    "cleantech",
    "utilities",
    "government",
    "civic-tech",
    "public-sector",
    "manufacturing",
    "industrial",
    "iot",
    "agriculture",
    "agtech",
    "legal",
    "legaltech",
    "compliance",
    "hr",
    "hrtech",
    "recruiting",
    "marketing",
    "martech",
    "advertising",
    "analytics",
    "business-intelligence",
    "data-science",
    "cybersecurity",
    "infosec",
    "devtools",
    "infrastructure",
    "monitoring",
    "other",
    "general-purpose",
]

ComplianceChoice = Literal[
    "gdpr",
    "ccpa",
    "lgpd",
    "pdpa",
    "hipaa",
    "hitech",
    "fda",
    "sox",
    "mifid",
    "basel-iii",
    "pci-dss",
    "pa-dss",
    "soc2",
    "soc2-type1",
    "soc2-type2",
    "iso27001",
    "iso27017",
    "iso27018",
    "fedramp",
    "fisma",
    "itar",
    "coppa",
    "ferpa",
    "fips-140-2",
    "fips-199",
    "nist",
    "cis-benchmarks",
    "wcag",
    "ada",
    "none",
]

ProjectMaturityChoice = Literal[
    "concept",
    "prototype",
    "mvp",
    "greenfield",
    "alpha",
    "beta",
    "active-dev",
    "production",
    "stable",
    "maintenance",
    "legacy",
    "legacy-migration",
    "sunset",
    "archived",
]

TeamSizeChoice = Literal[
    "solo",
    "duo",
    "small-2-5",
    "medium-5-10",
    "medium-10-20",
    "large-20-50",
    "large-50-100",
    "xlarge-100-500",
    "enterprise-500plus",
]

LicenseChoice = Literal["proprietary", "open-source", "dual-license"]

# Development Style Types
CodePhilosophyChoice = Literal[
    "legacy-maintenance",
    "very-conservative",
    "conservative",
    "pragmatic",
    "balanced",
    "modern",
    "progressive",
    "cutting-edge",
    "bleeding-edge",
    "experimental",
]

DevelopmentPaceChoice = Literal[
    "move-fast-break-things",
    "rapid-prototype",
    "agile-fast",
    "balanced",
    "measured",
    "deliberate-design",
    "waterfall",
    "slow-and-steady",
]

TDDAdherenceChoice = Literal[
    "strict-tdd",
    "tdd-preferred",
    "pragmatic-tests",
    "test-alongside",
    "test-after",
    "test-critical-only",
    "minimal",
    "no-tests",
]

RefactoringChoice = Literal["continuous", "milestone-based", "when-needed", "rarely"]
BreakingChangesChoice = Literal["never", "deprecation-cycle", "semver-major", "justified"]
CodeReviewChoice = Literal["mandatory-all", "critical-only", "optional"]
PairProgrammingChoice = Literal["always", "complex-tasks", "onboarding", "never"]
FeatureFlagsChoice = Literal["extensive", "major-features", "experiments", "none"]

# Code Quality Types
LintingStrictnessChoice = Literal[
    "disabled",
    "relaxed",
    "moderate",
    "standard",
    "strict",
    "pedantic",
    "paranoid",
    "custom",
]

TypeCoverageChoice = Literal[
    "none",
    "not-set",
    "0",
    "20",
    "40",
    "50",
    "60",
    "70",
    "75",
    "80",
    "85",
    "90",
    "95",
    "98",
    "100",
    "critical-only",
    "public-api-only",
]

DRYEnforcementChoice = Literal["zero-tolerance", "pragmatic", "relaxed"]
CodeCommentChoice = Literal["extensive", "moderate", "self-documenting"]
NamingConventionChoice = Literal["enforced", "suggested", "flexible"]
MagicNumberChoice = Literal["forbidden", "named-constants", "contextual", "allowed"]
ImportOrganizationChoice = Literal["strict-alphabetical", "grouped-logical", "flexible"]
LineLengthChoice = Literal["80", "100", "120", "none"]

# Documentation Types
DocVerbosityChoice = Literal["extensive", "concise", "minimal"]
DocAudienceChoice = Literal["beginners", "intermediate", "experts"]
DocStyleChoice = Literal["tutorial-driven", "reference-manual", "example-heavy", "hybrid"]
InlineDocChoice = Literal["every-function", "public-api", "complex-only"]
ArchitectureDiagramsChoice = Literal["required", "complex-areas", "optional"]
APIDocChoice = Literal["openapi-spec", "markdown", "code-comments"]
ReadmeLengthChoice = Literal["comprehensive", "concise", "minimal"]

# Testing Types
TestCoverageChoice = Literal[
    "none",
    "not-set",
    "0",
    "20",
    "40",
    "50",
    "60",
    "70",
    "75",
    "80",
    "85",
    "90",
    "95",
    "98",
    "100",
    "critical-only",
    "new-code-only",
]

TestPyramidChoice = Literal[
    "80-15-5",
    "70-20-10",
    "70-25-5",
    "60-30-10",
    "60-35-5",
    "50-40-10",
    "50-30-20",
    "40-40-20",
    "30-50-20",
    "custom",
    "balanced",
]

MutationTestingChoice = Literal["required", "recommended", "optional", "none"]
PropertyTestingChoice = Literal["extensive", "complex-logic", "none"]
TestIsolationChoice = Literal["strict-no-shared", "pragmatic-fixtures", "flexible"]
TestNamingChoice = Literal["descriptive-sentences", "method-name", "short"]
MockingChoice = Literal["minimal-real-deps", "balanced", "extensive-isolated"]

# Security Types
SecurityStanceChoice = Literal[
    "zero-trust",
    "paranoid",
    "very-strict",
    "strict",
    "balanced",
    "pragmatic",
    "permissive",
    "minimal",
]

SecretManagementChoice = Literal[
    "hashicorp-vault",
    "aws-secrets-manager",
    "azure-key-vault",
    "gcp-secret-manager",
    "kubernetes-secrets",
    "docker-secrets",
    "doppler",
    "infisical",
    "env-vars",
    "env-files",
    "config-files",
    "encrypted-config",
    "sops",
    "sealed-secrets",
    "age",
    "git-crypt",
    "bitwarden",
    "1password",
    "lastpass",
    "none",
    "plaintext",
]

EncryptionScopeChoice = Literal[
    "at-rest-all",
    "at-rest-sensitive",
    "at-rest-pii",
    "at-rest-payments",
    "in-transit-all",
    "in-transit-external",
    "in-transit-internal",
    "database-level",
    "application-level",
    "field-level",
    "backups",
    "logs",
    "cache",
    "session-data",
    "end-to-end",
    "client-side",
    "homomorphic",
    "minimal",
    "none",
]

AuditLoggingChoice = Literal[
    "authentication",
    "authorization",
    "data-access",
    "data-modification",
    "admin-actions",
    "config-changes",
    "privilege-escalation",
    "failed-attempts",
    "suspicious-activity",
    "compliance-events",
    "api-calls",
    "database-queries",
    "file-access",
    "user-activity",
    "system-events",
    "errors-only",
    "everything",
    "none",
]

InputValidationChoice = Literal["schema-everything", "external-only", "pragmatic"]
DependencyScanningChoice = Literal["every-commit", "every-pr", "weekly", "monthly", "none"]

# Performance Types
OptimizationPriorityChoice = Literal["performance-first", "balanced", "maintainability-first"]
CachingStrategyChoice = Literal["aggressive", "selective", "minimal", "none"]
DatabaseQueriesChoice = Literal["hand-optimized", "orm-with-indexes", "orm-simple"]
PrematureOptimizationChoice = Literal["allowed", "profile-first", "forbidden"]
DuplicationForPerfChoice = Literal["acceptable", "contextual", "never"]

# Collaboration Types
GitWorkflowChoice = Literal["git-flow", "trunk-based", "github-flow", "gitlab-flow"]
VersioningStrategyChoice = Literal[
    "auto_semver", "pr_based_semver", "manual_semver", "calver", "no_versioning"
]
CommitConventionChoice = Literal["conventional-enforced", "conventional-suggested", "freeform"]
PRSizeChoice = Literal["small-200", "medium-500", "large-1000", "no-limit"]
CodeOwnershipChoice = Literal["strict-codeowners", "team-ownership", "open"]

# DevOps Types
CICDTriggerChoice = Literal["every-commit", "every-pr", "manual", "scheduled"]
DeploymentFrequencyChoice = Literal["continuous", "daily", "weekly", "manual"]
RollbackStrategyChoice = Literal["automated", "manual-approval", "manual"]

InfrastructureChoice = Literal[
    "kubernetes",
    "k3s",
    "k8s-managed",
    "eks",
    "gke",
    "aks",
    "docker",
    "docker-compose",
    "docker-swarm",
    "podman",
    "serverless",
    "lambda",
    "cloud-functions",
    "cloud-run",
    "fargate",
    "nomad",
    "mesos",
    "openshift",
    "vms",
    "ec2",
    "gce",
    "azure-vms",
    "bare-metal",
    "on-prem",
    "hybrid",
    "paas",
    "heroku",
    "render",
    "fly-io",
    "railway",
    "edge",
    "cloudflare-workers",
    "vercel",
    "netlify",
    "ansible",
    "terraform",
    "pulumi",
    "cloudformation",
]

MonitoringChoice = Literal[
    "prometheus",
    "grafana",
    "victoria-metrics",
    "thanos",
    "datadog",
    "new-relic",
    "dynatrace",
    "appdynamics",
    "elastic-stack",
    "elk",
    "splunk",
    "sumo-logic",
    "jaeger",
    "zipkin",
    "tempo",
    "opentelemetry",
    "sentry",
    "rollbar",
    "bugsnag",
    "airbrake",
    "cloudwatch",
    "stackdriver",
    "azure-monitor",
    "uptime-kuma",
    "statping",
    "healthchecks-io",
    "pagerduty",
    "opsgenie",
    "victorops",
    "logs-only",
    "metrics-only",
    "traces-only",
    "full-observability",
    "minimal",
    "none",
]

EnvironmentChoice = Literal[
    "local",
    "dev",
    "development",
    "integration",
    "test",
    "qa",
    "staging",
    "pre-prod",
    "uat",
    "prod",
    "production",
    "canary",
    "blue-green",
    "shadow",
    "demo",
    "sandbox",
    "preview",
    "ephemeral",
    "feature-branches",
]


# ============================================================================
# PYDANTIC MODELS
# ============================================================================


class ProjectIdentity(BaseModel):
    """12 customization points - Project identification"""

    name: str = Field(..., description="Project name (auto-detected or user-provided)")

    types: List[ProjectTypeChoice] = Field(
        default=[],
        description="Project types (can be multiple)",
    )

    primary_language: str = Field(..., description="Primary programming language")

    secondary_languages: List[str] = Field(
        default=[],
        description="Additional languages",
    )

    frameworks: List[str] = Field(
        default=[],
        description="Detected frameworks",
    )

    deployment_target: List[DeploymentTargetChoice] = Field(
        default=["cloud-other"],
        description="Where this will be deployed (can be multiple)",
    )

    expected_scale: ExpectedScaleChoice = Field(
        default="startup",
        description="Expected traffic/usage scale",
    )

    business_domain: List[BusinessDomainChoice] = Field(
        default=["general-purpose"],
        description="Business domain(s)",
    )

    compliance_requirements: List[ComplianceChoice] = Field(
        default=["none"],
        description="Regulatory compliance needs",
    )

    project_maturity: ProjectMaturityChoice = Field(
        default="active-dev",
        description="Current project stage",
    )

    team_trajectory: TeamSizeChoice = Field(
        default="solo",
        description="Current and expected team size",
    )

    license_model: LicenseChoice = Field(
        default="proprietary",
        description="Licensing strategy",
    )


class DevelopmentStyle(BaseModel):
    """8 customization points - Development philosophy"""

    code_philosophy: CodePhilosophyChoice = Field(
        default="balanced",
        description="Conservative=battle-tested, Cutting-edge=latest features",
    )

    development_pace: DevelopmentPaceChoice = Field(
        default="balanced",
        description="Speed vs. design quality trade-off",
    )

    tdd_adherence: TDDAdherenceChoice = Field(
        default="pragmatic-tests",
        description="Test-driven development approach",
    )

    refactoring_frequency: RefactoringChoice = Field(
        default="when-needed",
        description="How often to refactor",
    )

    breaking_changes_policy: BreakingChangesChoice = Field(
        default="semver-major",
        description="Policy for breaking changes",
    )

    code_review_strictness: CodeReviewChoice = Field(
        default="mandatory-all",
        description="Code review requirements",
    )

    pair_programming: PairProgrammingChoice = Field(
        default="complex-tasks",
        description="Pair programming frequency",
    )

    feature_flags: FeatureFlagsChoice = Field(
        default="major-features",
        description="Feature flag usage",
    )


class CodeQualityStandards(BaseModel):
    """10 customization points - Code quality"""

    linting_strictness: LintingStrictnessChoice = Field(
        default="strict",
        description="Linter strictness level",
    )

    type_coverage_target: TypeCoverageChoice = Field(
        default="90",
        description="Type annotation coverage target",
    )

    cyclomatic_complexity_limit: Optional[int] = Field(
        10,
        ge=0,
        le=50,
        description="Max cyclomatic complexity (0 = no limit)",
    )

    function_length_limit: Optional[int] = Field(
        50,
        ge=0,
        le=200,
        description="Max function length in lines (0 = no limit)",
    )

    dry_enforcement: DRYEnforcementChoice = Field(
        default="pragmatic",
        description="Don't Repeat Yourself enforcement level",
    )

    code_comment_density: CodeCommentChoice = Field(
        default="moderate",
        description="Expected code comment frequency",
    )

    naming_convention_strictness: NamingConventionChoice = Field(
        default="enforced",
        description="Naming convention enforcement",
    )

    magic_number_tolerance: MagicNumberChoice = Field(
        default="named-constants",
        description="Magic number policy",
    )

    import_organization: ImportOrganizationChoice = Field(
        default="grouped-logical",
        description="Import statement organization",
    )

    line_length_limit: LineLengthChoice = Field(
        default="100",
        description="Max line length",
    )


class DocumentationPreferences(BaseModel):
    """7 customization points - Documentation"""

    verbosity: DocVerbosityChoice = Field(
        default="concise",
        description="Documentation detail level",
    )

    target_audience: DocAudienceChoice = Field(
        default="intermediate",
        description="Primary documentation audience",
    )

    documentation_style: DocStyleChoice = Field(
        default="hybrid",
        description="Documentation approach",
    )

    inline_documentation: InlineDocChoice = Field(
        default="public-api",
        description="Inline docstring coverage",
    )

    architecture_diagrams: ArchitectureDiagramsChoice = Field(
        default="complex-areas",
        description="When to include architecture diagrams",
    )

    api_documentation: APIDocChoice = Field(
        default="openapi-spec",
        description="API documentation format",
    )

    readme_length: ReadmeLengthChoice = Field(
        default="concise",
        description="README.md target length",
    )


class TestingStrategy(BaseModel):
    """7 customization points - Testing"""

    coverage_target: TestCoverageChoice = Field(
        default="90",
        description="Test coverage target",
    )

    test_pyramid_ratio: TestPyramidChoice = Field(
        default="70-20-10",
        description="Unit/Integration/E2E test ratio",
    )

    mutation_testing: MutationTestingChoice = Field(
        default="optional",
        description="Mutation testing usage",
    )

    property_based_testing: PropertyTestingChoice = Field(
        default="complex-logic",
        description="Property-based testing approach",
    )

    test_isolation: TestIsolationChoice = Field(
        default="pragmatic-fixtures",
        description="Test isolation requirements",
    )

    test_naming: TestNamingChoice = Field(
        default="descriptive-sentences",
        description="Test naming convention",
    )

    mocking_philosophy: MockingChoice = Field(
        default="balanced",
        description="Mocking approach",
    )


class SecurityPosture(BaseModel):
    """6 customization points - Security"""

    security_stance: SecurityStanceChoice = Field(
        default="balanced",
        description="Overall security approach",
    )

    secret_management: List[SecretManagementChoice] = Field(
        default=["env-vars"],
        description="Secret management methods (can be multiple)",
    )

    encryption_scope: List[EncryptionScopeChoice] = Field(
        default=["at-rest-sensitive", "in-transit-external"],
        description="Data encryption scope (can be multiple)",
    )

    audit_logging: List[AuditLoggingChoice] = Field(
        default=["authentication", "authorization", "data-modification"],
        description="Audit logging events (can be multiple)",
    )

    input_validation: InputValidationChoice = Field(
        default="external-only",
        description="Input validation strategy",
    )

    dependency_scanning: DependencyScanningChoice = Field(
        default="every-pr",
        description="Dependency vulnerability scanning frequency",
    )


class PerformanceVsMaintainability(BaseModel):
    """5 customization points - Performance"""

    optimization_priority: OptimizationPriorityChoice = Field(
        default="balanced",
        description="Optimization philosophy",
    )

    caching_strategy: CachingStrategyChoice = Field(
        default="selective",
        description="Caching approach",
    )

    database_queries: DatabaseQueriesChoice = Field(
        default="orm-with-indexes",
        description="Database query approach",
    )

    premature_optimization: PrematureOptimizationChoice = Field(
        default="profile-first",
        description="Premature optimization policy",
    )

    duplication_for_performance: DuplicationForPerfChoice = Field(
        default="contextual",
        description="Allow code duplication for performance",
    )


class TeamCollaboration(BaseModel):
    """5 customization points - Collaboration"""

    git_workflow: GitWorkflowChoice = Field(
        default="github-flow",
        description="Git branching strategy",
    )

    versioning_strategy: VersioningStrategyChoice = Field(
        default="auto_semver",
        description="Version bumping strategy (automated semantic versioning)",
    )

    commit_convention: CommitConventionChoice = Field(
        default="conventional-suggested",
        description="Commit message format",
    )

    pr_size_limit: PRSizeChoice = Field(
        default="medium-500",
        description="Pull request size limit",
    )

    code_ownership: CodeOwnershipChoice = Field(
        default="team-ownership",
        description="Code ownership model",
    )


class DevOpsAutomation(BaseModel):
    """6 customization points - DevOps"""

    ci_cd_trigger: CICDTriggerChoice = Field(
        default="every-pr",
        description="When should CI/CD execute",
    )

    deployment_frequency: DeploymentFrequencyChoice = Field(
        default="manual",
        description="Deployment cadence",
    )

    rollback_strategy: RollbackStrategyChoice = Field(
        default="manual-approval",
        description="Rollback approach",
    )

    infrastructure: List[InfrastructureChoice] = Field(
        default=["docker-compose"],
        description="Infrastructure platforms (can be multiple)",
    )

    monitoring: List[MonitoringChoice] = Field(
        default=["prometheus", "grafana"],
        description="Monitoring and observability tools (can be multiple)",
    )

    environment_count: List[EnvironmentChoice] = Field(
        default=["dev", "prod"],
        description="Environments maintained (can be multiple)",
    )


class CCOPreferences(BaseModel):
    """
    Complete CCO configuration - 66 customization points across 9 categories
    """

    project_identity: ProjectIdentity
    development_style: DevelopmentStyle = Field(default_factory=DevelopmentStyle)
    code_quality: CodeQualityStandards = Field(default_factory=CodeQualityStandards)
    documentation: DocumentationPreferences = Field(default_factory=DocumentationPreferences)
    testing: TestingStrategy = Field(default_factory=TestingStrategy)
    security: SecurityPosture = Field(default_factory=SecurityPosture)
    performance: PerformanceVsMaintainability = Field(default_factory=PerformanceVsMaintainability)
    collaboration: TeamCollaboration = Field(default_factory=TeamCollaboration)
    devops: DevOpsAutomation = Field(default_factory=DevOpsAutomation)

    # Principle Selection
    selected_principle_ids: List[str] = Field(
        default=[],
        description="User-selected principle IDs (from 53 principles)",
    )

    # Metadata
    cco_version: str = Field(default=cco_version, description="CCO version")
    configured_at: datetime = Field(
        default_factory=datetime.now,
        description="Configuration timestamp",
    )
    last_updated: datetime = Field(
        default_factory=datetime.now,
        description="Last update timestamp",
    )


# ============================================================================
# UTILITY FUNCTIONS - Extract choices from Literal types
# ============================================================================


def get_literal_choices(literal_type: type) -> List[str]:
    """Extract all choices from a Literal type annotation"""
    return list(get_args(literal_type))


# Export all choice types for use in questions.py
__all__ = [
    "CCOPreferences",
    "ProjectIdentity",
    "DevelopmentStyle",
    "CodeQualityStandards",
    "DocumentationPreferences",
    "TestingStrategy",
    "SecurityPosture",
    "PerformanceVsMaintainability",
    "TeamCollaboration",
    "DevOpsAutomation",
    # Choice types
    "ProjectTypeChoice",
    "DeploymentTargetChoice",
    "ExpectedScaleChoice",
    "BusinessDomainChoice",
    "ComplianceChoice",
    "ProjectMaturityChoice",
    "TeamSizeChoice",
    "LicenseChoice",
    "CodePhilosophyChoice",
    "DevelopmentPaceChoice",
    "TDDAdherenceChoice",
    "RefactoringChoice",
    "BreakingChangesChoice",
    "CodeReviewChoice",
    "PairProgrammingChoice",
    "FeatureFlagsChoice",
    "LintingStrictnessChoice",
    "TypeCoverageChoice",
    "DRYEnforcementChoice",
    "CodeCommentChoice",
    "NamingConventionChoice",
    "MagicNumberChoice",
    "ImportOrganizationChoice",
    "LineLengthChoice",
    "DocVerbosityChoice",
    "DocAudienceChoice",
    "DocStyleChoice",
    "InlineDocChoice",
    "ArchitectureDiagramsChoice",
    "APIDocChoice",
    "ReadmeLengthChoice",
    "TestCoverageChoice",
    "TestPyramidChoice",
    "MutationTestingChoice",
    "PropertyTestingChoice",
    "TestIsolationChoice",
    "TestNamingChoice",
    "MockingChoice",
    "SecurityStanceChoice",
    "SecretManagementChoice",
    "EncryptionScopeChoice",
    "AuditLoggingChoice",
    "InputValidationChoice",
    "DependencyScanningChoice",
    "OptimizationPriorityChoice",
    "CachingStrategyChoice",
    "DatabaseQueriesChoice",
    "PrematureOptimizationChoice",
    "DuplicationForPerfChoice",
    "GitWorkflowChoice",
    "CommitConventionChoice",
    "PRSizeChoice",
    "CodeOwnershipChoice",
    "CICDTriggerChoice",
    "DeploymentFrequencyChoice",
    "RollbackStrategyChoice",
    "InfrastructureChoice",
    "MonitoringChoice",
    "EnvironmentChoice",
    # Utility
    "get_literal_choices",
]
