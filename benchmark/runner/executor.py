"""
Test executor for CCO benchmarks.

Runs projects through ccbox (vanilla and cco modes) and collects results.

ccbox behavior:
- Mounts current working directory as project root
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
    calculate_overall_score,
    calculate_verdict,
    compare_metrics,
)

# Configure logger for detailed debugging
logger = logging.getLogger("cco-benchmark.executor")

# Platform detection for select compatibility
IS_WINDOWS = sys.platform == "win32"


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


def _truncate(text: str, max_len: int = 1000) -> str:
    """Truncate text with ellipsis indicator."""
    if len(text) <= max_len:
        return text
    return text[:max_len] + f"\n... [truncated, {len(text) - max_len} more chars]"


def _parse_ccbox_error(stdout: str, stderr: str, exit_code: int) -> str:
    """Parse ccbox output to extract meaningful error message."""
    error_parts = []

    # Check for common ccbox errors
    combined = (stdout + stderr).lower()

    if "docker" in combined and ("not found" in combined or "not running" in combined):
        error_parts.append("Docker issue detected")
    if "permission denied" in combined:
        error_parts.append("Permission denied (check Docker permissions)")
    if "no such file" in combined or "not found" in combined:
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

    status.ready = status.docker_installed and status.docker_running and status.ccbox_installed
    return status


@dataclass
class ExecutionResult:
    """Result of a single test execution."""

    project_id: str
    variant: str  # "cco" or "vanilla"
    success: bool
    metrics: Metrics | None
    score: float
    generation_time_seconds: float
    prompt_used: str
    error_message: str = ""
    output_dir: str = ""
    command: str = ""  # Full command executed
    exit_code: int | None = None
    stdout_excerpt: str = ""  # Last 500 chars of stdout
    stderr_excerpt: str = ""  # Last 500 chars of stderr
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict[str, Any]:
        return {
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
    """

    def __init__(
        self,
        output_base: Path,
        ccbox_cmd: str = "ccbox",
        timeout_seconds: int = 300,  # Inactivity timeout (5 min no output = stuck)
        stall_threshold: float = 120.0,
        progress_callback: Callable[[str, ActivityState], None] | None = None,
        streaming: bool = True,
    ):
        self.output_base = output_base
        self.ccbox_cmd = ccbox_cmd
        self.timeout = timeout_seconds
        self.setup_timeout = 120  # 2 minutes for CCO setup
        self.stall_threshold = stall_threshold  # Seconds without output = stall warning
        self.progress_callback = progress_callback
        self.streaming = streaming
        self.output_base.mkdir(parents=True, exist_ok=True)

    def _run_with_streaming(
        self,
        cmd: list[str],
        project_dir: Path,
        variant: str,
        timeout: float,
        env: dict[str, str] | None = None,
    ) -> tuple[int | None, str, str, ActivityState]:
        """Run command with real-time output streaming and activity tracking.

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
                        msg = f"[{variant.upper()}] [{stream_name}] {line_stripped}"
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
                        f"[{variant.upper()}] TIMEOUT - no output for {inactivity:.0f}s "
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
                    activity.stall_warnings += 1
                    stall_time = now - activity.last_output_time

                    # Check file activity as secondary indicator
                    if now - activity.last_file_check_time > file_check_interval:
                        current_files = _count_project_files(project_dir)
                        file_change = current_files - activity.last_file_count
                        activity.last_file_count = current_files
                        activity.last_file_check_time = now

                        if file_change > 0:
                            logger.info(
                                f"[{variant.upper()}] [ACTIVITY] No output for {stall_time:.0f}s "
                                f"but {file_change} new files created - still working"
                            )
                            activity.is_stalled = False
                        else:
                            logger.warning(
                                f"[{variant.upper()}] [STALL] No output for {stall_time:.0f}s, "
                                f"no new files - may be stuck (warning #{activity.stall_warnings})"
                            )
                    else:
                        logger.warning(
                            f"[{variant.upper()}] [STALL] No output for {stall_time:.0f}s "
                            f"(warning #{activity.stall_warnings})"
                        )

            # Periodic log flush
            if now - last_log_flush > log_flush_interval:
                last_log_flush = now
                try:
                    with lock:
                        if stdout_lines:
                            (project_dir / "_ccbox_stdout.log").write_text(
                                "".join(stdout_lines), encoding="utf-8"
                            )
                        if stderr_lines:
                            (project_dir / "_ccbox_stderr.log").write_text(
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

    def _run_cco_setup(self, project_dir: Path, model: str) -> dict[str, Any]:
        """Run cco-config --auto to setup CCO rules before the actual test.

        This runs in a separate ccbox invocation so that:
        1. CCO rules are configured and persisted
        2. Container restarts with rules in context

        Uses streaming mode with inactivity-based timeout - the process continues
        as long as output is being produced.

        Returns:
            Dict with success, time, command, exit_code, stdout, stderr, error
        """
        # ccbox parameters (as of latest version):
        # -y: unattended mode (deps=ALL, stack=auto-detect, no prompts)
        # -dd: debug logging (stream output)
        # -C: change directory
        # -m/--model: model selection
        # -p/--prompt: initial prompt (enables --print mode)
        cmd = [
            self.ccbox_cmd,
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

        logger.info(f"[CCO Setup] Starting: {cmd_str}")
        logger.info(f"[CCO Setup] Project dir: {project_dir}")
        logger.info(f"[CCO Setup] Using inactivity timeout: {self.setup_timeout}s")

        try:
            # Use streaming mode with inactivity-based timeout
            exit_code, stdout, stderr, activity = self._run_with_streaming(
                cmd=cmd,
                project_dir=project_dir,
                variant="cco-setup",
                timeout=float(self.setup_timeout),
                env={"CLAUDE_MODEL": model},
            )

            elapsed = time.time() - start_time

            # Save setup logs with detailed info
            log_content = f"""CCO Setup Log (Streaming Mode)
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
            (project_dir / "_cco_setup.log").write_text(log_content, encoding="utf-8")
            (project_dir / "_cco_setup_stdout.log").write_text(stdout, encoding="utf-8")
            (project_dir / "_cco_setup_stderr.log").write_text(stderr, encoding="utf-8")

            # Handle FileNotFoundError (exit_code is None and no output)
            if exit_code is None and not stdout and not stderr:
                error_msg = f"ccbox command not found: {self.ccbox_cmd}"
                logger.error(f"[CCO Setup] {error_msg}")
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
                error_msg = f"Setup inactivity timeout after {self.setup_timeout}s without output"
                logger.error(f"[CCO Setup] TIMEOUT: {error_msg}")
                logger.error(f"[CCO Setup] Partial stdout:\n{_truncate(stdout, 1000)}")
                logger.error(f"[CCO Setup] Partial stderr:\n{_truncate(stderr, 1000)}")
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
                logger.error(f"[CCO Setup] FAILED: {error_msg}")
                logger.error(f"[CCO Setup] Full stdout:\n{_truncate(stdout, 2000)}")
                logger.error(f"[CCO Setup] Full stderr:\n{_truncate(stderr, 2000)}")

                return {
                    "success": False,
                    "time": elapsed,
                    "command": cmd_str,
                    "exit_code": exit_code,
                    "stdout": stdout,
                    "stderr": stderr,
                    "error": error_msg,
                }

            logger.info(f"[CCO Setup] SUCCESS in {elapsed:.2f}s")
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
            logger.error(f"[CCO Setup] EXCEPTION: {error_msg}")
            logger.error(f"[CCO Setup] Traceback:\n{traceback.format_exc()}")
            return {
                "success": False,
                "time": elapsed,
                "command": cmd_str,
                "exit_code": None,
                "stdout": "",
                "stderr": "",
                "error": error_msg,
            }

    def _run_cco_optimize(self, project_dir: Path, model: str) -> dict[str, Any]:
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
        logger.info(f"[CCO Optimize] Using inactivity timeout: {self.setup_timeout}s")

        try:
            # Use streaming mode with inactivity-based timeout
            exit_code, stdout, stderr, activity = self._run_with_streaming(
                cmd=cmd,
                project_dir=project_dir,
                variant="cco-optimize",
                timeout=float(self.setup_timeout),
                env={"CLAUDE_MODEL": model},
            )

            elapsed = time.time() - start_time

            # Save optimize logs
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
            (project_dir / "_cco_optimize.log").write_text(log_content, encoding="utf-8")

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
                    f"Optimize inactivity timeout after {self.setup_timeout}s without output"
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
        logger.info(f"[{variant.upper()}] Starting project: {config.id}")

        # Fixed folder name (no timestamp) - same test always uses same folder
        project_dir = self.output_base / f"{config.id}_{variant}"

        # Clean existing folder before run
        if project_dir.exists():
            logger.info(f"[{variant.upper()}] Cleaning existing folder: {project_dir}")
            shutil.rmtree(project_dir)

        project_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"[{variant.upper()}] Output dir: {project_dir}")

        # Save prompt to file - ccbox will read from here instead of command line
        # This avoids Windows command line length limits (~8192 chars) and shell escaping issues
        prompt_file = project_dir / "_benchmark_prompt.md"
        prompt_file.write_text(config.prompt, encoding="utf-8")

        # Short instruction for ccbox - actual task is in the file
        short_prompt = "Read _benchmark_prompt.md and complete all tasks described in it. Follow the requirements exactly."

        # CCO variant: First run cco-config --auto to setup rules
        if variant == "cco":
            logger.info("[CCO] Running setup phase...")
            setup_result = self._run_cco_setup(project_dir, model)
            if not setup_result["success"]:
                logger.error(f"[CCO] Setup phase FAILED: {setup_result['error']}")
                return ExecutionResult(
                    project_id=config.id,
                    variant=variant,
                    success=False,
                    metrics=None,
                    score=0.0,
                    generation_time_seconds=setup_result["time"],
                    prompt_used=config.prompt,
                    output_dir=str(project_dir),
                    command=setup_result["command"],
                    exit_code=setup_result["exit_code"],
                    stdout_excerpt=setup_result["stdout"][-1000:] if setup_result["stdout"] else "",
                    stderr_excerpt=setup_result["stderr"][-1000:] if setup_result["stderr"] else "",
                    error_message=f"CCO setup failed: {setup_result['error']}",
                )
            logger.info("[CCO] Setup phase completed successfully")

        # Build ccbox command for the actual test
        # ccbox parameters (as of latest version):
        # -y: unattended mode (deps=ALL, stack=auto-detect, no prompts)
        # -dd: debug logging (stream output)
        # -C: change directory
        # --bare: vanilla mode (no CCO rules)
        # -m/--model: model selection
        # -p/--prompt: initial prompt (enables --print mode)
        cmd = [self.ccbox_cmd, "-y", "-dd"]

        # Project directory (ccbox -C flag)
        cmd.extend(["-C", str(project_dir)])

        # Variant-specific flags
        if variant == "vanilla":
            cmd.append("--bare")  # No CCO rules
        # else: CCO variant - rules already configured in setup phase

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

        logger.info(f"[{variant.upper()}] Executing: {cmd_str[:200]}...")

        # Use streaming mode for real-time output and activity tracking
        if self.streaming:
            exit_code, stdout, stderr, activity = self._run_with_streaming(
                cmd=cmd,
                project_dir=project_dir,
                variant=variant,
                timeout=self.timeout,
                env={"CLAUDE_MODEL": model},
            )

            generation_time = time.time() - start_time

            # Handle FileNotFoundError (exit_code is None and no output)
            if exit_code is None and not stdout and not stderr:
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

            success = exit_code == 0

            # Build stall info for error message
            stall_info = ""
            if activity.stall_warnings > 0:
                stall_info = f" ({activity.stall_warnings} stall warnings)"
            if activity.is_stalled:
                stall_info += " [STALLED]"

            # Save ccbox output with detailed info including activity
            log_content = f"""ccbox Execution Log ({variant}) - STREAMING MODE
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
            (project_dir / "_ccbox_run.log").write_text(log_content, encoding="utf-8")
            (project_dir / "_ccbox_stdout.log").write_text(stdout, encoding="utf-8")
            (project_dir / "_ccbox_stderr.log").write_text(stderr, encoding="utf-8")

            if success:
                logger.info(f"[{variant.upper()}] SUCCESS in {generation_time:.2f}s{stall_info}")

                # CCO variant: Run cco-optimize --auto after successful test
                if variant == "cco":
                    logger.info("[CCO] Running optimize phase...")
                    optimize_result = self._run_cco_optimize(project_dir, model)
                    if optimize_result["success"]:
                        logger.info(
                            f"[CCO] Optimize phase completed in {optimize_result['time']:.2f}s"
                        )
                    else:
                        # Non-blocking: log warning but continue with analysis
                        logger.warning(
                            f"[CCO] Optimize phase failed (non-blocking): {optimize_result['error']}"
                        )
            else:
                if exit_code is None:
                    logger.error(
                        f"[{variant.upper()}] TIMEOUT after {generation_time:.2f}s{stall_info}"
                    )
                else:
                    logger.error(
                        f"[{variant.upper()}] FAILED with exit code {exit_code}{stall_info}"
                    )
                logger.error(f"[{variant.upper()}] stdout:\n{_truncate(stdout, 1500)}")
                logger.error(f"[{variant.upper()}] stderr:\n{_truncate(stderr, 1500)}")

            # Analyze generated code
            analyzer = CodeAnalyzer(project_dir)
            metrics = analyzer.analyze()
            metrics.name = config.name
            metrics.variant = variant
            metrics.generation_time_seconds = generation_time
            score = calculate_overall_score(metrics)

            # Build detailed error message if failed
            error_msg = ""
            if not success:
                if exit_code is None:
                    error_msg = f"Inactivity timeout ({self.timeout}s without output){stall_info}"
                else:
                    error_msg = _parse_ccbox_error(stdout, stderr, exit_code) + stall_info

            return ExecutionResult(
                project_id=config.id,
                variant=variant,
                success=success,
                metrics=metrics,
                score=round(score, 1),
                generation_time_seconds=round(generation_time, 2),
                prompt_used=config.prompt,
                output_dir=str(project_dir),
                command=cmd_str,
                exit_code=exit_code,
                stdout_excerpt=stdout[-1000:] if stdout else "",
                stderr_excerpt=stderr[-1000:] if stderr else "",
                error_message=error_msg,
            )

        # Legacy non-streaming mode (fallback)
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                env={**os.environ, "CLAUDE_MODEL": model},
                encoding="utf-8",
                errors="replace",
            )

            generation_time = time.time() - start_time
            success = result.returncode == 0

            log_content = f"""ccbox Execution Log ({variant})
{"=" * 60}
Command: {cmd_str}
Exit Code: {result.returncode}
Duration: {generation_time:.2f}s
Success: {success}
Project Dir: {project_dir}
{"=" * 60}

