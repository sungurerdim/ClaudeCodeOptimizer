"""Unit tests for operations module."""

from pathlib import Path
from unittest.mock import patch

from claudecodeoptimizer.operations import (
    clean_claude_md_markers,
    remove_agent_files,
    remove_all_cco_markers,
    remove_command_files,
    remove_new_rules,
    remove_old_rules,
)


class TestRemoveCommandFiles:
    """Test remove_command_files function."""

    def test_removes_all_cco_command_files(self, tmp_path: Path) -> None:
        """Test remove_command_files removes all cco-*.md files."""
        commands_dir = tmp_path / "commands"
        commands_dir.mkdir()

        # Create CCO command files
        (commands_dir / "cco-config.md").write_text("config")
        (commands_dir / "cco-optimize.md").write_text("optimize")
        # Create non-CCO file (should not be removed)
        (commands_dir / "custom-command.md").write_text("custom")

        count = remove_command_files(commands_dir)

        assert count == 2
        assert not (commands_dir / "cco-config.md").exists()
        assert not (commands_dir / "cco-optimize.md").exists()
        assert (commands_dir / "custom-command.md").exists()

    def test_returns_zero_when_no_files(self, tmp_path: Path) -> None:
        """Test remove_command_files returns zero when no files to remove."""
        commands_dir = tmp_path / "commands"
        commands_dir.mkdir()

        count = remove_command_files(commands_dir)

        assert count == 0

    def test_returns_zero_when_directory_missing(self, tmp_path: Path) -> None:
        """Test remove_command_files returns zero when directory doesn't exist."""
        nonexistent = tmp_path / "nonexistent"

        count = remove_command_files(nonexistent)

        assert count == 0

    def test_uses_global_commands_dir_when_none(self) -> None:
        """Test remove_command_files uses global COMMANDS_DIR when path is None."""
        with patch("claudecodeoptimizer.operations.COMMANDS_DIR") as mock_dir:
            mock_dir.exists.return_value = False
            count = remove_command_files(path=None, verbose=False)
            assert count == 0


class TestRemoveAgentFiles:
    """Test remove_agent_files function."""

    def test_removes_all_cco_agent_files(self, tmp_path: Path) -> None:
        """Test remove_agent_files removes all cco-*.md files."""
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()

        # Create CCO agent files
        (agents_dir / "cco-apply.md").write_text("apply")
        (agents_dir / "cco-audit.md").write_text("audit")
        # Create non-CCO file
        (agents_dir / "custom-agent.md").write_text("custom")

        count = remove_agent_files(agents_dir)

        assert count == 2
        assert not (agents_dir / "cco-apply.md").exists()
        assert not (agents_dir / "cco-audit.md").exists()
        assert (agents_dir / "custom-agent.md").exists()

    def test_returns_zero_when_no_files(self, tmp_path: Path) -> None:
        """Test remove_agent_files returns zero when no files to remove."""
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()

        count = remove_agent_files(agents_dir)

        assert count == 0

    def test_returns_zero_when_directory_missing(self, tmp_path: Path) -> None:
        """Test remove_agent_files returns zero when directory doesn't exist."""
        nonexistent = tmp_path / "nonexistent"

        count = remove_agent_files(nonexistent)

        assert count == 0

    def test_uses_global_agents_dir_when_none(self) -> None:
        """Test remove_agent_files uses global AGENTS_DIR when path is None."""
        with patch("claudecodeoptimizer.operations.AGENTS_DIR") as mock_dir:
            mock_dir.exists.return_value = False
            count = remove_agent_files(path=None, verbose=False)
            assert count == 0


