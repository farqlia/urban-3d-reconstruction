import time
from dataclasses import field
from typing import List

import torch
from gsplat.distributed import cli
from gsplat.strategy import DefaultStrategy, MCMCStrategy

from src.splats.config import Config
from src.splats.training import Runner


def main(local_rank: int, world_rank, world_size: int, cfg: Config):
    if world_size > 1 and not cfg.disable_viewer:
        cfg.disable_viewer = True
        if world_rank == 0:
            print("Viewer is disabled in distributed training.")

    runner = Runner(local_rank, world_rank, world_size, cfg)

    if cfg.ckpt is not None:
        # run eval only
        ckpts = [
            torch.load(file, map_location=runner.device, weights_only=True)
            for file in cfg.ckpt
        ]
        for k in runner.splats.keys():
            runner.splats[k].data = torch.cat([ckpt["splats"][k] for ckpt in ckpts])
        step = ckpts[0]["step"]
        runner.eval(step=step)
        runner.render_traj(step=step)
        if cfg.compression is not None:
            runner.run_compression(step=step)
    else:
        runner.train()

    if not cfg.disable_viewer:
        print("Viewer running... Ctrl+C to exit.")
        time.sleep(1000000)

# TODO: configuration should be saved! (later for comparison)
# TODO: what does batch size mean?
if __name__ == "__main__":
    """
    Usage:

    ```bash
    # Single GPU training
    CUDA_VISIBLE_DEVICES=0 python simple_trainer.py default

    # Distributed training on 4 GPUs: Effectively 4x batch size so run 4x less steps.
    CUDA_VISIBLE_DEVICES=0,1,2,3 python simple_trainer.py default --steps_scaler 0.25

    """

    init_type = "random"
    strategy = "mcmc"
    max_steps: int = 100_000

    init_num_pts: int = 100_000 # only for random

    data_dir = "../data/small_city_road_down_test"
    result_dir = f"../results/small_city_road_down_test/{init_type}/{strategy}/epochs_{max_steps}"

    eval_steps_mapping = {
        100_000: [2000, 10_000, 30_000, 50_000, 60_000, 75_000, 100_000]
    }

    # Steps to evaluate the model
    eval_steps: List[int] = eval_steps_mapping[max_steps]
    # Steps to save the model
    save_steps: List[int] = eval_steps_mapping[max_steps]

    # Config objects we can choose between.
    # Each is a tuple of (CLI description, config object).
    configs = {
        "default": (
            "Gaussian splatting training using densification heuristics from the original paper.",
            Config(
                data_dir=data_dir,
                result_dir=result_dir,
                init_type=init_type,
                max_steps=max_steps,
                eval_steps=eval_steps,
                init_num_pts=init_num_pts,
                save_steps=save_steps,
                strategy=DefaultStrategy(verbose=True),
            ),
        ),
        "mcmc": (
            "Gaussian splatting training using densification from the paper '3D Gaussian Splatting as Markov Chain Monte Carlo'.",
            Config(
                data_dir=data_dir,
                result_dir=result_dir,
                init_type=init_type,
                eval_steps=eval_steps,
                save_steps=save_steps,
                max_steps=max_steps,
                init_num_pts=init_num_pts,
                init_opa=0.5,
                init_scale=0.1,
                opacity_reg=0.01,
                scale_reg=0.01,
                strategy=MCMCStrategy(verbose=True),
            ),
        ),
    }
    cfg = configs[strategy][1] # tyro.extras.overridable_config_cli(configs)
    cfg.adjust_steps(cfg.steps_scaler)

    # try import extra dependencies
    if cfg.compression == "png":
        try:
            import plas
            import torchpq
        except:
            raise ImportError(
                "To use PNG compression, you need to install "
                "torchpq (instruction at https://github.com/DeMoriarty/TorchPQ?tab=readme-ov-file#install) "
                "and plas (via 'pip install git+https://github.com/fraunhoferhhi/PLAS.git') "
            )

    cli(main, cfg, verbose=True)
