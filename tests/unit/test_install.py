"""Unit tests for install module."""

from pathlib import Path
from unittest.mock import patch

import pytest

from claudecodeoptimizer.install import (
    _check_claude_dir,
    _setup_content,
    clean_claude_md,
    clean_previous_installation,
    setup_agents,
    setup_commands,
    setup_rules,
)


class TestCheckClaudeDir:
    """Test _check_claude_dir function."""

    def test_returns_none_when_dir_exists(self, tmp_path: Path) -> None:
        """Test _check_claude_dir returns None when directory exists."""
        with patch("claudecodeoptimizer.install.CLAUDE_DIR", tmp_path):
            result = _check_claude_dir()
            assert result is None

    def test_returns_error_when_dir_missing(self, tmp_path: Path) -> None:
        """Test _check_claude_dir returns error when directory doesn't exist."""
        nonexistent = tmp_path / "nonexistent"
        with patch("claudecodeoptimizer.install.CLAUDE_DIR", nonexistent):
            result = _check_claude_dir()
            assert result is not None
            assert "~/.claude/ not found" in result


class TestSetupContent:
    """Test _setup_content function."""

    def test_copies_files_to_destination(self, tmp_path: Path) -> None:
        """Test _setup_content copies cco-*.md files to destination."""
        # Create source directory with test files
        src_dir = tmp_path / "source"
        src_dir.mkdir()
        (src_dir / "cco-test1.md").write_text("test1")
        (src_dir / "cco-test2.md").write_text("test2")

        # Create destination directory
        dest_dir = tmp_path / "dest"

        with patch("claudecodeoptimizer.install.get_content_path", return_value=src_dir):
            result = _setup_content("command-templates", dest_dir, verbose=False)

        assert len(result) == 2
        assert "cco-test1.md" in result
        assert "cco-test2.md" in result
        assert (dest_dir / "cco-test1.md").read_text() == "test1"
        assert (dest_dir / "cco-test2.md").read_text() == "test2"

    def test_removes_existing_files_before_copy(self, tmp_path: Path) -> None:
        """Test _setup_content removes existing cco-*.md files before copying."""
        # Create source directory
        src_dir = tmp_path / "source"
        src_dir.mkdir()
        (src_dir / "cco-new.md").write_text("new content")

        # Create destination with old file
        dest_dir = tmp_path / "dest"
        dest_dir.mkdir()
        old_file = dest_dir / "cco-old.md"
        old_file.write_text("old content")

        with patch("claudecodeoptimizer.install.get_content_path", return_value=src_dir):
            result = _setup_content("command-templates", dest_dir, verbose=False)

        # Old file should be removed
        assert not old_file.exists()
        # New file should be copied
        assert (dest_dir / "cco-new.md").exists()
        assert len(result) == 1

    def test_returns_empty_list_when_source_missing(self, tmp_path: Path) -> None:
        """Test _setup_content returns empty list when source doesn't exist."""
        nonexistent = tmp_path / "nonexistent"
        dest_dir = tmp_path / "dest"

        with patch("claudecodeoptimizer.install.get_content_path", return_value=nonexistent):
            result = _setup_content("command-templates", dest_dir, verbose=False)

        assert result == []

    def test_creates_dest_directory_if_missing(self, tmp_path: Path) -> None:
        """Test _setup_content creates destination directory if it doesn't exist."""
        src_dir = tmp_path / "source"
        src_dir.mkdir()
        (src_dir / "cco-test.md").write_text("test")

        dest_dir = tmp_path / "dest" / "nested" / "path"

        with patch("claudecodeoptimizer.install.get_content_path", return_value=src_dir):
            _setup_content("command-templates", dest_dir, verbose=False)

        assert dest_dir.exists()
        assert (dest_dir / "cco-test.md").exists()


