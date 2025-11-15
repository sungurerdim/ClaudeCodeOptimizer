"""
Comprehensive tests for core generator module.

Tests cover:
- CommandGenerator initialization
- Project configuration loading
- Command registry loading
- Template variable replacement
- Template finding
- Command generation
- Batch command generation
- Error handling

Target Coverage: 100%
"""

import json
from datetime import datetime
from pathlib import Path

import pytest

from claudecodeoptimizer.core.generator import CommandGenerator


class TestCommandGeneratorInit:
    """Test CommandGenerator initialization"""

    def test_init_with_path(self, temp_dir):
        """Test initialization with a path"""
        generator = CommandGenerator(temp_dir)

        assert generator.project_root == temp_dir.absolute()
        assert generator.templates_dir.name == "templates"

    def test_init_converts_to_absolute(self, temp_dir):
        """Test that project_root is converted to absolute path"""
        # Create a relative path
        relative_path = Path(".")
        generator = CommandGenerator(relative_path)

        assert generator.project_root.is_absolute()

    def test_templates_dir_path(self, temp_dir):
        """Test templates directory path is correct"""
        generator = CommandGenerator(temp_dir)

        # templates_dir should be sibling to generator.py
        assert generator.templates_dir.parent.name == "claudecodeoptimizer"
        assert generator.templates_dir.name == "templates"


class TestLoadProjectConfig:
    """Test load_project_config method"""

    def test_load_valid_config(self, temp_dir):
        """Test loading valid project configuration"""
        # Setup
        generator = CommandGenerator(temp_dir)
        claude_dir = temp_dir / ".claude"
        claude_dir.mkdir(parents=True)

        config_data = {
            "project": {"name": "TestProject", "type": "web_app"},
            "language": {"primary": "python"},
        }

        config_file = claude_dir / "project.json"
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config_data, f)

        # Execute
        result = generator.load_project_config()

        # Assert
        assert result == config_data
        assert result["project"]["name"] == "TestProject"
        assert result["language"]["primary"] == "python"

    def test_load_config_file_not_found(self, temp_dir):
        """Test FileNotFoundError when config doesn't exist"""
        generator = CommandGenerator(temp_dir)

        with pytest.raises(FileNotFoundError) as exc_info:
            generator.load_project_config()

        assert "Project config not found" in str(exc_info.value)

    def test_load_config_invalid_json(self, temp_dir):
        """Test handling of invalid JSON in config file"""
        # Setup
        generator = CommandGenerator(temp_dir)
        claude_dir = temp_dir / ".claude"
        claude_dir.mkdir(parents=True)

        config_file = claude_dir / "project.json"
        with open(config_file, "w", encoding="utf-8") as f:
            f.write("invalid json {")

        # Execute & Assert
        with pytest.raises(json.JSONDecodeError):
            generator.load_project_config()

    def test_load_config_empty_file(self, temp_dir):
        """Test loading empty config file"""
        # Setup
        generator = CommandGenerator(temp_dir)
        claude_dir = temp_dir / ".claude"
        claude_dir.mkdir(parents=True)

        config_file = claude_dir / "project.json"
        with open(config_file, "w", encoding="utf-8") as f:
            f.write("{}")

        # Execute
        result = generator.load_project_config()

        # Assert
        assert result == {}


