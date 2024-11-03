from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[2] 
INPUT_DATA_FOLDER = BASE_DIR / os.getenv("INPUT_DATA_FOLDER")
DATA_FOLDER = BASE_DIR / os.getenv("DATA_FOLDER")
SCRIPTS_DIR = BASE_DIR / "scripts"
COLMAP_RECONSTRUCTION_DIR = BASE_DIR / os.getenv("RECONSTRUCTION_FOLDER")
GAUSSIAN_MODEL_PT = BASE_DIR / os.getenv("GAUSSIAN_MODEL_PT_PATH")
GAUSSIAN_MODEL_PLY = BASE_DIR / os.getenv("GAUSSIAN_MODEL_PLY_PATH")