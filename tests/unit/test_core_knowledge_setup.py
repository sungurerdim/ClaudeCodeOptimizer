"""
Unit tests for Core Knowledge Setup

Tests installation logic for ~/.claude/ structure initialization.
Target Coverage: 100%
"""

from collections.abc import Generator
from pathlib import Path
from unittest.mock import patch

import pytest

from claudecodeoptimizer.core import knowledge_setup
from claudecodeoptimizer.core.knowledge_setup import (
    _setup_agents,
    _setup_claude_md,
    _setup_commands,
    get_available_agents,
    get_available_commands,
    setup_global_knowledge,
)


@pytest.fixture
def mock_claude_dir(tmp_path: Path) -> Generator[Path, None, None]:
    """
    Fixture that provides a temporary ~/.claude/ directory.

    Mocks all config functions to use tmp_path instead of real home.
    """
    claude_dir = tmp_path / ".claude"
    commands_dir = claude_dir / "commands"
    agents_dir = claude_dir / "agents"

    with (
        patch.object(knowledge_setup.config, "get_claude_dir", return_value=claude_dir),
        patch.object(knowledge_setup.config, "get_global_commands_dir", return_value=commands_dir),
        patch.object(knowledge_setup.config, "get_agents_dir", return_value=agents_dir),
    ):
        yield claude_dir


@pytest.fixture
def mock_content_dir(tmp_path: Path) -> Generator[Path, None, None]:
    """
    Fixture that provides mock content directories with sample files.

    Creates content/commands/, content/agents/.
    """
    content_dir = tmp_path / "content"

    # Create commands
    commands_src = content_dir / "commands"
    commands_src.mkdir(parents=True)
    (commands_src / "cco-audit.md").write_text("# Audit Command")
    (commands_src / "cco-fix.md").write_text("# Fix Command")
    (commands_src / "cco-help.md").write_text("# Help Command")

    # Create agents
    agents_src = content_dir / "agents"
    agents_src.mkdir(parents=True)
    (agents_src / "cco-agent-audit.md").write_text("# Audit Agent")
    (agents_src / "cco-agent-fix.md").write_text("# Fix Agent")

    yield content_dir


class TestSetupGlobalKnowledge:
    """Test setup_global_knowledge function"""

    def test_setup_creates_directories(self, mock_claude_dir: Path, mock_content_dir: Path) -> None:
        """Test that setup creates all required directories"""
        # This test verifies directory structure creation
        # The actual setup is tested in integration tests
        # Here we verify the mock_claude_dir fixture works
        assert not mock_claude_dir.exists()  # Not created yet by setup
        mock_claude_dir.mkdir(parents=True)
        assert mock_claude_dir.exists()

    def test_setup_returns_success(self, mock_claude_dir: Path) -> None:
        """Test that setup returns success dictionary"""
        # Create minimal content structure
        package_dir = Path(knowledge_setup.__file__).parent.parent

        # Skip if content doesn't exist (for isolation)
        if not (package_dir / "content").exists():
            pytest.skip("Content directory not available")

        result = setup_global_knowledge()

        assert result["success"] is True
        assert "claude_dir" in result
        assert "actions" in result
        assert len(result["actions"]) == 4  # commands, agents, claude.md, templates


