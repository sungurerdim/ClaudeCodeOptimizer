"""
Unit tests for Core Knowledge Setup

Tests global knowledge directory initialization, file copying, and path validation.
Target Coverage: 100%
"""

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, Mock, patch

import pytest

from claudecodeoptimizer.core import knowledge_setup


class TestSetupGlobalKnowledge:
    """Test setup_global_knowledge function"""

    @patch("claudecodeoptimizer.core.knowledge_setup._setup_claude_home_links")
    @patch("claudecodeoptimizer.core.knowledge_setup._setup_skills")
    @patch("claudecodeoptimizer.core.knowledge_setup._setup_agents")
    @patch("claudecodeoptimizer.core.knowledge_setup._setup_principles")
    @patch("claudecodeoptimizer.core.knowledge_setup._setup_guides")
    @patch("claudecodeoptimizer.core.knowledge_setup._setup_commands")
    @patch("claudecodeoptimizer.core.knowledge_setup._setup_templates")
    @patch("claudecodeoptimizer.config.get_skills_dir")
    @patch("claudecodeoptimizer.config.get_agents_dir")
    @patch("claudecodeoptimizer.config.get_principles_dir")
    @patch("claudecodeoptimizer.config.get_guides_dir")
    @patch("claudecodeoptimizer.config.get_global_commands_dir")
    @patch("claudecodeoptimizer.config.get_templates_dir")
    @patch("claudecodeoptimizer.config.get_global_dir")
    def test_setup_creates_all_directories(
        self,
        mock_global_dir: Mock,
        mock_templates_dir: Mock,
        mock_commands_dir: Mock,
        mock_guides_dir: Mock,
        mock_principles_dir: Mock,
        mock_agents_dir: Mock,
        mock_skills_dir: Mock,
        mock_setup_templates: Mock,
        mock_setup_commands: Mock,
        mock_setup_guides: Mock,
        mock_setup_principles: Mock,
        mock_setup_agents: Mock,
        mock_setup_skills: Mock,
        mock_setup_claude_home_links: Mock,
    ) -> None:
        """Test that setup_global_knowledge creates all necessary directories"""
        # Setup mocks
        global_dir_path = MagicMock(spec=Path)
        mock_global_dir.return_value = global_dir_path
        mock_templates_dir.return_value = MagicMock(spec=Path)
        mock_commands_dir.return_value = MagicMock(spec=Path)
        mock_guides_dir.return_value = MagicMock(spec=Path)
        mock_principles_dir.return_value = MagicMock(spec=Path)
        mock_agents_dir.return_value = MagicMock(spec=Path)
        mock_skills_dir.return_value = MagicMock(spec=Path)

        # Execute
        result = knowledge_setup.setup_global_knowledge()

        # Verify global directory creation
        global_dir_path.mkdir.assert_called_once_with(parents=True, exist_ok=True)

        # Verify all setup functions called
        mock_setup_templates.assert_called_once()
        mock_setup_commands.assert_called_once()
        mock_setup_guides.assert_called_once()
        mock_setup_principles.assert_called_once()
        mock_setup_agents.assert_called_once()
        mock_setup_skills.assert_called_once()
        mock_setup_claude_home_links.assert_called_once()

        # Verify result structure
        assert result["success"] is True
        assert "global_dir" in result
        assert "actions" in result
        assert len(result["actions"]) == 7
        assert "Deployed template files" in result["actions"]
        assert "Copied command files" in result["actions"]
        assert "Copied guide files" in result["actions"]
        assert "Generated principles files" in result["actions"]
        assert "Setup agents directory" in result["actions"]
        assert "Setup skills directory" in result["actions"]
        assert "Setup ~/.claude/ symlinks for universal agents" in result["actions"]

    @patch("claudecodeoptimizer.core.knowledge_setup._setup_claude_home_links")
    @patch("claudecodeoptimizer.core.knowledge_setup._setup_skills")
    @patch("claudecodeoptimizer.core.knowledge_setup._setup_agents")
    @patch("claudecodeoptimizer.core.knowledge_setup._setup_principles")
    @patch("claudecodeoptimizer.core.knowledge_setup._setup_guides")
    @patch("claudecodeoptimizer.core.knowledge_setup._setup_commands")
    @patch("claudecodeoptimizer.core.knowledge_setup._setup_templates")
    @patch("claudecodeoptimizer.config.get_skills_dir")
    @patch("claudecodeoptimizer.config.get_agents_dir")
    @patch("claudecodeoptimizer.config.get_principles_dir")
    @patch("claudecodeoptimizer.config.get_guides_dir")
    @patch("claudecodeoptimizer.config.get_global_commands_dir")
    @patch("claudecodeoptimizer.config.get_templates_dir")
    @patch("claudecodeoptimizer.config.get_global_dir")
    def test_setup_force_parameter_ignored(
        self,
        mock_global_dir: Mock,
        mock_templates_dir: Mock,
        mock_commands_dir: Mock,
        mock_guides_dir: Mock,
        mock_principles_dir: Mock,
        mock_agents_dir: Mock,
        mock_skills_dir: Mock,
        mock_setup_templates: Mock,
        mock_setup_commands: Mock,
        mock_setup_guides: Mock,
        mock_setup_principles: Mock,
        mock_setup_agents: Mock,
        mock_setup_skills: Mock,
        mock_setup_claude_home_links: Mock,
    ) -> None:
        """Test that force parameter is accepted but always regenerates"""
        global_dir_path = MagicMock(spec=Path)
        mock_global_dir.return_value = global_dir_path
        mock_templates_dir.return_value = MagicMock(spec=Path)
        mock_commands_dir.return_value = MagicMock(spec=Path)
        mock_guides_dir.return_value = MagicMock(spec=Path)
        mock_principles_dir.return_value = MagicMock(spec=Path)
        mock_agents_dir.return_value = MagicMock(spec=Path)
        mock_skills_dir.return_value = MagicMock(spec=Path)

        # Execute with force=True
        result = knowledge_setup.setup_global_knowledge(force=True)

        # Should still call all setup functions
        mock_setup_templates.assert_called_once()
        mock_setup_commands.assert_called_once()
        mock_setup_guides.assert_called_once()
        mock_setup_principles.assert_called_once()
        mock_setup_agents.assert_called_once()
        mock_setup_skills.assert_called_once()
        mock_setup_claude_home_links.assert_called_once()
        assert result["success"] is True


