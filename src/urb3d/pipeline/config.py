from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[3]
INPUT_DATA_FOLDER = BASE_DIR / os.getenv("INPUT_DATA_FOLDER")
DATA_FOLDER = BASE_DIR / os.getenv("DATA_FOLDER")
SCRIPTS_DIR = BASE_DIR / "scripts"
COLMAP_RECONSTRUCTION_DIR = BASE_DIR / os.getenv("RECONSTRUCTION_FOLDER")
GAUSSIAN_MODEL_PLY = BASE_DIR / os.getenv("GAUSSIAN_MODEL_PLY_PATH")
CKPTS_PATH = BASE_DIR / os.getenv("CKPTS_PATH")
SEGMENTATION_MODEL_CKPT_PATH = BASE_DIR / os.getenv("SEGMENTATION_MODEL_CKPT_PATH")
SEGMENTED_PLY_PATH = BASE_DIR / os.getenv("SEGMENTED_PLY_PATH")
COLORED_SEGMENTED_PLY_PATH = BASE_DIR / os.getenv("COLORED_SEGMENTED_PLY_PATH")