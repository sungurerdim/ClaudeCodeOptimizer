"""
Comprehensive tests for wizard questions module.

Tests cover:
- Conditional question display logic (should_ask_question)
- AI hint generators for all categories
- Default value generators
- Question filtering based on answers
- Question counting
- All edge cases and error conditions
"""

from typing import Any, Dict

import pytest

from claudecodeoptimizer.wizard.questions import (
    QUESTIONS,
    count_questions_for_answers,
    default_deployment_target,
    default_frameworks,
    default_infrastructure,
    default_maturity,
    default_primary_language,
    default_project_types,
    default_scale,
    default_secondary_languages,
    get_compliance_hint,
    get_deployment_hint,
    get_filtered_questions,
    get_framework_hint,
    get_infrastructure_hint,
    get_language_hint,
    get_linting_hint,
    get_maturity_hint,
    get_monitoring_hint,
    get_project_type_hint,
    get_scale_hint,
    get_security_stance_hint,
    get_team_size_hint,
    get_testing_coverage_hint,
    get_type_coverage_hint,
    no_hint,
    should_ask_question,
)

# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def empty_report() -> Dict[str, Any]:
    """Empty detection report"""
    return {}


@pytest.fixture
def minimal_report() -> Dict[str, Any]:
    """Minimal detection report with basic data"""
    return {
        "project_root": "/path/to/project",
        "project_types": [],
        "languages": [],
        "frameworks": [],
        "tools": [],
        "codebase_patterns": {
            "total_files": 10,
            "has_tests": False,
            "has_ci_cd": False,
        },
    }


@pytest.fixture
def comprehensive_report() -> Dict[str, Any]:
    """Comprehensive detection report with all data"""
    return {
        "project_root": "/path/to/my-awesome-project",
        "project_types": [
            {"detected_value": "api"},
            {"detected_value": "backend"},
        ],
        "languages": [
            {"detected_value": "python"},
            {"detected_value": "javascript"},
            {"detected_value": "typescript"},
        ],
        "frameworks": [
            {"detected_value": "fastapi"},
            {"detected_value": "react"},
        ],
        "tools": [
            {"detected_value": "docker"},
            {"detected_value": "kubernetes"},
            {"detected_value": "pytest"},
            {"detected_value": "mypy"},
            {"detected_value": "ruff"},
            {"detected_value": "coverage"},
            {"detected_value": "vault"},
            {"detected_value": "prometheus"},
            {"detected_value": "grafana"},
        ],
        "codebase_patterns": {
            "total_files": 1500,
            "has_tests": True,
            "has_ci_cd": True,
        },
    }


@pytest.fixture
def empty_answers() -> Dict[str, Any]:
    """Empty answers dict"""
    return {}


@pytest.fixture
def solo_dev_answers() -> Dict[str, Any]:
    """Answers for solo developer"""
    return {
        "team_trajectory": "solo",
    }


@pytest.fixture
def team_answers() -> Dict[str, Any]:
    """Answers for team development"""
    return {
        "team_trajectory": "small-team-growing",
    }


# ============================================================================
# TEST should_ask_question - Team Questions
# ============================================================================


class TestShouldAskQuestionTeam:
    """Test conditional logic for team-related questions"""

    def test_skip_team_questions_for_solo_dev(self, solo_dev_answers):
        """Team questions should be skipped for solo developers"""
        team_questions = [
            "code_review_strictness",
            "pair_programming",
            "pr_size_limit",
            "code_ownership",
            "git_workflow",
            "commit_convention",
        ]

        for question_id in team_questions:
            assert should_ask_question(question_id, solo_dev_answers) is False

    def test_ask_team_questions_for_teams(self, team_answers):
        """Team questions should be asked for teams"""
        team_questions = [
            "code_review_strictness",
            "pair_programming",
            "pr_size_limit",
            "code_ownership",
            "git_workflow",
            "commit_convention",
        ]

        for question_id in team_questions:
            assert should_ask_question(question_id, team_answers) is True

    def test_ask_team_questions_when_no_team_info(self, empty_answers):
        """Team questions should be skipped when team info is missing (defaults to solo)"""
        # Default is "solo" so team questions are skipped
        assert should_ask_question("code_review_strictness", empty_answers) is False
        assert should_ask_question("pair_programming", empty_answers) is False


