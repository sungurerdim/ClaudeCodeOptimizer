"""
CCO Benchmark - Web UI Server

FastAPI server for the benchmark dashboard.
"""

import asyncio
import logging
import shutil
import subprocess
import sys
import traceback
from collections import deque
from datetime import datetime
from pathlib import Path
from typing import Any

from fastapi import BackgroundTasks, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from ..runner import (
    ProjectConfig,
    ResultsManager,
    TestExecutor,
    discover_projects,
)


# ANSI color codes
class LogColors:
    """ANSI color codes for terminal output."""

    RESET = "\033[0m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    GRAY = "\033[90m"
    BOLD = "\033[1m"


class ColoredFormatter(logging.Formatter):
    """Formatter with colors and truncation for non-error messages.

    Format: DATE | LEVEL | SERVICE | MESSAGE
    Colors (priority order):
    - SUCCESS in message: Green
    - FAILED in message: Red
    - Completed in message: Green
    - [VANILLA]/[CCO]/[stdout]: Cyan
    - ERROR level: Red
    - WARNING level: Yellow
    - Other: Default
    """

    LEVEL_COLORS = {
        logging.ERROR: LogColors.RED,
        logging.WARNING: LogColors.YELLOW,
        logging.DEBUG: LogColors.GRAY,
    }

    def format(self, record: logging.LogRecord) -> str:
        # Truncate message for non-error levels
        original_msg = record.msg
        if record.levelno < logging.ERROR and len(str(record.msg)) > 100:
            record.msg = str(record.msg)[:100] + "..."

        # Format the base message
        formatted = super().format(record)

        # Restore original message
        record.msg = original_msg

        # Apply colors
        color = self.LEVEL_COLORS.get(record.levelno, "")

        # Apply semantic colors (priority order: success/fail > variant > default)
        msg_str = str(original_msg)
        if "SUCCESS" in msg_str:
            color = LogColors.GREEN
        elif "FAILED" in msg_str:
            color = LogColors.RED
        elif "Completed" in msg_str:
            color = LogColors.GREEN
        # Container/executor variant logs (cyan) - lower priority than success/fail
        elif "[VANILLA]" in msg_str or "[CCO]" in msg_str or "[stdout]" in msg_str:
            color = LogColors.CYAN

        if color:
            # Color the entire line
            formatted = f"{color}{formatted}{LogColors.RESET}"

        return formatted


# Configure logging with professional format
# Format: DATE | LEVEL | SERVICE | MESSAGE
handler = logging.StreamHandler()
handler.setFormatter(
    ColoredFormatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)-15s | %(message)s",
        datefmt="%d.%m.%Y %H:%M:%S",
    )
)
logging.basicConfig(level=logging.INFO, handlers=[handler])
logger = logging.getLogger("cco-benchmark")

# Configuration
BENCHMARK_DIR = Path(__file__).parent.parent
PROJECTS_DIR = BENCHMARK_DIR / "projects"
RESULTS_DIR = BENCHMARK_DIR / "results"
OUTPUT_DIR = BENCHMARK_DIR / "output"
SUITE_DIR = BENCHMARK_DIR / "suite"
STATIC_DIR = Path(__file__).parent / "static"


# ============== Activity Log ==============


class ActivityLog:
    """Activity log for tracking operations (shown in UI)."""

    def __init__(self, max_entries: int = 500) -> None:
        self._entries: deque[dict[str, str]] = deque(maxlen=max_entries)

    def add(self, message: str, level: str = "info") -> None:
        """Add an entry to the activity log."""
        # Truncation handled by TruncatingFormatter at logging level
        entry = {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "message": message[:100] + "..."
            if level != "error" and len(message) > 100
            else message,
            "level": level,
        }
        self._entries.append(entry)
        # Use appropriate log level so formatter can decide truncation
        if level == "error":
            logger.error(message)
        elif level == "warning":
            logger.warning(message)
        else:
            logger.info(message)

    def get_entries(self, limit: int = 50) -> list[dict[str, str]]:
        """Get recent log entries (newest first)."""
        entries = list(self._entries)
        return list(reversed(entries[-limit:]))

    def clear(self) -> None:
        """Clear all log entries."""
        self._entries.clear()


activity_log = ActivityLog()