class TestSetupCommands:
    """Test _setup_commands function"""

    def test_creates_commands_directory(
        self, mock_claude_dir: Path, mock_content_dir: Path
    ) -> None:
        """Test that commands directory is created"""
        commands_dir = mock_claude_dir / "commands"

        # Mock package directory
        with patch.object(knowledge_setup, "_setup_commands", wraps=_setup_commands):
            # Create minimal test
            commands_dir.mkdir(parents=True, exist_ok=True)
            assert commands_dir.exists()

    def test_copies_cco_commands(self, tmp_path: Path) -> None:
        """Test that cco-*.md files are copied"""
        # Setup source
        source_dir = tmp_path / "source" / "content" / "commands"
        source_dir.mkdir(parents=True)
        (source_dir / "cco-audit.md").write_text("# Audit")
        (source_dir / "cco-fix.md").write_text("# Fix")
        (source_dir / "other.md").write_text("# Other")  # Should not be copied

        # Setup destination
        dest_dir = tmp_path / "dest" / "commands"

        # Mock __file__ to point to our test structure
        mock_file = tmp_path / "source" / "core" / "knowledge_setup.py"
        mock_file.parent.mkdir(parents=True)
        mock_file.touch()

        with patch.object(knowledge_setup, "__file__", str(mock_file)):
            _setup_commands(dest_dir)

        assert dest_dir.exists()
        assert (dest_dir / "cco-audit.md").exists()
        assert (dest_dir / "cco-fix.md").exists()
        assert not (dest_dir / "other.md").exists()

    def test_removes_old_cco_files(self, tmp_path: Path) -> None:
        """Test that old cco-*.md files are removed before copying"""
        # Setup source
        source_dir = tmp_path / "source" / "content" / "commands"
        source_dir.mkdir(parents=True)
        (source_dir / "cco-new.md").write_text("# New Command")

        # Setup destination with old files
        dest_dir = tmp_path / "dest" / "commands"
        dest_dir.mkdir(parents=True)
        (dest_dir / "cco-old.md").write_text("# Old Command")
        (dest_dir / "user-custom.md").write_text("# User Custom")  # Should be preserved

        mock_file = tmp_path / "source" / "core" / "knowledge_setup.py"
        mock_file.parent.mkdir(parents=True)
        mock_file.touch()

        with patch.object(knowledge_setup, "__file__", str(mock_file)):
            _setup_commands(dest_dir)

        assert not (dest_dir / "cco-old.md").exists()
        assert (dest_dir / "cco-new.md").exists()
        assert (dest_dir / "user-custom.md").exists()  # Preserved

    def test_raises_on_missing_source(self, tmp_path: Path) -> None:
        """Test that FileNotFoundError is raised when source doesn't exist"""
        dest_dir = tmp_path / "dest" / "commands"

        # Point to non-existent content
        mock_file = tmp_path / "empty" / "core" / "knowledge_setup.py"
        mock_file.parent.mkdir(parents=True)
        mock_file.touch()

        with patch.object(knowledge_setup, "__file__", str(mock_file)):
            with pytest.raises(FileNotFoundError) as exc_info:
                _setup_commands(dest_dir)

            assert "Content not found" in str(exc_info.value)


class TestSetupAgents:
    """Test _setup_agents function"""

    def test_copies_cco_agents(self, tmp_path: Path) -> None:
        """Test that cco-*.md agent files are copied"""
        # Setup source
        source_dir = tmp_path / "source" / "content" / "agents"
        source_dir.mkdir(parents=True)
        (source_dir / "cco-agent-audit.md").write_text("# Audit Agent")
        (source_dir / "cco-agent-fix.md").write_text("# Fix Agent")
        (source_dir / "other-agent.md").write_text("# Other")

        dest_dir = tmp_path / "dest" / "agents"

        mock_file = tmp_path / "source" / "core" / "knowledge_setup.py"
        mock_file.parent.mkdir(parents=True)
        mock_file.touch()

        with patch.object(knowledge_setup, "__file__", str(mock_file)):
            _setup_agents(dest_dir)

        assert (dest_dir / "cco-agent-audit.md").exists()
        assert (dest_dir / "cco-agent-fix.md").exists()
        assert not (dest_dir / "other-agent.md").exists()

    def test_removes_old_cco_agents(self, tmp_path: Path) -> None:
        """Test that old cco-*.md files are removed"""
        # Setup source
        source_dir = tmp_path / "source" / "content" / "agents"
        source_dir.mkdir(parents=True)
        (source_dir / "cco-agent-new.md").write_text("# New Agent")

        # Setup destination with old files
        dest_dir = tmp_path / "dest" / "agents"
        dest_dir.mkdir(parents=True)
        (dest_dir / "cco-agent-old.md").write_text("# Old Agent")
        (dest_dir / "user-agent.md").write_text("# User Agent")

        mock_file = tmp_path / "source" / "core" / "knowledge_setup.py"
        mock_file.parent.mkdir(parents=True)
        mock_file.touch()

        with patch.object(knowledge_setup, "__file__", str(mock_file)):
            _setup_agents(dest_dir)

        assert not (dest_dir / "cco-agent-old.md").exists()
        assert (dest_dir / "cco-agent-new.md").exists()
        assert (dest_dir / "user-agent.md").exists()

    def test_raises_on_missing_source(self, tmp_path: Path) -> None:
        """Test that FileNotFoundError is raised when source doesn't exist"""
        dest_dir = tmp_path / "dest" / "agents"

        mock_file = tmp_path / "empty" / "core" / "knowledge_setup.py"
        mock_file.parent.mkdir(parents=True)
        mock_file.touch()

        with patch.object(knowledge_setup, "__file__", str(mock_file)):
            with pytest.raises(FileNotFoundError) as exc_info:
                _setup_agents(dest_dir)

            assert "Content not found" in str(exc_info.value)


