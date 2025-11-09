"""
System Context Detection (TIER 0)

Automatically detects system, terminal, locale, and project context.
This information is used to:
1. Adapt command syntax (PowerShell vs Bash)
2. Choose appropriate output formatting (unicode vs ascii)
3. Set language preferences
4. Detect development environment
5. Inform AI recommendations
"""

import locale
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

from .models import SystemContext


class SystemDetector:
    """Detect system environment and context"""

    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path.cwd()

    def detect_all(self) -> SystemContext:
        """Run all detection and return SystemContext"""
        return SystemContext(
            # OS
            os_type=self._detect_os_type(),
            os_version=self._detect_os_version(),
            os_platform=sys.platform,
            # Terminal
            shell_type=self._detect_shell(),
            terminal_emulator=self._detect_terminal_emulator(),
            color_support=self._detect_color_support(),
            unicode_support=self._detect_unicode_support(),
            # Locale
            system_locale=self._detect_locale(),
            detected_language=self._detect_language(),
            encoding=self._detect_encoding(),
            # Python
            python_version=self._detect_python_version(),
            python_executable=sys.executable,
            pip_version=self._detect_pip_version(),
            # Git
            git_installed=self._detect_git_installed(),
            git_user_name=self._detect_git_user_name(),
            git_user_email=self._detect_git_user_email(),
            # Editors
            detected_editors=self._detect_editors(),
            active_editor=self._detect_active_editor(),
            # Project (will be enriched by UniversalDetector)
            project_root=self.project_root,
            is_git_repo=self._is_git_repo(),
        )

    # ========================================================================
    # OS Detection
    # ========================================================================

    def _detect_os_type(self) -> str:
        """Detect OS type"""
        system = platform.system().lower()
        if system == "windows":
            return "windows"
        elif system == "darwin":
            return "macos"
        else:
            return "linux"

    def _detect_os_version(self) -> str:
        """Detect OS version"""
        try:
            return platform.version()
        except Exception:
            return "unknown"

    # ========================================================================
    # Terminal Detection
    # ========================================================================

    def _detect_shell(self) -> str:
        """Detect active shell"""
        # Check SHELL environment variable
        shell_env = os.environ.get("SHELL", "")
        if shell_env:
            shell_name = Path(shell_env).name.lower()
            if "bash" in shell_name:
                return "bash"
            elif "zsh" in shell_name:
                return "zsh"
            elif "fish" in shell_name:
                return "fish"

        # Check on Windows
        if sys.platform == "win32":
            # Check if running in PowerShell
            if os.environ.get("PSModulePath"):
                return "powershell"
            return "cmd"

        # Default
        return "bash"

    def _detect_terminal_emulator(self) -> str:
        """Detect terminal emulator"""
        # Windows
        if sys.platform == "win32":
            if os.environ.get("WT_SESSION"):
                return "windows-terminal"
            elif os.environ.get("ConEmuPID"):
                return "conemu"
            return "cmd"

        # macOS
        if sys.platform == "darwin":
            term_program = os.environ.get("TERM_PROGRAM", "")
            if "iterm" in term_program.lower():
                return "iterm2"
            elif "apple_terminal" in term_program.lower():
                return "terminal.app"
            elif "vscode" in term_program.lower():
                return "vscode-terminal"

        # Linux
        term = os.environ.get("TERM", "")
        if "gnome" in term:
            return "gnome-terminal"
        elif "konsole" in term:
            return "konsole"
        elif "xterm" in term:
            return "xterm"

        return os.environ.get("TERM_PROGRAM", "unknown")

    def _detect_color_support(self) -> bool:
        """Check if terminal supports colors"""
        # Check TERM environment
        term = os.environ.get("TERM", "")
        if "color" in term or "256" in term or "24bit" in term:
            return True

        # Check for known color-supporting terminals
        if sys.platform == "win32":
            # Windows 10+ supports colors
            return True

        # Check if stdout is a TTY
        return sys.stdout.isatty()

    def _detect_unicode_support(self) -> bool:
        """Check if terminal supports unicode"""
        # Check encoding
        encoding = self._detect_encoding().lower()
        if "utf-8" in encoding or "utf8" in encoding:
            return True

        # Windows with unicode support
        if sys.platform == "win32":
            try:
                # Try to encode unicode character
                "✓".encode(sys.stdout.encoding or "utf-8")
                return True
            except (UnicodeEncodeError, AttributeError):
                return False

        return False

    # ========================================================================
    # Locale Detection
    # ========================================================================

    def _detect_locale(self) -> str:
        """Detect system locale"""
        try:
            # Try to get locale
            loc, _ = locale.getlocale()
            if loc:
                return loc
        except Exception:
            pass

        # Fallback to environment variables
        for env_var in ["LC_ALL", "LC_CTYPE", "LANG"]:
            val = os.environ.get(env_var)
            if val:
                return val.split(".")[0]  # e.g., "en_US.UTF-8" -> "en_US"

        return "en_US"

    def _detect_language(self) -> str:
        """Detect user language (2-letter code)"""
        loc = self._detect_locale()
        # Extract language code (e.g., "en_US" -> "en", "tr_TR" -> "tr")
        return loc.split("_")[0].lower() if "_" in loc else loc[:2].lower()

    def _detect_encoding(self) -> str:
        """Detect system encoding"""
        # Try stdout encoding first
        if hasattr(sys.stdout, "encoding") and sys.stdout.encoding:
            return sys.stdout.encoding

        # Try locale encoding
        try:
            return locale.getpreferredencoding()
        except Exception:
            pass

        # Fallback
        return "utf-8"

    # ========================================================================
    # Python Environment
    # ========================================================================

    def _detect_python_version(self) -> str:
        """Get Python version"""
        return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

    def _detect_pip_version(self) -> str:
        """Get pip version"""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "--version"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                # Parse "pip 23.0.1 from ..."
                parts = result.stdout.split()
                if len(parts) >= 2:
                    return parts[1]
        except Exception:
            pass
        return "unknown"

    # ========================================================================
    # Git Detection
    # ========================================================================

    def _detect_git_installed(self) -> bool:
        """Check if git is installed"""
        return shutil.which("git") is not None

    def _detect_git_user_name(self) -> Optional[str]:
        """Get git user name"""
        if not self._detect_git_installed():
            return None

        try:
            result = subprocess.run(
                ["git", "config", "--global", "user.name"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception:
            pass
        return None

    def _detect_git_user_email(self) -> Optional[str]:
        """Get git user email"""
        if not self._detect_git_installed():
            return None

        try:
            result = subprocess.run(
                ["git", "config", "--global", "user.email"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception:
            pass
        return None

    def _is_git_repo(self) -> bool:
        """Check if project root is a git repository"""
        git_dir = self.project_root / ".git"
        return git_dir.exists()

    # ========================================================================
    # Editor Detection
    # ========================================================================

    def _detect_editors(self) -> List[str]:
        """Detect installed editors/IDEs"""
        editors = []

        # Check for common editor executables
        editor_executables = {
            "code": "vscode",
            "code-insiders": "vscode-insiders",
            "pycharm": "pycharm",
            "idea": "intellij-idea",
            "vim": "vim",
            "nvim": "neovim",
            "emacs": "emacs",
            "subl": "sublime",
            "atom": "atom",
        }

        for executable, editor_name in editor_executables.items():
            if shutil.which(executable):
                editors.append(editor_name)

        # Check for IDE config directories
        if (self.project_root / ".vscode").exists():
            if "vscode" not in editors:
                editors.append("vscode")

        if (self.project_root / ".idea").exists():
            if "pycharm" not in editors and "intellij-idea" not in editors:
                editors.append("pycharm")

        return editors

    def _detect_active_editor(self) -> Optional[str]:
        """Detect currently active/preferred editor"""
        # Check EDITOR environment variable
        editor_env = os.environ.get("EDITOR", "")
        if editor_env:
            editor_name = Path(editor_env).name.lower()
            if "code" in editor_name:
                return "vscode"
            elif "vim" in editor_name:
                return "vim"
            elif "emacs" in editor_name:
                return "emacs"
            elif "nano" in editor_name:
                return "nano"

        # Check VISUAL
        visual_env = os.environ.get("VISUAL", "")
        if visual_env and not editor_env:
            editor_name = Path(visual_env).name.lower()
            if "code" in editor_name:
                return "vscode"

        # Check running in vscode terminal
        if os.environ.get("TERM_PROGRAM") == "vscode":
            return "vscode"

        # Use first detected editor
        detected = self._detect_editors()
        return detected[0] if detected else None

    # ========================================================================
    # Helper Methods
    # ========================================================================

    def enrich_with_project_detection(
        self,
        context: SystemContext,
        detection_report: dict,
    ) -> SystemContext:
        """
        Enrich SystemContext with data from UniversalDetector.

        This bridges TIER 0 (system) with project detection.
        """
        # Extract data from detection report
        context.existing_tools = [
            tool["detected_value"] for tool in detection_report.get("tools", [])
        ]
        context.detected_languages = [
            lang["detected_value"] for lang in detection_report.get("languages", [])
        ]
        context.detected_frameworks = [
            fw["detected_value"] for fw in detection_report.get("frameworks", [])
        ]
        context.detected_project_types = [
            pt["detected_value"] for pt in detection_report.get("project_types", [])
        ]

        # Extract patterns
        patterns = detection_report.get("codebase_patterns", {})
        context.file_count = patterns.get("total_files", 0)
        context.line_count = patterns.get("total_lines", 0)
        context.has_tests = patterns.get("has_tests", False)
        context.has_ci = patterns.get("has_ci_cd", False)

        return context


# Convenience function
def detect_system_context(project_root: Optional[Path] = None) -> SystemContext:
    """
    Detect system context for CCO wizard.

    Args:
        project_root: Project root directory (default: current directory)

    Returns:
        SystemContext with all detected information
    """
    detector = SystemDetector(project_root)
    return detector.detect_all()
