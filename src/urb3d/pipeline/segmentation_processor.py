from .config import (SEGMENTED_PLY_PATH, COLORED_SEGMENTED_PLY_PATH, SEGMENTATION_MODEL_CKPT_PATH, GAUSSIAN_MODEL_PLY,
                     FILTERED_PRESEG_MODEL, CHUNKED_MODEL_FOLDER)
from .utils import run_script
import os
import open3d as o3d

class SegmentationProcessor:

    def __init__(self):
        self.input_gaussian_model_path = GAUSSIAN_MODEL_PLY
        self.segmented_ply_path = SEGMENTED_PLY_PATH
        self.colored_ply_path = COLORED_SEGMENTED_PLY_PATH
        self.filtered_model_path = FILTERED_PRESEG_MODEL
        self.segmentation_model_path = SEGMENTATION_MODEL_CKPT_PATH
        self.chunked_model_folder = CHUNKED_MODEL_FOLDER

    def run_segmentation(self):
        if not os.path.exists(self.filtered_model_path):
            run_script("statistical_pcd_filtering.py","--input",
                   str(self.input_gaussian_model_path), "--method", "iqr", "--alpha", str(2),
                   "--output", str(self.filtered_model_path))

        if not self.chunked_model_folder.exists():
            run_script("chunk_dataset.py", "--input", str(self.filtered_model_path),
                   "--output", str(self.chunked_model_folder))

        if not os.path.exists(self.segmented_ply_path):
            run_script("segmentation.py", "--ckpt", str(self.segmentation_model_path),
                       "--input", str(self.chunked_model_folder), "--output", str(self.segmented_ply_path),
                       "--chunked", str(True))

        if not os.path.exists(self.colored_ply_path):
            print("Run coloring....")
            run_script("pcd_coloring.py", "--input", str(self.segmented_ply_path),
                       "--output", str(self.colored_ply_path))


#sp = SegmentationProcessor()
#sp.run_segmentation()

#cloud = o3d.io.read_point_cloud(str(sp.colored_ply_path))
#o3d.visualization.draw_geometries([cloud])