class TestSetupCommands:
    """Test setup_commands function."""

    def test_copies_commands_to_commands_dir(self, tmp_path: Path) -> None:
        """Test setup_commands copies commands to ~/.claude/commands/."""
        claude_dir = tmp_path / ".claude"
        commands_dir = claude_dir / "commands"
        claude_dir.mkdir()

        # Create source directory
        src_dir = tmp_path / "source"
        src_dir.mkdir()
        (src_dir / "cco-config.md").write_text("config command")

        with patch("claudecodeoptimizer.install.CLAUDE_DIR", claude_dir):
            with patch("claudecodeoptimizer.install.COMMANDS_DIR", commands_dir):
                with patch("claudecodeoptimizer.install.get_content_path", return_value=src_dir):
                    result = setup_commands(verbose=False)

        assert "cco-config.md" in result
        assert (commands_dir / "cco-config.md").exists()

    def test_raises_error_when_claude_dir_missing(self, tmp_path: Path) -> None:
        """Test setup_commands raises error when ~/.claude/ doesn't exist."""
        nonexistent = tmp_path / "nonexistent"

        with patch("claudecodeoptimizer.install.CLAUDE_DIR", nonexistent):
            with pytest.raises(RuntimeError, match="~/.claude/ not found"):
                setup_commands(verbose=False)


class TestSetupAgents:
    """Test setup_agents function."""

    def test_copies_agents_to_agents_dir(self, tmp_path: Path) -> None:
        """Test setup_agents copies agents to ~/.claude/agents/."""
        claude_dir = tmp_path / ".claude"
        agents_dir = claude_dir / "agents"
        claude_dir.mkdir()

        # Create source directory
        src_dir = tmp_path / "source"
        src_dir.mkdir()
        (src_dir / "cco-apply.md").write_text("apply agent")

        with patch("claudecodeoptimizer.install.CLAUDE_DIR", claude_dir):
            with patch("claudecodeoptimizer.install.AGENTS_DIR", agents_dir):
                with patch("claudecodeoptimizer.install.get_content_path", return_value=src_dir):
                    result = setup_agents(verbose=False)

        assert "cco-apply.md" in result
        assert (agents_dir / "cco-apply.md").exists()

    def test_raises_error_when_claude_dir_missing(self, tmp_path: Path) -> None:
        """Test setup_agents raises error when ~/.claude/ doesn't exist."""
        nonexistent = tmp_path / "nonexistent"

        with patch("claudecodeoptimizer.install.CLAUDE_DIR", nonexistent):
            with pytest.raises(RuntimeError, match="~/.claude/ not found"):
                setup_agents(verbose=False)


