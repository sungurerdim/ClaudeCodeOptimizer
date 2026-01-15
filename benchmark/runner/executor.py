"""
Test executor for CCO benchmarks.

Runs projects through ccbox (vanilla and cco modes) and collects results.

ccbox behavior:
- Mounts current working directory as project root
- -U flag removes CPU/I/O soft limits (required for accurate benchmarking)
- --bare flag runs without CCO rules (vanilla)
- Default (no flag) runs with CCO rules (ccbox:base image)

Requirements:
- Docker must be installed and running (ccbox uses Docker containers)
- ccbox must be installed (pip install ccbox)
"""

import json
import logging
import os
import shutil
import subprocess
import sys
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from .metrics import (
    CodeAnalyzer,
    Metrics,
    calculate_verdict,
    compare_metrics,
)

# Configure logger for detailed debugging
logger = logging.getLogger("cco-benchmark.executor")

# Platform detection for select compatibility
IS_WINDOWS = sys.platform == "win32"

# Windows Ctrl+C exit code (STATUS_CONTROL_C_EXIT = 0xC000013A)
# Can appear as unsigned (3221225786) or signed (-1073741510)
WINDOWS_CTRL_C_EXIT = 3221225786
WINDOWS_CTRL_C_EXIT_SIGNED = -1073741510


@dataclass
class ActivityState:
    """Tracks process activity for stall detection."""

    last_output_time: float = 0.0
    last_file_count: int = 0
    last_file_check_time: float = 0.0
    total_output_lines: int = 0
    stdout_buffer: list[str] = field(default_factory=list)
    stderr_buffer: list[str] = field(default_factory=list)
    stall_warnings: int = 0
    is_stalled: bool = False

    def update_output(self) -> None:
        """Mark that output was received."""
        self.last_output_time = time.time()
        self.total_output_lines += 1
        self.is_stalled = False

    def check_stall(self, stall_threshold: float = 60.0) -> bool:
        """Check if process appears stalled (no output for threshold seconds)."""
        if self.last_output_time == 0:
            return False
        elapsed = time.time() - self.last_output_time
        if elapsed > stall_threshold:
            self.is_stalled = True
            return True
        return False


def _count_project_files(project_dir: Path) -> int:
    """Count non-metadata files in project directory."""
    count = 0
    try:
        for f in project_dir.rglob("*"):
            if f.is_file() and not f.name.startswith("_"):
                count += 1
    except Exception:
        pass
    return count


def _capture_context_snapshot(
    project_dir: Path,
    variant: str,
    model: str,
    ccbox_cmd: str = "ccbox",
) -> dict[str, Any]:
    """Capture context snapshot to verify CCO vs vanilla state.

    This helps verify that:
    - CCO variant actually has rules loaded
    - Vanilla variant is truly bare (no rules)

    Returns:
        Dict with context state for verification
    """
    snapshot: dict[str, Any] = {
        "variant": variant,
        "model": model,
        "timestamp": datetime.now().isoformat(),
        "project_dir": str(project_dir),
        "ccbox_version": None,
        "claude_md": None,
        "claude_dir_exists": False,
        "rules_files": {},
        "settings_json": None,
        "rules_count": 0,
        "rules_total_size": 0,
        "verification": {
            "expected_rules": variant == "cco",
            "has_rules": False,
            "status": "UNKNOWN",
        },
    }

    # Get ccbox version
    try:
        result = subprocess.run(
            [ccbox_cmd, "--version"],
            capture_output=True,
            text=True,
            timeout=5,
            encoding="utf-8",
            errors="replace",
        )
        if result.returncode == 0:
            snapshot["ccbox_version"] = result.stdout.strip()
    except Exception:
        pass

    # Check CLAUDE.md
    claude_md = project_dir / "CLAUDE.md"
    if claude_md.exists():
        try:
            content = claude_md.read_text(encoding="utf-8")
            snapshot["claude_md"] = {
                "exists": True,
                "size": len(content),
                "lines": content.count("\n") + 1,
                "preview": content[:500] + "..." if len(content) > 500 else content,
            }
        except Exception as e:
            snapshot["claude_md"] = {"exists": True, "error": str(e)}

    # Check .claude directory
    claude_dir = project_dir / ".claude"
    if claude_dir.exists() and claude_dir.is_dir():
        snapshot["claude_dir_exists"] = True

        # Read settings.json
        settings_file = claude_dir / "settings.json"
        if settings_file.exists():
            try:
                content = settings_file.read_text(encoding="utf-8")
                snapshot["settings_json"] = json.loads(content)
            except Exception as e:
                snapshot["settings_json"] = {"error": str(e)}

        # Read all rules files
        rules_dir = claude_dir / "rules"
        if rules_dir.exists() and rules_dir.is_dir():
            for rule_file in rules_dir.rglob("*"):
                if rule_file.is_file() and rule_file.suffix in (".md", ".txt", ".json"):
                    rel_path = str(rule_file.relative_to(rules_dir))
                    try:
                        content = rule_file.read_text(encoding="utf-8")
                        snapshot["rules_files"][rel_path] = {
                            "size": len(content),
                            "lines": content.count("\n") + 1,
                            "preview": content[:300] + "..." if len(content) > 300 else content,
                        }
                        snapshot["rules_count"] += 1
                        snapshot["rules_total_size"] += len(content)
                    except Exception as e:
                        snapshot["rules_files"][rel_path] = {"error": str(e)}

    # Verification logic
    # Check for valid CLAUDE.md (exists without error)
    claude_md_valid = (
        snapshot["claude_md"] is not None
        and isinstance(snapshot["claude_md"], dict)
        and snapshot["claude_md"].get("exists", False)
        and "error" not in snapshot["claude_md"]
    )
    has_rules = snapshot["rules_count"] > 0 or claude_md_valid
    snapshot["verification"]["has_rules"] = has_rules

    if variant == "cco":
        if has_rules:
            snapshot["verification"]["status"] = "OK"
            snapshot["verification"]["message"] = (
                f"CCO variant has {snapshot['rules_count']} rule files "
                f"({snapshot['rules_total_size']} bytes)"
            )
        else:
            snapshot["verification"]["status"] = "WARNING"
            snapshot["verification"]["message"] = (
                "CCO variant but no rules found - cco-config may have failed"
            )
    else:  # vanilla
        if has_rules:
            snapshot["verification"]["status"] = "WARNING"
            snapshot["verification"]["message"] = (
                f"Vanilla variant but found {snapshot['rules_count']} rule files - "
                "may not be truly bare"
            )
        else:
            snapshot["verification"]["status"] = "OK"
            snapshot["verification"]["message"] = "Vanilla variant confirmed bare (no rules)"

    return snapshot


def _save_context_snapshot(project_dir: Path, snapshot: dict[str, Any]) -> Path | None:
    """Save context snapshot to file (only if not already exists)."""
    snapshot_file = project_dir / "_context_snapshot.json"
    if snapshot_file.exists():
        return None  # Already captured, skip
    snapshot_file.write_text(
        json.dumps(snapshot, indent=2, default=str),
        encoding="utf-8",
    )
    logger.info(
        f"[{snapshot['variant'].upper()}] Context snapshot: "
        f"{snapshot['verification']['status']} - {snapshot['verification']['message']}"
    )
    return snapshot_file


def _truncate(text: str, max_len: int = 1000) -> str:
    """Truncate text with ellipsis indicator."""
    if len(text) <= max_len:
        return text
    return text[:max_len] + f"\n... [truncated, {len(text) - max_len} more chars]"


def _check_jsonl_for_success(stdout: str) -> tuple[bool, str | None]:
    """Check if jsonl output contains a successful result.

    ccbox/Claude Code CLI can return exit_code=1 even when the task completed
    successfully, if there's a post-completion streaming mode error. This function
    parses the jsonl to detect actual task success.

    Returns:
        Tuple of (has_success, error_if_no_success)
    """
    if not stdout:
        return False, "No output captured"

    has_success_result = False
    last_error = None

    for line in stdout.splitlines():
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
            if entry.get("type") == "result":
                subtype = entry.get("subtype", "")
                if subtype == "success":
                    has_success_result = True
                elif subtype == "error_during_execution":
                    errors = entry.get("errors", [])
                    # Ignore post-completion streaming mode errors
                    if errors and "only prompt commands are supported in streaming mode" in errors:
                        logger.debug("Ignoring post-completion streaming mode error")
                        continue
                    last_error = ", ".join(errors) if errors else "Unknown error"
        except json.JSONDecodeError:
            continue

    if has_success_result:
        return True, None
    return False, last_error


def _parse_ccbox_error(stdout: str, stderr: str, exit_code: int) -> str:
    """Parse ccbox output to extract meaningful error message."""
    error_parts = []

    # Check for user interruption first (highest priority)
    if exit_code in (WINDOWS_CTRL_C_EXIT, WINDOWS_CTRL_C_EXIT_SIGNED, 130):
        return f"Exit code {exit_code}: Process interrupted by user (Ctrl+C)"
    if "keyboardinterrupt" in (stdout + stderr).lower():
        return f"Exit code {exit_code}: Process interrupted by user (KeyboardInterrupt)"

    # Check for common ccbox errors
    combined = (stdout + stderr).lower()

    # Gosu user switching error (common on Windows/WSL2)
    if "gosu" in combined and "operation not permitted" in combined:
        error_parts.append(
            "Docker user switching failed (gosu). "
            "Fix: Run Docker Desktop as Administrator, or check WSL2 integration settings"
        )
    elif "failed switching to" in combined and "operation not permitted" in combined:
        error_parts.append(
            "Container user switching failed. "
            "Fix: Ensure Docker Desktop has proper permissions on Windows/WSL2"
        )
    if "docker" in combined and ("not found" in combined or "not running" in combined):
        error_parts.append("Docker issue detected")
    if "permission denied" in combined:
        error_parts.append("Permission denied (check Docker permissions)")
    if "no such file" in combined or "not found" in combined:
        # Skip if already reported gosu error
        if "gosu" not in combined:
            error_parts.append("File/command not found")
    if "timeout" in combined:
        error_parts.append("Operation timed out")
    if "authentication" in combined or "api key" in combined or "unauthorized" in combined:
        error_parts.append("Authentication/API key issue")
    if "rate limit" in combined:
        error_parts.append("Rate limit exceeded")
    if "network" in combined or "connection" in combined:
        error_parts.append("Network/connection issue")

    # Extract actual error lines from stderr
    error_lines = []
    for line in stderr.splitlines():
        line_lower = line.lower()
        if any(kw in line_lower for kw in ["error", "failed", "exception", "traceback", "fatal"]):
            error_lines.append(line.strip())

    if error_lines:
        error_parts.append("Errors: " + "; ".join(error_lines[:5]))

    # If no specific error found, include raw output
    if not error_parts:
        if stderr.strip():
            error_parts.append(f"stderr: {_truncate(stderr.strip(), 500)}")
        elif stdout.strip():
            error_parts.append(f"stdout: {_truncate(stdout.strip(), 500)}")
        else:
            error_parts.append("No output captured")

    return f"Exit code {exit_code}: " + " | ".join(error_parts)


