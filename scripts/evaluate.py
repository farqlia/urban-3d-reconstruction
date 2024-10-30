import argparse
from src.models.evaluation import Evaluator

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Gaussian Splatting torch model to .ply format")

    root_data_dir = "C:\\Users\\julia\\PycharmProjects\\urban-3d-reconstruction\\data"

    parser.add_argument('--model_path', type=str, required=True, help='Path to the model checkpoint.')
    parser.add_argument('--cfg_path', type=str, required=True, help='Path to the config file (csv format!).')
    parser.add_argument("--root_data_dir", type=str, default=root_data_dir, help="Path to the root data directory.")

    args = parser.parse_args()

    model_path = args.model_path
    cfg_path = args.cfg_path
    root_data_dir = args.root_data_dir

    evaluator = Evaluator(model_path, cfg_path, root_data_dir)
    evaluator.evaluate()


