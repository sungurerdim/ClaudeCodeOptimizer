"""Pytest configuration and shared fixtures."""

import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest


@pytest.fixture
def project_root() -> Path:
    """Return the project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing"""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    # Cleanup
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def mock_claude_dir(tmp_path: Path):
    """Create a mock .claude directory structure for testing.

    Creates:
        tmp_path/.claude/
        tmp_path/.claude/commands/
        tmp_path/.claude/agents/
        tmp_path/.claude/rules/cco/

    Yields:
        Path to the mock .claude directory
    """
    claude_dir = tmp_path / ".claude"
    claude_dir.mkdir()
    (claude_dir / "commands").mkdir()
    (claude_dir / "agents").mkdir()
    (claude_dir / "rules" / "cco").mkdir(parents=True)
    yield claude_dir


@pytest.fixture
def mock_content_files(mock_claude_dir: Path):
    """Populate mock .claude directory with sample content files.

    Creates sample command, agent, and rule files for testing.

    Yields:
        Dict with paths to created files
    """
    files = {}

    # Create sample command
    cmd_file = mock_claude_dir / "commands" / "cco-test.md"
    cmd_file.write_text("# Test Command\nTest content")
    files["command"] = cmd_file

    # Create sample agent
    agent_file = mock_claude_dir / "agents" / "cco-test-agent.md"
    agent_file.write_text("# Test Agent\nTest content")
    files["agent"] = agent_file

    # Create sample rules
    for rule in ["core.md", "ai.md"]:
        rule_file = mock_claude_dir / "rules" / "cco" / rule
        rule_file.write_text(f"# {rule}\n- **Test-Rule**: Description")
        files[f"rule_{rule}"] = rule_file

    yield files


@pytest.fixture
def isolated_config(tmp_path: Path):
    """Context manager that isolates config module from real filesystem.

    Patches CLAUDE_DIR and related paths to use tmp_path.
    Useful for testing install/uninstall without touching real config.

    Yields:
        tmp_path for assertions
    """
    claude_dir = tmp_path / ".claude"
    claude_dir.mkdir()

    with (
        patch("claudecodeoptimizer.config.CLAUDE_DIR", claude_dir),
        patch("claudecodeoptimizer.config.COMMANDS_DIR", claude_dir / "commands"),
        patch("claudecodeoptimizer.config.AGENTS_DIR", claude_dir / "agents"),
        patch("claudecodeoptimizer.config.RULES_DIR", claude_dir / "rules" / "cco"),
    ):
        yield tmp_path


# Test markers
def pytest_configure(config) -> None:
    """Configure custom pytest markers"""
    config.addinivalue_line("markers", "slow: marks tests as slow")
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "unit: marks tests as unit tests")
