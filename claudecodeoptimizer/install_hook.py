"""CCO Setup - CLI entry point for cco-install command."""

import argparse
import sys

from .config import (
    CLAUDE_DIR,
    SEPARATOR,
    cli_entrypoint,
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

Dry run mode:
  cco-install --dry-run

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
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be installed without making changes",
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


def _run_global_install(dry_run: bool = False) -> int:
    """Execute global installation to ~/.claude/.

    Args:
        dry_run: If True, show what would be installed without making changes.

    Returns:
        Exit code: 0 on success, 1 on failure.
    """
    if dry_run:
        print("\n" + SEPARATOR)
        print("CCO Setup (DRY RUN)")
        print(SEPARATOR)
        print(f"\nLocation: {CLAUDE_DIR}\n")
        print("The following would be installed:\n")
    else:
        print("\n" + SEPARATOR)
        print("CCO Setup")
        print(SEPARATOR)
        print(f"\nLocation: {CLAUDE_DIR}\n")

    # Step 1: Clean previous installation (ensures fresh state)
    if not dry_run:
        clean_previous_installation()
    else:
        print("Would clean previous installation:")
        print("  - Remove old command files")
        print("  - Remove old agent files")
        print("  - Remove old rule files")
        print()

    # Step 2: Install commands
    print("Commands:")
    if not dry_run:
        cmds = setup_commands()
        if not cmds:
            print("  (none)")
    else:
        # Show what would be installed
        commands_src = get_content_path("command-templates")
        if commands_src.exists():
            cmd_files = sorted(commands_src.glob("cco-*.md"))
            for f in cmd_files:
                print(f"  + {f.name}")
        else:
            print("  (none)")
    print()

    # Step 3: Install agents
    print("Agents:")
    if not dry_run:
        agents = setup_agents()
        if not agents:
            print("  (none)")
    else:
        # Show what would be installed
        agents_src = get_content_path("agent-templates")
        if agents_src.exists():
            agent_files = sorted(agents_src.glob("cco-*.md"))
            for f in agent_files:
                print(f"  + {f.name}")
        else:
            print("  (none)")
    print()

    # Step 4: Install rules to ~/.claude/rules/cco/
    print("Rules (to cco/ subdirectory):")
    if not dry_run:
        rules_installed = setup_rules()
    else:
        # Show what would be installed
        rules_src = get_content_path("rules")
        if rules_src.exists():
            print("  + cco/core.md")
            print("  + cco/ai.md")
        else:
            print("  (none)")
    print()

    # Step 5: Clean old CCO markers from CLAUDE.md
    if not dry_run:
        markers_cleaned = clean_claude_md(verbose=True)
        if markers_cleaned == 0:
            print("  CLAUDE.md: no old markers to clean")
        print()
    else:
        print("Would clean old CCO markers from CLAUDE.md")
        print()

    # Summary
    breakdown = get_rules_breakdown()
    print(SEPARATOR)
    if not dry_run:
        cmds = setup_commands(verbose=False)
        agents = setup_agents(verbose=False)
        rules_installed = setup_rules(verbose=False)
        print(f"Installed: {len(cmds)} commands, {len(agents)} agents")
        print(f"  Global rules (in cco/): {rules_installed.get('total', 0)}")
    else:
        print("Would install:")
        commands_src = get_content_path("command-templates")
        agents_src = get_content_path("agent-templates")
        cmd_count = len(list(commands_src.glob("cco-*.md"))) if commands_src.exists() else 0
        agent_count = len(list(agents_src.glob("cco-*.md"))) if agents_src.exists() else 0
        print(f"  {cmd_count} commands, {agent_count} agents")
        print("  Global rules (in cco/): 2")

    print(f"    - core.md: {breakdown['core']} rules (always loaded)")
    print(f"    - ai.md: {breakdown['ai']} rules (always loaded)")
    print("  Embedded in commands/agents:")
    print(f"    - tools rules: {breakdown['tools']} (workflow rules)")
    print(f"    - adaptive rules: {breakdown['adaptive']} (project-specific)")
    print(SEPARATOR)
    print()

    if not dry_run:
        print("Restart Claude Code for changes to take effect.")
        print()
        print("Next: /cco-config to configure statusline, permissions, and project context")
        print()
    else:
        print("This was a dry run. No changes were made.")
        print("Run without --dry-run to perform the installation.")
        print()

    return 0


@cli_entrypoint
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
    return _run_global_install(dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(post_install())
