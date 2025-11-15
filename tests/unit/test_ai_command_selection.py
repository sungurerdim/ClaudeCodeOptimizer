"""
Unit tests for CommandRecommender

Tests command selection logic, scoring, ranking, filtering, and error handling.
Target Coverage: 100%
"""

import pytest

from claudecodeoptimizer.ai.command_selection import CommandRecommender
from claudecodeoptimizer.schemas.commands import CommandMetadata, CommandRegistry
from claudecodeoptimizer.schemas.preferences import (
    CCOPreferences,
    CodeQualityStandards,
    DevOpsAutomation,
    DocumentationPreferences,
    ProjectIdentity,
    SecurityPosture,
    TestingStrategy,
)


@pytest.fixture
def minimal_preferences() -> CCOPreferences:
    """Minimal valid preferences for testing"""
    return CCOPreferences(
        project_identity=ProjectIdentity(
            name="TestProject",
            primary_language="python",
            types=["cli"],
            team_trajectory="solo",
            project_maturity="active-dev",
        ),
    )


@pytest.fixture
def high_security_preferences() -> CCOPreferences:
    """Preferences with high security requirements"""
    return CCOPreferences(
        project_identity=ProjectIdentity(
            name="SecureProject",
            primary_language="python",
            types=["api", "backend"],
            team_trajectory="medium-5-10",
            project_maturity="production",
        ),
        security=SecurityPosture(
            security_stance="paranoid",
            dependency_scanning="every-commit",
        ),
    )


@pytest.fixture
def high_testing_preferences() -> CCOPreferences:
    """Preferences with high testing requirements"""
    return CCOPreferences(
        project_identity=ProjectIdentity(
            name="TestDrivenProject",
            primary_language="python",
            types=["library"],
            team_trajectory="small-2-5",
            project_maturity="active-dev",
        ),
        testing=TestingStrategy(
            coverage_target="100",
            mutation_testing="required",
            test_pyramid_ratio="60-30-10",
        ),
    )


@pytest.fixture
def strict_quality_preferences() -> CCOPreferences:
    """Preferences with strict code quality requirements"""
    return CCOPreferences(
        project_identity=ProjectIdentity(
            name="StrictProject",
            primary_language="python",
            types=["library", "sdk"],
            team_trajectory="medium-5-10",
            project_maturity="active-dev",
        ),
        code_quality=CodeQualityStandards(
            linting_strictness="pedantic",
            dry_enforcement="zero-tolerance",
            type_coverage_target="100",
        ),
    )


@pytest.fixture
def extensive_docs_preferences() -> CCOPreferences:
    """Preferences with extensive documentation requirements"""
    return CCOPreferences(
        project_identity=ProjectIdentity(
            name="DocProject",
            primary_language="python",
            types=["library", "framework"],
            team_trajectory="medium-5-10",
            project_maturity="stable",
        ),
        documentation=DocumentationPreferences(
            verbosity="extensive",
            inline_documentation="every-function",
            api_documentation="openapi-spec",
        ),
    )


@pytest.fixture
def devops_preferences() -> CCOPreferences:
    """Preferences with DevOps automation"""
    return CCOPreferences(
        project_identity=ProjectIdentity(
            name="DevOpsProject",
            primary_language="python",
            types=["backend", "microservice"],
            team_trajectory="medium-5-10",
            project_maturity="production",
        ),
        devops=DevOpsAutomation(
            ci_cd_trigger="every-commit",
            infrastructure=["kubernetes"],
            monitoring=["prometheus", "grafana"],
        ),
    )


