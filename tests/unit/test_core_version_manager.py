"""
Unit tests for Core Version Manager

Tests automated semantic versioning based on conventional commits.
Target Coverage: 100%
"""

import subprocess
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from claudecodeoptimizer.core.version_manager import BumpType, VersionManager


class TestBumpType:
    """Test BumpType enum"""

    def test_enum_values(self) -> None:
        """Test enum has correct values"""
        assert BumpType.MAJOR.value == "major"
        assert BumpType.MINOR.value == "minor"
        assert BumpType.PATCH.value == "patch"
        assert BumpType.NO_BUMP.value == "no_bump"

    def test_enum_members(self) -> None:
        """Test enum has all required members"""
        assert hasattr(BumpType, "MAJOR")
        assert hasattr(BumpType, "MINOR")
        assert hasattr(BumpType, "PATCH")
        assert hasattr(BumpType, "NO_BUMP")


class TestVersionManagerInit:
    """Test VersionManager initialization"""

    def test_init_with_path(self, temp_dir: Path) -> None:
        """Test initialization with project root path"""
        vm = VersionManager(temp_dir)
        assert vm.project_root == temp_dir

    def test_init_stores_path(self, temp_dir: Path) -> None:
        """Test that project root is stored correctly"""
        vm = VersionManager(temp_dir)
        assert isinstance(vm.project_root, Path)
        assert vm.project_root.exists()


class TestDetectBumpType:
    """Test detect_bump_type method"""

    def test_breaking_change_feat_exclamation(self, temp_dir: Path) -> None:
        """Test breaking change with feat!"""
        vm = VersionManager(temp_dir)
        commits = ["feat!: breaking API change"]
        assert vm.detect_bump_type(commits) == BumpType.MAJOR

    def test_breaking_change_fix_exclamation(self, temp_dir: Path) -> None:
        """Test breaking change with fix!"""
        vm = VersionManager(temp_dir)
        commits = ["fix!: breaking bug fix"]
        assert vm.detect_bump_type(commits) == BumpType.MAJOR

    def test_breaking_change_in_body(self, temp_dir: Path) -> None:
        """Test breaking change with BREAKING CHANGE: in body"""
        vm = VersionManager(temp_dir)
        commits = ["feat: new feature\n\nBREAKING CHANGE: removed old API"]
        assert vm.detect_bump_type(commits) == BumpType.MAJOR

    def test_breaking_change_lowercase(self, temp_dir: Path) -> None:
        """Test breaking change with lowercase"""
        vm = VersionManager(temp_dir)
        commits = ["feat: new feature\n\nbreaking change: api updated"]
        assert vm.detect_bump_type(commits) == BumpType.MAJOR

    def test_feature_commit(self, temp_dir: Path) -> None:
        """Test feature commit triggers minor bump"""
        vm = VersionManager(temp_dir)
        commits = ["feat: add new feature"]
        assert vm.detect_bump_type(commits) == BumpType.MINOR

    def test_feature_with_scope(self, temp_dir: Path) -> None:
        """Test feature commit with scope"""
        vm = VersionManager(temp_dir)
        commits = ["feat(api): add new endpoint"]
        assert vm.detect_bump_type(commits) == BumpType.MINOR

    def test_fix_commit(self, temp_dir: Path) -> None:
        """Test fix commit triggers patch bump"""
        vm = VersionManager(temp_dir)
        commits = ["fix: correct typo"]
        assert vm.detect_bump_type(commits) == BumpType.PATCH

    def test_fix_with_scope(self, temp_dir: Path) -> None:
        """Test fix commit with scope"""
        vm = VersionManager(temp_dir)
        commits = ["fix(ui): button alignment"]
        assert vm.detect_bump_type(commits) == BumpType.PATCH

    def test_no_bump_needed(self, temp_dir: Path) -> None:
        """Test commits that don't trigger version bump"""
        vm = VersionManager(temp_dir)
        commits = ["docs: update README", "chore: update dependencies"]
        assert vm.detect_bump_type(commits) == BumpType.NO_BUMP

    def test_empty_commits(self, temp_dir: Path) -> None:
        """Test empty commit list"""
        vm = VersionManager(temp_dir)
        commits = []
        assert vm.detect_bump_type(commits) == BumpType.NO_BUMP

    def test_priority_breaking_over_feat(self, temp_dir: Path) -> None:
        """Test breaking change has priority over feature"""
        vm = VersionManager(temp_dir)
        commits = ["feat: new feature", "feat!: breaking change"]
        assert vm.detect_bump_type(commits) == BumpType.MAJOR

    def test_priority_feat_over_fix(self, temp_dir: Path) -> None:
        """Test feature has priority over fix"""
        vm = VersionManager(temp_dir)
        commits = ["fix: bug fix", "feat: new feature"]
        assert vm.detect_bump_type(commits) == BumpType.MINOR

    def test_multiple_commits_same_type(self, temp_dir: Path) -> None:
        """Test multiple commits of same type"""
        vm = VersionManager(temp_dir)
        commits = ["feat: feature 1", "feat: feature 2", "feat: feature 3"]
        assert vm.detect_bump_type(commits) == BumpType.MINOR

    def test_mixed_commits(self, temp_dir: Path) -> None:
        """Test mixed commit types"""
        vm = VersionManager(temp_dir)
        commits = [
            "docs: update docs",
            "fix: bug fix",
            "chore: cleanup",
            "feat: new feature",
        ]
        assert vm.detect_bump_type(commits) == BumpType.MINOR

    def test_whitespace_handling(self, temp_dir: Path) -> None:
        """Test commits with leading/trailing whitespace"""
        vm = VersionManager(temp_dir)
        commits = ["  feat: new feature  ", "\tfeat: another feature\n"]
        assert vm.detect_bump_type(commits) == BumpType.MINOR