class TestRemoveOldRules:
    """Test remove_old_rules function."""

    def test_removes_old_cco_rule_files_from_root(self, tmp_path: Path) -> None:
        """Test remove_old_rules removes old CCO rule files from rules root."""
        rules_dir = tmp_path / "rules"
        rules_dir.mkdir()

        # Create old CCO rule files in root
        (rules_dir / "cco-core.md").write_text("core")
        (rules_dir / "cco-ai.md").write_text("ai")
        (rules_dir / "cco-adaptive.md").write_text("adaptive")
        (rules_dir / "cco-tools.md").write_text("tools")
        # Create non-CCO file
        (rules_dir / "custom-rule.md").write_text("custom")

        count = remove_old_rules(rules_dir)

        assert count == 4
        assert not (rules_dir / "cco-core.md").exists()
        assert not (rules_dir / "cco-ai.md").exists()
        assert not (rules_dir / "cco-adaptive.md").exists()
        assert not (rules_dir / "cco-tools.md").exists()
        assert (rules_dir / "custom-rule.md").exists()

    def test_returns_zero_when_no_files(self, tmp_path: Path) -> None:
        """Test remove_old_rules returns zero when no files to remove."""
        rules_dir = tmp_path / "rules"
        rules_dir.mkdir()

        count = remove_old_rules(rules_dir)

        assert count == 0

    def test_returns_zero_when_directory_missing(self, tmp_path: Path) -> None:
        """Test remove_old_rules returns zero when directory doesn't exist."""
        nonexistent = tmp_path / "nonexistent"

        count = remove_old_rules(nonexistent)

        assert count == 0

    def test_uses_global_old_rules_root_when_none(self) -> None:
        """Test remove_old_rules uses global OLD_RULES_ROOT when path is None."""
        with patch("claudecodeoptimizer.operations.OLD_RULES_ROOT") as mock_dir:
            mock_dir.exists.return_value = False
            count = remove_old_rules(path=None, verbose=False)
            assert count == 0


class TestRemoveNewRules:
    """Test remove_new_rules function."""

    def test_removes_cco_rules_from_cco_subdirectory(self, tmp_path: Path) -> None:
        """Test remove_new_rules removes CCO rules from cco/ subdirectory."""
        cco_dir = tmp_path / "rules" / "cco"
        cco_dir.mkdir(parents=True)

        # Create CCO rule files (without cco- prefix)
        (cco_dir / "core.md").write_text("core")
        (cco_dir / "ai.md").write_text("ai")
        (cco_dir / "tools.md").write_text("tools")
        (cco_dir / "adaptive.md").write_text("adaptive")
        # Create non-CCO file
        (cco_dir / "custom.md").write_text("custom")

        count = remove_new_rules(cco_dir)

        assert count == 4
        assert not (cco_dir / "core.md").exists()
        assert not (cco_dir / "ai.md").exists()
        assert not (cco_dir / "tools.md").exists()
        assert not (cco_dir / "adaptive.md").exists()
        assert (cco_dir / "custom.md").exists()

    def test_removes_empty_cco_directory(self, tmp_path: Path) -> None:
        """Test remove_new_rules removes empty cco/ directory."""
        cco_dir = tmp_path / "rules" / "cco"
        cco_dir.mkdir(parents=True)

        # Create only CCO rule files
        (cco_dir / "core.md").write_text("core")
        (cco_dir / "ai.md").write_text("ai")

        remove_new_rules(cco_dir)

        # Directory should be removed when empty
        assert not cco_dir.exists()

    def test_does_not_remove_nonempty_cco_directory(self, tmp_path: Path) -> None:
        """Test remove_new_rules doesn't remove cco/ directory if it has other files."""
        cco_dir = tmp_path / "rules" / "cco"
        cco_dir.mkdir(parents=True)

        # Create CCO and custom files
        (cco_dir / "core.md").write_text("core")
        (cco_dir / "custom.md").write_text("custom")

        remove_new_rules(cco_dir)

        # Directory should still exist
        assert cco_dir.exists()
        assert (cco_dir / "custom.md").exists()

    def test_returns_zero_when_no_files(self, tmp_path: Path) -> None:
        """Test remove_new_rules returns zero when no files to remove."""
        cco_dir = tmp_path / "rules" / "cco"
        cco_dir.mkdir(parents=True)

        count = remove_new_rules(cco_dir)

        assert count == 0

    def test_returns_zero_when_directory_missing(self, tmp_path: Path) -> None:
        """Test remove_new_rules returns zero when directory doesn't exist."""
        nonexistent = tmp_path / "nonexistent"

        count = remove_new_rules(nonexistent)

        assert count == 0

    def test_uses_global_rules_dir_when_none(self) -> None:
        """Test remove_new_rules uses global RULES_DIR when path is None."""
        with patch("claudecodeoptimizer.operations.RULES_DIR") as mock_dir:
            mock_dir.exists.return_value = False
            count = remove_new_rules(path=None, verbose=False)
            assert count == 0


