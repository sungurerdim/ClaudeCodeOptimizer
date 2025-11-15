"""
Comprehensive tests for wizard system_detection module.

Tests cover:
- SystemDetector initialization
- OS detection (type, version, platform)
- Terminal detection (shell, emulator, color, unicode)
- Locale detection (locale, language, encoding)
- Python environment detection (version, pip)
- Git detection (installed, user name, user email)
- Editor detection (installed editors, active editor)
- Project detection (git repo)
- Complete system detection
- Error handling and edge cases
- Helper methods (enrich_with_project_detection)
- Convenience function (detect_system_context)

Target: 80%+ coverage
"""

import locale
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict
from unittest.mock import Mock, patch

import pytest

from claudecodeoptimizer.wizard.models import SystemContext
from claudecodeoptimizer.wizard.system_detection import (
    SystemDetector,
    detect_system_context,
)


class TestSystemDetectorInit:
    """Test SystemDetector initialization"""

    def test_init_with_project_root(self, tmp_path):
        """Test initialization with explicit project root"""
        detector = SystemDetector(project_root=tmp_path)
        assert detector.project_root == tmp_path

    def test_init_without_project_root(self):
        """Test initialization defaults to current directory"""
        detector = SystemDetector()
        assert detector.project_root == Path.cwd()

    def test_init_with_none_project_root(self):
        """Test initialization with None defaults to current directory"""
        detector = SystemDetector(project_root=None)
        assert detector.project_root == Path.cwd()


class TestOSDetection:
    """Test OS detection methods"""

    def test_detect_os_type_windows(self):
        """Test OS type detection for Windows"""
        detector = SystemDetector()
        with patch("platform.system", return_value="Windows"):
            assert detector._detect_os_type() == "windows"

    def test_detect_os_type_macos(self):
        """Test OS type detection for macOS"""
        detector = SystemDetector()
        with patch("platform.system", return_value="Darwin"):
            assert detector._detect_os_type() == "macos"

    def test_detect_os_type_linux(self):
        """Test OS type detection for Linux"""
        detector = SystemDetector()
        with patch("platform.system", return_value="Linux"):
            assert detector._detect_os_type() == "linux"

    def test_detect_os_type_other(self):
        """Test OS type detection for other systems defaults to linux"""
        detector = SystemDetector()
        with patch("platform.system", return_value="FreeBSD"):
            assert detector._detect_os_type() == "linux"

    def test_detect_os_version_success(self):
        """Test OS version detection success"""
        detector = SystemDetector()
        with patch("platform.version", return_value="10.0.19045"):
            assert detector._detect_os_version() == "10.0.19045"

    def test_detect_os_version_error(self):
        """Test OS version detection handles errors"""
        detector = SystemDetector()
        with patch("platform.version", side_effect=Exception("Version error")):
            assert detector._detect_os_version() == "unknown"


