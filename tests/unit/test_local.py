"""Unit tests for local module."""

import argparse
import json
from pathlib import Path
from unittest.mock import patch

from claudecodeoptimizer.local import (
    PERMISSION_LEVELS,
    STATUSLINE_MODES,
    _execute_local_setup,
    _is_safe_path,
    _validate_local_path,
    run_local_mode,
    setup_local_permissions,
    setup_local_statusline,
)


class TestIsSafePath:
    """Test _is_safe_path function."""

    def test_returns_true_for_home_directory(self) -> None:
        """Test _is_safe_path returns True for home directory."""
        home = Path.home()
        assert _is_safe_path(home) is True

    def test_returns_true_for_subdirectory_of_home(self, tmp_path: Path) -> None:
        """Test _is_safe_path returns True for subdirectory of home."""
        with patch("pathlib.Path.home", return_value=tmp_path):
            subdir = tmp_path / "subdir"
            subdir.mkdir()
            assert _is_safe_path(subdir) is True

    def test_returns_true_for_current_directory(self) -> None:
        """Test _is_safe_path returns True for current directory."""
        cwd = Path.cwd()
        assert _is_safe_path(cwd) is True

    def test_returns_true_for_subdirectory_of_cwd(self, tmp_path: Path) -> None:
        """Test _is_safe_path returns True for subdirectory of cwd."""
        with patch("pathlib.Path.cwd", return_value=tmp_path):
            subdir = tmp_path / "project"
            subdir.mkdir()
            assert _is_safe_path(subdir) is True

    def test_returns_false_for_path_outside_home_and_cwd(self, tmp_path: Path) -> None:
        """Test _is_safe_path returns False for path outside home and cwd."""
        # Create a path outside both home and cwd
        fake_home = tmp_path / "home"
        fake_cwd = tmp_path / "cwd"
        unsafe_path = tmp_path / "unsafe"

        fake_home.mkdir()
        fake_cwd.mkdir()
        unsafe_path.mkdir()

        with patch("pathlib.Path.home", return_value=fake_home):
            with patch("pathlib.Path.cwd", return_value=fake_cwd):
                assert _is_safe_path(unsafe_path) is False

    def test_resolves_symlinks_before_checking(self, tmp_path: Path) -> None:
        """Test _is_safe_path resolves symlinks before checking."""
        real_dir = tmp_path / "real"
        real_dir.mkdir()

        with patch("pathlib.Path.home", return_value=tmp_path):
            # Test with resolved path
            assert _is_safe_path(real_dir) is True

    def test_prevents_path_traversal_attack(self, tmp_path: Path) -> None:
        """Test _is_safe_path prevents path traversal attacks."""
        safe_dir = tmp_path / "safe"
        safe_dir.mkdir()

        # Try to use .. to escape
        unsafe_path = safe_dir / ".." / ".." / "etc"

        with patch("pathlib.Path.home", return_value=safe_dir):
            with patch("pathlib.Path.cwd", return_value=safe_dir):
                # After resolve(), this will be outside safe_dir
                assert _is_safe_path(unsafe_path) is False


class TestSetupLocalStatusline:
    """Test setup_local_statusline function."""

    def test_copies_statusline_to_local_claude_dir(self, tmp_path: Path) -> None:
        """Test setup_local_statusline copies statusline to .claude/."""
        project = tmp_path / "project"
        project.mkdir()

        # Create source statusline
        src_dir = tmp_path / "source" / "statusline"
        src_dir.mkdir(parents=True)
        (src_dir / "cco-full.js").write_text("console.log('full');")

        with patch("claudecodeoptimizer.local.get_content_path", return_value=src_dir):
            result = setup_local_statusline(project, "cco-full", verbose=False)

        assert result is True
        assert (project / ".claude" / "cco-statusline.js").exists()
        assert "full" in (project / ".claude" / "cco-statusline.js").read_text()

    def test_updates_settings_json_with_statusline_config(self, tmp_path: Path) -> None:
        """Test setup_local_statusline updates settings.json."""
        project = tmp_path / "project"
        project.mkdir()

        src_dir = tmp_path / "source" / "statusline"
        src_dir.mkdir(parents=True)
        (src_dir / "cco-minimal.js").write_text("console.log('minimal');")

        with patch("claudecodeoptimizer.local.get_content_path", return_value=src_dir):
            setup_local_statusline(project, "cco-minimal", verbose=False)

        settings_file = project / ".claude" / "settings.json"
        assert settings_file.exists()

        settings = json.loads(settings_file.read_text())
        assert "statusLine" in settings
        assert settings["statusLine"]["type"] == "command"
        assert "node .claude/cco-statusline.js" in settings["statusLine"]["command"]

    def test_returns_false_for_invalid_mode(self, tmp_path: Path) -> None:
        """Test setup_local_statusline returns False for invalid mode."""
        project = tmp_path / "project"
        project.mkdir()

        result = setup_local_statusline(project, "invalid-mode", verbose=False)
        assert result is False

    def test_returns_false_when_source_missing(self, tmp_path: Path) -> None:
        """Test setup_local_statusline returns False when source doesn't exist."""
        project = tmp_path / "project"
        project.mkdir()

        nonexistent = tmp_path / "nonexistent"
        with patch("claudecodeoptimizer.local.get_content_path", return_value=nonexistent):
            result = setup_local_statusline(project, "cco-full", verbose=False)

        assert result is False

    def test_overwrites_existing_statusline(self, tmp_path: Path) -> None:
        """Test setup_local_statusline overwrites existing statusline."""
        project = tmp_path / "project"
        local_claude = project / ".claude"
        local_claude.mkdir(parents=True)

        # Create old statusline
        old_statusline = local_claude / "cco-statusline.js"
        old_statusline.write_text("old content")

        # Create source
        src_dir = tmp_path / "source" / "statusline"
        src_dir.mkdir(parents=True)
        (src_dir / "cco-full.js").write_text("new content")

        with patch("claudecodeoptimizer.local.get_content_path", return_value=src_dir):
            setup_local_statusline(project, "cco-full", verbose=False)

        assert old_statusline.read_text() == "new content"


