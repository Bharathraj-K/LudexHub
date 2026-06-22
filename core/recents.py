from __future__ import annotations

import json
import time
from pathlib import Path

from core.paths import get_data_dir

DATA_DIR = get_data_dir()
RECENTS_FILE = DATA_DIR / "recents.json"
MAX_RECENTS = 10


def load_recents() -> list[dict]:
    if not RECENTS_FILE.exists():
        return []
    try:
        with open(RECENTS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except (json.JSONDecodeError, OSError):
        return []


def save_recents(recents: list[dict]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(RECENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(recents, f, indent=2)


def record_launch(appid: str) -> list[dict]:
    recents = load_recents()
    recents = [r for r in recents if r["appid"] != appid]
    recents.insert(0, {"appid": appid, "timestamp": int(time.time())})
    recents = recents[:MAX_RECENTS]
    save_recents(recents)
    return recents


def get_recent_appids() -> list[str]:
    recents = load_recents()
    return [r["appid"] for r in recents]
