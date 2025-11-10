"""
Complete Decision Tree for CCO Wizard (TIER 1-3)

Defines all decision points in hierarchical order.
Both Interactive and Quick modes use the same tree.

Structure:
- TIER 1: Fundamental decisions (Purpose, Team, Maturity, Philosophy)
- TIER 2: Strategy decisions (Principles, Testing, Security, Docs)
- TIER 3: Tactical decisions (Tool preferences, Commands)
- TIER 0: System detection (automatic, in system_detection.py)
- TIER 4: System-specific (automatic adaptation)
"""

from .context_matrix import ContextMatrix
from .models import AnswerContext, DecisionPoint, Option
from .recommendations import RecommendationEngine
from .tool_comparison import ToolComparator
from .validators import validate_no_conflicts

# Initialize engines
_rec_engine = RecommendationEngine()
_context_matrix = ContextMatrix()


# ============================================================================
# TIER 1: Fundamental Decisions (Foundation)
# ============================================================================

TIER1_PROJECT_PURPOSE = DecisionPoint(
    id="project_purpose",
    tier=1,
    category="project_identity",
    question="What type of project is this?",
    why_this_question="🎯 Understanding your project type helps us recommend relevant principles and tools",
    multi_select=True,
    validator=validate_no_conflicts,
    options=[
        # Backend Services (1-2)
        Option(
            value="api_service",
            label="API Service",
            description="Pure backend API (REST/GraphQL/gRPC), no UI",
            recommended_for=["fastapi", "flask", "express", "spring", "gin"],
            effects="Focus on: API design, performance, security, data validation",
            conflicts_with=["web_app", "spa"],
        ),
        Option(
            value="microservice",
            label="Microservice",
            description="Part of distributed system, service mesh",
            recommended_for=["docker", "kubernetes", "service-mesh"],
            effects="Focus on: Inter-service communication, resilience, observability",
            conflicts_with=[],
        ),
        # Frontend/Full-Stack (3-4)
        Option(
            value="web_app",
            label="Web Application (Full-Stack)",
            description="Frontend + backend integrated, monolithic or modular",
            recommended_for=["next", "nuxt", "django", "rails"],
            effects="Focus on: UX, security, performance, SEO",
            conflicts_with=["api_service", "spa"],
        ),
        Option(
            value="spa",
            label="Single Page Application",
            description="Frontend-only, consumes external API",
            recommended_for=["react", "vue", "angular", "svelte"],
            effects="Focus on: Client-side routing, state management, API integration",
            conflicts_with=["web_app", "api_service"],
        ),
        # Libraries & Tools (5-7)
        Option(
            value="library",
            label="Library/SDK",
            description="Reusable package for developers",
            recommended_for=["setup.py", "package.json", "cargo.toml"],
            effects="Focus on: Public API, versioning, semver, documentation",
            conflicts_with=[],
        ),
        Option(
            value="framework",
            label="Framework/Platform",
            description="Opinionated foundation for building applications",
            recommended_for=["plugin", "extension", "hooks"],
            effects="Focus on: Plugin system, extensibility, DX, conventions",
            conflicts_with=[],
        ),
        Option(
            value="cli_tool",
            label="CLI Tool/Utility",
            description="Command-line application or script",
            recommended_for=["click", "argparse", "commander", "cobra"],
            effects="Focus on: UX, error messages, help text, piping",
            conflicts_with=[],
        ),
        # Data & Processing (8-10)
        Option(
            value="data_pipeline",
            label="Data Pipeline",
            description="ETL, batch processing, data transformation",
            recommended_for=["airflow", "pandas", "spark", "dbt"],
            effects="Focus on: Idempotency, retry logic, data quality, monitoring",
            conflicts_with=[],
        ),
        Option(
            value="ml_pipeline",
            label="ML/AI Pipeline",
            description="Training, inference, MLOps workflows",
            recommended_for=["pytorch", "tensorflow", "mlflow", "kubeflow"],
            effects="Focus on: Reproducibility, experiment tracking, model versioning",
            conflicts_with=[],
        ),
        Option(
            value="stream_processing",
            label="Stream Processing",
            description="Real-time data processing (Kafka, Flink, etc.)",
            recommended_for=["kafka", "flink", "spark-streaming"],
            effects="Focus on: Low latency, exactly-once semantics, backpressure",
            conflicts_with=[],
        ),
        # Desktop & Mobile (11-12)
        Option(
            value="desktop_app",
            label="Desktop Application",
            description="Native or cross-platform desktop app",
            recommended_for=["electron", "qt", "tkinter", "tauri"],
            effects="Focus on: UX, installers, auto-updates, native APIs",
            conflicts_with=[],
        ),
        Option(
            value="mobile_app",
            label="Mobile Application",
            description="iOS, Android, or cross-platform mobile",
            recommended_for=["react-native", "flutter", "swift", "kotlin"],
            effects="Focus on: Performance, offline support, app store guidelines",
            conflicts_with=[],
        ),
        # Infrastructure (13-14)
        Option(
            value="infrastructure",
            label="Infrastructure as Code",
            description="Terraform, Pulumi, CloudFormation modules",
            recommended_for=["terraform", "pulumi", "cdk"],
            effects="Focus on: Idempotency, state management, drift detection",
            conflicts_with=[],
        ),
        Option(
            value="automation",
            label="Automation/Orchestration",
            description="CI/CD, deployment automation, workflow orchestration",
            recommended_for=["github-actions", "gitlab-ci", "jenkins"],
            effects="Focus on: Reliability, rollback strategies, observability",
            conflicts_with=[],
        ),
    ],
    auto_strategy=lambda ctx: _auto_detect_project_purpose(ctx),
    ai_hint_generator=lambda ctx: _rec_engine.recommend_project_purpose(ctx),
)

