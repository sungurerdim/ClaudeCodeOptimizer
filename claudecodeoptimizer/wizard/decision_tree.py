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

from .models import AnswerContext, DecisionPoint, Option
from .recommendations import RecommendationEngine
from .tool_comparison import ToolComparator

# Initialize recommendation engine
_rec_engine = RecommendationEngine()


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
    options=[
        Option(
            value="api_backend",
            label="API/Backend Service",
            description="REST/GraphQL API, microservice, backend server",
            recommended_for=["fastapi", "flask", "django", "express", "spring"],
            effects="Focus on: API design, performance, security, data validation",
        ),
        Option(
            value="web_app",
            label="Web Application (Full-Stack)",
            description="Complete web app with frontend + backend",
            recommended_for=["next", "nuxt", "django", "rails"],
            effects="Focus on: UX, security, performance, SEO",
        ),
        Option(
            value="library",
            label="Library/SDK/Package",
            description="Reusable code package for other developers",
            recommended_for=["setup.py", "package.json"],
            effects="Focus on: Public API clarity, versioning, documentation, backward compatibility",
        ),
        Option(
            value="cli_tool",
            label="CLI Tool/Utility",
            description="Command-line application or script",
            recommended_for=["click", "argparse", "commander"],
            effects="Focus on: User experience, error messages, help text",
        ),
        Option(
            value="data_pipeline",
            label="Data Pipeline/Processing",
            description="ETL, data analysis, batch processing",
            recommended_for=["airflow", "pandas", "spark"],
            effects="Focus on: Idempotency, error recovery, monitoring, data quality",
        ),
        Option(
            value="desktop_app",
            label="Desktop Application",
            description="Native or cross-platform desktop app",
            recommended_for=["electron", "qt", "tkinter"],
            effects="Focus on: UX, installers, auto-updates",
        ),
        Option(
            value="mobile_app",
            label="Mobile Application",
            description="iOS, Android, or cross-platform mobile",
            recommended_for=["react-native", "flutter", "swift", "kotlin"],
            effects="Focus on: Performance, offline support, app store guidelines",
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
    ai_hint_generator=lambda ctx: _rec_engine.recommend_testing_approach(ctx),
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
    ai_hint_generator=lambda ctx: _rec_engine.recommend_git_workflow(ctx)
    if hasattr(_rec_engine, "recommend_git_workflow")
    else "",
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
    ai_hint_generator=lambda ctx: _rec_engine.recommend_versioning_strategy(ctx)
    if hasattr(_rec_engine, "recommend_versioning_strategy")
    else "",
)


# ============================================================================
# TIER 3: Tactical Decisions (Tool Preferences)
# ============================================================================

# These are generated dynamically based on detected tools
# See: _build_tier3_tool_decisions() function


# ============================================================================
# Auto-Detection Strategies (for Quick Mode)
# ============================================================================


def _auto_detect_project_purpose(ctx: AnswerContext) -> list:
    """Auto-detect project types from system context"""
    sys = ctx.system
    detected = []

    # Use UniversalDetector results if available
    if sys.detected_project_types:
        return sys.detected_project_types

    # Infer from frameworks
    frameworks = [fw.lower() for fw in sys.detected_frameworks]

    if any(fw in frameworks for fw in ["fastapi", "flask", "django-rest", "express"]):
        detected.append("api_backend")

    if any(fw in frameworks for fw in ["react", "vue", "next", "nuxt", "svelte"]):
        detected.append("web_app")

    if any(fw in frameworks for fw in ["click", "argparse", "commander"]):
        detected.append("cli_tool")

    if any(fw in frameworks for fw in ["airflow", "pandas", "spark"]):
        detected.append("data_pipeline")

    if any(fw in frameworks for fw in ["electron", "qt", "tkinter"]):
        detected.append("desktop_app")

    if any(fw in frameworks for fw in ["react-native", "flutter"]):
        detected.append("mobile_app")

    # Check for library indicators
    if sys.project_root and (
        (sys.project_root / "setup.py").exists() or (sys.project_root / "pyproject.toml").exists()
    ):
        # Check if it's a library (no server dependencies)
        if not any(fw in frameworks for fw in ["fastapi", "flask", "django"]):
            detected.append("library")

    # Default fallback
    return detected if detected else ["api_backend"]


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
    if any(t in project_types for t in ["api_backend", "web_app"]):
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

    # Libraries need comprehensive
    if "library" in project_types:
        return "comprehensive"

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

    # Libraries and APIs should always have versioning
    needs_versioning = any(pt in project_types for pt in ["library", "api_backend"])

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
# Dynamic TIER 3 Builder (Tool Preferences)
# ============================================================================


def build_tier3_tool_decisions(ctx: AnswerContext) -> list:
    """
    Dynamically build TIER 3 decisions based on detected tools.

    Only ask about tools where conflicts exist (e.g., both ruff and black detected).
    """
    sys = ctx.system
    comparator = ToolComparator(sys.existing_tools)
    conflicts = comparator.find_all_conflicts()

    decisions = []

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
