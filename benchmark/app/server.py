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
    BenchmarkResult,
    ProjectConfig,
    ResultsManager,
    TestExecutor,
    discover_projects,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("cco-benchmark")

# Configuration
BENCHMARK_DIR = Path(__file__).parent.parent
PROJECTS_DIR = BENCHMARK_DIR / "projects"
RESULTS_DIR = BENCHMARK_DIR / "results"
OUTPUT_DIR = BENCHMARK_DIR / "output"
STATIC_DIR = Path(__file__).parent / "static"


# ============== Activity Log ==============


class ActivityLog:
    """Activity log for tracking operations (shown in UI)."""

    def __init__(self, max_entries: int = 500) -> None:
        self._entries: deque[dict[str, str]] = deque(maxlen=max_entries)

    def add(self, message: str, level: str = "info") -> None:
        """Add an entry to the activity log."""
        entry = {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "message": message,
            "level": level,
        }
        self._entries.append(entry)
        logger.info(f"[{level.upper()}] {message}")

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


class RunTestRequest(BaseModel):
    project_ids: list[str]
    model: str = "opus"


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
async def run_tests(request: RunTestRequest, background_tasks: BackgroundTasks) -> dict[str, str]:
    """Start benchmark tests for selected projects."""
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Initialize status for all projects
    for project_id in request.project_ids:
        running_tests[f"{run_id}_{project_id}"] = {
            "project_id": project_id,
            "status": "pending",
            "progress": 0,
            "current_variant": None,
            "error": None,
            "result": None,
            "started_at": datetime.now().isoformat(),
        }

    # Start background execution
    background_tasks.add_task(execute_tests_background, run_id, request.project_ids, request.model)

    return {"run_id": run_id, "message": f"Started {len(request.project_ids)} tests"}


async def execute_tests_background(run_id: str, project_ids: list[str], model: str) -> None:
    """Execute tests in background."""
    executor = TestExecutor(OUTPUT_DIR)
    log_activity(f"Starting benchmark run: {len(project_ids)} project(s)", "info")

    for project_id in project_ids:
        key = f"{run_id}_{project_id}"
        project_dir = PROJECTS_DIR / project_id

        if not project_dir.exists():
            running_tests[key]["status"] = "failed"
            running_tests[key]["error"] = f"Project not found: {project_id}"
            log_activity(f"Project not found: {project_id}", "error")
            continue

        config = ProjectConfig(project_dir)
        log_activity(f"Testing project: {config.name}", "info")

        try:
            # Run vanilla
            running_tests[key]["status"] = "running_vanilla"
            running_tests[key]["current_variant"] = "vanilla"
            running_tests[key]["progress"] = 25
            log_activity(f"[VANILLA] Starting: {config.name}", "info")

            vanilla_result = await asyncio.to_thread(executor.run_project, config, "vanilla", model)

            if vanilla_result.success:
                log_activity(
                    f"[VANILLA] Completed: score={vanilla_result.score}, time={vanilla_result.generation_time_seconds:.1f}s",
                    "success",
                )
            else:
                log_activity(f"[VANILLA] FAILED: {vanilla_result.error_message}", "error")
                log_activity(f"[VANILLA] Exit code: {vanilla_result.exit_code}", "error")
                if vanilla_result.command:
                    log_activity(f"[VANILLA] Command: {vanilla_result.command[:150]}...", "warning")
                if vanilla_result.stderr_excerpt:
                    # Show more stderr for debugging
                    stderr_lines = vanilla_result.stderr_excerpt.strip().split("\n")[:5]
                    for line in stderr_lines:
                        if line.strip():
                            log_activity(f"[VANILLA] stderr: {line[:150]}", "warning")
                if vanilla_result.stdout_excerpt and not vanilla_result.stderr_excerpt:
                    stdout_lines = vanilla_result.stdout_excerpt.strip().split("\n")[:3]
                    for line in stdout_lines:
                        if line.strip():
                            log_activity(f"[VANILLA] stdout: {line[:150]}", "warning")
                log_activity(f"[VANILLA] Output dir: {vanilla_result.output_dir}", "info")

            running_tests[key]["progress"] = 50

            # Run CCO (two phases: setup + test)
            running_tests[key]["status"] = "running_cco"
            running_tests[key]["current_variant"] = "cco"
            running_tests[key]["progress"] = 60
            log_activity(f"[CCO] Starting: {config.name} (setup + test phases)", "info")

            cco_result = await asyncio.to_thread(executor.run_project, config, "cco", model)

            running_tests[key]["progress"] = 90

            if cco_result.success:
                log_activity(
                    f"[CCO] Completed: score={cco_result.score}, time={cco_result.generation_time_seconds:.1f}s",
                    "success",
                )
            else:
                log_activity(f"[CCO] FAILED: {cco_result.error_message}", "error")
                log_activity(f"[CCO] Exit code: {cco_result.exit_code}", "error")
                if cco_result.command:
                    log_activity(f"[CCO] Command: {cco_result.command[:150]}...", "warning")
                if cco_result.stderr_excerpt:
                    # Show more stderr for debugging
                    stderr_lines = cco_result.stderr_excerpt.strip().split("\n")[:5]
                    for line in stderr_lines:
                        if line.strip():
                            log_activity(f"[CCO] stderr: {line[:150]}", "warning")
                if cco_result.stdout_excerpt and not cco_result.stderr_excerpt:
                    stdout_lines = cco_result.stdout_excerpt.strip().split("\n")[:3]
                    for line in stdout_lines:
                        if line.strip():
                            log_activity(f"[CCO] stdout: {line[:150]}", "warning")
                log_activity(f"[CCO] Output dir: {cco_result.output_dir}", "info")

            # Build full benchmark result
            from ..runner import compare_metrics

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

            # Save result
            results_manager.save_result(benchmark_result)

            running_tests[key]["status"] = "completed"
            running_tests[key]["progress"] = 100
            running_tests[key]["result"] = benchmark_result.to_dict()
            log_activity(f"Completed: {config.name} - {verdict} (diff: {diff:+.1f})", "success")

        except Exception as e:
            running_tests[key]["status"] = "failed"
            running_tests[key]["error"] = str(e)
            log_activity(f"Failed: {project_id} - {e}", "error")

    log_activity("Benchmark run completed", "success")


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

    # Disable ANSI colors for Windows CMD compatibility
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(message)s"
    log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    log_config["formatters"]["access"]["use_colors"] = False
    log_config["formatters"]["default"]["use_colors"] = False

    print("Starting CCO Benchmark Suite server...")
    print("Open http://localhost:8765 in your browser")
    uvicorn.run(app, host="127.0.0.1", port=8765, log_config=log_config)


if __name__ == "__main__":
    main()
