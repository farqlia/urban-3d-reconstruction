from pathlib import Path

import pytest
from src.urb3d.pipeline.utils import run_script

@pytest.fixture
def ckpts_path():
    return Path('data/gerrard-hall/ckpts')

@pytest.fixture
def ply_path(tmp_path):
    return tmp_path / 'model.ply'

def test_save_model(ckpts_path, ply_path):
    run_script("save_model.py", "--ckpts", str(ckpts_path),
               "--output", str(ply_path))

    assert ply_path.exists()

def test_fail_on_wrong_path_name(tmp_path, ply_path):
    with pytest.raises(RuntimeError) as e:
        run_script("save_model.py", "--ckpts", str(tmp_path / 'checkpoints'),
                   "--output", str(ply_path))
    assert 'Failed to execute save_model.py)' in str(e.value)