"""
Comprehensive tests for wizard decision_tree module.

Tests cover:
- Decision tree structure and organization
- Auto-detection strategies for all decision points
- AI hint generation
- Conditional logic (skip_if, should_ask)
- Dynamic TIER 3 tool decisions
- Validation functions
- Complete decision tree navigation
"""

from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest

from claudecodeoptimizer.wizard.decision_tree import (
    DECISION_TREE_TIER1,
    DECISION_TREE_TIER2,
    TIER1_DEVELOPMENT_PHILOSOPHY,
    TIER1_PROJECT_MATURITY,
    TIER1_PROJECT_PURPOSE,
    TIER1_TEAM_DYNAMICS,
    TIER2_CI_PROVIDER,
    TIER2_DOCUMENTATION_LEVEL,
    TIER2_ERROR_HANDLING,
    TIER2_GIT_WORKFLOW,
    TIER2_PRINCIPLE_STRATEGY,
    TIER2_SECRETS_MANAGEMENT,
    TIER2_SECURITY_STANCE,
    TIER2_TESTING_APPROACH,
    TIER2_VERSIONING_STRATEGY,
    TIER3_API_DOCS_TOOL,
    TIER3_AUTH_PATTERN,
    TIER3_BRANCH_NAMING,
    TIER3_CODE_REVIEW_REQUIREMENTS,
    TIER3_DOCUMENTATION_STRATEGY,
    TIER3_LINE_LENGTH,
    TIER3_LOGGING_LEVEL,
    TIER3_NAMING_CONVENTION,
    TIER3_PACKAGE_MANAGER,
    TIER3_PRECOMMIT_HOOKS,
    _auto_detect_api_docs_tool,
    _auto_detect_auth_pattern,
    _auto_detect_branch_naming,
    _auto_detect_ci_provider,
    _auto_detect_code_review_requirements,
    _auto_detect_documentation_strategy,
    _auto_detect_error_handling,
    _auto_detect_line_length,
    _auto_detect_logging_level,
    _auto_detect_maturity,
    _auto_detect_package_manager,
    _auto_detect_philosophy,
    _auto_detect_precommit_hooks,
    _auto_detect_project_purpose,
    _auto_detect_secrets_management,
    _auto_detect_security_stance,
    _auto_detect_team_size,
    _auto_detect_testing_approach,
    _auto_detect_versioning_strategy,
    _auto_select_principle_strategy,
    _generate_ci_provider_hint,
    _generate_error_handling_hint,
    _generate_git_workflow_hint,
    _generate_logging_level_hint,
    _generate_precommit_hooks_hint,
    _generate_secrets_management_hint,
    _generate_testing_hint,
    _generate_versioning_hint,
    _get_principle_strategy_options,
    _should_ask_api_docs_tool,
    _should_ask_auth_pattern,
    _should_ask_code_review_requirements,
    _validate_project_purpose,
    build_tier3_tool_decisions,
    get_all_decisions,
    get_decisions_by_tier,
)
from claudecodeoptimizer.wizard.models import AnswerContext, DecisionPoint, SystemContext


@pytest.fixture
def mock_system_context():
    """Create a mock system context for testing"""
    return SystemContext(
        os_type="linux",
        os_version="5.15.0",
        os_platform="linux",
        shell_type="bash",
        terminal_emulator="gnome-terminal",
        color_support=True,
        unicode_support=True,
        system_locale="en_US",
        detected_language="en",
        encoding="utf-8",
        python_version="3.11.0",
        python_executable="/usr/bin/python3",
        pip_version="23.0.1",
        git_installed=True,
        project_root=Path("/tmp/test_project"),
        is_git_repo=True,
        existing_tools=["pytest", "black", "ruff"],
        file_count=100,
        line_count=5000,
        has_tests=True,
        has_ci=True,
        detected_languages=["python"],
        detected_frameworks=["fastapi"],
        detected_project_types=["backend"],
    )


@pytest.fixture
def mock_answer_context(mock_system_context):
    """Create a mock answer context for testing"""
    return AnswerContext(
        system=mock_system_context,
        answers={
            "project_purpose": ["backend"],
            "team_dynamics": "solo",
            "project_maturity": "mvp",
            "development_philosophy": "balanced",
            "principle_strategy": "recommended",
            "testing_approach": "balanced",
            "security_stance": "production",
            "documentation_level": "practical",
            "git_workflow": "main_only",
        },
    )


class TestDecisionTreeStructure:
    """Test decision tree structure and organization"""

    def test_tier1_decision_count(self):
        """Test TIER 1 has exactly 4 fundamental decisions"""
        assert len(DECISION_TREE_TIER1) == 4

    def test_tier1_decision_ids(self):
        """Test TIER 1 decision IDs are correct"""
        ids = [dp.id for dp in DECISION_TREE_TIER1]
        assert "project_purpose" in ids
        assert "team_dynamics" in ids
        assert "project_maturity" in ids
        assert "development_philosophy" in ids

    def test_tier1_all_have_tier_1(self):
        """Test all TIER 1 decisions have tier=1"""
        for dp in DECISION_TREE_TIER1:
            assert dp.tier == 1

    def test_tier2_decision_count(self):
        """Test TIER 2 has expected number of strategy decisions"""
        assert len(DECISION_TREE_TIER2) == 9

    def test_tier2_decision_ids(self):
        """Test TIER 2 decision IDs are correct"""
        ids = [dp.id for dp in DECISION_TREE_TIER2]
        assert "principle_strategy" in ids
        assert "testing_approach" in ids
        assert "security_stance" in ids
        assert "documentation_level" in ids
        assert "git_workflow" in ids
        assert "versioning_strategy" in ids
        assert "ci_provider" in ids
        assert "secrets_management" in ids
        assert "error_handling" in ids

    def test_tier2_all_have_tier_2(self):
        """Test all TIER 2 decisions have tier=2"""
        for dp in DECISION_TREE_TIER2:
            assert dp.tier == 2

    def test_all_decisions_have_options(self):
        """Test all decisions have at least 2 options"""
        all_decisions = DECISION_TREE_TIER1 + DECISION_TREE_TIER2
        for dp in all_decisions:
            assert len(dp.options) >= 2, f"{dp.id} has less than 2 options"

    def test_all_decisions_have_questions(self):
        """Test all decisions have question text"""
        all_decisions = DECISION_TREE_TIER1 + DECISION_TREE_TIER2
        for dp in all_decisions:
            assert dp.question, f"{dp.id} has no question"
            assert len(dp.question) > 0

    def test_all_decisions_have_category(self):
        """Test all decisions have category"""
        all_decisions = DECISION_TREE_TIER1 + DECISION_TREE_TIER2
        for dp in all_decisions:
            assert dp.category, f"{dp.id} has no category"


