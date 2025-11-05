"""Core functionality for ClaudeCodeOptimizer."""

from .installer import GlobalInstaller
from .project import ProjectManager
from .registry import ProjectRegistry

__all__ = ["GlobalInstaller", "ProjectManager", "ProjectRegistry"]
