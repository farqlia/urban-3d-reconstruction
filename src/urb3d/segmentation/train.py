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

subsample_size = 1024
batch_size = 32
max_epochs = 500
train_set_path = Path('data/birmingham_blocks/block_6_train')
val_set_path = Path('data/birmingham_blocks/block_7_train')
file_cloud_path = Path('data/birmingham_blocks/birmingham_block_6.ply')

pt = PyntCloud.from_file(str(file_cloud_path))
classes_count = pd.DataFrame(pt.points['class']).value_counts().reset_index().set_index('class')
classes_df = pd.DataFrame.from_dict({'class': np.arange(13), 'name': ['ground', 'vegetation', 'building', 'wall', 'bridge',
    'parking', 'rail', 'traffic road', 'street furniture', 'car', 'footpath', 'bike', 'water']}).set_index('class')
counts = classes_df.join(classes_count).fillna(0)
counts['weight'] = (1 / counts['count'] ** 0.5).replace([np.inf, -np.inf], 1e-6)



training_dataset = ChunkedPointCloudDataset(train_set_path, subsample_size=subsample_size)

train_loader = DataLoader(training_dataset, batch_size=batch_size, shuffle=True)

validation_dataset = ChunkedPointCloudDataset(val_set_path, subsample_size=subsample_size)
val_loader = DataLoader(validation_dataset, batch_size=batch_size)

model = PointNetSegmentor(classes=len(classes_df), weights=torch.Tensor(counts['weight']))
experiment_name = "pointnet_weighted_isns_6_7"
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
                         default_root_dir=checkpoint_dir, callbacks=[checkpoint_callback], logger=logger,
                         log_every_n_steps=1)

    trainer.fit(model, train_loader, val_loader)