TIER1_TEAM_DYNAMICS = DecisionPoint(
    id="team_dynamics",
    tier=1,
    category="project_identity",
    question="What's your team situation?",
    why_this_question="👥 Team size affects collaboration practices, review processes, and tooling needs",
    multi_select=False,
    options=[
        Option(
            value="solo",
            label="Solo Developer",
            description="Just me, working alone",
            effects="Simpler workflows, skip team practices, faster decisions",
        ),
        Option(
            value="small_team",
            label="Small Team (2-5)",
            description="Close-knit team, frequent communication",
            effects="Lightweight collaboration, code review, shared ownership",
        ),
        Option(
            value="growing_team",
            label="Growing Team (6-20)",
            description="Multiple sub-teams or areas",
            effects="More structure, ownership areas, formal processes",
        ),
        Option(
            value="large_org",
            label="Large Organization (20+)",
            description="Multiple teams, formal processes",
            effects="Strict governance, compliance, architectural review",
        ),
    ],
    auto_strategy=lambda ctx: _auto_detect_team_size(ctx),
    ai_hint_generator=lambda ctx: _rec_engine.recommend_team_dynamics(ctx),
)

TIER1_PROJECT_MATURITY = DecisionPoint(
    id="project_maturity",
    tier=1,
    category="project_identity",
    question="What's your project's current stage?",
    why_this_question="📈 Project stage determines quality requirements and appropriate trade-offs",
    multi_select=False,
    options=[
        Option(
            value="prototype",
            label="Prototype/Proof of Concept",
            description="Exploring ideas, fast iteration, may be thrown away",
            recommended_for=["experimentation", "learning", "hackathons"],
            effects="Low strictness, only critical principles, minimal testing",
            trade_offs="Speed now, may need refactoring later",
        ),
        Option(
            value="mvp",
            label="MVP/Early Development",
            description="First version, finding product-market fit",
            recommended_for=["startups", "new features", "initial release"],
            effects="Medium strictness, practical principles, basic testing",
            trade_offs="Balance speed and quality",
        ),
        Option(
            value="active_dev",
            label="Active Development",
            description="Established product, regular releases, users depend on it",
            recommended_for=["most production projects"],
            effects="Medium-high strictness, balanced quality, good testing",
            trade_offs="Standard best practices",
        ),
        Option(
            value="production",
            label="Production/Mature",
            description="Mission-critical, high stability requirements, large user base",
            recommended_for=["core infrastructure", "revenue-generating systems"],
            effects="High strictness, comprehensive quality, extensive testing",
            trade_offs="Slower development, fewer surprises",
        ),
        Option(
            value="maintenance",
            label="Maintenance Mode",
            description="Stable, minimal changes, focus on security/bugs",
            recommended_for=["legacy systems", "stable products"],
            effects="Focus on stability, security, regression prevention",
            trade_offs="Limited new features",
        ),
    ],
    auto_strategy=lambda ctx: _auto_detect_maturity(ctx),
    ai_hint_generator=lambda ctx: _rec_engine.recommend_project_maturity(ctx),
)

TIER1_DEVELOPMENT_PHILOSOPHY = DecisionPoint(
    id="development_philosophy",
    tier=1,
    category="development_style",
    question="What's your development approach?",
    why_this_question="⚡ Your approach shapes all tactical decisions: speed vs quality, testing depth, etc.",
    multi_select=False,
    options=[
        Option(
            value="move_fast",
            label="Move Fast & Iterate",
            description="Speed over perfection, learn by shipping, refactor later",
            recommended_for=["startups", "prototypes", "learning", "experimentation"],
            effects="Lower coverage targets, minimal docs, pragmatic principles",
            trade_offs="More tech debt, may need refactoring",
            time_investment="Fastest initial development",
        ),
        Option(
            value="balanced",
            label="Balanced & Pragmatic [RECOMMENDED]",
            description="Quality where it matters, pragmatic shortcuts elsewhere",
            recommended_for=["most projects", "solo devs", "productive teams"],
            effects="Standard practices, practical testing, clear priorities",
            trade_offs="Best ROI - balanced approach",
            time_investment="Moderate, sustainable pace",
        ),
        Option(
            value="quality_first",
            label="Quality-First & Thorough",
            description="Correct the first time, comprehensive testing, proper design",
            recommended_for=["production systems", "team projects", "long-term maintenance"],
            effects="High coverage, comprehensive docs, strict principles",
            trade_offs="Slower initial development, fewer surprises later",
            time_investment="Slower but predictable",
        ),
    ],
    auto_strategy=lambda ctx: _auto_detect_philosophy(ctx),
    ai_hint_generator=lambda ctx: _rec_engine.recommend_development_philosophy(ctx),
)


# ============================================================================
# TIER 2: Strategy Decisions (Built on Tier 1)
# ============================================================================

TIER2_PRINCIPLE_STRATEGY = DecisionPoint(
    id="principle_strategy",
    tier=2,
    category="principles",
    question="How should we select development principles?",
    why_this_question="📋 This determines how many principles to enforce (minimal, balanced, or comprehensive)",
    multi_select=False,
    options=[
        Option(
            value="recommended",
            label="Recommended Preset ⭐",
            description="Smart selection based on your project type",
            effects="~20-25 principles, medium strictness, AI-optimized for your context",
            recommended_for=["most projects", "balanced approach"],
        ),
        Option(
            value="minimal",
            label="Minimal/Pragmatic",
            description="Only critical must-haves, maximum flexibility",
            effects="~10-12 principles, low strictness, fast iteration",
            recommended_for=["prototypes", "learning", "fast iteration"],
        ),
        Option(
            value="comprehensive",
            label="Comprehensive/Strict",
            description="Full quality enforcement, all best practices",
            effects="~40-45 principles, high strictness, maximum quality",
            recommended_for=["team projects", "production systems", "compliance"],
        ),
        Option(
            value="custom",
            label="Custom Selection",
            description="I'll review and choose each principle individually",
            effects="You decide exactly which principles apply",
            recommended_for=["advanced users", "specific requirements"],
        ),
    ],
    auto_strategy=lambda ctx: _auto_select_principle_strategy(ctx),
    ai_hint_generator=lambda ctx: _rec_engine.recommend_principle_strategy(ctx),
)