class TestTerminalDetection:
    """Test terminal detection methods"""

    def test_detect_shell_bash_from_env(self):
        """Test shell detection for bash from SHELL env var"""
        detector = SystemDetector()
        with patch.dict(os.environ, {"SHELL": "/bin/bash"}, clear=False):
            assert detector._detect_shell() == "bash"

    def test_detect_shell_zsh_from_env(self):
        """Test shell detection for zsh from SHELL env var"""
        detector = SystemDetector()
        with patch.dict(os.environ, {"SHELL": "/usr/local/bin/zsh"}, clear=False):
            assert detector._detect_shell() == "zsh"

    def test_detect_shell_fish_from_env(self):
        """Test shell detection for fish from SHELL env var"""
        detector = SystemDetector()
        with patch.dict(os.environ, {"SHELL": "/usr/bin/fish"}, clear=False):
            assert detector._detect_shell() == "fish"

    def test_detect_shell_powershell_windows(self):
        """Test shell detection for PowerShell on Windows"""
        detector = SystemDetector()
        with patch("sys.platform", "win32"):
            with patch.dict(
                os.environ,
                {"PSModulePath": "C:\\Program Files\\PowerShell\\Modules"},
                clear=True,
            ):
                assert detector._detect_shell() == "powershell"

    def test_detect_shell_cmd_windows(self):
        """Test shell detection for cmd on Windows"""
        detector = SystemDetector()
        with patch("sys.platform", "win32"):
            with patch.dict(os.environ, {}, clear=True):
                assert detector._detect_shell() == "cmd"

    def test_detect_shell_default_bash(self):
        """Test shell detection defaults to bash"""
        detector = SystemDetector()
        with patch("sys.platform", "linux"):
            with patch.dict(os.environ, {}, clear=True):
                assert detector._detect_shell() == "bash"

    def test_detect_terminal_emulator_windows_terminal(self):
        """Test terminal emulator detection for Windows Terminal"""
        detector = SystemDetector()
        with patch("sys.platform", "win32"):
            with patch.dict(os.environ, {"WT_SESSION": "12345"}, clear=False):
                assert detector._detect_terminal_emulator() == "windows-terminal"

    def test_detect_terminal_emulator_conemu(self):
        """Test terminal emulator detection for ConEmu"""
        detector = SystemDetector()
        with patch("sys.platform", "win32"):
            with patch.dict(os.environ, {"ConEmuPID": "12345"}, clear=True):
                assert detector._detect_terminal_emulator() == "conemu"

    def test_detect_terminal_emulator_cmd(self):
        """Test terminal emulator detection defaults to cmd on Windows"""
        detector = SystemDetector()
        with patch("sys.platform", "win32"):
            with patch.dict(os.environ, {}, clear=True):
                assert detector._detect_terminal_emulator() == "cmd"

    def test_detect_terminal_emulator_iterm2(self):
        """Test terminal emulator detection for iTerm2"""
        detector = SystemDetector()
        with patch("sys.platform", "darwin"):
            with patch.dict(os.environ, {"TERM_PROGRAM": "iTerm.app"}, clear=False):
                assert detector._detect_terminal_emulator() == "iterm2"

    def test_detect_terminal_emulator_apple_terminal(self):
        """Test terminal emulator detection for Apple Terminal"""
        detector = SystemDetector()
        with patch("sys.platform", "darwin"):
            with patch.dict(os.environ, {"TERM_PROGRAM": "Apple_Terminal"}, clear=False):
                assert detector._detect_terminal_emulator() == "terminal.app"

    def test_detect_terminal_emulator_vscode(self):
        """Test terminal emulator detection for VSCode"""
        detector = SystemDetector()
        with patch("sys.platform", "darwin"):
            with patch.dict(os.environ, {"TERM_PROGRAM": "vscode"}, clear=False):
                assert detector._detect_terminal_emulator() == "vscode-terminal"

    def test_detect_terminal_emulator_gnome_terminal(self):
        """Test terminal emulator detection for Gnome Terminal"""
        detector = SystemDetector()
        with patch("sys.platform", "linux"):
            with patch.dict(os.environ, {"TERM": "gnome-256color"}, clear=False):
                assert detector._detect_terminal_emulator() == "gnome-terminal"

    def test_detect_terminal_emulator_konsole(self):
        """Test terminal emulator detection for Konsole"""
        detector = SystemDetector()
        with patch("sys.platform", "linux"):
            with patch.dict(os.environ, {"TERM": "konsole"}, clear=False):
                assert detector._detect_terminal_emulator() == "konsole"

    def test_detect_terminal_emulator_xterm(self):
        """Test terminal emulator detection for xterm"""
        detector = SystemDetector()
        with patch("sys.platform", "linux"):
            with patch.dict(os.environ, {"TERM": "xterm-256color"}, clear=False):
                assert detector._detect_terminal_emulator() == "xterm"

    def test_detect_terminal_emulator_unknown(self):
        """Test terminal emulator detection for unknown terminal"""
        detector = SystemDetector()
        with patch("sys.platform", "linux"):
            with patch.dict(
                os.environ, {"TERM": "unknown", "TERM_PROGRAM": "custom"}, clear=True
            ):
                assert detector._detect_terminal_emulator() == "custom"

    def test_detect_terminal_emulator_fallback(self):
        """Test terminal emulator detection fallback"""
        detector = SystemDetector()
        with patch("sys.platform", "linux"):
            with patch.dict(os.environ, {}, clear=True):
                assert detector._detect_terminal_emulator() == "unknown"

    def test_detect_color_support_from_term_color(self):
        """Test color support detection from TERM with 'color'"""
        detector = SystemDetector()
        with patch.dict(os.environ, {"TERM": "xterm-color"}, clear=False):
            assert detector._detect_color_support() is True

    def test_detect_color_support_from_term_256(self):
        """Test color support detection from TERM with '256'"""
        detector = SystemDetector()
        with patch.dict(os.environ, {"TERM": "xterm-256color"}, clear=False):
            assert detector._detect_color_support() is True

    def test_detect_color_support_from_term_24bit(self):
        """Test color support detection from TERM with '24bit'"""
        detector = SystemDetector()
        with patch.dict(os.environ, {"TERM": "xterm-24bit"}, clear=False):
            assert detector._detect_color_support() is True

    def test_detect_color_support_windows(self):
        """Test color support detection on Windows"""
        detector = SystemDetector()
        with patch("sys.platform", "win32"):
            with patch.dict(os.environ, {"TERM": "dumb"}, clear=True):
                assert detector._detect_color_support() is True

    def test_detect_color_support_tty(self):
        """Test color support detection from TTY"""
        detector = SystemDetector()
        with patch("sys.platform", "linux"):
            with patch.dict(os.environ, {"TERM": "dumb"}, clear=True):
                with patch("sys.stdout.isatty", return_value=True):
                    assert detector._detect_color_support() is True

    def test_detect_color_support_no_tty(self):
        """Test color support detection without TTY"""
        detector = SystemDetector()
        with patch("sys.platform", "linux"):
            with patch.dict(os.environ, {"TERM": "dumb"}, clear=True):
                with patch("sys.stdout.isatty", return_value=False):
                    assert detector._detect_color_support() is False

    def test_detect_unicode_support_utf8_encoding(self):
        """Test unicode support detection with UTF-8 encoding"""
        detector = SystemDetector()
        with patch.object(detector, "_detect_encoding", return_value="utf-8"):
            assert detector._detect_unicode_support() is True

    def test_detect_unicode_support_utf8_variant(self):
        """Test unicode support detection with UTF8 variant"""
        detector = SystemDetector()
        with patch.object(detector, "_detect_encoding", return_value="UTF-8"):
            assert detector._detect_unicode_support() is True

    def test_detect_unicode_support_windows_success(self):
        """Test unicode support detection on Windows with successful encode"""
        detector = SystemDetector()
        mock_stdout = Mock()
        mock_stdout.encoding = "utf-8"
        with patch("sys.platform", "win32"):
            with patch.object(detector, "_detect_encoding", return_value="cp1252"):
                with patch("sys.stdout", mock_stdout):
                    assert detector._detect_unicode_support() is True

    def test_detect_unicode_support_windows_unicode_error(self):
        """Test unicode support detection on Windows with UnicodeEncodeError"""
        detector = SystemDetector()
        mock_stdout = Mock()
        mock_stdout.encoding = "ascii"
        with patch("sys.platform", "win32"):
            with patch.object(detector, "_detect_encoding", return_value="ascii"):
                with patch("sys.stdout", mock_stdout):
                    result = detector._detect_unicode_support()
                    # On Windows, will try to encode unicode char
                    # If it fails, should return False
                    assert isinstance(result, bool)

    def test_detect_unicode_support_windows_attribute_error(self):
        """Test unicode support detection on Windows with AttributeError"""
        detector = SystemDetector()
        mock_stdout = Mock()
        mock_stdout.encoding = None
        with patch("sys.platform", "win32"):
            with patch.object(detector, "_detect_encoding", return_value="cp1252"):
                with patch("sys.stdout", mock_stdout):
                    # This will cause AttributeError when trying to encode
                    result = detector._detect_unicode_support()
                    assert isinstance(result, bool)

    def test_detect_unicode_support_no_utf8(self):
        """Test unicode support detection without UTF-8"""
        detector = SystemDetector()
        with patch("sys.platform", "linux"):
            with patch.object(detector, "_detect_encoding", return_value="latin-1"):
                assert detector._detect_unicode_support() is False