class TestRemoveAllCcoMarkers:
    """Test remove_all_cco_markers function."""

    def test_removes_cco_markers_with_uppercase(self) -> None:
        """Test remove_all_cco_markers removes markers with uppercase."""
        content = """# Project

<!-- CCO_STANDARDS_START -->
CCO content here
<!-- CCO_STANDARDS_END -->

User content"""

        result, count = remove_all_cco_markers(content)

        assert count == 1
        assert "CCO_STANDARDS_START" not in result
        assert "User content" in result

    def test_removes_cco_markers_with_lowercase(self) -> None:
        """Test remove_all_cco_markers removes markers with lowercase."""
        content = """# Project

<!-- cco-standards-start -->
CCO content here
<!-- cco-standards-end -->

User content"""

        result, count = remove_all_cco_markers(content)

        assert count == 1
        assert "cco-standards-start" not in result
        assert "User content" in result

    def test_removes_multiple_different_markers(self) -> None:
        """Test remove_all_cco_markers removes multiple different markers."""
        content = """# Project

<!-- CCO_STANDARDS_START -->
standards content
<!-- CCO_STANDARDS_END -->

<!-- CCO_ADAPTIVE_START -->
adaptive content
<!-- CCO_ADAPTIVE_END -->

User content"""

        result, count = remove_all_cco_markers(content)

        assert count == 2
        assert "CCO_STANDARDS_START" not in result
        assert "CCO_ADAPTIVE_START" not in result
        assert "User content" in result

    def test_removes_markers_with_mixed_naming(self) -> None:
        """Test remove_all_cco_markers handles markers with different naming styles."""
        content = """# Project

<!-- CCO_SNAKE_CASE_START -->
content1
<!-- CCO_SNAKE_CASE_END -->

<!-- CCO_ANOTHER_CASE_START -->
content2
<!-- CCO_ANOTHER_CASE_END -->

User content"""

        result, count = remove_all_cco_markers(content)

        assert count == 2
        assert "CCO_SNAKE_CASE" not in result
        assert "CCO_ANOTHER_CASE" not in result
        assert "User content" in result

    def test_returns_zero_when_no_markers(self) -> None:
        """Test remove_all_cco_markers returns zero when no markers found."""
        content = "# Project\n\nNo CCO markers here"

        result, count = remove_all_cco_markers(content)

        assert count == 0
        assert result == content

    def test_preserves_non_cco_comments(self) -> None:
        """Test remove_all_cco_markers preserves non-CCO HTML comments."""
        content = """# Project

<!-- This is a user comment -->
User content
<!-- Another comment -->"""

        result, count = remove_all_cco_markers(content)

        assert count == 0
        assert "This is a user comment" in result
        assert "Another comment" in result


class TestCleanClaudeMdMarkers:
    """Test clean_claude_md_markers function."""

    def test_removes_markers_from_file(self, tmp_path: Path) -> None:
        """Test clean_claude_md_markers removes markers from CLAUDE.md file."""
        claude_md = tmp_path / "CLAUDE.md"
        content = """# Project

<!-- CCO_TEST_START -->
CCO content
<!-- CCO_TEST_END -->

User content"""

        claude_md.write_text(content)

        count = clean_claude_md_markers(claude_md)

        assert count == 1
        new_content = claude_md.read_text()
        assert "CCO_TEST_START" not in new_content
        assert "User content" in new_content

    def test_normalizes_multiple_newlines(self, tmp_path: Path) -> None:
        """Test clean_claude_md_markers normalizes excessive newlines."""
        claude_md = tmp_path / "CLAUDE.md"
        content = """# Project

<!-- CCO_TEST_START -->
CCO content
<!-- CCO_TEST_END -->


User content"""

        claude_md.write_text(content)

        clean_claude_md_markers(claude_md)

        new_content = claude_md.read_text()
        # Should not have more than 2 consecutive newlines
        assert "\n\n\n" not in new_content

    def test_returns_zero_when_file_missing(self, tmp_path: Path) -> None:
        """Test clean_claude_md_markers returns zero when file doesn't exist."""
        claude_md = tmp_path / "CLAUDE.md"

        count = clean_claude_md_markers(claude_md)

        assert count == 0

    def test_returns_zero_when_no_markers(self, tmp_path: Path) -> None:
        """Test clean_claude_md_markers returns zero when no markers to remove."""
        claude_md = tmp_path / "CLAUDE.md"
        content = "# Project\n\nNo markers here"
        claude_md.write_text(content)

        count = clean_claude_md_markers(claude_md)

        assert count == 0

    def test_preserves_user_content(self, tmp_path: Path) -> None:
        """Test clean_claude_md_markers preserves user content."""
        claude_md = tmp_path / "CLAUDE.md"
        content = """# My Project

User section 1

<!-- CCO_TEST_START -->
CCO content
<!-- CCO_TEST_END -->

User section 2"""

        claude_md.write_text(content)

        clean_claude_md_markers(claude_md)

        new_content = claude_md.read_text()
        assert "My Project" in new_content
        assert "User section 1" in new_content
        assert "User section 2" in new_content