# ============================================================================
# TEST should_ask_question - Testing Questions
# ============================================================================


class TestShouldAskQuestionTesting:
    """Test conditional logic for testing-related questions"""

    def test_skip_advanced_testing_when_no_coverage(self):
        """Advanced testing questions should be skipped when coverage is none"""
        no_test_scenarios = [
            {"coverage_target": "none"},
            {"coverage_target": "not-set"},
            {"coverage_target": "0"},
        ]

        for answers in no_test_scenarios:
            assert should_ask_question("mutation_testing", answers) is False
            assert should_ask_question("property_based_testing", answers) is False
            assert should_ask_question("test_pyramid_ratio", answers) is False

    def test_ask_advanced_testing_when_has_coverage(self):
        """Advanced testing questions should be asked when coverage exists"""
        test_scenarios = [
            {"coverage_target": "90"},
            {"coverage_target": "80"},
            {"coverage_target": "100"},
        ]

        for answers in test_scenarios:
            assert should_ask_question("mutation_testing", answers) is True
            assert should_ask_question("property_based_testing", answers) is True
            assert should_ask_question("test_pyramid_ratio", answers) is True

    def test_ask_advanced_testing_when_no_coverage_info(self, empty_answers):
        """Advanced testing questions should be asked by default"""
        assert should_ask_question("mutation_testing", empty_answers) is True
        assert should_ask_question("property_based_testing", empty_answers) is True


# ============================================================================
# TEST should_ask_question - Type Coverage
# ============================================================================


class TestShouldAskQuestionTypeChecker:
    """Test conditional logic for type coverage questions"""

    def test_ask_type_coverage_for_dynamic_languages(self):
        """Type coverage should be asked for languages with optional typing"""
        dynamic_languages = ["javascript", "python", "ruby", "php"]

        for lang in dynamic_languages:
            answers = {"primary_language": lang}
            assert should_ask_question("type_coverage_target", answers) is True

    def test_ask_type_coverage_for_static_languages(self):
        """Type coverage should be asked for statically typed languages"""
        static_languages = ["java", "c", "c++", "rust", "go", "typescript"]

        for lang in static_languages:
            answers = {"primary_language": lang}
            assert should_ask_question("type_coverage_target", answers) is True

    def test_ask_type_coverage_for_unknown_language(self):
        """Type coverage should be asked for unknown languages"""
        answers = {"primary_language": "brainfuck"}
        assert should_ask_question("type_coverage_target", answers) is True

    def test_ask_type_coverage_when_no_language_info(self, empty_answers):
        """Type coverage should be asked when language is unknown"""
        assert should_ask_question("type_coverage_target", empty_answers) is True


# ============================================================================
# TEST should_ask_question - CI/CD Questions
# ============================================================================


class TestShouldAskQuestionCICD:
    """Test conditional logic for CI/CD questions"""

    def test_skip_deployment_questions_for_manual_cicd(self):
        """Deployment questions should be skipped for manual CI/CD"""
        answers = {"ci_cd_trigger": "manual"}
        assert should_ask_question("deployment_frequency", answers) is False
        assert should_ask_question("rollback_strategy", answers) is False

    def test_ask_deployment_questions_for_automated_cicd(self):
        """Deployment questions should be asked for automated CI/CD"""
        automated_scenarios = [
            {"ci_cd_trigger": "every-pr"},
            {"ci_cd_trigger": "every-commit"},
        ]

        for answers in automated_scenarios:
            assert should_ask_question("deployment_frequency", answers) is True
            assert should_ask_question("rollback_strategy", answers) is True

    def test_ask_deployment_questions_when_no_cicd_info(self, empty_answers):
        """Deployment questions should be asked when CI/CD info is missing"""
        assert should_ask_question("deployment_frequency", empty_answers) is True
        assert should_ask_question("rollback_strategy", empty_answers) is True


# ============================================================================
# TEST should_ask_question - Infrastructure Questions
# ============================================================================


class TestShouldAskQuestionInfrastructure:
    """Test conditional logic for infrastructure questions"""

    def test_ask_monitoring_for_all_infrastructures(self):
        """Monitoring should be asked regardless of infrastructure"""
        scenarios = [
            {"infrastructure": []},
            {"infrastructure": ["bare-metal"]},
            {"infrastructure": ["kubernetes"]},
            {"infrastructure": ["docker-compose"]},
        ]

        for answers in scenarios:
            assert should_ask_question("monitoring", answers) is True

    def test_ask_monitoring_when_no_infra_info(self, empty_answers):
        """Monitoring should be asked when infrastructure is unknown"""
        assert should_ask_question("monitoring", empty_answers) is True