TIER2_TESTING_APPROACH = DecisionPoint(
    id="testing_approach",
    tier=2,
    category="testing",
    question="What's your testing strategy?",
    why_this_question="🧪 Testing strategy affects principle selection, CI/CD setup, and quality expectations",
    multi_select=False,
    options=[
        Option(
            value="no_tests",
            label="No Tests Yet",
            description="Not testing yet, will add later",
            effects="Skip all testing principles, no coverage requirements",
            recommended_for=["early exploration", "learning"],
        ),
        Option(
            value="critical_paths",
            label="Critical Paths Only",
            description="Test core business logic and data handling",
            effects="~40-60% meaningful coverage, core testing principles only",
            recommended_for=["MVP", "small projects", "pragmatic approach"],
        ),
        Option(
            value="balanced",
            label="Balanced Testing [RECOMMENDED]",
            description="Test most features, pragmatic about simple code",
            effects="~70-85% meaningful coverage, standard testing principles",
            recommended_for=["production projects", "professional development"],
        ),
        Option(
            value="comprehensive",
            label="Comprehensive Testing",
            description="High confidence through extensive testing",
            effects="~85-95% coverage, all testing principles including mutation testing",
            recommended_for=["mission-critical", "team projects", "compliance"],
        ),
    ],
    auto_strategy=lambda ctx: _auto_detect_testing_approach(ctx),
    ai_hint_generator=lambda ctx: _generate_testing_hint(ctx),
)

TIER2_SECURITY_STANCE = DecisionPoint(
    id="security_stance",
    tier=2,
    category="security",
    question="What's your security stance?",
    why_this_question="🔒 Security needs determine validation strictness, audit requirements, and best practices",
    multi_select=False,
    options=[
        Option(
            value="standard",
            label="Standard Security",
            description="Basic security hygiene, common vulnerabilities",
            effects="Input validation, no hardcoded secrets, HTTPS",
            recommended_for=["internal tools", "prototypes", "low-risk projects"],
        ),
        Option(
            value="production",
            label="Production Security [RECOMMENDED]",
            description="Comprehensive security for production systems",
            effects="Authentication, authorization, audit logging, encryption",
            recommended_for=["most production apps", "user-facing systems"],
        ),
        Option(
            value="high",
            label="High Security / Compliance",
            description="Strict security for sensitive data",
            effects="Everything + compliance requirements, security audits",
            recommended_for=["finance", "healthcare", "PII handling", "regulated"],
        ),
    ],
    auto_strategy=lambda ctx: _auto_detect_security_stance(ctx),
    ai_hint_generator=lambda ctx: _rec_engine.recommend_security_stance(ctx),
)

TIER2_DOCUMENTATION_LEVEL = DecisionPoint(
    id="documentation_level",
    tier=2,
    category="documentation",
    question="How much documentation do you want?",
    why_this_question="📝 Documentation choices affect time investment and collaboration effectiveness",
    multi_select=False,
    options=[
        Option(
            value="minimal",
            label="Minimal",
            description="README + critical comments only",
            effects="Basic README, complex algorithm comments",
            time_investment="~5% of dev time",
            recommended_for=["solo dev", "prototypes", "self-explanatory code"],
        ),
        Option(
            value="practical",
            label="Practical [RECOMMENDED]",
            description="Useful docs without ceremony",
            effects="Good README, API docs, architecture overview",
            time_investment="~10-15% of dev time",
            recommended_for=["most projects", "team collaboration"],
        ),
        Option(
            value="comprehensive",
            label="Comprehensive",
            description="Extensive documentation for all aspects",
            effects="Full API docs, architecture diagrams, guides, examples",
            time_investment="~20-30% of dev time",
            recommended_for=["public libraries", "large teams", "complex systems"],
        ),
    ],
    auto_strategy=lambda ctx: _auto_detect_documentation_level(ctx),
    ai_hint_generator=lambda ctx: _rec_engine.recommend_documentation_level(ctx),
)

TIER2_GIT_WORKFLOW = DecisionPoint(
    id="git_workflow",
    tier=2,
    category="collaboration",
    question="Which Git workflow do you prefer?",
    why_this_question="🔀 Git workflow affects team collaboration, code review, and release management",
    multi_select=False,
    options=[
        Option(
            value="main_only",
            label="Main-Only (Simple) [RECOMMENDED for Solo]",
            description="Single branch, direct commits with clear messages",
            effects="Fast, simple, minimal overhead",
            time_investment="No extra time",
            recommended_for=["solo dev", "small teams", "fast iteration"],
        ),
        Option(
            value="github_flow",
            label="GitHub Flow (Balanced) [RECOMMENDED for Small Teams]",
            description="Feature branches + Pull requests from main",
            effects="Branch protection, code review, moderate structure",
            time_investment="~10-15% overhead",
            recommended_for=["small-medium teams", "continuous deployment"],
        ),
        Option(
            value="git_flow",
            label="Git Flow (Professional) [RECOMMENDED for Large Teams]",
            description="develop + main branches, formal release process",
            effects="Feature/release/hotfix branches, maximum structure",
            time_investment="~20-30% overhead",
            recommended_for=["large teams", "scheduled releases", "complex projects"],
        ),
        Option(
            value="custom",
            label="Custom",
            description="I'll define my own workflow",
            effects="Full control, custom branching strategy",
            recommended_for=["experienced teams", "specific requirements"],
        ),
    ],
    skip_if=lambda ctx: ctx.get("team_dynamics") == "solo",  # Auto-select for solo devs
    auto_strategy=lambda ctx: _auto_detect_git_workflow(ctx),
    ai_hint_generator=lambda ctx: _generate_git_workflow_hint(ctx),
)

