"""
Unit tests for Core Principles Management

Tests principle loading, selection, and management functionality.
Target Coverage: 90%+
"""

from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from claudecodeoptimizer.config import VERSION
from claudecodeoptimizer.core.principles import (
    Principle,
    PrinciplesManager,
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

    def test_init_without_dir(self, tmp_path: Path) -> None:
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
        return principles_manager_factory(
            [
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
            ]
        )

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