class TestTier1DecisionPoints:
    """Test TIER 1 decision points"""

    def test_project_purpose_multi_select(self):
        """Test project_purpose allows multiple selections"""
        assert TIER1_PROJECT_PURPOSE.multi_select is True

    def test_project_purpose_has_validator(self):
        """Test project_purpose has validator"""
        assert TIER1_PROJECT_PURPOSE.validator is not None

    def test_project_purpose_validator_accepts_list(self):
        """Test project_purpose validator accepts list"""
        validator = TIER1_PROJECT_PURPOSE.validator
        assert validator(["backend", "microservice"]) is True

    def test_project_purpose_validator_accepts_string(self):
        """Test project_purpose validator accepts non-list"""
        validator = TIER1_PROJECT_PURPOSE.validator
        assert validator("backend") is True

    def test_project_purpose_has_auto_strategy(self):
        """Test project_purpose has auto-detection strategy"""
        assert TIER1_PROJECT_PURPOSE.auto_strategy is not None

    def test_team_dynamics_single_select(self):
        """Test team_dynamics is single select"""
        assert TIER1_TEAM_DYNAMICS.multi_select is False

    def test_team_dynamics_has_4_options(self):
        """Test team_dynamics has 4 team size options"""
        assert len(TIER1_TEAM_DYNAMICS.options) == 4

    def test_project_maturity_has_5_stages(self):
        """Test project_maturity has 5 maturity stages"""
        assert len(TIER1_PROJECT_MATURITY.options) == 5

    def test_development_philosophy_has_3_options(self):
        """Test development_philosophy has 3 philosophy options"""
        assert len(TIER1_DEVELOPMENT_PHILOSOPHY.options) == 3


class TestTier2DecisionPoints:
    """Test TIER 2 decision points"""

    def test_principle_strategy_dynamic_options(self):
        """Test principle_strategy generates options dynamically"""
        options = _get_principle_strategy_options()
        assert len(options) == 4
        assert any(opt.value == "recommended" for opt in options)
        assert any(opt.value == "minimal" for opt in options)
        assert any(opt.value == "comprehensive" for opt in options)
        assert any(opt.value == "custom" for opt in options)

    def test_testing_approach_has_4_options(self):
        """Test testing_approach has 4 testing levels"""
        assert len(TIER2_TESTING_APPROACH.options) == 4

    def test_security_stance_has_3_options(self):
        """Test security_stance has 3 security levels"""
        assert len(TIER2_SECURITY_STANCE.options) == 3

    def test_git_workflow_has_skip_condition(self):
        """Test git_workflow has skip condition for solo devs"""
        assert TIER2_GIT_WORKFLOW.skip_if is not None

    def test_git_workflow_skip_for_solo(self):
        """Test git_workflow is skipped for solo developers"""
        skip_func = TIER2_GIT_WORKFLOW.skip_if
        assert skip_func({"team_dynamics": "solo"}) is True

    def test_git_workflow_not_skip_for_team(self):
        """Test git_workflow is not skipped for teams"""
        skip_func = TIER2_GIT_WORKFLOW.skip_if
        assert skip_func({"team_dynamics": "small_team"}) is False

    def test_versioning_strategy_has_5_options(self):
        """Test versioning_strategy has 5 versioning options"""
        assert len(TIER2_VERSIONING_STRATEGY.options) == 5

    def test_ci_provider_has_4_options(self):
        """Test ci_provider has 4 provider options"""
        assert len(TIER2_CI_PROVIDER.options) == 4

    def test_secrets_management_has_4_options(self):
        """Test secrets_management has 4 secret management options"""
        assert len(TIER2_SECRETS_MANAGEMENT.options) == 4

    def test_error_handling_has_3_options(self):
        """Test error_handling has 3 error handling strategies"""
        assert len(TIER2_ERROR_HANDLING.options) == 3


class TestTier3DecisionPoints:
    """Test TIER 3 tactical decision points"""

    def test_precommit_hooks_multi_select(self):
        """Test precommit_hooks allows multiple selections"""
        assert TIER3_PRECOMMIT_HOOKS.multi_select is True

    def test_precommit_hooks_has_5_options(self):
        """Test precommit_hooks has 5 hook options"""
        assert len(TIER3_PRECOMMIT_HOOKS.options) == 5

    def test_logging_level_has_4_levels(self):
        """Test logging_level has 4 log levels"""
        assert len(TIER3_LOGGING_LEVEL.options) == 4

    def test_branch_naming_has_4_conventions(self):
        """Test branch_naming has 4 naming conventions"""
        assert len(TIER3_BRANCH_NAMING.options) == 4

    def test_naming_convention_has_3_options(self):
        """Test naming_convention has 3 naming styles"""
        assert len(TIER3_NAMING_CONVENTION.options) == 3

    def test_line_length_has_4_options(self):
        """Test line_length has 4 length options"""
        assert len(TIER3_LINE_LENGTH.options) == 4

    def test_package_manager_has_6_options(self):
        """Test package_manager has 6 package manager options"""
        assert len(TIER3_PACKAGE_MANAGER.options) == 6

    def test_documentation_strategy_has_3_levels(self):
        """Test documentation_strategy has 3 documentation levels"""
        assert len(TIER3_DOCUMENTATION_STRATEGY.options) == 3


