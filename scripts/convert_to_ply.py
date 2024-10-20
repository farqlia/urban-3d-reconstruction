import pycolmap
from pathlib import Path

# path to a folder with 'cameras.bin images.bin points3D.bin' files
sparse_model = Path('../data/small_city_road_outside_d4x_recon')

output_path = Path('../data/small_city_road_outside_d4x_recon')

reconstruction = pycolmap.Reconstruction(sparse_model)

reconstruction.export_PLY(output_path / 'sparse-0.ply')

