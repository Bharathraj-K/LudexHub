"""Centralized path resolution for both dev and PyInstaller frozen builds.

When frozen by PyInstaller:
  - sys._MEIPASS = temp extraction dir (bundled read-only files: fonts, tray.ico)
  - sys.executable.parent = next to .exe (writable runtime data: settings, games)
"""

from __future__ import annotations

import sys
from pathlib import Path


def get_bundle_dir() -> Path:
    """Read-only bundled files (fonts, tray.ico). Points to _MEIPASS when frozen."""
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent.parent


def get_app_root() -> Path:
    """Writable runtime data. Points next to .exe when frozen."""
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent


def get_data_dir() -> Path:
    return get_app_root() / "data"


def get_assets_dir() -> Path:
    return get_bundle_dir() / "assets"
