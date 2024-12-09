from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(os.path.dirname(os.path.abspath(sys.argv[0]))).resolve().parents[1]
INPUT_DATA_FOLDER = BASE_DIR / os.getenv("INPUT_DATA_FOLDER")
DATA_FOLDER = BASE_DIR / os.getenv("DATA_FOLDER")
SCRIPTS_DIR = BASE_DIR / "scripts"
COLMAP_RECONSTRUCTION_DIR = BASE_DIR / os.getenv("RECONSTRUCTION_FOLDER")
GAUSSIAN_MODEL_PLY = BASE_DIR / os.getenv("GAUSSIAN_MODEL_PLY_PATH")
GAUSSIAN_MODEL_PT = BASE_DIR / os.getenv("GAUSSIAN_MODEL_PT_PATH")
CKPTS_PATH = BASE_DIR / os.getenv("CKPTS_PATH")
SEGMENTATION_MODEL_CKPT_PATH = BASE_DIR / os.getenv("SEGMENTATION_MODEL_CKPT_PATH")
CHUNKED_MODEL_FOLDER = BASE_DIR / os.getenv("CHUNKED_MODEL_FOLDER")
SEGMENTED_PLY_PATH = BASE_DIR / os.getenv("SEGMENTED_PLY_PATH")
COLORED_SEGMENTED_PLY_PATH = BASE_DIR / os.getenv("COLORED_SEGMENTED_PLY_PATH")
PNG_RENDERS_FOLDER = BASE_DIR / os.getenv("DATA_FOLDER") / "renders"
COLMAP_ENV = os.getenv("COLMAP_ENV")
POINT_CLOUD_SPARSE = BASE_DIR / os.getenv("POINT_CLOUD_SPARSE")
FILTERED_PRESEG_MODEL = BASE_DIR / os.getenv("DATA_FOLDER") / "filtered_model.ply" # "data/input/birmingham_block_6_subsampled.ply"