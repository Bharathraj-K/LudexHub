from __future__ import annotations

import winreg
from pathlib import Path


def find_steam_install() -> Path | None:
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Valve\Steam",
        )
        steam_path, _ = winreg.QueryValueEx(key, "SteamPath")
        winreg.CloseKey(key)
        path = Path(steam_path)
        if path.exists():
            return path
    except (OSError, FileNotFoundError):
        pass

    default = Path(r"C:\Program Files (x86)\Steam")
    if default.exists():
        return default

    return None


def get_library_folders(steam_path: Path) -> list[Path]:
    candidates = [
        steam_path / "config" / "libraryfolders.vdf",
        steam_path / "steamapps" / "libraryfolders.vdf",
    ]

    vdf_path = None
    for candidate in candidates:
        if candidate.exists():
            vdf_path = candidate
            break

    if vdf_path is None:
        return [steam_path]

    import vdf

    with open(vdf_path, "r", encoding="utf-8") as f:
        data = vdf.load(f)

    folders = []
    libraryfolders = data.get("libraryfolders", {})
    for _key, entry in libraryfolders.items():
        raw_path = entry.get("path", "")
        if raw_path:
            p = Path(raw_path)
            if p.exists():
                folders.append(p)

    if not folders:
        folders.append(steam_path)

    return folders
