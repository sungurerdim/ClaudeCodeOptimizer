"""Entry point for running CCO as a module: python -m claudecodeoptimizer"""

import sys

# Fix Unicode encoding on all platforms (MUST be first, before any imports that print)
from .core.safe_print import configure_utf8_encoding

configure_utf8_encoding()


def main() -> None:
    """
    CCO Command Line Interface

    New Architecture (v0.1.0+):
    - Global installation to ~/.claude/ (automatic via pip install)
    - No per-project initialization needed
    - All commands available immediately in Claude Code
    """
    # Check for version flag
    if len(sys.argv) > 1 and sys.argv[1] in ["--version", "-v", "version"]:
        from . import __version__

        print(f"ClaudeCodeOptimizer v{__version__}")
        print()
        print("Architecture: Stateless, global ~/.claude/ installation")
        print("Use '/cco-help' in Claude Code to see all available commands")
        return

    # Default: Show help
    print()
    print("=" * 60)
    print("ClaudeCodeOptimizer - AI-Powered Development Workflow")
    print("=" * 60)
    print()
    print("CCO is installed globally in ~/.claude/")
    print()
    print("📦 Installation:")
    print("  pip install claudecodeoptimizer")
    print("  → Automatically installs to ~/.claude/")
    print()
    print("🚀 Usage:")
    print("  1. Open any project in Claude Code")
    print("  2. Use CCO commands immediately:")
    print()
    print("     /cco-help                  - Show all commands")
    print("     /cco-status                - Analyze current project")
    print("     /cco-audit-security-owasp  - Security audit")
    print("     /cco-audit-code-quality    - Code quality audit")
    print("     /cco-generate-tests        - Generate tests")
    print("     ... and 75+ more commands")
    print()
    print("🗑️  Uninstall:")
    print("  pip uninstall claudecodeoptimizer")
    print()
    print("📚 Documentation:")
    print("  https://github.com/sungurerdim/ClaudeCodeOptimizer")
    print()
    print("💡 Tip: No setup needed! Commands work in all projects immediately.")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()
