"""Command generator for ClaudeCodeOptimizer."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .. import config


class CommandGenerator:
    """Generates Claude Code commands from templates."""

    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root.absolute()
        self.templates_dir = Path(__file__).parent.parent / "templates"

    def load_project_config(self) -> Dict[str, Any]:
        """Load project configuration from .cco/project.json."""
        config_file = config.get_project_claude_dir(self.project_root) / "project.json"

        if not config_file.exists():
            raise FileNotFoundError(f"Project config not found: {config_file}")

        with open(config_file, encoding="utf-8") as f:
            return json.load(f)

    def load_command_registry(self) -> List[str]:
        """Load enabled commands from .cco/commands.json."""
        registry_file = config.get_project_claude_dir(self.project_root) / "commands.json"

        if not registry_file.exists():
            raise FileNotFoundError(f"Command registry not found: {registry_file}")

        with open(registry_file, encoding="utf-8") as f:
            registry = json.load(f)

        return [cmd["id"] for cmd in registry["commands"] if cmd.get("enabled", False)]

    def replace_variables(
        self,
        content: str,
        project_config: Dict[str, Any],
        enabled_commands: List[str],
    ) -> str:
        """Replace template variables with project config values."""
        replacements: Dict[str, str] = {
            "${PROJECT_NAME}": project_config.get("project", {})
            .get("name", "")
            .lower()
            .replace(" ", ""),
            "${PROJECT_TYPE}": project_config.get("project", {}).get("type", ""),
            "${PRIMARY_LANGUAGE}": project_config.get("language", {}).get("primary", ""),
            "${SERVICE_DIR}": project_config.get("structure", {}).get("service_dir", "services"),
            "${SHARED_DIR}": project_config.get("structure", {}).get("shared_dir", "shared"),
            "${TESTS_DIR}": project_config.get("structure", {}).get("tests_dir", "tests"),
            "${PRINCIPLES_COUNT}": str(project_config.get("cco", {}).get("principle_count", "10")),
            "${FILE_EXTENSION}": project_config.get("language", {}).get("file_extension", ".py"),
            "${FORMATTER_CMD}": project_config.get("tools", {})
            .get("formatter", {})
            .get("command", ""),
            "${LINTER_CMD}": project_config.get("tools", {}).get("linter", {}).get("command", ""),
            "${TYPE_CHECKER}": project_config.get("tools", {})
            .get("type_checker", {})
            .get("name", ""),
            "${TYPE_CHECKER_CMD}": project_config.get("tools", {})
            .get("type_checker", {})
            .get("command", ""),
            "${OS_TYPE}": project_config.get("environment", {}).get("os", ""),
            "${ENV_TYPE}": project_config.get("environment", {})
            .get("container_system", "")
            .lower()
            .replace(" ", "_"),
            "${ACTIVATE_CMD}": project_config.get("environment", {}).get("activate_cmd", ""),
            "${DEACTIVATE_CMD}": project_config.get("environment", {}).get("deactivate_cmd", ""),
            "${CONTAINER_START}": project_config.get("environment", {}).get("container_start", ""),
            "${CONTAINER_STOP}": project_config.get("environment", {}).get("container_stop", ""),
            "${CONTAINER_LOGS}": project_config.get("environment", {}).get("container_logs", ""),
            "${FORMAT_CMD}": project_config.get("tools", {})
            .get("formatter", {})
            .get("command", ""),
            "${LINT_CMD}": project_config.get("tools", {}).get("linter", {}).get("command", ""),
        }

        # Service list
        services = project_config.get("structure", {}).get("services", [])
        if isinstance(services, list) and services:
            service_list = "\n|   ".join([f"|-- {svc}/" for svc in services])
            replacements["${SERVICE_LIST}"] = service_list
        else:
            replacements["${SERVICE_LIST}"] = "No services defined"

        # Installed commands list
        commands_list = "\n".join([f"- /{cmd}" for cmd in enabled_commands])
        replacements["${INSTALLED_COMMANDS}"] = commands_list

        # Replace all variables
        for var, value in replacements.items():
            content = content.replace(var, str(value))

        return content

    def find_template(self, command_id: str) -> Optional[Path]:
        """Find template file for command."""
        # Search in all subdirectories
        for template_file in self.templates_dir.rglob(f"{command_id}.template.md"):
            return template_file

        return None

    def generate_command(
        self,
        command_id: str,
        project_config: Dict[str, Any],
        enabled_commands: List[str],
    ) -> bool:
        """Generate a single command from template."""
        template_path = self.find_template(command_id)

        if not template_path or not template_path.exists():
            print(f"[!] Template not found: {command_id}")
            return False

        # Read template
        with open(template_path, encoding="utf-8") as f:
            content = f.read()

        # Replace variables
        content = self.replace_variables(content, project_config, enabled_commands)

        # Write command to project-local .claude/commands/
        commands_dir = config.get_project_claude_dir(self.project_root) / "commands"
        commands_dir.mkdir(parents=True, exist_ok=True)

        output_path = commands_dir / f"{command_id}.md"

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        return True

    def generate_all(self) -> Dict[str, Any]:
        """Generate all enabled commands for the project."""
        try:
            # Load configuration
            project_config = self.load_project_config()
            enabled_commands = self.load_command_registry()

            generated = []
            failed = []

            for command_id in enabled_commands:
                if self.generate_command(command_id, project_config, enabled_commands):
                    generated.append(command_id)
                else:
                    failed.append(command_id)

            # Update command registry with generation timestamp
            registry_file = config.get_project_claude_dir(self.project_root) / "commands.json"
            registry = {
                "version": config.VERSION,
                "generated_at": datetime.now().isoformat(),
                "commands": [
                    {"id": cmd, "enabled": True, "generated_at": datetime.now().isoformat()}
                    for cmd in generated
                ],
            }

            with open(registry_file, "w", encoding="utf-8") as f:
                json.dump(registry, f, indent=2)

            return {
                "success": True,
                "generated": len(generated),
                "failed": len(failed),
                "failed_commands": failed,
                "commands_dir": str(
                    config.get_project_claude_dir(self.project_root) / "commands",
                ),
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }
