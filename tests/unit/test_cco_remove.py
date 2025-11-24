"""Unit tests for cco_remove.py

Tests uninstallation, file counting, and removal verification.
Target Coverage: 95%+
"""

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from claudecodeoptimizer.cco_remove import (
    backup_claude_dir,
    confirm_deletion,
    count_cco_files,
    detect_package_install,
    get_claude_dir,
    get_package_location,
    main,
    remove_claude_dir,
    remove_package,
    show_removal_preview,
    verify_removal,
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


class TestDetectPackageInstall:
    """Test detect_package_install function"""

    @patch("subprocess.run")
    def test_detect_pipx_installation(self, mock_run: MagicMock):
        """Test detection of pipx installation"""
        mock_run.return_value = MagicMock(
            returncode=0, stdout="  package claudecodeoptimizer 0.1.0\n"
        )

        result = detect_package_install()
        assert result == "pipx"
        mock_run.assert_called_once()

    @patch("subprocess.run")
    def test_detect_uv_installation(self, mock_run: MagicMock):
        """Test detection of uv installation"""
        # First call (pipx) returns no match, second call (uv) succeeds
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout="other packages"),
            MagicMock(returncode=0, stdout="claudecodeoptimizer"),
        ]

        result = detect_package_install()
        assert result == "uv"
        assert mock_run.call_count == 2

    @patch("subprocess.run")
    def test_detect_pip_installation(self, mock_run: MagicMock):
        """Test detection of pip installation"""
        # First two calls fail, third (pip) succeeds
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout="other packages"),
            MagicMock(returncode=0, stdout="other packages"),
            MagicMock(returncode=0, stdout="claudecodeoptimizer"),
        ]

        result = detect_package_install()
        assert result == "pip"
        assert mock_run.call_count == 3

    @patch("subprocess.run")
    def test_detect_no_installation(self, mock_run: MagicMock):
        """Test when package not installed"""
        mock_run.return_value = MagicMock(returncode=1, stdout="")

        result = detect_package_install()
        assert result is None

    @patch("subprocess.run")
    def test_detect_timeout(self, mock_run: MagicMock):
        """Test handling of subprocess timeout"""
        mock_run.side_effect = subprocess.TimeoutExpired("pipx", 5)

        result = detect_package_install()
        assert result is None

    @patch("subprocess.run")
    def test_detect_file_not_found(self, mock_run: MagicMock):
        """Test handling when command not found"""
        mock_run.side_effect = FileNotFoundError()

        result = detect_package_install()
        assert result is None