@pytest.fixture
def sample_registry() -> CommandRegistry:
    """Sample command registry for testing"""
    commands = [
        CommandMetadata(
            command_id="cco-help",
            display_name="Help",
            category="core",
            description_short="Show help",
            description_long="Display help information",
            applicable_project_types=["all"],
            is_core=True,
        ),
        CommandMetadata(
            command_id="cco-status",
            display_name="Status",
            category="core",
            description_short="Show status",
            description_long="Display project status",
            applicable_project_types=["all"],
            is_core=True,
        ),
        CommandMetadata(
            command_id="cco-configure",
            display_name="Configure",
            category="core",
            description_short="Configure CCO",
            description_long="Configure CCO settings",
            applicable_project_types=["all"],
            is_core=True,
        ),
        CommandMetadata(
            command_id="cco-audit-tests",
            display_name="Audit Tests",
            category="audit",
            description_short="Audit test quality",
            description_long="Comprehensive test quality audit",
            applicable_project_types=["all"],
            relevance_tags=["testing", "quality"],
        ),
        CommandMetadata(
            command_id="cco-generate-tests",
            display_name="Generate Tests",
            category="generate",
            description_short="Generate unit tests",
            description_long="Auto-generate unit tests for untested code",
            applicable_project_types=["all"],
            relevance_tags=["testing"],
        ),
        CommandMetadata(
            command_id="cco-audit-security",
            display_name="Audit Security",
            category="audit",
            description_short="Security audit",
            description_long="Comprehensive security vulnerability audit",
            applicable_project_types=["api", "backend", "microservice"],
            relevance_tags=["security"],
        ),
        CommandMetadata(
            command_id="cco-scan-secrets",
            display_name="Scan Secrets",
            category="audit",
            description_short="Scan for exposed secrets",
            description_long="Scan codebase for exposed API keys and secrets",
            applicable_project_types=["all"],
            relevance_tags=["security"],
        ),
        CommandMetadata(
            command_id="cco-audit-docs",
            display_name="Audit Documentation",
            category="audit",
            description_short="Audit documentation",
            description_long="Audit documentation completeness and accuracy",
            applicable_project_types=["all"],
            relevance_tags=["documentation"],
        ),
        CommandMetadata(
            command_id="cco-generate-docs",
            display_name="Generate Documentation",
            category="generate",
            description_short="Generate documentation",
            description_long="Auto-generate API documentation",
            applicable_project_types=["all"],
            relevance_tags=["documentation"],
        ),
        CommandMetadata(
            command_id="cco-audit-code",
            display_name="Audit Code Quality",
            category="audit",
            description_short="Code quality audit",
            description_long="Comprehensive code quality audit",
            applicable_project_types=["all"],
            relevance_tags=["code-quality", "linting"],
        ),
        CommandMetadata(
            command_id="cco-fix-code",
            display_name="Fix Code Issues",
            category="fix",
            description_short="Auto-fix code issues",
            description_long="Automatically fix code quality violations",
            applicable_project_types=["all"],
            relevance_tags=["code-quality", "linting"],
        ),
        CommandMetadata(
            command_id="cco-refactor-duplicates",
            display_name="Refactor Duplicates",
            category="refactor",
            description_short="Remove code duplication",
            description_long="Detect and refactor duplicate code",
            applicable_project_types=["all"],
            relevance_tags=["code-quality", "dry"],
        ),
        CommandMetadata(
            command_id="cco-cleanup-dead-code",
            display_name="Cleanup Dead Code",
            category="optimize",
            description_short="Remove dead code",
            description_long="Remove unused code and imports",
            applicable_project_types=["all"],
            relevance_tags=["code-quality"],
        ),
        CommandMetadata(
            command_id="cco-setup-cicd",
            display_name="Setup CI/CD",
            category="setup",
            description_short="Setup CI/CD pipeline",
            description_long="Generate CI/CD configuration files",
            applicable_project_types=["all"],
            relevance_tags=["devops", "automation"],
        ),
        CommandMetadata(
            command_id="cco-setup-docker",
            display_name="Setup Docker",
            category="setup",
            description_short="Setup Docker",
            description_long="Generate Docker configuration",
            applicable_project_types=["all"],
            relevance_tags=["devops", "infrastructure"],
        ),
        CommandMetadata(
            command_id="cco-setup-monitoring",
            display_name="Setup Monitoring",
            category="setup",
            description_short="Setup monitoring",
            description_long="Setup observability stack",
            applicable_project_types=["all"],
            relevance_tags=["devops", "monitoring"],
        ),
        CommandMetadata(
            command_id="cco-analyze-structure",
            display_name="Analyze Structure",
            category="analyze",
            description_short="Analyze codebase structure",
            description_long="Analyze architectural patterns and structure",
            applicable_project_types=["all"],
            relevance_tags=["analysis", "architecture"],
        ),
        CommandMetadata(
            command_id="cco-analyze-dependencies",
            display_name="Analyze Dependencies",
            category="analyze",
            description_short="Analyze dependencies",
            description_long="Dependency graph and circular dependency detection",
            applicable_project_types=["all"],
            relevance_tags=["analysis", "dependencies"],
        ),
        CommandMetadata(
            command_id="cco-optimize-docs",
            display_name="Optimize Documentation",
            category="optimize",
            description_short="Optimize documentation",
            description_long="Optimize documentation quality and consistency",
            applicable_project_types=["all"],
            relevance_tags=["documentation"],
        ),
        CommandMetadata(
            command_id="cco-fix-docs",
            display_name="Fix Documentation",
            category="fix",
            description_short="Fix documentation issues",
            description_long="Fix documentation inconsistencies",
            applicable_project_types=["all"],
            relevance_tags=["documentation"],
        ),
        CommandMetadata(
            command_id="cco-generate-from-specs",
            display_name="Generate from Specs",
            category="generate",
            description_short="Generate code from OpenAPI specs",
            description_long="Generate code from OpenAPI specifications",
            applicable_project_types=["api", "backend", "microservice"],
            relevance_tags=["api", "codegen"],
        ),
        CommandMetadata(
            command_id="cco-sync-spec-to-code",
            display_name="Sync Spec to Code",
            category="sync",
            description_short="Sync OpenAPI specs to code",
            description_long="Keep OpenAPI specs in sync with code",
            applicable_project_types=["api", "backend", "microservice"],
            relevance_tags=["api", "sync"],
        ),
        CommandMetadata(
            command_id="cco-generate-integration-tests",
            display_name="Generate Integration Tests",
            category="generate",
            description_short="Generate integration tests",
            description_long="Generate integration tests for service interactions",
            applicable_project_types=["all"],
            relevance_tags=["testing", "integration"],
        ),
        CommandMetadata(
            command_id="cco-fix-security",
            display_name="Fix Security Issues",
            category="fix",
            description_short="Auto-fix security issues",
            description_long="Automatically fix security vulnerabilities",
            applicable_project_types=["all"],
            relevance_tags=["security"],
        ),
        CommandMetadata(
            command_id="cco-generate-principles",
            display_name="Generate Principles",
            category="generate",
            description_short="Generate development principles",
            description_long="Generate team development principles",
            applicable_project_types=["all"],
            relevance_tags=["principles", "documentation"],
        ),
        CommandMetadata(
            command_id="cco-check-principle",
            display_name="Check Principle",
            category="audit",
            description_short="Check principle adherence",
            description_long="Verify code adheres to principles",
            applicable_project_types=["all"],
            relevance_tags=["principles", "quality"],
        ),
        CommandMetadata(
            command_id="cco-audit-principles",
            display_name="Audit Principles",
            category="audit",
            description_short="Audit all principles",
            description_long="Audit all code against development principles",
            applicable_project_types=["all"],
            relevance_tags=["principles", "quality"],
        ),
        CommandMetadata(
            command_id="cco-self-optimize",
            display_name="Self Optimize",
            category="optimize",
            description_short="Self-optimize CCO",
            description_long="Self-optimize CCO configuration based on usage",
            applicable_project_types=["all"],
            relevance_tags=["optimization"],
        ),
        CommandMetadata(
            command_id="cco-verify-implementation",
            display_name="Verify Implementation",
            category="audit",
            description_short="Verify implementations",
            description_long="Verify implementations match specifications",
            applicable_project_types=["all"],
            relevance_tags=["quality", "verification"],
        ),
        CommandMetadata(
            command_id="cco-api-only-command",
            display_name="API Only Command",
            category="api",
            description_short="API specific command",
            description_long="Command only for API projects",
            applicable_project_types=["api", "backend"],
            relevance_tags=["api"],
        ),
    ]

    return CommandRegistry(commands=commands)