# ============================================================================
# TEST should_ask_question - Compliance Questions
# ============================================================================


class TestShouldAskQuestionCompliance:
    """Test conditional logic for compliance questions"""

    def test_ask_audit_logging_for_no_compliance(self):
        """Audit logging should still be asked even without compliance"""
        scenarios = [
            {"compliance_requirements": ["none"]},
            {"compliance_requirements": []},
        ]

        for answers in scenarios:
            assert should_ask_question("audit_logging", answers) is True

    def test_ask_audit_logging_with_compliance(self):
        """Audit logging should be asked with compliance requirements"""
        answers = {"compliance_requirements": ["gdpr", "hipaa"]}
        assert should_ask_question("audit_logging", answers) is True


# ============================================================================
# TEST should_ask_question - Documentation Questions
# ============================================================================


class TestShouldAskQuestionDocumentation:
    """Test conditional logic for documentation questions"""

    def test_skip_architecture_diagrams_for_minimal_docs(self):
        """Architecture diagrams should be skipped for minimal documentation"""
        answers = {"verbosity": "minimal"}
        assert should_ask_question("architecture_diagrams", answers) is False

    def test_ask_architecture_diagrams_for_other_verbosity(self):
        """Architecture diagrams should be asked for other verbosity levels"""
        scenarios = [
            {"verbosity": "concise"},
            {"verbosity": "detailed"},
            {"verbosity": "comprehensive"},
        ]

        for answers in scenarios:
            assert should_ask_question("architecture_diagrams", answers) is True

    def test_skip_api_docs_for_non_api_projects(self):
        """API documentation should be skipped for non-API projects"""
        non_api_scenarios = [
            {"types": ["cli"]},
            {"types": ["library"]},
            {"types": ["frontend"]},
            {"types": []},
        ]

        for answers in non_api_scenarios:
            assert should_ask_question("api_documentation", answers) is False

    def test_ask_api_docs_for_api_projects(self):
        """API documentation should be asked for API projects"""
        api_scenarios = [
            {"types": ["api"]},
            {"types": ["backend"]},
            {"types": ["microservice"]},
            {"types": ["api", "backend"]},
        ]

        for answers in api_scenarios:
            assert should_ask_question("api_documentation", answers) is True


# ============================================================================
# TEST should_ask_question - Default Behavior
# ============================================================================


class TestShouldAskQuestionDefault:
    """Test default behavior for questions without conditions"""

    def test_ask_by_default_for_unknown_questions(self, empty_answers):
        """Unknown questions should be asked by default"""
        assert should_ask_question("some_random_question", empty_answers) is True
        assert should_ask_question("another_question", empty_answers) is True

    def test_ask_by_default_for_unconditioned_questions(self, empty_answers):
        """Questions without skip conditions should always be asked"""
        assert should_ask_question("linting_strictness", empty_answers) is True
        assert should_ask_question("security_stance", empty_answers) is True


# ============================================================================
# TEST AI Hint Generators - Project Identity
# ============================================================================


