"""Setup script for ClaudeCodeOptimizer with auto-install of global commands."""

from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install


class PostInstallCommand(install):
    """Post-installation hook to install global CCO commands."""

    def run(self) -> None:
        # Run standard install
        install.run(self)

        # Install global CCO commands
        self._install_global_commands()

    def _install_global_commands(self) -> None:
        """Setup global CCO structure (~/.cco/)"""
        try:
            print("\n" + "=" * 60)
            print("ClaudeCodeOptimizer Post-Install Setup")
            print("=" * 60)

            # Import after installation
            from claudecodeoptimizer.core.knowledge_setup import setup_global_knowledge

            # Setup global ~/.cco/ structure
            result = setup_global_knowledge(force=False)

            if result.get("success"):
                print(f"\n✓ Global CCO directory: {result['global_dir']}")
                for action in result.get("actions", []):
                    print(f"  • {action}")
                print("\n✓ CCO is ready! Run 'python -m claudecodeoptimizer init' in your project.")
            else:
                print("\n⚠ Warning: Global setup completed with warnings")

        except Exception as e:
            print(f"\n⚠ Warning: CCO post-install setup failed: {e}")
            print("You can manually run setup later with: python -m claudecodeoptimizer init")

        print("=" * 60 + "\n")


class PostDevelopCommand(develop):
    """Post-development hook to install global CCO commands."""

    def run(self) -> None:
        # Run standard develop
        develop.run(self)

        # Install global CCO commands
        self._install_global_commands()

    def _install_global_commands(self) -> None:
        """Setup global CCO structure (~/.cco/) in editable mode"""
        try:
            print("\n" + "=" * 60)
            print("ClaudeCodeOptimizer Post-Install Setup (editable mode)")
            print("=" * 60)

            # Import after installation
            from claudecodeoptimizer.core.knowledge_setup import setup_global_knowledge

            # Setup global ~/.cco/ structure
            result = setup_global_knowledge(force=False)

            if result.get("success"):
                print(f"\n✓ Global CCO directory: {result['global_dir']}")
                for action in result.get("actions", []):
                    print(f"  • {action}")
                print("\n✓ CCO is ready! Run 'python -m claudecodeoptimizer init' in your project.")
            else:
                print("\n⚠ Warning: Global setup completed with warnings")

        except Exception as e:
            print(f"\n⚠ Warning: CCO post-install setup failed: {e}")
            print("You can manually run setup later with: python -m claudecodeoptimizer init")

        print("=" * 60 + "\n")


# Use pyproject.toml for package configuration
# This setup.py only adds post-install hooks
setup(
    cmdclass={
        "install": PostInstallCommand,
        "develop": PostDevelopCommand,
    },
)