class TestSetupTemplates:
    """Test _setup_templates function"""

    @patch("shutil.copy2")
    @patch("shutil.rmtree")
    def test_setup_templates_copies_files(
        self, mock_rmtree: Mock, mock_copy2: Mock, tmp_path: Path
    ) -> None:
        """Test that templates are copied and .template extension removed"""
        # Create mock source templates
        package_dir = Path(__file__).parent.parent.parent / "claudecodeoptimizer"
        source_templates = package_dir.parent / "templates"

        templates_dir = tmp_path / "templates"

        # Mock the source templates to exist
        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "glob") as mock_glob:
                # Mock template files
                mock_template = MagicMock(spec=Path)
                mock_template.name = "CLAUDE.md.template"
                mock_glob.return_value = [mock_template]

                # Execute
                knowledge_setup._setup_templates(templates_dir)

                # Verify directory cleanup
                mock_rmtree.assert_called_once_with(templates_dir)

                # Verify file copied with .template removed
                expected_dest = templates_dir / "CLAUDE.md"
                mock_copy2.assert_called_once_with(mock_template, expected_dest)

    @patch("shutil.copy2")
    @patch("shutil.rmtree")
    def test_setup_templates_removes_existing_directory(
        self, mock_rmtree: Mock, mock_copy2: Mock, tmp_path: Path
    ) -> None:
        """Test that existing templates directory is removed"""
        templates_dir = tmp_path / "templates"
        templates_dir.mkdir(parents=True)
        (templates_dir / "old_file.md").touch()

        package_dir = Path(__file__).parent.parent.parent / "claudecodeoptimizer"
        source_templates = package_dir.parent / "templates"

        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "glob", return_value=[]):
                knowledge_setup._setup_templates(templates_dir)

                # Verify rmtree called before copying
                mock_rmtree.assert_called_once_with(templates_dir)

    def test_setup_templates_raises_if_source_not_found(self, tmp_path: Path) -> None:
        """Test that FileNotFoundError raised if source templates not found"""
        templates_dir = tmp_path / "templates"

        with patch.object(Path, "exists", return_value=False):
            with pytest.raises(FileNotFoundError, match="Template directory not found"):
                knowledge_setup._setup_templates(templates_dir)

    @patch("shutil.copy2")
    @patch("shutil.rmtree")
    def test_setup_templates_handles_multiple_files(
        self, mock_rmtree: Mock, mock_copy2: Mock, tmp_path: Path
    ) -> None:
        """Test copying multiple template files"""
        templates_dir = tmp_path / "templates"

        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "glob") as mock_glob:
                # Mock multiple template files
                mock_templates = [MagicMock(spec=Path, name=f"file{i}.template") for i in range(3)]
                for i, mock_template in enumerate(mock_templates):
                    mock_template.name = f"file{i}.template"
                mock_glob.return_value = mock_templates

                knowledge_setup._setup_templates(templates_dir)

                # Verify all files copied
                assert mock_copy2.call_count == 3


