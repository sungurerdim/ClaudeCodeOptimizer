"""Plugin schema and integration validation tests.

These tests validate:
- JSON schema correctness (catches malformed config)
- Hook integration (catches broken session injection)
- Convention enforcement (catches naming violations)

NOT tested (would break on every file change):
- Hardcoded file counts
- File/directory existence
"""

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent


class TestPluginJson:
    """Validate plugin.json schema - catches malformed plugin config."""

    @pytest.fixture
    def plugin_json(self):
        path = ROOT / ".claude-plugin" / "plugin.json"
        return json.loads(path.read_text(encoding="utf-8"))

    @pytest.fixture
    def hooks_json(self):
        path = ROOT / "hooks" / "hooks.json"
        return json.loads(path.read_text(encoding="utf-8"))

    def test_has_required_fields(self, plugin_json, hooks_json):
        """Plugin must have name, version, description. Hooks in separate file."""
        assert plugin_json.get("name") == "cco"
        assert isinstance(plugin_json.get("version"), str)
        assert isinstance(plugin_json.get("description"), str)
        # Hooks are in hooks/hooks.json for modularity
        assert "SessionStart" in hooks_json.get("hooks", {})


class TestMarketplaceJson:
    """Validate marketplace.json schema - catches broken marketplace listing."""

    @pytest.fixture
    def marketplace_json(self):
        path = ROOT / ".claude-plugin" / "marketplace.json"
        return json.loads(path.read_text(encoding="utf-8"))

    def test_has_required_fields(self, marketplace_json):
        """Marketplace listing must have name, version, description, owner."""
        required = ["name", "version", "description", "owner"]
        for field in required:
            assert field in marketplace_json, f"Missing field: {field}"


class TestRuleConventions:
    """Validate rule naming conventions - catches accidental pollution."""

    def test_all_rules_have_cco_prefix(self):
        """All rule files must use cco- prefix for safe updates."""
        rules_dir = ROOT / "rules"
        for subdir in ["core", "languages", "frameworks", "operations"]:
            subdir_path = rules_dir / subdir
            if not subdir_path.exists():
                continue
            for md_file in subdir_path.glob("*.md"):
                assert md_file.name.startswith("cco-"), (
                    f"{md_file} missing cco- prefix - would conflict with user rules"
                )
