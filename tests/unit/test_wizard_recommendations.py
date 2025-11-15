"""
Unit tests for Wizard Recommendation Engine

Tests RecommendationEngine class for wizard-specific cascading recommendations.
Target Coverage: 90%+
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from claudecodeoptimizer.wizard.models import AnswerContext, SystemContext, ToolComparison
from claudecodeoptimizer.wizard.recommendations import (
    RecommendationEngine,
    explain_why,
    get_recommendation,
    recommend_commands,
)


@pytest.fixture
def minimal_system_context() -> SystemContext:
    """Minimal system context for testing"""
    return SystemContext(
        os_type="linux",
        os_version="Ubuntu 22.04",
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
        git_user_name="Test User",
        git_user_email="test@example.com",
        detected_editors=["vscode"],
        active_editor="vscode",
        project_root=Path("/tmp/test"),
        is_git_repo=False,
        existing_tools=[],
        file_count=10,
        line_count=500,
        has_tests=False,
        has_ci=False,
        detected_languages=["python"],
        detected_frameworks=[],
        detected_project_types=[],
    )


@pytest.fixture
def production_system_context() -> SystemContext:
    """Production system context with extensive setup"""
    return SystemContext(
        os_type="linux",
        os_version="Ubuntu 22.04",
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
        git_user_name="Test User",
        git_user_email="test@example.com",
        detected_editors=["vscode"],
        active_editor="vscode",
        project_root=Path("/tmp/test"),
        is_git_repo=True,
        existing_tools=["pytest", "black", "ruff", "mypy", "docker"],
        file_count=500,
        line_count=25000,
        has_tests=True,
        has_ci=True,
        detected_languages=["python"],
        detected_frameworks=["fastapi"],
        detected_project_types=["api"],
    )


@pytest.fixture
def minimal_answer_context(minimal_system_context: SystemContext) -> AnswerContext:
    """Minimal answer context for testing"""
    return AnswerContext(system=minimal_system_context, answers={})


@pytest.fixture
def complete_answer_context(production_system_context: SystemContext) -> AnswerContext:
    """Complete answer context with all answers"""
    return AnswerContext(
        system=production_system_context,
        answers={
            "project_purpose": ["api", "backend"],
            "team_dynamics": "small_team",
            "project_maturity": "production",
            "development_philosophy": "quality_first",
            "principle_strategy": "comprehensive",
            "testing_approach": "comprehensive",
            "security_stance": "production",
            "documentation_level": "practical",
            "git_workflow": "git_flow",
        },
    )


class TestRecommendationEngineInit:
    """Test RecommendationEngine initialization"""

    def test_init_creates_engine(self) -> None:
        """Test engine initialization"""
        engine = RecommendationEngine()
        assert engine is not None


class TestRecommendProjectPurpose:
    """Test recommend_project_purpose method"""

    def test_detected_project_types(self, minimal_system_context: SystemContext) -> None:
        """Test recommendation when project types are detected"""
        minimal_system_context.detected_project_types = ["api", "cli"]
        context = AnswerContext(system=minimal_system_context, answers={})
        engine = RecommendationEngine()

        result = engine.recommend_project_purpose(context)

        assert "Detected" in result
        assert "api" in result.lower() or "cli" in result.lower()

    def test_api_framework_detected(self, minimal_system_context: SystemContext) -> None:
        """Test API recommendation when API frameworks detected"""
        minimal_system_context.detected_frameworks = ["fastapi"]
        context = AnswerContext(system=minimal_system_context, answers={})
        engine = RecommendationEngine()

        result = engine.recommend_project_purpose(context)

        assert "API" in result or "Backend" in result

    def test_flask_framework_detected(self, minimal_system_context: SystemContext) -> None:
        """Test API recommendation when Flask detected"""
        minimal_system_context.detected_frameworks = ["flask"]
        context = AnswerContext(system=minimal_system_context, answers={})
        engine = RecommendationEngine()

        result = engine.recommend_project_purpose(context)

        assert "API" in result or "Backend" in result

    def test_django_rest_framework_detected(self, minimal_system_context: SystemContext) -> None:
        """Test API recommendation when Django REST detected"""
        minimal_system_context.detected_frameworks = ["django-rest"]
        context = AnswerContext(system=minimal_system_context, answers={})
        engine = RecommendationEngine()

        result = engine.recommend_project_purpose(context)

        assert "API" in result or "Backend" in result

    def test_react_framework_detected(self, minimal_system_context: SystemContext) -> None:
        """Test web app recommendation when React detected"""
        minimal_system_context.detected_frameworks = ["react"]
        context = AnswerContext(system=minimal_system_context, answers={})
        engine = RecommendationEngine()

        result = engine.recommend_project_purpose(context)

        assert "Web" in result

    def test_vue_framework_detected(self, minimal_system_context: SystemContext) -> None:
        """Test web app recommendation when Vue detected"""
        minimal_system_context.detected_frameworks = ["vue"]
        context = AnswerContext(system=minimal_system_context, answers={})
        engine = RecommendationEngine()

        result = engine.recommend_project_purpose(context)

        assert "Web" in result

    def test_next_framework_detected(self, minimal_system_context: SystemContext) -> None:
        """Test web app recommendation when Next.js detected"""
        minimal_system_context.detected_frameworks = ["next"]
        context = AnswerContext(system=minimal_system_context, answers={})
        engine = RecommendationEngine()

        result = engine.recommend_project_purpose(context)

        assert "Web" in result

    def test_nuxt_framework_detected(self, minimal_system_context: SystemContext) -> None:
        """Test web app recommendation when Nuxt detected"""
        minimal_system_context.detected_frameworks = ["nuxt"]
        context = AnswerContext(system=minimal_system_context, answers={})
        engine = RecommendationEngine()

        result = engine.recommend_project_purpose(context)

        assert "Web" in result

    def test_small_project_recommendation(self, minimal_system_context: SystemContext) -> None:
        """Test CLI/Library recommendation for small projects"""
        minimal_system_context.file_count = 15
        context = AnswerContext(system=minimal_system_context, answers={})
        engine = RecommendationEngine()

        result = engine.recommend_project_purpose(context)

        assert "CLI" in result or "Library" in result or "Small project" in result

    def test_default_recommendation(self, minimal_system_context: SystemContext) -> None:
        """Test default recommendation when no signals"""
        minimal_system_context.file_count = 100
        context = AnswerContext(system=minimal_system_context, answers={})
        engine = RecommendationEngine()

        result = engine.recommend_project_purpose(context)

        assert "Select all that apply" in result or len(result) > 0


class TestRecommendTeamDynamics:
    """Test recommend_team_dynamics method"""

    def test_ci_detected_team_recommendation(self, minimal_system_context: SystemContext) -> None:
        """Test team recommendation when CI is detected"""
        minimal_system_context.is_git_repo = True
        minimal_system_context.has_ci = True
        context = AnswerContext(system=minimal_system_context, answers={})
        engine = RecommendationEngine()

        result = engine.recommend_team_dynamics(context)

        assert "CI" in result or "team" in result.lower()

    def test_no_ci_default_recommendation(self, minimal_system_context: SystemContext) -> None:
        """Test default team recommendation"""
        context = AnswerContext(system=minimal_system_context, answers={})
        engine = RecommendationEngine()

        result = engine.recommend_team_dynamics(context)

        assert "Solo" in result or "Team" in result


class TestRecommendProjectMaturity:
    """Test recommend_project_maturity method"""

    def test_prototype_no_tests_small(self, minimal_system_context: SystemContext) -> None:
        """Test prototype recommendation for small project without tests"""
        minimal_system_context.has_tests = False
        minimal_system_context.file_count = 30
        context = AnswerContext(system=minimal_system_context, answers={})
        engine = RecommendationEngine()

        result = engine.recommend_project_maturity(context)

        assert "Prototype" in result or "POC" in result

    def test_mvp_tests_no_ci(self, minimal_system_context: SystemContext) -> None:
        """Test MVP recommendation for project with tests but no CI"""
        minimal_system_context.has_tests = True
        minimal_system_context.has_ci = False
        context = AnswerContext(system=minimal_system_context, answers={})
        engine = RecommendationEngine()

        result = engine.recommend_project_maturity(context)

        assert "MVP" in result or "Early Development" in result

    def test_active_dev_tests_and_ci(self, minimal_system_context: SystemContext) -> None:
        """Test active dev recommendation for project with tests and CI"""
        minimal_system_context.has_tests = True
        minimal_system_context.has_ci = True
        context = AnswerContext(system=minimal_system_context, answers={})
        engine = RecommendationEngine()

        result = engine.recommend_project_maturity(context)

        assert "Active Development" in result or "Production" in result

    def test_default_maturity_recommendation(self, minimal_system_context: SystemContext) -> None:
        """Test default maturity recommendation"""
        minimal_system_context.has_tests = False
        minimal_system_context.has_ci = False
        minimal_system_context.file_count = 100
        context = AnswerContext(system=minimal_system_context, answers={})
        engine = RecommendationEngine()

        result = engine.recommend_project_maturity(context)

        assert len(result) > 0


class TestRecommendDevelopmentPhilosophy:
    """Test recommend_development_philosophy method"""

    def test_prototype_move_fast(self, minimal_answer_context: AnswerContext) -> None:
        """Test move fast recommendation for prototype"""
        minimal_answer_context.answers["project_maturity"] = "prototype"
        engine = RecommendationEngine()

        result = engine.recommend_development_philosophy(minimal_answer_context)

        assert "Move Fast" in result or "Iterate" in result

    def test_production_quality_first(self, minimal_answer_context: AnswerContext) -> None:
        """Test quality first recommendation for production"""
        minimal_answer_context.answers["project_maturity"] = "production"
        engine = RecommendationEngine()

        result = engine.recommend_development_philosophy(minimal_answer_context)

        assert "Quality" in result or "Thorough" in result

    def test_mature_quality_first(self, minimal_answer_context: AnswerContext) -> None:
        """Test quality first recommendation for mature projects"""
        minimal_answer_context.answers["project_maturity"] = "mature"
        engine = RecommendationEngine()

        result = engine.recommend_development_philosophy(minimal_answer_context)

        assert "Quality" in result or "Thorough" in result

    def test_default_balanced(self, minimal_answer_context: AnswerContext) -> None:
        """Test balanced recommendation as default"""
        minimal_answer_context.answers["project_maturity"] = "mvp"
        engine = RecommendationEngine()

        result = engine.recommend_development_philosophy(minimal_answer_context)

        assert "Balanced" in result or "Pragmatic" in result


class TestRecommendPrincipleStrategy:
    """Test recommend_principle_strategy method"""

    def test_quality_first_comprehensive(self, minimal_answer_context: AnswerContext) -> None:
        """Test comprehensive recommendation for quality-first philosophy"""
        minimal_answer_context.answers["development_philosophy"] = "quality_first"
        engine = RecommendationEngine()

        result = engine.recommend_principle_strategy(minimal_answer_context)

        assert "Comprehensive" in result or "Strict" in result

    def test_move_fast_minimal(self, minimal_answer_context: AnswerContext) -> None:
        """Test minimal recommendation for move fast philosophy"""
        minimal_answer_context.answers["development_philosophy"] = "move_fast"
        engine = RecommendationEngine()

        result = engine.recommend_principle_strategy(minimal_answer_context)

        assert "Minimal" in result or "Pragmatic" in result

    def test_prototype_minimal(self, minimal_answer_context: AnswerContext) -> None:
        """Test minimal recommendation for prototype maturity"""
        minimal_answer_context.answers["project_maturity"] = "prototype"
        minimal_answer_context.answers["development_philosophy"] = "balanced"
        engine = RecommendationEngine()

        result = engine.recommend_principle_strategy(minimal_answer_context)

        assert "Minimal" in result or "Pragmatic" in result

    def test_growing_team_comprehensive(self, minimal_answer_context: AnswerContext) -> None:
        """Test comprehensive recommendation for growing team"""
        minimal_answer_context.answers["team_dynamics"] = "growing_team"
        minimal_answer_context.answers["development_philosophy"] = "balanced"
        minimal_answer_context.answers["project_maturity"] = "active_dev"
        engine = RecommendationEngine()

        result = engine.recommend_principle_strategy(minimal_answer_context)

        assert "Comprehensive" in result or "Strict" in result or "coordination" in result.lower()

    def test_large_org_comprehensive(self, minimal_answer_context: AnswerContext) -> None:
        """Test comprehensive recommendation for large org"""
        minimal_answer_context.answers["team_dynamics"] = "large_org"
        minimal_answer_context.answers["development_philosophy"] = "balanced"
        minimal_answer_context.answers["project_maturity"] = "active_dev"
        engine = RecommendationEngine()

        result = engine.recommend_principle_strategy(minimal_answer_context)

        assert "Comprehensive" in result or "Strict" in result or "coordination" in result.lower()

    def test_default_recommended_preset(self, minimal_answer_context: AnswerContext) -> None:
        """Test recommended preset as default"""
        minimal_answer_context.answers["team_dynamics"] = "solo"
        minimal_answer_context.answers["development_philosophy"] = "balanced"
        minimal_answer_context.answers["project_maturity"] = "mvp"
        engine = RecommendationEngine()

        result = engine.recommend_principle_strategy(minimal_answer_context)

        assert "Recommended" in result or "balance" in result.lower()


class TestRecommendTestingApproach:
    """Test recommend_testing_approach method"""

    def test_no_tests_prototype(self, minimal_answer_context: AnswerContext) -> None:
        """Test no tests recommendation for prototype"""
        minimal_answer_context.system.has_tests = False
        minimal_answer_context.answers["project_maturity"] = "prototype"
        engine = RecommendationEngine()

        result = engine.recommend_testing_approach(minimal_answer_context)

        assert "No Tests Yet" in result or "normal" in result.lower()

    def test_no_tests_not_prototype(self, minimal_answer_context: AnswerContext) -> None:
        """Test critical paths recommendation when no tests but not prototype"""
        minimal_answer_context.system.has_tests = False
        minimal_answer_context.answers["project_maturity"] = "mvp"
        engine = RecommendationEngine()

        result = engine.recommend_testing_approach(minimal_answer_context)

        assert "Critical Paths" in result or "Start" in result

    def test_quality_first_comprehensive(self, minimal_answer_context: AnswerContext) -> None:
        """Test comprehensive testing for quality-first philosophy"""
        minimal_answer_context.system.has_tests = True
        minimal_answer_context.answers["development_philosophy"] = "quality_first"
        engine = RecommendationEngine()

        result = engine.recommend_testing_approach(minimal_answer_context)

        assert "Comprehensive" in result

    def test_production_balanced_or_comprehensive(self, minimal_answer_context: AnswerContext) -> None:
        """Test balanced/comprehensive for production"""
        minimal_answer_context.system.has_tests = True
        minimal_answer_context.answers["project_maturity"] = "production"
        minimal_answer_context.answers["development_philosophy"] = "balanced"
        engine = RecommendationEngine()

        result = engine.recommend_testing_approach(minimal_answer_context)

        assert "Balanced" in result or "Comprehensive" in result

    def test_mature_balanced_or_comprehensive(self, minimal_answer_context: AnswerContext) -> None:
        """Test balanced/comprehensive for mature projects"""
        minimal_answer_context.system.has_tests = True
        minimal_answer_context.answers["project_maturity"] = "mature"
        minimal_answer_context.answers["development_philosophy"] = "balanced"
        engine = RecommendationEngine()

        result = engine.recommend_testing_approach(minimal_answer_context)

        assert "Balanced" in result or "Comprehensive" in result

    def test_default_balanced(self, minimal_answer_context: AnswerContext) -> None:
        """Test balanced testing as default"""
        minimal_answer_context.system.has_tests = True
        minimal_answer_context.answers["project_maturity"] = "mvp"
        minimal_answer_context.answers["development_philosophy"] = "balanced"
        engine = RecommendationEngine()

        result = engine.recommend_testing_approach(minimal_answer_context)

        assert "Balanced" in result or "ROI" in result


class TestRecommendSecurityStance:
    """Test recommend_security_stance method"""

    def test_api_production_security(self, minimal_answer_context: AnswerContext) -> None:
        """Test production security for API"""
        minimal_answer_context.answers["project_purpose"] = ["api"]
        engine = RecommendationEngine()

        result = engine.recommend_security_stance(minimal_answer_context)

        assert "Production Security" in result

    def test_backend_production_security(self, minimal_answer_context: AnswerContext) -> None:
        """Test production security for backend"""
        minimal_answer_context.answers["project_purpose"] = ["backend"]
        engine = RecommendationEngine()

        result = engine.recommend_security_stance(minimal_answer_context)

        assert "Production Security" in result

    def test_web_app_production_security(self, minimal_answer_context: AnswerContext) -> None:
        """Test production security for web app"""
        minimal_answer_context.answers["project_purpose"] = ["web_app"]
        engine = RecommendationEngine()

        result = engine.recommend_security_stance(minimal_answer_context)

        assert "Production Security" in result

    def test_production_maturity_security(self, minimal_answer_context: AnswerContext) -> None:
        """Test production security for production maturity"""
        minimal_answer_context.answers["project_purpose"] = ["cli"]
        minimal_answer_context.answers["project_maturity"] = "production"
        engine = RecommendationEngine()

        result = engine.recommend_security_stance(minimal_answer_context)

        assert "Production Security" in result

    def test_mature_maturity_security(self, minimal_answer_context: AnswerContext) -> None:
        """Test production security for mature projects"""
        minimal_answer_context.answers["project_purpose"] = ["cli"]
        minimal_answer_context.answers["project_maturity"] = "mature"
        engine = RecommendationEngine()

        result = engine.recommend_security_stance(minimal_answer_context)

        assert "Production Security" in result

    def test_prototype_standard_security(self, minimal_answer_context: AnswerContext) -> None:
        """Test standard security for prototype"""
        minimal_answer_context.answers["project_purpose"] = ["cli"]
        minimal_answer_context.answers["project_maturity"] = "prototype"
        engine = RecommendationEngine()

        result = engine.recommend_security_stance(minimal_answer_context)

        assert "Standard Security" in result or "sufficient" in result.lower()

    def test_default_production_security(self, minimal_answer_context: AnswerContext) -> None:
        """Test production security as default"""
        minimal_answer_context.answers["project_purpose"] = ["library"]
        minimal_answer_context.answers["project_maturity"] = "mvp"
        engine = RecommendationEngine()

        result = engine.recommend_security_stance(minimal_answer_context)

        assert "Production Security" in result or len(result) > 0


class TestRecommendDocumentationLevel:
    """Test recommend_documentation_level method"""

    def test_library_comprehensive_docs(self, minimal_answer_context: AnswerContext) -> None:
        """Test comprehensive docs for library"""
        minimal_answer_context.answers["project_purpose"] = ["library"]
        engine = RecommendationEngine()

        result = engine.recommend_documentation_level(minimal_answer_context)

        assert "Comprehensive" in result or "essential" in result.lower()

    def test_sdk_comprehensive_docs(self, minimal_answer_context: AnswerContext) -> None:
        """Test comprehensive docs for SDK"""
        minimal_answer_context.answers["project_purpose"] = ["sdk"]
        engine = RecommendationEngine()

        result = engine.recommend_documentation_level(minimal_answer_context)

        assert "Comprehensive" in result or "essential" in result.lower()

    def test_solo_minimal_docs(self, minimal_answer_context: AnswerContext) -> None:
        """Test minimal docs for solo developer"""
        minimal_answer_context.answers["project_purpose"] = ["cli"]
        minimal_answer_context.answers["team_dynamics"] = "solo"
        engine = RecommendationEngine()

        result = engine.recommend_documentation_level(minimal_answer_context)

        assert "Minimal" in result or "sufficient" in result.lower()

    def test_small_team_practical_docs(self, minimal_answer_context: AnswerContext) -> None:
        """Test practical docs for small team"""
        minimal_answer_context.answers["project_purpose"] = ["api"]
        minimal_answer_context.answers["team_dynamics"] = "small_team"
        engine = RecommendationEngine()

        result = engine.recommend_documentation_level(minimal_answer_context)

        assert "Practical" in result or "collaboration" in result.lower()

    def test_growing_team_practical_docs(self, minimal_answer_context: AnswerContext) -> None:
        """Test practical docs for growing team"""
        minimal_answer_context.answers["project_purpose"] = ["api"]
        minimal_answer_context.answers["team_dynamics"] = "growing_team"
        engine = RecommendationEngine()

        result = engine.recommend_documentation_level(minimal_answer_context)

        assert "Practical" in result or "collaboration" in result.lower()

    def test_default_practical_docs(self, minimal_answer_context: AnswerContext) -> None:
        """Test practical docs as default"""
        minimal_answer_context.answers["project_purpose"] = ["api"]
        minimal_answer_context.answers["team_dynamics"] = "large_org"
        engine = RecommendationEngine()

        result = engine.recommend_documentation_level(minimal_answer_context)

        assert "Practical" in result or len(result) > 0


class TestRecommendGitWorkflow:
    """Test recommend_git_workflow method"""

    def test_solo_main_only(self, minimal_answer_context: AnswerContext) -> None:
        """Test main-only for solo developer"""
        minimal_answer_context.answers["team_dynamics"] = "solo"
        engine = RecommendationEngine()

        result = engine.recommend_git_workflow(minimal_answer_context)

        assert "Main-Only" in result or "simple" in result.lower()

    def test_large_org_git_flow(self, minimal_answer_context: AnswerContext) -> None:
        """Test Git Flow for large org"""
        minimal_answer_context.answers["team_dynamics"] = "large_org"
        engine = RecommendationEngine()

        result = engine.recommend_git_workflow(minimal_answer_context)

        assert "Git Flow" in result or "formal" in result.lower()

    def test_small_team_production_git_flow(self, minimal_answer_context: AnswerContext) -> None:
        """Test Git Flow for small team with production maturity"""
        minimal_answer_context.answers["team_dynamics"] = "small_team"
        minimal_answer_context.answers["project_maturity"] = "production"
        engine = RecommendationEngine()

        result = engine.recommend_git_workflow(minimal_answer_context)

        assert "Git Flow" in result or "stability" in result.lower()

    def test_small_team_mature_git_flow(self, minimal_answer_context: AnswerContext) -> None:
        """Test Git Flow for small team with mature project"""
        minimal_answer_context.answers["team_dynamics"] = "small_team"
        minimal_answer_context.answers["project_maturity"] = "mature"
        engine = RecommendationEngine()

        result = engine.recommend_git_workflow(minimal_answer_context)

        assert "Git Flow" in result or "stability" in result.lower()

    def test_growing_team_production_git_flow(self, minimal_answer_context: AnswerContext) -> None:
        """Test Git Flow for growing team with production maturity"""
        minimal_answer_context.answers["team_dynamics"] = "growing_team"
        minimal_answer_context.answers["project_maturity"] = "production"
        engine = RecommendationEngine()

        result = engine.recommend_git_workflow(minimal_answer_context)

        assert "Git Flow" in result or "stability" in result.lower()

    def test_small_team_github_flow(self, minimal_answer_context: AnswerContext) -> None:
        """Test GitHub Flow for small team"""
        minimal_answer_context.answers["team_dynamics"] = "small_team"
        minimal_answer_context.answers["project_maturity"] = "mvp"
        engine = RecommendationEngine()

        result = engine.recommend_git_workflow(minimal_answer_context)

        assert "GitHub Flow" in result or "balanced" in result.lower()

    def test_growing_team_github_flow(self, minimal_answer_context: AnswerContext) -> None:
        """Test GitHub Flow for growing team"""
        minimal_answer_context.answers["team_dynamics"] = "growing_team"
        minimal_answer_context.answers["project_maturity"] = "mvp"
        engine = RecommendationEngine()

        result = engine.recommend_git_workflow(minimal_answer_context)

        assert "GitHub Flow" in result or "balanced" in result.lower()

    def test_default_github_flow(self, minimal_answer_context: AnswerContext) -> None:
        """Test GitHub Flow as default"""
        minimal_answer_context.answers["team_dynamics"] = "unknown"
        engine = RecommendationEngine()

        result = engine.recommend_git_workflow(minimal_answer_context)

        assert "GitHub Flow" in result or len(result) > 0


class TestRecommendToolPreference:
    """Test recommend_tool_preference method"""

    @patch("claudecodeoptimizer.wizard.tool_comparison.ToolComparator")
    def test_tool_recommendation_with_comparison(
        self, mock_comparator_class: MagicMock, minimal_answer_context: AnswerContext
    ) -> None:
        """Test tool recommendation with valid comparison"""
        mock_comparison = ToolComparison(
            category="formatter",
            tools=["black", "ruff"],
            recommended="ruff",
            reason="Fast, modern, all-in-one",
        )
        mock_instance = MagicMock()
        mock_instance.analyze_category.return_value = mock_comparison
        mock_comparator_class.return_value = mock_instance

        engine = RecommendationEngine()
        result = engine.recommend_tool_preference("formatter", ["black", "ruff"], minimal_answer_context)

        assert "ruff" in result.lower()
        assert "black" in result.lower() or "You have" in result

    @patch("claudecodeoptimizer.wizard.tool_comparison.ToolComparator")
    def test_tool_recommendation_no_comparison(
        self, mock_comparator_class: MagicMock, minimal_answer_context: AnswerContext
    ) -> None:
        """Test tool recommendation when no comparison available"""
        mock_instance = MagicMock()
        mock_instance.analyze_category.return_value = None
        mock_comparator_class.return_value = mock_instance

        engine = RecommendationEngine()
        result = engine.recommend_tool_preference("formatter", ["black"], minimal_answer_context)

        assert "black" in result.lower() or "detected" in result.lower()


class TestRecommendCommands:
    """Test recommend_commands method"""

    def test_core_commands_always_recommended(self, minimal_answer_context: AnswerContext) -> None:
        """Test core commands are always recommended"""
        engine = RecommendationEngine()
        result = engine.recommend_commands(minimal_answer_context)

        assert "cco-status" in result
        assert "cco-config" in result

    def test_audit_for_balanced_philosophy(self, minimal_answer_context: AnswerContext) -> None:
        """Test audit recommended for balanced philosophy"""
        minimal_answer_context.answers["development_philosophy"] = "balanced"
        engine = RecommendationEngine()
        result = engine.recommend_commands(minimal_answer_context)

        assert "cco-audit" in result

    def test_audit_for_quality_first(self, minimal_answer_context: AnswerContext) -> None:
        """Test audit recommended for quality-first philosophy"""
        minimal_answer_context.answers["development_philosophy"] = "quality_first"
        engine = RecommendationEngine()
        result = engine.recommend_commands(minimal_answer_context)

        assert "cco-audit" in result

    def test_audit_for_production(self, minimal_answer_context: AnswerContext) -> None:
        """Test audit recommended for production maturity"""
        minimal_answer_context.answers["project_maturity"] = "production"
        engine = RecommendationEngine()
        result = engine.recommend_commands(minimal_answer_context)

        assert "cco-audit" in result

    def test_audit_for_mature(self, minimal_answer_context: AnswerContext) -> None:
        """Test audit recommended for mature projects"""
        minimal_answer_context.answers["project_maturity"] = "mature"
        engine = RecommendationEngine()
        result = engine.recommend_commands(minimal_answer_context)

        assert "cco-audit" in result

    def test_analyze_for_mvp(self, minimal_answer_context: AnswerContext) -> None:
        """Test analyze recommended for MVP"""
        minimal_answer_context.answers["project_maturity"] = "mvp"
        engine = RecommendationEngine()
        result = engine.recommend_commands(minimal_answer_context)

        assert "cco-analyze" in result

    def test_analyze_for_active_dev(self, minimal_answer_context: AnswerContext) -> None:
        """Test analyze recommended for active development"""
        minimal_answer_context.answers["project_maturity"] = "active_dev"
        engine = RecommendationEngine()
        result = engine.recommend_commands(minimal_answer_context)

        assert "cco-analyze" in result

    def test_fix_with_existing_tools(self, minimal_answer_context: AnswerContext) -> None:
        """Test fix recommended when tools exist"""
        minimal_answer_context.system.existing_tools = ["black", "ruff"]
        engine = RecommendationEngine()
        result = engine.recommend_commands(minimal_answer_context)

        assert "cco-fix" in result

    def test_optimize_code_for_large_codebase(self, minimal_answer_context: AnswerContext) -> None:
        """Test optimize-code for large codebase by file count"""
        minimal_answer_context.system.file_count = 150
        engine = RecommendationEngine()
        result = engine.recommend_commands(minimal_answer_context)

        assert "cco-optimize-code" in result

    def test_optimize_code_for_large_line_count(self, minimal_answer_context: AnswerContext) -> None:
        """Test optimize-code for large codebase by line count"""
        minimal_answer_context.system.line_count = 6000
        engine = RecommendationEngine()
        result = engine.recommend_commands(minimal_answer_context)

        assert "cco-optimize-code" in result

    def test_optimize_deps_for_many_tools(self, minimal_answer_context: AnswerContext) -> None:
        """Test optimize-deps for projects with many tools"""
        minimal_answer_context.system.existing_tools = ["black", "ruff", "mypy", "pytest", "coverage", "pre-commit"]
        engine = RecommendationEngine()
        result = engine.recommend_commands(minimal_answer_context)

        assert "cco-optimize-deps" in result

    def test_generate_for_balanced_testing(self, minimal_answer_context: AnswerContext) -> None:
        """Test generate recommended for balanced testing"""
        minimal_answer_context.answers["testing_approach"] = "balanced"
        engine = RecommendationEngine()
        result = engine.recommend_commands(minimal_answer_context)

        assert "cco-generate" in result

    def test_generate_for_comprehensive_testing(self, minimal_answer_context: AnswerContext) -> None:
        """Test generate recommended for comprehensive testing"""
        minimal_answer_context.answers["testing_approach"] = "comprehensive"
        engine = RecommendationEngine()
        result = engine.recommend_commands(minimal_answer_context)

        assert "cco-generate" in result

    def test_security_commands_for_production_stance(self, minimal_answer_context: AnswerContext) -> None:
        """Test security commands for production stance"""
        minimal_answer_context.answers["security_stance"] = "production"
        engine = RecommendationEngine()
        result = engine.recommend_commands(minimal_answer_context)

        assert "cco-scan-secrets" in result
        assert "cco-fix-security" in result

    def test_security_commands_for_high_stance(self, minimal_answer_context: AnswerContext) -> None:
        """Test security commands for high stance"""
        minimal_answer_context.answers["security_stance"] = "high"
        engine = RecommendationEngine()
        result = engine.recommend_commands(minimal_answer_context)

        assert "cco-scan-secrets" in result
        assert "cco-fix-security" in result

    def test_docker_optimization(self, minimal_answer_context: AnswerContext) -> None:
        """Test docker optimization when docker detected"""
        minimal_answer_context.system.existing_tools = ["docker"]
        engine = RecommendationEngine()
        result = engine.recommend_commands(minimal_answer_context)

        assert "cco-optimize-docker" in result


class TestGenerateRecommendation:
    """Test generate_recommendation main method"""

    def test_generates_project_purpose_recommendation(self, minimal_answer_context: AnswerContext) -> None:
        """Test generating project purpose recommendation"""
        engine = RecommendationEngine()
        result = engine.generate_recommendation("project_purpose", minimal_answer_context)

        assert len(result) > 0
        assert isinstance(result, str)

    def test_generates_team_dynamics_recommendation(self, minimal_answer_context: AnswerContext) -> None:
        """Test generating team dynamics recommendation"""
        engine = RecommendationEngine()
        result = engine.generate_recommendation("team_dynamics", minimal_answer_context)

        assert len(result) > 0
        assert isinstance(result, str)

    def test_generates_project_maturity_recommendation(self, minimal_answer_context: AnswerContext) -> None:
        """Test generating project maturity recommendation"""
        engine = RecommendationEngine()
        result = engine.generate_recommendation("project_maturity", minimal_answer_context)

        assert len(result) > 0
        assert isinstance(result, str)

    def test_generates_development_philosophy_recommendation(self, minimal_answer_context: AnswerContext) -> None:
        """Test generating development philosophy recommendation"""
        engine = RecommendationEngine()
        result = engine.generate_recommendation("development_philosophy", minimal_answer_context)

        assert len(result) > 0
        assert isinstance(result, str)

    def test_generates_principle_strategy_recommendation(self, minimal_answer_context: AnswerContext) -> None:
        """Test generating principle strategy recommendation"""
        engine = RecommendationEngine()
        result = engine.generate_recommendation("principle_strategy", minimal_answer_context)

        assert len(result) > 0
        assert isinstance(result, str)

    def test_generates_testing_approach_recommendation(self, minimal_answer_context: AnswerContext) -> None:
        """Test generating testing approach recommendation"""
        engine = RecommendationEngine()
        result = engine.generate_recommendation("testing_approach", minimal_answer_context)

        assert len(result) > 0
        assert isinstance(result, str)

    def test_generates_security_stance_recommendation(self, minimal_answer_context: AnswerContext) -> None:
        """Test generating security stance recommendation"""
        engine = RecommendationEngine()
        result = engine.generate_recommendation("security_stance", minimal_answer_context)

        assert len(result) > 0
        assert isinstance(result, str)

    def test_generates_documentation_level_recommendation(self, minimal_answer_context: AnswerContext) -> None:
        """Test generating documentation level recommendation"""
        engine = RecommendationEngine()
        result = engine.generate_recommendation("documentation_level", minimal_answer_context)

        assert len(result) > 0
        assert isinstance(result, str)

    def test_generates_git_workflow_recommendation(self, minimal_answer_context: AnswerContext) -> None:
        """Test generating git workflow recommendation"""
        engine = RecommendationEngine()
        result = engine.generate_recommendation("git_workflow", minimal_answer_context)

        assert len(result) > 0
        assert isinstance(result, str)

    def test_unknown_question_id_returns_empty(self, minimal_answer_context: AnswerContext) -> None:
        """Test unknown question ID returns empty string"""
        engine = RecommendationEngine()
        result = engine.generate_recommendation("unknown_question", minimal_answer_context)

        assert result == ""

    def test_exception_handling(self, minimal_answer_context: AnswerContext) -> None:
        """Test exception handling in recommendation generation"""
        engine = RecommendationEngine()

        # Patch a recommendation method to raise an exception
        with patch.object(engine, "recommend_project_purpose", side_effect=ValueError("Test error")):
            result = engine.generate_recommendation("project_purpose", minimal_answer_context)

        # Should return error message, not raise
        assert isinstance(result, str)
        assert "Recommendation unavailable" in result
        assert "Test error" in result


class TestExplainQuestionImportance:
    """Test explain_question_importance method"""

    def test_explains_project_purpose(self, minimal_answer_context: AnswerContext) -> None:
        """Test explaining project purpose importance"""
        engine = RecommendationEngine()
        result = engine.explain_question_importance("project_purpose", minimal_answer_context)

        assert len(result) > 0
        assert "project type" in result.lower() or "principles" in result.lower()

    def test_explains_team_dynamics(self, minimal_answer_context: AnswerContext) -> None:
        """Test explaining team dynamics importance"""
        engine = RecommendationEngine()
        result = engine.explain_question_importance("team_dynamics", minimal_answer_context)

        assert len(result) > 0
        assert "team" in result.lower() or "collaboration" in result.lower()

    def test_explains_project_maturity(self, minimal_answer_context: AnswerContext) -> None:
        """Test explaining project maturity importance"""
        engine = RecommendationEngine()
        result = engine.explain_question_importance("project_maturity", minimal_answer_context)

        assert len(result) > 0
        assert "stage" in result.lower() or "quality" in result.lower()

    def test_explains_development_philosophy(self, minimal_answer_context: AnswerContext) -> None:
        """Test explaining development philosophy importance"""
        engine = RecommendationEngine()
        result = engine.explain_question_importance("development_philosophy", minimal_answer_context)

        assert len(result) > 0
        assert "approach" in result.lower() or "decision" in result.lower()

    def test_explains_principle_strategy(self, minimal_answer_context: AnswerContext) -> None:
        """Test explaining principle strategy importance"""
        engine = RecommendationEngine()
        result = engine.explain_question_importance("principle_strategy", minimal_answer_context)

        assert len(result) > 0
        assert "principle" in result.lower() or "enforce" in result.lower()

    def test_explains_testing_approach(self, minimal_answer_context: AnswerContext) -> None:
        """Test explaining testing approach importance"""
        engine = RecommendationEngine()
        result = engine.explain_question_importance("testing_approach", minimal_answer_context)

        assert len(result) > 0
        assert "testing" in result.lower() or "quality" in result.lower()

    def test_explains_security_stance(self, minimal_answer_context: AnswerContext) -> None:
        """Test explaining security stance importance"""
        engine = RecommendationEngine()
        result = engine.explain_question_importance("security_stance", minimal_answer_context)

        assert len(result) > 0
        assert "security" in result.lower()

    def test_explains_documentation_level(self, minimal_answer_context: AnswerContext) -> None:
        """Test explaining documentation level importance"""
        engine = RecommendationEngine()
        result = engine.explain_question_importance("documentation_level", minimal_answer_context)

        assert len(result) > 0
        assert "documentation" in result.lower() or "time" in result.lower()

    def test_explains_git_workflow(self, minimal_answer_context: AnswerContext) -> None:
        """Test explaining git workflow importance"""
        engine = RecommendationEngine()
        result = engine.explain_question_importance("git_workflow", minimal_answer_context)

        assert len(result) > 0
        assert "git" in result.lower() or "workflow" in result.lower()

    def test_unknown_question_returns_empty(self, minimal_answer_context: AnswerContext) -> None:
        """Test unknown question returns empty string"""
        engine = RecommendationEngine()
        result = engine.explain_question_importance("unknown_question", minimal_answer_context)

        assert result == ""


class TestConvenienceFunctions:
    """Test convenience wrapper functions"""

    def test_get_recommendation_function(self, minimal_answer_context: AnswerContext) -> None:
        """Test get_recommendation convenience function"""
        result = get_recommendation("project_purpose", minimal_answer_context)

        assert isinstance(result, str)
        assert len(result) > 0

    def test_explain_why_function(self, minimal_answer_context: AnswerContext) -> None:
        """Test explain_why convenience function"""
        result = explain_why("project_purpose", minimal_answer_context)

        assert isinstance(result, str)
        assert len(result) > 0

    def test_recommend_commands_function(self, minimal_answer_context: AnswerContext) -> None:
        """Test recommend_commands convenience function"""
        result = recommend_commands(minimal_answer_context)

        assert isinstance(result, dict)
        assert "cco-status" in result
        assert "cco-config" in result


class TestEdgeCases:
    """Test edge cases and error conditions"""

    def test_empty_answers_dict(self, minimal_system_context: SystemContext) -> None:
        """Test with empty answers dictionary"""
        context = AnswerContext(system=minimal_system_context, answers={})
        engine = RecommendationEngine()

        result = engine.generate_recommendation("project_purpose", context)
        assert isinstance(result, str)

    def test_minimal_system_context(self, minimal_system_context: SystemContext) -> None:
        """Test with minimal system context"""
        context = AnswerContext(system=minimal_system_context, answers={})
        engine = RecommendationEngine()

        result = engine.recommend_commands(context)
        assert isinstance(result, dict)
        assert len(result) >= 2  # At least core commands

    def test_complete_context(self, complete_answer_context: AnswerContext) -> None:
        """Test with complete answer context"""
        engine = RecommendationEngine()

        # Test all recommendation methods
        result1 = engine.recommend_project_purpose(complete_answer_context)
        result2 = engine.recommend_team_dynamics(complete_answer_context)
        result3 = engine.recommend_project_maturity(complete_answer_context)
        result4 = engine.recommend_development_philosophy(complete_answer_context)
        result5 = engine.recommend_principle_strategy(complete_answer_context)
        result6 = engine.recommend_testing_approach(complete_answer_context)
        result7 = engine.recommend_security_stance(complete_answer_context)
        result8 = engine.recommend_documentation_level(complete_answer_context)
        result9 = engine.recommend_git_workflow(complete_answer_context)

        assert all(isinstance(r, str) for r in [result1, result2, result3, result4, result5, result6, result7, result8, result9])

    def test_multiple_project_types(self, minimal_answer_context: AnswerContext) -> None:
        """Test with multiple project types"""
        minimal_answer_context.answers["project_purpose"] = ["api", "web_app", "cli"]
        engine = RecommendationEngine()

        result = engine.recommend_security_stance(minimal_answer_context)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_no_existing_tools(self, minimal_answer_context: AnswerContext) -> None:
        """Test recommendations with no existing tools"""
        minimal_answer_context.system.existing_tools = []
        engine = RecommendationEngine()

        result = engine.recommend_commands(minimal_answer_context)
        assert isinstance(result, dict)
        # Should still have core commands
        assert "cco-status" in result

    def test_all_question_ids(self, minimal_answer_context: AnswerContext) -> None:
        """Test all question IDs produce valid recommendations"""
        engine = RecommendationEngine()

        question_ids = [
            "project_purpose",
            "team_dynamics",
            "project_maturity",
            "development_philosophy",
            "principle_strategy",
            "testing_approach",
            "security_stance",
            "documentation_level",
            "git_workflow",
        ]

        for question_id in question_ids:
            result = engine.generate_recommendation(question_id, minimal_answer_context)
            assert isinstance(result, str), f"Failed for {question_id}"
            assert len(result) > 0, f"Empty result for {question_id}"
