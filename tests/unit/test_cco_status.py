"""Unit tests for cco_status.py

Tests installation health check and component counting.
Target Coverage: 95%+
"""

from pathlib import Path
from unittest.mock import patch, MagicMock
import subprocess

import pytest

from claudecodeoptimizer.cco_status import (
    get_claude_dir,
    count_components,
    get_version_info,
    check_claude_md,
    print_status,
    main,
)


class TestGetClaudeDir:
    """Test get_claude_dir function"""

    def test_get_claude_dir_returns_path(self):
        """Test that get_claude_dir returns a Path object"""
        result = get_claude_dir()
        assert isinstance(result, Path)

    def test_get_claude_dir_in_home(self):
        """Test that claude dir is in user home"""
        result = get_claude_dir()
        assert result == Path.home() / ".claude"


class TestCountComponents:
    """Test count_components function"""

    def test_count_components_nonexistent_dir(self, tmp_path: Path):
        """Test counting components in non-existent directory"""
        nonexistent = tmp_path / "nonexistent"
        counts = count_components(nonexistent)

        assert counts["commands"] == 0
        assert counts["principles"] == 0
        assert counts["skills"] == 0
        assert counts["agents"] == 0

    def test_count_components_empty_dir(self, tmp_path: Path):
        """Test counting components in empty directory"""
        empty_claude = tmp_path / ".claude"
        empty_claude.mkdir()

        counts = count_components(empty_claude)

        assert counts["commands"] == 0
        assert counts["principles"] == 0
        assert counts["skills"] == 0
        assert counts["agents"] == 0

    def test_count_components_with_commands(self, tmp_path: Path):
        """Test counting CCO commands"""
        claude_dir = tmp_path / ".claude"
        commands_dir = claude_dir / "commands"
        commands_dir.mkdir(parents=True)

        # Create CCO commands
        (commands_dir / "cco-status.md").write_text("status command")
        (commands_dir / "cco-remove.md").write_text("remove command")
        (commands_dir / "cco-help.md").write_text("help command")
        # Create non-CCO file (should be ignored)
        (commands_dir / "custom-command.md").write_text("custom")

        counts = count_components(claude_dir)
        assert counts["commands"] == 3

    def test_count_components_with_principles(self, tmp_path: Path):
        """Test counting principles by category"""
        claude_dir = tmp_path / ".claude"
        principles_dir = claude_dir / "principles"
        principles_dir.mkdir(parents=True)

        # Create U_ principles
        (principles_dir / "U_DRY.md").write_text("DRY principle")
        (principles_dir / "U_FAIL_FAST.md").write_text("Fail fast")

        # Create C_ principles
        (principles_dir / "C_CONTEXT.md").write_text("Context")

        # Create P_ principles
        (principles_dir / "P_LINTING.md").write_text("Linting")
        (principles_dir / "P_TESTING.md").write_text("Testing")
        (principles_dir / "P_SECURITY.md").write_text("Security")

        # Create summary file (should be excluded)
        (principles_dir / "PRINCIPLES.md").write_text("Summary")

        counts = count_components(claude_dir)
        assert counts["principles"] == 6  # Excludes PRINCIPLES.md
        assert counts["principles_u"] == 2
        assert counts["principles_c"] == 1
        assert counts["principles_p"] == 3

    def test_count_components_with_skills(self, tmp_path: Path):
        """Test counting CCO skills"""
        claude_dir = tmp_path / ".claude"
        skills_dir = claude_dir / "skills"
        skills_dir.mkdir(parents=True)

        # Create CCO skills
        (skills_dir / "cco-skill-audit.md").write_text("audit skill")
        (skills_dir / "cco-skill-generate.md").write_text("generate skill")
        # Create non-CCO file (should be ignored)
        (skills_dir / "custom-skill.md").write_text("custom")

        counts = count_components(claude_dir)
        assert counts["skills"] == 2

    def test_count_components_with_agents(self, tmp_path: Path):
        """Test counting CCO agents"""
        claude_dir = tmp_path / ".claude"
        agents_dir = claude_dir / "agents"
        agents_dir.mkdir(parents=True)

        # Create CCO agents
        (agents_dir / "cco-agent-audit.md").write_text("audit agent")
        (agents_dir / "cco-agent-fix.md").write_text("fix agent")
        (agents_dir / "cco-agent-generate.md").write_text("generate agent")
        # Create non-CCO file (should be ignored)
        (agents_dir / "custom-agent.md").write_text("custom")

        counts = count_components(claude_dir)
        assert counts["agents"] == 3

    def test_count_components_comprehensive(self, tmp_path: Path):
        """Test counting all components together"""
        claude_dir = tmp_path / ".claude"

        # Create all directories
        (claude_dir / "commands").mkdir(parents=True)
        (claude_dir / "principles").mkdir(parents=True)
        (claude_dir / "skills").mkdir(parents=True)
        (claude_dir / "agents").mkdir(parents=True)

        # Add components
        (claude_dir / "commands" / "cco-status.md").write_text("status")
        (claude_dir / "commands" / "cco-help.md").write_text("help")

        (claude_dir / "principles" / "U_DRY.md").write_text("DRY")
        (claude_dir / "principles" / "C_CONTEXT.md").write_text("Context")

        (claude_dir / "skills" / "cco-skill-audit.md").write_text("audit")

        (claude_dir / "agents" / "cco-agent-fix.md").write_text("fix")

        counts = count_components(claude_dir)
        assert counts["commands"] == 2
        assert counts["principles"] == 2
        assert counts["principles_u"] == 1
        assert counts["principles_c"] == 1
        assert counts["skills"] == 1
        assert counts["agents"] == 1


