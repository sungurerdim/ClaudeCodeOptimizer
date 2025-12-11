"""Entry point: python -m claudecodeoptimizer"""

import sys

from . import __description__, __version__

HELP_TEXT = f"""
CCO v{__version__}
{"-" * 40}
{__description__}

Usage:
  python -m claudecodeoptimizer [OPTIONS]
  cco-setup                      Install CCO to ~/.claude/
  cco-remove                     Remove CCO from ~/.claude/

Options:
  --version, -v                  Show version
  --help, -h                     Show this help

In Claude Code:
  /cco-tune                      Configure project settings
  /cco-health                    View project health dashboard
  /cco-audit                     Run security and quality audit
"""


def main() -> int:
    """CCO CLI entry point.

    Returns:
        Exit code (0 for success)
    """
    try:
        if len(sys.argv) > 1:
            arg = sys.argv[1]
            if arg in ["--version", "-v", "version"]:
                print(f"CCO v{__version__}")
                return 0
            if arg in ["--help", "-h", "help"]:
                print(HELP_TEXT)
                return 0

        # Default: show help
        print(HELP_TEXT)
        return 0

    except KeyboardInterrupt:
        print("\nCancelled.")
        return 130


if __name__ == "__main__":
    sys.exit(main())
