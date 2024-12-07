from pathlib import Path

import pytest
from pyntcloud import PyntCloud

from src.urb3d.pipeline.utils import run_script

@pytest.fixture
def colored_ply_path(tmp_path):
    return tmp_path / 'colored.ply'

@pytest.fixture
def pt_path():
    return Path('data/gerrard-hall/model.pt')

@pytest.fixture()
def color_cloud(pt_path, colored_ply_path):
    run_script("torch_model_to_ply.py", "--input", str(pt_path),
               "--output", str(colored_ply_path))
    run_script("add_rgb_color.py", "--input", str(colored_ply_path))


@pytest.fixture
def test_colored_file_exists(color_cloud, colored_ply_path):
    assert colored_ply_path.exists()

@pytest.fixture
def test_cloud_contains_color_fields(color_cloud, colored_ply_path):
    cloud = PyntCloud.from_file(str(colored_ply_path))
    assert 'red' in cloud.points.columns
    assert 'green' in cloud.points.columns
    assert 'blue' in cloud.points.columns