TIER2_VERSIONING_STRATEGY = DecisionPoint(
    id="versioning_strategy",
    tier=2,
    category="collaboration",
    question="How do you want to manage version bumping?",
    why_this_question="📦 Versioning strategy affects release management and changelog generation (P074)",
    multi_select=False,
    options=[
        Option(
            value="auto_semver",
            label="Automatic SemVer [RECOMMENDED for Solo]",
            description="Auto-bump version based on commit types (feat: → MINOR, fix: → PATCH)",
            effects="Zero overhead, automated versioning, CHANGELOG generation",
            time_investment="0% overhead (fully automated)",
            recommended_for=["solo dev", "small teams", "CI/CD pipelines"],
        ),
        Option(
            value="pr_based_semver",
            label="PR-Based SemVer [RECOMMENDED for Small Teams]",
            description="Version bump suggested in PR, reviewer confirms",
            effects="Team review of version bumps, manual confirmation",
            time_investment="~5% overhead (PR review)",
            recommended_for=["small-medium teams", "peer review culture"],
        ),
        Option(
            value="manual_semver",
            label="Manual SemVer [RECOMMENDED for Large Orgs]",
            description="Release managers manually bump versions",
            effects="Full control, formal release process",
            time_investment="~10% overhead (release management)",
            recommended_for=["large teams", "release managers", "formal processes"],
        ),
        Option(
            value="calver",
            label="Calendar Versioning",
            description="Version based on date (YYYY.MM.DD or YYYY.MM.PATCH)",
            effects="Time-based versions, clear release timeline",
            recommended_for=["scheduled releases", "date-driven projects"],
        ),
        Option(
            value="no_versioning",
            label="No Versioning",
            description="Internal tool, no need for versions",
            effects="No version tracking",
            recommended_for=["internal tools", "prototypes"],
        ),
    ],
    auto_strategy=lambda ctx: _auto_detect_versioning_strategy(ctx),
    ai_hint_generator=lambda ctx: _generate_versioning_hint(ctx),
)

TIER2_CI_PROVIDER = DecisionPoint(
    id="ci_provider",
    tier=2,
    category="infrastructure",
    question="Which CI/CD provider do you use?",
    why_this_question="🔄 CI/CD configuration affects automation, testing, and deployment workflows",
    multi_select=False,
    options=[
        Option(
            value="github_actions",
            label="GitHub Actions [RECOMMENDED]",
            description="Native GitHub CI/CD with marketplace integrations",
            effects="Automated testing, deployment, release workflows",
            time_investment="~2-4 hours initial setup",
            recommended_for=["github", "has_git", "small_team", "large_org"],
        ),
        Option(
            value="gitlab_ci",
            label="GitLab CI",
            description="GitLab's integrated CI/CD pipeline",
            effects="Built-in CI/CD, Docker registry, deployment",
            time_investment="~2-4 hours initial setup",
            recommended_for=["gitlab", "has_git"],
        ),
        Option(
            value="circle_ci",
            label="CircleCI",
            description="Cloud-based CI/CD platform",
            effects="Fast builds, Docker support, parallelism",
            recommended_for=["complex builds", "large_org"],
        ),
        Option(
            value="none",
            label="No CI/CD Yet",
            description="Will add later or run tests manually",
            effects="Manual testing and deployment",
            recommended_for=["prototype", "solo"],
        ),
    ],
    auto_strategy=lambda ctx: _auto_detect_ci_provider(ctx),
    ai_hint_generator=lambda ctx: _generate_ci_provider_hint(ctx),
)

TIER2_SECRETS_MANAGEMENT = DecisionPoint(
    id="secrets_management",
    tier=2,
    category="security",
    question="How do you manage secrets (API keys, passwords)?",
    why_this_question="🔐 Secrets management affects security posture and deployment complexity",
    multi_select=False,
    options=[
        Option(
            value="dotenv",
            label=".env Files [RECOMMENDED for Local]",
            description="Environment variables in .env files (gitignored)",
            effects="Simple local development, manual production setup",
            time_investment="~30 minutes setup",
            recommended_for=["solo", "small_team", "prototype"],
        ),
        Option(
            value="vault",
            label="HashiCorp Vault",
            description="Centralized secrets management with encryption",
            effects="Secure storage, rotation, audit logging",
            time_investment="~1-2 days setup",
            recommended_for=["large_org", "production", "high security"],
        ),
        Option(
            value="cloud_secrets",
            label="Cloud Provider Secrets",
            description="AWS Secrets Manager, Azure Key Vault, GCP Secret Manager",
            effects="Integrated with cloud services, IAM-based access",
            time_investment="~2-4 hours setup",
            recommended_for=["cloud deployment", "production"],
        ),
        Option(
            value="none",
            label="Not Using Secrets Yet",
            description="Will add when needed",
            effects="No secrets management",
            recommended_for=["prototype", "learning"],
        ),
    ],
    auto_strategy=lambda ctx: _auto_detect_secrets_management(ctx),
    ai_hint_generator=lambda ctx: _generate_secrets_management_hint(ctx),
)

