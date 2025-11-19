"""
Unit tests for Core Principles Management

Tests principle loading, selection, and management functionality.
Target Coverage: 90%+
"""

from pathlib import Path
from typing import Any, Dict
from unittest.mock import Mock, patch

from claudecodeoptimizer.core.constants import (
    SERVICE_COUNT_THRESHOLD_LARGE,
    SERVICE_COUNT_THRESHOLD_MEDIUM,
)
from claudecodeoptimizer.config import VERSION
import pytest

from claudecodeoptimizer.core.principles import (
    Principle,
    PrinciplesManager,
    ProjectCharacteristics,
    create_characteristics_from_analysis,
    get_principles_manager,
)


class TestPrinciple:
    """Test Principle dataclass"""

    def test_principle_initialization(self) -> None:
        """Test creating a Principle instance"""
        principle = Principle(
            id="U_TEST",
            number=1,
            title="Test Principle",
            category="Universal",
            severity="critical",
            weight=10,
            description="A test principle",
            applicability={"project_types": ["all"]},
            rules=[{"id": "RULE_001", "description": "Test rule"}],
            examples={"good": ["example1"], "bad": ["example2"]},
            autofix={"available": True, "method": "test_fix"},
        )

        assert principle.id == "U_TEST"
        assert principle.number == 1
        assert principle.title == "Test Principle"
        assert principle.category == "Universal"
        assert principle.severity == "critical"
        assert principle.weight == 10
        assert principle.description == "A test principle"
        assert principle.applicability == {"project_types": ["all"]}
        assert len(principle.rules) == 1
        assert len(principle.examples["good"]) == 1
        assert principle.autofix["available"] is True


class TestProjectCharacteristics:
    """Test ProjectCharacteristics dataclass"""

    def test_project_characteristics_initialization(self) -> None:
        """Test creating a ProjectCharacteristics instance"""
        chars = ProjectCharacteristics(
            project_type="api",
            primary_language="python",
            team_size="solo",
            services_count=0,
            privacy_critical=False,
            security_critical=True,
            performance_critical=False,
            has_containers=True,
            has_tests=True,
            contexts=["api_endpoints", "database"],
        )

        assert chars.project_type == "api"
        assert chars.primary_language == "python"
        assert chars.team_size == "solo"
        assert chars.services_count == 0
        assert chars.privacy_critical is False
        assert chars.security_critical is True
        assert chars.performance_critical is False
        assert chars.has_containers is True
        assert chars.has_tests is True
        assert "api_endpoints" in chars.contexts


class TestPrinciplesManagerInit:
    """Test PrinciplesManager initialization"""

    def test_init_with_custom_dir(self, tmp_path: Path) -> None:
        """Test initialization with custom principles directory"""
        principles_dir = tmp_path / "principles"
        principles_dir.mkdir()

        manager = PrinciplesManager(principles_dir)

        assert manager.principles_dir == principles_dir
        assert manager.version == VERSION
        assert isinstance(manager.principles, dict)
        assert isinstance(manager.categories, list)
        assert isinstance(manager.selection_strategies, dict)

    def test_init_without_dir(self) -> None:
        """Test initialization without providing directory"""
        manager = PrinciplesManager()

        # Should use default path from package
        assert manager.principles_dir is not None
        assert "principles" in str(manager.principles_dir)

    def test_init_with_nonexistent_dir(self, tmp_path: Path) -> None:
        """Test initialization with non-existent directory"""
        principles_dir = tmp_path / "nonexistent"

        manager = PrinciplesManager(principles_dir)

        assert manager.principles_dir == principles_dir
        # Should not crash, just not load principles
        assert len(manager.principles) == 0


class TestPrinciplesManagerLoading:
    """Test principle loading functionality"""

    @patch("claudecodeoptimizer.core.principle_md_loader.load_all_principles")
    def test_load_principles_success(self, mock_load: Mock, tmp_path: Path) -> None:
        """Test successful principle loading"""
        principles_dir = tmp_path / "principles"
        principles_dir.mkdir()

        # Mock loaded principles
        mock_load.return_value = [
            {
                "id": "U_TEST_1",
                "number": 1,
                "title": "Test Principle 1",
                "category": "Universal",
                "severity": "critical",
                "weight": 10,
                "description": "Test principle 1",
                "applicability": {"project_types": ["all"]},
                "rules": [],
                "examples": {},
                "autofix": {"available": False},
            },
            {
                "id": "U_TEST_2",
                "number": 2,
                "title": "Test Principle 2",
                "category": "Testing",
                "severity": "high",
                "weight": 7,
                "description": "Test principle 2",
                "applicability": {"project_types": ["all"]},
                "rules": [],
                "examples": {},
                "autofix": {"available": True},
            },
        ]

        manager = PrinciplesManager(principles_dir)

        assert len(manager.principles) == 2
        assert "U_TEST_1" in manager.principles
        assert "U_TEST_2" in manager.principles
        assert len(manager.categories) == 2  # Universal, Testing

    @patch("claudecodeoptimizer.core.principle_md_loader.load_all_principles")
    def test_load_principles_failure(self, mock_load: Mock, tmp_path: Path) -> None:
        """Test principle loading failure handling"""
        principles_dir = tmp_path / "principles"
        principles_dir.mkdir()

        # Mock loading failure
        mock_load.side_effect = Exception("Loading failed")

        manager = PrinciplesManager(principles_dir)

        # Should not crash, just have empty principles
        assert len(manager.principles) == 0