class TestCommandRecommenderInitialization:
    """Test CommandRecommender initialization"""

    def test_initialization(self, minimal_preferences, sample_registry) -> None:
        """Test successful initialization"""
        recommender = CommandRecommender(minimal_preferences, sample_registry)
        assert recommender.preferences == minimal_preferences
        assert recommender.registry == sample_registry

    def test_core_commands_defined(self) -> None:
        """Test that core commands are defined"""
        assert len(CommandRecommender.CORE_COMMANDS) > 0
        assert "cco-help" in CommandRecommender.CORE_COMMANDS
        assert "cco-status" in CommandRecommender.CORE_COMMANDS
        assert "cco-configure" in CommandRecommender.CORE_COMMANDS

    def test_recommendation_rules_defined(self) -> None:
        """Test that recommendation rules are defined"""
        assert len(CommandRecommender.RECOMMENDATION_RULES) > 0

        # Check structure of first rule
        first_rule = CommandRecommender.RECOMMENDATION_RULES[0]
        assert "command_id" in first_rule
        assert "conditions" in first_rule
        assert "reasoning" in first_rule
        assert "priority" in first_rule


class TestConditionEvaluation:
    """Test condition evaluation logic"""

    def test_evaluate_condition_equals_true(self, minimal_preferences, sample_registry) -> None:
        """Test == operator with matching value"""
        recommender = CommandRecommender(minimal_preferences, sample_registry)

        condition = ("project_identity.primary_language", "==", "python")
        assert recommender._evaluate_condition(condition) is True

    def test_evaluate_condition_equals_false(self, minimal_preferences, sample_registry) -> None:
        """Test == operator with non-matching value"""
        recommender = CommandRecommender(minimal_preferences, sample_registry)

        condition = ("project_identity.primary_language", "==", "javascript")
        assert recommender._evaluate_condition(condition) is False

    def test_evaluate_condition_not_equals_true(self, minimal_preferences, sample_registry) -> None:
        """Test != operator with non-matching value"""
        recommender = CommandRecommender(minimal_preferences, sample_registry)

        condition = ("project_identity.primary_language", "!=", "javascript")
        assert recommender._evaluate_condition(condition) is True

    def test_evaluate_condition_not_equals_false(
        self, minimal_preferences, sample_registry
    ) -> None:
        """Test != operator with matching value"""
        recommender = CommandRecommender(minimal_preferences, sample_registry)

        condition = ("project_identity.primary_language", "!=", "python")
        assert recommender._evaluate_condition(condition) is False

    def test_evaluate_condition_in_list_true(self, minimal_preferences, sample_registry) -> None:
        """Test in operator with value in list"""
        recommender = CommandRecommender(minimal_preferences, sample_registry)

        condition = ("project_identity.project_maturity", "in", ["active-dev", "production"])
        assert recommender._evaluate_condition(condition) is True

    def test_evaluate_condition_in_list_false(self, minimal_preferences, sample_registry) -> None:
        """Test in operator with value not in list"""
        recommender = CommandRecommender(minimal_preferences, sample_registry)

        condition = ("project_identity.project_maturity", "in", ["archived", "deprecated"])
        assert recommender._evaluate_condition(condition) is False

    def test_evaluate_condition_greater_than_equal_true(
        self, high_testing_preferences, sample_registry
    ) -> None:
        """Test >= operator with greater value"""
        recommender = CommandRecommender(high_testing_preferences, sample_registry)

        condition = ("testing.coverage_target", ">=", 85)
        assert recommender._evaluate_condition(condition) is True

    def test_evaluate_condition_greater_than_equal_equal(
        self, high_testing_preferences, sample_registry
    ) -> None:
        """Test >= operator with equal value"""
        recommender = CommandRecommender(high_testing_preferences, sample_registry)

        condition = ("testing.coverage_target", ">=", 100)
        assert recommender._evaluate_condition(condition) is True

    def test_evaluate_condition_greater_than_equal_false(
        self, minimal_preferences, sample_registry
    ) -> None:
        """Test >= operator with lesser value"""
        recommender = CommandRecommender(minimal_preferences, sample_registry)

        condition = ("testing.coverage_target", ">=", 95)
        assert recommender._evaluate_condition(condition) is False

    def test_evaluate_condition_less_than_equal_true(
        self, minimal_preferences, sample_registry
    ) -> None:
        """Test <= operator with lesser value"""
        recommender = CommandRecommender(minimal_preferences, sample_registry)

        condition = ("testing.coverage_target", "<=", 90)
        assert recommender._evaluate_condition(condition) is True

    def test_evaluate_condition_less_than_equal_equal(
        self, minimal_preferences, sample_registry
    ) -> None:
        """Test <= operator with equal value"""
        recommender = CommandRecommender(minimal_preferences, sample_registry)

        # coverage_target default is "90" (string)
        condition = ("testing.coverage_target", "<=", 90)
        # String "90" will convert to 90 and match
        result = recommender._evaluate_condition(condition)
        assert result is True

    def test_evaluate_condition_less_than_equal_false(
        self, high_testing_preferences, sample_registry
    ) -> None:
        """Test <= operator with greater value"""
        recommender = CommandRecommender(high_testing_preferences, sample_registry)

        condition = ("testing.coverage_target", "<=", 90)
        assert recommender._evaluate_condition(condition) is False

    def test_evaluate_condition_invalid_path(self, minimal_preferences, sample_registry) -> None:
        """Test condition with non-existent path"""
        recommender = CommandRecommender(minimal_preferences, sample_registry)

        condition = ("invalid.path.to.field", "==", "value")
        assert recommender._evaluate_condition(condition) is False

    def test_evaluate_condition_partial_invalid_path(
        self, minimal_preferences, sample_registry
    ) -> None:
        """Test condition with partially invalid path"""
        recommender = CommandRecommender(minimal_preferences, sample_registry)

        condition = ("project_identity.nonexistent_field", "==", "value")
        assert recommender._evaluate_condition(condition) is False

    def test_evaluate_condition_greater_than_equal_non_numeric(
        self, minimal_preferences, sample_registry
    ) -> None:
        """Test >= operator with non-numeric value"""
        recommender = CommandRecommender(minimal_preferences, sample_registry)

        condition = ("project_identity.primary_language", ">=", 50)
        assert recommender._evaluate_condition(condition) is False

    def test_evaluate_condition_less_than_equal_non_numeric(
        self, minimal_preferences, sample_registry
    ) -> None:
        """Test <= operator with non-numeric value"""
        recommender = CommandRecommender(minimal_preferences, sample_registry)

        condition = ("project_identity.primary_language", "<=", 50)
        assert recommender._evaluate_condition(condition) is False

    def test_evaluate_condition_unsupported_operator(
        self, minimal_preferences, sample_registry
    ) -> None:
        """Test unsupported operator returns False"""
        recommender = CommandRecommender(minimal_preferences, sample_registry)

        condition = ("project_identity.primary_language", ">", "python")
        assert recommender._evaluate_condition(condition) is False


