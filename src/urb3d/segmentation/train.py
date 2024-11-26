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

from urb3d.segmentation.dataset import PointSampler, PointCloudSegmentationDataset
from urb3d.segmentation.segmentor import PointNetSegmentor
from urb3d.segmentation.pointnet2 import PointNetPP

subsample_size = 1024
batch_size = 64
max_epochs = 2


file_cloud = 'data/birmingham_blocks/birmingham_block_7_subsampled_train.ply'
pt = PyntCloud.from_file(file_cloud)
classes_count = pd.DataFrame(pt.points['scalar_class']).value_counts().reset_index().set_index('scalar_class')
classes_df = pd.DataFrame.from_dict({'scalar_class': np.arange(13), 'name': ['ground', 'vegetation', 'building', 'wall', 'bridge',
    'parking', 'rail', 'traffic road', 'street furniture', 'car', 'footpath', 'bike', 'water']}).set_index('scalar_class')
counts = classes_df.join(classes_count).fillna(0)
counts['weight'] = (1 / counts['count']).replace([np.inf, -np.inf], 1e-6)



training_dataset = PointCloudSegmentationDataset('data/birmingham_blocks/birmingham_block_7_subsampled_train.ply',
                                     subsample_size=subsample_size, point_sampler=PointSampler(subsample_size))
train_loader = DataLoader(training_dataset, batch_size=batch_size, shuffle=True)

validation_dataset = PointCloudSegmentationDataset('data/birmingham_blocks/birmingham_block_7_subsampled_test.ply',
                                     subsample_size=subsample_size, point_sampler=PointSampler(subsample_size))
val_loader = DataLoader(validation_dataset, batch_size=batch_size, )

model = PointNetSegmentor(classes=len(classes_df), weights=torch.Tensor(counts['weight']))
experiment_name = "pointnet_weighted"
checkpoint_dir = Path(f"models/{experiment_name}")
logger = TensorBoardLogger(save_dir=f"models/{experiment_name}/tlogs", name=experiment_name)


checkpoint_callback = pl.callbacks.ModelCheckpoint(dirpath=checkpoint_dir / 'best_results', filename='{epoch}-{val_loss:.2f}-{train_loss:.2f}',
                                      monitor='val_loss', save_last=True)
#early_stopping = pl.callbacks.EarlyStopping(monitor='val_loss', verbose=True)

trainer = pl.Trainer(max_epochs=max_epochs, fast_dev_run=False,
                     default_root_dir=checkpoint_dir, callbacks=[checkpoint_callback], logger=logger, log_every_n_steps=1)

trainer.fit(model, train_loader, val_loader)


if __name__=="__main__":
    # usage:
    # python scripts\statistical_pcd_filtering.py --input "path_to_file.ply" --method iqr --output "filtered_output.ply"
    # python scripts\statistical_pcd_filtering.py --input "path_to_file.ply" --method z-score --output "filtered_output.ply" --threshold 2
    # higher alpha and higher threshold = more inliers

    parser = argparse.ArgumentParser(description="Train new model.")

    parser.add_argument('--input', type=str, required=True, help='Path to the point cloud file')