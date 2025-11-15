"""Entry point for running CCO as a module: python -m claudecodeoptimizer"""

import argparse
import sys
from pathlib import Path
from typing import Any

# Fix Unicode encoding on all platforms (MUST be first, before any imports that print)
from .core.safe_print import configure_utf8_encoding

configure_utf8_encoding()


def main() -> None:
    """
    CCO Command Line Interface

    Commands are dynamically loaded from .md templates.
    Single source of truth: templates/global/cco-*.md files.
    """
    from .commands_loader import get_slash_commands

    parser = argparse.ArgumentParser(
        prog="claudecodeoptimizer",
        description="ClaudeCodeOptimizer - AI-powered development workflow optimizer",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Main commands
    init_parser = subparsers.add_parser(
        "init", help="Initialize CCO for this project with AI-powered configuration"
    )
    init_parser.add_argument(
        "--mode",
        choices=["interactive", "quick"],
        default="quick",
        help="Initialization mode: interactive (full wizard) or quick (AI auto-config)",
    )
    init_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview configuration without writing files",
    )

    subparsers.add_parser(
        "remove", help="Remove CCO from current project (keeps global installation)"
    )

    # Utility commands
    subparsers.add_parser("status", help="Show CCO status for current project")
    subparsers.add_parser("version", help="Show CCO version")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        print()
        print("💡 Tip: For full features, use CCO via Claude Code:")
        print("   1. Open project in Claude Code")
        print("   2. Run: /cco-init")
        print(f"   3. Available: {get_slash_commands()}")
        return

    if args.command == "init":
        # Use unified wizard with mode from args
        mode = args.mode
        dry_run = args.dry_run

        from .wizard.orchestrator import CCOWizard

        try:
            wizard = CCOWizard(
                project_root=Path.cwd(),
                mode=mode,
                dry_run=dry_run,
            )
            result = wizard.run()

            if result.success:
                if dry_run:
                    print("\n✓ Dry run complete!")
                    print("  No files were written")
                    print(f"  Mode: {mode}")
                    print(f"  Principles selected: {len(result.selected_principles)}")
                    print(f"  Commands selected: {len(result.selected_commands)}")
                    print()
                    print("Run without --dry-run to apply configuration")
                else:
                    print()
                    print("Next steps:")
                    print("  1. Review PRINCIPLES.md to understand your principles")
                    print("  2. Run /cco-status to see your configuration")
                    print("  3. Run /cco-audit to analyze your codebase")
                sys.exit(0)
            else:
                print(f"\n❌ Initialization failed: {result.error}")
                sys.exit(1)
        except KeyboardInterrupt:
            print("\n\n⚠️  Initialization cancelled by user")
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ Initialization failed: {e}")
            import traceback

            traceback.print_exc()
            sys.exit(1)

    elif args.command == "status":
        try:
            # Check if initialized
            config_dir = Path.cwd() / ".claude"
            claude_md = Path.cwd() / "CLAUDE.md"

            if config_dir.exists() and claude_md.exists():
                print("✓ CCO is initialized for this project")
                print(f"  Configuration: {config_dir}")
                print(f"  Guide: {claude_md}")
            else:
                print("❌ CCO is not initialized")
                print()
                print("To initialize:")
                print("  python -m claudecodeoptimizer init")
                print("  or use Claude Code: /cco-init")
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)

    elif args.command == "remove":
        from .wizard.orchestrator import CCOWizard

        try:
            uninit_result: dict[str, Any] = CCOWizard.uninitialize(Path.cwd())

            if uninit_result["success"]:
                print("\n✓ All CCO files removed successfully!")
                print(f"  Project: {uninit_result.get('project_name', 'unknown')}")
                print(f"  Files removed: {len(uninit_result.get('files_removed', []))}")
                if uninit_result.get("files_removed"):
                    for file in uninit_result["files_removed"]:
                        print(f"    - {file}")
                print()
                print("CCO has been cleanly removed from this project.")
                print("To reinitialize: python -m claudecodeoptimizer init")
            else:
                print(
                    f"\n❌ Uninitialization failed: {uninit_result.get('error', 'unknown error')}"
                )
                sys.exit(1)
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback

            traceback.print_exc()
            sys.exit(1)

    elif args.command == "version":
        from . import __version__

        print(f"ClaudeCodeOptimizer v{__version__}")


if __name__ == "__main__":
    main()
