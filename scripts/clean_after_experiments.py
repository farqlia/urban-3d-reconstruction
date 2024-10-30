import argparse
import os
from pathlib import Path

from src.models.ckpts_cleanup import remove_ckpts

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean experiment directories.")
    parser.add_argument("--model_names", type=str, nargs="+", help="space separated model names")
    parser.add_argument("--input_dir", type=str, help="path to results directory")

    args = parser.parse_args()

    models_names = args.model_names
    input_dir = Path(args.input_dir)

    for model in models_names:
        model_path = input_dir / model
        for experiment_name in os.listdir(model_path):
            experiment_path = Path(model_path) / experiment_name
            if os.path.exists(experiment_path / 'ckpts'):
                print(f"Removing {experiment_path / 'ckpts'} directory")
                remove_ckpts(experiment_path / 'ckpts')