def get_platform_info() -> dict[str, str]:
    """Get platform-specific Docker installation/startup info."""
    import platform

    system = platform.system().lower()

    if system == "windows":
        return {
            "os": "windows",
            "os_name": "Windows",
            "docker_install_url": "https://docs.docker.com/desktop/install/windows-install/",
            "docker_start_cmd": "Start Docker Desktop from the Start menu",
        }
    elif system == "darwin":
        return {
            "os": "macos",
            "os_name": "macOS",
            "docker_install_url": "https://docs.docker.com/desktop/install/mac-install/",
            "docker_start_cmd": "open -a Docker",
        }
    else:  # Linux
        return {
            "os": "linux",
            "os_name": "Linux",
            "docker_install_url": "https://docs.docker.com/engine/install/",
            "docker_start_cmd": "sudo systemctl start docker",
        }


PLATFORM_INFO = get_platform_info()
DOCKER_INSTALL_URL = PLATFORM_INFO["docker_install_url"]


@dataclass
class DependencyStatus:
    """Status of system dependencies."""

    platform: str = ""
    docker_installed: bool = False
    docker_running: bool = False
    docker_version: str | None = None
    docker_install_url: str = ""
    docker_start_cmd: str = ""
    ccbox_installed: bool = False
    ccbox_version: str | None = None
    ready: bool = False
    error_message: str = ""
    warning_message: str = ""  # Non-blocking warnings

    def to_dict(self) -> dict[str, Any]:
        return {
            "platform": self.platform,
            "docker_installed": self.docker_installed,
            "docker_running": self.docker_running,
            "docker_version": self.docker_version,
            "docker_install_url": self.docker_install_url,
            "docker_start_cmd": self.docker_start_cmd,
            "ccbox_installed": self.ccbox_installed,
            "ccbox_version": self.ccbox_version,
            "ready": self.ready,
            "error_message": self.error_message,
            "warning_message": self.warning_message,
        }


def check_dependencies() -> DependencyStatus:
    """Check if Docker and ccbox are available."""
    status = DependencyStatus(
        platform=PLATFORM_INFO["os_name"],
        docker_install_url=PLATFORM_INFO["docker_install_url"],
        docker_start_cmd=PLATFORM_INFO["docker_start_cmd"],
    )

    # Check Docker
    docker_path = shutil.which("docker")
    if docker_path:
        status.docker_installed = True
        try:
            version_result = subprocess.run(
                ["docker", "--version"],
                capture_output=True,
                text=True,
                timeout=5,
                encoding="utf-8",
                errors="replace",
            )
            if version_result.returncode == 0:
                # Parse "Docker version 24.0.7, build afdd53b"
                version_str = version_result.stdout.strip()
                parts = version_str.split()
                for i, p in enumerate(parts):
                    if p.lower() == "version" and i + 1 < len(parts):
                        status.docker_version = parts[i + 1].rstrip(",")
                        break

            # Check if daemon is running
            daemon_result = subprocess.run(
                ["docker", "info"],
                capture_output=True,
                text=True,
                timeout=10,
                encoding="utf-8",
                errors="replace",
            )
            status.docker_running = daemon_result.returncode == 0
            if not status.docker_running:
                status.error_message = f"Docker daemon is not running. {status.docker_start_cmd}"
        except subprocess.TimeoutExpired:
            status.error_message = "Docker daemon check timed out"
        except Exception as e:
            status.error_message = f"Docker check failed: {e}"
    else:
        status.error_message = f"Docker is not installed. Install from: {status.docker_install_url}"

    # Check ccbox
    ccbox_path = shutil.which("ccbox")
    if ccbox_path:
        status.ccbox_installed = True
        try:
            version_result = subprocess.run(
                ["ccbox", "--version"],
                capture_output=True,
                text=True,
                timeout=5,
                encoding="utf-8",
                errors="replace",
            )
            if version_result.returncode == 0:
                status.ccbox_version = version_result.stdout.strip().split()[-1]
        except Exception:
            pass
    elif status.docker_running and not status.error_message:
        status.error_message = "ccbox is not installed. Run: pip install ccbox"

    # Add Windows/WSL2 warning about potential gosu issues
    if status.ready and PLATFORM_INFO["os"] == "windows":
        status.warning_message = (
            "Windows/WSL2 detected. If you see 'gosu: operation not permitted' errors, "
            "try running Docker Desktop as Administrator. See README for more solutions."
        )

    status.ready = status.docker_installed and status.docker_running and status.ccbox_installed
    return status


@dataclass
class BenchmarkPhase:
    """Single benchmark phase result for new flow."""

    name: str  # vanilla_generation, vanilla_analysis, cco_derive, cco_config, cco_optimize, cco_review, cco_analysis
    success: bool
    duration_seconds: float
    error: str | None = None
    output: dict[str, Any] | None = None
    skipped: bool = False  # True if phase was skipped during resume

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "success": self.success,
            "duration_seconds": round(self.duration_seconds, 2),
            "error": self.error,
            "skipped": self.skipped,
        }


@dataclass
class ResumeState:
    """Tracks what phases can be skipped when resuming a benchmark.

    Checks for:
    - Phase 1: vanilla_dir exists with source files
    - Phase 2: vanilla analysis JSON files exist
    - Phase 3: cco_dir exists with source files
    - Phase 4: .claude folder exists in cco_dir (config done)
    - Phase 5-6: Always re-run (optimize/review are the main CCO value)
    - Phase 7: cco analysis JSON files exist
    """

    vanilla_generated: bool = False
    vanilla_analyzed: bool = False
    cco_derived: bool = False
    cco_configured: bool = False
    # Loaded data from previous run
    vanilla_metrics: Metrics | None = None
    vanilla_ai_result: dict[str, Any] | None = None

    @property
    def can_skip_vanilla_generation(self) -> bool:
        return self.vanilla_generated

    @property
    def can_skip_vanilla_analysis(self) -> bool:
        return self.vanilla_analyzed and self.vanilla_metrics is not None

    @property
    def can_skip_cco_derive(self) -> bool:
        return self.cco_derived

    @property
    def can_skip_cco_config(self) -> bool:
        return self.cco_configured

    @property
    def resume_from_phase(self) -> int:
        """Return the phase number to resume from (1-7)."""
        if not self.vanilla_generated:
            return 1
        if not self.vanilla_analyzed:
            return 2
        if not self.cco_derived:
            return 3
        if not self.cco_configured:
            return 4
        # Always re-run optimize/review (5-6) - that's the CCO value
        return 5