TIER2_ERROR_HANDLING = DecisionPoint(
    id="error_handling",
    tier=2,
    category="code_quality",
    question="What's your error handling philosophy?",
    why_this_question="⚠️ Error handling strategy affects reliability, debugging, and user experience",
    multi_select=False,
    options=[
        Option(
            value="fail_fast",
            label="Fail-Fast [RECOMMENDED]",
            description="Errors crash immediately with clear messages (P001)",
            effects="No silent failures, easier debugging, explicit error handling",
            time_investment="No overhead",
            recommended_for=["production", "quality_first", "team projects"],
        ),
        Option(
            value="graceful_degradation",
            label="Graceful Degradation",
            description="Try to continue with fallback behavior",
            effects="Better UX, harder to debug, potential hidden issues",
            time_investment="~20% more code",
            recommended_for=["user-facing apps", "high availability"],
        ),
        Option(
            value="retry_logic",
            label="Retry with Backoff",
            description="Automatically retry failed operations",
            effects="Resilient to transient failures, more complex",
            time_investment="~15% more code",
            recommended_for=["distributed systems", "external APIs"],
        ),
    ],
    auto_strategy=lambda ctx: _auto_detect_error_handling(ctx),
    ai_hint_generator=lambda ctx: _generate_error_handling_hint(ctx),
)


# ============================================================================
# TIER 3: Tactical Decisions (Tool Preferences)
# ============================================================================

TIER3_PRECOMMIT_HOOKS = DecisionPoint(
    id="precommit_hooks",
    tier=3,
    category="code_quality",
    question="Which pre-commit hooks do you want?",
    why_this_question="🔧 Pre-commit hooks catch issues before they're committed",
    multi_select=True,
    options=[
        Option(
            value="format",
            label="Code Formatting",
            description="Auto-format code (black, prettier, rustfmt)",
            effects="Consistent code style across team",
            time_investment="~1 second per commit",
            recommended_for=["all"],
        ),
        Option(
            value="lint",
            label="Linting",
            description="Check code quality (ruff, eslint, clippy)",
            effects="Catch bugs and style issues early",
            time_investment="~2-5 seconds per commit",
            recommended_for=["small_team", "large_org"],
        ),
        Option(
            value="type_check",
            label="Type Checking",
            description="Static type validation (mypy, tsc)",
            effects="Prevent type errors",
            time_investment="~5-10 seconds per commit",
            recommended_for=["large_org", "quality_first"],
        ),
        Option(
            value="secrets",
            label="Secrets Detection",
            description="Scan for API keys and passwords",
            effects="Prevent secret leaks",
            time_investment="~1 second per commit",
            recommended_for=["all"],
        ),
        Option(
            value="test",
            label="Run Tests",
            description="Run unit tests before commit",
            effects="Ensure tests pass locally",
            time_investment="~10-60 seconds per commit",
            recommended_for=["no_ci", "quality_first"],
        ),
    ],
    auto_strategy=lambda ctx: _auto_detect_precommit_hooks(ctx),
    ai_hint_generator=lambda ctx: _generate_precommit_hooks_hint(ctx),
)

TIER3_LOGGING_LEVEL = DecisionPoint(
    id="logging_level",
    tier=3,
    category="code_quality",
    question="What's your default logging level?",
    why_this_question="📋 Logging level affects debugging capability and log volume",
    multi_select=False,
    options=[
        Option(
            value="DEBUG",
            label="DEBUG",
            description="Detailed diagnostic information",
            effects="High log volume, useful for development",
            recommended_for=["prototype", "debugging"],
        ),
        Option(
            value="INFO",
            label="INFO [RECOMMENDED]",
            description="General informational messages",
            effects="Balanced log volume, good for production",
            recommended_for=["production", "mvp"],
        ),
        Option(
            value="WARNING",
            label="WARNING",
            description="Warning messages only",
            effects="Low log volume, focus on issues",
            recommended_for=["production", "high_traffic"],
        ),
        Option(
            value="ERROR",
            label="ERROR",
            description="Error messages only",
            effects="Minimal logs, only failures",
            recommended_for=["production", "minimal"],
        ),
    ],
    auto_strategy=lambda ctx: _auto_detect_logging_level(ctx),
    ai_hint_generator=lambda ctx: _generate_logging_level_hint(ctx),
)

# These are generated dynamically based on detected tools
# See: _build_tier3_tool_decisions() function


# ============================================================================
# Auto-Detection Strategies (for Quick Mode)
# ============================================================================


def _auto_detect_project_purpose(ctx: AnswerContext) -> list:
    """Auto-detect with better disambiguation"""
    sys = ctx.system

    # Use UniversalDetector results if available
    if sys.detected_project_types:
        return sys.detected_project_types

    # Infer from frameworks
    frameworks = [fw.lower() for fw in sys.detected_frameworks]

    # Check for explicit conflicts and disambiguate
    has_frontend = any(fw in frameworks for fw in ["react", "vue", "angular", "svelte", "next", "nuxt"])
    has_backend = any(fw in frameworks for fw in ["fastapi", "flask", "django", "express", "spring", "gin"])

    if has_frontend and has_backend:
        return ["web_app"]  # Full-stack
    elif has_backend and not has_frontend:
        return ["api_service"]  # Pure backend
    elif has_frontend and not has_backend:
        return ["spa"]  # Pure frontend

    # Check for other types
    detected = []

    if "docker" in frameworks or "kubernetes" in frameworks:
        detected.append("microservice")
    if "terraform" in frameworks or "pulumi" in frameworks:
        detected.append("infrastructure")
    if "airflow" in frameworks or "spark" in frameworks or "dbt" in frameworks:
        detected.append("data_pipeline")
    if "pytorch" in frameworks or "tensorflow" in frameworks:
        detected.append("ml_pipeline")
    if "kafka" in frameworks or "flink" in frameworks:
        detected.append("stream_processing")
    if "electron" in frameworks or "qt" in frameworks:
        detected.append("desktop_app")
    if "react-native" in frameworks or "flutter" in frameworks:
        detected.append("mobile_app")
    if "click" in frameworks or "argparse" in frameworks or "commander" in frameworks:
        detected.append("cli_tool")

    # Check for library indicators
    if sys.project_root and (
        (sys.project_root / "setup.py").exists() or (sys.project_root / "pyproject.toml").exists()
    ):
        # Check if it's a library (no server dependencies)
        if not any(fw in frameworks for fw in ["fastapi", "flask", "django"]):
            detected.append("library")

    # Default fallback
    return detected if detected else ["api_service"]


