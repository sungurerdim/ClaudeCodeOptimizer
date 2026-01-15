"""
CCO Benchmark - Web UI Server

FastAPI server for the benchmark dashboard.
"""

import asyncio
import json
import logging
import shutil
import subprocess
import sys
import threading
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
    BenchmarkPhase,
    ProjectConfig,
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
    MAGENTA = "\033[95m"  # For AI evaluator
    BOLD = "\033[1m"


class ColoredFormatter(logging.Formatter):
    """Formatter with colors and truncation for non-error messages.

    Format: DATE | LEVEL | SERVICE | MESSAGE

    Color rules (strict - only benchmark status, not AI model output):
    1. Skip [stdout] messages entirely - AI model working output, don't interpret
    2. Explicit benchmark status: SUCCESS/FAILED with variant prefix (green/red)
    3. Log level: ERROR (red), WARNING (yellow)
    4. Benchmark completion markers (green)
    5. AI evaluator service logs (magenta)
    6. Debug level (gray)

    Does NOT color AI model tool results or intermediate states.
    """

    LEVEL_COLORS = {
        logging.ERROR: LogColors.RED,
        logging.WARNING: LogColors.YELLOW,
        logging.DEBUG: LogColors.GRAY,
    }

    # Success patterns - explicit benchmark status
    SUCCESS_PATTERNS = (
        "] SUCCESS:",  # [VARIANT] SUCCESS: message
        "] SUCCESS ",  # [VARIANT] SUCCESS message
        "SUCCESS in ",  # CCO config SUCCESS in X.Xs
        "] Completed:",  # [BENCHMARK] Completed: project
        "benchmark completed",  # Benchmark run completed
        "succeeded,",  # X succeeded, Y failed
    )

    # Failure patterns - explicit benchmark status
    FAILURE_PATTERNS = (
        "] FAILED:",  # [VARIANT] FAILED: message
        "] FAILED ",  # [VARIANT] FAILED message
        "] ERROR:",  # [VARIANT] ERROR: message
        "] Failed:",  # [BENCHMARK] Failed: project
    )

    # Warning patterns - benchmark warnings
    WARNING_PATTERNS = (
        "] Cancelled:",  # [BENCHMARK] Cancelled: project
        "cancelled",  # X cancelled
        "run cancelled",  # run cancelled
        "Skipping",  # Skipping project
    )

    # Completion patterns - benchmark phase completion
    COMPLETION_PATTERNS = (
        "AI comparison complete",  # AI comparison complete for
        "comparison saved",  # Comparison saved to
    )

    def format(self, record: logging.LogRecord) -> str:
        # Truncate message for non-error levels using shared utility
        original_msg = record.msg
        if record.levelno < logging.ERROR:
            record.msg = _truncate_message(str(record.msg))

        # Format the base message
        formatted = super().format(record)

        # Restore original message
        record.msg = original_msg

        # Determine color with precise pattern matching
        color = self._determine_color(record, str(original_msg))

        if color:
            formatted = f"{color}{formatted}{LogColors.RESET}"

        return formatted

    def _determine_color(self, record: logging.LogRecord, msg: str) -> str:
        """Determine the appropriate color for the log message.

        Strict matching - only colors benchmark status messages,
        not AI model working output (stdout/stderr).
        """
        # Skip AI model output entirely - don't interpret tool results
        if "[stdout]" in msg or "[stderr]" in msg:
            return ""

        # Priority 1: Explicit benchmark success markers (green)
        if any(pattern in msg for pattern in self.SUCCESS_PATTERNS):
            return LogColors.GREEN

        # Priority 2: Explicit benchmark failure markers (red)
        if any(pattern in msg for pattern in self.FAILURE_PATTERNS):
            return LogColors.RED

        # Priority 3: Warning patterns (yellow) - cancelled, skipped, etc.
        if any(pattern.lower() in msg.lower() for pattern in self.WARNING_PATTERNS):
            return LogColors.YELLOW

        # Priority 4: Log level colors for ERROR/WARNING
        if record.levelno >= logging.ERROR:
            return LogColors.RED
        if record.levelno >= logging.WARNING:
            return LogColors.YELLOW

        # Priority 5: Benchmark completion markers (green)
        if any(pattern in msg for pattern in self.COMPLETION_PATTERNS):
            return LogColors.GREEN

        # Priority 6: AI evaluator service logs (magenta)
        if "ai_evaluator" in record.name or "[AI]" in msg:
            return LogColors.MAGENTA

        # Priority 7: Variant/Benchmark status markers (cyan)
        # Match old format [VARIANT], new format [VARIANT:id], and [BENCHMARK] prefix
        if any(marker in msg for marker in (
            "[VANILLA]", "[VANILLA:", "[CCO]", "[CCO:",
            "[BENCHMARK]", "[BENCHMARK:",
            "[CCO Config]", "[CCO Optimize]", "[CCO Review]",
        )):
            return LogColors.CYAN

        # Priority 8: Debug level (gray)
        if record.levelno <= logging.DEBUG:
            return LogColors.GRAY

        # Default: no color
        return ""


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
OUTPUT_DIR = BENCHMARK_DIR / "output"
SUITE_DIR = BENCHMARK_DIR / "suite"
STATIC_DIR = Path(__file__).parent / "static"


