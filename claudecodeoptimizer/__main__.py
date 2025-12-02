"""Entry point: python -m claudecodeoptimizer"""

import sys

from . import __description__, __version__


def main() -> None:
    """CCO CLI."""
    if len(sys.argv) > 1 and sys.argv[1] in ["--version", "-v", "version"]:
        print(f"CCO v{__version__}")
        return

    print(f"\nCCO v{__version__}")
    print("-" * 40)
    print(__description__)
    print()
    print("Setup:   cco-setup")
    print("Remove:  cco-remove")
    print()
    print("In Claude Code: /cco-tune")


if __name__ == "__main__":
    main()
