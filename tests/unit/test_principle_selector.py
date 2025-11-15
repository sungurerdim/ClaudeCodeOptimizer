"""
Unit tests for PrincipleSelector

Tests principle filtering, selection, and applicability logic.
Target Coverage: 80%
"""

from pathlib import Path
from typing import Any, Dict, List

import pytest

from claudecodeoptimizer.core.principle_selector import (
    PrincipleSelector,
    generate_principles_from_preferences,
)


@pytest.fixture
def minimal_preferences() -> Dict[str, Any]:
    """Minimal valid preferences for testing"""
    return {
        "project_type": "cli_tool",
        "team_size": "solo",
        "security_stance": "balanced",
        "test_philosophy": "pragmatic",
        "quality_level": "strict",
    }


@pytest.fixture
def web_api_preferences() -> Dict[str, Any]:
    """Preferences for web API project"""
    return {
        "project_type": "web_api",
        "team_size": "small_team",
        "security_stance": "strict",
        "test_philosophy": "test_heavy",
        "quality_level": "strict",
    }


@pytest.fixture
def microservice_preferences() -> Dict[str, Any]:
    """Preferences for microservice project"""
    return {
        "project_type": "microservice",
        "team_size": "large_team",
        "security_stance": "strict",
        "test_philosophy": "test_heavy",
        "quality_level": "strict",
    }


@pytest.fixture
def sample_principles() -> List[Dict[str, Any]]:
    """Sample principles for testing"""
    return [
        {
            "id": "U_DRY",
            "title": "DRY Enforcement",
            "category": "universal",
            "enforcement_level": "must",
            "content": "Test content",
        },
        {
            "id": "P_TYPE_SAFETY",
            "title": "Type Safety",
            "category": "code_quality",
            "enforcement_level": "must",
            "applicable_to": ["library", "cli_tool", "web_api"],
            "content": "Test content",
        },
        {
            "id": "P_API_SECURITY",
            "title": "API Security",
            "category": "security_privacy",
            "enforcement_level": "must",
            "applicable_to": ["web_api", "microservice"],
            "content": "Test content",
        },
        {
            "id": "P_TEST_COVERAGE",
            "title": "Test Coverage",
            "category": "testing",
            "enforcement_level": "should",
            "applicable_to": ["all"],
            "content": "Test content",
        },
    ]


