import pytest
from pathlib import Path

from src.urb3d.pipeline.config import COLMAP_ENV
from src.urb3d.pipeline.utils import run_script_with_env


@pytest.fixture(scope='session')
def images_path():
    return Path('data/gerrard-hall/images')

@pytest.fixture
def reconstruction_path(tmp_path):
    return tmp_path / 'reconstruction'

@pytest.mark.skip(reason="Long execution time")
def test_colmap_reconstruction_files_exist(images_path, reconstruction_path):
    run_script_with_env(COLMAP_ENV, "colmap_reconstruction.py", "--input", str(images_path),
                        "--output", str(reconstruction_path))

    assert images_path.exists()
    assert reconstruction_path.exists()
    assert (reconstruction_path / '0').exists()
    assert (reconstruction_path / '0/points3D.bin').exists()
    assert (reconstruction_path / '0/cameras.bin').exists()
    assert (reconstruction_path / '0/images.bin').exists()

