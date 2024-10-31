import argparse
import os
import shutil
from pathlib import Path
import pandas as pd

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean experiment directory.")
    parser.add_argument("--input_dir", type=str, help="Path to model/experiment")

    args = parser.parse_args()

    experiment_path = Path(args.input_dir)

    if os.path.exists(experiment_path / 'ckpts'):
        print(f"Removing {experiment_path / 'ckpts'} directory")
        shutil.rmtree(experiment_path / 'ckpts')

    if os.path.exists(experiment_path / 'stats'):
        print(f"Removing {experiment_path / 'stats'} directory")
        shutil.rmtree(experiment_path / "stats", ignore_errors=True)

    if os.path.exists(experiment_path / 'renders'):
        print(f"Removing {experiment_path / 'renders'} directory")
        shutil.rmtree(experiment_path / "renders", ignore_errors=True)

    if os.path.exists(experiment_path / 'videos'):
        print(f"Removing {experiment_path / 'videos'} directory")
        shutil.rmtree(experiment_path / "videos", ignore_errors=True)