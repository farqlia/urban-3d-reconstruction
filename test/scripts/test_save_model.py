from pathlib import Path

import pytest
from src.urb3d.pipeline.utils import run_script

@pytest.fixture
def ckpts_path():
    return Path('data/gerrard-hall/ckpts')

@pytest.fixture
def pt_path(tmp_path):
    return tmp_path / 'model.ply'

def test_save_model(ckpts_path, pt_path):
    run_script("save_model.py", "--ckpts", str(ckpts_path),
               "--output", str(pt_path))

    assert pt_path.exists()