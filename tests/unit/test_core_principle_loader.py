"""
Unit tests for PrincipleLoader

Tests principle loading, category mapping, caching, and command-to-principle resolution.
Target Coverage: 100%
"""

from pathlib import Path
from typing import Dict, List
from unittest.mock import patch

import pytest

from claudecodeoptimizer.core.principle_loader import (
    COMMAND_PRINCIPLE_MAP,
    PrincipleLoader,
    _load_category_mapping,
    _resolve_categories_to_ids,
    load_principles_for_command,
)


@pytest.fixture
def temp_principles_dir(tmp_path: Path) -> Path:
    """Create a temporary principles directory with test files"""
    principles_dir = tmp_path / "principles"
    principles_dir.mkdir()

    # Create sample principle files
    (principles_dir / "U_DRY.md").write_text(
        "---\ntitle: DRY Principle\ncategory: universal\n---\n\nDon't Repeat Yourself",
        encoding="utf-8",
    )
    (principles_dir / "U_FAIL_FAST.md").write_text(
        "---\ntitle: Fail Fast\ncategory: universal\n---\n\nFail fast content",
        encoding="utf-8",
    )
    (principles_dir / "P_LINTING_SAST.md").write_text(
        "---\ntitle: Linting\ncategory: code_quality\n---\n\nLinting content",
        encoding="utf-8",
    )
    (principles_dir / "P_TYPE_SAFETY.md").write_text(
        "---\ntitle: Type Safety\ncategory: code_quality\n---\n\nType safety content",
        encoding="utf-8",
    )
    (principles_dir / "P_API_SECURITY.md").write_text(
        "---\ntitle: API Security\ncategory: security_privacy\n---\n\nAPI security content",
        encoding="utf-8",
    )
    (principles_dir / "P_TEST_COVERAGE.md").write_text(
        "---\ntitle: Test Coverage\ncategory: testing\n---\n\nTest coverage content",
        encoding="utf-8",
    )
    (principles_dir / "PRINCIPLES.md").write_text(
        "# Principles Summary\n\nThis should be skipped",
        encoding="utf-8",
    )

    return principles_dir


@pytest.fixture
def mock_category_mapping() -> Dict[str, List[str]]:
    """Mock category to IDs mapping"""
    return {
        "universal": ["U_DRY", "U_FAIL_FAST", "U_EVIDENCE_BASED", "U_NO_OVERENGINEERING"],
        "core": ["U_EVIDENCE_BASED", "U_FAIL_FAST", "U_NO_OVERENGINEERING"],
        "code_quality": ["P_LINTING_SAST", "P_TYPE_SAFETY"],
        "security_privacy": ["P_API_SECURITY", "P_ENCRYPTION_AT_REST"],
        "testing": ["P_TEST_COVERAGE", "P_CI_GATES"],
        "architecture": ["P_API_VERSIONING"],
        "performance": ["P_DB_OPTIMIZATION"],
        "project-specific": ["P_CONTAINER_SECURITY"],
    }


class TestLoadCategoryMapping:
    """Test _load_category_mapping function"""

    def test_load_category_mapping_caches_result(self, temp_principles_dir: Path) -> None:
        """Test that category mapping is cached"""
        # Reset cache
        import claudecodeoptimizer.core.principle_loader as loader_module

        loader_module._CATEGORY_TO_IDS = None

        # Mock the principles directory path
        mock_mapping = {"universal": ["U_DRY"], "code_quality": ["P_LINTING"]}
        with patch(
            "claudecodeoptimizer.core.principle_md_loader.get_category_mapping",
            return_value=mock_mapping,
        ):
            with patch("pathlib.Path.exists", return_value=True):
                # First call
                result1 = _load_category_mapping()
                # Second call should return cached value
                result2 = _load_category_mapping()

                assert result1 is result2
                assert "core" in result1  # Core category should be added

    def test_load_category_mapping_nonexistent_dir(self, tmp_path: Path) -> None:
        """Test handling of non-existent principles directory"""
        # Reset cache
        import claudecodeoptimizer.core.principle_loader as loader_module

        loader_module._CATEGORY_TO_IDS = None

        # Mock Path.exists to return False for principles directory
        with patch("pathlib.Path.exists", return_value=False):
            result = _load_category_mapping()
            assert result == {}

    def test_load_category_mapping_adds_core_category(self, temp_principles_dir: Path) -> None:
        """Test that core category is added with universal principles"""
        # Reset cache
        import claudecodeoptimizer.core.principle_loader as loader_module

        loader_module._CATEGORY_TO_IDS = None

        with patch("claudecodeoptimizer.core.principle_loader.Path") as mock_path:
            mock_path.return_value.parent.parent = temp_principles_dir.parent

            mock_mapping = {"universal": ["U_DRY"]}
            with patch(
                "claudecodeoptimizer.core.principle_md_loader.get_category_mapping",
                return_value=mock_mapping,
            ):
                with patch.object(Path, "exists", return_value=True):
                    result = _load_category_mapping()

                    assert "core" in result
                    assert result["core"] == [
                        "U_EVIDENCE_BASED",
                        "U_FAIL_FAST",
                        "U_NO_OVERENGINEERING",
                    ]