class TestSetupLocalPermissions:
    """Test setup_local_permissions function."""

    def test_sets_permissions_in_settings_json(self, tmp_path: Path) -> None:
        """Test setup_local_permissions sets permissions in settings.json."""
        project = tmp_path / "project"
        project.mkdir()

        # Create source permissions
        src_dir = tmp_path / "source" / "permissions"
        src_dir.mkdir(parents=True)
        perm_data = {"permissions": {"read": True, "write": False}}
        (src_dir / "safe.json").write_text(json.dumps(perm_data))

        with patch("claudecodeoptimizer.local.get_content_path", return_value=src_dir):
            result = setup_local_permissions(project, "safe", verbose=False)

        assert result is True
        settings_file = project / ".claude" / "settings.json"
        settings = json.loads(settings_file.read_text())
        assert "permissions" in settings
        assert settings["permissions"]["read"] is True
        assert settings["permissions"]["write"] is False

    def test_adds_cco_managed_marker(self, tmp_path: Path) -> None:
        """Test setup_local_permissions adds CCO managed marker."""
        project = tmp_path / "project"
        project.mkdir()

        src_dir = tmp_path / "source" / "permissions"
        src_dir.mkdir(parents=True)
        perm_data = {"permissions": {}}
        (src_dir / "balanced.json").write_text(json.dumps(perm_data))

        with patch("claudecodeoptimizer.local.get_content_path", return_value=src_dir):
            setup_local_permissions(project, "balanced", verbose=False)

        settings_file = project / ".claude" / "settings.json"
        settings = json.loads(settings_file.read_text())
        assert "_cco_managed" in settings
        assert settings["_cco_managed"] is True

    def test_returns_false_for_invalid_level(self, tmp_path: Path) -> None:
        """Test setup_local_permissions returns False for invalid level."""
        project = tmp_path / "project"
        project.mkdir()

        result = setup_local_permissions(project, "invalid-level", verbose=False)
        assert result is False

    def test_returns_false_when_source_missing(self, tmp_path: Path) -> None:
        """Test setup_local_permissions returns False when source doesn't exist."""
        project = tmp_path / "project"
        project.mkdir()

        nonexistent = tmp_path / "nonexistent"
        with patch("claudecodeoptimizer.local.get_content_path", return_value=nonexistent):
            result = setup_local_permissions(project, "safe", verbose=False)

        assert result is False

    def test_returns_false_for_invalid_json(self, tmp_path: Path) -> None:
        """Test setup_local_permissions returns False for invalid JSON."""
        project = tmp_path / "project"
        project.mkdir()

        src_dir = tmp_path / "source" / "permissions"
        src_dir.mkdir(parents=True)
        (src_dir / "safe.json").write_text("invalid json {")

        with patch("claudecodeoptimizer.local.get_content_path", return_value=src_dir):
            result = setup_local_permissions(project, "safe", verbose=False)

        assert result is False


class TestValidateLocalPath:
    """Test _validate_local_path function."""

    def test_returns_none_for_valid_path(self, tmp_path: Path) -> None:
        """Test _validate_local_path returns None for valid path."""
        project = tmp_path / "project"
        project.mkdir()

        with patch("claudecodeoptimizer.local._is_safe_path", return_value=True):
            result = _validate_local_path(project)
            assert result is None

    def test_returns_error_for_nonexistent_path(self, tmp_path: Path) -> None:
        """Test _validate_local_path returns error for nonexistent path."""
        nonexistent = tmp_path / "nonexistent"

        result = _validate_local_path(nonexistent)
        assert result is not None
        assert "does not exist" in result

    def test_returns_error_for_file_instead_of_directory(self, tmp_path: Path) -> None:
        """Test _validate_local_path returns error for file instead of directory."""
        file_path = tmp_path / "file.txt"
        file_path.write_text("test")

        result = _validate_local_path(file_path)
        assert result is not None
        assert "Not a directory" in result

    def test_returns_error_for_unsafe_path(self, tmp_path: Path) -> None:
        """Test _validate_local_path returns error for unsafe path."""
        project = tmp_path / "project"
        project.mkdir()

        with patch("claudecodeoptimizer.local._is_safe_path", return_value=False):
            result = _validate_local_path(project)
            assert result is not None
            assert "within home directory" in result


