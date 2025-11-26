"""
Central configuration and branding for ClaudeCodeOptimizer.

All naming, paths, and branding are managed from this single source of truth.
"""

from pathlib import Path
from typing import Any

# ============================================================================
# BRANDING & NAMING (Module-level constants)
# ============================================================================

BRAND_NAME = "CCO"
FULL_NAME = "ClaudeCodeOptimizer"
PACKAGE_NAME = "claudecodeoptimizer"

# Version is imported from __init__.py to maintain single source of truth
from . import __version__ as VERSION  # noqa: E402, N812

# Display names
DISPLAY_NAME = "Claude Code Optimizer"
SHORT_NAME = "CCO"
CLI_NAME = "cco"

# Command prefix
COMMAND_PREFIX = "cco"

# ============================================================================
# PATH HELPERS
# ============================================================================


def get_home_dir() -> Path:
    """Get user home directory."""
    return Path.home()


def get_claude_dir() -> Path:
    """Get Claude directory (~/.claude/)."""
    return Path.home() / ".claude"


def get_global_commands_dir() -> Path:
    """
    Get global commands directory (~/.claude/commands/).

    All CCO commands stored globally in Claude Code's standard location.
    """
    return get_claude_dir() / "commands"


def get_agents_dir() -> Path:
    """
    Get global agents directory (~/.claude/agents/).

    All CCO agent definitions stored globally.
    """
    return get_claude_dir() / "agents"


# ============================================================================
# COMMAND NAMING
# ============================================================================


def get_command_name(action: str) -> str:
    """
    Generate command name with CCO brand prefix.

    Args:
        action: Command action name (e.g., "help", "status", "audit")

    Returns:
        Formatted command name with prefix (e.g., "/cco-help", "/cco-status")

    Example:
        >>> get_command_name("help")
        '/cco-help'
        >>> get_command_name("audit")
        '/cco-audit'
    """
    return f"/{COMMAND_PREFIX}-{action}"


# ============================================================================
# FILE MARKERS & IDENTIFIERS
# ============================================================================

# Git ignore patterns - CCO keeps project directories completely clean
GITIGNORE_PATTERNS: list[str] = []

# ============================================================================
# DEFAULTS & PREFERENCES
# ============================================================================

DEFAULT_CONFIG = {
    "version": VERSION,
    "brand": {
        "name": BRAND_NAME,
        "full_name": FULL_NAME,
        "display_name": DISPLAY_NAME,
    },
    "paths": {
        "claude_dir": str(get_claude_dir()),
    },
}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================


def get_all_paths() -> dict[str, Path]:
    """
    Get dictionary of all configured paths.

    Returns:
        Dictionary mapping path names to Path objects:
        - claude_dir: ~/.claude/ (base directory)
        - commands_dir: ~/.claude/commands/
        - agents_dir: ~/.claude/agents/

    Example:
        >>> paths = get_all_paths()
        >>> paths["claude_dir"]
        PosixPath('/home/user/.claude')
    """
    return {
        "claude_dir": get_claude_dir(),
        "commands_dir": get_global_commands_dir(),
        "agents_dir": get_agents_dir(),
    }


# ============================================================================
# CCOConfig Class
# ============================================================================


class CCOConfig:
    """
    Central configuration class for ClaudeCodeOptimizer.

    Provides namespace access to all module-level configuration values.
    """

    # Branding
    BRAND_NAME = BRAND_NAME
    FULL_NAME = FULL_NAME
    PACKAGE_NAME = PACKAGE_NAME
    VERSION = VERSION
    DISPLAY_NAME = DISPLAY_NAME
    SHORT_NAME = SHORT_NAME
    CLI_NAME = CLI_NAME
    COMMAND_PREFIX = COMMAND_PREFIX

    # File markers
    GITIGNORE_PATTERNS = GITIGNORE_PATTERNS

    # Defaults
    DEFAULT_CONFIG = DEFAULT_CONFIG

    # Static methods (delegate to module functions)
    get_home_dir = staticmethod(get_home_dir)

    get_claude_dir = staticmethod(get_claude_dir)

    get_global_commands_dir = staticmethod(get_global_commands_dir)
    get_agents_dir = staticmethod(get_agents_dir)

    # REMOVED: get_project_backups_dir - No backups with stateless architecture
    get_command_name = staticmethod(get_command_name)
    get_all_paths = staticmethod(get_all_paths)

    @staticmethod
    def to_dict() -> dict[str, Any]:
        """Export config as dictionary."""
        return {
            "branding": {
                "brand_name": BRAND_NAME,
                "full_name": FULL_NAME,
                "display_name": DISPLAY_NAME,
                "cli_name": CLI_NAME,
                "version": VERSION,
            },
            "paths": {
                "claude_dir": str(get_claude_dir()),
            },
            "commands": {
                "prefix": COMMAND_PREFIX,
                "init": get_command_name("init"),
                "status": get_command_name("status"),
                "help": get_command_name("help"),
            },
            "defaults": DEFAULT_CONFIG,
        }


# Convenience singleton
CONFIG = CCOConfig()

__all__ = [
    "CCOConfig",
    "CONFIG",
    "BRAND_NAME",
    "FULL_NAME",
    "DISPLAY_NAME",
    "SHORT_NAME",
    "CLI_NAME",
    "VERSION",
    "COMMAND_PREFIX",
]
