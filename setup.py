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
        """Install global CCO commands to ~/.claude/commands/"""
        try:
            from claudecodeoptimizer.core.constants import SEPARATOR_WIDTH

            print("\n" + "=" * SEPARATOR_WIDTH)
            print("Installing CCO global commands...")
            print("=" * SEPARATOR_WIDTH)

            # Import after installation
            from claudecodeoptimizer.commands_loader import get_command_list, get_slash_commands
            from claudecodeoptimizer.core.installer import GlobalInstaller

            installer = GlobalInstaller()
            result = installer.install()

            if result.get("success"):
                print("\n[OK] CCO global commands installed successfully!")
                print("     Location: ~/.claude/commands/")
                print(f"     Commands: {get_command_list()}")
                print(f"\n     Restart Claude Code to use: {get_slash_commands()}")
            else:
                print("\n[!] Warning: Could not install global commands")
                print(f"    Error: {result.get('error', 'Unknown error')}")
                print("\n    You can manually install later with: cco install --force")

        except Exception as e:
            print(f"\n[!] Warning: Could not install global commands: {e}")
            print("    You can manually install later with: cco install --force")

        from claudecodeoptimizer.core.constants import SEPARATOR_WIDTH

        print("=" * SEPARATOR_WIDTH + "\n")


class PostDevelopCommand(develop):
    """Post-development hook to install global CCO commands."""

    def run(self) -> None:
        # Run standard develop
        develop.run(self)

        # Install global CCO commands
        self._install_global_commands()

    def _install_global_commands(self) -> None:
        """Install global CCO commands to ~/.claude/commands/"""
        try:
            print("\n" + "=" * 60)
            print("Installing CCO global commands (editable mode)...")
            print("=" * 60)

            # Import after installation
            from claudecodeoptimizer.commands_loader import get_command_list, get_slash_commands
            from claudecodeoptimizer.core.installer import GlobalInstaller

            installer = GlobalInstaller()
            result = installer.install()

            if result.get("success"):
                print("\n[OK] CCO global commands installed successfully!")
                print("     Location: ~/.claude/commands/")
                print(f"     Commands: {get_command_list()}")
                print(f"\n     Restart Claude Code to use: {get_slash_commands()}")
            else:
                print("\n[!] Warning: Could not install global commands")
                print(f"    Error: {result.get('error', 'Unknown error')}")
                print("\n    You can manually install later with: cco install --force")

        except Exception as e:
            print(f"\n[!] Warning: Could not install global commands: {e}")
            print("    You can manually install later with: cco install --force")

        from claudecodeoptimizer.core.constants import SEPARATOR_WIDTH

        print("=" * SEPARATOR_WIDTH + "\n")


# Use pyproject.toml for package configuration
# This setup.py only adds post-install hooks
setup(
    cmdclass={
        "install": PostInstallCommand,
        "develop": PostDevelopCommand,
    },
)
