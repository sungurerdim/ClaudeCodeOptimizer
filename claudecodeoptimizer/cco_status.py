"""CCO Status - Show installation info."""

import sys

from .config import CLAUDE_DIR, VERSION, get_cco_agents, get_cco_commands


def count_files() -> dict[str, int]:
    """Count CCO files."""
    return {
        "commands": len(get_cco_commands()),
        "agents": len(get_cco_agents()),
    }


def has_standards() -> bool:
    """Check if CLAUDE.md has CCO standards."""
    claude_md = CLAUDE_DIR / "CLAUDE.md"
    if not claude_md.exists():
        return False
    content = claude_md.read_text(encoding="utf-8")
    return "CCO_STANDARDS_START" in content or "CCO_RULES_START" in content


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
    print(f"Standards: {'yes' if has_standards() else 'no'}")
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


if __name__ == "__main__":
    sys.exit(main())