class TestConditionalDecisions:
    """Test conditional decision points (TIER 3)"""

    def test_auth_pattern_has_skip_condition(self):
        """Test auth_pattern has skip condition"""
        assert TIER3_AUTH_PATTERN.skip_if is not None

    def test_api_docs_tool_has_skip_condition(self):
        """Test api_docs_tool has skip condition"""
        assert TIER3_API_DOCS_TOOL.skip_if is not None

    def test_code_review_requirements_has_skip_condition(self):
        """Test code_review_requirements has skip condition"""
        assert TIER3_CODE_REVIEW_REQUIREMENTS.skip_if is not None

    def test_should_ask_auth_pattern_for_api(self, mock_answer_context):
        """Test auth pattern is asked for API projects"""
        mock_answer_context.answers["project_purpose"] = ["api_service"]
        assert _should_ask_auth_pattern(mock_answer_context) is True

    def test_should_ask_auth_pattern_for_web_app(self, mock_answer_context):
        """Test auth pattern is asked for web apps"""
        mock_answer_context.answers["project_purpose"] = ["web_app"]
        assert _should_ask_auth_pattern(mock_answer_context) is True

    def test_should_not_ask_auth_pattern_for_cli(self, mock_answer_context):
        """Test auth pattern is not asked for CLI tools"""
        mock_answer_context.answers["project_purpose"] = ["cli"]
        assert _should_ask_auth_pattern(mock_answer_context) is False

    def test_should_ask_api_docs_for_api_service(self, mock_answer_context):
        """Test API docs is asked for API services"""
        mock_answer_context.answers["project_purpose"] = ["api_service"]
        assert _should_ask_api_docs_tool(mock_answer_context) is True

    def test_should_not_ask_api_docs_for_library(self, mock_answer_context):
        """Test API docs is not asked for libraries"""
        mock_answer_context.answers["project_purpose"] = ["library"]
        assert _should_ask_api_docs_tool(mock_answer_context) is False

    def test_should_ask_code_review_for_team(self, mock_answer_context):
        """Test code review is asked for team projects"""
        mock_answer_context.answers["team_dynamics"] = "small_team"
        assert _should_ask_code_review_requirements(mock_answer_context) is True

    def test_should_not_ask_code_review_for_solo(self, mock_answer_context):
        """Test code review is not asked for solo developers"""
        mock_answer_context.answers["team_dynamics"] = "solo"
        assert _should_ask_code_review_requirements(mock_answer_context) is False


class TestAutoDetectionStrategies:
    """Test auto-detection strategies"""

    def test_auto_detect_project_purpose_from_detected_types(self, mock_answer_context):
        """Test project purpose uses detected types when available"""
        mock_answer_context.system.detected_project_types = ["backend", "microservice"]
        result = _auto_detect_project_purpose(mock_answer_context)
        assert "backend" in result
        assert "microservice" in result

    def test_auto_detect_project_purpose_from_frameworks(self, mock_answer_context):
        """Test project purpose infers from frameworks"""
        mock_answer_context.system.detected_project_types = []
        mock_answer_context.system.detected_frameworks = ["fastapi", "flask"]
        result = _auto_detect_project_purpose(mock_answer_context)
        assert "backend" in result

    def test_auto_detect_project_purpose_frontend(self, mock_answer_context):
        """Test project purpose detects frontend projects"""
        mock_answer_context.system.detected_project_types = []
        mock_answer_context.system.detected_frameworks = ["react", "vue"]
        result = _auto_detect_project_purpose(mock_answer_context)
        assert "spa" in result

    def test_auto_detect_project_purpose_fullstack(self, mock_answer_context):
        """Test project purpose detects full-stack projects"""
        mock_answer_context.system.detected_project_types = []
        mock_answer_context.system.detected_frameworks = ["next", "fastapi"]
        result = _auto_detect_project_purpose(mock_answer_context)
        assert "web-app" in result

    def test_auto_detect_team_size_solo_no_ci(self, mock_answer_context):
        """Test team size detects solo developer without CI"""
        mock_answer_context.system.has_ci = False
        result = _auto_detect_team_size(mock_answer_context)
        assert result == "solo"

    def test_auto_detect_team_size_team_with_ci(self, mock_answer_context):
        """Test team size detects team with CI"""
        mock_answer_context.system.has_ci = True
        mock_answer_context.system.has_tests = True
        result = _auto_detect_team_size(mock_answer_context)
        assert result == "small-2-5"

    def test_auto_detect_maturity_prototype(self, mock_answer_context):
        """Test maturity detects prototype projects"""
        mock_answer_context.system.has_tests = False
        mock_answer_context.system.file_count = 30
        result = _auto_detect_maturity(mock_answer_context)
        assert result == "prototype"

    def test_auto_detect_maturity_mvp(self, mock_answer_context):
        """Test maturity detects MVP projects"""
        mock_answer_context.system.has_tests = True
        mock_answer_context.system.has_ci = False
        result = _auto_detect_maturity(mock_answer_context)
        assert result == "mvp"

    def test_auto_detect_maturity_production(self, mock_answer_context):
        """Test maturity detects production projects"""
        mock_answer_context.system.has_tests = True
        mock_answer_context.system.has_ci = True
        mock_answer_context.system.file_count = 250
        result = _auto_detect_maturity(mock_answer_context)
        assert result == "production"

    def test_auto_detect_philosophy_prototype(self, mock_answer_context):
        """Test philosophy detects move_fast for prototypes"""
        mock_answer_context.answers["project_maturity"] = "prototype"
        result = _auto_detect_philosophy(mock_answer_context)
        assert result == "move_fast"

    def test_auto_detect_philosophy_production(self, mock_answer_context):
        """Test philosophy detects quality_first for production"""
        mock_answer_context.answers["project_maturity"] = "production"
        result = _auto_detect_philosophy(mock_answer_context)
        assert result == "quality_first"

    def test_auto_detect_philosophy_balanced(self, mock_answer_context):
        """Test philosophy defaults to balanced"""
        mock_answer_context.answers["project_maturity"] = "mvp"
        result = _auto_detect_philosophy(mock_answer_context)
        assert result == "balanced"


