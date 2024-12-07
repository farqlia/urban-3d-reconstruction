import numpy as np
import open3d as o3d
import argparse
from pycolmap import Reconstruction

def get_outliers_and_inliers_pcds(pcd, inlier_indices):

    outlier_indices = list(set(range(len(pcd.points))) - set(inlier_indices))
 
    inliers = pcd.select_by_index(inlier_indices)
    outliers = pcd.select_by_index(outlier_indices)

    np.asarray(outliers.colors)[:] = [1, 0, 1]  #set outliers' color to magenta 
    
    return inliers, outliers

def filter_reconstruction(reconstruction, pcd):

    pcd_points = set(map(tuple, np.asarray(pcd.points)))
    points = reconstruction.points3D

    for idx, point in points.items():
        point_coords = np.array(point.xyz)

        if not (any(np.allclose(point_coords, pcd_point) for pcd_point in pcd_points)):
            reconstruction.delete_point3D(idx)

if __name__ == '__main__':

    # Usage examples:
    # python scripts\neighbor-based_pcd_filtering.py --input "path_to_file.ply" --method statistical --nb_neighbors 50 --std_ratio 0.5
    # python scripts\neighbor-based_pcd_filtering.py --input "path_to_file.ply" --method radius --output "filtered_pcd.ply"

    parser = argparse.ArgumentParser(description="Remove outliers from point cloud and visualize the results.")

    parser.add_argument('--point_cloud', type=str, required=True, help='Path to the point cloud file')
    parser.add_argument('--reconstruction_dir', type=str, required=True, help='Path to the reconstruction directory')
    parser.add_argument('--method', type=str, required=True, choices=['statistical', 'radius'],
                        help="Choose the outlier removal method: 'statistical' or 'radius'.")
    parser.add_argument('--nb_neighbors', type=int, default=20, help="Number of neighbors (for statistical method).")
    parser.add_argument('--std_ratio', type=float, default=1.0, help="Standard deviation ratio (for statistical method).")
    parser.add_argument('--nb_points', type=int, default=2, help="Minimum number of points (for radius method).")
    parser.add_argument('--radius', type=float, default=0.2, help="Radius (for radius method).")

    args = parser.parse_args()

    reconstruction = Reconstruction(args.reconstruction_dir)
    pcd = o3d.io.read_point_cloud(args.point_cloud)

    if args.method == 'statistical':
        _, inlier_indices = pcd.remove_statistical_outlier(nb_neighbors=args.nb_neighbors, std_ratio=args.std_ratio)
    elif args.method == 'radius':
        _, inlier_indices = pcd.remove_radius_outlier(nb_points=args.nb_points, radius=args.radius)

    inliers, outliers = get_outliers_and_inliers_pcds(pcd, inlier_indices)
    #o3d.visualization.draw_geometries([inliers, outliers])

    filter_reconstruction(reconstruction, inliers)
    reconstruction.write(args.reconstruction_dir)
    reconstruction.export_PLY(args.point_cloud)

    #pcd = o3d.io.read_point_cloud(args.point_cloud)
    #o3d.visualization.draw_geometries([pcd])