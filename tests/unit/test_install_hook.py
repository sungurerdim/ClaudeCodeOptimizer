"""
Unit tests for install_hook module

Tests post-install hook functionality.
Target Coverage: 100%
"""

import sys
from unittest.mock import patch

import pytest

from claudecodeoptimizer.install_hook import (
    _show_installation_summary,
    post_install,
)


class TestShowInstallationSummary:
    """Test _show_installation_summary function"""

    def test_shows_new_files(self, capsys) -> None:
        """Test displaying new files (0 → N)"""
        counts_before: dict[str, int] = {}
        counts_after = {"agents": 3, "commands": 10, "skills": 26, "principles": 15}

        _show_installation_summary(counts_before, counts_after, was_already_installed=False)

        captured = capsys.readouterr()
        assert "New:" in captured.out
        assert "Agents: 3 files" in captured.out
        assert "Commands: 10 files" in captured.out
        assert "Skills: 26 files" in captured.out
        assert "Principles: 15 files" in captured.out
        assert "Total: 0 → 54 files" in captured.out

    def test_shows_reinstalled_files_same_count(self, capsys) -> None:
        """Test displaying re-installed files when count stays same"""
        counts_before = {"agents": 3, "commands": 10}
        counts_after = {"agents": 3, "commands": 10}

        _show_installation_summary(counts_before, counts_after, was_already_installed=True)

        captured = capsys.readouterr()
        assert "Re-installed:" in captured.out
        assert "Agents: 3 files" in captured.out
        assert "Commands: 10 files" in captured.out
        assert "Total: 13 → 13 files" in captured.out

    def test_shows_reinstalled_files_different_count(self, capsys) -> None:
        """Test displaying re-installed files when count changes (N → M)"""
        counts_before = {"commands": 8, "skills": 20}
        counts_after = {"commands": 10, "skills": 26}

        _show_installation_summary(counts_before, counts_after, was_already_installed=True)

        captured = capsys.readouterr()
        assert "Re-installed:" in captured.out
        assert "Commands: 8 → 10 files" in captured.out
        assert "Skills: 20 → 26 files" in captured.out
        assert "Total: 28 → 36 files" in captured.out

    def test_shows_updated_when_not_previously_installed(self, capsys) -> None:
        """Test shows 'Updated' instead of 'Re-installed' for first install"""
        counts_before = {"commands": 5}
        counts_after = {"commands": 10}

        _show_installation_summary(counts_before, counts_after, was_already_installed=False)

        captured = capsys.readouterr()
        assert "Updated:" in captured.out
        assert "Re-installed:" not in captured.out

    def test_shows_removed_files(self, capsys) -> None:
        """Test displaying removed files (N → 0)"""
        counts_before = {"agents": 5, "commands": 10}
        counts_after = {"commands": 10}

        _show_installation_summary(counts_before, counts_after, was_already_installed=False)

        captured = capsys.readouterr()
        assert "Removed:" in captured.out
        assert "Agents: 5 files removed" in captured.out
        assert "Total: 15 → 10 files" in captured.out

    def test_respects_category_order(self, capsys) -> None:
        """Test that categories are displayed in correct order"""
        counts_before: dict[str, int] = {}
        counts_after = {
            "principles": 15,
            "agents": 3,
            "skills": 26,
            "commands": 10,
            "templates": 2,
        }

        _show_installation_summary(counts_before, counts_after, was_already_installed=False)

        captured = capsys.readouterr()
        # Find positions of each category
        agents_pos = captured.out.find("Agents:")
        commands_pos = captured.out.find("Commands:")
        skills_pos = captured.out.find("Skills:")
        principles_pos = captured.out.find("Principles:")
        templates_pos = captured.out.find("Templates:")

        # Verify order: agents → commands → skills → principles → templates
        assert agents_pos < commands_pos < skills_pos < principles_pos < templates_pos

    def test_handles_mixed_changes(self, capsys) -> None:
        """Test displaying mix of new, updated, and removed files"""
        counts_before = {"commands": 8, "skills": 20, "principles": 10}
        counts_after = {"agents": 3, "commands": 10, "skills": 26}

        _show_installation_summary(counts_before, counts_after, was_already_installed=False)

        captured = capsys.readouterr()
        # New agents
        assert "New:" in captured.out
        assert "Agents: 3 files" in captured.out
        # Updated commands and skills
        assert "Updated:" in captured.out
        assert "Commands: 8 → 10 files" in captured.out
        assert "Skills: 20 → 26 files" in captured.out
        # Removed principles
        assert "Removed:" in captured.out
        assert "Principles: 10 files removed" in captured.out

    def test_handles_empty_counts(self, capsys) -> None:
        """Test handles empty before and after counts"""
        _show_installation_summary({}, {}, was_already_installed=False)

        captured = capsys.readouterr()
        assert "Total: 0 → 0 files" in captured.out


