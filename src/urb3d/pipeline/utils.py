import os.path
from subprocess import run, CalledProcessError

from src.urb3d.pipeline.config import SCRIPTS_DIR


# TODO: handle exceptions
def run_script(script_name, *args):
    try:
        run(["python", SCRIPTS_DIR / script_name, *args], check=True)
    except CalledProcessError as e:
        raise RuntimeError(f"Failed to execute {script_name})") from e

# env_path: path to a given python.exe
def run_script_with_env(env_path, script_name, *args):
    try:
        if os.path.exists(env_path):
            run([env_path, SCRIPTS_DIR / script_name, *args], check=True)
        else:
            run_script(script_name, *args)
    except CalledProcessError as e:
        raise RuntimeError(f"Failed to execute {script_name})") from e