class TestSetupRules:
    """Test setup_rules function."""

    def test_copies_rules_to_cco_subdirectory(self, tmp_path: Path) -> None:
        """Test setup_rules copies rules to ~/.claude/rules/cco/."""
        claude_dir = tmp_path / ".claude"
        rules_dir = claude_dir / "rules" / "cco"
        claude_dir.mkdir()

        # Create source directory with rule files
        src_dir = tmp_path / "source"
        src_dir.mkdir()
        (src_dir / "cco-core.md").write_text("core rules")
        (src_dir / "cco-ai.md").write_text("ai rules")

        with patch("claudecodeoptimizer.install.CLAUDE_DIR", claude_dir):
            with patch("claudecodeoptimizer.install.RULES_DIR", rules_dir):
                with patch("claudecodeoptimizer.install.get_content_path", return_value=src_dir):
                    result = setup_rules(verbose=False)

        # Files should be renamed without cco- prefix
        assert (rules_dir / "core.md").exists()
        assert (rules_dir / "ai.md").exists()
        assert result["core"] == 1
        assert result["ai"] == 1
        assert result["total"] == 2

    def test_removes_existing_rules_before_copy(self, tmp_path: Path) -> None:
        """Test setup_rules removes existing rules before copying new ones."""
        claude_dir = tmp_path / ".claude"
        rules_dir = claude_dir / "rules" / "cco"
        rules_dir.mkdir(parents=True)

        # Create old rule files
        (rules_dir / "core.md").write_text("old core")
        (rules_dir / "ai.md").write_text("old ai")

        # Create source directory
        src_dir = tmp_path / "source"
        src_dir.mkdir()
        (src_dir / "cco-core.md").write_text("new core")
        (src_dir / "cco-ai.md").write_text("new ai")

        with patch("claudecodeoptimizer.install.CLAUDE_DIR", claude_dir):
            with patch("claudecodeoptimizer.install.RULES_DIR", rules_dir):
                with patch("claudecodeoptimizer.install.get_content_path", return_value=src_dir):
                    setup_rules(verbose=False)

        # New content should be in place
        assert (rules_dir / "core.md").read_text() == "new core"
        assert (rules_dir / "ai.md").read_text() == "new ai"

    def test_raises_error_when_claude_dir_missing(self, tmp_path: Path) -> None:
        """Test setup_rules raises error when ~/.claude/ doesn't exist."""
        nonexistent = tmp_path / "nonexistent"

        with patch("claudecodeoptimizer.install.CLAUDE_DIR", nonexistent):
            with pytest.raises(RuntimeError, match="~/.claude/ not found"):
                setup_rules(verbose=False)

    def test_returns_zero_counts_when_source_missing(self, tmp_path: Path) -> None:
        """Test setup_rules returns zero counts when source doesn't exist."""
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()
        nonexistent = tmp_path / "nonexistent"

        with patch("claudecodeoptimizer.install.CLAUDE_DIR", claude_dir):
            with patch("claudecodeoptimizer.install.get_content_path", return_value=nonexistent):
                result = setup_rules(verbose=False)

        assert result == {"core": 0, "ai": 0, "tools": 0, "total": 0}


class TestCleanPreviousInstallation:
    """Test clean_previous_installation function."""

    def test_removes_all_previous_cco_files(self, tmp_path: Path) -> None:
        """Test clean_previous_installation removes all CCO files."""
        claude_dir = tmp_path / ".claude"
        commands_dir = claude_dir / "commands"
        agents_dir = claude_dir / "agents"
        rules_dir = claude_dir / "rules"
        cco_rules_dir = rules_dir / "cco"

        # Create directories
        commands_dir.mkdir(parents=True)
        agents_dir.mkdir(parents=True)
        rules_dir.mkdir(parents=True)
        cco_rules_dir.mkdir(parents=True)

        # Create old CCO files
        (commands_dir / "cco-config.md").write_text("old command")
        (agents_dir / "cco-apply.md").write_text("old agent")
        (rules_dir / "cco-core.md").write_text("old root rule")
        (cco_rules_dir / "core.md").write_text("old cco rule")
        (claude_dir / "CLAUDE.md").write_text("<!-- CCO_TEST_START -->content<!-- CCO_TEST_END -->")

        with patch("claudecodeoptimizer.install.CLAUDE_DIR", claude_dir):
            with patch("claudecodeoptimizer.install.COMMANDS_DIR", commands_dir):
                with patch("claudecodeoptimizer.install.AGENTS_DIR", agents_dir):
                    with patch("claudecodeoptimizer.install.RULES_DIR", cco_rules_dir):
                        with patch("claudecodeoptimizer.operations.OLD_RULES_ROOT", rules_dir):
                            result = clean_previous_installation(verbose=False)

        # All old files should be removed
        assert not (commands_dir / "cco-config.md").exists()
        assert not (agents_dir / "cco-apply.md").exists()
        assert not (rules_dir / "cco-core.md").exists()
        assert not (cco_rules_dir / "core.md").exists()

        # Counts should reflect removals
        assert result["commands"] == 1
        assert result["agents"] == 1
        assert result["rules"] >= 2  # At least 2 rule files + possibly CLAUDE.md marker

    def test_returns_zero_when_nothing_to_remove(self, tmp_path: Path) -> None:
        """Test clean_previous_installation returns zero when nothing to remove."""
        claude_dir = tmp_path / ".claude"
        commands_dir = claude_dir / "commands"
        agents_dir = claude_dir / "agents"
        rules_dir = claude_dir / "rules"
        cco_rules_dir = rules_dir / "cco"

        # Create empty directories
        commands_dir.mkdir(parents=True)
        agents_dir.mkdir(parents=True)
        rules_dir.mkdir(parents=True)

        with patch("claudecodeoptimizer.install.CLAUDE_DIR", claude_dir):
            with patch("claudecodeoptimizer.install.COMMANDS_DIR", commands_dir):
                with patch("claudecodeoptimizer.install.AGENTS_DIR", agents_dir):
                    with patch("claudecodeoptimizer.install.RULES_DIR", cco_rules_dir):
                        with patch("claudecodeoptimizer.operations.OLD_RULES_ROOT", rules_dir):
                            result = clean_previous_installation(verbose=False)

        assert result["commands"] == 0
        assert result["agents"] == 0
        assert result["rules"] == 0


