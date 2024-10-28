import csv
import os
import re
import sys
from pathlib import Path
from typing import List

import pandas as pd


def parse_yaml_text(yaml_file):
    # Define regex patterns for each field to match
    field_patterns = {
        "app_opt_lr": r"^app_opt_lr:\s*(.+)$",
        "app_opt_reg": r"^app_opt_reg:\s*(.+)$",
        "data_dir": r"^data_dir:\s*(.+)$",
        "data_factor": r"^data_factor:\s*(.+)$",
        "far_plane": r"^far_plane:\s*(.+)$",
        "global_scale": r"^global_scale:\s*(.+)$",
        "init_extent": r"^init_extent:\s*(.+)$",
        "init_num_pts": r"^init_num_pts:\s*(.+)$",
        "init_opa": r"^init_opa:\s*(.+)$",
        "init_scale": r"^init_scale:\s*(.+)$",
        "init_type": r"^init_type:\s*(.+)$",
        "max_steps": r"^max_steps:\s*(.+)$",
        "near_plane": r"^near_plane:\s*(.+)$",
        "opacity_reg": r"^opacity_reg:\s*(.+)$",
        "result_dir": r"^result_dir:\s*(.+)$",
        "scale_reg": r"^scale_reg:\s*(.+)$",
        "sh_degree": r"^sh_degree:\s*(.+)$",
        "sh_degree_interval": r"^sh_degree_interval:\s*(.+)$"
    }

    strategy_patterns = {
        "default": {
            "refine_every": r"^\s*refine_every:\s*(.+)$",
            "refine_start_iter": r"^\s*refine_start_iter:\s*(.+)$",
            "refine_stop_iter": r"^\s*refine_stop_iter:\s*(.+)$",
            "reset_every": r"^\s*reset_every:\s*(.+)$"
        },
        "mcmc": {
            "cap_max": r"^\s*cap_max:\s*(.+)$",
            "min_opacity": r"^\s*min_opacity:\s*(.+)$",
            "refine_every": r"^\s*refine_every:\s*(.+)$",
            "refine_start_iter": r"^\s*refine_start_iter:\s*(.+)$",
            "refine_stop_iter": r"^\s*refine_stop_iter:\s*(.+)$"
        }
    }

    extracted_data = {}
    current_strategy = None

    with open(yaml_file, "r") as file:
        for line in file:
            # Check for each field pattern
            for key, pattern in field_patterns.items():
                match = re.match(pattern, line)
                if match:
                    extracted_data[key] = match.group(1).strip()
                    break

            # Check if we encounter a strategy definition
            if re.match(r"^strategy:", line):
                # Capture strategy type (either DefaultStrategy or MCMCStrategy)
                strategy_type_match = re.search(r"!!python/object:gsplat.strategy\.(\w+)", line)
                if strategy_type_match:
                    current_strategy = strategy_type_match.group(1)
                    extracted_data["strategy"] = current_strategy
                continue

            # If a strategy is defined, capture its attributes based on the type
            if current_strategy and current_strategy in strategy_patterns:
                for key, pattern in strategy_patterns[current_strategy].items():
                    match = re.match(pattern, line)
                    if match:
                        extracted_data[key] = match.group(1).strip()
                        break

    return extracted_data


def save_to_csv(data, csv_file):
    # Write to CSV file
    with open(csv_file, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        writer.writeheader()
        writer.writerow(data)
    return csv_file


def collect_cfgs(models_names: List, root_dir: Path):
    experiment_cfgs = []
    for model in models_names:
        model_path = root_dir / model
        for experiment_name in os.listdir(model_path):
            experiment_cfg_path = model_path / f"{experiment_name}/cfg.yml"
            experiment_cfgs.append(experiment_cfg_path)

    return experiment_cfgs


def merge_csv_files(files, output_file):
    dataframes = [pd.read_csv(file) for file in files]
    merged_df = pd.concat(dataframes, ignore_index=True)

    merged_df.to_csv(output_file, index=False)