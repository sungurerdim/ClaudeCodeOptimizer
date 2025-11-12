"""
Post-install hook for ClaudeCodeOptimizer

Automatically sets up ~/.cco/ structure after pip install.
This ensures global CCO content is ready before any project init.
"""

import sys
from pathlib import Path


def post_install():
    """
    Post-install hook - sets up ~/.cco/ structure.

    Called automatically after pip install via setuptools entry point.
    """
    try:
        # Import here to avoid circular dependencies
        from claudecodeoptimizer.core.knowledge_setup import setup_global_knowledge

        print("\n" + "=" * 60)
        print("ClaudeCodeOptimizer Post-Install Setup")
        print("=" * 60)

        # Setup global ~/.cco/ structure
        result = setup_global_knowledge(force=False)

        if result.get("success"):
            print(f"\n✓ Global CCO directory: {result['global_dir']}")
            for action in result.get("actions", []):
                print(f"  • {action}")
            print("\n✓ CCO is ready! Run 'python -m claudecodeoptimizer init' in your project.")
        else:
            print("\n⚠ Warning: Global setup completed with warnings")

        print("=" * 60 + "\n")

    except Exception as e:
        # Non-fatal: Don't break pip install if setup fails
        print(f"\n⚠ Warning: CCO post-install setup failed: {e}")
        print("You can manually run setup later with: python -m claudecodeoptimizer init")
        print("=" * 60 + "\n")


if __name__ == "__main__":
    post_install()