class TestIsBreakingChange:
    """Test _is_breaking_change method"""

    def test_feat_exclamation(self, temp_dir: Path) -> None:
        """Test feat! pattern"""
        vm = VersionManager(temp_dir)
        assert vm._is_breaking_change("feat!: breaking change") is True

    def test_fix_exclamation(self, temp_dir: Path) -> None:
        """Test fix! pattern"""
        vm = VersionManager(temp_dir)
        assert vm._is_breaking_change("fix!: breaking fix") is True

    def test_breaking_change_body_uppercase(self, temp_dir: Path) -> None:
        """Test BREAKING CHANGE: in body"""
        vm = VersionManager(temp_dir)
        assert vm._is_breaking_change("feat: test\n\nBREAKING CHANGE: details") is True

    def test_breaking_change_body_lowercase(self, temp_dir: Path) -> None:
        """Test breaking change: in body (lowercase)"""
        vm = VersionManager(temp_dir)
        assert vm._is_breaking_change("feat: test\n\nbreaking change: details") is True

    def test_breaking_change_mixed_case(self, temp_dir: Path) -> None:
        """Test Breaking Change: in body (mixed case)"""
        vm = VersionManager(temp_dir)
        assert vm._is_breaking_change("feat: test\n\nBreaking Change: details") is True

    def test_non_breaking_commit(self, temp_dir: Path) -> None:
        """Test non-breaking commit"""
        vm = VersionManager(temp_dir)
        assert vm._is_breaking_change("feat: normal feature") is False

    def test_breaking_word_not_in_footer(self, temp_dir: Path) -> None:
        """Test 'breaking' word in description but not as footer"""
        vm = VersionManager(temp_dir)
        assert vm._is_breaking_change("fix: breaking bug in code") is False

    def test_whitespace_before_exclamation(self, temp_dir: Path) -> None:
        """Test whitespace handling before exclamation"""
        vm = VersionManager(temp_dir)
        assert vm._is_breaking_change("  feat!: breaking") is True


