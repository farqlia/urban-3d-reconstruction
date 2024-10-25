import argparse
import os
import pycolmap
from pathlib import Path

def run_reconstruction(input_images_path, output_path, database_path, camera_model='SIMPLE_PINHOLE'):
    os.makedirs(output_path, exist_ok=True)
    ba_global_images_ratio = 1.1
    ba_global_images_freq = 500
    ba_global_max_refinement_change = 0.0005
    ba_global_max_refinements = 5
    ba_global_points_freq = 250000
    ba_global_points_ratio = 1.1
    ba_local_max_refinement_change = 0.001
    incremental_pipeline_options = pycolmap.IncrementalPipelineOptions(
        ba_global_images_ratio=ba_global_images_ratio,
        ba_global_images_freq=ba_global_images_freq,
        ba_global_max_refinement_change=ba_global_max_refinement_change,
        ba_global_max_refinements=ba_global_max_refinements,
        ba_global_points_ratio=ba_global_points_ratio,
        ba_global_points_freq=ba_global_points_freq,
        ba_local_max_refinement_change=ba_local_max_refinement_change,
    )
    if not os.path.exists(output_path / '0'):
        pycolmap.extract_features(database_path, input_images_path, camera_model=camera_model)
        pycolmap.match_exhaustive(database_path)
        maps = pycolmap.incremental_mapping(database_path, input_images_path, output_path,
                                            options=incremental_pipeline_options)
        maps[0].write(output_path)
        undistorted_path = output_path / 'undistorted_images'
        pycolmap.undistort_images(output_path=str(undistorted_path), 
                                  image_path=str(input_images_path), input_path= output_path / '0')
    return pycolmap.Reconstruction(undistorted_path / 'sparse')


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Run COLMAP reconstruction and save results as .ply.")
    
    parser.add_argument('--input', type=str, required=True, help='Path to the input folder of images.')
    parser.add_argument('--output', type=str, required=True, help='Path to the output directory.')
    #parser.add_argument('--cam_model', type=str, required=False, default='SIMPLE_PINHOLE', help='Camera model (default is SIMPLE_PINHOLE).')

    args = parser.parse_args()

    input_images_path = Path(args.input)
    output_path = Path(args.output)
    database_path = Path(args.output + '/database.db')

    reconstruction = run_reconstruction(input_images_path, output_path, database_path)
    reconstruction.export_PLY(output_path / 'sparse.ply')