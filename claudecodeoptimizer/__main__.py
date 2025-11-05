"""Entry point for running CCO as a module: python -m claudecodeoptimizer"""

import argparse
import sys
from pathlib import Path

# Fix Unicode encoding on Windows
if sys.platform == "win32":
    import codecs

    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


def main() -> None:
    """
    CCO Command Line Interface

    Commands are dynamically loaded from .md templates.
    Single source of truth: templates/global/cco-*.md files.
    """
    from .commands_loader import get_slash_commands, load_global_commands

    parser = argparse.ArgumentParser(
        prog="claudecodeoptimizer",
        description="ClaudeCodeOptimizer - AI-powered development workflow optimizer",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Load commands dynamically from templates
    available_commands = load_global_commands()

    # Create CLI parsers from template metadata
    for cmd_name, cmd_info in available_commands.items():
        subparser = subparsers.add_parser(cmd_name, help=cmd_info["description"])

        # Add command-specific arguments
        if cmd_name == "init":
            subparser.add_argument(
                "--mode",
                choices=["interactive", "quick"],
                default="quick",
                help="Initialization mode: interactive (full wizard) or quick (AI auto-config)",
            )
            subparser.add_argument(
                "-i",
                "--interactive",
                action="store_true",
                help="Shortcut for --mode=interactive",
            )
            subparser.add_argument(
                "--dry-run",
                action="store_true",
                help="Preview configuration without writing files",
            )

    # Utility commands (not slash commands, CLI-only)
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
        # Determine mode
        mode = "interactive" if args.interactive else args.mode
        dry_run = args.dry_run

        # Use new unified wizard
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
        from .core.project import ProjectManager

        try:
            manager = ProjectManager(Path.cwd())
            # Check if initialized
            config_dir = Path.cwd() / ".claude"
            if config_dir.exists():
                print("✓ CCO is initialized for this project")
                print(f"  Configuration: {config_dir}")
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
        from .core.project import ProjectManager

        try:
            manager = ProjectManager(Path.cwd())
            result = manager.uninitialize()

            if result["success"]:
                print("\n✓ All CCO files removed successfully!")
                print(f"  Project: {result.get('project_name', 'unknown')}")
                print(f"  Files removed: {len(result.get('files_removed', []))}")
                if result.get("files_removed"):
                    for file in result["files_removed"]:
                        print(f"    - {file}")
                print()
                print("CCO has been cleanly removed from this project.")
                print("To reinitialize: python -m claudecodeoptimizer init")
            else:
                print(f"\n❌ Uninitialization failed: {result.get('error', 'unknown error')}")
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