class TestProjectIdentityHints:
    """Test AI hint generators for project identity category"""

    def test_project_type_hint_with_detected_types(self, comprehensive_report):
        """Project type hint should show detected types"""
        hint = get_project_type_hint(comprehensive_report)
        assert "Detected:" in hint
        assert "api" in hint
        assert "backend" in hint

    def test_project_type_hint_no_detection(self, minimal_report):
        """Project type hint should handle no detection"""
        hint = get_project_type_hint(minimal_report)
        assert "No project types auto-detected" in hint

    def test_language_hint_with_detection(self, comprehensive_report):
        """Language hint should show primary language"""
        hint = get_language_hint(comprehensive_report)
        assert "Detected:" in hint
        assert "python" in hint

    def test_language_hint_no_detection(self, minimal_report):
        """Language hint should handle no detection"""
        hint = get_language_hint(minimal_report)
        assert "No languages auto-detected" in hint

    def test_framework_hint_with_detection(self, comprehensive_report):
        """Framework hint should show detected frameworks"""
        hint = get_framework_hint(comprehensive_report)
        assert "Detected:" in hint
        assert "fastapi" in hint
        assert "react" in hint

    def test_framework_hint_no_detection(self, minimal_report):
        """Framework hint should handle no detection"""
        hint = get_framework_hint(minimal_report)
        assert "No frameworks detected" in hint

    def test_deployment_hint_with_docker(self, comprehensive_report):
        """Deployment hint should detect Docker/K8s"""
        hint = get_deployment_hint(comprehensive_report)
        assert "Docker" in hint or "K8s" in hint

    def test_deployment_hint_no_docker(self, minimal_report):
        """Deployment hint should handle no Docker"""
        hint = get_deployment_hint(minimal_report)
        assert "Inferred from tooling" in hint

    def test_scale_hint_large_codebase(self, comprehensive_report):
        """Scale hint should detect large codebase"""
        hint = get_scale_hint(comprehensive_report)
        assert "codebase" in hint.lower()

    def test_scale_hint_small_codebase(self, minimal_report):
        """Scale hint should detect small codebase"""
        hint = get_scale_hint(minimal_report)
        assert "Small" in hint or "hobby" in hint or "startup" in hint

    def test_scale_hint_medium_codebase(self):
        """Scale hint should detect medium codebase"""
        from claudecodeoptimizer.core.constants import MEDIUM_CODEBASE_THRESHOLD

        report = {"codebase_patterns": {"total_files": MEDIUM_CODEBASE_THRESHOLD + 1}}
        hint = get_scale_hint(report)
        assert "Medium codebase" in hint or "growth" in hint

    def test_scale_hint_small_but_above_threshold(self):
        """Scale hint should detect small but above threshold codebase"""
        from claudecodeoptimizer.core.constants import SMALL_CODEBASE_THRESHOLD

        report = {"codebase_patterns": {"total_files": SMALL_CODEBASE_THRESHOLD + 1}}
        hint = get_scale_hint(report)
        assert "Small codebase" in hint or "startup" in hint

    def test_compliance_hint_with_security_tools(self, comprehensive_report):
        """Compliance hint should detect security tools"""
        hint = get_compliance_hint(comprehensive_report)
        assert "Security tools detected" in hint

    def test_compliance_hint_no_security_tools(self, minimal_report):
        """Compliance hint should handle no security tools"""
        hint = get_compliance_hint(minimal_report)
        assert "No compliance indicators detected" in hint

    def test_maturity_hint_with_tests_and_ci(self, comprehensive_report):
        """Maturity hint should detect tests and CI"""
        hint = get_maturity_hint(comprehensive_report)
        assert "Tests and CI detected" in hint or "mature" in hint

    def test_maturity_hint_no_tests_or_ci(self, minimal_report):
        """Maturity hint should handle no tests or CI"""
        hint = get_maturity_hint(minimal_report)
        assert "early stage" in hint or "Minimal" in hint

    def test_maturity_hint_tests_only(self):
        """Maturity hint should detect tests without CI"""
        report = {
            "codebase_patterns": {
                "has_tests": True,
                "has_ci_cd": False,
            }
        }
        hint = get_maturity_hint(report)
        assert "Some infrastructure detected" in hint or "active development" in hint

    def test_maturity_hint_ci_only(self):
        """Maturity hint should detect CI without tests"""
        report = {
            "codebase_patterns": {
                "has_tests": False,
                "has_ci_cd": True,
            }
        }
        hint = get_maturity_hint(report)
        assert "Some infrastructure detected" in hint or "active development" in hint

    def test_team_size_hint(self, comprehensive_report):
        """Team size hint should indicate unable to detect"""
        hint = get_team_size_hint(comprehensive_report)
        assert "Unable to detect" in hint or "select based on" in hint


# ============================================================================
# TEST AI Hint Generators - Code Quality
# ============================================================================


