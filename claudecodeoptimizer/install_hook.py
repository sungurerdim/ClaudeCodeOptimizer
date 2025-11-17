"""
Post-install hook for ClaudeCodeOptimizer

Automatically sets up ~/.claude/ structure after pip install.
"""


def post_install() -> int:
    """
    Post-install hook - sets up ~/.claude/ structure.

    Called automatically after pip install.

    Returns:
        Exit code (0 for success)
    """
    try:
        # Import here to avoid circular dependencies
        from claudecodeoptimizer.core.knowledge_setup import setup_global_knowledge

        print("\n" + "=" * 60)
        print("ClaudeCodeOptimizer Post-Install Setup")
        print("=" * 60)

        # Setup global ~/.claude/ structure
        result = setup_global_knowledge(force=False)

        if result.get("success"):
            print(f"\n[OK] Global CCO directory: {result['claude_dir']}")
            for action in result.get("actions", []):
                print(f"  - {action}")
            print("\n[OK] CCO is ready!")
            print("  All CCO commands are now available globally in Claude Code.")
            print("\n  Next steps:")
            print("  1. Open/Restart Claude Code")
            print("  2. Try: /cco-help or /cco-status")
        else:
            print("\n[WARNING] Global setup completed with warnings")

        print("=" * 60 + "\n")

        # Return success for scripting
        return 0

    except Exception as e:
        # Non-fatal: Don't break pip install if setup fails
        print(f"\n[WARNING] CCO post-install setup failed: {e}")
        print("You can manually run setup later")
        print("=" * 60 + "\n")
        return 1


if __name__ == "__main__":
    post_install()