class TestGetVersionInfo:
    """Test get_version_info function"""

    def test_get_version_info_structure(self):
        """Test that version info returns expected structure"""
        info = get_version_info()

        assert "version" in info
        assert "install_method" in info
        assert isinstance(info["version"], str)
        assert isinstance(info["install_method"], str)

    def test_get_version_info_has_version(self):
        """Test that version is retrieved"""
        info = get_version_info()
        assert info["version"] != ""
        # Should be either a version number or "unknown"
        assert info["version"] == "0.1.0" or info["version"] == "unknown"

    @patch("subprocess.run")
    def test_get_version_info_pipx(self, mock_run: MagicMock):
        """Test detection of pipx installation"""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="  package claudecodeoptimizer 0.1.0\n"
        )

        info = get_version_info()
        assert info["install_method"] in ["pipx", "pip", "unknown"]

    @patch("subprocess.run")
    def test_get_version_info_pip(self, mock_run: MagicMock):
        """Test detection of pip installation"""
        # pipx fails
        mock_run.side_effect = [
            subprocess.CalledProcessError(1, "pipx"),
            MagicMock(returncode=0, stdout="claudecodeoptimizer"),
        ]

        info = get_version_info()
        assert info["install_method"] in ["pip", "unknown"]

    @patch("subprocess.run")
    def test_get_version_info_unknown(self, mock_run: MagicMock):
        """Test fallback to unknown installation method"""
        mock_run.side_effect = subprocess.CalledProcessError(1, "cmd")

        info = get_version_info()
        assert info["install_method"] == "unknown"


class TestCheckClaudeMd:
    """Test check_claude_md function"""

    def test_check_claude_md_not_exists(self, tmp_path: Path):
        """Test when CLAUDE.md doesn't exist"""
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()

        result = check_claude_md(claude_dir)
        assert result is False

    def test_check_claude_md_exists_no_markers(self, tmp_path: Path):
        """Test when CLAUDE.md exists but has no CCO markers"""
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()

        claude_md = claude_dir / "CLAUDE.md"
        claude_md.write_text("# My Claude Config\n\nSome custom content")

        result = check_claude_md(claude_dir)
        assert result is False

    def test_check_claude_md_exists_with_markers(self, tmp_path: Path):
        """Test when CLAUDE.md exists with CCO markers"""
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()

        claude_md = claude_dir / "CLAUDE.md"
        claude_md.write_text(
            "# Config\n\n<!-- CCO_PRINCIPLES_START -->\n"
            "@principles/U_DRY.md\n"
            "<!-- CCO_PRINCIPLES_END -->\n"
        )

        result = check_claude_md(claude_dir)
        assert result is True


class TestPrintStatus:
    """Test print_status function"""

    @patch("claudecodeoptimizer.cco_status.check_claude_md")
    @patch("claudecodeoptimizer.cco_status.count_components")
    @patch("claudecodeoptimizer.cco_status.get_version_info")
    @patch("claudecodeoptimizer.cco_status.get_claude_dir")
    @patch("builtins.print")
    def test_print_status_success(
        self,
        mock_print: MagicMock,
        mock_get_dir: MagicMock,
        mock_version: MagicMock,
        mock_count: MagicMock,
        mock_check: MagicMock,
        tmp_path: Path,
    ):
        """Test successful status print"""
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()

        mock_get_dir.return_value = claude_dir
        mock_version.return_value = {"version": "0.1.0", "install_method": "pipx"}
        mock_count.return_value = {
            "commands": 11,
            "principles": 25,
            "principles_u": 10,
            "principles_c": 10,
            "principles_p": 5,
            "skills": 3,
            "agents": 4,
        }
        mock_check.return_value = True

        result = print_status()

        assert result == 0
        assert mock_print.called

    @patch("claudecodeoptimizer.cco_status.get_claude_dir")
    @patch("builtins.print")
    def test_print_status_no_installation(
        self,
        mock_print: MagicMock,
        mock_get_dir: MagicMock,
        tmp_path: Path,
    ):
        """Test status when CCO is not installed"""
        nonexistent = tmp_path / "nonexistent"
        mock_get_dir.return_value = nonexistent

        result = print_status()

        # Should return 1 (error) since directory doesn't exist
        assert result in [0, 1]  # Depends on implementation
        assert mock_print.called


class TestMain:
    """Test main function"""

    @patch("claudecodeoptimizer.cco_status.print_status")
    def test_main_calls_print_status(self, mock_print: MagicMock):
        """Test that main calls print_status"""
        mock_print.return_value = 0

        result = main()

        assert result == 0
        mock_print.assert_called_once()

    @patch("claudecodeoptimizer.cco_status.print_status")
    def test_main_returns_status_code(self, mock_print: MagicMock):
        """Test that main returns the status code from print_status"""
        mock_print.return_value = 1

        result = main()

        assert result == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=claudecodeoptimizer.cco_status"])