class TestPrincipleStrategySelection:
    """Test principle strategy auto-selection"""

    def test_auto_select_minimal_for_prototype(self, mock_answer_context):
        """Test minimal strategy for prototype projects"""
        mock_answer_context.answers["project_maturity"] = "prototype"
        mock_answer_context.answers["development_philosophy"] = "move_fast"
        result = _auto_select_principle_strategy(mock_answer_context)
        assert result == "minimal"

    def test_auto_select_comprehensive_for_quality_first(self, mock_answer_context):
        """Test comprehensive strategy for quality-first philosophy"""
        mock_answer_context.answers["development_philosophy"] = "quality_first"
        result = _auto_select_principle_strategy(mock_answer_context)
        assert result == "comprehensive"

    def test_auto_select_recommended_for_balanced(self, mock_answer_context):
        """Test recommended strategy for balanced approach"""
        mock_answer_context.answers["development_philosophy"] = "balanced"
        result = _auto_select_principle_strategy(mock_answer_context)
        assert result == "recommended"


class TestTestingApproachDetection:
    """Test testing approach auto-detection"""

    def test_auto_detect_no_tests(self, mock_answer_context):
        """Test detects no tests when tests don't exist"""
        mock_answer_context.system.has_tests = False
        result = _auto_detect_testing_approach(mock_answer_context)
        assert result == "no_tests"

    def test_auto_detect_comprehensive_for_quality_first(self, mock_answer_context):
        """Test detects comprehensive for quality-first philosophy"""
        mock_answer_context.system.has_tests = True
        mock_answer_context.answers["development_philosophy"] = "quality_first"
        result = _auto_detect_testing_approach(mock_answer_context)
        assert result == "comprehensive"

    def test_auto_detect_balanced_for_production(self, mock_answer_context):
        """Test detects balanced for production projects"""
        mock_answer_context.system.has_tests = True
        mock_answer_context.answers["project_maturity"] = "production"
        result = _auto_detect_testing_approach(mock_answer_context)
        assert result == "balanced"

    def test_auto_detect_critical_paths_default(self, mock_answer_context):
        """Test detects critical paths as default"""
        mock_answer_context.system.has_tests = True
        mock_answer_context.answers["project_maturity"] = "mvp"
        mock_answer_context.answers["development_philosophy"] = "balanced"
        result = _auto_detect_testing_approach(mock_answer_context)
        assert result == "critical_paths"


class TestSecurityStanceDetection:
    """Test security stance auto-detection"""

    def test_auto_detect_production_for_api(self, mock_answer_context):
        """Test detects production security for API services"""
        mock_answer_context.answers["project_purpose"] = ["api_service"]
        result = _auto_detect_security_stance(mock_answer_context)
        assert result == "production"

    def test_auto_detect_production_for_web_app(self, mock_answer_context):
        """Test detects production security for web apps"""
        mock_answer_context.answers["project_purpose"] = ["web_app"]
        result = _auto_detect_security_stance(mock_answer_context)
        assert result == "production"

    def test_auto_detect_standard_for_prototype(self, mock_answer_context):
        """Test detects standard security for prototypes"""
        mock_answer_context.answers["project_purpose"] = ["cli"]
        mock_answer_context.answers["project_maturity"] = "prototype"
        result = _auto_detect_security_stance(mock_answer_context)
        assert result == "standard"

    def test_auto_detect_production_for_data_pipeline(self, mock_answer_context):
        """Test detects production security for data pipelines"""
        mock_answer_context.answers["project_purpose"] = ["data-pipeline"]
        result = _auto_detect_security_stance(mock_answer_context)
        assert result == "production"


class TestDocumentationLevelDetection:
    """Test documentation level auto-detection"""

    def test_auto_detect_comprehensive_for_library(self, mock_answer_context):
        """Test detects comprehensive docs for libraries"""
        from claudecodeoptimizer.wizard.decision_tree import _auto_detect_documentation_level
        mock_answer_context.answers["project_purpose"] = ["library"]
        result = _auto_detect_documentation_level(mock_answer_context)
        assert result == "comprehensive"

    def test_auto_detect_practical_for_api(self, mock_answer_context):
        """Test detects practical docs for APIs"""
        from claudecodeoptimizer.wizard.decision_tree import _auto_detect_documentation_level
        mock_answer_context.answers["project_purpose"] = ["api_service"]
        result = _auto_detect_documentation_level(mock_answer_context)
        assert result == "practical"

    def test_auto_detect_minimal_for_solo(self, mock_answer_context):
        """Test detects minimal docs for solo developers"""
        from claudecodeoptimizer.wizard.decision_tree import _auto_detect_documentation_level
        mock_answer_context.answers["team_dynamics"] = "solo"
        mock_answer_context.answers["project_purpose"] = ["cli"]
        result = _auto_detect_documentation_level(mock_answer_context)
        assert result == "minimal"


class TestVersioningStrategyDetection:
    """Test versioning strategy auto-detection"""

    def test_auto_detect_no_versioning_for_prototype(self, mock_answer_context):
        """Test detects no versioning for prototypes"""
        mock_answer_context.answers["project_maturity"] = "prototype"
        result = _auto_detect_versioning_strategy(mock_answer_context)
        assert result == "no_versioning"

    def test_auto_detect_auto_semver_for_solo(self, mock_answer_context):
        """Test detects auto semver for solo developers"""
        mock_answer_context.answers["team_dynamics"] = "solo"
        mock_answer_context.answers["project_purpose"] = ["library"]
        result = _auto_detect_versioning_strategy(mock_answer_context)
        assert result == "auto_semver"

    def test_auto_detect_manual_semver_for_large_org(self, mock_answer_context):
        """Test detects manual semver for large organizations"""
        mock_answer_context.answers["team_dynamics"] = "large_org"
        result = _auto_detect_versioning_strategy(mock_answer_context)
        assert result == "manual_semver"

    def test_auto_detect_pr_based_for_team_production(self, mock_answer_context):
        """Test detects PR-based semver for team production projects"""
        mock_answer_context.answers["team_dynamics"] = "small_team"
        mock_answer_context.answers["project_maturity"] = "production"
        result = _auto_detect_versioning_strategy(mock_answer_context)
        assert result == "pr_based_semver"


