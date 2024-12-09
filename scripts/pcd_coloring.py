from pyntcloud import PyntCloud
import numpy as np
import argparse
import open3d as o3d

COLOR_MAP = {
    0: (150, 75, 0),       # ground, brown
    1: (34, 139, 34),      # vegetation, dark green
    2: (169, 169, 169),    # building, gray
    3: (61, 61, 61),       # wall, dark gray
    4: (0, 255, 255),      # bridge, cyan
    5: (255, 255, 0),      # parking, yellow
    6: (128, 0, 128),      # rail, purple
    7: (25, 255, 0),       # traffic road, green
    8: (255, 20, 147),     # street furniture, pink
    9: (255, 0, 0),        # car, red
    10: (255, 130, 0),     # footpath, orange
    11: (22, 0, 130),      # bike, navy
    12: (0, 166, 255)      # water, blue
}

def set_color_based_on_class_labels(input_ply_path, output_ply_path, color_map):
    cloud = PyntCloud.from_file(input_ply_path)
    data = cloud.points

    colors = np.array([color_map.get(label, [0, 0, 0]) for label in data['class']])
    # print(data['class'])
    data['red'], data['green'], data['blue'] = colors.T

    colors = colors / 255.0  
    pcd = o3d.io.read_point_cloud(input_ply_path)
    pcd.colors = o3d.utility.Vector3dVector(colors)

    o3d.io.write_point_cloud(output_ply_path, pcd)
    
    o3d_cloud = o3d.io.read_point_cloud(output_ply_path)
    o3d.visualization.draw_geometries([o3d_cloud])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Changes colors of points in a .ply file based on class labels.")
    parser.add_argument("--input", type=str, required=True, help="Path to the input .ply file with class labels.")
    parser.add_argument("--output", type=str, required=True, help="Path to save the modified .ply file with colors.")
    args = parser.parse_args()

    # set_color_based_on_class_labels(args.input, args.output, COLOR_MAP)


