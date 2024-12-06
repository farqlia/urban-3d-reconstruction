from pyntcloud import PyntCloud
import argparse
from torch.utils.data import DataLoader
import pytorch_lightning as pl
from urb3d.segmentation.segmentor import PointNetSegmentor
from urb3d.segmentation.dataset import PointCloudSegmentationDataset
import numpy as np

def run(segmentor_ckpt_path, input_ply_path, output_ply_path):
    model = PointNetSegmentor.load_from_checkpoint(segmentor_ckpt_path, strict=False)
    dataset = PointCloudSegmentationDataset(input_ply_path)
    data_loader = DataLoader(dataset)
    trainer = pl.Trainer()

    preds = trainer.predict(model, data_loader)[0][0].numpy()

    save_class_labels_in_ply(dataset.pt, output_ply_path, preds) # sampled point cloud instead of pt


def save_class_labels_in_ply(cloud, output_ply_path, class_labels):
    data = cloud.points
    print(class_labels)
    if len(class_labels) != len(data):
        raise ValueError("Number of class labels must match the number of points in the .ply file.")

    class_labels = np.array(class_labels, dtype=np.int32)
    data.drop('scalar_class', axis=1, inplace=True)
    data['class_label'] = class_labels

    new_cloud = PyntCloud(data)
    new_cloud.points.dropna(subset=['x', 'y', 'z'], inplace=True)
    new_cloud.to_file(output_ply_path)

if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--ckpt", type=str, required=True, help="Path to the checkpoint .ckpt file.")
    parser.add_argument("--input", type=str, required=True, help="Path to the input .ply file.")
    parser.add_argument("--output", type=str, required=True, help="Path to save the modified .ply file after segmentation.")

    args = parser.parse_args()

    run(args.ckpt, args.input, args.output)

    cloud = PyntCloud.from_file(args.output)                             ##
    print(cloud.points)                                                  ##
