"""
Central configuration and branding for ClaudeCodeOptimizer.

All naming, paths, and branding are managed from this single source of truth.
"""

from pathlib import Path
from typing import Any, Dict

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


def get_global_dir() -> Path:
    """Get global CCO directory (~/.cco/)."""
    return Path.home() / f".{CLI_NAME}"


def get_claude_dir() -> Path:
    """Get Claude directory (~/.claude/)."""
    return Path.home() / ".claude"


def get_templates_dir() -> Path:
    """Get global templates directory (~/.cco/templates/)."""
    return get_global_dir() / "templates"


def get_global_commands_dir() -> Path:
    """
    Get global commands directory (~/.cco/commands/).

    This stores reusable, project-agnostic commands that are linked to project
    .claude/commands/ directories. When pip install -U updates these commands,
    all projects auto-update (via hardlink/symlink).

    Note: These are NOT templates - they're ready-to-use commands with no placeholders.
    """
    return get_global_dir() / "commands"


def get_knowledge_dir() -> Path:
    """Get global knowledge base directory (~/.cco/knowledge/)."""
    return get_global_dir() / "knowledge"


def get_principles_dir() -> Path:
    """
    Get global principles directory (~/.cco/knowledge/principles/).

    Category-specific principle files stored globally to avoid duplication
    across projects. Similar to global commands pattern.
    """
    return get_knowledge_dir() / "principles"


def get_guides_dir() -> Path:
    """
    Get global guides directory (~/.cco/knowledge/guides/).

    Static guide files (verification, git workflow, security, etc.) stored
    globally to avoid duplication. Loaded via @~/.cco/knowledge/guides/...
    """
    return get_knowledge_dir() / "guides"


def get_knowledge_commands_dir() -> Path:
    """
    Get global knowledge commands directory (~/.cco/knowledge/commands/).

    Slash command templates stored globally. Projects symlink to selected commands
    in their .claude/commands/ directory.
    """
    return get_knowledge_dir() / "commands"


def get_agents_dir() -> Path:
    """
    Get global agents directory (~/.cco/knowledge/agents/).

    Task agent definitions stored globally. Projects symlink to selected agents
    in their .claude/agents/ directory.
    """
    return get_knowledge_dir() / "agents"


def get_skills_dir() -> Path:
    """
    Get global skills directory (~/.cco/knowledge/skills/).

    Skill definitions stored globally. Projects symlink to selected skills
    in their .claude/skills/ directory.
    """
    return get_knowledge_dir() / "skills"


def get_projects_registry_dir() -> Path:
    """Get central projects registry (~/.cco/projects/)."""
    return get_global_dir() / "projects"


def get_global_config_file() -> Path:
    """Get global config file (~/.cco/config.json)."""
    return get_global_dir() / "config.json"


def get_registry_index_file() -> Path:
    """Get master registry index file (~/.cco/projects/index.json)."""
    return get_projects_registry_dir() / "index.json"


# ============================================================================
# PROJECT-LOCAL PATH HELPERS (Claude Code directories only)
# ============================================================================
# Note: CCO keeps project directories clean - no CCO-specific files in projects.
# All project data is stored in global registry (~/.cco/projects/).
# Only .claude/ directory is used for commands/hooks (standard Claude Code location).


def get_project_claude_dir(project_root: Path) -> Path:
    """Get project .claude directory (standard Claude Code location)."""
    return project_root / ".claude"


def get_project_commands_dir(project_root: Path) -> Path:
    """Get project commands directory (.claude/commands/)."""
    return get_project_claude_dir(project_root) / "commands"


def get_project_hooks_dir(project_root: Path) -> Path:
    """Get project hooks directory (.claude/hooks/)."""
    return get_project_claude_dir(project_root) / "hooks"


def get_project_registry_file(project_name: str) -> Path:
    """Get registry file for a specific project."""
    return get_projects_registry_dir() / f"{project_name}.json"


# ============================================================================
# PROJECT-SPECIFIC GLOBAL DATA (Zero project pollution)
# ============================================================================
# All project-specific data is stored in ~/.cco/projects/{project_name}/
# This keeps project directories completely clean - no .cco/ folder in projects.


def get_project_data_dir(project_name: str) -> Path:
    """
    Get project-specific data directory in global storage.

    Returns: ~/.cco/projects/{project_name}/

    This directory contains all project-specific CCO data:
    - backups/  (file backups)
    - reports/  (audit, analyze, fix reports)
    - temp/     (temporary files and scripts)
    - changes.json (change tracking manifest)
    """
    return get_projects_registry_dir() / project_name


def get_project_backups_dir(project_name: str) -> Path:
    """
    Get project backups directory in global storage.

    Returns: ~/.cco/projects/{project_name}/backups/

    Stores backups of PRINCIPLES.md, CLAUDE.md, etc.
    Format: {filename}.YYYYMMDD_HHMMSS.backup
    Retention: Last 5 backups per file
    """
    return get_project_data_dir(project_name) / "backups"


def get_project_reports_dir(project_name: str) -> Path:
    """
    Get project reports directory in global storage.

    Returns: ~/.cco/projects/{project_name}/reports/

    Subdirectories:
    - audit/    (audit reports)
    - analyze/  (analysis reports)
    - fix/      (fix reports)
    - sync/     (sync reports)
    """
    return get_project_data_dir(project_name) / "reports"


def get_project_temp_dir(project_name: str) -> Path:
    """
    Get project temp directory in global storage.

    Returns: ~/.cco/projects/{project_name}/temp/

    Stores temporary files, scripts, and working data.
    """
    return get_project_data_dir(project_name) / "temp"


