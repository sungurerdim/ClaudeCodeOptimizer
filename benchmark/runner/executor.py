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
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from .metrics import CodeAnalyzer, Metrics, calculate_overall_score, compare_metrics

# Configure logger for detailed debugging
logger = logging.getLogger("cco-benchmark.executor")


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

    def __init__(self, output_base: Path, ccbox_cmd: str = "ccbox", timeout_seconds: int = 600):
        self.output_base = output_base
        self.ccbox_cmd = ccbox_cmd
        self.timeout = timeout_seconds
        self.setup_timeout = 120  # 2 minutes for CCO setup
        self.output_base.mkdir(parents=True, exist_ok=True)

    def _run_cco_setup(self, project_dir: Path, model: str) -> dict[str, Any]:
        """Run cco-config --auto to setup CCO rules before the actual test.

        This runs in a separate ccbox invocation so that:
        1. CCO rules are configured and persisted
        2. Container restarts with rules in context

        Returns:
            Dict with success, time, command, exit_code, stdout, stderr, error
        """
        # ccbox parameters (as of latest version):
        # -C: change directory
        # -m/--model: model selection
        # -p/--prompt: initial prompt (enables --print mode)
        # Note: --yes was removed from ccbox
        cmd = [
            self.ccbox_cmd,
            "-C",
            str(project_dir),
            "-m",
            model,
            "-p",
            "/cco-config --auto",
        ]
        cmd_str = " ".join(cmd)
        start_time = time.time()

        logger.info(f"[CCO Setup] Starting: {cmd_str}")
        logger.info(f"[CCO Setup] Project dir: {project_dir}")

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.setup_timeout,
                env={**os.environ, "CLAUDE_MODEL": model},
                encoding="utf-8",
                errors="replace",
            )

            elapsed = time.time() - start_time

            # Save setup logs with detailed info
            log_content = f"""CCO Setup Log
{"=" * 60}
Command: {cmd_str}
Exit Code: {result.returncode}
Duration: {elapsed:.2f}s
Project Dir: {project_dir}
{"=" * 60}

STDOUT:
{result.stdout or "(empty)"}

{"=" * 60}
STDERR:
{result.stderr or "(empty)"}
"""
            (project_dir / "_cco_setup.log").write_text(log_content, encoding="utf-8")
            (project_dir / "_cco_setup_stdout.log").write_text(result.stdout, encoding="utf-8")
            (project_dir / "_cco_setup_stderr.log").write_text(result.stderr, encoding="utf-8")

            if result.returncode != 0:
                error_msg = _parse_ccbox_error(result.stdout, result.stderr, result.returncode)
                logger.error(f"[CCO Setup] FAILED: {error_msg}")
                logger.error(f"[CCO Setup] Full stdout:\n{_truncate(result.stdout, 2000)}")
                logger.error(f"[CCO Setup] Full stderr:\n{_truncate(result.stderr, 2000)}")

                return {
                    "success": False,
                    "time": elapsed,
                    "command": cmd_str,
                    "exit_code": result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "error": error_msg,
                }

            logger.info(f"[CCO Setup] SUCCESS in {elapsed:.2f}s")
            return {
                "success": True,
                "time": elapsed,
                "command": cmd_str,
                "exit_code": 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "error": "",
            }

        except subprocess.TimeoutExpired as e:
            elapsed = time.time() - start_time
            error_msg = f"Setup timeout after {self.setup_timeout}s"
            logger.error(f"[CCO Setup] TIMEOUT: {error_msg}")
            # Try to get partial output (may be str or bytes depending on subprocess config)
            stdout = ""
            stderr = ""
            if e.stdout:
                stdout = (
                    e.stdout
                    if isinstance(e.stdout, str)
                    else e.stdout.decode("utf-8", errors="replace")
                )
            if e.stderr:
                stderr = (
                    e.stderr
                    if isinstance(e.stderr, str)
                    else e.stderr.decode("utf-8", errors="replace")
                )
            if stdout or stderr:
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
        except FileNotFoundError:
            error_msg = f"ccbox command not found: {self.ccbox_cmd}"
            logger.error(f"[CCO Setup] {error_msg}")
            return {
                "success": False,
                "time": 0,
                "command": cmd_str,
                "exit_code": None,
                "stdout": "",
                "stderr": "",
                "error": error_msg,
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

    def run_project(
        self, config: ProjectConfig, variant: str, model: str = "opus"
    ) -> ExecutionResult:
        """Run a single project variant.

        Creates an isolated directory, cd's into it, and runs ccbox.
        ccbox will mount this directory and generate code there.

        For CCO variant, runs two phases:
        1. Setup phase: Run /cco-config --auto to configure CCO rules
        2. Test phase: Run the actual benchmark prompt
        """
        logger.info(f"[{variant.upper()}] Starting project: {config.id}")

        # Create isolated project directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_dir = self.output_base / f"{config.id}_{variant}_{timestamp}"
        project_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"[{variant.upper()}] Output dir: {project_dir}")

        # Save prompt for reference
        prompt_file = project_dir / "_benchmark_prompt.md"
        prompt_file.write_text(config.prompt, encoding="utf-8")

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
        # -C: change directory
        # --bare: vanilla mode (no CCO rules)
        # -m/--model: model selection
        # -p/--prompt: initial prompt (enables --print mode)
        # Note: --yes was removed from ccbox
        cmd = [self.ccbox_cmd]

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
                config.prompt,  # Pass prompt (enables --print mode)
            ]
        )

        start_time = time.time()
        cmd_str = " ".join(cmd)

        logger.info(f"[{variant.upper()}] Executing: {cmd_str[:200]}...")

        try:
            # Run ccbox with -C pointing to project directory
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

            # Save ccbox output with detailed info
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

            # Analyze generated code (ccbox creates files in project_dir)
            # Exclude our benchmark metadata files
            analyzer = CodeAnalyzer(project_dir)
            metrics = analyzer.analyze()
            metrics.name = config.name
            metrics.variant = variant
            metrics.generation_time_seconds = generation_time
            score = calculate_overall_score(metrics)

            # Build detailed error message if failed
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
        # Run vanilla first
        vanilla_result = self.run_project(config, "vanilla", model)

        # Run CCO version
        cco_result = self.run_project(config, "cco", model)

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

        # Determine verdict
        diff = comparison["score_diff"]
        if diff >= 15:
            verdict = "Strong CCO Advantage"
        elif diff >= 5:
            verdict = "Moderate CCO Advantage"
        elif diff >= -5:
            verdict = "Mixed Results"
        elif diff >= -15:
            verdict = "Moderate Vanilla Advantage"
        else:
            verdict = "Strong Vanilla Advantage"

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