class TestCodeQualityHints:
    """Test AI hint generators for code quality category"""

    def test_linting_hint_with_linters(self, comprehensive_report):
        """Linting hint should detect linters"""
        hint = get_linting_hint(comprehensive_report)
        assert "Detected:" in hint
        assert "ruff" in hint

    def test_linting_hint_no_linters(self, minimal_report):
        """Linting hint should handle no linters"""
        hint = get_linting_hint(minimal_report)
        assert "No linters detected" in hint

    def test_type_coverage_hint_typescript(self):
        """Type coverage hint should recommend 100% for type-safe languages"""
        report = {
            "languages": [{"detected_value": "typescript"}],
            "tools": [],
        }
        hint = get_type_coverage_hint(report)
        assert "100%" in hint or "Type-safe" in hint

    def test_type_coverage_hint_python_with_mypy(self, comprehensive_report):
        """Type coverage hint should detect type checker"""
        hint = get_type_coverage_hint(comprehensive_report)
        assert "mypy" in hint or "Type checker detected" in hint

    def test_type_coverage_hint_default(self, minimal_report):
        """Type coverage hint should provide default recommendation"""
        hint = get_type_coverage_hint(minimal_report)
        assert "80-90%" in hint or "Recommend" in hint


# ============================================================================
# TEST AI Hint Generators - Testing & Security
# ============================================================================


class TestTestingSecurityHints:
    """Test AI hint generators for testing and security"""

    def test_testing_coverage_hint_with_coverage_tool(self, comprehensive_report):
        """Testing coverage hint should detect coverage tools"""
        hint = get_testing_coverage_hint(comprehensive_report)
        assert "Coverage tool detected" in hint or "90%" in hint

    def test_testing_coverage_hint_no_coverage_tool(self, minimal_report):
        """Testing coverage hint should provide default"""
        hint = get_testing_coverage_hint(minimal_report)
        assert "80-90%" in hint or "Recommend" in hint

    def test_security_stance_hint_with_security_tools(self, comprehensive_report):
        """Security stance hint should detect security tools"""
        hint = get_security_stance_hint(comprehensive_report)
        assert "Security tools detected" in hint or "paranoid" in hint

    def test_security_stance_hint_no_security_tools(self, minimal_report):
        """Security stance hint should provide default"""
        hint = get_security_stance_hint(minimal_report)
        assert "balanced" in hint or "Recommend" in hint


# ============================================================================
# TEST AI Hint Generators - Infrastructure
# ============================================================================


class TestInfrastructureHints:
    """Test AI hint generators for infrastructure"""

    def test_infrastructure_hint_kubernetes(self, comprehensive_report):
        """Infrastructure hint should detect Kubernetes"""
        hint = get_infrastructure_hint(comprehensive_report)
        assert "Kubernetes detected" in hint or "kubernetes" in hint

    def test_infrastructure_hint_docker_only(self):
        """Infrastructure hint should detect Docker"""
        report = {
            "tools": [{"detected_value": "docker"}],
        }
        hint = get_infrastructure_hint(report)
        assert "Docker detected" in hint

    def test_infrastructure_hint_none(self, minimal_report):
        """Infrastructure hint should handle no containerization"""
        hint = get_infrastructure_hint(minimal_report)
        assert "No containerization detected" in hint

    def test_monitoring_hint_with_tools(self, comprehensive_report):
        """Monitoring hint should detect monitoring tools"""
        hint = get_monitoring_hint(comprehensive_report)
        assert "Detected:" in hint
        assert "prometheus" in hint or "grafana" in hint

    def test_monitoring_hint_no_tools(self, minimal_report):
        """Monitoring hint should handle no monitoring tools"""
        hint = get_monitoring_hint(minimal_report)
        assert "No monitoring tools detected" in hint


# ============================================================================
# TEST AI Hint Generators - No Hint
# ============================================================================


class TestNoHint:
    """Test no_hint function"""

    def test_no_hint_returns_empty_string(self, comprehensive_report):
        """no_hint should always return empty string"""
        assert no_hint(comprehensive_report) == ""
        assert no_hint({}) == ""
        assert no_hint({"random": "data"}) == ""


# ============================================================================
# TEST Default Value Generators
# ============================================================================


