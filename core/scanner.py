from __future__ import annotations

import json
from pathlib import Path

from core.steam import find_steam_install, get_library_folders
from models.game import Game

SKIP = {"Steamworks Common Redistributables"}

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CACHE_FILE = DATA_DIR / "games.json"


def _parse_appmanifest(path: Path) -> Game | None:
    try:
        import vdf

        with open(path, "r", encoding="utf-8") as f:
            data = vdf.load(f)

        app_state = data.get("AppState", {})
        name = app_state.get("name", "")
        appid = app_state.get("appid", "")

        if not name or not appid:
            return None
        if name in SKIP:
            return None
        if name.startswith("Proton"):
            return None
        if name.startswith("Steam Linux Runtime"):
            return None

        return Game(name=name, appid=appid, library="")
    except Exception:
        return None


def scan_games() -> list[Game]:
    steam_path = find_steam_install()
    if steam_path is None:
        return []

    libraries = get_library_folders(steam_path)
    games: list[Game] = []

    for library in libraries:
        steamapps = library / "steamapps"
        if not steamapps.exists():
            continue

        for manifest in steamapps.glob("appmanifest_*.acf"):
            game = _parse_appmanifest(manifest)
            if game is not None:
                game.library = str(library)
                games.append(game)

    games.sort(key=lambda g: g.name.lower())
    return games


def load_cache() -> list[Game] | None:
    if not CACHE_FILE.exists():
        return None
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Game.from_dict(entry) for entry in data]
    except (json.JSONDecodeError, KeyError):
        return None


def save_cache(games: list[Game]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump([g.to_dict() for g in games], f, indent=2)


def get_games() -> list[Game]:
    games = scan_games()
    if games:
        save_cache(games)
    else:
        cached = load_cache()
        if cached:
            return cached
    return games