class TestSetupPrinciples:
    """Test _setup_principles function"""

    @patch("shutil.copy2")
    @patch("shutil.rmtree")
    def test_setup_principles_copies_files(
        self, mock_rmtree: Mock, mock_copy2: Mock, tmp_path: Path
    ) -> None:
        """Test that principles are copied from content directory"""
        principles_dir = tmp_path / "principles"

        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "glob") as mock_glob:
                # Mock principle files
                mock_principle = MagicMock(spec=Path)
                mock_principle.name = "U_ATOMIC_COMMITS.md"
                mock_glob.return_value = [mock_principle]

                knowledge_setup._setup_principles(principles_dir)

                # Verify directory cleanup
                mock_rmtree.assert_called_once_with(principles_dir)

                # Verify file copied
                expected_dest = principles_dir / "U_ATOMIC_COMMITS.md"
                mock_copy2.assert_called_once_with(mock_principle, expected_dest)

    def test_setup_principles_raises_if_source_not_found(self, tmp_path: Path) -> None:
        """Test that FileNotFoundError raised if source principles not found"""
        principles_dir = tmp_path / "principles"

        with patch.object(Path, "exists", return_value=False):
            with pytest.raises(FileNotFoundError, match="Content principles not found"):
                knowledge_setup._setup_principles(principles_dir)

    @patch("shutil.copy2")
    @patch("shutil.rmtree")
    def test_setup_principles_handles_universal_and_project(
        self, mock_rmtree: Mock, mock_copy2: Mock, tmp_path: Path
    ) -> None:
        """Test copying both U and P prefixed principles"""
        principles_dir = tmp_path / "principles"

        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "glob") as mock_glob:
                mock_principles = [
                    MagicMock(spec=Path, name="U_TEST.md"),
                    MagicMock(spec=Path, name="P_TEST.md"),
                ]
                for mock_principle in mock_principles:
                    pass  # name already set
                mock_glob.return_value = mock_principles

                knowledge_setup._setup_principles(principles_dir)

                assert mock_copy2.call_count == 2


class TestSetupCommands:
    """Test _setup_commands function"""

    @patch("shutil.copy2")
    @patch("shutil.rmtree")
    def test_setup_commands_copies_files(
        self, mock_rmtree: Mock, mock_copy2: Mock, tmp_path: Path
    ) -> None:
        """Test that commands are copied from content directory"""
        commands_dir = tmp_path / "commands"

        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "glob") as mock_glob:
                mock_command = MagicMock(spec=Path)
                mock_command.name = "cco-audit.md"
                mock_glob.return_value = [mock_command]

                knowledge_setup._setup_commands(commands_dir)

                mock_rmtree.assert_called_once_with(commands_dir)

                expected_dest = commands_dir / "cco-audit.md"
                mock_copy2.assert_called_once_with(mock_command, expected_dest)

    def test_setup_commands_raises_if_source_not_found(self, tmp_path: Path) -> None:
        """Test that FileNotFoundError raised if source commands not found"""
        commands_dir = tmp_path / "commands"

        with patch.object(Path, "exists", return_value=False):
            with pytest.raises(FileNotFoundError, match="Content commands not found"):
                knowledge_setup._setup_commands(commands_dir)


class TestSetupGuides:
    """Test _setup_guides function"""

    @patch("shutil.copy2")
    @patch("shutil.rmtree")
    def test_setup_guides_copies_files(
        self, mock_rmtree: Mock, mock_copy2: Mock, tmp_path: Path
    ) -> None:
        """Test that guides are copied from content directory"""
        guides_dir = tmp_path / "guides"

        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "glob") as mock_glob:
                mock_guide = MagicMock(spec=Path)
                mock_guide.name = "cco-security-response.md"
                mock_glob.return_value = [mock_guide]

                knowledge_setup._setup_guides(guides_dir)

                mock_rmtree.assert_called_once_with(guides_dir)

                expected_dest = guides_dir / "cco-security-response.md"
                mock_copy2.assert_called_once_with(mock_guide, expected_dest)

    def test_setup_guides_raises_if_source_not_found(self, tmp_path: Path) -> None:
        """Test that FileNotFoundError raised if source guides not found"""
        guides_dir = tmp_path / "guides"

        with patch.object(Path, "exists", return_value=False):
            with pytest.raises(FileNotFoundError, match="Content guides not found"):
                knowledge_setup._setup_guides(guides_dir)


