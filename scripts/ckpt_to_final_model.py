import argparse
from pathlib import Path

from urb3d.models.save_model import save_ckpt

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Gaussian Splatting torch model to .ply format")

    parser.add_argument('--ckpts_dir', type=str, required=True, help='Path to the ckpts dir.')

    args = parser.parse_args()

    ckpts_dir = args.ckpts_dir
    save_ckpt(Path(ckpts_dir))