class TestPrinciplesManagerGetters:
    """Test principle getter methods"""

    @pytest.fixture
    def getter_manager(self, principles_manager_factory) -> PrinciplesManager:
        """Create a test manager with sample principles for getter tests"""
        return principles_manager_factory([
            {
                "id": "U_TEST_1",
                "number": 1,
                "title": "Test 1",
                "category": "Universal",
                "severity": "critical",
                "weight": 10,
                "description": "Test",
                "applicability": {},
                "rules": [],
                "examples": {},
                "autofix": {"available": False},
            },
            {
                "id": "U_TEST_2",
                "number": 2,
                "title": "Test 2",
                "category": "Testing",
                "severity": "high",
                "weight": 7,
                "description": "Test",
                "applicability": {},
                "rules": [{"id": "RULE_1"}],
                "examples": {},
                "autofix": {"available": True},
            },
            {
                "id": "P_TEST_3",
                "number": 3,
                "title": "Test 3",
                "category": "Testing",
                "severity": "medium",
                "weight": 5,
                "description": "Test",
                "applicability": {},
                "rules": [],
                "examples": {},
                "autofix": {"available": False},
            },
        ])

    def test_get_principle_exists(self, getter_manager) -> None:
        """Test getting an existing principle"""
        principle = getter_manager.get_principle("U_TEST_1")

        assert principle is not None
        assert principle.id == "U_TEST_1"
        assert principle.title == "Test 1"

    def test_get_principle_not_exists(self, getter_manager) -> None:
        """Test getting a non-existent principle"""
        principle = getter_manager.get_principle("NONEXISTENT")

        assert principle is None

    def test_get_all_principles(self, getter_manager) -> None:
        """Test getting all principles"""
        principles = getter_manager.get_all_principles()

        assert len(principles) == 3
        assert all(isinstance(p, Principle) for p in principles)

    def test_get_principles_by_category(self, getter_manager) -> None:
        """Test getting principles by category"""
        testing_principles = getter_manager.get_principles_by_category("Testing")

        assert len(testing_principles) == 2
        assert all(p.category == "Testing" for p in testing_principles)

    def test_get_principles_by_category_empty(self, getter_manager) -> None:
        """Test getting principles by non-existent category"""
        principles = getter_manager.get_principles_by_category("Nonexistent")

        assert len(principles) == 0

    def test_get_principles_by_severity(self, getter_manager) -> None:
        """Test getting principles by severity"""
        critical = getter_manager.get_principles_by_severity("critical")
        high = getter_manager.get_principles_by_severity("high")
        medium = getter_manager.get_principles_by_severity("medium")

        assert len(critical) == 1
        assert len(high) == 1
        assert len(medium) == 1

    def test_get_autofix_principles(self, getter_manager) -> None:
        """Test getting principles with autofix"""
        autofix = getter_manager.get_autofix_principles()

        assert len(autofix) == 1
        assert autofix[0].id == "U_TEST_2"