@dataclass
class NewBenchmarkResult:
    """Complete benchmark result for new flow.

    New flow: vanilla → derive CCO → optimize → review → analyze both.
    CCO no longer generates code from scratch - it optimizes vanilla code.
    """

    project_id: str
    project_name: str
    phases: list[BenchmarkPhase]
    vanilla_metrics: Metrics | None
    vanilla_ai_result: dict[str, Any] | None
    cco_metrics: Metrics | None
    cco_ai_result: dict[str, Any] | None
    comparison: dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    # Legacy fields for compatibility
    categories: list[str] = field(default_factory=list)
    complexity: str = "Medium"

    def to_dict(self) -> dict[str, Any]:
        return {
            "project_id": self.project_id,
            "project_name": self.project_name,
            "phases": [p.to_dict() for p in self.phases],
            "vanilla": {
                "metrics": self.vanilla_metrics.to_dict() if self.vanilla_metrics else None,
                "ai_analysis": self.vanilla_ai_result,
            },
            "cco": {
                "metrics": self.cco_metrics.to_dict() if self.cco_metrics else None,
                "ai_analysis": self.cco_ai_result,
            },
            "comparison": self.comparison,
            "timestamp": self.timestamp,
            "categories": self.categories,
            "complexity": self.complexity,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "NewBenchmarkResult":
        phases = [
            BenchmarkPhase(
                name=p["name"],
                success=p["success"],
                duration_seconds=p["duration_seconds"],
                error=p.get("error"),
                skipped=p.get("skipped", False),
            )
            for p in data.get("phases", [])
        ]
        vanilla_data = data.get("vanilla", {})
        cco_data = data.get("cco", {})
        return cls(
            project_id=data["project_id"],
            project_name=data["project_name"],
            phases=phases,
            vanilla_metrics=Metrics.from_dict(vanilla_data.get("metrics"))
            if vanilla_data.get("metrics")
            else None,
            vanilla_ai_result=vanilla_data.get("ai_analysis"),
            cco_metrics=Metrics.from_dict(cco_data.get("metrics"))
            if cco_data.get("metrics")
            else None,
            cco_ai_result=cco_data.get("ai_analysis"),
            comparison=data.get("comparison", {}),
            timestamp=data.get("timestamp", ""),
            categories=data.get("categories", []),
            complexity=data.get("complexity", "Medium"),
        )


@dataclass
class ExecutionResult:
    """Result of a single test execution."""

    project_id: str
    variant: str  # "cco" or "vanilla"
    success: bool
    metrics: Metrics | None
    score: float
    generation_time_seconds: float  # Total time (all phases)
    prompt_used: str
    error_message: str = ""
    output_dir: str = ""
    command: str = ""  # Full command executed
    exit_code: int | None = None
    stdout_excerpt: str = ""  # Last 500 chars of stdout
    stderr_excerpt: str = ""  # Last 500 chars of stderr
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    # CCO phase timings (None for vanilla)
    config_time_seconds: float | None = None  # cco-config phase
    coding_time_seconds: float | None = None  # Main coding phase
    optimize_time_seconds: float | None = None  # cco-optimize phase
    optimize_success: bool | None = None  # Track optimize phase result (None for vanilla)
    optimize_error: str | None = None  # Optimize phase error message if failed

    def to_dict(self) -> dict[str, Any]:
        result = {
            "project_id": self.project_id,
            "variant": self.variant,
            "success": self.success,
            "metrics": self.metrics.to_dict() if self.metrics else None,
            "score": self.score,
            "generation_time_seconds": self.generation_time_seconds,
            "prompt_used": self.prompt_used,
            "error_message": self.error_message,
            "output_dir": self.output_dir,
            "command": self.command,
            "exit_code": self.exit_code,
            "stdout_excerpt": self.stdout_excerpt,
            "stderr_excerpt": self.stderr_excerpt,
            "timestamp": self.timestamp,
        }
        # Include phase timings for CCO variant
        if self.variant == "cco":
            result["config_time_seconds"] = self.config_time_seconds
            result["coding_time_seconds"] = self.coding_time_seconds
            result["optimize_time_seconds"] = self.optimize_time_seconds
            result["optimize_success"] = self.optimize_success
            result["optimize_error"] = self.optimize_error
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ExecutionResult":
        metrics_data = data.pop("metrics", None)
        metrics = Metrics.from_dict(metrics_data) if metrics_data else None
        return cls(metrics=metrics, **data)


@dataclass
class BenchmarkResult:
    """Full benchmark result comparing CCO vs Vanilla."""

    project_id: str
    project_name: str
    categories: list[str]
    complexity: str
    cco_result: ExecutionResult
    vanilla_result: ExecutionResult
    comparison: dict[str, Any]
    verdict: str
    score_difference: float
    prompt_used: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict[str, Any]:
        return {
            "project_id": self.project_id,
            "project_name": self.project_name,
            "categories": self.categories,
            "complexity": self.complexity,
            "cco_result": self.cco_result.to_dict(),
            "vanilla_result": self.vanilla_result.to_dict(),
            "comparison": self.comparison,
            "verdict": self.verdict,
            "score_difference": self.score_difference,
            "prompt_used": self.prompt_used,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BenchmarkResult":
        cco_data = data.pop("cco_result")
        vanilla_data = data.pop("vanilla_result")
        result = cls(
            cco_result=ExecutionResult.from_dict(cco_data),
            vanilla_result=ExecutionResult.from_dict(vanilla_data),
            **data,
        )
        return result


class ProjectConfig:
    """Configuration for a benchmark project."""

    def __init__(self, project_dir: Path):
        self.project_dir = project_dir
        self.prompt_file = project_dir / "PROMPT.md"
        self.spec_file = project_dir / "SPEC.md"
        self._load()

    def _load(self) -> None:
        """Load project configuration from SPEC.md."""
        self.id = self.project_dir.name
        self.name = self.id.replace("_", " ").title()
        self.categories: list[str] = []
        self.complexity = "Medium"

        if self.spec_file.exists():
            content = self.spec_file.read_text(encoding="utf-8")
            # Parse categories
            for line in content.splitlines():
                if line.startswith("- ") and ":" in line:
                    cat = line.strip("- ").strip()
                    if any(c in cat for c in [":", "::"]):
                        self.categories.append(cat)
                elif "Complexity:" in line:
                    self.complexity = line.split(":")[-1].strip()

        if self.prompt_file.exists():
            self.prompt = self.prompt_file.read_text(encoding="utf-8")
        else:
            self.prompt = ""


class TestExecutor:
    """Executes benchmark tests using ccbox.

    ccbox mounts the current working directory as project root.
    We create isolated directories for each test run and cd into them.

    Log files are organized in benchmark/logs/{project_id}/{variant}/:
        benchmark/logs/
        └── {project_id}/
            ├── cco/
            │   ├── summary.json          # Machine-readable results
            │   ├── 01_config.log         # CCO config phase summary
            │   ├── 01_config.jsonl       # CCO config output stream
            │   ├── 02_coding.log         # Main coding phase summary
            │   ├── 02_coding.jsonl       # Claude output (JSON Lines)
            │   ├── 02_coding_errors.log  # stderr output
            │   └── 03_optimize.log       # CCO optimize phase summary
            └── vanilla/
                ├── summary.json
                ├── 02_coding.log
                ├── 02_coding.jsonl
                └── 02_coding_errors.log
    """

    def __init__(
        self,
        output_base: Path,
        ccbox_cmd: str = "ccbox",
        timeout_seconds: int = 1800,  # Inactivity timeout (30 min - Opus 4.5 extended thinking)
        stall_threshold: float = 120.0,
        progress_callback: Callable[[str, ActivityState], None] | None = None,
    ):
        self.output_base = output_base
        self.logs_base = output_base.parent / "logs"  # benchmark/logs/
        self.ccbox_cmd = ccbox_cmd
        self.timeout = timeout_seconds
        # Opus 4.5 extended thinking can take several minutes without output
        self.phase_timeout = 1800  # 30 minutes for CCO config/optimize phases
        self.stall_threshold = stall_threshold  # Seconds without output = stall warning
        self.progress_callback = progress_callback
        self.output_base.mkdir(parents=True, exist_ok=True)
        self.logs_base.mkdir(parents=True, exist_ok=True)

    def _get_log_dir(self, project_id: str, variant: str) -> Path:
        """Get or create the log directory for a project variant.

        Structure: benchmark/logs/{project_id}/{variant}/
        """
        log_dir = self.logs_base / project_id / variant
        log_dir.mkdir(parents=True, exist_ok=True)
        return log_dir

    def _check_resume_state(self, config: ProjectConfig) -> ResumeState:
        """Check what phases have already completed for resume functionality.

        Returns ResumeState with flags for each completed phase and loaded data.
        """
        state = ResumeState()
        vanilla_dir = self.output_base / f"{config.id}_vanilla"
        cco_dir = self.output_base / f"{config.id}_cco"
        logs_dir = self.logs_base / config.id

        # Check Phase 1: Vanilla generation
        if vanilla_dir.exists():
            # Check for source files (not just prompt file)
            source_files = list(vanilla_dir.glob("**/*.py")) + list(vanilla_dir.glob("**/*.js"))
            source_files = [f for f in source_files if not f.name.startswith("_")]
            if source_files:
                state.vanilla_generated = True
                logger.info(f"[RESUME] Vanilla dir exists with {len(source_files)} source files")

        # Check Phase 2: Vanilla analysis
        vanilla_log_dir = logs_dir / "vanilla"
        static_file = vanilla_log_dir / "analysis_static.json"
        ai_file = vanilla_log_dir / "analysis_ai.json"

        if static_file.exists():
            try:
                static_data = json.loads(static_file.read_text(encoding="utf-8"))
                state.vanilla_metrics = Metrics.from_dict(static_data)
                logger.info("[RESUME] Loaded vanilla static analysis")
            except Exception as e:
                logger.warning(f"[RESUME] Failed to load vanilla static analysis: {e}")

        if ai_file.exists():
            try:
                state.vanilla_ai_result = json.loads(ai_file.read_text(encoding="utf-8"))
                logger.info("[RESUME] Loaded vanilla AI analysis")
            except Exception as e:
                logger.warning(f"[RESUME] Failed to load vanilla AI analysis: {e}")

        state.vanilla_analyzed = state.vanilla_metrics is not None

        # Check Phase 3: CCO derivation
        if cco_dir.exists():
            source_files = list(cco_dir.glob("**/*.py")) + list(cco_dir.glob("**/*.js"))
            source_files = [f for f in source_files if not f.name.startswith("_")]
            if source_files:
                state.cco_derived = True
                logger.info(f"[RESUME] CCO dir exists with {len(source_files)} source files")

        # Check Phase 4: CCO config
        claude_dir = cco_dir / ".claude"
        if claude_dir.exists() and claude_dir.is_dir():
            state.cco_configured = True
            logger.info("[RESUME] CCO .claude folder exists (config done)")

        # Log resume state
        logger.info(f"[RESUME] State: vanilla_gen={state.vanilla_generated}, "
                    f"vanilla_analysis={state.vanilla_analyzed}, "
                    f"cco_derived={state.cco_derived}, "
                    f"cco_configured={state.cco_configured}")
        logger.info(f"[RESUME] Will resume from phase {state.resume_from_phase}")

        return state

    def _save_analysis_results(
        self, project_id: str, variant: str, metrics: Metrics | None, ai_result: dict[str, Any] | None
    ) -> None:
        """Save analysis results to log directory for resume functionality."""
        log_dir = self._get_log_dir(project_id, variant)

        if metrics:
            static_file = log_dir / "analysis_static.json"
            static_file.write_text(
                json.dumps(metrics.to_dict(), indent=2, default=str),
                encoding="utf-8",
            )
            logger.info(f"[SAVE] Static analysis saved to {static_file}")

        if ai_result:
            ai_file = log_dir / "analysis_ai.json"
            ai_file.write_text(
                json.dumps(ai_result, indent=2, default=str),
                encoding="utf-8",
            )
            logger.info(f"[SAVE] AI analysis saved to {ai_file}")

    def _run_with_streaming(
        self,
        cmd: list[str],
        project_dir: Path,
        project_id: str,
        variant: str,
        timeout: float,
        env: dict[str, str] | None = None,
        log_phase: str = "02_coding",  # Log file prefix: 01_config, 02_coding, 03_optimize
    ) -> tuple[int | None, str, str, ActivityState]:
        """Run command with real-time output streaming and activity tracking.

        Args:
            project_id: Project identifier for log directory
            log_phase: Phase prefix for log files (01_config, 02_coding, 03_optimize)

        Returns:
            Tuple of (exit_code, stdout, stderr, activity_state)
        """
        activity = ActivityState()
        activity.last_output_time = time.time()
        activity.last_file_check_time = time.time()
        activity.last_file_count = _count_project_files(project_dir)

        process_env = {**os.environ, **(env or {})}
        start_time = time.time()

        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=process_env,
                encoding="utf-8",
                errors="replace",
                bufsize=1,  # Line buffered
            )
        except FileNotFoundError:
            return None, "", "", activity

        # Thread-safe buffers
        stdout_lines: list[str] = []
        stderr_lines: list[str] = []
        lock = threading.Lock()

        def read_stream(stream: Any, buffer: list[str], stream_name: str) -> None:
            """Read from stream and update activity."""
            try:
                for line in iter(stream.readline, ""):
                    if not line:
                        break
                    with lock:
                        buffer.append(line)
                        activity.update_output()

                    # Log real-time output (truncation handled by ColoredFormatter)
                    line_stripped = line.rstrip()
                    if line_stripped:
                        msg = f"[{variant.upper()}:{project_id}] [{stream_name}] {line_stripped}"
                        # stderr = error, stdout = info (ccbox should not write info to stderr)
                        if stream_name == "stderr":
                            logger.error(msg)
                        else:
                            logger.info(msg)

                    # Call progress callback
                    if self.progress_callback:
                        try:
                            self.progress_callback(line_stripped, activity)
                        except Exception:
                            pass
            except Exception as e:
                logger.debug(f"Stream read error ({stream_name}): {e}")
            finally:
                try:
                    stream.close()
                except Exception:
                    pass

        # Start reader threads
        stdout_thread = threading.Thread(
            target=read_stream, args=(process.stdout, stdout_lines, "stdout"), daemon=True
        )
        stderr_thread = threading.Thread(
            target=read_stream, args=(process.stderr, stderr_lines, "stderr"), daemon=True
        )
        stdout_thread.start()
        stderr_thread.start()

        # Monitor loop with stall detection
        last_stall_check = time.time()
        last_log_flush = time.time()
        stall_check_interval = 30.0  # Check every 30 seconds
        file_check_interval = 60.0  # Check files every 60 seconds
        log_flush_interval = 30.0  # Flush logs every 30 seconds

        while process.poll() is None:
            elapsed = time.time() - start_time
            now = time.time()

            # Inactivity timeout - terminate if no output for too long
            if activity.last_output_time > 0:
                inactivity = now - activity.last_output_time
                if inactivity > timeout:
                    logger.warning(
                        f"[{variant.upper()}:{project_id}] TIMEOUT - no output for {inactivity:.0f}s "
                        f"(total runtime: {elapsed:.0f}s) - terminating..."
                    )
                    process.terminate()
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        process.wait()
                    break

            # Stall detection (warning only, timeout handles termination)
            if now - last_stall_check > stall_check_interval:
                last_stall_check = now

                if activity.check_stall(self.stall_threshold):
                    stall_time = now - activity.last_output_time

                    # Check file activity as secondary indicator
                    if now - activity.last_file_check_time > file_check_interval:
                        current_files = _count_project_files(project_dir)
                        file_change = current_files - activity.last_file_count
                        activity.last_file_count = current_files
                        activity.last_file_check_time = now

                        if file_change > 0:
                            logger.info(
                                f"[{variant.upper()}:{project_id}] [ACTIVITY] No output for {stall_time:.0f}s "
                                f"but {file_change} new files created - still working"
                            )
                            # Reset stall state - file activity proves process is working
                            activity.is_stalled = False
                            activity.last_output_time = now  # Reset timer
                        else:
                            activity.stall_warnings += 1
                            logger.warning(
                                f"[{variant.upper()}:{project_id}] [STALL] No output for {stall_time:.0f}s, "
                                f"no new files - may be stuck (warning #{activity.stall_warnings})"
                            )
                    else:
                        activity.stall_warnings += 1
                        logger.warning(
                            f"[{variant.upper()}:{project_id}] [STALL] No output for {stall_time:.0f}s "
                            f"(warning #{activity.stall_warnings})"
                        )

            # Periodic log flush to benchmark/logs/
            if now - last_log_flush > log_flush_interval:
                last_log_flush = now
                try:
                    log_dir = self._get_log_dir(project_id, variant)
                    with lock:
                        if stdout_lines:
                            (log_dir / f"{log_phase}.jsonl").write_text(
                                "".join(stdout_lines), encoding="utf-8"
                            )
                        if stderr_lines:
                            (log_dir / f"{log_phase}_errors.log").write_text(
                                "".join(stderr_lines), encoding="utf-8"
                            )
                except OSError:
                    pass  # Ignore flush errors, final write will catch issues

            time.sleep(0.5)

        # Wait for reader threads to finish
        stdout_thread.join(timeout=5)
        stderr_thread.join(timeout=5)

        # Collect output
        with lock:
            stdout = "".join(stdout_lines)
            stderr = "".join(stderr_lines)
            activity.stdout_buffer = stdout_lines
            activity.stderr_buffer = stderr_lines

        exit_code = process.returncode
        return exit_code, stdout, stderr, activity

    def _run_cco_config(self, project_dir: Path, project_id: str, model: str) -> dict[str, Any]:
        """Run cco-config --auto to configure CCO rules before the actual test.

        This runs in a separate ccbox invocation so that:
        1. CCO rules are configured and persisted
        2. Container restarts with rules in context

        Uses streaming mode with inactivity-based timeout - the process continues
        as long as output is being produced.

        Returns:
            Dict with success, time, command, exit_code, stdout, stderr, error
        """
        # ccbox parameters (as of latest version):
        # -U: unrestricted mode (no CPU/I/O soft limits - required for benchmarking)
        # -y: unattended mode (deps=ALL, stack=auto-detect, no prompts)
        # -dd: debug logging (stream output)
        # -C: change directory
        # -m/--model: model selection
        # -p/--prompt: initial prompt (enables --print mode)
        cmd = [
            self.ccbox_cmd,
            "-U",  # Unrestricted mode (no CPU/I/O limits for benchmarking)
            "-y",  # Unattended mode (deps=ALL, stack=auto)
            "-dd",  # Debug logging
            "-C",
            str(project_dir),
            "-m",
            model,
            "-p",
            "/cco-config --auto --target-dir .claude",  # Persist config in project dir
        ]
        cmd_str = " ".join(cmd)
        start_time = time.time()

        logger.info(f"[CCO Config] Starting: {cmd_str}")
        logger.info(f"[CCO Config] Project dir: {project_dir}")
        logger.info(f"[CCO Config] Using inactivity timeout: {self.phase_timeout}s")

        try:
            # Use streaming mode with inactivity-based timeout
            exit_code, stdout, stderr, activity = self._run_with_streaming(
                cmd=cmd,
                project_dir=project_dir,
                project_id=project_id,
                variant="cco",  # Config is part of CCO variant
                timeout=float(self.phase_timeout),
                env={"CLAUDE_MODEL": model},
                log_phase="01_config",
            )

            elapsed = time.time() - start_time

            # Save config logs with detailed info
            log_content = f"""CCO Config Log (Streaming Mode)
{"=" * 60}
Command: {cmd_str}
Exit Code: {exit_code}
Duration: {elapsed:.2f}s
Project Dir: {project_dir}
{"=" * 60}

ACTIVITY TRACKING:
- Total output lines: {activity.total_output_lines}
- Stall warnings: {activity.stall_warnings}
- Final stall state: {activity.is_stalled}
{"=" * 60}

STDOUT:
{stdout or "(empty)"}

{"=" * 60}
STDERR:
{stderr or "(empty)"}
"""
            log_dir = self._get_log_dir(project_id, "cco")
            (log_dir / "01_config.log").write_text(log_content, encoding="utf-8")
            (log_dir / "01_config.jsonl").write_text(stdout, encoding="utf-8")
            (log_dir / "01_config_errors.log").write_text(stderr, encoding="utf-8")

            # Handle FileNotFoundError (exit_code is None and no output)
            if exit_code is None and not stdout and not stderr:
                error_msg = f"ccbox command not found: {self.ccbox_cmd}"
                logger.error(f"[CCO Config] {error_msg}")
                return {
                    "success": False,
                    "time": elapsed,
                    "command": cmd_str,
                    "exit_code": None,
                    "stdout": "",
                    "stderr": "",
                    "error": error_msg,
                }

            # Handle timeout (exit_code is None but we have output)
            if exit_code is None:
                error_msg = f"Config inactivity timeout after {self.phase_timeout}s without output"
                logger.error(f"[CCO Config] TIMEOUT: {error_msg}")
                logger.error(f"[CCO Config] Partial stdout:\n{_truncate(stdout, 1000)}")
                logger.error(f"[CCO Config] Partial stderr:\n{_truncate(stderr, 1000)}")
                return {
                    "success": False,
                    "time": elapsed,
                    "command": cmd_str,
                    "exit_code": None,
                    "stdout": stdout,
                    "stderr": stderr,
                    "error": error_msg,
                }

            if exit_code != 0:
                error_msg = _parse_ccbox_error(stdout, stderr, exit_code)
                logger.error(f"[CCO Config] FAILED: {error_msg}")
                logger.error(f"[CCO Config] Full stdout:\n{_truncate(stdout, 2000)}")
                logger.error(f"[CCO Config] Full stderr:\n{_truncate(stderr, 2000)}")

                return {
                    "success": False,
                    "time": elapsed,
                    "command": cmd_str,
                    "exit_code": exit_code,
                    "stdout": stdout,
                    "stderr": stderr,
                    "error": error_msg,
                }

            logger.info(f"[CCO Config] SUCCESS in {elapsed:.2f}s")
            return {
                "success": True,
                "time": elapsed,
                "command": cmd_str,
                "exit_code": 0,
                "stdout": stdout,
                "stderr": stderr,
                "error": "",
            }

        except Exception as e:
            elapsed = time.time() - start_time
            import traceback

            error_msg = f"{type(e).__name__}: {e}"
            logger.error(f"[CCO Config] EXCEPTION: {error_msg}")
            logger.error(f"[CCO Config] Traceback:\n{traceback.format_exc()}")
            return {
                "success": False,
                "time": elapsed,
                "command": cmd_str,
                "exit_code": None,
                "stdout": "",
                "stderr": "",
                "error": error_msg,
            }

    def _run_cco_optimize(self, project_dir: Path, project_id: str, model: str) -> dict[str, Any]:
        """Run cco-optimize --auto to optimize generated code after test completion.

        This runs in a separate ccbox invocation to apply security, quality,
        and best-practice fixes to the generated code.

        Uses streaming mode with inactivity-based timeout - the process continues
        as long as output is being produced.

        Returns:
            Dict with success, time, command, exit_code, stdout, stderr, error
        """
        cmd = [
            self.ccbox_cmd,
            "-U",  # Unrestricted mode (no CPU/I/O limits for benchmarking)
            "-y",  # Unattended mode (deps=ALL, stack=auto)
            "-dd",  # Debug logging
            "-C",
            str(project_dir),
            "-m",
            model,
            "-p",
            "/cco-optimize --auto",  # Full scope, fix all, silent execution
        ]
        cmd_str = " ".join(cmd)
        start_time = time.time()

        logger.info(f"[CCO Optimize] Starting: {cmd_str}")
        logger.info(f"[CCO Optimize] Project dir: {project_dir}")
        logger.info(f"[CCO Optimize] Using inactivity timeout: {self.phase_timeout}s")

        try:
            # Use streaming mode with inactivity-based timeout
            exit_code, stdout, stderr, activity = self._run_with_streaming(
                cmd=cmd,
                project_dir=project_dir,
                project_id=project_id,
                variant="cco",  # Optimize is part of CCO variant
                timeout=float(self.phase_timeout),
                env={"CLAUDE_MODEL": model},
                log_phase="03_optimize",
            )

            elapsed = time.time() - start_time

            # Save optimize logs to benchmark/logs/
            log_content = f"""CCO Optimize Log (Streaming Mode)
{"=" * 60}
Command: {cmd_str}
Exit Code: {exit_code}
Duration: {elapsed:.2f}s
Project Dir: {project_dir}
{"=" * 60}

ACTIVITY TRACKING:
- Total output lines: {activity.total_output_lines}
- Stall warnings: {activity.stall_warnings}
- Final stall state: {activity.is_stalled}
{"=" * 60}

STDOUT:
{stdout or "(empty)"}

{"=" * 60}
STDERR:
{stderr or "(empty)"}
"""
            log_dir = self._get_log_dir(project_id, "cco")
            (log_dir / "03_optimize.log").write_text(log_content, encoding="utf-8")
            (log_dir / "03_optimize.jsonl").write_text(stdout, encoding="utf-8")
            (log_dir / "03_optimize_errors.log").write_text(stderr, encoding="utf-8")

            # Handle FileNotFoundError (exit_code is None and no output)
            if exit_code is None and not stdout and not stderr:
                error_msg = f"ccbox command not found: {self.ccbox_cmd}"
                logger.warning(f"[CCO Optimize] {error_msg} (non-blocking)")
                return {
                    "success": False,
                    "time": elapsed,
                    "command": cmd_str,
                    "exit_code": None,
                    "stdout": "",
                    "stderr": "",
                    "error": error_msg,
                }

            # Handle timeout (exit_code is None but we have output)
            if exit_code is None:
                error_msg = (
                    f"Optimize inactivity timeout after {self.phase_timeout}s without output"
                )
                logger.warning(f"[CCO Optimize] TIMEOUT (non-blocking): {error_msg}")
                return {
                    "success": False,
                    "time": elapsed,
                    "command": cmd_str,
                    "exit_code": None,
                    "stdout": stdout,
                    "stderr": stderr,
                    "error": error_msg,
                }

            if exit_code != 0:
                error_msg = _parse_ccbox_error(stdout, stderr, exit_code)
                logger.warning(f"[CCO Optimize] FAILED (non-blocking): {error_msg}")
                return {
                    "success": False,
                    "time": elapsed,
                    "command": cmd_str,
                    "exit_code": exit_code,
                    "stdout": stdout,
                    "stderr": stderr,
                    "error": error_msg,
                }

            logger.info(f"[CCO Optimize] SUCCESS in {elapsed:.2f}s")
            return {
                "success": True,
                "time": elapsed,
                "command": cmd_str,
                "exit_code": 0,
                "stdout": stdout,
                "stderr": stderr,
                "error": "",
            }

        except Exception as e:
            elapsed = time.time() - start_time
            error_msg = f"{type(e).__name__}: {e}"
            logger.warning(f"[CCO Optimize] EXCEPTION (non-blocking): {error_msg}")
            return {
                "success": False,
                "time": elapsed,
                "command": cmd_str,
                "exit_code": None,
                "stdout": "",
                "stderr": "",
                "error": error_msg,
            }

    def run_project(
        self, config: ProjectConfig, variant: str, model: str = "opus"
    ) -> ExecutionResult:
        """Run a single project variant.

        Creates an isolated directory, cd's into it, and runs ccbox.
        ccbox will mount this directory and generate code there.

        Uses fixed folder names (no timestamps) and cleans before each run.

        For CCO variant, runs three phases:
        1. Setup phase: Run /cco-config --auto to configure CCO rules
        2. Test phase: Run the actual benchmark prompt
        3. Optimize phase: Run /cco-optimize --auto to apply fixes (non-blocking)
        """
        # Visual separator for variant start
        separator_heavy = "═" * 60
        separator_light = "─" * 40

        logger.info(f"\n{separator_heavy}")
        logger.info(f"[{variant.upper()}:{config.id}] STARTING")
        logger.info(separator_heavy)

        # Fixed folder name (no timestamp) - same test always uses same folder
        project_dir = self.output_base / f"{config.id}_{variant}"

        # Clean existing folder before run
        if project_dir.exists():
            logger.info(f"[{variant.upper()}:{config.id}] Cleaning existing folder")
            shutil.rmtree(project_dir)

        project_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"[{variant.upper()}:{config.id}] Output dir: {project_dir}")

        # Save prompt to file - ccbox will read from here instead of command line
        # This avoids Windows command line length limits (~8192 chars) and shell escaping issues
        prompt_file = project_dir / "_benchmark_prompt.md"
        prompt_file.write_text(config.prompt, encoding="utf-8")

        # Short instruction for ccbox - actual task is in the file
        # CRITICAL: Explicit constraints to prevent streaming mode errors:
        # - No slash commands (not supported in streaming/print mode)
        # - No interactive commands or follow-up questions
        # - Clear completion signal without attempting unsupported actions
        short_prompt = """Read _benchmark_prompt.md and complete all tasks described in it.

CRITICAL CONSTRAINTS:
- Do NOT use slash commands (/, /help, /commit, etc.) - they are not available in this mode
- Do NOT ask follow-up questions or request user input
- When finished, simply summarize what was built - do not attempt any post-completion commands
- Focus only on writing code, tests, and configuration files

Execute the task autonomously and completely."""

        # CCO phase timings and results
        config_time: float | None = None
        optimize_time: float | None = None
        optimize_success: bool | None = None
        optimize_error: str | None = None
        config_result: dict[str, Any] | None = None
        optimize_result: dict[str, Any] | None = None

        # CCO variant: First run cco-config --auto to configure rules
        if variant == "cco":
            logger.info(f"\n{separator_light}")
            logger.info(f"[CCO:{config.id}] Phase 1/3: config")
            logger.info(separator_light)
            config_result = self._run_cco_config(project_dir, config.id, model)
            config_time = config_result["time"]
            if not config_result["success"]:
                logger.error(f"[CCO:{config.id}] Config phase FAILED: {config_result['error']}")
                # Capture context snapshot even on failure
                snapshot = _capture_context_snapshot(project_dir, variant, model, self.ccbox_cmd)
                _save_context_snapshot(project_dir, snapshot)
                return ExecutionResult(
                    project_id=config.id,
                    variant=variant,
                    success=False,
                    metrics=None,
                    score=0.0,
                    generation_time_seconds=round(config_time, 2),
                    prompt_used=config.prompt,
                    output_dir=str(project_dir),
                    command=config_result["command"],
                    exit_code=config_result["exit_code"],
                    stdout_excerpt=config_result["stdout"][-1000:]
                    if config_result["stdout"]
                    else "",
                    stderr_excerpt=config_result["stderr"][-1000:]
                    if config_result["stderr"]
                    else "",
                    error_message=f"CCO config failed: {config_result['error']}",
                    config_time_seconds=round(config_time, 2),
                )
            logger.info(f"[CCO:{config.id}] Config phase completed in {config_time:.2f}s")

        # Build ccbox command for the actual test
        # ccbox parameters (as of latest version):
        # -U: unrestricted mode (no CPU/I/O soft limits - required for benchmarking)
        # -y: unattended mode (deps=ALL, stack=auto-detect, no prompts)
        # -dd: debug logging (stream output)
        # -C: change directory
        # --bare: vanilla mode (no CCO rules)
        # -m/--model: model selection
        # -p/--prompt: initial prompt (enables --print mode)
        cmd = [self.ccbox_cmd, "-U", "-y", "-dd"]

        # Project directory (ccbox -C flag)
        cmd.extend(["-C", str(project_dir)])

        # Variant-specific flags
        if variant == "vanilla":
            cmd.append("--bare")  # No CCO rules
        # else: CCO variant - rules already configured in config phase

        # Common flags
        cmd.extend(
            [
                "-m",
                model,  # Model selection
                "-p",
                short_prompt,  # Short instruction, actual task is in _benchmark_prompt.md
            ]
        )

        start_time = time.time()
        cmd_str = " ".join(cmd)

        # Coding phase separator
        if variant == "cco":
            logger.info(f"\n{separator_light}")
            logger.info(f"[CCO:{config.id}] Phase 2/3: coding")
            logger.info(separator_light)
        else:
            logger.info(f"\n{separator_light}")
            logger.info(f"[VANILLA:{config.id}] coding")
            logger.info(separator_light)

        logger.info(f"[{variant.upper()}:{config.id}] Executing: {cmd_str[:200]}...")

        # Run with streaming for real-time output and activity tracking
        exit_code, stdout, stderr, activity = self._run_with_streaming(
            cmd=cmd,
            project_dir=project_dir,
            project_id=config.id,
            variant=variant,
            timeout=self.timeout,
            env={"CLAUDE_MODEL": model},
            log_phase="02_coding",
        )

        generation_time = time.time() - start_time

        # Handle FileNotFoundError (exit_code is None and no output)
        if exit_code is None and not stdout and not stderr:
            # Still capture snapshot for debugging
            snapshot = _capture_context_snapshot(project_dir, variant, model, self.ccbox_cmd)
            _save_context_snapshot(project_dir, snapshot)
            return ExecutionResult(
                project_id=config.id,
                variant=variant,
                success=False,
                metrics=None,
                score=0.0,
                generation_time_seconds=0.0,
                prompt_used=config.prompt,
                output_dir=str(project_dir),
                command=cmd_str,
                exit_code=None,
                error_message=f"ccbox command not found: {self.ccbox_cmd}",
            )

        # Determine success: exit_code == 0 OR jsonl contains successful result
        # ccbox can return exit_code=1 even when task succeeded if there's a
        # post-completion streaming mode error
        if exit_code == 0:
            success = True
            jsonl_error = None
        else:
            # Check jsonl output for actual success despite non-zero exit code
            success, jsonl_error = _check_jsonl_for_success(stdout)
            if success:
                logger.info(
                    f"[{variant.upper()}:{config.id}] Task completed successfully despite exit_code={exit_code} "
                    "(post-completion CLI error ignored)"
                )

        # Build stall info for error message
        stall_info = ""
        if activity.stall_warnings > 0:
            stall_info = f" ({activity.stall_warnings} stall warnings)"
        if activity.is_stalled:
            stall_info += " [STALLED]"

        # Save ccbox output with detailed info including activity
        log_content = f"""ccbox Execution Log ({variant})
{"=" * 60}
Command: {cmd_str}
Exit Code: {exit_code}
Duration: {generation_time:.2f}s
Success: {success}
Project Dir: {project_dir}
{"=" * 60}

ACTIVITY TRACKING:
- Total output lines: {activity.total_output_lines}
- Stall warnings: {activity.stall_warnings}
- Final stall state: {activity.is_stalled}
{"=" * 60}

STDOUT:
{stdout or "(empty)"}

{"=" * 60}
STDERR:
{stderr or "(empty)"}
"""
        log_dir = self._get_log_dir(config.id, variant)
        (log_dir / "02_coding.log").write_text(log_content, encoding="utf-8")
        (log_dir / "02_coding.jsonl").write_text(stdout, encoding="utf-8")
        (log_dir / "02_coding_errors.log").write_text(stderr, encoding="utf-8")

        if success:
            logger.info(f"[{variant.upper()}:{config.id}] SUCCESS in {generation_time:.2f}s{stall_info}")

            # CCO variant: Run cco-optimize --auto after successful test
            if variant == "cco":
                logger.info(f"\n{separator_light}")
                logger.info(f"[CCO:{config.id}] Phase 3/3: optimize")
                logger.info(separator_light)
                optimize_result = self._run_cco_optimize(project_dir, config.id, model)
                optimize_time = optimize_result["time"]
                optimize_success = optimize_result["success"]
                if optimize_success:
                    logger.info(f"[CCO:{config.id}] Optimize phase completed in {optimize_time:.2f}s")
                else:
                    # Non-blocking: log warning but continue with analysis
                    # Track error for visibility in results
                    optimize_error = optimize_result.get("error", "Unknown error")
                    logger.warning(f"[CCO:{config.id}] Optimize phase failed (non-blocking): {optimize_error}")
        else:
            if exit_code is None:
                logger.error(
                    f"[{variant.upper()}:{config.id}] TIMEOUT after {generation_time:.2f}s{stall_info}"
                )
            else:
                logger.error(f"[{variant.upper()}:{config.id}] FAILED with exit code {exit_code}{stall_info}")
            logger.error(f"[{variant.upper()}:{config.id}] stdout:\n{_truncate(stdout, 1500)}")
            logger.error(f"[{variant.upper()}:{config.id}] stderr:\n{_truncate(stderr, 1500)}")

        # Calculate total time (all phases)
        total_time = generation_time
        if config_time is not None:
            total_time += config_time
        if optimize_time is not None:
            total_time += optimize_time

        # Log CCO phase summary
        if variant == "cco":
            logger.info(
                f"[CCO:{config.id}] Phase timings: config={config_time:.2f}s, "
                f"coding={generation_time:.2f}s, "
                f"optimize={optimize_time:.2f}s, "
                f"total={total_time:.2f}s"
                if optimize_time is not None
                else f"[CCO:{config.id}] Phase timings: config={config_time:.2f}s, "
                f"coding={generation_time:.2f}s, total={total_time:.2f}s"
            )

        # Analyze generated code
        analyzer = CodeAnalyzer(project_dir)
        metrics = analyzer.analyze()
        metrics.name = config.name
        metrics.variant = variant
        metrics.generation_time_seconds = total_time
        # Use dimension-based overall_score (calculated by CodeAnalyzer)
        score = metrics.overall_score

        # Build detailed error message if failed
        error_msg = ""
        if not success:
            if exit_code is None:
                error_msg = f"Inactivity timeout ({self.timeout}s without output){stall_info}"
            else:
                error_msg = _parse_ccbox_error(stdout, stderr, exit_code) + stall_info

        # Capture context snapshot for verification
        snapshot = _capture_context_snapshot(project_dir, variant, model, self.ccbox_cmd)
        _save_context_snapshot(project_dir, snapshot)

        # Variant completion separator
        status = "SUCCESS" if success else "FAILED"
        logger.info(f"\n{separator_heavy}")
        logger.info(
            f"[{variant.upper()}:{config.id}] {status} (score={round(score, 1)}, time={total_time:.1f}s)"
        )
        logger.info(f"{separator_heavy}\n")

        # Generate summary.json for machine-readable results
        summary = {
            "project_id": config.id,
            "variant": variant,
            "success": success,
            "score": round(score, 1),
            "phases": {
                "config": {
                    "enabled": variant == "cco",
                    "time_seconds": round(config_time, 2) if config_time is not None else None,
                    "success": config_result.get("success")
                    if variant == "cco" and config_result
                    else None,
                },
                "coding": {
                    "time_seconds": round(generation_time, 2),
                    "exit_code": exit_code,
                    "success": success,
                    "stall_warnings": activity.stall_warnings,
                },
                "optimize": {
                    "enabled": variant == "cco" and success,
                    "time_seconds": round(optimize_time, 2) if optimize_time is not None else None,
                    "success": optimize_result.get("success")
                    if variant == "cco" and success and optimize_result
                    else None,
                },
            },
            "total_time_seconds": round(total_time, 2),
            "error_message": error_msg if error_msg else None,
        }
        (log_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

        return ExecutionResult(
            project_id=config.id,
            variant=variant,
            success=success,
            metrics=metrics,
            score=round(score, 1),
            generation_time_seconds=round(total_time, 2),
            prompt_used=config.prompt,
            output_dir=str(project_dir),
            command=cmd_str,
            exit_code=exit_code,
            stdout_excerpt=stdout[-1000:] if stdout else "",
            stderr_excerpt=stderr[-1000:] if stderr else "",
            error_message=error_msg,
            config_time_seconds=round(config_time, 2) if config_time is not None else None,
            coding_time_seconds=round(generation_time, 2),
            optimize_time_seconds=round(optimize_time, 2) if optimize_time is not None else None,
            optimize_success=optimize_success,
            optimize_error=optimize_error,
        )

    # =========================================================================
    # Benchmark Flow: Vanilla → Derive CCO → Optimize → Review → Analyze
    # =========================================================================

    def run_benchmark(
        self,
        config: ProjectConfig,
        model: str = "opus",
        progress_callback: Callable[[str, BenchmarkPhase], None] | None = None,
        resume: bool = False,
    ) -> NewBenchmarkResult:
        """Run new benchmark flow: vanilla → derive CCO → optimize → review → analyze both.

        New flow where CCO optimizes vanilla code instead of generating from scratch.
        This measures CCO's actual optimization capability, not code generation.

        Args:
            config: Project configuration
            model: AI model to use (opus, sonnet, haiku)
            progress_callback: Called after each phase completion
            resume: If True, skip completed phases and continue from where it left off

        Phases:
        1. vanilla_generation: Generate vanilla project from scratch
        2. vanilla_analysis: Static + AI analysis of vanilla code
        3. cco_derive: Copy vanilla to create CCO base (identical starting point)
        4. cco_config: Run /cco-config --auto
        5. cco_optimize: Run /cco-optimize --auto (all 6 scopes, full fix)
        6. cco_review: Run /cco-review --auto (all 5 scopes, full fix)
        7. cco_analysis: Static + AI analysis of CCO-optimized code

        Returns:
            NewBenchmarkResult with all phase results and pre-computed comparison
        """
        from .ai_evaluator import run_single_variant_ai_analysis

        phases: list[BenchmarkPhase] = []
        separator = "═" * 60
        vanilla_dir = self.output_base / f"{config.id}_vanilla"
        cco_dir = self.output_base / f"{config.id}_cco"

        # Check resume state if resuming
        resume_state: ResumeState | None = None
        if resume:
            resume_state = self._check_resume_state(config)

        def _report_phase(phase: BenchmarkPhase) -> None:
            """Report phase completion to callback and logger."""
            phases.append(phase)
            status = "✓" if phase.success else "✗"
            logger.info(f"[BENCHMARK:{config.id}] {status} {phase.name} ({phase.duration_seconds:.1f}s)")
            if progress_callback:
                try:
                    progress_callback(f"Phase completed: {phase.name}", phase)
                except Exception:
                    pass

        def _report_skipped(phase_name: str) -> None:
            """Report skipped phase (resume mode)."""
            phase = BenchmarkPhase(name=phase_name, success=True, duration_seconds=0.0, skipped=True)
            phases.append(phase)
            logger.info(f"[BENCHMARK:{config.id}] ⏭ {phase_name} (skipped - resume)")
            if progress_callback:
                try:
                    progress_callback(f"Phase skipped: {phase_name}", phase)
                except Exception:
                    pass

        logger.info(f"\n{separator}")
        if resume and resume_state:
            logger.info(f"[BENCHMARK:{config.id}] RESUMING FROM PHASE {resume_state.resume_from_phase}")
        else:
            logger.info(f"[BENCHMARK:{config.id}] STARTING NEW BENCHMARK FLOW")
        logger.info(separator)

        # ─────────────────────────────────────────────────────────────────────
        # Phase 1: Vanilla Generation
        # ─────────────────────────────────────────────────────────────────────
        if resume_state and resume_state.can_skip_vanilla_generation:
            logger.info(f"\n[BENCHMARK:{config.id}] Phase 1/7: vanilla_generation (SKIPPING)")
            _report_skipped("vanilla_generation")
        else:
            logger.info(f"\n[BENCHMARK:{config.id}] Phase 1/7: vanilla_generation")
            phase1 = self._run_vanilla_generation(config, vanilla_dir, model)
            _report_phase(phase1)

            if not phase1.success:
                return self._build_failed_result(
                    config, phases, f"Vanilla generation failed: {phase1.error}"
                )

        # ─────────────────────────────────────────────────────────────────────
        # Phase 2: Vanilla Analysis (Static + AI)
        # ─────────────────────────────────────────────────────────────────────
        vanilla_metrics: Metrics | None = None
        vanilla_ai_result: dict[str, Any] | None = None

        if resume_state and resume_state.can_skip_vanilla_analysis:
            logger.info(f"\n[BENCHMARK:{config.id}] Phase 2/7: vanilla_analysis (SKIPPING)")
            _report_skipped("vanilla_analysis")
            vanilla_metrics = resume_state.vanilla_metrics
            vanilla_ai_result = resume_state.vanilla_ai_result
        else:
            logger.info(f"\n[BENCHMARK:{config.id}] Phase 2/7: vanilla_analysis")
            phase2 = self._run_variant_analysis(
                config.id, vanilla_dir, "vanilla", config.prompt, run_single_variant_ai_analysis
            )
            _report_phase(phase2)

            vanilla_metrics = phase2.output.get("metrics") if phase2.output else None
            vanilla_ai_result = phase2.output.get("ai_result") if phase2.output else None

            # Save for future resume
            self._save_analysis_results(config.id, "vanilla", vanilla_metrics, vanilla_ai_result)

        # ─────────────────────────────────────────────────────────────────────
        # Phase 3: CCO Derivation (Copy from Vanilla - identical starting point)
        # ─────────────────────────────────────────────────────────────────────
        if resume_state and resume_state.can_skip_cco_derive:
            logger.info(f"\n[BENCHMARK:{config.id}] Phase 3/7: cco_derive (SKIPPING)")
            _report_skipped("cco_derive")
        else:
            logger.info(f"\n[BENCHMARK:{config.id}] Phase 3/7: cco_derive")
            phase3 = self._derive_cco_from_vanilla(vanilla_dir, cco_dir)
            _report_phase(phase3)

            if not phase3.success:
                return self._build_failed_result(
                    config, phases, f"CCO derivation failed: {phase3.error}",
                    vanilla_metrics=vanilla_metrics, vanilla_ai_result=vanilla_ai_result
                )

        # ─────────────────────────────────────────────────────────────────────
        # Phase 4: CCO Config
        # ─────────────────────────────────────────────────────────────────────
        if resume_state and resume_state.can_skip_cco_config:
            logger.info(f"\n[BENCHMARK:{config.id}] Phase 4/7: cco_config (SKIPPING)")
            _report_skipped("cco_config")
        else:
            logger.info(f"\n[BENCHMARK:{config.id}] Phase 4/7: cco_config")
            phase4 = self._run_cco_config(cco_dir, config.id, model)
            _report_phase(phase4)

            if not phase4.success:
                return self._build_failed_result(
                    config, phases, f"CCO config failed: {phase4.error}",
                    vanilla_metrics=vanilla_metrics, vanilla_ai_result=vanilla_ai_result
                )

        # ─────────────────────────────────────────────────────────────────────
        # Phase 5: CCO Optimize (--auto = all 6 scopes, full fix)
        # ─────────────────────────────────────────────────────────────────────
        logger.info(f"\n[BENCHMARK:{config.id}] Phase 5/7: cco_optimize")
        phase5 = self._run_cco_optimize(cco_dir, config.id, model)
        _report_phase(phase5)
        # Optimize failure is non-blocking but logged

        # ─────────────────────────────────────────────────────────────────────
        # Phase 6: CCO Review (--auto = all 5 scopes, full fix)
        # ─────────────────────────────────────────────────────────────────────
        logger.info(f"\n[BENCHMARK:{config.id}] Phase 6/7: cco_review")
        phase6 = self._run_cco_review(cco_dir, config.id, model)
        _report_phase(phase6)
        # Review failure is non-blocking but logged

        # ─────────────────────────────────────────────────────────────────────
        # Phase 7: CCO Analysis (Static + AI)
        # ─────────────────────────────────────────────────────────────────────
        logger.info(f"\n[BENCHMARK:{config.id}] Phase 7/7: cco_analysis")
        phase7 = self._run_variant_analysis(
            config.id, cco_dir, "cco", config.prompt, run_single_variant_ai_analysis
        )
        _report_phase(phase7)

        cco_metrics = phase7.output.get("metrics") if phase7.output else None
        cco_ai_result = phase7.output.get("ai_result") if phase7.output else None

        # Save for potential debugging (CCO analysis is always re-run, but good to have)
        self._save_analysis_results(config.id, "cco", cco_metrics, cco_ai_result)

        # ─────────────────────────────────────────────────────────────────────
        # Build comparison from pre-computed analyses
        # ─────────────────────────────────────────────────────────────────────
        comparison = self._build_comparison(
            vanilla_metrics, vanilla_ai_result, cco_metrics, cco_ai_result
        )

        # Final summary
        total_time = sum(p.duration_seconds for p in phases)
        successful_phases = sum(1 for p in phases if p.success)
        logger.info(f"\n{separator}")
        logger.info(f"[BENCHMARK:{config.id}] COMPLETED: {successful_phases}/7 phases successful")
        logger.info(f"[BENCHMARK:{config.id}] Total time: {total_time:.1f}s")
        logger.info(f"[BENCHMARK:{config.id}] Verdict: {comparison.get('verdict', 'N/A')}")
        logger.info(separator)

        return NewBenchmarkResult(
            project_id=config.id,
            project_name=config.name,
            phases=phases,
            vanilla_metrics=vanilla_metrics,
            vanilla_ai_result=vanilla_ai_result,
            cco_metrics=cco_metrics,
            cco_ai_result=cco_ai_result,
            comparison=comparison,
            categories=config.categories,
            complexity=config.complexity,
        )

    def _run_vanilla_generation(
        self, config: ProjectConfig, vanilla_dir: Path, model: str
    ) -> BenchmarkPhase:
        """Phase 1: Generate vanilla project from scratch using ccbox --bare."""
        start = time.time()

        # Clean existing folder
        if vanilla_dir.exists():
            shutil.rmtree(vanilla_dir)
        vanilla_dir.mkdir(parents=True, exist_ok=True)

        # Save prompt to file
        prompt_file = vanilla_dir / "_benchmark_prompt.md"
        prompt_file.write_text(config.prompt, encoding="utf-8")

        short_prompt = """Read _benchmark_prompt.md and complete all tasks described in it.

CRITICAL CONSTRAINTS:
- Do NOT use slash commands (/, /help, /commit, etc.) - they are not available in this mode
- Do NOT ask follow-up questions or request user input
- When finished, simply summarize what was built - do not attempt any post-completion commands
- Focus only on writing code, tests, and configuration files

Execute the task autonomously and completely."""

        cmd = [
            self.ccbox_cmd, "-U", "-y", "-dd",
            "-C", str(vanilla_dir),
            "--bare",  # No CCO rules
            "-m", model,
            "-p", short_prompt,
        ]

        try:
            exit_code, stdout, stderr, activity = self._run_with_streaming(
                cmd=cmd,
                project_dir=vanilla_dir,
                project_id=config.id,
                variant="vanilla",
                timeout=self.timeout,
                env={"CLAUDE_MODEL": model},
                log_phase="01_generation",
            )

            elapsed = time.time() - start

            # Save logs
            log_dir = self._get_log_dir(config.id, "vanilla")
            (log_dir / "01_generation.log").write_text(
                f"Vanilla Generation\nCommand: {' '.join(cmd)}\n"
                f"Exit: {exit_code}\nDuration: {elapsed:.1f}s\n\n{stdout}",
                encoding="utf-8"
            )
            (log_dir / "01_generation.jsonl").write_text(stdout, encoding="utf-8")

            # Check success
            if exit_code == 0:
                success = True
            else:
                success, _ = _check_jsonl_for_success(stdout)

            if success:
                return BenchmarkPhase(
                    name="vanilla_generation",
                    success=True,
                    duration_seconds=elapsed,
                )
            else:
                error = _parse_ccbox_error(stdout, stderr, exit_code or -1)
                return BenchmarkPhase(
                    name="vanilla_generation",
                    success=False,
                    duration_seconds=elapsed,
                    error=error,
                )

        except Exception as e:
            return BenchmarkPhase(
                name="vanilla_generation",
                success=False,
                duration_seconds=time.time() - start,
                error=str(e),
            )

    def _derive_cco_from_vanilla(self, vanilla_dir: Path, cco_dir: Path) -> BenchmarkPhase:
        """Phase 3: Copy vanilla to create CCO base (identical starting point)."""
        start = time.time()
        try:
            logger.info(f"[CCO Derive] Copying {vanilla_dir} to {cco_dir}")

            if cco_dir.exists():
                logger.info(f"[CCO Derive] Removing existing cco_dir: {cco_dir}")
                shutil.rmtree(cco_dir)

            # Use copytree to create exact copy (ignore symlinks to avoid issues)
            shutil.copytree(vanilla_dir, cco_dir, symlinks=False, ignore_dangling_symlinks=True)
            logger.info("[CCO Derive] Copy completed")

            # Count files (skip verification to avoid issues with symlinks/.venv)
            try:
                file_count = sum(1 for f in cco_dir.rglob("*") if f.is_file())
                logger.info(f"[CCO Derive] Files copied: {file_count}")
            except Exception as count_err:
                logger.warning(f"[CCO Derive] Could not count files: {count_err}")
                file_count = -1

            return BenchmarkPhase(
                name="cco_derive",
                success=True,
                duration_seconds=time.time() - start,
                output={"files_copied": file_count},
            )
        except Exception as e:
            error_msg = f"{type(e).__name__}: {e}"
            logger.error(f"[CCO Derive] FAILED: {error_msg}")
            return BenchmarkPhase(
                name="cco_derive",
                success=False,
                duration_seconds=time.time() - start,
                error=error_msg,
            )

    def _run_cco_config(self, cco_dir: Path, project_id: str, model: str) -> BenchmarkPhase:
        """Phase 4: Run /cco-config --auto to configure CCO rules."""
        start = time.time()

        cmd = [
            self.ccbox_cmd, "-U", "-y", "-dd",
            "-C", str(cco_dir),
            "-m", model,
            "-p", "/cco-config --auto --target-dir .claude",
        ]

        try:
            exit_code, stdout, stderr, _ = self._run_with_streaming(
                cmd=cmd,
                project_dir=cco_dir,
                project_id=project_id,
                variant="cco",
                timeout=float(self.phase_timeout),
                env={"CLAUDE_MODEL": model},
                log_phase="02_config",
            )

            elapsed = time.time() - start

            # Save logs
            log_dir = self._get_log_dir(project_id, "cco")
            (log_dir / "02_config.log").write_text(
                f"CCO Config\nCommand: {' '.join(cmd)}\n"
                f"Exit: {exit_code}\nDuration: {elapsed:.1f}s\n\n{stdout}",
                encoding="utf-8"
            )
            (log_dir / "02_config.jsonl").write_text(stdout, encoding="utf-8")

            if exit_code == 0:
                return BenchmarkPhase(
                    name="cco_config",
                    success=True,
                    duration_seconds=elapsed,
                )
            else:
                error = _parse_ccbox_error(stdout, stderr, exit_code or -1)
                return BenchmarkPhase(
                    name="cco_config",
                    success=False,
                    duration_seconds=elapsed,
                    error=error,
                )

        except Exception as e:
            return BenchmarkPhase(
                name="cco_config",
                success=False,
                duration_seconds=time.time() - start,
                error=str(e),
            )

    def _run_cco_optimize(self, cco_dir: Path, project_id: str, model: str) -> BenchmarkPhase:
        """Phase 5: Run /cco-optimize --auto (all 6 scopes, full fix, silent)."""
        start = time.time()

        cmd = [
            self.ccbox_cmd, "-U", "-y", "-dd",
            "-C", str(cco_dir),
            "-m", model,
            "-p", "/cco-optimize --auto",  # All 6 scopes, full fix, silent
        ]

        try:
            exit_code, stdout, stderr, _ = self._run_with_streaming(
                cmd=cmd,
                project_dir=cco_dir,
                project_id=project_id,
                variant="cco",
                timeout=float(self.phase_timeout),
                env={"CLAUDE_MODEL": model},
                log_phase="03_optimize",
            )

            elapsed = time.time() - start

            # Save logs
            log_dir = self._get_log_dir(project_id, "cco")
            (log_dir / "03_optimize.log").write_text(
                f"CCO Optimize\nCommand: {' '.join(cmd)}\n"
                f"Exit: {exit_code}\nDuration: {elapsed:.1f}s\n\n{stdout}",
                encoding="utf-8"
            )
            (log_dir / "03_optimize.jsonl").write_text(stdout, encoding="utf-8")

            if exit_code == 0:
                return BenchmarkPhase(
                    name="cco_optimize",
                    success=True,
                    duration_seconds=elapsed,
                )
            else:
                error = _parse_ccbox_error(stdout, stderr, exit_code or -1)
                return BenchmarkPhase(
                    name="cco_optimize",
                    success=False,
                    duration_seconds=elapsed,
                    error=error,
                )

        except Exception as e:
            return BenchmarkPhase(
                name="cco_optimize",
                success=False,
                duration_seconds=time.time() - start,
                error=str(e),
            )

    def _run_cco_review(self, cco_dir: Path, project_id: str, model: str) -> BenchmarkPhase:
        """Phase 6: Run /cco-review --auto (all 5 scopes, full fix, silent)."""
        start = time.time()

        cmd = [
            self.ccbox_cmd, "-U", "-y", "-dd",
            "-C", str(cco_dir),
            "-m", model,
            "-p", "/cco-review --auto",  # All 5 scopes, full fix, silent
        ]

        try:
            exit_code, stdout, stderr, _ = self._run_with_streaming(
                cmd=cmd,
                project_dir=cco_dir,
                project_id=project_id,
                variant="cco",
                timeout=float(self.phase_timeout),
                env={"CLAUDE_MODEL": model},
                log_phase="04_review",
            )

            elapsed = time.time() - start

            # Save logs
            log_dir = self._get_log_dir(project_id, "cco")
            (log_dir / "04_review.log").write_text(
                f"CCO Review\nCommand: {' '.join(cmd)}\n"
                f"Exit: {exit_code}\nDuration: {elapsed:.1f}s\n\n{stdout}",
                encoding="utf-8"
            )
            (log_dir / "04_review.jsonl").write_text(stdout, encoding="utf-8")

            if exit_code == 0:
                return BenchmarkPhase(
                    name="cco_review",
                    success=True,
                    duration_seconds=elapsed,
                )
            else:
                error = _parse_ccbox_error(stdout, stderr, exit_code or -1)
                return BenchmarkPhase(
                    name="cco_review",
                    success=False,
                    duration_seconds=elapsed,
                    error=error,
                )

        except Exception as e:
            return BenchmarkPhase(
                name="cco_review",
                success=False,
                duration_seconds=time.time() - start,
                error=str(e),
            )

    def _run_variant_analysis(
        self,
        project_id: str,
        variant_dir: Path,
        variant: str,
        original_prompt: str,
        ai_analysis_func: Callable[..., dict[str, Any]],
    ) -> BenchmarkPhase:
        """Phase 2/7: Run both static and AI analysis on a single variant."""
        start = time.time()
        output: dict[str, Any] = {}

        try:
            # Static analysis using CodeAnalyzer
            analyzer = CodeAnalyzer(variant_dir)
            metrics = analyzer.analyze()
            metrics.name = project_id
            metrics.variant = variant
            output["metrics"] = metrics

            # AI analysis (single variant evaluation)
            ai_result = ai_analysis_func(
                project_id=project_id,
                variant_dir=variant_dir,
                variant=variant,
                original_prompt=original_prompt,
                suite_dir=self.output_base.parent / "suite",
            )
            output["ai_result"] = ai_result

            # Save analysis results
            log_dir = self._get_log_dir(project_id, variant)
            phase_num = "02" if variant == "vanilla" else "05"
            (log_dir / f"{phase_num}_analysis_static.json").write_text(
                json.dumps(metrics.to_dict(), indent=2), encoding="utf-8"
            )
            (log_dir / f"{phase_num}_analysis_ai.json").write_text(
                json.dumps(ai_result, indent=2, default=str), encoding="utf-8"
            )

            return BenchmarkPhase(
                name=f"{variant}_analysis",
                success=True,
                duration_seconds=time.time() - start,
                output=output,
            )

        except Exception as e:
            logger.error(f"[BENCHMARK:{project_id}] Analysis failed for {variant}: {e}")
            return BenchmarkPhase(
                name=f"{variant}_analysis",
                success=False,
                duration_seconds=time.time() - start,
                error=str(e),
                output=output,  # Include partial results
            )

    def _build_comparison(
        self,
        vanilla_metrics: Metrics | None,
        vanilla_ai: dict[str, Any] | None,
        cco_metrics: Metrics | None,
        cco_ai: dict[str, Any] | None,
    ) -> dict[str, Any]:
        """Build comparison from pre-computed analyses."""
        comparison: dict[str, Any] = {
            "score_improvement": 0.0,
            "dimension_improvements": [],
            "verdict": "Analysis Incomplete",
        }

        # Static metrics comparison
        if vanilla_metrics and cco_metrics:
            vanilla_score = vanilla_metrics.overall_score
            cco_score = cco_metrics.overall_score
            diff = cco_score - vanilla_score
            comparison["score_improvement"] = round(diff, 1)
            comparison["vanilla_score"] = round(vanilla_score, 1)
            comparison["cco_score"] = round(cco_score, 1)

            # Use existing compare_metrics for detailed comparison
            detailed = compare_metrics(cco_metrics, vanilla_metrics)
            comparison["detailed_comparison"] = detailed
            comparison["verdict"] = calculate_verdict(diff)

        # AI analysis comparison (if both available)
        if vanilla_ai and cco_ai:
            ai_comparison = self._compare_ai_analyses(vanilla_ai, cco_ai)
            comparison["ai_comparison"] = ai_comparison

            # Calculate AI-based improvement
            vanilla_ai_score = vanilla_ai.get("overall_score", 0)
            cco_ai_score = cco_ai.get("overall_score", 0)
            comparison["ai_score_improvement"] = round(cco_ai_score - vanilla_ai_score, 1)

        return comparison

    def _compare_ai_analyses(
        self, vanilla_ai: dict[str, Any], cco_ai: dict[str, Any]
    ) -> dict[str, Any]:
        """Compare two AI analysis results dimension by dimension."""
        dimensions = [
            "functional_completeness", "correctness_robustness", "architecture",
            "code_quality", "security", "type_safety", "testing",
            "maintainability", "performance", "best_practices"
        ]

        dimension_diffs = []
        for dim in dimensions:
            vanilla_dim = vanilla_ai.get(dim, {})
            cco_dim = cco_ai.get(dim, {})

            vanilla_score = vanilla_dim.get("score", 0) if isinstance(vanilla_dim, dict) else 0
            cco_score = cco_dim.get("score", 0) if isinstance(cco_dim, dict) else 0

            diff = cco_score - vanilla_score
            # Winner: any positive diff = CCO, any negative = Vanilla, zero = tie
            winner = "cco" if diff > 0 else ("vanilla" if diff < 0 else "tie")
            dimension_diffs.append({
                "dimension": dim,
                "vanilla_score": vanilla_score,
                "cco_score": cco_score,
                "improvement": round(diff, 1),
                "winner": winner,
            })

        cco_wins = sum(1 for d in dimension_diffs if d["winner"] == "cco")
        vanilla_wins = sum(1 for d in dimension_diffs if d["winner"] == "vanilla")

        return {
            "dimension_breakdown": dimension_diffs,
            "cco_wins": cco_wins,
            "vanilla_wins": vanilla_wins,
            "ties": len(dimensions) - cco_wins - vanilla_wins,
        }

    def _build_failed_result(
        self,
        config: ProjectConfig,
        phases: list[BenchmarkPhase],
        error: str,
        vanilla_metrics: Metrics | None = None,
        vanilla_ai_result: dict[str, Any] | None = None,
    ) -> NewBenchmarkResult:
        """Build a failed result when benchmark cannot complete."""
        return NewBenchmarkResult(
            project_id=config.id,
            project_name=config.name,
            phases=phases,
            vanilla_metrics=vanilla_metrics,
            vanilla_ai_result=vanilla_ai_result,
            cco_metrics=None,
            cco_ai_result=None,
            comparison={"error": error, "verdict": "Failed"},
            categories=config.categories,
            complexity=config.complexity,
        )


class ResultsManager:
    """Manages benchmark results storage and retrieval."""

    def __init__(self, results_dir: Path):
        self.results_dir = results_dir
        self.results_dir.mkdir(parents=True, exist_ok=True)

    def save_result(self, result: BenchmarkResult) -> Path:
        """Save a benchmark result to JSON."""
        filename = f"{result.project_id}_{result.timestamp.replace(':', '-')}.json"
        filepath = self.results_dir / filename

        filepath.write_text(json.dumps(result.to_dict(), indent=2), encoding="utf-8")
        return filepath

    def load_result(self, filepath: Path) -> BenchmarkResult:
        """Load a benchmark result from JSON."""
        data = json.loads(filepath.read_text(encoding="utf-8"))
        return BenchmarkResult.from_dict(data)

    def list_results(self) -> list[Path]:
        """List all saved results."""
        return sorted(self.results_dir.glob("*.json"), reverse=True)

    def get_latest_results(self, limit: int = 10) -> list[BenchmarkResult]:
        """Get the most recent results."""
        files = self.list_results()[:limit]
        return [self.load_result(f) for f in files]

    def get_summary(self) -> dict[str, Any]:
        """Get summary statistics across all results."""
        results = [self.load_result(f) for f in self.list_results()]

        if not results:
            return {"total_runs": 0}

        cco_wins = sum(1 for r in results if r.score_difference > 5)
        vanilla_wins = sum(1 for r in results if r.score_difference < -5)
        mixed = len(results) - cco_wins - vanilla_wins

        avg_cco_score = sum(r.cco_result.score for r in results) / len(results)
        avg_vanilla_score = sum(r.vanilla_result.score for r in results) / len(results)
        avg_diff = sum(r.score_difference for r in results) / len(results)

        return {
            "total_runs": len(results),
            "cco_wins": cco_wins,
            "vanilla_wins": vanilla_wins,
            "mixed": mixed,
            "avg_cco_score": round(avg_cco_score, 1),
            "avg_vanilla_score": round(avg_vanilla_score, 1),
            "avg_difference": round(avg_diff, 1),
            "by_project": self._group_by_project(results),
        }

    def _group_by_project(self, results: list[BenchmarkResult]) -> dict[str, Any]:
        """Group results by project."""
        grouped: dict[str, list[BenchmarkResult]] = {}
        for r in results:
            if r.project_id not in grouped:
                grouped[r.project_id] = []
            grouped[r.project_id].append(r)

        summary = {}
        for project_id, project_results in grouped.items():
            avg_diff = sum(r.score_difference for r in project_results) / len(project_results)
            summary[project_id] = {
                "runs": len(project_results),
                "avg_difference": round(avg_diff, 1),
                "latest_verdict": project_results[0].verdict,
            }

        return summary


def discover_projects(projects_dir: Path) -> list[ProjectConfig]:
    """Discover all benchmark projects."""
    projects = []
    for subdir in sorted(projects_dir.iterdir()):
        if subdir.is_dir() and (subdir / "PROMPT.md").exists():
            projects.append(ProjectConfig(subdir))
    return projects
