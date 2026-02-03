import json
import os
from pathlib import Path

from backend.utils.s3_json_store import load_json, save_json
from backend.models.tricount import Tricount
from backend.utils.utils import tricount_from_dict, tricount_to_dict

DATA_FILE = Path("data/tricounts.json")
STORAGE_BACKEND = os.environ.get("STORAGE_BACKEND", "local").lower()
S3_TRICOUNTS_KEY = "tricounts.json"


def save_tricounts(tricounts):
    if STORAGE_BACKEND == "s3":
        save_json(S3_TRICOUNTS_KEY, tricounts)
        return

    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(tricounts, f, indent=2)


def load_tricounts():
    if STORAGE_BACKEND == "s3":
        return load_json(S3_TRICOUNTS_KEY, default=[])

    if not DATA_FILE.exists() or DATA_FILE.stat().st_size == 0:
        return []

    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError, TypeError):
        return []
