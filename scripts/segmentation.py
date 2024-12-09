import os

import pandas as pd
import torch
from pyntcloud import PyntCloud
import argparse
from torch.utils.data import DataLoader
import pytorch_lightning as pl
from urb3d.segmentation.segmentor import PointNetSegmentor
from urb3d.segmentation.dataset import PointCloudSegmentationDataset, ChunkedPointCloudDataset, SAMPLE_SIZE
import numpy as np
import warnings

warnings.filterwarnings('ignore')


def run(segmentor_ckpt_path, input_ply_path, output_ply_path):
    model = PointNetSegmentor.load_from_checkpoint(segmentor_ckpt_path, strict=False)
    dataset = PointCloudSegmentationDataset(input_ply_path)
    data_loader = DataLoader(dataset)
    trainer = pl.Trainer()

    preds = trainer.predict(model, data_loader)[0][0].numpy()

    save_class_labels_in_ply(dataset.pt, output_ply_path, preds)  # sampled point cloud instead of pt


def run_chunked(segmentor_ckpt_path, input_chunks_dir, output_ply_path):
    model = PointNetSegmentor.load_from_checkpoint(segmentor_ckpt_path, strict=False)
    dataset = ChunkedPointCloudDataset(input_chunks_dir)
    data_loader = DataLoader(dataset)
    trainer = pl.Trainer()

    preds = trainer.predict(model, data_loader)
    merge_chunked_with_labels_in_ply(preds, input_chunks_dir, output_ply_path)  # sampled point cloud instead of pt


def merge_chunked_with_labels_in_ply(preds, input_chunks_dir, output_ply_path):
    merged_cloud = None
    predictions = np.array([])

    for idx in range(len(os.listdir(input_chunks_dir))):
        chunk_preds = preds[idx][0].cpu().numpy()
        predictions = np.concatenate([predictions, chunk_preds])
        chunk_cloud = PyntCloud.from_file(f"{input_chunks_dir}/chunk_{idx}.csv").points[
            ['x', 'y', 'z']]  # chunk[0][0].cpu().numpy().transpose()
        merged_cloud = chunk_cloud if merged_cloud is None else np.concatenate([merged_cloud, chunk_cloud])

    # combine cloud and predictions
    new_cloud = pd.DataFrame(np.concatenate([merged_cloud, predictions[..., np.newaxis]], axis=1),
                             columns=['x', 'y', 'z', 'class'])
    cloud = PyntCloud(new_cloud)
    # save new point cloud
    cloud.to_file(output_ply_path)


def save_class_labels_in_ply(cloud, output_ply_path, class_labels):
    data = cloud.points
    print(class_labels)
    if len(class_labels) != len(data):
        raise ValueError("Number of class labels must match the number of points in the .ply file.")

    class_labels = np.array(class_labels, dtype=np.int32)
    data['class'] = class_labels
    # new_cloud = PyntCloud.from_file(args.input)
    new_cloud = PyntCloud(data)
    # print(type(new_cloud))
    # print(new_cloud)
    # print(new_cloud.points[:3])
    # print(new_cloud.points.dtypes)
    new_cloud.to_file(output_ply_path)
    from_file_cloud = PyntCloud.from_file(args.output)
    # print(from_file_cloud.points[:3])
    # print(from_file_cloud.points.dtypes)
    # print(type(from_file_cloud))
    # print(from_file_cloud)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--ckpt", type=str, required=True, help="Path to the checkpoint .ckpt file.")
    parser.add_argument("--input", type=str, required=True, help="Path to the input .ply file or chunked directory")
    parser.add_argument("--chunked", type=bool, default=False, help="Whether the provided cloud is chunked")
    parser.add_argument("--output", type=str, required=True,
                        help="Path to save the modified .ply file after segmentation.")

    args = parser.parse_args()

    if args.chunked:
        run_chunked(args.ckpt, args.input, args.output)
    else:
        run(args.ckpt, args.input, args.output)
