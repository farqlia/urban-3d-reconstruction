from pyntcloud import PyntCloud
import numpy as np
import argparse

def save_class_labels_in_ply(input_ply_path, output_ply_path, class_labels):
    cloud = PyntCloud.from_file(input_ply_path)
    data = cloud.points
    
    if len(class_labels) != len(data):
        raise ValueError("Number of class labels must match the number of points in the .ply file.")

    data['class_label'] = class_labels

    new_cloud = PyntCloud(data)
    new_cloud.to_file(output_ply_path)

if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, help="Path to the input .ply file.")
    parser.add_argument("--output", type=str, help="Path to save the modified .ply file after segmentation.")

    args = parser.parse_args()

    input = args.input                                              ## 
    cloud = PyntCloud.from_file(input)                              ##
    print(cloud.points)                                             ##
    output = args.output                                            ##
    class_labels = np.random.randint(1, 6, size=len(cloud.points))  ## 

    save_class_labels_in_ply(input, output, class_labels)

    cloud = PyntCloud.from_file(output)                             ##
    print(cloud.points)                                             ##