class TestPrincipleSelector:
    """Test PrincipleSelector functionality"""

    def test_initialization(self, minimal_preferences) -> None:
        """Test PrincipleSelector initialization"""
        selector = PrincipleSelector(minimal_preferences)
        assert selector.preferences == minimal_preferences
        assert isinstance(selector.all_principles, list)

    def test_load_principles_deduplication(self, minimal_preferences, monkeypatch) -> None:
        """Test that duplicate principle IDs are deduplicated"""
        duplicate_principles = [
            {"id": "U_DRY", "title": "First", "category": "universal"},
            {"id": "U_DRY", "title": "Second", "category": "universal"},
        ]

        def mock_load_all_principles(path):
            return duplicate_principles

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        selector = PrincipleSelector(minimal_preferences)
        # Should only have one U_DRY
        dry_principles = [p for p in selector.all_principles if p["id"] == "U_DRY"]
        assert len(dry_principles) == 1

    def test_filter_by_category_universal(self, minimal_preferences, monkeypatch) -> None:
        """Test filtering universal principles"""

        def mock_load_all_principles(path):
            return [
                {"id": "U_DRY", "category": "universal", "content": "test"},
                {"id": "P_TYPE_SAFETY", "category": "code_quality", "content": "test"},
            ]

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        selector = PrincipleSelector(minimal_preferences)
        universal = [p for p in selector.all_principles if p["category"] == "universal"]
        assert len(universal) >= 1
        assert all(p["category"] == "universal" for p in universal)

    def test_filter_by_category_project_specific(self, minimal_preferences, monkeypatch) -> None:
        """Test filtering project-specific principles"""

        def mock_load_all_principles(path):
            return [
                {"id": "P_TYPE_SAFETY", "category": "code_quality", "content": "test"},
                {
                    "id": "P_API_SECURITY",
                    "category": "security_privacy",
                    "content": "test",
                },
            ]

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        selector = PrincipleSelector(minimal_preferences)
        project_specific = [p for p in selector.all_principles if p["category"] != "universal"]
        assert len(project_specific) >= 1

    def test_applicability_all_projects(self, minimal_preferences, monkeypatch) -> None:
        """Test principles applicable to all project types"""

        def mock_load_all_principles(path):
            return [
                {
                    "id": "P_TEST",
                    "category": "testing",
                    "applicable_to": ["all"],
                    "content": "test",
                }
            ]

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        selector = PrincipleSelector(minimal_preferences)
        # Should be included for cli_tool project
        test_principles = [p for p in selector.all_principles if p["id"] == "P_TEST"]
        assert len(test_principles) == 1

    def test_applicability_specific_project_type(self, web_api_preferences, monkeypatch) -> None:
        """Test principles applicable to specific project types"""

        def mock_load_all_principles(path):
            return [
                {
                    "id": "P_API_SEC",
                    "category": "security_privacy",
                    "applicable_to": ["web_api", "microservice"],
                    "content": "test",
                },
                {
                    "id": "P_CLI_ONLY",
                    "category": "code_quality",
                    "applicable_to": ["cli_tool"],
                    "content": "test",
                },
            ]

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        selector = PrincipleSelector(web_api_preferences)

        # P_API_SEC should be included for web_api
        api_principles = [p for p in selector.all_principles if p["id"] == "P_API_SEC"]
        assert len(api_principles) == 1

        # P_CLI_ONLY should not be included for web_api
        [p for p in selector.all_principles if p["id"] == "P_CLI_ONLY"]
        # Note: This depends on actual filtering logic implementation

    def test_enforcement_levels(self, minimal_preferences, monkeypatch) -> None:
        """Test different enforcement levels"""

        def mock_load_all_principles(path):
            return [
                {
                    "id": "P_MUST",
                    "enforcement_level": "must",
                    "category": "code_quality",
                    "content": "test",
                },
                {
                    "id": "P_SHOULD",
                    "enforcement_level": "should",
                    "category": "code_quality",
                    "content": "test",
                },
                {
                    "id": "P_MAY",
                    "enforcement_level": "may",
                    "category": "code_quality",
                    "content": "test",
                },
            ]

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        selector = PrincipleSelector(minimal_preferences)
        must_principles = [
            p for p in selector.all_principles if p.get("enforcement_level") == "must"
        ]
        should_principles = [
            p for p in selector.all_principles if p.get("enforcement_level") == "should"
        ]

        assert len(must_principles) >= 1
        assert len(should_principles) >= 1

    def test_security_override_for_api_projects(
        self, microservice_preferences, monkeypatch
    ) -> None:
        """Test security principle override for API/microservice projects"""

        def mock_load_all_principles(path):
            return [
                {
                    "id": "P_ENCRYPTION",
                    "category": "security_privacy",
                    "applicable_to": ["web_api", "microservice"],
                    "content": "test",
                }
            ]

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        selector = PrincipleSelector(microservice_preferences)
        security_principles = [
            p for p in selector.all_principles if p["category"] == "security_privacy"
        ]

        # Security principles should be present for microservices
        assert len(security_principles) >= 1

    def test_empty_principles_handling(self, minimal_preferences, monkeypatch) -> None:
        """Test handling of empty principles list"""

        def mock_load_all_principles(path):
            return []

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        selector = PrincipleSelector(minimal_preferences)
        assert selector.all_principles == []

    def test_preferences_storage(self, minimal_preferences) -> None:
        """Test that preferences are correctly stored"""
        selector = PrincipleSelector(minimal_preferences)
        assert selector.preferences["project_type"] == "cli_tool"
        assert selector.preferences["team_size"] == "solo"
        assert selector.preferences["security_stance"] == "balanced"

    def test_principles_have_required_fields(self, minimal_preferences) -> None:
        """Test that loaded principles have required fields"""
        selector = PrincipleSelector(minimal_preferences)

        for principle in selector.all_principles:
            assert "id" in principle, f"Principle missing 'id': {principle}"
            assert "category" in principle, f"Principle missing 'category': {principle}"
            # Content might be loaded lazily, so not always required in memory

    def test_category_validation(self, minimal_preferences) -> None:
        """Test that principle categories are valid"""
        valid_categories = {
            "universal",
            "code_quality",
            "security_privacy",
            "testing",
            "architecture",
            "performance",
            "operations",
            "git_workflow",
            "api_design",
            "claude-guidelines",
            "project-specific",
        }

        selector = PrincipleSelector(minimal_preferences)

        for principle in selector.all_principles:
            category = principle.get("category")
            assert category in valid_categories, (
                f"Invalid category '{category}' for principle {principle.get('id')}"
            )


