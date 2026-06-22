"""Centralized path resolution for both dev and PyInstaller frozen builds."""

from __future__ import annotations

import sys
from pathlib import Path


def get_app_root() -> Path:
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent


def get_data_dir() -> Path:
    return get_app_root() / "data"


def get_assets_dir() -> Path:
    return get_app_root() / "assets"