class TestBumpVersion:
    """Test bump_version method"""

    def test_major_bump(self, temp_dir: Path) -> None:
        """Test major version bump"""
        vm = VersionManager(temp_dir)
        assert vm.bump_version("1.2.3", BumpType.MAJOR) == "2.0.0"

    def test_minor_bump(self, temp_dir: Path) -> None:
        """Test minor version bump"""
        vm = VersionManager(temp_dir)
        assert vm.bump_version("1.2.3", BumpType.MINOR) == "1.3.0"

    def test_patch_bump(self, temp_dir: Path) -> None:
        """Test patch version bump"""
        vm = VersionManager(temp_dir)
        assert vm.bump_version("1.2.3", BumpType.PATCH) == "1.2.4"

    def test_no_bump(self, temp_dir: Path) -> None:
        """Test no bump returns current version"""
        vm = VersionManager(temp_dir)
        assert vm.bump_version("1.2.3", BumpType.NO_BUMP) == "1.2.3"

    def test_version_with_v_prefix(self, temp_dir: Path) -> None:
        """Test version with 'v' prefix"""
        vm = VersionManager(temp_dir)
        assert vm.bump_version("v1.2.3", BumpType.MINOR) == "1.3.0"

    def test_version_zero(self, temp_dir: Path) -> None:
        """Test bumping from 0.0.0"""
        vm = VersionManager(temp_dir)
        assert vm.bump_version("0.0.0", BumpType.MAJOR) == "1.0.0"
        assert vm.bump_version("0.0.0", BumpType.MINOR) == "0.1.0"
        assert vm.bump_version("0.0.0", BumpType.PATCH) == "0.0.1"

    def test_large_version_numbers(self, temp_dir: Path) -> None:
        """Test bumping large version numbers"""
        vm = VersionManager(temp_dir)
        assert vm.bump_version("99.99.99", BumpType.MAJOR) == "100.0.0"
        assert vm.bump_version("99.99.99", BumpType.MINOR) == "99.100.0"
        assert vm.bump_version("99.99.99", BumpType.PATCH) == "99.99.100"

    def test_invalid_version_format(self, temp_dir: Path) -> None:
        """Test invalid version format raises error"""
        vm = VersionManager(temp_dir)
        with pytest.raises(ValueError, match="Invalid version format"):
            vm.bump_version("invalid", BumpType.MAJOR)

    def test_invalid_version_partial(self, temp_dir: Path) -> None:
        """Test partial version format raises error"""
        vm = VersionManager(temp_dir)
        with pytest.raises(ValueError, match="Invalid version format"):
            vm.bump_version("1.2", BumpType.MAJOR)

    def test_major_resets_minor_and_patch(self, temp_dir: Path) -> None:
        """Test major bump resets minor and patch to 0"""
        vm = VersionManager(temp_dir)
        assert vm.bump_version("1.5.8", BumpType.MAJOR) == "2.0.0"

    def test_minor_resets_patch(self, temp_dir: Path) -> None:
        """Test minor bump resets patch to 0"""
        vm = VersionManager(temp_dir)
        assert vm.bump_version("1.2.8", BumpType.MINOR) == "1.3.0"

    def test_bump_version_all_enum_values(self, temp_dir: Path) -> None:
        """Test bump_version handles all BumpType enum values"""
        vm = VersionManager(temp_dir)
        # Test all enum values to ensure complete coverage
        for bump_type in BumpType:
            if bump_type == BumpType.NO_BUMP:
                assert vm.bump_version("1.2.3", bump_type) == "1.2.3"
            elif bump_type == BumpType.MAJOR:
                assert vm.bump_version("1.2.3", bump_type) == "2.0.0"
            elif bump_type == BumpType.MINOR:
                assert vm.bump_version("1.2.3", bump_type) == "1.3.0"
            elif bump_type == BumpType.PATCH:
                assert vm.bump_version("1.2.3", bump_type) == "1.2.4"

    def test_bump_version_fallback_unreachable(self, temp_dir: Path) -> None:
        """Test bump_version fallback return (defensive code)"""
        vm = VersionManager(temp_dir)
        # Create a mock BumpType that's not in the enum but has value attribute
        mock_bump = Mock()
        mock_bump.value = "unknown"
        # This tests the final fallback return statement
        # In normal usage this should never be reached, but it's defensive code
        result = vm.bump_version("1.2.3", mock_bump)
        assert result == "1.2.3"


class TestGetVersionFiles:
    """Test get_version_files method"""

    def test_finds_pyproject_toml(self, temp_dir: Path) -> None:
        """Test finds pyproject.toml"""
        (temp_dir / "pyproject.toml").touch()
        vm = VersionManager(temp_dir)
        files = vm.get_version_files()
        assert temp_dir / "pyproject.toml" in files

    def test_finds_package_json(self, temp_dir: Path) -> None:
        """Test finds package.json"""
        (temp_dir / "package.json").touch()
        vm = VersionManager(temp_dir)
        files = vm.get_version_files()
        assert temp_dir / "package.json" in files

    def test_finds_init_py(self, temp_dir: Path) -> None:
        """Test finds __init__.py"""
        (temp_dir / "__init__.py").touch()
        vm = VersionManager(temp_dir)
        files = vm.get_version_files()
        assert temp_dir / "__init__.py" in files

    def test_finds_cargo_toml(self, temp_dir: Path) -> None:
        """Test finds Cargo.toml"""
        (temp_dir / "Cargo.toml").touch()
        vm = VersionManager(temp_dir)
        files = vm.get_version_files()
        assert temp_dir / "Cargo.toml" in files

    def test_finds_go_mod(self, temp_dir: Path) -> None:
        """Test finds go.mod"""
        (temp_dir / "go.mod").touch()
        vm = VersionManager(temp_dir)
        files = vm.get_version_files()
        assert temp_dir / "go.mod" in files

    def test_finds_setup_py(self, temp_dir: Path) -> None:
        """Test finds setup.py"""
        (temp_dir / "setup.py").touch()
        vm = VersionManager(temp_dir)
        files = vm.get_version_files()
        assert temp_dir / "setup.py" in files

    def test_finds_version_txt(self, temp_dir: Path) -> None:
        """Test finds version.txt"""
        (temp_dir / "version.txt").touch()
        vm = VersionManager(temp_dir)
        files = vm.get_version_files()
        assert temp_dir / "version.txt" in files

    def test_finds_multiple_files(self, temp_dir: Path) -> None:
        """Test finds multiple version files"""
        (temp_dir / "pyproject.toml").touch()
        (temp_dir / "package.json").touch()
        (temp_dir / "__init__.py").touch()
        vm = VersionManager(temp_dir)
        files = vm.get_version_files()
        assert len(files) == 3
        assert temp_dir / "pyproject.toml" in files
        assert temp_dir / "package.json" in files
        assert temp_dir / "__init__.py" in files

    def test_no_version_files(self, temp_dir: Path) -> None:
        """Test returns empty list when no version files exist"""
        vm = VersionManager(temp_dir)
        files = vm.get_version_files()
        assert files == []

    def test_preserves_order(self, temp_dir: Path) -> None:
        """Test preserves order of version files"""
        (temp_dir / "pyproject.toml").touch()
        (temp_dir / "package.json").touch()
        vm = VersionManager(temp_dir)
        files = vm.get_version_files()
        # pyproject.toml should come before package.json based on candidates list
        assert files.index(temp_dir / "pyproject.toml") < files.index(temp_dir / "package.json")