def log_activity(message: str, level: str = "info") -> None:
    """Log an activity message."""
    activity_log.add(message, level)


# ============== System Check ==============


def get_platform_info() -> dict[str, Any]:
    """Get platform-specific information for Docker setup."""
    import platform

    system = platform.system().lower()

    if system == "windows":
        return {
            "os": "windows",
            "os_name": "Windows",
            "docker_install_url": "https://docs.docker.com/desktop/install/windows-install/",
            "docker_start_cmd": "Start Docker Desktop from the Start menu",
            "docker_start_hint": "Open Docker Desktop application",
        }
    elif system == "darwin":
        return {
            "os": "macos",
            "os_name": "macOS",
            "docker_install_url": "https://docs.docker.com/desktop/install/mac-install/",
            "docker_start_cmd": "open -a Docker",
            "docker_start_hint": "Open Docker Desktop from Applications or run: open -a Docker",
        }
    else:  # Linux and others
        return {
            "os": "linux",
            "os_name": "Linux",
            "docker_install_url": "https://docs.docker.com/engine/install/",
            "docker_start_cmd": "sudo systemctl start docker",
            "docker_start_hint": "Run: sudo systemctl start docker",
        }


def check_system_dependencies() -> dict[str, Any]:
    """Check if required dependencies are installed."""
    platform_info = get_platform_info()

    result = {
        "platform": platform_info,
        "python": {
            "installed": True,
            "version": sys.version.split()[0],
            "path": sys.executable,
        },
        "docker": {
            "installed": False,
            "running": False,
            "version": None,
            "path": None,
            "install_url": platform_info["docker_install_url"],
            "start_hint": platform_info["docker_start_hint"],
        },
        "ccbox": {
            "installed": False,
            "version": None,
            "path": None,
            "install_cmd": "pip install ccbox",
        },
        "ready": False,
    }

    # Check Docker first (ccbox requires Docker)
    docker_path = shutil.which("docker")
    if docker_path:
        result["docker"]["installed"] = True
        result["docker"]["path"] = docker_path
        try:
            # Get Docker version
            version_output = subprocess.run(
                ["docker", "--version"],
                capture_output=True,
                text=True,
                timeout=5,
                encoding="utf-8",
                errors="replace",
            )
            if version_output.returncode == 0:
                # "Docker version 24.0.7, build afdd53b"
                version_str = version_output.stdout.strip()
                if "version" in version_str.lower():
                    parts = version_str.split()
                    for i, p in enumerate(parts):
                        if p.lower() == "version" and i + 1 < len(parts):
                            result["docker"]["version"] = parts[i + 1].rstrip(",")
                            break

            # Check if Docker daemon is running
            daemon_check = subprocess.run(
                ["docker", "info"],
                capture_output=True,
                text=True,
                timeout=10,
                encoding="utf-8",
                errors="replace",
            )
            result["docker"]["running"] = daemon_check.returncode == 0
        except subprocess.TimeoutExpired:
            result["docker"]["running"] = False
        except Exception:
            pass

    # Check ccbox (only useful if Docker is running)
    ccbox_path = shutil.which("ccbox")
    if ccbox_path:
        result["ccbox"]["installed"] = True
        result["ccbox"]["path"] = ccbox_path
        try:
            version_output = subprocess.run(
                ["ccbox", "--version"],
                capture_output=True,
                text=True,
                timeout=5,
                encoding="utf-8",
                errors="replace",
            )
            if version_output.returncode == 0:
                result["ccbox"]["version"] = version_output.stdout.strip().split()[-1]
        except Exception:
            pass

    # System is ready only if Docker is running AND ccbox is installed
    result["ready"] = (
        result["python"]["installed"]
        and result["docker"]["installed"]
        and result["docker"]["running"]
        and result["ccbox"]["installed"]
    )
    return result


# ============== Initialize App ==============

app = FastAPI(title="CCO Benchmark", version="1.0.0")
results_manager = ResultsManager(RESULTS_DIR)

# Track running tests
running_tests: dict[str, dict[str, Any]] = {}

# Track installation status
install_status: dict[str, Any] = {"installing": False, "package": None, "output": ""}


