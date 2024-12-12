import argparse
from pathlib import Path

from urb3d.models.evaluation import Evaluator

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate Gaussian Splatting model on validation dataset")

    root_data_dir = "C:\\Users\\julia\\PycharmProjects\\urban-3d-reconstruction\\data"

    parser.add_argument('--exp_path', type=str, required=True, help='Path to the experiment.')
    parser.add_argument("--project_dir", type=str, default=root_data_dir, help="Path to the parent of the root data directory.")

    args = parser.parse_args()

    exp_path = Path(args.exp_path)
    project_dir = Path(args.project_dir)

    evaluator = Evaluator(exp_path, project_dir)
    evaluator.evaluate()
    evaluator.save_model_description()


