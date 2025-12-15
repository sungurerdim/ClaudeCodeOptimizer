"""CCO Setup - CLI entry point for cco-install command."""

import argparse
import sys

from .config import (
    CLAUDE_DIR,
    SEPARATOR,
    get_content_path,
    get_rules_breakdown,
)
from .install import (
    clean_claude_md,
    clean_previous_installation,
    setup_agents,
    setup_commands,
    setup_rules,
)
from .local import (
    PERMISSION_LEVELS,
    STATUSLINE_MODES,
    run_local_mode,
)

# Module-level verbose flag (set by CLI, used by all functions)
VERBOSE = True


def _create_install_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser for cco-install.

    Returns:
        Configured ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(
        prog="cco-install",
        description="Install CCO commands, agents, and rules to ~/.claude/",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Local mode (for cco-config):
  cco-install --local . --statusline full --permissions balanced

Statusline modes: full, minimal
Permission levels: safe, balanced, permissive, full
""",
    )

    parser.add_argument(
        "--local",
        metavar="PATH",
        help="Project path for local setup (used by /cco-config)",
    )
    parser.add_argument(
        "--statusline",
        choices=STATUSLINE_MODES,
        help="Statusline mode (requires --local)",
    )
    parser.add_argument(
        "--permissions",
        choices=PERMISSION_LEVELS,
        help="Permission level (requires --local)",
    )
    parser.add_argument(
        "--path",
        metavar="SUBPATH",
        help="Output pip package content path (e.g., rules/cco-adaptive.md)",
    )
    parser.add_argument(
        "--cat",
        metavar="SUBPATH",
        help="Output file content from pip package (e.g., rules/cco-adaptive.md)",
    )

    return parser


def _validate_global_mode_args(parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    """Validate arguments for global installation mode.

    Args:
        parser: ArgumentParser instance for error reporting.
        args: Parsed command-line arguments.

    Raises:
        SystemExit: If validation fails (via parser.error).
    """
    if args.statusline or args.permissions:
        parser.error("--statusline and --permissions require --local")


def _run_global_install() -> int:
    """Execute global installation to ~/.claude/.

    Returns:
        Exit code: 0 on success, 1 on failure.
    """
    try:
        print("\n" + SEPARATOR)
        print("CCO Setup")
        print(SEPARATOR)
        print(f"\nLocation: {CLAUDE_DIR}\n")

        # Step 1: Clean previous installation (ensures fresh state)
        clean_previous_installation()

        # Step 2: Install commands
        print("Commands:")
        cmds = setup_commands()
        if not cmds:
            print("  (none)")
        print()

        # Step 3: Install agents
        print("Agents:")
        agents = setup_agents()
        if not agents:
            print("  (none)")
        print()

        # Step 4: Install rules to ~/.claude/rules/cco/
        print("Rules (to cco/ subdirectory):")
        rules_installed = setup_rules()
        print()

        # Step 5: Clean old CCO markers from CLAUDE.md
        markers_cleaned = clean_claude_md(verbose=True)
        if markers_cleaned == 0:
            print("  CLAUDE.md: no old markers to clean")
        print()

        # Summary
        breakdown = get_rules_breakdown()
        print(SEPARATOR)
        print(f"Installed: {len(cmds)} commands, {len(agents)} agents")
        print(f"  Global rules (in cco/): {rules_installed.get('total', 0)}")
        print(f"    - core.md: {breakdown['core']} rules (always loaded)")
        print(f"    - ai.md: {breakdown['ai']} rules (always loaded)")
        print("  Embedded in commands/agents:")
        print(f"    - tools rules: {breakdown['tools']} (workflow rules)")
        print(f"    - adaptive rules: {breakdown['adaptive']} (project-specific)")
        print(SEPARATOR)
        print()
        print("Restart Claude Code for changes to take effect.")
        print()
        print("Next: /cco-config to configure statusline, permissions, and project context")
        print()
        return 0

    except Exception as e:
        print(f"Setup failed: {e}", file=sys.stderr)
        return 1


def post_install() -> int:
    """CLI entry point for cco-install.

    Orchestrates the installation process by:
    1. Parsing command-line arguments
    2. Routing to local or global installation mode
    3. Validating arguments for global mode
    4. Executing the appropriate installation

    Returns:
        Exit code: 0 on success, 1 on failure.
    """
    parser = _create_install_parser()
    args = parser.parse_args()

    # Utility: output pip package content path
    if args.path:
        content_path = get_content_path() / args.path
        if content_path.exists():
            print(content_path)
            return 0
        print(f"Path not found: {args.path}", file=sys.stderr)
        return 1

    # Utility: output file content from pip package
    if args.cat:
        content_path = get_content_path() / args.cat
        if content_path.exists() and content_path.is_file():
            print(content_path.read_text(encoding="utf-8"))
            return 0
        print(f"File not found: {args.cat}", file=sys.stderr)
        return 1

    # Local mode - used by cco-config
    if args.local:
        return run_local_mode(args)

    # Validate: --statusline and --permissions require --local
    _validate_global_mode_args(parser, args)

    # Global mode - default behavior
    return _run_global_install()


if __name__ == "__main__":
    sys.exit(post_install())