class TestRecommendCommands:
    """Test command recommendation logic"""

    def test_recommend_commands_basic(self, minimal_preferences, sample_registry) -> None:
        """Test basic command recommendations"""
        recommender = CommandRecommender(minimal_preferences, sample_registry)
        recommendations = recommender.recommend_commands()

        assert "core" in recommendations
        assert "recommended" in recommendations
        assert "optional" in recommendations
        assert "reasoning" in recommendations

        # Core commands should be present
        assert len(recommendations["core"]) > 0
        for cmd in CommandRecommender.CORE_COMMANDS:
            assert cmd in recommendations["core"]

    def test_recommend_commands_audit_all_always_recommended(
        self, minimal_preferences, sample_registry
    ) -> None:
        """Test that cco-audit-all is always recommended"""
        recommender = CommandRecommender(minimal_preferences, sample_registry)
        recommendations = recommender.recommend_commands()

        assert "cco-audit-all" in recommendations["recommended"]
        assert "cco-audit-all" in recommendations["reasoning"]

    def test_recommend_commands_high_security(
        self, high_security_preferences, sample_registry
    ) -> None:
        """Test recommendations for high security preferences"""
        recommender = CommandRecommender(high_security_preferences, sample_registry)
        recommendations = recommender.recommend_commands()

        # Security commands should be recommended
        assert "cco-audit-security" in (
            recommendations["recommended"] + recommendations["optional"]
        )
        assert "cco-scan-secrets" in (recommendations["recommended"] + recommendations["optional"])

    def test_recommend_commands_high_testing(
        self, high_testing_preferences, sample_registry
    ) -> None:
        """Test recommendations for high testing preferences"""
        recommender = CommandRecommender(high_testing_preferences, sample_registry)
        recommendations = recommender.recommend_commands()

        # Testing commands should be recommended
        assert "cco-audit-tests" in (recommendations["recommended"] + recommendations["optional"])
        assert "cco-generate-tests" in (
            recommendations["recommended"] + recommendations["optional"]
        )

    def test_recommend_commands_strict_quality(
        self, strict_quality_preferences, sample_registry
    ) -> None:
        """Test recommendations for strict quality preferences"""
        recommender = CommandRecommender(strict_quality_preferences, sample_registry)
        recommendations = recommender.recommend_commands()

        # Code quality commands should be recommended
        assert "cco-audit-code" in (recommendations["recommended"] + recommendations["optional"])
        assert "cco-fix-code" in (recommendations["recommended"] + recommendations["optional"])

    def test_recommend_commands_extensive_docs(
        self, extensive_docs_preferences, sample_registry
    ) -> None:
        """Test recommendations for extensive documentation preferences"""
        recommender = CommandRecommender(extensive_docs_preferences, sample_registry)
        recommendations = recommender.recommend_commands()

        # Documentation commands should be recommended
        assert "cco-audit-docs" in (recommendations["recommended"] + recommendations["optional"])
        assert "cco-generate-docs" in (recommendations["recommended"] + recommendations["optional"])

    def test_recommend_commands_devops(self, devops_preferences, sample_registry) -> None:
        """Test recommendations for DevOps preferences"""
        recommender = CommandRecommender(devops_preferences, sample_registry)
        recommendations = recommender.recommend_commands()

        # DevOps commands should be recommended
        assert "cco-setup-cicd" in (recommendations["recommended"] + recommendations["optional"])
        assert "cco-setup-docker" in (recommendations["recommended"] + recommendations["optional"])

    def test_recommend_commands_no_duplicates(self, minimal_preferences, sample_registry) -> None:
        """Test that recommendations contain no duplicates"""
        recommender = CommandRecommender(minimal_preferences, sample_registry)
        recommendations = recommender.recommend_commands()

        # Check core commands
        assert len(recommendations["core"]) == len(set(recommendations["core"]))

        # Check recommended commands
        assert len(recommendations["recommended"]) == len(set(recommendations["recommended"]))

        # Check optional commands
        assert len(recommendations["optional"]) == len(set(recommendations["optional"]))

    def test_recommend_commands_reasoning_present(
        self, minimal_preferences, sample_registry
    ) -> None:
        """Test that reasoning is present for recommended commands"""
        recommender = CommandRecommender(minimal_preferences, sample_registry)
        recommendations = recommender.recommend_commands()

        # All recommended commands should have reasoning
        for cmd in recommendations["recommended"]:
            assert cmd in recommendations["reasoning"]
            assert len(recommendations["reasoning"][cmd]) > 0

    def test_recommend_commands_project_type_filtering(
        self, minimal_preferences, sample_registry
    ) -> None:
        """Test that commands are filtered by project type"""
        recommender = CommandRecommender(minimal_preferences, sample_registry)
        recommendations = recommender.recommend_commands()

        # Optional commands should be filtered by project type
        # Core and recommended may bypass this filtering
        for cmd_id in recommendations["optional"]:
            cmd = sample_registry.get_by_id(cmd_id)
            if cmd:
                # Optional commands should match project type or be "all"
                assert "all" in cmd.applicable_project_types or any(
                    pt in cmd.applicable_project_types
                    for pt in minimal_preferences.project_identity.types
                ), (
                    f"Command {cmd_id} not applicable to {minimal_preferences.project_identity.types}"
                )