def _auto_detect_team_size(ctx: AnswerContext) -> str:
    """Auto-detect team size from git history"""
    sys = ctx.system

    # TODO: Actually check git log for contributors
    # git log --all --format='%an' --since='6 months ago' | sort -u | wc -l

    # For now, use heuristics
    if sys.has_ci and sys.has_tests:
        return "small_team"  # CI suggests team

    return "solo"


def _auto_detect_maturity(ctx: AnswerContext) -> str:
    """Auto-detect project maturity"""
    sys = ctx.system

    # Prototype indicators
    if not sys.has_tests and sys.file_count < 50:
        return "prototype"

    # MVP indicators
    if sys.has_tests and not sys.has_ci:
        return "mvp"

    # Production indicators
    if sys.has_tests and sys.has_ci and sys.file_count > 200:
        return "production"

    # Active development (default for tested projects)
    if sys.has_tests and sys.has_ci:
        return "active_dev"

    # Default
    return "mvp"


def _auto_detect_philosophy(ctx: AnswerContext) -> str:
    """Auto-detect development philosophy"""
    maturity = ctx.maturity

    if maturity == "prototype":
        return "move_fast"
    elif maturity in ["production", "mature"]:
        return "quality_first"
    else:
        return "balanced"


def _auto_select_principle_strategy(ctx: AnswerContext) -> str:
    """Auto-select principle strategy"""
    philosophy = ctx.philosophy
    maturity = ctx.maturity
    team = ctx.team_size

    # Fast iteration → minimal
    if philosophy == "move_fast" or maturity == "prototype":
        return "minimal"

    # Quality-first → comprehensive
    if philosophy == "quality_first" or team in ["growing_team", "large_org"]:
        return "comprehensive"

    # Default → recommended
    return "recommended"


def _auto_detect_testing_approach(ctx: AnswerContext) -> str:
    """Auto-detect testing approach"""
    sys = ctx.system
    maturity = ctx.maturity
    philosophy = ctx.philosophy

    # No tests
    if not sys.has_tests:
        return "no_tests"

    # Quality-first wants comprehensive
    if philosophy == "quality_first":
        return "comprehensive"

    # Production needs good testing
    if maturity in ["production", "mature"]:
        return "balanced"

    # Default
    return "critical_paths"


def _auto_detect_security_stance(ctx: AnswerContext) -> str:
    """Auto-detect security stance"""
    project_types = ctx.project_types
    maturity = ctx.maturity

    # APIs need production security
    if any(t in project_types for t in ["api_service", "microservice", "web_app", "spa"]):
        return "production"

    # Data handling needs production security
    if any(t in project_types for t in ["data_pipeline", "ml_pipeline", "stream_processing"]):
        return "production"

    # Prototypes can be standard
    if maturity == "prototype":
        return "standard"

    # Default production
    return "production"


def _auto_detect_documentation_level(ctx: AnswerContext) -> str:
    """Auto-detect documentation level"""
    project_types = ctx.project_types
    team = ctx.team_size

    # Libraries, frameworks, and infrastructure need comprehensive docs
    if any(t in project_types for t in ["library", "framework", "infrastructure"]):
        return "comprehensive"

    # APIs and services benefit from good documentation
    if any(t in project_types for t in ["api_service", "microservice"]):
        return "practical"

    # Solo can be minimal
    if team == "solo":
        return "minimal"

    # Teams need practical
    return "practical"


def _auto_detect_git_workflow(ctx: AnswerContext) -> str:
    """Auto-detect Git workflow based on team size and maturity"""
    team = ctx.team_size
    maturity = ctx.maturity

    # Solo developers always use main-only
    if team == "solo":
        return "main_only"

    # Large teams benefit from Git Flow
    if team in ["large_org"]:
        return "git_flow"

    # Growing/medium teams use GitHub Flow
    if team in ["small_team", "growing_team"]:
        if maturity in ["production", "mature"]:
            return "git_flow"  # More structure for production
        return "github_flow"

    # Default to GitHub Flow for teams
    return "github_flow"


def _auto_detect_versioning_strategy(ctx: AnswerContext) -> str:
    """Auto-detect versioning strategy based on team size and project type"""
    team = ctx.team_size
    project_types = ctx.get("project_purpose", [])
    maturity = ctx.maturity

    # No versioning for prototypes or internal tools
    if maturity == "prototype":
        return "no_versioning"

    # Libraries, APIs, frameworks, and infrastructure should always have versioning
    needs_versioning = any(
        pt in project_types
        for pt in ["library", "framework", "api_service", "microservice", "infrastructure"]
    )

    # Solo developers benefit from automation
    if team == "solo":
        return "auto_semver" if needs_versioning else "no_versioning"

    # Large organizations prefer manual control
    if team in ["large_org"]:
        return "manual_semver"

    # Small to medium teams use PR-based review
    if team in ["small_team", "growing_team"]:
        if maturity in ["production", "mature"]:
            return "pr_based_semver"
        return "auto_semver"  # Auto for active development

    # Default to auto for modern workflows
    return "auto_semver"


