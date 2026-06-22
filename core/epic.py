from __future__ import annotations

import json
import os
from pathlib import Path

from models.game import Game

PROGRAM_DATA = Path(os.environ.get("PROGRAMDATA", r"C:\ProgramData"))
MANIFEST_DIR = PROGRAM_DATA / "Epic" / "EpicGamesLauncher" / "Data" / "Manifests"
LAUNCHER_DAT = PROGRAM_DATA / "Epic" / "UnrealEngineLauncher" / "LauncherInstalled.dat"

SKIP_EPIC = {"Fortnite", "Unreal Editor"}


def scan_epic_games(manifest_dir_override: str = "") -> list[Game]:
    games: list[Game] = []

    if manifest_dir_override:
        manifest_dir = Path(manifest_dir_override)
        launcher_dat = manifest_dir.parent / "LauncherInstalled.dat"
    else:
        manifest_dir = MANIFEST_DIR
        launcher_dat = LAUNCHER_DAT

    manifest_items: dict[str, dict] = {}
    if manifest_dir.exists():
        for item_file in manifest_dir.glob("*.item"):
            try:
                with open(item_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                app_name = data.get("AppName", "")
                if app_name:
                    manifest_items[app_name] = data
            except (json.JSONDecodeError, OSError):
                continue

    if not launcher_dat.exists():
        return games

    try:
        with open(launcher_dat, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return games

    for entry in data.get("InstallationList", []):
        app_name = entry.get("AppName", "")
        install_loc = entry.get("InstallLocation", "")

        if not app_name or not install_loc:
            continue

        display_name = app_name
        launch_exe = ""
        manifest = manifest_items.get(app_name, {})
        if manifest:
            display_name = manifest.get("AppDisplayName", app_name) or app_name
            launch_exe = manifest.get("LaunchExecutable", "")

        if display_name in SKIP_EPIC:
            continue

        exe_path = ""
        if launch_exe and install_loc:
            full = Path(install_loc) / launch_exe
            if full.exists():
                exe_path = str(full)

        games.append(
            Game(
                name=display_name,
                appid=app_name,
                library=install_loc,
                launcher="epic",
                executable=exe_path,
            )
        )

    games.sort(key=lambda g: g.name.lower())
    return games