class TestPostInstall:
    """Test post_install function"""

    def test_help_flag_shows_usage(self, capsys) -> None:
        """Test --help flag displays usage information"""
        with patch.object(sys, "argv", ["cco-setup", "--help"]):
            result = post_install()

        captured = capsys.readouterr()
        assert result == 0
        assert "Usage: cco-setup [--help]" in captured.out
        assert "Setup CCO global configuration" in captured.out

    def test_h_flag_shows_usage(self, capsys) -> None:
        """Test -h flag displays usage information"""
        with patch.object(sys, "argv", ["cco-setup", "-h"]):
            result = post_install()

        captured = capsys.readouterr()
        assert result == 0
        assert "Usage: cco-setup [--help]" in captured.out

    def test_successful_fresh_install(self, capsys) -> None:
        """Test successful installation from scratch"""
        mock_result = {
            "success": True,
            "claude_dir": "/home/user/.claude",
            "actions": [
                "Copied command files",
                "Copied principle files",
                "Updated CLAUDE.md",
            ],
            "counts_before": {},
            "counts_after": {"commands": 10, "principles": 15, "agents": 3},
        }

        with (
            patch(
                "claudecodeoptimizer.core.knowledge_setup.check_existing_installation",
                return_value=None,
            ),
            patch(
                "claudecodeoptimizer.core.knowledge_setup.setup_global_knowledge",
                return_value=mock_result,
            ),
        ):
            result = post_install()

        captured = capsys.readouterr()
        assert result == 0
        assert "ClaudeCodeOptimizer Setup" in captured.out
        assert "INSTALLATION COMPLETE" in captured.out
        assert "CCO IS READY!" in captured.out
        assert "Copied command files" in captured.out

    def test_existing_installation_yes_proceeds(self, capsys, monkeypatch) -> None:
        """Test proceeding with overwrite when user selects 'y'"""
        existing = {"commands": 8, "principles": 12}
        mock_result = {
            "success": True,
            "claude_dir": "/home/user/.claude",
            "actions": ["Updated files"],
            "counts_before": existing,
            "counts_after": {"commands": 10, "principles": 15},
        }

        # Mock user input
        monkeypatch.setattr("builtins.input", lambda _: "y")

        with (
            patch(
                "claudecodeoptimizer.core.knowledge_setup.check_existing_installation",
                return_value=existing,
            ),
            patch(
                "claudecodeoptimizer.core.knowledge_setup.setup_global_knowledge",
                return_value=mock_result,
            ),
        ):
            result = post_install()

        captured = capsys.readouterr()
        assert result == 0
        assert "[NOTICE] Found existing CCO installation" in captured.out
        assert "Commands: 8 files" in captured.out
        assert "[OK] Proceeding with setup..." in captured.out
        assert "INSTALLATION COMPLETE" in captured.out

    def test_existing_installation_no_cancels(self, capsys, monkeypatch) -> None:
        """Test canceling installation when user selects 'n'"""
        existing = {"commands": 8}

        # Mock user input
        monkeypatch.setattr("builtins.input", lambda _: "n")

        with patch(
            "claudecodeoptimizer.core.knowledge_setup.check_existing_installation",
            return_value=existing,
        ):
            result = post_install()

        captured = capsys.readouterr()
        assert result == 0
        assert "[CANCELLED] Setup cancelled by user" in captured.out
        assert "INSTALLATION COMPLETE" not in captured.out

    def test_existing_installation_diff_then_yes(self, capsys, monkeypatch) -> None:
        """Test showing diff then proceeding with 'y'"""
        existing = {"commands": 8, "principles": 12}
        mock_result = {
            "success": True,
            "claude_dir": "/home/user/.claude",
            "actions": ["Updated files"],
            "counts_before": existing,
            "counts_after": {"commands": 10, "principles": 15},
        }

        # Mock user inputs: first 'd' for diff, then 'y' to proceed
        inputs = iter(["d", "y"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        with (
            patch(
                "claudecodeoptimizer.core.knowledge_setup.check_existing_installation",
                return_value=existing,
            ),
            patch("claudecodeoptimizer.core.knowledge_setup.show_installation_diff") as mock_diff,
            patch(
                "claudecodeoptimizer.core.knowledge_setup.setup_global_knowledge",
                return_value=mock_result,
            ),
        ):
            result = post_install()

        captured = capsys.readouterr()
        assert result == 0
        assert mock_diff.called
        assert "INSTALLATION COMPLETE" in captured.out
        # Should show "Re-installed" because existing installation was found
        assert "Re-installed:" in captured.out

    def test_existing_installation_diff_then_no(self, capsys, monkeypatch) -> None:
        """Test showing diff then canceling with 'n'"""
        existing = {"commands": 8}

        # Mock user inputs: first 'd' for diff, then 'n' to cancel
        inputs = iter(["d", "n"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        with (
            patch(
                "claudecodeoptimizer.core.knowledge_setup.check_existing_installation",
                return_value=existing,
            ),
            patch("claudecodeoptimizer.core.knowledge_setup.show_installation_diff") as mock_diff,
        ):
            result = post_install()

        captured = capsys.readouterr()
        assert result == 0
        assert mock_diff.called
        assert "[CANCELLED] Setup cancelled by user" in captured.out

    def test_setup_returns_non_success(self, capsys, monkeypatch) -> None:
        """Test handling when setup returns success=False"""
        mock_result = {
            "success": False,
            "claude_dir": "/home/user/.claude",
            "actions": [],
            "counts_before": {},
            "counts_after": {},
        }

        with (
            patch(
                "claudecodeoptimizer.core.knowledge_setup.check_existing_installation",
                return_value=None,
            ),
            patch(
                "claudecodeoptimizer.core.knowledge_setup.setup_global_knowledge",
                return_value=mock_result,
            ),
        ):
            result = post_install()

        captured = capsys.readouterr()
        assert result == 0  # Still returns 0 but shows warning
        assert "[WARNING] Setup completed with warnings" in captured.out

    def test_exception_during_setup(self, capsys) -> None:
        """Test handling exception during setup"""
        with (
            patch(
                "claudecodeoptimizer.core.knowledge_setup.check_existing_installation",
                return_value=None,
            ),
            patch(
                "claudecodeoptimizer.core.knowledge_setup.setup_global_knowledge",
                side_effect=Exception("Setup failed"),
            ),
        ):
            result = post_install()

        captured = capsys.readouterr()
        assert result == 1
        assert "[ERROR] Setup failed" in captured.out
        assert "Error: Setup failed" in captured.out
        assert "You can run setup manually with: cco-setup" in captured.out

    def test_displays_file_summary(self, capsys) -> None:
        """Test that file summary is displayed when counts available"""
        mock_result = {
            "success": True,
            "claude_dir": "/home/user/.claude",
            "actions": ["Updated files"],
            "counts_before": {"commands": 8},
            "counts_after": {"commands": 10, "principles": 15},
        }

        with (
            patch(
                "claudecodeoptimizer.core.knowledge_setup.check_existing_installation",
                return_value=None,
            ),
            patch(
                "claudecodeoptimizer.core.knowledge_setup.setup_global_knowledge",
                return_value=mock_result,
            ),
        ):
            result = post_install()

        captured = capsys.readouterr()
        assert result == 0
        assert "FILE SUMMARY" in captured.out
        assert "Total:" in captured.out

    def test_skips_file_summary_when_no_counts(self, capsys) -> None:
        """Test file summary is skipped when no counts available"""
        mock_result = {
            "success": True,
            "claude_dir": "/home/user/.claude",
            "actions": ["Updated files"],
            "counts_before": {},
            "counts_after": {},
        }

        with (
            patch(
                "claudecodeoptimizer.core.knowledge_setup.check_existing_installation",
                return_value=None,
            ),
            patch(
                "claudecodeoptimizer.core.knowledge_setup.setup_global_knowledge",
                return_value=mock_result,
            ),
        ):
            result = post_install()

        captured = capsys.readouterr()
        assert result == 0
        # File summary section is skipped when both counts are empty
        assert "FILE SUMMARY" not in captured.out


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
