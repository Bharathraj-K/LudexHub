from __future__ import annotations

import json
from pathlib import Path

from core.paths import get_bundle_dir, get_data_dir

DATA_DIR = get_data_dir()
SETTINGS_FILE = DATA_DIR / "settings.json"

DEFAULTS = {
    "hotkey": "alt+space",
    "tray_icon": str(get_bundle_dir() / "data" / "icons" / "tray.ico"),
    "theme": "cyberpunk",
    "font_family": "Orbitron",
    "position": "center",
    "scan_on_startup": True,
    "steam_path": "",
    "epic_path": "",
    "gog_path": "",
    "start_with_windows": False,  # STARTUP FEATURE: toggled via core/startup.py
}


def load_settings() -> dict:
    if SETTINGS_FILE.exists():
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                user = json.load(f)
            merged = {**DEFAULTS, **user}
            return merged
        except (json.JSONDecodeError, OSError):
            pass
    return dict(DEFAULTS)


def save_settings(settings: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)
