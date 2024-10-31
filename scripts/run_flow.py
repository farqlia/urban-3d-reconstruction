import argparse
import subprocess
import os
from pathlib import Path

def run_experiment(experiment_path, data_root):
    # Define paths for each step based on the experiment path
    input_dir = Path(experiment_path)
    model_input = os.path.join(input_dir, "model.pt")
    model_output = os.path.join(input_dir, "model.ply")
    data_dir = os.path.join(data_root, "data")

    # Step 1: Convert config to CSV
    print("Converting config to CSV...")
    subprocess.run([
        "python", "./scripts/config_to_csv.py",
        "--input_dir", input_dir
    ], check=True)

    # Step 2: Evaluate
    print("Running evaluation...")
    subprocess.run([
        "python", "./scripts/evaluate.py",
        "--exp_path", input_dir,
        "--project_dir", data_dir
    ], check=True)

    # Step 3: Clean up
    print("Cleaning up...")
    subprocess.run([
        "python", "./scripts/clean_after_experiments.py",
        "--input_dir", input_dir
    ], check=True)

    # Step 4: Convert to cloud format (PLY)
    print("Converting model to PLY format...")
    subprocess.run([
        "python", "./scripts/torch_model_to_ply.py",
        "--input", model_input,
        "--output", model_output
    ], check=True)

    print("All steps completed successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run workload after model training")

    parser.add_argument('--experiment_path', type=str, required=True, help='Path to the experiment.')
    parser.add_argument('--data_root', type=str, required=True, help='Path to the data root dir.')

    args = parser.parse_args()

    experiment_path = args.experiment_path
    data_root = args.data_root

    run_experiment(experiment_path, data_root)