class TestDefaultValueGenerators:
    """Test default value generators"""

    def test_default_project_types_with_detection(self, comprehensive_report):
        """Should return detected project types"""
        result = default_project_types(comprehensive_report)
        assert result == ["api", "backend"]

    def test_default_project_types_no_detection(self, minimal_report):
        """Should return default backend when no detection"""
        result = default_project_types(minimal_report)
        assert result == ["backend"]

    def test_default_primary_language_with_detection(self, comprehensive_report):
        """Should return first detected language"""
        result = default_primary_language(comprehensive_report)
        assert result == "python"

    def test_default_primary_language_no_detection(self, minimal_report):
        """Should return default python when no detection"""
        result = default_primary_language(minimal_report)
        assert result == "python"

    def test_default_secondary_languages_with_detection(self, comprehensive_report):
        """Should return 2nd and 3rd detected languages"""
        result = default_secondary_languages(comprehensive_report)
        assert result == ["javascript", "typescript"]

    def test_default_secondary_languages_no_detection(self, minimal_report):
        """Should return empty list when no detection"""
        result = default_secondary_languages(minimal_report)
        assert result == []

    def test_default_frameworks_with_detection(self, comprehensive_report):
        """Should return detected frameworks"""
        result = default_frameworks(comprehensive_report)
        assert result == ["fastapi", "react"]

    def test_default_frameworks_no_detection(self, minimal_report):
        """Should return empty list when no detection"""
        result = default_frameworks(minimal_report)
        assert result == []

    def test_default_deployment_target_kubernetes(self, comprehensive_report):
        """Should return kubernetes when detected"""
        result = default_deployment_target(comprehensive_report)
        assert result == ["kubernetes"]

    def test_default_deployment_target_docker(self):
        """Should return docker when detected (no kubernetes)"""
        report = {
            "tools": [{"detected_value": "docker"}],
        }
        result = default_deployment_target(report)
        assert result == ["docker"]

    def test_default_deployment_target_none(self, minimal_report):
        """Should return cloud-other when no detection"""
        result = default_deployment_target(minimal_report)
        assert result == ["cloud-other"]

    def test_default_scale_large_codebase(self, comprehensive_report):
        """Should return enterprise for large codebase"""
        result = default_scale(comprehensive_report)
        assert result == "enterprise"

    def test_default_scale_small_codebase(self, minimal_report):
        """Should return startup for small codebase"""
        result = default_scale(minimal_report)
        assert result == "startup"

    def test_default_maturity_with_tests_and_ci(self, comprehensive_report):
        """Should return active-dev when tests and CI detected"""
        result = default_maturity(comprehensive_report)
        assert result == "active-dev"

    def test_default_maturity_no_tests_or_ci(self, minimal_report):
        """Should return greenfield when no tests or CI"""
        result = default_maturity(minimal_report)
        assert result == "greenfield"

    def test_default_maturity_tests_only(self):
        """Should return active-dev when only tests detected"""
        report = {
            "codebase_patterns": {
                "has_tests": True,
                "has_ci_cd": False,
            }
        }
        result = default_maturity(report)
        assert result == "active-dev"

    def test_default_maturity_ci_only(self):
        """Should return active-dev when only CI detected"""
        report = {
            "codebase_patterns": {
                "has_tests": False,
                "has_ci_cd": True,
            }
        }
        result = default_maturity(report)
        assert result == "active-dev"

    def test_default_infrastructure_kubernetes(self, comprehensive_report):
        """Should detect kubernetes and docker-compose"""
        result = default_infrastructure(comprehensive_report)
        assert "kubernetes" in result
        assert "docker-compose" in result

    def test_default_infrastructure_docker_only(self):
        """Should detect docker-compose when only docker found"""
        report = {
            "tools": [{"detected_value": "docker"}],
        }
        result = default_infrastructure(report)
        assert result == ["docker-compose"]

    def test_default_infrastructure_none(self, minimal_report):
        """Should return docker-compose as default"""
        result = default_infrastructure(minimal_report)
        assert result == ["docker-compose"]


# ============================================================================
# TEST get_filtered_questions
# ============================================================================