class TestSetupAgents:
    """Test _setup_agents function"""

    @patch("shutil.copy2")
    @patch("shutil.rmtree")
    def test_setup_agents_copies_files(
        self, mock_rmtree: Mock, mock_copy2: Mock, tmp_path: Path
    ) -> None:
        """Test that agents are copied from content directory"""
        agents_dir = tmp_path / "agents"

        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "glob") as mock_glob:
                mock_agent = MagicMock(spec=Path)
                mock_agent.name = "cco-agent-audit.md"
                mock_glob.return_value = [mock_agent]

                knowledge_setup._setup_agents(agents_dir)

                mock_rmtree.assert_called_once_with(agents_dir)

                expected_dest = agents_dir / "cco-agent-audit.md"
                mock_copy2.assert_called_once_with(mock_agent, expected_dest)

    def test_setup_agents_raises_if_source_not_found(self, tmp_path: Path) -> None:
        """Test that FileNotFoundError raised if source agents not found"""
        agents_dir = tmp_path / "agents"

        with patch.object(Path, "exists", return_value=False):
            with pytest.raises(FileNotFoundError, match="Content agents not found"):
                knowledge_setup._setup_agents(agents_dir)

    @patch("shutil.copy2")
    @patch("shutil.rmtree")
    def test_setup_agents_copies_templates_and_readme(
        self, mock_rmtree: Mock, mock_copy2: Mock, tmp_path: Path
    ) -> None:
        """Test that both templates and README are copied"""
        agents_dir = tmp_path / "agents"

        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "glob") as mock_glob:
                mock_agents = [
                    MagicMock(spec=Path, name="_template.md"),
                    MagicMock(spec=Path, name="README.md"),
                    MagicMock(spec=Path, name="cco-agent-audit.md"),
                ]
                for mock_agent in mock_agents:
                    pass  # name already set
                mock_glob.return_value = mock_agents

                knowledge_setup._setup_agents(agents_dir)

                # All files should be copied including templates and README
                assert mock_copy2.call_count == 3


class TestSetupSkills:
    """Test _setup_skills function"""

    @patch("shutil.copy2")
    @patch("shutil.rmtree")
    def test_setup_skills_copies_root_files(
        self, mock_rmtree: Mock, mock_copy2: Mock, tmp_path: Path
    ) -> None:
        """Test that skills are copied from content directory root"""
        skills_dir = tmp_path / "skills"

        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "glob") as mock_glob:
                with patch.object(Path, "iterdir", return_value=[]):
                    mock_skill = MagicMock(spec=Path)
                    mock_skill.name = "cco-skill-verification-protocol.md"
                    mock_glob.return_value = [mock_skill]

                    knowledge_setup._setup_skills(skills_dir)

                    mock_rmtree.assert_called_once_with(skills_dir)

                    expected_dest = skills_dir / "cco-skill-verification-protocol.md"
                    mock_copy2.assert_called_once_with(mock_skill, expected_dest)

    @patch("shutil.copy2")
    @patch("shutil.rmtree")
    def test_setup_skills_copies_language_subdirectories(
        self, mock_rmtree: Mock, mock_copy2: Mock, tmp_path: Path
    ) -> None:
        """Test that language-specific skills are copied from subdirectories"""
        skills_dir = tmp_path / "skills"

        with patch.object(Path, "exists", return_value=True):
            # Mock root .md files
            with patch.object(Path, "glob") as mock_glob:
                mock_glob.return_value = []  # No root files

                # Mock language subdirectories
                mock_python_dir = MagicMock(spec=Path)
                mock_python_dir.name = "python"
                mock_python_dir.is_dir.return_value = True

                with patch.object(Path, "iterdir", return_value=[mock_python_dir]):
                    # Mock Python skills
                    mock_python_skill = MagicMock(spec=Path)
                    mock_python_skill.name = "cco-skill-async-patterns.md"
                    mock_python_dir.glob.return_value = [mock_python_skill]

                    knowledge_setup._setup_skills(skills_dir)

                    # Verify subdirectory created
                    # Verify file copied
                    assert mock_copy2.call_count >= 1

    @patch("shutil.copy2")
    @patch("shutil.rmtree")
    def test_setup_skills_skips_private_directories(
        self, mock_rmtree: Mock, mock_copy2: Mock, tmp_path: Path
    ) -> None:
        """Test that directories starting with _ or . are skipped"""
        skills_dir = tmp_path / "skills"

        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "glob") as mock_glob:
                mock_glob.return_value = []

                # Mock private directories
                mock_pycache = MagicMock(spec=Path)
                mock_pycache.name = "__pycache__"
                mock_pycache.is_dir.return_value = True

                mock_hidden = MagicMock(spec=Path)
                mock_hidden.name = ".hidden"
                mock_hidden.is_dir.return_value = True

                with patch.object(Path, "iterdir", return_value=[mock_pycache, mock_hidden]):
                    knowledge_setup._setup_skills(skills_dir)

                    # Neither directory should be processed
                    mock_pycache.glob.assert_not_called()
                    mock_hidden.glob.assert_not_called()

    def test_setup_skills_raises_if_source_not_found(self, tmp_path: Path) -> None:
        """Test that FileNotFoundError raised if source skills not found"""
        skills_dir = tmp_path / "skills"

        with patch.object(Path, "exists", return_value=False):
            with pytest.raises(FileNotFoundError, match="Content skills not found"):
                knowledge_setup._setup_skills(skills_dir)