class TestCountCcoFiles:
    """Test count_cco_files function"""

    def test_count_nonexistent_dir(self, tmp_path: Path):
        """Test counting in non-existent directory"""
        nonexistent = tmp_path / "nonexistent"
        counts = count_cco_files(nonexistent)

        assert counts["agents"] == 0
        assert counts["commands"] == 0
        assert counts["skills"] == 0
        assert counts["principles"] == 0
        assert counts["templates"] == 0

    def test_count_empty_dir(self, tmp_path: Path):
        """Test counting in empty directory"""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()

        counts = count_cco_files(empty_dir)

        assert counts["agents"] == 0
        assert counts["commands"] == 0
        assert counts["skills"] == 0
        assert counts["principles"] == 0

    def test_count_agents(self, tmp_path: Path):
        """Test counting CCO agents"""
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()

        (agents_dir / "cco-agent-audit.md").write_text("audit agent")
        (agents_dir / "cco-agent-fix.md").write_text("fix agent")
        (agents_dir / "cco-agent-generate.md").write_text("generate agent")
        (agents_dir / "custom-agent.md").write_text("custom")  # Should be ignored

        counts = count_cco_files(tmp_path)
        assert counts["agents"] == 3

    def test_count_commands(self, tmp_path: Path):
        """Test counting CCO commands"""
        commands_dir = tmp_path / "commands"
        commands_dir.mkdir()

        (commands_dir / "cco-status.md").write_text("status")
        (commands_dir / "cco-remove.md").write_text("remove")
        (commands_dir / "custom.md").write_text("custom")  # Should be ignored

        counts = count_cco_files(tmp_path)
        assert counts["commands"] == 2

    def test_count_skills(self, tmp_path: Path):
        """Test counting CCO skills"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        (skills_dir / "cco-skill-audit.md").write_text("audit")
        (skills_dir / "cco-skill-generate.md").write_text("generate")
        (skills_dir / "custom.md").write_text("custom")  # Should be ignored

        counts = count_cco_files(tmp_path)
        assert counts["skills"] == 2

    def test_count_principles(self, tmp_path: Path):
        """Test counting principles by category"""
        principles_dir = tmp_path / "principles"
        principles_dir.mkdir()

        # Create U_ principles
        (principles_dir / "U_DRY.md").write_text("DRY")
        (principles_dir / "U_FAIL_FAST.md").write_text("Fail fast")

        # Create C_ principles
        (principles_dir / "C_CONTEXT.md").write_text("Context")

        # Create P_ principles
        (principles_dir / "P_LINTING.md").write_text("Linting")
        (principles_dir / "P_TESTING.md").write_text("Testing")

        # Create summary file (should be excluded)
        (principles_dir / "PRINCIPLES.md").write_text("Summary")

        counts = count_cco_files(tmp_path)
        assert counts["principles"] == 5  # Excludes PRINCIPLES.md
        assert counts["principles_u"] == 2
        assert counts["principles_c"] == 1
        assert counts["principles_p"] == 2

    def test_count_templates(self, tmp_path: Path):
        """Test counting template files"""
        (tmp_path / "settings.json.cco").write_text("settings")
        (tmp_path / "statusline.js.cco").write_text("statusline")

        counts = count_cco_files(tmp_path)
        assert counts["templates"] == 2

    def test_count_comprehensive(self, tmp_path: Path):
        """Test counting all components together"""
        # Create all directories
        (tmp_path / "agents").mkdir()
        (tmp_path / "commands").mkdir()
        (tmp_path / "skills").mkdir()
        (tmp_path / "principles").mkdir()

        # Add components
        (tmp_path / "agents" / "cco-agent-audit.md").write_text("audit")
        (tmp_path / "commands" / "cco-status.md").write_text("status")
        (tmp_path / "skills" / "cco-skill-audit.md").write_text("audit")
        (tmp_path / "principles" / "U_DRY.md").write_text("DRY")
        (tmp_path / "settings.json.cco").write_text("settings")

        counts = count_cco_files(tmp_path)
        assert counts["agents"] == 1
        assert counts["commands"] == 1
        assert counts["skills"] == 1
        assert counts["principles"] == 1
        assert counts["templates"] == 1


class TestGetPackageLocation:
    """Test get_package_location function"""

    @patch("subprocess.run")
    def test_get_location_success(self, mock_run: MagicMock):
        """Test successful package location retrieval"""
        mock_run.return_value = MagicMock(
            returncode=0, stdout="Name: claudecodeoptimizer\nLocation: /usr/local/lib\n"
        )

        result = get_package_location()
        assert result == "/usr/local/lib"

    @patch("subprocess.run")
    def test_get_location_not_found(self, mock_run: MagicMock):
        """Test when package not found"""
        mock_run.return_value = MagicMock(returncode=1, stdout="")

        result = get_package_location()
        assert result is None

    @patch("subprocess.run")
    def test_get_location_timeout(self, mock_run: MagicMock):
        """Test handling of subprocess timeout"""
        mock_run.side_effect = subprocess.TimeoutExpired("pip", 5)

        result = get_package_location()
        assert result is None

    @patch("subprocess.run")
    def test_get_location_file_not_found(self, mock_run: MagicMock):
        """Test handling when pip not found"""
        mock_run.side_effect = FileNotFoundError()

        result = get_package_location()
        assert result is None


class TestShowRemovalPreview:
    """Test show_removal_preview function"""

    @patch("builtins.print")
    def test_show_preview_with_package(self, mock_print: MagicMock):
        """Test preview display with package"""
        counts = {
            "agents": 3,
            "commands": 11,
            "skills": 2,
            "principles": 25,
            "principles_u": 10,
            "principles_c": 10,
            "principles_p": 5,
            "templates": 2,
        }

        show_removal_preview("pipx", "/usr/local/lib", counts)

        assert mock_print.called
        # Verify key sections printed
        printed_text = " ".join(
            [str(call.args[0]) for call in mock_print.call_args_list if call.args]
        )
        assert "CCO UNINSTALL - PREVIEW" in printed_text
        assert "pipx" in printed_text
        assert "Agents: 3" in printed_text
        assert "Commands: 11" in printed_text

    @patch("builtins.print")
    def test_show_preview_no_package(self, mock_print: MagicMock):
        """Test preview when no package installed"""
        counts = {
            "agents": 0,
            "commands": 0,
            "skills": 0,
            "principles": 0,
            "principles_u": 0,
            "principles_c": 0,
            "principles_p": 0,
            "templates": 0,
        }

        show_removal_preview(None, None, counts)

        assert mock_print.called


class TestConfirmDeletion:
    """Test confirm_deletion function"""

    @patch("builtins.input")
    @patch("builtins.print")
    def test_confirm_with_correct_text(self, mock_print: MagicMock, mock_input: MagicMock):
        """Test confirmation with correct text"""
        mock_input.return_value = "yes-delete-cco"

        result = confirm_deletion()
        assert result is True

    @patch("builtins.input")
    @patch("builtins.print")
    def test_confirm_with_wrong_text(self, mock_print: MagicMock, mock_input: MagicMock):
        """Test confirmation with wrong text"""
        mock_input.return_value = "yes"

        result = confirm_deletion()
        assert result is False

    @patch("builtins.input")
    @patch("builtins.print")
    def test_confirm_with_whitespace(self, mock_print: MagicMock, mock_input: MagicMock):
        """Test confirmation strips whitespace"""
        mock_input.return_value = "  yes-delete-cco  "

        result = confirm_deletion()
        assert result is True


class TestRemovePackage:
    """Test remove_package function"""

    @patch("subprocess.run")
    def test_remove_pipx_success(self, mock_run: MagicMock):
        """Test successful pipx uninstall"""
        mock_run.return_value = MagicMock(returncode=0)

        result = remove_package("pipx")
        assert result is True
        mock_run.assert_called_once()
        assert "pipx" in mock_run.call_args[0][0]

    @patch("subprocess.run")
    def test_remove_uv_success(self, mock_run: MagicMock):
        """Test successful uv uninstall"""
        mock_run.return_value = MagicMock(returncode=0)

        result = remove_package("uv")
        assert result is True
        assert "uv" in mock_run.call_args[0][0]

    @patch("subprocess.run")
    def test_remove_pip_success(self, mock_run: MagicMock):
        """Test successful pip uninstall"""
        mock_run.return_value = MagicMock(returncode=0)

        result = remove_package("pip")
        assert result is True
        assert "pip" in mock_run.call_args[0][0]

    @patch("subprocess.run")
    def test_remove_failure(self, mock_run: MagicMock):
        """Test failed uninstall"""
        mock_run.return_value = MagicMock(returncode=1)

        result = remove_package("pipx")
        assert result is False

    @patch("subprocess.run")
    def test_remove_timeout(self, mock_run: MagicMock):
        """Test uninstall timeout"""
        mock_run.side_effect = subprocess.TimeoutExpired("pipx", 30)

        result = remove_package("pipx")
        assert result is False

    @patch("subprocess.run")
    def test_remove_file_not_found(self, mock_run: MagicMock):
        """Test when uninstall command not found"""
        mock_run.side_effect = FileNotFoundError()

        result = remove_package("pipx")
        assert result is False


class TestBackupClaudeDir:
    """Test backup_claude_dir function"""

    def test_backup_success(self, tmp_path: Path):
        """Test successful backup creation"""
        source_dir = tmp_path / ".claude"
        source_dir.mkdir()
        (source_dir / "test.txt").write_text("test content")

        backup_path = backup_claude_dir(source_dir)

        assert backup_path is not None
        assert backup_path.exists()
        assert (backup_path / "test.txt").exists()
        assert (backup_path / "test.txt").read_text() == "test content"

    def test_backup_nonexistent_dir(self, tmp_path: Path):
        """Test backup of non-existent directory"""
        nonexistent = tmp_path / "nonexistent"

        backup_path = backup_claude_dir(nonexistent)
        assert backup_path is None

    @patch("shutil.copytree")
    def test_backup_exception(self, mock_copytree: MagicMock, tmp_path: Path):
        """Test backup with exception"""
        mock_copytree.side_effect = Exception("Permission denied")
        source_dir = tmp_path / ".claude"
        source_dir.mkdir()

        backup_path = backup_claude_dir(source_dir)
        assert backup_path is None


class TestRemoveClaudeDir:
    """Test remove_claude_dir function"""

    def test_remove_without_backup(self, tmp_path: Path):
        """Test removal without backup"""
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()
        (claude_dir / "test.txt").write_text("test")

        success, backup_path = remove_claude_dir(claude_dir, create_backup=False)

        assert success is True
        assert backup_path is None
        assert not claude_dir.exists()

    def test_remove_with_backup(self, tmp_path: Path):
        """Test removal with backup"""
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()
        (claude_dir / "test.txt").write_text("test")

        success, backup_path = remove_claude_dir(claude_dir, create_backup=True)

        assert success is True
        assert backup_path is not None
        assert backup_path.exists()
        assert not claude_dir.exists()

    def test_remove_nonexistent_dir(self, tmp_path: Path):
        """Test removal of non-existent directory"""
        nonexistent = tmp_path / "nonexistent"

        success, backup_path = remove_claude_dir(nonexistent, create_backup=False)

        assert success is False
        assert backup_path is None

    @patch("shutil.rmtree")
    def test_remove_exception(self, mock_rmtree: MagicMock, tmp_path: Path):
        """Test removal with exception"""
        mock_rmtree.side_effect = Exception("Permission denied")
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()

        success, backup_path = remove_claude_dir(claude_dir, create_backup=False)

        assert success is False


class TestVerifyRemoval:
    """Test verify_removal function"""

    @patch("claudecodeoptimizer.cco_remove.detect_package_install")
    @patch("claudecodeoptimizer.cco_remove.get_claude_dir")
    def test_verify_complete_removal(
        self, mock_get_dir: MagicMock, mock_detect: MagicMock, tmp_path: Path
    ):
        """Test verification when fully removed"""
        mock_detect.return_value = None
        nonexistent = tmp_path / "nonexistent"
        mock_get_dir.return_value = nonexistent

        results = verify_removal("pipx")

        assert results["package_removed"] is True
        assert results["directory_removed"] is True

    @patch("claudecodeoptimizer.cco_remove.detect_package_install")
    @patch("claudecodeoptimizer.cco_remove.get_claude_dir")
    def test_verify_package_still_installed(
        self, mock_get_dir: MagicMock, mock_detect: MagicMock, tmp_path: Path
    ):
        """Test verification when package still installed"""
        mock_detect.return_value = "pipx"
        nonexistent = tmp_path / "nonexistent"
        mock_get_dir.return_value = nonexistent

        results = verify_removal("pipx")

        assert results["package_removed"] is False
        assert results["directory_removed"] is True

    @patch("claudecodeoptimizer.cco_remove.detect_package_install")
    @patch("claudecodeoptimizer.cco_remove.get_claude_dir")
    def test_verify_files_still_present(
        self, mock_get_dir: MagicMock, mock_detect: MagicMock, tmp_path: Path
    ):
        """Test verification when CCO files still present"""
        mock_detect.return_value = None
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()
        commands_dir = claude_dir / "commands"
        commands_dir.mkdir()
        (commands_dir / "cco-status.md").write_text("status")
        mock_get_dir.return_value = claude_dir

        results = verify_removal(None)

        assert results["package_removed"] is True
        assert results["directory_removed"] is False


class TestMain:
    """Test main function"""

    @patch("claudecodeoptimizer.cco_remove.detect_package_install")
    @patch("claudecodeoptimizer.cco_remove.get_claude_dir")
    @patch("builtins.print")
    def test_main_nothing_to_remove(
        self,
        mock_print: MagicMock,
        mock_get_dir: MagicMock,
        mock_detect: MagicMock,
        tmp_path: Path,
    ):
        """Test main when nothing to remove"""
        mock_detect.return_value = None
        nonexistent = tmp_path / "nonexistent"
        mock_get_dir.return_value = nonexistent

        result = main()

        assert result == 0
        printed_text = " ".join(
            [str(call.args[0]) for call in mock_print.call_args_list if call.args]
        )
        assert "not installed" in printed_text

    @patch("claudecodeoptimizer.cco_remove.verify_removal")
    @patch("claudecodeoptimizer.cco_remove.remove_package")
    @patch("claudecodeoptimizer.cco_remove.remove_claude_dir")
    @patch("claudecodeoptimizer.cco_remove.confirm_deletion")
    @patch("claudecodeoptimizer.cco_remove.show_removal_preview")
    @patch("claudecodeoptimizer.cco_remove.count_cco_files")
    @patch("claudecodeoptimizer.cco_remove.get_package_location")
    @patch("claudecodeoptimizer.cco_remove.detect_package_install")
    @patch("claudecodeoptimizer.cco_remove.get_claude_dir")
    @patch("builtins.print")
    def test_main_user_cancels(
        self,
        mock_print: MagicMock,
        mock_get_dir: MagicMock,
        mock_detect: MagicMock,
        mock_location: MagicMock,
        mock_count: MagicMock,
        mock_preview: MagicMock,
        mock_confirm: MagicMock,
        mock_remove_dir: MagicMock,
        mock_remove_pkg: MagicMock,
        mock_verify: MagicMock,
        tmp_path: Path,
    ):
        """Test main when user cancels"""
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()
        mock_get_dir.return_value = claude_dir
        mock_detect.return_value = "pipx"
        mock_location.return_value = "/usr/local/lib"
        mock_count.return_value = {
            "agents": 1,
            "commands": 1,
            "skills": 1,
            "principles": 1,
            "principles_u": 0,
            "principles_c": 0,
            "principles_p": 0,
            "templates": 0,
        }
        mock_confirm.return_value = False

        result = main()

        assert result == 0
        printed_text = " ".join(
            [str(call.args[0]) for call in mock_print.call_args_list if call.args]
        )
        assert "CANCELLED" in printed_text

    @patch("claudecodeoptimizer.cco_remove.verify_removal")
    @patch("claudecodeoptimizer.cco_remove.remove_package")
    @patch("claudecodeoptimizer.cco_remove.remove_claude_dir")
    @patch("claudecodeoptimizer.cco_remove.confirm_deletion")
    @patch("claudecodeoptimizer.cco_remove.show_removal_preview")
    @patch("claudecodeoptimizer.cco_remove.count_cco_files")
    @patch("claudecodeoptimizer.cco_remove.get_package_location")
    @patch("claudecodeoptimizer.cco_remove.detect_package_install")
    @patch("claudecodeoptimizer.cco_remove.get_claude_dir")
    @patch("builtins.print")
    def test_main_successful_removal(
        self,
        mock_print: MagicMock,
        mock_get_dir: MagicMock,
        mock_detect: MagicMock,
        mock_location: MagicMock,
        mock_count: MagicMock,
        mock_preview: MagicMock,
        mock_confirm: MagicMock,
        mock_remove_dir: MagicMock,
        mock_remove_pkg: MagicMock,
        mock_verify: MagicMock,
        tmp_path: Path,
    ):
        """Test successful removal"""
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()
        mock_get_dir.return_value = claude_dir
        mock_detect.return_value = "pipx"
        mock_location.return_value = "/usr/local/lib"
        mock_count.return_value = {
            "agents": 3,
            "commands": 11,
            "skills": 2,
            "principles": 25,
            "principles_u": 10,
            "principles_c": 10,
            "principles_p": 5,
            "templates": 2,
        }
        mock_confirm.return_value = True
        mock_remove_pkg.return_value = True
        mock_remove_dir.return_value = (True, None)
        mock_verify.return_value = {"package_removed": True, "directory_removed": True}

        result = main()

        assert result == 0
        printed_text = " ".join(
            [str(call.args[0]) for call in mock_print.call_args_list if call.args]
        )
        assert "COMPLETE" in printed_text

    @patch("claudecodeoptimizer.cco_remove.detect_package_install")
    @patch("claudecodeoptimizer.cco_remove.get_claude_dir")
    def test_main_keyboard_interrupt(
        self, mock_get_dir: MagicMock, mock_detect: MagicMock, tmp_path: Path
    ):
        """Test handling of keyboard interrupt"""
        mock_detect.side_effect = KeyboardInterrupt()
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()
        mock_get_dir.return_value = claude_dir

        result = main()

        assert result == 130

    @patch("claudecodeoptimizer.cco_remove.detect_package_install")
    @patch("claudecodeoptimizer.cco_remove.get_claude_dir")
    def test_main_unexpected_error(
        self, mock_get_dir: MagicMock, mock_detect: MagicMock, tmp_path: Path
    ):
        """Test handling of unexpected error"""
        mock_detect.side_effect = Exception("Unexpected error")
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()
        mock_get_dir.return_value = claude_dir

        result = main()

        assert result == 1

    @patch("claudecodeoptimizer.cco_remove.verify_removal")
    @patch("claudecodeoptimizer.cco_remove.remove_package")
    @patch("claudecodeoptimizer.cco_remove.remove_claude_dir")
    @patch("claudecodeoptimizer.cco_remove.confirm_deletion")
    @patch("claudecodeoptimizer.cco_remove.show_removal_preview")
    @patch("claudecodeoptimizer.cco_remove.count_cco_files")
    @patch("claudecodeoptimizer.cco_remove.get_package_location")
    @patch("claudecodeoptimizer.cco_remove.detect_package_install")
    @patch("claudecodeoptimizer.cco_remove.get_claude_dir")
    @patch("builtins.print")
    def test_main_package_removal_failed(
        self,
        mock_print: MagicMock,
        mock_get_dir: MagicMock,
        mock_detect: MagicMock,
        mock_location: MagicMock,
        mock_count: MagicMock,
        mock_preview: MagicMock,
        mock_confirm: MagicMock,
        mock_remove_dir: MagicMock,
        mock_remove_pkg: MagicMock,
        mock_verify: MagicMock,
        tmp_path: Path,
    ):
        """Test main when package removal fails (line 340)"""
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()
        mock_get_dir.return_value = claude_dir
        mock_detect.return_value = "pipx"
        mock_location.return_value = "/usr/local/lib"
        mock_count.return_value = {
            "agents": 1,
            "commands": 1,
            "skills": 1,
            "principles": 1,
            "principles_u": 0,
            "principles_c": 0,
            "principles_p": 0,
            "templates": 0,
        }
        mock_confirm.return_value = True
        mock_remove_pkg.return_value = False  # Package removal fails
        mock_remove_dir.return_value = (True, None)
        mock_verify.return_value = {"package_removed": True, "directory_removed": True}

        result = main()

        assert result == 0
        printed_text = " ".join(
            [str(call.args[0]) for call in mock_print.call_args_list if call.args]
        )
        assert "Failed to uninstall package" in printed_text

    @patch("claudecodeoptimizer.cco_remove.verify_removal")
    @patch("claudecodeoptimizer.cco_remove.remove_package")
    @patch("claudecodeoptimizer.cco_remove.remove_claude_dir")
    @patch("claudecodeoptimizer.cco_remove.confirm_deletion")
    @patch("claudecodeoptimizer.cco_remove.show_removal_preview")
    @patch("claudecodeoptimizer.cco_remove.count_cco_files")
    @patch("claudecodeoptimizer.cco_remove.get_package_location")
    @patch("claudecodeoptimizer.cco_remove.detect_package_install")
    @patch("claudecodeoptimizer.cco_remove.get_claude_dir")
    @patch("builtins.print")
    def test_main_removal_with_backup(
        self,
        mock_print: MagicMock,
        mock_get_dir: MagicMock,
        mock_detect: MagicMock,
        mock_location: MagicMock,
        mock_count: MagicMock,
        mock_preview: MagicMock,
        mock_confirm: MagicMock,
        mock_remove_dir: MagicMock,
        mock_remove_pkg: MagicMock,
        mock_verify: MagicMock,
        tmp_path: Path,
    ):
        """Test main when removal creates backup (lines 351-353)"""
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()
        backup_dir = tmp_path / ".claude.backup.20240101_120000"
        backup_dir.mkdir()

        mock_get_dir.return_value = claude_dir
        mock_detect.return_value = "pipx"
        mock_location.return_value = "/usr/local/lib"
        mock_count.return_value = {
            "agents": 1,
            "commands": 1,
            "skills": 1,
            "principles": 1,
            "principles_u": 0,
            "principles_c": 0,
            "principles_p": 0,
            "templates": 0,
        }
        mock_confirm.return_value = True
        mock_remove_pkg.return_value = True
        mock_remove_dir.return_value = (True, backup_dir)  # With backup
        mock_verify.return_value = {"package_removed": True, "directory_removed": True}

        result = main()

        assert result == 0
        printed_text = " ".join(
            [str(call.args[0]) for call in mock_print.call_args_list if call.args]
        )
        assert "Backup created" in printed_text

    @patch("claudecodeoptimizer.cco_remove.verify_removal")
    @patch("claudecodeoptimizer.cco_remove.remove_package")
    @patch("claudecodeoptimizer.cco_remove.remove_claude_dir")
    @patch("claudecodeoptimizer.cco_remove.confirm_deletion")
    @patch("claudecodeoptimizer.cco_remove.show_removal_preview")
    @patch("claudecodeoptimizer.cco_remove.count_cco_files")
    @patch("claudecodeoptimizer.cco_remove.get_package_location")
    @patch("claudecodeoptimizer.cco_remove.detect_package_install")
    @patch("claudecodeoptimizer.cco_remove.get_claude_dir")
    @patch("builtins.print")
    def test_main_directory_removal_failed(
        self,
        mock_print: MagicMock,
        mock_get_dir: MagicMock,
        mock_detect: MagicMock,
        mock_location: MagicMock,
        mock_count: MagicMock,
        mock_preview: MagicMock,
        mock_confirm: MagicMock,
        mock_remove_dir: MagicMock,
        mock_remove_pkg: MagicMock,
        mock_verify: MagicMock,
        tmp_path: Path,
    ):
        """Test main when directory removal fails (line 353)"""
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()
        mock_get_dir.return_value = claude_dir
        mock_detect.return_value = "pipx"
        mock_location.return_value = "/usr/local/lib"
        mock_count.return_value = {
            "agents": 1,
            "commands": 1,
            "skills": 1,
            "principles": 1,
            "principles_u": 0,
            "principles_c": 0,
            "principles_p": 0,
            "templates": 0,
        }
        mock_confirm.return_value = True
        mock_remove_pkg.return_value = True
        mock_remove_dir.return_value = (False, None)  # Directory removal fails
        mock_verify.return_value = {"package_removed": True, "directory_removed": False}

        result = main()

        assert result == 1
        printed_text = " ".join(
            [str(call.args[0]) for call in mock_print.call_args_list if call.args]
        )
        assert "Failed to remove directory" in printed_text

    @patch("claudecodeoptimizer.cco_remove.verify_removal")
    @patch("claudecodeoptimizer.cco_remove.remove_package")
    @patch("claudecodeoptimizer.cco_remove.remove_claude_dir")
    @patch("claudecodeoptimizer.cco_remove.confirm_deletion")
    @patch("claudecodeoptimizer.cco_remove.show_removal_preview")
    @patch("claudecodeoptimizer.cco_remove.count_cco_files")
    @patch("claudecodeoptimizer.cco_remove.get_package_location")
    @patch("claudecodeoptimizer.cco_remove.detect_package_install")
    @patch("claudecodeoptimizer.cco_remove.get_claude_dir")
    @patch("builtins.print")
    def test_main_incomplete_removal(
        self,
        mock_print: MagicMock,
        mock_get_dir: MagicMock,
        mock_detect: MagicMock,
        mock_location: MagicMock,
        mock_count: MagicMock,
        mock_preview: MagicMock,
        mock_confirm: MagicMock,
        mock_remove_dir: MagicMock,
        mock_remove_pkg: MagicMock,
        mock_verify: MagicMock,
        tmp_path: Path,
    ):
        """Test main when removal is incomplete (lines 387-393)"""
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()
        mock_get_dir.return_value = claude_dir
        mock_detect.return_value = "pipx"
        mock_location.return_value = "/usr/local/lib"
        mock_count.return_value = {
            "agents": 1,
            "commands": 1,
            "skills": 1,
            "principles": 1,
            "principles_u": 0,
            "principles_c": 0,
            "principles_p": 0,
            "templates": 0,
        }
        mock_confirm.return_value = True
        mock_remove_pkg.return_value = True
        mock_remove_dir.return_value = (True, None)
        mock_verify.return_value = {
            "package_removed": False,
            "directory_removed": False,
        }  # Both failed

        result = main()

        assert result == 1
        printed_text = " ".join(
            [str(call.args[0]) for call in mock_print.call_args_list if call.args]
        )
        assert "Removal incomplete" in printed_text
        assert "Package still installed" in printed_text
        assert "CCO files still present" in printed_text


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=claudecodeoptimizer.cco_remove"])
