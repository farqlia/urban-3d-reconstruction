from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[2]
QML_IMPORT = BASE_DIR / os.getenv("QML_IMPORT")
HEADER_FILE = BASE_DIR / os.getenv("HEADER_FILE")
LEFT_PANE_FILE = BASE_DIR / os.getenv("LEFT_PANE_FILE")
FOOTER_FILE = BASE_DIR / os.getenv("FOOTER_FILE")