class TestCleanClaudeMd:
    """Test clean_claude_md function."""

    def test_removes_cco_markers_from_claude_md(self, tmp_path: Path) -> None:
        """Test clean_claude_md removes CCO markers from CLAUDE.md."""
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()
        claude_md = claude_dir / "CLAUDE.md"

        content = """# My Project

<!-- CCO_STANDARDS_START -->
Old CCO content
<!-- CCO_STANDARDS_END -->

User content here"""

        claude_md.write_text(content)

        with patch("claudecodeoptimizer.install.CLAUDE_DIR", claude_dir):
            result = clean_claude_md(verbose=False)

        # Marker should be removed
        assert result == 1
        new_content = claude_md.read_text()
        assert "CCO_STANDARDS_START" not in new_content
        assert "User content here" in new_content

    def test_returns_zero_when_no_markers(self, tmp_path: Path) -> None:
        """Test clean_claude_md returns zero when no markers to remove."""
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()
        claude_md = claude_dir / "CLAUDE.md"

        content = "# My Project\n\nNo CCO markers here"
        claude_md.write_text(content)

        with patch("claudecodeoptimizer.install.CLAUDE_DIR", claude_dir):
            result = clean_claude_md(verbose=False)

        assert result == 0

    def test_returns_zero_when_file_missing(self, tmp_path: Path) -> None:
        """Test clean_claude_md returns zero when CLAUDE.md doesn't exist."""
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()

        with patch("claudecodeoptimizer.install.CLAUDE_DIR", claude_dir):
            result = clean_claude_md(verbose=False)

        assert result == 0

    def test_deletes_file_when_empty_after_cleanup(self, tmp_path: Path) -> None:
        """Test clean_claude_md deletes file when empty after removing markers."""
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()
        claude_md = claude_dir / "CLAUDE.md"

        # File with only CCO markers
        content = "<!-- CCO_TEST_START -->content<!-- CCO_TEST_END -->"
        claude_md.write_text(content)

        with patch("claudecodeoptimizer.install.CLAUDE_DIR", claude_dir):
            clean_claude_md(verbose=False)

        # File should be deleted
        assert not claude_md.exists()

    def test_normalizes_multiple_newlines(self, tmp_path: Path) -> None:
        """Test clean_claude_md normalizes multiple consecutive newlines."""
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()
        claude_md = claude_dir / "CLAUDE.md"

        content = """# Project

<!-- CCO_TEST_START -->marker<!-- CCO_TEST_END -->


More content"""

        claude_md.write_text(content)

        with patch("claudecodeoptimizer.install.CLAUDE_DIR", claude_dir):
            clean_claude_md(verbose=False)

        new_content = claude_md.read_text()
        # Should not have more than 2 consecutive newlines
        assert "\n\n\n" not in new_content