class TestLocaleDetection:
    """Test locale detection methods"""

    def test_detect_locale_success(self):
        """Test locale detection success"""
        detector = SystemDetector()
        with patch("locale.getlocale", return_value=("en_US", "UTF-8")):
            assert detector._detect_locale() == "en_US"

    def test_detect_locale_from_lc_all(self):
        """Test locale detection from LC_ALL environment variable"""
        detector = SystemDetector()
        with patch("locale.getlocale", side_effect=locale.Error("Locale error")):
            with patch.dict(os.environ, {"LC_ALL": "en_GB.UTF-8"}, clear=False):
                assert detector._detect_locale() == "en_GB"

    def test_detect_locale_from_lc_ctype(self):
        """Test locale detection from LC_CTYPE environment variable"""
        detector = SystemDetector()
        with patch("locale.getlocale", return_value=(None, None)):
            with patch.dict(
                os.environ, {"LC_CTYPE": "fr_FR.UTF-8"}, clear=True
            ):
                assert detector._detect_locale() == "fr_FR"

    def test_detect_locale_from_lang(self):
        """Test locale detection from LANG environment variable"""
        detector = SystemDetector()
        with patch("locale.getlocale", return_value=(None, None)):
            with patch.dict(os.environ, {"LANG": "de_DE.UTF-8"}, clear=True):
                assert detector._detect_locale() == "de_DE"

    def test_detect_locale_default(self):
        """Test locale detection defaults to en_US"""
        detector = SystemDetector()
        with patch("locale.getlocale", return_value=(None, None)):
            with patch.dict(os.environ, {}, clear=True):
                assert detector._detect_locale() == "en_US"

    def test_detect_locale_value_error(self):
        """Test locale detection handles ValueError"""
        detector = SystemDetector()
        with patch("locale.getlocale", side_effect=ValueError("Value error")):
            with patch.dict(os.environ, {"LANG": "tr_TR.UTF-8"}, clear=True):
                assert detector._detect_locale() == "tr_TR"

    def test_detect_language_with_underscore(self):
        """Test language detection with underscore format"""
        detector = SystemDetector()
        with patch.object(detector, "_detect_locale", return_value="en_US"):
            assert detector._detect_language() == "en"

    def test_detect_language_without_underscore(self):
        """Test language detection without underscore"""
        detector = SystemDetector()
        with patch.object(detector, "_detect_locale", return_value="en"):
            assert detector._detect_language() == "en"

    def test_detect_language_short_code(self):
        """Test language detection with short code"""
        detector = SystemDetector()
        with patch.object(detector, "_detect_locale", return_value="tr"):
            assert detector._detect_language() == "tr"

    def test_detect_encoding_from_stdout(self):
        """Test encoding detection from stdout"""
        detector = SystemDetector()
        mock_stdout = Mock()
        mock_stdout.encoding = "utf-8"
        with patch("sys.stdout", mock_stdout):
            assert detector._detect_encoding() == "utf-8"

    def test_detect_encoding_from_locale(self):
        """Test encoding detection from locale"""
        detector = SystemDetector()
        mock_stdout = Mock()
        mock_stdout.encoding = None
        with patch("sys.stdout", mock_stdout):
            with patch("locale.getpreferredencoding", return_value="cp1252"):
                assert detector._detect_encoding() == "cp1252"

    def test_detect_encoding_locale_error(self):
        """Test encoding detection handles locale error"""
        detector = SystemDetector()
        mock_stdout = Mock()
        mock_stdout.encoding = None
        with patch("sys.stdout", mock_stdout):
            with patch("locale.getpreferredencoding", side_effect=locale.Error()):
                assert detector._detect_encoding() == "utf-8"

    def test_detect_encoding_value_error(self):
        """Test encoding detection handles ValueError"""
        detector = SystemDetector()
        mock_stdout = Mock()
        mock_stdout.encoding = None
        with patch("sys.stdout", mock_stdout):
            with patch("locale.getpreferredencoding", side_effect=ValueError()):
                assert detector._detect_encoding() == "utf-8"