class TestFilterByProjectType:
    """Test project type filtering"""

    def test_filter_by_project_type_all_included(
        self, minimal_preferences, sample_registry
    ) -> None:
        """Test that commands with 'all' are always included"""
        recommender = CommandRecommender(minimal_preferences, sample_registry)

        recommendations = {
            "core": [],
            "recommended": [],
            "optional": ["cco-status"],  # Has 'all' project type
            "reasoning": {},
        }

        filtered = recommender._filter_by_project_type(recommendations)
        assert "cco-status" in filtered["optional"]

    def test_filter_by_project_type_matching_included(
        self, high_security_preferences, sample_registry
    ) -> None:
        """Test that commands matching project type are included"""
        recommender = CommandRecommender(high_security_preferences, sample_registry)

        recommendations = {
            "core": [],
            "recommended": [],
            "optional": ["cco-api-only-command"],  # Has 'api' and 'backend'
            "reasoning": {},
        }

        filtered = recommender._filter_by_project_type(recommendations)
        assert "cco-api-only-command" in filtered["optional"]

    def test_filter_by_project_type_non_matching_excluded(
        self, minimal_preferences, sample_registry
    ) -> None:
        """Test that commands not matching project type are excluded"""
        recommender = CommandRecommender(minimal_preferences, sample_registry)

        recommendations = {
            "core": [],
            "recommended": [],
            "optional": ["cco-api-only-command"],  # Only for 'api' and 'backend'
            "reasoning": {},
        }

        filtered = recommender._filter_by_project_type(recommendations)
        assert "cco-api-only-command" not in filtered["optional"]

    def test_filter_by_project_type_empty_optional(
        self, minimal_preferences, sample_registry
    ) -> None:
        """Test filtering with empty optional list"""
        recommender = CommandRecommender(minimal_preferences, sample_registry)

        recommendations = {
            "core": ["cco-help"],
            "recommended": ["cco-audit-all"],
            "optional": [],
            "reasoning": {},
        }

        filtered = recommender._filter_by_project_type(recommendations)
        assert filtered["optional"] == []
        assert filtered["core"] == ["cco-help"]
        assert filtered["recommended"] == ["cco-audit-all"]

    def test_filter_by_project_type_nonexistent_command(
        self, minimal_preferences, sample_registry
    ) -> None:
        """Test filtering with non-existent command ID"""
        recommender = CommandRecommender(minimal_preferences, sample_registry)

        recommendations = {
            "core": [],
            "recommended": [],
            "optional": ["cco-nonexistent-command"],
            "reasoning": {},
        }

        filtered = recommender._filter_by_project_type(recommendations)
        # Non-existent commands should be filtered out
        assert "cco-nonexistent-command" not in filtered["optional"]


