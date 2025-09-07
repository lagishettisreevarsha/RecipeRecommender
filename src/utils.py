import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
EXTERNAL_DIR = DATA_DIR / "external"
DB_PATH = DATA_DIR / "recipes.db"
RAW_JSON = RAW_DIR / "recipes.json"

# Ensure folders exist
for p in [DATA_DIR, RAW_DIR, PROCESSED_DIR, EXTERNAL_DIR]:
    p.mkdir(parents=True, exist_ok=True)

# Simple constants
DEFAULT_TOP_N = 5