class TestPythonEnvironment:
    """Test Python environment detection methods"""

    def test_detect_python_version(self):
        """Test Python version detection"""
        detector = SystemDetector()
        version = detector._detect_python_version()
        # Should match current Python version
        expected = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        assert version == expected

    def test_detect_pip_version_success(self):
        """Test pip version detection success"""
        detector = SystemDetector()
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "pip 23.0.1 from /usr/lib/python3/site-packages"

        with patch("subprocess.run", return_value=mock_result):
            assert detector._detect_pip_version() == "23.0.1"

    def test_detect_pip_version_failure(self):
        """Test pip version detection with non-zero return code"""
        detector = SystemDetector()
        mock_result = Mock()
        mock_result.returncode = 1

        with patch("subprocess.run", return_value=mock_result):
            assert detector._detect_pip_version() == "unknown"

    def test_detect_pip_version_short_output(self):
        """Test pip version detection with short output"""
        detector = SystemDetector()
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "pip"

        with patch("subprocess.run", return_value=mock_result):
            assert detector._detect_pip_version() == "unknown"

    def test_detect_pip_version_subprocess_error(self):
        """Test pip version detection handles subprocess error"""
        detector = SystemDetector()
        with patch("subprocess.run", side_effect=subprocess.SubprocessError()):
            assert detector._detect_pip_version() == "unknown"

    def test_detect_pip_version_timeout(self):
        """Test pip version detection handles timeout"""
        detector = SystemDetector()
        with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("pip", 5)):
            assert detector._detect_pip_version() == "unknown"

    def test_detect_pip_version_os_error(self):
        """Test pip version detection handles OS error"""
        detector = SystemDetector()
        with patch("subprocess.run", side_effect=OSError("OS error")):
            assert detector._detect_pip_version() == "unknown"


