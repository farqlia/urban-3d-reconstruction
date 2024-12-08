import argparse
import os
import pandas as pd
import numpy as np
from pyntcloud import PyntCloud

from urb3d.segmentation.dataset import SAMPLE_SIZE


def save_pointcloud_in_chunks_multiple_files(input_files, chunk_size, output_dir):
    last_chunk = 0
    os.makedirs(output_dir, exist_ok=True)
    # Load points from each file
    for idx, file_path in enumerate(input_files):
        print(f"Loading: {file_path} ({idx+1}/{len(input_files)}) ", end='')
        pt = PyntCloud.from_file(file_path)
        points = pt.points

        print(f"Points: {len(points)}")

        # Shuffle points
        points = points.sample(frac=1, random_state=42).reset_index(drop=True)

        # Calculate number of chunks
        num_chunks = (len(points) + chunk_size - 1) // chunk_size  # Round up

        # Save points in chunks
        for i in range(num_chunks):
            chunk = points.iloc[i * chunk_size: (i + 1) * chunk_size]
            chunk.to_csv(f"{output_dir}/chunk_{last_chunk+i}.csv", index=False)
            print(f"Saved chunk {i + 1}/{num_chunks}")
        last_chunk = num_chunks


input_files = [
    '../data/segmentation_data/cambridge_block_4.ply',
]


if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True, help="Path to the input .ply file")
    parser.add_argument("--output", type=str, required=True, help="Path to save the chunked .ply files.")

    args = parser.parse_args()

    save_pointcloud_in_chunks_multiple_files([args.input], SAMPLE_SIZE, args.output)