class TestUpdateVersionInFile:
    """Test _update_version_in_file method"""

    def test_update_pyproject_toml(self, temp_dir: Path) -> None:
        """Test updating version in pyproject.toml"""
        file_path = temp_dir / "pyproject.toml"
        file_path.write_text('version = "1.0.0"\nname = "test"', encoding="utf-8")

        vm = VersionManager(temp_dir)
        vm._update_version_in_file(file_path, "2.0.0")

        content = file_path.read_text(encoding="utf-8")
        assert 'version = "2.0.0"' in content
        assert 'name = "test"' in content

    def test_update_package_json(self, temp_dir: Path) -> None:
        """Test updating version in package.json"""
        file_path = temp_dir / "package.json"
        file_path.write_text('{\n  "version": "1.0.0",\n  "name": "test"\n}', encoding="utf-8")

        vm = VersionManager(temp_dir)
        vm._update_version_in_file(file_path, "2.0.0")

        content = file_path.read_text(encoding="utf-8")
        assert '"version": "2.0.0"' in content
        assert '"name": "test"' in content

    def test_update_init_py(self, temp_dir: Path) -> None:
        """Test updating version in __init__.py"""
        file_path = temp_dir / "__init__.py"
        file_path.write_text('__version__ = "1.0.0"\n__author__ = "test"', encoding="utf-8")

        vm = VersionManager(temp_dir)
        vm._update_version_in_file(file_path, "2.0.0")

        content = file_path.read_text(encoding="utf-8")
        assert '__version__ = "2.0.0"' in content
        assert '__author__ = "test"' in content

    def test_update_init_py_single_quotes(self, temp_dir: Path) -> None:
        """Test updating version in __init__.py with single quotes"""
        file_path = temp_dir / "__init__.py"
        file_path.write_text("__version__ = '1.0.0'", encoding="utf-8")

        vm = VersionManager(temp_dir)
        vm._update_version_in_file(file_path, "2.0.0")

        content = file_path.read_text(encoding="utf-8")
        assert '__version__ = "2.0.0"' in content

    def test_update_cargo_toml(self, temp_dir: Path) -> None:
        """Test updating version in Cargo.toml"""
        file_path = temp_dir / "Cargo.toml"
        content = '[package]\nversion = "1.0.0"\nname = "test"\n\n[dependencies]\nfoo = { version = "0.5.0" }'
        file_path.write_text(content, encoding="utf-8")

        vm = VersionManager(temp_dir)
        vm._update_version_in_file(file_path, "2.0.0")

        content = file_path.read_text(encoding="utf-8")
        # Should only update first occurrence (package version, not dependency)
        assert content.count('"2.0.0"') == 1
        assert 'version = "2.0.0"' in content
        assert 'foo = { version = "0.5.0" }' in content

    def test_update_version_txt(self, temp_dir: Path) -> None:
        """Test updating version in version.txt"""
        file_path = temp_dir / "version.txt"
        file_path.write_text("1.0.0\n", encoding="utf-8")

        vm = VersionManager(temp_dir)
        vm._update_version_in_file(file_path, "2.0.0")

        content = file_path.read_text(encoding="utf-8")
        assert content == "2.0.0\n"

    def test_update_with_whitespace_variations(self, temp_dir: Path) -> None:
        """Test updating with various whitespace patterns"""
        file_path = temp_dir / "pyproject.toml"
        file_path.write_text('version  =  "1.0.0"', encoding="utf-8")

        vm = VersionManager(temp_dir)
        vm._update_version_in_file(file_path, "2.0.0")

        content = file_path.read_text(encoding="utf-8")
        assert '"2.0.0"' in content


