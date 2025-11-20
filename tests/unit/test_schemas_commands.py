"""
Unit tests for Command Schemas

Tests CommandMetadata, CommandSelection, and CommandRegistry models.
Target Coverage: 100%
"""

from datetime import datetime

import pytest
from pydantic import ValidationError

from claudecodeoptimizer.schemas.commands import (
    CommandMetadata,
    CommandRegistry,
    CommandSelection,
)


class TestCommandMetadata:
    """Test CommandMetadata model"""

    def test_minimal_creation(self) -> None:
        """Test creating command with minimal required fields"""
        cmd = CommandMetadata(
            command_id="test-cmd",
            display_name="Test Command",
            category="test",
            description_short="Test",
            description_long="Test command for testing",
        )

        assert cmd.command_id == "test-cmd"
        assert cmd.display_name == "Test Command"
        assert cmd.category == "test"
        assert cmd.description_short == "Test"
        assert cmd.description_long == "Test command for testing"

    def test_full_creation(self) -> None:
        """Test creating command with all fields"""
        cmd = CommandMetadata(
            command_id="cco-audit-code",
            display_name="Code Quality Audit",
            category="audit",
            description_short="Audit code for quality issues",
            description_long="Comprehensive code quality audit with linting and type checking",
            relevance_tags=["code-quality", "linting"],
            applicable_project_types=["api", "backend"],
            applicable_team_sizes=["solo", "small-2-5"],
            applicable_maturity_stages=["active-dev"],
            required_tools=["black", "ruff"],
            required_commands=["cco-status"],
            is_core=True,
            is_experimental=False,
            usage_frequency=10,
            success_rate=0.95,
            last_used="2025-01-01T00:00:00",
        )

        assert cmd.command_id == "cco-audit-code"
        assert cmd.is_core is True
        assert cmd.usage_frequency == 10
        assert cmd.success_rate == 0.95
        assert "linting" in cmd.relevance_tags
        assert "black" in cmd.required_tools

    def test_defaults(self) -> None:
        """Test default field values"""
        cmd = CommandMetadata(
            command_id="test",
            display_name="Test",
            category="test",
            description_short="Test",
            description_long="Test",
        )

        assert cmd.relevance_tags == []
        assert cmd.applicable_project_types == ["all"]
        assert cmd.applicable_team_sizes == ["all"]
        assert cmd.applicable_maturity_stages == ["all"]
        assert cmd.required_tools == []
        assert cmd.required_commands == []
        assert cmd.is_core is False
        assert cmd.is_experimental is False
        assert cmd.usage_frequency == 0
        assert cmd.success_rate is None
        assert cmd.last_used is None

    def test_missing_required_fields(self) -> None:
        """Test that missing required fields raises validation error"""
        with pytest.raises(ValidationError):
            CommandMetadata()

    def test_success_rate_bounds(self) -> None:
        """Test success rate is bounded between 0 and 1"""
        # Valid values
        cmd = CommandMetadata(
            command_id="test",
            display_name="Test",
            category="test",
            description_short="Test",
            description_long="Test",
            success_rate=0.0,
        )
        assert cmd.success_rate == 0.0

        cmd = CommandMetadata(
            command_id="test",
            display_name="Test",
            category="test",
            description_short="Test",
            description_long="Test",
            success_rate=1.0,
        )
        assert cmd.success_rate == 1.0

        # Invalid values
        with pytest.raises(ValidationError):
            CommandMetadata(
                command_id="test",
                display_name="Test",
                category="test",
                description_short="Test",
                description_long="Test",
                success_rate=1.5,
            )

        with pytest.raises(ValidationError):
            CommandMetadata(
                command_id="test",
                display_name="Test",
                category="test",
                description_short="Test",
                description_long="Test",
                success_rate=-0.1,
            )


