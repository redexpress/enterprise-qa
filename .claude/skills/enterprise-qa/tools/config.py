import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]

DB_PATH = os.environ.get("ENTERPRISE_QA_DB_PATH") or str(ROOT / "enterprise.db")
KB_PATH = os.environ.get("ENTERPRISE_QA_KB_PATH") or str(ROOT / "knowledge")
