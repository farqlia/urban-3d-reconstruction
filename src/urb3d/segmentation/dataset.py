import os

import pandas as pd
from pyntcloud import PyntCloud
import torch
from torch.utils.data import Dataset
import numpy as np

SAMPLE_SIZE = 20_000

class MockPointSampler:

    def __call__(self, point_cloud):
        return point_cloud

def min_max_standardize(coords):
    x = (coords.loc[:, 'x'] - np.min(coords.loc[:, 'x'])) / (np.max(coords.loc[:, 'x']) - np.min(coords.loc[:, 'x']))
    y = (coords.loc[:, 'y'] - np.min(coords.loc[:, 'y'])) / (np.max(coords.loc[:, 'y']) - np.min(coords.loc[:, 'y']))
    z = (coords.loc[:, 'z'] - np.min(coords.loc[:, 'z'])) / (np.max(coords.loc[:, 'z']) - np.min(coords.loc[:, 'z']))

    return x, y, z


class PointSampler:
    def __init__(self, subsample_size):
        self.subsample_size = subsample_size

    def __call__(self, point_cloud):
        # Work directly on tensors for efficiency
        total_points = point_cloud.shape[0]
        indices = torch.randperm(total_points)[:self.subsample_size]
        return point_cloud[indices]


class PointCloudSegmentationDataset(Dataset):

    def __init__(self, point_cloud_path, subsample_size=None, point_sampler=None, ds_size=None):
        self.point_sampler = point_sampler if point_sampler else MockPointSampler()
        self.pt: PyntCloud = PyntCloud.from_file(point_cloud_path)
        # self.pt.points['scalar_class'] = -1  ## temp
        self.ds_size = ds_size
        self.subsample_size = subsample_size if subsample_size else len(self.pt.points)
        x, y, z = min_max_standardize(self.pt.points[['x', 'y', 'z']])

        self.pt.points['x_norm'] = x
        self.pt.points['y_norm'] = y
        self.pt.points['z_norm'] = z

    def get_pointcloud(self) -> PyntCloud:
        return self.pt
    
    def __len__(self):
        # How to set the number of batches?
        return len(self.pt.points) // self.subsample_size if self.ds_size is None else self.ds_size

    def __getitem__(self, idx):
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        # For now, a point cloud is sampled each time this function is called (it doesn't depend on idx)
        sampled_cloud = self.point_sampler(self.pt.points[['x_norm', 'y_norm', 'z_norm']])
        sampled_points = torch.tensor(sampled_cloud[['x_norm', 'y_norm', 'z_norm']].values, device=device)
        labels = torch.tensor(sampled_cloud[['class']].values, device=device, dtype=torch.long).flatten() \
            if 'class' in sampled_cloud.columns \
            else torch.zeros(self.subsample_size, dtype=torch.long, device=device)
        return sampled_points.T, labels


class ChunkedPointCloudDataset(Dataset):
    def __init__(self, chunk_dir, subsample_size=None, point_sampler=None):
        self.chunk_dir = chunk_dir
        self.chunk_files = sorted([os.path.join(chunk_dir, f) for f in os.listdir(chunk_dir) if f.endswith('.csv')])
        self.subsample_size = subsample_size or 1024
        self.point_sampler = point_sampler or PointSampler(subsample_size)

    def __len__(self):
        return len(self.chunk_files)

    def __getitem__(self, idx):
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        # Load the specific chunk
        chunk = pd.read_csv(self.chunk_files[idx])

        # Normalize and convert to tensor
        x, y, z = min_max_standardize(chunk[['x', 'y', 'z']])
        points = torch.tensor(np.column_stack([x, y, z]), dtype=torch.float32)

        # Handle labels (during inference we have no labels)
        labels = torch.tensor(chunk['class'].values, dtype=torch.long) if 'class' in chunk.columns\
            else torch.zeros(len(chunk), dtype=torch.long)

        # Combine points and labels
        point_cloud_with_labels = torch.cat([points, labels.unsqueeze(-1)], dim=-1).to(device)

        # Sample the data
        sampled_cloud = self.point_sampler(point_cloud_with_labels)
        sampled_points = sampled_cloud[:, :3]  # Extract coordinates
        labels = sampled_cloud[:, 3].long()  # Extract labels

        return sampled_points.T, labels
