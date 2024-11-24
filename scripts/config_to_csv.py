import argparse
from pathlib import Path

from urb3d.models.config_conversion import (parse_yaml_text, save_to_csv,
                                          collect_cfgs, merge_csv_files)

def main(yaml_file, csv_file):
    # Parse the YAML-like file
    data = parse_yaml_text(yaml_file)

    # Save extracted fields to CSV
    save_to_csv(data, csv_file)
    print(f"Data saved to {csv_file}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge model configs.")
    parser.add_argument("--model_names", type=str, nargs="+", help="space separated model names")
    parser.add_argument("--input_dir", type=str, help="path to results directory")
    parser.add_argument("--output_file", type=str, help="output csv file")

    # args = parser.parse_args("--model_names c7 sks --input_dir ../results --output_file ../results/model_configs.csv".split())
    args = parser.parse_args()

    models = args.model_names
    input_dir = args.input_dir
    output_file = args.output_file

    config_yml_files = collect_cfgs(models, Path(input_dir))
    config_csv_files = []
    for config_file in config_yml_files:
        csv_file = save_to_csv(parse_yaml_text(config_file), f"{str(config_file)[:-3]}csv")
        print(f"Save config to {csv_file}")
        config_csv_files.append(csv_file)

    merge_csv_files(config_csv_files, output_file)