class TestPrinciplesManagerSummary:
    """Test principle summary and statistics"""

    @pytest.fixture
    def summary_manager(self, principles_manager_factory) -> PrinciplesManager:
        """Create a test manager with sample principles for summary tests"""
        return principles_manager_factory(
            [
                {
                    "id": "U_TEST_1",
                    "number": 1,
                    "title": "Test 1",
                    "category": "Universal",
                    "severity": "critical",
                    "weight": 10,
                    "description": "Critical principle",
                    "applicability": {},
                    "rules": [{"id": "RULE_1"}, {"id": "RULE_2"}],
                    "examples": {},
                    "autofix": {"available": True},
                },
                {
                    "id": "U_TEST_2",
                    "number": 2,
                    "title": "Test 2",
                    "category": "Testing",
                    "severity": "high",
                    "weight": 7,
                    "description": "High priority",
                    "applicability": {},
                    "rules": [],
                    "examples": {},
                    "autofix": {"available": False},
                },
            ],
            categories=[
                {"id": "Universal", "name": "Universal"},
                {"id": "Testing", "name": "Testing"},
            ],
        )

    def test_get_principle_summary_exists(self, summary_manager) -> None:
        """Test getting summary for existing principle"""
        summary = summary_manager.get_principle_summary("U_TEST_1")

        assert summary is not None
        assert summary["id"] == "U_TEST_1"
        assert summary["number"] == 1
        assert summary["title"] == "Test 1"
        assert summary["category"] == "Universal"
        assert summary["severity"] == "critical"
        assert summary["description"] == "Critical principle"
        assert summary["autofix_available"] is True
        assert summary["rules_count"] == 2

    def test_get_principle_summary_not_exists(self, summary_manager) -> None:
        """Test getting summary for non-existent principle"""
        summary = summary_manager.get_principle_summary("NONEXISTENT")

        assert summary is None

    def test_get_statistics(self, summary_manager) -> None:
        """Test getting principle statistics"""
        stats = summary_manager.get_statistics()

        assert stats["version"] == VERSION
        assert stats["total_principles"] == 2
        assert stats["by_severity"]["critical"] == 1
        assert stats["by_severity"]["high"] == 1
        assert stats["by_severity"]["medium"] == 0
        assert stats["by_severity"]["low"] == 0
        assert stats["by_category"]["Universal"] == 1
        assert stats["by_category"]["Testing"] == 1
        assert stats["autofix_available"] == 1


class TestPrincipleSelection:
    """Test principle selection strategies"""

    @pytest.fixture
    def selection_manager(self, principles_manager_factory) -> PrinciplesManager:
        """Create a test manager with sample principles for selection tests"""
        return principles_manager_factory(
            [
                {
                    "id": "U_CRITICAL",
                    "number": 1,
                    "title": "Critical",
                    "category": "Universal",
                    "severity": "critical",
                    "weight": 10,
                    "description": "Critical",
                    "applicability": {"project_types": ["all"]},
                    "rules": [],
                    "examples": {},
                    "autofix": {},
                },
                {
                    "id": "P_HIGH",
                    "number": 2,
                    "title": "High",
                    "category": "Project",
                    "severity": "high",
                    "weight": 7,
                    "description": "High",
                    "applicability": {"project_types": ["api"], "languages": ["python"]},
                    "rules": [],
                    "examples": {},
                    "autofix": {},
                },
                {
                    "id": "P_MEDIUM",
                    "number": 3,
                    "title": "Medium",
                    "category": "Project",
                    "severity": "medium",
                    "weight": 5,
                    "description": "Medium",
                    "applicability": {
                        "project_types": ["api"],
                        "contexts": ["api_endpoints"],
                    },
                    "rules": [],
                    "examples": {},
                    "autofix": {},
                },
            ],
            selection_strategies={
                "minimal": {"include": ["U_CRITICAL"]},
                "auto": {"rules": []},
            },
        )

    def test_select_principles_comprehensive(self, selection_manager) -> None:
        """Test comprehensive selection strategy"""
        chars = ProjectCharacteristics(
            project_type="api",
            primary_language="python",
            team_size="solo",
            services_count=0,
            privacy_critical=False,
            security_critical=False,
            performance_critical=False,
            has_containers=False,
            has_tests=False,
            contexts=["all"],
        )

        selected = selection_manager.select_principles(chars, strategy="comprehensive")

        assert len(selected) == 3
        assert "U_CRITICAL" in selected
        assert "P_HIGH" in selected
        assert "P_MEDIUM" in selected

    def test_select_principles_minimal(self, selection_manager) -> None:
        """Test minimal selection strategy"""
        chars = ProjectCharacteristics(
            project_type="api",
            primary_language="python",
            team_size="solo",
            services_count=0,
            privacy_critical=False,
            security_critical=False,
            performance_critical=False,
            has_containers=False,
            has_tests=False,
            contexts=["all"],
        )

        selected = selection_manager.select_principles(chars, strategy="minimal")

        assert "U_CRITICAL" in selected

    def test_select_principles_with_user_preferences(self, selection_manager) -> None:
        """Test selection with user preferences"""
        chars = ProjectCharacteristics(
            project_type="api",
            primary_language="python",
            team_size="solo",
            services_count=0,
            privacy_critical=False,
            security_critical=False,
            performance_critical=False,
            has_containers=False,
            has_tests=False,
            contexts=["all"],
        )

        selected = selection_manager.select_principles(
            chars, strategy="minimal", user_preferences=["P_HIGH", "P_MEDIUM"]
        )

        assert "P_HIGH" in selected
        assert "P_MEDIUM" in selected


