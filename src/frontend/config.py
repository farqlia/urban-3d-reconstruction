from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[2]
QML_IMPORT = BASE_DIR / os.getenv("QML_IMPORT")
HEADER_FILE = BASE_DIR / os.getenv("HEADER_FILE")
LEFT_PANE_FILE = BASE_DIR / os.getenv("LEFT_PANE_FILE")
FOOTER_FILE = BASE_DIR / os.getenv("FOOTER_FILE")
LOADING_WINDOW_FILE = BASE_DIR / os.getenv("LOADING_WINDOW_FILE")
SUCC_WINDOW_FILE = BASE_DIR / os.getenv("SUCC_WINDOW_FILE")
FAIL_WINDOW_FILE = BASE_DIR / os.getenv("FAIL_WINDOW_FILE")
SETTINGS_WINDOW = BASE_DIR / os.getenv("SETTINGS_WINDOW")
RIGHT_PANE_LT_FILE = BASE_DIR / os.getenv("RIGHT_PANE_LT_FILE")
RIGHT_PANE_RT_FILE = BASE_DIR / os.getenv("RIGHT_PANE_RT_FILE")
RIGHT_PANE_LB_FILE = BASE_DIR / os.getenv("RIGHT_PANE_LB_FILE")
RIGHT_PANE_RB_FILE = BASE_DIR / os.getenv("RIGHT_PANE_RB_FILE")