@pytest.mark.skip(reason="Old behavior - now only copies commands, not agents")
class TestSetupClaudeHomeLinks:
    """Test _setup_claude_home_links function"""

    @patch("shutil.copy2")
    @patch("platform.system", return_value="Linux")
    @patch("claudecodeoptimizer.config.get_agents_dir")
    @patch("claudecodeoptimizer.config.get_claude_dir")
    def test_setup_claude_home_links_creates_symlinks_unix(
        self,
        mock_claude_dir: Mock,
        mock_agents_dir: Mock,
        mock_platform: Mock,
        mock_copy2: Mock,
        tmp_path: Path,
    ) -> None:
        """Test that symlinks are created on Unix systems"""
        claude_dir = tmp_path / ".claude"
        agents_dir = tmp_path / ".cco" / "agents"
        agents_dir.mkdir(parents=True)

        # Create test agent file
        agent_file = agents_dir / "test-agent.md"
        agent_file.write_text("test content")

        mock_claude_dir.return_value = claude_dir
        mock_agents_dir.return_value = agents_dir

        # Execute
        knowledge_setup._setup_claude_home_links()

        # Verify symlink created
        target = claude_dir / "agents" / "test-agent.md"
        assert target.is_symlink()
        assert target.resolve() == agent_file.resolve()

    @patch("subprocess.run")
    @patch("platform.system", return_value="Windows")
    @patch("claudecodeoptimizer.config.get_agents_dir")
    @patch("claudecodeoptimizer.config.get_claude_dir")
    def test_setup_claude_home_links_creates_symlinks_windows(
        self,
        mock_claude_dir: Mock,
        mock_agents_dir: Mock,
        mock_platform: Mock,
        mock_subprocess: Mock,
        tmp_path: Path,
    ) -> None:
        """Test that mklink is used on Windows systems"""
        claude_dir = tmp_path / ".claude"
        agents_dir = tmp_path / ".cco" / "agents"
        agents_dir.mkdir(parents=True)

        agent_file = agents_dir / "test-agent.md"
        agent_file.write_text("test content")

        mock_claude_dir.return_value = claude_dir
        mock_agents_dir.return_value = agents_dir

        knowledge_setup._setup_claude_home_links()

        # Verify mklink command called
        mock_subprocess.assert_called_once()
        call_args = mock_subprocess.call_args[0][0]
        assert call_args[0] == "cmd"
        assert call_args[1] == "/c"
        assert call_args[2] == "mklink"

    @patch("claudecodeoptimizer.config.get_agents_dir")
    @patch("claudecodeoptimizer.config.get_claude_dir")
    def test_setup_claude_home_links_skips_if_no_agents(
        self, mock_claude_dir: Mock, mock_agents_dir: Mock, tmp_path: Path
    ) -> None:
        """Test that function returns early if agents directory doesn't exist"""
        claude_dir = tmp_path / ".claude"
        agents_dir = tmp_path / ".cco" / "agents"  # Not created

        mock_claude_dir.return_value = claude_dir
        mock_agents_dir.return_value = agents_dir

        # Should not raise, just return
        knowledge_setup._setup_claude_home_links()

        # Claude agents dir should not be created
        assert not (claude_dir / "agents").exists()

    @patch("claudecodeoptimizer.config.get_agents_dir")
    @patch("claudecodeoptimizer.config.get_claude_dir")
    def test_setup_claude_home_links_skips_templates_and_readme(
        self, mock_claude_dir: Mock, mock_agents_dir: Mock, tmp_path: Path
    ) -> None:
        """Test that template files and README are not linked"""
        claude_dir = tmp_path / ".claude"
        agents_dir = tmp_path / ".cco" / "agents"
        agents_dir.mkdir(parents=True)

        # Create files that should be skipped
        (agents_dir / "_template.md").write_text("template")
        (agents_dir / "README.md").write_text("readme")
        (agents_dir / "real-agent.md").write_text("agent")

        mock_claude_dir.return_value = claude_dir
        mock_agents_dir.return_value = agents_dir

        knowledge_setup._setup_claude_home_links()

        claude_agents_dir = claude_dir / "agents"
        assert not (claude_agents_dir / "_template.md").exists()
        assert not (claude_agents_dir / "README.md").exists()
        assert (claude_agents_dir / "real-agent.md").exists()

    @patch("platform.system", return_value="Linux")
    @patch("claudecodeoptimizer.config.get_agents_dir")
    @patch("claudecodeoptimizer.config.get_claude_dir")
    def test_setup_claude_home_links_validates_source_paths(
        self, mock_claude_dir: Mock, mock_agents_dir: Mock, mock_platform: Mock, tmp_path: Path
    ) -> None:
        """Test that path traversal validation prevents malicious source paths"""
        claude_dir = tmp_path / ".claude"
        agents_dir = tmp_path / ".cco" / "agents"
        agents_dir.mkdir(parents=True)

        # Create normal agent file
        agent_file = agents_dir / "normal-agent.md"
        agent_file.write_text("content")

        mock_claude_dir.return_value = claude_dir
        mock_agents_dir.return_value = agents_dir

        # Mock resolve to simulate path traversal attempt on source
        original_resolve = Path.resolve

        def mock_resolve(self: Path, strict: bool = False) -> Path:
            # If this is the source file being validated
            if "normal-agent" in str(self) and ".cco" in str(self):
                # Simulate a file that resolves outside the expected directory
                return tmp_path / "outside" / "normal-agent.md"
            return original_resolve(self, strict)

        with patch.object(Path, "resolve", mock_resolve):
            knowledge_setup._setup_claude_home_links()

            # File should not be linked due to path validation
            claude_agents_dir = claude_dir / "agents"
            # The directory gets created but file is skipped
            assert not (claude_agents_dir / "normal-agent.md").exists()

    @patch("platform.system", return_value="Linux")
    @patch("claudecodeoptimizer.config.get_agents_dir")
    @patch("claudecodeoptimizer.config.get_claude_dir")
    def test_setup_claude_home_links_validates_target_paths(
        self, mock_claude_dir: Mock, mock_agents_dir: Mock, mock_platform: Mock, tmp_path: Path
    ) -> None:
        """Test that path traversal validation prevents malicious target paths"""
        claude_dir = tmp_path / ".claude"
        agents_dir = tmp_path / ".cco" / "agents"
        agents_dir.mkdir(parents=True)

        # Create normal agent file
        agent_file = agents_dir / "normal-agent.md"
        agent_file.write_text("content")

        mock_claude_dir.return_value = claude_dir
        mock_agents_dir.return_value = agents_dir

        # Mock resolve to simulate path traversal attempt on target
        original_resolve = Path.resolve

        def mock_resolve(self: Path, strict: bool = False) -> Path:
            # If this is the target file being validated
            if "normal-agent" in str(self) and ".claude" in str(self):
                # Simulate a target that resolves outside the expected directory
                return tmp_path / "outside" / "normal-agent.md"
            return original_resolve(self, strict)

        with patch.object(Path, "resolve", mock_resolve):
            knowledge_setup._setup_claude_home_links()

            # File should not be linked due to path validation
            claude_agents_dir = claude_dir / "agents"
            # The directory gets created but file is skipped
            assert not (claude_agents_dir / "normal-agent.md").exists()

    @patch("platform.system", return_value="Linux")
    @patch("claudecodeoptimizer.config.get_agents_dir")
    @patch("claudecodeoptimizer.config.get_claude_dir")
    def test_setup_claude_home_links_replaces_existing(
        self,
        mock_claude_dir: Mock,
        mock_agents_dir: Mock,
        mock_platform: Mock,
        tmp_path: Path,
    ) -> None:
        """Test that existing symlinks are replaced"""
        claude_dir = tmp_path / ".claude"
        claude_agents_dir = claude_dir / "agents"
        claude_agents_dir.mkdir(parents=True)

        agents_dir = tmp_path / ".cco" / "agents"
        agents_dir.mkdir(parents=True)

        agent_file = agents_dir / "test-agent.md"
        agent_file.write_text("new content")

        # Create existing file (not symlink to avoid platform issues)
        existing_link = claude_agents_dir / "test-agent.md"
        existing_link.write_text("old content")

        mock_claude_dir.return_value = claude_dir
        mock_agents_dir.return_value = agents_dir

        knowledge_setup._setup_claude_home_links()

        # Symlink should point to new target
        assert existing_link.is_symlink()
        assert existing_link.resolve() == agent_file.resolve()

    @patch("shutil.copy2")
    @patch("platform.system", return_value="Windows")
    @patch("subprocess.run", side_effect=Exception("mklink failed"))
    @patch("claudecodeoptimizer.config.get_agents_dir")
    @patch("claudecodeoptimizer.config.get_claude_dir")
    def test_setup_claude_home_links_fallback_to_copy(
        self,
        mock_claude_dir: Mock,
        mock_agents_dir: Mock,
        mock_subprocess: Mock,
        mock_platform: Mock,
        mock_copy2: Mock,
        tmp_path: Path,
    ) -> None:
        """Test that if symlink fails, file is copied instead"""
        claude_dir = tmp_path / ".claude"
        agents_dir = tmp_path / ".cco" / "agents"
        agents_dir.mkdir(parents=True)

        agent_file = agents_dir / "test-agent.md"
        agent_file.write_text("content")

        mock_claude_dir.return_value = claude_dir
        mock_agents_dir.return_value = agents_dir

        knowledge_setup._setup_claude_home_links()

        # Should fall back to copy
        mock_copy2.assert_called_once()