class TestAutoSelection:
    """Test automatic principle selection"""

    @pytest.fixture
    def auto_manager(self, principles_manager_factory) -> PrinciplesManager:
        """Create a test manager for auto selection tests"""
        return principles_manager_factory(
            [
                {"id": "U_CRITICAL", "number": 1, "title": "Critical", "category": "Universal", "severity": "critical", "weight": 10, "description": "Critical", "applicability": {"project_types": ["all"]}, "rules": [], "examples": {}, "autofix": {}},
                {"id": "P_HIGH_API", "number": 2, "title": "High API", "category": "Project", "severity": "high", "weight": 7, "description": "High", "applicability": {"project_types": ["api"], "languages": ["python"]}, "rules": [], "examples": {}, "autofix": {}},
                {"id": "P_MEDIUM_CONTEXT", "number": 3, "title": "Medium Context", "category": "Project", "severity": "medium", "weight": 5, "description": "Medium", "applicability": {"project_types": ["api"], "contexts": ["api_endpoints"]}, "rules": [], "examples": {}, "autofix": {}},
                {"id": "P_MEDIUM_ALL_CONTEXTS", "number": 4, "title": "Medium All Contexts", "category": "Project", "severity": "medium", "weight": 5, "description": "Medium all contexts", "applicability": {"project_types": ["all"], "contexts": ["all"]}, "rules": [], "examples": {}, "autofix": {}},
            ],
            selection_strategies={"auto": {"rules": []}},
        )

    def test_auto_select_critical(self, auto_manager) -> None:
        """Test auto selection includes critical principles"""
        chars = ProjectCharacteristics(
            project_type="api",
            primary_language="python",
            team_size="solo",
            services_count=0,
            privacy_critical=False,
            security_critical=False,
            performance_critical=False,
            has_containers=False,
            has_tests=False,
            contexts=["api_endpoints"],
        )

        selected = auto_manager.select_principles(chars, strategy="auto")

        assert "U_CRITICAL" in selected

    def test_auto_select_high_severity(self, auto_manager) -> None:
        """Test auto selection includes applicable high severity principles"""
        chars = ProjectCharacteristics(
            project_type="api",
            primary_language="python",
            team_size="solo",
            services_count=0,
            privacy_critical=False,
            security_critical=False,
            performance_critical=False,
            has_containers=False,
            has_tests=False,
            contexts=["api_endpoints"],
        )

        selected = auto_manager.select_principles(chars, strategy="auto")

        assert "P_HIGH_API" in selected

    def test_auto_select_medium_with_context(self, auto_manager) -> None:
        """Test auto selection includes medium severity with matching context"""
        chars = ProjectCharacteristics(
            project_type="api",
            primary_language="python",
            team_size="solo",
            services_count=0,
            privacy_critical=False,
            security_critical=False,
            performance_critical=False,
            has_containers=False,
            has_tests=False,
            contexts=["api_endpoints"],
        )

        selected = auto_manager.select_principles(chars, strategy="auto")

        assert "P_MEDIUM_CONTEXT" in selected

    def test_auto_select_excludes_mismatched_context(self, auto_manager) -> None:
        """Test auto selection excludes medium severity without matching context"""
        chars = ProjectCharacteristics(
            project_type="api",
            primary_language="python",
            team_size="solo",
            services_count=0,
            privacy_critical=False,
            security_critical=False,
            performance_critical=False,
            has_containers=False,
            has_tests=False,
            contexts=["database"],  # Different context
        )

        selected = auto_manager.select_principles(chars, strategy="auto")

        assert "P_MEDIUM_CONTEXT" not in selected

    def test_auto_select_medium_all_contexts(self, auto_manager) -> None:
        """Test auto selection includes medium severity with 'all' contexts"""
        chars = ProjectCharacteristics(
            project_type="api",
            primary_language="python",
            team_size="solo",
            services_count=0,
            privacy_critical=False,
            security_critical=False,
            performance_critical=False,
            has_containers=False,
            has_tests=False,
            contexts=["database"],
        )

        selected = auto_manager.select_principles(chars, strategy="auto")

        assert "P_MEDIUM_ALL_CONTEXTS" in selected

    def test_auto_select_with_strategy_rules(self, auto_manager) -> None:
        """Test auto selection with strategy rules"""
        
        # Add a rule to the auto strategy
        auto_manager.selection_strategies = {
            "auto": {
                "rules": [
                    {
                        "condition": "privacy_critical",
                        "include": ["P_HIGH_API"],
                    }
                ]
            }
        }
        chars = ProjectCharacteristics(
            project_type="api",
            primary_language="python",
            team_size="solo",
            services_count=0,
            privacy_critical=True,
            security_critical=False,
            performance_critical=False,
            has_containers=False,
            has_tests=False,
            contexts=["api_endpoints"],
        )

        selected = auto_manager.select_principles(chars, strategy="auto")

        # Should include based on rule
        assert "P_HIGH_API" in selected


