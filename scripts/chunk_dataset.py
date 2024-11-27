import os
import pandas as pd
import numpy as np
from pyntcloud import PyntCloud


def save_pointcloud_in_chunks_multiple_files(input_files, chunk_size, output_dir):
    last_chunk = 0
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
    '../data/birmingham_blocks/birmingham_block_9.ply',
]
save_pointcloud_in_chunks_multiple_files(input_files, 131_072, '../data/birmingham_blocks/val')