class TestLoadCommandRegistry:
    """Test load_command_registry method"""

    def test_load_enabled_commands(self, temp_dir):
        """Test loading enabled commands from registry"""
        # Setup
        generator = CommandGenerator(temp_dir)
        claude_dir = temp_dir / ".claude"
        claude_dir.mkdir(parents=True)

        registry_data = {
            "commands": [
                {"id": "cco-status", "enabled": True},
                {"id": "cco-test", "enabled": False},
                {"id": "cco-audit", "enabled": True},
            ]
        }

        registry_file = claude_dir / "commands.json"
        with open(registry_file, "w", encoding="utf-8") as f:
            json.dump(registry_data, f)

        # Execute
        result = generator.load_command_registry()

        # Assert
        assert len(result) == 2
        assert "cco-status" in result
        assert "cco-audit" in result
        assert "cco-test" not in result

    def test_load_registry_all_disabled(self, temp_dir):
        """Test loading registry with all commands disabled"""
        # Setup
        generator = CommandGenerator(temp_dir)
        claude_dir = temp_dir / ".claude"
        claude_dir.mkdir(parents=True)

        registry_data = {
            "commands": [
                {"id": "cco-status", "enabled": False},
                {"id": "cco-test", "enabled": False},
            ]
        }

        registry_file = claude_dir / "commands.json"
        with open(registry_file, "w", encoding="utf-8") as f:
            json.dump(registry_data, f)

        # Execute
        result = generator.load_command_registry()

        # Assert
        assert len(result) == 0

    def test_load_registry_missing_enabled_field(self, temp_dir):
        """Test command with missing enabled field (should default to False)"""
        # Setup
        generator = CommandGenerator(temp_dir)
        claude_dir = temp_dir / ".claude"
        claude_dir.mkdir(parents=True)

        registry_data = {
            "commands": [
                {"id": "cco-status", "enabled": True},
                {"id": "cco-test"},  # Missing enabled field
            ]
        }

        registry_file = claude_dir / "commands.json"
        with open(registry_file, "w", encoding="utf-8") as f:
            json.dump(registry_data, f)

        # Execute
        result = generator.load_command_registry()

        # Assert
        assert len(result) == 1
        assert "cco-status" in result
        assert "cco-test" not in result

    def test_load_registry_file_not_found(self, temp_dir):
        """Test FileNotFoundError when registry doesn't exist"""
        generator = CommandGenerator(temp_dir)

        with pytest.raises(FileNotFoundError) as exc_info:
            generator.load_command_registry()

        assert "Command registry not found" in str(exc_info.value)

    def test_load_registry_empty(self, temp_dir):
        """Test loading empty command registry"""
        # Setup
        generator = CommandGenerator(temp_dir)
        claude_dir = temp_dir / ".claude"
        claude_dir.mkdir(parents=True)

        registry_data = {"commands": []}

        registry_file = claude_dir / "commands.json"
        with open(registry_file, "w", encoding="utf-8") as f:
            json.dump(registry_data, f)

        # Execute
        result = generator.load_command_registry()

        # Assert
        assert len(result) == 0


