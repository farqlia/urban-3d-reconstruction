import argparse
import os
import pycolmap
from pathlib import Path

def run_reconstruction(input_images_path, output_path, database_path, camera_model='SIMPLE_PINHOLE'):
    os.makedirs(output_path, exist_ok=True)
    if not os.path.exists(output_path / '0'):
        pycolmap.extract_features(database_path, input_images_path, camera_model=camera_model)
        pycolmap.match_exhaustive(database_path)
        maps = pycolmap.incremental_mapping(database_path, input_images_path, output_path)
        maps[0].write(output_path)
        pycolmap.undistort_images(output_path=str(output_path / 'undistorted_images'), 
                                  image_path=str(input_images_path), input_path= output_path / '0')
    return pycolmap.Reconstruction(output_path)


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