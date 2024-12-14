import time
from dataclasses import field
from typing import List

import torch
from gsplat.distributed import cli
from gsplat.strategy import DefaultStrategy, MCMCStrategy

from urb3d.splats.config import Config
from urb3d.splats.training import Runner
import argparse
from typing import List


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
        # runner.render_traj(step=step)
        # if cfg.compression is not None:
          #   runner.run_compression(step=step)
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

    parser = argparse.ArgumentParser(description="Script to run model training with configurable parameters.")

    # Define command-line arguments for each parameter except eval_steps and save_steps
    parser.add_argument("--data_dir", type=str, help="Path to the data directory.", required=True)
    parser.add_argument("--result_dir", type=str, help="Path to the results directory.", required=True)

    # -------------- ARGUMENTS FOR USER ----------------------
    parser.add_argument("--strategy", type=str, default="default", help="Strategy type.", choices=["default", "mcmc"])
    parser.add_argument("--max_steps", type=int, default=100_000, help="Maximum number of steps.")
    # Only for MCMC
    parser.add_argument("--cap_max", type=int, default=3_000_000,
                        help="Maximum cap for MCMC gaussians. [strategy=mcmc]")
    parser.add_argument("--refine_every", type=int, default=100, help="Refine frequency (iterations).")  # tune?

    parser.add_argument("--sh_degree", type=int, default=3, choices=[1, 2, 3], help="Degree of spherical harmonics.")
    # -------------- END ARGUMENTS FOR USER ----------------------

    parser.add_argument("--sh_degree_interval", type=int, default=5_000,
                        help="Add spherical harmonics degree interval.")
    parser.add_argument("--data_factor", type=int, default=1, help="Data factor.")
    parser.add_argument("--init_type", type=str, default="sfm", help="Initialization type.", choices=["sfm", "random"])
    parser.add_argument("--init_num_pts", type=int, default=300_000, help="Initial number of points (only for random).")
    parser.add_argument("--delta_steps", type=int, default=2_500, help="Delta steps for evaluation and saving.")
    parser.add_argument("--scale_reg", type=float, default=0.01, help="Scale regularization value.")
    parser.add_argument("--opacity_reg", type=float, default=0.01, help="Opacity regularization value.")

    # For default & MCMC strategies
    parser.add_argument("--min_opacity", type=float, default=0.005, help="Minimum opacity.")
    parser.add_argument("--refine_start_iter", type=int, default=100, help="Refinement start iteration.")

    # Only for default
    parser.add_argument("--reset_every", type=int, default=3_000, help="Reset opacities every this steps. [strategy=default]")
    parser.add_argument("--pause_refine_after_reset", type=int, default=0, help="Pause refining GSs until this number of steps after reset. [strategy=default]")
    parser.add_argument("--init_scale", type=float, default=1.0, help="Initial scale.")
    parser.add_argument("--init_opa", type=float, default=0.5, help="Initial opacity.")

    # Set below to true to have optimized rasterization that can make training more efficient
    parser.add_argument("--packed", type=bool, default=False, help="Use packed mode for rasterization.")
    parser.add_argument("--sparse_grad", type=bool, default=False, help="Use sparse gradients for optimization.")
    parser.add_argument("--ckpt", type=str, default=None, help="Ckpt path, only for evaluation purposes.")

    # Parse arguments
    args = parser.parse_args()

    # Use parsed arguments in the script
    data_dir = args.data_dir
    data_factor = args.data_factor
    result_dir = args.result_dir
    init_type = args.init_type
    strategy = args.strategy
    max_steps = args.max_steps
    init_num_pts = args.init_num_pts
    delta_steps = args.delta_steps
    scale_reg = args.scale_reg
    cap_max = args.cap_max
    refine_every = args.refine_every
    reset_every = args.reset_every
    refine_start_iter = args.refine_start_iter
    pause_refine_after_reset = args.pause_refine_after_reset
    refine_stop_iter = int(0.75 * max_steps)
    min_opacity = args.min_opacity
    opacity_reg = args.opacity_reg
    init_scale = args.init_scale
    init_opa = args.init_opa
    sh_degree_interval = args.sh_degree_interval
    sh_degree = args.sh_degree
    packed = args.packed
    sparse_grad = args.sparse_grad
    ckpt = [args.ckpt] if args.ckpt is not None else None

    # Define eval_steps and save_steps based on the values of max_steps and delta_steps
    eval_steps: List[int] = [i for i in range(2_000, max_steps + delta_steps, delta_steps)]
    save_steps: List[int] = [i for i in range(2_000, max_steps + delta_steps, delta_steps)]

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
                scale_reg=scale_reg,
                packed=packed,
                sparse_grad=sparse_grad,
                disable_viewer=True,
                ckpt=ckpt,
                sh_degree=sh_degree,
                sh_degree_interval=sh_degree_interval,
                strategy=DefaultStrategy(verbose=True, refine_start_iter=refine_start_iter,
                                         refine_every=refine_every, refine_stop_iter=refine_stop_iter,
                                         reset_every=reset_every, pause_refine_after_reset=pause_refine_after_reset,
                                         prune_opa=min_opacity),
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
                init_opa=init_opa,
                init_scale=init_scale,
                opacity_reg=opacity_reg,
                scale_reg=scale_reg,
                packed=packed,
                disable_viewer=True,
                ckpt=ckpt,
                sh_degree=sh_degree,
                sparse_grad=sparse_grad,
                sh_degree_interval=sh_degree_interval,
                strategy=MCMCStrategy(verbose=True, cap_max=cap_max, refine_every=refine_every,
                                      refine_start_iter=refine_start_iter, refine_stop_iter=refine_stop_iter,
                                      min_opacity=min_opacity),
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