class TestReplaceVariables:
    """Test replace_variables method"""

    def test_replace_basic_variables(self, temp_dir):
        """Test replacing basic project variables"""
        generator = CommandGenerator(temp_dir)

        content = "Project: ${PROJECT_NAME}, Language: ${PRIMARY_LANGUAGE}"
        project_config = {
            "project": {"name": "My Project", "type": "web_app"},
            "language": {"primary": "python"},
        }
        enabled_commands = ["cco-status"]

        result = generator.replace_variables(content, project_config, enabled_commands)

        assert "myproject" in result  # lowercase, no spaces
        assert "python" in result

    def test_replace_structure_variables(self, temp_dir):
        """Test replacing structure-related variables"""
        generator = CommandGenerator(temp_dir)

        content = "Tests: ${TESTS_DIR}, Services: ${SERVICE_DIR}"
        project_config = {
            "structure": {"tests_dir": "tests", "service_dir": "services", "shared_dir": "shared"}
        }
        enabled_commands = []

        result = generator.replace_variables(content, project_config, enabled_commands)

        assert "Tests: tests" in result
        assert "Services: services" in result

    def test_replace_tools_variables(self, temp_dir):
        """Test replacing tool-related variables"""
        generator = CommandGenerator(temp_dir)

        content = "Format: ${FORMATTER_CMD}, Lint: ${LINTER_CMD}, Type: ${TYPE_CHECKER_CMD}"
        project_config = {
            "tools": {
                "formatter": {"command": "black ."},
                "linter": {"command": "ruff check ."},
                "type_checker": {"name": "mypy", "command": "mypy ."},
            }
        }
        enabled_commands = []

        result = generator.replace_variables(content, project_config, enabled_commands)

        assert "Format: black ." in result
        assert "Lint: ruff check ." in result
        assert "Type: mypy ." in result

    def test_replace_environment_variables(self, temp_dir):
        """Test replacing environment-related variables"""
        generator = CommandGenerator(temp_dir)

        content = "OS: ${OS_TYPE}, Env: ${ENV_TYPE}"
        project_config = {"environment": {"os": "windows", "container_system": "Docker Compose"}}
        enabled_commands = []

        result = generator.replace_variables(content, project_config, enabled_commands)

        assert "OS: windows" in result
        assert "Env: docker_compose" in result  # lowercase with underscore

    def test_replace_service_list(self, temp_dir):
        """Test replacing service list variable"""
        generator = CommandGenerator(temp_dir)

        content = "Services:\n${SERVICE_LIST}"
        project_config = {"structure": {"services": ["api", "worker", "frontend"]}}
        enabled_commands = []

        result = generator.replace_variables(content, project_config, enabled_commands)

        assert "|-- api/" in result
        assert "|-- worker/" in result
        assert "|-- frontend/" in result

    def test_replace_service_list_empty(self, temp_dir):
        """Test replacing service list when no services defined"""
        generator = CommandGenerator(temp_dir)

        content = "Services:\n${SERVICE_LIST}"
        project_config = {"structure": {"services": []}}
        enabled_commands = []

        result = generator.replace_variables(content, project_config, enabled_commands)

        assert "No services defined" in result

    def test_replace_installed_commands(self, temp_dir):
        """Test replacing installed commands list"""
        generator = CommandGenerator(temp_dir)

        content = "Commands:\n${INSTALLED_COMMANDS}"
        project_config = {}
        enabled_commands = ["cco-status", "cco-test", "cco-audit"]

        result = generator.replace_variables(content, project_config, enabled_commands)

        assert "- /cco-status" in result
        assert "- /cco-test" in result
        assert "- /cco-audit" in result

    def test_replace_missing_config_values(self, temp_dir):
        """Test replacement with missing config values (should use empty strings)"""
        generator = CommandGenerator(temp_dir)

        content = "Project: ${PROJECT_NAME}, Type: ${PROJECT_TYPE}"
        project_config = {}  # Empty config
        enabled_commands = []

        result = generator.replace_variables(content, project_config, enabled_commands)

        assert "Project: , Type: " in result

    def test_replace_all_variables(self, temp_dir):
        """Test replacing all possible variables"""
        generator = CommandGenerator(temp_dir)

        content = """
        ${PROJECT_NAME}
        ${PROJECT_TYPE}
        ${PRIMARY_LANGUAGE}
        ${SERVICE_DIR}
        ${SHARED_DIR}
        ${TESTS_DIR}
        ${PRINCIPLES_COUNT}
        ${FILE_EXTENSION}
        ${FORMATTER_CMD}
        ${LINTER_CMD}
        ${TYPE_CHECKER}
        ${TYPE_CHECKER_CMD}
        ${OS_TYPE}
        ${ENV_TYPE}
        ${ACTIVATE_CMD}
        ${DEACTIVATE_CMD}
        ${CONTAINER_START}
        ${CONTAINER_STOP}
        ${CONTAINER_LOGS}
        ${FORMAT_CMD}
        ${LINT_CMD}
        ${SERVICE_LIST}
        ${INSTALLED_COMMANDS}
        """

        project_config = {
            "project": {"name": "Test Project", "type": "web_app"},
            "language": {"primary": "python", "file_extension": ".py"},
            "structure": {
                "service_dir": "services",
                "shared_dir": "shared",
                "tests_dir": "tests",
                "services": ["api"],
            },
            "cco": {"principle_count": 15},
            "tools": {
                "formatter": {"command": "black ."},
                "linter": {"command": "ruff ."},
                "type_checker": {"name": "mypy", "command": "mypy ."},
            },
            "environment": {
                "os": "linux",
                "container_system": "Docker",
                "activate_cmd": "source venv/bin/activate",
                "deactivate_cmd": "deactivate",
                "container_start": "docker-compose up",
                "container_stop": "docker-compose down",
                "container_logs": "docker-compose logs",
            },
        }
        enabled_commands = ["cco-test"]

        result = generator.replace_variables(content, project_config, enabled_commands)

        # Check all replacements occurred
        assert "${" not in result or result.count("${") == 0  # No unresolved variables


