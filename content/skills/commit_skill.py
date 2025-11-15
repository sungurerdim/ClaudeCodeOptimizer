"""
Smart Git Commit Skill

Simple git operations utility for commit workflows.
Semantic analysis and grouping done by AI in command layer.
"""

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass
class GitFile:
    """Represents a git file change"""

    status: str  # M, A, D, R, ??
    path: str


@dataclass
class CommitProposal:
    """AI-proposed commit"""

    type: str  # feat, fix, docs, etc.
    scope: str  # wizard, core, skills, etc.
    subject: str  # Short description
    body: List[str]  # Bullet points
    files: List[str]  # File paths


class GitCommitHelper:
    """
    Simple git operations helper.

    Provides basic git operations for commit workflows.
    Semantic analysis done by AI in command layer.
    """

    def __init__(self, project_root: Path) -> None:
        """
        Initialize git helper.

        Args:
            project_root: Project root directory
        """
        self.project_root = project_root

    def get_uncommitted_changes(self) -> List[GitFile]:
        """
        Get list of uncommitted changes.

        Returns:
            List of GitFile objects
        """
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=self.project_root,
            capture_output=True,
            text=True,
            check=True,
        )

        files = []
        for line in result.stdout.splitlines():
            if not line:
                continue

            # Parse git status format (XY PATH where X/Y are status chars)
            status = line[:2].strip()
            path = line[3:] if len(line) > 3 else line[2:].strip()

            files.append(GitFile(status=status, path=path))

        return files

    def get_diff(self, file_path: Optional[str] = None) -> str:
        """
        Get git diff for file or all changes.

        Args:
            file_path: Specific file path, or None for all changes

        Returns:
            Diff output
        """
        cmd = ["git", "diff", "HEAD"]
        if file_path:
            cmd.extend(["--", file_path])

        result = subprocess.run(
            cmd,
            cwd=self.project_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            timeout=10,
        )

        return result.stdout

    def get_file_summary(self, files: List[GitFile]) -> str:
        """
        Get summary of files for AI analysis.

        Args:
            files: List of GitFile objects

        Returns:
            Formatted file list with status
        """
        summary = []
        for file in files:
            summary.append(f"[{file.status:2}] {file.path}")
        return "\n".join(summary)

    def stage_files(self, file_paths: List[str]) -> bool:
        """
        Stage files for commit.

        Args:
            file_paths: List of file paths to stage

        Returns:
            True if successful
        """
        try:
            subprocess.run(["git", "add"] + file_paths, cwd=self.project_root, check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def create_commit(self, message: str) -> Optional[str]:
        """
        Create git commit.

        Args:
            message: Commit message

        Returns:
            Commit hash (short) or None if failed
        """
        try:
            subprocess.run(["git", "commit", "-m", message], cwd=self.project_root, check=True)

            # Get commit hash
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip()[:7]

        except subprocess.CalledProcessError:
            return None

    def push(self) -> bool:
        """
        Push commits to remote.

        Returns:
            True if successful
        """
        try:
            subprocess.run(["git", "push"], cwd=self.project_root, check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def format_commit_message(self, proposal: CommitProposal) -> str:
        """
        Format commit message from AI proposal.

        Args:
            proposal: CommitProposal object

        Returns:
            Formatted commit message
        """
        # Subject line
        subject = f"{proposal.type}({proposal.scope}): {proposal.subject}"

        # Ensure max 72 chars
        if len(subject) > 72:
            subject = subject[:69] + "..."

        # Body (max 5 bullets)
        body_lines = proposal.body[:5]

        # Build message
        message = f"{subject}\n\n"
        message += "\n".join(body_lines)

        return message
