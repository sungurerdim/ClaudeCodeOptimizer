"""CCO Status - Show installation info."""

import sys
from pathlib import Path
from typing import Any

from .config import AGENTS_DIR, CLAUDE_DIR, COMMANDS_DIR, VERSION


def count_files() -> dict[str, int]:
    """Count CCO files."""
    return {
        "commands": sum(1 for _ in COMMANDS_DIR.glob("cco-*.md")) if COMMANDS_DIR.exists() else 0,
        "agents": sum(1 for _ in AGENTS_DIR.glob("cco-*.md")) if AGENTS_DIR.exists() else 0,
    }


def has_rules() -> bool:
    """Check if CLAUDE.md has CCO rules."""
    claude_md = CLAUDE_DIR / "CLAUDE.md"
    if not claude_md.exists():
        return False
    content = claude_md.read_text(encoding="utf-8")
    return "CCO_RULES_START" in content


def print_status() -> int:
    """Print status and return exit code."""
    counts = count_files()
    total = sum(counts.values())

    if total == 0:
        print("CCO not installed. Run: cco-setup")
        return 1

    print(f"\nCCO v{VERSION}")
    print("-" * 40)
    print(f"Location: {CLAUDE_DIR}")
    print(f"Commands: {counts['commands']}")
    print(f"Agents: {counts['agents']}")
    print(f"Rules: {'yes' if has_rules() else 'no'}")
    print("\nTry: /cco-help")
    return 0


def main() -> int:
    """CLI entry point."""
    try:
        return print_status()
    except KeyboardInterrupt:
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


# Exports for backwards compatibility
def get_claude_dir() -> Path:
    return CLAUDE_DIR


def count_components(claude_dir: Path) -> dict[str, int]:
    return count_files()


def get_version_info() -> dict[str, Any]:
    return {
        "version": VERSION,
        "install_method": "unknown",
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "platform": sys.platform,
    }


def check_claude_md(claude_dir: Path) -> bool:
    return has_rules()


if __name__ == "__main__":
    sys.exit(main())
