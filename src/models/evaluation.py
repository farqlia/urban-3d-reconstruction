import json
import json
import os
from collections import defaultdict
from pathlib import Path

import imageio
import numpy as np
import pandas as pd
import torch
from gsplat import DefaultStrategy, MCMCStrategy
from torchmetrics.image import StructuralSimilarityIndexMeasure, PeakSignalNoiseRatio, \
    LearnedPerceptualImagePatchSimilarity

from src.datasets.colmap import Dataset
from src.splats.config import Config
from src.splats.rasterization import Rasterizer

import os
import shutil
from pathlib import Path


def save_ckpt(ckpt_path) -> int:
    '''
    Saves the model from the last checkpoint and removes all other checkpoints
    :param ckpt_path: path to checkpoint directories
    :return iteration at which the checkpoint was saved
    '''
    ckpts = os.listdir(ckpt_path)
    assert str(ckpt_path).endswith("ckpts")
    iter_to_ckpt = {
        int(name.split("_")[1]): name for name in ckpts
    }
    final_model = iter_to_ckpt[max(iter_to_ckpt.keys())]
    shutil.copy(ckpt_path / final_model, ckpt_path.parent / 'model.pt')
    print(f"...Saving model {final_model}")
    return max(iter_to_ckpt.keys())

def open_cfg(cfg_path, root_data_dir):
    config = pd.read_csv(cfg_path)

    strategy = DefaultStrategy() if config.loc[0, "strategy"] == "default" else MCMCStrategy()

    return Config(
        data_dir=str((root_data_dir / Path(config.loc[0, "data_dir"])).resolve()),
        data_factor=config.loc[0, "data_factor"],
        normalize_world_space=config.loc[0, "normalize_world_space"],
        test_every=config.loc[0, "test_every"],
        antialiased=False,
        strategy=strategy,
        packed=config.loc[0, "packed"],
        sparse_grad=config.loc[0, "sparse_grad"],
        camera_model=config.loc[0, "camera_model"],
    )


class Evaluator:

    # cfg_path: already as csv file
    def __init__(self, exp_path, root_data_dir):
        self.experiment_path = exp_path
        self.cfg_path = exp_path / 'cfg.csv'
        self._max_iter = save_ckpt(exp_path / 'ckpts')
        model_path = exp_path / 'model.pt'
        self.cfg = open_cfg(self.cfg_path, Path(root_data_dir))
        self.render_dir = self.experiment_path / 'eval_renders'
        os.makedirs(self.render_dir, exist_ok=True)
        self.scene_name = Path(model_path).parents[1].name
        self.rasterizer = Rasterizer(model_path, self.cfg)
        self.device=torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.ssim = StructuralSimilarityIndexMeasure(data_range=1.0).to(self.device)
        self.psnr = PeakSignalNoiseRatio(data_range=1.0).to(self.device)
        self.lpips = LearnedPerceptualImagePatchSimilarity(
            net_type="alex", normalize=True
        ).to(self.device)
        self.valset = Dataset(self.rasterizer.parser, split="val")

    def save_model_description(self):
        stat_file = f"{self.experiment_path}/final_eval.json"
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


    def evaluate(self):
        print("Running evaluation...")
        device = self.device

        valloader = torch.utils.data.DataLoader(
            self.valset, batch_size=1, shuffle=False, num_workers=1
        )
        metrics = defaultdict(list)
        for i, data in enumerate(valloader):
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
            canvas_list = [pixels, colors]

            canvas = torch.cat(canvas_list, dim=2).squeeze(0).cpu().numpy()
            canvas = (canvas * 255).astype(np.uint8)
            imageio.imwrite(
                f"{self.render_dir}/eval_{i:04d}.png",
                canvas,
            )

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
        print(
            f"PSNR: {stats['psnr']:.3f}, SSIM: {stats['ssim']:.4f}, LPIPS: {stats['lpips']:.3f} "
            f"Number of GS: {stats['num_GS']}"
        )
        # save stats as json
        stat_file = f"{self.experiment_path}/final_eval.json"
        with open(stat_file, "w") as f:
            print(f"Stats for {self.scene_name} are saved to {stat_file}")
            json.dump(stats, f)


if __name__ == "__main__":
    evaluator = Evaluator("../../results/c5/monkey",
                          "../../results/c5/monkey/cfg.csv",
                          "C:\\Users\\julia\\PycharmProjects\\urban-3d-reconstruction")

    evaluator.evaluate()