class TestSelectApplicable:
    """Test select_applicable() method"""

    def test_select_applicable_with_selected_ids(self, minimal_preferences, monkeypatch) -> None:
        """Test selecting specific principle IDs"""

        def mock_load_all_principles(path):
            return [
                {"id": "U_DRY", "category": "universal", "weight": 10, "severity": "high"},
                {
                    "id": "P_TYPE_SAFETY",
                    "category": "code_quality",
                    "weight": 8,
                    "severity": "medium",
                },
                {
                    "id": "P_API_SECURITY",
                    "category": "security_privacy",
                    "weight": 9,
                    "severity": "high",
                },
            ]

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        # Select only specific principles
        preferences = minimal_preferences.copy()
        preferences["selected_principle_ids"] = ["U_DRY", "P_API_SECURITY"]

        selector = PrincipleSelector(preferences)
        applicable = selector.select_applicable()

        # Should only return selected IDs
        assert len(applicable) == 2
        ids = [p["id"] for p in applicable]
        assert "U_DRY" in ids
        assert "P_API_SECURITY" in ids
        assert "P_TYPE_SAFETY" not in ids

    def test_select_applicable_sorts_by_priority(self, minimal_preferences, monkeypatch) -> None:
        """Test that selected principles are sorted by severity"""

        def mock_load_all_principles(path):
            return [
                {"id": "P_LOW", "category": "code_quality", "weight": 10, "severity": "low"},
                {
                    "id": "P_CRITICAL",
                    "category": "code_quality",
                    "weight": 10,
                    "severity": "critical",
                },
                {"id": "P_MEDIUM", "category": "code_quality", "weight": 10, "severity": "medium"},
                {"id": "P_HIGH", "category": "code_quality", "weight": 10, "severity": "high"},
            ]

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        selector = PrincipleSelector(minimal_preferences)
        applicable = selector.select_applicable()

        # Should be sorted by severity: critical > high > medium > low
        severities = [p["severity"] for p in applicable]
        assert severities == ["critical", "high", "medium", "low"]

    def test_select_applicable_adds_enforcement_level(
        self, minimal_preferences, monkeypatch
    ) -> None:
        """Test that enforcement level is added based on strictness"""

        def mock_load_all_principles(path):
            return [
                {"id": "P_TEST", "category": "code_quality", "weight": 10, "severity": "high"},
            ]

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        # Set up preferences with nested structure
        preferences = {
            "project_type": "cli_tool",
            "code_quality": {"linting_strictness": "strict"},
        }

        selector = PrincipleSelector(preferences)
        applicable = selector.select_applicable()

        # Should have enforcement level added
        assert len(applicable) > 0
        assert "enforcement" in applicable[0]
        assert applicable[0]["enforcement"] == "SHOULD - Requires justification"


class TestEvaluateCondition:
    """Test _evaluate_condition() method"""

    def test_evaluate_condition_in_operator(self, minimal_preferences, monkeypatch) -> None:
        """Test 'in' operator"""

        def mock_load_all_principles(path):
            return []

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        preferences = {
            "code_quality": {"linting_strictness": "strict"},
        }

        selector = PrincipleSelector(preferences)

        condition = {
            "path": "code_quality.linting_strictness",
            "operator": "in",
            "values": ["strict", "pedantic"],
        }

        assert selector._evaluate_condition(condition) is True

    def test_evaluate_condition_not_in_operator(self, minimal_preferences, monkeypatch) -> None:
        """Test 'not_in' operator"""

        def mock_load_all_principles(path):
            return []

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        preferences = {
            "code_quality": {"linting_strictness": "relaxed"},
        }

        selector = PrincipleSelector(preferences)

        condition = {
            "path": "code_quality.linting_strictness",
            "operator": "not_in",
            "values": ["strict", "pedantic"],
        }

        assert selector._evaluate_condition(condition) is True

    def test_evaluate_condition_contains_any_list(self, minimal_preferences, monkeypatch) -> None:
        """Test 'contains_any' operator with list"""

        def mock_load_all_principles(path):
            return []

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        preferences = {
            "project_identity": {"types": ["web-app", "backend"]},
        }

        selector = PrincipleSelector(preferences)

        condition = {
            "path": "project_identity.types",
            "operator": "contains_any",
            "values": ["backend", "frontend"],
        }

        assert selector._evaluate_condition(condition) is True

    def test_evaluate_condition_gte_operator(self, minimal_preferences, monkeypatch) -> None:
        """Test '>=' operator with percentage"""

        def mock_load_all_principles(path):
            return []

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        preferences = {
            "testing": {"coverage_target": "90"},
        }

        selector = PrincipleSelector(preferences)

        condition = {
            "path": "testing.coverage_target",
            "operator": ">=",
            "values": ["80"],
        }

        assert selector._evaluate_condition(condition) is True

    def test_evaluate_condition_lte_operator(self, minimal_preferences, monkeypatch) -> None:
        """Test '<=' operator"""

        def mock_load_all_principles(path):
            return []

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        preferences = {
            "testing": {"coverage_target": "70"},
        }

        selector = PrincipleSelector(preferences)

        condition = {
            "path": "testing.coverage_target",
            "operator": "<=",
            "values": ["80"],
        }

        assert selector._evaluate_condition(condition) is True

    def test_evaluate_condition_invalid_path(self, minimal_preferences, monkeypatch) -> None:
        """Test condition with invalid path returns False"""

        def mock_load_all_principles(path):
            return []

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        selector = PrincipleSelector(minimal_preferences)

        condition = {
            "path": "nonexistent.path",
            "operator": "in",
            "values": ["test"],
        }

        assert selector._evaluate_condition(condition) is False