class TestUpdateVersionFiles:
    """Test update_version_files method"""

    def test_update_default_files(self, temp_dir: Path) -> None:
        """Test updating auto-detected files"""
        pyproject = temp_dir / "pyproject.toml"
        pyproject.write_text('version = "1.0.0"', encoding="utf-8")

        vm = VersionManager(temp_dir)
        vm.update_version_files("2.0.0")

        content = pyproject.read_text(encoding="utf-8")
        assert '"2.0.0"' in content

    def test_update_specified_files(self, temp_dir: Path) -> None:
        """Test updating specified files only"""
        pyproject = temp_dir / "pyproject.toml"
        pyproject.write_text('version = "1.0.0"', encoding="utf-8")
        package = temp_dir / "package.json"
        package.write_text('"version": "1.0.0"', encoding="utf-8")

        vm = VersionManager(temp_dir)
        vm.update_version_files("2.0.0", files=[pyproject])

        # Only pyproject.toml should be updated
        assert '"2.0.0"' in pyproject.read_text(encoding="utf-8")
        assert '"1.0.0"' in package.read_text(encoding="utf-8")

    def test_update_multiple_files(self, temp_dir: Path) -> None:
        """Test updating multiple files"""
        pyproject = temp_dir / "pyproject.toml"
        pyproject.write_text('version = "1.0.0"', encoding="utf-8")
        package = temp_dir / "package.json"
        package.write_text('"version": "1.0.0"', encoding="utf-8")

        vm = VersionManager(temp_dir)
        vm.update_version_files("2.0.0")

        assert '"2.0.0"' in pyproject.read_text(encoding="utf-8")
        assert '"2.0.0"' in package.read_text(encoding="utf-8")

    def test_update_empty_files_list(self, temp_dir: Path) -> None:
        """Test updating with empty files list"""
        vm = VersionManager(temp_dir)
        # Should not raise error
        vm.update_version_files("2.0.0", files=[])


class TestCreateGitTag:
    """Test create_git_tag method"""

    def test_tag_name_without_create(self, temp_dir: Path) -> None:
        """Test getting tag name without creating"""
        vm = VersionManager(temp_dir)
        tag = vm.create_git_tag("1.2.3", create=False)
        assert tag == "v1.2.3"

    def test_tag_name_format(self, temp_dir: Path) -> None:
        """Test tag name formatting"""
        vm = VersionManager(temp_dir)
        assert vm.create_git_tag("1.0.0", create=False) == "v1.0.0"
        assert vm.create_git_tag("2.5.8", create=False) == "v2.5.8"
        assert vm.create_git_tag("10.20.30", create=False) == "v10.20.30"

    @patch("subprocess.run")
    def test_create_tag_success(self, mock_run: Mock, temp_dir: Path) -> None:
        """Test successful tag creation"""
        mock_run.return_value = Mock(stdout="", stderr="", returncode=0)

        vm = VersionManager(temp_dir)
        tag = vm.create_git_tag("1.2.3", create=True)

        assert tag == "v1.2.3"
        mock_run.assert_called_once_with(
            ["git", "tag", "-a", "v1.2.3", "-m", "Release 1.2.3"],
            cwd=temp_dir,
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        )

    @patch("subprocess.run")
    def test_create_tag_failure(self, mock_run: Mock, temp_dir: Path) -> None:
        """Test tag creation failure"""
        mock_run.side_effect = subprocess.CalledProcessError(1, "git", stderr="tag already exists")

        vm = VersionManager(temp_dir)
        with pytest.raises(RuntimeError, match="Failed to create git tag"):
            vm.create_git_tag("1.2.3", create=True)

    @patch("subprocess.run")
    def test_create_tag_with_error_message(self, mock_run: Mock, temp_dir: Path) -> None:
        """Test tag creation failure includes error message"""
        error_msg = "fatal: tag 'v1.2.3' already exists"
        mock_run.side_effect = subprocess.CalledProcessError(1, "git", stderr=error_msg)

        vm = VersionManager(temp_dir)
        with pytest.raises(RuntimeError, match=error_msg):
            vm.create_git_tag("1.2.3", create=True)