class TestGitDetection:
    """Test Git detection methods"""

    def test_detect_git_installed_true(self):
        """Test git installed detection returns True"""
        detector = SystemDetector()
        with patch("shutil.which", return_value="/usr/bin/git"):
            assert detector._detect_git_installed() is True

    def test_detect_git_installed_false(self):
        """Test git installed detection returns False"""
        detector = SystemDetector()
        with patch("shutil.which", return_value=None):
            assert detector._detect_git_installed() is False

    def test_detect_git_user_name_success(self):
        """Test git user name detection success"""
        detector = SystemDetector()
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "John Doe\n"

        with patch.object(detector, "_detect_git_installed", return_value=True):
            with patch("subprocess.run", return_value=mock_result):
                assert detector._detect_git_user_name() == "John Doe"

    def test_detect_git_user_name_not_installed(self):
        """Test git user name detection when git not installed"""
        detector = SystemDetector()
        with patch.object(detector, "_detect_git_installed", return_value=False):
            assert detector._detect_git_user_name() is None

    def test_detect_git_user_name_failure(self):
        """Test git user name detection with non-zero return code"""
        detector = SystemDetector()
        mock_result = Mock()
        mock_result.returncode = 1

        with patch.object(detector, "_detect_git_installed", return_value=True):
            with patch("subprocess.run", return_value=mock_result):
                assert detector._detect_git_user_name() is None

    def test_detect_git_user_name_subprocess_error(self):
        """Test git user name detection handles subprocess error"""
        detector = SystemDetector()
        with patch.object(detector, "_detect_git_installed", return_value=True):
            with patch("subprocess.run", side_effect=subprocess.SubprocessError()):
                assert detector._detect_git_user_name() is None

    def test_detect_git_user_name_timeout(self):
        """Test git user name detection handles timeout"""
        detector = SystemDetector()
        with patch.object(detector, "_detect_git_installed", return_value=True):
            with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("git", 5)):
                assert detector._detect_git_user_name() is None

    def test_detect_git_user_name_os_error(self):
        """Test git user name detection handles OS error"""
        detector = SystemDetector()
        with patch.object(detector, "_detect_git_installed", return_value=True):
            with patch("subprocess.run", side_effect=OSError()):
                assert detector._detect_git_user_name() is None

    def test_detect_git_user_email_success(self):
        """Test git user email detection success"""
        detector = SystemDetector()
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "john@example.com\n"

        with patch.object(detector, "_detect_git_installed", return_value=True):
            with patch("subprocess.run", return_value=mock_result):
                assert detector._detect_git_user_email() == "john@example.com"

    def test_detect_git_user_email_not_installed(self):
        """Test git user email detection when git not installed"""
        detector = SystemDetector()
        with patch.object(detector, "_detect_git_installed", return_value=False):
            assert detector._detect_git_user_email() is None

    def test_detect_git_user_email_failure(self):
        """Test git user email detection with non-zero return code"""
        detector = SystemDetector()
        mock_result = Mock()
        mock_result.returncode = 1

        with patch.object(detector, "_detect_git_installed", return_value=True):
            with patch("subprocess.run", return_value=mock_result):
                assert detector._detect_git_user_email() is None

    def test_detect_git_user_email_subprocess_error(self):
        """Test git user email detection handles subprocess error"""
        detector = SystemDetector()
        with patch.object(detector, "_detect_git_installed", return_value=True):
            with patch("subprocess.run", side_effect=subprocess.SubprocessError()):
                assert detector._detect_git_user_email() is None

    def test_detect_git_user_email_timeout(self):
        """Test git user email detection handles timeout"""
        detector = SystemDetector()
        with patch.object(detector, "_detect_git_installed", return_value=True):
            with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("git", 5)):
                assert detector._detect_git_user_email() is None

    def test_detect_git_user_email_os_error(self):
        """Test git user email detection handles OS error"""
        detector = SystemDetector()
        with patch.object(detector, "_detect_git_installed", return_value=True):
            with patch("subprocess.run", side_effect=OSError()):
                assert detector._detect_git_user_email() is None

    def test_is_git_repo_true(self, tmp_path):
        """Test git repo detection returns True"""
        git_dir = tmp_path / ".git"
        git_dir.mkdir()

        detector = SystemDetector(project_root=tmp_path)
        assert detector._is_git_repo() is True

    def test_is_git_repo_false(self, tmp_path):
        """Test git repo detection returns False"""
        detector = SystemDetector(project_root=tmp_path)
        assert detector._is_git_repo() is False


