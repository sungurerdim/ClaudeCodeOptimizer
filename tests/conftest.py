"""Pytest configuration and shared fixtures."""

import shutil
import tempfile
from pathlib import Path
from typing import Any, Dict

import pytest


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
def minimal_preferences() -> Dict[str, Any]:
    """Minimal valid preferences for testing"""
    return {
        "project_name": "TestProject",
        "project_type": "cli_tool",
        "team_size": "solo",
        "security_stance": "balanced",
        "test_philosophy": "pragmatic",
        "quality_level": "strict",
    }


# Test markers
def pytest_configure(config) -> None:
    """Configure custom pytest markers"""
    config.addinivalue_line("markers", "slow: marks tests as slow")
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "unit: marks tests as unit tests")