# ============== Exception Handlers ==============


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception on {request.method} {request.url.path}")
    logger.error(f"Exception: {type(exc).__name__}: {exc}")
    logger.error(traceback.format_exc())
    log_activity(f"Error: {type(exc).__name__}: {exc}", "error")
    return JSONResponse(
        status_code=500,
        content={
            "detail": f"Internal server error: {type(exc).__name__}: {str(exc)}",
            "path": request.url.path,
        },
    )


# ============== Models ==============


class ProjectVariants(BaseModel):
    """Variant selection for a single project."""

    project_id: str
    run_vanilla: bool = False
    run_cco: bool = False


class RunTestRequest(BaseModel):
    """Request to run tests with per-project variant selection."""

    projects: list[ProjectVariants]
    model: str = "opus"


class CompareRequest(BaseModel):
    """Request to compare vanilla vs cco for a project."""

    project_id: str


class TestStatus(BaseModel):
    project_id: str
    status: str  # "pending", "running_vanilla", "running_cco", "completed", "failed"
    progress: int  # 0-100
    current_variant: str | None = None
    error: str | None = None
    result: dict | None = None


# ============== API Routes ==============


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "service": "cco-benchmark"}


@app.get("/api/system")
async def get_system_status() -> dict[str, Any]:
    """Get system status and dependency checks."""
    deps = check_system_dependencies()
    return {
        "dependencies": deps,
        "ready": deps["ready"],
        "installing": install_status["installing"],
        "install_package": install_status["package"],
    }


@app.post("/api/install/{package}")
async def install_package(package: str, background_tasks: BackgroundTasks) -> dict[str, str]:
    """Install a Python package via pip."""
    allowed_packages = ["ccbox"]  # Whitelist

    if package not in allowed_packages:
        raise HTTPException(400, f"Package not allowed: {package}")

    if install_status["installing"]:
        raise HTTPException(409, "Installation already in progress")

    install_status["installing"] = True
    install_status["package"] = package
    install_status["output"] = ""

    log_activity(f"Starting installation of {package}...", "info")
    background_tasks.add_task(run_pip_install, package)

    return {"message": f"Installing {package}...", "status": "started"}


async def run_pip_install(package: str) -> None:
    """Run pip install in background."""
    try:
        result = await asyncio.to_thread(
            subprocess.run,
            [sys.executable, "-m", "pip", "install", package, "-q"],
            capture_output=True,
            text=True,
            timeout=300,
            encoding="utf-8",
            errors="replace",
        )
        install_status["output"] = result.stdout + result.stderr
        if result.returncode == 0:
            log_activity(f"Successfully installed {package}", "success")
        else:
            log_activity(f"Failed to install {package}: {result.stderr}", "error")
    except Exception as e:
        log_activity(f"Installation error: {e}", "error")
        install_status["output"] = str(e)
    finally:
        install_status["installing"] = False
        install_status["package"] = None


@app.get("/api/install/status")
async def get_install_status() -> dict[str, Any]:
    """Get current installation status."""
    return {
        "installing": install_status["installing"],
        "package": install_status["package"],
        "output": install_status["output"],
    }


