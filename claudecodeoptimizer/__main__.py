"""Entry point: python -m claudecodeoptimizer"""

import sys

from . import __version__


def main() -> None:
    """CCO CLI."""
    if len(sys.argv) > 1 and sys.argv[1] in ["--version", "-v", "version"]:
        print(f"CCO v{__version__}")
        return

    print(f"\nCCO v{__version__}")
    print("-" * 40)
    print("Commands, agents, and standards for Claude Code")
    print()
    print("Setup:   cco-setup")
    print("Remove:  cco-remove")
    print()
    print("In Claude Code: /cco-calibrate")


if __name__ == "__main__":
    main()
