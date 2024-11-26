from subprocess import run, CalledProcessError
from .config import SCRIPTS_DIR

def run_script(script_name, *args):
    try:
        run(["python", SCRIPTS_DIR / script_name, *args], check=True)
    except CalledProcessError as e:
        raise RuntimeError(f"Failed to execute {script_name})") from e