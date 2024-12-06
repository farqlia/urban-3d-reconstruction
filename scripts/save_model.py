import os
import shutil
import argparse
from urb3d.models.model_conversion import convert
from pathlib import Path

def save_pt_model(ckpts_path):
    ckpts = os.listdir(ckpts_path)
    assert str(ckpts_path).endswith("ckpts")
    iter_to_ckpt = {
        int(name.split("_")[1]): name for name in ckpts
    }
    final_model = iter_to_ckpt[max(iter_to_ckpt.keys())]
    model_path = Path(ckpts_path).parent / 'model.pt'
    shutil.copy(Path(ckpts_path) / final_model, model_path)
    return model_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Save Gaussian Splatting torch model from ckpts and convert it to .ply format")

    parser.add_argument('--ckpts', type=str, required=True, help='Path to the ckpts.')
    parser.add_argument('--output', type=str, required=True, help='Path to the ply destination file.')

    args = parser.parse_args()

    ckpts_path = args.ckpts
    output_path = args.output

    pt_model_path = save_pt_model(ckpts_path)
    convert(pt_model_path, output_path)