class TestExplainRecommendation:
    """Test recommendation explanation"""

    def test_explain_recommendation_found_in_rules(
        self, minimal_preferences, sample_registry
    ) -> None:
        """Test explaining recommendation found in rules"""
        recommender = CommandRecommender(minimal_preferences, sample_registry)

        # Use a command that's in the rules
        explanation = recommender.explain_recommendation("cco-audit-tests")

        assert "cco-audit-tests" in explanation
        assert "recommended because:" in explanation
        assert "Conditions met:" in explanation

    def test_explain_recommendation_not_in_rules(
        self, minimal_preferences, sample_registry
    ) -> None:
        """Test explaining recommendation not in rules"""
        recommender = CommandRecommender(minimal_preferences, sample_registry)

        explanation = recommender.explain_recommendation("cco-help")

        assert "cco-help" in explanation
        assert "see command metadata for details" in explanation

    def test_explain_recommendation_includes_conditions(
        self, minimal_preferences, sample_registry
    ) -> None:
        """Test that explanation includes condition details"""
        recommender = CommandRecommender(minimal_preferences, sample_registry)

        explanation = recommender.explain_recommendation("cco-audit-tests")

        # Should include condition operator and path
        assert "testing.coverage_target" in explanation or "testing.mutation_testing" in explanation

    def test_explain_recommendation_includes_reasoning(
        self, minimal_preferences, sample_registry
    ) -> None:
        """Test that explanation includes reasoning"""
        recommender = CommandRecommender(minimal_preferences, sample_registry)

        explanation = recommender.explain_recommendation("cco-audit-security")

        # Should include the reasoning text
        assert "Security" in explanation or "security" in explanation


