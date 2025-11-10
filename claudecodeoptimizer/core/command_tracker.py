"""
Command Tracking Decorator

Automatically tracks command usage using StateTracker.
Wraps command execution to record statistics.
"""

import functools
import time
from pathlib import Path
from typing import Any, Callable

from .registry import ProjectRegistry
from .state import StateTracker


def track_command(command_name: str) -> Callable:
    """
    Decorator to track command usage.

    Usage:
        @track_command("cco-audit")
        def run_audit():
            # command logic
            pass

    Args:
        command_name: Name of the command (e.g., "cco-audit")

    Returns:
        Decorated function that tracks usage
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Get project root (try to detect from cwd)
            project_root = Path.cwd()

            # Check if this is a CCO project
            registry = ProjectRegistry()
            project_info = registry.get_by_path(project_root)

            if not project_info:
                # Not a CCO project, skip tracking
                return func(*args, **kwargs)

            # Initialize tracker
            project_name = project_info.get("name", project_root.name)
            tracker = StateTracker(project_name)

            # Start tracking
            start_time = time.time()
            error = None

            try:
                # Execute command
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                error = str(e)
                raise
            finally:
                # Record command usage
                duration = time.time() - start_time
                tracker.record_command(
                    command=command_name,
                    duration_seconds=duration,
                    success=(error is None),
                    error=error
                )

        return wrapper
    return decorator


def get_command_stats(project_name: str) -> dict:
    """
    Get command usage statistics for a project.

    Args:
        project_name: Name of the project

    Returns:
        Dictionary with command statistics
    """
    tracker = StateTracker(project_name)
    state = tracker.get_state()

    commands = state.get("commands", {})

    # Calculate statistics
    total_commands = sum(cmd.get("count", 0) for cmd in commands.values())
    most_used = max(commands.items(), key=lambda x: x[1].get("count", 0))[0] if commands else None

    return {
        "total_commands_run": total_commands,
        "unique_commands": len(commands),
        "most_used_command": most_used,
        "command_breakdown": commands
    }
