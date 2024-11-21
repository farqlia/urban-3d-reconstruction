import open3d as o3d
from pyntcloud import PyntCloud
import numpy as np
import argparse

# based on https://santoshraviteja.medium.com/how-to-remove-outliers-using-python-ea52877f5a78
# adapted for 3D point cloud data

def filter_outliers_iqr(df, alpha):
    inliers = df.copy()
    outliers = df.copy()
    conditions_inliers = []
    conditions_outliers = []

    for col in ['x', 'y', 'z']:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - alpha * IQR
        upper_bound = Q3 + alpha * IQR

        conditions_inliers.append((inliers[col] >= lower_bound) & (inliers[col] <= upper_bound))
        conditions_outliers.append((outliers[col] < lower_bound) | (outliers[col] > upper_bound))

    inliers = inliers[np.logical_and.reduce(conditions_inliers)]
    outliers = outliers[np.logical_or.reduce(conditions_outliers)]

    return inliers, outliers

def filter_outliers_zscore(df, threshold):
    inliers = df.copy()
    outliers = df.copy()
    conditions_inliers = []
    conditions_outliers = []

    for col in ['x', 'y', 'z']:
        mean = df[col].mean()
        std = df[col].std()
        z_scores = (df[col] - mean) / std

        conditions_inliers.append(np.abs(z_scores) < threshold)
        conditions_outliers.append(np.abs(z_scores) >= threshold)

    inliers = inliers[np.logical_and.reduce(conditions_inliers)]
    outliers = outliers[np.logical_or.reduce(conditions_outliers)]

    return inliers, outliers

def load_and_filter_cloud(file_path, output_path, method, alpha, threshold, outliers_path=None):
    cloud = PyntCloud.from_file(file_path)
    points = cloud.points

    if method=="iqr":
        inliers, outliers = filter_outliers_iqr(points, alpha)
    else:
        inliers, outliers = filter_outliers_zscore(points, threshold)

    cloud.points = inliers
    cloud.to_file(output_path, as_text=True)

    if outliers_path is not None:
        cloud.points = outliers
        cloud.to_file(outliers_path, as_text=True)

if __name__=="__main__":
    # usage:
    # python scripts\statistical_pcd_filtering.py --input "path_to_file.ply" --method iqr --output "filtered_output.ply"
    # python scripts\statistical_pcd_filtering.py --input "path_to_file.ply" --method z-score --output "filtered_output.ply" --threshold 2
    # higher alpha and higher threshold = more inliers

    parser = argparse.ArgumentParser(description="Remove outliers from point cloud.")

    parser.add_argument('--input', type=str, required=True, help='Path to the point cloud file')
    parser.add_argument('--method', type=str, required=True, choices=['iqr', 'z-score'],
                        help="Choose the outlier removal method: 'iqr' or 'z-score'.")
    parser.add_argument('--alpha', type=float, default=3,
                        help='IQR method: the multiplier for the IQR range (default: 3).')
    parser.add_argument('--threshold', type=float, default=1.5,
                        help='Z-score method: the threshold for filtering (default: 1.5).')
    parser.add_argument('--output', type=str, required=True,
                        help='Path to save the point cloud without outliers.')

    args = parser.parse_args()

    load_and_filter_cloud(args.input, args.output, args.method, args.alpha, args.threshold)

    #inliers = o3d.io.read_point_cloud(args.output)
    #o3d.visualization.draw_geometries([inliers])

    #outliers = o3d.io.read_point_cloud(outliers_path)
    #o3d.visualization.draw_geometries([outliers])