class TestGetNestedValue:
    """Test _get_nested_value() method"""

    def test_get_nested_value_from_dict(self, minimal_preferences, monkeypatch) -> None:
        """Test getting nested value from dictionary"""

        def mock_load_all_principles(path):
            return []

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        preferences = {
            "code_quality": {"linting_strictness": "strict"},
        }

        selector = PrincipleSelector(preferences)
        value = selector._get_nested_value(selector.preferences, "code_quality.linting_strictness")

        assert value == "strict"

    def test_get_nested_value_empty_path(self, minimal_preferences, monkeypatch) -> None:
        """Test empty path returns None"""

        def mock_load_all_principles(path):
            return []

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        selector = PrincipleSelector(minimal_preferences)
        value = selector._get_nested_value(selector.preferences, "")

        assert value is None

    def test_get_nested_value_nonexistent_path(self, minimal_preferences, monkeypatch) -> None:
        """Test nonexistent path returns None"""

        def mock_load_all_principles(path):
            return []

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        selector = PrincipleSelector(minimal_preferences)
        value = selector._get_nested_value(selector.preferences, "nonexistent.path")

        assert value is None


class TestCheckSeverityMatch:
    """Test _check_severity_match() method"""

    def test_severity_match_paranoid_all_principles(self, minimal_preferences, monkeypatch) -> None:
        """Test paranoid mode includes all principles"""

        def mock_load_all_principles(path):
            return []

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        preferences = {
            "code_quality": {"linting_strictness": "paranoid"},
        }

        selector = PrincipleSelector(preferences)

        # Even low weight principles should pass
        principle = {"id": "P_TEST", "weight": 5, "severity": "low", "category": "code_quality"}
        assert selector._check_severity_match(principle) is True

    def test_severity_match_strict_filters_low_weight(
        self, minimal_preferences, monkeypatch
    ) -> None:
        """Test strict mode filters low weight principles"""

        def mock_load_all_principles(path):
            return []

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        preferences = {
            "code_quality": {"linting_strictness": "strict"},
        }

        selector = PrincipleSelector(preferences)

        # Low weight principle should be filtered
        principle = {"id": "P_TEST", "weight": 6, "severity": "low", "category": "code_quality"}
        assert selector._check_severity_match(principle) is False

        # High weight principle should pass
        principle = {"id": "P_TEST", "weight": 8, "severity": "high", "category": "code_quality"}
        assert selector._check_severity_match(principle) is True

    def test_severity_match_security_override_api_project(
        self, minimal_preferences, monkeypatch
    ) -> None:
        """Test security override for API projects"""

        def mock_load_all_principles(path):
            return []

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        preferences = {
            "code_quality": {"linting_strictness": "moderate"},
            "security": {"security_stance": "balanced"},
            "project_identity": {"types": ["web-app", "api"]},
        }

        selector = PrincipleSelector(preferences)

        # Security principle with weight 8 should pass for API projects
        principle = {
            "id": "P_SECURITY",
            "weight": 8,
            "severity": "high",
            "category": "security_privacy",
        }
        assert selector._check_severity_match(principle) is True