class TestCommandSelection:
    """Test CommandSelection model"""

    def test_minimal_creation(self) -> None:
        """Test creating selection with minimal fields"""
        selection = CommandSelection(
            selected_commands=["cmd1", "cmd2"],
            recommended_commands=["cmd1", "cmd2", "cmd3"],
            selection_method="wizard",
        )

        assert selection.selected_commands == ["cmd1", "cmd2"]
        assert selection.recommended_commands == ["cmd1", "cmd2", "cmd3"]
        assert selection.selection_method == "wizard"

    def test_defaults(self) -> None:
        """Test default field values"""
        selection = CommandSelection(
            selected_commands=["cmd1"],
            recommended_commands=["cmd1"],
            selection_method="wizard",
        )

        assert selection.deselected_recommended == []
        assert selection.custom_additions == []
        assert selection.selected_at is not None
        # Check it's a valid ISO format datetime
        datetime.fromisoformat(selection.selected_at)

    def test_with_all_fields(self) -> None:
        """Test creating selection with all fields"""
        selection = CommandSelection(
            selected_commands=["cmd1", "cmd2"],
            recommended_commands=["cmd1", "cmd2", "cmd3"],
            deselected_recommended=["cmd3"],
            custom_additions=["cmd4"],
            selection_method="fast-track",
            selected_at="2025-01-01T00:00:00",
        )

        assert selection.deselected_recommended == ["cmd3"]
        assert selection.custom_additions == ["cmd4"]
        assert selection.selection_method == "fast-track"
        assert selection.selected_at == "2025-01-01T00:00:00"

    def test_missing_required_fields(self) -> None:
        """Test that missing required fields raises validation error"""
        with pytest.raises(ValidationError):
            CommandSelection()

        with pytest.raises(ValidationError):
            CommandSelection(selected_commands=["cmd1"])


class TestCommandRegistry:
    """Test CommandRegistry model"""

    def test_empty_registry(self) -> None:
        """Test creating empty registry"""
        registry = CommandRegistry()

        assert registry.commands == []
        assert registry.version is not None
        assert registry.last_updated is not None

    def test_registry_with_commands(self) -> None:
        """Test creating registry with commands"""
        cmd1 = CommandMetadata(
            command_id="cmd1",
            display_name="Command 1",
            category="audit",
            description_short="Test",
            description_long="Test",
        )
        cmd2 = CommandMetadata(
            command_id="cmd2",
            display_name="Command 2",
            category="generate",
            description_short="Test",
            description_long="Test",
        )

        registry = CommandRegistry(commands=[cmd1, cmd2])

        assert len(registry.commands) == 2
        assert registry.commands[0].command_id == "cmd1"
        assert registry.commands[1].command_id == "cmd2"

    def test_get_by_id(self) -> None:
        """Test getting command by ID"""
        cmd = CommandMetadata(
            command_id="test-cmd",
            display_name="Test",
            category="test",
            description_short="Test",
            description_long="Test",
        )
        registry = CommandRegistry(commands=[cmd])

        found = registry.get_by_id("test-cmd")
        assert found is not None
        assert found.command_id == "test-cmd"

        not_found = registry.get_by_id("nonexistent")
        assert not_found is None

    def test_get_by_category(self) -> None:
        """Test getting commands by category"""
        cmd1 = CommandMetadata(
            command_id="cmd1",
            display_name="Command 1",
            category="audit",
            description_short="Test",
            description_long="Test",
        )
        cmd2 = CommandMetadata(
            command_id="cmd2",
            display_name="Command 2",
            category="audit",
            description_short="Test",
            description_long="Test",
        )
        cmd3 = CommandMetadata(
            command_id="cmd3",
            display_name="Command 3",
            category="generate",
            description_short="Test",
            description_long="Test",
        )

        registry = CommandRegistry(commands=[cmd1, cmd2, cmd3])

        audit_cmds = registry.get_by_category("audit")
        assert len(audit_cmds) == 2
        assert all(cmd.category == "audit" for cmd in audit_cmds)

        generate_cmds = registry.get_by_category("generate")
        assert len(generate_cmds) == 1
        assert generate_cmds[0].command_id == "cmd3"

        empty = registry.get_by_category("nonexistent")
        assert empty == []

    def test_get_by_tag(self) -> None:
        """Test getting commands by tag"""
        cmd1 = CommandMetadata(
            command_id="cmd1",
            display_name="Command 1",
            category="test",
            description_short="Test",
            description_long="Test",
            relevance_tags=["python", "testing"],
        )
        cmd2 = CommandMetadata(
            command_id="cmd2",
            display_name="Command 2",
            category="test",
            description_short="Test",
            description_long="Test",
            relevance_tags=["python", "linting"],
        )
        cmd3 = CommandMetadata(
            command_id="cmd3",
            display_name="Command 3",
            category="test",
            description_short="Test",
            description_long="Test",
            relevance_tags=["javascript"],
        )

        registry = CommandRegistry(commands=[cmd1, cmd2, cmd3])

        python_cmds = registry.get_by_tag("python")
        assert len(python_cmds) == 2
        assert all("python" in cmd.relevance_tags for cmd in python_cmds)

        js_cmds = registry.get_by_tag("javascript")
        assert len(js_cmds) == 1

        empty = registry.get_by_tag("nonexistent")
        assert empty == []

    def test_filter_by_project_type(self) -> None:
        """Test filtering commands by project type"""
        cmd1 = CommandMetadata(
            command_id="cmd1",
            display_name="Command 1",
            category="test",
            description_short="Test",
            description_long="Test",
            applicable_project_types=["all"],
        )
        cmd2 = CommandMetadata(
            command_id="cmd2",
            display_name="Command 2",
            category="test",
            description_short="Test",
            description_long="Test",
            applicable_project_types=["api", "backend"],
        )
        cmd3 = CommandMetadata(
            command_id="cmd3",
            display_name="Command 3",
            category="test",
            description_short="Test",
            description_long="Test",
            applicable_project_types=["frontend"],
        )

        registry = CommandRegistry(commands=[cmd1, cmd2, cmd3])

        # Should include "all" commands and api-specific
        api_cmds = registry.filter_by_project_type(["api"])
        assert len(api_cmds) == 2
        assert "cmd1" in [cmd.command_id for cmd in api_cmds]
        assert "cmd2" in [cmd.command_id for cmd in api_cmds]

        # Should include "all" commands and frontend-specific
        frontend_cmds = registry.filter_by_project_type(["frontend"])
        assert len(frontend_cmds) == 2
        assert "cmd1" in [cmd.command_id for cmd in frontend_cmds]
        assert "cmd3" in [cmd.command_id for cmd in frontend_cmds]

        # Multiple project types
        multi_cmds = registry.filter_by_project_type(["api", "frontend"])
        assert len(multi_cmds) == 3  # All commands match

    def test_filter_by_team_size(self) -> None:
        """Test filtering commands by team size"""
        cmd1 = CommandMetadata(
            command_id="cmd1",
            display_name="Command 1",
            category="test",
            description_short="Test",
            description_long="Test",
            applicable_team_sizes=["all"],
        )
        cmd2 = CommandMetadata(
            command_id="cmd2",
            display_name="Command 2",
            category="test",
            description_short="Test",
            description_long="Test",
            applicable_team_sizes=["solo", "small-2-5"],
        )
        cmd3 = CommandMetadata(
            command_id="cmd3",
            display_name="Command 3",
            category="test",
            description_short="Test",
            description_long="Test",
            applicable_team_sizes=["large-20+"],
        )

        registry = CommandRegistry(commands=[cmd1, cmd2, cmd3])

        # Should include "all" commands and solo-specific
        solo_cmds = registry.filter_by_team_size("solo")
        assert len(solo_cmds) == 2
        assert "cmd1" in [cmd.command_id for cmd in solo_cmds]
        assert "cmd2" in [cmd.command_id for cmd in solo_cmds]

        # Should include "all" commands and large-specific
        large_cmds = registry.filter_by_team_size("large-20+")
        assert len(large_cmds) == 2
        assert "cmd1" in [cmd.command_id for cmd in large_cmds]
        assert "cmd3" in [cmd.command_id for cmd in large_cmds]