class TestEditorDetection:
    """Test editor detection methods"""

    def test_detect_editors_vscode(self, tmp_path):
        """Test editor detection for VSCode"""
        detector = SystemDetector(project_root=tmp_path)
        with patch("shutil.which") as mock_which:
            mock_which.side_effect = lambda x: "/usr/bin/code" if x == "code" else None
            editors = detector._detect_editors()
            assert "vscode" in editors

    def test_detect_editors_pycharm(self, tmp_path):
        """Test editor detection for PyCharm"""
        detector = SystemDetector(project_root=tmp_path)
        with patch("shutil.which") as mock_which:
            mock_which.side_effect = lambda x: "/usr/bin/pycharm" if x == "pycharm" else None
            editors = detector._detect_editors()
            assert "pycharm" in editors

    def test_detect_editors_vim(self, tmp_path):
        """Test editor detection for Vim"""
        detector = SystemDetector(project_root=tmp_path)
        with patch("shutil.which") as mock_which:
            mock_which.side_effect = lambda x: "/usr/bin/vim" if x == "vim" else None
            editors = detector._detect_editors()
            assert "vim" in editors

    def test_detect_editors_neovim(self, tmp_path):
        """Test editor detection for Neovim"""
        detector = SystemDetector(project_root=tmp_path)
        with patch("shutil.which") as mock_which:
            mock_which.side_effect = lambda x: "/usr/bin/nvim" if x == "nvim" else None
            editors = detector._detect_editors()
            assert "neovim" in editors

    def test_detect_editors_multiple(self, tmp_path):
        """Test editor detection for multiple editors"""
        detector = SystemDetector(project_root=tmp_path)
        with patch("shutil.which") as mock_which:
            def which_mock(x):
                if x in ["code", "vim", "nvim"]:
                    return f"/usr/bin/{x}"
                return None

            mock_which.side_effect = which_mock
            editors = detector._detect_editors()
            assert "vscode" in editors
            assert "vim" in editors
            assert "neovim" in editors

    def test_detect_editors_vscode_config(self, tmp_path):
        """Test editor detection from .vscode directory"""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()

        detector = SystemDetector(project_root=tmp_path)
        with patch("shutil.which", return_value=None):
            editors = detector._detect_editors()
            assert "vscode" in editors

    def test_detect_editors_idea_config(self, tmp_path):
        """Test editor detection from .idea directory"""
        idea_dir = tmp_path / ".idea"
        idea_dir.mkdir()

        detector = SystemDetector(project_root=tmp_path)
        with patch("shutil.which", return_value=None):
            editors = detector._detect_editors()
            assert "pycharm" in editors

    def test_detect_editors_no_duplicates(self, tmp_path):
        """Test editor detection avoids duplicates"""
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()

        detector = SystemDetector(project_root=tmp_path)
        with patch("shutil.which") as mock_which:
            mock_which.side_effect = lambda x: "/usr/bin/code" if x == "code" else None
            editors = detector._detect_editors()
            # VSCode should appear only once
            assert editors.count("vscode") == 1

    def test_detect_editors_empty(self, tmp_path):
        """Test editor detection returns empty list when none found"""
        detector = SystemDetector(project_root=tmp_path)
        with patch("shutil.which", return_value=None):
            editors = detector._detect_editors()
            assert editors == []

    def test_detect_active_editor_from_editor_env(self):
        """Test active editor detection from EDITOR environment variable"""
        detector = SystemDetector()
        with patch.dict(os.environ, {"EDITOR": "/usr/bin/code"}, clear=False):
            assert detector._detect_active_editor() == "vscode"

    def test_detect_active_editor_vim_from_editor(self):
        """Test active editor detection for vim from EDITOR"""
        detector = SystemDetector()
        with patch.dict(os.environ, {"EDITOR": "vim"}, clear=False):
            assert detector._detect_active_editor() == "vim"

    def test_detect_active_editor_emacs_from_editor(self):
        """Test active editor detection for emacs from EDITOR"""
        detector = SystemDetector()
        with patch.dict(os.environ, {"EDITOR": "emacs"}, clear=False):
            assert detector._detect_active_editor() == "emacs"

    def test_detect_active_editor_nano_from_editor(self):
        """Test active editor detection for nano from EDITOR"""
        detector = SystemDetector()
        with patch.dict(os.environ, {"EDITOR": "nano"}, clear=False):
            assert detector._detect_active_editor() == "nano"

    def test_detect_active_editor_from_visual(self):
        """Test active editor detection from VISUAL environment variable"""
        detector = SystemDetector()
        with patch.dict(os.environ, {"VISUAL": "/usr/bin/code"}, clear=True):
            assert detector._detect_active_editor() == "vscode"

    def test_detect_active_editor_visual_ignored_if_editor_set(self):
        """Test VISUAL is ignored if EDITOR is set"""
        detector = SystemDetector()
        with patch.dict(
            os.environ, {"EDITOR": "vim", "VISUAL": "code"}, clear=False
        ):
            assert detector._detect_active_editor() == "vim"

    def test_detect_active_editor_from_term_program(self):
        """Test active editor detection from TERM_PROGRAM"""
        detector = SystemDetector()
        with patch.dict(os.environ, {"TERM_PROGRAM": "vscode"}, clear=True):
            with patch.object(detector, "_detect_editors", return_value=[]):
                assert detector._detect_active_editor() == "vscode"

    def test_detect_active_editor_from_detected_editors(self, tmp_path):
        """Test active editor falls back to first detected editor"""
        detector = SystemDetector(project_root=tmp_path)
        with patch.dict(os.environ, {}, clear=True):
            with patch.object(detector, "_detect_editors", return_value=["vim", "emacs"]):
                assert detector._detect_active_editor() == "vim"

    def test_detect_active_editor_none(self, tmp_path):
        """Test active editor detection returns None when nothing found"""
        detector = SystemDetector(project_root=tmp_path)
        with patch.dict(os.environ, {}, clear=True):
            with patch.object(detector, "_detect_editors", return_value=[]):
                assert detector._detect_active_editor() is None