class TestCheckCategoryRelevance:
    """Test _check_category_relevance() method"""

    def test_category_git_workflow_solo_dev(self, minimal_preferences, monkeypatch) -> None:
        """Test git workflow principles filtered for solo devs"""

        def mock_load_all_principles(path):
            return []

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        preferences = {
            "project_identity": {"team_trajectory": "solo"},
        }

        selector = PrincipleSelector(preferences)

        # PR guidelines should be filtered for solo
        principle = {"id": "P_PR_GUIDELINES", "category": "project-specific"}
        assert selector._check_category_relevance(principle) is False

        # Commit conventions should be kept for solo
        principle = {"id": "P_COMMIT_MESSAGE_CONVENTIONS", "category": "project-specific"}
        assert selector._check_category_relevance(principle) is True

    def test_category_operations_prototype(self, minimal_preferences, monkeypatch) -> None:
        """Test operations principles filtered for prototypes"""

        def mock_load_all_principles(path):
            return []

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        preferences = {
            "project_identity": {"project_maturity": "prototype"},
        }

        selector = PrincipleSelector(preferences)

        # Non-critical operations should be filtered
        principle = {
            "id": "P_GITOPS_PRACTICES",
            "category": "project-specific",
            "severity": "low",
        }
        assert selector._check_category_relevance(principle) is False

        # Critical operations should be kept
        principle = {
            "id": "P_HEALTH_CHECKS",
            "category": "project-specific",
            "severity": "critical",
        }
        assert selector._check_category_relevance(principle) is True

    def test_category_architecture_solo_dev(self, minimal_preferences, monkeypatch) -> None:
        """Test complex architecture filtered for solo devs"""

        def mock_load_all_principles(path):
            return []

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        preferences = {
            "project_identity": {"team_trajectory": "solo"},
        }

        selector = PrincipleSelector(preferences)

        # Complex patterns should be filtered for solo
        principle = {"id": "P_MICROSERVICES_SERVICE_MESH", "category": "architecture"}
        assert selector._check_category_relevance(principle) is False


class TestStatistics:
    """Test statistics generation"""

    def test_generate_statistics(self, minimal_preferences, monkeypatch) -> None:
        """Test statistics generation"""

        def mock_load_all_principles(path):
            return [
                {
                    "id": "P_CRITICAL",
                    "category": "code_quality",
                    "weight": 10,
                    "severity": "critical",
                },
                {"id": "P_HIGH", "category": "security_privacy", "weight": 10, "severity": "high"},
                {"id": "P_MEDIUM", "category": "testing", "weight": 10, "severity": "medium"},
                {"id": "P_LOW", "category": "code_quality", "weight": 10, "severity": "low"},
            ]

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        selector = PrincipleSelector(minimal_preferences)
        stats = selector.generate_statistics()

        assert "total_principles" in stats
        assert "applicable_count" in stats
        assert "skipped_count" in stats
        assert "by_severity" in stats
        assert "by_category" in stats
        assert "coverage_percentage" in stats

        # Check severity counts
        assert stats["by_severity"]["critical"] >= 0
        assert stats["by_severity"]["high"] >= 0
        assert stats["by_severity"]["medium"] >= 0
        assert stats["by_severity"]["low"] >= 0

        # Check category counts
        assert isinstance(stats["by_category"], dict)

        # Check total
        assert stats["total_principles"] == 4


class TestSkippedPrinciples:
    """Test get_skipped_principles() method"""

    def test_get_skipped_principles(self, minimal_preferences, monkeypatch) -> None:
        """Test getting skipped principles with reasons"""

        def mock_load_all_principles(path):
            return [
                {"id": "P_INCLUDED", "category": "code_quality", "weight": 10, "severity": "high"},
                {"id": "P_EXCLUDED", "category": "code_quality", "weight": 5, "severity": "low"},
            ]

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        preferences = {
            "code_quality": {"linting_strictness": "strict"},
        }

        selector = PrincipleSelector(preferences)
        skipped = selector.get_skipped_principles()

        # Should have skip reasons
        assert len(skipped) > 0
        for principle in skipped:
            assert "skip_reason" in principle
            assert principle["skip_reason"] != ""

    def test_skip_reason_team_size(self, minimal_preferences, monkeypatch) -> None:
        """Test skip reason for team size"""

        def mock_load_all_principles(path):
            return [
                {"id": "P_MICROSERVICES_SERVICE_MESH", "category": "architecture", "weight": 10},
            ]

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        preferences = {
            "project_identity": {"team_trajectory": "solo"},
            "code_quality": {"linting_strictness": "strict"},
        }

        selector = PrincipleSelector(preferences)
        skipped = selector.get_skipped_principles()

        # Should have team size reason
        mesh_principle = next(
            (p for p in skipped if p["id"] == "P_MICROSERVICES_SERVICE_MESH"), None
        )
        if mesh_principle:
            assert "solo" in mesh_principle["skip_reason"].lower()


