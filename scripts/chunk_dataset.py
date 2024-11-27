import pandas as pd
import numpy as np
from pyntcloud import PyntCloud


def save_pointcloud_in_chunks(point_cloud_path, chunk_size, output_dir):
    pt = PyntCloud.from_file(point_cloud_path)
    points = pt.points.sample(frac=1, random_state=42).reset_index(drop=True)
    num_chunks = (len(points) + chunk_size - 1) // chunk_size  # Round up

    for i in range(num_chunks):
        chunk = points.iloc[i * chunk_size: (i + 1) * chunk_size]
        chunk.to_csv(f"{output_dir}/chunk_{i}.csv", index=False)
        print(i, '/', num_chunks, flush=True)

save_pointcloud_in_chunks('../data/birmingham_blocks/birmingham_block_6.ply', 65536, '../data/birmingham_blocks/block_6_train')