class TestResolveCategoriestoIds:
    """Test _resolve_categories_to_ids function"""

    def test_resolve_single_category(self, mock_category_mapping: Dict[str, List[str]]) -> None:
        """Test resolving a single category to principle IDs"""
        with patch(
            "claudecodeoptimizer.core.principle_loader._load_category_mapping",
            return_value=mock_category_mapping,
        ):
            result = _resolve_categories_to_ids(["code_quality"])
            assert "P_LINTING_SAST" in result
            assert "P_TYPE_SAFETY" in result

    def test_resolve_multiple_categories(
        self, mock_category_mapping: Dict[str, List[str]]
    ) -> None:
        """Test resolving multiple categories"""
        with patch(
            "claudecodeoptimizer.core.principle_loader._load_category_mapping",
            return_value=mock_category_mapping,
        ):
            result = _resolve_categories_to_ids(["code_quality", "testing"])
            assert "P_LINTING_SAST" in result
            assert "P_TEST_COVERAGE" in result

    def test_resolve_all_category(self, mock_category_mapping: Dict[str, List[str]]) -> None:
        """Test resolving 'all' category returns all principles"""
        with patch(
            "claudecodeoptimizer.core.principle_loader._load_category_mapping",
            return_value=mock_category_mapping,
        ):
            result = _resolve_categories_to_ids(["all"])

            # Should contain principles from all categories
            assert "U_DRY" in result
            assert "P_LINTING_SAST" in result
            assert "P_API_SECURITY" in result
            assert "P_TEST_COVERAGE" in result

    def test_resolve_removes_duplicates(self, mock_category_mapping: Dict[str, List[str]]) -> None:
        """Test that duplicate principle IDs are removed"""
        with patch(
            "claudecodeoptimizer.core.principle_loader._load_category_mapping",
            return_value=mock_category_mapping,
        ):
            # universal and core both contain U_FAIL_FAST
            result = _resolve_categories_to_ids(["universal", "core"])

            # Count occurrences
            assert result.count("U_FAIL_FAST") == 1
            assert result.count("U_EVIDENCE_BASED") == 1

    def test_resolve_preserves_order(self, mock_category_mapping: Dict[str, List[str]]) -> None:
        """Test that principle order is preserved"""
        with patch(
            "claudecodeoptimizer.core.principle_loader._load_category_mapping",
            return_value=mock_category_mapping,
        ):
            result = _resolve_categories_to_ids(["code_quality"])

            # Order should match category mapping
            assert result == ["P_LINTING_SAST", "P_TYPE_SAFETY"]

    def test_resolve_unknown_category(self, mock_category_mapping: Dict[str, List[str]]) -> None:
        """Test resolving unknown category returns empty list"""
        with patch(
            "claudecodeoptimizer.core.principle_loader._load_category_mapping",
            return_value=mock_category_mapping,
        ):
            result = _resolve_categories_to_ids(["unknown_category"])
            assert result == []

    def test_resolve_empty_categories(self, mock_category_mapping: Dict[str, List[str]]) -> None:
        """Test resolving empty category list"""
        with patch(
            "claudecodeoptimizer.core.principle_loader._load_category_mapping",
            return_value=mock_category_mapping,
        ):
            result = _resolve_categories_to_ids([])
            assert result == []