class TestGetPrincipleCategories:
    """Test get_principle_categories function"""

    @patch("claudecodeoptimizer.config.get_principles_dir")
    def test_get_principle_categories_returns_empty_if_not_exists(
        self, mock_principles_dir: Mock
    ) -> None:
        """Test returns empty list if principles directory doesn't exist"""
        mock_dir = MagicMock(spec=Path)
        mock_dir.exists.return_value = False
        mock_principles_dir.return_value = mock_dir

        result = knowledge_setup.get_principle_categories()

        assert result == []

    @patch("claudecodeoptimizer.config.get_principles_dir")
    def test_get_principle_categories_extracts_categories(
        self, mock_principles_dir: Mock, tmp_path: Path
    ) -> None:
        """Test that categories are extracted from principle files"""
        principles_dir = tmp_path / "principles"
        principles_dir.mkdir()

        # Create principle files with categories
        p1 = principles_dir / "P_TEST1.md"
        p1.write_text("---\ncategory: code_quality\n---\nContent")

        p2 = principles_dir / "P_TEST2.md"
        p2.write_text("---\ncategory: security_privacy\n---\nContent")

        mock_principles_dir.return_value = principles_dir

        result = knowledge_setup.get_principle_categories()

        assert sorted(result) == ["code_quality", "security_privacy"]

    @patch("claudecodeoptimizer.config.get_principles_dir")
    def test_get_principle_categories_deduplicates(
        self, mock_principles_dir: Mock, tmp_path: Path
    ) -> None:
        """Test that duplicate categories are removed"""
        principles_dir = tmp_path / "principles"
        principles_dir.mkdir()

        # Create multiple files with same category
        for i in range(3):
            p = principles_dir / f"P_TEST{i}.md"
            p.write_text("---\ncategory: testing\n---\nContent")

        mock_principles_dir.return_value = principles_dir

        result = knowledge_setup.get_principle_categories()

        assert result == ["testing"]

    @patch("claudecodeoptimizer.config.get_principles_dir")
    def test_get_principle_categories_handles_malformed_files(
        self, mock_principles_dir: Mock, tmp_path: Path
    ) -> None:
        """Test that malformed files are skipped without error"""
        principles_dir = tmp_path / "principles"
        principles_dir.mkdir()

        # Create valid file
        p1 = principles_dir / "P_GOOD.md"
        p1.write_text("---\ncategory: good\n---\nContent")

        # Create malformed file (no category)
        p2 = principles_dir / "P_BAD.md"
        p2.write_text("No frontmatter here")

        mock_principles_dir.return_value = principles_dir

        result = knowledge_setup.get_principle_categories()

        assert result == ["good"]

    @patch("claudecodeoptimizer.config.get_principles_dir")
    def test_get_principle_categories_returns_sorted(
        self, mock_principles_dir: Mock, tmp_path: Path
    ) -> None:
        """Test that categories are returned in sorted order"""
        principles_dir = tmp_path / "principles"
        principles_dir.mkdir()

        # Create files with categories in non-alphabetical order
        categories = ["zebra", "apple", "middle"]
        for i, cat in enumerate(categories):
            p = principles_dir / f"P_TEST{i}.md"
            p.write_text(f"---\ncategory: {cat}\n---\nContent")

        mock_principles_dir.return_value = principles_dir

        result = knowledge_setup.get_principle_categories()

        assert result == ["apple", "middle", "zebra"]


