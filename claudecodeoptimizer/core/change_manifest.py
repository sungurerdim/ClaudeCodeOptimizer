"""
Change Manifest - CCO

Tracks all changes made during CCO initialization for selective removal.

Design Philosophy:
- Track every change CCO makes to the project
- Enable granular, selective removal
- Provide clear change summaries for user
- Support safe rollback with backups for critical files
"""

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional


class Change:
    """Represents a single change made by CCO."""

    def __init__(
        self,
        change_type: Literal[
            "file_created",
            "file_modified",
            "directory_created",
            "principles_added",
            "commands_installed",
            "config_created",
        ],
        description: str,
        path: Optional[str] = None,
        items: Optional[List[str]] = None,
        backup_path: Optional[str] = None,
        reversible: bool = True,
        reverse_action: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize change.

        Args:
            change_type: Type of change
            description: Human-readable description (1 sentence)
            path: File/directory path (for file operations)
            items: List of items (for bulk operations like principles)
            backup_path: Path to backup (for modified files)
            reversible: Whether change can be reversed
            reverse_action: How to reverse (delete_file, restore_backup, etc.)
            metadata: Additional metadata
        """
        self.type = change_type
        self.description = description
        self.path = path
        self.items = items or []
        self.backup_path = backup_path
        self.reversible = reversible
        self.reverse_action = reverse_action
        self.metadata = metadata or {}
        self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "type": self.type,
            "description": self.description,
            "path": self.path,
            "items": self.items,
            "backup_path": self.backup_path,
            "reversible": self.reversible,
            "reverse_action": self.reverse_action,
            "metadata": self.metadata,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Change":
        """Create Change from dictionary."""
        return cls(
            change_type=data["type"],
            description=data["description"],
            path=data.get("path"),
            items=data.get("items"),
            backup_path=data.get("backup_path"),
            reversible=data.get("reversible", True),
            reverse_action=data.get("reverse_action"),
            metadata=data.get("metadata", {}),
        )


class ChangeManifest:
    """Manages CCO change tracking and removal."""

    def __init__(self, project_root: Path) -> None:
        """
        Initialize manifest.

        Args:
            project_root: Project root directory
        """
        self.project_root = project_root
        self.manifest_path = project_root / ".cco" / "changes.json"
        self.backup_dir = project_root / ".cco" / "backups"
        self.changes: List[Change] = []

        # Load existing manifest
        if self.manifest_path.exists():
            self._load()

    def add_change(self, change: Change) -> None:
        """
        Add a change to manifest.

        Args:
            change: Change to add
        """
        self.changes.append(change)

    def track_file_created(self, file_path: Path, description: str) -> None:
        """Track file creation."""
        self.add_change(
            Change(
                change_type="file_created",
                description=description,
                path=str(file_path.relative_to(self.project_root)),
                reverse_action="delete_file",
            ),
        )

    def track_file_modified(
        self,
        file_path: Path,
        description: str,
        create_backup: bool = True,
    ) -> None:
        """
        Track file modification with optional backup.

        Args:
            file_path: Path to modified file
            description: Change description
            create_backup: Whether to create backup (for critical files)
        """
        backup_path = None

        if create_backup and file_path.exists():
            backup_path = self._create_backup(file_path)

        self.add_change(
            Change(
                change_type="file_modified",
                description=description,
                path=str(file_path.relative_to(self.project_root)),
                backup_path=str(backup_path.relative_to(self.project_root))
                if backup_path
                else None,
                reverse_action="restore_backup" if backup_path else None,
            ),
        )

    def track_directory_created(self, dir_path: Path, description: str) -> None:
        """Track directory creation."""
        self.add_change(
            Change(
                change_type="directory_created",
                description=description,
                path=str(dir_path.relative_to(self.project_root)),
                reverse_action="delete_directory",
            ),
        )

    def track_principles_added(self, principle_ids: List[str]) -> None:
        """Track principles addition."""
        description = f"Added {len(principle_ids)} development principles to PRINCIPLES.md"

        self.add_change(
            Change(
                change_type="principles_added",
                description=description,
                items=principle_ids,
                reversible=False,  # Can't selectively remove principles
                metadata={
                    "count": len(principle_ids),
                    "principle_ids": principle_ids[:10],  # First 10 for display
                },
            ),
        )

    def track_commands_installed(self, command_names: List[str]) -> None:
        """Track slash commands installation."""
        description = f"Installed {len(command_names)} CCO slash commands"

        self.add_change(
            Change(
                change_type="commands_installed",
                description=description,
                items=command_names,
                reverse_action="delete_commands",
                metadata={"command_names": command_names},
            ),
        )

    def track_config_created(self, config_type: str, description: str) -> None:
        """Track configuration file creation."""
        self.add_change(
            Change(
                change_type="config_created",
                description=description,
                metadata={"config_type": config_type},
            ),
        )

    def save(self) -> None:
        """Save manifest to disk."""
        # Ensure directory exists
        self.manifest_path.parent.mkdir(parents=True, exist_ok=True)

        # Convert changes to dict
        data = {
            "version": "1.0.0",
            "project": self.project_root.name,
            "initialized_at": (
                self.changes[0].timestamp if self.changes else datetime.now().isoformat()
            ),
            "last_updated": datetime.now().isoformat(),
            "changes": [c.to_dict() for c in self.changes],
        }

        # Write JSON
        with open(self.manifest_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def _load(self) -> None:
        """Load manifest from disk."""
        try:
            with open(self.manifest_path, encoding="utf-8") as f:
                data = json.load(f)

            self.changes = [Change.from_dict(c) for c in data.get("changes", [])]

        except Exception:
            # If load fails, start fresh
            self.changes = []

    def _create_backup(self, file_path: Path) -> Path:
        """
        Create backup of file.

        Args:
            file_path: File to backup

        Returns:
            Path to backup file
        """
        # Ensure backup directory exists
        self.backup_dir.mkdir(parents=True, exist_ok=True)

        # Create backup filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.name}.{timestamp}.backup"
        backup_path = self.backup_dir / backup_name

        # Copy file
        shutil.copy2(file_path, backup_path)

        return backup_path

    def get_change_summary(self) -> Dict[str, Any]:
        """
        Get summary of all changes.

        Returns:
            {
                "total_changes": int,
                "files_created": int,
                "files_modified": int,
                "directories_created": int,
                "principles_count": int,
                "commands_count": int,
                "reversible_changes": int,
            }
        """
        summary = {
            "total_changes": len(self.changes),
            "files_created": 0,
            "files_modified": 0,
            "directories_created": 0,
            "principles_count": 0,
            "commands_count": 0,
            "reversible_changes": 0,
        }

        for change in self.changes:
            if change.type == "file_created":
                summary["files_created"] += 1
            elif change.type == "file_modified":
                summary["files_modified"] += 1
            elif change.type == "directory_created":
                summary["directories_created"] += 1
            elif change.type == "principles_added":
                summary["principles_count"] = len(change.items)
            elif change.type == "commands_installed":
                summary["commands_count"] = len(change.items)

            if change.reversible:
                summary["reversible_changes"] += 1

        return summary

    def get_removable_groups(self) -> List[Dict[str, Any]]:
        """
        Get groups of changes that can be removed together.

        Returns:
            List of removable groups for multiselect UI:
            [
                {
                    "label": "Slash Commands (12 commands)",
                    "description": "Remove all CCO slash commands from .claude/commands/",
                    "change_indices": [0, 5, 8],  # Indices in self.changes
                    "safe": True,
                },
                ...
            ]
        """
        groups = []

        # Group 1: Slash Commands
        command_changes = [
            (i, c)
            for i, c in enumerate(self.changes)
            if c.type == "commands_installed" and c.reversible
        ]
        if command_changes:
            total_commands = sum(len(c.items) for _, c in command_changes)
            groups.append(
                {
                    "label": f"Slash Commands ({total_commands} commands)",
                    "description": "Remove all CCO slash commands from .claude/commands/",
                    "change_indices": [i for i, _ in command_changes],
                    "safe": True,
                },
            )

        # Group 2: PRINCIPLES.md
        principles_changes = [
            (i, c) for i, c in enumerate(self.changes) if c.path == "PRINCIPLES.md"
        ]
        if principles_changes:
            count = sum(len(c.items) for _, c in principles_changes if c.type == "principles_added")
            groups.append(
                {
                    "label": "PRINCIPLES.md",
                    "description": f"Delete PRINCIPLES.md file ({count} principles)",
                    "change_indices": [i for i, _ in principles_changes],
                    "safe": True,
                },
            )

        # Group 3: Modified Files (with backups)
        modified_with_backup = [
            (i, c)
            for i, c in enumerate(self.changes)
            if c.type == "file_modified" and c.backup_path and c.reversible
        ]
        if modified_with_backup:
            for i, change in modified_with_backup:
                groups.append(
                    {
                        "label": f"Restore {change.path} from backup",
                        "description": f"Restore original file: {change.description}",
                        "change_indices": [i],
                        "safe": True,
                    },
                )

        # Group 4: .cco Directory
        cco_dir_changes = [
            (i, c) for i, c in enumerate(self.changes) if c.path and c.path.startswith(".cco/")
        ]
        if cco_dir_changes:
            groups.append(
                {
                    "label": ".cco Directory",
                    "description": "Remove entire .cco directory (configs, backups, cache)",
                    "change_indices": [i for i, _ in cco_dir_changes],
                    "safe": True,
                },
            )

        # Group 5: .claude Directory (created by CCO)
        claude_dir_changes = [
            (i, c)
            for i, c in enumerate(self.changes)
            if c.type == "directory_created" and c.path == ".claude"
        ]
        if claude_dir_changes:
            groups.append(
                {
                    "label": ".claude Directory",
                    "description": "Remove .claude directory (WARNING: removes ALL slash commands)",
                    "change_indices": [i for i, _ in claude_dir_changes],
                    "safe": False,  # Dangerous
                },
            )

        return groups

    def remove_changes(self, change_indices: List[int]) -> Dict[str, Any]:
        """
        Remove changes by indices.

        Args:
            change_indices: Indices of changes to remove

        Returns:
            Result dict with success status and details
        """
        removed = []
        errors = []

        for idx in sorted(change_indices, reverse=True):  # Reverse to avoid index shift
            if idx >= len(self.changes):
                continue

            change = self.changes[idx]

            try:
                # Execute reverse action
                if change.reverse_action == "delete_file":
                    file_path = self.project_root / change.path
                    if file_path.exists():
                        file_path.unlink()
                        removed.append(f"Deleted {change.path}")

                elif change.reverse_action == "restore_backup":
                    # Restore from backup
                    if change.backup_path:
                        backup_path = self.project_root / change.backup_path
                        file_path = self.project_root / change.path
                        if backup_path.exists():
                            shutil.copy2(backup_path, file_path)
                            removed.append(f"Restored {change.path} from backup")

                elif change.reverse_action == "delete_directory":
                    dir_path = self.project_root / change.path
                    if dir_path.exists():
                        shutil.rmtree(dir_path)
                        removed.append(f"Deleted directory {change.path}")

                elif change.reverse_action == "delete_commands":
                    # Delete command files
                    for cmd_name in change.items:
                        cmd_path = self.project_root / ".claude" / "commands" / f"{cmd_name}.md"
                        if cmd_path.exists():
                            cmd_path.unlink()
                    removed.append(f"Deleted {len(change.items)} commands")

                # Remove from manifest
                self.changes.pop(idx)

            except Exception as e:
                errors.append(f"Failed to reverse {change.description}: {e}")

        # Save updated manifest
        if removed:
            self.save()

        return {
            "success": len(errors) == 0,
            "removed": removed,
            "errors": errors,
            "removed_count": len(removed),
        }
