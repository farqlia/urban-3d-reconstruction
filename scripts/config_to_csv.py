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
    parser = argparse.ArgumentParser(description="Convert model config to csv file.")
    parser.add_argument("--input_dir", type=str, help="Path to model/experiment")

    # args = parser.parse_args("--model_names c7 sks --input_dir ../results --output_file ../results/model_configs.csv".split())
    args = parser.parse_args()

    input_dir = Path(args.input_dir)

    yaml_file = input_dir / 'cfg.yml'
    csv_file = input_dir / 'cfg.csv'

    main(yaml_file, csv_file)