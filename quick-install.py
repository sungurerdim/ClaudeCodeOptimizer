#!/usr/bin/env python3
"""
ClaudeCodeOptimizer - Quick Installer

Usage:
    curl -sSL https://raw.githubusercontent.com/sungurerdim/ClaudeCodeOptimizer/main/quick-install.py | python3

What it does:
    1. Installs CCO package from GitHub
    2. Runs cco-setup (installs commands, agents, rules to ~/.claude/)
"""

import subprocess
import sys

GITHUB_URL = "git+https://github.com/sungurerdim/ClaudeCodeOptimizer.git"
MIN_PYTHON = (3, 10)


def main() -> int:
    """Quick installer from GitHub."""
    # Check Python version
    if sys.version_info < MIN_PYTHON:
        print(f"Error: Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+ required")
        print(f"Current: Python {sys.version_info.major}.{sys.version_info.minor}")
        return 1

    print("=" * 50)
    print("CCO Quick Install")
    print("=" * 50)
    print(f"\nPython {sys.version_info.major}.{sys.version_info.minor} ✓")

    # Remove existing installation if present
    check = subprocess.run(
        [sys.executable, "-m", "pip", "show", "claudecodeoptimizer"],
        capture_output=True,
        timeout=30,
        shell=False,
    )
    if check.returncode == 0:
        print("\nRemoving previous installation...")
        subprocess.run(
            [sys.executable, "-m", "pip", "uninstall", "-y", "claudecodeoptimizer"],
            capture_output=True,
            timeout=60,
            shell=False,
        )

    # Install from GitHub
    print("\nInstalling from GitHub...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", GITHUB_URL],
        capture_output=True,
        text=True,
        timeout=120,
        shell=False,
    )
    if result.returncode != 0:
        print("Error: pip install failed")
        print(result.stderr)
        return 1

    print("Package installed ✓")

    # Run cco-setup (it prints its own detailed output)
    print()
    result = subprocess.run(
        [sys.executable, "-m", "claudecodeoptimizer.install_hook"],
        timeout=60,
        shell=False,
    )
    if result.returncode != 0:
        print("\nSetup failed. Try manually: cco-setup")
        return 1

    # Next steps
    print("Next: Open Claude Code and run /cco-tune")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
