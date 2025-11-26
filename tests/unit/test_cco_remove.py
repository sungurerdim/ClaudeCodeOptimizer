"""Unit tests for cco_remove module."""

from unittest.mock import MagicMock, patch

from claudecodeoptimizer.cco_remove import (
    count_cco_files,
    detect_install_method,
    main,
    remove_cco_files,
    uninstall_package,
)


class TestDetectInstallMethod:
    """Test detect_install_method function."""

    @patch("subprocess.run")
    def test_detect_pipx(self, mock_run):
        """Test detection of pipx installation."""
        mock_run.return_value = MagicMock(returncode=0, stdout="claudecodeoptimizer")
        assert detect_install_method() == "pipx"

    @patch("subprocess.run")
    def test_detect_none(self, mock_run):
        """Test when not installed."""
        mock_run.return_value = MagicMock(returncode=1, stdout="")
        assert detect_install_method() is None


class TestCountCcoFiles:
    """Test count_cco_files function."""

    def test_count_empty(self, tmp_path):
        """Test counting when no files."""
        with patch("claudecodeoptimizer.cco_remove.CLAUDE_DIR", tmp_path):
            with patch("claudecodeoptimizer.cco_remove.COMMANDS_DIR", tmp_path / "commands"):
                with patch("claudecodeoptimizer.cco_remove.AGENTS_DIR", tmp_path / "agents"):
                    counts = count_cco_files()
                    assert counts["commands"] == 0
                    assert counts["agents"] == 0

    def test_count_with_files(self, tmp_path):
        """Test counting with CCO files."""
        (tmp_path / "commands").mkdir()
        (tmp_path / "agents").mkdir()
        (tmp_path / "commands" / "cco-help.md").touch()
        (tmp_path / "agents" / "cco-agent-scan.md").touch()

        with patch("claudecodeoptimizer.cco_remove.CLAUDE_DIR", tmp_path):
            with patch("claudecodeoptimizer.cco_remove.COMMANDS_DIR", tmp_path / "commands"):
                with patch("claudecodeoptimizer.cco_remove.AGENTS_DIR", tmp_path / "agents"):
                    counts = count_cco_files()
                    assert counts["commands"] == 1
                    assert counts["agents"] == 1


class TestRemoveCcoFiles:
    """Test remove_cco_files function."""

    def test_remove_files(self, tmp_path):
        """Test removing CCO files."""
        (tmp_path / "commands").mkdir()
        (tmp_path / "commands" / "cco-help.md").touch()
        (tmp_path / "commands" / "user-custom.md").touch()

        with patch("claudecodeoptimizer.cco_remove.CLAUDE_DIR", tmp_path):
            with patch("claudecodeoptimizer.cco_remove.COMMANDS_DIR", tmp_path / "commands"):
                with patch("claudecodeoptimizer.cco_remove.AGENTS_DIR", tmp_path / "agents"):
                    deleted = remove_cco_files()

        assert deleted == 1
        assert not (tmp_path / "commands" / "cco-help.md").exists()
        assert (tmp_path / "commands" / "user-custom.md").exists()


class TestUninstallPackage:
    """Test uninstall_package function."""

    @patch("subprocess.run")
    def test_uninstall_pip(self, mock_run):
        """Test pip uninstall."""
        mock_run.return_value = MagicMock(returncode=0)
        assert uninstall_package("pip") is True


class TestMain:
    """Test main function."""

    @patch("claudecodeoptimizer.cco_remove.detect_install_method")
    @patch("claudecodeoptimizer.cco_remove.count_cco_files")
    def test_not_installed(self, mock_count, mock_detect):
        """Test when not installed."""
        mock_detect.return_value = None
        mock_count.return_value = {"agents": 0, "commands": 0, "templates": 0}
        assert main() == 0

    @patch("claudecodeoptimizer.cco_remove.detect_install_method")
    @patch("claudecodeoptimizer.cco_remove.count_cco_files")
    @patch("builtins.input")
    def test_cancelled(self, mock_input, mock_count, mock_detect):
        """Test user cancellation."""
        mock_detect.return_value = "pip"
        mock_count.return_value = {"agents": 1, "commands": 1, "templates": 0}
        mock_input.return_value = "n"
        assert main() == 0