def get_project_changes_file(project_name: str) -> Path:
    """
    Get project change manifest file in global storage.

    Returns: ~/.cco/projects/{project_name}/changes.json

    Tracks all CCO-made changes to the project.
    """
    return get_project_data_dir(project_name) / "changes.json"


# ============================================================================
# COMMAND NAMING
# ============================================================================


def get_command_name(action: str) -> str:
    """Generate command name with brand prefix."""
    return f"/{COMMAND_PREFIX}-{action}"


# ============================================================================
# FILE MARKERS & IDENTIFIERS
# ============================================================================

GLOBAL_MARKER_FILE = ".installed"

# Git ignore patterns - CCO keeps project directories completely clean
GITIGNORE_PATTERNS = []

# ============================================================================
# DISPLAY STRINGS
# ============================================================================

MSG_GLOBAL_INSTALL_SUCCESS = f"[OK] {DISPLAY_NAME} installed globally"
MSG_PROJECT_INIT_SUCCESS = f"[OK] Project initialized with {SHORT_NAME}"
MSG_ALREADY_INSTALLED = f"[INFO] {SHORT_NAME} is already installed"
MSG_NOT_INSTALLED = f"[ERROR] {SHORT_NAME} is not installed. Run: {CLI_NAME} install"
MSG_NOT_INITIALIZED = "[ERROR] Project not initialized. Run: /cco-init"
MSG_INSTALL_FAILED = f"[ERROR] Failed to install {SHORT_NAME}"
MSG_INIT_FAILED = "[ERROR] Failed to initialize project"

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
        "global_dir": str(get_global_dir()),
        "claude_dir": str(get_claude_dir()),
    },
    "preferences": {
        "auto_update_check": True,
        "telemetry_enabled": False,
        "statusline_enabled": True,
    },
    "features": {
        "audit": True,
        "recommendations": True,
        "auto_fix": True,
        "cost_tracking": True,
    },
}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================


def is_global_installed() -> bool:
    """Check if CCO is installed globally."""
    global_dir = get_global_dir()
    marker = global_dir / GLOBAL_MARKER_FILE
    return global_dir.exists() and marker.exists()


def is_project_initialized(project_root: Path) -> bool:
    """
    Check if project is initialized with CCO.

    Looks up project in global registry by project root path.
    CCO keeps project directories completely clean - no files added.
    """
    import json

    registry_dir = get_projects_registry_dir()
    if not registry_dir.exists():
        return False

    project_root_str = str(project_root.absolute())

    # Check all registry files
    for registry_file in registry_dir.glob("*.json"):
        if registry_file.name == "index.json":
            continue
        try:
            data = json.loads(registry_file.read_text())
            if data.get("root") == project_root_str:
                return True
        except Exception:  # noqa: S112
            # Silently skip malformed registry files
            continue

    return False


def get_all_paths() -> Dict[str, Path]:
    """Get dictionary of all configured paths."""
    return {
        "global_dir": get_global_dir(),
        "claude_dir": get_claude_dir(),
        "templates_dir": get_templates_dir(),
        "knowledge_dir": get_knowledge_dir(),
        "projects_registry_dir": get_projects_registry_dir(),
        "global_config_file": get_global_config_file(),
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
    GLOBAL_MARKER_FILE = GLOBAL_MARKER_FILE
    GITIGNORE_PATTERNS = GITIGNORE_PATTERNS

    # Messages
    MSG_GLOBAL_INSTALL_SUCCESS = MSG_GLOBAL_INSTALL_SUCCESS
    MSG_PROJECT_INIT_SUCCESS = MSG_PROJECT_INIT_SUCCESS
    MSG_ALREADY_INSTALLED = MSG_ALREADY_INSTALLED
    MSG_NOT_INSTALLED = MSG_NOT_INSTALLED
    MSG_NOT_INITIALIZED = MSG_NOT_INITIALIZED
    MSG_INSTALL_FAILED = MSG_INSTALL_FAILED
    MSG_INIT_FAILED = MSG_INIT_FAILED

    # Defaults
    DEFAULT_CONFIG = DEFAULT_CONFIG

    # Static methods (delegate to module functions)
    get_home_dir = staticmethod(get_home_dir)
    get_global_dir = staticmethod(get_global_dir)
    get_claude_dir = staticmethod(get_claude_dir)
    get_templates_dir = staticmethod(get_templates_dir)
    get_knowledge_dir = staticmethod(get_knowledge_dir)
    get_projects_registry_dir = staticmethod(get_projects_registry_dir)
    get_global_config_file = staticmethod(get_global_config_file)
    get_registry_index_file = staticmethod(get_registry_index_file)
    get_project_claude_dir = staticmethod(get_project_claude_dir)
    get_project_commands_dir = staticmethod(get_project_commands_dir)
    get_project_hooks_dir = staticmethod(get_project_hooks_dir)
    get_project_registry_file = staticmethod(get_project_registry_file)
    get_project_data_dir = staticmethod(get_project_data_dir)
    get_project_backups_dir = staticmethod(get_project_backups_dir)
    get_project_reports_dir = staticmethod(get_project_reports_dir)
    get_project_temp_dir = staticmethod(get_project_temp_dir)
    get_project_changes_file = staticmethod(get_project_changes_file)
    get_command_name = staticmethod(get_command_name)
    is_global_installed = staticmethod(is_global_installed)
    is_project_initialized = staticmethod(is_project_initialized)
    get_all_paths = staticmethod(get_all_paths)

    @staticmethod
    def to_dict() -> Dict[str, Any]:
        """Export config as dictionary."""
        return {
            "branding": {
                "brand_name": BRAND_NAME,
                "full_name": FULL_NAME,
                "display_name": DISPLAY_NAME,
                "cli_name": CLI_NAME,
                "version": VERSION,
            },
            "paths": {k: str(v) for k, v in get_all_paths().items()},
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
