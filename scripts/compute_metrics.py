import os

import numpy as np
from torch.fx.experimental.meta_tracer import torch_abs_override
from torchmetrics.image import StructuralSimilarityIndexMeasure, PeakSignalNoiseRatio, \
    LearnedPerceptualImagePatchSimilarity
import imageio
import torch
import argparse
from pathlib import Path

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
SSIM = StructuralSimilarityIndexMeasure(data_range=1.0).to(device)
PSNR = PeakSignalNoiseRatio(data_range=1.0).to(device)
LPIPS = LearnedPerceptualImagePatchSimilarity(
            net_type="alex", normalize=True
        ).to(device)

def compute_metrics(pred_img, real_img):
    pred = torch.tensor(imageio.v2.imread(pred_img) / 255.0).type(torch.float32).to(device)[None, ...]
    real = torch.tensor(imageio.v2.imread(real_img) / 255.0).type(torch.float32).to(device)[None, ...]

    pred_p = pred.permute(0, 3, 1, 2)  # [1, 3, H, W]
    real_p = real.permute(0, 3, 1, 2)  # [1, 3, H, W]
    return PSNR(pred_p, real_p), SSIM(pred_p, real_p), LPIPS(pred_p, real_p)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate rendered images against real ones.")

    parser.add_argument("--render_dir", type=str, required=True, help='Path to the directory of rendered images.')
    parser.add_argument("--real_dir", type=str, required=True, help='Path to the directory of real images.')

    args = parser.parse_args()

    render_dir = Path(args.render_dir)
    real_dir = Path(args.real_dir)

    n = len(os.listdir(render_dir))

    for name in zip([f"eval_{i:04d}.png" for i in range(n)], [f"img_{i:04d}.png" for i in range(n)]):
        psnr, ssim, lpips = compute_metrics(render_dir / name[0], real_dir / name[1])
        print(f"Image {name[1]} metrics: psnr = {psnr:.3f}, ssim = {ssim:.3f}, lpips = {lpips:.3f}")
