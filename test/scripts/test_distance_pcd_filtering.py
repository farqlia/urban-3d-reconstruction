from pathlib import Path

import pytest
from src.urb3d.pipeline.utils import run_script


@pytest.fixture
def ply_path():
    return Path("data/very_small_truck.ply")

@pytest.fixture
def filtered_ply_path(tmp_path):
    return tmp_path / "filtered_path.ply"

def test_distance_pcd_filtering(ply_path, filtered_ply_path):
    run_script("distance_pcd_filtering.py", "--input", str(ply_path),
               "--output", str(filtered_ply_path))

    assert filtered_ply_path.exists()
