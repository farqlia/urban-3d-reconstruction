import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import pytorch_lightning as pl
import torch
from lightning.pytorch.loggers import TensorBoardLogger
from pyntcloud import PyntCloud
from torch.utils.data import DataLoader
from torch.utils.data import Dataset

from urb3d.segmentation.dataset import PointSampler, PointCloudSegmentationDataset, ChunkedPointCloudDataset
from urb3d.segmentation.segmentor import PointNetSegmentor
from urb3d.segmentation.pointnet2 import PointNetPP
from pathlib import Path

experiment_name = "pointnet_weighted_32_256"

subsample_size = 16384
batch_size = 16
max_epochs = 500
train_set_path = Path('data/birmingham_blocks/train')
val_set_path = Path('data/birmingham_blocks/val')
file_cloud_path = Path('data/birmingham_blocks/birmingham_block_6.ply')
weight_files = [
    'data/birmingham_blocks/birmingham_block_6.ply',
    'data/birmingham_blocks/birmingham_block_7.ply',
    'data/birmingham_blocks/cambridge_block_10.ply'
]

def get_weights(input_files):
    all_points = []

    # Load points from each file
    for file_path in input_files:
        print(f"Processing: {file_path}")
        pt = PyntCloud.from_file(file_path)
        all_points.append(pt.points)

    # Concatenate all points into a single DataFrame
    combined_points = pd.concat(all_points, ignore_index=True)

    # Count occurrences of each class
    classes_count = (
        pd.DataFrame(combined_points['class'])
        .value_counts()
        .reset_index()
        .rename(columns={0: 'count'})
        .set_index('class')
    )

    # Class names and mapping
    classes_df = pd.DataFrame.from_dict({
        'class': np.arange(13),
        'name': ['ground', 'vegetation', 'building', 'wall', 'bridge',
                 'parking', 'rail', 'traffic road', 'street furniture',
                 'car', 'footpath', 'bike', 'water']
    }).set_index('class')

    # Join class counts with class names
    counts = classes_df.join(classes_count).fillna(0)

    counts['weight'] = (1 / counts['count']).replace([np.inf, -np.inf], 1e-6)

    return torch.Tensor(counts['weight']), len(classes_df)


weights, classes_num = get_weights(weight_files)


training_dataset = ChunkedPointCloudDataset(train_set_path, subsample_size=subsample_size)

train_loader = DataLoader(training_dataset, batch_size=batch_size, shuffle=True)

validation_dataset = ChunkedPointCloudDataset(val_set_path, subsample_size=subsample_size)
val_loader = DataLoader(validation_dataset, batch_size=batch_size)

model = PointNetSegmentor(classes=classes_num, weights=weights)
checkpoint_dir = Path(f"models/{experiment_name}")
logger = TensorBoardLogger(save_dir=f"models/{experiment_name}/tlogs", name=experiment_name)


checkpoint_callback = pl.callbacks.ModelCheckpoint(dirpath=checkpoint_dir / 'best_results', filename='{epoch}-{val_loss:.2f}-{train_loss:.2f}',
                                      monitor='val_loss', save_last=True)
early_stopping = pl.callbacks.EarlyStopping(monitor='val_loss', verbose=True, patience=15)


if __name__=="__main__":
    # usage:
    # python scripts\statistical_pcd_filtering.py --input "path_to_file.ply" --method iqr --output "filtered_output.ply"
    # python scripts\statistical_pcd_filtering.py --input "path_to_file.ply" --method z-score --output "filtered_output.ply" --threshold 2
    # higher alpha and higher threshold = more inliers

    trainer = pl.Trainer(max_epochs=max_epochs, fast_dev_run=False,
                         default_root_dir=checkpoint_dir, callbacks=[checkpoint_callback, early_stopping], logger=logger,
                         log_every_n_steps=1)

    trainer.fit(model, train_loader, val_loader)