class TestCIProviderDetection:
    """Test CI provider auto-detection"""

    def test_auto_detect_github_actions_from_directory(self, mock_answer_context):
        """Test detects GitHub Actions from .github/workflows"""
        mock_answer_context.system.has_ci = True
        workflows_dir = mock_answer_context.system.project_root / ".github" / "workflows"
        workflows_dir.mkdir(parents=True, exist_ok=True)
        result = _auto_detect_ci_provider(mock_answer_context)
        workflows_dir.rmdir()
        (mock_answer_context.system.project_root / ".github").rmdir()
        assert result == "github_actions"

    def test_auto_detect_none_no_ci(self, mock_answer_context):
        """Test detects none when no CI exists"""
        mock_answer_context.system.has_ci = False
        mock_answer_context.system.is_git_repo = False
        result = _auto_detect_ci_provider(mock_answer_context)
        assert result == "none"

    def test_auto_detect_github_actions_default_for_git(self, mock_answer_context):
        """Test defaults to GitHub Actions for git repos"""
        mock_answer_context.system.has_ci = False
        mock_answer_context.system.is_git_repo = True
        result = _auto_detect_ci_provider(mock_answer_context)
        assert result == "github_actions"


class TestSecretsManagementDetection:
    """Test secrets management auto-detection"""

    def test_auto_detect_dotenv_from_env_file(self, mock_answer_context):
        """Test detects dotenv from .env file"""
        env_file = mock_answer_context.system.project_root / ".env"
        env_file.parent.mkdir(parents=True, exist_ok=True)
        env_file.touch()
        result = _auto_detect_secrets_management(mock_answer_context)
        env_file.unlink()
        assert result == "dotenv"

    def test_auto_detect_cloud_secrets_for_microservice(self, mock_answer_context):
        """Test detects cloud secrets for microservices"""
        mock_answer_context.answers["project_purpose"] = ["microservice"]
        result = _auto_detect_secrets_management(mock_answer_context)
        assert result == "cloud_secrets"

    def test_auto_detect_vault_for_large_org(self, mock_answer_context):
        """Test detects vault for large organizations"""
        mock_answer_context.answers["team_dynamics"] = "large_org"
        result = _auto_detect_secrets_management(mock_answer_context)
        assert result == "vault"


class TestErrorHandlingDetection:
    """Test error handling auto-detection"""

    def test_auto_detect_fail_fast_for_quality_first(self, mock_answer_context):
        """Test detects fail-fast for quality-first philosophy"""
        mock_answer_context.answers["development_philosophy"] = "quality_first"
        result = _auto_detect_error_handling(mock_answer_context)
        assert result == "fail_fast"

    def test_auto_detect_retry_logic_for_microservice(self, mock_answer_context):
        """Test detects retry logic for microservices when no philosophy set"""
        # Remove philosophy to test project type logic
        del mock_answer_context.answers["development_philosophy"]
        mock_answer_context.answers["project_purpose"] = ["microservice"]
        result = _auto_detect_error_handling(mock_answer_context)
        assert result == "retry_logic"

    def test_auto_detect_graceful_degradation_for_web_app(self, mock_answer_context):
        """Test detects graceful degradation for web apps when no philosophy set"""
        # Remove philosophy to test project type logic
        del mock_answer_context.answers["development_philosophy"]
        mock_answer_context.answers["project_purpose"] = ["web_app"]
        result = _auto_detect_error_handling(mock_answer_context)
        assert result == "graceful_degradation"


class TestPrecommitHooksDetection:
    """Test pre-commit hooks auto-detection"""

    @patch("claudecodeoptimizer.wizard.decision_tree._context_matrix")
    def test_auto_detect_precommit_hooks(self, mock_matrix, mock_answer_context):
        """Test detects pre-commit hooks using context matrix"""
        mock_matrix.recommend_precommit_hooks.return_value = ["format", "lint"]
        result = _auto_detect_precommit_hooks(mock_answer_context)
        assert "format" in result
        assert "lint" in result


class TestLoggingLevelDetection:
    """Test logging level auto-detection"""

    def test_auto_detect_debug_for_prototype(self, mock_answer_context):
        """Test detects DEBUG for prototypes"""
        mock_answer_context.answers["project_maturity"] = "prototype"
        result = _auto_detect_logging_level(mock_answer_context)
        assert result == "DEBUG"

    def test_auto_detect_info_for_mvp(self, mock_answer_context):
        """Test detects INFO for MVP"""
        mock_answer_context.answers["project_maturity"] = "mvp"
        result = _auto_detect_logging_level(mock_answer_context)
        assert result == "INFO"

    def test_auto_detect_info_for_production(self, mock_answer_context):
        """Test detects INFO for production"""
        mock_answer_context.answers["project_maturity"] = "production"
        result = _auto_detect_logging_level(mock_answer_context)
        assert result == "INFO"


class TestBranchNamingDetection:
    """Test branch naming convention auto-detection"""

    def test_auto_detect_conventional_for_large_team(self, mock_answer_context):
        """Test detects conventional for large teams"""
        mock_answer_context.answers["team_dynamics"] = "growing_team"
        result = _auto_detect_branch_naming(mock_answer_context)
        assert result == "conventional"

    def test_auto_detect_descriptive_for_small_team(self, mock_answer_context):
        """Test detects descriptive for small teams"""
        mock_answer_context.answers["team_dynamics"] = "small_team"
        result = _auto_detect_branch_naming(mock_answer_context)
        assert result == "descriptive"

    def test_auto_detect_freeform_for_solo(self, mock_answer_context):
        """Test detects freeform for solo developers"""
        mock_answer_context.answers["team_dynamics"] = "solo"
        result = _auto_detect_branch_naming(mock_answer_context)
        assert result == "freeform"