class TestFindTemplate:
    """Test find_template method"""

    def test_find_existing_template(self, temp_dir):
        """Test finding an existing template file"""
        generator = CommandGenerator(temp_dir)

        # Create a mock template file
        templates_dir = generator.templates_dir
        templates_dir.mkdir(parents=True, exist_ok=True)
        template_file = templates_dir / "cco-test.template.md"
        template_file.write_text("Test template")

        result = generator.find_template("cco-test")

        assert result == template_file
        assert result.exists()

    def test_find_template_in_subdirectory(self, temp_dir):
        """Test finding template in subdirectory"""
        generator = CommandGenerator(temp_dir)

        # Create template in subdirectory
        templates_dir = generator.templates_dir
        subdir = templates_dir / "commands"
        subdir.mkdir(parents=True, exist_ok=True)
        template_file = subdir / "cco-custom-test.template.md"
        template_file.write_text("Custom template")

        result = generator.find_template("cco-custom-test")

        assert result == template_file
        assert result.exists()

    def test_find_nonexistent_template(self, temp_dir):
        """Test finding a template that doesn't exist"""
        generator = CommandGenerator(temp_dir)

        # Ensure templates dir exists but is empty
        templates_dir = generator.templates_dir
        templates_dir.mkdir(parents=True, exist_ok=True)

        result = generator.find_template("nonexistent")

        assert result is None


class TestGenerateCommand:
    """Test generate_command method"""

    def test_generate_command_success(self, temp_dir):
        """Test successful command generation"""
        generator = CommandGenerator(temp_dir)

        # Create template
        templates_dir = generator.templates_dir
        templates_dir.mkdir(parents=True, exist_ok=True)
        template_file = templates_dir / "cco-test.template.md"
        template_file.write_text("Project: ${PROJECT_NAME}")

        # Create .claude directory
        claude_dir = temp_dir / ".claude"
        claude_dir.mkdir(parents=True)

        project_config = {"project": {"name": "Test Project"}}
        enabled_commands = ["cco-test"]

        result = generator.generate_command("cco-test", project_config, enabled_commands)

        assert result is True

        # Check output file was created
        output_file = claude_dir / "commands" / "cco-test.md"
        assert output_file.exists()

        # Check content was replaced
        content = output_file.read_text()
        assert "testproject" in content  # lowercase, no spaces

    def test_generate_command_template_not_found(self, temp_dir, capsys):
        """Test command generation when template doesn't exist"""
        generator = CommandGenerator(temp_dir)

        # Ensure templates dir exists but is empty
        templates_dir = generator.templates_dir
        templates_dir.mkdir(parents=True, exist_ok=True)

        project_config = {}
        enabled_commands = []

        result = generator.generate_command("nonexistent", project_config, enabled_commands)

        assert result is False

        # Check error message was printed
        captured = capsys.readouterr()
        assert "Template not found: nonexistent" in captured.out

    def test_generate_command_creates_commands_dir(self, temp_dir):
        """Test that commands directory is created if it doesn't exist"""
        generator = CommandGenerator(temp_dir)

        # Create template
        templates_dir = generator.templates_dir
        templates_dir.mkdir(parents=True, exist_ok=True)
        template_file = templates_dir / "cco-test.template.md"
        template_file.write_text("Test content")

        # Create .claude but not commands subdirectory
        claude_dir = temp_dir / ".claude"
        claude_dir.mkdir(parents=True)

        project_config = {}
        enabled_commands = []

        result = generator.generate_command("cco-test", project_config, enabled_commands)

        assert result is True

        # Check commands directory was created
        commands_dir = claude_dir / "commands"
        assert commands_dir.exists()
        assert commands_dir.is_dir()


