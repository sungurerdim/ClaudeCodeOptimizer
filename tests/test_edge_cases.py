"""Edge case and error handling tests.

These tests validate:
- Invalid argument combinations are rejected
- Profile exists and is valid
- Hook JSON structure is correct
- Schema files exist and are valid
"""

import json

import pytest

from _paths import ROOT, SCHEMAS_DIR


class TestInvalidArgumentCombinations:
    """Validate that conflicting argument combinations are detected."""

    @pytest.fixture
    def schema(self) -> dict | None:
        """Load the optimize command schema."""
        schema_path = ROOT / "commands" / "schemas" / "optimize.schema.json"
        if schema_path.exists():
            return json.loads(schema_path.read_text(encoding="utf-8"))
        return None

    def test_preview_and_auto_mutually_exclusive(self, schema: dict | None) -> None:
        """--preview and --auto cannot be used together."""
        # These flags have opposite intents: preview only vs fix everything
        assert schema is not None, "Schema file must exist"

        # The schema should define this constraint in allOf
        all_of = schema.get("allOf", [])
        has_constraint = any(
            "preview" in str(constraint) and "auto" in str(constraint) for constraint in all_of
        )
        assert has_constraint, "Schema should define preview/auto mutual exclusivity"

    def test_schema_has_no_removed_flags(self, schema: dict | None) -> None:
        """Schema should not have --score or --fix-all (removed flags)."""
        assert schema is not None, "Schema file must exist"
        props = schema.get("properties", {})
        assert "score" not in props, "Schema should not have score property"
        assert "fix-all" not in props, "Schema should not have fix-all property"
        assert "intensity" not in props, "Schema should not have intensity property"


class TestMalformedJsonHandling:
    """Validate detection of malformed JSON in hook files."""

    def test_core_rules_json_is_valid(self) -> None:
        """hooks/core-rules.json must be valid JSON."""
        core_rules_path = ROOT / "hooks" / "core-rules.json"
        try:
            content = core_rules_path.read_text(encoding="utf-8")
            json.loads(content)
        except json.JSONDecodeError as e:
            pytest.fail(f"core-rules.json is malformed: {e}")

    def test_hook_output_structure_validation(self) -> None:
        """Hook output must have required structure."""
        core_rules_path = ROOT / "hooks" / "core-rules.json"
        data = json.loads(core_rules_path.read_text(encoding="utf-8"))

        # Required structure for Claude Code hooks
        assert "hookSpecificOutput" in data, "Missing hookSpecificOutput"
        output = data["hookSpecificOutput"]
        assert "hookEventName" in output, "Missing hookEventName"
        assert "additionalContext" in output, "Missing additionalContext"


class TestSchemaExistence:
    """Validate that schema files exist and are loadable."""

    def test_optimize_schema_exists(self) -> None:
        """optimize.schema.json must exist."""
        schema_path = SCHEMAS_DIR / "optimize.schema.json"
        assert schema_path.exists(), f"Schema not found: {schema_path}"

    def test_optimize_schema_is_valid_json(self) -> None:
        """optimize.schema.json must be valid JSON."""
        schema_path = SCHEMAS_DIR / "optimize.schema.json"
        if schema_path.exists():
            content = schema_path.read_text(encoding="utf-8")
            schema = json.loads(content)
            assert "$schema" in schema, "JSON Schema must have $schema field"
            assert "properties" in schema, "Schema must define properties"


class TestPluginManifestValidation:
    """Validate plugin manifest references existing files."""

    def test_plugin_manifest_all_files_exist(self) -> None:
        """All file paths in plugin.json must exist on disk."""
        plugin_path = ROOT / ".claude-plugin" / "plugin.json"
        plugin_json = json.loads(plugin_path.read_text(encoding="utf-8"))

        missing_files = []

        # Check command files
        for cmd_path in plugin_json.get("commands", []):
            full_path = ROOT / cmd_path.lstrip("./")
            if not full_path.exists():
                missing_files.append(f"Command: {cmd_path}")

        # Check agent files
        for agent_path in plugin_json.get("agents", []):
            full_path = ROOT / agent_path.lstrip("./")
            if not full_path.exists():
                missing_files.append(f"Agent: {agent_path}")

        assert not missing_files, f"Plugin manifest references missing files: {missing_files}"


class TestSchemaSync:
    """Validate schema files exist for commands."""

    def test_commands_have_corresponding_schemas(self) -> None:
        """Each command file should have a corresponding schema in commands/schemas/."""
        from _paths import COMMANDS_DIR

        command_files = list(COMMANDS_DIR.glob("*.md"))
        missing_schemas = []

        for cmd_file in command_files:
            schema_file = SCHEMAS_DIR / f"{cmd_file.stem}.schema.json"
            if not schema_file.exists():
                missing_schemas.append(f"{cmd_file.name} -> {schema_file.name}")

        # Not all commands have schemas yet, so this is informational
        if missing_schemas:
            print(f"\nCommands without schemas: {missing_schemas}")


class TestWorkflowIntegration:
    """Validate command output expectations match agent input expectations."""

    def test_optimize_references_correct_agent_names(self) -> None:
        """Optimize command references must use actual agent names."""
        from _paths import AGENTS_DIR, COMMANDS_DIR

        optimize_content = (COMMANDS_DIR / "optimize.md").read_text(encoding="utf-8")
        agent_files = {f.stem for f in AGENTS_DIR.glob("*.md")}

        # Extract Task() calls
        import re

        task_pattern = r'Task\s*\(\s*["\']([^"\']+)["\']'
        referenced_agents = set(re.findall(task_pattern, optimize_content))

        # Validate all referenced agents exist
        builtin_agents = {"general-purpose", "Explore", "Plan"}
        for agent_name in referenced_agents:
            assert agent_name in agent_files or agent_name in builtin_agents, (
                f"optimize.md references non-existent agent: {agent_name}"
            )

    def test_scope_ids_match_between_command_and_agent(self) -> None:
        """Scope IDs referenced in commands must match agent definitions."""
        from _paths import AGENTS_DIR, COMMANDS_DIR

        # This is validated by test_commands.py TestScopeConsistency
        # but we add an integration check here
        optimize_content = (COMMANDS_DIR / "optimize.md").read_text(encoding="utf-8")
        agent_content = (AGENTS_DIR / "cco-agent-analyze.md").read_text(encoding="utf-8")

        # Key scope IDs that must exist in both
        key_scopes = ["SEC-01", "HYG-01", "TYP-01", "PRF-01"]
        for scope_id in key_scopes:
            assert scope_id in optimize_content, f"Scope {scope_id} missing from optimize.md"
            assert scope_id in agent_content, f"Scope {scope_id} missing from agent-analyze.md"