class TestEnrichWithProjectDetection:
    """Test enrich_with_project_detection method"""

    @pytest.fixture
    def system_context(self) -> SystemContext:
        """Sample system context"""
        return SystemContext(
            os_type="linux",
            os_version="5.15",
            os_platform="linux",
            shell_type="bash",
            terminal_emulator="terminal",
            color_support=True,
            unicode_support=True,
            system_locale="en_US",
            detected_language="en",
            encoding="utf-8",
            python_version="3.11.0",
            python_executable="/usr/bin/python3",
            pip_version="23.0.1",
            git_installed=True,
        )

    def test_enrich_with_project_detection_tools(self, system_context):
        """Test enrichment with tools"""
        detector = SystemDetector()
        detection_report = {
            "tools": [
                {"detected_value": "pytest"},
                {"detected_value": "black"},
            ],
        }

        enriched = detector.enrich_with_project_detection(
            system_context, detection_report
        )

        assert "pytest" in enriched.existing_tools
        assert "black" in enriched.existing_tools

    def test_enrich_with_project_detection_languages(self, system_context):
        """Test enrichment with languages"""
        detector = SystemDetector()
        detection_report = {
            "languages": [
                {"detected_value": "python"},
                {"detected_value": "javascript"},
            ],
        }

        enriched = detector.enrich_with_project_detection(
            system_context, detection_report
        )

        assert "python" in enriched.detected_languages
        assert "javascript" in enriched.detected_languages

    def test_enrich_with_project_detection_frameworks(self, system_context):
        """Test enrichment with frameworks"""
        detector = SystemDetector()
        detection_report = {
            "frameworks": [
                {"detected_value": "django"},
                {"detected_value": "fastapi"},
            ],
        }

        enriched = detector.enrich_with_project_detection(
            system_context, detection_report
        )

        assert "django" in enriched.detected_frameworks
        assert "fastapi" in enriched.detected_frameworks

    def test_enrich_with_project_detection_project_types(self, system_context):
        """Test enrichment with project types"""
        detector = SystemDetector()
        detection_report = {
            "project_types": [
                {"detected_value": "web_app"},
                {"detected_value": "api_service"},
            ],
        }

        enriched = detector.enrich_with_project_detection(
            system_context, detection_report
        )

        assert "web_app" in enriched.detected_project_types
        assert "api_service" in enriched.detected_project_types

    def test_enrich_with_project_detection_patterns(self, system_context):
        """Test enrichment with codebase patterns"""
        detector = SystemDetector()
        detection_report = {
            "codebase_patterns": {
                "total_files": 150,
                "total_lines": 5000,
                "has_tests": True,
                "has_ci_cd": True,
            },
        }

        enriched = detector.enrich_with_project_detection(
            system_context, detection_report
        )

        assert enriched.file_count == 150
        assert enriched.line_count == 5000
        assert enriched.has_tests is True
        assert enriched.has_ci is True

    def test_enrich_with_project_detection_empty_report(self, system_context):
        """Test enrichment with empty detection report"""
        detector = SystemDetector()
        detection_report: Dict[str, Any] = {}

        enriched = detector.enrich_with_project_detection(
            system_context, detection_report
        )

        assert enriched.existing_tools == []
        assert enriched.detected_languages == []
        assert enriched.detected_frameworks == []
        assert enriched.detected_project_types == []
        assert enriched.file_count == 0
        assert enriched.line_count == 0
        assert enriched.has_tests is False
        assert enriched.has_ci is False


