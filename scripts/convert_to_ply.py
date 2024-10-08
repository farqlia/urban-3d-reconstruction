import pycolmap
from pathlib import Path

# path to a folder with 'cameras.bin images.bin points3D.bin' files
sparse_model = Path('../data/south-building/0')

output_path = Path('../data/south-building')

reconstruction = pycolmap.Reconstruction(sparse_model)

reconstruction.export_PLY(output_path / 'sparse-2.ply')