STDOUT:
{result.stdout or "(empty)"}

{"=" * 60}
STDERR:
{result.stderr or "(empty)"}
"""
            (project_dir / "_ccbox_run.log").write_text(log_content, encoding="utf-8")
            (project_dir / "_ccbox_stdout.log").write_text(result.stdout, encoding="utf-8")
            (project_dir / "_ccbox_stderr.log").write_text(result.stderr, encoding="utf-8")

            if success:
                logger.info(f"[{variant.upper()}] SUCCESS in {generation_time:.2f}s")
            else:
                logger.error(f"[{variant.upper()}] FAILED with exit code {result.returncode}")
                logger.error(f"[{variant.upper()}] stdout:\n{_truncate(result.stdout, 1500)}")
                logger.error(f"[{variant.upper()}] stderr:\n{_truncate(result.stderr, 1500)}")

            analyzer = CodeAnalyzer(project_dir)
            metrics = analyzer.analyze()
            metrics.name = config.name
            metrics.variant = variant
            metrics.generation_time_seconds = generation_time
            score = calculate_overall_score(metrics)

            error_msg = ""
            if not success:
                error_msg = _parse_ccbox_error(result.stdout, result.stderr, result.returncode)

            return ExecutionResult(
                project_id=config.id,
                variant=variant,
                success=success,
                metrics=metrics,
                score=round(score, 1),
                generation_time_seconds=round(generation_time, 2),
                prompt_used=config.prompt,
                output_dir=str(project_dir),
                command=cmd_str,
                exit_code=result.returncode,
                stdout_excerpt=result.stdout[-1000:] if result.stdout else "",
                stderr_excerpt=result.stderr[-1000:] if result.stderr else "",
                error_message=error_msg,
            )

        except subprocess.TimeoutExpired:
            generation_time = time.time() - start_time
            return ExecutionResult(
                project_id=config.id,
                variant=variant,
                success=False,
                metrics=None,
                score=0.0,
                generation_time_seconds=round(generation_time, 2),
                prompt_used=config.prompt,
                output_dir=str(project_dir),
                command=cmd_str,
                exit_code=None,
                error_message=f"Timeout after {self.timeout} seconds",
            )
        except FileNotFoundError:
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
        except Exception as e:
            generation_time = time.time() - start_time
            import traceback

            return ExecutionResult(
                project_id=config.id,
                variant=variant,
                success=False,
                metrics=None,
                score=0.0,
                generation_time_seconds=round(generation_time, 2),
                prompt_used=config.prompt,
                output_dir=str(project_dir),
                command=cmd_str,
                exit_code=None,
                error_message=f"{type(e).__name__}: {e}\n{traceback.format_exc()[:500]}",
            )

    def run_benchmark(self, config: ProjectConfig, model: str = "opus") -> BenchmarkResult:
        """Run full benchmark (both variants) for a project."""
        # Run CCO first (primary test subject)
        cco_result = self.run_project(config, "cco", model)

        # Run vanilla version (baseline)
        vanilla_result = self.run_project(config, "vanilla", model)

        # Compare results
        if cco_result.metrics and vanilla_result.metrics:
            comparison = compare_metrics(cco_result.metrics, vanilla_result.metrics)
        else:
            comparison = {
                "comparisons": [],
                "cco_wins": 0,
                "vanilla_wins": 0,
                "ties": 0,
                "cco_score": cco_result.score,
                "vanilla_score": vanilla_result.score,
                "score_diff": cco_result.score - vanilla_result.score,
            }

        # Determine verdict using SSOT function
        diff = comparison["score_diff"]
        verdict = calculate_verdict(diff)

        return BenchmarkResult(
            project_id=config.id,
            project_name=config.name,
            categories=config.categories,
            complexity=config.complexity,
            cco_result=cco_result,
            vanilla_result=vanilla_result,
            comparison=comparison,
            verdict=verdict,
            score_difference=round(diff, 1),
            prompt_used=config.prompt,
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