class TestApplicability:
    """Test principle applicability checking"""

    def create_principle(self, applicability: Dict[str, Any]) -> Principle:
        """Create a test principle"""
        return Principle(
            id="TEST",
            number=1,
            title="Test",
            category="Test",
            severity="medium",
            weight=5,
            description="Test",
            applicability=applicability,
            rules=[],
            examples={},
            autofix={},
        )

    def test_is_applicable_all_types(self) -> None:
        """Test applicability with 'all' project types"""
        manager = PrinciplesManager(Path("/tmp/test"))
        principle = self.create_principle({"project_types": ["all"]})
        chars = ProjectCharacteristics(
            project_type="library",
            primary_language="python",
            team_size="solo",
            services_count=0,
            privacy_critical=False,
            security_critical=False,
            performance_critical=False,
            has_containers=False,
            has_tests=False,
            contexts=["all"],
        )

        result = manager._is_applicable(principle, chars)

        assert result is True

    def test_is_applicable_specific_type_match(self) -> None:
        """Test applicability with specific matching project type"""
        manager = PrinciplesManager(Path("/tmp/test"))
        principle = self.create_principle({"project_types": ["api", "web"]})
        chars = ProjectCharacteristics(
            project_type="api",
            primary_language="python",
            team_size="solo",
            services_count=0,
            privacy_critical=False,
            security_critical=False,
            performance_critical=False,
            has_containers=False,
            has_tests=False,
            contexts=["all"],
        )

        result = manager._is_applicable(principle, chars)

        assert result is True

    def test_is_applicable_specific_type_mismatch(self) -> None:
        """Test applicability with specific non-matching project type"""
        manager = PrinciplesManager(Path("/tmp/test"))
        principle = self.create_principle({"project_types": ["api", "web"]})
        chars = ProjectCharacteristics(
            project_type="library",
            primary_language="python",
            team_size="solo",
            services_count=0,
            privacy_critical=False,
            security_critical=False,
            performance_critical=False,
            has_containers=False,
            has_tests=False,
            contexts=["all"],
        )

        result = manager._is_applicable(principle, chars)

        assert result is False

    def test_is_applicable_language_match(self) -> None:
        """Test applicability with matching language"""
        manager = PrinciplesManager(Path("/tmp/test"))
        principle = self.create_principle(
            {"project_types": ["all"], "languages": ["python", "javascript"]}
        )
        chars = ProjectCharacteristics(
            project_type="api",
            primary_language="python",
            team_size="solo",
            services_count=0,
            privacy_critical=False,
            security_critical=False,
            performance_critical=False,
            has_containers=False,
            has_tests=False,
            contexts=["all"],
        )

        result = manager._is_applicable(principle, chars)

        assert result is True

    def test_is_applicable_language_mismatch(self) -> None:
        """Test applicability with non-matching language"""
        manager = PrinciplesManager(Path("/tmp/test"))
        principle = self.create_principle({"project_types": ["all"], "languages": ["go", "rust"]})
        chars = ProjectCharacteristics(
            project_type="api",
            primary_language="python",
            team_size="solo",
            services_count=0,
            privacy_critical=False,
            security_critical=False,
            performance_critical=False,
            has_containers=False,
            has_tests=False,
            contexts=["all"],
        )

        result = manager._is_applicable(principle, chars)

        assert result is False

    def test_is_applicable_context_match(self) -> None:
        """Test applicability with matching context"""
        manager = PrinciplesManager(Path("/tmp/test"))
        principle = self.create_principle(
            {"project_types": ["all"], "contexts": ["api_endpoints", "database"]}
        )
        chars = ProjectCharacteristics(
            project_type="api",
            primary_language="python",
            team_size="solo",
            services_count=0,
            privacy_critical=False,
            security_critical=False,
            performance_critical=False,
            has_containers=False,
            has_tests=False,
            contexts=["database", "web_frontend"],
        )

        result = manager._is_applicable(principle, chars)

        assert result is True

    def test_is_applicable_context_mismatch(self) -> None:
        """Test applicability with non-matching context"""
        manager = PrinciplesManager(Path("/tmp/test"))
        principle = self.create_principle({"project_types": ["all"], "contexts": ["api_endpoints"]})
        chars = ProjectCharacteristics(
            project_type="api",
            primary_language="python",
            team_size="solo",
            services_count=0,
            privacy_critical=False,
            security_critical=False,
            performance_critical=False,
            has_containers=False,
            has_tests=False,
            contexts=["database", "web_frontend"],
        )

        result = manager._is_applicable(principle, chars)

        assert result is False

    def test_is_applicable_with_conditions(self) -> None:
        """Test applicability with conditions that must be met"""
        manager = PrinciplesManager(Path("/tmp/test"))
        principle = self.create_principle(
            {
                "project_types": ["all"],
                "conditions": ["privacy_critical"],
            }
        )

        # Test with privacy_critical = True
        chars = ProjectCharacteristics(
            project_type="api",
            primary_language="python",
            team_size="solo",
            services_count=0,
            privacy_critical=True,
            security_critical=False,
            performance_critical=False,
            has_containers=False,
            has_tests=False,
            contexts=["all"],
        )
        result = manager._is_applicable(principle, chars)
        assert result is True

        # Test with privacy_critical = False
        chars.privacy_critical = False
        result = manager._is_applicable(principle, chars)
        assert result is False