class TestGetAvailableCommands:
    """Test get_available_commands function"""

    @patch("claudecodeoptimizer.config.get_global_commands_dir")
    def test_get_available_commands_returns_empty_if_not_exists(
        self, mock_commands_dir: Mock
    ) -> None:
        """Test returns empty list if commands directory doesn't exist"""
        mock_dir = MagicMock(spec=Path)
        mock_dir.exists.return_value = False
        mock_commands_dir.return_value = mock_dir

        result = knowledge_setup.get_available_commands()

        assert result == []

    @patch("claudecodeoptimizer.config.get_global_commands_dir")
    def test_get_available_commands_returns_filenames_without_extension(
        self, mock_commands_dir: Mock, tmp_path: Path
    ) -> None:
        """Test that command filenames are returned without .md extension"""
        commands_dir = tmp_path / "commands"
        commands_dir.mkdir()

        (commands_dir / "cco-audit.md").touch()
        (commands_dir / "cco-fix.md").touch()
        (commands_dir / "cco-test.md").touch()

        mock_commands_dir.return_value = commands_dir

        result = knowledge_setup.get_available_commands()

        assert sorted(result) == ["cco-audit", "cco-fix", "cco-test"]


class TestGetAvailableGuides:
    """Test get_available_guides function"""

    @patch("claudecodeoptimizer.config.get_guides_dir")
    def test_get_available_guides_returns_empty_if_not_exists(self, mock_guides_dir: Mock) -> None:
        """Test returns empty list if guides directory doesn't exist"""
        mock_dir = MagicMock(spec=Path)
        mock_dir.exists.return_value = False
        mock_guides_dir.return_value = mock_dir

        result = knowledge_setup.get_available_guides()

        assert result == []

    @patch("claudecodeoptimizer.config.get_guides_dir")
    def test_get_available_guides_returns_filenames_without_extension(
        self, mock_guides_dir: Mock, tmp_path: Path
    ) -> None:
        """Test that guide filenames are returned without .md extension"""
        guides_dir = tmp_path / "guides"
        guides_dir.mkdir()

        (guides_dir / "cco-security-response.md").touch()
        (guides_dir / "cco-git-workflow.md").touch()

        mock_guides_dir.return_value = guides_dir

        result = knowledge_setup.get_available_guides()

        assert sorted(result) == ["cco-git-workflow", "cco-security-response"]