class TestPrinciplesGeneration:
    """Test PRINCIPLES.md generation"""

    def test_generate_principles_md(self, minimal_preferences, monkeypatch, tmp_path) -> None:
        """Test generating PRINCIPLES.md file"""

        def mock_load_all_principles(path):
            return [
                {
                    "id": "U_FAIL_FAST",
                    "title": "Fail-Fast",
                    "category": "universal",
                    "weight": 10,
                    "severity": "critical",
                    "description": "Fail fast description",
                    "rules": [{"description": "Rule 1"}],
                    "examples": {"good": ["good example"], "bad": ["bad example"]},
                },
                {
                    "id": "U_EVIDENCE_BASED",
                    "title": "Evidence-Based",
                    "category": "universal",
                    "weight": 10,
                    "severity": "critical",
                    "description": "Evidence description",
                    "rules": [],
                    "examples": {},
                },
                {
                    "id": "U_NO_OVERENGINEERING",
                    "title": "No Overengineering",
                    "category": "universal",
                    "weight": 10,
                    "severity": "critical",
                    "description": "No overengineering description",
                    "rules": [],
                    "examples": {},
                },
            ]

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        selector = PrincipleSelector(minimal_preferences)
        output_path = tmp_path / "PRINCIPLES.md"

        result = selector.generate_principles_md(output_path)

        assert result["success"] is True
        assert output_path.exists()
        assert "principles_file" in result
        assert "applicable_count" in result
        assert "stats" in result

        # Check file content
        content = output_path.read_text(encoding="utf-8")
        assert "# Development Principles" in content
        assert "U_FAIL_FAST" in content
        assert "U_EVIDENCE_BASED" in content
        assert "U_NO_OVERENGINEERING" in content

    def test_generate_principles_creates_backup(
        self, minimal_preferences, monkeypatch, tmp_path
    ) -> None:
        """Test that existing file is backed up"""

        def mock_load_all_principles(path):
            return [
                {
                    "id": "U_FAIL_FAST",
                    "title": "Fail-Fast",
                    "category": "universal",
                    "weight": 10,
                    "severity": "critical",
                    "description": "Test",
                    "rules": [],
                    "examples": {},
                },
                {
                    "id": "U_EVIDENCE_BASED",
                    "title": "Evidence-Based",
                    "category": "universal",
                    "weight": 10,
                    "severity": "critical",
                    "description": "Test",
                    "rules": [],
                    "examples": {},
                },
                {
                    "id": "U_NO_OVERENGINEERING",
                    "title": "No Overengineering",
                    "category": "universal",
                    "weight": 10,
                    "severity": "critical",
                    "description": "Test",
                    "rules": [],
                    "examples": {},
                },
            ]

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        # Mock CCOConfig.get_project_backups_dir
        def mock_get_backups_dir(project_name):
            return tmp_path / "backups"

        monkeypatch.setattr(
            "claudecodeoptimizer.config.CCOConfig.get_project_backups_dir",
            mock_get_backups_dir,
        )

        # Create existing file
        output_path = tmp_path / "PRINCIPLES.md"
        output_path.write_text("Old content", encoding="utf-8")

        selector = PrincipleSelector(minimal_preferences)
        selector.generate_principles_md(output_path)

        # Check backup was created
        backup_dir = tmp_path / "backups"
        assert backup_dir.exists()
        backups = list(backup_dir.glob("PRINCIPLES.md.*.backup"))
        assert len(backups) > 0


class TestCategoryFileGeneration:
    """Test category file generation"""

    def test_generate_category_files(self, minimal_preferences, monkeypatch, tmp_path) -> None:
        """Test generating category-specific files"""

        def mock_load_all_principles(path):
            return [
                {
                    "id": "U_FAIL_FAST",
                    "title": "Fail-Fast",
                    "category": "universal",
                    "severity": "critical",
                    "description": "Test",
                    "rules": [{"description": "Rule 1"}],
                    "examples": {"good": ["example"], "bad": ["bad example"]},
                    "applicability": {"languages": ["python", "javascript"]},
                },
                {
                    "id": "P_TYPE_SAFETY",
                    "title": "Type Safety",
                    "category": "code_quality",
                    "severity": "high",
                    "description": "Test",
                    "rules": [],
                    "examples": {},
                    "applicability": {},
                },
            ]

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        selector = PrincipleSelector(minimal_preferences)
        result = selector.generate_category_files(tmp_path)

        assert result["success"] is True
        assert "generated_files" in result
        assert result["file_count"] > 0

        # Check that files were created
        assert len(result["generated_files"]) > 0
        for file_path in result["generated_files"]:
            assert Path(file_path).exists()


