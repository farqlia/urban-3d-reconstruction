import numpy as np
from pyntcloud import PyntCloud
import open3d as o3d
import argparse

def filter_by_distance(cloud, max_distance):
    center = cloud.points[['x', 'y', 'z']].mean()
    distances = np.sqrt((cloud.points['x'] - center['x']) ** 2 +
                        (cloud.points['y'] - center['y']) ** 2 +
                        (cloud.points['z'] - center['z']) ** 2)

    inliers = cloud.points[distances <= max_distance]
    outliers = cloud.points[distances > max_distance]

    return inliers, outliers

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Filter point cloud by distance from center.")
    parser.add_argument('--input', type=str, required=True, help='Path to the input .ply point cloud file')
    parser.add_argument('--output', type=str, required=True,
                        help='Path to save the filtered .ply point cloud file')
    parser.add_argument('--max_distance', type=float, default=3.0,
                        help='Maximum distance from center to keep points (default: 3.0)')

    args = parser.parse_args()

    cloud = PyntCloud.from_file(args.input)
    inliers, outliers = filter_by_distance(cloud, args.max_distance)

    cloud.points = inliers
    cloud.to_file(args.output)

    #inliers = o3d.io.read_point_cloud(args.output)
    #o3d.visualization.draw_geometries([inliers])