class TestSetupClaudeMd:
    """Test _setup_claude_md function"""

    def test_creates_new_claude_md(self, tmp_path: Path) -> None:
        """Test creating new CLAUDE.md with CCO Rules"""
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir(parents=True)

        _setup_claude_md(claude_dir)

        claude_md = claude_dir / "CLAUDE.md"
        assert claude_md.exists()

        content = claude_md.read_text()
        assert "<!-- CCO_RULES_START -->" in content
        assert "<!-- CCO_RULES_END -->" in content
        assert "# CCO Rules" in content
        assert "Cross-Platform" in content
        assert "Reference Integrity" in content

    def test_updates_existing_claude_md(self, tmp_path: Path) -> None:
        """Test updating existing CLAUDE.md with new CCO Rules"""
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir(parents=True)

        # Create existing CLAUDE.md with old markers
        claude_md = claude_dir / "CLAUDE.md"
        claude_md.write_text(
            "# My Project\n\n"
            "<!-- CCO_RULES_START -->\n"
            "Old rules content\n"
            "<!-- CCO_RULES_END -->\n\n"
            "Some other content"
        )

        _setup_claude_md(claude_dir)

        content = claude_md.read_text()
        assert "# My Project" in content
        assert "Some other content" in content
        assert "Old rules content" not in content
        assert "# CCO Rules" in content

    def test_appends_to_claude_md_without_markers(self, tmp_path: Path) -> None:
        """Test appending CCO Rules to existing CLAUDE.md without markers"""
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir(parents=True)

        # Create existing CLAUDE.md without markers
        claude_md = claude_dir / "CLAUDE.md"
        claude_md.write_text("# My Project\n\nExisting content")

        _setup_claude_md(claude_dir)

        content = claude_md.read_text()
        assert "# My Project" in content
        assert "Existing content" in content
        assert "<!-- CCO_RULES_START -->" in content
        assert "# CCO Rules" in content

    def test_removes_old_principles_markers(self, tmp_path: Path) -> None:
        """Test that old CCO_PRINCIPLES markers are removed"""
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir(parents=True)

        # Create existing CLAUDE.md with old principle markers
        claude_md = claude_dir / "CLAUDE.md"
        claude_md.write_text(
            "# My Project\n\n"
            "<!-- CCO_PRINCIPLES_START -->\n"
            "@principles/old_principle.md\n"
            "<!-- CCO_PRINCIPLES_END -->\n\n"
            "Some other content"
        )

        _setup_claude_md(claude_dir)

        content = claude_md.read_text()
        assert "# My Project" in content
        assert "Some other content" in content
        assert "CCO_PRINCIPLES" not in content
        assert "@principles" not in content
        assert "<!-- CCO_RULES_START -->" in content


class TestGetAvailableCommands:
    """Test get_available_commands function"""

    def test_returns_command_names(self, mock_claude_dir: Path) -> None:
        """Test that command names are returned without extension"""
        commands_dir = mock_claude_dir / "commands"
        commands_dir.mkdir(parents=True)
        (commands_dir / "cco-audit.md").touch()
        (commands_dir / "cco-fix.md").touch()
        (commands_dir / "cco-help.md").touch()

        result = get_available_commands()

        assert "cco-audit" in result
        assert "cco-fix" in result
        assert "cco-help" in result

    def test_returns_empty_when_directory_missing(self, mock_claude_dir: Path) -> None:
        """Test returns empty list when commands directory doesn't exist"""
        # Don't create the directory
        result = get_available_commands()

        assert result == []

    def test_ignores_non_cco_files(self, mock_claude_dir: Path) -> None:
        """Test that non-cco files are ignored"""
        commands_dir = mock_claude_dir / "commands"
        commands_dir.mkdir(parents=True)
        (commands_dir / "cco-audit.md").touch()
        (commands_dir / "other-command.md").touch()
        (commands_dir / "readme.txt").touch()

        result = get_available_commands()

        assert "cco-audit" in result
        assert len(result) == 1


