"""CCO Setup - CLI entry point for cco-install command."""

import argparse
import sys
from collections.abc import Callable
from pathlib import Path

from .config import (
    SEPARATOR,
    ContentSubdir,
    cli_entrypoint,
    get_claude_dir,
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
  cco-install --local . --statusline cco-full --permissions balanced

Dry run mode:
  cco-install --dry-run

Statusline modes: cco-full, cco-minimal
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
    parser.add_argument(
        "--dir",
        "-d",
        type=Path,
        metavar="PATH",
        help="Target config directory (default: $CLAUDE_CONFIG_DIR or ~/.claude)",
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


def _print_header(dry_run: bool, claude_dir: Path) -> None:
    """Print installation header."""
    title = "CCO Setup (DRY RUN)" if dry_run else "CCO Setup"
    print("\n" + SEPARATOR)
    print(title)
    print(SEPARATOR)
    print(f"\nLocation: {claude_dir}\n")
    if dry_run:
        print("The following would be installed:\n")


def _run_cleanup_step(dry_run: bool, target_dir: Path | None) -> None:
    """Run cleanup step for previous installation."""
    if dry_run:
        print("Would clean previous installation:")
        print("  - Remove old command files")
        print("  - Remove old agent files")
        print("  - Remove old rule files")
        print()
    else:
        clean_previous_installation(target_dir=target_dir)


def _preview_files(subdir: ContentSubdir, prefix: str = "cco-*.md") -> None:
    """Preview files that would be installed from a content subdirectory."""
    src = get_content_path(subdir)
    if src.exists():
        for f in sorted(src.glob(prefix)):
            print(f"  + {f.name}")
    else:
        print("  (none)")


def _run_install_step(
    label: str,
    dry_run: bool,
    subdir: ContentSubdir,
    install_fn: Callable[..., list[str]] | Callable[..., dict[str, int]],
    target_dir: Path | None,
) -> list[str] | dict[str, int]:
    """Run a single installation step (commands, agents, or rules).

    Returns:
        Installed items (list for commands/agents, dict for rules).
    """
    print(f"{label}:")
    if dry_run:
        if subdir == ContentSubdir.RULES:
            src = get_content_path(subdir)
            if src.exists():
                print("  + cco/core.md")
                print("  + cco/ai.md")
            else:
                print("  (none)")
        else:
            _preview_files(subdir)
        print()
        return {} if subdir == ContentSubdir.RULES else []

    # install_fn is typed as object to accept both setup_commands (returns list) and setup_rules (returns dict)
    result = install_fn(target_dir=target_dir)  # type: ignore[operator]  # Callable union cannot be narrowed by mypy
    if not result:
        print("  (none)")
    print()
    return result


def _run_claude_md_cleanup(dry_run: bool, target_dir: Path | None) -> None:
    """Clean old CCO markers from CLAUDE.md."""
    if dry_run:
        print("Would clean old CCO markers from CLAUDE.md")
    else:
        markers_cleaned = clean_claude_md(verbose=True, target_dir=target_dir)
        if markers_cleaned == 0:
            print("  CLAUDE.md: no old markers to clean")
    print()


def _print_summary(
    dry_run: bool, cmds: list[str], agents: list[str], rules: dict[str, int]
) -> None:
    """Print installation summary."""
    breakdown = get_rules_breakdown()
    print(SEPARATOR)

    if dry_run:
        print("Would install:")
        commands_src = get_content_path(ContentSubdir.COMMANDS)
        agents_src = get_content_path(ContentSubdir.AGENTS)
        cmd_count = len(list(commands_src.glob("cco-*.md"))) if commands_src.exists() else 0
        agent_count = len(list(agents_src.glob("cco-*.md"))) if agents_src.exists() else 0
        print(f"  {cmd_count} commands, {agent_count} agents")
        print("  Global rules (in cco/): 2")
    else:
        print(f"Installed: {len(cmds)} commands, {len(agents)} agents")
        print(f"  Global rules (in cco/): {rules.get('total', 0)}")

    print(f"    - core.md: {breakdown['core']} rules (always loaded)")
    print(f"    - ai.md: {breakdown['ai']} rules (always loaded)")
    print("  Embedded in commands/agents:")
    print(f"    - adaptive rules: {breakdown['adaptive']} (project-specific)")
    print("    - tool rules: embedded in templates (workflow mechanisms)")
    print(SEPARATOR)
    print()


def _print_footer(dry_run: bool) -> None:
    """Print installation footer message."""
    if dry_run:
        print("This was a dry run. No changes were made.")
        print("Run without --dry-run to perform the installation.")
    else:
        print("Restart Claude Code for changes to take effect.")
        print()
        print("Your First 5 Minutes with CCO:")
        print("  1. /cco-config     Configure project (statusline, permissions, context)")
        print("  2. /cco-status     See project health dashboard")
        print("  3. /cco-optimize   Quick wins (auto-fix safe issues)")
        print()
        breakdown = get_rules_breakdown()
        print(
            f"What changed: {breakdown['core']} core + {breakdown['ai']} AI rules now active in every session."
        )
        print("Project-specific rules are added when you run /cco-config.")
    print()


def _run_global_install(dry_run: bool = False, target_dir: Path | None = None) -> int:
    """Execute global installation to target directory.

    Args:
        dry_run: If True, show what would be installed without making changes.
        target_dir: Target directory. If None, uses get_claude_dir().

    Returns:
        Exit code: 0 on success, 1 on failure.
    """
    claude_dir = target_dir or get_claude_dir()

    # Create target directory if --dir is specified
    if target_dir and not target_dir.exists() and not dry_run:
        target_dir.mkdir(parents=True, exist_ok=True)

    _print_header(dry_run, claude_dir)
    _run_cleanup_step(dry_run, target_dir)

    # Install commands, agents, rules
    cmds = _run_install_step(
        "Commands", dry_run, ContentSubdir.COMMANDS, setup_commands, target_dir
    )
    agents = _run_install_step("Agents", dry_run, ContentSubdir.AGENTS, setup_agents, target_dir)
    rules = _run_install_step(
        "Rules (to cco/ subdirectory)", dry_run, ContentSubdir.RULES, setup_rules, target_dir
    )

    _run_claude_md_cleanup(dry_run, target_dir)
    _print_summary(dry_run, cmds, agents, rules)  # type: ignore[arg-type]  # _run_install_step returns union, narrowed by runtime logic
    _print_footer(dry_run)

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
    return _run_global_install(dry_run=args.dry_run, target_dir=args.dir)


if __name__ == "__main__":
    sys.exit(post_install())