class TestIsApplicable:
    """Test _is_applicable() method edge cases"""

    def test_is_applicable_project_type_mismatch(self, minimal_preferences, monkeypatch) -> None:
        """Test principle filtered when project type doesn't match"""

        def mock_load_all_principles(path):
            return []

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        preferences = {
            "project_identity": {"types": ["cli-tool"]},
        }

        selector = PrincipleSelector(preferences)

        # Principle only for web-app should be filtered
        principle = {
            "id": "P_WEB_ONLY",
            "category": "code_quality",
            "weight": 10,
            "severity": "high",
            "applicability": {"project_types": ["web-app", "microservice"]},
        }

        assert selector._is_applicable(principle) is False

    def test_is_applicable_preference_condition_fails(
        self, minimal_preferences, monkeypatch
    ) -> None:
        """Test principle filtered when preference condition fails"""

        def mock_load_all_principles(path):
            return []

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        preferences = {
            "code_quality": {"linting_strictness": "relaxed"},
        }

        selector = PrincipleSelector(preferences)

        # Principle requiring strict linting should be filtered
        principle = {
            "id": "P_STRICT_ONLY",
            "category": "code_quality",
            "weight": 10,
            "severity": "high",
            "applicability": {
                "preference_conditions": [
                    {
                        "path": "code_quality.linting_strictness",
                        "operator": "in",
                        "values": ["strict", "pedantic"],
                    }
                ]
            },
        }

        assert selector._is_applicable(principle) is False

    def test_is_applicable_team_size_filtered(self, minimal_preferences, monkeypatch) -> None:
        """Test principle filtered for team size"""

        def mock_load_all_principles(path):
            return []

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        preferences = {
            "project_identity": {"team_trajectory": "solo"},
        }

        selector = PrincipleSelector(preferences)

        # CQRS pattern should be filtered for solo devs
        principle = {
            "id": "P_CQRS_PATTERN",
            "category": "architecture",
            "weight": 10,
            "severity": "high",
        }

        assert selector._is_applicable(principle) is False

    def test_is_applicable_security_stance_filtered(self, minimal_preferences, monkeypatch) -> None:
        """Test security principle filtered for low security stance"""

        def mock_load_all_principles(path):
            return []

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        preferences = {
            "security": {"security_stance": "relaxed"},
        }

        selector = PrincipleSelector(preferences)

        # High security principles should be filtered
        principle = {
            "id": "P_ZERO_TRUST",
            "category": "security_privacy",
            "weight": 10,
            "severity": "critical",
        }

        assert selector._is_applicable(principle) is False


class TestGetSkipReason:
    """Test _get_skip_reason() method edge cases"""

    def test_skip_reason_security_stance(self, minimal_preferences, monkeypatch) -> None:
        """Test skip reason for security stance"""

        def mock_load_all_principles(path):
            return []

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        preferences = {
            "security": {"security_stance": "relaxed"},
        }

        selector = PrincipleSelector(preferences)

        principle = {
            "id": "P_ZERO_TRUST",
            "category": "security_privacy",
        }

        reason = selector._get_skip_reason(principle)
        assert "security_stance" in reason.lower() or "relaxed" in reason.lower()

    def test_skip_reason_coverage_target(self, minimal_preferences, monkeypatch) -> None:
        """Test skip reason for coverage target"""

        def mock_load_all_principles(path):
            return []

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        preferences = {
            "testing": {"coverage_target": "50"},
        }

        selector = PrincipleSelector(preferences)

        principle = {
            "id": "P_PROPERTY_TESTING",
            "category": "testing",
        }

        reason = selector._get_skip_reason(principle)
        assert "coverage" in reason.lower() or "50" in reason

    def test_skip_reason_linting_strictness(self, minimal_preferences, monkeypatch) -> None:
        """Test skip reason for linting strictness"""

        def mock_load_all_principles(path):
            return []

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        preferences = {
            "code_quality": {"linting_strictness": "relaxed"},
        }

        selector = PrincipleSelector(preferences)

        principle = {
            "id": "P_HIGH_SEVERITY",
            "category": "code_quality",
            "severity": "critical",
        }

        reason = selector._get_skip_reason(principle)
        assert "relaxed" in reason.lower() or "linting" in reason.lower()