class TestCommandRegistryIntegration:
    """Integration tests for CommandRegistry"""

    def test_complex_filtering(self) -> None:
        """Test combining multiple filtering operations"""
        registry = CommandRegistry(
            commands=[
                CommandMetadata(
                    command_id="cmd1",
                    display_name="Command 1",
                    category="audit",
                    description_short="Test",
                    description_long="Test",
                    relevance_tags=["python", "testing"],
                    applicable_project_types=["api"],
                    applicable_team_sizes=["solo"],
                ),
                CommandMetadata(
                    command_id="cmd2",
                    display_name="Command 2",
                    category="audit",
                    description_short="Test",
                    description_long="Test",
                    relevance_tags=["python", "linting"],
                    applicable_project_types=["api"],
                    applicable_team_sizes=["small-2-5"],
                ),
                CommandMetadata(
                    command_id="cmd3",
                    display_name="Command 3",
                    category="generate",
                    description_short="Test",
                    description_long="Test",
                    relevance_tags=["javascript"],
                    applicable_project_types=["frontend"],
                    applicable_team_sizes=["solo"],
                ),
            ]
        )

        # Filter by category, then by tag, then by project type
        audit_cmds = registry.get_by_category("audit")
        assert len(audit_cmds) == 2

        python_cmds = [cmd for cmd in audit_cmds if "python" in cmd.relevance_tags]
        assert len(python_cmds) == 2

        api_cmds = [
            cmd
            for cmd in python_cmds
            if "api" in cmd.applicable_project_types
            or "all" in cmd.applicable_project_types
        ]
        assert len(api_cmds) == 2

    def test_empty_registry_operations(self) -> None:
        """Test all operations on empty registry"""
        registry = CommandRegistry()

        assert registry.get_by_id("test") is None
        assert registry.get_by_category("audit") == []
        assert registry.get_by_tag("python") == []
        assert registry.filter_by_project_type(["api"]) == []
        assert registry.filter_by_team_size("solo") == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
