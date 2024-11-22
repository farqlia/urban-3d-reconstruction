import json
from collections import defaultdict

import imageio
import numpy as np
import pandas as pd
import torch
from gsplat import DefaultStrategy, MCMCStrategy
from torchmetrics.image import StructuralSimilarityIndexMeasure, PeakSignalNoiseRatio, \
    LearnedPerceptualImagePatchSimilarity

from urb3d.models.save_model import save_ckpt
from urb3d.datasets.colmap import Dataset
from urb3d.splats.config import Config
from urb3d.splats.rasterization import Rasterizer

import os
from pathlib import Path


def read_training_time(stats_path):
    stats = os.listdir(stats_path)
    iter_to_ckpt = {
        int(name.split("_")[1][4:]): name for name in stats if name.startswith("train")
    }
    final_stat = iter_to_ckpt[max(iter_to_ckpt.keys())]
    with open(stats_path / final_stat) as f:
        stat_json = json.load(f)
    return stat_json["ellipse_time"]

def open_cfg(cfg_path, root_data_dir):
    config = pd.read_csv(cfg_path)

    strategy = DefaultStrategy() if config.loc[0, "strategy"] == "default" else MCMCStrategy()

    return Config(
        data_dir=str((root_data_dir / Path(config.loc[0, "data_dir"]).resolve())),
        data_factor=config.loc[0, "data_factor"],
        normalize_world_space=config.loc[0, "normalize_world_space"],
        test_every=config.loc[0, "test_every"],
        antialiased=False,
        strategy=strategy,
        sh_degree=config.loc[0, 'sh_degree'],
        packed=config.loc[0, "packed"],
        sparse_grad=config.loc[0, "sparse_grad"],
        camera_model=config.loc[0, "camera_model"],
    )


class Evaluator:

    # cfg_path: already as csv file
    def __init__(self, exp_path, root_data_dir):
        self.experiment_path = exp_path
        self.cfg_path = exp_path / 'cfg.csv'

        if os.path.exists(self.experiment_path / 'ckpts'):
            self._max_iter = save_ckpt(exp_path / 'ckpts')
        else:
            self._max_iter = 0

        model_path = exp_path / 'model.pt'
        self.cfg = open_cfg(self.cfg_path, Path(root_data_dir))
        self.scene_name = Path(model_path).parents[1].name
        self.scene_path = Path(model_path).parents[1]
        self.rasterizer = Rasterizer(model_path, self.cfg)
        self.device=torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.ssim = StructuralSimilarityIndexMeasure(data_range=1.0).to(self.device)
        self.psnr = PeakSignalNoiseRatio(data_range=1.0).to(self.device)
        self.lpips = LearnedPerceptualImagePatchSimilarity(
            net_type="alex", normalize=True
        ).to(self.device)
        self.valset = Dataset(self.rasterizer.parser, split="val")
        self.trainset = Dataset(self.rasterizer.parser, split="train")

    def save_model_description(self, split="val"):
        stat_file = f"{self.experiment_path}/eval_{split}.json"
        with open(stat_file) as f:
            stats = json.load(f)
            stats_df = pd.DataFrame(stats, index=[0])

        config = pd.read_csv(self.cfg_path)
        config['experiment'] = self.experiment_path.name
        config['iteration'] = self._max_iter
        description = pd.concat((config, stats_df), axis=1)
        file = self.experiment_path / 'description.csv'
        print(f"Save model description to {file}")
        description.to_csv(file, index=False)


    def save_true_img(self, pixels, i):
        pixels = pixels.squeeze(0).cpu().numpy()
        pixels = (pixels * 255).astype(np.uint8)
        imageio.imwrite(
            f"{self.render_true_dir}/img_{i:04d}.png",
            pixels,
        )

    def save_render_img(self, colors, i):
        colors = colors.squeeze(0).cpu().numpy()
        colors = (colors * 255).astype(np.uint8)
        imageio.imwrite(
            f"{self.render_eval_dir}/eval_{i:04d}.png",
            colors,
        )

    def evaluate(self, split="val"):
        print("Running evaluation...")
        device = self.device

        self.render_eval_dir = self.experiment_path / f'renders_{split}'
        self.render_true_dir = self.scene_path / f'images_{split}'
        os.makedirs(self.render_eval_dir, exist_ok=True)
        os.makedirs(self.render_true_dir, exist_ok=True)

        if split == "val":
            loader = torch.utils.data.DataLoader(
                self.valset, batch_size=1, shuffle=False, num_workers=1
            )
        else:
            loader = torch.utils.data.DataLoader(
                self.trainset, batch_size=1, shuffle=False, num_workers=1
            )

        metrics = defaultdict(list)
        for i, data in enumerate(loader):
            camtoworlds = data["camtoworld"].to(device)
            Ks = data["K"].to(device)
            pixels = data["image"].to(device) / 255.0
            masks = data["mask"].to(device) if "mask" in data else None
            height, width = pixels.shape[1:3]

            torch.cuda.synchronize()
            colors, _, _ = self.rasterizer.rasterize_splats(
                camtoworlds=camtoworlds,
                Ks=Ks,
                width=width,
                height=height,
                masks=masks,
            )  # [1, H, W, 3]
            torch.cuda.synchronize()

            colors = torch.clamp(colors, 0.0, 1.0)

            self.save_true_img(pixels, i)
            self.save_render_img(colors, i)

            '''
            canvas_list = [pixels, colors]
            canvas = torch.cat(canvas_list, dim=2).squeeze(0).cpu().numpy()
            canvas = (canvas * 255).astype(np.uint8)
            imageio.imwrite(
                f"{self.render_eval_dir}/eval_{i:04d}.png",
                canvas,
            )
            '''

            pixels_p = pixels.permute(0, 3, 1, 2)  # [1, 3, H, W]
            colors_p = colors.permute(0, 3, 1, 2)  # [1, 3, H, W]
            metrics["psnr"].append(self.psnr(colors_p, pixels_p))
            metrics["ssim"].append(self.ssim(colors_p, pixels_p))
            metrics["lpips"].append(self.lpips(colors_p, pixels_p))


        stats = {k: torch.stack(v).mean().item() for k, v in metrics.items()}
        stats.update(
            {
                "num_GS": len(self.rasterizer.splats["means"]),
            }
        )

        if os.path.exists(self.experiment_path / "stats"):
            stats.update({
                "time": read_training_time(self.experiment_path / "stats")
            })
        else:
            stats.update({
                "time": 0.0
            })

        print(
            f"PSNR: {stats['psnr']:.3f}, SSIM: {stats['ssim']:.4f}, LPIPS: {stats['lpips']:.3f} "
            f"Number of GS: {stats['num_GS']}"
        )
        # save stats as json
        stat_file = f"{self.experiment_path}/eval_{split}.json"
        with open(stat_file, "w") as f:
            print(f"Stats for {self.scene_name} are saved to {stat_file}")
            json.dump(stats, f)