class TestGenerateAll:
    """Test generate_all method"""

    def test_generate_all_success(self, temp_dir):
        """Test successful generation of all commands"""
        generator = CommandGenerator(temp_dir)

        # Setup project config
        claude_dir = temp_dir / ".claude"
        claude_dir.mkdir(parents=True)

        project_config = {"project": {"name": "Test"}}
        with open(claude_dir / "project.json", "w", encoding="utf-8") as f:
            json.dump(project_config, f)

        # Setup command registry
        registry_data = {
            "commands": [{"id": "cco-test", "enabled": True}, {"id": "cco-audit", "enabled": True}]
        }
        with open(claude_dir / "commands.json", "w", encoding="utf-8") as f:
            json.dump(registry_data, f)

        # Create templates
        templates_dir = generator.templates_dir
        templates_dir.mkdir(parents=True, exist_ok=True)
        (templates_dir / "cco-test.template.md").write_text("Test template")
        (templates_dir / "cco-audit.template.md").write_text("Audit template")

        # Execute
        result = generator.generate_all()

        # Assert
        assert result["success"] is True
        assert result["generated"] == 2
        assert result["failed"] == 0
        assert len(result["failed_commands"]) == 0

        # Check output files
        commands_dir = claude_dir / "commands"
        assert (commands_dir / "cco-test.md").exists()
        assert (commands_dir / "cco-audit.md").exists()

    def test_generate_all_partial_failure(self, temp_dir):
        """Test generation with some commands failing"""
        generator = CommandGenerator(temp_dir)

        # Setup project config
        claude_dir = temp_dir / ".claude"
        claude_dir.mkdir(parents=True)

        project_config = {"project": {"name": "Test"}}
        with open(claude_dir / "project.json", "w", encoding="utf-8") as f:
            json.dump(project_config, f)

        # Setup command registry with one missing template
        registry_data = {
            "commands": [
                {"id": "cco-test", "enabled": True},
                {"id": "cco-missing", "enabled": True},
            ]
        }
        with open(claude_dir / "commands.json", "w", encoding="utf-8") as f:
            json.dump(registry_data, f)

        # Create only one template
        templates_dir = generator.templates_dir
        templates_dir.mkdir(parents=True, exist_ok=True)
        (templates_dir / "cco-test.template.md").write_text("Test template")

        # Execute
        result = generator.generate_all()

        # Assert
        assert result["success"] is True
        assert result["generated"] == 1
        assert result["failed"] == 1
        assert "cco-missing" in result["failed_commands"]

    def test_generate_all_config_not_found(self, temp_dir):
        """Test generation when project config is missing"""
        generator = CommandGenerator(temp_dir)

        # Execute
        result = generator.generate_all()

        # Assert
        assert result["success"] is False
        assert "error" in result
        assert "Project config not found" in result["error"]

    def test_generate_all_updates_registry(self, temp_dir):
        """Test that command registry is updated with timestamps"""
        generator = CommandGenerator(temp_dir)

        # Setup project config
        claude_dir = temp_dir / ".claude"
        claude_dir.mkdir(parents=True)

        project_config = {"project": {"name": "Test"}}
        with open(claude_dir / "project.json", "w", encoding="utf-8") as f:
            json.dump(project_config, f)

        # Setup command registry
        registry_data = {"commands": [{"id": "cco-test", "enabled": True}]}
        with open(claude_dir / "commands.json", "w", encoding="utf-8") as f:
            json.dump(registry_data, f)

        # Create template
        templates_dir = generator.templates_dir
        templates_dir.mkdir(parents=True, exist_ok=True)
        (templates_dir / "cco-test.template.md").write_text("Test template")

        # Execute
        result = generator.generate_all()

        # Check registry was updated
        with open(claude_dir / "commands.json", encoding="utf-8") as f:
            updated_registry = json.load(f)

        assert "version" in updated_registry
        assert "generated_at" in updated_registry
        assert len(updated_registry["commands"]) == 1
        assert updated_registry["commands"][0]["id"] == "cco-test"
        assert updated_registry["commands"][0]["enabled"] is True
        assert "generated_at" in updated_registry["commands"][0]

        # Verify timestamp format
        timestamp = updated_registry["generated_at"]
        datetime.fromisoformat(timestamp)  # Should not raise

    def test_generate_all_no_enabled_commands(self, temp_dir):
        """Test generation when no commands are enabled"""
        generator = CommandGenerator(temp_dir)

        # Setup project config
        claude_dir = temp_dir / ".claude"
        claude_dir.mkdir(parents=True)

        project_config = {"project": {"name": "Test"}}
        with open(claude_dir / "project.json", "w", encoding="utf-8") as f:
            json.dump(project_config, f)

        # Setup empty command registry
        registry_data = {"commands": []}
        with open(claude_dir / "commands.json", "w", encoding="utf-8") as f:
            json.dump(registry_data, f)

        # Execute
        result = generator.generate_all()

        # Assert
        assert result["success"] is True
        assert result["generated"] == 0
        assert result["failed"] == 0

    def test_generate_all_exception_handling(self, temp_dir):
        """Test exception handling in generate_all"""
        generator = CommandGenerator(temp_dir)

        # Don't create any config files - should raise FileNotFoundError

        # Execute
        result = generator.generate_all()

        # Assert
        assert result["success"] is False
        assert "error" in result


