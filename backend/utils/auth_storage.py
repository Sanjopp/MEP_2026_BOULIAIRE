import json
import os
from dataclasses import asdict
from pathlib import Path

from backend.models.auth_user import AuthUser
from backend.utils.s3_json_store import load_json, save_json


DATA_FILE = Path("data/users.json")
STORAGE_BACKEND = os.environ.get("STORAGE_BACKEND", "local").lower()
S3_USERS_KEY = "users.json"


def load_users() -> list[AuthUser]:
    if STORAGE_BACKEND == "s3":
        data = load_json(S3_USERS_KEY, default=[])
        try:
            return [AuthUser(**u) for u in data]
        except TypeError:
            return []
    if not DATA_FILE.exists() or DATA_FILE.stat().st_size == 0:
        return []
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            return [AuthUser(**u) for u in data]
    except (json.JSONDecodeError, FileNotFoundError, TypeError):
        return []


def save_users(users: list[AuthUser]) -> None:
    if STORAGE_BACKEND == "s3":
        save_json(S3_USERS_KEY, [asdict(u) for u in users])
        return

    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump([asdict(u) for u in users], f, indent=2)