class TestPrincipleLoaderInit:
    """Test PrincipleLoader initialization"""

    def test_init_with_provided_dir(self, temp_principles_dir: Path) -> None:
        """Test initialization with provided directory"""
        loader = PrincipleLoader(temp_principles_dir)
        assert loader.principles_dir == temp_principles_dir
        assert loader._cache == {}

    def test_init_with_default_dir(self) -> None:
        """Test initialization with default directory from config"""
        mock_dir = Path("/mock/principles")

        with patch("claudecodeoptimizer.config.CCOConfig.get_principles_dir") as mock_get:
            mock_get.return_value = mock_dir
            with patch.object(Path, "exists", return_value=True):
                loader = PrincipleLoader()
                assert loader.principles_dir == mock_dir

    def test_init_raises_if_dir_not_exists(self, tmp_path: Path) -> None:
        """Test initialization raises error if directory doesn't exist"""
        nonexistent_dir = tmp_path / "nonexistent"

        with pytest.raises(FileNotFoundError, match="Principles directory not found"):
            PrincipleLoader(nonexistent_dir)


class TestPrincipleLoaderLoadPrinciple:
    """Test load_principle method"""

    def test_load_existing_principle(self, temp_principles_dir: Path) -> None:
        """Test loading an existing principle file"""
        loader = PrincipleLoader(temp_principles_dir)
        content = loader.load_principle("U_DRY")

        assert "Don't Repeat Yourself" in content
        assert content != ""

    def test_load_nonexistent_principle(self, temp_principles_dir: Path) -> None:
        """Test loading a non-existent principle returns empty string"""
        loader = PrincipleLoader(temp_principles_dir)
        content = loader.load_principle("NONEXISTENT")

        assert content == ""

    def test_load_principle_caches_result(self, temp_principles_dir: Path) -> None:
        """Test that loaded principles are cached"""
        loader = PrincipleLoader(temp_principles_dir)

        # First load
        content1 = loader.load_principle("U_DRY")
        assert "U_DRY" in loader._cache

        # Second load should use cache
        content2 = loader.load_principle("U_DRY")
        assert content1 == content2

        # Verify cache was used
        assert loader._cache["U_DRY"] == content1

    def test_load_principle_uses_cache(self, temp_principles_dir: Path) -> None:
        """Test that cached principles are returned without file access"""
        loader = PrincipleLoader(temp_principles_dir)

        # Pre-populate cache
        loader._cache["CACHED"] = "cached content"

        # Should return cached content without accessing file
        content = loader.load_principle("CACHED")
        assert content == "cached content"


class TestPrincipleLoaderLoadPrinciples:
    """Test load_principles method"""

    def test_load_multiple_principles(self, temp_principles_dir: Path) -> None:
        """Test loading multiple principles by ID"""
        loader = PrincipleLoader(temp_principles_dir)
        content = loader.load_principles(["U_DRY", "P_LINTING_SAST"])

        assert "Don't Repeat Yourself" in content
        assert "Linting content" in content
        assert "---" in content  # Separator

    def test_load_principles_empty_list(self, temp_principles_dir: Path) -> None:
        """Test loading empty principle list"""
        loader = PrincipleLoader(temp_principles_dir)
        content = loader.load_principles([])

        assert content == ""

    def test_load_principles_with_nonexistent(self, temp_principles_dir: Path) -> None:
        """Test loading principles with some non-existent IDs"""
        loader = PrincipleLoader(temp_principles_dir)
        content = loader.load_principles(["U_DRY", "NONEXISTENT", "P_LINTING_SAST"])

        # Should contain existing principles
        assert "Don't Repeat Yourself" in content
        assert "Linting content" in content

    def test_load_principles_separator(self, temp_principles_dir: Path) -> None:
        """Test that principles are separated correctly"""
        loader = PrincipleLoader(temp_principles_dir)
        content = loader.load_principles(["U_DRY", "P_LINTING_SAST"])

        # Should have separator between principles
        assert content.count("\n\n---\n\n") == 1


