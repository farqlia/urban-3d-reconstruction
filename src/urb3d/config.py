from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[2] 
INPUT_DATA_FOLDER = BASE_DIR / os.getenv("INPUT_DATA_FOLDER")
DATA_FOLDER = BASE_DIR / os.getenv("DATA_FOLDER")
SCRIPTS_DIR = BASE_DIR / "scripts"
SCENE_FOLDER = BASE_DIR / os.getenv("SCENE_FOLDER")
GAUSSIAN_MODEL_PT = BASE_DIR / os.getenv("GAUSSIAN_MODEL_PT_PATH")
GAUSSIAN_MODEL_PLY = BASE_DIR / os.getenv("GAUSSIAN_MODEL_PLY_PATH")
GAUSSIAN_MODEL_SEG_PLY = BASE_DIR / os.getenv("GAUSSIAN_MODEL_SEG_PLY_PATH")
COLMAP_ENV = str(Path(os.getenv("COLMAP_ENV")))  # pycolmap must be downloaded with conda to use GPU
CHECKPOINT_DIR = BASE_DIR / os.getenv("CHECKPOINT_DIR")