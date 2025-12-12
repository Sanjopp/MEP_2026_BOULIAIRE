import json
import os
from dataclasses import asdict

from backend.models.auth_user import AuthUser

DATA_FILE = "data/users.json"


def load_users():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            return [AuthUser(**u) for u in data]
    except (json.JSONDecodeError, FileNotFoundError, TypeError):
        return []


def save_users(users):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump([asdict(u) for u in users], f, indent=2)