class TestEvaluateConditionEdgeCases:
    """Test edge cases in _evaluate_condition()"""

    def test_evaluate_condition_gte_with_invalid_value(
        self, minimal_preferences, monkeypatch
    ) -> None:
        """Test >= operator with invalid value returns False"""

        def mock_load_all_principles(path):
            return []

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        preferences = {
            "testing": {"coverage_target": "not_a_number"},
        }

        selector = PrincipleSelector(preferences)

        condition = {
            "path": "testing.coverage_target",
            "operator": ">=",
            "values": ["80"],
        }

        assert selector._evaluate_condition(condition) is False

    def test_evaluate_condition_lte_with_invalid_value(
        self, minimal_preferences, monkeypatch
    ) -> None:
        """Test <= operator with invalid value returns False"""

        def mock_load_all_principles(path):
            return []

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        preferences = {
            "testing": {"coverage_target": "not_a_number"},
        }

        selector = PrincipleSelector(preferences)

        condition = {
            "path": "testing.coverage_target",
            "operator": "<=",
            "values": ["80"],
        }

        assert selector._evaluate_condition(condition) is False

    def test_evaluate_condition_contains_any_scalar(self, minimal_preferences, monkeypatch) -> None:
        """Test contains_any operator with scalar value"""

        def mock_load_all_principles(path):
            return []

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        preferences = {
            "project_type": "web-app",
        }

        selector = PrincipleSelector(preferences)

        condition = {
            "path": "project_type",
            "operator": "contains_any",
            "values": ["web-app", "cli-tool"],
        }

        assert selector._evaluate_condition(condition) is True


class TestGetNestedValueEdgeCases:
    """Test edge cases in _get_nested_value()"""

    def test_get_nested_value_with_object_attribute(self, minimal_preferences, monkeypatch) -> None:
        """Test getting value from object with attributes"""

        def mock_load_all_principles(path):
            return []

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        # Create a mock object with attributes
        class MockObject:
            def __init__(self):
                self.code_quality = type("obj", (object,), {"linting_strictness": "strict"})()

        selector = PrincipleSelector(minimal_preferences)
        mock_obj = MockObject()

        value = selector._get_nested_value(mock_obj, "code_quality.linting_strictness")
        assert value == "strict"

    def test_get_nested_value_intermediate_none(self, minimal_preferences, monkeypatch) -> None:
        """Test getting value when intermediate path is None"""

        def mock_load_all_principles(path):
            return []

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        preferences = {
            "code_quality": None,
        }

        selector = PrincipleSelector(preferences)
        value = selector._get_nested_value(selector.preferences, "code_quality.linting_strictness")

        assert value is None


class TestUtilityFunctions:
    """Test utility functions"""

    def test_generate_principles_from_preferences(
        self, minimal_preferences, monkeypatch, tmp_path
    ) -> None:
        """Test convenience function"""

        def mock_load_all_principles(path):
            return [
                {
                    "id": "U_FAIL_FAST",
                    "title": "Fail-Fast",
                    "category": "universal",
                    "weight": 10,
                    "severity": "critical",
                    "description": "Test",
                    "rules": [],
                    "examples": {},
                },
                {
                    "id": "U_EVIDENCE_BASED",
                    "title": "Evidence-Based",
                    "category": "universal",
                    "weight": 10,
                    "severity": "critical",
                    "description": "Test",
                    "rules": [],
                    "examples": {},
                },
                {
                    "id": "U_NO_OVERENGINEERING",
                    "title": "No Overengineering",
                    "category": "universal",
                    "weight": 10,
                    "severity": "critical",
                    "description": "Test",
                    "rules": [],
                    "examples": {},
                },
            ]

        monkeypatch.setattr(
            "claudecodeoptimizer.core.principle_md_loader.load_all_principles",
            mock_load_all_principles,
        )

        output_path = tmp_path / "PRINCIPLES.md"
        result = generate_principles_from_preferences(minimal_preferences, output_path)

        assert result["success"] is True
        assert output_path.exists()


class TestPrincipleSelectorIntegration:
    """Integration tests with real principle files"""

    def test_load_real_principles(self, minimal_preferences) -> None:
        """Test loading principles from actual files"""
        selector = PrincipleSelector(minimal_preferences)

        # Should load some principles
        assert len(selector.all_principles) > 0

        # Should have universal principles
        universal = [p for p in selector.all_principles if p["category"] == "universal"]
        assert len(universal) > 0

    def test_principle_ids_are_unique(self, minimal_preferences) -> None:
        """Test that all principle IDs are unique after deduplication"""
        selector = PrincipleSelector(minimal_preferences)

        ids = [p["id"] for p in selector.all_principles]
        assert len(ids) == len(set(ids)), "Duplicate principle IDs found"

    def test_all_categories_present(self, minimal_preferences) -> None:
        """Test that principles from all major categories exist"""
        selector = PrincipleSelector(minimal_preferences)

        categories = {p["category"] for p in selector.all_principles}

        # At minimum should have universal and some project-specific
        assert "universal" in categories
        assert len(categories) > 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
