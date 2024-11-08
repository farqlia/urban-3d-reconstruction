import argparse
from src.models.model_conversion import convert

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Gaussian Splatting torch model to .ply format")

    parser.add_argument('--input', type=str, required=True, help='Path to the model.')
    parser.add_argument('--output', type=str, required=True, help='Path to the point cloud destination file.')

    args = parser.parse_args()

    input_path = args.input
    output_path = args.output

    convert(input_path, output_path)