class TestLineLengthDetection:
    """Test line length auto-detection"""

    def test_auto_detect_88_for_black(self, mock_answer_context):
        """Test detects 88 when black is used"""
        mock_answer_context.system.existing_tools = ["black"]
        result = _auto_detect_line_length(mock_answer_context)
        assert result == "88"

    def test_auto_detect_88_for_ruff(self, mock_answer_context):
        """Test detects 88 when ruff is used"""
        mock_answer_context.system.existing_tools = ["ruff"]
        result = _auto_detect_line_length(mock_answer_context)
        assert result == "88"

    def test_auto_detect_88_default(self, mock_answer_context):
        """Test detects 88 as default"""
        mock_answer_context.system.existing_tools = []
        result = _auto_detect_line_length(mock_answer_context)
        assert result == "88"


class TestPackageManagerDetection:
    """Test package manager auto-detection"""

    def test_auto_detect_poetry_from_lock(self, mock_answer_context):
        """Test detects poetry from poetry.lock"""
        lock_file = mock_answer_context.system.project_root / "poetry.lock"
        lock_file.parent.mkdir(parents=True, exist_ok=True)
        lock_file.touch()
        result = _auto_detect_package_manager(mock_answer_context)
        lock_file.unlink()
        assert result == "poetry"

    def test_auto_detect_npm_from_lock(self, mock_answer_context):
        """Test detects npm from package-lock.json"""
        lock_file = mock_answer_context.system.project_root / "package-lock.json"
        lock_file.parent.mkdir(parents=True, exist_ok=True)
        lock_file.touch()
        result = _auto_detect_package_manager(mock_answer_context)
        lock_file.unlink()
        assert result == "npm"

    def test_auto_detect_pip_default(self, mock_answer_context):
        """Test detects pip as default"""
        result = _auto_detect_package_manager(mock_answer_context)
        assert result == "pip"


class TestDocumentationStrategyDetection:
    """Test documentation strategy auto-detection"""

    def test_auto_detect_comprehensive_for_library(self, mock_answer_context):
        """Test detects comprehensive for libraries"""
        mock_answer_context.answers["project_purpose"] = ["library"]
        result = _auto_detect_documentation_strategy(mock_answer_context)
        assert result == "comprehensive"

    def test_auto_detect_minimal_for_prototype(self, mock_answer_context):
        """Test detects minimal for prototypes"""
        mock_answer_context.answers["project_maturity"] = "prototype"
        result = _auto_detect_documentation_strategy(mock_answer_context)
        assert result == "minimal"

    def test_auto_detect_standard_default(self, mock_answer_context):
        """Test detects standard as default"""
        mock_answer_context.answers["project_purpose"] = ["cli"]
        mock_answer_context.answers["project_maturity"] = "mvp"
        result = _auto_detect_documentation_strategy(mock_answer_context)
        assert result == "standard"


class TestAuthPatternDetection:
    """Test auth pattern auto-detection"""

    def test_auto_detect_jwt_for_api_service(self, mock_answer_context):
        """Test detects JWT for API services"""
        mock_answer_context.answers["project_purpose"] = ["api_service"]
        result = _auto_detect_auth_pattern(mock_answer_context)
        assert result == "jwt"

    def test_auto_detect_session_for_web_app(self, mock_answer_context):
        """Test detects session for web apps"""
        mock_answer_context.answers["project_purpose"] = ["web_app"]
        result = _auto_detect_auth_pattern(mock_answer_context)
        assert result == "session"

    def test_auto_detect_jwt_default(self, mock_answer_context):
        """Test detects JWT as default"""
        mock_answer_context.answers["project_purpose"] = ["cli"]
        result = _auto_detect_auth_pattern(mock_answer_context)
        assert result == "jwt"


class TestApiDocsToolDetection:
    """Test API docs tool auto-detection"""

    def test_auto_detect_openapi_for_fastapi(self, mock_answer_context):
        """Test detects OpenAPI for FastAPI"""
        mock_answer_context.system.existing_tools = ["fastapi"]
        result = _auto_detect_api_docs_tool(mock_answer_context)
        assert result == "openapi"

    def test_auto_detect_graphql_schema_for_graphql(self, mock_answer_context):
        """Test detects GraphQL schema for GraphQL"""
        mock_answer_context.system.existing_tools = ["graphql"]
        result = _auto_detect_api_docs_tool(mock_answer_context)
        assert result == "graphql_schema"

    def test_auto_detect_openapi_default(self, mock_answer_context):
        """Test detects OpenAPI as default"""
        mock_answer_context.system.existing_tools = []
        result = _auto_detect_api_docs_tool(mock_answer_context)
        assert result == "openapi"


class TestCodeReviewRequirementsDetection:
    """Test code review requirements auto-detection"""

    def test_auto_detect_none_for_solo(self, mock_answer_context):
        """Test detects none for solo developers"""
        mock_answer_context.answers["team_dynamics"] = "solo"
        result = _auto_detect_code_review_requirements(mock_answer_context)
        assert result == "none"

    def test_auto_detect_optional_for_small_team(self, mock_answer_context):
        """Test detects optional for small teams"""
        mock_answer_context.answers["team_dynamics"] = "small_team"
        result = _auto_detect_code_review_requirements(mock_answer_context)
        assert result == "optional"

    def test_auto_detect_required_one_for_growing_team(self, mock_answer_context):
        """Test detects required_one for growing teams"""
        mock_answer_context.answers["team_dynamics"] = "growing_team"
        result = _auto_detect_code_review_requirements(mock_answer_context)
        assert result == "required_one"

    def test_auto_detect_required_two_for_large_org(self, mock_answer_context):
        """Test detects required_two for large organizations"""
        mock_answer_context.answers["team_dynamics"] = "large_org"
        result = _auto_detect_code_review_requirements(mock_answer_context)
        assert result == "required_two"