class TestConditionEvaluation:
    """Test condition evaluation logic"""

    def test_evaluate_api_type(self) -> None:
        """Test evaluation of API project type condition"""
        manager = PrinciplesManager(Path("/tmp/test"))
        chars = ProjectCharacteristics(
            project_type="api",
            primary_language="python",
            team_size="solo",
            services_count=0,
            privacy_critical=False,
            security_critical=False,
            performance_critical=False,
            has_containers=False,
            has_tests=False,
            contexts=["all"],
        )

        result = manager._evaluate_condition("project.type == 'api'", chars)

        assert result is True

    def test_evaluate_microservices_type(self) -> None:
        """Test evaluation of microservices type condition"""
        manager = PrinciplesManager(Path("/tmp/test"))
        chars = ProjectCharacteristics(
            project_type="microservices",
            primary_language="python",
            team_size="solo",
            services_count=0,
            privacy_critical=False,
            security_critical=False,
            performance_critical=False,
            has_containers=False,
            has_tests=False,
            contexts=["all"],
        )

        result = manager._evaluate_condition("project.type == 'microservices'", chars)

        assert result is True

    def test_evaluate_privacy_critical(self) -> None:
        """Test evaluation of privacy critical condition"""
        manager = PrinciplesManager(Path("/tmp/test"))
        chars = ProjectCharacteristics(
            project_type="api",
            primary_language="python",
            team_size="solo",
            services_count=0,
            privacy_critical=True,
            security_critical=False,
            performance_critical=False,
            has_containers=False,
            has_tests=False,
            contexts=["all"],
        )

        result = manager._evaluate_condition("privacy_critical == true", chars)
        assert result is True

        result = manager._evaluate_condition("privacy_critical", chars)
        assert result is True

    def test_evaluate_security_critical(self) -> None:
        """Test evaluation of security critical condition"""
        manager = PrinciplesManager(Path("/tmp/test"))
        chars = ProjectCharacteristics(
            project_type="api",
            primary_language="python",
            team_size="solo",
            services_count=0,
            privacy_critical=False,
            security_critical=True,
            performance_critical=False,
            has_containers=False,
            has_tests=False,
            contexts=["all"],
        )

        result = manager._evaluate_condition("security_critical == true", chars)

        assert result is True

    def test_evaluate_performance_critical(self) -> None:
        """Test evaluation of performance critical condition"""
        manager = PrinciplesManager(Path("/tmp/test"))
        chars = ProjectCharacteristics(
            project_type="api",
            primary_language="python",
            team_size="solo",
            services_count=0,
            privacy_critical=False,
            security_critical=False,
            performance_critical=True,
            has_containers=False,
            has_tests=False,
            contexts=["all"],
        )

        result = manager._evaluate_condition("performance_critical == true", chars)

        assert result is True

    def test_evaluate_team_size_large(self) -> None:
        """Test evaluation of large team size condition"""
        manager = PrinciplesManager(Path("/tmp/test"))
        chars = ProjectCharacteristics(
            project_type="api",
            primary_language="python",
            team_size="large",
            services_count=0,
            privacy_critical=False,
            security_critical=False,
            performance_critical=False,
            has_containers=False,
            has_tests=False,
            contexts=["all"],
        )

        result = manager._evaluate_condition("team.size == 'large'", chars)
        assert result is True

        result = manager._evaluate_condition("team_size > 5", chars)
        assert result is True

    def test_evaluate_team_size_medium(self) -> None:
        """Test evaluation of medium team size condition"""
        manager = PrinciplesManager(Path("/tmp/test"))
        chars = ProjectCharacteristics(
            project_type="api",
            primary_language="python",
            team_size="medium",
            services_count=0,
            privacy_critical=False,
            security_critical=False,
            performance_critical=False,
            has_containers=False,
            has_tests=False,
            contexts=["all"],
        )

        result = manager._evaluate_condition("team.size == 'medium'", chars)
        assert result is True

        result = manager._evaluate_condition("team_size > 1", chars)
        assert result is True

    def test_evaluate_team_size_small(self) -> None:
        """Test evaluation of small team size condition"""
        manager = PrinciplesManager(Path("/tmp/test"))
        chars = ProjectCharacteristics(
            project_type="api",
            primary_language="python",
            team_size="small",
            services_count=0,
            privacy_critical=False,
            security_critical=False,
            performance_critical=False,
            has_containers=False,
            has_tests=False,
            contexts=["all"],
        )

        result = manager._evaluate_condition("team_size > 1", chars)
        assert result is True

        result = manager._evaluate_condition("team.size > 1", chars)
        assert result is True

    def test_evaluate_team_size_medium_threshold(self) -> None:
        """Test evaluation of team size > 2 condition"""
        manager = PrinciplesManager(Path("/tmp/test"))
        chars = ProjectCharacteristics(
            project_type="api",
            primary_language="python",
            team_size="medium",
            services_count=0,
            privacy_critical=False,
            security_critical=False,
            performance_critical=False,
            has_containers=False,
            has_tests=False,
            contexts=["all"],
        )

        result = manager._evaluate_condition("team_size > 2", chars)
        assert result is True

        # Test with small team
        chars.team_size = "small"
        result = manager._evaluate_condition("team_size > 2", chars)
        assert result is False

    def test_evaluate_services_count_medium(self) -> None:
        """Test evaluation of medium services count condition"""
        manager = PrinciplesManager(Path("/tmp/test"))
        chars = ProjectCharacteristics(
            project_type="microservices",
            primary_language="python",
            team_size="solo",
            services_count=SERVICE_COUNT_THRESHOLD_MEDIUM + 1,
            privacy_critical=False,
            security_critical=False,
            performance_critical=False,
            has_containers=False,
            has_tests=False,
            contexts=["all"],
        )

        result = manager._evaluate_condition("services > 2", chars)

        assert result is True

    def test_evaluate_services_count_large(self) -> None:
        """Test evaluation of large services count condition"""
        manager = PrinciplesManager(Path("/tmp/test"))
        chars = ProjectCharacteristics(
            project_type="microservices",
            primary_language="python",
            team_size="solo",
            services_count=SERVICE_COUNT_THRESHOLD_LARGE + 1,
            privacy_critical=False,
            security_critical=False,
            performance_critical=False,
            has_containers=False,
            has_tests=False,
            contexts=["all"],
        )

        result = manager._evaluate_condition("services > 3", chars)

        assert result is True

    def test_evaluate_containers(self) -> None:
        """Test evaluation of containers condition"""
        manager = PrinciplesManager(Path("/tmp/test"))
        chars = ProjectCharacteristics(
            project_type="api",
            primary_language="python",
            team_size="solo",
            services_count=0,
            privacy_critical=False,
            security_critical=False,
            performance_critical=False,
            has_containers=True,
            has_tests=False,
            contexts=["all"],
        )

        result = manager._evaluate_condition("containers.runtime != null", chars)
        assert result is True

        result = manager._evaluate_condition("has_containers", chars)
        assert result is True

    def test_evaluate_unknown_condition(self) -> None:
        """Test evaluation of unknown condition defaults to True"""
        manager = PrinciplesManager(Path("/tmp/test"))
        chars = ProjectCharacteristics(
            project_type="api",
            primary_language="python",
            team_size="solo",
            services_count=0,
            privacy_critical=False,
            security_critical=False,
            performance_critical=False,
            has_containers=False,
            has_tests=False,
            contexts=["all"],
        )

        result = manager._evaluate_condition("unknown.condition == true", chars)

        assert result is True

    def test_evaluate_exception_handling(self) -> None:
        """Test evaluation handles exceptions gracefully"""
        manager = PrinciplesManager(Path("/tmp/test"))

        # Create a mock characteristics that will raise an exception when accessed
        class BadCharacteristics:
            @property
            def project_type(self) -> str:
                raise ValueError("Simulated error")

        chars_bad = BadCharacteristics()  # type: ignore

        # Should not crash, should return True on exception
        result = manager._evaluate_condition("project.type == 'api'", chars_bad)  # type: ignore

        assert result is True


