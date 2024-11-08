import pycolmap
from pathlib import Path

# path to a folder with 'cameras.bin images.bin points3D.bin' files
sparse_model = Path('data/360_v2/room/sparse/0')

output_path = Path('data/360_v2/room/sparse')

reconstruction = pycolmap.Reconstruction(sparse_model)

reconstruction.export_PLY(output_path / 'sparse.ply')