class TestIntegration:
    """Integration tests for CommandGenerator"""

    def test_full_workflow(self, temp_dir):
        """Test complete workflow from config to generated commands"""
        generator = CommandGenerator(temp_dir)

        # Setup complete project structure
        claude_dir = temp_dir / ".claude"
        claude_dir.mkdir(parents=True)

        # Create comprehensive project config
        project_config = {
            "project": {"name": "Integration Test", "type": "web_app"},
            "language": {"primary": "python", "file_extension": ".py"},
            "structure": {
                "service_dir": "services",
                "tests_dir": "tests",
                "services": ["api", "worker"],
            },
            "tools": {
                "formatter": {"command": "black ."},
                "linter": {"command": "ruff check ."},
                "type_checker": {"name": "mypy", "command": "mypy ."},
            },
            "environment": {"os": "linux", "container_system": "Docker"},
            "cco": {"principle_count": 10},
        }

        with open(claude_dir / "project.json", "w", encoding="utf-8") as f:
            json.dump(project_config, f)

        # Create command registry
        registry_data = {
            "commands": [{"id": "cco-test", "enabled": True}, {"id": "cco-status", "enabled": True}]
        }

        with open(claude_dir / "commands.json", "w", encoding="utf-8") as f:
            json.dump(registry_data, f)

        # Create templates with various placeholders
        templates_dir = generator.templates_dir
        templates_dir.mkdir(parents=True, exist_ok=True)

        test_template = """
# Test Command

Project: ${PROJECT_NAME}
Type: ${PROJECT_TYPE}
Language: ${PRIMARY_LANGUAGE}
Services:
${SERVICE_LIST}

Tools:
- Formatter: ${FORMATTER_CMD}
- Linter: ${LINTER_CMD}
"""
        (templates_dir / "cco-test.template.md").write_text(test_template)

        status_template = """
# Status Command

OS: ${OS_TYPE}
Tests: ${TESTS_DIR}
"""
        (templates_dir / "cco-status.template.md").write_text(status_template)

        # Execute
        result = generator.generate_all()

        # Assert generation succeeded
        assert result["success"] is True
        assert result["generated"] == 2
        assert result["failed"] == 0

        # Verify test command content
        test_output = claude_dir / "commands" / "cco-test.md"
        assert test_output.exists()
        test_content = test_output.read_text()
        assert "integrationtest" in test_content
        assert "web_app" in test_content
        assert "python" in test_content
        assert "|-- api/" in test_content
        assert "|-- worker/" in test_content
        assert "black ." in test_content
        assert "ruff check ." in test_content

        # Verify status command content
        status_output = claude_dir / "commands" / "cco-status.md"
        assert status_output.exists()
        status_content = status_output.read_text()
        assert "linux" in status_content
        assert "tests" in status_content

        # Verify registry was updated
        with open(claude_dir / "commands.json", encoding="utf-8") as f:
            updated_registry = json.load(f)

        assert "generated_at" in updated_registry
        assert len(updated_registry["commands"]) == 2