class TestGetCommitsSinceLastTag:
    """Test get_commits_since_last_tag method"""

    @patch("subprocess.run")
    def test_get_commits_success(self, mock_run: Mock, temp_dir: Path) -> None:
        """Test getting commits since last tag"""
        # Mock git describe
        describe_result = Mock(stdout="v1.2.3\n", stderr="", returncode=0)
        # Mock git log
        log_result = Mock(stdout="feat: new feature\nfix: bug fix\n", stderr="", returncode=0)

        mock_run.side_effect = [describe_result, log_result]

        vm = VersionManager(temp_dir)
        version, commits = vm.get_commits_since_last_tag()

        assert version == "1.2.3"
        assert commits == ["feat: new feature", "fix: bug fix"]

    @patch("subprocess.run")
    def test_get_commits_no_tags(self, mock_run: Mock, temp_dir: Path) -> None:
        """Test when no tags exist"""
        mock_run.side_effect = subprocess.CalledProcessError(1, "git", stderr="No tags")

        vm = VersionManager(temp_dir)
        version, commits = vm.get_commits_since_last_tag()

        assert version == "0.0.0"
        assert commits == []

    @patch("subprocess.run")
    def test_get_commits_with_v_prefix(self, mock_run: Mock, temp_dir: Path) -> None:
        """Test extracting version from tag with v prefix"""
        describe_result = Mock(stdout="v2.5.8\n", stderr="", returncode=0)
        log_result = Mock(stdout="feat: feature\n", stderr="", returncode=0)

        mock_run.side_effect = [describe_result, log_result]

        vm = VersionManager(temp_dir)
        version, commits = vm.get_commits_since_last_tag()

        assert version == "2.5.8"

    @patch("subprocess.run")
    def test_get_commits_no_new_commits(self, mock_run: Mock, temp_dir: Path) -> None:
        """Test when no new commits since tag"""
        describe_result = Mock(stdout="v1.2.3\n", stderr="", returncode=0)
        log_result = Mock(stdout="", stderr="", returncode=0)

        mock_run.side_effect = [describe_result, log_result]

        vm = VersionManager(temp_dir)
        version, commits = vm.get_commits_since_last_tag()

        assert version == "1.2.3"
        assert commits == []

    @patch("subprocess.run")
    def test_get_commits_filters_empty_lines(self, mock_run: Mock, temp_dir: Path) -> None:
        """Test filtering empty lines from commits"""
        describe_result = Mock(stdout="v1.2.3\n", stderr="", returncode=0)
        log_result = Mock(stdout="feat: feature\n\n\nfix: fix\n", stderr="", returncode=0)

        mock_run.side_effect = [describe_result, log_result]

        vm = VersionManager(temp_dir)
        version, commits = vm.get_commits_since_last_tag()

        assert commits == ["feat: feature", "fix: fix"]

    @patch("subprocess.run")
    def test_get_commits_strips_whitespace(self, mock_run: Mock, temp_dir: Path) -> None:
        """Test stripping whitespace from commits"""
        describe_result = Mock(stdout="v1.2.3\n", stderr="", returncode=0)
        log_result = Mock(stdout="  feat: feature  \n\tfix: fix\t\n", stderr="", returncode=0)

        mock_run.side_effect = [describe_result, log_result]

        vm = VersionManager(temp_dir)
        version, commits = vm.get_commits_since_last_tag()

        assert commits == ["feat: feature", "fix: fix"]

    @patch("subprocess.run")
    def test_get_commits_complex_tag(self, mock_run: Mock, temp_dir: Path) -> None:
        """Test extracting version from complex tag name"""
        describe_result = Mock(stdout="release-v1.2.3-beta\n", stderr="", returncode=0)
        log_result = Mock(stdout="feat: feature\n", stderr="", returncode=0)

        mock_run.side_effect = [describe_result, log_result]

        vm = VersionManager(temp_dir)
        version, commits = vm.get_commits_since_last_tag()

        assert version == "1.2.3"

    @patch("subprocess.run")
    def test_git_describe_called_correctly(self, mock_run: Mock, temp_dir: Path) -> None:
        """Test git describe is called with correct arguments"""
        describe_result = Mock(stdout="v1.2.3\n", stderr="", returncode=0)
        log_result = Mock(stdout="", stderr="", returncode=0)

        mock_run.side_effect = [describe_result, log_result]

        vm = VersionManager(temp_dir)
        vm.get_commits_since_last_tag()

        # Check first call (git describe)
        first_call = mock_run.call_args_list[0]
        assert first_call[1]["cwd"] == temp_dir
        assert first_call[0][0] == ["git", "describe", "--tags", "--abbrev=0"]

    @patch("subprocess.run")
    def test_git_log_called_correctly(self, mock_run: Mock, temp_dir: Path) -> None:
        """Test git log is called with correct arguments"""
        describe_result = Mock(stdout="v1.2.3\n", stderr="", returncode=0)
        log_result = Mock(stdout="", stderr="", returncode=0)

        mock_run.side_effect = [describe_result, log_result]

        vm = VersionManager(temp_dir)
        vm.get_commits_since_last_tag()

        # Check second call (git log)
        second_call = mock_run.call_args_list[1]
        assert second_call[1]["cwd"] == temp_dir
        assert second_call[0][0] == [
            "git",
            "log",
            "v1.2.3..HEAD",
            "--pretty=format:%s",
        ]


