from __future__ import annotations

import json
from pathlib import Path

from core.paths import get_data_dir

DATA_DIR = get_data_dir()
FAVORITES_FILE = DATA_DIR / "favorites.json"


def load_favorites() -> set[str]:
    if not FAVORITES_FILE.exists():
        return set()
    try:
        with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return set(data)
    except (json.JSONDecodeError, OSError):
        return set()


def save_favorites(favs: set[str]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
        json.dump(sorted(favs), f, indent=2)


def toggle_favorite(appid: str) -> bool:
    favs = load_favorites()
    if appid in favs:
        favs.discard(appid)
    else:
        favs.add(appid)
    save_favorites(favs)
    return appid in favs