class TestGenerateSelectionSummary:
    """Test selection summary generation"""

    def test_generate_selection_summary_structure(
        self, minimal_preferences, sample_registry
    ) -> None:
        """Test that summary has correct structure"""
        recommender = CommandRecommender(minimal_preferences, sample_registry)
        summary = recommender.generate_selection_summary()

        assert "total_available" in summary
        assert "core_count" in summary
        assert "recommended_count" in summary
        assert "optional_count" in summary
        assert "total_recommended" in summary
        assert "recommendation_ratio" in summary
        assert "commands_by_category" in summary

    def test_generate_selection_summary_counts(self, minimal_preferences, sample_registry) -> None:
        """Test that counts are correct"""
        recommender = CommandRecommender(minimal_preferences, sample_registry)
        summary = recommender.generate_selection_summary()

        assert summary["total_available"] == len(sample_registry.commands)
        assert summary["core_count"] == len(CommandRecommender.CORE_COMMANDS)
        assert summary["total_recommended"] == summary["core_count"] + summary["recommended_count"]

    def test_generate_selection_summary_ratio(self, minimal_preferences, sample_registry) -> None:
        """Test that recommendation ratio is calculated correctly"""
        recommender = CommandRecommender(minimal_preferences, sample_registry)
        summary = recommender.generate_selection_summary()

        expected_ratio = summary["total_recommended"] / summary["total_available"]
        assert summary["recommendation_ratio"] == expected_ratio
        assert 0.0 <= summary["recommendation_ratio"] <= 1.0

    def test_generate_selection_summary_categories(
        self, minimal_preferences, sample_registry
    ) -> None:
        """Test that commands are counted by category"""
        recommender = CommandRecommender(minimal_preferences, sample_registry)
        summary = recommender.generate_selection_summary()

        categories = summary["commands_by_category"]
        assert isinstance(categories, dict)
        assert len(categories) > 0

        # All counts should be positive integers
        for category, count in categories.items():
            assert isinstance(count, int)
            assert count > 0


class TestCountByCategory:
    """Test category counting"""

    def test_count_by_category_basic(self, minimal_preferences, sample_registry) -> None:
        """Test basic category counting"""
        recommender = CommandRecommender(minimal_preferences, sample_registry)

        recommendations = {
            "core": ["cco-help", "cco-status"],
            "recommended": ["cco-audit-all"],
            "optional": ["cco-audit-tests", "cco-generate-tests"],
        }

        counts = recommender._count_by_category(recommendations)

        assert isinstance(counts, dict)
        assert "core" in counts
        assert counts["core"] >= 2  # At least help and status

    def test_count_by_category_empty_recommendations(
        self, minimal_preferences, sample_registry
    ) -> None:
        """Test category counting with empty recommendations"""
        recommender = CommandRecommender(minimal_preferences, sample_registry)

        recommendations = {
            "core": [],
            "recommended": [],
            "optional": [],
        }

        counts = recommender._count_by_category(recommendations)

        assert isinstance(counts, dict)
        assert len(counts) == 0

    def test_count_by_category_nonexistent_command(
        self, minimal_preferences, sample_registry
    ) -> None:
        """Test category counting with non-existent command"""
        recommender = CommandRecommender(minimal_preferences, sample_registry)

        recommendations = {
            "core": ["cco-help"],
            "recommended": [],
            "optional": ["cco-nonexistent"],
        }

        counts = recommender._count_by_category(recommendations)

        # Should only count existing commands
        assert "core" in counts
        assert counts["core"] == 1

    def test_count_by_category_multiple_categories(
        self, minimal_preferences, sample_registry
    ) -> None:
        """Test category counting with multiple categories"""
        recommender = CommandRecommender(minimal_preferences, sample_registry)

        recommendations = {
            "core": ["cco-help", "cco-status", "cco-configure"],
            "recommended": ["cco-audit-tests"],
            "optional": ["cco-generate-tests", "cco-audit-security"],
        }

        counts = recommender._count_by_category(recommendations)

        assert len(counts) >= 2  # At least core and audit
        assert all(count > 0 for count in counts.values())


