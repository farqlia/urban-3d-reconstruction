from pathlib import Path

import pytest
from src.urb3d.pipeline.utils import run_script


@pytest.fixture
def reconstruction_path():
    return Path('data/gerrard-hall/')

@pytest.fixture
def result_path(tmp_path):
    return tmp_path / 'gs_reconstruction'

def test_simple_trainer(reconstruction_path, result_path):
    run_script("simple_trainer.py", "--data_dir", str(reconstruction_path),  # ?
               "--result_dir", str(result_path), "--max_steps", "50", "--delta_steps", "50")

    assert result_path.exists()
    assert (result_path / 'ckpts').exists()
    assert (result_path / 'tb').exists()
    assert (result_path / 'stats').exists()