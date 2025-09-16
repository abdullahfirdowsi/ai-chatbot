"""
Enhanced Server Startup Script (Upgraded)
- Adds CLI options (host/port/reload/workers/log-level)
- Smarter env checks (supports GROQ_API_KEY/OPENAI_API_KEY, MONGO_URI)
- Optional dependency installation and pip upgrade
- Better logging and helpful startup output
- Uses venv python directly; no interactive shell activation required
"""
import os
import sys
import subprocess
import platform
import socket
import argparse
from pathlib import Path
from dotenv import load_dotenv
import logging

# Configure logging (can be overridden by --log-level)
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger("start_server")

# Constants
VENV_NAME = "venv"
REQUIREMENTS_FILE = "requirements.txt"
PROJECT_ROOT = Path(__file__).parent
VENV_PATH = PROJECT_ROOT / VENV_NAME
IS_WINDOWS = platform.system() == "Windows"
PYTHON_EXE = "python" if IS_WINDOWS else "python3"


def run_command(command, shell=False, capture_output=False):
    """Run a command and return the result."""
    try:
        display = command if isinstance(command, str) else " ".join(map(str, command))
        logger.debug(f"Running: {display}")
        result = subprocess.run(
            command,
            shell=shell,
            capture_output=capture_output,
            text=True,
            cwd=PROJECT_ROOT,
        )
        return result
    except Exception as e:
        logger.error(f"Command failed: {e}")
        return None