# ============================================================================
# AI Hint Generators (using ContextMatrix)
# ============================================================================


def _generate_testing_hint(ctx: AnswerContext) -> str:
    """Generate testing approach hint using ContextMatrix"""
    if not ctx.has_answer("team_dynamics") or not ctx.has_answer("project_maturity"):
        return ""

    recommendation = _context_matrix.recommend_testing_approach(
        ctx.team_size, ctx.maturity, ctx.get("development_philosophy", "balanced")
    )

    return f"💡 Recommended: {recommendation['approach']} (target: {recommendation['coverage_target']}) - {recommendation['reason']}"


def _generate_git_workflow_hint(ctx: AnswerContext) -> str:
    """Generate git workflow hint using ContextMatrix"""
    if not ctx.has_answer("team_dynamics") or not ctx.has_answer("project_maturity"):
        return ""

    recommendation = _context_matrix.recommend_git_workflow(
        ctx.team_size, ctx.maturity, ctx.system.has_ci
    )

    hint = f"💡 Recommended: {recommendation['workflow']} - {recommendation['reason']}"

    if recommendation.get("alternatives"):
        alternatives = ", ".join(recommendation["alternatives"].keys())
        hint += f" (alternatives: {alternatives})"

    return hint


def _generate_versioning_hint(ctx: AnswerContext) -> str:
    """Generate versioning strategy hint using ContextMatrix"""
    if not ctx.has_answer("team_dynamics") or not ctx.has_answer("project_maturity"):
        return ""

    recommendation = _context_matrix.recommend_versioning_strategy(
        ctx.team_size, ctx.maturity, ctx.system.has_ci
    )

    hint = f"💡 Recommended: {recommendation['strategy']} - {recommendation['reason']}"

    if recommendation.get("alternatives"):
        alternatives = ", ".join(recommendation["alternatives"].keys())
        hint += f" (alternatives: {alternatives})"

    return hint


def _generate_ci_provider_hint(ctx: AnswerContext) -> str:
    """Generate CI provider hint"""
    if ctx.system.has_ci:
        return "💡 CI/CD already detected in your project"

    if ctx.system.is_git_repo:
        # Check if GitHub or GitLab based on remote
        return "💡 Recommended: GitHub Actions (native GitHub integration)"

    return "💡 Add CI/CD later when you're ready for automation"


def _generate_secrets_management_hint(ctx: AnswerContext) -> str:
    """Generate secrets management hint"""
    if not ctx.has_answer("team_dynamics") or not ctx.has_answer("project_maturity"):
        return ""

    team = ctx.team_size
    maturity = ctx.maturity

    if team == "solo" or maturity == "prototype":
        return "💡 Recommended: .env files - simple and effective for local development"
    elif team == "small_team" and maturity in ["mvp", "production"]:
        return "💡 Recommended: .env files with cloud secrets for production deployments"
    elif team == "large_org" or maturity == "legacy":
        return "💡 Recommended: HashiCorp Vault or cloud provider secrets for enterprise security"

    return "💡 Recommended: .env files - upgrade to cloud secrets when needed"


def _generate_error_handling_hint(ctx: AnswerContext) -> str:
    """Generate error handling hint"""
    if not ctx.has_answer("development_philosophy"):
        return ""

    philosophy = ctx.philosophy

    if philosophy == "quality_first":
        return "💡 Recommended: Fail-Fast (P001) - catch errors early, debug faster"
    elif philosophy == "balanced":
        return "💡 Recommended: Fail-Fast with targeted graceful degradation"
    else:  # move_fast
        return "💡 Recommended: Fail-Fast - simple and effective, add complexity only when needed"


# ============================================================================
# Auto-Detection Functions for New Decision Points
# ============================================================================


def _auto_detect_ci_provider(ctx: AnswerContext) -> str:
    """Auto-detect CI provider"""
    if ctx.system.has_ci:
        # Try to detect which provider
        if (ctx.system.project_root / ".github" / "workflows").exists():
            return "github_actions"
        elif (ctx.system.project_root / ".gitlab-ci.yml").exists():
            return "gitlab_ci"
        elif (ctx.system.project_root / ".circleci").exists():
            return "circle_ci"

    # No CI detected - recommend based on git provider
    if ctx.system.is_git_repo:
        return "github_actions"  # Default to GitHub Actions

    return "none"


def _auto_detect_secrets_management(ctx: AnswerContext) -> str:
    """Auto-detect secrets management approach"""
    # Check for .env file
    if (ctx.system.project_root / ".env").exists() or (
        ctx.system.project_root / ".env.example"
    ).exists():
        return "dotenv"

    # Check for cloud provider secrets
    project_types = ctx.get("project_purpose", [])
    if any(
        pt in project_types for pt in ["microservice", "api_service", "infrastructure"]
    ):
        return "cloud_secrets"

    # Default based on team size
    if ctx.has_answer("team_dynamics"):
        if ctx.team_size == "large_org":
            return "vault"
        elif ctx.team_size == "small_team":
            return "dotenv"

    return "none"


def _auto_detect_error_handling(ctx: AnswerContext) -> str:
    """Auto-detect error handling philosophy"""
    # Check development philosophy
    if ctx.has_answer("development_philosophy"):
        if ctx.philosophy == "quality_first":
            return "fail_fast"
        elif ctx.philosophy == "balanced":
            return "fail_fast"  # Still prefer fail-fast
        else:  # move_fast
            return "fail_fast"  # Simplest approach

    # Check project type
    project_types = ctx.get("project_purpose", [])
    if "microservice" in project_types or "distributed_system" in project_types:
        return "retry_logic"

    if "web_app" in project_types or "mobile_app" in project_types:
        return "graceful_degradation"

    return "fail_fast"