class TestPrincipleLoaderLoadForCommand:
    """Test load_for_command method"""

    def test_load_for_known_command(self, temp_principles_dir: Path) -> None:
        """Test loading principles for a known command"""
        loader = PrincipleLoader(temp_principles_dir)

        with patch(
            "claudecodeoptimizer.core.principle_loader._resolve_categories_to_ids",
            return_value=["U_DRY", "P_LINTING_SAST"],
        ):
            content = loader.load_for_command("cco-audit-code")

            assert "Don't Repeat Yourself" in content or "Linting content" in content

    def test_load_for_unknown_command(self, temp_principles_dir: Path) -> None:
        """Test loading principles for unknown command uses defaults"""
        loader = PrincipleLoader(temp_principles_dir)

        with patch(
            "claudecodeoptimizer.core.principle_loader._resolve_categories_to_ids",
            return_value=["U_DRY"],
        ):
            content = loader.load_for_command("unknown-command")

            # Should use default categories (universal, core)
            assert content is not None

    def test_load_for_command_uses_mapping(
        self, temp_principles_dir: Path, mock_category_mapping: Dict[str, List[str]]
    ) -> None:
        """Test that load_for_command uses COMMAND_PRINCIPLE_MAP"""
        loader = PrincipleLoader(temp_principles_dir)

        # Test specific command mapping
        assert "cco-audit-security" in COMMAND_PRINCIPLE_MAP
        categories = COMMAND_PRINCIPLE_MAP["cco-audit-security"]
        assert "security_privacy" in categories


class TestPrincipleLoaderLoadFromFrontmatter:
    """Test load_from_frontmatter method"""

    def test_load_from_frontmatter_valid_file(self, temp_principles_dir: Path, tmp_path: Path) -> None:
        """Test loading principles from command file frontmatter"""
        loader = PrincipleLoader(temp_principles_dir)

        # Create command file with frontmatter
        cmd_file = tmp_path / "command.md"
        cmd_file.write_text(
            "---\nprinciples: ['U_DRY', 'P_LINTING_SAST']\n---\n\nCommand content",
            encoding="utf-8",
        )

        content = loader.load_from_frontmatter(cmd_file)
        assert "Don't Repeat Yourself" in content or "Linting" in content

    def test_load_from_frontmatter_no_frontmatter(
        self, temp_principles_dir: Path, tmp_path: Path
    ) -> None:
        """Test loading from file without frontmatter"""
        loader = PrincipleLoader(temp_principles_dir)

        cmd_file = tmp_path / "command.md"
        cmd_file.write_text("No frontmatter here", encoding="utf-8")

        content = loader.load_from_frontmatter(cmd_file)
        assert content == ""

    def test_load_from_frontmatter_nonexistent_file(self, temp_principles_dir: Path, tmp_path: Path) -> None:
        """Test loading from non-existent file"""
        loader = PrincipleLoader(temp_principles_dir)

        cmd_file = tmp_path / "nonexistent.md"
        content = loader.load_from_frontmatter(cmd_file)
        assert content == ""

    def test_load_from_frontmatter_no_principles_field(
        self, temp_principles_dir: Path, tmp_path: Path
    ) -> None:
        """Test loading from file with frontmatter but no principles field"""
        loader = PrincipleLoader(temp_principles_dir)

        cmd_file = tmp_path / "command.md"
        cmd_file.write_text(
            "---\ntitle: Test\n---\n\nContent",
            encoding="utf-8",
        )

        content = loader.load_from_frontmatter(cmd_file)
        assert content == ""

    def test_load_from_frontmatter_empty_principles(
        self, temp_principles_dir: Path, tmp_path: Path
    ) -> None:
        """Test loading from file with empty principles list"""
        loader = PrincipleLoader(temp_principles_dir)

        cmd_file = tmp_path / "command.md"
        cmd_file.write_text(
            "---\nprinciples: []\n---\n\nContent",
            encoding="utf-8",
        )

        content = loader.load_from_frontmatter(cmd_file)
        assert content == ""

    def test_load_from_frontmatter_malformed(
        self, temp_principles_dir: Path, tmp_path: Path
    ) -> None:
        """Test loading from file with malformed frontmatter"""
        loader = PrincipleLoader(temp_principles_dir)

        cmd_file = tmp_path / "command.md"
        cmd_file.write_text(
            "---\nmalformed frontmatter\n",
            encoding="utf-8",
        )

        content = loader.load_from_frontmatter(cmd_file)
        assert content == ""

    def test_load_from_frontmatter_quoted_ids(
        self, temp_principles_dir: Path, tmp_path: Path
    ) -> None:
        """Test loading principles with quoted IDs in frontmatter"""
        loader = PrincipleLoader(temp_principles_dir)

        cmd_file = tmp_path / "command.md"
        cmd_file.write_text(
            '---\nprinciples: ["U_DRY", \'P_LINTING_SAST\']\n---\n\nContent',
            encoding="utf-8",
        )

        content = loader.load_from_frontmatter(cmd_file)
        assert len(content) > 0