class TestGetFilteredQuestions:
    """Test get_filtered_questions function"""

    def test_all_questions_for_team_dev(self, team_answers):
        """Should include all questions for team development"""
        filtered = get_filtered_questions(team_answers)
        # Should not skip team questions
        fields = [q["field"] for q in filtered]
        assert "code_review_strictness" in fields
        assert "pair_programming" in fields
        assert "git_workflow" in fields

    def test_skip_team_questions_for_solo_dev(self, solo_dev_answers):
        """Should skip team questions for solo developer"""
        filtered = get_filtered_questions(solo_dev_answers)
        fields = [q["field"] for q in filtered]
        assert "code_review_strictness" not in fields
        assert "pair_programming" not in fields
        assert "git_workflow" not in fields

    def test_skip_api_docs_for_cli_project(self):
        """Should skip API docs for non-API projects"""
        answers = {"types": ["cli"]}
        filtered = get_filtered_questions(answers)
        fields = [q["field"] for q in filtered]
        assert "api_documentation" not in fields

    def test_include_api_docs_for_api_project(self):
        """Should include API docs for API projects"""
        answers = {"types": ["api"]}
        filtered = get_filtered_questions(answers)
        fields = [q["field"] for q in filtered]
        assert "api_documentation" in fields

    def test_skip_advanced_testing_for_no_coverage(self):
        """Should skip advanced testing questions when no coverage"""
        answers = {"coverage_target": "none"}
        filtered = get_filtered_questions(answers)
        fields = [q["field"] for q in filtered]
        assert "mutation_testing" not in fields
        assert "property_based_testing" not in fields

    def test_skip_deployment_for_manual_cicd(self):
        """Should skip deployment questions for manual CI/CD"""
        answers = {"ci_cd_trigger": "manual"}
        filtered = get_filtered_questions(answers)
        fields = [q["field"] for q in filtered]
        assert "deployment_frequency" not in fields
        assert "rollback_strategy" not in fields

    def test_skip_architecture_diagrams_for_minimal_docs(self):
        """Should skip architecture diagrams for minimal documentation"""
        answers = {"verbosity": "minimal"}
        filtered = get_filtered_questions(answers)
        fields = [q["field"] for q in filtered]
        assert "architecture_diagrams" not in fields

    def test_handle_invalid_skip_condition(self):
        """Should gracefully handle invalid skip conditions"""
        # This should not crash even with weird answers
        answers = {"team_trajectory": None}
        filtered = get_filtered_questions(answers)
        assert isinstance(filtered, list)
        assert len(filtered) > 0

    def test_empty_answers_returns_all_questions(self, empty_answers):
        """Should return most questions when answers are empty"""
        filtered = get_filtered_questions(empty_answers)
        # Should have many questions (not all, since some have defaults)
        assert len(filtered) > 50


# ============================================================================
# TEST count_questions_for_answers
# ============================================================================


class TestCountQuestionsForAnswers:
    """Test count_questions_for_answers function"""

    def test_count_matches_filtered_length(self, team_answers):
        """Count should match length of filtered questions"""
        filtered = get_filtered_questions(team_answers)
        count = count_questions_for_answers(team_answers)
        assert count == len(filtered)

    def test_count_for_solo_dev_less_than_team(self, solo_dev_answers, team_answers):
        """Solo dev should have fewer questions than team"""
        solo_count = count_questions_for_answers(solo_dev_answers)
        team_count = count_questions_for_answers(team_answers)
        assert solo_count < team_count

    def test_count_for_no_tests_less_than_with_tests(self):
        """No tests should have fewer questions than with tests"""
        no_tests = {"coverage_target": "none"}
        with_tests = {"coverage_target": "90"}

        no_tests_count = count_questions_for_answers(no_tests)
        with_tests_count = count_questions_for_answers(with_tests)
        assert no_tests_count < with_tests_count

    def test_count_returns_positive_integer(self, empty_answers):
        """Count should always return a positive integer"""
        count = count_questions_for_answers(empty_answers)
        assert isinstance(count, int)
        assert count > 0


# ============================================================================
# TEST QUESTIONS Structure
# ============================================================================


