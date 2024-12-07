from pathlib import Path

import pytest
import torch

from src.urb3d.pipeline.utils import run_script


@pytest.fixture
def reconstruction_path():
    return Path('data/gerrard-hall/')

@pytest.fixture
def corrupted_reconstruction_path():
    return Path('data/gerrard-hall-corrupted/')

@pytest.fixture
def result_path(tmp_path):
    return tmp_path / 'gs_reconstruction'

@pytest.fixture
def ply_path(tmp_path):
    return tmp_path / 'model.ply'

@pytest.fixture
def run_simple_trainer(reconstruction_path, result_path):
    run_script("simple_trainer.py", "--data_dir", str(reconstruction_path),  # ?
               "--result_dir", str(result_path), "--max_steps", "50", "--delta_steps", "50")

@pytest.mark.skip(reason="Long execution time")
def test_simple_trainer_files_exist(run_simple_trainer, result_path):
    assert result_path.exists()
    assert (result_path / 'ckpts').exists()
    assert (result_path / 'tb').exists()
    assert (result_path / 'stats').exists()

@pytest.mark.skip(reason="Long execution time")
def test_simple_trainer_pt_file_is_correct(run_simple_trainer, result_path, ply_path):
    run_script("save_model.py", "--ckpts", str(result_path / 'ckpts'),
               "--output", str(ply_path))

    model = torch.load(str(result_path / 'model.pt'), map_location="cpu", weights_only=True)
    assert 'splats' in model

def test_training_fails_on_incomplete_input(run_simple_trainer, corrupted_reconstruction_path, result_path):
    with pytest.raises(RuntimeError) as e:
        run_script("simple_trainer.py", "--data_dir", str(corrupted_reconstruction_path),  # ?
                   "--result_dir", str(result_path), "--max_steps", "50", "--delta_steps", "50")
    assert 'Failed to execute simple_trainer.py)' in str(e.value)