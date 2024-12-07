from pathlib import Path

import pytest
from pyntcloud import PyntCloud

from src.urb3d.pipeline.utils import run_script


@pytest.fixture
def ply_model_path():
    return Path('data/birmingham_block_6_subsampled_test.ply')

@pytest.fixture
def corrupted_ply_model_path(tmp_path):
    original_cloud = PyntCloud.from_file('data/birmingham_block_6_subsampled_test.ply')
    original_cloud.points.drop(['x', 'y', 'z'], axis=1, inplace=True)
    original_cloud.to_file(str(tmp_path / 'corrupted.ply'))
    return tmp_path / 'corrupted.ply'

@pytest.fixture
def ckpt_model_path():
    return Path('data/pointnet-weighted_loss-epoch=31-val_loss=1.99-train_loss=1.35.ckpt')

@pytest.fixture
def segmented_path(tmp_path):
    return tmp_path / 'segmented.ply'

@pytest.fixture
def run_segmentation(ply_model_path, ckpt_model_path, segmented_path):
    run_script("segmentation.py", "--ckpt", str(ckpt_model_path),
               "--input", str(ply_model_path), "--output", str(segmented_path))

def test_segmentation_files_exist(run_segmentation, segmented_path):
    assert segmented_path.exists()
    assert segmented_path.is_file()
    assert segmented_path.stat().st_size > 0

def test_segmentation_class_is_added(run_segmentation, segmented_path):
    cloud = PyntCloud.from_file(str(segmented_path))
    assert 'class_label' in cloud.points.columns

def test_segmentation_classes_are_in_range(run_segmentation, segmented_path):
    cloud = PyntCloud.from_file(str(segmented_path))
    classes = cloud.points['class_label'].unique()
    assert max(classes) <= 12
    assert min(classes) >= 0

def test_segmentation_fails_on_corrupted_input(corrupted_ply_model_path, ckpt_model_path, segmented_path):
    with pytest.raises(RuntimeError) as e:
        run_script("segmentation.py", "--ckpt", str(ckpt_model_path),
                   "--input", str(corrupted_ply_model_path), "--output", str(segmented_path))
    assert 'Failed to execute segmentation.py)' in str(e.value)