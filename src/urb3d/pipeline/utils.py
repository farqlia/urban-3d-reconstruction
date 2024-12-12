from subprocess import run, CalledProcessError
from config import SCRIPTS_DIR
import sys

def run_script(script_name, *args):
    python_executable = sys.executable
    try:
        run([python_executable, SCRIPTS_DIR / script_name, *args], check=True)
    except CalledProcessError as e:
        raise RuntimeError(f"Failed to execute {script_name})") from e