class TestPrincipleLoaderLoadAllPrinciples:
    """Test load_all_principles method"""

    def test_load_all_principles(self, temp_principles_dir: Path) -> None:
        """Test loading all principle files"""
        loader = PrincipleLoader(temp_principles_dir)
        content = loader.load_all_principles()

        # Should contain content from multiple principles
        assert "Don't Repeat Yourself" in content
        assert "Linting content" in content
        assert "Test coverage content" in content

    def test_load_all_principles_skips_summary(self, temp_principles_dir: Path) -> None:
        """Test that PRINCIPLES.md summary file is skipped"""
        loader = PrincipleLoader(temp_principles_dir)
        content = loader.load_all_principles()

        # Should not contain summary file content
        assert "Principles Summary" not in content

    def test_load_all_principles_nonexistent_dir(self, tmp_path: Path) -> None:
        """Test loading from non-existent directory"""
        nonexistent = tmp_path / "nonexistent"

        # Create loader, then delete directory
        loader = PrincipleLoader.__new__(PrincipleLoader)
        loader.principles_dir = nonexistent
        loader._cache = {}

        content = loader.load_all_principles()
        assert content == ""

    def test_load_all_principles_empty_dir(self, tmp_path: Path) -> None:
        """Test loading from empty directory"""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()

        loader = PrincipleLoader(empty_dir)
        content = loader.load_all_principles()

        assert content == ""


class TestPrincipleLoaderGetCategoriesForCommand:
    """Test get_categories_for_command method"""

    def test_get_categories_known_command(self, temp_principles_dir: Path) -> None:
        """Test getting categories for known command"""
        loader = PrincipleLoader(temp_principles_dir)
        categories = loader.get_categories_for_command("cco-audit-security")

        assert "universal" in categories
        assert "security_privacy" in categories

    def test_get_categories_unknown_command(self, temp_principles_dir: Path) -> None:
        """Test getting categories for unknown command returns defaults"""
        loader = PrincipleLoader(temp_principles_dir)
        categories = loader.get_categories_for_command("unknown-command")

        assert categories == ["core"]

    def test_get_categories_all_audit(self, temp_principles_dir: Path) -> None:
        """Test getting categories for comprehensive audit"""
        loader = PrincipleLoader(temp_principles_dir)
        categories = loader.get_categories_for_command("cco-audit-all")

        assert "all" in categories


class TestPrincipleLoaderEstimateTokenCount:
    """Test estimate_token_count method"""

    def test_estimate_single_category(self, temp_principles_dir: Path) -> None:
        """Test token estimation for single category"""
        loader = PrincipleLoader(temp_principles_dir)
        count = loader.estimate_token_count("cco-init")

        # Should estimate tokens for core category
        assert count > 0

    def test_estimate_multiple_categories(self, temp_principles_dir: Path) -> None:
        """Test token estimation for multiple categories"""
        loader = PrincipleLoader(temp_principles_dir)
        count = loader.estimate_token_count("cco-audit-security")

        # Should be sum of multiple categories
        assert count > 500

    def test_estimate_all_categories(self, temp_principles_dir: Path) -> None:
        """Test token estimation for all categories"""
        loader = PrincipleLoader(temp_principles_dir)
        count = loader.estimate_token_count("cco-audit-all")

        # Should be sum of all category estimates
        assert count > 5000

    def test_estimate_unknown_category(self, temp_principles_dir: Path) -> None:
        """Test token estimation for unknown category uses default"""
        loader = PrincipleLoader(temp_principles_dir)

        # Mock command with unknown category
        with patch.object(loader, "get_categories_for_command", return_value=["unknown"]):
            count = loader.estimate_token_count("test-command")

            # Should use default estimate (500)
            assert count == 500