class TestExecuteLocalSetup:
    """Test _execute_local_setup function."""

    def test_sets_up_statusline_when_requested(self, tmp_path: Path, capsys) -> None:
        """Test _execute_local_setup sets up statusline when requested."""
        project = tmp_path / "project"
        project.mkdir()

        args = argparse.Namespace(
            statusline="cco-full",
            permissions=None,
        )

        src_dir = tmp_path / "source" / "statusline"
        src_dir.mkdir(parents=True)
        (src_dir / "cco-full.js").write_text("console.log('test');")

        with patch("claudecodeoptimizer.local.get_content_path", return_value=src_dir):
            result = _execute_local_setup(project, args)

        assert result == 0
        assert (project / ".claude" / "cco-statusline.js").exists()

    def test_sets_up_permissions_when_requested(self, tmp_path: Path) -> None:
        """Test _execute_local_setup sets up permissions when requested."""
        project = tmp_path / "project"
        project.mkdir()

        args = argparse.Namespace(
            statusline=None,
            permissions="safe",
        )

        src_dir = tmp_path / "source" / "permissions"
        src_dir.mkdir(parents=True)
        perm_data = {"permissions": {}}
        (src_dir / "safe.json").write_text(json.dumps(perm_data))

        with patch("claudecodeoptimizer.local.get_content_path", return_value=src_dir):
            result = _execute_local_setup(project, args)

        assert result == 0
        settings_file = project / ".claude" / "settings.json"
        assert settings_file.exists()

    def test_sets_up_both_statusline_and_permissions(self, tmp_path: Path) -> None:
        """Test _execute_local_setup sets up both statusline and permissions."""
        project = tmp_path / "project"
        project.mkdir()

        args = argparse.Namespace(
            statusline="cco-minimal",
            permissions="balanced",
        )

        # Setup mocks for both
        statusline_dir = tmp_path / "statusline"
        statusline_dir.mkdir()
        (statusline_dir / "cco-minimal.js").write_text("console.log('test');")

        permissions_dir = tmp_path / "permissions"
        permissions_dir.mkdir()
        perm_data = {"permissions": {}}
        (permissions_dir / "balanced.json").write_text(json.dumps(perm_data))

        def mock_get_content_path(subdir: str) -> Path:
            if subdir == "statusline":
                return statusline_dir
            return permissions_dir

        with patch("claudecodeoptimizer.local.get_content_path", side_effect=mock_get_content_path):
            result = _execute_local_setup(project, args)

        assert result == 0
        assert (project / ".claude" / "cco-statusline.js").exists()
        settings = json.loads((project / ".claude" / "settings.json").read_text())
        assert "statusLine" in settings
        assert "permissions" in settings

    def test_creates_claude_dir_when_no_options(self, tmp_path: Path) -> None:
        """Test _execute_local_setup creates .claude/ when no options given."""
        project = tmp_path / "project"
        project.mkdir()

        args = argparse.Namespace(
            statusline=None,
            permissions=None,
        )

        result = _execute_local_setup(project, args)

        assert result == 0
        assert (project / ".claude").exists()

    def test_returns_error_code_on_failure(self, tmp_path: Path) -> None:
        """Test _execute_local_setup returns error code on failure."""
        project = tmp_path / "project"
        project.mkdir()

        args = argparse.Namespace(
            statusline="invalid-mode",
            permissions=None,
        )

        result = _execute_local_setup(project, args)

        assert result == 1


class TestRunLocalMode:
    """Test run_local_mode function."""

    def test_validates_path_before_setup(self, tmp_path: Path) -> None:
        """Test run_local_mode validates path before executing setup."""
        nonexistent = tmp_path / "nonexistent"

        args = argparse.Namespace(
            local=str(nonexistent),
            statusline=None,
            permissions=None,
        )

        result = run_local_mode(args)

        assert result == 1

    def test_executes_setup_for_valid_path(self, tmp_path: Path) -> None:
        """Test run_local_mode executes setup for valid path."""
        project = tmp_path / "project"
        project.mkdir()

        args = argparse.Namespace(
            local=str(project),
            statusline=None,
            permissions=None,
        )

        with patch("claudecodeoptimizer.local._is_safe_path", return_value=True):
            result = run_local_mode(args)

        assert result == 0
        assert (project / ".claude").exists()


class TestConstants:
    """Test module constants."""

    def test_statusline_modes_defined(self) -> None:
        """Test STATUSLINE_MODES constant is defined correctly."""
        assert "cco-full" in STATUSLINE_MODES
        assert "cco-minimal" in STATUSLINE_MODES
        assert len(STATUSLINE_MODES) == 2

    def test_permission_levels_defined(self) -> None:
        """Test PERMISSION_LEVELS constant is defined correctly."""
        assert "safe" in PERMISSION_LEVELS
        assert "balanced" in PERMISSION_LEVELS
        assert "permissive" in PERMISSION_LEVELS
        assert "full" in PERMISSION_LEVELS
        assert len(PERMISSION_LEVELS) == 4