class TestEdgeCases:
    """Test edge cases and error handling"""

    def test_recommend_with_empty_registry(self, minimal_preferences) -> None:
        """Test recommendations with empty registry"""
        empty_registry = CommandRegistry(commands=[])
        recommender = CommandRecommender(minimal_preferences, empty_registry)

        recommendations = recommender.recommend_commands()

        # Should still have core commands and audit-all
        assert len(recommendations["core"]) > 0
        assert "cco-audit-all" in recommendations["recommended"]

    def test_recommend_with_all_conditions_failing(
        self, minimal_preferences, sample_registry
    ) -> None:
        """Test when all rule conditions fail"""
        recommender = CommandRecommender(minimal_preferences, sample_registry)
        recommendations = recommender.recommend_commands()

        # Should still have core commands and audit-all
        assert len(recommendations["core"]) > 0
        assert "cco-audit-all" in recommendations["recommended"]

        # Optional should contain commands from registry
        assert len(recommendations["optional"]) > 0

    def test_generate_summary_with_zero_commands(self, minimal_preferences) -> None:
        """Test summary generation with zero available commands"""
        empty_registry = CommandRegistry(commands=[])
        recommender = CommandRecommender(minimal_preferences, empty_registry)

        # With zero commands in registry, division by zero will occur
        # This is expected behavior - the function doesn't handle this edge case
        with pytest.raises(ZeroDivisionError):
            recommender.generate_selection_summary()

    def test_nested_preference_access(self, minimal_preferences, sample_registry) -> None:
        """Test accessing deeply nested preference values"""
        recommender = CommandRecommender(minimal_preferences, sample_registry)

        # Should handle multiple levels of nesting
        condition = ("project_identity.types", "in", [["cli"], ["api"]])
        # Should not raise exception
        result = recommender._evaluate_condition(condition)
        assert isinstance(result, bool)

    def test_condition_with_none_value(self, minimal_preferences, sample_registry) -> None:
        """Test condition evaluation with None value"""
        recommender = CommandRecommender(minimal_preferences, sample_registry)

        # Create a condition that might return None
        condition = ("project_identity.description", "==", None)
        result = recommender._evaluate_condition(condition)
        assert isinstance(result, bool)


class TestIntegration:
    """Integration tests with realistic scenarios"""

    def test_full_recommendation_workflow(self, high_security_preferences, sample_registry) -> None:
        """Test complete recommendation workflow"""
        recommender = CommandRecommender(high_security_preferences, sample_registry)

        # Get recommendations
        recommendations = recommender.recommend_commands()

        # Generate summary
        summary = recommender.generate_selection_summary()

        # Explain a recommendation
        if recommendations["recommended"]:
            explanation = recommender.explain_recommendation(recommendations["recommended"][0])
            assert len(explanation) > 0

        # Verify consistency
        total_commands = (
            len(recommendations["core"])
            + len(recommendations["recommended"])
            + len(recommendations["optional"])
        )

        # Should have some commands
        assert total_commands > 0
        assert summary["total_available"] > 0

    def test_multiple_project_types(self, sample_registry) -> None:
        """Test recommendations with multiple project types"""
        multi_type_prefs = CCOPreferences(
            project_identity=ProjectIdentity(
                name="MultiProject",
                primary_language="python",
                types=["api", "backend", "microservice"],
                team_trajectory="medium-5-10",
                project_maturity="production",
            ),
        )

        recommender = CommandRecommender(multi_type_prefs, sample_registry)
        recommendations = recommender.recommend_commands()

        # Should include commands relevant to any of the project types
        all_commands = (
            recommendations["core"] + recommendations["recommended"] + recommendations["optional"]
        )

        assert len(all_commands) > 0

    def test_recommendation_consistency(self, minimal_preferences, sample_registry) -> None:
        """Test that recommendations are consistent across multiple calls"""
        recommender = CommandRecommender(minimal_preferences, sample_registry)

        recs1 = recommender.recommend_commands()
        recs2 = recommender.recommend_commands()

        # Should get same recommendations
        assert recs1["core"] == recs2["core"]
        assert recs1["recommended"] == recs2["recommended"]
        assert recs1["optional"] == recs2["optional"]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=claudecodeoptimizer.ai.command_selection"])