# ============== Activity Log ==============


def _truncate_message(message: str, max_len: int = 200) -> str:
    """Truncate message with ellipsis if it exceeds max length.

    Single source of truth for message truncation across the application.
    """
    if len(message) <= max_len:
        return message
    return message[:max_len] + "..."


class ActivityLog:
    """Thread-safe activity log for tracking operations (shown in UI).

    Uses threading.Lock to ensure safe concurrent access from multiple
    background tasks (test execution, pip install, etc.).
    """

    def __init__(self, max_entries: int = 500) -> None:
        self._entries: deque[dict[str, str]] = deque(maxlen=max_entries)
        self._lock = threading.Lock()

    def add(self, message: str, level: str = "info") -> None:
        """Add an entry to the activity log (thread-safe)."""
        # Truncate non-error messages for UI display
        display_message = message if level == "error" else _truncate_message(message)
        entry = {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "message": display_message,
            "level": level,
        }
        with self._lock:
            self._entries.append(entry)
        # Log full message - formatter handles its own truncation
        if level == "error":
            logger.error(message)
        elif level == "warning":
            logger.warning(message)
        else:
            logger.info(message)

    def get_entries(self, limit: int = 50) -> list[dict[str, str]]:
        """Get recent log entries (newest first, thread-safe)."""
        with self._lock:
            entries = list(self._entries)
        return list(reversed(entries[-limit:]))

    def clear(self) -> None:
        """Clear all log entries (thread-safe)."""
        with self._lock:
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

    result: dict[str, Any] = {
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

# Track running tests
running_tests: dict[str, dict[str, Any]] = {}

# Track cancellation requests: {run_id: True}
cancellation_requests: dict[str, bool] = {}

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


class RunTestRequest(BaseModel):
    """Request to run benchmark (vanilla → CCO optimization flow)."""

    project_ids: list[str]
    model: str = "opus"
    resume: bool = False  # If True, resume from last completed phase


class CompareRequest(BaseModel):
    """Request to compare vanilla vs cco for a project."""

    project_id: str


class TestStatus(BaseModel):
    """Status of a benchmark run."""

    project_id: str
    status: str  # "pending", "running", "completed", "failed", "cancelled"
    current_phase: str | None = None
    phases_completed: int = 0
    total_phases: int = 7
    progress: int = 0  # 0-100
    error: str | None = None


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


# ============== Benchmark API ==============


@app.post("/api/run")
async def run_tests(request: RunTestRequest, background_tasks: BackgroundTasks) -> dict[str, Any]:
    """Start benchmark: vanilla → derive CCO → optimize → review → analyze.

    New benchmark flow that measures CCO's optimization capability on existing code
    rather than comparing two independently generated codebases.

    Phases:
    1. vanilla_generation: Generate vanilla project from scratch
    2. vanilla_analysis: Static + AI analysis of vanilla code
    3. cco_derive: Copy vanilla to create CCO base (identical starting point)
    4. cco_config: Run /cco-config --auto
    5. cco_optimize: Run /cco-optimize --auto (all 6 scopes, full fix)
    6. cco_review: Run /cco-review --auto (all 5 scopes, full fix)
    7. cco_analysis: Static + AI analysis of CCO-optimized code
    """
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    if not request.project_ids:
        return {"run_id": run_id, "message": "No projects selected", "count": 0}

    # Validate all project IDs
    valid_projects: list[str] = []
    for pid in request.project_ids:
        project_dir = PROJECTS_DIR / pid
        if project_dir.exists():
            valid_projects.append(pid)
        else:
            log_activity(f"Project not found: {pid}", "warning")

    if not valid_projects:
        return {"run_id": run_id, "message": "No valid projects found", "count": 0}

    # Initialize status for all projects
    for project_id in valid_projects:
        running_tests[f"{run_id}_{project_id}"] = {
            "run_id": run_id,
            "project_id": project_id,
            "status": "pending",
            "current_phase": None,
            "phases_completed": 0,
            "total_phases": 7,
            "progress": 0,
            "error": None,
            "result": None,
            "started_at": datetime.now().isoformat(),
        }

    # Start background execution
    background_tasks.add_task(
        execute_tests_background, run_id, valid_projects, request.model, request.resume
    )

    resume_msg = " (resume mode)" if request.resume else ""
    return {
        "run_id": run_id,
        "message": f"Started benchmark for {len(valid_projects)} project(s){resume_msg}",
        "count": len(valid_projects),
        "flow": "vanilla → derive CCO → optimize → review → analyze",
        "resume": request.resume,
    }


async def execute_tests_background(
    run_id: str, project_ids: list[str], model: str, resume: bool = False
) -> None:
    """Execute benchmark tests in background."""
    executor = TestExecutor(OUTPUT_DIR)
    log_activity(f"Starting benchmark run: {len(project_ids)} project(s)", "info")

    # Results directory
    results_dir = OUTPUT_DIR / "_results"
    results_dir.mkdir(exist_ok=True)

    for project_id in project_ids:
        key = f"{run_id}_{project_id}"

        # Check for cancellation before starting each project
        if cancellation_requests.get(run_id):
            if running_tests[key]["status"] == "pending":
                running_tests[key]["status"] = "cancelled"
                running_tests[key]["error"] = "Cancelled by user"
            log_activity(f"[BENCHMARK] Skipping {project_id} - run cancelled", "warning")
            continue

        project_dir = PROJECTS_DIR / project_id

        if not project_dir.exists():
            running_tests[key]["status"] = "failed"
            running_tests[key]["error"] = f"Project not found: {project_id}"
            log_activity(f"Project not found: {project_id}", "error")
            continue

        config = ProjectConfig(project_dir)
        log_activity(f"[BENCHMARK] Starting: {config.name}", "info")
        running_tests[key]["status"] = "running"

        def progress_callback(
            message: str,
            phase: BenchmarkPhase,
            _key: str = key,
            _project_id: str = project_id,
            _run_id: str = run_id,
        ) -> None:
            """Update progress as phases complete."""
            # Check for cancellation during execution
            if cancellation_requests.get(_run_id):
                running_tests[_key]["status"] = "cancelled"
                running_tests[_key]["error"] = "Cancelled by user"
                raise InterruptedError("Benchmark cancelled by user")

            phases_done = running_tests[_key]["phases_completed"] + 1
            running_tests[_key]["phases_completed"] = phases_done
            running_tests[_key]["current_phase"] = phase.name
            running_tests[_key]["progress"] = int((phases_done / 7) * 100)
            log_activity(f"[BENCHMARK:{_project_id}] {message}", "info")

        try:
            # Run benchmark
            result = await asyncio.to_thread(
                executor.run_benchmark,
                config,
                model,
                progress_callback,
                resume,
            )

            # Check if cancelled during execution
            if running_tests[key]["status"] == "cancelled":
                continue

            # Check if benchmark failed internally (e.g., phase failure)
            verdict = result.comparison.get("verdict", "")
            is_failed = verdict == "Failed" or result.comparison.get("error")

            if is_failed:
                running_tests[key]["status"] = "failed"
                running_tests[key]["error"] = result.comparison.get("error", "Benchmark failed")
                running_tests[key]["progress"] = 100
                running_tests[key]["result"] = result.to_dict()

                # Save failed result for analysis
                result_file = results_dir / f"{project_id}_{run_id}.json"
                result_file.write_text(
                    json.dumps(result.to_dict(), indent=2, default=str),
                    encoding="utf-8",
                )
                log_activity(
                    f"[BENCHMARK] Failed: {config.name} - {result.comparison.get('error', 'Unknown error')}",
                    "error",
                )
            else:
                running_tests[key]["status"] = "completed"
                running_tests[key]["progress"] = 100
                running_tests[key]["result"] = result.to_dict()

                # Save result
                result_file = results_dir / f"{project_id}_{run_id}.json"
                result_file.write_text(
                    json.dumps(result.to_dict(), indent=2, default=str),
                    encoding="utf-8",
                )
                log_activity(
                    f"[BENCHMARK] Completed: {config.name} - {verdict}",
                    "success",
                )

        except InterruptedError:
            log_activity(f"[BENCHMARK] Cancelled: {project_id}", "warning")

        except Exception as e:
            running_tests[key]["status"] = "failed"
            running_tests[key]["error"] = str(e)
            log_activity(f"[BENCHMARK] Failed: {project_id} - {e}", "error")

    # Clean up cancellation request
    if run_id in cancellation_requests:
        del cancellation_requests[run_id]

    # Log final status
    completed = sum(1 for k, v in running_tests.items() if k.startswith(f"{run_id}_") and v["status"] == "completed")
    cancelled = sum(1 for k, v in running_tests.items() if k.startswith(f"{run_id}_") and v["status"] == "cancelled")
    failed = sum(1 for k, v in running_tests.items() if k.startswith(f"{run_id}_") and v["status"] == "failed")

    if cancelled > 0:
        log_activity(f"Benchmark run ended: {completed} completed, {cancelled} cancelled, {failed} failed", "warning")
    else:
        log_activity(f"Benchmark run completed: {completed} succeeded, {failed} failed", "success")


@app.get("/api/running")
async def get_running_tests() -> dict[str, Any]:
    """Get all currently running tests."""
    active_runs: dict[str, list[dict[str, Any]]] = {}
    for status in running_tests.values():
        if status["status"] not in ("completed", "failed", "cancelled"):
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


@app.post("/api/cancel/{run_id}")
async def cancel_benchmark(run_id: str) -> dict[str, Any]:
    """Cancel a running benchmark.

    Sets a cancellation flag that the background task checks.
    Running processes will be terminated gracefully.
    """
    # Check if run exists
    found = False
    cancelled_count = 0
    for key, status in running_tests.items():
        if key.startswith(f"{run_id}_"):
            found = True
            if status["status"] in ("pending", "running"):
                status["status"] = "cancelled"
                status["error"] = "Cancelled by user"
                cancelled_count += 1

    if not found:
        raise HTTPException(404, "Run not found")

    # Set cancellation flag for background task
    cancellation_requests[run_id] = True
    log_activity(f"Benchmark run {run_id} cancelled ({cancelled_count} test(s))", "warning")

    return {
        "message": f"Cancelled {cancelled_count} test(s)",
        "run_id": run_id,
        "cancelled_count": cancelled_count,
    }


@app.get("/api/results")
async def list_results(limit: int = 20) -> list[dict[str, Any]]:
    """List saved benchmark results."""
    results_dir = OUTPUT_DIR / "_results"
    if not results_dir.exists():
        return []

    files = sorted(results_dir.glob("*.json"), reverse=True)[:limit]
    results = []
    for f in files:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            results.append({
                "filename": f.name,
                "project_id": data.get("project_id"),
                "project_name": data.get("project_name"),
                "timestamp": data.get("timestamp"),
                "verdict": data.get("comparison", {}).get("verdict"),
                "score_improvement": data.get("comparison", {}).get("score_improvement"),
                "phases_count": len(data.get("phases", [])),
                "vanilla_score": data.get("vanilla", {}).get("metrics", {}).get("overall_score"),
                "cco_score": data.get("cco", {}).get("metrics", {}).get("overall_score"),
            })
        except Exception:
            pass
    return results


@app.get("/api/results/{filename}")
async def get_result(filename: str) -> dict[str, Any]:
    """Get a specific result by filename."""
    results_dir = OUTPUT_DIR / "_results"
    filepath = results_dir / filename
    if not filepath.exists():
        raise HTTPException(404, "Result not found")

    return json.loads(filepath.read_text(encoding="utf-8"))


@app.delete("/api/results/{filename}")
async def delete_result(filename: str) -> dict[str, str]:
    """Delete a result file."""
    results_dir = OUTPUT_DIR / "_results"
    filepath = results_dir / filename
    if not filepath.exists():
        raise HTTPException(404, "Result not found")

    filepath.unlink()
    return {"message": f"Deleted {filename}"}


# ============== Output & Comparison ==============


@app.get("/api/output")
async def list_output_folders() -> list[dict[str, Any]]:
    """List all output folders with their status and AI comparison info."""
    if not OUTPUT_DIR.exists():
        return []

    # Load saved AI comparisons
    ai_comparisons: dict[str, dict[str, Any]] = {}
    ai_results_dir = OUTPUT_DIR / "_ai_comparisons"
    if ai_results_dir.exists():
        for result_file in ai_results_dir.glob("*.json"):
            try:
                data = json.loads(result_file.read_text(encoding="utf-8"))
                project_id = data.get("project_id")
                if project_id:
                    ai_comparisons[project_id] = {
                        "timestamp": data.get("timestamp"),
                        "verdict": data.get("comparison", {}).get("verdict"),
                        "cco_score": data.get("cco", {}).get("overall_score"),
                        "cco_grade": data.get("cco", {}).get("grade"),
                        "vanilla_score": data.get("vanilla", {}).get("overall_score"),
                        "vanilla_grade": data.get("vanilla", {}).get("grade"),
                        "score_difference": data.get("comparison", {}).get("score_difference"),
                        "production_ready_cco": data.get("comparison", {})
                        .get("production_readiness", {})
                        .get("production_ready", {})
                        .get("b"),
                        "production_ready_vanilla": data.get("comparison", {})
                        .get("production_readiness", {})
                        .get("production_ready", {})
                        .get("a"),
                    }
            except Exception:
                pass

    # Load saved static comparisons
    static_comparisons: dict[str, dict[str, Any]] = {}
    static_results_dir = OUTPUT_DIR / "_static_comparisons"
    if static_results_dir.exists():
        for result_file in static_results_dir.glob("*.json"):
            try:
                data = json.loads(result_file.read_text(encoding="utf-8"))
                project_id = data.get("project_id")
                if project_id:
                    cco_metrics = data.get("cco_metrics", {})
                    vanilla_metrics = data.get("vanilla_metrics", {})
                    static_comparisons[project_id] = {
                        "timestamp": data.get("timestamp"),
                        "verdict": data.get("verdict"),
                        "cco_score": cco_metrics.get("overall_score"),
                        "cco_grade": cco_metrics.get("grade"),
                        "vanilla_score": vanilla_metrics.get("overall_score"),
                        "vanilla_grade": vanilla_metrics.get("grade"),
                        "score_difference": round(
                            (cco_metrics.get("overall_score") or 0)
                            - (vanilla_metrics.get("overall_score") or 0),
                            1,
                        ),
                    }
            except Exception:
                pass

    folders = []
    for folder in sorted(OUTPUT_DIR.iterdir()):
        if not folder.is_dir():
            continue
        # Skip AI comparisons folder
        if folder.name.startswith("_"):
            continue

        # Parse folder name: {project_id}_{variant}
        name = folder.name
        parts = name.rsplit("_", 1)
        if len(parts) != 2:
            continue

        project_id, variant = parts
        if variant not in ("vanilla", "cco"):
            continue

        # Check if folder has content (recursive search, excluding cache/deps dirs)
        skip_dirs = {
            "__pycache__",
            ".mypy_cache",
            ".pytest_cache",
            ".ruff_cache",
            "node_modules",
            ".venv",
            "venv",
            ".deps",  # ccbox dependency cache
            "site-packages",
            ".git",
            "dist",
            "build",
        }
        # Suffixes to skip (e.g., mlserve.egg-info)
        skip_suffixes = (".egg-info",)

        def should_skip(path: Path) -> bool:
            """Check if path should be skipped (deps/cache/build dirs)."""
            for part in path.parts:
                if part in skip_dirs:
                    return True
                if any(part.endswith(suffix) for suffix in skip_suffixes):
                    return True
            return False

        files = [
            f
            for f in (
                list(folder.rglob("*.py")) + list(folder.rglob("*.ts")) + list(folder.rglob("*.js"))
            )
            if not should_skip(f)
        ]
        has_code = len(files) > 0

        # Get modification time
        try:
            mtime = folder.stat().st_mtime
            modified = datetime.fromtimestamp(mtime).isoformat()
        except Exception:
            modified = None

        folder_info: dict[str, Any] = {
            "folder": name,
            "project_id": project_id,
            "variant": variant,
            "has_code": has_code,
            "file_count": len(files),
            "modified": modified,
        }

        # Add AI comparison info if available
        if project_id in ai_comparisons:
            folder_info["ai_comparison"] = ai_comparisons[project_id]

        # Add static comparison info if available
        if project_id in static_comparisons:
            folder_info["static_comparison"] = static_comparisons[project_id]

        folders.append(folder_info)

    return folders


@app.post("/api/compare/{project_id}")
async def compare_project(project_id: str) -> dict[str, Any]:
    """Compare vanilla vs cco output for a project."""
    from ..runner import CodeAnalyzer, compare_metrics

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
        # Use dimension-based overall_score (calculated by CodeAnalyzer)
        vanilla_score = vanilla_metrics.overall_score

        cco_analyzer = CodeAnalyzer(cco_dir)
        cco_metrics = cco_analyzer.analyze()
        cco_metrics.variant = "cco"
        # Use dimension-based overall_score (calculated by CodeAnalyzer)
        cco_score = cco_metrics.overall_score

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
    """Comprehensive multi-dimensional comparison of vanilla vs cco.

    Uses the unified CodeAnalyzer with 6-dimension scoring.
    """
    from ..runner import CodeAnalyzer, compare_comprehensive

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
        # Comprehensive analysis of both variants using unified CodeAnalyzer
        log_activity(f"Starting comprehensive analysis: {project_id}", "info")

        vanilla_analyzer = CodeAnalyzer(vanilla_dir)
        vanilla_metrics = vanilla_analyzer.analyze(comprehensive=True)
        vanilla_metrics.variant = "vanilla"

        cco_analyzer = CodeAnalyzer(cco_dir)
        cco_metrics = cco_analyzer.analyze(comprehensive=True)
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

        # Save static comparison result to file
        static_results_dir = OUTPUT_DIR / "_static_comparisons"
        static_results_dir.mkdir(exist_ok=True)
        result_file = static_results_dir / f"{project_id}.json"
        result_with_timestamp = {
            **result,
            "timestamp": datetime.now().isoformat(),
        }
        result_file.write_text(
            json.dumps(result_with_timestamp, indent=2, default=str),
            encoding="utf-8",
        )
        log_activity(f"Static comparison saved to {result_file.name}", "info")

    except Exception as e:
        import traceback

        logger.error(f"Comprehensive comparison failed: {traceback.format_exc()}")
        result["error"] = f"Comprehensive comparison failed: {e}"

    return result


@app.get("/api/static-comparisons/{project_id}")
async def get_static_comparison(project_id: str) -> dict[str, Any]:
    """Get saved static comparison result for a project."""
    static_results_dir = OUTPUT_DIR / "_static_comparisons"
    result_file = static_results_dir / f"{project_id}.json"

    if not result_file.exists():
        raise HTTPException(status_code=404, detail="Static comparison not found")

    try:
        return json.loads(result_file.read_text(encoding="utf-8"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read result: {e}") from e


@app.delete("/api/static-comparisons/{project_id}")
async def delete_static_comparison(project_id: str) -> dict[str, str]:
    """Delete saved static comparison result for a project."""
    static_results_dir = OUTPUT_DIR / "_static_comparisons"
    result_file = static_results_dir / f"{project_id}.json"

    if not result_file.exists():
        raise HTTPException(status_code=404, detail="Static comparison not found")

    result_file.unlink()
    log_activity(f"Deleted static comparison for {project_id}", "info")
    return {"message": f"Deleted static comparison for {project_id}"}


@app.delete("/api/ai-comparisons/{project_id}")
async def delete_ai_comparison(project_id: str) -> dict[str, str]:
    """Delete saved AI comparison result for a project."""
    ai_results_dir = OUTPUT_DIR / "_ai_comparisons"
    result_file = ai_results_dir / f"{project_id}.json"

    if not result_file.exists():
        raise HTTPException(status_code=404, detail="AI comparison not found")

    result_file.unlink()
    log_activity(f"Deleted AI comparison for {project_id}", "info")
    return {"message": f"Deleted AI comparison for {project_id}"}


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

            # Save AI comparison result to file
            ai_results_dir = OUTPUT_DIR / "_ai_comparisons"
            ai_results_dir.mkdir(exist_ok=True)
            result_file = ai_results_dir / f"{project_id}.json"
            result_with_timestamp = {
                **result,
                "timestamp": datetime.now().isoformat(),
            }
            result_file.write_text(
                json.dumps(result_with_timestamp, indent=2, default=str),
                encoding="utf-8",
            )
            log_activity(f"AI comparison saved to {result_file.name}", "info")

    except Exception as e:
        import traceback

        logger.error(f"AI comparison failed: {traceback.format_exc()}")
        result["error"] = f"AI comparison failed: {e}"
        log_activity(f"AI comparison error: {e}", "error")

    return result


@app.get("/api/ai-comparisons")
async def list_ai_comparisons() -> list[dict[str, Any]]:
    """List all saved AI comparison results."""
    ai_results_dir = OUTPUT_DIR / "_ai_comparisons"
    if not ai_results_dir.exists():
        return []

    results = []
    for result_file in sorted(ai_results_dir.glob("*.json"), reverse=True):
        try:
            data = json.loads(result_file.read_text(encoding="utf-8"))
            results.append(
                {
                    "project_id": data.get("project_id"),
                    "timestamp": data.get("timestamp"),
                    "verdict": data.get("comparison", {}).get("verdict"),
                    "cco_score": data.get("cco", {}).get("overall_score"),
                    "cco_grade": data.get("cco", {}).get("grade"),
                    "vanilla_score": data.get("vanilla", {}).get("overall_score"),
                    "vanilla_grade": data.get("vanilla", {}).get("grade"),
                    "score_difference": data.get("comparison", {}).get("score_difference"),
                    "has_production_readiness": "production_readiness"
                    in data.get("comparison", {}),
                    "filename": result_file.name,
                }
            )
        except Exception:
            pass

    return results


@app.get("/api/ai-comparisons/{project_id}")
async def get_ai_comparison(project_id: str) -> dict[str, Any]:
    """Get saved AI comparison result for a project."""
    ai_results_dir = OUTPUT_DIR / "_ai_comparisons"
    result_file = ai_results_dir / f"{project_id}.json"

    if not result_file.exists():
        raise HTTPException(status_code=404, detail="AI comparison not found")

    try:
        return json.loads(result_file.read_text(encoding="utf-8"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read result: {e}") from e


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


def main(port: int = 8765):
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
    print(f"Open http://localhost:{port} in your browser")
    uvicorn.run(app, host="127.0.0.1", port=port, log_config=log_config)


if __name__ == "__main__":
    main()
