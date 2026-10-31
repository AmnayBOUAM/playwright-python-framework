import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

SAUCEDEMO_URL = os.getenv("SAUCEDEMO_URL", "https://www.saucedemo.com")
APP_USERNAME = os.getenv("APP_USERNAME", "standard_user")
APP_PASSWORD = os.getenv("APP_PASSWORD", "secret_sauce")

# saucedemo utilise data-test au lieu de data-testid
TEST_ID_ATTRIBUTE = "data-test"
STORAGE_STATE = ROOT_DIR / ".auth" / "user.json"
DEFAULT_TIMEOUT_MS = 10_000
DATA_DIR = ROOT_DIR / "data"
REPORTS_DIR = ROOT_DIR / "reports"