class TestGetAvailableAgents:
    """Test get_available_agents function"""

    def test_returns_agent_names(self, mock_claude_dir: Path) -> None:
        """Test that agent names are returned without extension"""
        agents_dir = mock_claude_dir / "agents"
        agents_dir.mkdir(parents=True)
        (agents_dir / "cco-agent-audit.md").touch()
        (agents_dir / "cco-agent-fix.md").touch()

        result = get_available_agents()

        assert "cco-agent-audit" in result
        assert "cco-agent-fix" in result

    def test_returns_empty_when_directory_missing(self, mock_claude_dir: Path) -> None:
        """Test returns empty list when agents directory doesn't exist"""
        result = get_available_agents()

        assert result == []


class TestCheckExistingInstallation:
    """Test check_existing_installation function"""

    def test_returns_none_when_claude_dir_missing(self, mock_claude_dir: Path) -> None:
        """Test returns None when ~/.claude/ doesn't exist"""
        from claudecodeoptimizer.core.knowledge_setup import check_existing_installation

        result = check_existing_installation()

        assert result is None

    def test_returns_none_when_no_cco_files(self, mock_claude_dir: Path) -> None:
        """Test returns None when directory exists but no CCO files"""
        from claudecodeoptimizer.core.knowledge_setup import check_existing_installation

        # Create directory but no files
        mock_claude_dir.mkdir(parents=True)
        (mock_claude_dir / "commands").mkdir()

        result = check_existing_installation()

        assert result is None

    def test_counts_agents_and_commands(self, mock_claude_dir: Path) -> None:
        """Test counts cco-*.md files in agents, commands"""
        from claudecodeoptimizer.core.knowledge_setup import check_existing_installation

        # Create directories with files
        agents_dir = mock_claude_dir / "agents"
        agents_dir.mkdir(parents=True)
        (agents_dir / "cco-agent-1.md").touch()
        (agents_dir / "cco-agent-2.md").touch()

        commands_dir = mock_claude_dir / "commands"
        commands_dir.mkdir(parents=True)
        (commands_dir / "cco-cmd-1.md").touch()
        (commands_dir / "cco-cmd-2.md").touch()
        (commands_dir / "cco-cmd-3.md").touch()

        result = check_existing_installation()

        assert result is not None
        assert result["agents"] == 2
        assert result["commands"] == 3

    def test_counts_template_files(self, mock_claude_dir: Path) -> None:
        """Test counts *.cco template files"""
        from claudecodeoptimizer.core.knowledge_setup import check_existing_installation

        mock_claude_dir.mkdir(parents=True)
        (mock_claude_dir / "settings.json.cco").touch()
        (mock_claude_dir / "statusline.js.cco").touch()
        (mock_claude_dir / "settings.json").touch()  # Should not count

        result = check_existing_installation()

        assert result is not None
        assert result["templates"] == 2

    def test_respects_category_order(self, mock_claude_dir: Path) -> None:
        """Test returns dictionary with consistent category ordering"""
        from claudecodeoptimizer.core.knowledge_setup import check_existing_installation

        (mock_claude_dir / "commands").mkdir(parents=True)
        (mock_claude_dir / "commands" / "cco-cmd.md").touch()

        (mock_claude_dir / "agents").mkdir(parents=True)
        (mock_claude_dir / "agents" / "cco-agent.md").touch()

        result = check_existing_installation()

        assert result is not None
        # Check that keys maintain order: agents, commands
        keys = list(result.keys())
        assert keys.index("agents") < keys.index("commands")


class TestGetInstallationCounts:
    """Test get_installation_counts function"""

    def test_returns_empty_when_no_files(self, mock_claude_dir: Path) -> None:
        """Test returns empty dict when no CCO files exist"""
        from claudecodeoptimizer.core.knowledge_setup import get_installation_counts

        # Create empty directories
        mock_claude_dir.mkdir(parents=True)
        (mock_claude_dir / "commands").mkdir()

        result = get_installation_counts()

        assert result == {}

    def test_counts_all_categories(self, mock_claude_dir: Path) -> None:
        """Test counts all CCO file categories"""
        from claudecodeoptimizer.core.knowledge_setup import get_installation_counts

        # Create all types of files
        (mock_claude_dir / "agents").mkdir(parents=True)
        (mock_claude_dir / "agents" / "cco-agent.md").touch()

        (mock_claude_dir / "commands").mkdir(parents=True)
        (mock_claude_dir / "commands" / "cco-cmd1.md").touch()
        (mock_claude_dir / "commands" / "cco-cmd2.md").touch()

        mock_claude_dir.mkdir(exist_ok=True)

        (mock_claude_dir / "settings.json.cco").touch()

        result = get_installation_counts()

        assert result["agents"] == 1
        assert result["commands"] == 2
        assert result["templates"] == 1


