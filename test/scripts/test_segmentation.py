from pathlib import Path

import pytest

from urb3d.pipeline.utils import run_script


@pytest.fixture
def ply_model_path():
    return Path('../data/very_small_truck.ply')

@pytest.fixture
def ckpt_model_path():
    return Path('data/pointnet-weighted_loss-epoch=31-val_loss=1.99-train_loss=1.35.ckpt')

@pytest.fixture
def segmented_path(tmp_path):
    return tmp_path / 'segmented.ply'

def test_segmentation(ply_model_path, ckpt_model_path, segmented_path):
    run_script("segmentation.py", "--ckpt", str(ckpt_model_path),
               "--input", str(ply_model_path), "--output", str(segmented_path))

    assert segmented_path.exists()
    assert segmented_path.is_file()
    assert segmented_path.stat().st_size > 0