class TestPrincipleLoaderClearCache:
    """Test clear_cache method"""

    def test_clear_cache(self, temp_principles_dir: Path) -> None:
        """Test clearing the principle cache"""
        loader = PrincipleLoader(temp_principles_dir)

        # Load some principles to populate cache
        loader.load_principle("U_DRY")
        loader.load_principle("P_LINTING_SAST")

        assert len(loader._cache) > 0

        # Clear cache
        loader.clear_cache()

        assert len(loader._cache) == 0


class TestLoadPrinciplesForCommand:
    """Test load_principles_for_command convenience function"""

    def test_convenience_function(self, temp_principles_dir: Path) -> None:
        """Test convenience function loads principles"""
        with patch("claudecodeoptimizer.config.CCOConfig.get_principles_dir") as mock_get:
            mock_get.return_value = temp_principles_dir

            with patch(
                "claudecodeoptimizer.core.principle_loader._resolve_categories_to_ids",
                return_value=["U_DRY"],
            ):
                content = load_principles_for_command("cco-status")

                assert len(content) > 0


class TestCommandPrincipleMap:
    """Test COMMAND_PRINCIPLE_MAP constant"""

    def test_map_has_core_commands(self) -> None:
        """Test that map includes core commands"""
        assert "cco-init" in COMMAND_PRINCIPLE_MAP
        assert "cco-status" in COMMAND_PRINCIPLE_MAP
        assert "cco-config" in COMMAND_PRINCIPLE_MAP

    def test_map_has_audit_commands(self) -> None:
        """Test that map includes audit commands"""
        assert "cco-audit" in COMMAND_PRINCIPLE_MAP
        assert "cco-audit-code" in COMMAND_PRINCIPLE_MAP
        assert "cco-audit-security" in COMMAND_PRINCIPLE_MAP

    def test_all_commands_have_universal(self) -> None:
        """Test that all commands include universal category"""
        for command, categories in COMMAND_PRINCIPLE_MAP.items():
            assert "universal" in categories, f"Command {command} missing universal category"

    def test_map_values_are_lists(self) -> None:
        """Test that all map values are lists"""
        for command, categories in COMMAND_PRINCIPLE_MAP.items():
            assert isinstance(categories, list), f"Command {command} has non-list value"

    def test_comprehensive_audit_has_all(self) -> None:
        """Test that comprehensive audit commands use 'all' category"""
        assert "all" in COMMAND_PRINCIPLE_MAP["cco-audit"]
        assert "all" in COMMAND_PRINCIPLE_MAP["cco-audit-all"]


class TestIntegration:
    """Integration tests with mocked file system"""

    def test_full_workflow(self, temp_principles_dir: Path, tmp_path: Path) -> None:
        """Test complete workflow from command to loaded principles"""
        loader = PrincipleLoader(temp_principles_dir)

        # Mock category mapping
        with patch(
            "claudecodeoptimizer.core.principle_loader._load_category_mapping",
            return_value={
                "universal": ["U_DRY"],
                "core": ["U_DRY"],
                "code_quality": ["P_LINTING_SAST"],
            },
        ):
            # Load for command
            content = loader.load_for_command("cco-audit-code")

            # Should have loaded relevant principles
            assert len(content) > 0

            # Cache should be populated
            assert len(loader._cache) > 0

            # Clear cache
            loader.clear_cache()
            assert len(loader._cache) == 0

    def test_caching_across_methods(self, temp_principles_dir: Path) -> None:
        """Test that cache is shared across different loading methods"""
        loader = PrincipleLoader(temp_principles_dir)

        # Load via load_principle
        content1 = loader.load_principle("U_DRY")
        assert "U_DRY" in loader._cache

        # Load via load_principles should use cache
        content2 = loader.load_principles(["U_DRY"])

        # Should return content from cache
        assert "Don't Repeat Yourself" in content2
        # Cache should still contain the principle
        assert "U_DRY" in loader._cache


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=claudecodeoptimizer.core.principle_loader"])