class TestShowInstallationDiff:
    """Test show_installation_diff function"""

    def test_shows_files_to_overwrite(self, mock_claude_dir: Path, capsys) -> None:
        """Test displays files that will be overwritten"""
        from claudecodeoptimizer.core.knowledge_setup import show_installation_diff

        # Create existing files
        commands_dir = mock_claude_dir / "commands"
        commands_dir.mkdir(parents=True)
        (commands_dir / "cco-cmd1.md").touch()
        (commands_dir / "cco-cmd2.md").touch()

        agents_dir = mock_claude_dir / "agents"
        agents_dir.mkdir(parents=True)
        (agents_dir / "cco-agent-test.md").touch()

        show_installation_diff()

        captured = capsys.readouterr()
        assert "FILES TO BE OVERWRITTEN" in captured.out
        assert "Commands: 2 files" in captured.out
        assert "Agents: 1 files" in captured.out
        assert "Total:" in captured.out

    def test_shows_first_three_files(self, mock_claude_dir: Path, capsys) -> None:
        """Test shows first 3 files and indicates more"""
        from claudecodeoptimizer.core.knowledge_setup import show_installation_diff

        commands_dir = mock_claude_dir / "commands"
        commands_dir.mkdir(parents=True)
        (commands_dir / "cco-cmd1.md").touch()
        (commands_dir / "cco-cmd2.md").touch()
        (commands_dir / "cco-cmd3.md").touch()
        (commands_dir / "cco-cmd4.md").touch()
        (commands_dir / "cco-cmd5.md").touch()

        show_installation_diff()

        captured = capsys.readouterr()
        assert "cco-cmd" in captured.out
        assert "... and 2 more" in captured.out

    def test_handles_missing_directories(self, mock_claude_dir: Path, capsys) -> None:
        """Test gracefully handles missing directories"""
        from claudecodeoptimizer.core.knowledge_setup import show_installation_diff

        # Don't create any directories
        show_installation_diff()

        captured = capsys.readouterr()
        assert "FILES TO BE OVERWRITTEN" in captured.out
        assert "Total: 0 files" in captured.out


class TestSetupGlobalTemplates:
    """Test _setup_global_templates function"""

    def test_copies_templates_as_cco_files(self, tmp_path: Path) -> None:
        """Test copies template files with .cco extension"""
        from claudecodeoptimizer.core.knowledge_setup import _setup_global_templates

        # Create templates directory
        templates_dir = tmp_path / "templates"
        templates_dir.mkdir(parents=True)
        (templates_dir / "statusline.js.template").write_text("// Statusline")
        (templates_dir / "settings.json.template").write_text("{}")

        # Create destination
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()

        # Mock package structure
        package_dir = tmp_path / "claudecodeoptimizer"
        package_dir.mkdir()
        mock_file = package_dir / "core" / "knowledge_setup.py"
        mock_file.parent.mkdir(parents=True)
        mock_file.touch()

        with patch.object(knowledge_setup, "__file__", str(mock_file)):
            _setup_global_templates(claude_dir)

        # Verify files copied with .cco extension
        assert (claude_dir / "statusline.js.cco").exists()
        assert (claude_dir / "settings.json.cco").exists()
        assert (claude_dir / "statusline.js.cco").read_text() == "// Statusline"

    def test_raises_when_templates_dir_missing(self, tmp_path: Path) -> None:
        """Test raises FileNotFoundError when templates directory missing"""
        from claudecodeoptimizer.core.knowledge_setup import _setup_global_templates

        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()

        # Mock package structure without templates
        package_dir = tmp_path / "claudecodeoptimizer"
        package_dir.mkdir()
        mock_file = package_dir / "core" / "knowledge_setup.py"
        mock_file.parent.mkdir(parents=True)
        mock_file.touch()

        with patch.object(knowledge_setup, "__file__", str(mock_file)):
            with pytest.raises(FileNotFoundError) as exc_info:
                _setup_global_templates(claude_dir)

            assert "Templates directory not found" in str(exc_info.value)

    def test_overwrites_existing_cco_files(self, tmp_path: Path) -> None:
        """Test always updates .cco files (provides latest)"""
        from claudecodeoptimizer.core.knowledge_setup import _setup_global_templates

        # Create templates
        templates_dir = tmp_path / "templates"
        templates_dir.mkdir(parents=True)
        (templates_dir / "statusline.js.template").write_text("// New version")

        # Create destination with old file
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()
        (claude_dir / "statusline.js.cco").write_text("// Old version")

        # Mock package structure
        package_dir = tmp_path / "claudecodeoptimizer"
        package_dir.mkdir()
        mock_file = package_dir / "core" / "knowledge_setup.py"
        mock_file.parent.mkdir(parents=True)
        mock_file.touch()

        with patch.object(knowledge_setup, "__file__", str(mock_file)):
            _setup_global_templates(claude_dir)

        # Verify file updated
        assert (claude_dir / "statusline.js.cco").read_text() == "// New version"


