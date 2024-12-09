import argparse
import os
import pycolmap
from pathlib import Path


def run_reconstruction(input_images_path, output_path, database_path, camera_model='SIMPLE_PINHOLE'):
    os.makedirs(output_path, exist_ok=True)

    ba_global_function_tolerance= 0.0   # 0.0
    ba_local_function_tolerance= 0.0    # 0.0

    ba_global_images_ratio = 2.2   # 1.1
    ba_global_images_freq = 1000   # 500

    ba_global_max_refinement_change = 0.02  # 0.0005
    ba_global_max_refinements = 3  # 5

    ba_global_points_freq = 500000      # 250000
    ba_global_points_ratio = 2.2        # 1.1

    ba_local_max_refinement_change = 0.01  # 0.001
    ba_local_max_refinements=2      # 2

    incremental_pipeline_options = pycolmap.IncrementalPipelineOptions(
        ba_global_images_ratio=ba_global_images_ratio,
        ba_global_images_freq=ba_global_images_freq,
        ba_global_function_tolerance=ba_global_function_tolerance,
        ba_local_function_tolerance=ba_local_function_tolerance,
        ba_global_max_refinement_change=ba_global_max_refinement_change,
        ba_global_max_refinements=ba_global_max_refinements,
        ba_global_points_ratio=ba_global_points_ratio,
        ba_global_points_freq=ba_global_points_freq,
        ba_local_max_refinement_change=ba_local_max_refinement_change,
        ba_local_max_refinements=ba_local_max_refinements
    )

    if not os.path.exists(database_path):
        pycolmap.extract_features(database_path, input_images_path, camera_model=camera_model)
        
    pycolmap.match_exhaustive(database_path)

    maps = pycolmap.incremental_mapping(database_path, input_images_path, output_path,
                                            options=incremental_pipeline_options)

    maps[0].write(output_path)

    reconstruction = pycolmap.Reconstruction(output_path)
    return reconstruction

def export_reconstructions_to_ply(reconstructions):
    for i, reconstruction in enumerate(reconstructions):
            ply_output_path = output_path / f'sparse_model_{i}.ply'
            reconstruction.export_PLY(ply_output_path)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Run COLMAP reconstruction and save results as .ply.")
    
    parser.add_argument('--input', type=str, required=True, help='Path to the input folder of images.')
    parser.add_argument('--output', type=str, required=True, help='Path to the output directory.')
    parser.add_argument('--database_path', type=str, required=False, help='Path to the colmap database (optional).')
    #parser.add_argument('--cam_model', type=str, required=False, default='SIMPLE_PINHOLE', help='Camera model (default is SIMPLE_PINHOLE).')

    args = parser.parse_args()

    input_images_path = Path(args.input)
    output_path = Path(args.output)
    database_path = Path(args.database_path) if args.database_path else output_path / 'database.db'

    if not os.path.exists(output_path):
        reconstruction = run_reconstruction(input_images_path, output_path, database_path)
        #export_reconstructions_to_ply(reconstructions)
        reconstruction.export_PLY(output_path / 'sparse.ply')