def _auto_detect_precommit_hooks(ctx: AnswerContext) -> list:
    """Auto-detect recommended pre-commit hooks"""
    hooks = _context_matrix.recommend_precommit_hooks(
        ctx.team_size if ctx.has_answer("team_dynamics") else "solo",
        ctx.system.has_ci,
    )
    return hooks


def _auto_detect_logging_level(ctx: AnswerContext) -> str:
    """Auto-detect logging level"""
    if not ctx.has_answer("project_maturity"):
        return "INFO"

    maturity = ctx.maturity

    if maturity == "prototype":
        return "DEBUG"
    elif maturity in ["mvp", "production"]:
        return "INFO"
    elif maturity == "legacy":
        return "WARNING"

    return "INFO"


def _generate_precommit_hooks_hint(ctx: AnswerContext) -> str:
    """Generate pre-commit hooks hint"""
    if not ctx.has_answer("team_dynamics"):
        return ""

    recommended = _context_matrix.recommend_precommit_hooks(
        ctx.team_size, ctx.system.has_ci
    )

    hooks_str = ", ".join(recommended)
    return f"💡 Recommended: {hooks_str}"


def _generate_logging_level_hint(ctx: AnswerContext) -> str:
    """Generate logging level hint"""
    if not ctx.has_answer("project_maturity"):
        return ""

    maturity = ctx.maturity

    if maturity == "prototype":
        return "💡 Recommended: DEBUG - useful for development and troubleshooting"
    elif maturity in ["mvp", "production"]:
        return "💡 Recommended: INFO - balanced for production monitoring"
    elif maturity == "legacy":
        return "💡 Recommended: WARNING - reduce log volume in mature systems"

    return "💡 Recommended: INFO - good default for most applications"


# ============================================================================
# Dynamic TIER 3 Builder (Tool Preferences)
# ============================================================================


def build_tier3_tool_decisions(ctx: AnswerContext) -> list:
    """
    Build TIER 3 decisions: static decisions + dynamic tool conflicts.

    Static decisions (always asked):
    - Pre-commit hooks
    - Logging level

    Dynamic decisions (only if tool conflicts detected):
    - Tool preferences (e.g., ruff vs black)
    """
    # Start with static TIER3 decisions
    decisions = [
        TIER3_PRECOMMIT_HOOKS,
        TIER3_LOGGING_LEVEL,
    ]

    # Add dynamic tool conflict decisions
    sys = ctx.system
    comparator = ToolComparator(sys.existing_tools)
    conflicts = comparator.find_all_conflicts()

    for conflict in conflicts:
        # Build options for this tool category
        options = []
        for tool in conflict.tools:
            is_recommended = tool == conflict.recommended
            label = f"{tool} {'⭐ [RECOMMENDED]' if is_recommended else ''}"
            description = comparator.get_tool_description(tool)

            options.append(
                Option(
                    value=tool,
                    label=label,
                    description=description,
                    recommended_for=[conflict.category],
                ),
            )

        # Create decision point
        decision = DecisionPoint(
            id=f"tool_preference_{conflict.category}",
            tier=3,
            category="tool_preferences",
            question=f"Which {conflict.category} do you want to use?",
            why_this_question=f"🔧 Multiple {conflict.category}s detected - choose your preferred tool",
            multi_select=False,
            options=options,
            auto_strategy=lambda ctx, conf=conflict: conf.recommended,
            ai_hint_generator=lambda ctx,
            cat=conflict.category,
            tools=conflict.tools: _rec_engine.recommend_tool_preference(cat, tools, ctx),
        )

        decisions.append(decision)

    return decisions


# ============================================================================
# Complete Decision Tree
# ============================================================================

DECISION_TREE_TIER1 = [
    TIER1_PROJECT_PURPOSE,
    TIER1_TEAM_DYNAMICS,
    TIER1_PROJECT_MATURITY,
    TIER1_DEVELOPMENT_PHILOSOPHY,
]

DECISION_TREE_TIER2 = [
    TIER2_PRINCIPLE_STRATEGY,
    TIER2_TESTING_APPROACH,
    TIER2_SECURITY_STANCE,
    TIER2_DOCUMENTATION_LEVEL,
    TIER2_GIT_WORKFLOW,
    TIER2_VERSIONING_STRATEGY,
    TIER2_CI_PROVIDER,
    TIER2_SECRETS_MANAGEMENT,
    TIER2_ERROR_HANDLING,
]

# TIER3 is dynamically generated
# TIER3 = build_tier3_tool_decisions(context)


def get_all_decisions(ctx: AnswerContext) -> list:
    """
    Get all decision points in order, including dynamically generated TIER 3.

    Args:
        ctx: Current answer context

    Returns:
        List of all DecisionPoint objects in execution order
    """
    tier1 = DECISION_TREE_TIER1
    tier2 = DECISION_TREE_TIER2
    tier3 = build_tier3_tool_decisions(ctx)

    return tier1 + tier2 + tier3


def get_decisions_by_tier(tier: int, ctx: AnswerContext = None) -> list:
    """Get decisions for a specific tier"""
    if tier == 1:
        return DECISION_TREE_TIER1
    elif tier == 2:
        return DECISION_TREE_TIER2
    elif tier == 3:
        if ctx is None:
            raise ValueError("Context required for TIER 3 decisions")
        return build_tier3_tool_decisions(ctx)
    else:
        return []