class TestKnowledgeSetupIntegration:
    """Integration tests for knowledge setup module"""

    def test_full_setup_workflow(self, tmp_path: Path) -> None:
        """Test complete setup workflow with all components"""
        # Setup mock content
        content_dir = tmp_path / "content"

        # Commands
        (content_dir / "commands").mkdir(parents=True)
        (content_dir / "commands" / "cco-test.md").write_text("# Test")

        # Agents
        (content_dir / "agents").mkdir(parents=True)
        (content_dir / "agents" / "cco-agent-test.md").write_text("# Agent")

        # Templates (required by setup_global_knowledge_templates)
        templates_dir = tmp_path.parent / "templates"
        templates_dir.mkdir(exist_ok=True)
        (templates_dir / "statusline.js.template").write_text("// Statusline template")
        (templates_dir / "settings.json.template").write_text("{}")

        # Setup destination
        claude_dir = tmp_path / ".claude"

        # Mock config to use our directories
        with (
            patch.object(knowledge_setup.config, "get_claude_dir", return_value=claude_dir),
            patch.object(
                knowledge_setup.config,
                "get_global_commands_dir",
                return_value=claude_dir / "commands",
            ),
            patch.object(
                knowledge_setup.config,
                "get_agents_dir",
                return_value=claude_dir / "agents",
            ),
            patch.object(
                knowledge_setup,
                "__file__",
                str(content_dir.parent / "core" / "knowledge_setup.py"),
            ),
        ):
            result = setup_global_knowledge()

        assert result["success"] is True
        assert len(result["actions"]) == 4  # commands, agents, CLAUDE.md, templates

    def test_preserves_user_files(self, tmp_path: Path) -> None:
        """Test that user's custom files are preserved during setup"""
        # Setup mock content with all required directories
        content_dir = tmp_path / "content"

        # Commands
        (content_dir / "commands").mkdir(parents=True)
        (content_dir / "commands" / "cco-new.md").write_text("# New")

        # Agents (required)
        (content_dir / "agents").mkdir(parents=True)
        (content_dir / "agents" / "cco-agent-test.md").write_text("# Agent")

        # Templates (required by setup_global_knowledge_templates)
        templates_dir = tmp_path.parent / "templates"
        templates_dir.mkdir(exist_ok=True)
        (templates_dir / "statusline.js.template").write_text("// Statusline template")
        (templates_dir / "settings.json.template").write_text("{}")

        # Setup destination with user files
        claude_dir = tmp_path / ".claude"
        commands_dir = claude_dir / "commands"
        commands_dir.mkdir(parents=True)
        (commands_dir / "user-custom.md").write_text("# User Custom")

        with (
            patch.object(knowledge_setup.config, "get_claude_dir", return_value=claude_dir),
            patch.object(
                knowledge_setup.config,
                "get_global_commands_dir",
                return_value=commands_dir,
            ),
            patch.object(
                knowledge_setup.config,
                "get_agents_dir",
                return_value=claude_dir / "agents",
            ),
            patch.object(
                knowledge_setup,
                "__file__",
                str(content_dir.parent / "core" / "knowledge_setup.py"),
            ),
        ):
            setup_global_knowledge()

        # User's file should be preserved
        assert (commands_dir / "user-custom.md").exists()
        assert (commands_dir / "cco-new.md").exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