class TestAIHintGenerators:
    """Test AI hint generation functions"""

    @patch("claudecodeoptimizer.wizard.decision_tree._context_matrix")
    def test_generate_testing_hint(self, mock_matrix, mock_answer_context):
        """Test generates testing approach hint"""
        mock_matrix.recommend_testing_approach.return_value = {
            "approach": "balanced",
            "coverage_target": "70-85%",
            "reason": "Good balance for production projects",
        }
        hint = _generate_testing_hint(mock_answer_context)
        assert "Recommended" in hint
        assert "balanced" in hint

    @patch("claudecodeoptimizer.wizard.decision_tree._context_matrix")
    def test_generate_git_workflow_hint(self, mock_matrix, mock_answer_context):
        """Test generates git workflow hint"""
        mock_matrix.recommend_git_workflow.return_value = {
            "workflow": "github_flow",
            "reason": "Good for small teams",
            "alternatives": {"main_only": "Simpler for solo"},
        }
        hint = _generate_git_workflow_hint(mock_answer_context)
        assert "Recommended" in hint
        assert "github_flow" in hint

    @patch("claudecodeoptimizer.wizard.decision_tree._context_matrix")
    def test_generate_versioning_hint(self, mock_matrix, mock_answer_context):
        """Test generates versioning strategy hint"""
        mock_matrix.recommend_versioning_strategy.return_value = {
            "strategy": "auto_semver",
            "reason": "Zero overhead for solo devs",
            "alternatives": {},
        }
        hint = _generate_versioning_hint(mock_answer_context)
        assert "Recommended" in hint
        assert "auto_semver" in hint

    def test_generate_ci_provider_hint_with_ci(self, mock_answer_context):
        """Test generates CI provider hint when CI exists"""
        mock_answer_context.system.has_ci = True
        hint = _generate_ci_provider_hint(mock_answer_context)
        assert "CI/CD already detected" in hint

    def test_generate_ci_provider_hint_without_ci(self, mock_answer_context):
        """Test generates CI provider hint without CI"""
        mock_answer_context.system.has_ci = False
        mock_answer_context.system.is_git_repo = True
        hint = _generate_ci_provider_hint(mock_answer_context)
        assert "GitHub Actions" in hint

    def test_generate_secrets_management_hint_solo(self, mock_answer_context):
        """Test generates secrets management hint for solo"""
        mock_answer_context.answers["team_dynamics"] = "solo"
        mock_answer_context.answers["project_maturity"] = "mvp"
        hint = _generate_secrets_management_hint(mock_answer_context)
        assert ".env" in hint

    def test_generate_error_handling_hint_quality_first(self, mock_answer_context):
        """Test generates error handling hint for quality-first"""
        mock_answer_context.answers["development_philosophy"] = "quality_first"
        hint = _generate_error_handling_hint(mock_answer_context)
        assert "Fail-Fast" in hint

    @patch("claudecodeoptimizer.wizard.decision_tree._context_matrix")
    def test_generate_precommit_hooks_hint(self, mock_matrix, mock_answer_context):
        """Test generates pre-commit hooks hint"""
        mock_matrix.recommend_precommit_hooks.return_value = ["format", "lint"]
        hint = _generate_precommit_hooks_hint(mock_answer_context)
        assert "Recommended" in hint
        assert "format" in hint

    def test_generate_logging_level_hint_prototype(self, mock_answer_context):
        """Test generates logging level hint for prototype"""
        mock_answer_context.answers["project_maturity"] = "prototype"
        hint = _generate_logging_level_hint(mock_answer_context)
        assert "DEBUG" in hint


class TestDynamicTier3Builder:
    """Test dynamic TIER 3 decision builder"""

    def test_build_tier3_includes_static_decisions(self, mock_answer_context):
        """Test TIER 3 includes static decisions"""
        decisions = build_tier3_tool_decisions(mock_answer_context)
        ids = [dp.id for dp in decisions]
        assert "precommit_hooks" in ids
        assert "logging_level" in ids
        assert "branch_naming_convention" in ids

    def test_build_tier3_includes_auth_for_api(self, mock_answer_context):
        """Test TIER 3 includes auth pattern for API projects"""
        mock_answer_context.answers["project_purpose"] = ["api_service"]
        decisions = build_tier3_tool_decisions(mock_answer_context)
        ids = [dp.id for dp in decisions]
        assert "auth_pattern" in ids

    def test_build_tier3_excludes_auth_for_cli(self, mock_answer_context):
        """Test TIER 3 excludes auth pattern for CLI tools"""
        mock_answer_context.answers["project_purpose"] = ["cli"]
        decisions = build_tier3_tool_decisions(mock_answer_context)
        ids = [dp.id for dp in decisions]
        assert "auth_pattern" not in ids

    def test_build_tier3_includes_code_review_for_team(self, mock_answer_context):
        """Test TIER 3 includes code review for team projects"""
        mock_answer_context.answers["team_dynamics"] = "small-2-5"
        decisions = build_tier3_tool_decisions(mock_answer_context)
        ids = [dp.id for dp in decisions]
        assert "code_review_requirements" in ids

    @patch("claudecodeoptimizer.wizard.decision_tree.ToolComparator")
    def test_build_tier3_includes_tool_conflicts(self, mock_comparator, mock_answer_context):
        """Test TIER 3 includes tool conflict decisions"""
        # Mock tool conflict
        mock_conflict = Mock()
        mock_conflict.category = "formatter"
        mock_conflict.tools = ["black", "ruff"]
        mock_conflict.recommended = "ruff"

        mock_instance = Mock()
        mock_instance.find_all_conflicts.return_value = [mock_conflict]
        mock_instance.get_tool_description.return_value = "Tool description"
        mock_comparator.return_value = mock_instance

        decisions = build_tier3_tool_decisions(mock_answer_context)
        ids = [dp.id for dp in decisions]
        assert "tool_preference_formatter" in ids