def check_python_installation():
    """Check if Python is installed and accessible."""
    try:
        result = subprocess.run([PYTHON_EXE, "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            out = (result.stdout or result.stderr).strip()
            logger.info(f"Python detected: {out}")
            return True
        logger.error("Python not found in PATH")
        return False
    except FileNotFoundError:
        logger.error("Python not found. Please install Python 3.9+ and add it to PATH.")
        return False


def check_venv_exists():
    """Check if virtual environment exists."""
    if IS_WINDOWS:
        python_exe = VENV_PATH / "Scripts" / "python.exe"
        pip_exe = VENV_PATH / "Scripts" / "pip.exe"
    else:
        python_exe = VENV_PATH / "bin" / "python"
        pip_exe = VENV_PATH / "bin" / "pip"

    exists = python_exe.exists() and pip_exe.exists()
    if exists:
        logger.info(f"Virtual environment found: {VENV_PATH}")
    else:
        logger.info(f"Virtual environment not found at: {VENV_PATH}")

    return exists


def create_virtual_environment():
    """Create a new virtual environment."""
    logger.info(f"Creating virtual environment at {VENV_PATH}...")

    # Remove existing venv if it exists but is broken
    if VENV_PATH.exists():
        logger.info("Removing existing virtual environment (fresh setup)...")
        import shutil
        shutil.rmtree(VENV_PATH)

    # Create new virtual environment
    result = run_command([PYTHON_EXE, "-m", "venv", str(VENV_PATH)])

    if result and result.returncode == 0:
        logger.info("Virtual environment created successfully")
        return True
    else:
        logger.error("Failed to create virtual environment")
        return False


def get_venv_python():
    """Get the path to the Python executable in the virtual environment."""
    if IS_WINDOWS:
        return VENV_PATH / "Scripts" / "python.exe"
    else:
        return VENV_PATH / "bin" / "python"


def get_venv_pip():
    """Get the path to the pip executable in the virtual environment."""
    if IS_WINDOWS:
        return VENV_PATH / "Scripts" / "pip.exe"
    else:
        return VENV_PATH / "bin" / "pip"


def install_requirements(upgrade_pip: bool = True) -> bool:
    """Install requirements in the virtual environment."""
    requirements_path = PROJECT_ROOT / REQUIREMENTS_FILE

    if not requirements_path.exists():
        logger.warning(f"{REQUIREMENTS_FILE} not found, skipping dependency installation")
        return True

    pip_exe = get_venv_pip()

    if upgrade_pip:
        logger.info("Upgrading pip...")
        run_command([str(get_venv_python()), "-m", "pip", "install", "--upgrade", "pip"])  # best-effort

    logger.info(f"Installing dependencies from {REQUIREMENTS_FILE}...")
    result = run_command([str(pip_exe), "install", "-r", str(requirements_path)])

    if result and result.returncode == 0:
        logger.info("Dependencies installed successfully")
        return True
    else:
        logger.error("Failed to install dependencies")
        if result and result.stderr:
            logger.error(result.stderr)
        return False


def check_dependencies() -> bool:
    """Check if critical dependencies are installed."""
    logger.info("Checking critical dependencies...")

    critical_packages = ["fastapi", "uvicorn", "pymongo", "groq"]
    pip_exe = get_venv_pip()

    missing_packages = []

    for package in critical_packages:
        result = run_command([str(pip_exe), "show", package], capture_output=True)
        if not result or result.returncode != 0:
            missing_packages.append(package)

    if missing_packages:
        logger.warning(f"Missing packages: {', '.join(missing_packages)}")
        return False
    else:
        logger.info("All critical dependencies are installed")
        return True


def setup_virtual_environment(skip_install: bool = False) -> bool:
    """Set up virtual environment with all dependencies."""
    logger.info("Setting up virtual environment...")

    # Check if Python is installed
    if not check_python_installation():
        return False

    # Check if venv exists
    if not check_venv_exists():
        # Create virtual environment
        if not create_virtual_environment():
            return False

    if not skip_install:
        # Check dependencies
        if not check_dependencies():
            logger.info("Installing missing dependencies...")
            if not install_requirements():
                return False

    logger.info("Virtual environment setup complete")
    return True


def check_port_available(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        try:
            result = s.connect_ex((host, port))
            return result != 0
        except OSError:
            return True  # treat as available if check fails


def start_server_in_venv(host: str, port: int, reload: bool, log_level: str, workers: int | None):
    """Start the server using the virtual environment Python with provided options."""
    python_exe = get_venv_python()

    command = [str(python_exe), "-m", "uvicorn", "app.main:app", "--host", host, "--port", str(port), "--log-level", log_level]

    # workers cannot be used with --reload; prefer reload in dev
    if reload:
        command.append("--reload")
    elif workers and workers > 1:
        command.extend(["--workers", str(workers)])

    logger.info("Starting FastAPI server...")
    logger.info(f"URL: http://{host}:{port}  (Docs: http://{host}:{port}/docs)")

    try:
        subprocess.run(command, cwd=PROJECT_ROOT)
    except KeyboardInterrupt:
        logger.info("\nServer stopped by user")
    except Exception as e:
        logger.error(f"\nServer startup failed: {e}")


def check_critical_environment() -> bool:
    """Check only critical environment variables."""
    # Load .env from project root if present
    env_path = PROJECT_ROOT / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
    else:
        load_dotenv()  # fallback to default search

    # Support either GROQ_API_KEY or OPENAI_API_KEY; and MONGO_URI if used
    critical_sets = [
        ("GROQ_API_KEY",),
        ("OPENAI_API_KEY",),
    ]
    has_llm_key = any(os.getenv(v) for vs in critical_sets for v in vs)

    mongo_ok = True
    if "MONGO_URI" in (open(".env").read() if env_path.exists() else ""):
        mongo_ok = bool(os.getenv("MONGO_URI"))

    missing = []
    if not has_llm_key:
        missing.append("GROQ_API_KEY or OPENAI_API_KEY")
    if not mongo_ok:
        missing.append("MONGO_URI")

    if missing:
        logger.error("Missing critical environment variables:")
        for var in missing:
            logger.error(f"  - {var}")
        return False

    return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Start the FastAPI backend server")
    parser.add_argument("--host", default=os.getenv("HOST", "0.0.0.0"), help="Bind address (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=int(os.getenv("PORT", "8000")), help="Port to listen on (default: 8000)")
    parser.add_argument("--reload", action="store_true", default=os.getenv("RELOAD", "true").lower() == "true", help="Enable auto-reload for development")
    parser.add_argument("--log-level", default=os.getenv("LOG_LEVEL", "info"), choices=["critical", "error", "warning", "info", "debug", "trace"])
    parser.add_argument("--workers", type=int, default=None, help="Number of worker processes (ignored when --reload is set)")
    parser.add_argument("--skip-env-check", action="store_true", help="Skip environment variable checks")
    parser.add_argument("--no-install", action="store_true", help="Skip dependency installation step")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    print("🚀 Starting AI Tutor Backend...")

    # Setup virtual environment
    print("🔧 Preparing virtual environment...")
    if not setup_virtual_environment(skip_install=args.no_install):
        print("❌ Failed to setup virtual environment")
        sys.exit(1)

    # Environment checks
    if not args.skip_env_check:
        print("🔎 Validating environment configuration...")
        if not check_critical_environment():
            print("❌ Server startup aborted due to missing critical configuration")
            print("   Copy .env.example to .env and fill in the required values")
            sys.exit(1)

    # Port availability
    if not check_port_available(args.host, args.port):
        print(f"⚠️ Port {args.port} on {args.host} is already in use. Choose a different --port or stop the other process.")
        sys.exit(1)

    # Start server using virtual environment
    start_server_in_venv(args.host, args.port, args.reload, args.log_level, args.workers)