class TestCheckConditions:
    """Test condition checking on principles"""

    def test_check_conditions_no_conditions(self) -> None:
        """Test checking when no conditions are specified"""
        manager = PrinciplesManager(Path("/tmp/test"))
        principle = Principle(
            id="TEST",
            number=1,
            title="Test",
            category="Test",
            severity="medium",
            weight=5,
            description="Test",
            applicability={},
            rules=[],
            examples={},
            autofix={},
        )
        chars = ProjectCharacteristics(
            project_type="api",
            primary_language="python",
            team_size="solo",
            services_count=0,
            privacy_critical=False,
            security_critical=False,
            performance_critical=False,
            has_containers=False,
            has_tests=False,
            contexts=["all"],
        )

        result = manager._check_conditions(principle, chars)

        assert result is True

    def test_check_conditions_all_pass(self) -> None:
        """Test checking when all conditions pass"""
        manager = PrinciplesManager(Path("/tmp/test"))
        principle = Principle(
            id="TEST",
            number=1,
            title="Test",
            category="Test",
            severity="medium",
            weight=5,
            description="Test",
            applicability={"conditions": ["project.type == 'api'", "privacy_critical"]},
            rules=[],
            examples={},
            autofix={},
        )
        chars = ProjectCharacteristics(
            project_type="api",
            primary_language="python",
            team_size="solo",
            services_count=0,
            privacy_critical=True,
            security_critical=False,
            performance_critical=False,
            has_containers=False,
            has_tests=False,
            contexts=["all"],
        )

        result = manager._check_conditions(principle, chars)

        assert result is True

    def test_check_conditions_one_fails(self) -> None:
        """Test checking when one condition fails"""
        manager = PrinciplesManager(Path("/tmp/test"))
        principle = Principle(
            id="TEST",
            number=1,
            title="Test",
            category="Test",
            severity="medium",
            weight=5,
            description="Test",
            applicability={"conditions": ["project.type == 'api'", "privacy_critical"]},
            rules=[],
            examples={},
            autofix={},
        )
        chars = ProjectCharacteristics(
            project_type="api",
            primary_language="python",
            team_size="solo",
            services_count=0,
            privacy_critical=False,  # This will fail
            security_critical=False,
            performance_critical=False,
            has_containers=False,
            has_tests=False,
            contexts=["all"],
        )

        result = manager._check_conditions(principle, chars)

        assert result is False