class TestAutoBump:
    """Test auto_bump method"""

    @patch.object(VersionManager, "get_commits_since_last_tag")
    @patch.object(VersionManager, "update_version_files")
    def test_auto_bump_no_commits(
        self, mock_update: Mock, mock_get_commits: Mock, temp_dir: Path
    ) -> None:
        """Test auto bump with no commits"""
        mock_get_commits.return_value = ("1.2.3", [])

        vm = VersionManager(temp_dir)
        result = vm.auto_bump()

        assert result is None
        mock_update.assert_not_called()

    @patch.object(VersionManager, "get_commits_since_last_tag")
    @patch.object(VersionManager, "update_version_files")
    def test_auto_bump_no_bump_needed(
        self, mock_update: Mock, mock_get_commits: Mock, temp_dir: Path
    ) -> None:
        """Test auto bump with no version bump needed"""
        mock_get_commits.return_value = ("1.2.3", ["docs: update README"])

        vm = VersionManager(temp_dir)
        result = vm.auto_bump()

        assert result is None
        mock_update.assert_not_called()

    @patch.object(VersionManager, "get_commits_since_last_tag")
    @patch.object(VersionManager, "update_version_files")
    def test_auto_bump_patch(
        self, mock_update: Mock, mock_get_commits: Mock, temp_dir: Path
    ) -> None:
        """Test auto bump with patch"""
        mock_get_commits.return_value = ("1.2.3", ["fix: bug fix"])

        vm = VersionManager(temp_dir)
        result = vm.auto_bump()

        assert result == "1.2.4"
        mock_update.assert_called_once_with("1.2.4")

    @patch.object(VersionManager, "get_commits_since_last_tag")
    @patch.object(VersionManager, "update_version_files")
    def test_auto_bump_minor(
        self, mock_update: Mock, mock_get_commits: Mock, temp_dir: Path
    ) -> None:
        """Test auto bump with minor"""
        mock_get_commits.return_value = ("1.2.3", ["feat: new feature"])

        vm = VersionManager(temp_dir)
        result = vm.auto_bump()

        assert result == "1.3.0"
        mock_update.assert_called_once_with("1.3.0")

    @patch.object(VersionManager, "get_commits_since_last_tag")
    @patch.object(VersionManager, "update_version_files")
    def test_auto_bump_major(
        self, mock_update: Mock, mock_get_commits: Mock, temp_dir: Path
    ) -> None:
        """Test auto bump with major"""
        mock_get_commits.return_value = ("1.2.3", ["feat!: breaking change"])

        vm = VersionManager(temp_dir)
        result = vm.auto_bump()

        assert result == "2.0.0"
        mock_update.assert_called_once_with("2.0.0")

    @patch.object(VersionManager, "get_commits_since_last_tag")
    @patch.object(VersionManager, "update_version_files")
    @patch.object(VersionManager, "create_git_tag")
    def test_auto_bump_with_tag_creation(
        self,
        mock_create_tag: Mock,
        mock_update: Mock,
        mock_get_commits: Mock,
        temp_dir: Path,
    ) -> None:
        """Test auto bump with tag creation"""
        mock_get_commits.return_value = ("1.2.3", ["feat: new feature"])
        mock_create_tag.return_value = "v1.3.0"

        vm = VersionManager(temp_dir)
        result = vm.auto_bump(create_tag=True)

        assert result == "1.3.0"
        mock_update.assert_called_once_with("1.3.0")
        mock_create_tag.assert_called_once_with("1.3.0", create=True)

    @patch.object(VersionManager, "get_commits_since_last_tag")
    @patch.object(VersionManager, "update_version_files")
    @patch.object(VersionManager, "create_git_tag")
    def test_auto_bump_without_tag_creation(
        self,
        mock_create_tag: Mock,
        mock_update: Mock,
        mock_get_commits: Mock,
        temp_dir: Path,
    ) -> None:
        """Test auto bump without tag creation"""
        mock_get_commits.return_value = ("1.2.3", ["feat: new feature"])

        vm = VersionManager(temp_dir)
        result = vm.auto_bump(create_tag=False)

        assert result == "1.3.0"
        mock_update.assert_called_once_with("1.3.0")
        mock_create_tag.assert_not_called()

    @patch.object(VersionManager, "get_commits_since_last_tag")
    @patch.object(VersionManager, "update_version_files")
    @patch("builtins.print")
    def test_auto_bump_prints_messages(
        self,
        mock_print: Mock,
        mock_update: Mock,
        mock_get_commits: Mock,
        temp_dir: Path,
    ) -> None:
        """Test auto bump prints appropriate messages"""
        mock_get_commits.return_value = ("1.2.3", ["feat: new feature"])

        vm = VersionManager(temp_dir)
        vm.auto_bump()

        # Check that print was called with expected messages
        print_calls = [call[0][0] for call in mock_print.call_args_list]
        assert any("1.2.3 → 1.3.0" in str(call) for call in print_calls)
        assert any("Updated version files" in str(call) for call in print_calls)

    @patch.object(VersionManager, "get_commits_since_last_tag")
    @patch.object(VersionManager, "update_version_files")
    @patch.object(VersionManager, "create_git_tag")
    @patch("builtins.print")
    def test_auto_bump_prints_tag_message(
        self,
        mock_print: Mock,
        mock_create_tag: Mock,
        mock_update: Mock,
        mock_get_commits: Mock,
        temp_dir: Path,
    ) -> None:
        """Test auto bump prints tag creation message"""
        mock_get_commits.return_value = ("1.2.3", ["feat: new feature"])
        mock_create_tag.return_value = "v1.3.0"

        vm = VersionManager(temp_dir)
        vm.auto_bump(create_tag=True)

        print_calls = [call[0][0] for call in mock_print.call_args_list]
        assert any("v1.3.0" in str(call) for call in print_calls)

    @patch.object(VersionManager, "get_commits_since_last_tag")
    @patch("builtins.print")
    def test_auto_bump_no_commits_message(
        self, mock_print: Mock, mock_get_commits: Mock, temp_dir: Path
    ) -> None:
        """Test auto bump prints message when no commits"""
        mock_get_commits.return_value = ("1.2.3", [])

        vm = VersionManager(temp_dir)
        vm.auto_bump()

        print_calls = [call[0][0] for call in mock_print.call_args_list]
        assert any("No commits since last version" in str(call) for call in print_calls)

    @patch.object(VersionManager, "get_commits_since_last_tag")
    @patch("builtins.print")
    def test_auto_bump_no_bump_message(
        self, mock_print: Mock, mock_get_commits: Mock, temp_dir: Path
    ) -> None:
        """Test auto bump prints message when no bump needed"""
        mock_get_commits.return_value = ("1.2.3", ["docs: update"])

        vm = VersionManager(temp_dir)
        vm.auto_bump()

        print_calls = [call[0][0] for call in mock_print.call_args_list]
        assert any("No version bump needed" in str(call) for call in print_calls)


