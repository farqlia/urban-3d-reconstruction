from lib2to3.pygram import python_grammar_no_print_and_exec_statement
from pathlib import Path

import pytest
from pyntcloud import PyntCloud

from src.urb3d.pipeline.utils import run_script


@pytest.fixture
def ply_path():
    return Path('data/birmingham_block_6_subsampled_test.ply')

@pytest.fixture
def pt_path():
    return Path('data/gerrard-hall/model.pt')

@pytest.fixture
def filtered_ply_path(tmp_path):
    return tmp_path / "filtered_path.ply"

@pytest.fixture
def run_filtering(ply_path, filtered_ply_path):
    run_script("statistical_pcd_filtering.py", "--input", str(ply_path),
               "--output", str(filtered_ply_path), '--method', 'iqr')

@pytest.fixture
def test_filtered_pcd_file_exists(run_filtering, filtered_ply_path):
    assert filtered_ply_path.exists()

@pytest.fixture
def test_filtering_works_correctly(run_filtering, ply_path, filtered_ply_path):
    cloud = PyntCloud.from_file(str(ply_path))
    filtered_cloud = PyntCloud.from_file(str(filtered_ply_path))
    assert len(filtered_cloud.points) <= len(cloud.points)

def test_error_on_wrong_type(pt_path, filtered_ply_path):
    with pytest.raises(RuntimeError) as e:
        run_script("statistical_pcd_filtering.py", "--input", str(pt_path),
                   "--output", str(filtered_ply_path), '--method', 'iqr')
    assert 'Failed to execute statistical_pcd_filtering.py)' in str(e.value)