@app.post("/api/docker/start")
async def start_docker() -> dict[str, Any]:
    """Attempt to start Docker Desktop."""
    import platform

    system = platform.system().lower()
    log_activity("Attempting to start Docker...", "info")

    try:
        if system == "windows":
            # Try to start Docker Desktop on Windows
            result = subprocess.run(
                ["powershell", "-Command", "Start-Process", "Docker Desktop"],
                capture_output=True,
                text=True,
                timeout=10,
                encoding="utf-8",
                errors="replace",
            )
            if result.returncode == 0:
                log_activity("Docker Desktop start command sent", "success")
                return {"success": True, "message": "Docker Desktop starting..."}
            else:
                # Try alternative method - use full path to Docker Desktop
                import os

                docker_path = os.path.expandvars(r"%ProgramFiles%\Docker\Docker\Docker Desktop.exe")
                result = subprocess.run(
                    ["cmd", "/c", "start", "", docker_path],
                    capture_output=True,
                    text=True,
                    timeout=10,
                    encoding="utf-8",
                    errors="replace",
                )
                if result.returncode == 0:
                    log_activity("Docker Desktop start command sent (alt)", "success")
                    return {"success": True, "message": "Docker Desktop starting..."}
                log_activity(f"Failed to start Docker: {result.stderr}", "error")
                return {"success": False, "message": "Could not start Docker Desktop"}

        elif system == "darwin":
            # macOS
            result = subprocess.run(
                ["open", "-a", "Docker"],
                capture_output=True,
                text=True,
                timeout=10,
                encoding="utf-8",
                errors="replace",
            )
            if result.returncode == 0:
                log_activity("Docker Desktop starting on macOS", "success")
                return {"success": True, "message": "Docker Desktop starting..."}
            log_activity(f"Failed to start Docker: {result.stderr}", "error")
            return {"success": False, "message": "Could not start Docker Desktop"}

        else:
            # Linux - try systemctl
            result = subprocess.run(
                ["systemctl", "start", "docker"],
                capture_output=True,
                text=True,
                timeout=30,
                encoding="utf-8",
                errors="replace",
            )
            if result.returncode == 0:
                log_activity("Docker daemon started", "success")
                return {"success": True, "message": "Docker daemon starting..."}
            # May need sudo - inform user
            log_activity("Docker start requires sudo", "warning")
            return {
                "success": False,
                "message": "Run 'sudo systemctl start docker' in terminal",
            }

    except subprocess.TimeoutExpired:
        log_activity("Docker start command timed out", "warning")
        return {"success": False, "message": "Start command timed out"}
    except FileNotFoundError as e:
        log_activity(f"Docker Desktop not found: {e}", "error")
        return {"success": False, "message": "Docker Desktop not found"}
    except Exception as e:
        log_activity(f"Failed to start Docker: {e}", "error")
        return {"success": False, "message": str(e)}


@app.get("/api/activity")
async def get_activity(limit: int = 50) -> list[dict[str, str]]:
    """Get recent activity log entries."""
    return activity_log.get_entries(limit)


@app.get("/api/projects")
async def list_projects() -> list[dict[str, Any]]:
    """List all available benchmark projects."""
    projects = discover_projects(PROJECTS_DIR)
    return [
        {
            "id": p.id,
            "name": p.name,
            "categories": p.categories,
            "complexity": p.complexity,
            "has_prompt": bool(p.prompt),
        }
        for p in projects
    ]


@app.get("/api/projects/{project_id}")
async def get_project(project_id: str) -> dict[str, Any]:
    """Get project details including prompt."""
    project_dir = PROJECTS_DIR / project_id
    if not project_dir.exists():
        raise HTTPException(404, f"Project not found: {project_id}")

    config = ProjectConfig(project_dir)
    return {
        "id": config.id,
        "name": config.name,
        "categories": config.categories,
        "complexity": config.complexity,
        "prompt": config.prompt,
        "spec": (project_dir / "SPEC.md").read_text(encoding="utf-8")
        if (project_dir / "SPEC.md").exists()
        else "",
    }


@app.get("/api/projects/{project_id}/prompt")
async def get_project_prompt(project_id: str) -> dict[str, str]:
    """Get project prompt text (for copying)."""
    project_dir = PROJECTS_DIR / project_id
    if not project_dir.exists():
        raise HTTPException(404, f"Project not found: {project_id}")

    config = ProjectConfig(project_dir)
    return {"prompt": config.prompt}


@app.post("/api/run")
async def run_tests(request: RunTestRequest, background_tasks: BackgroundTasks) -> dict[str, Any]:
    """Start benchmark tests for selected projects with per-project variant selection."""
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Filter projects that have at least one variant selected
    valid_projects = [p for p in request.projects if p.run_vanilla or p.run_cco]

    if not valid_projects:
        return {"run_id": run_id, "message": "No variants selected", "count": 0}

    # Initialize status for all projects
    for project in valid_projects:
        running_tests[f"{run_id}_{project.project_id}"] = {
            "run_id": run_id,
            "project_id": project.project_id,
            "run_vanilla": project.run_vanilla,
            "run_cco": project.run_cco,
            "status": "pending",
            "progress": 0,
            "current_variant": None,
            "error": None,
            "vanilla_result": None,
            "cco_result": None,
            "started_at": datetime.now().isoformat(),
        }

    # Start background execution
    background_tasks.add_task(execute_tests_background, run_id, valid_projects, request.model)

    return {
        "run_id": run_id,
        "message": f"Started {len(valid_projects)} project(s)",
        "count": len(valid_projects),
    }