class TestVersionManagerIntegration:
    """Integration tests for VersionManager"""

    def test_full_workflow_patch(self, temp_dir: Path) -> None:
        """Test full workflow for patch bump"""
        # Setup version file
        pyproject = temp_dir / "pyproject.toml"
        pyproject.write_text('[tool.poetry]\nversion = "1.2.3"', encoding="utf-8")

        vm = VersionManager(temp_dir)

        # Detect bump type
        commits = ["fix: bug fix"]
        bump_type = vm.detect_bump_type(commits)
        assert bump_type == BumpType.PATCH

        # Calculate new version
        new_version = vm.bump_version("1.2.3", bump_type)
        assert new_version == "1.2.4"

        # Update files
        vm.update_version_files(new_version)

        # Verify update
        content = pyproject.read_text(encoding="utf-8")
        assert '"1.2.4"' in content

    def test_full_workflow_minor(self, temp_dir: Path) -> None:
        """Test full workflow for minor bump"""
        pyproject = temp_dir / "pyproject.toml"
        pyproject.write_text('[tool.poetry]\nversion = "1.2.3"', encoding="utf-8")

        vm = VersionManager(temp_dir)

        commits = ["feat: new feature"]
        bump_type = vm.detect_bump_type(commits)
        new_version = vm.bump_version("1.2.3", bump_type)

        assert new_version == "1.3.0"

        vm.update_version_files(new_version)
        content = pyproject.read_text(encoding="utf-8")
        assert '"1.3.0"' in content

    def test_full_workflow_major(self, temp_dir: Path) -> None:
        """Test full workflow for major bump"""
        pyproject = temp_dir / "pyproject.toml"
        pyproject.write_text('[tool.poetry]\nversion = "1.2.3"', encoding="utf-8")

        vm = VersionManager(temp_dir)

        commits = ["feat!: breaking change"]
        bump_type = vm.detect_bump_type(commits)
        new_version = vm.bump_version("1.2.3", bump_type)

        assert new_version == "2.0.0"

        vm.update_version_files(new_version)
        content = pyproject.read_text(encoding="utf-8")
        assert '"2.0.0"' in content

    def test_multiple_version_files(self, temp_dir: Path) -> None:
        """Test updating multiple version files simultaneously"""
        pyproject = temp_dir / "pyproject.toml"
        pyproject.write_text('version = "1.0.0"', encoding="utf-8")

        package = temp_dir / "package.json"
        package.write_text('{"version": "1.0.0"}', encoding="utf-8")

        init = temp_dir / "__init__.py"
        init.write_text('__version__ = "1.0.0"', encoding="utf-8")

        vm = VersionManager(temp_dir)
        vm.update_version_files("2.0.0")

        assert '"2.0.0"' in pyproject.read_text(encoding="utf-8")
        assert '"2.0.0"' in package.read_text(encoding="utf-8")
        assert '"2.0.0"' in init.read_text(encoding="utf-8")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=claudecodeoptimizer.core.version_manager"])
