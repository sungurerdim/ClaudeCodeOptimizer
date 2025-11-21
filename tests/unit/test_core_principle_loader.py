"""
Unit tests for PrincipleLoader

Tests principle loading from frontmatter, caching, and individual principle loading.
Target Coverage: 100%
"""

from pathlib import Path
from unittest.mock import patch

import pytest

from claudecodeoptimizer.core.principle_loader import (
    PrincipleLoader,
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
def temp_commands_dir(tmp_path: Path) -> Path:
    """Create a temporary commands directory with test files"""
    commands_dir = tmp_path / "commands"
    commands_dir.mkdir()

    # Command with principles in frontmatter
    (commands_dir / "cco-test-with-principles.md").write_text(
        "---\nprinciples: ['U_DRY', 'P_LINTING_SAST']\n---\n\nTest command",
        encoding="utf-8",
    )

    # Command without frontmatter
    (commands_dir / "cco-test-no-frontmatter.md").write_text(
        "No frontmatter here",
        encoding="utf-8",
    )

    # Command with empty principles
    (commands_dir / "cco-test-empty-principles.md").write_text(
        "---\nprinciples: []\n---\n\nEmpty principles",
        encoding="utf-8",
    )

    # Command with no principles field
    (commands_dir / "cco-test-no-principles-field.md").write_text(
        "---\ntitle: Test\n---\n\nNo principles field",
        encoding="utf-8",
    )

    return commands_dir


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

    def test_load_single_principle(self, temp_principles_dir: Path) -> None:
        """Test loading single principle through load_principles"""
        loader = PrincipleLoader(temp_principles_dir)
        content = loader.load_principles(["U_DRY"])

        assert "Don't Repeat Yourself" in content
        assert content.count("\n\n---\n\n") == 0  # No separator for single principle


class TestPrincipleLoaderLoadFromFrontmatter:
    """Test load_from_frontmatter method"""

    def test_load_from_frontmatter_valid_file(
        self, temp_principles_dir: Path, temp_commands_dir: Path
    ) -> None:
        """Test loading principles from command file frontmatter"""
        loader = PrincipleLoader(temp_principles_dir)

        cmd_file = temp_commands_dir / "cco-test-with-principles.md"
        content = loader.load_from_frontmatter(cmd_file)
        assert "Don't Repeat Yourself" in content or "Linting" in content

    def test_load_from_frontmatter_no_frontmatter(
        self, temp_principles_dir: Path, temp_commands_dir: Path
    ) -> None:
        """Test loading from file without frontmatter"""
        loader = PrincipleLoader(temp_principles_dir)

        cmd_file = temp_commands_dir / "cco-test-no-frontmatter.md"
        content = loader.load_from_frontmatter(cmd_file)
        assert content == ""

    def test_load_from_frontmatter_nonexistent_file(
        self, temp_principles_dir: Path, tmp_path: Path
    ) -> None:
        """Test loading from non-existent file"""
        loader = PrincipleLoader(temp_principles_dir)

        cmd_file = tmp_path / "nonexistent.md"
        content = loader.load_from_frontmatter(cmd_file)
        assert content == ""

    def test_load_from_frontmatter_no_principles_field(
        self, temp_principles_dir: Path, temp_commands_dir: Path
    ) -> None:
        """Test loading from file with frontmatter but no principles field"""
        loader = PrincipleLoader(temp_principles_dir)

        cmd_file = temp_commands_dir / "cco-test-no-principles-field.md"
        content = loader.load_from_frontmatter(cmd_file)
        assert content == ""

    def test_load_from_frontmatter_empty_principles(
        self, temp_principles_dir: Path, temp_commands_dir: Path
    ) -> None:
        """Test loading from file with empty principles list"""
        loader = PrincipleLoader(temp_principles_dir)

        cmd_file = temp_commands_dir / "cco-test-empty-principles.md"
        content = loader.load_from_frontmatter(cmd_file)
        assert content == ""

    def test_load_from_frontmatter_malformed(
        self, temp_principles_dir: Path, tmp_path: Path
    ) -> None:
        """Test loading from file with malformed frontmatter"""
        loader = PrincipleLoader(temp_principles_dir)

        cmd_file = tmp_path / "malformed.md"
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

        cmd_file = tmp_path / "quoted.md"
        cmd_file.write_text(
            "---\nprinciples: [\"U_DRY\", 'P_LINTING_SAST']\n---\n\nContent",
            encoding="utf-8",
        )

        content = loader.load_from_frontmatter(cmd_file)
        assert len(content) > 0
        assert "Don't Repeat Yourself" in content or "Linting" in content

    def test_load_from_frontmatter_incomplete_frontmatter(
        self, temp_principles_dir: Path, tmp_path: Path
    ) -> None:
        """Test loading from file with incomplete frontmatter (no closing ---)"""
        loader = PrincipleLoader(temp_principles_dir)

        cmd_file = tmp_path / "incomplete.md"
        cmd_file.write_text(
            "---\nprinciples: ['U_DRY']\nNo closing delimiter",
            encoding="utf-8",
        )

        content = loader.load_from_frontmatter(cmd_file)
        assert content == ""


class TestPrincipleLoaderLoadForCommand:
    """Test load_for_command method"""

    def test_load_for_command_with_frontmatter(
        self, temp_principles_dir: Path, tmp_path: Path
    ) -> None:
        """Test loading principles for command with frontmatter"""
        loader = PrincipleLoader(temp_principles_dir)

        # Mock the package directory structure
        package_dir = tmp_path / "package"
        commands_dir = package_dir / "content" / "commands"
        commands_dir.mkdir(parents=True)

        cmd_file = commands_dir / "cco-test.md"
        cmd_file.write_text(
            "---\nprinciples: ['U_DRY']\n---\n\nTest",
            encoding="utf-8",
        )

        with patch("claudecodeoptimizer.core.principle_loader.Path") as mock_path:
            # Mock Path(__file__).parent.parent to return package_dir
            mock_path.return_value.parent.parent = package_dir

            content = loader.load_for_command("cco-test")
            assert "Don't Repeat Yourself" in content

    def test_load_for_command_no_frontmatter(
        self, temp_principles_dir: Path, tmp_path: Path
    ) -> None:
        """Test loading principles for command without frontmatter"""
        loader = PrincipleLoader(temp_principles_dir)

        # Mock the package directory structure
        package_dir = tmp_path / "package"
        commands_dir = package_dir / "content" / "commands"
        commands_dir.mkdir(parents=True)

        cmd_file = commands_dir / "cco-test.md"
        cmd_file.write_text("No frontmatter", encoding="utf-8")

        with patch("claudecodeoptimizer.core.principle_loader.Path") as mock_path:
            mock_path.return_value.parent.parent = package_dir

            content = loader.load_for_command("cco-test")
            assert content == ""

    def test_load_for_command_nonexistent_file(
        self, temp_principles_dir: Path, tmp_path: Path
    ) -> None:
        """Test loading principles for non-existent command file"""
        loader = PrincipleLoader(temp_principles_dir)

        # Mock the package directory structure
        package_dir = tmp_path / "package"
        commands_dir = package_dir / "content" / "commands"
        commands_dir.mkdir(parents=True)

        with patch("claudecodeoptimizer.core.principle_loader.Path") as mock_path:
            mock_path.return_value.parent.parent = package_dir

            content = loader.load_for_command("cco-nonexistent")
            assert content == ""


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

    def test_clear_cache_empty(self, temp_principles_dir: Path) -> None:
        """Test clearing already empty cache"""
        loader = PrincipleLoader(temp_principles_dir)

        assert len(loader._cache) == 0

        # Clear empty cache
        loader.clear_cache()

        assert len(loader._cache) == 0


class TestLoadPrinciplesForCommand:
    """Test load_principles_for_command convenience function"""

    def test_convenience_function(self, temp_principles_dir: Path, tmp_path: Path) -> None:
        """Test convenience function loads principles"""
        # Mock the package directory structure
        package_dir = tmp_path / "package"
        commands_dir = package_dir / "content" / "commands"
        commands_dir.mkdir(parents=True)

        cmd_file = commands_dir / "cco-test.md"
        cmd_file.write_text(
            "---\nprinciples: ['U_DRY']\n---\n\nTest",
            encoding="utf-8",
        )

        with patch("claudecodeoptimizer.config.CCOConfig.get_principles_dir") as mock_get:
            mock_get.return_value = temp_principles_dir

            with patch("claudecodeoptimizer.core.principle_loader.Path") as mock_path:
                mock_path.return_value.parent.parent = package_dir

                content = load_principles_for_command("cco-test")
                assert len(content) > 0


class TestIntegration:
    """Integration tests"""

    def test_full_workflow(self, temp_principles_dir: Path, tmp_path: Path) -> None:
        """Test complete workflow from command to loaded principles"""
        loader = PrincipleLoader(temp_principles_dir)

        # Mock the package directory structure
        package_dir = tmp_path / "package"
        commands_dir = package_dir / "content" / "commands"
        commands_dir.mkdir(parents=True)

        cmd_file = commands_dir / "cco-test.md"
        cmd_file.write_text(
            "---\nprinciples: ['U_DRY', 'P_LINTING_SAST']\n---\n\nTest",
            encoding="utf-8",
        )

        with patch("claudecodeoptimizer.core.principle_loader.Path") as mock_path:
            mock_path.return_value.parent.parent = package_dir

            # Load for command
            content = loader.load_for_command("cco-test")

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
