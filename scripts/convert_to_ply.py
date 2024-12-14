import argparse

import pycolmap

if __name__ == '__main__':

    # Usage examples:
    # python scripts\neighbor-based_pcd_filtering.py --input "path_to_file.ply" --method statistical --nb_neighbors 50 --std_ratio 0.5
    # python scripts\neighbor-based_pcd_filtering.py --input "path_to_file.ply" --method radius --output "filtered_pcd.ply"

    parser = argparse.ArgumentParser(description="Convert reconstruction to .ply file")

    parser.add_argument('--point_cloud', type=str, required=True, help='Path to the point cloud file')
    parser.add_argument('--reconstruction_dir', type=str, required=True, help='Path to the reconstruction directory')

    args = parser.parse_args()

    reconstruction = pycolmap.Reconstruction(args.reconstruction_dir)
    reconstruction.export_PLY(args.point_cloud)