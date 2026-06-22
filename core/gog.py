from __future__ import annotations

import os
import sqlite3
from pathlib import Path

from models.game import Game

PROGRAM_DATA = Path(os.environ.get("PROGRAMDATA", r"C:\ProgramData"))
GOG_DB = PROGRAM_DATA / "GOG.com" / "Galaxy" / "storage" / "galaxy-2.0.db"


def scan_gog_games(db_path_override: str = "") -> list[Game]:
    games: list[Game] = []

    db_path = Path(db_path_override) if db_path_override else GOG_DB

    if not db_path.exists():
        return games

    try:
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, title, installationPath
            FROM Game
            WHERE installationPath IS NOT NULL
              AND installationPath != ''
            """
        )
        for row in cursor.fetchall():
            game_id, title, install_path = row
            if not title or not install_path:
                continue

            exe_path = ""
            install_dir = Path(install_path)
            if install_dir.exists():
                exes = sorted(install_dir.glob("*.exe"))
                if exes:
                    exe_path = str(exes[0])

            games.append(
                Game(
                    name=title,
                    appid=str(game_id),
                    library=install_path,
                    launcher="gog",
                    executable=exe_path,
                )
            )
        conn.close()
    except sqlite3.Error:
        pass

    games.sort(key=lambda g: g.name.lower())
    return games
