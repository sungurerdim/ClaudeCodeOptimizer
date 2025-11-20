"""
Version Manager - Automated Semantic Versioning

Automatically bump version based on conventional commit types:
- feat: → MINOR (1.2.0 → 1.3.0)
- fix: → PATCH (1.2.0 → 1.2.1)
- feat!/BREAKING CHANGE → MAJOR (1.2.0 → 2.0.0)
"""

import re
import subprocess
from enum import Enum
from pathlib import Path


class BumpType(Enum):
    """Version bump types"""

    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"
    NO_BUMP = "no_bump"


class VersionManager:
    """
    Manage semantic versioning based on commit types.

    Implements automated semantic versioning based on conventional commits
    """

    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root

    def detect_bump_type(self, commit_messages: list[str]) -> BumpType:
        """
        Detect version bump type from commit messages.

        Args:
            commit_messages: List of commit messages since last version

        Returns:
            BumpType (MAJOR, MINOR, PATCH, or NO_BUMP)
        """
        has_breaking = False
        has_feat = False
        has_fix = False

        for msg in commit_messages:
            # Check for breaking changes
            if self._is_breaking_change(msg):
                has_breaking = True
            # Check for features
            elif msg.strip().startswith("feat:") or msg.strip().startswith("feat("):
                has_feat = True
            # Check for fixes
            elif msg.strip().startswith("fix:") or msg.strip().startswith("fix("):
                has_fix = True

        # Priority: BREAKING > feat > fix
        if has_breaking:
            return BumpType.MAJOR
        elif has_feat:
            return BumpType.MINOR
        elif has_fix:
            return BumpType.PATCH
        else:
            return BumpType.NO_BUMP

    def _is_breaking_change(self, commit_msg: str) -> bool:
        """Check if commit indicates a breaking change"""
        msg_lower = commit_msg.lower()

        # Check for feat! or fix!
        if re.match(r"^(feat|fix)!", commit_msg.strip()):
            return True

        # Check for BREAKING CHANGE: in body
        if "breaking change:" in msg_lower:
            return True

        return False

    def bump_version(self, current: str, bump_type: BumpType) -> str:
        """
        Calculate new version based on bump type.

        Args:
            current: Current version (e.g., "1.2.3")
            bump_type: Type of bump (MAJOR, MINOR, PATCH)

        Returns:
            New version string (e.g., "1.3.0")
        """
        if bump_type == BumpType.NO_BUMP:
            return current

        # Parse version
        match = re.match(r"^v?(\d+)\.(\d+)\.(\d+)", current)
        if not match:
            raise ValueError(f"Invalid version format: {current}")

        major, minor, patch = map(int, match.groups())

        # Apply bump
        if bump_type == BumpType.MAJOR:
            return f"{major + 1}.0.0"
        elif bump_type == BumpType.MINOR:
            return f"{major}.{minor + 1}.0"
        elif bump_type == BumpType.PATCH:
            return f"{major}.{minor}.{patch + 1}"

        return current

    def get_version_files(self) -> list[Path]:
        """
        Find all version files in project.

        Returns:
            List of paths to version files
        """
        version_files = []

        candidates = [
            "pyproject.toml",
            "package.json",
            "__init__.py",
            "Cargo.toml",
            "go.mod",
            "setup.py",
            "version.txt",
        ]

        for candidate in candidates:
            file_path = self.project_root / candidate
            if file_path.exists():
                version_files.append(file_path)

        return version_files

    def update_version_files(self, new_version: str, files: list[Path] | None = None) -> None:
        """
        Update version in all relevant files.

        Args:
            new_version: New version string (e.g., "1.3.0")
            files: Optional list of files to update (defaults to auto-detected)
        """
        if files is None:
            files = self.get_version_files()

        for file_path in files:
            self._update_version_in_file(file_path, new_version)

    def _update_version_in_file(self, file_path: Path, new_version: str) -> None:
        """Update version in a specific file"""
        content = file_path.read_text(encoding="utf-8")

        if file_path.name == "pyproject.toml":
            # Update: version = "1.2.3"
            content = re.sub(r'version\s*=\s*"[^"]*"', f'version = "{new_version}"', content)

        elif file_path.name == "package.json":
            # Update: "version": "1.2.3"
            content = re.sub(r'"version"\s*:\s*"[^"]*"', f'"version": "{new_version}"', content)

        elif file_path.name == "__init__.py":
            # Update: __version__ = "1.2.3"
            content = re.sub(
                r'__version__\s*=\s*["\'][^"\']*["\']',
                f'__version__ = "{new_version}"',
                content,
            )

        elif file_path.name == "Cargo.toml":
            # Update: version = "1.2.3"
            content = re.sub(
                r'version\s*=\s*"[^"]*"',
                f'version = "{new_version}"',
                content,
                count=1,  # Only first occurrence (package version, not dependencies)
            )

        elif file_path.name == "version.txt":
            # Simple file with just version number
            content = new_version + "\n"

        file_path.write_text(content, encoding="utf-8")

    def create_git_tag(self, version: str, create: bool = False) -> str | None:
        """
        Create git tag for version.

        Args:
            version: Version number (e.g., "1.3.0")
            create: If True, actually create the tag (otherwise just return tag name)

        Returns:
            Tag name (e.g., "v1.3.0")

        Raises:
            ValueError: If version format is invalid
        """
        # Validate version format before using in git commands
        if not re.match(r"^\d+\.\d+\.\d+$", version):
            raise ValueError(f"Invalid version format: {version}")

        tag_name = f"v{version}"

        if create:
            try:
                subprocess.run(  # noqa: S603
                    [  # noqa: S607 - git is a built-in system command
                        "git",
                        "tag",
                        "-a",
                        tag_name,
                        "-m",
                        f"Release {version}",
                    ],
                    cwd=self.project_root,
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                return tag_name
            except subprocess.CalledProcessError as e:
                raise RuntimeError(f"Failed to create git tag: {e.stderr}") from e

        return tag_name

    def get_commits_since_last_tag(self) -> tuple[str, list[str]]:
        """
        Get commit messages since last version tag.

        Returns:
            Tuple of (last_version, commits)
        """
        try:
            # Get last tag
            result = subprocess.run(  # noqa: S603
                [  # noqa: S607 - git is a built-in system command
                    "git",
                    "describe",
                    "--tags",
                    "--abbrev=0",
                ],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True,
                timeout=30,
            )
            last_tag = result.stdout.strip()

            # Get commits since last tag
            result = subprocess.run(  # noqa: S603
                [  # noqa: S607 - git is a built-in system command
                    "git",
                    "log",
                    f"{last_tag}..HEAD",
                    "--pretty=format:%s",
                ],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True,
                timeout=30,
            )
            commits = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]

            # Extract version from tag
            version_match = re.search(r"(\d+\.\d+\.\d+)", last_tag)
            last_version = version_match.group(1) if version_match else "0.0.0"

            return last_version, commits

        except subprocess.CalledProcessError:
            # No tags yet
            return "0.0.0", []

    def auto_bump(self, create_tag: bool = False) -> str | None:
        """
        Automatically bump version based on commits since last tag.

        Args:
            create_tag: If True, create git tag

        Returns:
            New version string, or None if no bump needed
        """
        # Get commits since last tag
        current_version, commits = self.get_commits_since_last_tag()

        if not commits:
            print("No commits since last version")
            return None

        # Detect bump type
        bump_type = self.detect_bump_type(commits)

        if bump_type == BumpType.NO_BUMP:
            print("No version bump needed (no feat/fix/breaking commits)")
            return None

        # Calculate new version
        new_version = self.bump_version(current_version, bump_type)

        print(f"Version bump: {current_version} → {new_version} ({bump_type.value})")

        # Update version files
        self.update_version_files(new_version)
        print("✓ Updated version files")

        # Create tag
        if create_tag:
            tag_name = self.create_git_tag(new_version, create=True)
            print(f"✓ Created git tag: {tag_name}")

        return new_version
