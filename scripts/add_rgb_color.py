import argparse
from pyntcloud import PyntCloud

from src.rendering.rendering_utils import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enrich .ply model with rgb colors computed from spherical harmonics")

    parser.add_argument('--input', type=str, required=True, help='Path to the model.')

    args = parser.parse_args()

    input_path = args.input

    ptcld = PyntCloud.from_file(input_path)
    normals = compute_normals(input_path)
    colors = sh_to_rgb(ptcld.points, normals)
    enrich(ptcld, colors)
    ptcld.to_file(input_path)