"""Pytest configuration and shared fixtures."""

import shutil
import tempfile
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

from claudecodeoptimizer.core.principles import (
    Principle,
    PrinciplesManager,
)


@pytest.fixture
def project_root() -> Path:
    """Return the project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def content_dir(project_root: Path) -> Path:
    """Return the content directory."""
    return project_root / "content"


@pytest.fixture
def templates_dir(project_root: Path) -> Path:
    """Return the templates directory."""
    return project_root / "templates"


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing"""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    # Cleanup
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def minimal_preferences() -> dict[str, Any]:
    """Minimal valid preferences for testing"""
    return {
        "project_name": "TestProject",
        "project_type": "cli_tool",
        "team_size": "solo",
        "security_stance": "balanced",
        "test_philosophy": "pragmatic",
        "quality_level": "strict",
    }


@pytest.fixture
def principles_manager_factory() -> Callable[[list[dict[str, Any]]], PrinciplesManager]:
    """Factory fixture to create PrinciplesManager with custom principles.

    Usage:
        def test_example(principles_manager_factory):
            principles_data = [
                {
                    "id": "U_TEST",
                    "number": 1,
                    "title": "Test",
                    "category": "Universal",
                    "severity": "critical",
                    "weight": 10,
                    "description": "Test",
                    "applicability": {"project_types": ["all"]},
                    "rules": [],
                    "examples": {},
                    "autofix": {"available": False},
                }
            ]
            manager = principles_manager_factory(principles_data)
    """

    def _create_manager(
        principles_data: list[dict[str, Any]],
        selection_strategies: dict[str, Any] | None = None,
        categories: list[dict[str, str]] | None = None,
        tmp_path: Path | None = None,
    ) -> PrinciplesManager:
        # CRITICAL: Use provided tmp_path (pytest fixture) or create in project .tmp
        # NEVER use system /tmp or global ~/.claude/.tmp/
        if tmp_path is None:
            import tempfile
            from pathlib import Path as PathLib

            project_root = PathLib(__file__).parent.parent
            tmp_base = project_root / ".tmp" / "pytest"
            tmp_base.mkdir(parents=True, exist_ok=True)
            tmp_path = PathLib(tempfile.mkdtemp(dir=tmp_base))

        # Verify tmp_path is safe (within project)
        project_root = Path(__file__).parent.parent
        try:
            tmp_path.resolve().relative_to(project_root)
        except ValueError as err:
            raise ValueError(
                f"Test temp path {tmp_path} is outside project root {project_root}. "
                f"Use pytest's tmp_path fixture or project .tmp/ only."
            ) from err

        manager = PrinciplesManager(tmp_path)
        manager.principles = {}
        for p_data in principles_data:
            principle = Principle(
                id=p_data["id"],
                number=p_data["number"],
                title=p_data["title"],
                category=p_data["category"],
                severity=p_data["severity"],
                weight=p_data["weight"],
                description=p_data["description"],
                applicability=p_data.get("applicability", {}),
                rules=p_data.get("rules", []),
                examples=p_data.get("examples", {}),
                autofix=p_data.get("autofix", {"available": False}),
            )
            manager.principles[p_data["id"]] = principle

        if categories:
            manager.categories = categories

        return manager

    return _create_manager


# Test markers
def pytest_configure(config) -> None:
    """Configure custom pytest markers"""
    config.addinivalue_line("markers", "slow: marks tests as slow")
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "unit: marks tests as unit tests")
