import argparse
import open3d as o3d
from pyntcloud import PyntCloud

if __name__=="__main__":
    # usage:
    # python scripts\statistical_pcd_filtering.py --input "path_to_file.ply" --method iqr --output "filtered_output.ply"
    # python scripts\statistical_pcd_filtering.py --input "path_to_file.ply" --method z-score --output "filtered_output.ply" --threshold 2
    # higher alpha and higher threshold = more inliers

    parser = argparse.ArgumentParser(description="Visualize pointcloud.")

    parser.add_argument('--input', type=str, required=True, help='Path to the point cloud file')

    args = parser.parse_args()

    # ptcl = PyntCloud.from_file(args.input)

    # ptcl.points['z'] = ptcl.points['z'] * (-1)
    # ptcl.to_file('../tmp_pt.ply')

    inliers = o3d.io.read_point_cloud(args.input)
    print(inliers)
    # inliers['z'] =
    o3d.visualization.draw_geometries([inliers])