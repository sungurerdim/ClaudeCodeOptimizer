"""SessionStart hook integration tests.

These tests validate:
- Hook JSON structure is valid
- additionalContext contains required sections
- Hook output format matches Claude Code plugin expectations
- Cross-platform command syntax validation

Tests ensure hooks work correctly without triggering session start.
"""

import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
HOOKS_DIR = ROOT / "hooks"


class TestHookJsonStructure:
    """Validate hook JSON file structure."""

    @pytest.fixture
    def hooks_json(self):
        """Load hooks.json configuration."""
        path = HOOKS_DIR / "hooks.json"
        return json.loads(path.read_text(encoding="utf-8"))

    @pytest.fixture
    def core_rules_json(self):
        """Load core-rules.json content."""
        path = HOOKS_DIR / "core-rules.json"
        return json.loads(path.read_text(encoding="utf-8"))

    def test_hooks_json_has_session_start(self, hooks_json):
        """hooks.json must define SessionStart hook."""
        assert "hooks" in hooks_json, "hooks.json missing hooks key"
        assert "SessionStart" in hooks_json["hooks"], "Missing SessionStart hook"

    def test_session_start_is_list(self, hooks_json):
        """SessionStart must be a list of hook definitions."""
        session_start = hooks_json["hooks"]["SessionStart"]
        assert isinstance(session_start, list), "SessionStart must be a list"
        assert len(session_start) > 0, "SessionStart must have at least one hook"

    def test_hook_definition_structure(self, hooks_json):
        """Hook definition must have correct structure."""
        session_start = hooks_json["hooks"]["SessionStart"]
        hook_def = session_start[0]
        assert "hooks" in hook_def, "Hook definition missing hooks array"
        inner_hook = hook_def["hooks"][0]
        assert "type" in inner_hook, "Inner hook missing type"
        assert inner_hook["type"] == "command", "Hook type should be command"
        assert "command" in inner_hook, "Inner hook missing command"

    def test_core_rules_json_structure(self, core_rules_json):
        """core-rules.json must have hookSpecificOutput."""
        assert "hookSpecificOutput" in core_rules_json, "core-rules.json missing hookSpecificOutput"
        output = core_rules_json["hookSpecificOutput"]
        assert output.get("hookEventName") == "SessionStart", "hookEventName should be SessionStart"
        assert "additionalContext" in output, "Missing additionalContext"


class TestAdditionalContextSections:
    """Validate that additionalContext contains required sections."""

    @pytest.fixture
    def additional_context(self):
        """Extract additionalContext content."""
        path = HOOKS_DIR / "core-rules.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        return data["hookSpecificOutput"]["additionalContext"]

    def test_contains_foundation_section(self, additional_context):
        """additionalContext must contain Foundation rules."""
        assert "Foundation" in additional_context, "Missing Foundation section"

    def test_contains_safety_section(self, additional_context):
        """additionalContext must contain Safety rules."""
        assert "Safety" in additional_context, "Missing Safety section"

    def test_contains_workflow_section(self, additional_context):
        """additionalContext must contain Workflow rules."""
        assert "Workflow" in additional_context, "Missing Workflow section"

    def test_context_is_substantial(self, additional_context):
        """additionalContext should have substantial content (not truncated)."""
        # Should be at least 1000 characters with all sections
        assert len(additional_context) > 1000, (
            f"additionalContext too short ({len(additional_context)} chars), may be truncated"
        )

    def test_context_has_blocker_definitions(self, additional_context):
        """additionalContext should define BLOCKER violations."""
        assert "[BLOCKER]" in additional_context, "additionalContext should define BLOCKER rules"

    def test_context_has_check_definitions(self, additional_context):
        """additionalContext should define CHECK guidelines."""
        assert "[CHECK]" in additional_context, "additionalContext should define CHECK rules"


class TestCrossPlatformCommands:
    """Validate command syntax works cross-platform."""

    @pytest.fixture
    def hooks_json(self):
        """Load hooks.json configuration."""
        path = HOOKS_DIR / "hooks.json"
        return json.loads(path.read_text(encoding="utf-8"))

    def test_command_uses_cat_for_portability(self, hooks_json):
        """Hook command should use cat which works on all platforms."""
        session_start = hooks_json["hooks"]["SessionStart"]
        hook_def = session_start[0]["hooks"][0]
        command = hook_def["command"]
        # cat is available on Linux, macOS, and Windows (via Git Bash/WSL)
        assert "cat" in command, "Command should use cat for portability"

    def test_command_uses_relative_paths(self, hooks_json):
        """Hook command should use relative paths from plugin root."""
        session_start = hooks_json["hooks"]["SessionStart"]
        hook_def = session_start[0]["hooks"][0]
        command = hook_def["command"]
        # Should not have absolute paths
        assert not command.startswith("/"), "Should use relative paths"
        assert "C:\\" not in command, "Should not have Windows absolute paths"

    def test_command_references_core_rules(self, hooks_json):
        """Hook command should reference core-rules.json."""
        session_start = hooks_json["hooks"]["SessionStart"]
        hook_def = session_start[0]["hooks"][0]
        command = hook_def["command"]
        assert "core-rules.json" in command, "Command should reference core-rules.json"


class TestHookWiring:
    """Validate hook wiring between files."""

    def test_hooks_json_references_correct_file(self):
        """hooks.json should reference hooks/core-rules.json."""
        hooks_path = HOOKS_DIR / "hooks.json"
        hooks_json = json.loads(hooks_path.read_text(encoding="utf-8"))
        session_start = hooks_json["hooks"]["SessionStart"]
        command = session_start[0]["hooks"][0]["command"]

        # Should reference the correct path
        assert "hooks/core-rules.json" in command or "core-rules.json" in command, (
            "hooks.json should reference core-rules.json"
        )

    def test_core_rules_file_exists(self):
        """core-rules.json must exist for hook to work."""
        path = HOOKS_DIR / "core-rules.json"
        assert path.exists(), f"core-rules.json not found at {path}"


class TestContentIntegrity:
    """Validate content integrity of injected rules."""

    @pytest.fixture
    def additional_context(self):
        """Extract additionalContext content."""
        path = HOOKS_DIR / "core-rules.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        return data["hookSpecificOutput"]["additionalContext"]

    def test_no_duplicate_headers(self, additional_context):
        """Should not have duplicate top-level headers."""
        # Find all H1 headers
        h1_pattern = r"^# [^\n]+$"
        h1_matches = re.findall(h1_pattern, additional_context, re.MULTILINE)
        # Check for duplicates
        seen = set()
        for header in h1_matches:
            normalized = header.lower()
            if normalized in seen:
                pytest.fail(f"Duplicate H1 header: {header}")
            seen.add(normalized)

    def test_tables_are_well_formed(self, additional_context):
        """Markdown tables should be well-formed."""
        # Find table-like patterns (| col | col |)
        table_lines = [
            line
            for line in additional_context.split("\n")
            if line.strip().startswith("|") and line.strip().endswith("|")
        ]
        for line in table_lines:
            # Each table row should have balanced pipes
            # Count pipes (excluding escaped ones)
            pipe_count = line.count("|")
            assert pipe_count >= 2, f"Malformed table row: {line[:50]}..."

    def test_code_blocks_are_closed(self, additional_context):
        """Code blocks should be properly closed."""
        # Count code block markers
        triple_backtick_count = additional_context.count("```")
        # Should be even (open + close pairs)
        assert triple_backtick_count % 2 == 0, (
            f"Unclosed code blocks: {triple_backtick_count} triple backticks"
        )