class TestCreateCharacteristicsFromAnalysis:
    """Test creating characteristics from analysis"""

    def test_create_characteristics_full_analysis(self) -> None:
        """Test creating characteristics from complete analysis"""
        analysis: Dict[str, Any] = {
            "type": "api",
            "language": "python",
            "team_size": "small",
            "services": [{"name": "api"}, {"name": "worker"}],
            "privacy_critical": True,
            "security_critical": True,
            "performance_critical": False,
            "containers": {"detected": True, "runtime": "docker"},
            "tests": {"detected": True, "framework": "pytest"},
            "contexts": ["api_endpoints", "database"],
        }

        chars = create_characteristics_from_analysis(analysis)

        assert chars.project_type == "api"
        assert chars.primary_language == "python"
        assert chars.team_size == "small"
        assert chars.services_count == 2
        assert chars.privacy_critical is True
        assert chars.security_critical is True
        assert chars.performance_critical is False
        assert chars.has_containers is True
        assert chars.has_tests is True
        assert chars.contexts == ["api_endpoints", "database"]

    def test_create_characteristics_minimal_analysis(self) -> None:
        """Test creating characteristics from minimal analysis"""
        analysis: Dict[str, Any] = {}

        chars = create_characteristics_from_analysis(analysis)

        assert chars.project_type == "unknown"
        assert chars.primary_language == "unknown"
        assert chars.team_size == "solo"
        assert chars.services_count == 0
        assert chars.privacy_critical is False
        assert chars.security_critical is False
        assert chars.performance_critical is False
        assert chars.has_containers is False
        assert chars.has_tests is False
        assert chars.contexts == ["all"]

    def test_create_characteristics_partial_analysis(self) -> None:
        """Test creating characteristics from partial analysis"""
        analysis: Dict[str, Any] = {
            "type": "web",
            "language": "javascript",
            "containers": {"detected": False},
        }

        chars = create_characteristics_from_analysis(analysis)

        assert chars.project_type == "web"
        assert chars.primary_language == "javascript"
        assert chars.has_containers is False


class TestGetPrinciplesManager:
    """Test singleton factory function"""

    def test_get_principles_manager_default(self) -> None:
        """Test getting default principles manager"""
        # Clear cache first
        get_principles_manager.cache_clear()

        manager = get_principles_manager()

        assert isinstance(manager, PrinciplesManager)
        assert manager.principles_dir is not None

    def test_get_principles_manager_cached(self) -> None:
        """Test that manager is cached"""
        # Clear cache first
        get_principles_manager.cache_clear()

        manager1 = get_principles_manager()
        manager2 = get_principles_manager()

        assert manager1 is manager2

    def test_get_principles_manager_with_dir(self, tmp_path: Path) -> None:
        """Test getting manager with custom directory"""
        # Clear cache first
        get_principles_manager.cache_clear()

        principles_dir = str(tmp_path / "principles")
        manager = get_principles_manager(principles_dir)

        assert isinstance(manager, PrinciplesManager)