class TestGetDecisionsFunctions:
    """Test get_all_decisions and get_decisions_by_tier functions"""

    def test_get_all_decisions_includes_all_tiers(self, mock_answer_context):
        """Test get_all_decisions includes all three tiers"""
        decisions = get_all_decisions(mock_answer_context)
        assert len(decisions) > len(DECISION_TREE_TIER1) + len(DECISION_TREE_TIER2)

    def test_get_all_decisions_correct_order(self, mock_answer_context):
        """Test get_all_decisions returns in tier order"""
        decisions = get_all_decisions(mock_answer_context)
        # First decisions should be tier 1
        for i in range(len(DECISION_TREE_TIER1)):
            assert decisions[i].tier == 1
        # Next should be tier 2
        for i in range(len(DECISION_TREE_TIER1), len(DECISION_TREE_TIER1) + len(DECISION_TREE_TIER2)):
            assert decisions[i].tier == 2

    def test_get_decisions_by_tier_1(self, mock_answer_context):
        """Test get_decisions_by_tier returns TIER 1 decisions"""
        decisions = get_decisions_by_tier(1, mock_answer_context)
        assert len(decisions) == len(DECISION_TREE_TIER1)
        assert all(dp.tier == 1 for dp in decisions)

    def test_get_decisions_by_tier_2(self, mock_answer_context):
        """Test get_decisions_by_tier returns TIER 2 decisions"""
        decisions = get_decisions_by_tier(2, mock_answer_context)
        assert len(decisions) == len(DECISION_TREE_TIER2)
        assert all(dp.tier == 2 for dp in decisions)

    def test_get_decisions_by_tier_3_requires_context(self):
        """Test get_decisions_by_tier requires context for TIER 3"""
        with pytest.raises(ValueError, match="Context required"):
            get_decisions_by_tier(3, None)

    def test_get_decisions_by_tier_3_returns_tier3(self, mock_answer_context):
        """Test get_decisions_by_tier returns TIER 3 decisions"""
        decisions = get_decisions_by_tier(3, mock_answer_context)
        assert len(decisions) > 0
        assert all(dp.tier == 3 for dp in decisions)

    def test_get_decisions_by_tier_invalid_tier(self, mock_answer_context):
        """Test get_decisions_by_tier returns empty for invalid tier"""
        decisions = get_decisions_by_tier(99, mock_answer_context)
        assert decisions == []


class TestValidationFunctions:
    """Test validation functions"""

    def test_validate_project_purpose_accepts_list(self):
        """Test project purpose validator accepts list"""
        assert _validate_project_purpose(["backend", "api_service"]) is True

    def test_validate_project_purpose_accepts_string(self):
        """Test project purpose validator accepts string"""
        assert _validate_project_purpose("backend") is True

    def test_validate_project_purpose_accepts_list_of_strings(self):
        """Test project purpose validator validates list contents"""
        assert _validate_project_purpose(["backend", "microservice"]) is True

    def test_validate_project_purpose_rejects_invalid_list(self):
        """Test project purpose validator rejects non-string list items"""
        assert _validate_project_purpose([123, 456]) is False

    def test_validate_project_purpose_handles_exception(self):
        """Test project purpose validator handles exceptions gracefully"""
        # Test with None
        assert _validate_project_purpose(None) is True


class TestGitWorkflowAutoDetection:
    """Test git workflow auto-detection"""

    def test_git_workflow_auto_detection_solo(self, mock_answer_context):
        """Test git workflow auto-detection for solo developers"""
        from claudecodeoptimizer.wizard.decision_tree import _auto_detect_git_workflow

        mock_answer_context.answers["team_dynamics"] = "solo"
        result = _auto_detect_git_workflow(mock_answer_context)
        assert result == "main_only"

    def test_git_workflow_auto_detection_small_team(self, mock_answer_context):
        """Test git workflow auto-detection for small teams"""
        from claudecodeoptimizer.wizard.decision_tree import _auto_detect_git_workflow

        mock_answer_context.answers["team_dynamics"] = "small_team"
        mock_answer_context.answers["project_maturity"] = "mvp"
        result = _auto_detect_git_workflow(mock_answer_context)
        assert result == "github_flow"

    def test_git_workflow_auto_detection_large_org(self, mock_answer_context):
        """Test git workflow auto-detection for large organizations"""
        from claudecodeoptimizer.wizard.decision_tree import _auto_detect_git_workflow

        mock_answer_context.answers["team_dynamics"] = "large_org"
        result = _auto_detect_git_workflow(mock_answer_context)
        assert result == "git_flow"


class TestEdgeCases:
    """Test edge cases and error handling"""

    def test_auto_detect_with_empty_context(self, mock_system_context):
        """Test auto-detection with empty answer context"""
        ctx = AnswerContext(system=mock_system_context, answers={})

        # Should not crash, should return defaults
        assert _auto_detect_team_size(ctx) is not None
        assert _auto_detect_maturity(ctx) is not None

    def test_should_ask_with_missing_answers(self, mock_system_context):
        """Test conditional logic with missing answers"""
        ctx = AnswerContext(system=mock_system_context, answers={})

        # Should handle missing answers gracefully
        result = _should_ask_auth_pattern(ctx)
        assert isinstance(result, bool)

    def test_hint_generation_with_missing_answers(self, mock_system_context):
        """Test hint generation with missing required answers"""
        ctx = AnswerContext(system=mock_system_context, answers={})

        # Should return empty string or handle gracefully
        hint = _generate_testing_hint(ctx)
        assert isinstance(hint, str)

    def test_versioning_strategy_with_non_list_project_types(self, mock_answer_context):
        """Test versioning strategy handles non-list project types"""
        mock_answer_context.answers["project_purpose"] = "backend"  # String instead of list
        result = _auto_detect_versioning_strategy(mock_answer_context)
        assert result in ["auto_semver", "manual_semver", "pr_based_semver", "no_versioning", "calver"]