class TestQuestionsStructure:
    """Test QUESTIONS list structure and integrity"""

    def test_questions_is_list(self):
        """QUESTIONS should be a list"""
        assert isinstance(QUESTIONS, list)
        assert len(QUESTIONS) > 0

    def test_all_questions_have_required_fields(self):
        """All questions should have required fields"""
        required_fields = ["category", "field", "type", "prompt"]

        for q in QUESTIONS:
            for field in required_fields:
                assert field in q, f"Question missing field: {field}"

    def test_all_questions_have_unique_fields(self):
        """All questions should have unique field names"""
        fields = [q["field"] for q in QUESTIONS]
        assert len(fields) == len(set(fields)), "Duplicate field names found"

    def test_choice_questions_have_choices(self):
        """Choice questions should have choices defined"""
        for q in QUESTIONS:
            if q["type"] in ["choice", "multi_choice"]:
                assert "choices" in q, f"Choice question missing choices: {q['field']}"
                assert callable(q["choices"]) or isinstance(q["choices"], list)

    def test_all_questions_have_defaults(self):
        """All questions should have default values"""
        for q in QUESTIONS:
            # Required fields may not have defaults
            if q.get("required"):
                continue
            assert "default" in q, f"Question missing default: {q['field']}"

    def test_all_questions_have_ai_hints(self):
        """All questions should have AI hints (even if no_hint)"""
        for q in QUESTIONS:
            assert "ai_hint" in q, f"Question missing ai_hint: {q['field']}"
            assert callable(q["ai_hint"])

    def test_int_questions_have_min_max(self):
        """Integer questions should have min/max bounds"""
        for q in QUESTIONS:
            if q["type"] == "int":
                assert "min" in q, f"Int question missing min: {q['field']}"
                assert "max" in q, f"Int question missing max: {q['field']}"

    def test_valid_categories(self):
        """Questions should have valid categories"""
        valid_categories = {
            "project_identity",
            "development_style",
            "code_quality",
            "documentation",
            "testing",
            "security",
            "performance",
            "collaboration",
            "devops",
        }

        for q in QUESTIONS:
            assert q["category"] in valid_categories, f"Invalid category: {q['category']}"

    def test_valid_types(self):
        """Questions should have valid types"""
        valid_types = {"text", "multi_text", "choice", "multi_choice", "int"}

        for q in QUESTIONS:
            assert q["type"] in valid_types, f"Invalid type: {q['type']}"


# ============================================================================
# TEST Edge Cases
# ============================================================================


class TestEdgeCases:
    """Test edge cases and error handling"""

    def test_hints_handle_empty_report(self, empty_report):
        """All hint generators should handle empty reports"""
        hint_funcs = [
            get_project_type_hint,
            get_language_hint,
            get_framework_hint,
            get_deployment_hint,
            get_scale_hint,
            get_compliance_hint,
            get_maturity_hint,
            get_team_size_hint,
            get_linting_hint,
            get_type_coverage_hint,
            get_testing_coverage_hint,
            get_security_stance_hint,
            get_infrastructure_hint,
            get_monitoring_hint,
        ]

        for func in hint_funcs:
            result = func(empty_report)
            assert isinstance(result, str)

    def test_defaults_handle_empty_report(self, empty_report):
        """All default generators should handle empty reports"""
        default_funcs = [
            default_project_types,
            default_primary_language,
            default_secondary_languages,
            default_frameworks,
            default_deployment_target,
            default_scale,
            default_maturity,
            default_infrastructure,
        ]

        for func in default_funcs:
            result = func(empty_report)
            assert result is not None

    def test_should_ask_question_with_malformed_answers(self):
        """should_ask_question should handle malformed answers"""
        malformed_answers = [
            {"team_trajectory": None},
            {"coverage_target": "invalid"},
            {"types": "not-a-list"},
            {"infrastructure": None},
        ]

        for answers in malformed_answers:
            # Should not crash
            result = should_ask_question("some_question", answers)
            assert isinstance(result, bool)

    def test_get_filtered_questions_with_none_answers(self):
        """get_filtered_questions should handle None values"""
        answers = {
            "team_trajectory": None,
            "coverage_target": None,
            "types": None,
        }

        filtered = get_filtered_questions(answers)
        assert isinstance(filtered, list)

    def test_default_scale_boundary_conditions(self):
        """Test default_scale with exact threshold values"""
        from claudecodeoptimizer.core.constants import (
            LARGE_CODEBASE_THRESHOLD,
            MEDIUM_CODEBASE_THRESHOLD,
            SMALL_CODEBASE_THRESHOLD,
        )

        # Just over large threshold
        report = {"codebase_patterns": {"total_files": LARGE_CODEBASE_THRESHOLD + 1}}
        assert default_scale(report) == "enterprise"

        # Just over medium threshold
        report = {"codebase_patterns": {"total_files": MEDIUM_CODEBASE_THRESHOLD + 1}}
        assert default_scale(report) == "growth"

        # Just over small threshold
        report = {"codebase_patterns": {"total_files": SMALL_CODEBASE_THRESHOLD + 1}}
        assert default_scale(report) == "startup"

        # At small threshold
        report = {"codebase_patterns": {"total_files": SMALL_CODEBASE_THRESHOLD}}
        assert default_scale(report) == "startup"

        # Zero files
        report = {"codebase_patterns": {"total_files": 0}}
        assert default_scale(report) == "startup"