class TestGetAvailableAgents:
    """Test get_available_agents function"""

    @patch("claudecodeoptimizer.config.get_agents_dir")
    def test_get_available_agents_returns_empty_if_not_exists(self, mock_agents_dir: Mock) -> None:
        """Test returns empty list if agents directory doesn't exist"""
        mock_dir = MagicMock(spec=Path)
        mock_dir.exists.return_value = False
        mock_agents_dir.return_value = mock_dir

        result = knowledge_setup.get_available_agents()

        assert result == []

    @patch("claudecodeoptimizer.config.get_agents_dir")
    def test_get_available_agents_excludes_templates_and_readme(
        self, mock_agents_dir: Mock, tmp_path: Path
    ) -> None:
        """Test that templates and README are excluded from results"""
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()

        (agents_dir / "cco-agent-audit.md").touch()
        (agents_dir / "cco-agent-fix.md").touch()
        (agents_dir / "_template.md").touch()
        (agents_dir / "README.md").touch()

        mock_agents_dir.return_value = agents_dir

        result = knowledge_setup.get_available_agents()

        assert sorted(result) == ["cco-agent-audit", "cco-agent-fix"]


class TestGetAvailableSkills:
    """Test get_available_skills function"""

    @patch("claudecodeoptimizer.config.get_skills_dir")
    def test_get_available_skills_returns_empty_if_not_exists(self, mock_skills_dir: Mock) -> None:
        """Test returns empty list if skills directory doesn't exist"""
        mock_dir = MagicMock(spec=Path)
        mock_dir.exists.return_value = False
        mock_skills_dir.return_value = mock_dir

        result = knowledge_setup.get_available_skills()

        assert result == []

    @patch("claudecodeoptimizer.config.get_skills_dir")
    def test_get_available_skills_excludes_templates_and_readme(
        self, mock_skills_dir: Mock, tmp_path: Path
    ) -> None:
        """Test that templates and README are excluded from results"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        (skills_dir / "cco-skill-verification-protocol.md").touch()
        (skills_dir / "test-first.md").touch()
        (skills_dir / "_template.md").touch()
        (skills_dir / "README.md").touch()

        mock_skills_dir.return_value = skills_dir

        result = knowledge_setup.get_available_skills()

        assert sorted(result) == ["cco-skill-verification-protocol", "test-first"]


class TestErrorHandling:
    """Test error handling across all functions"""

    @patch("claudecodeoptimizer.config.get_principles_dir")
    def test_get_principle_categories_handles_read_errors(
        self, mock_principles_dir: Mock, tmp_path: Path
    ) -> None:
        """Test that files that can't be read are skipped"""
        principles_dir = tmp_path / "principles"
        principles_dir.mkdir()

        # Create a valid file
        good_file = principles_dir / "P_GOOD.md"
        good_file.write_text("---\ncategory: valid\n---\n")

        # Create a file that will cause read error
        bad_file = principles_dir / "P_BAD.md"
        bad_file.write_text("content")

        mock_principles_dir.return_value = principles_dir

        # Mock read_text to fail for bad file
        original_read_text = Path.read_text

        def mock_read_text(self: Path, *args: Any, **kwargs: Any) -> str:  # noqa: ANN401
            if "BAD" in str(self):
                raise PermissionError("Cannot read")
            return original_read_text(self, *args, **kwargs)

        with patch.object(Path, "read_text", mock_read_text):
            result = knowledge_setup.get_principle_categories()

            # Should only include the valid category
            assert result == ["valid"]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