async def execute_tests_background(
    run_id: str, projects: list[ProjectVariants], model: str
) -> None:
    """Execute tests in background with per-project variant selection."""
    from ..runner import BenchmarkResult, compare_metrics

    executor = TestExecutor(OUTPUT_DIR)
    log_activity(f"Starting benchmark run: {len(projects)} project(s)", "info")

    for project in projects:
        project_id = project.project_id
        key = f"{run_id}_{project_id}"
        project_dir = PROJECTS_DIR / project_id

        if not project_dir.exists():
            running_tests[key]["status"] = "failed"
            running_tests[key]["error"] = f"Project not found: {project_id}"
            log_activity(f"Project not found: {project_id}", "error")
            continue

        config = ProjectConfig(project_dir)
        variants_to_run = []
        if project.run_vanilla:
            variants_to_run.append("vanilla")
        if project.run_cco:
            variants_to_run.append("cco")

        log_activity(f"Testing project: {config.name} ({', '.join(variants_to_run)})", "info")

        try:
            progress_per_variant = 100 // len(variants_to_run) if variants_to_run else 100
            current_progress = 0

            # Run vanilla if selected
            if project.run_vanilla:
                running_tests[key]["status"] = "running_vanilla"
                running_tests[key]["current_variant"] = "vanilla"
                running_tests[key]["progress"] = current_progress + 10
                log_activity(f"[VANILLA] Starting: {config.name}", "info")

                vanilla_result = await asyncio.to_thread(
                    executor.run_project, config, "vanilla", model
                )
                running_tests[key]["vanilla_result"] = vanilla_result.to_dict()

                if vanilla_result.success:
                    log_activity(
                        f"[VANILLA] Completed: score={vanilla_result.score}, "
                        f"time={vanilla_result.generation_time_seconds:.1f}s",
                        "success",
                    )
                else:
                    log_activity(f"[VANILLA] FAILED: {vanilla_result.error_message}", "error")
                    if vanilla_result.output_dir:
                        log_activity(f"[VANILLA] Output dir: {vanilla_result.output_dir}", "info")

                current_progress += progress_per_variant

            # Run CCO if selected
            if project.run_cco:
                running_tests[key]["status"] = "running_cco"
                running_tests[key]["current_variant"] = "cco"
                running_tests[key]["progress"] = current_progress + 10
                log_activity(f"[CCO] Starting: {config.name} (setup + test + optimize)", "info")

                cco_result = await asyncio.to_thread(executor.run_project, config, "cco", model)
                running_tests[key]["cco_result"] = cco_result.to_dict()

                if cco_result.success:
                    log_activity(
                        f"[CCO] Completed: score={cco_result.score}, "
                        f"time={cco_result.generation_time_seconds:.1f}s",
                        "success",
                    )
                else:
                    log_activity(f"[CCO] FAILED: {cco_result.error_message}", "error")
                    if cco_result.output_dir:
                        log_activity(f"[CCO] Output dir: {cco_result.output_dir}", "info")

                current_progress += progress_per_variant

            running_tests[key]["status"] = "completed"
            running_tests[key]["progress"] = 100
            log_activity(f"Completed: {config.name}", "success")

            # Save result if both variants were run
            if project.run_vanilla and project.run_cco:
                try:
                    vanilla_exec = running_tests[key].get("vanilla_result")
                    cco_exec = running_tests[key].get("cco_result")

                    if vanilla_exec and cco_exec:
                        from ..runner import ExecutionResult

                        vanilla_result = ExecutionResult.from_dict(vanilla_exec)
                        cco_result = ExecutionResult.from_dict(cco_exec)

                        # Compare metrics if both have them
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

                        diff = comparison.get("score_diff", cco_result.score - vanilla_result.score)
                        from ..runner import calculate_verdict

                        verdict = calculate_verdict(diff)

                        benchmark_result = BenchmarkResult(
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

                        filepath = results_manager.save_result(benchmark_result)
                        log_activity(f"Result saved: {filepath.name}", "info")
                except Exception as save_err:
                    log_activity(f"Failed to save result: {save_err}", "warning")

        except Exception as e:
            running_tests[key]["status"] = "failed"
            running_tests[key]["error"] = str(e)
            log_activity(f"Failed: {project_id} - {e}", "error")

    log_activity("Benchmark run completed", "success")


@app.get("/api/running")
async def get_running_tests() -> dict[str, Any]:
    """Get all currently running tests."""
    active_runs: dict[str, list[dict[str, Any]]] = {}
    for status in running_tests.values():
        if status["status"] not in ("completed", "failed"):
            run_id = status["run_id"]
            if run_id not in active_runs:
                active_runs[run_id] = []
            active_runs[run_id].append(status)
    return {"active_runs": active_runs, "has_running": len(active_runs) > 0}


@app.get("/api/status/{run_id}")
async def get_run_status(run_id: str) -> list[dict[str, Any]]:
    """Get status of all tests in a run."""
    statuses = []
    for key, status in running_tests.items():
        if key.startswith(f"{run_id}_"):
            statuses.append(status)
    return statuses


@app.get("/api/status/{run_id}/{project_id}")
async def get_test_status(run_id: str, project_id: str) -> dict[str, Any]:
    """Get status of a specific test."""
    key = f"{run_id}_{project_id}"
    if key not in running_tests:
        raise HTTPException(404, "Test not found")
    return running_tests[key]


@app.get("/api/results")
async def list_results(limit: int = 20) -> list[dict[str, Any]]:
    """List saved benchmark results."""
    files = results_manager.list_results()[:limit]
    results = []
    for f in files:
        try:
            result = results_manager.load_result(f)
            results.append(
                {
                    "filename": f.name,
                    "project_id": result.project_id,
                    "project_name": result.project_name,
                    "verdict": result.verdict,
                    "score_difference": result.score_difference,
                    "cco_score": result.cco_result.score,
                    "vanilla_score": result.vanilla_result.score,
                    "cco_time": result.cco_result.generation_time_seconds,
                    "vanilla_time": result.vanilla_result.generation_time_seconds,
                    "timestamp": result.timestamp,
                }
            )
        except Exception:
            pass
    return results


@app.get("/api/results/{filename}")
async def get_result(filename: str) -> dict[str, Any]:
    """Get a specific result by filename."""
    filepath = RESULTS_DIR / filename
    if not filepath.exists():
        raise HTTPException(404, "Result not found")

    result = results_manager.load_result(filepath)
    return result.to_dict()


@app.get("/api/summary")
async def get_summary() -> dict[str, Any]:
    """Get summary statistics."""
    return results_manager.get_summary()


@app.delete("/api/results/{filename}")
async def delete_result(filename: str) -> dict[str, str]:
    """Delete a result file."""
    filepath = RESULTS_DIR / filename
    if not filepath.exists():
        raise HTTPException(404, "Result not found")

    filepath.unlink()
    return {"message": f"Deleted {filename}"}


# ============== Output & Comparison ==============


@app.get("/api/output")
async def list_output_folders() -> list[dict[str, Any]]:
    """List all output folders with their status."""
    from ..runner import CodeAnalyzer, calculate_overall_score

    if not OUTPUT_DIR.exists():
        return []

    folders = []
    for folder in sorted(OUTPUT_DIR.iterdir()):
        if not folder.is_dir():
            continue

        # Parse folder name: {project_id}_{variant}
        name = folder.name
        parts = name.rsplit("_", 1)
        if len(parts) != 2:
            continue

        project_id, variant = parts
        if variant not in ("vanilla", "cco"):
            continue

        # Check if folder has content
        files = list(folder.glob("*.py")) + list(folder.glob("*.ts")) + list(folder.glob("*.js"))
        has_code = len(files) > 0

        # Try to get metrics if available
        metrics = None
        score = 0.0
        if has_code:
            try:
                analyzer = CodeAnalyzer(folder)
                metrics = analyzer.analyze()
                score = calculate_overall_score(metrics)
            except Exception:
                pass

        # Get modification time
        try:
            mtime = folder.stat().st_mtime
            modified = datetime.fromtimestamp(mtime).isoformat()
        except Exception:
            modified = None

        folders.append(
            {
                "folder": name,
                "project_id": project_id,
                "variant": variant,
                "has_code": has_code,
                "file_count": len(files),
                "score": round(score, 1) if metrics else None,
                "modified": modified,
            }
        )

    return folders


@app.post("/api/compare/{project_id}")
async def compare_project(project_id: str) -> dict[str, Any]:
    """Compare vanilla vs cco output for a project."""
    from ..runner import CodeAnalyzer, calculate_overall_score, compare_metrics

    vanilla_dir = OUTPUT_DIR / f"{project_id}_vanilla"
    cco_dir = OUTPUT_DIR / f"{project_id}_cco"

    result: dict[str, Any] = {
        "project_id": project_id,
        "vanilla_exists": vanilla_dir.exists(),
        "cco_exists": cco_dir.exists(),
        "can_compare": vanilla_dir.exists() and cco_dir.exists(),
    }

    if not result["can_compare"]:
        missing = []
        if not vanilla_dir.exists():
            missing.append("vanilla")
        if not cco_dir.exists():
            missing.append("cco")
        result["error"] = f"Missing output folders: {', '.join(missing)}"
        return result

    # Analyze both
    try:
        vanilla_analyzer = CodeAnalyzer(vanilla_dir)
        vanilla_metrics = vanilla_analyzer.analyze()
        vanilla_metrics.variant = "vanilla"
        vanilla_score = calculate_overall_score(vanilla_metrics)

        cco_analyzer = CodeAnalyzer(cco_dir)
        cco_metrics = cco_analyzer.analyze()
        cco_metrics.variant = "cco"
        cco_score = calculate_overall_score(cco_metrics)

        comparison = compare_metrics(cco_metrics, vanilla_metrics)
        diff = cco_score - vanilla_score

        # Verdict is included in comparison (SSOT)
        result.update(
            {
                "vanilla_score": round(vanilla_score, 1),
                "cco_score": round(cco_score, 1),
                "score_difference": round(diff, 1),
                "verdict": comparison["verdict"],
                "comparison": comparison,
                "vanilla_metrics": vanilla_metrics.to_dict(),
                "cco_metrics": cco_metrics.to_dict(),
            }
        )

    except Exception as e:
        result["error"] = f"Comparison failed: {e}"

    return result


@app.delete("/api/output/{folder_name}")
async def delete_output_folder(folder_name: str) -> dict[str, str]:
    """Delete an output folder."""
    import shutil

    folder_path = OUTPUT_DIR / folder_name
    if not folder_path.exists():
        raise HTTPException(404, "Folder not found")

    # Safety check - only allow deleting our format folders
    parts = folder_name.rsplit("_", 1)
    if len(parts) != 2 or parts[1] not in ("vanilla", "cco"):
        raise HTTPException(400, "Invalid folder name format")

    shutil.rmtree(folder_path)
    log_activity(f"Deleted output folder: {folder_name}", "info")
    return {"message": f"Deleted {folder_name}"}


@app.post("/api/compare-comprehensive/{project_id}")
async def compare_project_comprehensive(project_id: str) -> dict[str, Any]:
    """Comprehensive multi-dimensional comparison of vanilla vs cco."""
    from ..runner import ComprehensiveAnalyzer, compare_comprehensive

    vanilla_dir = OUTPUT_DIR / f"{project_id}_vanilla"
    cco_dir = OUTPUT_DIR / f"{project_id}_cco"

    result: dict[str, Any] = {
        "project_id": project_id,
        "vanilla_exists": vanilla_dir.exists(),
        "cco_exists": cco_dir.exists(),
        "can_compare": vanilla_dir.exists() and cco_dir.exists(),
    }

    if not result["can_compare"]:
        missing = []
        if not vanilla_dir.exists():
            missing.append("vanilla")
        if not cco_dir.exists():
            missing.append("cco")
        result["error"] = f"Missing output folders: {', '.join(missing)}"
        return result

    try:
        # Comprehensive analysis of both variants
        log_activity(f"Starting comprehensive analysis: {project_id}", "info")

        vanilla_analyzer = ComprehensiveAnalyzer(vanilla_dir)
        vanilla_metrics = vanilla_analyzer.analyze()
        vanilla_metrics.variant = "vanilla"

        cco_analyzer = ComprehensiveAnalyzer(cco_dir)
        cco_metrics = cco_analyzer.analyze()
        cco_metrics.variant = "cco"

        comparison = compare_comprehensive(cco_metrics, vanilla_metrics)

        result.update(
            {
                "vanilla_metrics": vanilla_metrics.to_dict(),
                "cco_metrics": cco_metrics.to_dict(),
                "comparison": comparison,
                "verdict": comparison["verdict"],
                "cco_grade": cco_metrics.grade,
                "vanilla_grade": vanilla_metrics.grade,
            }
        )

        log_activity(
            f"Comprehensive analysis complete: CCO={cco_metrics.grade} "
            f"({cco_metrics.overall_score:.1f}) vs Vanilla={vanilla_metrics.grade} "
            f"({vanilla_metrics.overall_score:.1f})",
            "success",
        )

    except Exception as e:
        import traceback

        logger.error(f"Comprehensive comparison failed: {traceback.format_exc()}")
        result["error"] = f"Comprehensive comparison failed: {e}"

    return result


@app.post("/api/compare-ai/{project_id}")
async def compare_project_ai(project_id: str) -> dict[str, Any]:
    """AI-powered comparison using Claude via ccbox."""
    from ..runner.ai_evaluator import run_ai_comparison

    result: dict[str, Any] = {
        "project_id": project_id,
        "method": "ai",
    }

    # Check if both variants exist
    cco_dir = OUTPUT_DIR / f"{project_id}_cco"
    vanilla_dir = OUTPUT_DIR / f"{project_id}_vanilla"

    if not cco_dir.exists() or not vanilla_dir.exists():
        missing = []
        if not cco_dir.exists():
            missing.append("cco")
        if not vanilla_dir.exists():
            missing.append("vanilla")
        result["error"] = f"Missing output folders: {', '.join(missing)}"
        return result

    # Get original prompt from project config
    project_dir = PROJECTS_DIR / project_id
    if not project_dir.exists():
        result["error"] = f"Project not found: {project_id}"
        return result

    config = ProjectConfig(project_dir)
    original_prompt = config.prompt

    log_activity(f"Starting AI comparison for {project_id}...", "info")

    try:
        ai_result = run_ai_comparison(
            project_id=project_id,
            output_dir=OUTPUT_DIR,
            suite_dir=SUITE_DIR,
            original_prompt=original_prompt,
            timeout=600,
        )

        if ai_result.error:
            result["error"] = ai_result.error
            log_activity(f"AI comparison failed: {ai_result.error}", "error")
        else:
            result.update(ai_result.to_dict())
            log_activity(
                f"AI comparison complete: {ai_result.verdict} "
                f"(CCO: {ai_result.cco.grade}, Vanilla: {ai_result.vanilla.grade})",
                "success",
            )

    except Exception as e:
        import traceback

        logger.error(f"AI comparison failed: {traceback.format_exc()}")
        result["error"] = f"AI comparison failed: {e}"
        log_activity(f"AI comparison error: {e}", "error")

    return result


# ============== Static Files & HTML ==============

# Serve static files
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", response_class=HTMLResponse)
async def index():
    """Serve main dashboard page."""
    html_file = Path(__file__).parent / "templates" / "index.html"
    if html_file.exists():
        return HTMLResponse(html_file.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>CCO Benchmark Suite</h1><p>Templates not found</p>")


# ============== Main ==============


def main():
    """Run the server."""
    import uvicorn

    # Configure uvicorn logging with professional format
    # Format: DATE | LEVEL | SERVICE | MESSAGE
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = (
        "%(asctime)s | %(levelname)-8s | uvicorn.access  | %(message)s"
    )
    log_config["formatters"]["default"]["fmt"] = (
        "%(asctime)s | %(levelname)-8s | uvicorn         | %(message)s"
    )
    log_config["formatters"]["access"]["datefmt"] = "%d.%m.%Y %H:%M:%S"
    log_config["formatters"]["default"]["datefmt"] = "%d.%m.%Y %H:%M:%S"
    log_config["formatters"]["access"]["use_colors"] = False
    log_config["formatters"]["default"]["use_colors"] = False

    print("Starting CCO Benchmark Suite server...")
    print("Open http://localhost:8765 in your browser")
    uvicorn.run(app, host="127.0.0.1", port=8765, log_config=log_config)


if __name__ == "__main__":
    main()