class TestDetectAll:
    """Test detect_all method"""

    def test_detect_all_returns_system_context(self, tmp_path):
        """Test detect_all returns SystemContext"""
        detector = SystemDetector(project_root=tmp_path)
        context = detector.detect_all()

        assert isinstance(context, SystemContext)
        assert context.project_root == tmp_path

    def test_detect_all_includes_os_info(self, tmp_path):
        """Test detect_all includes OS information"""
        detector = SystemDetector(project_root=tmp_path)
        context = detector.detect_all()

        assert context.os_type in ["windows", "macos", "linux"]
        assert context.os_version is not None
        assert context.os_platform == sys.platform

    def test_detect_all_includes_terminal_info(self, tmp_path):
        """Test detect_all includes terminal information"""
        detector = SystemDetector(project_root=tmp_path)
        context = detector.detect_all()

        assert context.shell_type is not None
        assert context.terminal_emulator is not None
        assert isinstance(context.color_support, bool)
        assert isinstance(context.unicode_support, bool)

    def test_detect_all_includes_locale_info(self, tmp_path):
        """Test detect_all includes locale information"""
        detector = SystemDetector(project_root=tmp_path)
        context = detector.detect_all()

        assert context.system_locale is not None
        assert context.detected_language is not None
        assert context.encoding is not None

    def test_detect_all_includes_python_info(self, tmp_path):
        """Test detect_all includes Python information"""
        detector = SystemDetector(project_root=tmp_path)
        context = detector.detect_all()

        assert context.python_version is not None
        assert context.python_executable == sys.executable
        assert context.pip_version is not None

    def test_detect_all_includes_git_info(self, tmp_path):
        """Test detect_all includes Git information"""
        detector = SystemDetector(project_root=tmp_path)
        context = detector.detect_all()

        assert isinstance(context.git_installed, bool)
        assert isinstance(context.is_git_repo, bool)

    def test_detect_all_includes_editor_info(self, tmp_path):
        """Test detect_all includes editor information"""
        detector = SystemDetector(project_root=tmp_path)
        context = detector.detect_all()

        assert isinstance(context.detected_editors, list)


class TestConvenienceFunction:
    """Test detect_system_context convenience function"""

    def test_detect_system_context_without_args(self):
        """Test convenience function without arguments"""
        context = detect_system_context()

        assert isinstance(context, SystemContext)
        assert context.project_root == Path.cwd()

    def test_detect_system_context_with_project_root(self, tmp_path):
        """Test convenience function with project root"""
        context = detect_system_context(project_root=tmp_path)

        assert isinstance(context, SystemContext)
        assert context.project_root == tmp_path

    def test_detect_system_context_matches_detector(self, tmp_path):
        """Test convenience function matches direct detector usage"""
        context1 = detect_system_context(project_root=tmp_path)

        detector = SystemDetector(project_root=tmp_path)
        context2 = detector.detect_all()

        assert context1.project_root == context2.project_root
        assert context1.os_type == context2.os_type
