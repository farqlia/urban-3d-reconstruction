import argparse
import subprocess
import os
from pathlib import Path

def run_experiment(experiment_path, project_dir):
    # Define paths for each step based on the experiment path
    input_dir = Path(experiment_path)
    model_input = os.path.join(input_dir, "model.pt")
    model_output = os.path.join(input_dir, "model.ply")


    print("Converting config to CSV...")
    subprocess.run([
        "python", "./scripts/config_to_csv.py",
        "--input_dir", input_dir
    ], check=True)


    print("Running evaluation...")
    subprocess.run([
        "python", "./scripts/evaluate.py",
        "--exp_path", input_dir,
        "--project_dir", project_dir
    ], check=True)


    print("Converting model to PLY format...")
    subprocess.run([
        "python", "./scripts/torch_model_to_ply.py",
        "--input", model_input,
        "--output", model_output
    ], check=True)

    print("Adding rgb color...")
    subprocess.run([
        "python", "./scripts/add_rgb_color.py",
        "--input", model_output,
    ], check=True)

    print("Compute image evaluation metrics...")
    subprocess.run([
        "python", "./scripts/compute_metrics.py",
        "--render_dir", input_dir / 'renders_val',
        "--real_dir", input_dir.parent / 'images_val',
        "--output_dir", input_dir / 'renders_val_'
    ], check=True)


    print("Cleaning up...")
    subprocess.run([
        "python", "./scripts/clean_after_experiments.py",
        "--input_dir", input_dir
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