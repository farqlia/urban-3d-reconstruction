from pyntcloud import PyntCloud
import torch
from torch.utils.data import Dataset
import numpy as np

class MockPointSampler:

    def __call__(self, point_cloud):
        return point_cloud

def min_max_standardize(coords):
    x = (coords.loc[:, 'x'] - np.min(coords.loc[:, 'x'])) / (np.max(coords.loc[:, 'x']) - np.min(coords.loc[:, 'x']))
    y = (coords.loc[:, 'y'] - np.min(coords.loc[:, 'y'])) / (np.max(coords.loc[:, 'y']) - np.min(coords.loc[:, 'y']))
    z = (coords.loc[:, 'z'] - np.min(coords.loc[:, 'z'])) / (np.max(coords.loc[:, 'z']) - np.min(coords.loc[:, 'z']))

    return x, y, z


class PointSampler:  # Smarter way to sample point cloud?

    def __init__(self, subsample_size):
        self.subsample_size = subsample_size

    def __call__(self, point_cloud):
        indices = np.random.choice(point_cloud.index.values, size=self.subsample_size, replace=False)
        sampled_points = point_cloud.loc[indices]
        return sampled_points

class PointCloudSegmentationDataset(Dataset):

    def __init__(self, point_cloud_path, subsample_size=None, point_sampler=None, ds_size=None):
        self.point_sampler = point_sampler if point_sampler is not None else PointSampler(1024)
        self.pt: PyntCloud = PyntCloud.from_file(point_cloud_path)
        # self.pt.points['scalar_class'] = -1  ## temp
        self.ds_size = ds_size
        self.subsample_size = subsample_size if subsample_size else len(self.pt.points)
        x, y, z = min_max_standardize(self.pt.points[['x', 'y', 'z']])

        self.pt.points['x_norm'] = x
        self.pt.points['y_norm'] = y
        self.pt.points['z_norm'] = z

        self.label = 'class' if 'class' in self.pt.points.columns else 'scalar_class'

    def get_pointcloud(self) -> PyntCloud:
        return self.pt

    def __len__(self):
        # How to set the number of batches?
        return len(self.pt.points) // self.subsample_size if self.ds_size is None else self.ds_size

    def __getitem__(self, idx):
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        # For now, a point cloud is sampled each time this function is called (it doesn't depend on idx)
        sampled_cloud = self.point_sampler(self.pt.points[['x_norm', 'y_norm', 'z_norm', self.label]])
        sampled_points = torch.tensor(sampled_cloud[['x_norm', 'y_norm', 'z_norm']].values, device=device)
        labels = torch.tensor(sampled_cloud[[self.label]].values, device=device, dtype=torch.long).flatten()
        return sampled_points.T, labels